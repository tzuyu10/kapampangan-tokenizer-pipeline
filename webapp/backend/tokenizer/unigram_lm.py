"""Minimal SentencePiece-Unigram decoder — copied verbatim from the team's
own `demo.py` (see `_reference_demo_source.py`). Not modified in any way;
only moved into its own module so the backend can import it without also
re-running demo.py's module-level side effects (which construct its
tokenizers using paths relative to demo.py's own location).
"""

from __future__ import annotations

import json
import math
from pathlib import Path


class UnigramLM:
    """Minimal SentencePiece-Unigram decoder (Viterbi best-path).

    Reads a Hugging Face `tokenizers` Unigram `tokenizer.json` (a list of
    ``[piece, log_prob]``). Verified piece-for-piece against
    `tokenizers.Tokenizer.from_file(...).encode()`.
    """

    def __init__(self, tokenizer_json: Path) -> None:
        doc = json.loads(tokenizer_json.read_text(encoding="utf-8"))
        model = doc["model"]
        if model.get("type") != "Unigram":
            raise ValueError("not a Unigram tokenizer.json")
        specials = {"<pad>", "<s>", "</s>"}
        self.score: dict[str, float] = {
            piece: logp for piece, logp in model["vocab"] if piece not in specials
        }
        self.vocabulary_size = len(model["vocab"])
        self._unk = min(s for s in self.score.values() if s < 0) - 10.0

    def encode(self, word: str) -> list[str]:
        n = len(word)
        best: list[tuple[float, int, str]] = [(-math.inf, -1, "")] * (n + 1)
        best[0] = (0.0, -1, "")
        for i in range(1, n + 1):
            choice = (-math.inf, -1, "")
            for j in range(i):
                if best[j][0] == -math.inf:
                    continue
                piece = word[j:i]
                sc = self.score.get(piece)
                if sc is not None:
                    cand = (best[j][0] + sc, j, piece)
                    if cand[0] > choice[0]:
                        choice = cand
            unk = (best[i - 1][0] + self._unk, i - 1, "<unk>")
            if best[i - 1][0] != -math.inf and unk[0] > choice[0]:
                choice = unk
            best[i] = choice
        out: list[str] = []
        i = n
        while i > 0:
            _, j, piece = best[i]
            out.append(piece)
            i = j
        out.reverse()
        merged: list[str] = []
        for p in out:
            if p == "<unk>" and merged and merged[-1] == "<unk>":
                continue
            merged.append(p)
        return merged
