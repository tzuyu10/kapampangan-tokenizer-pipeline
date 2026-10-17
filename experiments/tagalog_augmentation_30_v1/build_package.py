"""Prepare bounded, reproducible Tagalog additions without replacing original inputs."""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import heapq
import io
import json
import re
import shutil
import sys
import unicodedata
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
from kapampangan_morphbpe.pretokenizer import pretokenize_normalized as pretokenize
from kapampangan_morphbpe.serialization import fingerprint, write_json

EXPECTED = {
    "stream": "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7",
    "lexicon": "5219e018bcd9c4aec44e377f0ba37b07dd2ce38485173102b5462501651050d8",
    "tagalog": "9cfda555c64b3da921d94acd0ce7d6b0bb672f1ffdff80d4249fc47f54e077df",
    "parquet": "706d706496e3a085cf4506f97aa8b03faa20d4773d69453eaab4e3ca8f33caf9",
}
SEED = "pam-tl-30pct-v1-seed42"
WORDS = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.UNICODE)
MARKERS = set("ang mga ay isang ng sa na at ito nito nito nitong siya sila kanilang kanyang kaniyang ngunit upang mula nang habang hindi dahil para bilang noong kung rin din lamang kung saan sino ano bakit paano".split())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def key(text):
    # Punctuation-insensitive, whitespace/case/NFC-normalized exclusion key.
    return " ".join(WORDS.findall(unicodedata.normalize("NFC", text).casefold()))


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["id", "text"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_bytes(data):
    csv.field_size_limit(2**31 - 1)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def select_corpus(parquet, count, excluded):
    import pyarrow.parquet as pq

    stats, heap, seen = collections.Counter(), [], set()
    document, title, index = -1, "", 0
    for batch in pq.ParquetFile(parquet).iter_batches(batch_size=8192, columns=["text"]):
        for raw in batch.column(0).to_pylist():
            row_index = index
            index += 1
            stats["source_rows"] += 1
            text = unicodedata.normalize("NFC", raw or "").strip()
            if text.startswith("="):
                if re.fullmatch(r"=\s*[^=].*?\s*=", text):
                    document, title = row_index, text.strip("= ")
                stats["heading"] += 1
                continue
            for artifact, replacement in [("@-@", "-"), ("@,@", ","), ("@.@", ".")]:
                text = re.sub(r"\s*" + re.escape(artifact) + r"\s*", replacement, text)
            text = " ".join(text.split())
            words = WORDS.findall(text.casefold())
            reason = None
            if not 5 <= len(words) <= 80:
                reason = "word_length_outside_5_80"
            elif any(marker in text for marker in ["http://", "https://", "www.", "<", ">", "{", "}", "|", "="]):
                reason = "markup_url_or_table"
            elif sum(w in MARKERS for w in words) < 2:
                reason = "insufficient_tagalog_markers"
            elif any(unicodedata.category(c).startswith("C") for c in text):
                reason = "control_character"
            else:
                letters = [c for c in text if c.isalpha()]
                if not letters or sum("LATIN" in unicodedata.name(c, "") for c in letters) / len(letters) < .98:
                    reason = "non_latin_heavy"
            if reason:
                stats[reason] += 1
                continue
            text_key = key(text)
            kh = digest(text_key.encode())
            if text_key in excluded:
                stats["kap_train_or_held_out_overlap"] += 1
                continue
            if kh in seen:
                stats["duplicate_normalized_text"] += 1
                continue
            seen.add(kh)
            stats["eligible_unique"] += 1
            score = int(digest((SEED + "\0" + kh).encode()), 16)
            row = {"id": f"tl_wikitext39_train_{row_index:07d}", "text": text,
                   "raw_text": raw, "language": "tl", "split": "train",
                   "source_row_index": row_index, "source_document_start_row": document,
                   "source_document_title": title, "source_text_sha256": digest(raw.encode()),
                   "normalized_exclusion_key_sha256": kh,
                   "dataset_id": "linkanjarad/Wikitext-TL39",
                   "dataset_revision": "7c1a76c2c1864abf434453e312f034d0cf211fff",
                   "language_review_status": "dataset_label_plus_heuristic_not_human_verified",
                   "origin": "existing_external_corpus_not_generated_in_this_task"}
            entry = (-score, row_index, row)
            if len(heap) < count * 8:
                heapq.heappush(heap, entry)
            elif entry[:2] > heap[0][:2]:
                heapq.heapreplace(heap, entry)
        if index % (8192 * 20) == 0:
            print(f"Screened {index:,} corpus rows", flush=True)
    selected, docs = [], collections.Counter()
    for _score, _index, row in sorted(heap, key=lambda e: (-e[0], e[1])):
        document = row["source_document_start_row"]
        if docs[document] >= 3:
            continue
        docs[document] += 1
        selected.append(row)
        if len(selected) == count:
            break
    if len(selected) != count:
        raise ValueError(f"Only {len(selected)} qualifying corpus rows; need {count}")
    stats["selected"] = len(selected)
    stats["selected_documents"] = len(docs)
    return sorted(selected, key=lambda r: r["source_row_index"]), dict(stats)


def select_lexicon(path, count, existing, frequencies):
    rows = json.loads(path.read_text(encoding="utf-8"))
    candidates, stats = {}, collections.Counter()
    for index, row in enumerate(rows):
        word = unicodedata.normalize("NFC", row.get("word", "").strip()).lower()
        url = urlparse(row.get("link", ""))
        head = unquote(url.path.rstrip("/").split("/")[-1]).lower()
        reason = "eligible"
        if row.get("language") != "Tagalog":
            reason = "not_tagalog"
        elif len(word) < 4 or not re.fullmatch(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", word):
            reason = "empty_short_or_nonword"
        elif url.hostname != "tagalog.pinoydictionary.com" or head != word:
            reason = "source_headword_mismatch"
        elif not row.get("definition", "").strip():
            reason = "empty_definition"
        elif word in existing:
            reason = "existing_kapampangan_lexical_key"
        elif word in candidates:
            reason = "duplicate_word"
        stats[reason] += 1
        if reason == "eligible":
            candidates[word] = {**row, "word": word, "source_dictionary_row_index": index,
                                "selected_corpus_exact_word_frequency": frequencies[word],
                                "review_status": "automatically_filtered_not_human_validated"}
    ranked = sorted(candidates, key=lambda w: (-frequencies[w], digest((SEED + "\0" + w).encode())))
    if len(ranked) < count:
        raise ValueError("Insufficient cleaned Tagalog words")
    selected = [candidates[w] for w in sorted(ranked[:count])]
    stats["selected"] = len(selected)
    stats["selected_attested_in_tagalog_sample"] = sum(frequencies[r["word"]] > 0 for r in selected)
    return selected, dict(stats)


def copy_source(package, tagalog_repo, roots):
    for folder, target in [(REPO / "src/kapampangan_morphbpe", package / "source/kapampangan_morphbpe"),
                           (REPO / "runtime", package / "runtime")]:
        for source in folder.rglob("*.py"):
            if "__pycache__" in source.parts:
                continue
            dest = target / source.relative_to(folder)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
    shutil.copyfile(REPO / "experiments/expanded_morphology_v4/expanded_morphology.py", package / "source/expanded_morphology.py")
    for name in ["language_support.py", "train_tokenizer.py"]:
        shutil.copyfile(Path(__file__).parent / name, package / name)
    vendor = package / "vendor/filipino_tokenizer"
    (vendor / "tagalog").mkdir(parents=True)
    (vendor / "data").mkdir()
    for name in ["base.py", "tagalog/segmenter.py", "tagalog/roots.py", "tagalog/affixes.py", "tagalog/phonology.py"]:
        shutil.copyfile(tagalog_repo / "filipino_tokenizer" / name, vendor / name)
    (vendor / "__init__.py").write_text('"""Subset of upstream morphology helpers, MIT licensed."""\n', encoding="utf-8")
    (vendor / "tagalog/__init__.py").write_text('"""Morphology-only imports; no BPE or Transformers dependency."""\n', encoding="utf-8")
    for name in ["prefix_table.json", "suffix_table.json", "infix_table.json", "circumfix_table.json"]:
        raw = json.loads((tagalog_repo / "filipino_tokenizer/data" / name).read_text(encoding="utf-8"))
        filtered = {key: [r for r in rows if r.get("language") == "Tagalog"] for key, rows in raw.items()}
        write_json(vendor / "data" / name, {key: rows for key, rows in filtered.items() if rows})
    write_json(vendor / "data/tagalog_roots.json", roots)
    shutil.copyfile(tagalog_repo / "LICENSE", package / "provenance/FILIPINO_TOKENIZER_LICENSE.txt")


def prepare_stream(package, tagalog_rows):
    from language_support import surface_analysis, tagalog_segmenter
    from kapampangan_morphbpe.lexicon import load_lexicon
    sys.path.insert(0, str(package / "source"))
    from expanded_morphology import ExpandedMorphologicalSegmenter

    baseline = [json.loads(line) for line in (package / "original/kapampangan-training-stream.jsonl").read_text(encoding="utf-8").splitlines()]
    counts, roles = collections.Counter(), {}
    lexicon = load_lexicon(package / "lexicons/kapampangan-training-lexicon.json")
    analyzer = ExpandedMorphologicalSegmenter(lexicon)
    for row in baseline:
        k = (row["surface"], tuple(row["protected_boundaries"]), row["kind"])
        counts[k] += row["frequency"]
        spans = []
        if row["kind"] == "word":
            analysis = analyzer.segment(row["surface"])
            if analysis.status in {"accepted", "protected_root"} and analysis.protected_boundaries == k[1]:
                offset = 0
                for piece, unit in zip(analysis.segments, analysis.underlying_units, strict=True):
                    role = "infix" if unit.kind == "infix" else None
                    if role:
                        spans.append((offset, offset + len(piece), role))
                    offset += len(piece)
        roles[k] = tuple(spans)
    tag = tagalog_segmenter(package)
    tag_counts, tag_spans = collections.Counter(), {}
    stats = collections.Counter()
    for row in tagalog_rows:
        for token in pretokenize(row["text"]):
            k = (token.surface, (), token.kind)
            tag_counts[k] += 1
    prepared_tag = []
    for (surface, _empty, kind), frequency in sorted(tag_counts.items()):
        boundaries, spans, status = surface_analysis(tag, surface) if kind == "word" else ((), (), "nonword")
        stats[status + "_types"] += 1
        stats[status + "_occurrences"] += frequency
        k = (surface, boundaries, kind)
        counts[k] += frequency
        infixes = tuple(span for span in spans if span[2] == "infix")
        # When two languages share the same surface/boundary pattern, prioritize
        # only infix spans supported by both analyses. No language gets invented roles.
        if k in roles:
            roles[k] = tuple(span for span in roles[k] if span in infixes)
        else:
            roles[k] = infixes
        tag_spans[k] = infixes
        prepared_tag.append({"surface": surface, "protected_boundaries": list(boundaries), "kind": kind, "frequency": frequency})
    rows, all_spans, plain = [], [], collections.Counter()
    for (surface, boundaries, kind), frequency in sorted(counts.items()):
        rows.append({"surface": surface, "protected_boundaries": list(boundaries), "kind": kind, "frequency": frequency})
        all_spans.append(roles[(surface, boundaries, kind)])
        plain[(surface, kind)] += frequency
    write_jsonl(package / "prepared/training-stream.jsonl", rows)
    write_jsonl(package / "prepared/tagalog-training-stream.jsonl", prepared_tag)
    write_jsonl(package / "prepared/role-spans.jsonl", all_spans)
    write_jsonl(package / "prepared/plain-training-stream.jsonl", [
        {"surface": surface, "protected_boundaries": [], "kind": kind, "frequency": frequency}
        for (surface, kind), frequency in sorted(plain.items())])
    return {"sequences": len(rows), "initial_vocabulary_size": len({c for r in rows for c in r['surface']}) + 4,
            "tagalog_morphology": dict(stats),
            "kapampangan_word_occurrences": sum(r["frequency"] for r in baseline if r["kind"] == "word"),
            "tagalog_word_occurrences": sum(r["frequency"] for r in prepared_tag if r["kind"] == "word")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kap-bundle", type=Path, required=True)
    parser.add_argument("--tagalog-repo", type=Path, required=True)
    parser.add_argument("--parquet", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arrow-libs", type=Path)
    args = parser.parse_args()
    if args.arrow_libs:
        sys.path.insert(0, str(args.arrow_libs.resolve()))
    package = args.output.resolve()
    if package.exists():
        raise ValueError("Use a new output directory")
    package.mkdir(parents=True)
    for name in ["data", "original", "provenance", "lexicons", "prepared"]:
        (package / name).mkdir()
    tag_path = args.tagalog_repo / "filipino_tokenizer/data/tagalog_roots.json"
    assert digest(tag_path.read_bytes()) == EXPECTED["tagalog"]
    assert digest(args.parquet.read_bytes()) == EXPECTED["parquet"]
    with zipfile.ZipFile(args.kap_bundle) as outer:
        stream = outer.read("training-inputs/training-stream.jsonl")
        lex_bytes = outer.read("training-inputs/training-lexicon.json")
        assert digest(stream) == EXPECTED["stream"]
        assert digest(lex_bytes) == EXPECTED["lexicon"]
        (package / "original/kapampangan-training-stream.jsonl").write_bytes(stream)
        (package / "lexicons/kapampangan-training-lexicon.json").write_bytes(lex_bytes)
        for name in ["training-stream-manifest.json", "training-lexicon-manifest.json"]:
            (package / "provenance" / ("kapampangan-" + name)).write_bytes(outer.read("training-inputs/" + name))
        with zipfile.ZipFile(io.BytesIO(outer.read("source/kapampangan-general-corpus-v1.zip"))) as inner:
            prefix = "kapampangan-general-corpus-v1/"
            train_bytes = inner.read(prefix + "data/train.csv")
            training = read_csv_bytes(train_bytes)
            (package / "data/kapampangan_train.csv").write_bytes(train_bytes)
            excluded = {key(r["text"]) for r in training}
            held_out_hashes = {}
            for split in ["validation", "test"]:
                raw = inner.read(prefix + f"data/{split}.csv")
                excluded.update(key(r["text"]) for r in read_csv_bytes(raw))
                held_out_hashes[split] = digest(raw)
            for name in ["CITATIONS.md", "README.md", "metadata/dataset-manifest.json"]:
                (package / "provenance" / ("kapampangan-" + Path(name).name)).write_bytes(inner.read(prefix + name))
    translation_path = Path(r"C:\Users\Gabo\Downloads\kpm_tgl_cleaned.csv")
    if not translation_path.exists():
        raise FileNotFoundError("Current translation CSV required for held-out-overlap exclusion")
    translation_raw = translation_path.read_bytes()
    assert digest(translation_raw) == "69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b"
    for row in read_csv_bytes(translation_raw):
        if row["split"] in {"validation", "test"}:
            excluded.update([key(row["source"]), key(row["target"])])
    lexicon = json.loads(lex_bytes)
    root_count = len(lexicon["roots"])
    corpus_count = len(training)
    assert root_count == 3311 and corpus_count == 26268
    selection_identity = fingerprint({"seed": SEED, "excluded": sorted(excluded), "count": corpus_count * 3 // 10, "parquet": EXPECTED["parquet"], "filter_version": 1})
    selection_cache = args.parquet.parent / f"selected_{selection_identity}.json"
    if selection_cache.exists():
        cached = json.loads(selection_cache.read_text(encoding="utf-8"))
        assert fingerprint(cached["payload"]) == cached["fingerprint"]
        rows, corpus_stats = cached["payload"]["rows"], cached["payload"]["stats"]
    else:
        rows, corpus_stats = select_corpus(args.parquet, corpus_count * 3 // 10, excluded)
        payload = {"rows": rows, "stats": corpus_stats}
        write_json(selection_cache, {"payload": payload, "fingerprint": fingerprint(payload)})
    frequencies = collections.Counter(token.surface.lower() for row in rows for token in pretokenize(row["text"]) if token.kind == "word")
    existing = {r["comparison_key"] for r in lexicon["roots"]}
    existing.update(r["comparison_key"] for r in lexicon["spelling_variants"])
    existing.update(r["comparison_key"] for r in lexicon["compounds"] if r.get("operational"))
    roots, root_stats = select_lexicon(tag_path, root_count * 3 // 10, existing, frequencies)
    write_json(package / "lexicons/tagalog_roots.json", roots)
    write_json(package / "lexicons/lexicon-pam-tl.json", {
        "format": "language_partitioned_tokenizer_training_lexicons_v1",
        "pam": {"path": "kapampangan-training-lexicon.json", "root_entries": root_count},
        "tl": {"path": "tagalog_roots.json", "root_entries": len(roots)},
        "total_root_entries": root_count + len(roots),
        "policy": "Preserve Kapampangan morphology; apply Tagalog rules and selected roots to Tagalog corpus only."})
    write_jsonl(package / "data/tagalog_train.jsonl", rows)
    write_csv(package / "data/tagalog_train.csv", [{"id": r["id"], "text": r["text"]} for r in rows])
    write_csv(package / "data/train.csv", training + [{"id": r["id"], "text": r["text"]} for r in rows])
    (package / "data/tagalog_train.txt").write_text("\n".join(r["text"] for r in rows) + "\n", encoding="utf-8", newline="\n")
    copy_source(package, args.tagalog_repo, roots)
    print("Preparing language-specific morphology and combined BPE streams", flush=True)
    stream_stats = prepare_stream(package, rows)
    manifest = {
        "created_date": "2026-10-17", "experiment": "tagalog_augmentation_30_v1", "seed": SEED,
        "base_dataset_fingerprint": lexicon["dataset_fingerprint"],
        "selection_policy": {"ratio": "3/10", "rounding": "floor", "lexicon_unit": "unique operational root entries",
            "corpus_unit": "training text records, not words, tokens, documents or bytes",
            "sampling": "lowest seeded SHA256 scores over all eligible unique rows; maximum 3 rows per source document",
            "root_selection": "highest exact-word frequency in selected training text; seeded SHA256 ties; existing Kapampangan keys excluded",
            "root_quality": "NFC, lowercase, minimum 4 letters, one lexical token, exact dictionary URL headword match, nonempty definition, deduplicated",
            "language_status": "source dataset label plus automatic heuristics, not bilingual human validation",
            "held_out": "new rows exclude normalized punctuation-insensitive matches to original Kapampangan train/validation/test and translation validation/test source/target; no held-out scoring or original split change",
            "case_policy": "training text case preserved; roots compared in lowercase"},
        "counts": {"kapampangan_root_entries": root_count, "tagalog_root_entries": len(roots), "combined_root_entries": root_count + len(roots),
                   "kapampangan_train_records": corpus_count, "tagalog_train_records": len(rows), "combined_train_records": corpus_count + len(rows)},
        "sources": {"kapampangan_bundle_sha256": digest(args.kap_bundle.read_bytes()),
                    "kapampangan_train_sha256": digest(train_bytes), "original_stream_sha256": digest(stream),
                    "original_lexicon_sha256": digest(lex_bytes), "tagalog_dictionary_sha256": digest(tag_path.read_bytes()),
                    "wikitext_dataset": "linkanjarad/Wikitext-TL39", "wikitext_revision": "7c1a76c2c1864abf434453e312f034d0cf211fff",
                    "wikitext_parquet_sha256": digest(args.parquet.read_bytes()), "held_out_csv_sha256": held_out_hashes,
                    "translation_csv_sha256": digest(translation_raw)},
        "screening": {"corpus": corpus_stats, "lexicon": root_stats}, "prepared": stream_stats,
        "limits": ["No human morphology/language audit or quality improvement established", "Original corpus leakage beyond new-row exact exclusion remains unaudited",
                   "No full tokenizer or neural model training performed by this builder", "New source tokenizer requires newly trained compatible source embeddings before NLLB use"]}
    manifest["payload_sha256"] = {relative: digest((package / relative).read_bytes()) for relative in [
        "data/train.csv", "data/tagalog_train.jsonl", "lexicons/tagalog_roots.json",
        "prepared/training-stream.jsonl", "prepared/plain-training-stream.jsonl", "prepared/role-spans.jsonl"]}
    manifest["augmented_dataset_fingerprint"] = fingerprint(manifest)
    write_json(package / "manifest.json", manifest)
    shutil.copyfile(Path(__file__), package / "provenance/build_package.py")
    write_json(package / "provenance/source_code_snapshots.json", {
        "kapampangan_python_files": {p.relative_to(REPO).as_posix(): digest(p.read_bytes()) for p in (REPO / "src/kapampangan_morphbpe").rglob("*.py") if "__pycache__" not in p.parts},
        "tagalog_helpers": {n: digest((args.tagalog_repo / "filipino_tokenizer" / n).read_bytes()) for n in ["base.py", "tagalog/segmenter.py", "tagalog/roots.py", "tagalog/affixes.py", "tagalog/phonology.py"]}})
    for name in ["README.md", "Retrain_PAM_TL_30pct_Tokenizer_Colab.ipynb"]:
        shutil.copyfile(Path(__file__).parent / name, package / name)
    shutil.copyfile(Path(__file__).parent / "verify_package.py", package / "provenance/verify_package.py")
    inventory = {p.relative_to(package).as_posix(): digest(p.read_bytes())
                 for p in sorted(package.rglob("*")) if p.is_file()
                 and "__pycache__" not in p.parts and p.suffix != ".pyc" and p.name != "checksums.json"}
    write_json(package / "checksums.json", inventory)
    print(json.dumps({"output": str(package), "counts": manifest["counts"], "screening": manifest["screening"], "prepared": stream_stats}, indent=2), flush=True)


if __name__ == "__main__":
    main()
