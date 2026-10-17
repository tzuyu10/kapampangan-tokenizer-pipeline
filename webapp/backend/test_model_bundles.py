"""Startup bundle selection checks without loading NLLB or downloading files."""
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import model_bundles


RUNTIME = '''import json
from pathlib import Path
class Tokenizer:
    def __init__(self, artifact_dir):
        document = json.loads((Path(artifact_dir) / 'tokenizer.json').read_text())
        self.id_to_token = [entry['token'] for entry in document['vocabulary']]
        self.token_to_id = {token: index for index, token in enumerate(self.id_to_token)}
        self.vocabulary_size = len(self.id_to_token)
        self.special_by_role = {entry['role']: (entry['token'], entry['id'])
                                for entry in document['special_tokens']}
'''


def write_json(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_weights(path, shape=(4, 1024), dtype='F32', offsets=None):
    payload = bytes(shape[0] * shape[1] * 4)
    header = json.dumps({'weight': dict(dtype=dtype, shape=list(shape),
                                      data_offsets=offsets or [0, len(payload)])}).encode()
    header += b' ' * ((8 - len(header) % 8) % 8)
    path.write_bytes(struct.pack('<Q', len(header)) + header + payload)


def make_bundle(root, name, condition='morph_bpe', variant='infix_first_penalty48'):
    path = root / name
    artifact = path / 'source_artifact'
    artifact.mkdir(parents=True)
    tokens = [dict(id=index, kind='special', token=token)
              for index, token in enumerate(('<pad>', '<unk>', '<s>', '</s>'))]
    specials = [dict(role=role, token=entry['token'], id=entry['id'])
                for role, entry in zip(('pad', 'unk', 'bos', 'eos'), tokens)]
    normalization = dict(unicode_normalization='NFC', spelling_mappings=[])
    artifact_type = ('kapampangan_plain_bpe' if condition == 'plain_bpe'
                     else 'kapampangan_morphbpe')
    write_json(artifact / 'tokenizer.json', dict(schema_version='1.0.0',
        artifact_type=artifact_type, vocabulary=tokens, merges=[],
        special_tokens=specials, normalization=normalization))
    write_json(artifact / 'vocab.json', dict(schema_version='1.0.0', tokens=tokens,
        actual_vocabulary_size=4, target_vocabulary_size=4))
    write_json(artifact / 'merges.json', dict(schema_version='1.0.0', merges=[], merge_count=0))
    write_json(artifact / 'special_tokens.json', dict(schema_version='1.0.0', special_tokens=specials))
    write_json(artifact / 'normalization.json', normalization)
    write_json(artifact / 'pretokenizer.json', dict(type='unicode'))
    core = {file.name: digest(file) for file in artifact.iterdir()}
    write_json(artifact / 'tokenizer-manifest.json', dict(schema_version='1.0.0',
        actual_vocabulary_size=4, target_vocabulary_size=4, merge_count=0,
        special_token_count=4, artifact_type=artifact_type, core_file_sha256=core))
    (artifact / 'TOKENIZER_CARD.md').write_text('Tiny regression fixture.', encoding='utf-8')
    inventory = {file.name: digest(file) for file in artifact.iterdir()}
    (artifact / 'checksums.sha256').write_text(''.join(
        f'{value}  {name}\n' for name, value in sorted(inventory.items())), encoding='utf-8')
    runtime = path / 'runtime' / 'kapampangan_morphbpe_runtime'
    runtime.mkdir(parents=True)
    (runtime / 'tokenizer.py').write_text(RUNTIME, encoding='utf-8')
    (runtime / '__init__.py').write_text('from .tokenizer import Tokenizer\n', encoding='utf-8')
    (path / 'nllb_source_adapter.py').write_text('# Regression helper fixture.\n', encoding='utf-8')
    write_json(path / 'target_tokenizer' / 'tokenizer.json', dict(model=dict(type='BPE')))
    write_json(path / 'target_tokenizer' / 'tokenizer_config.json', dict(tokenizer_class='NllbTokenizerFast'))
    write_json(path / 'history.json', [dict(epoch=1, train_loss=1.7, validation_loss=1.5),
        dict(epoch=2, train_loss=1.4, validation_loss=1.2)])
    write_json(path / 'split_manifest.json', dict(test=['heldout']))
    write_weights(path / 'best_source.safetensors')
    identity = dict(condition=condition, source_limit=256, target_limit=128,
        max_new_tokens=160, beams=4, data_sha256='fixture-dataset',
        tokenizer_sha256=digest(artifact / 'tokenizer.json'),
        artifact_manifest_sha256=digest(artifact / 'tokenizer-manifest.json'),
        helper_sha256=digest(path / 'nllb_source_adapter.py'),
        runtime_sha256=digest(runtime / 'tokenizer.py'),
        model_id='facebook/nllb-200-distilled-600M', revision='fixture-revision',
        tokenizer_variant=variant, crossing_penalty=48)
    manifest = dict(identity=identity, model_id=identity['model_id'], revision=identity['revision'],
        source_vocab_size=4, source_format='kapampangan_project', source_id_mapping='swap_0_1',
        adaptation='source_embedding_only', target_language='tgl_Latn',
        tokenizer_variant=variant, crossing_penalty=48, weighted_penalty_used=True,
        training_status='completed', completed_epochs=2, selected_epoch=2, cfg=dict(seed=42))
    write_json(path / 'manifest.json', manifest)
    return path, manifest


class BundleFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        env = dict(os.environ)
        env.pop('KAPAMPANGAN_PLAIN_BUNDLE', None)
        env.pop('KAPAMPANGAN_MORPH_BUNDLE', None)
        env['KAPAMPANGAN_MODEL_DIR'] = str(self.root)
        self.environment = patch.dict(os.environ, env, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)


class BundleSelectionTests(BundleFixture):
    def test_defaults_and_selected_folder_alias_keep_condition_slots(self):
        self.assertEqual(model_bundles.resolve_bundle_path('plain_bpe'), self.root / 'plain_bpe')
        self.assertEqual(model_bundles.resolve_bundle_path('morph_bpe'), self.root / 'morph_bpe')
        os.environ['KAPAMPANGAN_MORPH_BUNDLE'] = 'infix48_seed42'
        self.assertEqual(model_bundles.resolve_bundle_path('morph_bpe'), self.root / 'infix48_seed42')
        self.assertEqual(model_bundles.resolve_bundle_path('plain_bpe'), self.root / 'plain_bpe')

    def test_unknown_condition_and_unsafe_names_are_rejected(self):
        with self.assertRaises(ValueError):
            model_bundles.resolve_bundle_path('different-model')
        for name in ('.', '..', '../other', 'nested/model', r'nested\model',
                     r'C:\outside', '/outside', 'model:stream'):
            with self.subTest(name=name):
                os.environ['KAPAMPANGAN_MORPH_BUNDLE'] = name
                with self.assertRaises(ValueError):
                    model_bundles.resolve_bundle_path('morph_bpe')

    def test_valid_backup_folder_identified_from_its_manifest(self):
        path, manifest = make_bundle(self.root, 'infix48_seed42')
        checked = model_bundles.validate_bundle(path, 'morph_bpe')
        self.assertEqual(checked, manifest)
        metadata = model_bundles.bundle_metadata(path, checked)
        self.assertEqual(metadata['bundle_id'], 'infix48_seed42')
        self.assertEqual(metadata['condition'], 'morph_bpe')
        self.assertEqual(metadata['tokenizer_variant'], 'infix_first_penalty48')
        self.assertEqual(metadata['crossing_penalty'], 48)
        self.assertEqual(metadata['source_vocab_size'], 4)
        self.assertEqual(metadata['completed_epochs'], 2)
        self.assertEqual(metadata['tokenizer_sha256'], manifest['identity']['tokenizer_sha256'])

    def test_wrong_condition_and_missing_weights_are_rejected(self):
        path, _ = make_bundle(self.root, 'chosen')
        with self.assertRaises(ValueError):
            model_bundles.validate_bundle(path, 'plain_bpe')
        (path / 'best_source.safetensors').unlink()
        with self.assertRaises((ValueError, OSError)):
            model_bundles.validate_bundle(path, 'morph_bpe')
        with self.assertRaises((ValueError, OSError)):
            model_bundles.validate_bundle(self.root / 'not-installed', 'morph_bpe')

    def test_changed_tokenizer_and_unlisted_artifact_file_are_rejected(self):
        path, _ = make_bundle(self.root, 'changed')
        (path / 'source_artifact' / 'tokenizer.json').write_text('{}', encoding='utf-8')
        with self.assertRaises(ValueError):
            model_bundles.validate_bundle(path, 'morph_bpe')
        path, _ = make_bundle(self.root, 'extra')
        (path / 'source_artifact' / 'unexpected.txt').write_text('unlisted', encoding='utf-8')
        with self.assertRaises(ValueError):
            model_bundles.validate_bundle(path, 'morph_bpe')

    def test_incompatible_weight_shape_dtype_and_offsets_are_rejected(self):
        for name, kwargs in [('shape', dict(shape=(5, 1024))),
                             ('dtype', dict(dtype='F16')),
                             ('offsets', dict(offsets=[0, 12]))]:
            with self.subTest(name=name):
                path, _ = make_bundle(self.root, name)
                write_weights(path / 'best_source.safetensors', **kwargs)
                with self.assertRaises(ValueError):
                    model_bundles.validate_bundle(path, 'morph_bpe')

    def test_discovery_separates_usable_and_rejected_bundles(self):
        make_bundle(self.root, 'infix48_seed42')
        make_bundle(self.root, 'plain30', 'plain_bpe', 'plain_bpe')
        path, _ = make_bundle(self.root, 'broken')
        (path / 'best_source.safetensors').unlink()
        available, rejected = model_bundles.discover_bundles(self.root)
        self.assertEqual({item['bundle_id'] for item in available}, {'infix48_seed42', 'plain30'})
        self.assertEqual({item['condition'] for item in available}, {'plain_bpe', 'morph_bpe'})
        self.assertTrue(rejected)
        self.assertIn('broken', json.dumps(rejected))

    def test_selected_diagnostics_read_selected_bundle_histories(self):
        import performance_metrics
        default, _ = make_bundle(self.root, 'morph_bpe', variant='weighted_penalty32')
        write_json(default / 'history.json', [dict(epoch=1, train_loss=9.0, validation_loss=8.0)])
        make_bundle(self.root, 'infix48_seed42')
        os.environ['KAPAMPANGAN_MORPH_BUNDLE'] = 'infix48_seed42'
        with patch.object(performance_metrics, 'REPORTS', self.root / 'unavailable-reports'):
            chosen = performance_metrics.selected_training_metrics('morph_bpe')
        self.assertEqual(chosen['bundle_id'], 'infix48_seed42')
        self.assertEqual(chosen['tokenizer_variant'], 'infix_first_penalty48')
        self.assertEqual(chosen['completed_epochs'], 2)
        self.assertEqual(chosen['train_loss'], 1.4)
        self.assertEqual(chosen['validation_loss'], 1.2)
        self.assertIsNone(chosen['bleu'])
        self.assertIsNone(chosen['chrf_plus_plus'])


class RuntimeBindingTests(BundleFixture):
    def test_each_source_wrapper_uses_its_selected_runtime_and_id_mapping(self):
        import translation_service as service

        class OriginalSourceTokenizer:
            def __init__(self, *_args):
                raise AssertionError('The helper must not import a global tokenizer runtime.')

            @staticmethod
            def to_model_id(identifier):
                return 1 - identifier if identifier in (0, 1) else identifier

            def content_ids(self, text):
                return [self.to_model_id(identifier) for identifier in self.backend.encode(text).ids]

            def encode(self, text):
                return [self.start] + self.content_ids(text) + [self.special['</s>']]

        for condition, identifier in (('plain_bpe', 1), ('morph_bpe', 0)):
            with self.subTest(condition=condition):
                path, manifest = make_bundle(self.root, condition, condition)
                native = SimpleNamespace(vocabulary_size=4,
                    token_to_id={'<pad>': 0, '<unk>': 1, '<s>': 2, '</s>': 3},
                    encode=lambda _text, token=identifier: SimpleNamespace(ids=[token]))
                helper = SimpleNamespace(SourceTokenizer=OriginalSourceTokenizer)
                with patch.object(service, '_bundle', return_value=(path, manifest)), \
                     patch.object(service, '_native_tokenizer', return_value=native) as loaded:
                    service._bind_source_tokenizer(helper, condition)
                    source = helper.SourceTokenizer(path / 'source_artifact', 4)
                    self.assertIs(source.backend, native)
                    self.assertEqual(source.encode('probe'), [2, 1 - identifier, 3])
                    loaded.assert_called_with(condition)
                    with self.assertRaises(ValueError):
                        helper.SourceTokenizer(self.root / 'another-artifact', 4)


class LauncherSelectionTests(BundleFixture):
    def setUp(self):
        super().setUp()
        path = Path(__file__).parents[1] / 'run-backend.py'
        spec = importlib.util.spec_from_file_location('startup_launcher_test', path)
        self.launcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.launcher)

    def invoke(self, argv):
        # argparse may return an exit status or use SystemExit; both conventions
        # are accepted while asserting that no unwanted server starts.
        try:
            return self.launcher.main(argv)
        except SystemExit as exc:
            return exc.code

    def test_list_models_does_not_start_server_or_load_nllb(self):
        make_bundle(self.root, 'infix48_seed42')
        output = io.StringIO()
        with patch.object(self.launcher.runpy, 'run_path') as run_server, redirect_stdout(output):
            result = self.invoke(['--list-models'])
        self.assertIn(result, (0, None))
        self.assertIn('infix48_seed42', output.getvalue())
        run_server.assert_not_called()

    def test_explicit_folder_selection_is_set_before_server_starts(self):
        make_bundle(self.root, 'plain30', 'plain_bpe', 'plain_bpe')
        make_bundle(self.root, 'infix48_seed42')
        observed = {}
        def observe_server(*args, **kwargs):
            observed.update(plain=os.environ.get('KAPAMPANGAN_PLAIN_BUNDLE'),
                            morph=os.environ.get('KAPAMPANGAN_MORPH_BUNDLE'))
        with patch.object(self.launcher.runpy, 'run_path', side_effect=observe_server) as run_server:
            result = self.invoke(['--plain-bundle', 'plain30', '--morph-bundle', 'infix48_seed42'])
        self.assertIn(result, (0, None))
        self.assertEqual(observed, dict(plain='plain30', morph='infix48_seed42'))
        run_server.assert_called_once()

    def test_invalid_explicit_selection_stops_before_server(self):
        make_bundle(self.root, 'wrong-slot', 'plain_bpe', 'plain_bpe')
        for chosen in ('missing-model', 'wrong-slot', '../outside'):
            with self.subTest(chosen=chosen), patch.object(self.launcher.runpy, 'run_path') as run_server:
                try:
                    result = self.invoke(['--morph-bundle', chosen])
                except (ValueError, OSError):
                    result = 1
                self.assertNotIn(result, (0, None))
                run_server.assert_not_called()

    def test_menu_retries_invalid_answer_and_accepts_bundle_name(self):
        make_bundle(self.root, 'plain30', 'plain_bpe', 'plain_bpe')
        make_bundle(self.root, 'morph_bpe', variant='weighted_penalty32')
        make_bundle(self.root, 'infix48_seed42')
        output = io.StringIO()
        answers = ['invalid-choice', 'plain30', 'infix48_seed42']
        with patch('builtins.input', side_effect=answers) as prompt, \
             patch.object(self.launcher.runpy, 'run_path') as run_server, redirect_stdout(output):
            result = self.invoke(['--select-models'])
        self.assertIn(result, (0, None))
        self.assertEqual(prompt.call_count, 3)
        self.assertIn('Choose one of the listed bundles.', output.getvalue())
        self.assertEqual(os.environ['KAPAMPANGAN_PLAIN_BUNDLE'], 'plain30')
        self.assertEqual(os.environ['KAPAMPANGAN_MORPH_BUNDLE'], 'infix48_seed42')
        run_server.assert_called_once()

    def test_cancelled_menu_does_not_start_server(self):
        make_bundle(self.root, 'plain30', 'plain_bpe', 'plain_bpe')
        output = io.StringIO()
        with patch('builtins.input', return_value='q'), \
             patch.object(self.launcher.runpy, 'run_path') as run_server, redirect_stdout(output):
            result = self.invoke(['--select-models'])
        self.assertEqual(result, 0)
        self.assertIn('Startup cancelled.', output.getvalue())
        run_server.assert_not_called()


if __name__ == '__main__':
    unittest.main()
