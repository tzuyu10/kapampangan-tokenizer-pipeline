"""Saved diagnostics and checkpoint-matched evaluation; no model loading."""
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINTS = Path(os.environ.get('KAPAMPANGAN_MODEL_DIR', str(ROOT / 'nllb' / 'checkpoints')))
REPORTS = ROOT / 'reports' / 'translation' / 'paired_evaluation_v2'


@lru_cache(maxsize=64)
def _file_digest(path, size, modified):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(path):
    stat = path.stat()
    return _file_digest(str(path.resolve()), stat.st_size, stat.st_mtime_ns)


def quality_metrics(path, report_root=None):
    """Never attribute a previous checkpoint's scores to installed weights."""
    missing = dict(bleu=None, chrf_plus_plus=None, quality_status='Not evaluated')
    report_root = REPORTS if report_root is None else report_root
    try:
        manifest = json.loads((path / 'manifest.json').read_text(encoding='utf-8'))
        trained = manifest['identity']
        condition = trained['condition']
        report = report_root / condition
        if not (report / 'metrics.json').is_file():
            return missing
        proof = json.loads((report_root / 'verification.json').read_text(encoding='utf-8'))
        checked = proof['conditions'][condition]
        if checked['validation'] != 'passed':
            raise ValueError('Report verification has not passed.')
        for name in ('metrics.json', 'evaluation_identity.json', 'predictions.jsonl',
                     'hypotheses.txt', 'references.txt'):
            if digest(report / name) != proof['files'][f'{condition}/{name}']:
                raise ValueError('Saved evaluation files changed after verification.')
        identity = json.loads((report / 'evaluation_identity.json').read_text(encoding='utf-8'))
        metrics = json.loads((report / 'metrics.json').read_text(encoding='utf-8'))
        scope = metrics['scope']
        if (identity['condition'] != condition or identity['split'] != 'test'
                or identity['final_full_split'] is not True or scope['full_split'] is not True
                or scope['split'] != 'test' or checked['split'] != 'test'):
            raise ValueError('A complete test-split evaluation is required.')
        split_ids = json.loads((path / 'split_manifest.json').read_text(encoding='utf-8'))['test']
        row_hash = hashlib.sha256(json.dumps(split_ids, ensure_ascii=False).encode()).hexdigest()
        if (identity['row_ids_sha256'] != row_hash
                or identity['examples'] != len(split_ids) or scope['examples'] != len(split_ids)
                or scope['available_rows'] != len(split_ids) or checked['examples'] != len(split_ids)):
            raise ValueError('Evaluation rows differ from the installed test split.')
        expected = dict(data=trained['data_sha256'], base=manifest['revision'],
                        beams=trained['beams'], max_new_tokens=trained['max_new_tokens'],
                        source_limit=trained['source_limit'], seed=manifest['cfg']['seed'])
        for key, rel in [('weights', 'best_source.safetensors'),
                         ('tokenizer', 'source_artifact/tokenizer.json'),
                         ('runtime', 'runtime/kapampangan_morphbpe_runtime/tokenizer.py'),
                         ('target', 'target_tokenizer/tokenizer.json'),
                         ('helper', 'nllb_source_adapter.py')]:
            expected[key] = digest(path / rel)
        differences = [key for key, value in expected.items() if identity.get(key) != value]
        if differences:
            return dict(missing, quality_status='Checkpoint mismatch',
                        quality_reason='Saved evaluation belongs to a different checkpoint '
                        f"({', '.join(differences)}). Evaluate the installed model to obtain its scores.")
        scores = {}
        for name in ('BLEU', 'chrF++'):
            score = metrics[name]['score']
            if (isinstance(score, bool) or not isinstance(score, (int, float))
                    or not math.isfinite(score) or not 0 <= score <= 100
                    or score != checked['scores'][name]):
                raise ValueError('Invalid or unverified evaluation score.')
            scores[name] = score
        return dict(bleu=scores['BLEU'], chrf_plus_plus=scores['chrF++'],
                    quality_status='Evaluated', evaluation_split='test',
                    evaluation_examples=len(split_ids), evaluation_precision=identity['precision'],
                    evaluation_beams=identity['beams'],
                    evaluation_max_new_tokens=identity['max_new_tokens'],
                    metric_signatures={name: metrics[name]['signature'] for name in scores})
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return dict(missing, quality_status='Report unavailable',
                    quality_reason=f'Cannot verify saved evaluation: {exc}')


def training_metrics(path):
    manifest_path, history_path = path / 'manifest.json', path / 'history.json'
    if not manifest_path.is_file() or not history_path.is_file():
        return dict(available=False, reason='Install a bundle with manifest.json and history.json.')
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        history = json.loads(history_path.read_text(encoding='utf-8'))
        if not isinstance(history, list) or not history:
            raise ValueError('Training history is empty or invalid.')
        for row in history:
            for key in ('epoch', 'train_loss', 'validation_loss'):
                if not isinstance(row.get(key), (int, float)) or not math.isfinite(row[key]):
                    raise ValueError('Training history contains invalid metrics.')
        best = min(history, key=lambda row: row['validation_loss'])
        return dict(available=True, completed_epochs=max(row['epoch'] for row in history),
                    best_epoch=best['epoch'], train_loss=best['train_loss'],
                    validation_loss=best['validation_loss'], **quality_metrics(path),
                    source=str(history_path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'history.json',
                    tokenizer_sha256=manifest.get('identity', {}).get('tokenizer_sha256'),
                    data_sha256=manifest.get('identity', {}).get('data_sha256'))
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return dict(available=False, reason=f'Cannot read saved metrics: {exc}')


def initial_metrics():
    import comparison_service as comparison
    import reference_data as ref

    # Fixed project demonstration references, not a held-out evaluation corpus.
    sentences = ref.SENTENCES + [forms for _, _, forms in ref.FAMILIES]
    rows = []
    encoded = {name: [] for name in comparison.NAMES}
    for sentence in sentences:
        rows.extend(ref.rows_for(sentence))
        groups = comparison.groups_by_tokenizer(' '.join(word for word, _ in sentence))
        for name in comparison.NAMES:
            if len(groups[name]) != len(sentence):
                raise ValueError('Initial diagnostic word alignment failed.')
            encoded[name].extend(groups[name])
    artifacts = dict(zip(comparison.NAMES, ('morphbpe-penalty32', 'plain-bpe', 'unigram-lm-6080')))
    tokenizer_rows = []
    for name in comparison.NAMES:
        scores = ref.score(rows, encoded[name])
        file = comparison.ARTIFACTS / artifacts[name] / 'tokenizer.json'
        tokenizer_rows.append(dict(condition=name, artifact=artifacts[name],
            tokenizer_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
            fertility=sum(len(group) for group in encoded[name]) / len(rows),
            boundary_f1=scores['boundary_f1'], consistency_f1=scores['mcf1']))
    return dict(tokenizer=dict(rows=tokenizer_rows, word_occurrences=len(rows),
        unique_words=len({row['surface'] for row in rows}),
        source='webapp/backend/tokenizer/reference_data.py: SENTENCES + FAMILIES',
        scope='Fixed project demonstration references; not independent held-out gold.',
        references=[dict(word=word, segmentation=seg or word) for sentence in sentences for word, seg in sentence]),
        translation=dict(rows=[dict(condition=label, **training_metrics(CHECKPOINTS / condition))
            for condition, label in [('plain_bpe', 'Plain BPE'), ('morph_bpe', 'Morph-BPE')]],
            scope='Saved training diagnostics and verified test scores for installed bundles. Loss is not translation accuracy.',
            quality_note='BLEU and chrF++ are corpus scores from 0 to 100, comparing saved translations with Filipino references. Scores appear only when the evaluated checkpoint and test split match the installed model. They do not score the current input or establish statistical significance.'))
