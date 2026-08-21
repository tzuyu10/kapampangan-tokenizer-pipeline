"""The segmentations the thesis itself names must come out right."""
import pytest


@pytest.mark.parametrize("word,expected", [
    ("kinan", ["k", "in", "an"]),         # thesis p. 3: kan + -in- (perfective)
    ("kuman", ["k", "um", "an"]),         # thesis p. 3: kan + -um- (actor focus)
    ("kapampangan", ["ka", "pampang", "an"]),   # ka-...-an circumfix
    ("masanting", ["ma", "santing"]),
    ("sulatan", ["sulat", "an"]),
    ("sumulat", ["s", "um", "ulat"]),
])
def test_documented_analyses(segmenter, word, expected):
    assert segmenter.segment(word).surfaces == expected


def test_surfaces_always_reconstruct_the_token(segmenter):
    for w in ["kinan", "kapampangan", "masanting", "balena", "gagawa", "zzz"]:
        assert "".join(segmenter.segment(w).surfaces) == w


def test_boundaries_exclude_word_edges(segmenter):
    assert segmenter.segment("kapampangan").boundaries == {2, 9}
    assert segmenter.segment("kan").boundaries == set()


def test_unknown_word_falls_back_whole(segmenter):
    s = segmenter.segment("qwertyuiop")
    assert s.surfaces == ["qwertyuiop"] and not s.analyzed


def test_longest_prefix_wins(lexicon):
    """R1: 'maka-' must beat 'ma-'. Without longest-first ordering this is
    order-dependent and silently wrong."""
    assert lexicon.prefixes == sorted(lexicon.prefixes, key=lambda s: (-len(s), s))


def test_strict_mode_is_more_conservative(segmenter, strict_segmenter):
    assert strict_segmenter.segment("gagawa").analyzed is False   # no reduplication
    assert segmenter.segment("gagawa").analyzed is True


def test_mark_boundaries(segmenter):
    assert segmenter.segment("kapampangan").marked() == "ka || pampang || an"
    assert segmenter.segment("kan").marked() == "kan"
