"""Regression checks for shared-root access and strictly lossless annotations."""
import importlib.util
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = Path(os.environ.get('TAGALOG_V2_INPUTS', str(HERE / 'inputs')))
spec = importlib.util.spec_from_file_location('tagalog_v2_language_support', HERE / 'language_support.py')
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)


class AnnotationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PACKAGE.is_dir():
            raise unittest.SkipTest('Set TAGALOG_V2_INPUTS to the prepared v2 input directory.')
        cls.segmenter = support.tagalog_segmenter(PACKAGE)

    def test_shared_roots_allow_prefix_suffix_and_infix_analyses(self):
        for word, expected in [('nagaral', ['nag', 'aral']), ('magsalita', ['mag', 'salita']),
                               ('basahin', ['basa', 'hin']), ('sulatan', ['sulat', 'an']),
                               ('sinulat', ['s', 'in', 'ulat'])]:
            with self.subTest(word=word):
                boundaries, spans, _status = support.surface_analysis(self.segmenter, word)
                cuts = [0, *boundaries, len(word)]
                self.assertEqual([word[a:b] for a, b in zip(cuts, cuts[1:])], expected)
                self.assertTrue(any(role == 'root' for _a, _b, role in spans))

    def test_explicit_hyphen_preserves_case_separator_and_stem_suffix(self):
        for word, expected in [('Nag-aral', ['Nag', '-', 'aral']),
                               ('pinag-aralan', ['pinag', '-', 'aral', 'an'])]:
            with self.subTest(word=word):
                boundaries, _spans, status = support.surface_analysis(self.segmenter, word)
                cuts = [0, *boundaries, len(word)]
                pieces = [word[a:b] for a, b in zip(cuts, cuts[1:])]
                self.assertEqual(pieces, expected)
                self.assertEqual(''.join(pieces), word)
                self.assertEqual(status, 'segmented_hyphenated_prefix')

    def test_unknown_stems_and_unrecognized_hyphen_prefix_stay_intact(self):
        for word in ['nag-qzxw', 'qzxw-aral', 'magqzxw', 'QZXW']:
            self.assertEqual(support.surface_analysis(self.segmenter, word)[0], ())

    def test_surface_spans_are_contiguous_and_infix_role_is_retained(self):
        for word in ['NAGARAL', 'Sinulat', 'Nag-aral', 'basahin']:
            _bounds, spans, _status = support.surface_analysis(self.segmenter, word)
            self.assertEqual(spans[0][0], 0)
            self.assertEqual(spans[-1][1], len(word))
            self.assertEqual([span[1] for span in spans[:-1]], [span[0] for span in spans[1:]])
        self.assertIn((1, 3, 'infix'), support.surface_analysis(self.segmenter, 'Sinulat')[1])


if __name__ == '__main__':
    unittest.main()
