"""Vocabulary-size selection by morphological distance (thesis p. 43).

"The vocabulary size is selected by computing morphological distance scores on
a validation set, ensuring that the tokenizer achieves meaningful morpheme
boundary alignment without unnecessary over-segmentation."

Asgari et al. (2025) state the criterion but the proposal does not give a
formula, so one is fixed here and must be written into Chapter 3:

    MorphDist(V) = mean over validation words of
                   1 - |B_pred ∩ B_gold| / |B_pred ∪ B_gold|      (Jaccard distance)

Words with no internal boundary in either set contribute 0.  Ties are broken
toward the *smaller* vocabulary.  ``objective="dist+fertility"`` adds a
fertility penalty, which is what "without unnecessary over-segmentation"
means operationally:

    J(V) = MorphDist(V) + lambda * max(0, FR(V) - FR_target)

Run this on the **validation** split only.  Selecting V on the test split
leaks and invalidates RQ1.
"""
from __future__ import annotations

from dataclasses import dataclass

from .morph_bpe import MorphBPEConfig, MorphBPETrainer
from .tokenizer import BYTE_TOKENS, RESERVED, KapampanganTokenizer


def morphological_distance(tokenizer, gold: dict[str, set[int]]) -> float:
    total = 0.0
    for word, gold_b in gold.items():
        pred_b = tokenizer.boundaries(word)
        union = pred_b | gold_b
        if not union:
            continue
        total += 1.0 - len(pred_b & gold_b) / len(union)
    return total / max(len(gold), 1)


@dataclass
class VocabSearchResult:
    vocab_size: int
    morph_distance: float
    fertility: float
    objective: float
    tokenizer: KapampanganTokenizer


def search_vocab_size(
    word_segmentations: dict[str, list[str]],
    word_freqs: dict[str, int],
    val_gold_boundaries: dict[str, set[int]],
    val_sentences: list[str],
    candidates: list[int] = (2000, 4000, 8000, 16000, 32000),
    constrain: bool = True,
    objective: str = "dist+fertility",
    fertility_target: float = 1.6,
    lam: float = 0.5,
    verbose: bool = True,
) -> tuple[VocabSearchResult, list[VocabSearchResult]]:
    reserved = len(RESERVED) + len(BYTE_TOKENS)
    results: list[VocabSearchResult] = []
    for V in sorted(candidates):
        cfg = MorphBPEConfig(vocab_size=V, constrain_to_morpheme_boundaries=constrain)
        model = MorphBPETrainer(cfg).train(
            word_segmentations, word_freqs, reserved=reserved, verbose=False
        )
        tok = KapampanganTokenizer.from_model(model)
        dist = morphological_distance(tok, val_gold_boundaries)
        T = W = 0
        for s in val_sentences:
            t, w = tok.fertility(s)
            T += t; W += w
        fert = T / W if W else 0.0
        obj = dist + (lam * max(0.0, fert - fertility_target)
                      if objective == "dist+fertility" else 0.0)
        results.append(VocabSearchResult(V, dist, fert, obj, tok))
        if verbose:
            print(f"  V={V:>6}  morph_dist={dist:.4f}  fertility={fert:.3f}  J={obj:.4f}")
    best = min(results, key=lambda r: (r.objective, r.vocab_size))
    return best, results
