"""80/10/10 split with stratification (thesis p. 35).

"the split will be organized so that major morphological patterns and
sentence-length distributions are preserved across the three subsets."

Strata = (length bucket, morphological-complexity bucket, domain).
Complexity = mean number of morphemes per analysable word in the sentence.
Splitting is deterministic given ``seed`` and reported per stratum.
"""
from __future__ import annotations

import random
from collections import defaultdict


def _length_bucket(n_words: int) -> str:
    if n_words <= 5: return "L1"
    if n_words <= 10: return "L2"
    if n_words <= 20: return "L3"
    return "L4"


def _complexity_bucket(mean_morphs: float) -> str:
    if mean_morphs < 1.2: return "M1"
    if mean_morphs < 1.8: return "M2"
    return "M3"


def stratified_split(
    pairs: list[tuple[str, str]],
    segmenter=None,
    domains: list[str] | None = None,
    ratios: tuple[float, float, float] = (0.8, 0.1, 0.1),
    seed: int = 13,
) -> dict:
    assert abs(sum(ratios) - 1.0) < 1e-9
    domains = domains or ["unknown"] * len(pairs)
    rng = random.Random(seed)

    buckets: dict[tuple, list[int]] = defaultdict(list)
    for i, ((src, _), dom) in enumerate(zip(pairs, domains)):
        words = src.split()
        if segmenter is not None and words:
            segs = [segmenter.segment(w) for w in words]
            mean_m = sum(len(s.morphs) for s in segs) / len(segs)
        else:
            mean_m = 1.0
        buckets[(_length_bucket(len(words)), _complexity_bucket(mean_m), dom)].append(i)

    train, val, test = [], [], []
    per_stratum = {}
    for key, idxs in sorted(buckets.items()):
        rng.shuffle(idxs)
        n = len(idxs)
        n_tr = int(round(n * ratios[0]))
        n_va = int(round(n * ratios[1]))
        n_tr = min(n_tr, n)
        n_va = min(n_va, n - n_tr)
        train += idxs[:n_tr]
        val += idxs[n_tr : n_tr + n_va]
        test += idxs[n_tr + n_va :]
        per_stratum["|".join(key)] = {"n": n, "train": n_tr, "val": n_va,
                                      "test": n - n_tr - n_va}

    for part in (train, val, test):
        part.sort()
    return {
        "train": [pairs[i] for i in train],
        "val": [pairs[i] for i in val],
        "test": [pairs[i] for i in test],
        "indices": {"train": train, "val": val, "test": test},
        "per_stratum": per_stratum,
        "seed": seed,
    }
