"""Train one frozen comparison condition with progress and timing evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--condition", choices=["weighted32", "infix_first48", "plain", "unigram"], required=True)
    args = parser.parse_args()
    started = time.monotonic()
    package = args.inputs.resolve()
    sys.path.insert(0, str(package))
    sys.path.insert(0, str(package / "source"))
    from train_tokenizer import verify_inputs
    from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json

    manifest = verify_inputs(package)
    if args.output.exists():
        raise ValueError("Output exists; preserve completed runs")
    if args.condition == "unigram":
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["RAYON_NUM_THREADS"] = "1"
        import tokenizers
        from tokenizers import Tokenizer, decoders, models, trainers

        rows = [json.loads(line) for line in (package / "prepared/plain-training-stream.jsonl").read_text(encoding="utf-8").splitlines()]
        characters = sorted({c for r in rows for c in r["surface"]}, key=lambda c: c.encode("utf-8"))
        special = ["<pad>", "<unk>", "<s>", "</s>"]
        tokenizer = Tokenizer(models.Unigram())
        trainer = trainers.UnigramTrainer(vocab_size=6080, special_tokens=special, unk_token="<unk>", initial_alphabet=characters)
        def iterator():
            for row in rows:
                for _ in range(row["frequency"]):
                    yield row["surface"]
        print(f"Training fresh Unigram, 6,080 tokens, {len(rows):,} atomic pretoken types", flush=True)
        tokenizer.train_from_iterator(iterator(), trainer=trainer)
        tokenizer.decoder = decoders.Fuse()
        assert tokenizer.get_vocab_size() == 6080
        assert all(tokenizer.token_to_id(s) == i for i, s in enumerate(special))
        assert all(c in tokenizer.get_vocab() for c in characters)
        args.output.mkdir(parents=True)
        tokenizer.save(str(args.output / "tokenizer.json"))
        body = {"artifact_type": "matched_fresh_unigram", "algorithm": "unigram_lm", "actual_vocabulary_size":6080,
                "dataset_fingerprint":manifest["augmented_dataset_fingerprint"], "base_dataset_fingerprint":manifest["base_dataset_fingerprint"],
                "training_stream_sha256":sha256_file(package / "prepared/plain-training-stream.jsonl"),
                "augmentation_manifest_sha256":sha256_file(package / "manifest.json"),
                "special_tokens":special, "character_inventory_size":len(characters),
                "training_pretokenizer":"none; original atomic pretoken surfaces repeated exactly by frequency",
                "runtime_decoder":"Fuse; project pretokenizer applied outside model", "training_normalizer":None,
                "library":"tokenizers", "library_version":tokenizers.__version__, "rayon_threads":1,
                "reproducibility":"one frozen run; independent Unigram/EM runs are not guaranteed byte-identical",
                "tokenizer_sha256":sha256_file(args.output / "tokenizer.json"), "not_nllb_target_tokenizer":True}
        write_json(args.output / "unigram-manifest.json", {**body, "artifact_fingerprint":fingerprint(body)})
        (args.output / "checksums.sha256").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in sorted(args.output.iterdir())),encoding="utf-8")
    else:
        from kapampangan_morphbpe.bpe import ConstrainedBPETrainer
        from kapampangan_morphbpe.root_priority_bpe import RootPriorityMorphBPETrainer
        from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer
        def instrument(cls):
            original = cls._merge_once
            def progress(self):
                result = original(self)
                if result and len(self.merges) % 250 == 0:
                    print(f"{args.condition}: {len(self.vocabulary):,}/6,080 tokens, {len(self.merges):,} merges, {time.monotonic()-started:.1f}s", flush=True)
                return result
            cls._merge_once = progress
        # Only the concrete trainer is wrapped, so subclass super-calls retain
        # the original unwrapped base logic and every learned decision is unchanged.
        cls = {"weighted32":WeightedMorphBPETrainer, "infix_first48":RootPriorityMorphBPETrainer, "plain":ConstrainedBPETrainer}[args.condition]
        instrument(cls)
        algorithm = {"weighted32":"weighted", "infix_first48":"infix-first", "plain":"plain"}[args.condition]
        sys.argv = ["train_tokenizer.py", "--inputs", str(package), "--output", str(args.output),
                    "--algorithm", algorithm, "--penalty", "48" if args.condition == "infix_first48" else "32", "--vocab-size", "6080"]
        from train_tokenizer import main as train
        train()
    write_json(args.output.parent / f"{args.condition}-training-time.json", {
        "condition":args.condition, "status":"completed", "actual_vocabulary_size":6080,
        "elapsed_seconds":time.monotonic()-started, "note":"wall time under shared local CPU load, not a speed benchmark",
        "augmentation_manifest_sha256":sha256_file(package / "manifest.json"),
        "neural_model_training":False})
    print(f"Completed {args.condition}: {time.monotonic()-started:.1f}s",flush=True)


if __name__ == "__main__":
    main()
