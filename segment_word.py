"""Type a Kapampangan word, see how it is analysed and how it is tokenised.

    python segment_word.py                 # interactive
    python segment_word.py kinan kuman     # one-shot
    python segment_word.py --plain kinan   # just the morphological split, nothing else

Shows TWO different things, because they are different and the difference
matters for your thesis:

  MORPHOLOGICAL SEGMENTATION  the Lexicon-guided analysis from Figure 7.
                              This is the k | um | an style split.
                              Training-time only.

  TOKENIZER OUTPUT            what the trained tokenizer actually emits at
                              runtime, using only its learned merge table.
                              This is what the translation model would see.

They usually agree. When they do not, that is Issue T-5 in docs/THESIS_ISSUES.md,
and it is a finding worth reporting rather than a bug.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

from kapampangan_mt.lexicon import Lexicon                    # noqa: E402
from kapampangan_mt.normalize import Normalizer               # noqa: E402
from kapampangan_mt.segmenter import MorphologicalSegmenter   # noqa: E402
from kapampangan_mt.tokenizer import KapampanganTokenizer     # noqa: E402

KIND_LABEL = {
    "root": "root", "prefix": "prefix", "infix": "infix", "suffix": "suffix",
    "clitic": "clitic", "redup": "reduplication", "unknown": "unanalysed",
}


def load():
    norm = Normalizer.from_rules_file(HERE / "data" / "lexicon" / "orthography_rules.tsv",
                                      lowercase=True, strip_accents=True)
    seg = MorphologicalSegmenter(Lexicon.load(HERE / "data" / "lexicon"), normalizer=norm)
    tok_path = HERE / "artifacts" / "tokenizer" / "morphbpe.json"
    tok = KapampanganTokenizer.load(tok_path) if tok_path.exists() else None
    return seg, tok


def show(word: str, seg, tok, plain: bool = False) -> None:
    a = seg.segment(word)
    morph = " | ".join(m.surface for m in a.morphs)

    if plain:
        print(morph)
        return

    print(f"\n  {word}")
    print(f"  {'-' * (len(word) + 2)}")
    print(f"  morphological segmentation : {morph}")
    if a.analyzed:
        parts = "  +  ".join(f"{m.surface} ({KIND_LABEL.get(m.kind, m.kind)})"
                             for m in a.morphs)
        print(f"  what each piece is         : {parts}")
        print(f"  rule that fired            : {a.rule}")
    else:
        print("  what each piece is         : not analysable with the current lexicon")
        print("  why                        : no licensed affix strips to a known root")

    if tok is not None:
        pieces = [p.replace("▁", "") for p in tok.tokenize_word(word)]
        print(f"  tokenizer output           : {' | '.join(pieces)}")
        if a.analyzed:
            same = [m.surface for m in a.morphs] == pieces
            print(f"  do they agree?             : "
                  + ("yes" if same else "no — the merge table split it differently (Issue T-5)"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*")
    ap.add_argument("--plain", action="store_true",
                    help="print only the morphological split, one line per word")
    a = ap.parse_args()

    seg, tok = load()

    if a.words:
        for w in a.words:
            show(w, seg, tok, a.plain)
        return 0

    print("=" * 60)
    print("Kapampangan morphological segmenter")
    print("Type a word and press Enter. Blank line or Ctrl-C to quit.")
    print("=" * 60)
    while True:
        try:
            w = input("\nword> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not w:
            return 0
        for token in w.split():
            show(token, seg, tok)


if __name__ == "__main__":
    sys.exit(main())
