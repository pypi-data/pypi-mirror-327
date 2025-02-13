from collections import defaultdict
import json
from typing import List, NamedTuple, Optional

import torch
from torch.utils.data import DataLoader
from transformers import (
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    AutoConfig,
    AutoTokenizer,
    LogitsProcessorList,
    GenerationConfig,
)

from quotect.common.constants import MARK_SPECIAL_IDS, SPECIAL_IDS
from quotect.data.data import (
    ConstrainedDataCollator,
    QuoteDataset,
    parse_int_output_tokens,
    parse_short_target_tokens,
)
from quotect.data.preprocess_data import get_quote_document
from quotect.model.logits_processor import IntProcessor, ShortSeqProcessor
from quotect.data.convert_quotes import convert_to_quote_json
from quotect.model.model import ConstrainedT5

max_len = 4096


def _text2doc(inp, filename, text):
    sent_map = {s: i for i, s in enumerate(inp.sents)}
    doc = {"annotations": [], "documentName": filename, "originalText": text}
    doc["sentences"] = [
        {
            "begin": s.start,
            "charBegin": s.start_char,
            "charEnd": s.end_char,
            "end": s.end,
            "id": i,
            "text": s.text,
            "tokenIds": [t.i for t in s],
            "tokens": [t.text for t in s],
        }
        for i, s in enumerate(inp.sents)
    ]
    doc["tokens"] = [
        {
            "charBegin": t.idx,
            "charEnd": t.idx + len(t),
            "id": t.i,
            "sentence": sent_map[t.sent],
            "text": t.text,
            "word": t.i - t.sent.start,
        }
        for t in inp
    ]
    return doc


class Token(NamedTuple):
    start: int
    end: int
    sent: int
    text: str


class Span(NamedTuple):
    start: int
    end: int
    text: str


class QuoteInput(NamedTuple):
    name: int
    tokens: List[Token]
    sentences: List[Span]
    text: str


def _input2doc(input: QuoteInput):
    doc = {
        "documentName": input.name,
        "annotations": [],
        "originalText": input.text,
    }
    doc["sentences"] = [
        {
            "begin": s.start,
            "charBegin": input.tokens[s.start].start,
            "charEnd": input.tokens[s.end].end,
            "end": s.end,
            "id": i,
            "text": s.text,
            "tokenIds": list(range(s.start, s.end+1)),
            "tokens": [input.tokens[t].text for t in range(s.start, s.end+1)],
        }
        for i, s in enumerate(input.sentences)
    ]
    doc["tokens"] = [
        {
            "charBegin": t.start,
            "charEnd": t.end,
            "id": i,
            "sentence": t.sent,
            "text": t.text,
            "word": i - input.sentences[t.sent].start,
        }
        for i, t in enumerate(input.tokens)
    ]
    return doc


class Quotect:
    def __init__(
        self,
        model_name_or_path: str,
        device: str = None,
        generation_max_length=max_len,
        generation_num_beams=1,
    ):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = self._get_tokenizer(model_name_or_path)
        self.model = self._get_model(model_name_or_path, device)
        self.gen_conf = GenerationConfig(
            max_length=generation_max_length,
            num_beams=generation_num_beams,
        )
        self.is_full_copy = isinstance(self.model, ConstrainedT5)
        print("model is on device", self.model.device)
        if self.is_full_copy:
            self.collator = ConstrainedDataCollator(self.tokenizer, model=self.model)
        else:
            self.collator = DataCollatorForSeq2Seq(self.tokenizer, model=self.model)
        self.nlp = None

    def predict(self, inputs: List[QuoteInput]):
        input_docs = []
        docs = []
        for input in inputs:
            if len(input.sentences) == 0 or len(input.tokens) == 0:
                if self.nlp is None:
                    import spacy

                    try:
                        self.nlp = spacy.load("de_dep_news_trf")
                    except OSError:
                        print("Downloading language model for spacy")
                        from spacy.cli import download

                        download("de_dep_news_trf")
                        self.nlp = spacy.load("de_dep_news_trf")
                doc = _text2doc(self.nlp(input.text), input.name, input.text)
            else:
                doc = _input2doc(input)
            docs.append(doc)
            input_doc = get_quote_document(
                doc,
                self.tokenizer,
                segment_len=max_len,
                stride=0,
                is_train=False,
                mark_sentence=True,
            )
            input_docs.extend(input_doc)

        dataset = QuoteDataset(self.tokenizer, input_docs)
        dataloader = DataLoader(dataset, batch_size=4, collate_fn=self.collator)
        i = 0
        predictions = {}
        for batch in dataloader:
            length = batch["input_ids"].shape[0]
            generated_tokens = self._generate_structured_sequence(batch)
            samples = dataset.samples[i : i + length]
            prediction = self._extract_information(samples, generated_tokens)
            predictions.update(prediction)
            i += length

        outputs = convert_to_quote_json(docs, predictions, mark_sentence=True)

        return outputs

    def _generate_structured_sequence(self, inputs):
        inputs = {
            k: v.to(self.model.device) if isinstance(v, torch.Tensor) else v
            for k, v in inputs.items()
        }
        if (
            hasattr(self.model, "encoder")
            and self.model.encoder.main_input_name != self.model.main_input_name
        ):
            generation_inputs = inputs[self.model.encoder.main_input_name]
        else:
            generation_inputs = inputs[self.model.main_input_name]
        #  add our logits_processor here
        if self.is_full_copy:
            lp = IntProcessor(generation_inputs, SPECIAL_IDS, "action")
        else:
            lp = ShortSeqProcessor(generation_inputs, MARK_SPECIAL_IDS)
        generated_tokens = self.model.generate(
            generation_inputs,
            generation_config=self.gen_conf,
            logits_processor=LogitsProcessorList([lp]),
            attention_mask=inputs.get("attention_mask", None),
        )
        return generated_tokens

    def _extract_information(self, samples, generated_tokens):
        tok = self.tokenizer
        documents_to_chunk_data = defaultdict(list)
        documents_to_chunk_gold = defaultdict(list)
        predictions = {}
        golds = {}
        out_sents = []
        last_doc_id = samples[0]["doc_key"] // 1000
        for predict, sample in zip(generated_tokens, samples):
            doc_key = sample["doc_key"]
            input_ids = sample["sentence"]
            subtoken_map = sample["subtoken_map"]
            offset = sample["offset"]
            gold_data = sample["seg_clusters"]
            doc_id = doc_key // 1000
            # remove bos and padding
            idx = (predict != tok.pad_token_id).count_nonzero()
            predict_ids = predict[1 : 1 + idx].tolist()
            if self.is_full_copy == "short_seq":
                pred_data, pred_token_mentions, predict_ids = parse_int_output_tokens(
                    input_ids, predict_ids, SPECIAL_IDS, subtoken_map, tok
                )
                pred_token_mentions = [
                    (m[0] + offset, m[1] + offset) for m in pred_token_mentions
                ]
                predict_ids = [t for t in predict_ids if t != tok.pad_token_id]
                pred_tokens = tok.convert_ids_to_tokens(predict_ids)
                out_predict = {
                    "doc_key": doc_key,
                    "pred_tokens": pred_tokens,
                    "pred_text": tok.convert_tokens_to_string(pred_tokens),
                    "predict_clusters": pred_data,
                    "gold_clusters": gold_data,
                    "predict_token_mentions": pred_token_mentions,
                }
            else:
                special_ids = SPECIAL_IDS if self.is_full_copy else MARK_SPECIAL_IDS
                pred_data, aligned_input_ids, aligned_pred_ids = (
                    parse_short_target_tokens(
                        input_ids,
                        predict_ids,
                        special_ids,
                        subtoken_map,
                        tok,
                        "l",
                        not self.is_full_copy,
                    )
                )
                predict_ids = [t for t in predict_ids if t != tok.pad_token_id]
                pred_tokens = tok.convert_ids_to_tokens(predict_ids)
                out_predict = {
                    "doc_key": doc_key,
                    "pred_tokens": pred_tokens,
                    "pred_text": tok.convert_tokens_to_string(pred_tokens),
                    "pred_aligned_text": tok.convert_ids_to_tokens(aligned_pred_ids),
                    "predict_clusters": pred_data,
                    "gold_clusters": gold_data,
                    "input_aligned_text": tok.convert_ids_to_tokens(aligned_input_ids),
                }
            # list of (m1,m2)

            documents_to_chunk_data[doc_id].extend(pred_data)
            documents_to_chunk_gold[doc_id].extend(gold_data)

            out_sents.append(out_predict)
            if doc_id != last_doc_id:
                predictions[last_doc_id] = documents_to_chunk_data[last_doc_id]
                golds[last_doc_id] = documents_to_chunk_gold[last_doc_id]
            last_doc_id = doc_id
        # final one
        predictions[last_doc_id] = documents_to_chunk_data[last_doc_id]
        golds[last_doc_id] = documents_to_chunk_gold[last_doc_id]
        return predictions

    def _get_tokenizer(self, model_name_or_path: str):
        tok = AutoTokenizer.from_pretrained(
            model_name_or_path, model_max_length=max_len
        )
        return tok

    def _get_model(self, model_name_or_path: str, device: str):
        config = AutoConfig.from_pretrained(model_name_or_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path, config=config)
        model = model.to(device)
        return model


if __name__ == "__main__":
    q = Quotect(
        model_name_or_path="fynnos/quotect-mt5-base",
    )
    input1 = QuoteInput(
        name=1,
        tokens=[],
        sentences=[],
        # text="Sie sagte gestern: 'Morgen scheint die Sonne!' Jemand anderes erwiderte, dass es bestimmt regnen wird.",
        text='US-Außenministerium berichtet von BeinbruchGenf - US-Außenminister John Kerry hat sich bei einem Fahrradunfall in den französischen Alpen ein Bein gebrochen. Der 71-Jährige habe sich am Sonntag bei einer Radtour nahe Chamonix eine Fraktur des rechten Oberschenkelknochens zugezogen, sagte sein Sprecher John Kirby. Der Minister kehre nun zur Behandlung in die USA zurück und müsse daher seine Reise zum Treffen der Anti-IS-Koalition in Paris absagen.Der Zustand des Außenministers sei stabil, sagte Kirby. "Er hat zu keinem Zeitpunkt das Bewusstsein verloren." Der 71-Jährige wurde nach dem Unfall mit einem Hubschrauber in die Genfer Uniklinik gebracht. Am Montag sollte er zur weiteren Behandlung in der US-Ostküstenstadt Boston geflogen werden. Kerry werde im Massachusetts General Hospital behandelt, sagte sein Sprecher. In der Klinik hatte sich der Politiker vor einigen Jahren bereits einer Hüft-Operation unterzogen.Iran-AtomgesprächeKerry hatte am Samstag in Genf Gespräche über das iranische Atomprogramm geführt, die jedoch keinen Durchbruch brachten. Ursprünglich sollten die Verhandlungen zwischen Kerry und seinem iranischen Kollegen Mohammed Jawad Sarif am Sonntag fortgesetzt werden. Diese Fortsetzung wurde bereits vor Kerrys Unfall abgesagt, stattdessen wurden Verhandlungen auf Expertenebene in der kommenden Woche angekündigt.Wegen seiner Verletzung muss Kerry einen für Sonntag und Montag geplanten Aufenthalt in Spanien absagen. In Madrid wollte sich der US-Außenminister unter anderem mit dem spanischen König Felipe VI. und Regierungschef Mariano Rajoy treffen. Auch beim Treffen der internationalen Koalition gegen die Jihadistenmiliz "Islamischer Staat" in Paris wird Kerry fehlen. Der Außenminister werde sich zu den Gesprächen am Dienstag aber zuschalten lassen, sagte sein Sprecher Kirby.Kerry gilt als begeisterter Sportler, immer wieder ist er während seiner Reisen rund um die Welt in Verhandlungspausen auf dem Fahrrad unterwegs. Dafür nimmt er immer sein eigenes Rad mit. Nach Angaben der örtlichen Behörden wollte Kerry am Sonntag den Gebirgspass Col de la Colombiere befahren, den auch die Profiradler bei der Tour de France bezwingen müssen. (APA/AFP, 1.6.2015)'
    )
    input2 = QuoteInput(
        name=2,
        tokens=[],
        sentences=[],
        text="'Das wird ein toller Tag!', rief er ihr zu. Sie antwortete, dass sie anderer Meinung sei.",
    )
    print(json.dumps(q.predict([input1]), ensure_ascii=False))
