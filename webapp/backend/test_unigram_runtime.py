"""Portable Unigram validation and optional parity against HF tokenizers."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unicodedata
import unittest

BACKEND = Path(__file__).resolve().parent
REPO = BACKEND.parents[1]
sys.path.insert(0, str(BACKEND / "tokenizer"))
from kapampangan_morphbpe_runtime.tokenizer import _pretokenize
from unigram_runtime import Tokenizer

try:
    from tokenizers import Tokenizer as HFTokenizer
except ImportError:
    HFTokenizer = None


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _checksums(path):
    (path / "checksums.sha256").write_text("".join(
        hashlib.sha256(file.read_bytes()).hexdigest() + "  " + file.name + "\n"
        for file in sorted(path.iterdir()) if file.name != "checksums.sha256"
    ), encoding="utf-8")


def _manifest(path, vocabulary_size):
    manifest = {
        "algorithm": "unigram_lm", "artifact_type": "matched_fresh_unigram",
        "actual_vocabulary_size": vocabulary_size,
        "tokenizer_sha256": hashlib.sha256((path / "tokenizer.json").read_bytes()).hexdigest(),
        "normalizer": None, "pre_tokenizer": None, "decoder": "Fuse",
        "special_tokens": ["<pad>", "<unk>", "<s>", "</s>"],
    }
    canonical = json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    manifest["artifact_fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    _write_json(path / "unigram-manifest.json", manifest)
    _checksums(path)


def _artifact(path, pieces):
    path.mkdir(exist_ok=True)
    specials = ["<pad>", "<unk>", "<s>", "</s>"]
    vocabulary = [[piece, 0.0] for piece in specials] + [list(pair) for pair in pieces]
    _write_json(path / "tokenizer.json", {
        "version": "1.0", "normalizer": None, "pre_tokenizer": None,
        "post_processor": None, "truncation": None, "padding": None,
        "decoder": {"type": "Fuse"},
        "added_tokens": [{"id": index, "content": piece, "special": True,
                          "single_word": False, "lstrip": False, "rstrip": False,
                          "normalized": False} for index, piece in enumerate(specials)],
        "model": {"type": "Unigram", "unk_id": 1, "vocab": vocabulary, "byte_fallback": False},
    })
    _manifest(path, len(vocabulary))
    return Tokenizer(path)


class UnigramRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary_root = REPO / ".cache"
        temporary_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="unigram-runtime-", dir=temporary_root)
        self.root = Path(self.temp.name)
        self.tokenizer = _artifact(self.root, [("a", -1), ("b", -1), ("ab", -2),
                                               (" ", -1), ("!", -1), ("á", -1)])

    def tearDown(self):
        self.temp.cleanup()

    def test_exact_tie_prefers_longest_final_piece(self):
        self.assertEqual(self.tokenizer.encode("ab").token_strings, ("ab",))
        tokenizer = _artifact(self.root, [("a", 0), ("aa", 0), ("aaa", 0)])
        self.assertEqual(tokenizer.encode("aaaa").token_strings, ("a", "aaa"))
        self.assertEqual(tokenizer.encode("aaaaa").token_strings, ("aa", "aaa"))
        self.assertEqual(tokenizer.encode("aaaaa").offsets, ((0, 2), (2, 5)))

    def test_full_vocabulary_piece_does_not_override_higher_scoring_split(self):
        tokenizer = _artifact(self.root, [("a", -1), ("b", -1), ("ab", -3)])
        self.assertEqual(tokenizer.encode("ab").token_strings, ("a", "b"))

    def test_nfc_offsets_whitespace_and_punctuation_are_preserved(self):
        encoding = self.tokenizer.encode("a\u0301 ab!")
        self.assertEqual(encoding.normalized_text, "á ab!")
        self.assertEqual(encoding.token_strings, ("á", " ", "ab", "!"))
        self.assertEqual(encoding.offsets, ((0, 1), (1, 2), (2, 4), (4, 5)))
        self.assertEqual([token.pretoken_kind for token in encoding.tokens],
                         ["word", "whitespace", "word", "punctuation"])
        self.assertEqual(self.tokenizer.decode(encoding.ids), "á ab!")

    def test_adjacent_unknown_letters_share_a_surface_span(self):
        encoding = self.tokenizer.encode("axyb")
        self.assertEqual(encoding.token_strings, ("a", "xy", "b"))
        self.assertEqual(encoding.ids, (4, 1, 5))
        self.assertEqual(encoding.offsets, ((0, 1), (1, 3), (3, 4)))
        self.assertEqual(self.tokenizer.decode(encoding.ids), "ab")
        self.assertEqual(self.tokenizer.decode(encoding.ids, skip_special_tokens=False), "a<unk>b")

    def test_optional_special_tokens_empty_input_and_invalid_inputs(self):
        self.assertEqual(self.tokenizer.encode("").ids, ())
        self.assertEqual(self.tokenizer.encode("", add_special_tokens=True).ids, (2, 3))
        encoding = self.tokenizer.encode("ab", add_special_tokens=True)
        self.assertEqual(encoding.ids, (2, 6, 3))
        self.assertEqual(encoding.offsets, ((0, 0), (0, 2), (2, 2)))
        self.assertEqual(self.tokenizer.decode(encoding.ids), "ab")
        for value in (-1, True, self.tokenizer.vocabulary_size, "4"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.tokenizer.decode([value])
        with self.assertRaises(TypeError):
            self.tokenizer.encode(None)

    def test_trace_uses_actual_viterbi_output_and_has_no_bpe_steps(self):
        trace = self.tokenizer.trace_word("axyb")
        self.assertEqual(trace["algorithm"], "unigram_lm")
        self.assertEqual(trace["steps"], [])
        self.assertEqual(trace["characters"], list("axyb"))
        self.assertEqual([entry["token"] for entry in trace["final_tokens"]], ["a", "xy", "b"])
        self.assertEqual([entry["id"] for entry in trace["final_tokens"]], [4, 1, 5])

    def test_rejects_changed_payload_and_extra_files(self):
        path = self.root / "tokenizer.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            self.tokenizer._validate_checksums()
        _checksums(self.root)
        (self.root / "extra.txt").write_text("unexpected", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inventory mismatch"):
            Tokenizer(self.root)

    def test_rejects_unsafe_duplicate_and_malformed_checksum_lines(self):
        path = self.root / "checksums.sha256"
        original = path.read_text(encoding="utf-8")
        for relative in ("../tokenizer.json", "C:/tokenizer.json", "..\\tokenizer.json", "/tokenizer.json"):
            path.write_text("0" * 64 + "  " + relative + "\n", encoding="utf-8")
            with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, "unsafe"):
                Tokenizer(self.root)
        path.write_text(original + original.splitlines()[0] + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            Tokenizer(self.root)
        path.write_text("z" * 64 + "  tokenizer.json\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "malformed"):
            Tokenizer(self.root)

    def test_rejects_manifest_fingerprint_or_identity_changes(self):
        path = self.root / "unigram-manifest.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for key, value in (("actual_vocabulary_size", 999), ("tokenizer_sha256", "0" * 64),
                           ("algorithm", "bpe"), ("artifact_fingerprint", "0" * 64)):
            document = dict(original, **{key: value})
            _write_json(path, document)
            _checksums(self.root)
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "manifest"):
                Tokenizer(self.root)

    def test_rejects_unsupported_model_configuration_with_valid_checksums(self):
        path = self.root / "tokenizer.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for key, value in (("type", "BPE"), ("unk_id", 0), ("byte_fallback", True),
                           ("vocab", [["a", float("nan")]])):
            document = dict(original, model=dict(original["model"], **{key: value}))
            _write_json(path, document)
            _manifest(self.root, len(document["model"]["vocab"]))
            with self.subTest(key=key), self.assertRaises(ValueError):
                Tokenizer(self.root)

    @unittest.skipUnless(HFTokenizer is not None, "optional HF tokenizers package is not installed")
    def test_tie_and_unknown_fixture_parity_with_hf(self):
        for pieces in ([("a", -1), ("b", -1), ("ab", -2)],
                       [("a", 0), ("aa", 0), ("aaa", 0)],
                       [("ab", -100), ("b", -1)]):
            tokenizer = _artifact(self.root, pieces)
            hf = HFTokenizer.from_file(str(self.root / "tokenizer.json"))
            for text in ("ab", "aaaa", "aaaaa", "axyb", "xyz", "a\U00020000\U00020001b"):
                actual = tokenizer.encode(text)
                expected = hf.encode(text)
                with self.subTest(pieces=pieces, text=text):
                    self.assertEqual(actual.token_strings, tuple(expected.tokens))
                    self.assertEqual(actual.ids, tuple(expected.ids))
                    self.assertEqual(actual.offsets, tuple(expected.offsets))


@unittest.skipUnless(HFTokenizer is not None, "optional HF tokenizers package is not installed")
class SavedArtifactParityTests(unittest.TestCase):
    def test_all_534_reference_forms_and_sentences_at_both_vocabulary_sizes(self):
        root = Path(os.environ.get("UNIGRAM_PARITY_ARTIFACT_ROOT", BACKEND / "tokenizer" / "artifacts"))
        reference = REPO / "experiments" / "tokenizer_selection_v1" / "data" / "reference-morphology.csv"
        if not reference.is_file():
            self.skipTest("research morphology reference is absent from this app-only checkout")
        with reference.open(encoding="utf-8", newline="") as stream:
            texts = [row["surface"] for row in csv.DictReader(stream)]
        self.assertEqual(len(texts), 534)
        texts += [
            "Masánting ya ing pamag-aral. Maligaya ang mga bata!",
            "pa\u0301ra at e\u0301dukasyon", "a\t  b\r\nc", "  Magandang araw!  ",
            "pamag-aral king bale, 'di ba?", "a\U00020000\U00020001b \U0001fae0\U0001fae8!",
            "\U00020000\U00020001xyz", "123,456.78\u00a0at 2026", "a\u200db", "",
        ]
        for size in (6080, 8192):
            path = root / f"unigram-lm-{size}"
            if not path.is_dir():
                path = root / f"vocab-{size}"
            self.assertTrue(path.is_dir(), f"saved {size}-token Unigram artifact is absent")
            tokenizer = Tokenizer(path)
            hf = HFTokenizer.from_file(str(path / "tokenizer.json"))
            self.assertEqual(tokenizer.vocabulary_size, size)
            for text in texts:
                normalized = unicodedata.normalize("NFC", text)
                pieces, identifiers, offsets = [], [], []
                for pretoken in _pretokenize(normalized):
                    encoded = hf.encode(pretoken.surface)
                    pieces.extend(encoded.tokens)
                    identifiers.extend(encoded.ids)
                    offsets.extend((start + pretoken.start, end + pretoken.start)
                                   for start, end in encoded.offsets)
                actual = tokenizer.encode(text)
                with self.subTest(size=size, text=text):
                    self.assertEqual(actual.normalized_text, normalized)
                    self.assertEqual(actual.token_strings, tuple(pieces))
                    self.assertEqual(actual.ids, tuple(identifiers))
                    self.assertEqual(actual.offsets, tuple(offsets))
                    self.assertEqual(tokenizer.decode(actual.ids), hf.decode(identifiers))
                    self.assertEqual(tokenizer.decode(actual.ids, skip_special_tokens=False),
                                     hf.decode(identifiers, skip_special_tokens=False))
                    self.assertEqual("".join(actual.token_strings), normalized)


if __name__ == "__main__":
    unittest.main()
