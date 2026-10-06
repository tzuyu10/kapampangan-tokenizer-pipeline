import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'tokenizer'))
import performance_metrics


class PerformanceMetricsTests(unittest.TestCase):
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
