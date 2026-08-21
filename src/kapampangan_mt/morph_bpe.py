"""Morph-BPE: boundary-constrained Byte-Pair Encoding (thesis p. 42-43).

Standard BPE (Sennrich et al., 2016) repeatedly merges the most frequent
adjacent symbol pair in the corpus.  Morph-BPE (Asgari et al., 2025) runs the
same loop but **never counts a pair that straddles a morpheme boundary**, so no
learned token can span two morphemes of a word that the segmenter analysed.

Implementation
--------------
Each training word is stored as a list of *cells*, one per morpheme:

    "kapampangan"  ->  [['▁','k','a'], ['p','a','m','p','a','n','g'], ['a','n']]
                        ka-             pampang                       -an

Pairs are counted inside cells only.  Merges are applied inside cells only.
Words the segmenter could not analyse become a single cell — they behave
exactly like standard BPE, which is the intended degradation.

The word-start marker ``▁`` is glued to the first symbol of the first cell so
that "▁kan" (sentence-initial) and "kan" (word-internal, e.g. after a hyphen)
stay distinguishable, matching SentencePiece conventions.
"""
from __future__ import annotations

import heapq
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from .pretokenize import WORD_BOUNDARY

Pair = tuple[str, str]


@dataclass
class MorphBPEConfig:
    vocab_size: int = 8000
    min_pair_frequency: int = 2
    #: If False the boundary constraint is switched off -> plain BPE on the same
    #: data. This is the *matched control tokenizer* the study needs (Issue M-3).
    constrain_to_morpheme_boundaries: bool = True
    #: Characters seen fewer than this many times are dropped from the base
    #: alphabet and handled by byte fallback at runtime.
    min_char_frequency: int = 1


@dataclass
class MorphBPEModel:
    """Learned artefact: an ordered merge list plus the resulting alphabet."""

    merges: list[Pair] = field(default_factory=list)
    alphabet: list[str] = field(default_factory=list)
    config: MorphBPEConfig = field(default_factory=MorphBPEConfig)
    stats: dict = field(default_factory=dict)


class MorphBPETrainer:
    """Boundary-constrained BPE learner."""

    def __init__(self, config: MorphBPEConfig | None = None) -> None:
        self.cfg = config or MorphBPEConfig()

    # ------------------------------------------------------------------ #
    def train(
        self,
        word_segmentations: dict[str, list[str]],
        word_freqs: dict[str, int],
        reserved: int = 0,
        verbose: bool = True,
    ) -> MorphBPEModel:
        """Learn merges.

        Parameters
        ----------
        word_segmentations:
            ``marked_word -> [morpheme surfaces]``.  The concatenation of the
            surfaces must equal the marked word (the ``▁`` marker is prepended
            here, not by the caller).
        word_freqs:
            ``marked_word -> corpus frequency``.
        reserved:
            Number of vocabulary slots already taken by special tokens and byte
            fallbacks.  ``vocab_size`` counts them.
        """
        # --- build cells -------------------------------------------------
        words: list[list[list[str]]] = []
        freqs: list[int] = []
        char_counts: Counter[str] = Counter()

        for word, freq in word_freqs.items():
            morphs = word_segmentations.get(word) or [word.lstrip(WORD_BOUNDARY)]
            if not self.cfg.constrain_to_morpheme_boundaries:
                morphs = ["".join(morphs)]
            cells: list[list[str]] = []
            first = True
            for m in morphs:
                if not m:
                    continue
                syms = list(m)
                if first and word.startswith(WORD_BOUNDARY):
                    syms[0] = WORD_BOUNDARY + syms[0]
                first = False
                cells.append(syms)
            if not cells:
                continue
            words.append(cells)
            freqs.append(freq)
            for cell in cells:
                for s in cell:
                    char_counts[s] += freq

        alphabet = sorted(
            s for s, c in char_counts.items() if c >= self.cfg.min_char_frequency
        )
        budget = self.cfg.vocab_size - reserved - len(alphabet)
        if budget <= 0:
            raise ValueError(
                f"vocab_size={self.cfg.vocab_size} is too small: {reserved} reserved "
                f"+ {len(alphabet)} alphabet symbols already exceed it."
            )

        # --- pair index --------------------------------------------------
        pair_counts: Counter[Pair] = Counter()
        pair_where: dict[Pair, set[tuple[int, int]]] = defaultdict(set)

        def index_cell(wi: int, ci: int, sign: int) -> None:
            cell, f = words[wi][ci], freqs[wi]
            for a, b in zip(cell, cell[1:]):
                p = (a, b)
                pair_counts[p] += sign * f
                if sign > 0:
                    pair_where[p].add((wi, ci))

        for wi, cells in enumerate(words):
            for ci in range(len(cells)):
                index_cell(wi, ci, +1)

        heap: list[tuple[int, Pair]] = [(-c, p) for p, c in pair_counts.items() if c > 0]
        heapq.heapify(heap)

        merges: list[Pair] = []
        while len(merges) < budget and heap:
            negc, pair = heapq.heappop(heap)
            cur = pair_counts.get(pair, 0)
            if cur <= 0 or -negc != cur:            # stale heap entry
                if cur > 0:
                    heapq.heappush(heap, (-cur, pair))
                continue
            if cur < self.cfg.min_pair_frequency:
                break

            new_sym = pair[0] + pair[1]
            touched = list(pair_where.pop(pair, ()))
            dirty: set[Pair] = set()
            for wi, ci in touched:
                cell = words[wi][ci]
                if len(cell) < 2:
                    continue
                for a, b in zip(cell, cell[1:]):
                    dirty.add((a, b))
                index_cell(wi, ci, -1)
                merged, i = [], 0
                while i < len(cell):
                    if i + 1 < len(cell) and cell[i] == pair[0] and cell[i + 1] == pair[1]:
                        merged.append(new_sym)
                        i += 2
                    else:
                        merged.append(cell[i])
                        i += 1
                words[wi][ci] = merged
                index_cell(wi, ci, +1)
                for a, b in zip(merged, merged[1:]):
                    dirty.add((a, b))
            pair_counts[pair] = 0
            for p in dirty:
                c = pair_counts.get(p, 0)
                if c > 0:
                    heapq.heappush(heap, (-c, p))
            merges.append(pair)
            if verbose and len(merges) % 1000 == 0:
                print(f"  merges: {len(merges)}/{budget}  last={new_sym!r} freq={cur}")

        model = MorphBPEModel(
            merges=merges,
            alphabet=alphabet,
            config=self.cfg,
            stats={
                "n_word_types": len(words),
                "n_alphabet": len(alphabet),
                "n_merges": len(merges),
                "constrained": self.cfg.constrain_to_morpheme_boundaries,
                "stopped_early": len(merges) < budget,
            },
        )
        return model
