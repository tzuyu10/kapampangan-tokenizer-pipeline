import pytest
from kapampangan_mt.metrics.boundary_f1 import boundary_f1_corpus, word_boundaries_from_segments
from kapampangan_mt.metrics.consistency_f1 import morphological_consistency_f1
from kapampangan_mt.metrics.fertility import fertility_corpus
from kapampangan_mt.stats import holm_bonferroni, paired_report


class FakeTok:
    """Deterministic stub so the metric maths is testable without training."""
    def __init__(self, table): self.table = table
    def tokenize_word(self, w): return self.table.get(w, [w])
    def tokenize(self, t): return [p for w in t.split() for p in self.tokenize_word(w)]
    def boundaries(self, w):
        out, pos = set(), 0
        for p in self.tokenize_word(w)[:-1]:
            pos += len(p.replace("▁", "")); out.add(pos)
        return out
    def fertility(self, t): return len(self.tokenize(t)), len(t.split())
    vocab_size = 10


def test_boundaries_from_segments():
    assert word_boundaries_from_segments(["ka", "pampang", "an"]) == {2, 9}


def test_perfect_tokenizer_scores_one():
    tok = FakeTok({"kapampangan": ["ka", "pampang", "an"]})
    gold = [("kapampangan", {2, 9}, 1)]
    assert boundary_f1_corpus(tok, gold)["mbf1_micro"] == pytest.approx(1.0)


def test_over_segmentation_hurts_precision_not_recall():
    tok = FakeTok({"kapampangan": list("kapampangan")})
    gold = [("kapampangan", {2, 9}, 1)]
    r = boundary_f1_corpus(tok, gold)
    assert r["boundary_recall"] == pytest.approx(1.0)
    assert r["boundary_precision"] < 0.3


def test_fertility_is_tokens_over_words():
    tok = FakeTok({"kinan": ["k", "in", "an"], "bale": ["bale"]})
    assert fertility_corpus(tok, ["kinan bale"])["fertility_corpus"] == pytest.approx(2.0)


def test_mcf1_rewards_shared_root_tokens():
    good = FakeTok({"kinan": ["k", "in", "an"], "kuman": ["k", "um", "an"],
                    "bale": ["bale"]})
    bad = FakeTok({"kinan": ["kinan"], "kuman": ["kuman"], "bale": ["bale"]})
    gold = {"kinan": ["kan"], "kuman": ["kan"], "bale": ["bale"]}
    words = list(gold)
    g = morphological_consistency_f1(good, words, gold, min_token_len=2)
    b = morphological_consistency_f1(bad, words, gold, min_token_len=2)
    assert g["mcf1"] > b["mcf1"]


def test_holm_is_stricter_than_uncorrected():
    reps = [paired_report([1.0, 1.1, 1.2, 1.3, 1.15], [1.0, 1.05, 1.1, 1.2, 1.1], f"m{i}")
            for i in range(5)]
    out = holm_bonferroni(reps)
    assert all(r["holm_threshold"] <= 0.05 for r in out)
    assert {r["holm_rank"] for r in out} == {1, 2, 3, 4, 5}
