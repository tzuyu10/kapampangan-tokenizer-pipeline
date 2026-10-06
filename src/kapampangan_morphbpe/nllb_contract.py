from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION
from .serialization import fingerprint, read_json, sha256_file, write_json


def export_nllb_contract(artifact_dir: Path, nllb_dir: Path) -> dict[str, object]:
    adapter_path = Path(__file__).with_name("nllb_adapter.py")
    manifest_raw: Any = read_json(artifact_dir / "tokenizer-manifest.json")
    specials_raw: Any = read_json(artifact_dir / "special_tokens.json")
    if not isinstance(manifest_raw, dict) or not isinstance(specials_raw, dict):
        raise ValueError("tokenizer artifact manifests malformed")
    manifest = cast(dict[str, Any], manifest_raw)
    specials = cast(dict[str, Any], specials_raw)
    contract_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "future_phase_contract_not_executed",
        "artifact_fingerprint": manifest.get("artifact_fingerprint"),
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "source_vocabulary_size": manifest.get("actual_vocabulary_size"),
        "source_special_tokens": specials.get("special_tokens"),
        "source_encoding_outputs": [
            "token_strings",
            "token_ids",
            "attention_mask",
            "normalized_codepoint_offsets",
        ],
        "source_adapter": {
            "python_class": "kapampangan_morphbpe.nllb_adapter.SourceTokenizerAdapter",
            "method": "encode_batch",
            "framework": (
                "framework-neutral Python; tensor conversion belongs to future integration"
            ),
        },
        "padding": {
            "token_role": "pad",
            "side": "right",
            "attention_mask_for_padding": 0,
            "caller_must_supply_target_length": True,
        },
        "truncation": {
            "default": "disabled",
            "side": "right_when_explicitly_enabled",
            "caller_must_supply_max_length": True,
        },
        "language_token_requirements": {
            "status": "must_be_verified_against_future_nllb_library",
            "kapampangan_native_nllb_language_token_assumed": False,
            "filipino_target_language_token_must_remain_native": True,
        },
        "model_condition": {
            "model": "NLLB-200 Distilled 600M",
            "source_tokenizer": "this artifact",
            "target_tokenizer": "native NLLB-200 Filipino tokenizer",
            "source_embedding_size": "source_vocabulary_size",
            "source_embeddings": "newly_initialized_and_only_trainable_parameters",
            "remaining_pretrained_parameters": "frozen",
            "decoder_vocabulary_changed": False,
            "target_output_projection_changed": False,
        },
        "integration_property": (
            "The software stack must expose a genuinely independent source embedding "
            "without changing tied target embeddings or output projection."
        ),
        "integration_property_verification": {
            "status": "verified_on_real_weights",
            "date": "2026-08-31",
            "model": "facebook/nllb-200-distilled-600M (M2M100ForConditionalGeneration)",
            "notebook": "notebooks/phase4-nllb-architecture-verification.ipynb",
            "result_file": "nllb/phase4-architecture-verification.json",
            "independent_source_embedding_supported": True,
            "target_side_provably_unchanged": True,
            "only_new_source_embedding_receives_gradient": True,
            "caveat": (
                "model.tie_weights() re-points the encoder embedding back to the shared "
                "matrix (from_pretrained calls it at load; resize_token_embeddings and "
                "save_pretrained/from_pretrained round-trips can too). Apply the "
                "encoder-only swap after model load, do not call tie_weights() again, and "
                "re-apply the swap after any checkpoint reload. lm_head<->shared tying is "
                "unaffected by the re-tie."
            ),
        },
    }
    contract = {**contract_body, "contract_fingerprint": fingerprint(contract_body)}
    nllb_dir.mkdir(parents=True, exist_ok=True)
    write_json(nllb_dir / "source-tokenizer-contract.json", contract)
    export_body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "status": "adapter_contract_exported_model_not_downloaded_or_trained",
        "artifact_fingerprint": manifest.get("artifact_fingerprint"),
        "artifact_manifest_sha256": sha256_file(artifact_dir / "tokenizer-manifest.json"),
        "source_contract_sha256": sha256_file(nllb_dir / "source-tokenizer-contract.json"),
        "source_adapter_sha256": sha256_file(adapter_path),
        "nllb_model_downloaded": False,
        "nllb_model_trained": False,
        "held_out_evaluation_executed": False,
    }
    export_manifest = {**export_body, "export_fingerprint": fingerprint(export_body)}
    write_json(nllb_dir / "export_manifest.json", export_manifest)
    return export_manifest
