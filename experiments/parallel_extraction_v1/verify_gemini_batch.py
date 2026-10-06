"""Mechanical word-level attestation check for the 500-sentence Gemini batch
(resources/gemini_kapampangan_sentence_batch.md).

Per explicit user decision (2026-08-26): given the batch's scale (500 items)
and grammatical complexity (full sentences with subordination, negation,
aspect marking -- not just vocabulary), this check is deliberately scoped
to what a mechanical pass can actually support: does each PAM content word
in each sentence appear in this project's own existing attestation evidence
(word-evidence.csv's comparison_key index and/or training-lexicon.json's
roots)? This does NOT judge whether a sentence's grammar, meaning, or
word choice is correct -- that requires native-speaker/linguist review,
which this project has consistently deferred elsewhere and is out of scope
here. A sentence where every word is attested may still be poor or wrong
Kapampangan; a sentence with an unattested word may still be perfectly
correct (this project's dictionary sources have known, documented gaps,
e.g. several basic words in the companion external-vocab check were
unattested but plausible). Treat the output as a coverage signal only.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MD_PATH = BASE_DIR / "resources" / "gemini_kapampangan_sentence_batch.md"
WORD_EVIDENCE_PATH = (
    BASE_DIR.parent / "internet_root_reconciliation_v1" / "reports" / "word-evidence.csv"
)
LEXICON_PATH = BASE_DIR.parent / "source_adjudicated_v2" / "resources" / "training-lexicon.json"
OUTPUT_CSV = BASE_DIR / "reports" / "gemini-batch-word-attestation.csv"
OUTPUT_REPORT = BASE_DIR / "reports" / "gemini-batch-word-attestation.md"

# 4-column rows (sections 1-8): | # | Tagalog | Kapampangan | English |
ROW4_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")
# 5-column rows (sections 9-11): | # | Filipino | Kapampangan | English | Grammatical Feature |
ROW5_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$")

STOPWORD_HEADERS = {"tagalog (filipino)", "filipino (tagalog)", "#"}


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for line in MD_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        m5 = ROW5_RE.match(line)
        if m5:
            num, fil, pam, eng, feature = m5.groups()
            if fil.strip().lower() in STOPWORD_HEADERS or fil.startswith("---"):
                continue
            rows.append({"num": int(num), "fil": fil, "pam": pam, "eng": eng, "feature": feature})
            continue
        m4 = ROW4_RE.match(line)
        if m4:
            num, fil, pam, eng = m4.groups()
            if fil.strip().lower() in STOPWORD_HEADERS or fil.startswith("---") or not num.isdigit():
                continue
            rows.append({"num": int(num), "fil": fil, "pam": pam, "eng": eng, "feature": ""})
    # De-duplicate: 5-column rows also match the 4-column-minus-one pattern
    # in some edge cases; keep the first parse per item number.
    seen: dict[int, dict] = {}
    for r in rows:
        seen.setdefault(r["num"], r)
    return [seen[n] for n in sorted(seen)]


def pam_content_tokens(pam_field: str) -> list[str]:
    # Strip italics/markup, split into words, drop pure punctuation/digits.
    text = re.sub(r"[*_]", "", pam_field)
    text = re.sub(r"[.,;:!?()\"'‘’“”]", " ", text)
    tokens = []
    for tok in text.split():
        key = tok.strip().lower()
        key = re.sub(r"^-+|-+$", "", key)
        if not key or key.isdigit():
            continue
        tokens.append(key)
    return tokens


def load_word_evidence_keys() -> set[str]:
    keys = set()
    with WORD_EVIDENCE_PATH.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            keys.add(row["comparison_key"])
    return keys


def load_lexicon_roots() -> set[str]:
    with LEXICON_PATH.open(encoding="utf-8") as f:
        lex = json.load(f)
    return {r["comparison_key"] for r in lex["roots"]}


def main() -> None:
    rows = load_rows()
    evidence_keys = load_word_evidence_keys()
    lexicon_roots = load_lexicon_roots()
    attested_keys = evidence_keys | lexicon_roots

    out_rows = []
    for row in rows:
        tokens = pam_content_tokens(row["pam"])
        n_tokens = len(tokens)
        n_attested = sum(1 for t in tokens if t in attested_keys)
        unattested = [t for t in tokens if t not in attested_keys]
        pct = (n_attested / n_tokens * 100) if n_tokens else 0.0
        out_rows.append(
            {
                "item_num": row["num"],
                "pam_text": row["pam"],
                "fil_text": row["fil"],
                "n_tokens": n_tokens,
                "n_attested": n_attested,
                "pct_attested": round(pct, 1),
                "unattested_tokens": ", ".join(unattested),
            }
        )

    fieldnames = [
        "item_num",
        "pam_text",
        "fil_text",
        "n_tokens",
        "n_attested",
        "pct_attested",
        "unattested_tokens",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    total_sentences = len(out_rows)
    total_tokens = sum(r["n_tokens"] for r in out_rows)
    total_attested = sum(r["n_attested"] for r in out_rows)
    fully_attested = sum(1 for r in out_rows if r["n_tokens"] > 0 and r["n_attested"] == r["n_tokens"])
    zero_attested = sum(1 for r in out_rows if r["n_tokens"] > 0 and r["n_attested"] == 0)

    # Frequency of unattested tokens across the whole batch, to spot
    # systematic gaps (a word appearing unattested many times is a more
    # useful signal than a one-off).
    from collections import Counter

    unattested_counter: Counter[str] = Counter()
    for r in out_rows:
        if r["unattested_tokens"]:
            for tok in r["unattested_tokens"].split(", "):
                unattested_counter[tok] += 1

    summary = {
        "total_sentences": total_sentences,
        "total_pam_content_tokens": total_tokens,
        "total_attested_tokens": total_attested,
        "overall_token_attestation_pct": round(total_attested / total_tokens * 100, 1) if total_tokens else 0.0,
        "sentences_fully_attested": fully_attested,
        "sentences_fully_attested_pct": round(fully_attested / total_sentences * 100, 1),
        "sentences_zero_attested": zero_attested,
        "top_30_unattested_tokens_by_frequency": unattested_counter.most_common(30),
    }

    with OUTPUT_REPORT.open("w", encoding="utf-8", newline="\n") as f:
        f.write("# Gemini batch -- mechanical word-attestation check\n\n")
        f.write(
            "Coverage signal only (see module docstring in `verify_gemini_batch.py` "
            "for exactly what this does and does not verify).\n\n"
        )
        f.write(f"- Total sentences checked: {summary['total_sentences']}\n")
        f.write(f"- Total PAM content tokens: {summary['total_pam_content_tokens']}\n")
        f.write(
            f"- Overall token attestation: {summary['total_attested_tokens']} / "
            f"{summary['total_pam_content_tokens']} "
            f"({summary['overall_token_attestation_pct']}%)\n"
        )
        f.write(
            f"- Sentences with every content word attested: {summary['sentences_fully_attested']} "
            f"({summary['sentences_fully_attested_pct']}%)\n"
        )
        f.write(f"- Sentences with zero attested content words: {summary['sentences_zero_attested']}\n\n")
        f.write("## Most frequent unattested tokens (top 30)\n\n")
        f.write("| Token | Occurrences |\n| --- | --- |\n")
        for tok, count in summary["top_30_unattested_tokens_by_frequency"]:
            f.write(f"| {tok} | {count} |\n")

    print(json.dumps({k: v for k, v in summary.items() if k != "top_30_unattested_tokens_by_frequency"}, indent=2))
    print("\nTop 15 unattested tokens by frequency:")
    for tok, count in summary["top_30_unattested_tokens_by_frequency"][:15]:
        print(f"  {tok}: {count}")


if __name__ == "__main__":
    main()
