"""Data and variant guard tests without Torch, model downloads, or training."""

import copy
import csv
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "infix_training_support_test_module", Path(__file__).with_name("training_support.py"),
)
support = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(support)
DATA_POLICY, read_matched_csv = support.DATA_POLICY, support.read_matched_csv


class MatchedCsvTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.csv_path = Path(self.temporary.name) / "data.csv"

    def fixture(self, rows, excluded=(), duplicates=None):
        with self.csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["id", "source", "target", "split", "group_id"])
            writer.writeheader()
            writer.writerows(rows)
        checksum = hashlib.sha256(self.csv_path.read_bytes()).hexdigest()
        ids = {
            split: [row["id"] for row in rows if row["split"] == split and row["id"] not in excluded]
            for split in ("train", "validation", "test")
        }
        audit = {
            "csv_sha256": checksum,
            "original_counts": {
                split: sum(row["split"] == split for row in rows) for split in ids
            },
            "used_counts": {split: len(values) for split, values in ids.items()},
            "excluded_train_ids": list(excluded),
            "policy": DATA_POLICY,
            "within_split_duplicate_excess": duplicates or {split: 0 for split in ids},
        }
        return checksum, audit, ids

    @staticmethod
    def row(identifier, source, split, group=None, target="Filipino reference"):
        return {"id": identifier, "source": source, "target": target,
                "split": split, "group_id": group or identifier}

    def ordinary(self):
        return [self.row("t1", "training source", "train"),
                self.row("v1", "validation source", "validation"),
                self.row("e1", "test source", "test")]

    def test_preserves_duplicates_order_and_raw_references(self):
        rows = [self.row("t1", "  Caf\u00e9\tword ", "train", target=" raw\t target "),
                self.row("t2", "CAFE\u0301 word", "train"),
                self.row("v1", "validation source", "validation"),
                self.row("e1", "test source", "test")]
        expected = self.fixture(rows, duplicates={"train": 1, "validation": 0, "test": 0})
        splits, audit = read_matched_csv(self.csv_path, *expected)
        self.assertEqual([row["id"] for row in splits["train"]], ["t1", "t2"])
        self.assertEqual(splits["train"][0]["source"], "  Caf\u00e9\tword ")
        self.assertEqual(splits["train"][1]["source"], "CAFE\u0301 word")
        self.assertEqual(splits["train"][0]["raw_target"], " raw\t target ")
        self.assertEqual(splits["train"][0]["target"], " raw\t target ")
        self.assertEqual(audit["within_split_duplicate_excess"]["train"], 1)

    def test_excludes_only_training_overlap_and_preserves_evaluation(self):
        rows = [self.row("t1", "unrelated source", "train"),
                self.row("t2", "  CAFE\u0301\tword ", "train"),
                self.row("v1", "Caf\u00e9 word", "validation"),
                self.row("e1", "test source", "test")]
        expected = self.fixture(rows, excluded=["t2"])
        splits, audit = read_matched_csv(self.csv_path, *expected)
        self.assertEqual([row["id"] for row in splits["train"]], ["t1"])
        self.assertEqual([row["id"] for row in splits["validation"]], ["v1"])
        self.assertEqual([row["id"] for row in splits["test"]], ["e1"])
        self.assertEqual(audit["excluded_train_ids"], ["t2"])

    def test_counts_duplicates_after_overlap_exclusion(self):
        rows = [self.row("t1", "retained source", "train"),
                self.row("t2", "  evaluation\t source ", "train"),
                self.row("t3", "EVALUATION source", "train"),
                self.row("v1", "evaluation source", "validation"),
                self.row("e1", "test source", "test")]
        expected = self.fixture(rows, excluded=["t2", "t3"])
        splits, audit = read_matched_csv(self.csv_path, *expected)
        self.assertEqual([row["id"] for row in splits["train"]], ["t1"])
        self.assertEqual(audit["within_split_duplicate_excess"]["train"], 0)
        self.assertEqual(audit["original_counts"]["train"], 3)

    def test_rejects_group_leakage_even_when_train_overlap_would_be_excluded(self):
        rows = [self.row("t1", "retained source", "train"),
                self.row("t2", "evaluation source", "train", group="shared-document"),
                self.row("v1", "evaluation source", "validation", group="shared-document"),
                self.row("e1", "test source", "test")]
        expected = self.fixture(rows, excluded=["t2"])
        with self.assertRaisesRegex(ValueError, "Document/group leakage across original splits"):
            read_matched_csv(self.csv_path, *expected)

    def test_rejects_changed_csv_even_when_rows_remain_parseable(self):
        expected = self.fixture(self.ordinary())
        with self.csv_path.open("a", encoding="utf-8") as handle:
            handle.write("\n")
        with self.assertRaisesRegex(ValueError, "CSV SHA-256"):
            read_matched_csv(self.csv_path, *expected)

    def test_rejects_reordered_baseline_split_ids(self):
        rows = self.ordinary() + [self.row("t2", "different train source", "train")]
        checksum, audit, ids = self.fixture(rows)
        ids["train"].reverse()
        with self.assertRaisesRegex(ValueError, "Ordered split IDs"):
            read_matched_csv(self.csv_path, checksum, audit, ids)

    def test_rejects_duplicate_id(self):
        rows = self.ordinary() + [self.row("t1", "other source", "train")]
        expected = self.fixture(rows)
        with self.assertRaisesRegex(ValueError, "Duplicate record ID"):
            read_matched_csv(self.csv_path, *expected)

    def test_rejects_group_leakage_in_retained_rows(self):
        rows = self.ordinary()
        rows[0]["group_id"] = rows[1]["group_id"] = "shared-document"
        expected = self.fixture(rows)
        with self.assertRaisesRegex(ValueError, "Document/group leakage"):
            read_matched_csv(self.csv_path, *expected)

    def test_rejects_validation_test_overlap_without_removing_rows(self):
        rows = self.ordinary()
        rows[2]["source"] = rows[1]["source"].upper()
        expected = self.fixture(rows)
        with self.assertRaisesRegex(ValueError, "validation and test"):
            read_matched_csv(self.csv_path, *expected)

    def test_rejects_audit_count_mismatch(self):
        checksum, audit, ids = self.fixture(self.ordinary())
        audit = copy.deepcopy(audit)
        audit["used_counts"]["train"] += 1
        with self.assertRaisesRegex(ValueError, "Baseline data audit mismatch: used_counts"):
            read_matched_csv(self.csv_path, checksum, audit, ids)


class FakeTensor:
    """Only the tensor metadata/predicate contract is exercised locally."""
    shape = (6080, 1024)
    dtype = "torch.float32"
    finite = True


class VariantGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cfg = {"epochs": 30, "seed": 42}

    def fixture(self, penalty=48):
        root = self.root / f"penalty-{penalty}"
        artifact = root / "source_artifact"
        artifact.mkdir(parents=True)
        fields = support.variant_fields(penalty)
        metadata = {key: fields[key] for key in (
            "crossing_penalty", "priority_order", "infix_token_budget", "root_token_budget",
            "affix_token_budget", "infixes_have_separate_training_role",
        )}
        metadata.update(algorithm="infix_priority_then_weighted", vocabulary_budget=6080,
                        lexicon_used_at_runtime=False, surface_specific_overrides=[])
        document = {
            "metadata": metadata,
            "vocabulary": [{"id": index, "token": f"fixture-{index}"} for index in range(6080)],
            "merges": [{"rank": index, "result": token} for index, token in enumerate(
                ["in", "um", "IN", "UM"] + [f"merge-{i}" for i in range(4484)]
            )],
        }
        core = {}
        for name in ("tokenizer.json", "vocab.json", "merges.json", "normalization.json",
                     "pretokenizer.json", "special_tokens.json"):
            contents = document if name == "tokenizer.json" else {"synthetic": name}
            path = artifact / name
            path.write_text(json.dumps(contents), encoding="utf-8")
            core[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        fingerprint = hashlib.sha256(f"fixture-infix-{penalty}".encode()).hexdigest()
        manifest = {
            "artifact_fingerprint": fingerprint, "actual_vocabulary_size": 6080,
            "target_vocabulary_size": 6080, "merge_count": 4488,
            "artifact_type": "kapampangan_morphbpe", "protected_boundary_merge_violations": 0,
            "metadata": metadata, "core_file_sha256": core,
        }
        (artifact / "tokenizer-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (artifact / "TOKENIZER_CARD.md").write_text("Synthetic guard fixture.", encoding="utf-8")
        inventory = "".join(
            hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.name + "\n"
            for path in sorted(artifact.iterdir())
        )
        (artifact / "checksums.sha256").write_text(inventory, encoding="utf-8")
        identity = dict(
            condition="morph_bpe", model_id="fixture-model", revision="fixture-revision",
            tokenizer_fingerprint=fingerprint, beams=4, max_new_tokens=160,
            runtime_controls={"gradient_checkpointing": True}, **fields,
        )
        for name, key in support.RUNTIME_IDENTITY_FILES.items():
            path = root / name
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(("Synthetic file: " + name).encode())
            identity[key] = hashlib.sha256(path.read_bytes()).hexdigest()
        info = dict(
            model_id=identity["model_id"], revision=identity["revision"],
            source_vocab_size=6080, source_format="kapampangan_project",
            source_id_mapping="swap_0_1", adaptation="source_embedding_only",
            target_language="tgl_Latn", source_marker="<s>", training_status="prepared",
            identity=identity, cfg=self.cfg, **fields,
        )
        return root, identity, info, manifest, document

    def checkpoint(self, identity):
        return dict(
            identity=copy.deepcopy(identity), cfg=dict(self.cfg), source_weight=FakeTensor(),
            next_epoch=2, history=[{"epoch": 1, "train_loss": 2.1, "validation_loss": 1.9},
                                   {"epoch": 2, "train_loss": 1.8, "validation_loss": 1.7}],
            best=1.7, optimizer={"state": "synthetic"}, scaler={},
        )

    @staticmethod
    def finite(tensor):
        return tensor.finite

    def report_fixture(self, root, identity, info):
        info.update(training_status="completed", completed_epochs=2, selected_epoch=2,
                    selected_validation_loss=1.7)
        weights = root / "best_source.safetensors"
        weights.write_bytes(b"Synthetic weights, never loaded as a tensor")
        return dict(
            status="passed", identity_sha256=support.identity_digest(identity),
            weights_sha256=hashlib.sha256(weights.read_bytes()).hexdigest(),
            tokenizer_sha256=identity["tokenizer_sha256"], selected_epoch=2,
            base_revision=identity["revision"], beams=4, max_new_tokens=160, precision="fp32",
            **support.variant_fields(identity["crossing_penalty"]),
        )

    def test_two_variants_have_distinct_identity_and_independent_metadata(self):
        fields48 = support.variant_fields(48)
        fields16 = support.variant_fields(16)
        self.assertEqual(fields48["tokenizer_variant"], "infix_first_penalty48")
        self.assertEqual(fields16["tokenizer_variant"], "infix_first_penalty16")
        fields48["priority_order"].append("root")
        self.assertEqual(support.variant_fields(48)["priority_order"], ["infix", "weighted"])
        for invalid in (8, 32, 0, True, "48"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                support.variant_fields(invalid)

    def test_artifact_guards_actual_penalty_algorithm_and_schedule(self):
        _, identity, _, manifest, document = self.fixture()
        support.validate_variant_artifact(manifest, document, 48, identity["tokenizer_fingerprint"])
        for name, value in (("crossing_penalty", 16), ("algorithm", "ordinary_weighted"),
                            ("priority_order", ["root", "affix", "weighted"]),
                            ("lexicon_used_at_runtime", True)):
            for location in ("manifest", "document"):
                changed_manifest, changed_document = copy.deepcopy(manifest), copy.deepcopy(document)
                target = changed_manifest if location == "manifest" else changed_document
                target["metadata"][name] = value
                with self.subTest(name=name, location=location), self.assertRaises(ValueError):
                    support.validate_variant_artifact(
                        changed_manifest, changed_document, 48, identity["tokenizer_fingerprint"],
                    )

    def test_runtime_guards_all_identity_files_and_full_inventory(self):
        root, identity, _, _, _ = self.fixture()
        support.validate_runtime_files(root, identity)
        for name in support.RUNTIME_IDENTITY_FILES:
            path = root / name
            original = path.read_bytes()
            path.write_bytes(original + b"changed")
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "identity mismatch"):
                support.validate_runtime_files(root, identity)
            path.write_bytes(original)
        (root / "source_artifact/vocab.json").write_bytes(b"changed vocabulary")
        with self.assertRaisesRegex(ValueError, "core inventory mismatch"):
            support.validate_runtime_files(root, identity)

    def test_runtime_rejects_an_inventory_that_omits_a_core_file(self):
        root, identity, _, _, _ = self.fixture()
        path = root / "source_artifact/checksums.sha256"
        path.write_text("\n".join(line for line in path.read_text().splitlines()
                                  if not line.endswith("vocab.json")) + "\n")
        with self.assertRaisesRegex(ValueError, "cover every artifact file"):
            support.validate_runtime_files(root, identity)

    def test_manifest_rejects_cross_variant_and_changed_top_level_metadata(self):
        _, identity48, info48, _, _ = self.fixture(48)
        _, identity16, info16, _, _ = self.fixture(16)
        support.validate_saved_manifest(info48, identity48, self.cfg)
        with self.assertRaisesRegex(ValueError, "identity/configuration"):
            support.validate_saved_manifest(info16, identity48, self.cfg)
        with self.assertRaisesRegex(ValueError, "identity/configuration"):
            support.validate_saved_manifest(info48, identity16, self.cfg)
        for name, value in (("crossing_penalty", 16), ("tokenizer_variant", "weighted_penalty48"),
                            ("weighted_penalty_used", False), ("source_id_mapping", "identity")):
            altered = copy.deepcopy(info48)
            altered[name] = value
            with self.subTest(name=name), self.assertRaises(ValueError):
                support.validate_saved_manifest(altered, identity48, self.cfg)

    def test_checkpoint_rejects_wrong_variant_tensor_or_history(self):
        _, identity, _, _, _ = self.fixture()
        good = self.checkpoint(identity)
        self.assertEqual(support.validate_checkpoint(good, identity, self.cfg, self.finite), 2)
        changes = [
            ("identity", {**identity, "crossing_penalty": 16}),
            ("cfg", {**self.cfg, "seed": 999}),
            ("next_epoch", 31), ("next_epoch", True), ("best", 1.9),
            ("history", [{"epoch": 1, "train_loss": float("nan"), "validation_loss": 1.7}]),
            ("history", [{"epoch": 2, "train_loss": 1.8, "validation_loss": 1.7}]),
            ("optimizer", None),
        ]
        for name, value in changes:
            changed = copy.deepcopy(good)
            changed[name] = value
            with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                support.validate_checkpoint(changed, identity, self.cfg, self.finite)
        for name, value in (("shape", (6079, 1024)), ("dtype", "torch.float16"), ("finite", False)):
            tensor = FakeTensor()
            setattr(tensor, name, value)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "source embedding"):
                support.validate_best_weights(tensor, self.finite)

    def test_checkpoint_checks_finite_train_loss_with_actual_helper_field_names(self):
        _, identity, _, _, _ = self.fixture()
        saved = self.checkpoint(identity)
        saved["history"][0]["train_loss"] = float("inf")
        with self.assertRaisesRegex(ValueError, "Nonfinite"):
            support.validate_checkpoint(saved, identity, self.cfg, self.finite)
        saved = self.checkpoint(identity)
        saved["history"][0].pop("train_loss")
        saved["history"][0]["training_loss"] = 2.1
        with self.assertRaisesRegex(ValueError, "invalid resumed history"):
            support.validate_checkpoint(saved, identity, self.cfg, self.finite)

    def test_inference_report_requires_exact_weights_variant_and_selection(self):
        root, identity, info, _, _ = self.fixture()
        report = self.report_fixture(root, identity, info)
        self.assertTrue(support.reload_report_matches(report, info, root))
        for name, value in (("crossing_penalty", 16), ("tokenizer_variant", "infix_first_penalty16"),
                            ("selected_epoch", 1), ("identity_sha256", "0" * 64),
                            ("base_revision", "different-base"), ("weights_sha256", "0" * 64),
                            ("precision", "fp16"), ("beams", 1)):
            changed = dict(report)
            changed[name] = value
            with self.subTest(name=name):
                self.assertFalse(support.reload_report_matches(changed, info, root))
        (root / "best_source.safetensors").write_bytes(b"Wrong weights")
        self.assertFalse(support.reload_report_matches(report, info, root))

    def test_inference_report_skips_prepared_runs_and_missing_report(self):
        root, identity, info, _, _ = self.fixture()
        self.assertFalse(support.reload_report_matches(None, info, root))
        report = self.report_fixture(root, identity, info)
        self.assertFalse(support.reload_report_matches(None, info, root))
        info["training_status"] = "prepared"
        self.assertFalse(support.reload_report_matches(report, info, root))

    def test_completed_manifest_requires_actual_epoch_selection(self):
        _, identity, info, _, _ = self.fixture()
        info["training_status"] = "completed"
        with self.assertRaisesRegex(ValueError, "epoch/selection"):
            support.validate_saved_manifest(info, identity, self.cfg)

    def test_safe_extraction_rejects_traversal_duplicates_and_links_before_writing(self):
        for name in ("../outside.txt", "/absolute.txt", "C:/absolute.txt", "folder\\file.txt"):
            archive = self.root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("safe.txt", b"Must not be extracted before validation")
                raw_entry = zipfile.ZipInfo("placeholder")
                raw_entry.filename = name
                handle.writestr(raw_entry, b"unsafe")
            destination = self.root / "extract"
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "Unsafe ZIP"):
                support.extract_safe_zip(archive, destination)
            self.assertFalse((destination / "safe.txt").exists())
        archive = self.root / "duplicate.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("same.txt", b"one")
            handle.writestr("SAME.txt", b"two")
        with self.assertRaisesRegex(ValueError, "Duplicate ZIP"):
            support.extract_safe_zip(archive, self.root / "duplicates")
        archive = self.root / "link.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            info = zipfile.ZipInfo("link")
            info.external_attr = 0o120777 << 16
            handle.writestr(info, "outside")
        with self.assertRaisesRegex(ValueError, "ZIP links"):
            support.extract_safe_zip(archive, self.root / "links")

    def test_safe_extraction_preserves_valid_member_bytes(self):
        archive = self.root / "safe.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("nested/file.txt", b"unchanged")
        root = support.extract_safe_zip(archive, self.root / "safe-extract")
        self.assertEqual((root / "nested/file.txt").read_bytes(), b"unchanged")


if __name__ == "__main__":
    unittest.main()
