"""Dataset + collator for Kapampangan -> Filipino fine-tuning.

Source ids come from whichever tokenizer the arm uses; target ids always come
from the native NLLB tokenizer, because the target side is unchanged in both
conditions (thesis p. 44).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch
from torch.utils.data import Dataset


@dataclass
class ParallelPair:
    src: str
    tgt: str


class KapampanganFilipinoDataset(Dataset):
    def __init__(
        self,
        pairs: list[ParallelPair],
        src_tokenizer,
        nllb_tokenizer,
        max_src_len: int = 128,
        max_tgt_len: int = 128,
        tgt_lang: str = "tgl_Latn",
    ) -> None:
        self.pairs = pairs
        self.src_tok = src_tokenizer
        self.tgt_tok = nllb_tokenizer
        self.max_src_len = max_src_len
        self.max_tgt_len = max_tgt_len
        self.tgt_tok.tgt_lang = tgt_lang

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, i: int) -> dict:
        p = self.pairs[i]
        src_ids = self.src_tok.encode(p.src, max_length=self.max_src_len)
        with self.tgt_tok.as_target_tokenizer() if hasattr(
            self.tgt_tok, "as_target_tokenizer"
        ) else _null_ctx():
            pass
        labels = self.tgt_tok(
            text_target=p.tgt, max_length=self.max_tgt_len, truncation=True
        )["input_ids"]
        return {"input_ids": src_ids, "labels": labels}


class _null_ctx:
    def __enter__(self): return None
    def __exit__(self, *a): return False


@dataclass
class Collator:
    src_pad_id: int
    tgt_pad_id: int
    label_pad_id: int = -100

    def __call__(self, batch: list[dict]) -> dict:
        max_s = max(len(b["input_ids"]) for b in batch)
        max_t = max(len(b["labels"]) for b in batch)
        input_ids, attn, labels = [], [], []
        for b in batch:
            s, t = b["input_ids"], b["labels"]
            pad_s = max_s - len(s)
            pad_t = max_t - len(t)
            input_ids.append(s + [self.src_pad_id] * pad_s)
            attn.append([1] * len(s) + [0] * pad_s)
            labels.append(t + [self.label_pad_id] * pad_t)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attn, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


def load_pairs(path: str) -> list[ParallelPair]:
    """Read a TSV with columns ``pam`` and ``fil`` (header required)."""
    import csv
    from pathlib import Path

    out: list[ParallelPair] = []
    with Path(path).open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            s, t = (r.get("pam") or "").strip(), (r.get("fil") or "").strip()
            if s and t:
                out.append(ParallelPair(s, t))
    return out
