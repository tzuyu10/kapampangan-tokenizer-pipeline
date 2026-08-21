"""Generate a SYNTHETIC toy parallel corpus so the pipeline runs before the
real data is collected.

    python scripts/make_toy_data.py --n 600

The output is NOT linguistic data. It is combinatorially generated from the
seed lexicon to exercise every code path (prefix, infix, circumfix, clitic,
reduplication, unanalysable words). Delete data/raw/parallel.tsv and replace it
with the real PLOC-derived corpus before producing any result.
"""
from __future__ import annotations

import argparse, csv, random, sys
from pathlib import Path

import _bootstrap  # noqa: F401

VERB_ROOTS = [("sulat", "sulat"), ("basa", "basa"), ("kan", "kain"), ("gawa", "gawa"),
              ("turu", "turo"), ("akit", "kita"), ("dimdam", "dinig"), ("kua", "kuha"),
              ("munta", "punta"), ("balik", "balik"), ("lukluk", "upo"), ("tudtud", "tulog")]
NOUNS = [("bale", "bahay"), ("balen", "bayan"), ("anak", "anak"), ("tau", "tao"),
         ("aldo", "araw"), ("danum", "tubig"), ("bulaklak", "bulaklak"),
         ("kaluguran", "kaibigan"), ("pamangan", "pagkain"), ("salita", "salita"),
         ("asu", "aso"), ("manuk", "manok"), ("nasi", "kanin"), ("dutung", "kahoy")]
ADJ = [("santing", "ganda"), ("lagu", "ganda"), ("yap", "buti"), ("tas", "taas"),
       ("rimla", "lamig"), ("pali", "init"), ("puti", "puti"), ("dakal", "dami")]
PRON = [("ku", "ko"), ("mu", "mo"), ("na", "niya"), ("mi", "namin"), ("da", "nila")]
PLACES = [("king bale", "sa bahay"), ("king balen", "sa bayan"),
          ("king pisamban", "sa simbahan"), ("king eskwela", "sa paaralan")]

TEMPLATES = [
    lambda r: (f"Sinulat ne ing {r['noun'][0]}.", f"Sinulat niya ang {r['noun'][1]}."),
    lambda r: (f"Kinan ne ing {r['noun'][0]} {r['place'][0]}.",
               f"Kinain niya ang {r['noun'][1]} {r['place'][1]}."),
    lambda r: (f"Ma{r['adj'][0]} ing {r['noun'][0]}.", f"Ma{r['adj'][1]} ang {r['noun'][1]}."),
    lambda r: (f"Mag{r['verb'][0]} ya ing anak {r['place'][0]}.",
               f"Mag{r['verb'][1]} siya ang bata {r['place'][1]}."),
    lambda r: (f"{r['verb'][0].capitalize()}an mu ing {r['noun'][0]}.",
               f"{r['verb'][1].capitalize()}an mo ang {r['noun'][1]}."),
    lambda r: (f"Ing ka{r['adj'][0]}an ning {r['noun'][0]} maragul ya.",
               f"Ang ka{r['adj'][1]}an ng {r['noun'][1]} ay malaki."),
    lambda r: (f"Atin kung {r['noun'][0]} {r['place'][0]}.",
               f"May {r['noun'][1]} ako {r['place'][1]}."),
    lambda r: (f"E ku balu nung nokarin ya ing {r['noun'][0]}.",
               f"Hindi ko alam kung nasaan ang {r['noun'][1]}."),
    lambda r: (f"Panga{r['verb'][0]}an ning {r['noun'][0]} masalese ya.",
               f"Ang pag{r['verb'][1]} ng {r['noun'][1]} ay maayos."),
    lambda r: (f"{r['noun'][0].capitalize()}{r['pron'][0]} ing makanini.",
               f"{r['noun'][1].capitalize()} {r['pron'][1]} ang ganito."),
    lambda r: (f"Kuman la reng {r['noun'][0]} king aldo.",
               f"Kumain sila ng {r['noun'][1]} sa araw."),
    lambda r: (f"Ma{r['adj'][0]} at ma{r['adj'][0]} ing {r['noun'][0]} keni.",
               f"Ma{r['adj'][1]} at ma{r['adj'][1]} ang {r['noun'][1]} dito."),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=600)
    ap.add_argument("--out", default="data/raw/parallel.tsv")
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()
    rng = random.Random(a.seed)

    rows, seen = [], set()
    while len(rows) < a.n:
        r = {"verb": rng.choice(VERB_ROOTS), "noun": rng.choice(NOUNS),
             "adj": rng.choice(ADJ), "pron": rng.choice(PRON), "place": rng.choice(PLACES)}
        src, tgt = rng.choice(TEMPLATES)(r)
        if (src, tgt) in seen:
            continue
        seen.add((src, tgt))
        rows.append((src, tgt, rng.choice(["religious", "conversational", "news"]), "TOY"))

    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["pam", "fil", "domain", "source"])
        w.writerows(rows)
    print(f"wrote {len(rows)} SYNTHETIC pairs -> {out}")
    print("!! replace with real data before reporting anything !!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
