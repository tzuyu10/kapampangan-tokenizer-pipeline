"""Phase 5 step 2: build the self-contained Colab bundle.

The notebook runs in Colab with NO project code. Everything it needs is
pre-computed here:

  data/bundle/{train,dev,test}.jsonl
      one row per pair: {pam_text, fil_text, tier, claude_review,
                         morphbpe_ids, penalty8_ids}
      *_ids are this project's MorphBPE runtime-tokenizer output for the
      Kapampangan side (ids already include <s>/</s>; ids are in [0, 6080)).
  data/bundle/meta.json
      vocab sizes, pad id, artifact fingerprints, split SHA-256s, and the
      NLLB settings the notebook should use.

The NLLB-native baseline needs no pre-tokenisation -- the notebook tokenises
`pam_text` with NLLB's own tokenizer there.

Runs in this project's `.venv` (uses `kapampangan_morphbpe.runtime_bridge`).
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT / "runtime"))

from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import read_json  # noqa: E402

DATA_DIR = EXPERIMENT_ROOT / "data"
BUNDLE_DIR = DATA_DIR / "bundle"
V4_ART = REPO_ROOT / "experiments/expanded_morphology_v4/artifacts"
MORPHBPE_ART = V4_ART / "morphbpe/candidates/vocab-6080"
PENALTY8_ART = V4_ART / "penalty-8/candidates/vocab-6080"


def artifact_fingerprint(art: Path) -> str:
    manifest = read_json(art / "tokenizer-manifest.json")
    assert isinstance(manifest, dict)
    return str(manifest.get("artifact_fingerprint"))


def main() -> int:
    morphbpe = load_runtime_tokenizer(MORPHBPE_ART)
    penalty8 = load_runtime_tokenizer(PENALTY8_ART)
    if morphbpe.vocabulary_size != 6080 or penalty8.vocabulary_size != 6080:
        raise SystemExit("expected vocab-6080 artifacts")

    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    split_hashes: dict[str, str] = {}
    counts: dict[str, int] = {}
    for split in ("train", "dev", "test"):
        src = DATA_DIR / f"{split}.csv"
        if not src.exists():
            raise SystemExit(f"missing {src}; run build_split.py first")
        with src.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        out = BUNDLE_DIR / f"{split}.jsonl"
        with out.open("w", encoding="utf-8", newline="\n") as handle:
            for r in rows:
                pam = r["pam_text"]
                rec = {
                    "pam_text": pam,
                    "fil_text": r["fil_text"],
                    "tier": r["tier"],
                    "claude_review": r["claude_review"],
                    "morphbpe_ids": list(morphbpe.encode(pam, add_special_tokens=True).ids),
                    "penalty8_ids": list(penalty8.encode(pam, add_special_tokens=True).ids),
                }
                handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
        split_hashes[split] = hashlib.sha256(out.read_bytes()).hexdigest()
        counts[split] = len(rows)

    meta = {
        "task": "Kapampangan -> Filipino (tgl_Latn) NLLB-200-distilled-600M fine-tune",
        "conditions": ["nllb_native", "morphbpe", "penalty8"],
        "seeds": [0, 1, 2],
        "training": {
            "trainable": "encoder input embedding only (nn.Embedding(6080,1024)); "
            "everything else frozen; do NOT call tie_weights() after the swap",
            "note": "matches Phase 4 verification (nllb/phase4-architecture-verification.md)",
        },
        "source_vocab_size_morphbpe": 6080,
        "source_pad_id_morphbpe": 0,
        "nllb": {
            "model": "facebook/nllb-200-distilled-600M",
            "target_lang": "tgl_Latn",
            "native_baseline_source_lang": "tgl_Latn",
            "decoder_start_token_id": 2,
            "pad_token_id": 1,
        },
        "artifact_fingerprints": {
            "morphbpe": artifact_fingerprint(MORPHBPE_ART),
            "penalty8": artifact_fingerprint(PENALTY8_ART),
        },
        "split_counts": counts,
        "split_sha256": split_hashes,
        "split_manifest": "reports/split-manifest.json",
        "label": "ALL SILVER training data. See split-manifest.json.",
        "rights_note": (
            "train/dev contain PLD-derived pairs (redistribution rights "
            "unresolved) + native-authored story pairs (author = the user) + "
            "gold_v1. Review before uploading to Colab."
        ),
    }
    (BUNDLE_DIR / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({"counts": counts, "split_sha256": split_hashes}, indent=2))
    print(f"bundle -> {BUNDLE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
