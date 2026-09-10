"""Build two deliverables:

  1. DATASET_INVENTORY.csv (repo root) -- every thesis-relevant dataset,
     separated and labelled: category, direction/type, live row count,
     quality tier, whether a native speaker has reviewed it, rights, and
     what it feeds.

  2. reports/native-speaker-review-sheet.csv -- every PAM<->FIL pair that is
     NOT yet native-speaker verified and is destined for use, in priority
     order, with blank verdict/correction columns.

Row counts are read live from the files; the descriptive metadata is a
curated table here. Re-run any time the datasets change.
"""

from __future__ import annotations

import csv
import hashlib
import random
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
THESIS_ROOT = REPO_ROOT.parent

INVENTORY_CSV = REPO_ROOT / "DATASET_INVENTORY.csv"
REVIEW_CSV = EXPERIMENT_ROOT / "reports/native-speaker-review-sheet.csv"
REVIEW_INSTRUCTIONS = EXPERIMENT_ROOT / "reports/native-speaker-review-INSTRUCTIONS.txt"

SEED = 20260903
BIBLE_REVIEW_SAMPLE = 200  # 3,084 verses can't be hand-reviewed; a spot-check sample

BATCH_LABELS = {
    "P1": "1 - main (please do these first)",
    "P2": "2 - extra",
    "P3": "3 - vocabulary",
    "P4": "4 - double-check",
    "P5": "5 - stories (already native-authored; light spot-check only)",
    "P6": "6 - religious (Bible sample; check the pair aligns, not a full review)",
    "P7": "7 - AI-generated (Gemini conversational/news; needs review)",
}


def rows_in(path: Path) -> str:
    if not path.exists():
        return "missing"
    if path.suffix == ".jsonl":
        return str(sum(1 for _ in path.open(encoding="utf-8")))
    if path.suffix == ".csv":
        with path.open(encoding="utf-8") as handle:
            return str(max(0, sum(1 for _ in handle) - 1))
    return "n/a"


def sha16(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# name, rel_path (repo unless ../), category, type/direction, tier,
# native_reviewed, rights, provenance, feeds, notes
INVENTORY: list[tuple[str, str, str, str, str, str, str, str, str, str]] = [
    (
        "native-authored story pairs",
        "experiments/parallel_extraction_v2/data/story-pairs.csv",
        "translation",
        "PAM<->FIL sentence (connected narrative)",
        "gold_stories (native-authored)",
        "yes - written/translated by a native Kapampangan speaker (per the user)",
        "author is the user / their collaborator; usable for this research",
        "supplied by the user 2026-09-01 as a sentence-by-sentence .md/PDF",
        "Phase 5 training (primary, use as-is)",
        "15 stories / 174 pairs; modern + cultural register the project otherwise lacks entirely",
    ),
    (
        "v1 PLD matched pairs",
        "experiments/parallel_extraction_v1/reports/matched-pairs.csv",
        "translation",
        "PAM<->FIL sentence + word",
        "gold (spot-checked)",
        "partial - user spot-check (user is not a native speaker)",
        "PLD archive; redistribution unresolved",
        "manual close-reading alignment of the PLD elicitation lists",
        "Phase 5 held-out test-set candidate",
        "26 sentence-level + ~12 Iso word-level; 1 pair removed after review",
    ),
    (
        "v1 external vocab pairs",
        "experiments/parallel_extraction_v1/reports/external-vocab-pairs.csv",
        "translation",
        "PAM<->FIL vocabulary",
        "silver (dictionary-verified)",
        "no",
        "derived from an AI-generated file; verified vs Forman/Bergano/Samson",
        "per-item check against 3 primary dictionaries",
        "Phase 5 auxiliary",
        "word/short-phrase level; meaning still non-native-unverified",
    ),
    (
        "v2 verified pairs -- silver_a",
        "experiments/parallel_extraction_v2/data/verified-pairs.csv",
        "translation",
        "PAM<->FIL sentence",
        "silver (high)",
        "no - three NON-native passes only",
        "PLD archive; redistribution unresolved",
        "LaBSE+MNN sweep + user dict-alignment + Claude read-through",
        "Phase 5 training (primary)",
        "232 rows inside verified-pairs.csv (tier=silver_a)",
    ),
    (
        "v2 verified pairs -- silver_b",
        "experiments/parallel_extraction_v2/data/verified-pairs.csv",
        "translation",
        "PAM<->FIL sentence",
        "silver (medium)",
        "no - three NON-native passes only",
        "PLD archive; redistribution unresolved",
        "same as silver_a, weaker similarity band",
        "Phase 5 training (optional)",
        "93 rows inside verified-pairs.csv (tier=silver_b)",
    ),
    (
        "v2 raw candidate pairs",
        "experiments/parallel_extraction_v2/data/candidate-pairs.csv",
        "translation",
        "PAM<->FIL sentence",
        "unverified candidates",
        "no",
        "PLD archive; redistribution unresolved",
        "LaBSE + lexical sweep over the full distinct-sentence pools",
        "superseded by verified-pairs.csv",
        "849 rows; 314 mutual-best",
    ),
    (
        "PLOC Kapampangan<->Tagalog Bible corpus",
        "experiments/parallel_extraction_v2/resources/kapampangan-tagalog-bible-parallel.csv",
        "translation",
        "PAM<->FIL (Tagalog) verse-aligned",
        "silver (committee translation; folded as tier=bible)",
        "no - committee translation, not reviewed for this project",
        "UNRESOLVED - from a groupmate; believed PLOC/DLSU LTL (LGPL) but unconfirmed",
        "supplied by the user 2026-09-03 (groupmate extract); the proposal's PRIMARY dataset",
        "Phase 5 training (PRIMARY) + in-domain test_bible",
        "3,085 verses (Gen 1527 / Deut 956 / Jud 602); 1 dup dropped (Deut 28:29==28:30 in source)",
    ),
    (
        "Gemini sentence batch",
        "experiments/parallel_extraction_v1/resources/gemini_kapampangan_sentence_batch.md",
        "translation",
        "PAM<->FIL sentence (conversational / news)",
        "silver (AI-generated, word-attested only; folded as tier=silver_gemini)",
        "no - external review still out; also queued as review batch 7",
        "AI-generated (Google/Gemini), pasted in chat; no source",
        "mechanical word-attestation check + >=77% attestation / no flagged Tagalog filter",
        "Phase 5 training (supplementary, register diversity)",
        "500 sentences -> 430 kept as silver_gemini, 70 dropped (~14%)",
    ),
    (
        "translation_gold_v1 triage",
        "experiments/translation_gold_v1/reports/mt-pair-triage.csv",
        "translation",
        "PAM<->FIL",
        "mostly rejected (10 correct of 250)",
        "no",
        "PLD auto-match set; redistribution unresolved",
        "0-3 rubric triage of the 250-row curated auto-match CSV",
        "reference / audit only",
        "confirms the auto-matched set is not usable parallel data",
    ),
    (
        "curated MT seed (Polytranslator)",
        "../curated_research_dataset/kapampangan_mt_seed_curated.csv",
        "translation",
        "EN<->PAM sentence",
        "silver (needs_linguist_review)",
        "no",
        "polytranslator.com dictionary; scrape rights per site",
        "seeded from the Polytranslator dictionary",
        "Phase 5 auxiliary candidate (wrong language pair for the thesis)",
        "710 rows; English target, not Filipino",
    ),
    (
        "SMOL / GATITOS en_pam",
        "experiments/parallel_extraction_v2/resources/smol-gatitos-en_pam.jsonl",
        "translation / lexicon",
        "EN->PAM lexicon + short phrase",
        "professional (external human)",
        "external professional vendor (not this project)",
        "CC-BY-4.0 (attribution) - cleanly usable",
        "Google SMOL release; arXiv 2502.12301 / 2303.15265",
        "auxiliary / lexicon cross-check; NOT folded into PAM->FIL training (wrong direction)",
        "3,993 entries; 93% single words; copied into the repo 2026-09-03 with a manifest",
    ),
    (
        "morphology_gold_v1 dataset",
        "experiments/morphology_gold_v1/resources/kapampangan_morph_annotated_dataset.csv",
        "morphology",
        "PAM word -> segmentation",
        "silver",
        "partial - 97 rows user-adjudicated (non-native)",
        "external CSV, copied with provenance",
        "4-signal mechanical triage + user adjudication of the F tier",
        "Phase 3 (done)",
        "650 rows; tiers A 220 / B 306 / C 26 / D 1 / F 97",
    ),
    (
        "tokenizer_selection_v1 morphology reference",
        "experiments/tokenizer_selection_v1/data/reference-morphology.csv",
        "morphology",
        "PAM word -> boundary gold",
        "silver + partial user adjudication",
        "no",
        "derived from morphology_gold_v1",
        "Tier A/B silver + Tier F user verdicts; 50/50 root-disjoint split",
        "Phase 3 tokenizer selection (done)",
        "534 rows (dev 272 / test 262)",
    ),
    (
        "v4 morphology index",
        "experiments/expanded_morphology_v4/runs/segmentations/morphology-index.jsonl",
        "morphology",
        "PAM word -> morphemes",
        "silver (rule-derived)",
        "no",
        "derived from the preserved training inventory",
        "v4 recursive analyzer over 143,529 word types",
        "MorphBPE training boundaries",
        "13,615 accepted analyses; gitignored (under runs/)",
    ),
    (
        "source_adjudicated_v2 training lexicon",
        "experiments/source_adjudicated_v2/resources/training-lexicon.json",
        "lexicon",
        "PAM roots + compounds",
        "silver (conservative adjudicated)",
        "no",
        "multi-source; local research use",
        "frozen conservative v2 policy over reconciled evidence",
        "root validation for all MorphBPE experiments",
        "3,311 roots + 26 compounds + 118 sample inflected forms",
    ),
    (
        "internet root reconciliation evidence",
        "experiments/internet_root_reconciliation_v1/reports/word-evidence.csv",
        "lexicon",
        "PAM word -> page-cited source evidence",
        "reference (page-cited)",
        "no",
        "local research use; sources' rights separate",
        "every training word type vs Forman/Bergano/Samson/ACD/Kaikki",
        "morphology triage cross-check; reference",
        "143,529 rows",
    ),
    (
        "curated local lexicon",
        "../curated_research_dataset/kapampangan_lexicon_local_curated.csv",
        "lexicon",
        "PAM lexicon",
        "silver (scraped/curated)",
        "no",
        "local curation",
        "prior-session curation",
        "reference / corroboration",
        "4,971 rows",
    ),
    (
        "curated Polytranslator lexicon",
        "../curated_research_dataset/kapampangan_lexicon_polytranslator_curated.csv",
        "lexicon",
        "PAM lexicon",
        "silver (scraped)",
        "no",
        "polytranslator.com",
        "prior-session scrape",
        "reference / corroboration",
        "216 rows",
    ),
    (
        "kapampangan-general-corpus-v1 (monolingual)",
        "(external) D:/DevTools/KapampanganTokenizer/kapampangan-general-corpus-v1/data/",
        "monolingual",
        "PAM sentences (no translation)",
        "experimental (human validation not claimed)",
        "no",
        "DATASET_CARD: public redistribution not claimed",
        "DevTools build; 80/10/10 split, seed 20260816",
        "tokenizer vocab/penalty selection (Phase 3)",
        "train 90,184 / validation 9,633 / test 9,295",
    ),
    (
        "preserved training inventory",
        "experiments/source_adjudicated_v2/runs/prepared/training-stream.jsonl",
        "monolingual",
        "PAM word types + frequencies",
        "frozen aggregate",
        "no",
        "local research use",
        "hash-verified preserved aggregate training stream",
        "all Plain-BPE / MorphBPE training",
        "143,529 word types; gitignored (under runs/)",
    ),
    (
        "POS PLD candidates",
        "../curated_research_dataset/kapampangan_pos_pld_curated.csv",
        "other",
        "PAM POS tag candidates",
        "unlabelled candidates",
        "no",
        "PLD archive; redistribution unresolved",
        "parsed from PLD; not gold-tagged",
        "not used by the thesis",
        "826 rows",
    ),
    (
        "source OCR / extracted text",
        "runs/source-ocr/ + runs/source-ocr-v2/",
        "source text",
        "PAM / EN reference text",
        "extracted (rights unresolved)",
        "no",
        "Forman/Mirikitani/Bergano/Samson etc.; rights unresolved",
        "OCR + embedded-text extraction (two passes)",
        "evidence for morphology/lexicon work only",
        "gitignored; not redistributable",
    ),
]


def build_inventory() -> None:
    fields = [
        "name",
        "path",
        "category",
        "type_or_direction",
        "quality_tier",
        "native_speaker_reviewed",
        "rights_license",
        "provenance",
        "feeds",
        "live_rows",
        "sha256_16",
        "notes",
    ]
    out: list[dict[str, str]] = []
    for name, rel, cat, typ, tier, nat, rights, prov, feeds, notes in INVENTORY:
        if rel.startswith("(external)") or rel.startswith("runs/"):
            live, sh = "see notes", ""
        else:
            base = THESIS_ROOT if rel.startswith("../") else REPO_ROOT
            p = (base / rel.removeprefix("../")).resolve()
            live, sh = rows_in(p), sha16(p)
        out.append(
            {
                "name": name,
                "path": rel,
                "category": cat,
                "type_or_direction": typ,
                "quality_tier": tier,
                "native_speaker_reviewed": nat,
                "rights_license": rights,
                "provenance": prov,
                "feeds": feeds,
                "live_rows": live,
                "sha256_16": sh,
                "notes": notes,
            }
        )
    with INVENTORY_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(f"wrote {INVENTORY_CSV}  ({len(out)} datasets)")


# ---------------------------------------------------------------------------


def _norm(s: str) -> str:
    return " ".join(s.split())


def build_review_sheet() -> None:
    verified = list(
        csv.DictReader((EXPERIMENT_ROOT / "data/verified-pairs.csv").open(encoding="utf-8"))
    )
    v1_matched = list(
        csv.DictReader(
            (REPO_ROOT / "experiments/parallel_extraction_v1/reports/matched-pairs.csv").open(
                encoding="utf-8"
            )
        )
    )
    v1_vocab = list(
        csv.DictReader(
            (
                REPO_ROOT / "experiments/parallel_extraction_v1/reports/external-vocab-pairs.csv"
            ).open(encoding="utf-8")
        )
    )

    rows: list[dict[str, str]] = []
    n = 0

    def add(priority: str, pam: str, fil: str, handle: str = "") -> None:
        nonlocal n
        n += 1
        rows.append(
            {
                "id": handle or f"rv_{n:04d}",
                "batch": BATCH_LABELS[priority],
                "kapampangan": _norm(pam),
                "filipino": _norm(fil),
                "correct": "",
                "comment": "",
            }
        )

    for r in verified:
        if r["tier"] == "silver_a":
            add("P1", r["pam_text"], r["fil_text"])
    for r in verified:
        if r["tier"] == "silver_b":
            add("P2", r["pam_text"], r["fil_text"])
    for r in v1_vocab:
        add("P3", r["pam_text"], r["fil_text"])
    for r in v1_matched:
        add("P4", r["pam_text"], r["fil_text"])
    story_csv = EXPERIMENT_ROOT / "data/story-pairs.csv"
    if story_csv.exists():
        for r in csv.DictReader(story_csv.open(encoding="utf-8")):
            add("P5", r["pam_text"], r["fil_text"])

    # batch 6: a seeded sample of the Bible corpus (full corpus too large for
    # a hand review) -- the id carries the verse ref so systematic
    # misalignment (e.g. the Deut 28:29==28:30 source dup) is catchable
    bible = [r for r in verified if r["tier"] == "bible"]
    random.Random(SEED).shuffle(bible)
    for r in bible[:BIBLE_REVIEW_SAMPLE]:
        ref = r["signal"].split("ref=", 1)[-1] if "ref=" in r["signal"] else r["pair_id"]
        add("P6", r["pam_text"], r["fil_text"], handle=ref)

    # batch 7: every Gemini row that passed the silver filter
    for r in verified:
        if r["tier"] == "silver_gemini":
            add("P7", r["pam_text"], r["fil_text"])

    fields = ["id", "batch", "kapampangan", "filipino", "correct", "comment"]
    REVIEW_CSV.parent.mkdir(parents=True, exist_ok=True)
    with REVIEW_CSV.open("w", encoding="utf-8", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    REVIEW_INSTRUCTIONS.write_text(
        "How to fill in native-speaker-review-sheet.csv\n"
        "============================================\n\n"
        "Each row is a Kapampangan sentence and its supposed Filipino translation.\n"
        "Please fill in two columns:\n\n"
        "  correct  -> y   (the Filipino is a correct translation of the Kapampangan)\n"
        "              n   (it is wrong: wrong meaning, or not a translation at all)\n"
        "              p   (partly right: understandable but has an error)\n"
        "              ?   (you are not sure)\n\n"
        "  comment  -> only if 'n' or 'p': say what is wrong, and if you can, write\n"
        "              the correct Kapampangan and/or Filipino. Free text, any format.\n\n"
        "Leave 'id' and 'batch' untouched (they are just for matching afterwards).\n\n"
        "Batches, in order of importance:\n"
        "  1 - main         : the sentences we most want to use. Please do these first.\n"
        "  2 - extra        : lower-confidence sentences.\n"
        "  3 - vocabulary   : short word / phrase pairs.\n"
        "  4 - double-check : pairs already checked once; a second look.\n"
        "  5 - stories      : native-authored story sentences; just a light spot-check\n"
        "                     for typos / obvious slips, not a full review.\n"
        "  6 - religious    : a sample of Bible verse pairs (Kapampangan <-> Tagalog).\n"
        "                     The 'id' is the verse reference. Main thing to catch:\n"
        "                     the Kapampangan and Tagalog being DIFFERENT verses, or\n"
        "                     an obviously wrong translation. Not a full review.\n"
        "  7 - AI-generated : Gemini-made conversational / news sentences. These are\n"
        "                     machine-generated and unreviewed - please check properly.\n\n"
        "If you only have time for batch 1 (and maybe 2), that is already very useful.\n",
        encoding="utf-8",
        newline="\n",
    )

    from collections import Counter

    by_b = Counter(r["batch"] for r in rows)
    print(f"wrote {REVIEW_CSV}  ({len(rows)} rows, 6 columns)")
    for b in sorted(by_b):
        print(f"  {b}: {by_b[b]}")
    print(f"wrote {REVIEW_INSTRUCTIONS}")


def main() -> int:
    build_inventory()
    build_review_sheet()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
