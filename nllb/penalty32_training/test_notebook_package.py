"""Exercise real notebook input cells without importing a model or training."""
import ast
import contextlib
import hashlib
import io
import json
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
NOTEBOOK = ROOT/'notebooks/NLLB_600M_Penalty32_Source_Embedding_Training.ipynb'
PACKAGE = HERE/'penalty32_training_inputs.zip'


class NotebookPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        cls.code = [c['source'] for c in cls.notebook['cells'] if c['cell_type']=='code']
        config = next(s for s in cls.code if 'EXPECTED_PACKAGE_SHA256 =' in s)
        cls.constants = {}
        for node in ast.parse(config).body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target,ast.Name) and target.id.startswith('EXPECTED_'):
                        cls.constants[target.id] = ast.literal_eval(node.value)
        cls.verify = next(s for s in cls.code if s.startswith('def digest('))
        cls.csv = next(s for s in cls.code if 'from training_support import read_matched_csv' in s)
        cls.reload = next(s for s in cls.code if s.startswith('reload_info ='))
        cls.export = next(s for s in cls.code if 'INFERENCE_ZIP = ' in s)

    def test_code_cells_compile_and_start_without_outputs(self):
        for index,cell in enumerate(self.notebook['cells']):
            if cell['cell_type']=='code':
                compile(cell['source'], f'notebook-cell-{index}', 'exec')
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])

    def _run_inputs(self, extracted=False, corrupt=False):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            input_folder=root/'kaggle_input'
            input_folder.mkdir()
            if extracted:
                package=input_folder/'expanded'
                package.mkdir()
                with zipfile.ZipFile(PACKAGE) as archive:
                    archive.extractall(package)
                if corrupt:
                    (package/'source_artifact/vocab.json').write_text('{}')
            else:
                package=input_folder/PACKAGE.name
                shutil.copy2(PACKAGE,package)
            work=root/'working'
            work.mkdir()
            namespace=dict(Path=Path,json=json,hashlib=hashlib,zipfile=zipfile,
                sys=sys,WORK=work,RUNS=work/'runs',SEARCH_ROOTS=[input_folder],
                INPUT_PATH='',DATA_CSV='',**self.constants)
            original_path=list(sys.path)
            old_module=sys.modules.pop('training_support',None)
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(self.verify,namespace)
                    exec(self.csv,namespace)
                self.assertEqual(namespace['data_audit']['used_counts'],
                                 dict(train=12911,validation=1636,test=1659))
                self.assertTrue(namespace['package']['csv_included'])
                self.assertEqual(namespace['data_audit']['within_split_duplicate_excess'],
                                 dict(train=60,validation=1,test=1))
            finally:
                sys.path[:]=original_path
                sys.modules.pop('training_support',None)
                if old_module is not None: sys.modules['training_support']=old_module

    def test_kaggle_zip_discovers_and_uses_packaged_csv(self):
        self._run_inputs(extracted=False)

    def test_kaggle_expanded_input_discovers_and_uses_packaged_csv(self):
        self._run_inputs(extracted=True)

    def test_corrupt_expanded_tokenizer_is_rejected_before_training(self):
        with self.assertRaisesRegex(ValueError,'Package checksum mismatch'):
            self._run_inputs(extracted=True,corrupt=True)

    def test_package_has_exact_visualization_artifact_and_no_source_weights(self):
        actual=ROOT/'webapp/backend/tokenizer/artifacts/morphbpe-penalty32'
        with zipfile.ZipFile(PACKAGE) as archive:
            self.assertNotIn('last.pt',archive.namelist())
            self.assertNotIn('best_source.safetensors',archive.namelist())
            for file in actual.iterdir():
                if file.is_file():
                    self.assertEqual(archive.read('source_artifact/'+file.name),file.read_bytes())
            csv=archive.read('data/kpm_tgl_cleaned.csv')
            self.assertEqual(hashlib.sha256(csv).hexdigest(),self.constants['EXPECTED_DATA_SHA256'])

    def test_interrupted_run_skips_reload_without_allocating_a_model(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)
            (out/'manifest.json').write_text(json.dumps(dict(training_status='prepared')))
            existing_model=object()
            namespace=dict(OUT=out,json=json,model=existing_model)
            with contextlib.redirect_stdout(io.StringIO()):
                exec(self.reload,namespace)
            self.assertIs(namespace['model'],existing_model)
            self.assertFalse((out/'reload_check.json').exists())

    def test_reload_rejects_changed_saved_helper_before_releasing_model(self):
        with tempfile.TemporaryDirectory() as temporary:
            out=Path(temporary)
            identity=dict(tokenizer_sha256='tokenizer',artifact_manifest_sha256='manifest',
                          helper_sha256='expected-helper',runtime_sha256='runtime')
            (out/'manifest.json').write_text(json.dumps(dict(training_status='completed',
                                                         identity=identity,cfg={})))
            expected_by_name={'tokenizer.json':'tokenizer','tokenizer-manifest.json':'manifest',
                              'nllb_source_adapter.py':'changed-helper','tokenizer.py':'runtime'}
            existing_model=object()
            namespace=dict(OUT=out,json=json,CFG={},identity=identity,model=existing_model,
                           digest=lambda path:expected_by_name[Path(path).name])
            with self.assertRaisesRegex(ValueError,'Reload identity mismatch: nllb_source_adapter.py'):
                exec(self.reload,namespace)
            self.assertIs(namespace['model'],existing_model)

    def _export_fixture(self,status,reload_status='passed',reload_revision='fixture-revision'):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            out=root/'morph_bpe'
            out.mkdir()
            identity={}
            for name,key in [('source_artifact/tokenizer.json','tokenizer_sha256'),
                             ('source_artifact/tokenizer-manifest.json','artifact_manifest_sha256'),
                             ('nllb_source_adapter.py','helper_sha256'),
                             ('runtime/kapampangan_morphbpe_runtime/tokenizer.py','runtime_sha256')]:
                path=out/name
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(b'export fixture')
                identity[key]=hashlib.sha256(path.read_bytes()).hexdigest()
            (out/'manifest.json').write_text(json.dumps(dict(identity=identity,training_status=status,
                                                           revision='fixture-revision')))
            (out/'last.pt').write_bytes(b'fixture checkpoint; never loaded')
            (out/'best_source.safetensors').write_bytes(b'fixture weights; never loaded')
            if reload_status is not None:
                (out/'reload_check.json').write_text(json.dumps(dict(status=reload_status,
                    weights_sha256=hashlib.sha256((out/'best_source.safetensors').read_bytes()).hexdigest(),
                    tokenizer_sha256=identity['tokenizer_sha256'],base_revision=reload_revision)))
            display_module=types.ModuleType('IPython.display')
            display_module.display=lambda value:None
            display_module.FileLink=lambda value:value
            namespace=dict(OUT=out,RUN_NAME='fixture',Path=Path,json=json,
                zipfile=zipfile,shutil=shutil,
                digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest())
            with mock.patch.dict(sys.modules,{'IPython.display':display_module}):
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(self.export,namespace)
            with zipfile.ZipFile(root/'fixture_full.zip') as archive:
                self.assertIn('manifest.json',archive.namelist())
                self.assertIn('last.pt',archive.namelist())
            inference=root/'fixture_inference.zip'
            if status=='completed' and reload_status=='passed' and reload_revision=='fixture-revision':
                with zipfile.ZipFile(inference) as archive:
                    self.assertIn('manifest.json',archive.namelist())
                    self.assertIn('best_source.safetensors',archive.namelist())
                    self.assertNotIn('last.pt',archive.namelist())
            else:
                self.assertFalse(inference.exists())

    def test_interrupted_run_can_export_full_resume_backup(self):
        self._export_fixture('prepared')

    def test_completed_run_exports_installable_root_without_optimizer(self):
        self._export_fixture('completed')

    def test_completed_run_without_reload_still_exports_resume_backup(self):
        self._export_fixture('completed',reload_status=None)

    def test_failed_reload_prevents_inference_export_without_losing_resume_backup(self):
        self._export_fixture('completed',reload_status='failed')

    def test_reload_report_from_different_base_prevents_inference_export(self):
        self._export_fixture('completed',reload_revision='other-base')


if __name__=='__main__':
    unittest.main()
