"""NLLB-200 Distilled 600M loading for the baseline and adapted conditions.

Implements thesis Ch.3 "NLLB-200 Distilled 600M Translation Pipeline":
the adapted condition detaches the encoder's input embedding table from the
model's tied shared embedding (which also backs the decoder input and the
output-projection `lm_head` in the HF M2M100/NLLB architecture) and replaces
it with a freshly initialized table sized to the proposed Kapampangan
tokenizer's vocabulary. Only that new table is trainable; the decoder
embedding and output projection are therefore provably unchanged, matching
the thesis's `decoder_vocabulary_changed: False` /
`target_output_projection_changed: False` requirements (see
`nllb/source-tokenizer-contract.json`).

See `docs/MT_PIPELINE_ARCHITECTURE.md` decisions M-01 and M-02 for the two
choices the thesis leaves unspecified that this module had to resolve:
the baseline condition's trainable-parameter scope, and the source-language
tag used for Kapampangan text (NLLB has no native Kapampangan code).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

NLLB_MODEL_ID = "facebook/nllb-200-distilled-600M"

# NLLB-200 has no Kapampangan ("pam") entry. Decision M-02: the baseline
# condition (which must use the native NLLB tokenizer end to end) tags
# Kapampangan source text with the Filipino/Tagalog code as the closest
# supported proxy, matching the transfer strategy used by Almendral (2025)
# and Macayan et al. (2026) cited in the thesis's own literature review.
# The adapted condition has no such tag available in its own vocabulary and
# does not use one; see docs/MT_PIPELINE_ARCHITECTURE.md decision M-02.
BASELINE_SOURCE_LANG_TAG = "tgl_Latn"
TARGET_LANG_TAG = "tgl_Latn"

ConditionName = Literal["baseline", "adapted"]


@dataclass(frozen=True, slots=True)
class LoadedMTModel:
    model: object
    target_tokenizer: object
    condition: ConditionName
    trainable_parameter_count: int
    total_parameter_count: int
    model_id: str

    def summary(self) -> dict[str, object]:
        return {
            "condition": self.condition,
            "model_id": self.model_id,
            "trainable_parameter_count": self.trainable_parameter_count,
            "total_parameter_count": self.total_parameter_count,
            "trainable_fraction": (
                self.trainable_parameter_count / self.total_parameter_count
                if self.total_parameter_count
                else 0.0
            ),
        }


def load_condition(
    condition: ConditionName,
    *,
    source_vocabulary_size: int | None = None,
    source_pad_id: int | None = None,
    model_id: str = NLLB_MODEL_ID,
    cache_dir: Path | None = None,
) -> LoadedMTModel:
    """Load one experimental MT condition.

    baseline: native NLLB tokenizer on both sides. Decision M-01: since the
      thesis specifies the adapted condition's trainable scope explicitly
      ("only the source embedding parameters will be updated") but is silent
      on the baseline's, and the baseline's encoder input embedding is the
      *same tensor* as its decoder input and output-projection embedding
      (tied by construction in this architecture), an embedding-only
      baseline would necessarily also retrain the decoder and output
      projection -- which the thesis explicitly forbids for the adapted
      condition. A truly parallel "embedding-only, nothing else moves"
      restriction is therefore architecturally impossible for the baseline.
      This implementation instead fully fine-tunes the baseline (all
      parameters trainable), the standard practice for adapting NLLB to a
      new low-resource pair with its existing tokenizer (matching the
      approach in Almendral, 2025, cited in the thesis). This asymmetry is
      a real, documented limitation -- see docs/MT_PIPELINE_ARCHITECTURE.md.

    adapted: encoder embed_tokens is replaced with a new, independently
      initialized nn.Embedding sized to source_vocabulary_size. Only that
      table is trainable; every other parameter (including the untouched
      decoder embedding / lm_head) is frozen.
    """
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    target_tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=cache_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id, cache_dir=cache_dir)

    for parameter in model.parameters():
        parameter.requires_grad = False

    if condition == "adapted":
        if source_vocabulary_size is None or source_pad_id is None:
            raise ValueError(
                "adapted condition requires source_vocabulary_size and source_pad_id"
            )
        hidden_size = model.config.d_model
        new_embedding = torch.nn.Embedding(
            source_vocabulary_size, hidden_size, padding_idx=source_pad_id
        )
        torch.nn.init.normal_(new_embedding.weight, mean=0.0, std=hidden_size**-0.5)
        with torch.no_grad():
            new_embedding.weight[source_pad_id].zero_()
        model.model.encoder.embed_tokens = new_embedding
        for parameter in model.model.encoder.embed_tokens.parameters():
            parameter.requires_grad = True
    elif condition == "baseline":
        for parameter in model.parameters():
            parameter.requires_grad = True
    else:
        raise ValueError(f"unknown condition: {condition!r}")

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    return LoadedMTModel(
        model=model,
        target_tokenizer=target_tokenizer,
        condition=condition,
        trainable_parameter_count=trainable,
        total_parameter_count=total,
        model_id=model_id,
    )
