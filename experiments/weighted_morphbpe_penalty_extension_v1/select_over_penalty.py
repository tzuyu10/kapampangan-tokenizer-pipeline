"""Apply configs/candidate-grid.json's frozen lexicographic selection
hierarchy across this experiment's (crossing_penalty, vocab) grid, the same
way select_candidate() already chooses over vocab size alone. Extends the
handoff's suggested next step: "extend select_candidate()'s hierarchy to
choose over crossing_penalty the same way it already chooses over vocab
size."

Reads this experiment's already-computed official-validation-scores.json
(no training, no re-evaluation) and configs/selected-candidate.json for the
shipped baseline. Both were trained on the same canonical
resources/training-lexicon.json, so this is an apples-to-apples comparison.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from kapampangan_morphbpe.serialization import read_json, write_json  # noqa: E402


def _selection_key(row: dict[str, Any]) -> tuple[float, float, float, float, int]:
    return (
        float(row["morphological_distance"]),
        -float(row["boundary_f1"]),
        -float(row["consistency_f1"]),
        float(row["fertility_rate"]),
        int(row["target_vocabulary_size"]),
    )


def main() -> int:
    scores = read_json(EXPERIMENT_ROOT / "reports/official-validation-scores.json")
    if not isinstance(scores, dict):
        raise ValueError("official-validation-scores.json malformed")
    rows = cast(list[dict[str, Any]], scores["rows"])

    eligible = [
        row for row in rows if row["training_protected_boundary_merge_violations"] == 0
    ]
    rejected = [row for row in rows if row not in eligible]
    if not eligible:
        raise ValueError("no candidate satisfies the protected-boundary training constraint")

    selected = min(eligible, key=_selection_key)

    selected_candidate = read_json(REPOSITORY_ROOT / "configs/selected-candidate.json")
    if not isinstance(selected_candidate, dict):
        raise ValueError("selected-candidate.json malformed")
    shipped_metrics = cast(dict[str, Any], selected_candidate["selected_metrics"])
    shipped_boundary = cast(dict[str, Any], shipped_metrics["morpheme_boundary"])
    shipped_consistency = cast(dict[str, Any], shipped_metrics["morphological_consistency"])

    print("Selected among this experiment's (penalty, vocab) grid:")
    print(f"  crossing_penalty={selected['crossing_penalty']}")
    print(f"  target_vocabulary_size={selected['target_vocabulary_size']}")
    print(f"  boundary_f1={selected['boundary_f1']:.4f}")
    print(f"  consistency_f1={selected['consistency_f1']:.4f}")
    print(f"  morphological_distance={selected['morphological_distance']:.4f}")
    print(f"  fertility_rate={selected['fertility_rate']:.4f}")
    print()
    print("Shipped ConstrainedBPETrainer (configs/selected-candidate.json):")
    print(f"  target_vocabulary_size={selected_candidate['selected_target_vocabulary_size']}")
    print(f"  boundary_f1={shipped_boundary['f1']:.4f}")
    print(f"  consistency_f1={shipped_consistency['f1']:.4f}")
    print(f"  morphological_distance={shipped_metrics['morphological_distance']:.4f}")
    print(f"  fertility_rate={shipped_metrics['fertility_rate']:.4f}")

    output = {
        "selection_hierarchy_source": "configs/candidate-grid.json",
        "grid_evaluated": "experiments/weighted_morphbpe_penalty_extension_v1 "
        "(canonical-lexicon-trained, penalties 1..64)",
        "eligible_candidate_count": len(eligible),
        "rejected_candidates": rejected,
        "selected": selected,
        "shipped_baseline": {
            "condition": "shipped_constrained_bpe",
            "target_vocabulary_size": selected_candidate["selected_target_vocabulary_size"],
            "boundary_f1": shipped_boundary["f1"],
            "consistency_f1": shipped_consistency["f1"],
            "morphological_distance": shipped_metrics["morphological_distance"],
            "fertility_rate": shipped_metrics["fertility_rate"],
        },
        "caveat": "morphological_distance was still decreasing at the top of the tested "
        "penalty range (64), so this selection is 'best of what was tried,' not a "
        "validated global optimum. See README.md.",
    }
    write_json(EXPERIMENT_ROOT / "reports/selection-attempt.json", output)
    print(f"\nWrote {(EXPERIMENT_ROOT / 'reports/selection-attempt.json').relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
