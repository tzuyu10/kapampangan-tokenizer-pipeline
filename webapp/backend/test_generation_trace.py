"""Use a tiny real encoder-decoder to check observation parity without downloads."""
import json
import unittest
from unittest.mock import patch

import torch
from transformers import M2M100Config, M2M100ForConditionalGeneration

from generation_trace import GenerationTrace


class TokenLabels:
    def convert_ids_to_tokens(self, i):
        return f'token{i}'

    def decode(self, ids, skip_special_tokens=True):
        return ' '.join(f'token{i}' for i in ids if i not in (0, 1, 2, 3))


class GenerationTraceTests(unittest.TestCase):
    def setUp(self):
        torch.set_num_threads(2)
        torch.manual_seed(17)
        config = M2M100Config(vocab_size=24, d_model=8, encoder_layers=1, decoder_layers=1,
            encoder_attention_heads=2, decoder_attention_heads=2, encoder_ffn_dim=16, decoder_ffn_dim=16,
            dropout=0., attention_dropout=0., activation_dropout=0., encoder_layerdrop=0., decoder_layerdrop=0.,
            pad_token_id=1, bos_token_id=0, eos_token_id=2, decoder_start_token_id=2)
        self.model = M2M100ForConditionalGeneration(config).eval()
        self.ids = torch.tensor([[0, 7, 8, 2]])
        self.kwargs = dict(input_ids=self.ids, attention_mask=torch.ones_like(self.ids),
                           num_beams=4, max_new_tokens=6, forced_bos_token_id=3, do_sample=False)

    def test_real_generation_is_unchanged_and_trace_matches_tensors(self):
        with torch.inference_mode():
            reference = self.model.generate(**self.kwargs, return_dict_in_generate=True, output_scores=True)
            expected = reference.sequences
            embeddings = self.model.get_encoder().embed_tokens(self.ids)
            encoder = self.model.get_encoder()(self.ids, attention_mask=torch.ones_like(self.ids)).last_hidden_state
            trace = GenerationTrace(TokenLabels())
            with trace.capture(self.model):
                output = self.model.generate(**self.kwargs)
            self.assertTrue(torch.equal(expected, output))
            data = trace.finish(output[0].tolist())
            self.assertEqual(data['embedding_vectors'], trace.vectors(embeddings))
            self.assertEqual(data['encoder_vectors'], trace.vectors(encoder))
            self.assertEqual(len(data['decoder_steps']), 6)
            self.assertEqual(len(data['final_candidates']), 4)
            self.assertTrue(data['final_candidates'][0]['chosen'])
            self.assertEqual(data['final_candidates'][0]['text'], TokenLabels().decode(output[0].tolist()))
            self.assertAlmostEqual(data['final_candidates'][0]['score'], reference.sequences_scores[0].item(), places=4)
            for index, step in enumerate(data['decoder_steps']):
                self.assertEqual(len(step['retained']), 4)
                self.assertEqual(step['final_choice']['id'], output[0, index + 1].item())
                for beam in step['beams']:
                    for candidate in beam['candidates']:
                        self.assertAlmostEqual(candidate['score'], reference.scores[index][beam['beam'], candidate['id']].item(), places=4)
                if index + 1 < len(data['decoder_steps']):
                    for item, following in zip(step['retained'], data['decoder_steps'][index+1]['beams']):
                        prefix = step['beams'][item['from_beam']]['prefix_ids'] + [item['id']]
                        self.assertEqual(prefix, following['prefix_ids'])
            self.assertEqual(data['decoder_steps'][0]['beams'][0]['candidates'],
                             [{'id': 3, 'token': 'token3', 'score': 0.0, 'chosen': True}])
            json.dumps(data, allow_nan=False)
            self.assertNotIn('_beam_search', self.model.__dict__)
            self.assertFalse(self.model.get_encoder()._forward_hooks)
            self.assertFalse(self.model.get_encoder().embed_tokens._forward_hooks)
            self.assertTrue(torch.equal(expected, self.model.generate(**self.kwargs)))

    def test_hooks_are_removed_on_failure(self):
        trace = GenerationTrace(TokenLabels())
        with self.assertRaisesRegex(RuntimeError, 'test failure'):
            with patch.object(self.model, 'forward', side_effect=RuntimeError('test failure')):
                with torch.inference_mode(), trace.capture(self.model):
                    self.model.generate(**self.kwargs)
        self.assertNotIn('_beam_search', self.model.__dict__)
        self.assertFalse(self.model.get_encoder()._forward_hooks)
        self.assertFalse(self.model.get_encoder().embed_tokens._forward_hooks)


if __name__ == '__main__':
    unittest.main()
