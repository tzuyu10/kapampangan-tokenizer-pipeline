"""Build the close-reading-matched PAM-FIL sentence pair candidate set.

Every pair below is identified only by (language, source_name_normalized,
prompt_ordinal) -- a reference into the copied canonical prompt inventory,
never a hand-retyped copy of the Kapampangan/Filipino text itself. This
avoids corrupting accented/curly-quote characters through manual
transcription; the actual text is looked up programmatically from
resources/pld_prompt_inventory_pam_fil.csv, which is a byte-identical copy
of the external source (see resources/provenance-manifest.json).

Matching was done by direct close reading of every candidate domain's full
canonical slot list (same manual method as translation_gold_v1's MT-pair
triage), not by ordinal position and not by an automated similarity model.
See reports/parallel-extraction-summary.md for full domain-by-domain
methodology, including which domains were checked and rejected as
non-parallel.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INVENTORY_PATH = BASE_DIR / "resources" / "pld_prompt_inventory_pam_fil.csv"
OUTPUT_CSV = BASE_DIR / "reports" / "matched-pairs.csv"
OUTPUT_STATS = BASE_DIR / "reports" / "matched-pairs-stats.json"

# (pam_domain, pam_ordinal, fil_domain, fil_ordinal, confidence, basis, note)
# confidence: "high" or "medium"
# basis: exact_translation | exact_translation_partial | conceptual_paraphrase | cross_domain_exact
PAIRS: list[tuple[str, int, str, int, str, str, str]] = [
    # --- Utt_Greetings.txt ---
    ("Utt_Greetings.txt", 11, "Utt_Greetings.txt", 1, "high", "exact_translation", ""),
    ("Utt_Greetings.txt", 3, "Utt_Greetings.txt", 2, "high", "exact_translation", ""),
    ("Utt_Greetings.txt", 5, "Utt_Greetings.txt", 8, "high", "exact_translation", ""),
    (
        "Utt_Greetings.txt",
        13,
        "Utt_Greetings.txt",
        9,
        "high",
        "exact_translation",
        "User review (2026-08-26): valid translation but carries a politeness-level mismatch -- "
        "PAM 'ye pu' is polite/plural register, FIL 'mo' is informal/singular.",
    ),
    ("Utt_Greetings.txt", 2, "Utt_Greetings.txt", 11, "high", "exact_translation", ""),
    ("Utt_Greetings.txt", 15, "Utt_Greetings.txt", 10, "high", "exact_translation", ""),
    (
        "Utt_Greetings.txt",
        9,
        "Utt_CommonExpressions.txt",
        12,
        "medium",
        "cross_domain_exact",
        "PAM slot filed under Greetings, FIL counterpart filed under CommonExpressions -- "
        "domain boundaries are not consistent across the two languages' elicitation sessions.",
    ),
    # --- Utt_Salawikain.txt (proverbs) ---
    ("Utt_Salawikain.txt", 1, "Utt_Salawikain.txt", 10, "high", "exact_translation", ""),
    ("Utt_Salawikain.txt", 11, "Utt_Salawikain.txt", 8, "high", "exact_translation", ""),
    ("Utt_Salawikain.txt", 15, "Utt_Salawikain.txt", 7, "high", "exact_translation", ""),
    (
        "Utt_Salawikain.txt",
        3,
        "Utt_Salawikain.txt",
        15,
        "medium",
        "conceptual_paraphrase",
        "Same 'true friend' proverb theme; predicate differs (treasure vs. always-companion) "
        "so this is equivalent wisdom, not a literal word-for-word translation.",
    ),
    # NOTE: a PAM Utt_Salawikain.txt slot 9 / FIL slot 5 pair was proposed here (walking-pace
    # proverb vs. a river proverb) and rejected on user review (2026-08-26): these are two
    # distinct proverbs with different morals (PAM teaches that deliberation/caution leaves a
    # deep, lasting result; FIL teaches that a quiet demeanor can mask hidden depth/danger), not
    # a shared lesson expressed through a different vehicle. Not included as a pair.
    # --- Utt_Essay.txt (folktale comparative essay, shares source material with Story) ---
    ("Utt_Essay.txt", 3, "Utt_Essay.txt", 12, "high", "exact_translation", ""),
    ("Utt_Essay.txt", 4, "Utt_Essay.txt", 5, "high", "exact_translation", ""),
    # --- Story narratives: PAM per-story files <-> FIL's single interleaved Utt_Story.txt ---
    ("Utt_StoryBernardo.txt", 10, "Utt_Story.txt", 4, "high", "exact_translation", ""),
    (
        "Utt_StoryIputipot.txt",
        4,
        "Utt_Story.txt",
        5,
        "high",
        "exact_translation_partial",
        "PAM slot includes an extra lead-in narration sentence before the quoted dialogue; "
        "only the dialogue portion aligns 1:1 with the FIL slot.",
    ),
    ("Utt_StoryBernardo.txt", 9, "Utt_Story.txt", 7, "high", "exact_translation", ""),
    ("Utt_StoryMatsing.txt", 7, "Utt_Story.txt", 8, "high", "exact_translation", ""),
    ("Utt_StoryBernardo.txt", 2, "Utt_Story.txt", 9, "high", "exact_translation", ""),
    (
        "Utt_StoryIputipot.txt",
        1,
        "Utt_Story.txt",
        14,
        "high",
        "exact_translation_partial",
        "PAM slot includes an extra leading quoted sentence ('Mituki cang cacampi...') not "
        "present in the FIL slot; only the 'Sinabi ni Amomongo...' portion aligns 1:1.",
    ),
    (
        "Utt_StoryMatsing.txt",
        5,
        "Utt_Story.txt",
        16,
        "high",
        "exact_translation_partial",
        "PAM slot includes two preceding sentences not present in the FIL slot; only the final "
        "two sentences ('Bayuan da ca king lusong...') align 1:1. User review (2026-08-26): also "
        "note a grammatical mood shift in that aligned portion -- PAM reads as a declarative "
        "statement/threat ('I will pound you...'), FIL as an interrogative offering a choice "
        "('Shall I pound you...?').",
    ),
    ("Utt_StoryIputipot.txt", 10, "Utt_Story.txt", 17, "high", "exact_translation", ""),
    # --- Utt_CommonExpressions.txt ---
    ("Utt_CommonExpressions.txt", 2, "Utt_CommonExpressions.txt", 17, "high", "exact_translation", ""),
    ("Utt_CommonExpressions.txt", 6, "Utt_CommonExpressions.txt", 16, "high", "exact_translation", ""),
    ("Utt_CommonExpressions.txt", 9, "Utt_CommonExpressions.txt", 8, "high", "exact_translation", ""),
    # --- Utt_Interrogatives.txt ---
    (
        "Utt_Interrogatives.txt",
        2,
        "Utt_Interrogatives.txt",
        2,
        "high",
        "exact_translation",
        "User review (2026-08-26): same core question, but note an aspectual shift -- PAM "
        "'Mawawala' is contemplative/future ('will get lost'), FIL 'Nawawala' is imperfective/"
        "present ('is missing'). Would need aspectual alignment for a use case where exact tense/"
        "aspect matters.",
    ),
    ("Utt_Interrogatives.txt", 6, "Utt_Interrogatives.txt", 3, "high", "exact_translation", ""),
    ("Utt_Interrogatives.txt", 3, "Utt_Interrogatives.txt", 12, "high", "exact_translation", ""),
    # --- Iso (word-level) domains ---
    # Ordinal numbers: matched by exact numeric value, not position -- unambiguous by
    # construction (a 27th is a 27th regardless of slot number).
    (
        "Iso_Ordinal.txt",
        7,
        "Iso_Ordinal.txt",
        3,
        "high",
        "exact_numeric_equivalence",
        "Both denote the 27th ordinal (PAM 'Caduampulu't pitung' = FIL 'ikadalawampu't pitong').",
    ),
    (
        "Iso_Ordinal.txt",
        12,
        "Iso_Ordinal.txt",
        5,
        "high",
        "exact_numeric_equivalence",
        "Both denote the 23rd ordinal (PAM 'Caduampulu't atlu' = FIL 'ikadalawampu't tatlo').",
    ),
    (
        "Iso_Time.txt",
        1,
        "Iso_Time.txt",
        5,
        "high",
        "shared_cognate_or_loanword",
        "'present/current' -- PAM 'Salucuiang' and FIL 'kasalukuyang' are the same root.",
    ),
    (
        "Iso_Weather.txt",
        6,
        "Iso_Weather.txt",
        8,
        "high",
        "shared_cognate_or_loanword",
        "'gust of wind' -- PAM 'Bugsu ning angin' and FIL 'bugso ng hangin' are the same words.",
    ),
    (
        "Iso_Weather.txt",
        7,
        "Iso_Weather.txt",
        6,
        "high",
        "shared_cognate_or_loanword",
        "'humid/humidity' -- PAM 'Maialumigmig' (adjective) and FIL 'halumigmig' (noun) share "
        "the same root; grammatical category differs slightly.",
    ),
    (
        "Iso_Weather.txt",
        1,
        "Iso_Weather.txt",
        5,
        "medium",
        "same_concept_different_word",
        "'cloudy/overcast' -- same weather concept, non-cognate words (PAM 'Madalumdum', FIL "
        "'makulimlim').",
    ),
    (
        "Iso_Educ.txt",
        9,
        "Iso_Educ.txt",
        8,
        "high",
        "shared_cognate_or_loanword",
        "Same proper noun: Spain (PAM 'Espana', FIL 'Espanya').",
    ),
    (
        "Iso_Educ.txt",
        13,
        "Iso_Educ.txt",
        7,
        "medium",
        "shared_cognate_or_loanword",
        "'arrival/arrived' -- shared root 'dating' (PAM 'Pangaratang', FIL 'dumating'); "
        "grammatical form differs (noun vs. verb).",
    ),
    (
        "Iso_BodyParts.txt",
        13,
        "Iso_BodyParts.txt",
        3,
        "medium",
        "shared_cognate_or_loanword",
        "'ring finger' (tentative) -- identical wordform ('palakingkingan') on both sides. User "
        "review (2026-08-28): downgraded from high confidence -- direct full-text search of "
        "Forman (1971), Bergano (1732/Samson translation), and Samson (2011) found zero hits "
        "for 'palakingking' or 'palasingsing' in any of the three; this word is not "
        "independently attested by primary sources, only inferred from the FIL synonym "
        "'palasingsingan' sharing the 'singsing' (ring) root.",
    ),
    # NOTE: a PAM Iso_BodyParts.txt slot 14 ('Malingmingan') / FIL slot 13 ('kalingkingan')
    # pair was proposed here as 'pinky finger' on the strength of a shared '-lingking-'
    # surface pattern, and rejected on direct dictionary verification (2026-08-28):
    # Forman (1971) p.69 glosses 'kalingki'ngan' as 'little finger' (confirmed correct), but
    # Bergano's 1732 dictionary (Samson translation) p.266 glosses 'MALINGMINGAN' as "the
    # temples / sides of the head" (Latin tempora) -- not a finger at all. The two words are
    # not actually related; this was a false-cognate match from surface similarity alone,
    # exactly the error class this project's Phase 1 adjudication already flagged once (the
    # 'galang-galangan' wrist/ankle case). No FIL word for "temples" appears in this specific
    # Iso_BodyParts.txt list, so no replacement pair is proposed. Not included.
    (
        "Iso_Kinship.txt",
        9,
        "Iso_Kinship.txt",
        4,
        "high",
        "shared_cognate_or_loanword",
        "'son/daughter-in-law' -- PAM 'Manuyang' and FIL 'manugang' are the same word.",
    ),
    (
        "Iso_Kinship.txt",
        8,
        "Iso_Kinship.txt",
        11,
        "high",
        "shared_cognate_or_loanword",
        "'sweetheart' -- PAM 'Capalsintan' and FIL 'kasintahan' share the 'sinta' (love) root.",
    ),
]


def load_inventory() -> dict[tuple[str, str, int], str]:
    index: dict[tuple[str, str, int], str] = {}
    with INVENTORY_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["lang_code"], row["source_name_normalized"], int(row["prompt_ordinal"]))
            index[key] = row["canonical_text"]
    return index


def main() -> None:
    index = load_inventory()
    out_rows = []
    for i, (pam_domain, pam_ord, fil_domain, fil_ord, confidence, basis, note) in enumerate(PAIRS, start=1):
        pam_key = ("PAM", pam_domain, pam_ord)
        fil_key = ("FIL", fil_domain, fil_ord)
        if pam_key not in index:
            raise KeyError(f"pair {i}: PAM key not found in inventory: {pam_key}")
        if fil_key not in index:
            raise KeyError(f"pair {i}: FIL key not found in inventory: {fil_key}")
        pam_text = index[pam_key]
        fil_text = index[fil_key]
        if not pam_text.strip() or not fil_text.strip():
            raise ValueError(f"pair {i}: empty canonical text for {pam_key} or {fil_key}")
        out_rows.append(
            {
                "pair_id": f"pldpair_{i:03d}",
                "confidence": confidence,
                "match_basis": basis,
                "pam_source_domain": pam_domain,
                "pam_prompt_ordinal": pam_ord,
                "pam_text": pam_text,
                "fil_source_domain": fil_domain,
                "fil_prompt_ordinal": fil_ord,
                "fil_text": fil_text,
                "note": note,
            }
        )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "pair_id",
        "confidence",
        "match_basis",
        "pam_source_domain",
        "pam_prompt_ordinal",
        "pam_text",
        "fil_source_domain",
        "fil_prompt_ordinal",
        "fil_text",
        "note",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    high = sum(1 for r in out_rows if r["confidence"] == "high")
    medium = sum(1 for r in out_rows if r["confidence"] == "medium")
    by_basis: dict[str, int] = {}
    for r in out_rows:
        by_basis[r["match_basis"]] = by_basis.get(r["match_basis"], 0) + 1
    stats = {
        "total_pairs": len(out_rows),
        "confidence_high": high,
        "confidence_medium": medium,
        "by_match_basis": by_basis,
        "distinct_domains_pam": sorted({r["pam_source_domain"] for r in out_rows}),
        "distinct_domains_fil": sorted({r["fil_source_domain"] for r in out_rows}),
    }
    with OUTPUT_STATS.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")

    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
