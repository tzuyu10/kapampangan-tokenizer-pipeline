"""Independent data-integrity and integration checks for the delivered package."""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse


def sha(data):
    return hashlib.sha256(data).hexdigest()


def csv_rows(data):
    csv.field_size_limit(2**31 - 1)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def exclusion_key(text):
    return " ".join(re.findall(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", unicodedata.normalize("NFC", text).casefold()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--kap-bundle", type=Path, required=True)
    parser.add_argument("--tagalog-repo", type=Path, required=True)
    parser.add_argument("--arrow-libs", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.inputs.resolve()
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "source"))
    sys.path.insert(0, str(args.arrow_libs.resolve()))
    import pyarrow.parquet as pq
    from kapampangan_morphbpe.prepare import load_prepared_stream
    from kapampangan_morphbpe.pretokenizer import pretokenize_normalized
    from language_support import surface_analysis, tagalog_segmenter

    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    counts = manifest["counts"]
    assert counts == {"kapampangan_root_entries":3311, "tagalog_root_entries":993, "combined_root_entries":4304,
                      "kapampangan_train_records":26268, "tagalog_train_records":7880, "combined_train_records":34148}
    assert counts["tagalog_root_entries"] == counts["kapampangan_root_entries"] * 3 // 10
    assert counts["tagalog_train_records"] == counts["kapampangan_train_records"] * 3 // 10
    tag = read_lines(root / "data/tagalog_train.jsonl")
    tag_by_index = {r["source_row_index"]:r for r in tag}
    assert len(tag_by_index) == 7880
    assert len({r["id"] for r in tag}) == 7880
    assert len({exclusion_key(r["text"]) for r in tag}) == 7880
    documents = collections.Counter(r["source_document_start_row"] for r in tag)
    assert max(documents.values()) <= 3
    matched, offset = 0, 0
    for batch in pq.ParquetFile(args.parquet).iter_batches(batch_size=16384, columns=["text"]):
        for i, text in enumerate(batch.column(0).to_pylist(), offset):
            if i in tag_by_index:
                row = tag_by_index[i]
                assert row["raw_text"] == text
                assert row["source_text_sha256"] == sha(text.encode())
                assert row["normalized_exclusion_key_sha256"] == sha(exclusion_key(row["text"]).encode())
                assert row["split"] == "train" and row["language"] == "tl"
                assert unicodedata.normalize("NFC", row["text"]) == row["text"]
                matched += 1
        offset += batch.num_rows
    assert matched == 7880 and offset == 1524071
    with zipfile.ZipFile(args.kap_bundle) as outer:
        original_lex = outer.read("training-inputs/training-lexicon.json")
        original_stream = outer.read("training-inputs/training-stream.jsonl")
        assert original_lex == (root / "lexicons/kapampangan-training-lexicon.json").read_bytes()
        assert original_stream == (root / "original/kapampangan-training-stream.jsonl").read_bytes()
        with zipfile.ZipFile(io.BytesIO(outer.read("source/kapampangan-general-corpus-v1.zip"))) as inner:
            train_raw = inner.read("kapampangan-general-corpus-v1/data/train.csv")
            assert train_raw == (root / "data/kapampangan_train.csv").read_bytes()
            original_train = csv_rows(train_raw)
            excluded = {exclusion_key(r["text"]) for r in original_train}
            for split in ["validation", "test"]:
                excluded.update(exclusion_key(r["text"]) for r in csv_rows(inner.read(f"kapampangan-general-corpus-v1/data/{split}.csv")))
    translation = Path(r"C:\Users\Gabo\Downloads\kpm_tgl_cleaned.csv")
    assert sha(translation.read_bytes()) == manifest["sources"]["translation_csv_sha256"]
    for row in csv_rows(translation.read_bytes()):
        if row["split"] in {"validation", "test"}:
            excluded.add(exclusion_key(row["source"]))
            excluded.add(exclusion_key(row["target"]))
    assert not {exclusion_key(r["text"]) for r in tag} & excluded
    combined = csv_rows((root / "data/train.csv").read_bytes())
    assert combined[:26268] == original_train
    assert combined[26268:] == [{"id":r["id"], "text":r["text"]} for r in tag]
    assert len({r["id"] for r in combined}) == 34148
    lex = json.loads(original_lex)
    roots = json.loads((root / "lexicons/tagalog_roots.json").read_text(encoding="utf-8"))
    source_roots = json.loads((args.tagalog_repo / "filipino_tokenizer/data/tagalog_roots.json").read_text(encoding="utf-8"))
    existing = {r["comparison_key"] for r in lex["roots"] + lex["spelling_variants"]}
    existing.update(r["comparison_key"] for r in lex["compounds"] if r.get("operational"))
    assert len(roots) == len({r["word"] for r in roots}) == 993
    assert not {r["word"] for r in roots} & existing
    frequencies = collections.Counter(t.surface.lower() for r in tag for t in pretokenize_normalized(r["text"]) if t.kind == "word")
    for row in roots:
        source = source_roots[row["source_dictionary_row_index"]]
        assert row["word"] == unicodedata.normalize("NFC", source["word"].strip()).lower()
        assert len(row["word"]) >= 4 and row["language"] == "Tagalog"
        for field in ["definition", "language", "part_of_speech", "link"]:
            assert row[field] == source[field]
        assert row["word"] == unquote(urlparse(row["link"]).path.rstrip('/').split('/')[-1]).lower()
        assert row["selected_corpus_exact_word_frequency"] == frequencies[row["word"]]
    segmenter = tagalog_segmenter(root)
    assert segmenter.roots.get_all_roots() == {r["word"] for r in roots}
    prepared = load_prepared_stream(root / "prepared/training-stream.jsonl")
    plain = load_prepared_stream(root / "prepared/plain-training-stream.jsonl")
    tag_prepared = load_prepared_stream(root / "prepared/tagalog-training-stream.jsonl")
    baseline = read_lines(root / "original/kapampangan-training-stream.jsonl")
    expected = collections.Counter()
    for row in baseline:
        expected[(row["surface"], tuple(row["protected_boundaries"]), row["kind"])] += row["frequency"]
    tag_surfaces = collections.Counter()
    for item in tag_prepared:
        expected[(item.surface, item.protected_boundaries, item.kind)] += item.frequency
        tag_surfaces[(item.surface, item.kind)] += item.frequency
        if item.kind == "word":
            boundaries, spans, status = surface_analysis(segmenter, item.surface)
            assert item.protected_boundaries == boundaries
            cuts = [0, *boundaries, len(item.surface)]
            pieces = [item.surface[a:b] for a,b in zip(cuts,cuts[1:])]
            assert ''.join(pieces) == item.surface and all(pieces)
    raw_surfaces = collections.Counter((t.surface, t.kind) for row in tag for t in pretokenize_normalized(row["text"]))
    assert raw_surfaces == tag_surfaces
    assert expected == collections.Counter({(p.surface,p.protected_boundaries,p.kind):p.frequency for p in prepared})
    totals = collections.Counter()
    for (surface,boundaries,kind), frequency in expected.items():
        totals[(surface,kind)] += frequency
    assert totals == collections.Counter({(p.surface,p.kind):p.frequency for p in plain})
    assert not any(p.protected_boundaries for p in plain)
    spans = read_lines(root / "prepared/role-spans.jsonl")
    assert len(spans) == len(prepared)
    for item, item_spans in zip(prepared, spans, strict=True):
        edges = {0,len(item.surface),*item.protected_boundaries}
        for start,end,role in item_spans:
            assert start in edges and end in edges and start<end and role == 'infix'
            assert not any(start < edge < end for edge in item.protected_boundaries)
    class FakeRoots:
        def is_root(self, word):return word == 'kain'
    class FakeAffixes:
        def get_infixes(self):return ['um','in']
    class FakeSegmenter:
        affixes,roots=FakeAffixes(),FakeRoots()
        def segment(self, word):return ['um','kain']
    boundaries,_,status=surface_analysis(FakeSegmenter(),'Kumain')
    assert boundaries==(1,3) and status=='segmented'
    assert surface_analysis(FakeSegmenter(),'Something')[2]=='nonconcatenative_fallback'
    for path in root.rglob('*.py'):
        compile(path.read_text(encoding='utf-8-sig'),str(path),'exec')
    report = {"status":"passed", "checks":["30_percent_floor_counts", "all_selected_parquet_rows_exact_provenance",
        "original_training_text_order_and_lexicon_stream_bytes_preserved", "new_text_normalized_deduplication_and_held_out_exclusion",
        "all_dictionary_entries_exact_provenance_and_source_headword_match", "selected_only_tagalog_dictionary_runtime",
        "lossless_tagalog_surface_offsets_and_case", "combined_morph_and_plain_stream_frequency_parity",
        "infix_roles_align_with_protected_boundaries", "all_packaged_python_compiles"],
        "counts":counts, "selected_documents":len(documents), "all_selected_roots_attested":all(frequencies[r['word']]>0 for r in roots),
        "full_tokenizer_training":"not_run; separate small smoke runs recorded separately", "translation_training_or_quality":"not_run"}
    args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
