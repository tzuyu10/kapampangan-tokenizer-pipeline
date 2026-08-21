"""Runtime Kapampangan tokenizer (thesis p. 43-44, "Runtime tokenization behavior").

After training, **no lexicon and no morphological analysis is used**.  The
tokenizer holds only:

  * a vocabulary (specials, 256 byte-fallback tokens, alphabet, merged symbols)
  * an ordered merge table

Encoding a word: split into characters, replace any character absent from the
vocabulary with its UTF-8 byte tokens, then apply the learned merges greedily
in rank order until no merge applies.  Byte tokens are always present, so no
input is ever unprocessable — this is the guarantee the thesis claims on p. 44,
made literally true by byte fallback rather than character fallback (a raw
character fallback breaks on any code point unseen in training).

Special-token ids deliberately mirror NLLB's layout so that ``pad_token_id``
stays 1 on both sides of the grafted model.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .normalize import Normalizer
from .pretokenize import WORD_BOUNDARY, pre_tokenize, words_only

BOS, PAD, EOS, UNK = "<s>", "<pad>", "</s>", "<unk>"
SRC_LANG = "__pam_Latn__"          # Kapampangan is NOT an NLLB-200 language code
#: Tokens skipped when ``skip_special_tokens=True``.
SPECIALS = [BOS, PAD, EOS, UNK, SRC_LANG]
#: Everything that occupies a fixed slot before the learned alphabet.
#: ``WORD_BOUNDARY`` is reserved but is NOT a special: dropping it on decode
#: would delete every space in the output.
RESERVED = SPECIALS + [WORD_BOUNDARY]
BYTE_TOKENS = [f"<0x{i:02X}>" for i in range(256)]


@dataclass
class KapampanganTokenizer:
    vocab: dict[str, int]
    merges: list[tuple[str, str]]
    lowercase: bool = True
    meta: dict | None = None

    # ------------------------------------------------------------------ #
    def __post_init__(self) -> None:
        self.ids_to_tokens = {i: t for t, i in self.vocab.items()}
        self.ranks = {tuple(p): i for i, p in enumerate(self.merges)}
        self.normalizer = Normalizer(lowercase=self.lowercase)
        self._cache: dict[str, list[str]] = {}

    # ---------------------------- factory ------------------------------ #
    @classmethod
    def from_model(cls, model, lowercase: bool = True) -> "KapampanganTokenizer":
        """Build the runtime vocabulary from a trained :class:`MorphBPEModel`."""
        tokens = list(RESERVED) + list(BYTE_TOKENS)
        seen = set(tokens)
        for sym in model.alphabet:
            if sym not in seen:
                tokens.append(sym)
                seen.add(sym)
        for a, b in model.merges:
            sym = a + b
            if sym not in seen:
                tokens.append(sym)
                seen.add(sym)
        vocab = {t: i for i, t in enumerate(tokens)}
        return cls(
            vocab=vocab,
            merges=[tuple(m) for m in model.merges],
            lowercase=lowercase,
            meta={"stats": model.stats, "config": vars(model.config)},
        )

    # ------------------------------ IO --------------------------------- #
    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            json.dumps(
                {
                    "version": 1,
                    "lowercase": self.lowercase,
                    "vocab": self.vocab,
                    "merges": [list(m) for m in self.merges],
                    "meta": self.meta or {},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "KapampanganTokenizer":
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            vocab=d["vocab"],
            merges=[tuple(m) for m in d["merges"]],
            lowercase=d.get("lowercase", True),
            meta=d.get("meta"),
        )

    # ---------------------------- properties --------------------------- #
    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    @property
    def bos_id(self) -> int: return self.vocab[BOS]
    @property
    def pad_id(self) -> int: return self.vocab[PAD]
    @property
    def eos_id(self) -> int: return self.vocab[EOS]
    @property
    def unk_id(self) -> int: return self.vocab[UNK]
    @property
    def src_lang_id(self) -> int: return self.vocab[SRC_LANG]

    # ---------------------------- encoding ----------------------------- #
    def _base_symbols(self, word: str) -> list[str]:
        """Reproduce the trainer's base units exactly.

        The trainer glues the word-start marker onto the first character of the
        first morpheme, so "▁kan" starts life as ["▁k", "a", "n"] and NOT as
        ["▁", "k", "a", "n"].  Splitting differently at runtime would make the
        learned merges unreachable and silently blow up fertility.
        """
        chars = list(word)
        if len(chars) > 1 and chars[0] == WORD_BOUNDARY:
            fused = WORD_BOUNDARY + chars[1]
            chars = ([fused] if fused in self.vocab
                     else [WORD_BOUNDARY, chars[1]]) + chars[2:]
        out: list[str] = []
        for ch in chars:
            if ch in self.vocab:
                out.append(ch)
                continue
            if ch.startswith(WORD_BOUNDARY) and len(ch) > 1:
                out.append(WORD_BOUNDARY)
                ch = ch[1:]
                if ch in self.vocab:
                    out.append(ch)
                    continue
            out.extend(f"<0x{b:02X}>" for b in ch.encode("utf-8"))
        return out

    def _bpe(self, word: str) -> list[str]:
        if word in self._cache:
            return self._cache[word]
        syms = self._base_symbols(word)
        while len(syms) > 1:
            best, best_rank, = None, None
            for i in range(len(syms) - 1):
                r = self.ranks.get((syms[i], syms[i + 1]))
                if r is not None and (best_rank is None or r < best_rank):
                    best, best_rank = i, r
            if best is None:
                break
            merged = syms[best] + syms[best + 1]
            syms[best : best + 2] = [merged]
        self._cache[word] = syms
        return syms

    def tokenize(self, text: str) -> list[str]:
        """Text -> list of subword strings (no special tokens)."""
        text = self.normalizer.normalize_text(text)
        out: list[str] = []
        for pt in pre_tokenize(text):
            out.extend(self._bpe(pt.marked))
        return out

    def tokenize_word(self, word: str) -> list[str]:
        """Tokenise one word as if it were sentence-initial (for MBF1/MCF1)."""
        return self._bpe(WORD_BOUNDARY + self.normalizer.normalize_token(word))

    def encode(
        self, text: str, add_special_tokens: bool = True, max_length: int | None = None
    ) -> list[int]:
        """Text -> token ids.

        Layout mirrors NLLB source formatting: ``<src_lang> tokens </s>``.
        """
        ids = [self.vocab.get(t, self.unk_id) for t in self.tokenize(text)]
        if add_special_tokens:
            ids = [self.src_lang_id] + ids + [self.eos_id]
        if max_length is not None and len(ids) > max_length:
            ids = ids[: max_length - 1] + [self.eos_id]
        return ids

    def batch_encode(
        self, texts: list[str], max_length: int | None = None
    ) -> list[list[int]]:
        return [self.encode(t, max_length=max_length) for t in texts]

    # ---------------------------- decoding ----------------------------- #
    def decode(self, ids: list[int], skip_special_tokens: bool = True) -> str:
        pieces, buf = [], bytearray()

        def flush() -> None:
            if buf:
                pieces.append(buf.decode("utf-8", errors="replace"))
                buf.clear()

        for i in ids:
            tok = self.ids_to_tokens.get(i, UNK)
            if tok in SPECIALS:
                if skip_special_tokens:
                    continue
                flush(); pieces.append(tok); continue
            if tok.startswith("<0x") and tok.endswith(">") and len(tok) == 6:
                buf.append(int(tok[3:5], 16)); continue
            flush(); pieces.append(tok)
        flush()
        return "".join(pieces).replace(WORD_BOUNDARY, " ").strip()

    # ------------------------- analysis helpers ------------------------ #
    def boundaries(self, word: str) -> set[int]:
        """Character offsets inside *word* where this tokenizer puts a split."""
        pieces = self.tokenize_word(word)
        out, pos = set(), 0
        for p in pieces[:-1]:
            pos += len(p.replace(WORD_BOUNDARY, ""))
            out.add(pos)
        return out

    def fertility(self, text: str) -> tuple[int, int]:
        """(n_tokens, n_source_words) for one sentence — inputs to eq. (1)."""
        return len(self.tokenize(text)), len(words_only(
            self.normalizer.normalize_text(text)))
