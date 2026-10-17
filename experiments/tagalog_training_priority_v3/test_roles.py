"""Role construction must retain the infix baseline and reject unsupported roles."""
import unittest
from train import combine_roles, pam_affixes
from types import SimpleNamespace


class RoleTests(unittest.TestCase):
    def test_shared_keys_require_matching_affix_support(self):
        self.assertEqual(combine_roles(set(), [{(0, 3, 'affix')}, set()]), [])
        self.assertEqual(combine_roles(set(), [{(0, 3, 'affix')}, {(0, 3, 'affix')}]), [(0, 3, 'affix')])

    def test_infix_roles_cannot_be_relabelled_or_absorbed(self):
        infix = {(1, 3, 'infix')}
        self.assertEqual(combine_roles(infix, [{(0, 4, 'affix')}]), [(1, 3, 'infix')])
        self.assertEqual(combine_roles(infix, [{(0, 1, 'affix'), (3, 5, 'affix')}]),
                         [(0, 1, 'affix'), (1, 3, 'infix'), (3, 5, 'affix')])

    def test_surface_offsets_are_used_for_prefix_and_suffix(self):
        analysis = SimpleNamespace(status='accepted', protected_boundaries=(3, 7),
            segments=('nag', 'aral', 'an'), underlying_units=[SimpleNamespace(kind=k) for k in ['prefix', 'root', 'suffix']])
        analyzer = SimpleNamespace(segment=lambda _word: analysis)
        self.assertEqual(pam_affixes(analyzer, 'nagaralan', (3, 7)), {(0, 3, 'affix'), (7, 9, 'affix')})

    def test_ambiguous_or_mismatched_analyses_add_no_roles(self):
        for status, boundaries in [('ambiguous', (3,)), ('accepted', (2,))]:
            analyzer = SimpleNamespace(segment=lambda _word: SimpleNamespace(status=status, protected_boundaries=boundaries))
            self.assertEqual(pam_affixes(analyzer, 'nagaral', (3,)), set())


if __name__ == '__main__':
    unittest.main()
