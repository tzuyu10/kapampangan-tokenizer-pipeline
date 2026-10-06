"""Initial diagnostics; no model loading or translation quality claims."""
import hashlib
import json
import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINTS = Path(os.environ.get('KAPAMPANGAN_MODEL_DIR', str(ROOT / 'nllb' / 'checkpoints')))


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
                    validation_loss=best['validation_loss'], bleu=None, chrf_plus_plus=None,
                    quality_status='Not evaluated', source=str(history_path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'history.json',
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
            scope='Saved training diagnostics for installed bundles. Loss is not translation accuracy.',
            quality_note='BLEU and chrF++ require held-out predictions and references. No paired quality report is available for these installed bundles.'))
