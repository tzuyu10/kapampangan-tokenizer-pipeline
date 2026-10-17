"""Train a matched 6,080 / 8,192 / 16,384 tokenizer vocabulary grid."""
from __future__ import annotations

import argparse
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
    package = args.inputs.resolve()
    sys.path.insert(0, str(package))
    sys.path.insert(0, str(package / "source"))
    from train_tokenizer import verify_inputs, set_augmented_identity
    from kapampangan_morphbpe.prepare import load_prepared_stream
    from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json
    from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files

    manifest = verify_inputs(package)
    if args.output.exists():
        raise ValueError("Use a new family output directory")
    targets = [6080, 8192, 16384]
    plain_path = package / "prepared/plain-training-stream.jsonl"
    morph_path = package / "prepared/training-stream.jsonl"
    started = time.monotonic()
    if args.condition == "unigram":
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        os.environ["RAYON_NUM_THREADS"] = "1"
        import tokenizers
        from tokenizers import Tokenizer, models, trainers, decoders

        rows = [json.loads(line) for line in plain_path.read_text(encoding="utf-8").splitlines()]
        characters = sorted({c for r in rows for c in r["surface"]}, key=lambda c:c.encode("utf-8"))
        special = ["<pad>","<unk>","<s>","</s>"]
        def iterator():
            for row in rows:
                for _ in range(row["frequency"]):
                    yield row["surface"]
        for size in targets:
            step_started = time.monotonic()
            print(f"Training fresh Unigram at vocabulary {size:,}", flush=True)
            tokenizer = Tokenizer(models.Unigram())
            trainer = trainers.UnigramTrainer(vocab_size=size,special_tokens=special,unk_token="<unk>",initial_alphabet=characters)
            tokenizer.train_from_iterator(iterator(),trainer=trainer)
            tokenizer.decoder = decoders.Fuse()
            assert tokenizer.get_vocab_size() == size
            assert all(tokenizer.token_to_id(s)==i for i,s in enumerate(special))
            assert all(c in tokenizer.get_vocab() for c in characters)
            out = args.output / f"vocab-{size}"
            out.mkdir(parents=True)
            tokenizer.save(str(out / "tokenizer.json"))
            body = {"artifact_type":"matched_fresh_unigram", "algorithm":"unigram_lm", "actual_vocabulary_size":size,
                "dataset_fingerprint":manifest["augmented_dataset_fingerprint"], "base_dataset_fingerprint":manifest["base_dataset_fingerprint"],
                "training_stream_sha256":sha256_file(plain_path), "augmentation_manifest_sha256":sha256_file(package / "manifest.json"),
                "special_tokens":special,"character_inventory_size":len(characters),"atomic_pretoken_frequency_expansion":True,
                "pre_tokenizer":None,"normalizer":None,"decoder":"Fuse","library_version":tokenizers.__version__,"rayon_threads":1,
                "not_nllb_target_tokenizer":True,"reproducibility":"one frozen run; independent Unigram EM runs can differ",
                "elapsed_seconds":time.monotonic()-step_started,"tokenizer_sha256":sha256_file(out / "tokenizer.json")}
            write_json(out / "unigram-manifest.json",{**body,"artifact_fingerprint":fingerprint(body)})
            (out / "checksums.sha256").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in sorted(out.iterdir())),encoding="utf-8")
            print(f"Completed Unigram {size:,}: {time.monotonic()-step_started:.1f}s",flush=True)
    else:
        from kapampangan_morphbpe.bpe import ConstrainedBPETrainer
        from kapampangan_morphbpe.weighted_bpe import WeightedMorphBPETrainer
        from kapampangan_morphbpe.root_priority_bpe import RootPriorityMorphBPETrainer,RoleSpan

        path = plain_path if args.condition == "plain" else morph_path
        prepared = load_prepared_stream(path)
        concrete = {"plain":ConstrainedBPETrainer,"weighted32":WeightedMorphBPETrainer,"infix_first48":RootPriorityMorphBPETrainer}[args.condition]
        original = concrete._merge_once
        def progress(self):
            result = original(self)
            if result and (len(self.merges)%250==0 or len(self.vocabulary) in targets):
                print(f"{args.condition}: {len(self.vocabulary):,}/16,384 tokens; {time.monotonic()-started:.1f}s",flush=True)
            return result
        concrete._merge_once = progress
        print(f"Initializing {args.condition}, {len(prepared):,} prepared sequences",flush=True)
        if args.condition == "plain":
            trainer = concrete(prepared)
        elif args.condition == "weighted32":
            trainer = concrete(prepared,32)
        else:
            spans = [[RoleSpan(*s) for s in json.loads(line)] for line in (package / "prepared/role-spans.jsonl").read_text(encoding="utf-8").splitlines()]
            trainer = concrete(prepared,48,spans,root_token_budget=0,affix_token_budget=0,infix_token_budget=32,priority_order=("infix",))
        models, report = trainer.train(targets)
        assert set(models)==set(targets),report
        for size in targets:
            out = args.output / f"vocab-{size}"
            metadata = {"condition":args.condition,"candidate":True,"selection_performed":False,"held_out_test_used":False,
                "lexicon_used_at_runtime":False,"vocabulary_budget":size,"crossing_penalty":None if args.condition=="plain" else (48 if args.condition=="infix_first48" else 32),
                "augmentation_manifest_sha256":sha256_file(package / "manifest.json"),"training_stream_sha256":sha256_file(path),
                "base_dataset_fingerprint":manifest["base_dataset_fingerprint"],"augmented_dataset_fingerprint":manifest["augmented_dataset_fingerprint"],
                "training_report_scope":"shared full grid training through16384; artifact itself is exact prefix snapshot at declared vocabulary size",
                "full_grid_training_report":report,"languages":["pam","tl"],"neural_model_training":False}
            export_tokenizer_artifact(models[size],out,metadata=metadata,
                artifact_type="kapampangan_plain_bpe" if args.condition=="plain" else "kapampangan_morphbpe")
            set_augmented_identity(out,manifest["augmented_dataset_fingerprint"])
            assert validate_artifact_files(out)["checksums_match"]
    write_json(args.output / "training-summary.json",{"condition":args.condition,"status":"completed","vocabulary_sizes":targets,
        "elapsed_seconds":time.monotonic()-started,"wall_time_scope":"shared local CPU load, not a speed benchmark",
        "augmentation_manifest_sha256":sha256_file(package / "manifest.json"),"neural_model_training":False})
    print(f"Completed {args.condition}: all three vocabulary sizes",flush=True)


if __name__ == "__main__":
    main()
