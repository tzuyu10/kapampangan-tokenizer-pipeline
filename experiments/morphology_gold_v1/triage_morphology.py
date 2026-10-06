"""Phase 1 AI-assisted triage of the 650-row morphology candidate set.

Reads the byte-identical copy under resources/ (never the external original)
and scores every row against mechanical, stated criteria -- not a single
opaque LLM judgment. Output remains silver/ai_triaged, never gold; see
reports/morphology-triage-summary.md for the full methodology writeup and
this experiment's README.md for scope.

Criteria (see summary report for full rationale):
  1. reconstruction_ok - do the segmented pieces losslessly reconstruct the
     normalized surface (the same lossless-reconstruction invariant this
     project already holds every accepted morphology analysis to).
  2. root_attestation - is the claimed root independently attested in the
     v2 vetted lexicon, or in
     experiments/internet_root_reconciliation_v1/reports/word-evidence.csv
     (this project's own prior page-cited reconciliation of the full
     143,529-word-type inventory against Forman/Bergano/Samson/ACD/Kaikki)?
  3. affix_recognized - is the claimed affix marker inside this project's
     own already-modeled affix inventory (Table 1 constants.py + v4's
     documented additions)?
  4. reconciliation_conflict - does this project's OWN existing v2/v4
     analysis of the row's exact surface (from the same reconciliation
     report) either (a) already accept a *different* root than this row
     claims, or (b) explicitly recommend against decomposing this surface
     at all (`decision: lexically_attested_unresolved`, i.e. the whole word
     is independently attested as its own dictionary headword with no
     source evidence supporting further decomposition)? This is the
     strongest signal available and overrides tiers 1-3: a row can
     reconstruct losslessly and reuse recognized affix-marker strings while
     still decomposing a word that is, in fact, monomorphemic (see
     `mamangan`/`tatang`/`pasbul`/`parang` in the summary report -- caught
     only by cross-referencing this reconciliation evidence, not by string
     matching alone).
Tier is a deterministic function of these signals plus the dataset's own
pre-existing confidence field; it never overrides a mechanical failure, and
reconciliation_conflict overrides everything else.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

EXPERIMENT_ROOT = Path(__file__).resolve().parent
RESOURCES = EXPERIMENT_ROOT / "resources"
REPORTS = EXPERIMENT_ROOT / "reports"
REPO_ROOT = EXPERIMENT_ROOT.parent.parent

MORPH_CSV = RESOURCES / "kapampangan_morph_annotated_dataset.csv"
LOCAL_LEXICON_CSV = RESOURCES / "kapampangan_lexicon_local_curated.csv"
POLY_LEXICON_CSV = RESOURCES / "kapampangan_lexicon_polytranslator_curated.csv"
V2_LEXICON_JSON = (
    REPO_ROOT / "experiments" / "source_adjudicated_v2" / "resources" / "training-lexicon.json"
)
RECONCILIATION_CSV = (
    REPO_ROOT
    / "experiments"
    / "internet_root_reconciliation_v1"
    / "reports"
    / "word-evidence.csv"
)

# whole_form_sources prefixes this project already tiers by authority
# (source-registry.json): Forman/Bergaño/Samson/ACD are page-cited
# dictionaries/comparative databases; kaikki_enwiktionary is a
# community-maintained Wiktionary export and, on its own, a weaker signal.
STRONG_RECONCILIATION_SOURCE_PREFIXES = (
    "forman1971:",
    "bergano1732_samson_translation:",
    "samson2011:",
    "acd_v1_2:",
)

# Table 1 baseline (src/kapampangan_morphbpe/constants.py) + v4's documented
# additions (experiments/expanded_morphology_v4/README.md "What changed vs.
# Table 1"), reduced to bare morpheme strings for a soft substring match.
# This is a recognition heuristic, not an authoritative grammar check: it
# only tells us whether the *marker string* is one this project's rule set
# already names, not whether the specific word's analysis is correct.
KNOWN_AFFIX_MARKERS = frozenset(
    {
        # Table 1
        "ma", "me", "pa", "maka", "ka", "mag", "meg", "mang", "meng", "i",
        "ipa", "makapag", "mig", "meka", "mekapag", "in", "um", "an",
        "pam", "pan", "panga", "na", "pa", "mu", "ku", "ya", "la", "ra",
        "ne", "no",
        # v4 additions (README "What changed vs. Table 1")
        "m", "man", "mam", "men", "mem", "many", "meny", "maki", "meki",
        "makipag", "mekipag", "paki", "peka", "mi", "pi", "pag", "magpa",
        "migpa", "megpa", "magka", "migka", "megka", "magpaka", "migpaka",
        "megpaka", "pang", "en", "anan",
    }
)

# Closed-class particles this dataset tags function_word/clitic_or_function;
# Table 1's own CLITICS tuple plus a small set of common Kapampangan
# prepositions/conjunctions/particles seen in the candidate set. This list is
# intentionally not exhaustive -- rows outside it still pass (see scoring),
# just without the extra corroboration signal.
KNOWN_FUNCTION_WORDS = frozenset(
    {
        "na", "pa", "mu", "ku", "ya", "la", "ra", "ne", "no", "king", "at",
        "ing", "ning", "keng", "kang", "kening", "deng", "ding", "reng",
        "ban", "pin", "ta", "kami", "ika", "ikami", "ikayu", "ikaming",
        "ala", "wa", "oo", "e", "at", "o", "kapag", "kanita",
    }
)


def _norm(text: str) -> str:
    return (text or "").strip().casefold()


def _load_v2_lexicon_keys() -> set[str]:
    data = json.loads(V2_LEXICON_JSON.read_text(encoding="utf-8"))
    keys: set[str] = set()
    for root in data.get("roots", []):
        key = root.get("comparison_key")
        if key:
            keys.add(_norm(key))
    for compound in data.get("compounds", []):
        key = compound.get("comparison_key")
        if key:
            keys.add(_norm(key))
    return keys


def _load_secondary_lexicon_keys() -> set[str]:
    keys: set[str] = set()
    with LOCAL_LEXICON_CSV.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            word = row.get("kapampangan_word_normalized") or row.get("kapampangan_word")
            if word:
                keys.add(_norm(word))
    with POLY_LEXICON_CSV.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            word = row.get("kapampangan_word")
            if word:
                keys.add(_norm(word))
    return keys


def _load_reconciliation() -> dict[str, dict[str, str]]:
    by_key: dict[str, dict[str, str]] = {}
    with RECONCILIATION_CSV.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = _norm(row.get("comparison_key", ""))
            if key and key not in by_key:
                by_key[key] = row
    return by_key


def _has_strong_source(whole_form_sources: str) -> bool:
    return any(
        entry.strip().startswith(STRONG_RECONCILIATION_SOURCE_PREFIXES)
        for entry in whole_form_sources.split("|")
    )


def _reconciliation_root_tier(root: str, reconciliation: dict[str, dict[str, str]]) -> str:
    entry = reconciliation.get(_norm(root))
    if entry is None:
        return "none"
    return "strong" if _has_strong_source(entry.get("whole_form_sources", "")) else "weak"


def _reconciliation_conflict(
    normalized: str,
    claimed_root: str,
    process: str,
    reconciliation: dict[str, dict[str, str]],
) -> tuple[bool, str]:
    """Cross-check the row's own claimed decomposition against this
    project's existing v2/v4 analysis of the exact same surface, and
    against the reconciliation experiment's own do-not-decompose calls.
    Returns (conflict, reason). See module docstring point 4.
    """
    if process in {"function_word", "clitic_or_function"}:
        return False, ""
    entry = reconciliation.get(_norm(normalized))
    if entry is None:
        return False, ""
    if entry.get("current_status") == "accepted":
        existing_root = _norm(entry.get("current_root", ""))
        if existing_root and existing_root != _norm(claimed_root):
            return (
                True,
                f"existing v2/v4 analysis already accepts root '{entry.get('current_root')}' "
                f"(segments '{entry.get('current_segments')}') for this exact surface, not "
                f"'{claimed_root}'",
            )
    if entry.get("decision") == "lexically_attested_unresolved":
        return (
            True,
            "reconciliation found this exact surface independently attested as its own "
            "dictionary headword with no source evidence supporting further decomposition "
            f"({entry.get('proposed_action')})",
        )
    return False, ""


def _reconstruction_ok(morph_segments: str, normalized: str) -> bool:
    if not morph_segments:
        return not normalized
    joined = re.sub(r"[+~]", "", morph_segments)
    return _norm(joined) == _norm(normalized)


def _affix_markers(affixes: str) -> list[str]:
    if not affixes:
        return []
    parts = re.split(r"[;]|\s\+\s", affixes)
    markers = []
    for part in parts:
        bare = re.sub(r"[-~]", "", part).strip()
        if bare:
            markers.append(bare.casefold())
    return markers


def _reduplication_marker_ok(marker: str, root: str) -> bool:
    """A reduplication marker isn't a fixed morpheme string -- it's a copy of
    the root's own initial CV/V/full form. Recognized iff it structurally is
    one (a prefix of the normalized root, or the whole root for ka-+full-root
    reduplication), matching v4's documented CV-/V-/full-root reduplication
    rules rather than a fixed-list lookup.
    """
    root_norm = _norm(root)
    marker_norm = marker.casefold()
    if not marker_norm or not root_norm:
        return False
    return root_norm == marker_norm or root_norm.startswith(marker_norm)


def _affix_recognized(affixes: str, process: str, root: str) -> bool | None:
    markers = _affix_markers(affixes)
    if not markers:
        return None
    if "reduplication" in process:
        return all(
            _reduplication_marker_ok(marker, root) or marker in KNOWN_AFFIX_MARKERS
            for marker in markers
        )
    return all(marker in KNOWN_AFFIX_MARKERS for marker in markers)


def score_row(
    row: dict[str, str],
    v2_keys: set[str],
    secondary_keys: set[str],
    reconciliation: dict[str, dict[str, str]],
) -> dict[str, object]:
    process = row["process"]
    is_function_row = process in {"function_word", "clitic_or_function"}
    reconstruction_ok = _reconstruction_ok(row["morph_segments"], row["normalized"])

    root_key = _norm(row["root"])
    root_in_v2 = bool(root_key) and root_key in v2_keys
    root_in_secondary = bool(root_key) and root_key in secondary_keys
    reconciliation_root_tier = _reconciliation_root_tier(row["root"], reconciliation)
    affix_recognized = _affix_recognized(row["affixes"], process, row["root"])
    in_function_word_list = _norm(row["surface"]) in KNOWN_FUNCTION_WORDS
    conflict, conflict_reason = _reconciliation_conflict(
        row["normalized"], row["root"], process, reconciliation
    )

    original_confidence = row["confidence"]
    root_strongly_attested = root_in_v2 or reconciliation_root_tier == "strong"

    if conflict:
        tier = "F_conflicts_with_reconciliation_evidence"
    elif is_function_row:
        if not reconstruction_ok:
            tier = "D_reject_structural_failure"
        elif in_function_word_list and original_confidence == "high":
            tier = "A_strong_silver"
        elif original_confidence == "high":
            tier = "B_moderate_silver"
        else:
            tier = "C_weak_needs_review"
    else:
        if not reconstruction_ok:
            tier = "D_reject_structural_failure"
        elif root_strongly_attested and affix_recognized is not False:
            tier = "A_strong_silver"
        elif (
            root_in_secondary or reconciliation_root_tier == "weak" or affix_recognized
        ) and affix_recognized is not False:
            tier = "B_moderate_silver"
        else:
            tier = "C_weak_needs_review"

    return {
        "id": row["id"],
        "surface": row["surface"],
        "normalized": row["normalized"],
        "root": row["root"],
        "morph_segments": row["morph_segments"],
        "affixes": row["affixes"],
        "process": process,
        "original_confidence": original_confidence,
        "reconstruction_ok": reconstruction_ok,
        "root_in_v2_lexicon": root_in_v2,
        "root_in_secondary_lexicon": root_in_secondary,
        "reconciliation_root_tier": reconciliation_root_tier,
        "affix_recognized": affix_recognized,
        "in_known_function_word_list": in_function_word_list,
        "reconciliation_conflict": conflict,
        "reconciliation_conflict_reason": conflict_reason,
        "tier": tier,
    }


def main() -> None:
    v2_keys = _load_v2_lexicon_keys()
    secondary_keys = _load_secondary_lexicon_keys()
    reconciliation = _load_reconciliation()

    with MORPH_CSV.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    scored = [score_row(row, v2_keys, secondary_keys, reconciliation) for row in rows]

    REPORTS.mkdir(parents=True, exist_ok=True)
    out_csv = REPORTS / "morphology-triage.csv"
    fieldnames = list(scored[0].keys())
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored)

    from collections import Counter

    tier_counts = Counter(r["tier"] for r in scored)
    process_by_tier: dict[str, Counter] = {}
    for r in scored:
        process_by_tier.setdefault(r["tier"], Counter())[r["process"]] += 1

    summary = {
        "total_rows": len(scored),
        "tier_counts": dict(sorted(tier_counts.items())),
        "process_by_tier": {
            tier: dict(sorted(counter.items())) for tier, counter in sorted(process_by_tier.items())
        },
        "reconstruction_failures": sum(1 for r in scored if not r["reconstruction_ok"]),
        "root_attested_v2": sum(1 for r in scored if r["root_in_v2_lexicon"]),
        "root_attested_secondary_only": sum(
            1 for r in scored if r["root_in_secondary_lexicon"] and not r["root_in_v2_lexicon"]
        ),
        "root_unattested": sum(
            1
            for r in scored
            if not r["root_in_v2_lexicon"]
            and not r["root_in_secondary_lexicon"]
            and r["process"] not in {"function_word", "clitic_or_function"}
        ),
        "affix_not_recognized": sum(1 for r in scored if r["affix_recognized"] is False),
        "reconciliation_conflicts": sum(1 for r in scored if r["reconciliation_conflict"]),
        "root_attested_reconciliation_strong": sum(
            1 for r in scored if r["reconciliation_root_tier"] == "strong"
        ),
        "root_attested_reconciliation_weak_only": sum(
            1 for r in scored if r["reconciliation_root_tier"] == "weak"
        ),
    }
    (REPORTS / "morphology-triage-stats.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
