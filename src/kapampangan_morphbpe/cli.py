from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast

from .artifact import validate_artifact_files
from .bpe import train_candidate_models
from .dataset import verify_dataset
from .evaluation import evaluate_candidates, select_candidate
from .lexicon import build_lexicon, load_lexicon
from .morphology import MorphologicalSegmenter
from .nllb_contract import export_nllb_contract
from .pipeline import export_candidate_models, finalize_selected_tokenizer
from .prepare import freeze_candidate_grid, prepare_training_stream
from .runtime_bridge import load_runtime_tokenizer
from .serialization import read_json, write_json
from .verification import verify_clean_runtime, verify_python_rust_parity


def _path(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True))


def _targets(grid_path: Path) -> list[int]:
    raw: Any = read_json(grid_path)
    if not isinstance(raw, dict):
        raise ValueError("candidate grid must be an object")
    values = cast(dict[str, Any], raw).get("candidate_vocabulary_sizes")
    if not isinstance(values, list) or not all(isinstance(item, int) for item in values):
        raise ValueError("candidate grid target list malformed")
    return cast(list[int], values)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kapampangan-morphbpe")
    subparsers = parser.add_subparsers(dest="command", required=True)

    verify = subparsers.add_parser("verify-dataset")
    verify.add_argument("--dataset-root", type=_path, required=True)
    verify.add_argument("--output", type=_path)

    lexicon = subparsers.add_parser("build-lexicon")
    lexicon.add_argument("--dataset-root", type=_path, required=True)
    lexicon.add_argument("--output-dir", type=_path, required=True)

    segment = subparsers.add_parser("segment")
    segment.add_argument("--lexicon", type=_path, required=True)
    segment.add_argument("--text", required=True)

    prepare = subparsers.add_parser("prepare-training")
    prepare.add_argument("--dataset-root", type=_path, required=True)
    prepare.add_argument("--lexicon", type=_path, required=True)
    prepare.add_argument("--output-dir", type=_path, required=True)
    prepare.add_argument("--engine", choices=("rust", "python"), default="rust")

    freeze = subparsers.add_parser("freeze-candidates")
    freeze.add_argument("--prepared-manifest", type=_path, required=True)
    freeze.add_argument("--output", type=_path, required=True)

    parity = subparsers.add_parser("verify-segmentation-parity")
    parity.add_argument("--dataset-root", type=_path, required=True)
    parity.add_argument("--lexicon", type=_path, required=True)
    parity.add_argument("--output", type=_path, required=True)

    train = subparsers.add_parser("train-candidates")
    train.add_argument("--prepared-stream", type=_path, required=True)
    train.add_argument("--prepared-manifest", type=_path, required=True)
    train.add_argument("--grid", type=_path, required=True)
    train.add_argument("--lexicon-manifest", type=_path, required=True)
    train.add_argument("--output-dir", type=_path, required=True)

    evaluate = subparsers.add_parser("evaluate-validation")
    evaluate.add_argument("--dataset-root", type=_path, required=True)
    evaluate.add_argument("--lexicon", type=_path, required=True)
    evaluate.add_argument("--candidates-dir", type=_path, required=True)
    evaluate.add_argument("--grid", type=_path, required=True)
    evaluate.add_argument("--reports-dir", type=_path, required=True)

    select = subparsers.add_parser("select-candidate")
    select.add_argument("--grid", type=_path, required=True)
    select.add_argument("--validation-report", type=_path, required=True)
    select.add_argument("--output", type=_path, required=True)

    finalize = subparsers.add_parser("finalize-tokenizer")
    finalize.add_argument("--prepared-stream", type=_path, required=True)
    finalize.add_argument("--selection", type=_path, required=True)
    finalize.add_argument("--lexicon-manifest", type=_path, required=True)
    finalize.add_argument("--prepared-manifest", type=_path, required=True)
    finalize.add_argument("--output-dir", type=_path, required=True)
    finalize.add_argument("--rebuild-dir", type=_path, required=True)

    tokenize = subparsers.add_parser("tokenize")
    tokenize.add_argument("--artifact", type=_path, required=True)
    tokenize.add_argument("--text", required=True)
    tokenize.add_argument("--add-special-tokens", action="store_true")

    decode = subparsers.add_parser("decode")
    decode.add_argument("--artifact", type=_path, required=True)
    decode.add_argument("--ids", required=True, help="JSON list of integer token IDs")

    inspect = subparsers.add_parser("inspect-artifact")
    inspect.add_argument("--artifact", type=_path, required=True)

    validate = subparsers.add_parser("validate-artifact")
    validate.add_argument("--artifact", type=_path, required=True)

    runtime = subparsers.add_parser("verify-runtime-independence")
    runtime.add_argument("--artifact", type=_path, required=True)
    runtime.add_argument("--runtime-root", type=_path, required=True)
    runtime.add_argument("--output", type=_path, required=True)

    nllb = subparsers.add_parser("export-nllb-contract")
    nllb.add_argument("--artifact", type=_path, required=True)
    nllb.add_argument("--output-dir", type=_path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = cast(str, args.command)
    if command == "verify-dataset":
        result = verify_dataset(args.dataset_root)
        if args.output is not None:
            write_json(args.output, result)
        _print(result)
    elif command == "build-lexicon":
        _print(build_lexicon(args.dataset_root, args.output_dir))
    elif command == "segment":
        _print(MorphologicalSegmenter(load_lexicon(args.lexicon)).segment(args.text).to_dict())
    elif command == "prepare-training":
        _print(
            prepare_training_stream(
                args.dataset_root, args.lexicon, args.output_dir, engine=args.engine
            )
        )
    elif command == "freeze-candidates":
        _print(freeze_candidate_grid(args.prepared_manifest, args.output))
    elif command == "verify-segmentation-parity":
        _print(verify_python_rust_parity(args.dataset_root, args.lexicon, args.output))
    elif command == "train-candidates":
        models, report = train_candidate_models(
            args.prepared_stream,
            args.prepared_manifest,
            args.grid,
            args.output_dir,
        )
        summary = export_candidate_models(
            models,
            args.output_dir,
            training_report_path=args.output_dir / "candidate-training-report.json",
            grid_path=args.grid,
            lexicon_manifest_path=args.lexicon_manifest,
            prepared_manifest_path=args.prepared_manifest,
        )
        _print({"training": report, "artifacts": summary})
    elif command == "evaluate-validation":
        _print(
            evaluate_candidates(
                args.dataset_root,
                args.lexicon,
                args.candidates_dir,
                _targets(args.grid),
                args.reports_dir,
            )
        )
    elif command == "select-candidate":
        _print(select_candidate(args.grid, args.validation_report, args.output))
    elif command == "finalize-tokenizer":
        _print(
            finalize_selected_tokenizer(
                args.prepared_stream,
                args.selection,
                args.output_dir,
                args.rebuild_dir,
                lexicon_manifest_path=args.lexicon_manifest,
                prepared_manifest_path=args.prepared_manifest,
            )
        )
    elif command == "tokenize":
        encoding = load_runtime_tokenizer(args.artifact).encode(
            args.text, add_special_tokens=args.add_special_tokens
        )
        _print(
            {
                "normalized_text": encoding.normalized_text,
                "tokens": [
                    {
                        "token": token.token,
                        "id": token.identifier,
                        "start": token.start,
                        "end": token.end,
                        "pretoken_kind": token.pretoken_kind,
                        "vocabulary_kind": token.vocabulary_kind,
                    }
                    for token in encoding.tokens
                ],
                "ids": list(encoding.ids),
            }
        )
    elif command == "decode":
        identifiers = json.loads(args.ids)
        if not isinstance(identifiers, list) or not all(
            isinstance(item, int) for item in identifiers
        ):
            raise ValueError("--ids must be a JSON list of integers")
        _print({"text": load_runtime_tokenizer(args.artifact).decode(identifiers)})
    elif command == "inspect-artifact":
        _print(read_json(args.artifact / "tokenizer-manifest.json"))
    elif command == "validate-artifact":
        result = validate_artifact_files(args.artifact)
        tokenizer = load_runtime_tokenizer(args.artifact)
        result["vocabulary_size"] = tokenizer.vocabulary_size
        result["reload_succeeded"] = True
        _print(result)
    elif command == "verify-runtime-independence":
        _print(verify_clean_runtime(args.artifact, args.runtime_root, args.output))
    elif command == "export-nllb-contract":
        _print(export_nllb_contract(args.artifact, args.output_dir))
    else:
        raise AssertionError(f"unhandled command: {command}")
    return 0
