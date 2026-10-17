"""Tokenizer catalog and tracing tests using tiny real-format portable artifacts."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

BACKEND = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND / 'tokenizer'))
import tokenizer_variants
import trace_service


def _write_json(path, document):
    path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')


def _artifact(path, merged):
    path.mkdir(parents=True)
    vocabulary = [dict(id=i, token=t, kind='special' if i < 4 else 'character')
                  for i, t in enumerate(['<pad>', '<unk>', '<s>', '</s>', 'a', 'b', ' '])]
    rules = []
    if merged:
        vocabulary.append(dict(id=7, token='ab', kind='merge'))
        rules.append(dict(rank=0, left='a', right='b', result='ab', result_id=7))
    specials = [dict(role=role, token=token, id=i)
                for i, (role, token) in enumerate([('pad', '<pad>'), ('unk', '<unk>'), ('bos', '<s>'), ('eos', '</s>')])]
    _write_json(path / 'tokenizer.json', dict(schema_version='1.0.0', artifact_type='kapampangan_morphbpe',
        normalization=dict(unicode_normalization='NFC', spelling_mappings=[]),
        vocabulary=vocabulary, merges=rules, special_tokens=specials))
    _write_json(path / 'tokenizer-manifest.json', dict(schema_version='1.0.0'))
    lines = [hashlib.sha256(file.read_bytes()).hexdigest() + '  ' + file.name
             for file in sorted(path.iterdir())]
    (path / 'checksums.sha256').write_text('\n'.join(lines) + '\n', encoding='utf-8')


class TokenizerVariantTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        runtime_source = BACKEND / 'tokenizer' / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
        runtime_target = self.root / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
        runtime_target.parent.mkdir()
        shutil.copyfile(runtime_source, runtime_target)
        _artifact(self.root / 'artifacts' / 'plain-bpe', False)
        _artifact(self.root / 'artifacts' / 'morphbpe-penalty32', True)
        self.pack = self.root / 'variants' / 'infix_first_penalty48'
        _artifact(self.pack / 'source_artifact', False)
        packed_runtime = self.pack / 'runtime' / 'kapampangan_morphbpe_runtime' / 'tokenizer.py'
        packed_runtime.parent.mkdir(parents=True)
        shutil.copyfile(runtime_source, packed_runtime)
        self.info = dict(label='Infix-first penalty 48', tokenizer_variant='infix_first_penalty48',
                         source_vocab_size=7,
                         runtime_sha256=hashlib.sha256(packed_runtime.read_bytes()).hexdigest(),
                         tokenizer_sha256=hashlib.sha256((self.pack / 'source_artifact' / 'tokenizer.json').read_bytes()).hexdigest(),
                         artifact_manifest_sha256=hashlib.sha256((self.pack / 'source_artifact' / 'tokenizer-manifest.json').read_bytes()).hexdigest())
        _write_json(self.pack / 'package_info.json', self.info)
        self.patcher = patch.object(tokenizer_variants, 'TOKENIZER_ROOT', self.root)
        self.patcher.start()
        self.environment = patch.dict(os.environ, {'KAPAMPANGAN_MODEL_DIR': str(self.root / 'models')})
        self.environment.start()
        tokenizer_variants._tokenizer.cache_clear()
        tokenizer_variants._runtime.cache_clear()

    def tearDown(self):
        self.patcher.stop()
        self.environment.stop()
        tokenizer_variants._tokenizer.cache_clear()
        tokenizer_variants._runtime.cache_clear()
        self.temp.cleanup()

    def test_catalog_distinguishes_tokenizer_only_and_declares_default(self):
        result = tokenizer_variants.catalog()
        self.assertEqual(result['default_tokenizer'], 'morphbpe-penalty32')
        self.assertEqual([r['id'] for r in result['tokenizers']],
                         ['plain-bpe', 'morphbpe-penalty32', 'variant:infix_first_penalty48'])
        self.assertTrue(all(r['source'] == 'tokenizer' for r in result['tokenizers']))
        self.assertEqual(result['unavailable'], [])

    def test_switching_uses_selected_merges_and_isolated_runtime(self):
        default = trace_service.analyze('abab')
        variant = trace_service.analyze('abab', 'variant:infix_first_penalty48')
        again = trace_service.analyze('abab')
        self.assertEqual([t['token'] for t in default['all_tokens']], ['ab', 'ab'])
        self.assertEqual([t['token'] for t in variant['all_tokens']], ['a', 'b', 'a', 'b'])
        self.assertEqual(default, again)
        left, _, _ = tokenizer_variants.load('morphbpe-penalty32')
        right, _, _ = tokenizer_variants.load('variant:infix_first_penalty48')
        self.assertNotEqual(type(left).__module__, type(right).__module__)
        self.assertEqual(default['words'][0]['steps'][-1]['units_after'], ['ab', 'ab'])

    def test_rejects_unknown_path_traversal_and_invalid_types(self):
        for identifier in ['missing', 'trained:../morph_bpe', 'variant:../pack', '', 123]:
            with self.subTest(identifier=identifier), self.assertRaises(ValueError):
                trace_service.analyze('ab', identifier)

    def test_corrupt_runtime_is_excluded_and_explicit_selection_rejected(self):
        self.info['runtime_sha256'] = '0' * 64
        _write_json(self.pack / 'package_info.json', self.info)
        result = tokenizer_variants.catalog()
        self.assertEqual(len(result['tokenizers']), 2)
        self.assertEqual(result['unavailable'][0]['id'], 'variant:infix_first_penalty48')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            tokenizer_variants.load('variant:infix_first_penalty48')

    def test_cached_artifact_does_not_hide_corruption(self):
        tokenizer_variants.load('variant:infix_first_penalty48')
        with (self.pack / 'source_artifact' / 'tokenizer-manifest.json').open('a', encoding='utf-8') as stream:
            stream.write(' ')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            tokenizer_variants.load('variant:infix_first_penalty48')

    def test_gold_is_user_supplied_and_unknown_offsets_are_preserved(self):
        self.assertIsNone(trace_service.analyze('abab')['gold'])
        result = trace_service.analyze('ab|ab')
        self.assertEqual(result['gold']['boundary_f1'], 1.0)
        unknown = trace_service.analyze('az')
        self.assertEqual([(t['token'], t['start'], t['end']) for t in unknown['all_tokens']],
                         [('a', 0, 1), ('<unk>', 1, 2)])
        self.assertIsNone(trace_service.analyze('a|z')['gold'])
        self.assertIn('does not align losslessly', trace_service.analyze('a|z')['gold_unavailable_reason'])

    def test_empty_request_still_validates_selection(self):
        result = trace_service.analyze(' ', 'plain-bpe')
        self.assertEqual(result['tokenizer']['id'], 'plain-bpe')
        self.assertEqual(result['all_tokens'], [])
        with self.assertRaises(ValueError):
            trace_service.analyze('', 'missing')

    def test_public_package_validation_checks_declared_size(self):
        self.assertEqual(tokenizer_variants.validate_package(self.pack)['source_vocab_size'], 7)
        self.info['source_vocab_size'] = 8
        _write_json(self.pack / 'package_info.json', self.info)
        with self.assertRaisesRegex(ValueError, 'vocabulary size'):
            tokenizer_variants.validate_package(self.pack)

    def test_installer_preserves_artifact_bytes_and_refuses_collision(self):
        path = BACKEND.parent / 'install-tokenizer-variant.py'
        spec = importlib.util.spec_from_file_location('test_tokenizer_installer', path)
        installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(installer)
        artifact = self.root / 'artifacts' / 'morphbpe-penalty32'
        install_root = self.root / 'installation'
        destination = installer.install(artifact, 'candidate', 'Candidate', 'candidate',
                                        self.root / 'kapampangan_morphbpe_runtime', root=install_root)
        before = {file.name: file.read_bytes() for file in artifact.iterdir()}
        self.assertEqual(before, {file.name: file.read_bytes() for file in (destination / 'source_artifact').iterdir()})
        with self.assertRaises(FileExistsError):
            installer.install(artifact, 'candidate', 'Candidate', 'candidate',
                              self.root / 'kapampangan_morphbpe_runtime', root=install_root)
        self.assertEqual(before, {file.name: file.read_bytes() for file in (destination / 'source_artifact').iterdir()})


if __name__ == '__main__':
    unittest.main()
