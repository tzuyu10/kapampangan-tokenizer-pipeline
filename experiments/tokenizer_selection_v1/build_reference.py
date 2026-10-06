"""Phase 3 Part 1, step 1: build the held-out morphology reference set.

Reads ONLY from `experiments/morphology_gold_v1/` (the Phase 1 triaged
650-row candidate set + its full 97-row user adjudication). Writes:

  data/reference-morphology.csv          -- one row per reference word
  reports/tierF-mapping-decisions.csv    -- audit of every Tier F row's fate
  reports/reference-build-manifest.json  -- counts + SHA-256 of the CSV

NOTHING here is independent native-speaker gold. It is:
  * Tier A/B (strong/moderate SILVER, corroborated by this project's own
    lexicon + page-cited reconciliation, not native-speaker verified), plus
  * the 97 Tier F rows re-annotated with the USER's adjudicated analysis
    (2026-08-25) -- the only human-verified subset in the whole 650.

Boundary convention (kept identical to the Tier A/B `tokenizer_target`
column so the two halves are comparable):
  * boundaries are the character offsets between surface morpheme pieces;
  * REDUPLICATION is fused -- the reduplicant is not split from its host
    (`lalaki` -> zero internal boundaries, `sasabian` -> only the `-an`
    boundary). Applied to Tier F reduplication rows too.
  * the `-ng` ligature is NOT a boundary (out of scope for this project,
    per AGENT_CONTEXT.md).
  * where a suffix surfaces as a bare `-n` after a vowel-final root
    (v4's documented allomorphy), the boundary sits before that `-n`.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
GOLD_DIR = REPO_ROOT / "experiments/morphology_gold_v1"
GOLD_CSV = GOLD_DIR / "resources/kapampangan_morph_annotated_dataset.csv"
TRIAGE_CSV = GOLD_DIR / "reports/morphology-triage.csv"
ADJ_CSV = GOLD_DIR / "reports/user-adjudication-2026-08-25.csv"

DATA_DIR = EXPERIMENT_ROOT / "data"
REPORTS_DIR = EXPERIMENT_ROOT / "reports"
REFERENCE_CSV = DATA_DIR / "reference-morphology.csv"
DECISIONS_CSV = REPORTS_DIR / "tierF-mapping-decisions.csv"
MANIFEST_JSON = REPORTS_DIR / "reference-build-manifest.json"

FUNCTION_PROCESSES = {"function_word", "clitic_or_function"}
BASE_TIERS = {"A_strong_silver", "B_moderate_silver"}


def boundaries_from_pieces(surface: str, pieces: list[str]) -> tuple[int, ...] | None:
    """Character offsets between `pieces`, iff they concatenate to `surface`."""
    if "".join(pieces).lower() != surface.lower():
        return None
    out: list[int] = []
    acc = 0
    for piece in pieces[:-1]:
        acc += len(piece)
        out.append(acc)
    return tuple(out)


def base_pool_boundaries(normalized: str, tokenizer_target: str) -> tuple[int, ...] | None:
    pieces = [p.strip().replace("~", "") for p in tokenizer_target.split("|")]
    return boundaries_from_pieces(normalized, pieces)


# --- Tier F: explicit per-row handling for rows whose user analysis does not
#     surface-reconstruct verbatim (nasal assimilation, medial d->r, vowel
#     hiatus, the -ng ligature, reduplication fusion, or genuine ambiguity).
#     Every entry is justified against the user's own note in ADJ_CSV.
#     value = tuple of boundaries  ->  include with that surface segmentation
#     value = "EXCLUDE:<reason>"   ->  left out of the reference entirely
TIER_F_OVERRIDES: dict[str, tuple[int, ...] | str] = {
    # reduplication fused, matching the Tier A/B convention (drop reduplicant boundary)
    "tutula": (),  # tu~ + tula        -> reduplicant fused, no affix
    "gagalgal": (),  # ga~ + galgal      -> reduplicant fused, no affix
    "kakanan": (5,),  # ka~ + kan + an    -> keep only the -an boundary
    # -ng ligature is not a segmentation boundary here
    "matuang": (2,),  # ma + tua(+ng)     -> ma|tuang, drop the -ng
    # medial d->r reversed only in the underlying analysis; gold is the SURFACE
    "katuliran": (2, 7),  # ka + tulir + an   (root tulid, surfaces tulir)
    "kapalaran": (2, 7),  # ka + palar + an   (root palad, surfaces palar)
    "parusa": (2,),  # pa + rusa         (root dusa, surfaces rusa)
    # nasal assimilation: the assimilated nasal stays attached to the root surface
    "panamdaman": (2, 8),  # pa + namdam + an  (root damdam)
    # ca- == ka- traditional spelling
    "camatayan": (2, 7),  # ca + matay + an
    # pa- is really present in the surface even though the root is salamat
    "kapasalamatan": (2, 4, 11),  # ka + pa + salamat + an
    # vowel-hiatus: suffix -an surfaces as bare -n after a vowel-final root
    "panayan": (6,),  # panaya + (a)n
    "pibatan": (2, 6),  # pi + bata + (a)n
    # genuine ambiguity or acknowledged "both wrong / too many layers" -> excluded
    "pamanalastas": "EXCLUDE:both_wrong; assimilated t, surface split not determinable",
    "kakaluguran": "EXCLUDE:nested ka~ over ka-...-an + d->r; surface split ambiguous",
    "kakalinguan": "EXCLUDE:ka~ reduplication over an already circumfixed stem; layered",
    "pakiramdaman": "EXCLUDE:damdam/ramdam alternation unresolved by the user",
    "dinan": "EXCLUDE:din/da root alternation unresolved",
    "maging": "EXCLUDE:m-/ma- and aging/ging both left open by the user",
    "panenayan": "EXCLUDE:'panaya-based derivation', no definite split given",
    "patayan": "EXCLUDE:patai/pate alternation + i->y glide, surface split unclear",
    "pakalulu": "EXCLUDE:paka-/pa- affix ambiguous per the user",
    "mumuna": "EXCLUDE:m-/um- alternation unresolved",
    "panamdam": "EXCLUDE:paN- + damdam/ramdam; assimilated surface, alternation open",
    "pengan": "EXCLUDE:pe- + pangan/mangan; nasal-assimilated, does not reconstruct",
    "paralaya": "EXCLUDE:alaya/dalaya root alternation unresolved",
    "migising": "EXCLUDE:mi-/mig- prefix alternation unresolved",
    "makalangan": "EXCLUDE:alang/kalangan root alternation unresolved",
}

MONO_MARKERS = ("monomorphemic", "proper name", "spanish loan", "tagalog loan")


def tier_f_auto(surface: str, analysis: str) -> tuple[int, ...] | None:
    """Boundaries from the user's analysis; `()` for monomorphemic; `None` if
    it does not reconstruct and needs a TIER_F_OVERRIDES entry."""
    low = analysis.lower()
    if any(m in low for m in MONO_MARKERS):
        return ()  # monomorphemic -> zero-boundary "do not over-split" row
    stripped = re.sub(r"\(.*?\)", "", analysis).strip()
    if "/" in stripped or "based" in stripped.lower():
        return None
    pieces = [p.replace("~", "").replace("-", "").strip() for p in stripped.split("+")]
    pieces = [p for p in pieces if p]
    return boundaries_from_pieces(surface, pieces)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def seg_from_boundaries(surface: str, bnds: tuple[int, ...]) -> str:
    prev = 0
    parts: list[str] = []
    for b in bnds:
        parts.append(surface[prev:b])
        prev = b
    parts.append(surface[prev:])
    return " | ".join(parts)


def main() -> int:
    gold = load_csv(GOLD_CSV)
    triage = {r["id"]: r for r in load_csv(TRIAGE_CSV)}
    adjudication = {r["surface"]: r for r in load_csv(ADJ_CSV)}

    reference: list[dict[str, object]] = []
    decisions: list[dict[str, object]] = []

    # ---- base pool: Tier A/B, non-function, reconstructs ----
    base_ok = base_skip_recon = base_skip_func = 0
    for row in gold:
        tier = triage.get(row["id"], {}).get("tier", "?")
        if tier not in BASE_TIERS:
            continue
        if row["process"] in FUNCTION_PROCESSES:
            base_skip_func += 1
            continue
        bnds = base_pool_boundaries(row["normalized"], row["tokenizer_target"])
        if bnds is None:
            base_skip_recon += 1
            continue
        base_ok += 1
        reference.append(
            {
                "id": row["id"],
                "surface": row["normalized"],
                "boundaries": " ".join(map(str, bnds)),
                "segmentation": seg_from_boundaries(row["normalized"], bnds),
                "n_boundaries": len(bnds),
                "process": row["process"],
                "source_tier": tier,
                "provenance": "tierAB_silver",
                "freq_in_sources": int(row["frequency_in_sources"] or 0),
            }
        )

    # ---- Tier F: re-annotated with the user's 2026-08-25 adjudication ----
    f_auto = f_mono = f_override = f_excluded = 0
    for row in gold:
        tier = triage.get(row["id"], {}).get("tier", "?")
        if tier != "F_conflicts_with_reconciliation_evidence":
            continue
        surface = row["normalized"]
        adj = adjudication.get(surface)
        if adj is None:
            decisions.append(
                {
                    "surface": surface,
                    "user_verdict": "(no adjudication row found)",
                    "user_correct_analysis": "",
                    "method": "EXCLUDE",
                    "boundaries": "",
                    "segmentation": "",
                    "note": "surface not present in user-adjudication CSV",
                }
            )
            f_excluded += 1
            continue

        analysis = adj["user_correct_analysis"]
        verdict = adj["user_verdict"]
        override = TIER_F_OVERRIDES.get(surface)
        method: str
        f_bnds: tuple[int, ...] | None

        if isinstance(override, str) and override.startswith("EXCLUDE:"):
            method, f_bnds = "EXCLUDE", None
            note = override[len("EXCLUDE:") :]
        elif isinstance(override, tuple):
            method, f_bnds = "manual_surface_map", override
            note = "surface-mapped from the user's underlying analysis"
        else:
            auto = tier_f_auto(surface, analysis)
            if auto is None:
                method, f_bnds = "EXCLUDE", None
                note = "user analysis has an unresolved alternation; not in override table"
            elif auto == ():
                if "monomorphemic" in analysis.lower() or "proper name" in analysis.lower():
                    method, f_bnds = "user_monomorphemic", ()
                    note = "user: monomorphemic / loan / proper name -> zero-boundary row"
                else:
                    method, f_bnds = "auto_parse", ()
                    note = "user analysis parsed to a single piece"
            else:
                method, f_bnds = "auto_parse", auto
                note = "user analysis parsed and surface-reconstructs verbatim"

        decisions.append(
            {
                "surface": surface,
                "user_verdict": verdict,
                "user_correct_analysis": analysis,
                "method": method,
                "boundaries": "" if f_bnds is None else " ".join(map(str, f_bnds)),
                "segmentation": ("" if f_bnds is None else seg_from_boundaries(surface, f_bnds)),
                "note": note,
            }
        )

        if method == "EXCLUDE":
            f_excluded += 1
            continue
        if method == "auto_parse":
            f_auto += 1
        elif method == "user_monomorphemic":
            f_mono += 1
        else:
            f_override += 1

        assert f_bnds is not None
        reference.append(
            {
                "id": row["id"],
                "surface": surface,
                "boundaries": " ".join(map(str, f_bnds)),
                "segmentation": seg_from_boundaries(surface, f_bnds),
                "n_boundaries": len(f_bnds),
                "process": row["process"],
                "source_tier": tier,
                "provenance": f"tierF_user_{method}",
                "freq_in_sources": int(row["frequency_in_sources"] or 0),
            }
        )

    reference.sort(key=lambda r: str(r["id"]))
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    fields = [
        "id",
        "surface",
        "boundaries",
        "segmentation",
        "n_boundaries",
        "process",
        "source_tier",
        "provenance",
        "freq_in_sources",
    ]
    with REFERENCE_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(reference)

    decisions.sort(key=lambda r: (r["method"] == "EXCLUDE", str(r["surface"])))
    with DECISIONS_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "surface",
                "user_verdict",
                "user_correct_analysis",
                "method",
                "boundaries",
                "segmentation",
                "note",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(decisions)

    sha = hashlib.sha256(REFERENCE_CSV.read_bytes()).hexdigest()
    total_boundaries = sum(cast(int, r["n_boundaries"]) for r in reference)
    zero_boundary = sum(1 for r in reference if cast(int, r["n_boundaries"]) == 0)
    manifest = {
        "reference_csv": REFERENCE_CSV.name,
        "reference_csv_sha256": sha,
        "source": "experiments/morphology_gold_v1/ (Tier A/B silver + Tier F user adjudication)",
        "label": "silver + partial user adjudication; NOT independent native-speaker gold",
        "rows_total": len(reference),
        "rows_tierAB_silver": base_ok,
        "rows_tierF_user_auto": f_auto,
        "rows_tierF_user_monomorphemic": f_mono,
        "rows_tierF_user_manual_surface_map": f_override,
        "tierF_excluded": f_excluded,
        "base_pool_skipped_function_word": base_skip_func,
        "base_pool_skipped_reconstruction_fail": base_skip_recon,
        "total_gold_boundaries": total_boundaries,
        "zero_boundary_rows": zero_boundary,
    }
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(manifest, indent=2))
    print(f"\nwrote {REFERENCE_CSV}")
    print(f"wrote {DECISIONS_CSV}")
    print(f"wrote {MANIFEST_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
