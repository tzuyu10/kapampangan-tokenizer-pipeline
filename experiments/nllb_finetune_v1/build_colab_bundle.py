"""Phase 5 step 2: build the self-contained Colab bundle.

The notebook runs in Colab with NO project code. Everything it needs is
pre-computed here:

  data/bundle/{train,dev,test_bible,test_ood}.jsonl
      one row per pair: {pam_text, fil_text, tier, claude_review,
                         morphbpe_ids, penalty8_ids, unigram_ids, bpe_ids}
      test_bible = held-out Bible chapters (in-domain); test_ood = whole
      native-authored stories + gold_v1 sentences (register transfer).
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
        bpe_ids       -- the plain (unconstrained) BPE candidate from the
                         same expanded_morphology_v4 grid as morphbpe/
                         penalty8: identical merge algorithm, same corpus,
                         same 6,080 vocab, but with NO morphology-boundary
                         penalty during training. Isolates the morphology
                         constraint itself (same algorithm family as
                         morphbpe/penalty8; only the constraint differs),
                         complementing unigram6080 (same constraint-free
                         setting but a different algorithm family).
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
PLAIN_ART = V4_ART / "plain/candidates/vocab-6080"
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
    plain = load_runtime_tokenizer(PLAIN_ART)
    unigram = Tokenizer.from_file(str(UNIGRAM_JSON))
    if morphbpe.vocabulary_size != 6080 or penalty8.vocabulary_size != 6080:
        raise SystemExit("expected vocab-6080 MorphBPE artifacts")
    if plain.vocabulary_size != 6080:
        raise SystemExit("expected vocab-6080 plain BPE artifact")
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
        "bpe6080": morphbpe_vocab(PLAIN_ART),
        "unigram6080": unigram_vocab,
    }
    (BUNDLE_DIR / "vocab.json").write_text(
        json.dumps(vocab, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    split_hashes: dict[str, str] = {}
    counts: dict[str, int] = {}
    for split in ("train", "dev", "test_bible", "test_ood"):
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
                    "bpe_ids": list(plain.encode(pam, add_special_tokens=True).ids),
                    "unigram_ids": unigram_ids(pam),
                }
                handle.write(json.dumps(rec, ensure_ascii=False) + "\n")
        split_hashes[split] = hashlib.sha256(out.read_bytes()).hexdigest()
        counts[split] = len(rows)

    unigram_meta = read_json(UNIGRAM_MANIFEST)
    assert isinstance(unigram_meta, dict)

    meta = {
        "task": "Kapampangan -> Filipino (tgl_Latn) NLLB-200-distilled-600M fine-tune",
        "conditions": ["morphbpe", "penalty8", "bpe6080", "unigram6080"],
        "reference_condition": "nllb_zeroshot (no training)",
        "comparison": {
            "fair_headline": "morphbpe / penalty8 vs unigram6080 -- same vocab (6,080), "
            "same Kapampangan corpus, same warm-started-embedding recipe; only the "
            "subword algorithm differs (morphology-constrained BPE vs Unigram-LM).",
            "constraint_ablation": "morphbpe / penalty8 vs bpe6080 -- same vocab (6,080), "
            "same Kapampangan corpus, same BPE merge algorithm, same warm-started-"
            "embedding recipe; only the morphology-boundary crossing penalty differs "
            "(constrained/weighted vs none). Isolates the morphology constraint itself, "
            "holding the algorithm family fixed -- the cleanest test of the thesis's "
            "actual claim.",
            "reference": "nllb_zeroshot -- the pretrained off-the-shelf NLLB-200 "
            "tokenizer named in the thesis proposal (Scope & Limitation, p.15). "
            "Trained nllb_native was dropped for v1 (256K trainable embedding OOMs a T4).",
        },
        "seeds": [0, 1, 2],
        "seeds_note": "3 seeds from the start -- the training set is now ~3,600 "
        "pairs (Bible-primary refresh 2026-09-03), past the point where a single "
        "seed is enough for a defensible tokenizer comparison.",
        "test_sets": {
            "test_bible": "IN-DOMAIN -- whole held-out Bible chapters. The "
            "headline number; matches the proposal's primary dataset.",
            "test_ood": "OUT-OF-DOMAIN -- native-authored stories + gold_v1 "
            "sentences. Register-transfer number (train is ~71% religious).",
        },
        "training": {
            "trainable": "encoder input embedding only -- nn.Embedding(6080,1024), "
            "WARM-STARTED from the mean of NLLB's own sub-token embeddings for each "
            "token string (see data/bundle/vocab.json). Everything else frozen; do "
            "NOT call tie_weights() after the swap.",
            "hyperparams": {
                "batch": 8,
                "epochs": 10,
                "patience": 3,
                "lr": 3e-4,
                "max_new_tokens": 160,
                "select_on": "dev loss (cheap); generation eval on both test sets only at the end",
                "batch_note": "8 is deliberately conservative for a T4 -- Bible verses are "
                "~40% longer than the old 598-pair set (morphbpe_ids p99 ~140, max 184). "
                "Raise to 16 in meta.json if the runtime has headroom.",
            },
            "note": "matches Phase 4 verification (nllb/phase4-architecture-verification.md). "
            "Warm-start kept from the 2026-09-03 rev (random-init collapsed to chrF++ "
            "~10 vs zero-shot 33.6 at 598 pairs); with ~3,600 pairs the frozen-encoder "
            "recipe may now hold on its own, but warm-start is cheap and de-risks.",
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
            "bpe6080": artifact_fingerprint(PLAIN_ART),
            "unigram6080": str(unigram_meta.get("artifact_fingerprint")),
        },
        "bpe6080_note": (
            "The 'plain' candidate from the expanded_morphology_v4 grid "
            "(tokenizer_selection_v1: intrinsic boundary F1 below every "
            "morphology-aware condition -- the floor of the ranking). Same BPE "
            "merge algorithm and training corpus as morphbpe/penalty8, vocab 6,080, "
            "but trained with NO morphology-boundary crossing penalty."
        ),
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
            "train/dev/test contain: the PLOC Kapampangan<->Tagalog Bible "
            "corpus (~71% of train; provenance via a groupmate, believed "
            "PLOC/DLSU LTL / LGPL but UNCONFIRMED -- redistribution rights "
            "UNRESOLVED), PLD-derived pairs (rights unresolved), native-"
            "authored story pairs (author = the user), gold_v1, and Gemini "
            "AI-generated sentences. Confirm the Bible corpus rights with the "
            "user before uploading to Colab."
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
