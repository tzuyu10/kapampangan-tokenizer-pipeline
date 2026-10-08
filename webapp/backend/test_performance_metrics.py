import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'tokenizer'))
import performance_metrics


class PerformanceMetricsTests(unittest.TestCase):
    def evaluation_fixture(self, directory):
        path = Path(directory) / 'model'
        reports = Path(directory) / 'reports'
        report = reports / 'plain_bpe'
        report.mkdir(parents=True)
        path.mkdir()
        files = {'weights': 'best_source.safetensors', 'tokenizer': 'source_artifact/tokenizer.json',
                 'runtime': 'runtime/kapampangan_morphbpe_runtime/tokenizer.py',
                 'target': 'target_tokenizer/tokenizer.json', 'helper': 'nllb_source_adapter.py'}
        identity = dict(condition='plain_bpe', split='test', final_full_split=True,
                        examples=2, data='dataset', base='revision', beams=4,
                        max_new_tokens=160, source_limit=256, seed=42, precision='fp32',
                        row_ids_sha256=hashlib.sha256(json.dumps(['a', 'b']).encode()).hexdigest())
        for key, rel in files.items():
            file = path / rel
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(key)
            identity[key] = hashlib.sha256(file.read_bytes()).hexdigest()
        (path / 'manifest.json').write_text(json.dumps(dict(revision='revision', cfg={'seed': 42},
            identity=dict(condition='plain_bpe', data_sha256='dataset', beams=4,
                          max_new_tokens=160, source_limit=256))))
        (path / 'split_manifest.json').write_text(json.dumps({'test': ['a', 'b']}))
        metrics = {'BLEU': {'score': 45.8, 'signature': 'bleu'},
                   'chrF++': {'score': 65.4, 'signature': 'chrf'},
                   'scope': dict(split='test', full_split=True, examples=2, available_rows=2)}
        (report / 'metrics.json').write_text(json.dumps(metrics))
        (report / 'evaluation_identity.json').write_text(json.dumps(identity))
        for name in ('predictions.jsonl', 'hypotheses.txt', 'references.txt'):
            (report / name).write_text('verified fixture')
        proof = dict(conditions={'plain_bpe': dict(validation='passed', split='test', examples=2,
                        scores={'BLEU': 45.8, 'chrF++': 65.4})},
                     files={f'plain_bpe/{f.name}': hashlib.sha256(f.read_bytes()).hexdigest()
                            for f in report.iterdir()})
        (reports / 'verification.json').write_text(json.dumps(proof))
        return path, reports

    def test_only_matching_checkpoint_receives_verified_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            path, reports = self.evaluation_fixture(directory)
            result = performance_metrics.quality_metrics(path, reports)
            self.assertEqual((result['bleu'], result['chrf_plus_plus']), (45.8, 65.4))
            self.assertEqual(result['evaluation_examples'], 2)
            (path / 'best_source.safetensors').write_text('replacement checkpoint')
            result = performance_metrics.quality_metrics(path, reports)
            self.assertEqual(result['quality_status'], 'Checkpoint mismatch')
            self.assertIsNone(result['bleu'])
            self.assertIsNone(result['chrf_plus_plus'])

    def test_changed_tokenizer_does_not_inherit_previous_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            path, reports = self.evaluation_fixture(directory)
            (path / 'source_artifact/tokenizer.json').write_text('penalty32 replacement tokenizer')
            result = performance_metrics.quality_metrics(path, reports)
            self.assertIsNone(result['bleu'])
            self.assertIn('tokenizer', result['quality_reason'])

    def test_report_tampering_or_different_split_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path, reports = self.evaluation_fixture(directory)
            (reports / 'plain_bpe/metrics.json').write_text('{}')
            self.assertIsNone(performance_metrics.quality_metrics(path, reports)['bleu'])
        with tempfile.TemporaryDirectory() as directory:
            path, reports = self.evaluation_fixture(directory)
            (path / 'split_manifest.json').write_text(json.dumps({'test': ['a', 'c']}))
            result = performance_metrics.quality_metrics(path, reports)
            self.assertIsNone(result['bleu'])
            self.assertIn('rows differ', result['quality_reason'])

    def test_best_epoch_losses_are_not_taken_from_last_epoch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / 'manifest.json').write_text(json.dumps({'identity': {'tokenizer_sha256': 'example'}}))
            (path / 'history.json').write_text(json.dumps([
                dict(epoch=1, train_loss=2.0, validation_loss=1.5),
                dict(epoch=2, train_loss=1.0, validation_loss=1.8)]))
            result = performance_metrics.training_metrics(path)
            self.assertEqual((result['completed_epochs'], result['best_epoch']), (2, 1))
            self.assertEqual(result['train_loss'], 2.0)
            self.assertIsNone(result['bleu'])
            self.assertIsNone(result['chrf_plus_plus'])

    def test_missing_or_invalid_history_has_no_invented_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            self.assertFalse(performance_metrics.training_metrics(path)['available'])
            (path / 'manifest.json').write_text('{}')
            (path / 'history.json').write_text('[]')
            self.assertFalse(performance_metrics.training_metrics(path)['available'])

    def test_diagnostics_match_deployed_tokenizers_and_reference_scoring(self):
        import comparison_service as comparison
        import reference_data as ref
        result = performance_metrics.initial_metrics()['tokenizer']
        sentence = [word for words in ref.SENTENCES for word in words] + [word for _, _, words in ref.FAMILIES for word in words]
        rows = ref.rows_for(sentence)
        groups = comparison.groups_by_tokenizer(' '.join(word for word, _ in sentence))
        self.assertEqual(result['word_occurrences'], len(rows))
        for measured in result['rows']:
            expected = ref.score(rows, groups[measured['condition']])
            self.assertEqual(measured['boundary_f1'], expected['boundary_f1'])
            self.assertEqual(measured['consistency_f1'], expected['mcf1'])
            self.assertAlmostEqual(measured['fertility'], sum(map(len, groups[measured['condition']])) / len(rows))
            self.assertEqual(len(measured['tokenizer_sha256']), 64)
        json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
