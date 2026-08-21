"""Adapters that give the baseline tokenizers the same interface as ours.

Two baselines matter:

``NLLBTokenizerAdapter``
    The *practical* baseline named in the thesis: the native NLLB-200
    SentencePiece tokenizer (256k multilingual vocabulary).

``MatchedBPEAdapter``
    The *scientific* control the thesis is missing: plain, unconstrained BPE
    trained on the same Kapampangan corpus with the same vocabulary size.
    Without it, any Fertility Rate win is explained by "we trained a tokenizer
    on Kapampangan", not by morphological awareness.  See Issue M-3.
"""
from __future__ import annotations

from .normalize import Normalizer
from .pretokenize import pre_tokenize, words_only

_SP_MARK = "▁"  # SentencePiece uses the same ▁ character


class NLLBTokenizerAdapter:
    """Wraps ``transformers.AutoTokenizer`` for NLLB-200."""

    def __init__(
        self,
        model_name: str = "facebook/nllb-200-distilled-600M",
        src_lang: str = "tgl_Latn",
        lowercase: bool = True,
        hf_tokenizer=None,
    ) -> None:
        if hf_tokenizer is None:
            from transformers import AutoTokenizer

            hf_tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=src_lang)
        self.tok = hf_tokenizer
        self.normalizer = Normalizer(lowercase=lowercase)
        self.src_lang = src_lang

    # Same public surface as KapampanganTokenizer -------------------------
    @property
    def vocab_size(self) -> int:
        return len(self.tok)

    def tokenize(self, text: str) -> list[str]:
        return self.tok.tokenize(self.normalizer.normalize_text(text))

    def tokenize_word(self, word: str) -> list[str]:
        return self.tok.tokenize(self.normalizer.normalize_token(word))

    def encode(self, text: str, add_special_tokens: bool = True,
               max_length: int | None = None) -> list[int]:
        return self.tok(
            self.normalizer.normalize_text(text),
            add_special_tokens=add_special_tokens,
            max_length=max_length,
            truncation=max_length is not None,
        )["input_ids"]

    def decode(self, ids, skip_special_tokens: bool = True) -> str:
        return self.tok.decode(ids, skip_special_tokens=skip_special_tokens)

    def boundaries(self, word: str) -> set[int]:
        pieces = self.tokenize_word(word)
        out, pos = set(), 0
        for p in pieces[:-1]:
            pos += len(p.replace(_SP_MARK, ""))
            if 0 < pos < len(word):
                out.add(pos)
        return out

    def fertility(self, text: str) -> tuple[int, int]:
        text = self.normalizer.normalize_text(text)
        return len(self.tokenize(text)), len(words_only(text))


class MatchedBPEAdapter:
    """Plain BPE on the same data — a :class:`KapampanganTokenizer` trained with
    ``constrain_to_morpheme_boundaries=False``.  Kept as a named type so
    experiment configs and result tables stay unambiguous."""

    def __init__(self, tokenizer) -> None:
        self._t = tokenizer

    def __getattr__(self, item):
        return getattr(self._t, item)
