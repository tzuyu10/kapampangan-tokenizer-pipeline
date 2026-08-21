from kapampangan_mt.data.clean import CleanConfig, clean_pairs
from kapampangan_mt.data.split import stratified_split


def test_cleaning_drops_and_logs():
    pairs = [("Kinan ne ing pamangan.", "Kinain niya ang pagkain."),
             ("Kinan ne ing pamangan.", "Kinain niya ang pagkain."),   # duplicate
             ("", "wala"),                                             # empty
             ("a b", "x y z a b c d e f g h i j k l"),                 # length ratio
             ("call 09171234567 now", "tawag 09171234567 ngayon")]     # PII redacted
    kept, rep = clean_pairs(pairs, CleanConfig())
    d = rep.as_dict()
    assert d["dropped"]["duplicate"] == 1
    assert d["dropped"]["empty"] == 1
    assert d["dropped"]["length_ratio"] == 1
    assert all("09171234567" not in s for s, _ in kept)
    assert len(rep.kept_indices) == rep.kept


def test_split_is_deterministic_and_disjoint():
    pairs = [(f"salita {i} keni", f"salita {i} dito") for i in range(200)]
    a = stratified_split(pairs, seed=13)
    b = stratified_split(pairs, seed=13)
    assert a["indices"] == b["indices"]
    idx = a["indices"]
    assert not (set(idx["train"]) & set(idx["val"]))
    assert not (set(idx["train"]) & set(idx["test"]))
    assert len(idx["train"]) + len(idx["val"]) + len(idx["test"]) == 200
    assert 0.75 <= len(idx["train"]) / 200 <= 0.85
