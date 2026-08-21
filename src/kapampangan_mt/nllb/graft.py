"""Grafting a new source vocabulary onto NLLB-200 distilled 600M (thesis p. 44).

The thesis says: "the source embedding layer will be resized and newly
initialized ... only the source embedding parameters will be updated ... all
remaining pretrained parameters remain frozen ... minimizing broader
architectural modification".

What that actually requires
---------------------------
NLLB (``M2M100ForConditionalGeneration``) has ONE embedding matrix,
``model.model.shared``, tied three ways: encoder input, decoder input and the
output projection ``lm_head``.  There is no separate "source embedding layer"
to resize.  Doing what the thesis describes therefore means **untying the
encoder input embedding** from the other two.  That is a real architectural
change and must be written down (Issue N-1).

This module performs the graft for BOTH experimental arms so they are
structurally identical and differ only in tokenizer + initialisation:

  arm ``baseline``  native NLLB tokenizer, encoder embedding = copy of the
                    pretrained ``shared`` matrix, everything else frozen
  arm ``adapted``   proposed tokenizer, fresh encoder embedding
  arm ``control``   native NLLB tokenizer, encoder embedding re-initialised
                    the same way as ``adapted``  (Issue N-2: without this arm
                    "tokenizer" and "embedding initialisation" are confounded
                    and the study cannot attribute a difference to morphology)

Initialisation strategies for the new matrix
--------------------------------------------
``random``            N(0, d_model^-0.5).  What the thesis literally specifies.
``subword_average``   For each new token, tokenize its surface string with the
                      native NLLB tokenizer and average the pretrained
                      embeddings of the resulting pieces.  Standard vocabulary
                      transfer.  Strongly recommended: with ~13k sentence pairs
                      and a frozen backbone, random init has far too little
                      signal to converge, and a failed adapted arm would be
                      reported as "morphology does not help" when it actually
                      means "we could not train 8M parameters on 260k tokens".
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import torch
import torch.nn as nn

MODEL_NAME = "facebook/nllb-200-distilled-600M"


@dataclass
class GraftConfig:
    arm: str = "adapted"                  # baseline | adapted | control
    model_name: str = MODEL_NAME
    init: str = "subword_average"         # random | subword_average | copy
    tgt_lang: str = "tgl_Latn"
    freeze_backbone: bool = True
    train_encoder_layernorms: bool = False  # cheap extra capacity; report if used
    seed: int = 13


def _random_init(weight: torch.Tensor, d_model: int, seed: int) -> None:
    g = torch.Generator().manual_seed(seed)
    with torch.no_grad():
        weight.normal_(mean=0.0, std=d_model ** -0.5, generator=g)


def _subword_average_init(
    weight: torch.Tensor, src_tokenizer, nllb_tokenizer, pretrained: torch.Tensor,
    d_model: int, seed: int,
) -> dict:
    """Seed each new token from the NLLB pieces that spell it."""
    _random_init(weight, d_model, seed)
    mean_vec = pretrained.mean(dim=0)
    hits = misses = 0
    id_map = {v: k for k, v in src_tokenizer.vocab.items()}
    with torch.no_grad():
        for idx in range(weight.shape[0]):
            surface = id_map.get(idx, "")
            if not surface:
                continue
            if surface.startswith("<") and surface.endswith(">"):
                weight[idx] = mean_vec           # specials / byte fallbacks
                continue
            probe = surface.replace("▁", " ").strip()
            if not probe:
                weight[idx] = mean_vec
                continue
            pieces = nllb_tokenizer(probe, add_special_tokens=False)["input_ids"]
            pieces = [p for p in pieces if p < pretrained.shape[0]]
            if pieces:
                weight[idx] = pretrained[pieces].mean(dim=0)
                hits += 1
            else:
                weight[idx] = mean_vec
                misses += 1
    return {"init_hits": hits, "init_misses": misses}


def build_model(
    cfg: GraftConfig,
    src_tokenizer=None,
    nllb_tokenizer=None,
    device: str = "cpu",
):
    """Return ``(model, nllb_tokenizer, info)`` ready for training.

    ``src_tokenizer`` is a :class:`KapampanganTokenizer` for the ``adapted``
    arm and ``None`` for ``baseline``/``control``.
    """
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

    if nllb_tokenizer is None:
        nllb_tokenizer = AutoTokenizer.from_pretrained(
            cfg.model_name, src_lang="tgl_Latn", tgt_lang=cfg.tgt_lang
        )
    model = AutoModelForSeq2SeqLM.from_pretrained(cfg.model_name)
    d_model = model.config.d_model
    pretrained = model.model.shared.weight.data.clone()

    if cfg.arm == "adapted":
        if src_tokenizer is None:
            raise ValueError("arm='adapted' needs the proposed src_tokenizer")
        src_vocab = src_tokenizer.vocab_size
        src_pad = src_tokenizer.pad_id
    else:
        src_vocab = pretrained.shape[0]
        src_pad = model.config.pad_token_id

    new_emb = nn.Embedding(src_vocab, d_model, padding_idx=src_pad)
    info: dict = {"arm": cfg.arm, "src_vocab": src_vocab, "d_model": d_model}

    if cfg.arm == "baseline":
        with torch.no_grad():
            new_emb.weight.copy_(pretrained)
        info["init"] = "copy(pretrained)"
    elif cfg.arm == "control":
        _random_init(new_emb.weight.data, d_model, cfg.seed)
        info["init"] = "random(control)"
    else:  # adapted
        if cfg.init == "random":
            _random_init(new_emb.weight.data, d_model, cfg.seed)
            info["init"] = "random"
        elif cfg.init == "copy":
            raise ValueError("init='copy' is meaningless for a new vocabulary")
        else:
            info.update(
                _subword_average_init(
                    new_emb.weight.data, src_tokenizer, nllb_tokenizer,
                    pretrained, d_model, cfg.seed,
                )
            )
            info["init"] = "subword_average"

    # --- untie: encoder gets its own matrix, decoder+lm_head keep `shared` ---
    model.model.encoder.embed_tokens = new_emb

    if cfg.freeze_backbone:
        for p in model.parameters():
            p.requires_grad = False
        new_emb.weight.requires_grad = True
        if cfg.train_encoder_layernorms:
            for name, p in model.model.encoder.named_parameters():
                if "layer_norm" in name:
                    p.requires_grad = True

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    info["trainable_params"] = trainable
    info["total_params"] = total
    info["trainable_pct"] = 100.0 * trainable / total

    model.config.forced_bos_token_id = nllb_tokenizer.convert_tokens_to_ids(cfg.tgt_lang)
    model.to(device)
    return model, nllb_tokenizer, info


def save_source_embeddings(model, path: str) -> None:
    """Persist the grafted matrix separately.

    ``save_pretrained`` can drop weights it believes are tied.  The encoder
    matrix is small (vocab x 1024) so an explicit ``.pt`` is simplest and safe.
    """
    torch.save(model.model.encoder.embed_tokens.state_dict(), path)


def load_source_embeddings(model, path: str, map_location="cpu") -> None:
    model.model.encoder.embed_tokens.load_state_dict(
        torch.load(path, map_location=map_location)
    )
