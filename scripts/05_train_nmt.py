"""Stage 5 — fine-tune one NLLB-200 arm.

    python scripts/05_train_nmt.py --arm baseline
    python scripts/05_train_nmt.py --arm adapted
    python scripts/05_train_nmt.py --arm control     # recommended third arm

All arms share the same split, schedule, optimiser, batch size and seed; the
only differences are the source tokenizer and the initialisation of the
grafted encoder embedding.
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import _bootstrap  # noqa: F401
import torch
from kapampangan_mt.config import load_config
from kapampangan_mt.nllb.dataset import Collator, KapampanganFilipinoDataset, load_pairs
from kapampangan_mt.nllb.graft import GraftConfig, build_model
from kapampangan_mt.nllb.train import TrainConfig, train
from kapampangan_mt.tokenizer import KapampanganTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/pipeline.yaml")
    ap.add_argument("--set", nargs="*", default=[])
    ap.add_argument("--arm", choices=["baseline", "adapted", "control"], required=True)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    a = ap.parse_args()
    cfg = load_config(a.config, a.set)

    proc = Path(cfg.get_path("paths.processed_dir"))
    out = Path(cfg.get_path("paths.artifacts_dir")) / "nmt" / a.arm
    out.mkdir(parents=True, exist_ok=True)

    src_tok = None
    if a.arm == "adapted":
        src_tok = KapampanganTokenizer.load(
            Path(cfg.get_path("paths.artifacts_dir")) / "tokenizer" / "morphbpe.json")

    gcfg = GraftConfig(
        arm=a.arm,
        model_name=cfg.get_path("nllb.model_name"),
        init=cfg.get_path("nllb.init", "subword_average"),
        tgt_lang=cfg.get_path("nllb.tgt_lang"),
        freeze_backbone=cfg.get_path("nllb.freeze_backbone", True),
        seed=cfg.get_path("seed", 13),
    )
    model, nllb_tok, info = build_model(gcfg, src_tok, device=a.device)
    print(json.dumps(info, indent=2))
    if a.arm != "adapted":
        from kapampangan_mt.baselines import NLLBTokenizerAdapter
        src_tok = NLLBTokenizerAdapter(
            cfg.get_path("nllb.model_name"),
            cfg.get_path("nllb.baseline_src_lang"), hf_tokenizer=nllb_tok)

    ds = {k: KapampanganFilipinoDataset(load_pairs(proc / f"{k}.tsv"), src_tok, nllb_tok,
                                        tgt_lang=cfg.get_path("nllb.tgt_lang"))
          for k in ("train", "val")}
    coll = Collator(src_pad_id=getattr(src_tok, "pad_id", nllb_tok.pad_token_id),
                    tgt_pad_id=nllb_tok.pad_token_id)

    tcfg = TrainConfig(**{k: v for k, v in cfg.get_path("train", {}).items()
                          if k in TrainConfig.__dataclass_fields__})
    tcfg.seed = cfg.get_path("seed", 13)
    summary = train(model, ds["train"], ds["val"], coll, tcfg, str(out), device=a.device)
    (out / "graft_info.json").write_text(json.dumps(info, indent=2))
    print(f"best val loss = {summary['best_val_loss']:.4f}; artefacts -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
