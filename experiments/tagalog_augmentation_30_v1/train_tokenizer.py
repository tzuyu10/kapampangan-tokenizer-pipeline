"""Train a new tokenizer from the verified, separate 30 percent input package."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def verify_inputs(root: Path):
    inventory = json.loads((root / "checksums.json").read_text(encoding="utf-8"))
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob("*")
                    if p.is_file() and "__pycache__" not in p.parts
                    and p.suffix != ".pyc" and p.name != "checksums.json"}
    if actual_files != set(inventory):
        raise ValueError("Input package file inventory changed")
    for relative, expected in inventory.items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError("Unsafe inventory path")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Input checksum mismatch: {relative}")
    return json.loads((root / "manifest.json").read_text(encoding="utf-8"))


def set_augmented_identity(output: Path, dataset_fingerprint: str):
    """Give newly trained exports their own dataset identity, with coherent hashes."""
    from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json

    tokenizer_path = output / "tokenizer.json"
    document = json.loads(tokenizer_path.read_text(encoding="utf-8"))
    document["metadata"]["dataset_fingerprint"] = dataset_fingerprint
    write_json(tokenizer_path, document)
    path = output / "tokenizer-manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["dataset_fingerprint"] = dataset_fingerprint
    manifest["core_file_sha256"]["tokenizer.json"] = sha256_file(tokenizer_path)
    manifest.pop("artifact_fingerprint")
    manifest["artifact_fingerprint"] = fingerprint(manifest)
    write_json(path, manifest)
    inventory = sorted(p for p in output.iterdir() if p.is_file() and p.name != "checksums.sha256")
    (output / "checksums.sha256").write_text(
        "".join(f"{sha256_file(p)}  {p.name}\n" for p in inventory), encoding="utf-8", newline="\n",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--algorithm", choices=["weighted", "infix-first", "plain"], default="weighted")
    parser.add_argument("--penalty", type=int, default=32)
    parser.add_argument("--vocab-size", type=int, default=6080)
    args = parser.parse_args()
    root = args.inputs.resolve()
    manifest = verify_inputs(root)
    if args.output.exists():
        raise ValueError("Use a new output directory to preserve existing artifacts")
    if args.output.resolve().is_relative_to(root):
        raise ValueError("Keep trained artifacts outside the frozen input package")
    sys.path.insert(0, str(root / "source"))
    from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files
    from kapampangan_morphbpe.bpe import ConstrainedBPETrainer
    from kapampangan_morphbpe.prepare import load_prepared_stream
    from kapampangan_morphbpe.root_priority_bpe import RootPriorityMorphBPETrainer, RoleSpan
    from kapampangan_morphbpe.serialization import write_json
    from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer

    name = "plain-training-stream.jsonl" if args.algorithm == "plain" else "training-stream.jsonl"
    prepared = load_prepared_stream(root / "prepared" / name)
    initial = len({c for item in prepared for c in item.surface}) + 4
    if args.vocab_size <= initial:
        raise ValueError(f"Vocabulary must exceed initial character/special inventory {initial}")
    print(f"Verified {manifest['counts']['combined_train_records']:,} training records; "
          f"{len(prepared):,} prepared sequences; initial vocabulary {initial:,}", flush=True)
    if args.algorithm == "infix-first":
        spans = []
        with (root / "prepared/role-spans.jsonl").open(encoding="utf-8") as stream:
            for line in stream:
                spans.append([RoleSpan(*span) for span in json.loads(line)])
        trainer = RootPriorityMorphBPETrainer(
            prepared, args.penalty, spans, root_token_budget=0, affix_token_budget=0,
            infix_token_budget=32, priority_order=("infix",),
        )
    elif args.algorithm == "plain":
        trainer = ConstrainedBPETrainer(prepared)
    else:
        trainer = WeightedMorphBPETrainer(prepared, args.penalty)
    print(f"Training {args.algorithm}, vocabulary={args.vocab_size}, penalty={args.penalty}", flush=True)
    models, report = trainer.train([args.vocab_size])
    if args.vocab_size not in models:
        raise ValueError(f"Training did not reach requested vocabulary: {report}")
    metadata = {
        "condition": f"pam_tl_30pct_{args.algorithm}_penalty{args.penalty}",
        "candidate": True, "selection_performed": False, "held_out_test_used": False,
        "lexicon_used_at_runtime": False, "crossing_penalty": args.penalty if args.algorithm != "plain" else None,
        "augmentation_manifest_sha256": hashlib.sha256((root / "manifest.json").read_bytes()).hexdigest(),
        "training_stream_sha256": hashlib.sha256((root / "prepared" / name).read_bytes()).hexdigest(),
        "base_dataset_fingerprint": manifest["base_dataset_fingerprint"],
        "augmented_dataset_fingerprint": manifest["augmented_dataset_fingerprint"],
        "languages": ["pam", "tl"], "tagalog_limit_basis": "30 percent of original Kapampangan counts, floored",
        "tagalog_morphology": "separate selected dictionary and source-language-specific preprocessing",
        "training_report": report,
    }
    export_tokenizer_artifact(
        models[args.vocab_size], args.output, metadata=metadata,
        artifact_type="kapampangan_plain_bpe" if args.algorithm == "plain" else "kapampangan_morphbpe",
        tokenizer_card="Experimental Kapampangan plus Tagalog tokenizer. New matching source embeddings required.\n",
    )
    set_augmented_identity(args.output, manifest["augmented_dataset_fingerprint"])
    verification = validate_artifact_files(args.output)
    assert verification["checksums_match"], verification
    write_json(args.output.parent / f"{args.output.name}-verification.json", verification)
    print(f"Exported verified tokenizer to {args.output.resolve()}", flush=True)


if __name__ == "__main__":
    main()
