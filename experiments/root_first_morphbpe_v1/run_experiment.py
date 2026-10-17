"""Train and evaluate morphology priority orders on frozen original inputs.

The input-dir must contain the verified dataset bundle's extracted
training-inputs/, provenance/ and validation.csv. Output-dir is a separate
research directory, never the installed tokenizer. No final test split is read.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from collections import Counter
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
ROOT = EXPERIMENT_ROOT.parents[1]
for extra in (ROOT / "src", ROOT / "runtime", ROOT / "experiments/expanded_morphology_v4"):
    sys.path.insert(0, str(extra))

from expanded_morphology import ExpandedMorphologicalSegmenter  # noqa: E402
from kapampangan_morphbpe.artifact import (  # noqa: E402
    export_tokenizer_artifact,
    validate_artifact_files,
)
from kapampangan_morphbpe.lexicon import load_lexicon  # noqa: E402
from kapampangan_morphbpe.models import PreparedSequence  # noqa: E402
from kapampangan_morphbpe.normalization import comparison_key  # noqa: E402
from kapampangan_morphbpe.prepare import load_prepared_stream  # noqa: E402
from kapampangan_morphbpe.pretokenizer import pretokenize  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402

STREAM_SHA = "fc520e0e3359c3643b70f68f9a63521436be1dd4aac14b0adb1467238e3753c7"
LEXICON_SHA = "5219e018bcd9c4aec44e377f0ba37b07dd2ce38485173102b5462501651050d8"
VALIDATION_SHA = "9b5db52e563e4f334244fb66f6379c12cafd8501532caacde99e1e8307fd82d2"
DEV = ROOT / "experiments/tokenizer_selection_v1/data/dev.csv"
DEV_SHA = "c36f662b31d882503d7bde33a245cba6626e8b34c780a082628e1cd992b34275"
CURRENT = ROOT / "webapp/backend/tokenizer/artifacts/morphbpe-penalty32"
ROOT_KINDS = frozenset({"root", "root_fragment"})
AFFIX_KINDS = frozenset({"prefix", "suffix", "infix", "circumfix_prefix", "circumfix_suffix"})
WORDS = ("kumain", "kuman", "sumulat", "sinulat", "bumasa", "sulat", "kan", "basa", "kain",
         "suminulat", "tumula", "tumakut", "mumunang", "lumapit", "sumakup", "minum")
PRIORITY_ORDERS = {
    "root-first": ("root", "affix"),
    "affix-first": ("affix", "root"),
    "infix-only": ("infix",),
    "infix-root-affix": ("infix", "root", "affix"),
}


def load_selection():
    spec = importlib.util.spec_from_file_location("frozen_tokenizer_selection", ROOT / "experiments/tokenizer_selection_v1/run_selection.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def analysis_spans(analysis, lexicon, *, separate_infixes=False):
    """Use surface segment offsets, not restored underlying lengths."""
    result = []
    position = 0
    for surface, unit in zip(analysis.segments, analysis.underlying_units, strict=True):
        role = None
        if unit.kind in ROOT_KINDS:
            role = "root"
        elif unit.kind == "root_or_compound" and comparison_key(surface) in lexicon.valid_hosts and comparison_key(surface) not in lexicon.compounds:
            role = "root"
        elif separate_infixes and unit.kind == "infix":
            role = "infix"
        elif unit.kind in AFFIX_KINDS:
            role = "affix"
        if role is not None:
            result.append({"start": position, "end": position + len(surface), "role": role,
                           "surface": surface, "unit_kind": unit.kind, "underlying": unit.underlying})
        position += len(surface)
    assert position == len(analysis.token)
    return result


def load_inputs(input_dir):
    stream = input_dir / "training-inputs/training-stream.jsonl"
    lexicon_path = input_dir / "training-inputs/training-lexicon.json"
    validation = input_dir / "validation.csv"
    for path, expected in ((stream, STREAM_SHA), (lexicon_path, LEXICON_SHA), (validation, VALIDATION_SHA), (DEV, DEV_SHA)):
        if sha256_file(path) != expected:
            raise ValueError(f"Frozen input checksum mismatch: {path}")
    supplied_manifest = input_dir / "provenance/penalty32-tokenizer-manifest.json"
    if supplied_manifest.read_bytes() != (CURRENT / "tokenizer-manifest.json").read_bytes():
        raise ValueError("Installed baseline no longer matches the supplied original tokenizer manifest")
    if not validate_artifact_files(CURRENT)["checksums_match"]:
        raise ValueError("Installed baseline inventory is invalid")
    prepared = load_prepared_stream(stream)
    lexicon = load_lexicon(lexicon_path)
    return prepared, lexicon, validation


def annotate(prepared, lexicon, output_dir, *, separate_infixes=False):
    analyzer = ExpandedMorphologicalSegmenter(lexicon)
    all_spans = []
    statuses = Counter()
    skipped = Counter()
    types = Counter()
    occurrences = Counter()
    surfaces = {"root": Counter(), "affix": Counter()}
    if separate_infixes:
        surfaces["infix"] = Counter()
    audit_path = output_dir / "training-role-spans.jsonl"
    with audit_path.open("w", encoding="utf-8", newline="\n") as handle:
        for index, item in enumerate(prepared):
            spans = []
            rule = None
            if item.kind == "word":
                analysis = analyzer.segment(item.surface)
                assert analysis.token == item.surface
                statuses[analysis.status] += 1
                if analysis.status not in {"accepted", "protected_root"}:
                    skipped[analysis.status] += 1
                elif analysis.protected_boundaries != item.protected_boundaries:
                    skipped["boundary_mismatch"] += 1
                else:
                    spans = analysis_spans(analysis, lexicon, separate_infixes=separate_infixes)
                    rule = analysis.rule_id
            all_spans.append(spans)
            if spans:
                handle.write(json.dumps({"sequence_index": index, "surface": item.surface,
                                         "frequency": item.frequency, "rule": rule, "spans": spans}, ensure_ascii=False) + "\n")
            for span in spans:
                types[span["role"]] += 1
                occurrences[span["role"]] += item.frequency
                surfaces[span["role"]][span["surface"]] += item.frequency
    summary = {
        "sequences": len(prepared), "annotated_sequences": sum(bool(s) for s in all_spans),
        "analyzer_status_types": dict(statuses), "excluded_types": dict(skipped),
        "role_span_types": dict(types), "role_span_occurrences": dict(occurrences),
        "distinct_role_surfaces": {role: len(counts) for role, counts in surfaces.items()},
        "role_surface_frequencies": {role: dict(sorted(counts.items())) for role, counts in surfaces.items()},
        "annotation_quality": "provisional training analyzer, not independent human gold",
        "infixes_have_separate_training_role": separate_infixes,
        "excluded_roles": ["compound", "reduplicant", "clitic", "unconfirmed root_or_compound"],
        "span_source": "analysis.segments surface offsets; unit.kind labels; matching frozen boundaries",
        "roles_sha256": sha256_file(audit_path),
    }
    write_json(output_dir / "annotation-summary.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "role_surface_frequencies"}), flush=True)
    return all_spans, analyzer, summary


def score_roles(runtime, rows, analyzer, lexicon):
    counts = {role: {"spans": 0, "isolated": 0, "characters": 0} for role in ("root", "affix")}
    by_length = {
        role: {length: {"spans": 0, "isolated": 0} for length in ("single_character", "multiple_characters")}
        for role in ("root", "affix")
    }
    families = {}
    skipped = Counter()
    details = []
    for row in rows:
        analysis = analyzer.segment(row["surface"])
        if list(analysis.segments) != list(row["gold_pieces"]) or set(analysis.protected_boundaries) != row["gold_boundaries"]:
            skipped["analyzer_reference_disagreement"] += 1
            continue
        if analysis.status not in {"accepted", "protected_root"}:
            skipped[analysis.status] += 1
            continue
        tokens = runtime.encode(row["surface"]).tokens
        for span in analysis_spans(analysis, lexicon):
            isolated = any(token.start == span["start"] and token.end == span["end"] and token.token == span["surface"] for token in tokens)
            counts[span["role"]]["spans"] += 1
            counts[span["role"]]["isolated"] += isolated
            counts[span["role"]]["characters"] += span["end"] - span["start"]
            length_group = "single_character" if span["end"] - span["start"] == 1 else "multiple_characters"
            by_length[span["role"]][length_group]["spans"] += 1
            by_length[span["role"]][length_group]["isolated"] += isolated
            if span["role"] == "affix":
                key = f"{span['unit_kind']}:{span['underlying']}"
                group = families.setdefault(key, {"spans": 0, "isolated": 0})
                group["spans"] += 1
                group["isolated"] += isolated
            details.append({"word": row["surface"], **span, "isolated": isolated})
    for group in [*counts.values(), *families.values(), *(g for role in by_length.values() for g in role.values())]:
        group["isolation_rate"] = group["isolated"] / group["spans"] if group["spans"] else None
    return {"counts": counts, "by_length": by_length, "families": families, "skipped_rows": dict(skipped), "details": details,
            "scope": "only frozen DEV references exactly aligned with analyzer; role labels are not independent gold"}


def evaluate(artifact, prepared, analyzer, lexicon, selection):
    runtime = load_runtime_tokenizer(artifact)
    rows = selection.load_split(DEV)
    encoded = selection._encode_runtime(artifact, rows)
    predictions = []
    for row, pieces in zip(rows, encoded, strict=True):
        predicted = set()
        position = 0
        for piece in pieces[:-1]:
            position += len(piece)
            predicted.add(position)
        gold = row["gold_boundaries"]
        original = runtime.encode(row["surface"])
        assert runtime.decode(original.ids) == row["surface"]
        predictions.append({"surface": row["surface"], "pieces": list(pieces), "reference": list(row["gold_pieces"]),
                            "tp": len(predicted & gold), "fp": len(predicted - gold), "fn": len(gold - predicted),
                            "exact": list(pieces) == list(row["gold_pieces"])})
    infixes = {}
    for infix in ("um", "in"):
        indices = [i for i, row in enumerate(rows) if row["process"] == "infixation" and row["gold_boundaries"] == {1, 3} and row["gold_pieces"][1] == infix]
        details = []
        for index in indices:
            tokens = runtime.encode(rows[index]["surface"]).tokens
            isolated = any(token.start == 1 and token.end == 3 and token.token == infix for token in tokens)
            details.append({**predictions[index], "isolated": isolated})
        infixes[infix] = {"rows": len(indices), "isolated": sum(d["isolated"] for d in details), "details": details}
    word_frequencies = Counter()
    for sequence in prepared:
        if sequence.kind == "word":
            word_frequencies[sequence.surface] += sequence.frequency
    total_tokens = unknown = 0
    for word, frequency in word_frequencies.items():
        tokens = runtime.encode(word).tokens
        total_tokens += len(tokens) * frequency
        unknown += sum(token.token == "<unk>" for token in tokens) * frequency
    by_process = {}
    for process in sorted({row["process"] for row in rows}):
        indices = [i for i, row in enumerate(rows) if row["process"] == process]
        by_process[process] = {"rows": len(indices), "metrics": selection._score([rows[i] for i in indices], [encoded[i] for i in indices])}
    probes = {}
    for word in WORDS:
        encoding = runtime.encode(word)
        assert runtime.decode(encoding.ids) == word
        probes[word] = [token.token for token in encoding.tokens]
    metrics = selection._score(rows, encoded)
    counts = {key: sum(pred[key] for pred in predictions) for key in ("tp", "fp", "fn", "exact")}
    assert abs(metrics["boundary_f1"] - 2 * counts["tp"] / (2 * counts["tp"] + counts["fp"] + counts["fn"])) < 1e-12
    return {"dev_rows": len(rows), "dev_metrics": metrics, "dev_counts": counts, "dev_predictions": predictions,
            "infixes": infixes, "by_process": by_process, "probe_tokens": probes,
            "role_diagnostics": score_roles(runtime, rows, analyzer, lexicon),
            "training_corpus": {"word_types": len(word_frequencies), "word_occurrences": sum(word_frequencies.values()),
                                "tokens": total_tokens, "frequency_weighted_fertility": total_tokens / sum(word_frequencies.values()), "unknown_tokens": unknown},
            "artifact_validation": validate_artifact_files(artifact)}


def score_validation(artifact, validation, prepared):
    runtime = load_runtime_tokenizer(artifact)
    rows = list(csv.DictReader(validation.open(encoding="utf-8")))
    assert len(rows) == 3284 and len({row["id"] for row in rows}) == 3284
    train_words = {s.surface.casefold() for s in prepared if s.kind == "word"}
    words = word_tokens = unknown = unknown_rows = unseen_words = unseen_tokens = 0
    for row in rows:
        encoded = runtime.encode(row["text"])
        _, pretokens = pretokenize(row["text"])
        word_spans = [span for span in pretokens if span.kind == "word"]
        words += len(word_spans)
        word_tokens += sum(token.pretoken_kind == "word" for token in encoded.tokens)
        n_unknown = sum(token.token == "<unk>" for token in encoded.tokens)
        unknown += n_unknown
        unknown_rows += bool(n_unknown)
        if not n_unknown:
            assert runtime.decode(encoded.ids) == encoded.normalized_text
        for span in word_spans:
            if span.surface.casefold() not in train_words:
                unseen_words += 1
                unseen_tokens += sum(span.start <= token.start and token.end <= span.end for token in encoded.tokens if token.pretoken_kind == "word")
    return {"records": len(rows), "word_occurrences": words, "word_tokens": word_tokens,
            "word_fertility": word_tokens / words, "unknown_tokens": unknown, "rows_with_unknown": unknown_rows,
            "unseen_word_occurrences": unseen_words, "unseen_word_fertility": unseen_tokens / unseen_words}


def root_controls(artifacts, lexicon):
    runtimes = {name: load_runtime_tokenizer(path) for name, path in artifacts.items()}
    words = sorted(word for word in lexicon.valid_hosts if "um" in word)
    details = []
    for word in words:
        row = {"surface": word}
        for name, runtime in runtimes.items():
            encoded = runtime.encode(word)
            assert runtime.decode(encoded.ids) == word
            row[name] = [token.token for token in encoded.tokens]
        details.append(row)
    return {"rows": len(words), "annotation_quality": "provisional training lexicon hosts containing um; diagnostic, not independent gold",
            "totals": {name: {"tokens": sum(len(row[name]) for row in details), "kept_whole": sum(row[name] == [row["surface"]] for row in details)} for name in artifacts},
            "details": details}


def snapshot(directory):
    return {path.relative_to(directory).as_posix(): sha256_file(path) for path in directory.rglob("*") if path.is_file()}


def write_report(result, output_dir):
    evaluations = result["evaluations"]
    priority_order = result["config"]["priority_order"]
    lines = ["# " + " -> ".join(priority_order) + " Morph-BPE comparison", "",
             f"Exact original frozen stream, penalty {result['config']['crossing_penalty']} and vocabulary6080. Current installed penalty32 tokenizer is freshly evaluated; candidate uses training-only morphology roles and ordinary global BPE runtime. No final test text or translation model is used.", "",
             f"Declared order: {' -> '.join(priority_order)}. Declared new-token budgets before DEV evaluation: infix {result['config'].get('infix_token_budget', 0)}, root {result['config']['root_token_budget']}, affix {result['config']['affix_token_budget']}. Affix excludes infixes in the new infix orders. Role frequency ranks eligible internal pairs, followed by weighted score/allowed-frequency/UTF8 tie breaks. Budget counts new tokens, not merge rules.", "",
             "| Tokenizer | Boundary F1 | Exact /272 | um /5 | in /41 | DEV tokens/word | Validation tokens/word |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for name, evaluation in evaluations.items():
        metrics = evaluation["dev_metrics"]
        lines.append(f"| {name} | {100*metrics['boundary_f1']:.2f}% | {evaluation['dev_counts']['exact']} | {evaluation['infixes']['um']['isolated']} | {evaluation['infixes']['in']['isolated']} | {metrics['fertility']:.4f} | {result['validation'][name]['word_fertility']:.6f} |")
    lines += ["", "| Word | " + " | ".join(evaluations) + " |", "|---|" + "---|" * len(evaluations)]
    for word in WORDS:
        lines.append("| " + word + " | " + " | ".join(" + ".join(evaluation["probe_tokens"][word]) for evaluation in evaluations.values()) + " |")
    lines += ["", "## Runtime role diagnostics", "",
              "Only analyzer/reference-aligned DEV spans are included; role assignments are analyzer-derived and are not independent morphology gold.", "",
              "| Tokenizer | Root spans isolated | Affix spans isolated | Multi-character roots | Multi-character affixes |", "|---|---:|---:|---:|---:|"]
    for name, evaluation in evaluations.items():
        counts = evaluation["role_diagnostics"]["counts"]
        lengths = evaluation["role_diagnostics"]["by_length"]
        root_long = lengths["root"]["multiple_characters"]
        affix_long = lengths["affix"]["multiple_characters"]
        lines.append(f"| {name} | {counts['root']['isolated']}/{counts['root']['spans']} | {counts['affix']['isolated']}/{counts['affix']['spans']} | {root_long['isolated']}/{root_long['spans']} | {affix_long['isolated']}/{affix_long['spans']} |")
    lines += ["", "## Training and controls", "", "Phase statistics:", "", "```json",
              json.dumps(result["training_report"], indent=2, ensure_ascii=False), "```", "",
              f"Provisional root controls containing um: {result['root_controls']['rows']} rows; {json.dumps(result['root_controls']['totals'])}.", "",
              "DEV contains 272 mixed silver/user-derived words, only five genuine um cases, and 270/272 words seen in training. Results are exploratory and do not establish unseen-root or translation superiority. The 3284-record validation corpus measures fertility and coverage, not morphology accuracy.", "",
              "Root fragments remain separate when interrupted by an infix. Restored underlying roots are metadata; training prioritizes actual surface spans. Excluded roles (compounds, reduplicants and clitics) use normal allowed merging. Global pair rules can apply to other allowed training contexts and can cross boundaries during inference.", "",
              "Candidate is separate from installed artifacts. Changed token IDs require compatible new source embeddings before translation deployment."]
    (output_dir / "comparison-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def run(args):
    # Imported late so --mode annotate can audit inputs before trainer setup.
    from kapampangan_morphbpe.root_priority_bpe import RoleSpan, RootPriorityMorphBPETrainer

    penalty = getattr(args, "crossing_penalty", 32)
    if penalty < 0:
        raise ValueError("Crossing penalty must be nonnegative")
    output_dir = args.output_dir.resolve()
    if output_dir == CURRENT.resolve() or CURRENT.resolve() in output_dir.parents:
        raise ValueError("Output must not be inside the installed tokenizer")
    output_dir.mkdir(parents=True, exist_ok=True)
    preserved = snapshot(CURRENT)
    prepared, lexicon, validation = load_inputs(args.input_dir.resolve())
    order_name = getattr(args, "priority_order", "root-first")
    priority_order = PRIORITY_ORDERS[order_name]
    separate_infixes = "infix" in priority_order
    all_spans, analyzer, annotation_summary = annotate(
        prepared, lexicon, output_dir, separate_infixes=separate_infixes)
    if args.mode == "annotate":
        assert snapshot(CURRENT) == preserved
        return
    role_spans = [tuple(RoleSpan(span["start"], span["end"], span["role"]) for span in spans) for spans in all_spans]
    candidate_key = order_name.replace("-", "_") + str(penalty)
    root_budget = args.root_budget if "root" in priority_order else 0
    affix_budget = args.affix_budget if "affix" in priority_order else 0
    infix_budget = getattr(args, "infix_budget", 32) if separate_infixes else 0
    started = time.perf_counter()

    class ProgressTrainer(RootPriorityMorphBPETrainer):
        def _merge_once(self):
            merged = super()._merge_once()
            if merged and len(self.merges) % 500 == 0:
                print(f"{order_name}: {len(self.merges)} merges, {time.perf_counter()-started:.1f}s", flush=True)
            return merged

    trainer = ProgressTrainer(prepared, penalty, role_spans, root_token_budget=root_budget,
                              affix_token_budget=affix_budget, infix_token_budget=infix_budget,
                              priority_order=priority_order)
    initial_size = len(trainer.vocabulary)
    if root_budget + affix_budget + infix_budget > 6080 - initial_size:
        raise ValueError("Priority budgets exceed the matched vocabulary capacity")
    models, report = trainer.train([6080])
    if 6080 not in models or len(models[6080].vocabulary) != 6080:
        raise AssertionError("Candidate failed to reach matched vocabulary6080")
    for sequence in trainer.sequences:
        assert all(not any(token.start < boundary < token.end for boundary in sequence.protected) for token in sequence.symbols)
    elapsed = time.perf_counter() - started
    if separate_infixes and infix_budget > 0:
        if any(trainer.role_counts["infix"].values()):
            raise AssertionError("Infix budget did not form all supported internal infix pairs")
    artifact = output_dir / f"{order_name}-penalty{penalty}"
    config = {"crossing_penalty": penalty, "vocabulary_budget": 6080,
              "root_token_budget": root_budget, "affix_token_budget": affix_budget,
              "infix_token_budget": infix_budget,
              "infixes_have_separate_training_role": separate_infixes,
              "priority_order": [*priority_order, "weighted"],
              "priority_selection": "role_frequency, weighted_score, allowed_frequency, UTF8 pair tie break"}
    inputs = {"training_stream_sha256": STREAM_SHA, "training_lexicon_sha256": LEXICON_SHA,
              "dev_sha256": DEV_SHA, "validation_sha256": VALIDATION_SHA,
              "analyzer_sha256": sha256_file(ROOT / "experiments/expanded_morphology_v4/expanded_morphology.py"),
              "trainer_sha256": sha256_file(ROOT / "src/kapampangan_morphbpe/root_priority_bpe.py"),
              "base_trainer_sha256": sha256_file(ROOT / "src/kapampangan_morphbpe/weighted_bpe.py"),
              "runner_sha256": sha256_file(Path(__file__)), "role_spans_sha256": annotation_summary["roles_sha256"],
              "selection_evaluator_sha256": sha256_file(ROOT / "experiments/tokenizer_selection_v1/run_selection.py")}
    export_tokenizer_artifact(models[6080], artifact, metadata={
        "candidate": True, "algorithm": report["algorithm"],
        **config, **inputs, "held_out_test_used": False, "selection_performed": False,
        "lexicon_used_at_runtime": False, "surface_specific_overrides": [],
    })
    print(f"Training finished in {elapsed:.1f}s; evaluating exported runtime", flush=True)
    selection = load_selection()
    artifacts = {"current32": CURRENT, candidate_key: artifact}
    if getattr(args, "matched_weighted", None) is not None:
        matched = args.matched_weighted.resolve()
        if not validate_artifact_files(matched)["checksums_match"]:
            raise ValueError("Matched ordinary weighted candidate inventory is invalid")
        matched_doc = json.loads((matched / "tokenizer.json").read_text(encoding="utf-8"))
        if (matched_doc["metadata"].get("training_stream_sha256") != STREAM_SHA
                or matched_doc["metadata"].get("crossing_penalty") != penalty
                or len(matched_doc["vocabulary"]) != 6080
                or matched_doc["metadata"].get("priority_order") is not None):
            raise ValueError("Matched weighted candidate must use the same original stream, penalty and budget without priority phases")
        artifacts[f"matched_weighted{penalty}"] = matched
    if args.um_first is not None:
        prior = args.um_first.resolve()
        if not validate_artifact_files(prior)["checksums_match"]:
            raise ValueError("Prior um-first candidate inventory is invalid")
        prior_doc = json.loads((prior / "tokenizer.json").read_text(encoding="utf-8"))
        assert prior_doc["metadata"]["training_stream_sha256"] == STREAM_SHA
        assert len(prior_doc["vocabulary"]) == 6080 and prior_doc["metadata"]["crossing_penalty"] == 32
        artifacts["um_first32"] = prior
    evaluations = {}
    validations = {}
    for name, candidate in artifacts.items():
        print(f"Evaluating {name}: DEV and training corpus", flush=True)
        evaluations[name] = evaluate(candidate, prepared, analyzer, lexicon, selection)
        print(f"Evaluating {name}: validation corpus", flush=True)
        validations[name] = score_validation(candidate, validation, prepared)
    result = {"config": config, "inputs": inputs, "initial_vocabulary": initial_size,
              "vocabulary_size": len(models[6080].vocabulary), "merge_count": len(models[6080].merges),
              "training_seconds": elapsed, "training_report": report,
              "annotation_summary": {k: v for k, v in annotation_summary.items() if k != "role_surface_frequencies"},
              "evaluations": evaluations, "validation": validations, "root_controls": root_controls(artifacts, lexicon),
              "held_out_test_used": False, "translation_training_or_quality_evaluation": False,
              "installed_inventory_unchanged": snapshot(CURRENT) == preserved}
    assert result["installed_inventory_unchanged"]
    load_inputs(args.input_dir.resolve())
    write_json(output_dir / "comparison-result.json", result)
    write_report(result, output_dir)
    print(json.dumps({name: {"F1": evaluation["dev_metrics"]["boundary_f1"], "exact": evaluation["dev_counts"]["exact"],
                             "um": evaluation["infixes"]["um"]["isolated"], "in": evaluation["infixes"]["in"]["isolated"]}
                      for name, evaluation in evaluations.items()}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("annotate", "train"), default="train")
    parser.add_argument("--root-budget", type=int, default=2244)
    parser.add_argument("--affix-budget", type=int, default=256)
    parser.add_argument("--infix-budget", type=int, default=32)
    parser.add_argument("--crossing-penalty", type=int, default=32)
    parser.add_argument("--priority-order", choices=tuple(PRIORITY_ORDERS), default="root-first")
    parser.add_argument("--um-first", type=Path)
    parser.add_argument("--matched-weighted", type=Path)
    run(parser.parse_args())
