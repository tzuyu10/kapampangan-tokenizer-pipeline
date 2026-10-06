"""Source-embedding-only NLLB adaptation. Embedded in the companion notebook."""
import copy
import hashlib
import json
import math
import random
import shutil
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader
from tokenizers import Tokenizer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize(text):
    import unicodedata
    return " ".join(unicodedata.normalize("NFC", text).split())


def read_parallel(path):
    """Require explicit, fixed splits; reject duplicate sources and document leakage."""
    import csv
    path = Path(path)
    if path.suffix == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    elif path.suffix == ".jsonl":
        rows = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines() if s.strip()]
    else:
        raise ValueError("Use UTF-8 .csv or .jsonl with id, source, target, split, group_id.")
    splits = {s: [] for s in ["train", "validation", "test"]}
    ids, sources, groups = set(), set(), {}
    for row in rows:
        for key in ["id", "source", "target", "split", "group_id"]:
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f"Missing/non-string {key}: {row.get('id')}")
        row = dict(row)
        row["source"], row["target"] = normalize(row["source"]), normalize(row["target"])
        split = row["split"]
        if split not in splits:
            raise ValueError(f"Invalid split {split}")
        if row["id"] in ids or row["source"] in sources:
            raise ValueError("Duplicate ID/source: deduplicate or consolidate references before splitting.")
        group = row["group_id"]
        if group in groups and groups[group] != split:
            raise ValueError(f"Document/group leakage: {group}")
        ids.add(row["id"]); sources.add(row["source"]); groups[group] = split
        splits[split].append(row)
    if not all(splits.values()):
        raise ValueError("Every split must contain at least one row.")
    return splits


class SourceTokenizer:
    """Portable tokenizer.json. Wrapper, not backend, inserts source control tokens."""
    def __init__(self, path, expected_size=6080):
        path = Path(path)
        self.artifact_dir = path if path.is_dir() else None
        if self.artifact_dir is not None:
            from kapampangan_morphbpe_runtime import Tokenizer as ProjectTokenizer
            manifest = json.loads((path/'tokenizer-manifest.json').read_text(encoding='utf-8'))
            for name, checksum in manifest['core_file_sha256'].items():
                if Path(name).name != name or digest(path/name) != checksum:
                    raise ValueError(f'Artifact checksum mismatch: {name}')
            self.backend = ProjectTokenizer(path)
            self.size = self.backend.vocabulary_size
            entries = json.loads((path/'special_tokens.json').read_text())['special_tokens']
            original = {e['token']:e['id'] for e in entries}
            if original != {'<pad>':0, '<unk>':1, '<s>':2, '</s>':3}:
                raise ValueError('Unexpected project special-token layout')
            # Reversible permutation ONLY at the model boundary, not in the artifact.
            # NLLB encoder positional embeddings treat ID 1 as padding.
            self.special = {t:self.to_model_id(i) for t,i in original.items()}
            self.pad = 1
            self.start = self.special['<s>']
            if self.size != expected_size:
                raise ValueError(f'Expected {expected_size} source entries, got {self.size}')
            return
        self.backend = Tokenizer.from_file(str(path))
        self.backend.no_padding(); self.backend.no_truncation()
        self.size = self.backend.get_vocab_size(with_added_tokens=True)
        if self.size != expected_size:
            raise ValueError(f"Expected exactly {expected_size} total IDs; got {self.size}. Do not pad vocab with dummy tokens.")
        if set(self.backend.get_vocab().values()) != set(range(self.size)):
            raise ValueError("Source IDs must be contiguous.")
        self.special = {t: self.backend.token_to_id(t) for t in ["<s>", "<pad>", "</s>", "<unk>", "<kap>"]}
        if any(v is None for v in self.special.values()) or len(set(self.special.values())) != 5:
            raise ValueError("Reserve <s>, <pad>, </s>, <unk>, <kap> in the 6080-token vocabulary.")
        # M2M100 position embeddings use config.pad_token_id; keep source PAD equal to it.
        if self.special["<pad>"] != 1:
            raise ValueError("Export source <pad> as ID 1 (needed by NLLB position indexing).")
        self.pad = 1
        self.start = self.special['<kap>']

    @staticmethod
    def to_model_id(i):
        return 1-i if i in (0,1) else i

    def vocab_strings(self):
        if self.artifact_dir is not None:
            entries = json.loads((self.artifact_dir/'vocab.json').read_text(encoding='utf-8'))['tokens']
            result = [''] * self.size
            for entry in entries: result[self.to_model_id(entry['id'])] = entry['token']
            return result
        result = [''] * self.size
        for token, i in self.backend.get_vocab().items(): result[i] = token
        return result

    def content_ids(self, text):
        if self.artifact_dir is not None:
            ids = [self.to_model_id(i) for i in self.backend.encode(text, add_special_tokens=False).ids]
        else:
            ids = self.backend.encode(normalize(text), add_special_tokens=False).ids
        reserved = set(self.special.values()) - {self.special["<unk>"]}
        if not ids or any(i < 0 or i >= self.size or i in reserved for i in ids):
            raise ValueError("Empty/invalid encoding or reserved control token inside source text.")
        return ids

    def encode(self, text):
        return [self.start] + self.content_ids(text) + [self.special["</s>"]]


def source_ids_for(condition, record):
    """Project bundle routing is closed: unknown conditions never fall back to NLLB."""
    fields = {'plain_bpe':'bpe_ids', 'bpe6080':'bpe_ids', 'morph_bpe':'morphbpe_ids', 'morphbpe':'morphbpe_ids'}
    if condition not in fields: raise ValueError(f'Unsupported thesis condition: {condition}')
    ids = record[fields[condition]]
    if not ids or any(type(i) is not int or not 0 <= i < 6080 for i in ids):
        raise ValueError('Invalid project source IDs')
    return [SourceTokenizer.to_model_id(i) for i in ids]


def read_project_bundle(root):
    """Validate the existing frozen bundle; preserve its two separate test sets."""
    root = Path(root)
    meta = json.loads((root/'meta.json').read_text(encoding='utf-8'))
    data = {}; seen = {}; audit = {'duplicate_sources_within_split':{}, 'cross_split_source_overlap':[]}
    for split in ['train','dev','test_bible','test_ood']:
        path = root/(split+'.jsonl')
        if digest(path) != meta['split_sha256'][split]: raise ValueError(f'Bundle hash mismatch: {split}')
        rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
        if len(rows) != meta['split_counts'][split]: raise ValueError('Split count mismatch')
        data[split] = []; duplicates = 0
        for i,row in enumerate(rows):
            for field in ['pam_text','fil_text']:
                if not isinstance(row.get(field),str) or not row[field].strip(): raise ValueError(f'Empty {field}')
            key = normalize(row['pam_text']).casefold()
            if key in seen:
                if seen[key] != split: audit['cross_split_source_overlap'].append({'split':split,'row':i,'other_split':seen[key]})
                else: duplicates += 1
            seen[key] = split
            # Stable row ID within the checksum-locked bundle; not a document ID.
            data[split].append({**row,'id':f'{split}:{i}','source':row['pam_text'],'target':row['fil_text']})
        audit['duplicate_sources_within_split'][split] = duplicates
    if audit['cross_split_source_overlap']:
        raise ValueError(f'Cross-split normalized source overlap: {audit["cross_split_source_overlap"][:10]}')
    audit['document_group_audit'] = 'See original split-manifest.json; bundle has no per-row document IDs.'
    audit['tokenizer_training_vs_translation_test_overlap'] = 'Not established by bundle checks; requires original tokenizer corpus.'
    return data, meta, audit


def prepare(splits, source, target, max_source, max_target):
    """No silent truncation: matched experiments must see the same complete sentences."""
    encoded, stats = {}, {}
    for split, rows in splits.items():
        encoded[split] = []
        unknown, count, max_s, max_t = 0, 0, 0, 0
        for row in rows:
            x = source.encode(row["source"])
            y = target(text_target=row["target"], truncation=False)["input_ids"]
            if len(x) > max_source or len(y) > max_target:
                raise ValueError(f"{row['id']} exceeds length limits ({len(x)}, {len(y)}). Increase limits equally for both conditions, or predefine a shared sentence segmentation policy.")
            unknown += x.count(source.special["<unk>"]); count += len(x)-2
            max_s, max_t = max(max_s, len(x)), max(max_t, len(y))
            encoded[split].append({"input_ids": x, "labels": y})
        stats[split] = {"rows": len(rows), "unknown_fraction": unknown/max(count, 1),
                        "max_source_tokens": max_s, "max_target_tokens": max_t}
    return encoded, stats


def collate(rows, pad=1):
    source_len = max(len(r["input_ids"]) for r in rows)
    target_len = max(len(r["labels"]) for r in rows)
    x = torch.full((len(rows), source_len), pad, dtype=torch.long)
    y = torch.full((len(rows), target_len), -100, dtype=torch.long)
    for i, r in enumerate(rows):
        x[i, :len(r["input_ids"])] = torch.tensor(r["input_ids"])
        y[i, :len(r["labels"])] = torch.tensor(r["labels"])
    return {"input_ids": x, "attention_mask": x.ne(pad).long(), "labels": y}


def install_source_embedding(model, vocab_size, seed, pad=1):
    """Detach ONLY encoder lookup; never resize global vocabulary or retie weights."""
    for p in model.parameters():
        p.requires_grad_(False)
    encoder = model.get_encoder()
    old = encoder.embed_tokens
    if pad != model.config.pad_token_id:
        raise ValueError("Source and model padding IDs must agree for positional embeddings.")
    # Keep the original embedding class and any scaling behavior, but use new storage.
    new = copy.copy(old)
    new._parameters = old._parameters.copy()
    new.num_embeddings = vocab_size
    new.padding_idx = pad
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seed)
        weight = torch.empty(vocab_size, old.embedding_dim, dtype=torch.float32)
        nn.init.normal_(weight, mean=0, std=model.config.init_std)
        weight[pad].zero_()
    new.weight = nn.Parameter(weight.to(old.weight.device), requires_grad=True)
    encoder.embed_tokens = new
    assert new.weight.data_ptr() != model.get_decoder().embed_tokens.weight.data_ptr()
    assert model.get_output_embeddings().weight.shape[0] == model.config.vocab_size
    assert [n for n,p in model.named_parameters() if p.requires_grad] == ["model.encoder.embed_tokens.weight"]
    return model


def load_base(model_id, revision, seed, source_size, source=None, target=None, initialization='random'):
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id, revision=revision,
        torch_dtype=torch.float32, attn_implementation="eager")
    install_source_embedding(model, source_size, seed)
    if initialization == 'warm_start':
        if source is None or target is None: raise ValueError('Warm start requires both tokenizers')
        warm_start(model, source, target)
    elif initialization != 'random': raise ValueError('Unknown initialization method')
    return model


@torch.no_grad()
def warm_start(model, source, target):
    """Same pretrained-subtoken mean recipe for both source vocabularies."""
    source_weight = model.get_encoder().embed_tokens.weight
    native_weight = model.get_decoder().embed_tokens.weight
    controls = {'<pad>':target.pad_token_id,'<unk>':target.unk_token_id,
                '<s>':target.bos_token_id,'</s>':target.eos_token_id}
    for i,token in enumerate(source.vocab_strings()):
        if token in controls:
            source_weight[i].copy_(native_weight[controls[token]])
        else:
            ids = target(token,add_special_tokens=False)['input_ids']
            if ids: source_weight[i].copy_(native_weight[ids].mean(dim=0))
    source_weight[source.pad].zero_()


def move(batch, device):
    return {k: v.to(device) for k,v in batch.items()}


def preflight(model, row, device):
    """One real backward/update/restore: catch frozen graphs and accidental tying."""
    model.eval()
    source = model.get_encoder().embed_tokens.weight
    original = source.detach().clone()
    decoder = model.get_decoder().embed_tokens.weight
    probe = decoder[:8].detach().clone()
    out = model(**move(collate([row]), device), use_cache=False)
    assert torch.isfinite(out.loss), "Non-finite forward loss"
    out.loss.backward()
    assert source.grad is not None and torch.isfinite(source.grad).all()
    assert source.grad.abs().sum() > 0, "No source embedding gradient"
    assert all(p.grad is None for p in model.parameters() if not p.requires_grad)
    with torch.no_grad():
        source.add_(source.grad, alpha=-0.01)
        assert not torch.equal(source, original)
        assert torch.equal(decoder[:8], probe)
        source.copy_(original)
    model.zero_grad(set_to_none=True)
    return float(out.loss.detach())


def amp_context(device):
    return torch.autocast(device_type=device.type, dtype=torch.float16, enabled=device.type=="cuda")


@torch.no_grad()
def validation_loss(model, data, device):
    model.eval(); total, tokens = 0., 0
    for batch in DataLoader(data, batch_size=1, collate_fn=collate):
        n = int(batch["labels"].ne(-100).sum())
        with amp_context(device):
            loss = model(**move(batch, device), use_cache=False).loss
        if not torch.isfinite(loss):
            raise RuntimeError("Non-finite validation loss")
        total += float(loss)*n; tokens += n
    return total/tokens


def train(model, data, cfg, identity, output, device, resume=False):
    """Epoch-boundary resume; checkpoint contains only trainable weights and optimizer."""
    from safetensors.torch import save_file, load_file
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    optimizer = torch.optim.AdamW([model.get_encoder().embed_tokens.weight], lr=cfg["lr"], weight_decay=0.)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type=="cuda")
    checkpoint = output/"last.pt"
    history, start, best = [], 0, float("inf")
    if resume:
        if not checkpoint.exists():
            raise FileNotFoundError("No epoch checkpoint to resume.")
        saved = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if saved["identity"] != identity or saved["cfg"] != cfg:
            raise ValueError("Resume configuration/data/tokenizer/base mismatch. Start a new run.")
        model.get_encoder().embed_tokens.weight.data.copy_(saved["source_weight"].to(device))
        optimizer.load_state_dict(saved["optimizer"]); scaler.load_state_dict(saved["scaler"])
        start, best, history = saved["next_epoch"], saved["best"], saved["history"]
    elif checkpoint.exists() or (output/"best_source.safetensors").exists():
        raise FileExistsError("Existing run: set RESUME=True or use a new output directory.")
    for epoch in range(start, cfg["epochs"]):
        # Epoch-specific seed makes restarting from an epoch boundary reproducible.
        torch.manual_seed(cfg["seed"]+epoch); random.seed(cfg["seed"]+epoch)
        if device.type=="cuda": torch.cuda.manual_seed_all(cfg["seed"]+epoch)
        gen = torch.Generator().manual_seed(cfg["seed"]+epoch)
        loader = DataLoader(data["train"], batch_size=cfg["batch_size"], shuffle=True,
                            generator=gen, collate_fn=collate)
        model.train(); optimizer.zero_grad(set_to_none=True)
        loss_sum, tokens, window_tokens = 0., 0, 0
        for step, batch in enumerate(loader):
            n = int(batch["labels"].ne(-100).sum()); window_tokens += n
            with amp_context(device):
                loss = model(**move(batch, device), use_cache=False).loss
            if not torch.isfinite(loss): raise RuntimeError("Non-finite loss; try fp32 and inspect data.")
            # Sum token losses; normalize gradients by exact token count at update time.
            scaler.scale(loss*n).backward()
            loss_sum += float(loss.detach())*n; tokens += n
            if (step+1) % cfg["accumulation"] == 0 or step+1 == len(loader):
                scaler.unscale_(optimizer)
                for p in model.parameters():
                    if p.grad is not None: p.grad.div_(window_tokens)
                torch.nn.utils.clip_grad_norm_([model.get_encoder().embed_tokens.weight], 1.)
                scaler.step(optimizer); scaler.update(); optimizer.zero_grad(set_to_none=True)
                window_tokens = 0
            if (step+1) % 100 == 0: print(f"epoch {epoch+1}, batch {step+1}/{len(loader)}, loss={loss_sum/tokens:.4f}")
        val = validation_loss(model, data["validation"], device)
        history.append({"epoch": epoch+1, "train_loss": loss_sum/tokens, "validation_loss": val})
        print(history[-1])
        if val < best:
            best = val
            save_file({"weight": model.get_encoder().embed_tokens.weight.detach().cpu().contiguous()}, str(output/"best_source.safetensors"))
        state = {"source_weight": model.get_encoder().embed_tokens.weight.detach().cpu(),
                 "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                 "next_epoch": epoch+1, "best": best, "history": history, "cfg": cfg, "identity": identity}
        torch.save(state, output/"last.tmp.pt")
        (output/"last.tmp.pt").replace(checkpoint)
        save_json(output/"history.json", history)
    model.get_encoder().embed_tokens.weight.data.copy_(load_file(str(output/"best_source.safetensors"))["weight"].to(device))
    return history


@torch.no_grad()
def predict(model, source, target, rows, device, max_new_tokens=128, beams=4):
    model.eval()
    lang = target.convert_tokens_to_ids("tgl_Latn")
    if lang == target.unk_token_id: raise ValueError("Missing target language tag")
    predictions = []
    for row in rows:
        ids = torch.tensor([source.encode(row["source"])], device=device)
        with amp_context(device):
            result = model.generate(input_ids=ids, attention_mask=ids.ne(source.pad).long(),
                forced_bos_token_id=lang, max_new_tokens=max_new_tokens,
                num_beams=beams, do_sample=False, use_cache=True)
        predictions.append(target.decode(result[0], skip_special_tokens=True))
    return predictions


def score_and_export(rows, predictions, output):
    from sacrebleu.metrics import BLEU, CHRF
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    refs = [r["target"] for r in rows]
    metrics = {}
    for name, metric in [("BLEU", BLEU(tokenize="13a")), ("chrF++", CHRF(word_order=2))]:
        metrics[name] = {"score": metric.corpus_score(predictions, [refs]).score,
                         "signature": str(metric.get_signature())}
    save_json(output/"metrics.json", metrics)
    (output/"predictions.jsonl").write_text("".join(json.dumps({**r, "prediction": p}, ensure_ascii=False)+"\n" for r,p in zip(rows,predictions)), encoding="utf-8")
    for name, lines in [("hypotheses.txt", predictions), ("references.txt", refs)]:
        (output/name).write_text("\n".join(lines)+"\n", encoding="utf-8")
    return metrics


def load_bundle(path, device="cpu"):
    """Use this loader instead of AutoModel.from_pretrained on the adapter folder."""
    from safetensors.torch import load_file
    path = Path(path); info = json.loads((path/"manifest.json").read_text(encoding="utf-8"))
    project = info.get('source_format') == 'kapampangan_project'
    source_path = path/'source_artifact' if project else path/'source_tokenizer.json'
    checksum_path = source_path/'tokenizer.json' if project else source_path
    if digest(checksum_path) != info["identity"]["tokenizer_sha256"]:
        raise ValueError("Tokenizer checksum mismatch")
    if project:
        import sys
        runtime_root = str(path/'runtime')
        if runtime_root not in sys.path: sys.path.insert(0,runtime_root)
    source = SourceTokenizer(source_path, info["source_vocab_size"])
    model = load_base(info["model_id"], info["revision"], info["cfg"]["seed"], source.size)
    model.get_encoder().embed_tokens.weight.data.copy_(load_file(str(path/"best_source.safetensors"))["weight"])
    target = AutoTokenizer.from_pretrained(path/"target_tokenizer", src_lang="tgl_Latn", tgt_lang="tgl_Latn")
    return model.to(device).eval(), source, target
