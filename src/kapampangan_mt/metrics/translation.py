"""BLEU (eq. 8) and chrF++ (eq. 9) via sacreBLEU.

chrF++ is ``chrF`` with word n-grams: ``word_order=2``.  Passing
``word_order=0`` gives plain chrF and would not match the thesis.

Sentence-level BLEU needs smoothing — an unsmoothed sentence with no 4-gram
match scores exactly 0, which makes the paired differences a spike-at-zero
distribution rather than anything a t-test likes.  ``exp`` smoothing
(Chen & Cherry 2014 method 3) is used; state this in Chapter 3.
"""
from __future__ import annotations


def _metrics(lowercase: bool = False):
    from sacrebleu.metrics import BLEU, CHRF

    return (
        BLEU(lowercase=lowercase, tokenize="13a", effective_order=True),
        CHRF(char_order=6, word_order=2, beta=2),  # chrF++
    )


def corpus_scores(hypotheses: list[str], references: list[str],
                  lowercase: bool = False) -> dict:
    bleu, chrf = _metrics(lowercase)
    b = bleu.corpus_score(hypotheses, [references])
    c = chrf.corpus_score(hypotheses, [references])
    return {
        "bleu": b.score, "bleu_signature": str(bleu.get_signature()),
        "chrf++": c.score, "chrf_signature": str(chrf.get_signature()),
        "n": len(hypotheses),
    }


def sentence_scores(hypotheses: list[str], references: list[str],
                    lowercase: bool = False) -> dict[str, list[float]]:
    """Per-sentence BLEU and chrF++ — the paired observations for RQ4."""
    bleu, chrf = _metrics(lowercase)
    return {
        "bleu": [bleu.sentence_score(h, [r]).score for h, r in zip(hypotheses, references)],
        "chrf++": [chrf.sentence_score(h, [r]).score for h, r in zip(hypotheses, references)],
    }
