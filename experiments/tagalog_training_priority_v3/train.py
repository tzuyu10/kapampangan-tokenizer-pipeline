"""Train infix -> other affix -> weighted BPE, with unchanged global inference."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import time

REPO = Path(__file__).resolve().parents[2]
AFFIX_KINDS = frozenset({'prefix', 'suffix', 'circumfix_prefix', 'circumfix_suffix'})


def pam_affixes(analyzer, surface, boundaries):
    analysis = analyzer.segment(surface)
    if analysis.status != 'accepted' or analysis.protected_boundaries != boundaries:
        return set()
    spans, offset = set(), 0
    for piece, unit in zip(analysis.segments, analysis.underlying_units, strict=True):
        end = offset + len(piece)
        if unit.kind in AFFIX_KINDS:
            spans.add((offset, end, 'affix'))
        offset = end
    return spans


def combine_roles(infixes, supported_affixes):
    """Shared surface/boundary keys retain only jointly supported affix roles."""
    affixes = set.intersection(*supported_affixes) if supported_affixes else set()
    affixes = {span for span in affixes if not any(
        span[0] < infix[1] and infix[0] < span[1] for infix in infixes)}
    result = sorted([*infixes, *affixes])
    assert all(left[1] <= right[0] for left, right in zip(result, result[1:]))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    package, output = args.inputs.resolve(), args.output.resolve()
    if (output / 'vocab_grid').exists():
        raise ValueError('Preserve existing training outputs.')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'reports').mkdir(exist_ok=True)
    sys.path[:0] = [str(package), str(package / 'source'), str(REPO / 'experiments/tagalog_augmentation_30_v1')]
    from train_tokenizer import verify_inputs, set_augmented_identity
    from language_support import surface_analysis, tagalog_segmenter
    from expanded_morphology import ExpandedMorphologicalSegmenter
    from kapampangan_morphbpe.lexicon import load_lexicon
    from kapampangan_morphbpe.prepare import load_prepared_stream
    from kapampangan_morphbpe.root_priority_bpe import RoleSpan, RootPriorityMorphBPETrainer
    from kapampangan_morphbpe.artifact import export_tokenizer_artifact, validate_artifact_files
    from kapampangan_morphbpe.serialization import write_json, sha256_file, fingerprint

    manifest = verify_inputs(package)
    started = time.monotonic()
    read_lines = lambda path: [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    key = lambda row: (row['surface'], tuple(row['protected_boundaries']), row['kind'])
    pam_keys = {key(row) for row in read_lines(package / 'original/kapampangan-training-stream.jsonl')}
    tag_keys = {key(row) for row in read_lines(package / 'prepared/tagalog-training-stream.jsonl')}
    prepared = load_prepared_stream(package / 'prepared/training-stream.jsonl')
    old_roles = read_lines(package / 'prepared/role-spans.jsonl')
    pam = ExpandedMorphologicalSegmenter(load_lexicon(package / 'lexicons/kapampangan-training-lexicon.json'))
    tag = tagalog_segmenter(package)
    roles, frequencies, type_counts, word_counts = [], Counter(), Counter(), Counter()
    for item, infix_list in zip(prepared, old_roles, strict=True):
        infixes = {tuple(span) for span in infix_list}
        sources = []
        k = item.surface, item.protected_boundaries, item.kind
        if item.kind == 'word':
            if k in pam_keys:
                sources.append(pam_affixes(pam, item.surface, item.protected_boundaries))
            if k in tag_keys:
                boundaries, spans, _status = surface_analysis(tag, item.surface)
                assert boundaries == item.protected_boundaries
                sources.append({tuple(span) for span in spans if span[2] == 'affix'})
        spans = combine_roles(infixes, sources)
        assert {span for span in spans if span[2] == 'infix'} == infixes
        roles.append([RoleSpan(*span) for span in spans])
        for start, end, role in spans:
            type_counts[role] += 1
            word_counts[role] += item.frequency
            if role == 'affix':
                frequencies[item.surface[start:end]] += item.frequency
    role_path = output / 'training-role-spans.jsonl'
    with role_path.open('w', encoding='utf-8', newline='\n') as stream:
        for spans in roles:
            stream.write(json.dumps([[s.start, s.end, s.role] for s in spans], separators=(',', ':')) + '\n')
    audit = dict(prepared_sequences=len(prepared), source_manifest_sha256=sha256_file(package / 'manifest.json'),
        training_stream_sha256=sha256_file(package / 'prepared/training-stream.jsonl'),
        roles_sha256=sha256_file(role_path), role_span_types=dict(type_counts),
        role_span_occurrences=dict(word_counts), other_affix_surface_frequencies=dict(sorted(frequencies.items())),
        infix_roles_unchanged=True, shared_role_policy='intersection across source-language analyses of shared surface/boundary keys',
        boundaries_corpus_and_lexicons_unchanged=True, labels='provisional training-analyzer roles, not independent gold')
    write_json(output / 'reports/role-audit.json', audit)
    print('Roles ready:', json.dumps(dict(types=dict(type_counts), occurrences=dict(word_counts))), flush=True)
    policy = dict(condition='infix_affix_first48', crossing_penalty=48, vocabulary_sizes=[6080, 8192],
        priority_order=['infix', 'affix', 'weighted'], infix_token_budget=32,
        affix_token_budget=256, root_token_budget=0, budgets_frozen_before_dev=True,
        runtime='unchanged ordinary global BPE', runtime_morphology=False,
        runtime_sha256=sha256_file(package / 'runtime/kapampangan_morphbpe_runtime/tokenizer.py'),
        dataset_fingerprint=manifest['augmented_dataset_fingerprint'], training_roles_sha256=sha256_file(role_path),
        trainer_source_sha256=sha256_file(package / 'source/kapampangan_morphbpe/root_priority_bpe.py'),
        source_manifest_sha256=sha256_file(package / 'manifest.json'))
    write_json(output / 'experiment.json', {**policy, 'experiment_fingerprint': fingerprint(policy)})
    trainer = RootPriorityMorphBPETrainer(prepared, 48, roles, root_token_budget=0,
        affix_token_budget=256, infix_token_budget=32, priority_order=('infix', 'affix'))
    models, report = trainer.train([6080, 8192])
    assert set(models) == {6080, 8192}
    for size in [6080, 8192]:
        target = output / f'vocab_grid/infix_affix_first48/vocab-{size}'
        metadata = dict(condition='infix_affix_first48', candidate=True, selection_performed=False,
            held_out_test_used=False, lexicon_used_at_runtime=False, training_roles_used_at_runtime=False,
            vocabulary_budget=size, crossing_penalty=48,
            training_stream_sha256=audit['training_stream_sha256'],
            augmentation_manifest_sha256=policy['source_manifest_sha256'],
            training_roles_sha256=policy['training_roles_sha256'],
            augmented_dataset_fingerprint=manifest['augmented_dataset_fingerprint'],
            training_runtime_policy=policy, full_grid_training_report=report,
            training_report_scope='shared trajectory through8192, snapshot at declared size', neural_model_training=False)
        export_tokenizer_artifact(models[size], target, metadata=metadata)
        set_augmented_identity(target, manifest['augmented_dataset_fingerprint'])
        assert validate_artifact_files(target)['checksums_match']
    write_json(output / 'reports/training-summary.json', dict(status='completed', vocabulary_sizes=[6080, 8192],
        elapsed_seconds=time.monotonic() - started, training_report=report, neural_training=False,
        runtime_morphology=False, portable_runtime_sha256=policy['runtime_sha256']))
    print('Both training-only variants completed.', flush=True)


if __name__ == '__main__':
    main()
