"""Data-protocol regression tests. No Torch, model downloads, or training."""

import copy
import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

from training_support import DATA_POLICY, read_matched_csv


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


if __name__ == "__main__":
    unittest.main()
