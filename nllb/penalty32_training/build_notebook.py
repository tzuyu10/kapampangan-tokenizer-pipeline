"""Build the penalty-32 GPU notebook and its checksummed private input package.

Reads installed baseline provenance and copies original bytes without changing
installed bundles, tokenizer artifacts, or the older training notebook.
"""
import argparse
import hashlib
import json
from pathlib import Path
import textwrap
import zipfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FINGERPRINT = '2dc38cb89b2b3545c134b43c932a1f343453372bdbaeea090900d5566d759ad1'
EXPECTED_DATA = '69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b'
NOTEBOOK_NAME = 'NLLB_600M_Penalty32_Source_Embedding_Training.ipynb'
PACKAGE_NAME = 'penalty32_training_inputs.zip'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def make_notebook(package_sha, package_manifest_sha):
    cells = []

    def md(source):
        cells.append(dict(cell_type='markdown', metadata={}, source=textwrap.dedent(source).strip()+'\n'))

    def code(source):
        cells.append(dict(cell_type='code', execution_count=None, metadata={}, outputs=[],
                          source=textwrap.dedent(source).strip()+'\n'))

    md('''
    # Penalty-32 Morph-BPE: source-embedding adaptation

    This trains a **new 6,080 x 1,024 source embedding table** using the exact
    frequency-weighted penalty-32 tokenizer from the visualization tab. The tokenizer
    is already trained. All pretrained NLLB encoder layers, decoder, target embeddings,
    and output projection remain frozen. The penalty is embodied in the tokenizer's
    vocabulary/merges; it is not added to the translation loss.

    The reference is the installed Plain BPE run: seed 42, warm initialization,
    learning rate 0.0003, batch size 1, accumulation 8, maximum 30 epochs, early
    stopping patience 3/minimum improvement 0.001, source/target limits 256/128.
    The actual stopping and selected epochs are reported from saved history.

    **Inputs:** this notebook and `penalty32_training_inputs.zip`. The supplied ZIP
    includes the exact original `kpm_tgl_cleaned.csv` used for the current 30-epoch runs.
    A separately supplied CSV override must also hash to
    `69a67a2773a5ecb49d16ef01c47057bd9b75916cf10f55d397df01d13c29c01b`.
    The package contains the exact tokenizer/runtime, unchanged training helper,
    native target tokenizer and baseline provenance, but no trained source weights.

    On Kaggle, attach the package as a private notebook input and select a
    GPU. Enable Internet for package installation and the first pinned-base download.
    Kaggle may unpack the ZIP automatically; both ZIP and extracted-directory inputs
    are supported. On Colab, select a GPU and place the input ZIP in
    `MyDrive/kapampangan_nllb_penalty32/`; outputs are saved to Drive by default.

    Run cells in order. Keep `RESUME=False` for the first run. Preserve the existing
    Plain30 and hard-constrained Morph30 bundles. This notebook creates separate
    outputs and does not install a model into the application. GPU training has not
    been executed during local notebook preparation.
    ''')
    md('''
    ## 1. Install the recorded tokenizer/Transformers dependencies

    Run this cell before importing Transformers. It retains the cloud runtime's GPU
    PyTorch rather than installing a CPU wheel. If these packages were already imported
    with different versions, restart the session after installation and continue.
    As in the original notebook, remove optional vision/audio/UI packages before
    installing the pinned stack. PyTorch itself is retained.
    The baseline recorded Torch 2.11.0+cu128; a different GPU Torch version is recorded
    as an environment difference rather than silently represented as identical.
    ''')
    code('''
    import sys, subprocess, os
    os.environ['USE_TF'] = '0'
    os.environ['USE_FLAX'] = '0'
    OPTIONAL_PACKAGES = ['diffusers', 'gradio', 'timm', 'torchvision', 'torchaudio']
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-q', '-y', *OPTIONAL_PACKAGES])
    PINS = ['transformers==4.48.3', 'tokenizers==0.21.0',
            'huggingface-hub==0.28.1', 'sentencepiece==0.2.0',
            'safetensors==0.5.3', 'sacrebleu==2.5.1']
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *PINS])
    print('Dependencies installed. Restart if a different version was already imported.')
    ''')
    md('''
    ## 2. Choose inputs and a new output run

    Blank input paths enable discovery in Kaggle inputs or the Colab input folder.
    Set explicit paths if multiple matches are found. `INPUT_PATH` may be the ZIP or
    the directory containing `package_manifest.json`. Leave `DATA_CSV` blank to use
    the CSV included in the package, or set it to a matching original CSV override.

    For resume, use the same configuration and run name. On Kaggle, optionally set
    `RESUME_BUNDLE` to an uploaded **penalty32 full backup ZIP** or its extracted root.
    This notebook refuses a hard-constrained/Plain checkpoint and requires both
    `last.pt` and the saved best source weights. Kaggle's working directory is session
    storage; download/save the full backup before ending a session. The helper saves
    at completed-epoch boundaries, so an interrupted epoch restarts.
    ''')
    code(f'''
    from pathlib import Path
    import os, json, hashlib, shutil, zipfile, tempfile, importlib.util

    INPUT_PATH = ''
    DATA_CSV = ''
    RUN_NAME = 'penalty32_warm_start_seed42_v2'
    RESUME = False
    RESUME_BUNDLE = ''
    RUN_VALIDATION_TRANSLATIONS = False
    RUN_TEST = False  # enable only after the experimental settings are frozen
    USE_GOOGLE_DRIVE = True

    EXPECTED_PACKAGE_SHA256 = '{package_sha}'
    EXPECTED_PACKAGE_MANIFEST_SHA256 = '{package_manifest_sha}'
    EXPECTED_TOKENIZER_FINGERPRINT = '{FINGERPRINT}'
    EXPECTED_DATA_SHA256 = '{EXPECTED_DATA}'
    PLATFORM = 'kaggle' if Path('/kaggle/working').exists() else 'colab'
    if PLATFORM == 'kaggle':
        WORK = Path('/kaggle/working/penalty32_training')
        SEARCH_ROOTS = [Path('/kaggle/input')]
        RUNS = WORK/'runs'
    else:
        WORK = Path('/content/penalty32_training')
        if USE_GOOGLE_DRIVE:
            from google.colab import drive
            drive.mount('/content/drive')
            CLOUD = Path('/content/drive/MyDrive/kapampangan_nllb_penalty32')
            SEARCH_ROOTS = [CLOUD, Path('/content')]
            RUNS = CLOUD/'runs'
        else:
            SEARCH_ROOTS = [Path('/content')]
            RUNS = WORK/'runs'
    if not RUN_NAME or Path(RUN_NAME).name != RUN_NAME or RUN_NAME in ('.', '..'):
        raise ValueError('RUN_NAME must be one folder name.')
    WORK.mkdir(parents=True, exist_ok=True)
    OUT = RUNS/'morph_bpe'/RUN_NAME
    print('Platform:', PLATFORM, 'Output:', OUT)
    ''')
    md('''
    ## 3. Verify and unpack the exact inputs

    Verification includes all package files, the penalty-32 fingerprint, tokenizer
    inventory, baseline configuration and data identity. No existing trained source
    weights or optimizer checkpoints are included in the training input package.
    ''')
    code('''
    def digest(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def discover(pattern):
        result = set()
        for root in SEARCH_ROOTS:
            if root.exists():
                for p in root.rglob(pattern):
                    if WORK not in p.parents and RUNS not in p.parents and p.is_file():
                        result.add(p.resolve())
        return sorted(result)

    if not INPUT_PATH:
        candidates = discover('penalty32_training_inputs.zip')
        if not candidates:
            candidates = [p.parent for p in discover('package_manifest.json')
                          if json.loads(p.read_text()).get('package_kind') == 'penalty32_source_training']
        if len(candidates) != 1:
            raise ValueError('Set INPUT_PATH to the ZIP or extracted package folder. Found: '+str(candidates))
        INPUT_PATH = str(candidates[0])
    package_path = Path(INPUT_PATH)
    if package_path.is_file():
        if digest(package_path) != EXPECTED_PACKAGE_SHA256:
            raise ValueError('Training input ZIP hash mismatch. Use the supplied package.')
        INPUT_ROOT = WORK/'inputs'
        INPUT_ROOT.mkdir(exist_ok=True)
        with zipfile.ZipFile(package_path) as archive:
            for entry in archive.infolist():
                target_path = (INPUT_ROOT/entry.filename).resolve()
                if not target_path.is_relative_to(INPUT_ROOT.resolve()):
                    raise ValueError('Unsafe ZIP path')
                if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('ZIP links are not supported')
            archive.extractall(INPUT_ROOT)
    else:
        INPUT_ROOT = package_path
    if digest(INPUT_ROOT/'package_manifest.json') != EXPECTED_PACKAGE_MANIFEST_SHA256:
        raise ValueError('Package manifest hash mismatch. Use the supplied input files.')
    package = json.loads((INPUT_ROOT/'package_manifest.json').read_text(encoding='utf-8'))
    if package['package_kind'] != 'penalty32_source_training':
        raise ValueError('Unexpected input package')
    for name, checksum in package['files'].items():
        file = (INPUT_ROOT/name).resolve()
        if not file.is_relative_to(INPUT_ROOT.resolve()) or digest(file) != checksum:
            raise ValueError('Package checksum mismatch: '+name)
    if (INPUT_ROOT/'last.pt').exists() or (INPUT_ROOT/'best_source.safetensors').exists():
        raise ValueError('Input package must not contain trained source weights.')
    baseline = json.loads((INPUT_ROOT/'reference/plain_bpe/manifest.json').read_text())
    baseline_audit = json.loads((INPUT_ROOT/'reference/plain_bpe/data_audit.json').read_text())
    baseline_splits = json.loads((INPUT_ROOT/'reference/plain_bpe/split_manifest.json').read_text())
    if baseline['identity']['data_sha256'] != EXPECTED_DATA_SHA256:
        raise ValueError('Baseline data identity mismatch')
    ARTIFACT = INPUT_ROOT/'source_artifact'
    artifact_manifest = json.loads((ARTIFACT/'tokenizer-manifest.json').read_text())
    if artifact_manifest['artifact_fingerprint'] != EXPECTED_TOKENIZER_FINGERPRINT:
        raise ValueError('This is not the visualization tokenizer')
    if artifact_manifest['actual_vocabulary_size'] != 6080 or artifact_manifest['metadata']['crossing_penalty'] != 32:
        raise ValueError('Wrong weighted tokenizer configuration')
    for line in (ARTIFACT/'checksums.sha256').read_text().splitlines():
        if not line.strip(): continue
        checksum, name = line.split(maxsplit=1)
        file = (ARTIFACT/name.lstrip('*')).resolve()
        if not file.is_relative_to(ARTIFACT.resolve()) or digest(file) != checksum:
            raise ValueError('Tokenizer inventory mismatch: '+name)
    if digest(INPUT_ROOT/'nllb_source_adapter.py') != baseline['identity']['helper_sha256']:
        raise ValueError('Training implementation differs from the recorded baseline')
    print('Verified penalty32 artifact, unchanged training helper and baseline provenance.')
    ''')
    md('''
    ## 4. Load the matched CSV without changing the comparison

    The reader follows the original notebook's recovered CSV loader and requires
    exact agreement with the installed baseline's CSV bytes, audit and ordered split
    IDs. Source and target strings remain unchanged. It preserves accepted within-split
    duplicates and evaluation references;
    it does not silently deduplicate, resplit, or truncate the dataset.
    ''')
    code('''
    sys.path.insert(0, str(INPUT_ROOT))
    sys.path.insert(0, str(INPUT_ROOT/'runtime'))
    from training_support import read_matched_csv
    if not DATA_CSV:
        packaged_csv = INPUT_ROOT/'data/kpm_tgl_cleaned.csv'
        candidates = [packaged_csv] if packaged_csv.is_file() else [p for p in discover('*.csv') if digest(p) == EXPECTED_DATA_SHA256]
        if len(candidates) != 1:
            raise ValueError('Set DATA_CSV to the original matching CSV. Hash-matched files: '+str(candidates))
        DATA_CSV = str(candidates[0])
    splits, data_audit = read_matched_csv(DATA_CSV, EXPECTED_DATA_SHA256,
                                         baseline_audit, baseline_splits)
    print('Matched rows:', {k:len(v) for k,v in splits.items()})
    print('Preserved duplicates:', data_audit['within_split_duplicate_excess'])
    print('Tokenizer-training-corpus overlap with translation test remains unverified.')
    ''')
    md('''
    ## 5. Load exact tokenization and reproduce baseline settings

    Source content token pieces come from the exact visualization runtime/artifact.
    The adapter adds BOS/EOS and swaps native IDs 0/1 at the NLLB boundary. These
    control differences do not change the content segmentation. Tokenization limits
    are checked before any training; overlength examples cause an error.
    ''')
    code('''
    import torch, transformers, random
    import nllb_source_adapter as helper
    from transformers import AutoTokenizer
    if transformers.__version__ != '4.48.3':
        raise RuntimeError('Restart the session to use Transformers 4.48.3.')
    if not torch.cuda.is_available():
        raise RuntimeError('Select a GPU runtime. This notebook does not start CPU training.')
    DEVICE = torch.device('cuda')
    CFG = dict(baseline['cfg'])
    expected_cfg = dict(seed=42, epochs=30, early_stopping_patience=3,
                        early_stopping_min_delta=0.001, lr=0.0003,
                        batch_size=1, accumulation=8, initialization='warm_start')
    if CFG != expected_cfg:
        raise ValueError('Unexpected baseline training configuration')
    MODEL_ID, REVISION = baseline['model_id'], baseline['revision']
    SOURCE_LIMIT = baseline['identity']['source_limit']
    TARGET_LIMIT = baseline['identity']['target_limit']
    BEAMS = baseline['identity']['beams']
    MAX_NEW_TOKENS = baseline['identity']['max_new_tokens']
    random.seed(CFG['seed']); torch.manual_seed(CFG['seed'])
    torch.cuda.manual_seed_all(CFG['seed'])
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.use_deterministic_algorithms(True, warn_only=True)
    RUNTIME_CONTROLS = dict(gradient_checkpointing=True, checkpoint_use_reentrant=False,
        cudnn_benchmark=False, cuda_matmul_allow_tf32=False, cudnn_allow_tf32=False,
        deterministic_algorithms=True, deterministic_warn_only=True)
    source = helper.SourceTokenizer(ARTIFACT, expected_size=6080)
    target = AutoTokenizer.from_pretrained(INPUT_ROOT/'target_tokenizer',
                                         src_lang='tgl_Latn', tgt_lang='tgl_Latn')
    encoded, tokenization_audit = helper.prepare(splits, source, target, SOURCE_LIMIT, TARGET_LIMIT)
    for text in ['sinulat', 'kabukasan', 'magsalita', 'pipaglutuan', 'ing an ang', '']:
        if not text: continue
        native = source.backend.encode(text, add_special_tokens=False)
        if source.content_ids(text) != [source.to_model_id(i) for i in native.ids]:
            raise ValueError('Content token parity failure')
    print('GPU:', torch.cuda.get_device_name(), 'Torch:', torch.__version__)
    print('Baseline Torch: 2.11.0+cu128; record any environment difference.')
    print(json.dumps(tokenization_audit, indent=2))
    ''')
    md('''
    ## 6. Protect a new run or verify an explicit penalty32 resume

    A new run refuses existing weights. A resume must match the exact tokenizer,
    data, helper, runtime, base and configuration. The application route remains
    `morph_bpe`, while the recorded research variant is `weighted_penalty32`.
    The existing hard-constrained checkpoint is never an initialization source.
    ''')
    code('''
    identity = dict(baseline['identity'])
    identity.update(condition='morph_bpe', tokenizer_sha256=digest(ARTIFACT/'tokenizer.json'),
                    artifact_manifest_sha256=digest(ARTIFACT/'tokenizer-manifest.json'),
                    helper_sha256=digest(INPUT_ROOT/'nllb_source_adapter.py'),
                    runtime_sha256=digest(INPUT_ROOT/'runtime/kapampangan_morphbpe_runtime/tokenizer.py'),
                    tokenizer_variant='weighted_penalty32', crossing_penalty=32,
                    runtime_controls=RUNTIME_CONTROLS,
                    training_support_sha256=digest(INPUT_ROOT/'training_support.py'),
                    split_manifest_sha256=digest(INPUT_ROOT/'reference/plain_bpe/split_manifest.json'))
    if RESUME_BUNDLE and not RESUME:
        raise ValueError('RESUME_BUNDLE requires RESUME=True')
    if RESUME_BUNDLE:
        if OUT.exists():
            raise FileExistsError('Output exists; resume it directly or choose a new RUN_NAME.')
        resume_path = Path(RESUME_BUNDLE)
        if resume_path.is_file():
            RUNS.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(dir=RUNS) as temporary:
                temp = Path(temporary)
                with zipfile.ZipFile(resume_path) as archive:
                    for entry in archive.infolist():
                        if not (temp/entry.filename).resolve().is_relative_to(temp.resolve()):
                            raise ValueError('Unsafe resume ZIP path')
                        if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                            raise ValueError('Resume ZIP links are not supported')
                    archive.extractall(temp)
                info = json.loads((temp/'manifest.json').read_text())
                if info['identity'] != identity or info['cfg'] != CFG:
                    raise ValueError('Not this exact penalty32 run/configuration')
                OUT.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(temp, OUT)
        else:
            info = json.loads((resume_path/'manifest.json').read_text())
            if info['identity'] != identity or info['cfg'] != CFG:
                raise ValueError('Not this exact penalty32 run/configuration')
            OUT.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(resume_path, OUT, ignore=shutil.ignore_patterns('__pycache__'))
    if RESUME:
        if not (OUT/'last.pt').is_file() or not (OUT/'best_source.safetensors').is_file():
            raise FileNotFoundError('Resume requires the full penalty32 backup including last.pt and best weights.')
        saved = torch.load(OUT/'last.pt', map_location='cpu', weights_only=True)
        if saved['identity'] != identity or saved['cfg'] != CFG:
            raise ValueError('Saved optimizer checkpoint does not match this run')
        if tuple(saved['source_weight'].shape) != (6080,1024) or not torch.isfinite(saved['source_weight']).all():
            raise ValueError('Invalid resumed source embedding table')
        saved_history = saved['history']
        expected_epochs = list(range(1, saved['next_epoch']+1))
        if (not saved_history or saved['next_epoch'] > CFG['epochs'] or
            [r['epoch'] for r in saved_history] != expected_epochs or
            any(not __import__('math').isfinite(r['validation_loss']) for r in saved_history) or
            not __import__('math').isfinite(saved['best']) or
            saved['best'] != min(r['validation_loss'] for r in saved_history)):
            raise ValueError('Inconsistent resumed history or checkpoint selection')
        from safetensors.torch import load_file
        saved_best = load_file(str(OUT/'best_source.safetensors'))['weight']
        if tuple(saved_best.shape) != (6080, 1024) or not torch.isfinite(saved_best).all():
            raise ValueError('Invalid saved best source weights')
        del saved, saved_best
        print('Verified resume checkpoint.')
    elif OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError('Use a new RUN_NAME or explicitly resume this penalty32 run.')
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = dict(model_id=MODEL_ID, revision=REVISION, source_vocab_size=6080,
                    source_format='kapampangan_project', source_id_mapping='swap_0_1',
                    cfg=CFG, identity=identity, adaptation='source_embedding_only',
                    target_language='tgl_Latn', source_marker='<s>',
                    tokenizer_variant='weighted_penalty32', weighted_penalty_used=True,
                    crossing_penalty=32, training_status='prepared')
    for name in ['source_artifact', 'runtime', 'target_tokenizer']:
        shutil.copytree(INPUT_ROOT/name, OUT/name, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(INPUT_ROOT/'nllb_source_adapter.py', OUT/'nllb_source_adapter.py')
    shutil.copy2(INPUT_ROOT/'training_support.py', OUT/'training_support.py')
    helper.save_json(OUT/'manifest.json', manifest)
    helper.save_json(OUT/'data_audit.json', data_audit)
    helper.save_json(OUT/'split_manifest.json', {k:[r['id'] for r in v] for k,v in splits.items()})
    helper.save_json(OUT/'tokenization_audit.json', tokenization_audit)
    helper.save_json(OUT/'baseline_reference.json', baseline)
    helper.save_json(OUT/'input_provenance.json', package)
    environment = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
    (OUT/'environment.txt').write_text(environment, encoding='utf-8')
    helper.save_json(OUT/'hardware.json', dict(torch=torch.__version__, gpu=torch.cuda.get_device_name(),
                     baseline_torch='2.11.0+cu128', python=sys.version,
                     runtime_controls=RUNTIME_CONTROLS))
    print('Separate penalty32 output prepared:', OUT)
    ''')
    md('''
    ## 7. Load the frozen base and initialize only the new source table

    The base downloads from its pinned revision if it is not cached. No old source
    embeddings are loaded for a fresh run. The preflight performs one temporary
    backward/update check and restores the weights before training.
    Gradient checkpointing uses the original non-reentrant setup to reduce GPU
    activation memory. Training does not use the generation cache.
    ''')
    code('''
    model = helper.load_base(MODEL_ID, REVISION, CFG['seed'], 6080,
                             source=source, target=target,
                             initialization=CFG['initialization']).to(DEVICE)
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
    trainable = [(name, p.numel()) for name,p in model.named_parameters() if p.requires_grad]
    if trainable != [('model.encoder.embed_tokens.weight', 6225920)]:
        raise ValueError('Only the source embedding table may train: '+str(trainable))
    print('Trainable parameters:', trainable)
    print('Preflight loss:', helper.preflight(model, encoded['train'][0], DEVICE))
    ''')
    md('''
    ## 8. Train the source embeddings and select by validation loss

    This is the GPU training cell. It uses the unchanged helper from the recorded
    30-epoch runs. Early stopping may stop before epoch 30; the lowest validation
    loss selects the inference weights. Do not claim 30 completed epochs unless
    the saved history actually contains them.
    ''')
    code('''
    import time
    started = time.time()
    history = helper.train(model, encoded, CFG, identity, OUT, DEVICE, resume=RESUME)
    best = min(history, key=lambda row:row['validation_loss'])
    from safetensors.torch import load_file
    saved_weight = load_file(str(OUT/'best_source.safetensors'))['weight']
    if tuple(saved_weight.shape) != (6080,1024) or not torch.isfinite(saved_weight).all():
        raise ValueError('Invalid exported source table')
    if not torch.equal(saved_weight, model.get_encoder().embed_tokens.weight.detach().cpu()):
        raise ValueError('Model did not restore the selected best weights')
    del saved_weight
    manifest.update(training_status='completed', completed_epochs=history[-1]['epoch'],
                    selected_epoch=best['epoch'], selected_validation_loss=best['validation_loss'])
    helper.save_json(OUT/'manifest.json', manifest)
    helper.save_json(OUT/'training_summary.json', dict(completed_epochs=history[-1]['epoch'],
                     selected_epoch=best['epoch'], best_validation_loss=best['validation_loss'],
                     configured_max_epochs=CFG['epochs'], this_session_seconds=time.time()-started,
                     tokenizer_variant='weighted_penalty32', crossing_penalty=32))
    print('Completed epochs:', history[-1]['epoch'], 'Selected epoch:', best['epoch'])
    print('Best validation loss:', best['validation_loss'])
    FULL_ZIP = Path(shutil.make_archive(str(OUT.parent/(RUN_NAME+'_full')), 'zip', root_dir=OUT))
    print('Full epoch-boundary resume backup:', FULL_ZIP)
    ''')
    md('''
    ### 8.1 Reload the saved bundle and verify one validation translation

    After completed training, reload the saved helper, source weights and tokenizers.
    The first GPU model is freed before allocating the reloaded model. Check the
    tokenizer IDs and selected weights, then generate one validation example in FP32
    with four beams and 160 new tokens. This checks the saved bundle's loading path;
    it is not a translation-quality measurement or a fresh-environment deployment test.

    Interrupted training skips this check; section 10 can still export a full resume
    backup. Completed inference export requires a passing check for the current weights.
    ''')
    code('''
    reload_info = json.loads((OUT/'manifest.json').read_text())
    if reload_info.get('training_status') != 'completed':
        print('Training unfinished: bundle reload skipped. Section 10 can save the full resume backup.')
    else:
        if reload_info['identity'] != identity or reload_info['cfg'] != CFG:
            raise ValueError('Saved bundle identity/configuration mismatch')
        for name, key in [('source_artifact/tokenizer.json','tokenizer_sha256'),
                          ('source_artifact/tokenizer-manifest.json','artifact_manifest_sha256'),
                          ('nllb_source_adapter.py','helper_sha256'),
                          ('runtime/kapampangan_morphbpe_runtime/tokenizer.py','runtime_sha256')]:
            if digest(OUT/name) != identity[key]:
                raise ValueError('Reload identity mismatch: '+name)
        from safetensors.torch import load_file
        selected_weight = load_file(str(OUT/'best_source.safetensors'))['weight']
        if tuple(selected_weight.shape) != (6080,1024) or not torch.isfinite(selected_weight).all():
            raise ValueError('Invalid selected weights for bundle reload')
        example = splits['validation'][0]['raw_source']
        expected_ids = source.encode(example)
        if 'model' in globals():
            del model
        import gc
        gc.collect()
        torch.cuda.empty_cache()
        saved_spec = importlib.util.spec_from_file_location('penalty32_saved_adapter', OUT/'nllb_source_adapter.py')
        saved_helper = importlib.util.module_from_spec(saved_spec)
        saved_spec.loader.exec_module(saved_helper)
        model, source, target = saved_helper.load_bundle(OUT, DEVICE)
        if not torch.equal(selected_weight, model.get_encoder().embed_tokens.weight.detach().cpu()):
            raise ValueError('Reloaded source weights differ from the selected checkpoint')
        if source.size != 6080 or source.encode(example) != expected_ids:
            raise ValueError('Reloaded tokenizer IDs differ from the training tokenizer')
        if model.get_encoder().embed_tokens.weight.data_ptr() == model.get_decoder().embed_tokens.weight.data_ptr():
            raise ValueError('Reloaded source and native target embeddings are incorrectly tied')
        del selected_weight
        if len(expected_ids) > SOURCE_LIMIT:
            raise ValueError('Reload example exceeds the trained source limit')
        model.eval()
        x = torch.tensor([expected_ids], device=DEVICE)
        with torch.inference_mode():
            generated = model.generate(input_ids=x, attention_mask=x.ne(source.pad).long(),
                forced_bos_token_id=target.convert_tokens_to_ids('tgl_Latn'),
                max_new_tokens=MAX_NEW_TOKENS, num_beams=BEAMS, do_sample=False, use_cache=True)
        translation = target.decode(generated[0], skip_special_tokens=True)
        reload_report = dict(status='passed', weights_sha256=digest(OUT/'best_source.safetensors'),
            tokenizer_sha256=identity['tokenizer_sha256'], selected_epoch=reload_info['selected_epoch'],
            base_revision=REVISION, beams=BEAMS, max_new_tokens=MAX_NEW_TOKENS, precision='fp32',
            validation_id=splits['validation'][0]['id'], source=example, prediction=translation)
        helper.save_json(OUT/'reload_check.json', reload_report)
        FULL_ZIP = Path(shutil.make_archive(str(OUT.parent/(RUN_NAME+'_full')), 'zip', root_dir=OUT))
        print('Saved bundle reload passed.')
        print('Kapampangan:', example)
        print('Filipino:', translation)
    ''')
    md('''
    ## 9. Optional translation evaluation with saved progress

    Both switches default to False. Validation can guide decisions; test results must
    be reserved for frozen settings. Generation uses FP32, four beams and 160 new
    tokens, matching the paired evaluation procedure. CSV reference strings are
    preserved. Evaluation identities include selected weights and package versions;
    partial runs resume only when identities and row order agree.

    Compare these outputs against Plain30 and hard-constrained Morph30 using the same
    rows and decoding precision. This cell produces only the weighted condition's
    scores. It does not establish superiority or statistical significance.
    ''')
    code('''
    from sacrebleu.metrics import BLEU, CHRF
    import importlib.metadata as metadata
    torch.backends.cuda.matmul.allow_tf32 = False
    eval_splits = ([] if not RUN_VALIDATION_TRANSLATIONS else ['validation']) + ([] if not RUN_TEST else ['test'])
    if eval_splits:
        model.eval()
        evaluation_manifest = json.loads((OUT/'manifest.json').read_text())
        if evaluation_manifest.get('training_status') != 'completed':
            raise ValueError('Finish training before generating scored translations.')
        from safetensors.torch import load_file
        evaluation_weight = load_file(str(OUT/'best_source.safetensors'))['weight']
        if not torch.equal(evaluation_weight, model.get_encoder().embed_tokens.weight.detach().cpu()):
            raise ValueError('Evaluation model is not using the selected best checkpoint.')
        del evaluation_weight
    for split in eval_splits:
        rows = splits[split]
        destination = OUT/'evaluation'/split
        destination.mkdir(parents=True, exist_ok=True)
        evaluation_identity = dict(condition='morph_bpe', tokenizer_variant='weighted_penalty32',
            split=split, data_sha256=EXPECTED_DATA_SHA256,
            weights_sha256=digest(OUT/'best_source.safetensors'), tokenizer_sha256=identity['tokenizer_sha256'],
            row_ids_sha256=hashlib.sha256(json.dumps([r['id'] for r in rows]).encode()).hexdigest(),
            base_revision=REVISION, beams=BEAMS, max_new_tokens=MAX_NEW_TOKENS,
            precision='fp32', torch=torch.__version__, transformers=transformers.__version__,
            sacrebleu=metadata.version('sacrebleu'), helper_sha256=identity['helper_sha256'])
        identity_file = destination/'evaluation_identity.json'
        if identity_file.exists():
            if json.loads(identity_file.read_text()) != evaluation_identity:
                raise ValueError('Evaluation resume identity mismatch')
        else:
            helper.save_json(identity_file, evaluation_identity)
        prediction_file = destination/'predictions.jsonl'
        completed = []
        if prediction_file.exists():
            lines = prediction_file.read_text(encoding='utf-8').splitlines()
            for index, line in enumerate(lines):
                try: record = json.loads(line)
                except json.JSONDecodeError:
                    if index != len(lines)-1: raise
                    break
                row = rows[len(completed)]
                if record['id'] != row['id'] or record['source'] != row['raw_source'] or record['target'] != row['raw_target']:
                    raise ValueError('Evaluation row mismatch')
                completed.append(record)
            prediction_file.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\\n' for r in completed), encoding='utf-8')
        with prediction_file.open('a', encoding='utf-8') as handle:
            for index in range(len(completed), len(rows)):
                row = rows[index]
                ids = source.encode(row['raw_source'])
                if len(ids) > SOURCE_LIMIT:
                    raise ValueError('Evaluation source exceeds unchanged trained limit')
                x = torch.tensor([ids], device=DEVICE)
                with torch.inference_mode():
                    generated = model.generate(input_ids=x, attention_mask=x.ne(source.pad).long(),
                        forced_bos_token_id=target.convert_tokens_to_ids('tgl_Latn'),
                        max_new_tokens=MAX_NEW_TOKENS, num_beams=BEAMS, do_sample=False, use_cache=True)
                record = dict(id=row['id'], source=row['raw_source'], target=row['raw_target'],
                              prediction=target.decode(generated[0], skip_special_tokens=True))
                handle.write(json.dumps(record,ensure_ascii=False)+'\\n'); handle.flush()
                completed.append(record)
                if (index+1) % 25 == 0 or index+1 == len(rows):
                    print(split, index+1, '/', len(rows))
        hypotheses = [r['prediction'] for r in completed]
        references = [r['target'] for r in completed]
        metrics = {}
        for name, metric in [('BLEU',BLEU(tokenize='13a')), ('chrF++',CHRF(word_order=2))]:
            metrics[name] = dict(score=metric.corpus_score(hypotheses,[references]).score,
                                 signature=str(metric.get_signature()))
        helper.save_json(destination/'metrics.json', metrics)
        (destination/'hypotheses.txt').write_text('\\n'.join(hypotheses)+'\\n', encoding='utf-8')
        (destination/'references.txt').write_text('\\n'.join(references)+'\\n', encoding='utf-8')
        print(split, metrics)
    if not eval_splits:
        print('Translation evaluation skipped. Set the relevant switch and rerun this cell when appropriate.')
    ''')
    md('''
    ## 10. Export installable inference and full training backups

    The inference ZIP puts `manifest.json` at its root for the repository installer.
    It omits optimizer checkpoints and therefore cannot resume training. Keep the
    separate full ZIP for resume. No ZIP contains the frozen NLLB model weights.
    If you interrupt training after a saved epoch, run this cell to create the full
    backup anyway; inference export is skipped until the training cell finishes.
    Completed inference export also requires the passing section 8.1 reload check.

    After evaluating, back up the application's current hard-constrained Morph30,
    install the new complete inference bundle into `nllb/checkpoints/morph_bpe`, and
    restart the backend. App descriptions that currently say hard-constrained must
    also be updated to identify the installed weighted penalty-32 condition. The
    existing Plain BPE bundle can remain when the comparison protocol is matched.
    ''')
    code('''
    info = json.loads((OUT/'manifest.json').read_text())
    if not (OUT/'last.pt').is_file() or not (OUT/'best_source.safetensors').is_file():
        raise ValueError('At least one completed epoch is required for a full resume backup')
    for name,key in [('source_artifact/tokenizer.json','tokenizer_sha256'),
                     ('source_artifact/tokenizer-manifest.json','artifact_manifest_sha256'),
                     ('nllb_source_adapter.py','helper_sha256'),
                     ('runtime/kapampangan_morphbpe_runtime/tokenizer.py','runtime_sha256')]:
        if digest(OUT/name) != info['identity'][key]:
            raise ValueError('Export identity mismatch: '+name)
    FULL_ZIP = Path(shutil.make_archive(str(OUT.parent/(RUN_NAME+'_full')), 'zip', root_dir=OUT))
    exports = [FULL_ZIP]
    reload_path = OUT/'reload_check.json'
    reload_ok = False
    if reload_path.is_file():
        report = json.loads(reload_path.read_text())
        reload_ok = (report.get('status') == 'passed' and
                     report.get('weights_sha256') == digest(OUT/'best_source.safetensors') and
                     report.get('tokenizer_sha256') == info['identity']['tokenizer_sha256'] and
                     report.get('base_revision') == info['revision'])
    if info.get('training_status') == 'completed' and reload_ok:
        INFERENCE_ZIP = OUT.parent/(RUN_NAME+'_inference.zip')
        with zipfile.ZipFile(INFERENCE_ZIP, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(OUT.rglob('*')):
                rel = file.relative_to(OUT)
                if not file.is_file() or '__pycache__' in rel.parts or file.suffix == '.pt': continue
                archive.write(file, str(rel).replace('\\\\','/'))
        exports.insert(0,INFERENCE_ZIP)
        print('Inference ZIP:', INFERENCE_ZIP)
    else:
        print('Full resume backup saved; inference export needs completed training and a passing section 8.1 reload check.')
    sums = OUT.parent/(RUN_NAME+'_SHA256SUMS.txt')
    sums.write_text(''.join(digest(p)+'  '+p.name+'\\n' for p in exports), encoding='utf-8')
    print('Full resume ZIP:', FULL_ZIP)
    print('Checksums:', sums)
    from IPython.display import display, FileLink
    for file in [*exports,sums]: display(FileLink(str(file)))
    ''')
    return dict(cells=cells, metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3'),
                language_info=dict(name='python', version='3.11'),
                colab=dict(name=NOTEBOOK_NAME, provenance=[])), nbformat=4, nbformat_minor=5)


def build(csv_path=None):
    artifact = ROOT/'webapp/backend/tokenizer/artifacts/morphbpe-penalty32'
    plain = ROOT/'nllb/checkpoints/plain_bpe'
    morph = ROOT/'nllb/checkpoints/morph_bpe'
    baseline = json.loads((plain/'manifest.json').read_text())
    selected = json.loads((artifact/'tokenizer-manifest.json').read_text())
    if baseline['identity']['data_sha256'] != EXPECTED_DATA or selected['artifact_fingerprint'] != FINGERPRINT:
        raise ValueError('Reference dataset or visualization tokenizer changed. Review before rebuilding.')
    files = {}

    def add(name, path):
        files[name] = Path(path).read_bytes()

    add('nllb_source_adapter.py', morph/'nllb_source_adapter.py')
    if sha(files['nllb_source_adapter.py']) != baseline['identity']['helper_sha256']:
        raise ValueError('Installed training helper does not match Plain BPE baseline')
    add('training_support.py', HERE/'training_support.py')
    for path in sorted(artifact.iterdir()):
        if path.is_file(): add('source_artifact/'+path.name, path)
    runtime = ROOT/'webapp/backend/tokenizer/kapampangan_morphbpe_runtime'
    for name in ['__init__.py','tokenizer.py']:
        add('runtime/kapampangan_morphbpe_runtime/'+name, runtime/name)
    for path in sorted((plain/'target_tokenizer').iterdir()):
        if path.is_file(): add('target_tokenizer/'+path.name, path)
    for name in ['manifest.json','data_audit.json','split_manifest.json','history.json','tokenization_audit.json']:
        add('reference/plain_bpe/'+name, plain/name)
    for name in ['manifest.json','history.json']:
        add('reference/morph_bpe/'+name, morph/name)
    if csv_path:
        content = Path(csv_path).read_bytes()
        if sha(content) != EXPECTED_DATA:
            raise ValueError('CSV does not match current baseline')
        files['data/kpm_tgl_cleaned.csv'] = content
    inventory = {name:sha(content) for name,content in sorted(files.items())}
    package = dict(package_kind='penalty32_source_training', format_version=1,
                   tokenizer_variant='weighted_penalty32', crossing_penalty=32,
                   tokenizer_fingerprint=FINGERPRINT, expected_data_sha256=EXPECTED_DATA,
                   csv_included=bool(csv_path), trained_source_weights_included=False,
                   files=inventory)
    files['package_manifest.json'] = (json.dumps(package, indent=2)+'\n').encode()
    archive_path = HERE/PACKAGE_NAME
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026,10,7,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    package_sha = sha(archive_path.read_bytes())
    notebook = make_notebook(package_sha, sha(files['package_manifest.json']))
    for index, cell in enumerate(notebook['cells']):
        cell['id'] = f'penalty32-{index:02d}'
        if cell['cell_type'] == 'code': compile(cell['source'], f'cell-{index}', 'exec')
    notebook_path = ROOT/'notebooks'/NOTEBOOK_NAME
    notebook_path.write_text(json.dumps(notebook,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    (HERE/'SHA256SUMS.txt').write_text(package_sha+'  '+PACKAGE_NAME+'\n'+sha(notebook_path.read_bytes())+'  '+NOTEBOOK_NAME+'\n', encoding='utf-8')
    print(json.dumps(dict(notebook=str(notebook_path), package=str(archive_path),
          package_bytes=archive_path.stat().st_size, package_sha256=package_sha,
          package_files=len(files), code_cells=sum(c['cell_type']=='code' for c in notebook['cells']),
          csv_included=bool(csv_path)), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, help='Optional exact matching CSV to include privately')
    build(parser.parse_args().csv)
