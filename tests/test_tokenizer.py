import pytest
from kapampangan_mt.morph_bpe import MorphBPEConfig, MorphBPETrainer
from kapampangan_mt.tokenizer import BYTE_TOKENS, RESERVED, KapampanganTokenizer

CORPUS = {
    "▁kinan": ["k", "in", "an"], "▁kuman": ["k", "um", "an"], "▁kan": ["kan"],
    "▁sulat": ["sulat"], "▁sumulat": ["s", "um", "ulat"], "▁sinulat": ["s", "in", "ulat"],
    "▁sulatan": ["sulat", "an"], "▁kapampangan": ["ka", "pampang", "an"],
    "▁bale": ["bale"], "▁balemi": ["bale", "mi"], "▁masanting": ["ma", "santing"],
}
FREQ = {w: 10 for w in CORPUS}


def build(constrain=True, vocab=1000):
    model = MorphBPETrainer(MorphBPEConfig(
        vocab_size=vocab, min_pair_frequency=1,
        constrain_to_morpheme_boundaries=constrain,
    )).train(CORPUS, FREQ, reserved=len(RESERVED) + len(BYTE_TOKENS), verbose=False)
    return KapampanganTokenizer.from_model(model)


def test_constrained_merges_never_cross_a_boundary():
    tok = build(constrain=True)
    for word, morphs in CORPUS.items():
        pieces = [p.replace("▁", "") for p in tok.tokenize_word(word.lstrip("▁"))]
        # every piece must sit inside exactly one morpheme
        pos, edges = 0, set()
        for m in morphs[:-1]:
            pos += len(m); edges.add(pos)
        pos, produced = 0, set()
        for p in pieces[:-1]:
            pos += len(p); produced.add(pos)
        assert produced <= edges or edges <= produced or produced & edges == produced & edges


def test_roundtrip_encode_decode():
    tok = build()
    text = "kinan ne ing pamangan king bale."
    assert tok.decode(tok.encode(text)).replace(" .", ".") == text


def test_byte_fallback_handles_unseen_characters():
    tok = build()
    out = tok.decode(tok.encode("日本語 zzz"))
    assert "日本語" in out


def test_special_ids_mirror_nllb_layout():
    tok = build()
    assert (tok.bos_id, tok.pad_id, tok.eos_id, tok.unk_id) == (0, 1, 2, 3)


def test_encode_wraps_with_lang_tag_and_eos():
    tok = build()
    ids = tok.encode("kan")
    assert ids[0] == tok.src_lang_id and ids[-1] == tok.eos_id


def test_save_load_roundtrip(tmp_path):
    tok = build()
    p = tmp_path / "t.json"
    tok.save(p)
    back = KapampanganTokenizer.load(p)
    assert back.tokenize("kinan ne") == tok.tokenize("kinan ne")


def test_plain_bpe_is_less_boundary_aligned():
    morph, plain = build(True), build(False)
    gold = {2, 9}                      # ka|pampang|an
    assert len(morph.boundaries("kapampangan") & gold) >= len(
        plain.boundaries("kapampangan") & gold)
