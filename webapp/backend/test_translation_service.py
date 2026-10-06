"""Process-response regression tests. Run with the translation Python environment."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import torch

import translation_service as service


class TranslationProcessTests(unittest.TestCase):
    def setUp(self):
        self.source = Mock(pad=1)
        self.source.encode.return_value = [2, 0, 10, 3]
        self.source.backend.encode.return_value.to_dict.return_value = {
            'normalized_text': 'example', 'ids': [1, 10],
            'tokens': [{'token': '<unk>', 'id': 1}, {'token': 'example', 'id': 10}],
        }
        self.target = Mock(all_special_ids=[2, 99])
        self.target.convert_tokens_to_ids.return_value = 99
        self.target.convert_ids_to_tokens.return_value = ['</s>', 'tgl_Latn', 'output', '</s>']
        self.target.decode.return_value = 'output'
        self.model = Mock(config=SimpleNamespace(d_model=1024, encoder_layers=12, decoder_layers=12))
        self.model.generate.return_value = torch.tensor([[2, 99, 12, 2]])
        manifest = {'identity': {'source_limit': 256, 'max_new_tokens': 160, 'beams': 4}}
        patches = [
            patch.object(service, '_bundle', return_value=(None, manifest)),
            patch.dict(service._CACHE, {'plain_bpe': (self.model, self.source, self.target, 'cpu')}, clear=True),
            patch.dict(service._EMBEDDINGS, {'plain_bpe': torch.nn.Embedding(20, 4)}, clear=True),
            patch.dict(service._RESULTS, {}, clear=True),
        ]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)

    def test_process_matches_generation_and_survives_cache(self):
        result = service.translate(' example ', 'plain_bpe')
        trace = result['process']
        self.assertEqual(trace['input_text'], 'example')
        self.assertEqual(trace['source_ids'], [1, 10])
        self.assertEqual(trace['model_source_ids'], [2, 0, 10, 3])
        self.assertEqual(trace['model_source_ids'], self.model.generate.call_args.kwargs['input_ids'][0].tolist())
        self.assertEqual([t['id'] for t in trace['target_tokens']], [2, 99, 12, 2])
        self.assertEqual([t['special'] for t in trace['target_tokens']], [True, True, False, True])
        self.target.decode.assert_any_call([2, 99, 12, 2], skip_special_tokens=True)
        self.assertEqual(result['source_token_count'], 4)
        self.assertEqual(result['output_token_count'], 1)
        self.assertEqual(trace['beams'], self.model.generate.call_args.kwargs['num_beams'])
        self.assertEqual(trace['embedding_dimension'], 1024)
        cached = service.translate('example', 'plain_bpe')
        self.assertTrue(cached['cache_hit'])
        self.assertEqual(cached['latency_ms'], 0)
        self.assertEqual(cached['process'], trace)
        self.model.generate.assert_called_once()

    def test_invalid_or_overlength_input_does_not_generate(self):
        for value in ['', ' ', 'a' * 501, None]:
            with self.assertRaises(ValueError):
                service.translate(value)
        with self.assertRaises(ValueError):
            service.translate('example', 'unknown')
        self.source.encode.return_value = [10] * 257
        with self.assertRaises(ValueError):
            service.translate('example')
        self.model.generate.assert_not_called()


if __name__ == '__main__':
    unittest.main()
