"""Phase 5 step 2: build the self-contained Colab bundle.

The notebook runs in Colab with NO project code. Everything it needs is
pre-computed here:

  data/bundle/{train,dev,test}.jsonl
      one row per pair: {pam_text, fil_text, tier, claude_review,
                         morphbpe_ids, penalty8_ids, unigram_ids}
      *_ids are the Kapampangan side tokenised at vocab 6,080 with <s>/</s>
      included, ids in [0, 6080):
        morphbpe_ids  -- paper-aligned hard-constrained MorphBPE
        penalty8_ids  -- weighted MorphBPE (crossing penalty 8)
        unigram_ids   -- the Unigram-LM ablation: NLLB's own subword
                         algorithm, trained from scratch on THIS project's
                         Kapampangan corpus at the matched 6,080 vocab,
                         matched character inventory + special tokens. The
                         fair "NLLB approach, trained on Kapampangan"
                         control -- only the subword algorithm differs from
                         MorphBPE. Tokenised the project's way (pretokenise,
                         then Unigram per segment) so it is directly
                         comparable.
  data/bundle/meta.json
      vocab sizes, pad id, artifact fingerprints, split SHA-256s, and the
      NLLB settings the notebook should use.

The `nllb_native` / `nllb_zeroshot` conditions need no pre-tokenisation --
the notebook tokenises `pam_text` with NLLB's own tokenizer there.

Runs in this project's `.venv` (uses `kapampangan_morphbpe.*` + the
`tokenizers` library from the `nllb-baseline` extra).
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

from kapampangan_morphbpe.normalization import normalize_text  # noqa: E402
from kapampangan_morphbpe.pretokenizer import pretokenize_normalized  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer  # noqa: E402
from kapampangan_morphbpe.serialization import read_json  # noqa: E402

DATA_DIR = EXPERIMENT_ROOT / "data"
BUNDLE_DIR = DATA_DIR / "bundle"
V4_ART = REPO_ROOT / "experiments/expanded_morphology_v4/artifacts"
MORPHBPE_ART = V4_ART / "morphbpe/candidates/vocab-6080"
PENALTY8_ART = V4_ART / "penalty-8/candidates/vocab-6080"
UNIGRAM_JSON = V4_ART / "unigram-ablation/vocab-6080/tokenizer.json"
UNIGRAM_MANIFEST = V4_ART / "unigram-ablation/vocab-6080/unigram-ablation-manifest.json"

BOS_ID, EOS_ID = 2, 3  # <s>, </s> -- shared special-token ids across all 6,080 vocabs


def artifact_fingerprint(art: Path) -> str:
    manifest = read_json(art / "tokenizer-manifest.json")
    assert isinstance(manifest, dict)
    return str(manifest.get("artifact_fingerprint"))


def main() -> int:
    from tokenizers import Tokenizer

    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    morphbpe = load_runtime_tokenizer(MORPHBPE_ART)
    penalty8 = load_runtime_tokenizer(PENALTY8_ART)
    unigram = Tokenizer.from_file(str(UNIGRAM_JSON))
    if morphbpe.vocabulary_size != 6080 or penalty8.vocabulary_size != 6080:
        raise SystemExit("expected vocab-6080 MorphBPE artifacts")
    if unigram.get_vocab_size() != 6080:
        raise SystemExit("expected vocab-6080 unigram ablation")
    if unigram.token_to_id("<s>") != BOS_ID or unigram.token_to_id("</s>") != EOS_ID:
        raise SystemExit("unigram ablation special-token ids differ from 2/3")

    def unigram_ids(text: str) -> list[int]:
        """Pretokenise the project's way, then Unigram-encode each segment
        (matches how the MorphBPE runtime consumes a sentence), + <s>/</s>."""
        ids: list[int] = [BOS_ID]
        for piece in pretokenize_normalized(normalize_text(text)):
            ids.extend(unigram.encode(piece.surface).ids)
        ids.append(EOS_ID)
        return ids

    # id-ordered token strings per condition, so the notebook can WARM-START
    # each new 6,080-row embedding from the mean of NLLB's own sub-token
    # embeddings for that string (standard vocab-replacement init).
    def morphbpe_vocab(art: Path) -> list[str]:
        doc = read_json(art / "vocab.json")
        assert isinstance(doc, dict)
        toks = doc["tokens"]
        assert isinstance(toks, list) and len(toks) == 6080
        out = [""] * 6080
        for entry in toks:
            out[int(entry["id"])] = str(entry["token"])
        return out

    unigram_vocab = [""] * 6080
    for tok, idx in unigram.get_vocab().items():
        unigram_vocab[idx] = tok
    vocab = {
        "morphbpe": morphbpe_vocab(MORPHBPE_ART),
        "penalty8": morphbpe_vocab(PENALTY8_ART),
        "unigram6080": unigram_vocab,
    }
    (BUNDLE_DIR / "vocab.json").write_text(
        json.dumps(vocab, ensure_ascii=False) + "\n", encoding="utf-8"
    )

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
                    "unigram_ids": unigram_ids(pam),
                }
                handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
        split_hashes[split] = hashlib.sha256(out.read_bytes()).hexdigest()
        counts[split] = len(rows)

    unigram_meta = read_json(UNIGRAM_MANIFEST)
    assert isinstance(unigram_meta, dict)

    meta = {
        "task": "Kapampangan -> Filipino (tgl_Latn) NLLB-200-distilled-600M fine-tune",
        "conditions": ["morphbpe", "penalty8", "unigram6080"],
        "reference_condition": "nllb_zeroshot (no training)",
        "comparison": {
            "fair_headline": "morphbpe / penalty8 vs unigram6080 -- same vocab (6,080), "
            "same Kapampangan corpus, same warm-started-embedding recipe; only the "
            "subword algorithm differs (morphology-constrained BPE vs Unigram-LM).",
            "reference": "nllb_zeroshot -- the pretrained off-the-shelf NLLB-200 "
            "tokenizer named in the thesis proposal (Scope & Limitation, p.15). "
            "Trained nllb_native was dropped for v1 (256K trainable embedding OOMs a T4).",
        },
        "seeds": [0],
        "seeds_note": "1 seed for the first warm-start pass; add [1, 2] once a "
        "condition beats nllb_zeroshot and the comparison is worth error bars.",
        "training": {
            "trainable": "encoder input embedding only -- nn.Embedding(6080,1024), "
            "WARM-STARTED from the mean of NLLB's own sub-token embeddings for each "
            "token string (see data/bundle/vocab.json). Everything else frozen; do "
            "NOT call tie_weights() after the swap.",
            "hyperparams": {
                "batch": 16,
                "epochs": 15,
                "patience": 4,
                "lr": 3e-4,
                "select_on": "dev loss (cheap); generation eval only at the end",
            },
            "note": "matches Phase 4 verification (nllb/phase4-architecture-verification.md). "
            "The random-init recipe (first run) collapsed to chrF++ ~10 vs zero-shot 33.6.",
        },
        "vocab_file": "vocab.json  {condition: [id-ordered token strings]}",
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
            "unigram6080": str(unigram_meta.get("artifact_fingerprint")),
        },
        "unigram6080_note": (
            "NOT NLLB's tokenizer file; a fresh Unigram-LM model trained on this "
            "project's Kapampangan corpus (train_unigram_ablation.py). Disclosed "
            "limitation: the tokenizers-library Unigram trainer is not byte-"
            "reproducible; this is one frozen instance."
        ),
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
