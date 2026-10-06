"""Control-mismatch regression tests; no GPU, torch, or downloaded model needed."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import translation_service as service


class ComparisonAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paths = []
        for condition in ('plain_bpe', 'morph_bpe'):
            path = Path(self.temp.name)/condition
            (path/'source_artifact').mkdir(parents=True)
            (path/'source_artifact/tokenizer-manifest.json').write_text(json.dumps({
                'core_file_sha256': {n: n for n in ('normalization.json', 'pretokenizer.json', 'special_tokens.json')},
                'metadata': {'prepared_manifest_fingerprint': 'same-stream', 'weighted_penalty_used': True},
            }))
            self.paths.append(path)
        manifest = dict(model_id='nllb', revision='pinned', source_vocab_size=6080,
                        cfg=dict(seed=42, epochs=15, lr=0.0003),
                        identity=dict(data_sha256='same-data', beams=4))
        self.manifests = [copy.deepcopy(manifest), copy.deepcopy(manifest)]
        service.comparison_audit.cache_clear()
        self.addCleanup(service.comparison_audit.cache_clear)
        bundle = patch.object(service, '_bundle', side_effect=lambda c: (
            self.paths[0 if c == 'plain_bpe' else 1],
            self.manifests[0 if c == 'plain_bpe' else 1]))
        bundle.start()
        self.addCleanup(bundle.stop)
        signature = patch.object(service, '_target_signature', return_value='same-target')
        self.signature = signature.start()
        self.addCleanup(signature.stop)

    def test_matched_controls(self):
        self.assertEqual(service.comparison_audit()['errors'], [])
        self.assertTrue(service.comparison_audit()['compatible'])

    def test_epoch_budget_disclosed(self):
        self.manifests[0]['cfg']['epochs'] = 30
        audit = service.comparison_audit()
        self.assertTrue(audit['compatible'])
        self.assertIn('cfg.epochs', audit['warnings'][0])

    def test_learning_rate_mismatch_blocks_comparison(self):
        self.manifests[1]['cfg']['lr'] = 0.001
        audit = service.comparison_audit()
        self.assertFalse(audit['compatible'])
        with patch.object(service, 'status', return_value={
            'can_translate': True, 'comparison_audit': audit,
        }), patch.object(service, 'translate') as generate:
            with self.assertRaisesRegex(ValueError, 'cfg.lr'):
                service.compare('sample')
            generate.assert_not_called()

    def test_target_config_mismatch(self):
        self.signature.side_effect = ['first', 'second']
        self.assertIn('Different target tokenizer', service.comparison_audit()['errors'])

    def test_data_mismatch(self):
        self.manifests[1]['identity']['data_sha256'] = 'other-data'
        self.assertFalse(service.comparison_audit()['compatible'])

    def test_tokenizer_stream_mismatch(self):
        path = self.paths[1]/'source_artifact/tokenizer-manifest.json'
        artifact = json.loads(path.read_text())
        artifact['metadata']['prepared_manifest_fingerprint'] = 'other-stream'
        path.write_text(json.dumps(artifact))
        self.assertIn('Different tokenizer training stream', service.comparison_audit()['errors'])


class SourceNormalizationTests(unittest.TestCase):
    def test_matches_training_normalization(self):
        self.assertEqual(service._normalize_source('  a\u0301\t  abak.\n'), 'á abak.')

    def test_adapted_display_uses_model_normalization(self):
        with patch.object(service, '_bundle', return_value=(None, {
            'identity': {'tokenizer_sha256': 'test'},
        })), patch.object(service, '_native_tokenizer') as native:
            native.return_value.encode.return_value.ids = [0, 1, 9]
            native.return_value.encode.return_value.to_dict.return_value = {}
            result = service.tokenize_adapted(' a\t  abak. ')
            native.return_value.encode.assert_called_once_with('a abak.')
            self.assertEqual(result['model_source_ids'], [2, 1, 0, 9, 3])


if __name__ == '__main__':
    unittest.main()
