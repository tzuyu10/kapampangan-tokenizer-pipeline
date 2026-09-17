"""Truthful readiness metadata for the planned translator comparison.

The repository currently contains the source-tokenizer adapter contract, but
not the baseline NLLB weights or a trained custom-tokenizer checkpoint.  This
module exposes that state to the UI so the comparison screen never invents a
translation or implies that an untrained model is usable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXPORT_MANIFEST = REPOSITORY_ROOT / "nllb" / "export_manifest.json"


def _manifest() -> dict[str, Any]:
    try:
        value = json.loads(EXPORT_MANIFEST.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def status() -> dict[str, Any]:
    manifest = _manifest()
    baseline_ready = manifest.get("nllb_model_downloaded") is True
    custom_ready = manifest.get("nllb_model_trained") is True

    # Loading/generation is intentionally not claimed here.  When inference
    # is implemented, make this flag true only after both checkpoints pass a
    # startup generation smoke test.
    inference_api_ready = False

    return {
        "direction": {
            "source": "Kapampangan",
            "target": "Filipino",
            "target_language_code": "tgl_Latn",
        },
        "can_compare": baseline_ready and custom_ready and inference_api_ready,
        "inference_api_ready": inference_api_ready,
        "conditions": {
            "custom": {
                "label": "MorphBPE + NLLB-200",
                "role": "Proposed system",
                "tokenizer": "MorphBPE penalty-32 (6,080 source tokens)",
                "model": "NLLB-200 Distilled 600M with source embedding swap",
                "ready": custom_ready and inference_api_ready,
                "checkpoint_ready": custom_ready,
                "reason": (
                    "Ready for inference."
                    if custom_ready and inference_api_ready
                    else "The custom-tokenizer NLLB checkpoint has not been trained and exported."
                ),
            },
            "baseline": {
                "label": "Original NLLB-200",
                "role": "Baseline",
                "tokenizer": "Native NLLB-200 tokenizer",
                "model": "facebook/nllb-200-distilled-600M",
                "ready": baseline_ready and inference_api_ready,
                "checkpoint_ready": baseline_ready,
                "reason": (
                    "Ready for inference."
                    if baseline_ready and inference_api_ready
                    else "The original NLLB-200 weights are not included in this repository."
                ),
            },
        },
        "message": (
            "Both translation conditions are ready."
            if baseline_ready and custom_ready and inference_api_ready
            else "Translation comparison is waiting for the baseline weights, the trained "
            "custom-tokenizer checkpoint, and the inference adapter."
        ),
        "manifest_status": manifest.get("status", "manifest_unavailable"),
    }

