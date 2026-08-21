"""Morphological Consistency F1 — thesis eqs. (5)-(7).

    P_c = |ST ∩ SM| / |ST|     R_c = |SM ∩ ST| / |SM|     MCF1 = 2 P R /(P+R)

where, over all unordered pairs of word types in the evaluation set,
``SM`` = pairs that share at least one morpheme and ``ST`` = pairs that share
at least one token.

Two definitional gaps in the thesis are closed here and MUST be reported in
Chapter 3, because the metric is meaningless without them:

1. **What counts as "sharing a token".**  If every shared token counts, then
   any two words sharing the letter "a" are an ST pair and *both* tokenizers
   score near-zero precision.  We therefore ignore tokens shorter than
   ``min_token_len`` (default 2) and tokens in ``ignore_tokens``.  Report the
   setting; results are not comparable across different settings.

2. **What counts as "sharing a morpheme".**  Function morphemes (``-an``,
   ``ma-``, clitics) appear in a huge share of words and would swamp the pair
   sets.  ``content_morphemes_only=True`` restricts SM to *root* morphemes,
   which is what "words sharing the same morphemes" means linguistically
   (kinan / kuman / mangan all share the root kan).

Implementation is exact, not sampled: incidence matrices + one boolean matmul.
With W word types the pair sets are O(W^2); ``max_types`` caps W (default
5,000 -> 12.5M pairs, ~1 s, ~25 MB).
"""
from __future__ import annotations

from collections import Counter

import numpy as np

DEFAULT_IGNORE = {"▁", "<unk>", "</s>", "<s>", "<pad>"}


def _incidence(items_per_word: list[list[str]]) -> np.ndarray:
    index: dict[str, int] = {}
    for items in items_per_word:
        for it in items:
            index.setdefault(it, len(index))
    M = np.zeros((len(items_per_word), max(len(index), 1)), dtype=bool)
    for i, items in enumerate(items_per_word):
        for it in items:
            M[i, index[it]] = True
    return M


def _pair_matrix(M: np.ndarray) -> np.ndarray:
    """Boolean W x W matrix: True where two words share >= 1 feature."""
    shared = (M.astype(np.uint16) @ M.astype(np.uint16).T) > 0
    np.fill_diagonal(shared, False)
    return np.triu(shared)


def morphological_consistency_f1(
    tokenizer,
    words: list[str],
    gold_morphemes: dict[str, list[str]],
    *,
    min_token_len: int = 2,
    ignore_tokens: set[str] | None = None,
    content_morphemes_only: bool = True,
    root_kinds: tuple[str, ...] = ("root",),
    max_types: int = 5000,
    seed: int = 13,
) -> dict:
    """Compute MCF1 for one tokenizer.

    Parameters
    ----------
    words:
        Evaluation word types (deduplicated inside).
    gold_morphemes:
        ``word -> [morpheme labels]``.  Use canonical labels so allomorphs of
        one morpheme (pang-/pam-/pan-) collapse.  When
        ``content_morphemes_only`` is set, pass ``{word: [root_labels]}``.
    """
    ignore = (ignore_tokens or set()) | DEFAULT_IGNORE
    types = sorted({w for w in words if w in gold_morphemes})
    if len(types) > max_types:
        rng = np.random.default_rng(seed)
        idx = rng.choice(len(types), size=max_types, replace=False)
        types = [types[i] for i in sorted(idx)]
    if len(types) < 2:
        return {"mcf1": 0.0, "precision_c": 0.0, "recall_c": 0.0,
                "n_types": len(types), "ST": 0, "SM": 0, "ST_and_SM": 0}

    tok_lists, mor_lists = [], []
    for w in types:
        toks = [
            t.replace("▁", "") for t in tokenizer.tokenize_word(w)
        ]
        toks = [t for t in toks if t and t not in ignore and len(t) >= min_token_len]
        tok_lists.append(toks)
        mor_lists.append(list(gold_morphemes[w]))

    ST = _pair_matrix(_incidence(tok_lists))
    SM = _pair_matrix(_incidence(mor_lists))
    inter = int(np.count_nonzero(ST & SM))
    n_st, n_sm = int(np.count_nonzero(ST)), int(np.count_nonzero(SM))
    P = inter / n_st if n_st else 0.0
    R = inter / n_sm if n_sm else 0.0
    F1 = 2 * P * R / (P + R) if (P + R) else 0.0
    return {
        "mcf1": F1, "precision_c": P, "recall_c": R,
        "n_types": len(types), "ST": n_st, "SM": n_sm, "ST_and_SM": inter,
        "min_token_len": min_token_len,
        "content_morphemes_only": content_morphemes_only,
    }


def _feature_matrices(tokenizer, types, gold_morphemes, min_token_len, ignore):
    tok_lists, mor_lists = [], []
    for w in types:
        toks = [t.replace("\u2581", "") for t in tokenizer.tokenize_word(w)]
        tok_lists.append([t for t in toks
                          if t and t not in ignore and len(t) >= min_token_len])
        mor_lists.append(list(gold_morphemes[w]))
    return _incidence(tok_lists), _incidence(mor_lists)


def bootstrap_mcf1(
    tokenizer_a, tokenizer_b, words, gold_morphemes, n_resamples: int = 1000,
    seed: int = 13, max_types: int = 1200, min_token_len: int = 2,
    ignore_tokens: set[str] | None = None, **_ignored,
) -> dict:
    """Paired bootstrap over word types for MCF1.

    MCF1 is a *set-level* statistic over word pairs: it has no per-sentence
    value, so the paired-samples t-test over 1,300 test sentences prescribed in
    the thesis cannot be applied to it (Issue S-1). Resampling word types is
    the correct paired procedure.

    Implementation note: the token/morpheme incidence matrices are built ONCE
    and each resample only re-indexes them. Rebuilding them per resample makes
    this metric take hours on a 20k-type corpus.
    """
    ignore = (ignore_tokens or set()) | DEFAULT_IGNORE
    rng = np.random.default_rng(seed)
    types = sorted({w for w in words if w in gold_morphemes})
    if len(types) > max_types:
        idx = rng.choice(len(types), size=max_types, replace=False)
        types = [types[i] for i in sorted(idx)]
    if len(types) < 2:
        return {"mean_diff": 0.0, "ci_low": 0.0, "ci_high": 0.0,
                "p_value": 1.0, "n_resamples": 0, "n_types": len(types)}

    Ta, M = _feature_matrices(tokenizer_a, types, gold_morphemes, min_token_len, ignore)
    Tb, _ = _feature_matrices(tokenizer_b, types, gold_morphemes, min_token_len, ignore)
    STa, STb, SM = _pair_matrix(Ta), _pair_matrix(Tb), _pair_matrix(M)
    STa, STb, SM = (X | X.T for X in (STa, STb, SM))
    STa, STb, SM = np.asarray(STa), np.asarray(STb), np.asarray(SM)

    def f1(ST, sel):
        st = ST[np.ix_(sel, sel)]
        sm = SM[np.ix_(sel, sel)]
        tri = np.triu(np.ones_like(st), 1).astype(bool)
        st, sm = st & tri, sm & tri
        inter = int(np.count_nonzero(st & sm))
        n_st, n_sm = int(np.count_nonzero(st)), int(np.count_nonzero(sm))
        p = inter / n_st if n_st else 0.0
        r = inter / n_sm if n_sm else 0.0
        return 2 * p * r / (p + r) if (p + r) else 0.0

    n = len(types)
    diffs = np.empty(n_resamples)
    for k in range(n_resamples):
        sel = rng.integers(0, n, n)
        diffs[k] = f1(STa, sel) - f1(STb, sel)
    return {
        "mean_diff": float(diffs.mean()),
        "ci_low": float(np.percentile(diffs, 2.5)),
        "ci_high": float(np.percentile(diffs, 97.5)),
        "p_value": float(2 * min((diffs <= 0).mean(), (diffs >= 0).mean())),
        "n_resamples": n_resamples,
        "n_types": n,
    }
