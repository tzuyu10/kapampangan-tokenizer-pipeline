"""Fine-tuning loop.

Only the grafted encoder embedding is trainable (see graft.py), so this is a
small optimisation problem and a plain loop is clearer than Seq2SeqTrainer —
and it keeps the *identical* schedule across arms, which is what the thesis
requires for a controlled comparison.
"""
from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from .dataset import Collator, KapampanganFilipinoDataset


@dataclass
class TrainConfig:
    epochs: int = 10
    batch_size: int = 8
    grad_accum: int = 4
    lr: float = 5e-4            # high on purpose: only embeddings train
    weight_decay: float = 0.01
    warmup_ratio: float = 0.06
    max_grad_norm: float = 1.0
    label_smoothing: float = 0.1
    fp16: bool = True
    seed: int = 13
    log_every: int = 25
    patience: int = 3           # early stopping on val loss


def _set_seed(seed: int) -> None:
    import random

    import numpy as np

    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def train(
    model,
    train_ds: KapampanganFilipinoDataset,
    val_ds: KapampanganFilipinoDataset,
    collator: Collator,
    cfg: TrainConfig,
    out_dir: str,
    device: str = "cuda",
) -> dict:
    _set_seed(cfg.seed)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)

    train_dl = DataLoader(train_ds, batch_size=cfg.batch_size, shuffle=True,
                          collate_fn=collator, drop_last=False)
    val_dl = DataLoader(val_ds, batch_size=cfg.batch_size, shuffle=False,
                        collate_fn=collator)

    params = [p for p in model.parameters() if p.requires_grad]
    if not params:
        raise RuntimeError("no trainable parameters — check GraftConfig.freeze_backbone")
    opt = torch.optim.AdamW(params, lr=cfg.lr, weight_decay=cfg.weight_decay)

    steps_per_epoch = math.ceil(len(train_dl) / cfg.grad_accum)
    total_steps = max(1, steps_per_epoch * cfg.epochs)
    warmup = int(total_steps * cfg.warmup_ratio)

    def lr_lambda(step: int) -> float:
        if step < warmup:
            return step / max(1, warmup)
        return max(0.0, (total_steps - step) / max(1, total_steps - warmup))

    sched = torch.optim.lr_scheduler.LambdaLR(opt, lr_lambda)
    use_amp = cfg.fp16 and device.startswith("cuda")
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    loss_fn = torch.nn.CrossEntropyLoss(
        ignore_index=-100, label_smoothing=cfg.label_smoothing
    )

    history, best, bad_epochs, gstep = [], float("inf"), 0, 0
    for epoch in range(1, cfg.epochs + 1):
        model.train(); running, seen, t0 = 0.0, 0, time.time()
        opt.zero_grad(set_to_none=True)
        for i, batch in enumerate(train_dl):
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.amp.autocast("cuda", enabled=use_amp):
                logits = model(**batch).logits
                loss = loss_fn(
                    logits.view(-1, logits.size(-1)), batch["labels"].view(-1)
                ) / cfg.grad_accum
            scaler.scale(loss).backward()
            running += loss.item() * cfg.grad_accum; seen += 1
            if (i + 1) % cfg.grad_accum == 0 or (i + 1) == len(train_dl):
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_(params, cfg.max_grad_norm)
                scaler.step(opt); scaler.update()
                opt.zero_grad(set_to_none=True); sched.step(); gstep += 1
                if gstep % cfg.log_every == 0:
                    print(f"  ep{epoch} step{gstep}/{total_steps} "
                          f"loss={running/max(seen,1):.4f} lr={sched.get_last_lr()[0]:.2e}")

        val_loss = evaluate_loss(model, val_dl, device, loss_fn, use_amp)
        rec = {"epoch": epoch, "train_loss": running / max(seen, 1),
               "val_loss": val_loss, "secs": round(time.time() - t0, 1)}
        history.append(rec)
        print(f"[epoch {epoch}] train={rec['train_loss']:.4f} val={val_loss:.4f} "
              f"({rec['secs']}s)")

        if val_loss < best - 1e-4:
            best, bad_epochs = val_loss, 0
            torch.save(model.model.encoder.embed_tokens.state_dict(),
                       out / "src_embeddings.best.pt")
        else:
            bad_epochs += 1
            if bad_epochs >= cfg.patience:
                print(f"early stopping at epoch {epoch}")
                break

    torch.save(model.model.encoder.embed_tokens.state_dict(), out / "src_embeddings.last.pt")
    summary = {"config": asdict(cfg), "history": history, "best_val_loss": best}
    (out / "train_log.json").write_text(json.dumps(summary, indent=2))
    model.model.encoder.embed_tokens.load_state_dict(
        torch.load(out / "src_embeddings.best.pt", map_location=device)
    )
    return summary


@torch.no_grad()
def evaluate_loss(model, dl, device, loss_fn, use_amp: bool) -> float:
    model.eval(); tot, n = 0.0, 0
    for batch in dl:
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.amp.autocast("cuda", enabled=use_amp):
            logits = model(**batch).logits
            loss = loss_fn(logits.view(-1, logits.size(-1)), batch["labels"].view(-1))
        tot += loss.item(); n += 1
    return tot / max(n, 1)
