"""Revise morphology annotations while preserving all selected words/text bytes."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import unicodedata
from urllib.parse import unquote, urlparse

REPO = Path(__file__).resolve().parents[2]
V1 = REPO / 'experiments/tagalog_augmentation_30_v1'
sys.path.insert(0, str(V1))
from train_tokenizer import verify_inputs
from build_package import prepare_stream
sys.path.insert(0, str(REPO / 'src'))
from kapampangan_morphbpe.serialization import fingerprint, write_json, sha256_file
from kapampangan_morphbpe.lexicon import load_lexicon


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--dictionary', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    old_manifest = verify_inputs(args.original)
    if args.output.exists():
        raise ValueError('Preserve existing runs; use a new output directory.')
    if sha256_file(args.dictionary) != old_manifest['sources']['tagalog_dictionary_sha256']:
        raise ValueError('Tagalog source dictionary changed.')
    shutil.copytree(args.original, args.output, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    root = args.output.resolve()
    lex = load_lexicon(root / 'lexicons/kapampangan-training-lexicon.json')
    selected = json.loads((root / 'lexicons/tagalog_roots.json').read_text(encoding='utf-8'))
    dictionary = json.loads(args.dictionary.read_text(encoding='utf-8'))
    shared = {}
    for index, row in enumerate(dictionary):
        word = unicodedata.normalize('NFC', row.get('word', '').strip()).lower()
        url = urlparse(row.get('link', ''))
        if (word in lex.roots and row.get('language') == 'Tagalog' and len(word) >= 4
                and re.fullmatch(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", word)
                and url.hostname == 'tagalog.pinoydictionary.com'
                and unquote(url.path.rstrip('/').split('/')[-1]).lower() == word
                and row.get('definition', '').strip()):
            shared.setdefault(word, dict(row, word=word, source_dictionary_row_index=index,
                inventory_role='reuse_existing_kapampangan_root_not_new_entry',
                review_status='source_matched_automatically_not_human_validated'))
    assert not set(shared) & {row['word'] for row in selected}
    assert set(shared) <= lex.roots
    write_json(root / 'lexicons/shared_tagalog_roots.json', [shared[word] for word in sorted(shared)])
    write_json(root / 'vendor/filipino_tokenizer/data/tagalog_roots.json',
               sorted([*selected, *shared.values()], key=lambda row: row['word']))
    shutil.copy2(Path(__file__).with_name('language_support.py'), root / 'language_support.py')
    sys.path.insert(0, str(root))
    sys.modules.pop('language_support', None)
    rows = [json.loads(line) for line in (root / 'data/tagalog_train.jsonl').read_text(encoding='utf-8').splitlines()]
    stats = prepare_stream(root, rows)
    for relative in ['data/train.csv', 'data/tagalog_train.csv', 'data/tagalog_train.jsonl',
                     'data/kapampangan_train.csv', 'lexicons/tagalog_roots.json',
                     'lexicons/kapampangan-training-lexicon.json',
                     'original/kapampangan-training-stream.jsonl', 'prepared/plain-training-stream.jsonl']:
        assert (root / relative).read_bytes() == (args.original / relative).read_bytes(), relative
    policy = dict(revision='shared_roots_hyphenated_prefix_v2',
        shared_root_count=len(shared), tagalog_recognizer_roots=len(shared) + len(selected),
        shared_roots_are_existing_entries=True, new_unique_root_count=len(selected),
        original_raw_text_and_selection_unchanged=True, original_kapampangan_annotations_unchanged=True,
        affix_inventory_and_infix_priority_unchanged=True, runtime_algorithm_unchanged=True,
        hyphen_policy='known prefix + explicit hyphen + dictionary-validated stem; preserve separator',
        supervision='automatic provisional morphology; no new independent human gold',
        prior_manifest_sha256=sha256_file(args.original / 'manifest.json'),
        shared_roots_sha256=sha256_file(root / 'lexicons/shared_tagalog_roots.json'),
        annotation_code_sha256=sha256_file(root / 'language_support.py'))
    manifest = dict(old_manifest, experiment='tagalog_augmentation_30_v2', prepared=stats,
                    annotation_revision=policy)
    manifest['payload_sha256'] = {name: sha256_file(root / name) for name in old_manifest['payload_sha256']}
    manifest['augmented_dataset_fingerprint'] = fingerprint(dict(
        base=old_manifest['augmented_dataset_fingerprint'], policy=policy,
        prepared_sha256=sha256_file(root / 'prepared/training-stream.jsonl'),
        roles_sha256=sha256_file(root / 'prepared/role-spans.jsonl')))
    write_json(root / 'manifest.json', manifest)
    shutil.copy2(Path(__file__), root / 'provenance/build_revision.py')
    (root / 'README.md').write_text(
        '# Revised Tagalog morphology preparation\n\n'
        'Raw records, the 993 additions, original Kapampangan roots and annotations are unchanged.\n'
        f'Tagalog recognition reuses {len(shared)} existing roots with source-matched Tagalog entries.\n'
        'Recognized prefix-hyphen-stem forms preserve the hyphen as a separate span.\n'
        'No new corpus text, unique roots, translations, runtime rules or priority budgets were added.\n'
        'Annotations are provisional automatic analyses, not independently reviewed linguistic gold.\n', encoding='utf-8')
    write_json(root / 'verification.json', dict(status='passed', preserved_payloads=True,
        combined_root_entries=4304, combined_records=34148, shared_roots_reused=len(shared)))
    inventory = {p.relative_to(root).as_posix(): sha256_file(p) for p in sorted(root.rglob('*'))
                 if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p.name != 'checksums.json'}
    write_json(root / 'checksums.json', inventory)
    verify_inputs(root)
    print(json.dumps(dict(counts=manifest['counts'], policy=policy, prepared=stats,
                         dataset_fingerprint=manifest['augmented_dataset_fingerprint']), indent=2))


if __name__ == '__main__':
    main()
