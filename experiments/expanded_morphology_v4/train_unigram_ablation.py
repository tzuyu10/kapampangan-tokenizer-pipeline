"""Train fresh SentencePiece-style Unigram-LM tokenizers on this project's
own Kapampangan corpus, at each of the same three vocabulary sizes (6,080 /
8,192 / 16,384) as the Plain-BPE and MorphBPE conditions trained by
`run_experiment.py`, so `nllbprop` can offer the same 6k/8k/16k choice as
`v4prop`.

This is NOT NLLB-200's tokenizer and is not a substitute for it. It exists
to isolate one variable that `nllb_baseline_report.py`'s native-NLLB
comparison cannot: NLLB uses a different subword *algorithm* (Unigram-LM,
via SentencePiece) than this project's Plain-BPE/MorphBPE (BPE), AND a much
larger vocabulary (256,204 vs. 8,192) trained on ~200 other languages, not
Kapampangan. Those two differences are confounded in the native-NLLB
comparison. This script holds vocabulary size, training corpus, character
inventory, and special tokens fixed -- identical to the local Plain-BPE
condition -- and swaps only the algorithm (Unigram-LM instead of BPE), so a
fertility difference against Plain-BPE here can be attributed to the
algorithm rather than to vocabulary size or corpus exposure.

Every training sequence (word, punctuation, whitespace run) from
`runs/prepared/plain-training-stream.jsonl` is fed to the trainer exactly
`frequency` times, with the tokenizer's own pre_tokenizer/normalizer
disabled -- mirroring exactly how `ConstrainedBPETrainer` (this project's
own Plain-BPE trainer) consumes the identical stream: each surface is
already an atomic pretoken, so nothing should be re-split before subword
training.

Known limitation, disclosed rather than hidden: unlike every other artifact
in this repository, training runs of this script are not guaranteed
byte-reproducible. The `tokenizers` library's Unigram/EM trainer is
third-party (not this project's own deterministic BPE trainers, which use
explicit, code-reviewed tie-breaking rules) and was empirically observed to
produce different merge tables across independent runs on the same input,
including single-threaded (RAYON_NUM_THREADS=1) -- see AGENT_CONTEXT.md.
The artifact trained here is one frozen instance, fingerprinted below;
re-running this script will very likely produce a similar but not
byte-identical tokenizer.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

import tokenizers  # noqa: E402
from tokenizers import Tokenizer, models, trainers  # noqa: E402

from kapampangan_morphbpe.constants import DATASET_FINGERPRINT, SCHEMA_VERSION  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, sha256_file, write_json  # noqa: E402

PLAIN_STREAM_PATH = EXPERIMENT_ROOT / "runs/prepared/plain-training-stream.jsonl"
PREPARED_MANIFEST_PATH = EXPERIMENT_ROOT / "runs/prepared/training-stream-manifest.json"

# Matches the vocabulary sizes trained for every other v4 condition
# (plain, penalty-1/2/4/8), so `nllbprop` can offer the same 6k/8k/16k
# size choice as `v4prop`.
TARGET_VOCAB_SIZES = (6080, 8192, 16384)
SPECIAL_TOKEN_SURFACES = ["<pad>", "<unk>", "<s>", "</s>"]

# Other v4 artifact families that must stay byte-unchanged by this script.
OTHER_V4_ARTIFACT_DIRS = {
    "plain": EXPERIMENT_ROOT / "artifacts/plain",
    "penalty-1": EXPERIMENT_ROOT / "artifacts/penalty-1",
    "penalty-2": EXPERIMENT_ROOT / "artifacts/penalty-2",
    "penalty-4": EXPERIMENT_ROOT / "artifacts/penalty-4",
    "penalty-8": EXPERIMENT_ROOT / "artifacts/penalty-8",
}


def _directory_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        return {}
    return {
        path.relative_to(directory).as_posix(): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def _snapshot_other_artifacts() -> dict[str, dict[str, str]]:
    return {name: _directory_hashes(path) for name, path in OTHER_V4_ARTIFACT_DIRS.items()}


def _load_stream() -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    with PLAIN_STREAM_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            rows.append((row["surface"], row["frequency"]))
    return rows


def _train(rows: list[tuple[str, int]], characters: list[str], vocab_size: int) -> Tokenizer:
    tokenizer = Tokenizer(models.Unigram())
    tokenizer.normalizer = None
    tokenizer.pre_tokenizer = None
    trainer = trainers.UnigramTrainer(  # type: ignore[no-untyped-call]
        vocab_size=vocab_size,
        special_tokens=SPECIAL_TOKEN_SURFACES,
        unk_token="<unk>",
        initial_alphabet=characters,
    )

    def iterator() -> Any:
        for surface, freq in rows:
            for _ in range(freq):
                yield surface

    tokenizer.train_from_iterator(iterator(), trainer=trainer)
    return tokenizer


def _train_one_size(
    vocab_size: int,
    rows: list[tuple[str, int]],
    characters: list[str],
    total_types: int,
    total_occurrences: int,
    plain_stream_sha256: str,
    prepared_manifest: Any,
) -> None:
    artifact_dir = EXPERIMENT_ROOT / f"artifacts/unigram-ablation/vocab-{vocab_size}"
    tokenizer_path = artifact_dir / "tokenizer.json"
    manifest_path = artifact_dir / "unigram-ablation-manifest.json"

    tokenizer = _train(rows, characters, vocab_size)
    if tokenizer.get_vocab_size() != vocab_size:
        raise AssertionError(
            f"Unigram training reached {tokenizer.get_vocab_size()}, expected {vocab_size}"
        )
    for role, surface in zip(["pad", "unk", "bos", "eos"], SPECIAL_TOKEN_SURFACES, strict=True):
        expected_id = SPECIAL_TOKEN_SURFACES.index(surface)
        if tokenizer.token_to_id(surface) != expected_id:
            raise AssertionError(f"special token {role} ({surface!r}) did not get id {expected_id}")

    artifact_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(tokenizer_path))
    tokenizer_sha256 = sha256_file(tokenizer_path)

    manifest_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "artifact_type": "kapampangan_unigram_ablation",
        "algorithm": "unigram_lm",
        "trainer_library": "tokenizers.trainers.UnigramTrainer",
        "trainer_library_version": tokenizers.__version__,
        "not_nllb_tokenizer": True,
        "purpose": (
            "Isolates the Unigram-LM-vs-BPE algorithm effect from the vocabulary-size "
            "and corpus-exposure confound in the native-NLLB comparison. Trained on "
            "this project's own corpus, matched vocabulary size, matched character "
            "inventory, matched special tokens -- only the subword algorithm differs "
            "from the local Plain-BPE condition."
        ),
        "vocabulary_size": tokenizer.get_vocab_size(),
        "target_vocabulary_size": vocab_size,
        "special_tokens": SPECIAL_TOKEN_SURFACES,
        "character_inventory_size": len(characters),
        "trained_on": (
            "experiments/expanded_morphology_v4/runs/prepared/plain-training-stream.jsonl"
        ),
        "trained_on_word_types": total_types,
        "trained_on_occurrences": total_occurrences,
        "trained_on_stream_sha256": plain_stream_sha256,
        "trained_on_stream_matches_plain_bpe_condition": (
            plain_stream_sha256 == prepared_manifest.get("plain_stream_sha256")
        ),
        "pre_tokenizer_at_training": "none (each stream surface is already an atomic pretoken)",
        "reproducibility": (
            "NOT verified byte-reproducible across independent runs, unlike every other "
            "artifact in this repository. Empirically, two independent training runs on "
            "identical input (including single-threaded, RAYON_NUM_THREADS=1) produced "
            "different tokenizer.json content. This is a characteristic of the "
            "third-party tokenizers-library Unigram/EM trainer, not of this project's "
            "own deterministic BPE trainers. This artifact is one frozen trained "
            "instance, fingerprinted below."
        ),
        "tokenizer_file": tokenizer_path.name,
        "tokenizer_sha256": tokenizer_sha256,
    }
    manifest = {**manifest_body, "artifact_fingerprint": fingerprint(manifest_body)}
    write_json(manifest_path, manifest)

    print(
        f"Trained vocabulary {tokenizer.get_vocab_size()} ({total_types} word types, "
        f"{total_occurrences} occurrences)"
    )
    print(f"Wrote {tokenizer_path}")
    print(f"Wrote {manifest_path}")


def main() -> int:
    if not PLAIN_STREAM_PATH.exists():
        raise SystemExit(
            f"{PLAIN_STREAM_PATH} not found; run `python run_experiment.py prepare` "
            "for this experiment first."
        )
    before = _snapshot_other_artifacts()

    rows = _load_stream()
    total_types = len(rows)
    total_occurrences = sum(freq for _, freq in rows)
    characters = sorted(
        {c for surface, _ in rows for c in surface}, key=lambda v: v.encode("utf-8")
    )
    prepared_manifest: Any = (
        json.loads(PREPARED_MANIFEST_PATH.read_text(encoding="utf-8-sig"))
        if PREPARED_MANIFEST_PATH.exists()
        else {}
    )
    plain_stream_sha256 = sha256_file(PLAIN_STREAM_PATH)

    for vocab_size in TARGET_VOCAB_SIZES:
        _train_one_size(
            vocab_size,
            rows,
            characters,
            total_types,
            total_occurrences,
            plain_stream_sha256,
            prepared_manifest,
        )

    after = _snapshot_other_artifacts()
    if before != after:
        raise AssertionError(
            "training the unigram ablation changed an existing v4 plain/penalty artifact"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
