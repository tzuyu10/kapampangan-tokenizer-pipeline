"""Trace correctness and input isolation regression checks."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'tokenizer'))
import comparison_service as service

class ProcessTests(unittest.TestCase):
    def test_trace_output_matches_each_runtime(self):
        for text in ['pipaglutuan', 'abababab', 'a\u0301 😀', 'ka|ligtas|an mag|ligtas']:
            result=service.custom_compare(text)
            for name,tok in [('MorphBPE',service.MORPH),('Plain BPE',service.PLAIN)]:
                for trace in result['process']['traces'][name]:
                    self.assertEqual([t['token'] for t in trace['final_tokens']], [t.token for t in tok.encode(trace['surface']).tokens])
            for trace in result['process']['traces']['Unigram-LM']:
                self.assertEqual(trace['final_tokens'],service.UNI.encode(trace['surface']))
    def test_unigram_receives_original_unknown_characters(self):
        with patch.object(service.UNI,'encode', wraps=service.UNI.encode) as encode:
            service.groups_by_tokenizer('😀')
            encode.assert_called_once_with('😀')
    def test_invalid_annotation_rejected(self):
        for text in ['|','a||b','|ab','ab|']:
            with self.assertRaises(ValueError): service.custom_compare(text)
    def test_scoring_parity(self):
        passed,total=service.verify_scoring_fidelity()
        self.assertEqual(passed,total)

if __name__=='__main__': unittest.main()
