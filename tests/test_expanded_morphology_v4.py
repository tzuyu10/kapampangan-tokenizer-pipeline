from __future__ import annotations

import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

_REPO_ROOT = Path(__file__).resolve().parents[1]
_V4_ROOT = _REPO_ROOT / "experiments/expanded_morphology_v4"
if str(_V4_ROOT) not in sys.path:
    sys.path.insert(0, str(_V4_ROOT))

from expanded_morphology import (  # noqa: E402
    NEW_CIRCUMFIX_PREFIXES,
    NEW_SUFFIX_FAMILIES,
    ExpandedMorphologicalSegmenter,
)

from kapampangan_morphbpe.lexicon import TrainingLexicon, load_lexicon  # noqa: E402


def synthetic_lexicon() -> TrainingLexicon:
    """Roots directly attested for each new rule; see EVIDENCE.md for citations."""
    return TrainingLexicon(
        roots=frozenset(
            {
                "samba",  # Forman dictionary headword; root/root+an in trilingual lexicon #19
                "aral",  # Mirikitani p.569/810 pagaralan
                "basa",  # Mirikitani p.510 mamasa
                "datang",  # Forman p.81 manyatang; Mirikitani p.510-511 daratang/karatangratang
                "kan",  # Mirikitani p.569 kanan; Forman p.76/471 mangan
                "sali",  # Mirikitani p.569 salwan
                "lawe",  # Mirikitani p.288/295 lawen
                "pandilu",  # Mirikitani p.491/497 pipandiluan
                "albe",  # Mirikitani p.288/295 albe "look at" (vowel-initial demonstration root)
                "tinda",  # Mirikitani p.686 paninda
                "kua",  # Mirikitani p.570 kuanan
                "sulat",  # existing baseline root, reused for -en and reduplication demos
                "inum",  # Forman p.79/Mirikitani p.471 (mi)minum
                "tali",  # ambiguity fixture only
            }
        ),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic",
    )


def test_target_misamban_matches_mi_an_circumfix_on_samba() -> None:
    """The required acceptance case: mi- + samba + -an, surface mi + samba + n."""
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("misamban")
    assert result.status == "accepted"
    assert result.segments == ("mi", "samba", "n")
    assert "".join(result.segments) == "misamban"
    assert result.rule_id == "CIRCUMFIX_MI_AN"
    assert result.underlying_display == "mi- + samba + -an"
    assert [unit.underlying for unit in result.underlying_units] == ["mi-", "samba", "-an"]


def test_target_misamban_on_real_source_adjudicated_v2_lexicon() -> None:
    """Same case against the real, unmodified v2 corpus lexicon (samba is already a root)."""
    lexicon_path = _REPO_ROOT / "experiments/source_adjudicated_v2/resources/training-lexicon.json"
    segmenter = ExpandedMorphologicalSegmenter(load_lexicon(lexicon_path))
    result = segmenter.segment("misamban")
    assert result.status == "accepted"
    assert result.segments == ("mi", "samba", "n")
    assert result.rule_id == "CIRCUMFIX_MI_AN"


def test_pi_an_circumfix_locative() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    church = segmenter.segment("pisamban")
    assert church.status == "accepted"
    assert church.segments == ("pi", "samba", "n")
    assert church.rule_id == "CIRCUMFIX_PI_AN"

    pool = segmenter.segment("pipandiluan")
    assert pool.status == "accepted"
    assert pool.segments == ("pi", "pandilu", "an")
    assert pool.rule_id == "CIRCUMFIX_PI_AN"


def test_pag_an_circumfix_no_nasal_assimilation() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("pagaralan")
    assert result.status == "accepted"
    assert result.segments == ("pag", "aral", "an")
    assert result.rule_id == "CIRCUMFIX_PAG_AN"


def test_maN_nasal_place_assimilation_dental_labial_velar() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())

    labial = segmenter.segment("mamasa")
    assert labial.segments == ("mam", "asa")
    assert labial.underlying_display == "maN- + basa"
    assert labial.rule_id == "PREFIX_MAN_MAM_LABIAL_M_SUBSTITUTION"

    velar = segmenter.segment("mangan")
    assert velar.segments == ("mang", "an")
    assert velar.underlying_display == "maN- + kan"
    assert velar.rule_id == "PREFIX_MAN_MANG_VELAR_NG_SUBSTITUTION"

    dental_unchanged = segmenter.segment("manalbe")
    assert dental_unchanged.segments == ("man", "albe")
    assert dental_unchanged.underlying_display == "maN- + albe"
    assert dental_unchanged.rule_id == "PREFIX_MAN_MAN_UNCHANGED"


def test_maN_dental_irregular_y_substitution() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("manyatang")
    assert result.status == "accepted"
    assert result.segments == ("many", "atang")
    assert result.underlying_display == "maN- + datang"
    assert result.rule_id == "PREFIX_MAN_MANY_DENTAL_Y_SUBSTITUTION"


def test_paN_nominalizer_is_compositional_over_mag_stem() -> None:
    """paN- attaches over an already mag-prefixed stem: pam- + (mag- + aral)."""
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("pamagaral")
    assert result.status == "accepted"
    assert result.segments == ("pam", "ag", "aral")
    assert "".join(result.segments) == "pamagaral"
    assert result.underlying_display == "paN- + mag- + aral"
    assert result.rule_id == "PREFIX_PAN_PAM_LABIAL_M_SUBSTITUTION"


def test_paN_nominalizer_standalone_dental() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("paninda")
    assert result.status == "accepted"
    assert result.segments == ("pan", "inda")
    assert result.underlying_display == "paN- + tinda"


def test_suffix_en_and_anan_allomorphs() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())

    en_form = segmenter.segment("sulaten")
    assert en_form.status == "accepted"
    assert en_form.segments == ("sulat", "en")
    assert en_form.rule_id == "SUFFIX_EN"

    anan_form = segmenter.segment("kuanan")
    assert anan_form.status == "accepted"
    assert anan_form.segments == ("kua", "nan")
    assert anan_form.underlying_display == "kua + -anan"
    assert anan_form.rule_id == "SUFFIX_ANAN"


def test_an_allomorphy_hiatus_collapse_and_w_insertion() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())

    hiatus = segmenter.segment("basan")
    assert hiatus.status == "accepted"
    assert hiatus.segments == ("basa", "n")
    assert hiatus.rule_id == "SUFFIX_AN"

    w_insertion = segmenter.segment("salwan")
    assert w_insertion.status == "accepted"
    assert w_insertion.segments == ("sal", "wan")
    assert w_insertion.underlying_display == "sali + -an"
    assert w_insertion.rule_id == "SUFFIX_AN"

    literal = segmenter.segment("kanan")
    assert literal.status == "accepted"
    assert literal.segments == ("kan", "an")


def test_hiatus_collapse_does_not_validate_short_noisy_roots() -> None:
    """The corpus-scraped v2 lexicon contains some 1-2 letter root rows (e.g.
    "sa", "ba", "ya"). Stripping only a bare "-n" is far more permissive than
    matching a full "-an"/"-en" suffix, so it must not accept a reconstructed
    root shorter than 3 letters -- otherwise "San" (a placename fragment)
    wrongly resolves to "Sa" + "n". This mirrors source_adjudicated_v2's own
    policy of holding roots shorter than three letters."""
    lexicon = TrainingLexicon(
        roots=frozenset({"sa", "ba", "ya"}),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic-short-roots",
    )
    segmenter = ExpandedMorphologicalSegmenter(lexicon)
    for word in ("San", "ban", "yan"):
        result = segmenter.segment(word)
        assert result.status == "unchanged", word


def test_an_en_hiatus_collision_is_preserved_as_ambiguous() -> None:
    """After an e-final root, -an and -en both collapse to bare -n: genuinely
    ambiguous without a per-root subcategorization lexicon, which this
    productive-rule engine deliberately does not encode. Mirikitani glosses
    'lawen' as -en specifically, but a general rule cannot know that from the
    surface alone, so both hypotheses must survive."""
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("lawen")
    assert result.status == "ambiguous"
    assert result.segments == ("lawen",)


def test_reduplication_cv_and_d_to_r_medial_alternation() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())

    cv_redup = segmenter.segment("susulat")
    assert cv_redup.status == "accepted"
    assert cv_redup.segments == ("su", "sulat")
    assert cv_redup.underlying_display == "REDUP(sulat) + sulat"
    assert cv_redup.rule_id == "REDUP_CV_REDUPLICATION"

    d_to_r = segmenter.segment("daratang")
    assert d_to_r.status == "accepted"
    assert d_to_r.segments == ("da", "ratang")
    assert "".join(d_to_r.segments) == "daratang"
    assert d_to_r.underlying_display == "REDUP(datang) + datang"

    v_redup = segmenter.segment("miminum")
    assert v_redup.status == "accepted"
    assert v_redup.segments == ("mi", "m", "inum")
    assert "".join(v_redup.segments) == "miminum"


def test_title_and_upper_case_input_is_still_analyzed() -> None:
    """Suffix/circumfix/reduplication matching must compare the lowercase
    comparison key, not the raw mixed-case token, or "ARAPAN"/"Daratang"-style
    sentence-cased corpus words silently fall through to unchanged (a real bug
    found by running the full corpus resegmentation)."""
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())

    upper_suffix = segmenter.segment("ARALAN")
    assert upper_suffix.status == "accepted"
    assert upper_suffix.segments == ("ARAL", "AN")
    assert upper_suffix.underlying_units[0].underlying == "ARAL"

    title_circumfix = segmenter.segment("Misamban")
    assert title_circumfix.status == "accepted"
    assert title_circumfix.segments == ("Mi", "samba", "n")
    assert title_circumfix.underlying_display == "mi- + samba + -an"

    title_redup = segmenter.segment("Susulat")
    assert title_redup.status == "accepted"
    assert title_redup.segments == ("Su", "sulat")
    assert title_redup.rule_id == "REDUP_CV_REDUPLICATION"


def test_ka_full_reduplication_recent_completive() -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment("kadatangdatang")
    assert result.status == "accepted"
    assert result.segments == ("ka", "datang", "datang")
    assert result.rule_id == "PREFIX_KA_FULL_REDUPLICATION"

    d_to_r = segmenter.segment("karatangratang")
    assert d_to_r.status == "accepted"
    assert d_to_r.segments == ("ka", "ratang", "ratang")
    assert "".join(d_to_r.segments) == "karatangratang"
    assert d_to_r.underlying_units[1].underlying == "datang"


def test_reconstruction_ambiguity_is_preserved_not_resolved() -> None:
    """Two dental roots (tali, sali) both validate the same nasal-substitution
    hypothesis space for 'manali': genuinely ambiguous, must not be silently
    resolved to either reading."""
    lexicon = TrainingLexicon(
        roots=frozenset({"tali", "sali"}),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic-ambiguous",
    )
    segmenter = ExpandedMorphologicalSegmenter(lexicon)
    result = segmenter.segment("manali")
    assert result.status == "ambiguous"
    assert result.segments == ("manali",)
    assert result.rule_id is None


def test_baseline_table1_behavior_is_unchanged() -> None:
    """The original paper-mandated rules still work exactly as before inside
    the expanded engine (it extends, never edits, Table 1)."""
    lexicon = TrainingLexicon(
        roots=frozenset({"kan", "sulat", "basa", "pagkan", "main"}),
        compounds=frozenset({"bahay-basa", "makasulat"}),
        variants=frozenset({"súlat"}),
        lexicon_fingerprint="synthetic",
    )
    segmenter = ExpandedMorphologicalSegmenter(lexicon)
    assert segmenter.segment("").status == "empty"
    assert segmenter.segment("sulat").status == "protected_root"
    assert segmenter.segment("bahay-basa").status == "protected_compound"
    assert segmenter.segment("masulat").segments == ("ma", "sulat")
    assert segmenter.segment("kuman").segments == ("k", "um", "an")
    assert segmenter.segment("sulatan").segments == ("sulat", "an")
    assert segmenter.segment("kasulatan").segments == ("ka", "sulat", "an")
    assert segmenter.segment("sulatya").segments == ("sulat", "ya")


def test_rejected_items_are_not_operationalized() -> None:
    """paki-...-an and the -in suffix are explicitly rejected; see EVIDENCE.md."""
    assert "paki" not in NEW_CIRCUMFIX_PREFIXES
    assert "in" not in NEW_SUFFIX_FAMILIES
    lexicon = TrainingLexicon(
        roots=frozenset({"sali"}),
        compounds=frozenset(),
        variants=frozenset(),
        lexicon_fingerprint="synthetic",
    )
    segmenter = ExpandedMorphologicalSegmenter(lexicon)
    # "pakisalian" would only ever be reachable through a paki-...-an circumfix
    # rule, which does not exist; it must fall through un-analyzed rather than
    # being force-fit into some other rule.
    result = segmenter.segment("pakisalian")
    assert result.status == "unchanged"


@given(
    st.sampled_from(["kan", "sulat", "basa", "aral"]),
    st.sampled_from(["ma", "mag", "ipa", "paki", "peka"]),
)
def test_accepted_literal_prefix_analysis_always_reconstructs(root: str, prefix: str) -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    result = segmenter.segment(prefix + root)
    assert "".join(result.segments) == result.token


@given(st.sampled_from(["samba", "aral", "pandilu", "basa"]))
def test_mi_an_and_pi_an_circumfix_always_reconstructs(root: str) -> None:
    segmenter = ExpandedMorphologicalSegmenter(synthetic_lexicon())
    for prefix in ("mi", "pi"):
        result = segmenter.segment(prefix + root + "an")
        assert "".join(result.segments) == result.token
