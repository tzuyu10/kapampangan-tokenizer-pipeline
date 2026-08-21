"""Corpus cleaning (thesis "Data Generation and Procedure", p. 50).

Removes duplicates, corrupted text, PII-looking strings, length outliers and
implausible source/target length ratios, then normalises both sides.
Every dropped row is logged with a reason so the cleaning step is auditable —
the panel will ask how 13,000 raw pairs became N usable pairs.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from ..normalize import Normalizer

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"(?:\+63|0)9\d{2}[\s-]?\d{3}[\s-]?\d{4}")
URL = re.compile(r"https?://\S+|www\.\S+")
LATIN_OK = re.compile(r"^[\w\s.,;:!?'\"()\-–—/%°ñÑáéíóúÁÉÍÓÚ]+$", re.UNICODE)


@dataclass
class CleanConfig:
    min_words: int = 2
    max_words: int = 80
    max_len_ratio: float = 3.0     # |src words| / |tgt words| and inverse
    min_alpha_ratio: float = 0.6   # share of alphabetic characters
    drop_duplicates: bool = True
    drop_src_equals_tgt: bool = True
    lowercase: bool = False        # keep case in the corpus; tokenizers fold it
    redact_pii: bool = True


@dataclass
class CleanReport:
    kept: int = 0
    dropped: Counter = field(default_factory=Counter)
    #: original row indices that survived, so parallel metadata (domain,
    #: source URL, annotator) can be filtered alongside the text.
    kept_indices: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"kept": self.kept, "dropped": dict(self.dropped),
                "total": self.kept + sum(self.dropped.values())}


def _alpha_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(c.isalpha() or c.isspace() for c in s) / len(s)


def clean_pairs(
    pairs: list[tuple[str, str]], cfg: CleanConfig | None = None
) -> tuple[list[tuple[str, str]], CleanReport]:
    cfg = cfg or CleanConfig()
    norm = Normalizer(lowercase=cfg.lowercase)
    rep = CleanReport()
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str]] = []

    for row_index, (src, tgt) in enumerate(pairs):
        if not src or not tgt:
            rep.dropped["empty"] += 1; continue
        if cfg.redact_pii:
            for rx in (EMAIL, PHONE, URL):
                src, tgt = rx.sub(" ", src), rx.sub(" ", tgt)
        src, tgt = norm.normalize_text(src), norm.normalize_text(tgt)
        if not src or not tgt:
            rep.dropped["empty_after_norm"] += 1; continue
        ws, wt = src.split(), tgt.split()
        if not (cfg.min_words <= len(ws) <= cfg.max_words):
            rep.dropped["src_length"] += 1; continue
        if not (cfg.min_words <= len(wt) <= cfg.max_words):
            rep.dropped["tgt_length"] += 1; continue
        ratio = len(ws) / max(len(wt), 1)
        if ratio > cfg.max_len_ratio or (1 / ratio) > cfg.max_len_ratio:
            rep.dropped["length_ratio"] += 1; continue
        if _alpha_ratio(src) < cfg.min_alpha_ratio or _alpha_ratio(tgt) < cfg.min_alpha_ratio:
            rep.dropped["non_text"] += 1; continue
        if cfg.drop_src_equals_tgt and src.lower() == tgt.lower():
            rep.dropped["src_equals_tgt"] += 1; continue
        key = (src.lower(), tgt.lower())
        if cfg.drop_duplicates and key in seen:
            rep.dropped["duplicate"] += 1; continue
        seen.add(key)
        out.append((src, tgt))
        rep.kept_indices.append(row_index)
        rep.kept += 1
    return out, rep
