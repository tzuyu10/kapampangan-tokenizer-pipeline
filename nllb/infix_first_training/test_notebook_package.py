"""Exercise both generated Kaggle notebooks without models, downloads, or training.

The real notebook input and export cells run against disposable local fixtures.
Every code cell is also compiled, but GPU/model cells are never executed here.
"""

import ast
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEMP_ROOT = ROOT / ".test-tmp" / "infix-first-notebooks"
PENALTIES = (48, 16)
ARTIFACT_ROOT = Path(
    "C:/Users/Gabo/.codex/visualizations/2026/10/10/"
    "01a123b1-9446-7a33-b574-09074e63c7e7/infix_penalty_comparison"
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def temporary_directory():
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(dir=TEMP_ROOT)


@contextlib.contextmanager
def isolated_support():
    """Notebook imports must not reuse a previously imported penalty32 helper."""
    original_path = list(sys.path)
    previous = sys.modules.pop("training_support", None)
    try:
        yield
    finally:
        sys.path[:] = original_path
        sys.modules.pop("training_support", None)
        if previous is not None:
            sys.modules["training_support"] = previous


class NotebookSpec:
    def __init__(self, penalty):
        self.penalty = penalty
        self.path = ROOT / "notebooks" / (
            f"NLLB_600M_InfixFirst_Penalty{penalty}_Source_Embedding_Training.ipynb"
        )
        self.notebook = json.loads(self.path.read_text(encoding="utf-8"))
        self.code = [cell["source"] for cell in self.notebook["cells"]
                     if cell["cell_type"] == "code"]
        config = next(source for source in self.code
                      if "EXPECTED_PACKAGE_SHA256 =" in source)
        self.constants = {}
        for node in ast.parse(config).body:
            if not isinstance(node, ast.Assign):
                continue
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.constants[target.id] = value
        candidates = [*HERE.glob("*.zip"),
                      *(ROOT / "release-assets" / "infix_first_training").glob("*.zip")]
        matches = [path for path in candidates
                   if digest(path) == self.constants["EXPECTED_PACKAGE_SHA256"]]
        if len(matches) != 1:
            raise ValueError(f"Expected one checksummed penalty{penalty} input ZIP: {matches}")
        self.package = matches[0]
        with zipfile.ZipFile(self.package) as archive:
            self.package_manifest = json.loads(archive.read("package_manifest.json"))
        self.verify = next(source for source in self.code if source.startswith("def digest("))
        self.csv = next(source for source in self.code
                        if "from training_support import read_matched_csv" in source)
        self.resume = next(source for source in self.code
                           if source.startswith("identity = dict(baseline['identity'])"))
        self.reload = next(source for source in self.code if source.startswith("reload_info ="))
        self.export = next(source for source in self.code if "INFERENCE_ZIP = " in source)


class NotebookPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.specs = {penalty: NotebookSpec(penalty) for penalty in PENALTIES}

    @staticmethod
    def _namespace(spec, root, input_path=""):
        work = root / "working"
        work.mkdir(exist_ok=True)
        return dict(spec.constants, Path=Path, os=os, json=json, hashlib=hashlib,
                    zipfile=zipfile, shutil=shutil, tempfile=tempfile,
                    importlib=__import__("importlib"), sys=sys, WORK=work,
                    RUNS=work / "runs", SEARCH_ROOTS=[root / "kaggle_input"],
                    INPUT_PATH=str(input_path), DATA_CSV="")

    @staticmethod
    def _attach(spec, folder, expanded=False):
        folder.mkdir(parents=True, exist_ok=True)
        if expanded:
            destination = folder / f"expanded-penalty{spec.penalty}"
            destination.mkdir()
            with zipfile.ZipFile(spec.package) as archive:
                archive.extractall(destination)
            return destination
        destination = folder / spec.package.name
        shutil.copy2(spec.package, destination)
        return destination

    @staticmethod
    def _execute_inputs(spec, namespace, read_csv=True):
        with contextlib.redirect_stdout(io.StringIO()):
            exec(spec.verify, namespace)
            if read_csv:
                exec(spec.csv, namespace)

    def _assert_data(self, namespace):
        splits = namespace["splits"]
        audit = namespace["data_audit"]
        self.assertEqual(audit["used_counts"],
                         dict(train=12911, validation=1636, test=1659))
        self.assertEqual(audit["within_split_duplicate_excess"],
                         dict(train=60, validation=1, test=1))
        self.assertTrue(namespace["package"]["csv_included"])
        csv_path = Path(namespace["DATA_CSV"])
        original = {row["id"]: row for row in csv.DictReader(
            io.StringIO(csv_path.read_bytes().decode("utf-8-sig"), newline=""))}
        for split, rows in splits.items():
            self.assertEqual([row["id"] for row in rows],
                             namespace["baseline_splits"][split])
            for row in rows:
                with self.subTest(split=split, row_id=row["id"]):
                    self.assertEqual(row["source"], original[row["id"]]["source"])
                    self.assertEqual(row["target"], original[row["id"]]["target"])
                    self.assertEqual(row["raw_source"], row["source"])
                    self.assertEqual(row["raw_target"], row["target"])

    def test_every_code_cell_compiles_and_has_no_saved_execution(self):
        for penalty, spec in self.specs.items():
            for index, cell in enumerate(spec.notebook["cells"]):
                if cell["cell_type"] != "code":
                    continue
                with self.subTest(penalty=penalty, cell=index):
                    compile(cell["source"], f"penalty{penalty}-cell-{index}", "exec")
                    self.assertEqual(cell["outputs"], [])
                    self.assertIsNone(cell["execution_count"])

    def test_zip_inputs_preserve_csv_text_duplicates_and_ordered_splits(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                self._attach(spec, root / "kaggle_input")
                namespace = self._namespace(spec, root)
                with isolated_support():
                    self._execute_inputs(spec, namespace)
                    self._assert_data(namespace)

    def test_expanded_inputs_preserve_csv_text_duplicates_and_ordered_splits(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                self._attach(spec, root / "kaggle_input", expanded=True)
                namespace = self._namespace(spec, root)
                with isolated_support():
                    self._execute_inputs(spec, namespace)
                    self._assert_data(namespace)

    def test_each_variant_discovers_its_own_expanded_input_when_both_are_attached(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                for other in self.specs.values():
                    self._attach(other, root / "kaggle_input", expanded=True)
                namespace = self._namespace(spec, root)
                with isolated_support():
                    self._execute_inputs(spec, namespace, read_csv=False)
                self.assertEqual(namespace["package"]["crossing_penalty"], penalty)

    def test_corrupt_expanded_tokenizer_is_rejected_before_data_loading(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                attached = self._attach(spec, root / "kaggle_input", expanded=True)
                (attached / "source_artifact" / "vocab.json").write_text("{}", encoding="utf-8")
                namespace = self._namespace(spec, root)
                with isolated_support(), self.assertRaisesRegex(ValueError, "checksum mismatch"):
                    self._execute_inputs(spec, namespace)
                self.assertNotIn("splits", namespace)

    def test_corrupt_input_zip_is_rejected_before_unpacking(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                attached = self._attach(spec, root / "kaggle_input")
                with attached.open("ab") as handle:
                    handle.write(b"changed archive bytes")
                namespace = self._namespace(spec, root)
                with isolated_support(), self.assertRaisesRegex(ValueError, "ZIP hash mismatch"):
                    self._execute_inputs(spec, namespace)
                self.assertFalse((namespace["WORK"] / "inputs").exists())

    def test_cross_variant_explicit_zip_and_expanded_inputs_are_rejected(self):
        for penalty, spec in self.specs.items():
            other = self.specs[16 if penalty == 48 else 48]
            for expanded in (False, True):
                with self.subTest(penalty=penalty, expanded=expanded), temporary_directory() as temporary:
                    root = Path(temporary)
                    attached = self._attach(other, root / "kaggle_input", expanded=expanded)
                    namespace = self._namespace(spec, root, input_path=attached)
                    with isolated_support(), self.assertRaisesRegex(ValueError, "hash mismatch"):
                        self._execute_inputs(spec, namespace)
                    self.assertNotIn("splits", namespace)

    def test_injected_trained_weights_are_rejected_as_training_inputs(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                root = Path(temporary)
                attached = self._attach(spec, root / "kaggle_input", expanded=True)
                (attached / "best_source.safetensors").write_bytes(b"old unrelated weights")
                namespace = self._namespace(spec, root)
                with isolated_support(), self.assertRaisesRegex(ValueError, "trained source weights"):
                    self._execute_inputs(spec, namespace)
                self.assertNotIn("splits", namespace)

    def test_input_packages_have_the_same_original_csv_and_no_trained_weights(self):
        csv_bytes = []
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), zipfile.ZipFile(spec.package) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), len(set(names)))
                self.assertFalse(any(name.endswith(".pt") for name in names))
                self.assertFalse(any(Path(name).name == "best_source.safetensors" for name in names))
                self.assertFalse(spec.package_manifest["trained_source_weights_included"])
                self.assertEqual(spec.package_manifest["crossing_penalty"], penalty)
                csv_bytes.append(archive.read("data/kpm_tgl_cleaned.csv"))
                self.assertEqual(hashlib.sha256(csv_bytes[-1]).hexdigest(),
                                 spec.constants["EXPECTED_DATA_SHA256"])
                expected_files = set(spec.package_manifest["files"]) | {"package_manifest.json"}
                self.assertEqual(set(names), expected_files)
                for name, checksum in spec.package_manifest["files"].items():
                    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), checksum)
        self.assertEqual(csv_bytes[0], csv_bytes[1])

    def test_source_artifacts_match_the_original_infix_visualization_bytes(self):
        tokenizer_hashes = []
        for penalty, spec in self.specs.items():
            original = ARTIFACT_ROOT / f"penalty-{penalty}" / f"infix-only-penalty{penalty}"
            with self.subTest(penalty=penalty), zipfile.ZipFile(spec.package) as archive:
                files = [path for path in original.iterdir() if path.is_file()]
                self.assertTrue(files)
                self.assertEqual(
                    {name.removeprefix("source_artifact/") for name in archive.namelist()
                     if name.startswith("source_artifact/")},
                    {path.name for path in files},
                )
                for path in files:
                    self.assertEqual(archive.read("source_artifact/" + path.name), path.read_bytes())
                artifact = json.loads(archive.read("source_artifact/tokenizer-manifest.json"))
                metadata = artifact["metadata"]
                self.assertEqual(artifact["artifact_fingerprint"],
                                 spec.constants["EXPECTED_TOKENIZER_FINGERPRINT"])
                self.assertEqual(artifact["actual_vocabulary_size"], 6080)
                self.assertEqual(metadata["crossing_penalty"], penalty)
                self.assertEqual(metadata["algorithm"], "infix_priority_then_weighted")
                self.assertEqual(metadata["priority_order"], ["infix", "weighted"])
                self.assertEqual(metadata["infix_token_budget"], 32)
                self.assertEqual(metadata["affix_token_budget"], 0)
                self.assertEqual(metadata["root_token_budget"], 0)
                self.assertFalse(metadata["selection_performed"])
                self.assertFalse(metadata["held_out_test_used"])
                tokenizer_hashes.append(hashlib.sha256(
                    archive.read("source_artifact/tokenizer.json")).hexdigest())
        self.assertNotEqual(tokenizer_hashes[0], tokenizer_hashes[1])

    def test_variant_defaults_use_distinct_run_names_and_preserve_test_lock(self):
        names = [spec.constants["RUN_NAME"] for spec in self.specs.values()]
        self.assertEqual(len(names), len(set(names)))
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty):
                self.assertFalse(spec.constants["RESUME"])
                self.assertEqual(spec.constants["RESUME_BUNDLE"], "")
                self.assertFalse(spec.constants["RUN_TEST"])
                self.assertFalse(spec.constants["RUN_VALIDATION_TRANSLATIONS"])

    def _prepared_namespace(self, spec, root):
        self._attach(spec, root / "kaggle_input")
        namespace = self._namespace(spec, root)
        self._execute_inputs(spec, namespace)
        baseline = namespace["baseline"]
        namespace.update(
            OUT=namespace["RUNS"] / "morph_bpe" / "fixture",
            RUN_NAME="fixture", RESUME=False, RESUME_BUNDLE="",
            CFG=dict(baseline["cfg"]), MODEL_ID=baseline["model_id"],
            REVISION=baseline["revision"],
            SOURCE_LIMIT=baseline["identity"]["source_limit"],
            TARGET_LIMIT=baseline["identity"]["target_limit"],
            BEAMS=baseline["identity"]["beams"],
            MAX_NEW_TOKENS=baseline["identity"]["max_new_tokens"],
            RUNTIME_CONTROLS=dict(
                gradient_checkpointing=True, checkpoint_use_reentrant=False,
                cudnn_benchmark=False, cuda_matmul_allow_tf32=False,
                cudnn_allow_tf32=False, deterministic_algorithms=True,
                deterministic_warn_only=True,
            ),
        )
        body = ast.parse(spec.resume).body
        boundary = next(index for index, node in enumerate(body)
                        if isinstance(node, ast.If) and "RESUME_BUNDLE" in ast.dump(node.test))
        prefix = ast.Module(body=body[:boundary], type_ignores=[])
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(prefix, "actual-resume-identity", "exec"), namespace)
        return namespace

    @staticmethod
    def _write_json(path, value):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")

    def _bundle_fixture(self, spec, root, status="completed"):
        namespace = self._prepared_namespace(spec, root)
        out = namespace["OUT"]
        out.mkdir(parents=True)
        inputs = namespace["INPUT_ROOT"]
        for folder in ("source_artifact", "runtime", "target_tokenizer"):
            shutil.copytree(inputs / folder, out / folder)
        for path in inputs.glob("*.py"):
            shutil.copy2(path, out / path.name)
        shutil.copy2(inputs / "reference/plain_bpe/split_manifest.json", out / "split_manifest.json")
        support = sys.modules["training_support"]
        fields = support.variant_fields(spec.penalty)
        manifest = dict(
            **fields, identity=namespace["identity"], cfg=namespace["CFG"],
            model_id=namespace["MODEL_ID"], revision=namespace["REVISION"],
            source_vocab_size=6080, source_format="kapampangan_project",
            source_id_mapping="swap_0_1", adaptation="source_embedding_only",
            target_language="tgl_Latn", source_marker="<s>",
            training_status=status, selected_epoch=3,
        )
        if status == "completed":
            manifest.update(completed_epochs=3, selected_validation_loss=1.5)
        self._write_json(out / "manifest.json", manifest)
        (out / "last.pt").write_bytes(b"fixture optimizer checkpoint; never deserialized")
        (out / "best_source.safetensors").write_bytes(b"fixture selected weights; never deserialized")
        namespace.update(
            validate_saved_manifest=support.validate_saved_manifest,
            validate_runtime_files=support.validate_runtime_files,
            reload_report_matches=support.reload_report_matches,
            identity_digest=support.identity_digest,
        )
        report = dict(
            **fields, status="passed", identity_sha256=support.identity_digest(namespace["identity"]),
            weights_sha256=digest(out / "best_source.safetensors"),
            tokenizer_sha256=namespace["identity"]["tokenizer_sha256"],
            base_revision=namespace["REVISION"], selected_epoch=3,
            beams=namespace["BEAMS"], max_new_tokens=namespace["MAX_NEW_TOKENS"],
            precision="fp32",
        )
        self._write_json(out / "reload_check.json", report)
        return namespace, manifest, report

    def test_cross_variant_resume_roots_and_zips_are_rejected_before_copying_output(self):
        for penalty, spec in self.specs.items():
            other = self.specs[16 if penalty == 48 else 48]
            for zipped in (False, True):
                with self.subTest(penalty=penalty, zipped=zipped), temporary_directory() as temporary:
                    root = Path(temporary)
                    with isolated_support():
                        other_root = root / "other"
                        other_root.mkdir()
                        incoming, _, _ = self._bundle_fixture(other, other_root)
                        namespace = self._prepared_namespace(spec, root)
                        incoming_path = incoming["OUT"]
                        if zipped:
                            incoming_path = Path(shutil.make_archive(
                                str(root / "wrong-variant"), "zip", root_dir=incoming_path))
                        namespace.update(RESUME=True, RESUME_BUNDLE=str(incoming_path))
                        with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(
                            ValueError, "identity/configuration mismatch"
                        ):
                            exec(spec.resume, namespace)
                        self.assertFalse(namespace["OUT"].exists())

    def test_resume_requires_full_optimizer_backup(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, _, _ = self._bundle_fixture(spec, Path(temporary), status="prepared")
                    (namespace["OUT"] / "last.pt").unlink()
                    namespace.update(RESUME=True, RESUME_BUNDLE="")
                    with contextlib.redirect_stdout(io.StringIO()), self.assertRaisesRegex(
                        FileNotFoundError, "full .*backup|last.pt"
                    ):
                        exec(spec.resume, namespace)

    def test_interrupted_run_skips_reload_without_allocating_a_model(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, _, _ = self._bundle_fixture(spec, Path(temporary), status="prepared")
                    (namespace["OUT"] / "reload_check.json").unlink()
                    model = object()
                    namespace["model"] = model
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(spec.reload, namespace)
                    self.assertIs(namespace["model"], model)
                    self.assertFalse((namespace["OUT"] / "reload_check.json").exists())

    def test_reload_rejects_changed_saved_helper_before_releasing_model(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, _, _ = self._bundle_fixture(spec, Path(temporary))
                    (namespace["OUT"] / "nllb_source_adapter.py").write_bytes(b"changed helper")
                    model = object()
                    namespace["model"] = model
                    with self.assertRaisesRegex(ValueError, "identity mismatch: nllb_source_adapter.py"):
                        exec(spec.reload, namespace)
                    self.assertIs(namespace["model"], model)

    def _run_export(self, spec, namespace, expect_inference):
        display = types.ModuleType("IPython.display")
        display.display = lambda value: None
        display.FileLink = lambda value: value
        with mock.patch.dict(sys.modules, {"IPython.display": display}):
            with contextlib.redirect_stdout(io.StringIO()):
                exec(spec.export, namespace)
        out = namespace["OUT"]
        with zipfile.ZipFile(out.parent / "fixture_full.zip") as archive:
            self.assertIn("manifest.json", archive.namelist())
            self.assertIn("last.pt", archive.namelist())
        inference = out.parent / "fixture_inference.zip"
        if expect_inference:
            with zipfile.ZipFile(inference) as archive:
                self.assertIn("manifest.json", archive.namelist())
                self.assertIn("best_source.safetensors", archive.namelist())
                self.assertIn("training_support.py", archive.namelist())
                self.assertFalse(any(name.endswith(".pt") for name in archive.namelist()))
                self.assertEqual(archive.read("source_artifact/tokenizer.json"),
                                 (out / "source_artifact/tokenizer.json").read_bytes())
        else:
            self.assertFalse(inference.exists())

    def test_completed_run_exports_installable_root_without_optimizer(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, _, _ = self._bundle_fixture(spec, Path(temporary))
                    self._run_export(spec, namespace, expect_inference=True)

    def test_interrupted_run_can_export_full_resume_backup(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, _, _ = self._bundle_fixture(spec, Path(temporary), status="prepared")
                    self._run_export(spec, namespace, expect_inference=False)

    def test_absent_or_stale_reload_reports_only_allow_full_resume_export(self):
        mutations = (
            None, {"status": "failed"}, {"base_revision": "wrong-base"},
            {"weights_sha256": "0" * 64}, {"selected_epoch": 2},
            {"identity_sha256": "0" * 64}, {"crossing_penalty": "other"},
            {"tokenizer_variant": "weighted_penalty32"},
        )
        for penalty, spec in self.specs.items():
            for mutation in mutations:
                with self.subTest(penalty=penalty, mutation=mutation), temporary_directory() as temporary:
                    with isolated_support():
                        namespace, _, report = self._bundle_fixture(spec, Path(temporary))
                        if mutation is None:
                            (namespace["OUT"] / "reload_check.json").unlink()
                        else:
                            report.update(mutation)
                            self._write_json(namespace["OUT"] / "reload_check.json", report)
                        self._run_export(spec, namespace, expect_inference=False)

    def test_cross_variant_manifest_prevents_any_export(self):
        for penalty, spec in self.specs.items():
            with self.subTest(penalty=penalty), temporary_directory() as temporary:
                with isolated_support():
                    namespace, manifest, _ = self._bundle_fixture(spec, Path(temporary))
                    manifest.update(sys.modules["training_support"].variant_fields(16 if penalty == 48 else 48))
                    self._write_json(namespace["OUT"] / "manifest.json", manifest)
                    with self.assertRaisesRegex(ValueError, "Saved manifest mismatch"):
                        self._run_export(spec, namespace, expect_inference=False)
                    self.assertFalse((namespace["OUT"].parent / "fixture_full.zip").exists())


if __name__ == "__main__":
    unittest.main()
