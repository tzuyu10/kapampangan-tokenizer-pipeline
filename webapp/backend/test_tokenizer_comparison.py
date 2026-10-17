"""Comparison selection and gold-scoring checks with real tiny-format encoders."""

import hashlib
import json
from dataclasses import replace
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

BACKEND = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(BACKEND / "tokenizer"))

import comparison_service as comparison
from kapampangan_morphbpe_runtime import Tokenizer
import reference_data as ref
import tokenizer_variants
import trace_service


def _encoder(root, name, merge_count):
    """Distinct, lossless encoders expose accidental reuse of another row/size."""
    path = root / name
    path.mkdir()
    tokens = ["<pad>", "<unk>", "<s>", "</s>", "a", "b", "c", " "]
    merges = []
    for left, right in [("a", "b"), ("ab", "c")][:merge_count]:
        result = left + right
        merges.append(dict(rank=len(merges), left=left, right=right,
                           result=result, result_id=len(tokens)))
        tokens.append(result)
    document = dict(
        schema_version="1.0.0", artifact_type="kapampangan_morphbpe",
        normalization=dict(unicode_normalization="NFC", spelling_mappings=[]),
        vocabulary=[dict(id=i, token=token,
                         kind="special" if i < 4 else "character" if i < 8 else "merge")
                    for i, token in enumerate(tokens)],
        merges=merges,
        special_tokens=[dict(role=role, token=tokens[i], id=i)
                        for i, role in enumerate(["pad", "unk", "bos", "eos"])],
    )
    file = path / "tokenizer.json"
    file.write_text(json.dumps(document), encoding="utf-8")
    (path / "checksums.sha256").write_text(
        hashlib.sha256(file.read_bytes()).hexdigest() + "  tokenizer.json\n", encoding="utf-8",
    )
    return Tokenizer(path)


class TokenizerComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.records = {}
        # The catalog's common Encoding API permits the same fixture encoder
        # type in all rows. This tests dispatch, not Unigram's Viterbi algorithm.
        for size, counts in [(6080, (1, 0, 2)), (8192, (2, 1, 0))]:
            for family, variant, count in zip(
                ["infix_first48", "plain", "unigram"],
                ["infix_first_penalty48", "plain_bpe", "unigram_lm"], counts,
            ):
                identifier = (f"unigram-lm-{size}" if family == "unigram"
                              else f"variant:pam_tl_{family}_{size}")
                tok = _encoder(self.root, f"{family}_{size}", count)
                info = dict(id=identifier, label=f"{family} {size}",
                            tokenizer_variant=variant, source_vocab_size=size,
                            tokenizer_sha256=hashlib.sha256(
                                (tok.artifact_dir / "tokenizer.json").read_bytes()).hexdigest())
                self.records[identifier] = (tok, None, info)
        legacy = _encoder(self.root, "legacy", 0)
        self.records["morphbpe-penalty32"] = (
            legacy, None,
            dict(id="morphbpe-penalty32", label="Legacy weighted32",
                 tokenizer_variant="weighted_penalty32", source_vocab_size=6080),
        )
        self.loader = patch.object(comparison.tokenizer_variants, "load", side_effect=self.load)
        self.loader.start()

    def tearDown(self):
        self.loader.stop()
        self.temporary.cleanup()

    def load(self, identifier):
        if not isinstance(identifier, str) or identifier not in self.records:
            raise ValueError("Unknown tokenizer identifier")
        return self.records[identifier]

    def test_default_is_new_6080_infix_and_identifies_matching_controls(self):
        result = comparison.custom_compare("abc")
        info = result["comparison"]
        self.assertEqual(info["selected"]["id"], "variant:pam_tl_infix_first48_6080")
        self.assertEqual(info["source_vocab_size"], 6080)
        self.assertEqual(info["tokenizers"]["Plain BPE"]["id"], "variant:pam_tl_plain_6080")
        self.assertEqual(info["tokenizers"]["Unigram-LM"]["id"], "unigram-lm-6080")

    def test_all_six_selections_use_actual_encoders_and_identify_actual_rows(self):
        for identifier in list(self.records)[:6]:
            with self.subTest(identifier=identifier):
                result = comparison.custom_compare("ab|c abc", identifier)
                self.assertEqual(result["comparison"]["selected"]["id"], identifier)
                self.assertEqual(set(result["splits"]), set(comparison.NAMES))
                for row, identity in result["comparison"]["tokenizers"].items():
                    encoder = self.records[identity["id"]][0]
                    expected = [[token.token for token in encoder.encode(word).tokens]
                                for word in ["abc", "abc"]]
                    self.assertEqual(result["splits"][row], expected)
                    self.assertEqual(result["fertility"][row]["tokens"],
                                     sum(map(len, expected)))
                    self.assertEqual(identity["source_vocab_size"],
                                     result["comparison"]["source_vocab_size"])
                selected_row = ("Unigram-LM" if identifier.startswith("unigram")
                                else "Plain BPE" if "_plain_" in identifier else "MorphBPE")
                self.assertEqual(result["comparison"]["tokenizers"][selected_row]["id"],
                                 identifier)
                self.assertEqual(result["clean_text"], "abc abc")
                self.assertIsNotNone(result["gold"])

    def test_8192_and_6080_selections_do_not_mutate_shared_defaults(self):
        first = comparison.custom_compare("abc", "variant:pam_tl_infix_first48_8192")
        second = comparison.custom_compare("abc", "variant:pam_tl_infix_first48_6080")
        again = comparison.custom_compare("abc", "variant:pam_tl_infix_first48_8192")
        self.assertEqual(first, again)
        for row in comparison.NAMES:
            self.assertNotEqual(first["splits"][row], second["splits"][row])

    def test_explicit_legacy_morph_selection_remains_the_morph_row(self):
        result = comparison.custom_compare("abc", "morphbpe-penalty32")
        self.assertEqual(result["comparison"]["tokenizers"]["MorphBPE"]["id"],
                         "morphbpe-penalty32")
        self.assertEqual(result["splits"]["MorphBPE"], [["a", "b", "c"]])
        self.assertEqual(result["comparison"]["tokenizers"]["Unigram-LM"]["id"],
                         "unigram-lm-6080")

    def test_invalid_selection_errors_including_empty_requests(self):
        for identifier in ["unknown", "variant:../outside", "", 123]:
            for text in ["abc", ""]:
                with self.subTest(identifier=identifier, text=text), self.assertRaises(ValueError):
                    comparison.custom_compare(text, identifier)
        self.assertIsNone(comparison.custom_compare("  "))
        with self.assertRaisesRegex(ValueError, "string"):
            comparison.custom_compare(123)

    def test_unsupported_vocabulary_size_is_explicit(self):
        tok, pretokenize, info = self.records["morphbpe-penalty32"]
        self.records["large"] = (tok, pretokenize, dict(info, id="large", source_vocab_size=16384))
        with self.assertRaisesRegex(ValueError, "6,080 or 8,192"):
            comparison.custom_compare("abc", "large")

    def test_gold_scores_reuse_reference_functions_and_unannotated_text_has_no_gold(self):
        result = comparison.custom_compare("ab|c ab|c")
        rows = ref.rows_for([("abc", "ab|c"), ("abc", "ab|c")])
        for row in comparison.NAMES:
            predictions = [tuple(pieces) for pieces in result["splits"][row]]
            self.assertEqual(result["gold"]["metrics"][row], ref.score(rows, predictions))
        self.assertIsNone(comparison.custom_compare("abc")["gold"])

    def test_unknown_pieces_prevent_invalid_gold_scoring(self):
        result = comparison.custom_compare("a|z")
        self.assertIsNone(result["gold"])
        self.assertIn("unknown token IDs", result["gold_unavailable_reason"])

    def test_surface_preserving_unigram_unknown_ids_cannot_receive_gold_scores(self):
        encoder = self.records["unigram-lm-6080"][0]
        real_encode = encoder.encode

        def unknown_with_surface(text):
            encoded = real_encode(text)
            tokens = tuple(replace(token, identifier=1, vocabulary_kind="special")
                           if token.pretoken_kind != "whitespace" else token
                           for token in encoded.tokens)
            return replace(encoded, tokens=tokens)

        with patch.object(encoder, "encode", side_effect=unknown_with_surface):
            result = comparison.custom_compare("ab|c")
        self.assertTrue(all("".join(pieces[0]) == "abc"
                            for pieces in result["splits"].values()))
        self.assertIsNone(result["gold"])
        self.assertIn("unknown token IDs", result["gold_unavailable_reason"])


class InstalledTokenizerComparisonTests(unittest.TestCase):
    """Verify the shipped six-option UI against the actual installed encoders."""

    CASES = (
        ("variant:pam_tl_infix_first48_6080", 6080, "MorphBPE"),
        ("variant:pam_tl_infix_first48_8192", 8192, "MorphBPE"),
        ("plain-bpe", 6080, "Plain BPE"),
        ("variant:pam_tl_plain_8192", 8192, "Plain BPE"),
        ("unigram-lm-6080", 6080, "Unigram-LM"),
        ("unigram-lm-8192", 8192, "Unigram-LM"),
    )

    def test_installed_catalog_has_all_six_options_and_new_morph_default(self):
        result = tokenizer_variants.catalog()
        available = {entry["id"]: entry for entry in result["tokenizers"]}
        self.assertEqual(result["default_tokenizer"], "variant:pam_tl_infix_first48_6080")
        for identifier, size, _row in self.CASES:
            with self.subTest(identifier=identifier):
                self.assertIn(identifier, available)
                self.assertEqual(available[identifier]["source_vocab_size"], size)
        self.assertNotIn("variant:pam_tl_plain_6080", available)
        self.assertEqual(comparison.configuration()["metadata"]["selected"]["id"],
                         result["default_tokenizer"])
        self.assertEqual(trace_service.analyze("sinulat")["tokenizer"]["id"],
                         result["default_tokenizer"])
        alias, _, alias_info = tokenizer_variants.load("variant:pam_tl_plain_6080")
        plain, _, plain_info = tokenizer_variants.load("plain-bpe")
        self.assertEqual(alias_info["id"], "variant:pam_tl_plain_6080")
        self.assertEqual(alias_info["tokenizer_sha256"], plain_info["tokenizer_sha256"])
        self.assertEqual(alias.encode("sinulat").ids, plain.encode("sinulat").ids)

    def test_installed_trace_and_comparison_match_each_actual_encoder(self):
        raw = "s|in|ulat ku ing amanu. Masánting ing abalu."
        clean = raw.replace("|", "")
        for identifier, size, selected_row in self.CASES:
            with self.subTest(identifier=identifier):
                tok, _, identity = tokenizer_variants.load(identifier)
                actual = tok.encode(clean)
                traced = trace_service.analyze(raw, identifier)
                result = comparison.custom_compare(raw, identifier)
                self.assertEqual(traced["tokenizer"], identity)
                self.assertEqual([token["token"] for token in traced["all_tokens"]],
                                 [token.token for token in actual.tokens])
                self.assertEqual([token["id"] for token in traced["all_tokens"]],
                                 list(actual.ids))
                self.assertEqual(result["comparison"]["selected"], identity)
                self.assertEqual(result["comparison"]["source_vocab_size"], size)
                self.assertEqual(result["comparison"]["tokenizers"][selected_row], identity)
                expected_ids = {
                    "MorphBPE": f"variant:pam_tl_infix_first48_{size}",
                    "Plain BPE": f"variant:pam_tl_plain_{size}",
                    "Unigram-LM": f"unigram-lm-{size}",
                }
                expected_ids[selected_row] = identifier
                for row, row_info in result["comparison"]["tokenizers"].items():
                    self.assertEqual(row_info["id"], expected_ids[row])
                    encoder, _, installed_info = tokenizer_variants.load(row_info["id"])
                    self.assertEqual(row_info, installed_info)
                    self.assertEqual(encoder.vocabulary_size, size)
                    expected = [[token.token for token in encoder.encode(word).tokens]
                                for word in clean.split()]
                    self.assertEqual(result["splits"][row], expected)
                    self.assertEqual(result["fertility"][row]["tokens"],
                                     sum(map(len, expected)))
                    artifact_hash = hashlib.sha256(
                        (encoder.artifact_dir / "tokenizer.json").read_bytes()).hexdigest()
                    self.assertEqual(row_info["tokenizer_sha256"], artifact_hash)
                self.assertIsNotNone(result["gold"])
                self.assertEqual(result["clean_text"], clean)
                json.dumps(result, allow_nan=False)

    def test_installed_initial_diagnostics_use_selected_size_and_actual_hashes(self):
        import performance_metrics

        sentences = ref.SENTENCES + [forms for _, _, forms in ref.FAMILIES]
        expected_rows = ref.rows_for([item for sentence in sentences for item in sentence])
        for size in (6080, 8192):
            identifier = f"variant:pam_tl_infix_first48_{size}"
            with self.subTest(size=size):
                result = performance_metrics.initial_metrics(identifier)
                metadata = result["tokenizer_comparison"]
                self.assertEqual(metadata["selected"]["id"], identifier)
                self.assertEqual(metadata["source_vocab_size"], size)
                self.assertEqual(result["tokenizer"]["word_occurrences"], len(expected_rows))
                for row in result["tokenizer"]["rows"]:
                    identity = metadata["tokenizers"][row["condition"]]
                    encoder, _, installed_info = tokenizer_variants.load(identity["id"])
                    expected_hash = hashlib.sha256(
                        (encoder.artifact_dir / "tokenizer.json").read_bytes()).hexdigest()
                    self.assertEqual(row["artifact"], identity["id"])
                    self.assertEqual(row["source_vocab_size"], size)
                    self.assertEqual(row["tokenizer_sha256"], expected_hash)
                    self.assertEqual(identity, installed_info)
                    groups = [tuple(token.token for token in encoder.encode(surface).tokens)
                              for sentence in sentences for surface, _spec in sentence]
                    self.assertTrue(all(
                        token.identifier != encoder.special_by_role["unk"][1]
                        for sentence in sentences for surface, _spec in sentence
                        for token in encoder.encode(surface).tokens
                    ))
                    scores = ref.score(expected_rows, groups)
                    self.assertEqual(row["boundary_f1"], scores["boundary_f1"])
                    self.assertEqual(row["consistency_f1"], scores["mcf1"])
                    self.assertAlmostEqual(row["fertility"],
                                           sum(map(len, groups)) / len(expected_rows))
                json.dumps(result, allow_nan=False)

    def test_installed_scoring_explanations_keep_reference_fidelity(self):
        self.assertEqual(comparison.verify_scoring_fidelity(), (6, 6))


if __name__ == "__main__":
    unittest.main()
