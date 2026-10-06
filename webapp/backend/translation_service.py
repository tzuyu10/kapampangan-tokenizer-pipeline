"""Real translation from matched source-embedding bundles; lazy single-process loading."""
from functools import lru_cache
from collections import OrderedDict
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import threading
import time
import unicodedata

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BUNDLE_ROOT = Path(os.environ.get('KAPAMPANGAN_MODEL_DIR', str(REPOSITORY_ROOT/'nllb'/'checkpoints')))
_LOCK = threading.Lock()
_CACHE = {}
_SHARED = {}
_EMBEDDINGS = {}
_RESULTS = OrderedDict()
_RESULT_LIMIT = 128


def _normalize_source(text):
    return ' '.join(unicodedata.normalize('NFC', text).split())

@lru_cache(maxsize=2)
def _target_signature(condition):
    path, _ = _bundle(condition)
    digest = hashlib.sha256()
    for f in sorted((path/'target_tokenizer').rglob('*')):
        if f.is_file():
            digest.update(f.relative_to(path).as_posix().encode())
            digest.update(f.read_bytes())
    return digest.hexdigest()

@lru_cache(maxsize=1)
def comparison_audit():
    paths, manifests = zip(*(_bundle(c) for c in ('plain_bpe', 'morph_bpe')))
    errors, warnings = [], []
    for field in ('model_id','revision','source_vocab_size','source_format','source_id_mapping','adaptation','target_language','source_marker'):
        if manifests[0].get(field) != manifests[1].get(field): errors.append('Different '+field)
    for field in ('data_sha256','data_hashes','data_policy','excluded_train_ids','initialization','source_limit','target_limit','max_new_tokens','beams','helper_sha256','runtime_sha256'):
        if manifests[0]['identity'].get(field) != manifests[1]['identity'].get(field): errors.append('Different identity.'+field)
    for field in set(manifests[0]['cfg']) | set(manifests[1]['cfg']):
        if manifests[0]['cfg'].get(field) != manifests[1]['cfg'].get(field):
            (warnings if field == 'epochs' else errors).append('Different cfg.'+field)
    artifacts=[json.loads((p/'source_artifact/tokenizer-manifest.json').read_text()) for p in paths]
    for field in ('normalization.json','pretokenizer.json','special_tokens.json'):
        if artifacts[0]['core_file_sha256'][field] != artifacts[1]['core_file_sha256'][field]: errors.append('Different '+field)
    if artifacts[0]['metadata'].get('prepared_manifest_fingerprint') != artifacts[1]['metadata'].get('prepared_manifest_fingerprint'): errors.append('Different tokenizer training stream')
    if _target_signature('plain_bpe') != _target_signature('morph_bpe'): errors.append('Different target tokenizer')
    splits=[p/'split_manifest.json' for p in paths]
    if all(p.exists() for p in splits) and json.loads(splits[0].read_text()) != json.loads(splits[1].read_text()):
        errors.append('Different saved split memberships')

    if not artifacts[1]['metadata'].get('weighted_penalty_used'):
        warnings.append('Translation Morph-BPE uses hard constraints, not the crossing-penalty scoring proposed in the manuscript. A matching weighted translation checkpoint still requires training.')
    return dict(compatible=not errors,errors=errors,warnings=warnings)

@lru_cache(maxsize=2)
def _bundle(condition):
    path = BUNDLE_ROOT/condition
    manifest = json.loads((path/'manifest.json').read_text(encoding='utf-8'))
    if manifest['identity']['condition'] != condition:
        raise ValueError('Checkpoint condition does not match its folder')
    for relative,key in [('source_artifact/tokenizer.json','tokenizer_sha256'),
                         ('source_artifact/tokenizer-manifest.json','artifact_manifest_sha256'),
                         ('nllb_source_adapter.py','helper_sha256'),
                         ('runtime/kapampangan_morphbpe_runtime/tokenizer.py','runtime_sha256')]:
        if hashlib.sha256((path/relative).read_bytes()).hexdigest() != manifest['identity'][key]:
            raise ValueError('Bundle checksum mismatch: '+relative)
    if not (path/'best_source.safetensors').is_file():
        raise ValueError('Trained source weights missing')
    return path,manifest

def status():
    conditions = {}
    for key,condition,label in [('baseline','plain_bpe','Plain BPE + NLLB-200'),('custom','morph_bpe','Morph-BPE + NLLB-200')]:
        try:
            _bundle(condition)
            installed = True
        except (OSError,ValueError,KeyError):
            installed = False
        dependencies = all(importlib.util.find_spec(x) is not None for x in ('torch','transformers','tokenizers','safetensors','sentencepiece'))
        ready = installed and dependencies
        conditions[key] = dict(label=label, role='Baseline' if key=='baseline' else 'Proposed system',
            tokenizer=('Plain BPE' if key=='baseline' else 'Hard-constrained Morph-BPE')+' (6,080 source tokens)',
            model='NLLB-200 Distilled 600M with trained source embeddings',ready=ready,
            checkpoint_ready=installed, loaded=condition in _CACHE,
            reason='Checkpoint installed; first translation loads the base model.' if ready else
            ('Install translation dependencies and restart the backend.' if installed else 'Trained checkpoint not installed.'))
    available = any(c['ready'] for c in conditions.values())
    audit = None
    if all(c['checkpoint_ready'] for c in conditions.values()):
        try: audit = comparison_audit()
        except (OSError,ValueError,KeyError) as exc: audit = dict(compatible=False,errors=[str(exc)],warnings=[])

    return dict(conditions=conditions,can_translate=available,
        can_compare=all(c['ready'] for c in conditions.values()) and bool(audit and audit['compatible']),inference_api_ready=available,comparison_audit=audit,
        direction=dict(source='Kapampangan',target='Filipino',target_language_code='tgl_Latn'),
        message='Plain BPE is available. Morph-BPE requires its own trained bundle.' if conditions['baseline']['ready'] and not conditions['custom']['ready'] else 'Translation uses installed trained bundles; first use may download the base model.')

def translate(text, condition='plain_bpe'):
    if not isinstance(text,str) or not text.strip() or len(text)>500:
        raise ValueError('Enter between 1 and 500 characters of Kapampangan text.')
    if condition not in ('plain_bpe','morph_bpe'):
        raise ValueError('Unknown translation condition')
    text = _normalize_source(text)
    with _LOCK:
        key = (condition, text.strip())
        if key in _RESULTS:
            _RESULTS.move_to_end(key)
            return dict(_RESULTS[key], latency_ms=0, cache_hit=True)
        path,manifest = _bundle(condition)
        import torch
        if condition not in _CACHE:
            spec=importlib.util.spec_from_file_location('translation_adapter_'+condition,path/'nllb_source_adapter.py')
            helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
            device=torch.device(os.environ.get('KAPAMPANGAN_DEVICE','cuda' if torch.cuda.is_available() else 'cpu'))
            if device.type == 'cpu' and not _SHARED:
                threads=int(os.environ.get('KAPAMPANGAN_CPU_THREADS', str(min(4, os.cpu_count() or 1))))
                if threads < 1: raise ValueError('KAPAMPANGAN_CPU_THREADS must be positive')
                torch.set_num_threads(threads)
            # Share frozen NLLB weights; only the source embedding differs.
            shared_key=(manifest['model_id'],manifest['revision'],str(device),
                        _target_signature(condition), manifest['identity']['helper_sha256'])
            if shared_key in _SHARED:
                model,target=_SHARED[shared_key]
                source=helper.SourceTokenizer(path/'source_artifact',manifest['source_vocab_size'])
                from safetensors.torch import load_file
                embedding=copy.copy(model.get_encoder().embed_tokens)
                embedding._parameters=dict(embedding._parameters)
                weight=load_file(str(path/'best_source.safetensors'))['weight']
                if tuple(weight.shape)!=(source.size,model.config.d_model):
                    raise ValueError('Source embedding dimensions do not match the base model')
                embedding.weight=torch.nn.Parameter(weight.to(device),requires_grad=False)
            else:
                model,source,target=helper.load_bundle(path,device)
                model.requires_grad_(False)
                embedding=model.get_encoder().embed_tokens
                _SHARED[shared_key]=(model,target)
            _EMBEDDINGS[condition]=embedding
            _CACHE[condition]=(model,source,target,device)
        model,source,target,device=_CACHE[condition]
        model.get_encoder().embed_tokens=_EMBEDDINGS[condition]
        model.eval()
        ids=source.encode(text.strip())
        if len(ids)>manifest['identity']['source_limit']:
            raise ValueError('Text exceeds the trained source-token limit. Translate a shorter passage.')
        started=time.perf_counter()
        with torch.inference_mode():
            tensor=torch.tensor([ids],device=device)
            output=model.generate(input_ids=tensor,attention_mask=tensor.ne(source.pad).long(),
                forced_bos_token_id=target.convert_tokens_to_ids('tgl_Latn'),
                max_new_tokens=manifest['identity']['max_new_tokens'],
                num_beams=manifest['identity']['beams'],do_sample=False,use_cache=True)
        token_ids=output[0].tolist()
        result=dict(translation=target.decode(token_ids,skip_special_tokens=True),condition=condition,
            source_token_count=len(ids),output_token_count=sum(x not in target.all_special_ids for x in token_ids),
            latency_ms=round((time.perf_counter()-started)*1000), cache_hit=False)
        result['process'] = dict(
            tokenization=tokenize_adapted(text, condition),
            attention_mask=tensor.ne(source.pad).long()[0].tolist(),
            embedding_shape=list(model.get_encoder().embed_tokens.weight.shape),
            output_ids=token_ids, output_tokens=target.convert_ids_to_tokens(token_ids),
            beams=manifest['identity']['beams'], max_new_tokens=manifest['identity']['max_new_tokens'],
            target_language=manifest['target_language'], adaptation=manifest['adaptation'])
        _RESULTS[key]=dict(result)
        if len(_RESULTS)>_RESULT_LIMIT: _RESULTS.popitem(last=False)
        return result

def compare(text):
    readiness=status()
    if not readiness['can_translate']:
        raise ValueError('No trained translation bundle is available in this backend environment.')
    audit = readiness.get('comparison_audit')
    if audit and not audit['compatible']: raise ValueError('Unmatched translation controls: '+'; '.join(audit['errors']))
    result={}
    for key,condition in [('baseline','plain_bpe'),('custom','morph_bpe')]:
        if readiness['conditions'][key]['ready']:
            result[key]=translate(text,condition)
    return result


def tokenize_adapted(text, condition='plain_bpe'):
    if not isinstance(text, str) or not text.strip() or len(text)>500:
        raise ValueError('Enter between 1 and 500 characters.')
    if condition not in ('plain_bpe', 'morph_bpe'):
        raise ValueError('Unknown tokenizer condition')
    path,manifest = _bundle(condition)
    tokenizer=_native_tokenizer(condition)
    encoded=tokenizer.encode(_normalize_source(text))
    result=encoded.to_dict()
    result['condition']=condition
    result['model_source_ids']=[2]+[1 if x==0 else 0 if x==1 else x for x in encoded.ids]+[3]
    result['tokenizer_sha256']=manifest['identity']['tokenizer_sha256']
    return result


@lru_cache(maxsize=2)
def _native_tokenizer(condition):
    path,manifest=_bundle(condition)
    import sys
    spec=importlib.util.spec_from_file_location('adapted_runtime_'+condition,path/'runtime/kapampangan_morphbpe_runtime/tokenizer.py')
    runtime=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=runtime
    spec.loader.exec_module(runtime)
    tokenizer=runtime.Tokenizer(path/'source_artifact')
    return tokenizer
