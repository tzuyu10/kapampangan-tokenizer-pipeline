"""Prepare fixed corpus diagnostics without using morphology TEST to select models."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

from build_package import WORDS, MARKERS, key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--kap-bundle", type=Path, required=True)
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--arrow-libs", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0,str(args.arrow_libs.resolve()))
    import pyarrow.parquet as pq
    csv.field_size_limit(2**31-1)
    args.output.mkdir(parents=True)
    with zipfile.ZipFile(args.kap_bundle) as outer:
        with zipfile.ZipFile(io.BytesIO(outer.read("source/kapampangan-general-corpus-v1.zip"))) as inner:
            validation = inner.read("kapampangan-general-corpus-v1/data/validation.csv")
            (args.output / "kapampangan_validation.csv").write_bytes(validation)
    train = [json.loads(line) for line in (args.inputs / "data/tagalog_train.jsonl").read_text(encoding="utf-8").splitlines()]
    training_titles = {key(row["source_document_title"]) for row in train}
    with (args.inputs / "data/train.csv").open(encoding="utf-8",newline="") as stream:
        excluded = {key(row["text"]) for row in csv.DictReader(stream)}
    selected, titles, seen = [], set(), set()
    document,title,title_key,index=-1,"","",0
    for batch in pq.ParquetFile(args.parquet).iter_batches(batch_size=8192,columns=["text"]):
        for raw in batch.column(0).to_pylist():
            row_index=index
            index+=1
            text=unicodedata.normalize("NFC",raw or "").strip()
            if text.startswith("="):
                if re.fullmatch(r"=\s*[^=].*?\s*=",text):
                    document,title=row_index,text.strip("= ")
                    title_key=key(title)
                continue
            if not title_key or title_key in training_titles or title_key in titles:
                continue
            if int(hashlib.sha256(("tl-eval-doc-seed42\0"+title_key).encode()).hexdigest(),16)%7:
                continue
            for artifact,replacement in [("@-@","-"),("@,@",","),("@.@",".")]:
                text=re.sub(r"\s*"+re.escape(artifact)+r"\s*",replacement,text)
            text=" ".join(text.split())
            words=WORDS.findall(text.casefold())
            if not 5<=len(words)<=80 or sum(w in MARKERS for w in words)<2:
                continue
            if any(m in text for m in ["http://","https://","www.","<",">","{","}","|","="]):
                continue
            if any(unicodedata.category(c).startswith("C") for c in text):
                continue
            letters=[c for c in text if c.isalpha()]
            if not letters or sum("LATIN" in unicodedata.name(c,"") for c in letters)/len(letters)<.98:
                continue
            text_key=key(text)
            if text_key in excluded or text_key in seen:
                continue
            titles.add(title_key);seen.add(text_key)
            selected.append({"id":f"tl_eval_{row_index:07d}","text":text,"raw_text":raw,
                "source_row_index":row_index,"document_start_row":document,"document_title":title,
                "document_title_key":title_key,"split":"evaluation_only","source":"Wikitext-TL39 train distribution, withheld from this tokenizer experiment",
                "source_revision":"7c1a76c2c1864abf434453e312f034d0cf211fff","human_morphology_gold":False})
            if len(selected)==1000:
                break
        if len(selected)==1000:
            break
    assert len(selected)==1000
    assert not titles & training_titles
    with (args.output / "tagalog_unseen_articles.jsonl").open("w",encoding="utf-8",newline="\n") as stream:
        for row in selected:
            stream.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
    manifest={"kapampangan_validation_records":len(list(csv.DictReader(io.StringIO(validation.decode("utf-8"))))),
        "kapampangan_validation_sha256":hashlib.sha256(validation).hexdigest(),
        "tagalog_evaluation_records":1000,"tagalog_unique_article_titles":len(titles),"article_title_overlap_with_added_training":0,
        "training_text_overlap_normalized":0,"tagalog_selection":"first qualifying paragraph per eligible nontraining article; seeded title-hash 1/7 screen; first1000 in source order",
        "selection_limit":"coverage/length diagnostic, not a representative language benchmark or morphology gold",
        "morphology_test_read":False,"translation_evaluation_or_neural_training":False}
    (args.output / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2),flush=True)


if __name__=="__main__":
    main()
