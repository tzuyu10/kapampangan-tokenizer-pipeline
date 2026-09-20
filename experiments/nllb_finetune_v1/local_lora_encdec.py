"""Phase 5 escalation (Option 3): LoRA on encoder AND decoder, run locally.

Local port of `notebooks/phase5-lora-encoder-decoder.ipynb` (written for
Colab, never run). Encoder-only LoRA (`local_lora.py`, Option 4) has all
four tokenizer conditions converging ~13-20 chrF++ below zero-shot -- the
frozen decoder never adapts to the new tokenisation at all. This unfreezes
the decoder's self-attention AND cross-attention (`encoder_attn`, where it
reads the encoder's output) via LoRA, so the model has actual capacity to
build a pathway that could differentiate a better-segmented source from a
worse-segmented one.

**This departs from the proposal's frozen-NLLB framing and needs an explicit
methodology caveat if reported.** It also risks catastrophic forgetting of
NLLB's existing Filipino fluency -- a real failure mode, not hypothetical.

**The matched control is mandatory.** Once the decoder adapts, `nllb_zeroshot`
is no longer a fair comparison (any gain could just be decoder fine-tuning,
nothing to do with the tokenizer). The real test is a swap condition
(`penalty8`/`morphbpe`/`bpe6080`/`unigram6080`) vs `--condition nllb_native`
under the IDENTICAL LoRA budget -- `nllb_native` uses NLLB's own tokenizer
and its own (frozen) `shared` embedding, no encoder-embedding swap, but
gets the same encoder+decoder LoRA adapters. `nllb_zeroshot` stays only as
the untrained reference.

decoder's `embed_tokens` / `lm_head` / `shared` (the 256K-vocab table) stay
frozen throughout -- LoRA only adds small adapters alongside them;
`tie_weights()` is never called after the encoder-embedding swap.

Run (repo root, isolated local venv):
  runs\\nllb-local\\.venv\\Scripts\\python.exe experiments\\nllb_finetune_v1\\local_lora_encdec.py

Key options (see --help):
  --condition {morphbpe,penalty8,bpe6080,unigram6080,nllb_native}  default penalty8
  --seed INT                default 0
  --r INT / --alpha INT      LoRA rank / alpha        default 16 / 32
  --targets q_proj,v_proj    self-attn (+ cross-attn) projections to adapt
  --emb-lr / --lora-lr       default 1e-3 / 2e-4  (separate param groups)
  --epochs / --patience / --batch     default 25 / 5 / 8

Result key: `<condition>-loraencdec/seed<N>` in reports/phase5-results-local.json
(distinct from `local_lora.py`'s `<condition>-lora/seed<N>` -- both live in
the same file without colliding).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import sacrebleu
import torch
import torch.nn as nn
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

with contextlib.suppress(Exception):
    sys.stdout.reconfigure(line_buffering=True)  # type: ignore[union-attr]

EXPERIMENT_ROOT = Path(__file__).resolve().parent
BUNDLE_DIR = EXPERIMENT_ROOT / "data" / "bundle"
DEFAULT_RESULTS = EXPERIMENT_ROOT / "reports" / "phase5-results-local.json"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
AMP_DTYPE = torch.bfloat16 if DEVICE == "cuda" else torch.float32


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def batched(seq: list[Any], n: int) -> Any:
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--condition",
        default="penalty8",
        choices=("morphbpe", "penalty8", "bpe6080", "penalty32", "unigram6080", "nllb_native"),
    )
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--targets", default="q_proj,v_proj")
    ap.add_argument("--lora-dropout", type=float, default=0.05)
    ap.add_argument("--emb-lr", type=float, default=1e-3)
    ap.add_argument("--lora-lr", type=float, default=2e-4)
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--patience", type=int, default=5)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max-new-tokens", type=int, default=160)
    ap.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    args = ap.parse_args()

    print(f"device={DEVICE}  amp_dtype={AMP_DTYPE}")
    if DEVICE == "cuda":
        p = torch.cuda.get_device_properties(0)
        print(f"GPU: {p.name}  {round(p.total_memory / 1024**3, 1)} GiB")

    meta = json.loads((BUNDLE_DIR / "meta.json").read_text(encoding="utf-8"))
    vocab = json.loads((BUNDLE_DIR / "vocab.json").read_text(encoding="utf-8"))
    train = read_jsonl(BUNDLE_DIR / "train.jsonl")
    dev = read_jsonl(BUNDLE_DIR / "dev.jsonl")
    test_sets = {
        "test_bible": read_jsonl(BUNDLE_DIR / "test_bible.jsonl"),
        "test_ood": read_jsonl(BUNDLE_DIR / "test_ood.jsonl"),
    }
    print(
        f"train {len(train)} | dev {len(dev)} | "
        f"test_bible {len(test_sets['test_bible'])} | test_ood {len(test_sets['test_ood'])}"
    )

    tgt_lang = meta["nllb"]["target_lang"]
    native_src_lang = meta["nllb"]["native_baseline_source_lang"]
    src_vocab = meta["source_vocab_size_morphbpe"]
    src_pad = meta["source_pad_id_morphbpe"]
    model_name = meta["nllb"]["model"]
    swap_conditions = set(meta["conditions"])

    args.results.parent.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = (
        json.loads(args.results.read_text(encoding="utf-8")) if args.results.exists() else {}
    )

    def save_results() -> None:
        args.results.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.tgt_lang = tgt_lang
    tgt_bos = tokenizer.convert_tokens_to_ids(tgt_lang)
    pad = tokenizer.pad_token_id

    def src_ids_for(condition: str, rec: dict[str, Any]) -> list[int]:
        if condition == "morphbpe":
            return rec["morphbpe_ids"]  # type: ignore[no-any-return]
        if condition == "penalty8":
            return rec["penalty8_ids"]  # type: ignore[no-any-return]
        if condition == "bpe6080":
            return rec["bpe_ids"]  # type: ignore[no-any-return]
        if condition == "penalty32":
            return rec["penalty32_ids"]  # type: ignore[no-any-return]
        if condition == "unigram6080":
            return rec["unigram_ids"]  # type: ignore[no-any-return]
        tokenizer.src_lang = native_src_lang
        return tokenizer(rec["pam_text"], add_special_tokens=True)["input_ids"]  # type: ignore[no-any-return]

    def label_ids(rec: dict[str, Any]) -> list[int]:
        return tokenizer(text_target=rec["fil_text"], add_special_tokens=True)["input_ids"]  # type: ignore[no-any-return]

    def src_pad_for(condition: str) -> int:
        return src_pad if condition in swap_conditions else pad  # type: ignore[no-any-return]

    def collate(
        batch: list[dict[str, Any]], condition: str
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        src = [src_ids_for(condition, r) for r in batch]
        lab = [label_ids(r) for r in batch]
        sm = max(len(x) for x in src)
        lm = max(len(x) for x in lab)
        p = src_pad_for(condition)
        ii = torch.full((len(batch), sm), p, dtype=torch.long)
        am = torch.zeros((len(batch), sm), dtype=torch.long)
        lb = torch.full((len(batch), lm), -100, dtype=torch.long)
        for i, (s, lab_ids) in enumerate(zip(src, lab, strict=True)):
            ii[i, : len(s)] = torch.tensor(s)
            am[i, : len(s)] = 1
            lb[i, : len(lab_ids)] = torch.tensor(lab_ids)
        return ii.to(DEVICE), am.to(DEVICE), lb.to(DEVICE)

    nllb_special_row = {
        0: pad,
        1: tokenizer.unk_token_id,
        2: tokenizer.bos_token_id,
        3: tokenizer.eos_token_id,
    }

    def warm_start_embedding(condition: str, shared_weight: torch.Tensor) -> nn.Embedding:
        d = shared_weight.size(1)
        emb = nn.Embedding(src_vocab, d, padding_idx=src_pad)
        strings = vocab[condition]
        with torch.no_grad():
            emb.weight.normal_(0.0, d**-0.5)
            for i, s in enumerate(strings):
                if i in nllb_special_row:
                    emb.weight[i] = shared_weight[nllb_special_row[i]].cpu()
                    continue
                sub = tokenizer(s, add_special_tokens=False)["input_ids"]
                if sub:
                    emb.weight[i] = shared_weight[sub].mean(0).cpu()
            emb.weight[src_pad].zero_()
        return emb

    projections = "|".join(t.strip() for t in args.targets.split(","))
    # encoder self-attn + decoder self-attn + decoder cross-attn (encoder_attn)
    target_regex = (
        rf"model\.(encoder|decoder)\.layers\.\d+\.(self_attn|encoder_attn)\.({projections})"
    )

    def prepare_model(condition: str, seed: int) -> tuple[Any, nn.Embedding | None]:
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        m = AutoModelForSeq2SeqLM.from_pretrained(model_name, dtype=torch.float32)
        m.config.use_cache = False
        for p in m.parameters():
            p.requires_grad_(False)
        emb = None
        if condition in swap_conditions:
            # swap encoder input embedding for a warm-started, trainable one
            emb = warm_start_embedding(condition, m.model.shared.weight.detach())
            emb.weight.requires_grad_(True)
            m.model.encoder.embed_tokens = emb
        # LoRA on encoder self-attn + decoder self-attn + decoder cross-attn
        cfg = LoraConfig(
            r=args.r,
            lora_alpha=args.alpha,
            lora_dropout=args.lora_dropout,
            target_modules=target_regex,
            bias="none",
            task_type="SEQ_2_SEQ_LM",
        )
        m = get_peft_model(m, cfg)
        # peft froze everything except adapters; re-enable the swapped embedding
        base = m.get_base_model()
        if emb is not None:
            base.model.encoder.embed_tokens.weight.requires_grad_(True)
        m.to(DEVICE)
        return m, (base.model.encoder.embed_tokens if emb is not None else None)

    gen_kw = dict(num_beams=4, max_new_tokens=args.max_new_tokens, forced_bos_token_id=tgt_bos)

    @torch.no_grad()
    def dev_loss(m: Any, condition: str) -> float:
        m.eval()
        tot, nb = 0.0, 0
        for chunk in batched(dev, args.batch):
            ii, am, lb = collate(chunk, condition)
            with torch.autocast(device_type="cuda", dtype=AMP_DTYPE, enabled=DEVICE == "cuda"):
                tot += float(m(input_ids=ii, attention_mask=am, labels=lb).loss)
            nb += 1
        return tot / nb

    @torch.no_grad()
    def eval_gen(m: Any, data: list[dict[str, Any]], condition: str) -> dict[str, float]:
        m.eval()
        hyps: list[str] = []
        refs = [r["fil_text"] for r in data]
        for chunk in batched(data, args.batch):
            src = [src_ids_for(condition, r) for r in chunk]
            sm = max(len(x) for x in src)
            p = src_pad_for(condition)
            ii = torch.full((len(chunk), sm), p, dtype=torch.long)
            am = torch.zeros((len(chunk), sm), dtype=torch.long)
            for i, s in enumerate(src):
                ii[i, : len(s)] = torch.tensor(s)
                am[i, : len(s)] = 1
            with torch.autocast(device_type="cuda", dtype=AMP_DTYPE, enabled=DEVICE == "cuda"):
                out = m.generate(input_ids=ii.to(DEVICE), attention_mask=am.to(DEVICE), **gen_kw)
            hyps += tokenizer.batch_decode(out, skip_special_tokens=True)
        return {
            "bleu": round(sacrebleu.corpus_bleu(hyps, [refs]).score, 2),
            "chrf": round(sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score, 2),
        }

    key = f"{args.condition}-loraencdec/seed{args.seed}"
    if key in results:
        print(f"{key} already in {args.results}; delete it to re-run.")
        return 0

    print(
        f"\n--- {key}  r={args.r} alpha={args.alpha} targets={args.targets} (enc+dec)  "
        f"emb-lr={args.emb_lr} lora-lr={args.lora_lr}  epochs<= {args.epochs} ---"
    )
    t0 = time.time()
    m, emb = prepare_model(args.condition, args.seed)
    lora_params = [p for n, p in m.named_parameters() if "lora_" in n and p.requires_grad]
    n_emb = emb.weight.numel() if emb is not None else 0
    n_lora = sum(p.numel() for p in lora_params)
    print(f"trainable: embedding {n_emb:,}  +  LoRA {n_lora:,}  =  {n_emb + n_lora:,}")
    param_groups = [{"params": lora_params, "lr": args.lora_lr}]
    if emb is not None:
        param_groups.append({"params": [emb.weight], "lr": args.emb_lr})
    opt = torch.optim.AdamW(param_groups)

    order = list(range(len(train)))
    best_loss = float("inf")
    best_state = {n: p.detach().clone() for n, p in m.named_parameters() if p.requires_grad}
    best_ep, bad = 0, 0
    for ep in range(1, args.epochs + 1):
        m.train()
        random.Random(1000 + args.seed * 97 + ep).shuffle(order)
        tr, nb = 0.0, 0
        ep_t0 = time.time()
        for idx in batched(order, args.batch):
            ii, am, lb = collate([train[i] for i in idx], args.condition)
            with torch.autocast(device_type="cuda", dtype=AMP_DTYPE, enabled=DEVICE == "cuda"):
                loss = m(input_ids=ii, attention_mask=am, labels=lb).loss
            loss.backward()
            opt.step()
            opt.zero_grad()
            tr += float(loss.detach())
            nb += 1
        dl = dev_loss(m, args.condition)
        print(
            f"  {key} ep{ep:02d}  train {tr / nb:.3f}  dev-loss {dl:.3f}  "
            f"({time.time() - ep_t0:.0f}s)"
        )
        if dl < best_loss - 1e-3:
            best_loss = dl
            best_state = {n: p.detach().clone() for n, p in m.named_parameters() if p.requires_grad}
            best_ep, bad = ep, 0
        else:
            bad += 1
            if bad >= args.patience:
                print("  early stop")
                break
    with torch.no_grad():
        for n, p in m.named_parameters():
            if n in best_state:
                p.copy_(best_state[n])

    dev_score = eval_gen(m, dev, args.condition)
    test_scores = {name: eval_gen(m, data, args.condition) for name, data in test_sets.items()}
    results[key] = {
        "condition": f"{args.condition}-loraencdec",
        "seed": args.seed,
        "lora": {
            "r": args.r,
            "alpha": args.alpha,
            "targets": args.targets,
            "scope": "encoder+decoder",
        },
        "trainable_params": {"embedding": n_emb, "lora": n_lora},
        "best_epoch": best_ep,
        "best_dev_loss": round(best_loss, 3),
        "emb_lr": args.emb_lr,
        "lora_lr": args.lora_lr,
        "dev": dev_score,
        **test_scores,
        "minutes": round((time.time() - t0) / 60, 1),
    }
    save_results()
    print(
        f"  -> {key}  DEV {dev_score}  test_bible {test_scores['test_bible']}  "
        f"test_ood {test_scores['test_ood']}  ({results[key]['minutes']} min)"
    )
    print(f"\nwrote {args.results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
