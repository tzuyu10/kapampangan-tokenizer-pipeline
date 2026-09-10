"""Phase 5 local diagnostic run -- runs on your own NVIDIA GPU, no Colab.

Question: is the embedding-only recipe's collapse (chrF++ ~13 vs zero-shot
~34 on 2026-09-04, warm-started, lr 3e-4, 10 epochs) a genuine capacity
bottleneck, or was the Colab recipe simply too conservative on LR / epoch
budget? This script re-runs the SAME recipe (warm-started
nn.Embedding(6080,1024), everything else frozen, never call tie_weights())
against the SAME bundle files, but with a much higher default LR and no
epoch cap pressure, so it can be watched to an honest plateau.

Uses bf16 autocast (RTX 40-series Tensor Cores support it natively --
no GradScaler needed, unlike Colab's T4-targeted fp32/fp16 choice). This
alone should also be markedly faster than the 122.6 min/run observed on
Colab (which ran in fp32).

Run (from the repo root, with the isolated local venv):
  runs\\nllb-local\\.venv\\Scripts\\python.exe experiments\\nllb_finetune_v1\\local_diagnostic.py

Options (all optional, see --help):
  --condition {morphbpe,penalty8,unigram6080}  default morphbpe
  --seed INT              default 0
  --lr FLOAT               default 3e-3 (10x the Colab recipe's 3e-4)
  --epochs INT              default 30
  --patience INT            default 6
  --batch INT               default 8
  --skip-zeroshot           skip the local nllb_zeroshot sanity check
  --results PATH             default reports/phase5-results-local.json

Results are appended to the same key schema as the Colab notebook
(`<condition>/seed<N>`, `nllb_zeroshot`) so they can be read side by side
with experiments/nllb_finetune_v1/reports/phase5-results-2026-09-04.json.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path
from typing import Any

import numpy as np
import sacrebleu
import torch
import torch.nn as nn
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

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
    # live output when stdout is a pipe/file (background runs, Monitor)
    try:
        import sys

        sys.stdout.reconfigure(line_buffering=True)  # type: ignore[union-attr]
    except Exception:
        pass

    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--condition", default="morphbpe", choices=("morphbpe", "penalty8", "unigram6080")
    )
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--patience", type=int, default=6)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--max-new-tokens", type=int, default=160)
    ap.add_argument("--skip-zeroshot", action="store_true")
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
    test_bible = read_jsonl(BUNDLE_DIR / "test_bible.jsonl")
    test_ood = read_jsonl(BUNDLE_DIR / "test_ood.jsonl")
    test_sets = {"test_bible": test_bible, "test_ood": test_ood}
    print(
        f"train {len(train)} | dev {len(dev)} | "
        f"test_bible {len(test_bible)} | test_ood {len(test_ood)}"
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

    def fresh_model() -> Any:
        m = AutoModelForSeq2SeqLM.from_pretrained(model_name, dtype=torch.float32)
        m.config.use_cache = False
        return m

    def src_ids_for(condition: str, rec: dict[str, Any]) -> list[int]:
        if condition == "morphbpe":
            return rec["morphbpe_ids"]  # type: ignore[no-any-return]
        if condition == "penalty8":
            return rec["penalty8_ids"]  # type: ignore[no-any-return]
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

    def prepare_model(condition: str, seed: int) -> tuple[Any, nn.Embedding]:
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        m = fresh_model()
        core = m.model
        for p in m.parameters():
            p.requires_grad_(False)
        emb = warm_start_embedding(condition, core.shared.weight.detach())
        emb.weight.requires_grad_(True)
        core.encoder.embed_tokens = emb  # encoder ONLY; never call tie_weights() after this
        m.to(DEVICE)
        trainable = [p for p in m.parameters() if p.requires_grad]
        assert len(trainable) == 1 and trainable[0] is emb.weight
        return m, emb

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

    def eval_all_tests(m: Any, condition: str) -> dict[str, dict[str, float]]:
        return {name: eval_gen(m, data, condition) for name, data in test_sets.items()}

    if not args.skip_zeroshot and "nllb_zeroshot" not in results:
        print("\n--- nllb_zeroshot (sanity check vs the Colab 33.78/33.49 numbers) ---")
        t0 = time.time()
        m = fresh_model().to(DEVICE)
        results["nllb_zeroshot"] = {
            "condition": "nllb_zeroshot",
            "dev": eval_gen(m, dev, "nllb_zeroshot"),
            **eval_all_tests(m, "nllb_zeroshot"),
        }
        save_results()
        print(f"nllb_zeroshot {results['nllb_zeroshot']}  ({(time.time() - t0) / 60:.1f} min)")
        del m
        torch.cuda.empty_cache()

    key = f"{args.condition}/seed{args.seed}"
    print(
        f"\n--- {key}  lr={args.lr}  epochs<= {args.epochs}  "
        f"patience={args.patience}  batch={args.batch} ---"
    )
    t0 = time.time()
    m, emb = prepare_model(args.condition, args.seed)
    opt = torch.optim.AdamW([emb.weight], lr=args.lr)
    order = list(range(len(train)))
    best_loss = float("inf")
    best_state = emb.weight.detach().clone()
    best_ep = 0
    bad = 0
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
            f"({(time.time() - ep_t0):.0f}s)"
        )
        if dl < best_loss - 1e-3:
            best_loss, best_state, best_ep, bad = dl, emb.weight.detach().clone(), ep, 0
        else:
            bad += 1
            if bad >= args.patience:
                print("  early stop")
                break
    with torch.no_grad():
        emb.weight.copy_(best_state)
    dev_score = eval_gen(m, dev, args.condition)
    test_scores = eval_all_tests(m, args.condition)
    results[key] = {
        "condition": args.condition,
        "seed": args.seed,
        "best_epoch": best_ep,
        "best_dev_loss": round(best_loss, 3),
        "lr": args.lr,
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
