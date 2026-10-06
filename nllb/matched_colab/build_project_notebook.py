"""Build the project-integrated Colab notebook and a portable input ZIP."""
import json
import runpy
import shutil
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).parent
REPO = Path(sys.argv[1]) if len(sys.argv)>1 else Path(r'C:/Users/vonvo/kapampangan-tokenizer/kapampangan-tokenizer-pipeline')
runpy.run_path(str(HERE/'build_notebook.py'))
path = HERE/'NLLB_600M_Kapampangan_Training.ipynb'
nb = json.loads(path.read_text(encoding='utf-8'))
def cell(i,s): nb['cells'][i]['source'] = s.strip()+'\n'

cell(0,'''# NLLB 600M — your Plain-BPE / MorphBPE translation experiment
This notebook uses the **existing matched 6,080-entry artifacts** from your
`expanded_morphology_v4` pipeline, with their exact standalone runtime.
It replaces the earlier generic-tokenizer setup. No tokenizer retraining, HF conversion,
or new `<kap>` entry is required. The two conditions are `plain_bpe` and `morph_bpe`.

Upload this notebook to Colab and select a GPU. Put the supplied
`kapampangan_colab_inputs.zip` in `MyDrive/kapampangan_nllb/` before section 2.
The ZIP contains your existing data and tokenizers, not trained NLLB weights.
Read README_PROJECT.md for the experiment protocol and remaining data limitations.

All pretrained weights stay frozen. Only the new source table trains. Both conditions
default to **warm-starting from native NLLB subtoken embeddings**, matching your existing
pipeline. This initialization must be disclosed in the thesis. `random` is an optional
separate matched experiment, not something to change between the two conditions.''')
cell(3,'''## 2. Mount Drive, unpack the supplied inputs, and select one condition
Run both conditions independently with identical settings. Restart the runtime between
conditions to release GPU memory. Existing tokenizer vocabulary and segmentation stay fixed.
Choose unique run names for new experiments. Resume only with the original configuration.''')
cell(4,'''from google.colab import drive
drive.mount('/content/drive')
from pathlib import Path
import zipfile, hashlib, json
ROOT = Path('/content/drive/MyDrive/kapampangan_nllb')
ROOT.mkdir(parents=True, exist_ok=True)
INPUT_ZIP = ROOT/'kapampangan_colab_inputs.zip'
INPUT_ROOT = Path('/content/kapampangan_inputs')
INPUT_ROOT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(INPUT_ZIP) as z:
    for entry in z.infolist():
        destination = (INPUT_ROOT/entry.filename).resolve()
        if not destination.is_relative_to(INPUT_ROOT.resolve()): raise ValueError('Unsafe ZIP path')
    z.extractall(INPUT_ROOT)
package_hashes = json.loads((INPUT_ROOT/'package_checksums.json').read_text())
for name, checksum in package_hashes.items():
    assert hashlib.sha256((INPUT_ROOT/name).read_bytes()).hexdigest() == checksum, name

CONDITION = 'plain_bpe'  # next independent run: 'morph_bpe'
INITIALIZATION = 'warm_start'  # OR 'random', identically for both conditions
RUN_NAME = 'warm_start_seed42_v2'
RESUME = False
SOURCE_VOCAB_SIZE = 6080
MODEL_ID = 'facebook/nllb-200-distilled-600M'
BASE_REVISION = 'f8d333a098d19b4fd9a8b18f94170487ad3f821d'
CFG = dict(seed=42, epochs=10, lr=3e-4, batch_size=1, accumulation=8,
           initialization=INITIALIZATION)
MAX_SOURCE_TOKENS = 256
MAX_TARGET_TOKENS = 128
MAX_NEW_TOKENS = 160
NUM_BEAMS = 4
RUN_TEST = False
assert CONDITION in {'plain_bpe','morph_bpe'}
assert INITIALIZATION in {'warm_start','random'}
assert all(CFG[k]>0 for k in ['epochs','lr','batch_size','accumulation'])
assert 2 < MAX_SOURCE_TOKENS <= 512 and 2 < MAX_TARGET_TOKENS <= 512
assert MAX_NEW_TOKENS >= MAX_TARGET_TOKENS
DATA_ROOT = INPUT_ROOT/'bundle'
ARTIFACT_PATH = INPUT_ROOT/'artifacts'/CONDITION
OUT = ROOT/'runs'/CONDITION/RUN_NAME''')
cell(5,'''## 3. Load the training implementation and project tokenizer runtime
The notebook embeds its training helper. The ZIP supplies the exact standalone runtime
from your project, requiring no Rust build or lexicon at inference time.''')
s=nb['cells'][7]['source']
s=s.replace("sys.path.insert(0, '/content')", "sys.path.insert(0, '/content')\nsys.path.insert(0, str(INPUT_ROOT/'runtime'))")
cell(7,s)
cell(8,'''## 4. Validate the existing frozen translation bundle
The original four splits are preserved: train, dev, test_bible, test_ood.
Checks include file hashes, row counts, cross-split normalized source duplicates, and
exact tokenizer-ID agreement. They do not prove that the earlier tokenizer-training
corpus excludes these translation test sentences. That separate audit needs the
original tokenizer corpus, which was unavailable during integration.

The supplied translations remain silver/development data; the existing split report
also identifies partial alignments. These are not silently relabeled as human-validated.''')
cell(9,'''project_splits, bundle_meta, data_audit = read_project_bundle(DATA_ROOT)
splits = {'train':project_splits['train'], 'validation':project_splits['dev'],
          'test_bible':project_splits['test_bible'], 'test_ood':project_splits['test_ood']}
print({k:len(v) for k,v in splits.items()})
print(data_audit)
save_json(OUT/'data_audit.json', data_audit)
save_json(OUT/'split_manifest.json', {k:[r['id'] for r in v] for k,v in splits.items()})''')
cell(10,'''## 5. Connect your exact tokenizer artifacts
The adapter preserves NFC normalization, whitespace tokens, learned merges, BOS/EOS,
and all 6,080 vocabulary entries. At the model boundary only, artifact PAD 0 becomes
model PAD 1, and artifact UNK 1 becomes model UNK 0. Every other ID stays unchanged.
This reversible permutation prevents unknown tokens from being mistaken for padding
by NLLB's positional embeddings. Decoder PAD remains 1.

Both artifacts must have the same prepared-corpus fingerprint. The raw-text runtime
must reproduce the corresponding pre-tokenized bundle IDs on every record.''')
cell(11,'''plain_manifest = json.loads((INPUT_ROOT/'artifacts/plain_bpe/tokenizer-manifest.json').read_text())
morph_manifest = json.loads((INPUT_ROOT/'artifacts/morph_bpe/tokenizer-manifest.json').read_text())
assert plain_manifest['metadata']['prepared_manifest_fingerprint'] == morph_manifest['metadata']['prepared_manifest_fingerprint']
assert plain_manifest['core_file_sha256']['normalization.json'] == morph_manifest['core_file_sha256']['normalization.json']
assert plain_manifest['core_file_sha256']['pretokenizer.json'] == morph_manifest['core_file_sha256']['pretokenizer.json']
for condition, native_name in [('plain_bpe','bpe6080'),('morph_bpe','morphbpe')]:
    artifact = INPUT_ROOT/'artifacts'/condition
    manifest_check = json.loads((artifact/'tokenizer-manifest.json').read_text())
    assert manifest_check['artifact_fingerprint'] == bundle_meta['artifact_fingerprints'][native_name]
    check_source = SourceTokenizer(artifact, SOURCE_VOCAB_SIZE)
    for rows in splits.values():
        for row in rows:
            assert check_source.encode(row['source']) == source_ids_for(condition,row), row['id']
source = SourceTokenizer(ARTIFACT_PATH, SOURCE_VOCAB_SIZE)
target = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION,
    src_lang='tgl_Latn', tgt_lang='tgl_Latn', use_fast=True)
encoded, token_stats = prepare(splits, source, target, MAX_SOURCE_TOKENS, MAX_TARGET_TOKENS)
save_json(OUT/'tokenization_audit.json', token_stats)
print(token_stats)
assert encoded['train'][0]['labels'][0] == target.convert_tokens_to_ids('tgl_Latn')
assert encoded['train'][0]['labels'][-1] == target.eos_token_id
print('Source controls (model IDs):', source.special)
if any(v['unknown_fraction']>0.01 for v in token_stats.values()):
    print('WARNING: >1% unknown source tokens. Inspect coverage before interpreting results.')''')
s=nb['cells'][13]['source'].replace("load_base(MODEL_ID, REVISION, CFG['seed'], SOURCE_VOCAB_SIZE)","load_base(MODEL_ID, REVISION, CFG['seed'], SOURCE_VOCAB_SIZE,\n                  source=source, target=target, initialization=INITIALIZATION)")
cell(13,s)
cell(15,'''identity = dict(data_hashes=bundle_meta['split_sha256'],
    tokenizer_sha256=digest(ARTIFACT_PATH/'tokenizer.json'),
    artifact_manifest_sha256=digest(ARTIFACT_PATH/'tokenizer-manifest.json'),
    model_id=MODEL_ID, revision=REVISION, condition=CONDITION,
    initialization=INITIALIZATION, source_limit=MAX_SOURCE_TOKENS,
    target_limit=MAX_TARGET_TOKENS, max_new_tokens=MAX_NEW_TOKENS, beams=NUM_BEAMS,
    helper_sha256=digest('/content/nllb_source_adapter.py'),
    runtime_sha256=digest(INPUT_ROOT/'runtime/kapampangan_morphbpe_runtime/tokenizer.py'))
manifest = dict(model_id=MODEL_ID, revision=REVISION, source_vocab_size=source.size,
    source_format='kapampangan_project', source_id_mapping='swap_0_1',
    cfg=CFG, identity=identity, adaptation='source_embedding_only',
    target_language='tgl_Latn', source_marker='<s>')
if (OUT/'manifest.json').exists():
    assert json.loads((OUT/'manifest.json').read_text()) == manifest, 'Existing run mismatch; choose a new RUN_NAME'
save_json(OUT/'manifest.json', manifest)
shutil.copytree(ARTIFACT_PATH, OUT/'source_artifact', dirs_exist_ok=True)
shutil.copytree(INPUT_ROOT/'runtime', OUT/'runtime', dirs_exist_ok=True)
shutil.copy2('/content/nllb_source_adapter.py', OUT/'nllb_source_adapter.py')
target.save_pretrained(OUT/'target_tokenizer')
(OUT/'environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'],text=True))
history = train(model, encoded, CFG, identity, OUT, device, resume=RESUME)''')
cell(19,'''if RUN_TEST:
    for split in ['test_bible','test_ood']:
        test_predictions = predict(model, source, target, splits[split], device,
            MAX_NEW_TOKENS, NUM_BEAMS)
        print(split, score_and_export(splits[split], test_predictions, OUT/split))
else:
    print('Test generation skipped. Finalize settings on validation first.')''')
cell(22,'''## Interpretation
The revised SOP's translation comparison is plain BPE versus hard-constrained MorphBPE.
The Unigram and penalty-8 variants are not silently included in this experiment.
This notebook uses a shared warm-start recipe by default; report that change in the
methods instead of describing the initialization as random. To study random initialization,
run both conditions with `INITIALIZATION='random'` and fresh run names.

Generation limits, beam count, update schedule, and checkpoint selection are identical
across conditions. Unresolved tokenizer-corpus/test overlap and silver-data quality remain
research limitations. Do not claim a clean held-out hypothesis test until those audits
are complete. Software checks and low validation loss are not linguistic validation.

See README_PROJECT.md and VALIDATION_PROJECT.md for integration details and tests.''')
nb['metadata']['colab']['name'] = path.name
path.write_text(json.dumps(nb,indent=1,ensure_ascii=False),encoding='utf-8')

# Export only necessary portable inputs. Never modify source artifacts or source data.
inputs = HERE/'project_inputs'
for dest,kind in [('plain_bpe','plain'),('morph_bpe','morphbpe')]:
    src = REPO/'experiments/expanded_morphology_v4/artifacts'/kind/'candidates/vocab-6080'
    (inputs/'artifacts'/dest).mkdir(parents=True,exist_ok=True)
    for p in src.iterdir():
        if p.is_file(): shutil.copy2(p,inputs/'artifacts'/dest/p.name)
for name in ['__init__.py','tokenizer.py']:
    p=inputs/'runtime/kapampangan_morphbpe_runtime'/name
    p.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(REPO/'runtime/kapampangan_morphbpe_runtime'/name,p)
(inputs/'bundle').mkdir(parents=True,exist_ok=True)
for name in ['train.jsonl','dev.jsonl','test_bible.jsonl','test_ood.jsonl','meta.json','vocab.json']:
    shutil.copy2(REPO/'experiments/nllb_finetune_v1/data/bundle'/name,inputs/'bundle'/name)
shutil.copy2(REPO/'experiments/nllb_finetune_v1/reports/split-manifest.json',inputs/'bundle/split-manifest.json')
import hashlib
files = [p for p in inputs.rglob('*') if p.is_file() and p.name!='package_checksums.json' and '__pycache__' not in p.parts]
hashes = {p.relative_to(inputs).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(inputs/'package_checksums.json').write_text(json.dumps(hashes,indent=2))
with ZipFile(HERE/'kapampangan_colab_inputs.zip','w',ZIP_DEFLATED) as z:
    for p in files+[inputs/'package_checksums.json']: z.write(p,p.relative_to(inputs).as_posix())
print('Built project notebook and input ZIP; source repo unchanged.')
