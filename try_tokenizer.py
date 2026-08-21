"""Quick local test of the trained tokenizer. No pip installs needed.

    python try_tokenizer.py               # run the built-in checks
    python try_tokenizer.py --interactive # type your own Kapampangan sentences
    python try_tokenizer.py --compare     # Morph-BPE vs the plain-BPE control
    python try_tokenizer.py --tokenizer path/to/morphbpe.json

Only the Python standard library is used, so this runs on a bare Python 3.10+
install. The tokenizer file is self-contained: vocabulary plus merge rules, no
lexicon required at runtime (thesis p. 42).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

try:
    from kapampangan_mt.tokenizer import KapampanganTokenizer
except ModuleNotFoundError:
    print("ERROR: cannot find the kapampangan_mt package.")
    print(f"       Expected it at: {HERE / 'src'}")
    print("       Run this script from inside the kapampangan-morphbpe folder.")
    sys.exit(1)

DEFAULT = HERE / "artifacts" / "tokenizer" / "morphbpe.json"
CONTROL = HERE / "artifacts" / "tokenizer" / "plainbpe.json"

# Sentences drawn from the actual corpus, plus the thesis' own examples.
SAMPLES = [
    "Kinan ne ing pamangan king bale.",
    "King kamumulan lelangan na ning Dios ing banua at ing labuad.",
    "Sinulat ne ing kalatas kang Jose.",
    "E ku balu nung nokarin ya ing anak.",
    "Masanting ya ing aldo ngeni.",
]
WORDS = [
    ("kinan", "thesis p.3: kan + -in- (perfective)"),
    ("kuman", "thesis p.3: kan + -um- (actor focus)"),
    ("kan", "the bare root"),
    ("sumulat", "sulat + -um-"),
    ("sinulat", "sulat + -in-"),
    ("balemi", "bale + clitic -mi"),
    ("gagawa", "reduplication of gawa"),
    ("kapampangan", "ka- + pampang + -an"),
    ("makapagsulat", "makapag- + sulat"),
    ("zzqwerty", "nonsense — must still tokenise, never crash"),
    ("日本語", "unseen script — byte fallback must handle it"),
]


def check(label: str, ok: bool, detail: str = "") -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  — {detail}" if detail else ""))
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenizer", default=str(DEFAULT))
    ap.add_argument("--interactive", action="store_true")
    ap.add_argument("--compare", action="store_true")
    a = ap.parse_args()

    path = Path(a.tokenizer)
    if not path.exists():
        print(f"ERROR: tokenizer not found at {path}")
        print("       Train one first:  python scripts/03_train_tokenizer.py")
        return 1

    tok = KapampanganTokenizer.load(path)
    stats = (tok.meta or {}).get("stats", {})
    print("=" * 72)
    print(f"loaded: {path.name}   ({path.stat().st_size / 1024:.0f} KB)")
    print(f"  vocabulary size      : {tok.vocab_size:,}")
    print(f"  merge rules          : {len(tok.merges):,}")
    print(f"  trained on           : {stats.get('n_word_types', '?')} word types")
    print(f"  boundary-constrained : {stats.get('constrained', '?')}"
          f"   <- True means this is Morph-BPE, False means the plain control")
    print("=" * 72)

    if a.interactive:
        print("\nType a Kapampangan sentence and press Enter. Blank line or Ctrl-C to quit.\n")
        while True:
            try:
                line = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                break
            pieces = tok.tokenize(line)
            n_words = len(line.split())
            print(f"  tokens ({len(pieces)}): {pieces}")
            print(f"  ids           : {tok.encode(line)}")
            print(f"  decoded back  : {tok.decode(tok.encode(line))!r}")
            print(f"  fertility     : {len(pieces) / max(n_words, 1):.2f} tokens/word\n")
        return 0

    if a.compare:
        if not CONTROL.exists():
            print(f"\ncontrol tokenizer not found at {CONTROL}")
            print("train it with:  python scripts/03_train_tokenizer.py --plain-bpe")
            return 1
        plain = KapampanganTokenizer.load(CONTROL)
        print(f"\n{'word':<16}{'Morph-BPE':<34}{'plain BPE (control)'}")
        print("-" * 84)
        for w, _why in WORDS[:9]:
            print(f"{w:<16}{' '.join(tok.tokenize_word(w)):<34}"
                  f"{' '.join(plain.tokenize_word(w))}")
        print("\nMorph-BPE should split more often at real morpheme joints;")
        print("plain BPE tends to keep frequent whole words in one piece.")
        return 0

    # ---------------- built-in checks ----------------
    print("\nWORD-LEVEL BEHAVIOUR")
    for w, why in WORDS:
        pieces = tok.tokenize_word(w)
        print(f"  {w:<14} -> {' '.join(pieces):<38} ({why})")

    print("\nSENTENCE-LEVEL BEHAVIOUR")
    for s in SAMPLES:
        pieces = tok.tokenize(s)
        print(f"  {s}")
        print(f"     {len(pieces)} tokens, {len(pieces)/len(s.split()):.2f} per word")
        print(f"     {pieces}")

    print("\nCORRECTNESS CHECKS")
    ok = True
    for s in SAMPLES:
        back = tok.decode(tok.encode(s))
        want = s.lower().replace(" .", ".")
        ok &= check("round-trip preserves the sentence",
                    back.replace(" .", ".") == want,
                    "" if back.replace(" .", ".") == want else f"{back!r} != {want!r}")
        if back.replace(" .", ".") != want:
            break

    weird = "日本語 zzz ñ á 123 !!"
    ok &= check("unseen characters survive byte fallback",
                "日本語" in tok.decode(tok.encode(weird)))
    ok &= check("special ids match the NLLB layout",
                (tok.bos_id, tok.pad_id, tok.eos_id, tok.unk_id) == (0, 1, 2, 3),
                f"{(tok.bos_id, tok.pad_id, tok.eos_id, tok.unk_id)}")
    ids = tok.encode("kan")
    ok &= check("encode wraps with the language tag and </s>",
                ids[0] == tok.src_lang_id and ids[-1] == tok.eos_id)
    ok &= check("no token is ever unprocessable",
                all(tok.tokenize_word(w) for w, _ in WORDS))

    print("\n" + ("ALL CHECKS PASSED — the tokenizer is working."
                  if ok else "SOME CHECKS FAILED — see above."))
    print("\nTry:  python try_tokenizer.py --interactive")
    print("      python try_tokenizer.py --compare")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
