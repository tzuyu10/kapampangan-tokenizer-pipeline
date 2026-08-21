"""Fertility Rate — thesis eq. (1):  FR = T / W.

``T`` = tokens produced, ``W`` = source words.  Two aggregations are reported
because they answer different questions and the thesis does not distinguish
them:

corpus-level (``fertility_corpus``)
    sum(T) / sum(W).  This is the number to put in Table 2.
per-sentence  (``fertility_per_sentence``)
    T_i / W_i for each sentence.  These are the paired observations fed to the
    paired-samples t-test in Research Question 3.

Caveat to state in Chapter 4: fertility falls monotonically as vocabulary size
rises, so a low FR against NLLB's 256k multilingual vocabulary is *not* by
itself evidence of morphological awareness.  Compare against the matched
plain-BPE control at the same vocabulary size.
"""
from __future__ import annotations


def fertility_per_sentence(tokenizer, sentences: list[str]) -> list[float]:
    out = []
    for s in sentences:
        t, w = tokenizer.fertility(s)
        out.append(t / w if w else 0.0)
    return out


def fertility_corpus(tokenizer, sentences: list[str]) -> dict:
    T = W = 0
    for s in sentences:
        t, w = tokenizer.fertility(s)
        T += t
        W += w
    per_sent = fertility_per_sentence(tokenizer, sentences)
    n = len(per_sent) or 1
    mean = sum(per_sent) / n
    var = sum((x - mean) ** 2 for x in per_sent) / (n - 1) if n > 1 else 0.0
    return {
        "fertility_corpus": T / W if W else 0.0,
        "fertility_sentence_mean": mean,
        "fertility_sentence_sd": var ** 0.5,
        "total_tokens": T,
        "total_words": W,
        "n_sentences": len(sentences),
    }
