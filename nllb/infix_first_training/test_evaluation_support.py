"""Check evaluation provenance and progress without importing GPU libraries."""

import contextlib
import copy
import csv
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluation = load_module("infix_evaluation_support_test_module", HERE / "evaluation_support.py")
support = load_module("infix_evaluation_training_support_test_module", HERE / "training_support.py")


class EvaluationProgressTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.identity = dict(tokenizer_variant="infix_first_penalty48", weights_sha256="a" * 64)
        self.rows = [dict(id="one", raw_source=" raw source ", raw_target="raw target")]
        self.record = dict(id="one", source=" raw source ", target="raw target",
                           prediction="a prediction", output_limit_hit=False)

    def save_progress(self, records, identity=True, tail=""):
        if identity:
            evaluation.save_json(self.root / "evaluation_identity.json", self.identity)
        self.path = self.root / "predictions.jsonl"
        self.path.write_text("".join(json.dumps(r) + "\n" for r in records) + tail,
                             encoding="utf-8")

    def test_predictions_without_identity_are_rejected_without_relabeling_or_rewriting(self):
        self.save_progress([self.record], identity=False)
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "without their saved identity"):
            evaluation._prepare_evaluation_progress(self.root, self.identity, self.rows)
        self.assertFalse((self.root / "evaluation_identity.json").exists())
        self.assertEqual(self.path.read_bytes(), before)

    def test_fresh_or_empty_progress_can_start_with_a_new_identity(self):
        self.save_progress([], identity=False)
        path, completed = evaluation._prepare_evaluation_progress(self.root, self.identity, self.rows)
        self.assertEqual(path, self.path)
        self.assertEqual(completed, [])
        self.assertEqual(json.loads((self.root / "evaluation_identity.json").read_text()), self.identity)

    def test_cross_variant_or_weight_identity_is_rejected_before_progress_rewrite(self):
        self.save_progress([self.record])
        before = self.path.read_bytes()
        for field, value in (("tokenizer_variant", "infix_first_penalty16"),
                             ("weights_sha256", "b" * 64)):
            changed = {**self.identity, field: value}
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "resume identity mismatch"):
                evaluation._prepare_evaluation_progress(self.root, changed, self.rows)
            self.assertEqual(self.path.read_bytes(), before)

    def test_matching_prefix_survives_an_interrupted_last_record(self):
        self.save_progress([self.record], tail='{"id":')
        path, completed = evaluation._prepare_evaluation_progress(self.root, self.identity, self.rows)
        self.assertEqual(completed, [self.record])
        self.assertEqual(path.read_text(), json.dumps(self.record, ensure_ascii=False) + "\n")

    def test_changed_raw_rows_or_extra_records_cannot_resume(self):
        for records in ([{**self.record, "source": "normalized source"}],
                        [self.record, self.record]):
            self.save_progress(records)
            before = self.path.read_bytes()
            with self.subTest(records=records), self.assertRaisesRegex(ValueError, "row mismatch|extra rows"):
                evaluation._prepare_evaluation_progress(self.root, self.identity, self.rows)
            self.assertEqual(self.path.read_bytes(), before)


class Current32ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.release = ROOT / "release-assets/infix_first_training"
        build = json.loads((cls.release / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
        cls.reference = build["current32_reference"]
        cls.archive = cls.release / "current_weighted32_reference.zip"
        cls.baseline = json.loads((ROOT / "nllb/checkpoints/plain_bpe/manifest.json").read_text())
        cls.splits = json.loads((ROOT / "nllb/checkpoints/plain_bpe/split_manifest.json").read_text())

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def verify(self, path, search_roots=(), **changes):
        arguments = dict(path=path, search_roots=search_roots, work=self.root / "work",
                         expected_zip_sha=self.reference["zip_sha256"],
                         expected_manifest_sha=self.reference["manifest_sha256"],
                         data_sha=self.baseline["identity"]["data_sha256"],
                         base_revision=self.baseline["revision"],
                         helper_sha=self.baseline["identity"]["helper_sha256"],
                         target_sha=evaluation.digest(ROOT / "nllb/checkpoints/plain_bpe/target_tokenizer/tokenizer.json"),
                         expected_cfg=self.baseline["cfg"], expected_splits=self.splits)
        arguments.update(changes)
        with mock.patch.dict(sys.modules, {"training_support": support}):
            return evaluation.verify_reference(**arguments)

    def expanded(self):
        return support.extract_safe_zip(self.archive, self.root / "expanded")

    def test_actual_current32_zip_and_expanded_discovery_keep_the_exact_source_weights(self):
        bundle, info = self.verify(self.archive)
        self.assertEqual(info["tokenizer_variant"], "weighted_penalty32")
        self.assertEqual(info["completed_epochs"], 30)
        self.assertEqual(info["selected_epoch"], 30)
        self.assertEqual(evaluation.digest(bundle / "best_source.safetensors"), self.reference["weights_sha256"])
        self.assertFalse((bundle / "last.pt").exists())
        expanded = self.expanded()
        discovered, second = self.verify("", [expanded])
        self.assertEqual(discovered, expanded / "morph_bpe")
        self.assertEqual(second, info)

    def test_changed_reference_zip_is_rejected_before_extraction(self):
        changed = self.root / self.archive.name
        shutil.copy2(self.archive, changed)
        with changed.open("ab") as handle:
            handle.write(b"changed reference")
        with self.assertRaisesRegex(ValueError, "reference ZIP hash mismatch"):
            self.verify(changed)
        self.assertFalse((self.root / "work/current32_reference").exists())

    def test_changed_expanded_weights_are_rejected_by_the_pinned_inventory(self):
        expanded = self.expanded()
        (expanded / "morph_bpe/best_source.safetensors").write_bytes(b"wrong candidate weights")
        with self.assertRaisesRegex(ValueError, "reference checksum mismatch"):
            self.verify(expanded)

    def test_current32_is_rejected_for_a_different_training_recipe_or_ordered_split(self):
        expanded = self.expanded()
        changed_splits = copy.deepcopy(self.splits)
        changed_splits["validation"] = list(reversed(changed_splits["validation"]))
        for changes in (dict(expected_cfg={**self.baseline["cfg"], "seed": 43}),
                        dict(expected_splits=changed_splits)):
            with self.subTest(changes=list(changes)), self.assertRaisesRegex(ValueError, "matched installed"):
                self.verify(expanded, **changes)


class ComparisonProtocolTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.candidate = self.root / "candidate"
        self.reference = self.root / "reference"
        self.identity = dict(split="validation", data_sha256="d" * 64,
                             row_ids_sha256="r" * 64, base_revision="pinned-revision",
                             beams=4, max_new_tokens=160, source_limit=256, precision="fp32",
                             torch="matched", transformers="4.48.3", sacrebleu="2.5.1",
                             helper_sha256="h" * 64, target_tokenizer_sha256="t" * 64,
                             evaluation_support_sha256="e" * 64)
        self.metrics = {"BLEU": dict(score=20.0, signature="matched BLEU signature"),
                        "chrF++": dict(score=40.0, signature="matched chrF signature")}
        for root, variant in ((self.candidate, "infix_first_penalty48"),
                              (self.reference, "weighted_penalty32")):
            evaluation.save_json(root / "validation/evaluation_identity.json",
                                 {**self.identity, "tokenizer_variant": variant})
            evaluation.save_json(root / "validation/metrics.json", self.metrics)

    def compare(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return evaluation.compare_scores(self.candidate, self.reference, "validation")

    def test_matching_protocol_writes_correct_labeled_score_differences(self):
        changed = copy.deepcopy(self.metrics)
        changed["BLEU"]["score"] = 21.5
        evaluation.save_json(self.candidate / "validation/metrics.json", changed)
        with self.compare().open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["metric"] for row in rows], ["BLEU", "chrF++"])
        self.assertEqual(rows[0]["candidate"], "infix_first_penalty48")
        self.assertEqual(float(rows[0]["candidate_minus_current32"]), 1.5)

    def test_different_decoding_rows_or_environment_never_write_a_comparison(self):
        for key, value in (("beams", 1), ("row_ids_sha256", "other rows"),
                           ("precision", "fp16"), ("transformers", "other version"),
                           ("evaluation_support_sha256", "other evaluator")):
            evaluation.save_json(self.reference / "validation/evaluation_identity.json",
                                 {**self.identity, "tokenizer_variant": "weighted_penalty32", key: value})
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "different rows, settings or environments"):
                self.compare()
            self.assertFalse((self.candidate / "validation_vs_current32.csv").exists())

    def test_different_metric_signatures_never_write_a_comparison(self):
        metrics = copy.deepcopy(self.metrics)
        metrics["BLEU"]["signature"] = "different tokenization"
        evaluation.save_json(self.reference / "validation/metrics.json", metrics)
        with self.assertRaisesRegex(ValueError, "different metric signatures"):
            self.compare()
        self.assertFalse((self.candidate / "validation_vs_current32.csv").exists())


if __name__ == "__main__":
    unittest.main()
