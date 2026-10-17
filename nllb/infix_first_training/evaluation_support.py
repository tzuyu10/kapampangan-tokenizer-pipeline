"""Matched, resumable FP32 translation evaluation and current32 input validation.

Standard-library imports are sufficient for package checks. Torch and SacreBLEU
are imported only when generating/scoring translations on the cloud GPU.
"""
import csv
import hashlib
import json
from pathlib import Path
import zipfile


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def verify_reference(path, search_roots, work, expected_zip_sha,
                     expected_manifest_sha, data_sha, base_revision, helper_sha,
                     target_sha, expected_cfg, expected_splits):
    """Find and verify the optional exact installed weighted32 inference bundle."""
    from training_support import extract_safe_zip
    if not path:
        candidates = set()
        for root in search_roots:
            root = Path(root)
            if not root.exists():
                continue
            candidates.update(p.resolve() for p in root.rglob("current_weighted32_reference.zip"))
        if not candidates:
            for root in search_roots:
                root = Path(root)
                if root.exists():
                    for p in root.rglob("reference_package_manifest.json"):
                        info = json.loads(p.read_text(encoding="utf-8"))
                        if info.get("package_kind") == "current_weighted32_translation_reference":
                            candidates.add(p.parent.resolve())
        if len(candidates) != 1:
            raise ValueError("Set CURRENT32_REFERENCE_PATH to its ZIP or extracted root. Found: " + str(sorted(candidates)))
        path = next(iter(candidates))
    root = Path(path)
    if root.is_file():
        if digest(root) != expected_zip_sha:
            raise ValueError("Current32 reference ZIP hash mismatch")
        root = extract_safe_zip(root, Path(work) / "current32_reference")
    if digest(root / "reference_package_manifest.json") != expected_manifest_sha:
        raise ValueError("Current32 reference manifest hash mismatch")
    package = json.loads((root / "reference_package_manifest.json").read_text(encoding="utf-8"))
    if package.get("package_kind") != "current_weighted32_translation_reference":
        raise ValueError("Not the current weighted32 evaluation reference")
    for name, checksum in package["files"].items():
        file = (root / name).resolve()
        if not file.is_relative_to(root.resolve()) or not file.is_file() or digest(file) != checksum:
            raise ValueError("Current32 reference checksum mismatch: " + name)
    bundle = root / "morph_bpe"
    info = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    history = json.loads((bundle / "history.json").read_text(encoding="utf-8"))
    identity = info["identity"]
    if (info.get("tokenizer_variant") != "weighted_penalty32" or
            info.get("crossing_penalty") != 32 or info.get("weighted_penalty_used") is not True or
            identity.get("tokenizer_variant") != "weighted_penalty32" or
            identity.get("crossing_penalty") != 32 or info.get("training_status") != "completed" or
            info.get("completed_epochs") != 30 or info.get("selected_epoch") != 30 or
            [r["epoch"] for r in history] != list(range(1, 31)) or
            min(history, key=lambda r: r["validation_loss"])["epoch"] != 30 or
            info["cfg"] != expected_cfg or identity["data_sha256"] != data_sha or
            info["revision"] != base_revision or identity["helper_sha256"] != helper_sha or
            digest(bundle / "nllb_source_adapter.py") != helper_sha or
            digest(bundle / "target_tokenizer/tokenizer.json") != target_sha or
            identity["source_limit"] != 256 or identity["target_limit"] != 128 or
            identity["beams"] != 4 or identity["max_new_tokens"] != 160 or
            json.loads((bundle / "split_manifest.json").read_text()) != expected_splits):
        raise ValueError("Current32 reference is not the matched installed 30-epoch condition")
    for name, key in (("source_artifact/tokenizer.json", "tokenizer_sha256"),
                      ("source_artifact/tokenizer-manifest.json", "artifact_manifest_sha256"),
                      ("runtime/kapampangan_morphbpe_runtime/tokenizer.py", "runtime_sha256")):
        if digest(bundle / name) != identity[key]:
            raise ValueError("Current32 bundle identity mismatch: " + name)
    if (bundle / "last.pt").exists():
        raise ValueError("Reference is an inference bundle, not a resume checkpoint")
    return bundle, info


def _prepare_evaluation_progress(destination, evaluation_identity, rows):
    """Resume only predictions already bound to this exact evaluation identity."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    identity_file = destination / "evaluation_identity.json"
    predictions = destination / "predictions.jsonl"
    if identity_file.exists():
        if json.loads(identity_file.read_text(encoding="utf-8")) != evaluation_identity:
            raise ValueError("Evaluation resume identity mismatch")
    else:
        if predictions.is_file() and predictions.stat().st_size:
            raise ValueError("Evaluation predictions exist without their saved identity")
        save_json(identity_file, evaluation_identity)
    completed = []
    if predictions.exists():
        lines = predictions.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                if index != len(lines) - 1:
                    raise
                break
            if len(completed) >= len(rows):
                raise ValueError("Evaluation progress contains extra rows")
            row = rows[len(completed)]
            if (record["id"] != row["id"] or record["source"] != row["raw_source"] or
                    record["target"] != row["raw_target"]):
                raise ValueError("Evaluation progress row mismatch")
            completed.append(record)
        predictions.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in completed), encoding="utf-8")
    return predictions, completed


def evaluate_selected(model, source, target, rows, split, destination, bundle,
                      data_sha, device, beams, max_new_tokens, source_limit):
    """Generate exact raw rows, resume matching predictions, and score both metrics."""
    import importlib.metadata as metadata
    import torch
    import transformers
    from safetensors.torch import load_file
    from sacrebleu.metrics import BLEU, CHRF
    bundle, destination = Path(bundle), Path(destination)
    info = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    identity = info["identity"]
    if info.get("training_status") != "completed":
        raise ValueError("Finish training before generating scored translations")
    weight = load_file(str(bundle / "best_source.safetensors"))["weight"]
    if (tuple(weight.shape) != (6080, 1024) or not torch.isfinite(weight).all() or
            not torch.equal(weight, model.get_encoder().embed_tokens.weight.detach().cpu())):
        raise ValueError("Evaluation model is not using the selected best source weights")
    del weight
    if any(p.is_floating_point() and p.dtype != torch.float32 for p in model.parameters()):
        raise ValueError("Matched translation scoring requires FP32 model weights")
    model.eval()
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    evaluation_identity = dict(
        condition="morph_bpe", tokenizer_variant=info["tokenizer_variant"],
        crossing_penalty=info["crossing_penalty"], infix_priority_used=info.get("infix_priority_used", False),
        split=split, data_sha256=data_sha,
        weights_sha256=digest(bundle / "best_source.safetensors"),
        tokenizer_sha256=identity["tokenizer_sha256"],
        artifact_manifest_sha256=identity["artifact_manifest_sha256"],
        target_tokenizer_sha256=digest(bundle / "target_tokenizer/tokenizer.json"),
        runtime_sha256=identity["runtime_sha256"], helper_sha256=identity["helper_sha256"],
        evaluation_support_sha256=digest(Path(__file__)),
        row_ids_sha256=hashlib.sha256(json.dumps([r["id"] for r in rows]).encode()).hexdigest(),
        base_revision=info["revision"], selected_epoch=info["selected_epoch"],
        beams=beams, max_new_tokens=max_new_tokens, source_limit=source_limit,
        precision="fp32", torch=torch.__version__, transformers=transformers.__version__,
        sacrebleu=metadata.version("sacrebleu"))
    predictions, completed = _prepare_evaluation_progress(destination, evaluation_identity, rows)
    language = target.convert_tokens_to_ids("tgl_Latn")
    if language == target.unk_token_id:
        raise ValueError("Missing native Filipino target language tag")
    with predictions.open("a", encoding="utf-8") as handle:
        for index in range(len(completed), len(rows)):
            row = rows[index]
            ids = source.encode(row["raw_source"])
            if len(ids) > source_limit:
                raise ValueError("Evaluation source exceeds unchanged trained limit")
            if source.special["<unk>"] in ids:
                raise ValueError("Unknown source token in evaluation")
            x = torch.tensor([ids], device=device)
            with torch.inference_mode():
                generated = model.generate(
                    input_ids=x, attention_mask=x.ne(source.pad).long(), forced_bos_token_id=language,
                    max_new_tokens=max_new_tokens, num_beams=beams, do_sample=False, use_cache=True)
            produced = generated[0].tolist()[1:]
            hit_limit = len(produced) >= max_new_tokens and target.eos_token_id not in produced
            record = dict(id=row["id"], source=row["raw_source"], target=row["raw_target"],
                          prediction=target.decode(generated[0], skip_special_tokens=True),
                          output_limit_hit=hit_limit)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
            completed.append(record)
            if (index + 1) % 25 == 0 or index + 1 == len(rows):
                print(info["tokenizer_variant"], split, index + 1, "/", len(rows))
    hypotheses = [r["prediction"] for r in completed]
    references = [r["target"] for r in completed]
    metrics = {}
    for name, metric in (("BLEU", BLEU(tokenize="13a")), ("chrF++", CHRF(word_order=2))):
        metrics[name] = dict(score=metric.corpus_score(hypotheses, [references]).score,
                             signature=str(metric.get_signature()))
    save_json(destination / "metrics.json", metrics)
    save_json(destination / "generation_audit.json", dict(rows=len(rows), output_limit_hits=sum(r["output_limit_hit"] for r in completed)))
    (destination / "hypotheses.txt").write_text("\n".join(hypotheses) + "\n", encoding="utf-8")
    (destination / "references.txt").write_text("\n".join(references) + "\n", encoding="utf-8")
    print(info["tokenizer_variant"], split, metrics)
    return metrics


def compare_scores(candidate_root, reference_root, split):
    """Write a comparison only when decoding, data, rows and environment match."""
    candidate_root, reference_root = Path(candidate_root), Path(reference_root)
    a = json.loads((candidate_root / split / "evaluation_identity.json").read_text())
    b = json.loads((reference_root / split / "evaluation_identity.json").read_text())
    shared = ("split", "data_sha256", "row_ids_sha256", "base_revision", "beams", "max_new_tokens",
              "source_limit", "precision", "torch", "transformers", "sacrebleu", "helper_sha256",
              "target_tokenizer_sha256", "evaluation_support_sha256")
    if any(a[key] != b[key] for key in shared):
        raise ValueError("Cannot compare evaluations with different rows, settings or environments")
    metrics_a = json.loads((candidate_root / split / "metrics.json").read_text())
    metrics_b = json.loads((reference_root / split / "metrics.json").read_text())
    if any(metrics_a[k]["signature"] != metrics_b[k]["signature"] for k in ("BLEU", "chrF++")):
        raise ValueError("Cannot compare different metric signatures")
    records = []
    for name in ("BLEU", "chrF++"):
        value_a, value_b = metrics_a[name]["score"], metrics_b[name]["score"]
        records.append(dict(split=split, metric=name, candidate=a["tokenizer_variant"],
                            candidate_score=value_a, current_weighted32_score=value_b,
                            candidate_minus_current32=value_a - value_b))
    path = candidate_root / (split + "_vs_current32.csv")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print("Matched comparison:", records)
    return path
