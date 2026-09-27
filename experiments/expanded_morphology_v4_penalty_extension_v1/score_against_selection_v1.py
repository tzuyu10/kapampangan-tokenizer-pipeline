"""Score the new penalty-16/32/64/128/256 candidates against the frozen,
partially-human-verified DEV/TEST morphology reference in
experiments/tokenizer_selection_v1/ -- the same reference and the exact
same scoring functions (imported directly, not reimplemented) that
established penalty-8 @ vocab 6,080 as the real Phase 3 winner
(DEV F1 0.4639 / TEST F1 0.4093).

Extends that grid with the new penalties, applying the identical selection
rule (max DEV boundary F1, tie-break exact_match, then lower fertility) to
see whether a higher penalty than 8 is actually the better choice under the
most rigorous evaluation this project has.

Writes only inside this experiment folder; does not touch
tokenizer_selection_v1/ or any existing artifact.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_ROOT.parents[1]
SELECTION_V1 = REPO_ROOT / "experiments/tokenizer_selection_v1"
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(SELECTION_V1))

from run_selection import _encode_runtime, _score, load_split  # noqa: E402
from kapampangan_morphbpe.serialization import fingerprint, write_json  # noqa: E402

DEV_CSV = SELECTION_V1 / "data/dev.csv"
TEST_CSV = SELECTION_V1 / "data/test.csv"
EXISTING_ART = REPO_ROOT / "experiments/expanded_morphology_v4/artifacts"
NEW_ART = EXPERIMENT_ROOT / "artifacts"

VOCAB_SIZES = (6080, 8192, 16384)
EXISTING_PENALTIES = (1, 2, 4, 8)
NEW_PENALTIES = (16, 32, 64, 128, 256)


def _artifact_path(penalty: int, vocab: int) -> Path:
    base = EXISTING_ART if penalty in EXISTING_PENALTIES else NEW_ART
    return base / f"penalty-{penalty}" / "candidates" / f"vocab-{vocab}"


def _key(m: dict[str, float]) -> tuple[float, float, float]:
    return (m["boundary_f1"], m["exact_match"], -m["fertility"])


def main() -> int:
    dev_rows = load_split(DEV_CSV)
    test_rows = load_split(TEST_CSV)

    dev_grid: dict[str, dict[str, dict[str, float]]] = {}
    test_grid: dict[str, dict[str, dict[str, float]]] = {}
    for penalty in (*EXISTING_PENALTIES, *NEW_PENALTIES):
        key_name = f"penalty-{penalty}"
        dev_grid[key_name] = {}
        test_grid[key_name] = {}
        for vocab in VOCAB_SIZES:
            artifact = _artifact_path(penalty, vocab)
            dev_encoded = _encode_runtime(artifact, dev_rows)
            test_encoded = _encode_runtime(artifact, test_rows)
            dev_grid[key_name][str(vocab)] = _score(dev_rows, dev_encoded)
            test_grid[key_name][str(vocab)] = _score(test_rows, test_encoded)
            print(
                f"{key_name:<12} vocab={vocab:<6} "
                f"DEV F1={dev_grid[key_name][str(vocab)]['boundary_f1']:.4f} "
                f"TEST F1={test_grid[key_name][str(vocab)]['boundary_f1']:.4f}"
            )

    best: tuple[tuple[float, float, float], str, int] | None = None
    for condition, by_vocab in dev_grid.items():
        for vocab in VOCAB_SIZES:
            cand = (_key(by_vocab[str(vocab)]), condition, vocab)
            if best is None or cand[0] > best[0]:
                best = cand
    assert best is not None
    winner_condition, winner_vocab = best[1], best[2]

    body: dict[str, Any] = {
        "reference": "experiments/tokenizer_selection_v1/data/reference-morphology.csv",
        "label": "silver + partial user adjudication; NOT independent native-speaker gold "
        "(same reference tokenizer_selection_v1 itself uses)",
        "extends": "tokenizer_selection_v1/reports/selection-report.json with penalty-16/32/64/128/256",
        "dev_rows": len(dev_rows),
        "test_rows": len(test_rows),
        "metric": "type-weighted boundary F1; tie-break exact_match then lower fertility "
        "(identical scoring functions imported from run_selection.py)",
        "previously_established_winner": {"condition": "penalty-8", "vocab": 6080},
        "new_grid_winner": {"condition": winner_condition, "vocab": winner_vocab},
        "new_grid_winner_confirmation": {
            "dev": dev_grid[winner_condition][str(winner_vocab)],
            "test": test_grid[winner_condition][str(winner_vocab)],
        },
        "dev_grid": dev_grid,
        "test_grid": test_grid,
    }
    report = {**body, "report_fingerprint": fingerprint(body)}
    (EXPERIMENT_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    write_json(EXPERIMENT_ROOT / "reports/selection-v1-extended-scores.json", report)

    print(f"\nNew grid winner: {winner_condition} @ vocab {winner_vocab}")
    conf = body["new_grid_winner_confirmation"]
    print(
        f"  DEV  F1={conf['dev']['boundary_f1']:.4f} exact={conf['dev']['exact_match']:.4f} "
        f"fert={conf['dev']['fertility']:.3f}"
    )
    print(
        f"  TEST F1={conf['test']['boundary_f1']:.4f} exact={conf['test']['exact_match']:.4f} "
        f"fert={conf['test']['fertility']:.3f}"
    )
    print("\nPreviously established winner: penalty-8 @ vocab 6,080 (DEV F1 0.4639 / TEST F1 0.4093)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
