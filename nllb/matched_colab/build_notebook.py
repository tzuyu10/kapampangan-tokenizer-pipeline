"""Rebuild the self-contained Colab notebook from the companion source module."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
cells = []
def md(s):
    cells.append({"cell_type":"markdown", "metadata":{}, "source":s.strip()+"\n"})
def code(s):
    cells.append({"cell_type":"code", "metadata":{}, "execution_count":None, "outputs":[], "source":s.strip()+"\n"})

md('''# NLLB-200 600M: Kapampangan → Filipino
**Source-embedding adaptation with pluggable source tokenizers.**

This notebook follows the two-page revised SOP in `G4-THESIS-MAIN-DOCU (9).pdf`:
plain BPE versus proposed Morph-BPE for translation, both with 6,080 source IDs.
The 72-page manuscript's embedding-only training recipe is retained.
The Filipino target tokenizer and all pretrained model weights remain frozen.

You must supply validated parallel translations. No dataset, proposed tokenizer,
trained model, or thesis results are fabricated here. The optional plain-BPE trainer
lets you establish the baseline first. Your Morph-BPE trainer remains a separate artifact.

**Before running:** choose Runtime → Change runtime type → GPU. Upload this notebook
through File → Upload notebook in [Google Colab](https://colab.research.google.com/).
Read README.md for scientific conflicts, file formats, and resume instructions.''')
md('''## 1. Install the pinned training stack
Run this first in a fresh runtime. It retains Colab's GPU-enabled PyTorch.
If packages were already imported, restart the runtime after installation and continue
from section 2. The CPU integration test uses PyTorch 2.6.0; GPU behavior must be checked
by the preflight cell in your actual Colab runtime.''')
code('''%pip -q install "transformers==4.48.3" "tokenizers==0.21.0" "sentencepiece==0.2.0" "sacrebleu==2.5.1" "safetensors==0.5.3" "huggingface-hub==0.28.1"
# These optional vision/audio packages are not used by this text model. Remove them
# to avoid incompatible torchvision/torchaudio imports in some Colab images.
%pip -q uninstall -y torchvision torchaudio''')
md('''## 2. Storage and experiment configuration
Use the same data, base revision, vocabulary size, seed, schedule, lengths, and decoding
settings for both conditions. Start with `plain_bpe`, then run `morph_bpe` in a fresh runtime.
The initial hyperparameters below are starter choices, not claimed optimal thesis settings.
Fix them using validation before the final matched experiments.''')
code('''from google.colab import drive
drive.mount('/content/drive')
from pathlib import Path
ROOT = Path('/content/drive/MyDrive/kapampangan_nllb')
ROOT.mkdir(parents=True, exist_ok=True)
DATA_PATH = ROOT / 'parallel.csv'
CONDITION = 'plain_bpe'  # 'plain_bpe' or 'morph_bpe'
TOKENIZER_PATH = ROOT / CONDITION / 'tokenizer.json'
PROVENANCE_PATH = ROOT / CONDITION / 'provenance.json'
TRAIN_PLAIN_BPE = True  # False for an existing tokenizer; MUST be False for morph_bpe
SOURCE_VOCAB_SIZE = 6080  # TOTAL IDs, including five control tokens
MODEL_ID = 'facebook/nllb-200-distilled-600M'
BASE_REVISION = 'f8d333a098d19b4fd9a8b18f94170487ad3f821d'  # verified base commit
RUN_NAME = 'seed42_v1'
OUT = ROOT / 'runs' / CONDITION / RUN_NAME
RESUME = False  # True resumes the last completed epoch; keep all settings identical
CFG = dict(seed=42, epochs=10, lr=1e-3, batch_size=1, accumulation=16)
MAX_SOURCE_TOKENS = 128
MAX_TARGET_TOKENS = 128
MAX_NEW_TOKENS = 128
NUM_BEAMS = 4
RUN_TEST = False  # set True only after finalizing settings using validation
assert CONDITION in {'plain_bpe', 'morph_bpe'}
assert not TRAIN_PLAIN_BPE or CONDITION == 'plain_bpe'
assert 2 < MAX_SOURCE_TOKENS <= 512 and 2 < MAX_TARGET_TOKENS <= 512
assert MAX_NEW_TOKENS >= MAX_TARGET_TOKENS
assert all(CFG[k] > 0 for k in ['epochs','lr','batch_size','accumulation'])''')
md('''## 3. Write the training helper
The complete helper is embedded below; no GitHub repository or separate upload is required.
It replaces only `model.encoder.embed_tokens`, preserves the original embedding scaling,
and saves a small source adapter rather than an incorrectly tied full model.''')
code('%%writefile /content/nllb_source_adapter.py\n'+(ROOT/'nllb_source_adapter.py').read_text(encoding='utf8'))
code('''import sys, json, shutil, hashlib, subprocess, platform
sys.path.insert(0, '/content')
import torch, transformers, tokenizers
from huggingface_hub import model_info
from transformers import AutoTokenizer
from nllb_source_adapter import *
assert torch.cuda.is_available(), 'Select a GPU runtime before continuing.'
device = torch.device('cuda')
print('GPU:', torch.cuda.get_device_name(0))
print('PyTorch:', torch.__version__, 'Transformers:', transformers.__version__)
assert transformers.__version__ == '4.48.3'
torch.backends.cudnn.benchmark = False
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.use_deterministic_algorithms(True, warn_only=True)
OUT.mkdir(parents=True, exist_ok=True)
lock = ROOT / 'base_revision.json'
if lock.exists():
    locked = json.loads(lock.read_text())
    assert locked['model_id'] == MODEL_ID
    REVISION = locked['revision']
    assert BASE_REVISION == 'main' or BASE_REVISION == REVISION
else:
    REVISION = model_info(MODEL_ID, revision=BASE_REVISION).sha
    save_json(lock, {'model_id': MODEL_ID, 'revision': REVISION})
print('Locked base revision:', REVISION)''')
md('''## 4. Validate the parallel corpus and export tokenizer-training text
Required CSV/JSONL columns: `id,source,target,split,group_id`.
`source` is raw Kapampangan; `target` is validated Filipino. Splits are exactly
`train`, `validation`, `test`. Prepare an approximately 80/10/10 partition by document
group before tokenizer training; keep related verses/articles/conversations together.
The notebook rejects repeated source sentences and groups appearing in multiple splits.
It does not silently invent translations or automatically reassign your splits.

Train **both** tokenizers on `tokenizer_train.txt` only. Audit morphology and domain
balance separately; a group split alone does not guarantee stratification.''')
code('''splits = read_parallel(DATA_PATH)
corpus = '\\n'.join(row['source'] for row in splits['train']) + '\\n'
CORPUS_PATH = ROOT / 'tokenizer_train.txt'
CORPUS_PATH.write_text(corpus, encoding='utf-8')
CORPUS_HASH = digest(CORPUS_PATH)
print({k: len(v) for k,v in splits.items()})
print('Training corpus SHA256:', CORPUS_HASH)
save_json(OUT/'split_manifest.json', {k:[r['id'] for r in v] for k,v in splits.items()})''')
md('''## 5. Train plain BPE OR plug in the proposed tokenizer
The optional trainer below is deliberately ordinary unconstrained BPE.
It is **not** an implementation of your proposed morphology algorithm.
It uses NFC/whitespace normalization and whitespace/punctuation pre-tokenization.
Match these choices in your proposed trainer, changing only morphology constraints.

For Morph-BPE: set `TRAIN_PLAIN_BPE=False`; place the complete exported
`tokenizer.json` and `provenance.json` at the configured paths. Encoding must work
on raw text without a runtime dictionary. See the README for the export contract.
Do not rename a plain BPE artifact and call it Morph-BPE.''')
code('''if TRAIN_PLAIN_BPE:
    from tokenizers import Tokenizer, models, pre_tokenizers, trainers
    if TOKENIZER_PATH.exists():
        print('Using existing tokenizer; no retraining. Delete neither artifact casually.')
    else:
        backend = Tokenizer(models.BPE(unk_token='<unk>'))
        backend.pre_tokenizer = pre_tokenizers.Whitespace()
        trainer = trainers.BpeTrainer(vocab_size=SOURCE_VOCAB_SIZE, min_frequency=2,
            special_tokens=['<s>', '<pad>', '</s>', '<unk>', '<kap>'], show_progress=True)
        backend.train_from_iterator((r['source'] for r in splits['train']), trainer=trainer)
        if backend.get_vocab_size() != SOURCE_VOCAB_SIZE:
            raise ValueError('Corpus did not yield 6080 real tokens. Supply more training text; do not add dummy tokens to meet the count.')
        TOKENIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
        backend.save(str(TOKENIZER_PATH))
        save_json(PROVENANCE_PATH, dict(condition='plain_bpe', vocab_size=SOURCE_VOCAB_SIZE,
            training_corpus_sha256=CORPUS_HASH, tokenizer_sha256=digest(TOKENIZER_PATH),
            normalization='NFC + whitespace collapse', pretokenizer='Whitespace',
            min_frequency=2, runtime_dictionary=False))
provenance = json.loads(PROVENANCE_PATH.read_text(encoding='utf-8'))
assert provenance['condition'] == CONDITION
assert provenance['vocab_size'] == SOURCE_VOCAB_SIZE
assert provenance['training_corpus_sha256'] == CORPUS_HASH, 'Tokenizer trained on a different corpus'
assert provenance['tokenizer_sha256'] == digest(TOKENIZER_PATH)
assert provenance['runtime_dictionary'] is False
source = SourceTokenizer(TOKENIZER_PATH, SOURCE_VOCAB_SIZE)
target = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION,
    src_lang='tgl_Latn', tgt_lang='tgl_Latn', use_fast=True)
# No claim that tgl_Latn represents Kapampangan: only text_target is used here.
encoded, token_stats = prepare(splits, source, target, MAX_SOURCE_TOKENS, MAX_TARGET_TOKENS)
save_json(OUT/'tokenization_audit.json', token_stats)
print(token_stats)
print('Source format:', source.encode(splits['train'][0]['source'])[:20])
print('Target prefix:', target.convert_ids_to_tokens(encoded['train'][0]['labels'][:5]))
assert encoded['train'][0]['labels'][0] == target.convert_tokens_to_ids('tgl_Latn')
assert encoded['train'][0]['labels'][-1] == target.eos_token_id
if any(v['unknown_fraction'] > 0.01 for v in token_stats.values()):
    print('WARNING: >1% unknown tokens in at least one split. Inspect coverage before training.')''')
md('''## 6. Load NLLB and verify the architecture
Source IDs address a fresh source table. Target IDs address NLLB's original decoder
table. The numeric ID spaces are independent. Do not call `resize_token_embeddings`,
`set_input_embeddings`, or `tie_weights` after this modification.

The backward test verifies that source weights can learn while pretrained weights are
frozen, then restores the source table before training.''')
code('''model = load_base(MODEL_ID, REVISION, CFG['seed'], SOURCE_VOCAB_SIZE).to(device)
model.config.use_cache = False
model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant': False})
print('Trainable parameters:', sum(p.numel() for p in model.parameters() if p.requires_grad))
print('Source table:', tuple(model.get_encoder().embed_tokens.weight.shape))
print('Decoder table:', tuple(model.get_decoder().embed_tokens.weight.shape))
print('Backward preflight loss:', preflight(model, encoded['train'][0], device))''')
md('''## 7. Train and checkpoint
Only source embeddings train. Constant-rate AdamW, token-weighted loss accumulation,
gradient clipping, FP16 autocast and gradient scaling are used. Every epoch saves the
source table, optimizer, and scaler. The best adapter is selected by validation loss.
An interruption mid-epoch resumes from the last **completed** epoch.
No test scores are used for checkpoint selection.''')
code('''identity = dict(data_sha256=digest(DATA_PATH), tokenizer_sha256=digest(TOKENIZER_PATH),
    corpus_sha256=CORPUS_HASH, model_id=MODEL_ID, revision=REVISION, condition=CONDITION,
    source_limit=MAX_SOURCE_TOKENS, target_limit=MAX_TARGET_TOKENS,
    max_new_tokens=MAX_NEW_TOKENS, beams=NUM_BEAMS,
    helper_sha256=digest('/content/nllb_source_adapter.py'))
manifest = dict(model_id=MODEL_ID, revision=REVISION, source_vocab_size=source.size,
    cfg=CFG, identity=identity, adaptation='source_embedding_only',
    target_language='tgl_Latn', source_marker='<kap>')
if (OUT/'manifest.json').exists():
    assert json.loads((OUT/'manifest.json').read_text()) == manifest, 'Run identity mismatch'
save_json(OUT/'manifest.json', manifest)
shutil.copy2(TOKENIZER_PATH, OUT/'source_tokenizer.json')
shutil.copy2(PROVENANCE_PATH, OUT/'provenance.json')
shutil.copy2('/content/nllb_source_adapter.py', OUT/'nllb_source_adapter.py')
target.save_pretrained(OUT/'target_tokenizer')
(OUT/'environment.txt').write_text(subprocess.check_output([sys.executable,'-m','pip','freeze'], text=True))
history = train(model, encoded, CFG, identity, OUT, device, resume=RESUME)''')
md('''## 8. Validation translations and BLEU / chrF++
Metrics use detokenized Filipino strings and one reference per sentence. chrF++ uses
word order 2. Scores and SacreBLEU signatures are saved alongside ordered predictions.
These validation scores may guide development; they are not final test results.''')
code('''val_predictions = predict(model, source, target, splits['validation'], device,
    MAX_NEW_TOKENS, NUM_BEAMS)
print(score_and_export(splits['validation'], val_predictions, OUT/'validation'))''')
md('''## 9. Held-out test (explicit opt-in)
After fixing the recipe, set `RUN_TEST=True` in section 2 and rerun this cell.
Run both tokenizer conditions and multiple matched seeds before interpreting effects.
A single run cannot establish either null hypothesis.''')
code('''if RUN_TEST:
    test_predictions = predict(model, source, target, splits['test'], device,
        MAX_NEW_TOKENS, NUM_BEAMS)
    print(score_and_export(splits['test'], test_predictions, OUT/'test'))
else:
    print('Test evaluation skipped. Finalize the recipe on validation first.')''')
md('''## 10. Reload and translate
The export is an adapter bundle, not a standalone `AutoModel` directory. It includes
the tokenizer, learned source weights and a locked base-model revision. Reloading
downloads the frozen base if it is not cached. A generic NLLB loader would restore the
original shared embedding architecture and must not be used for this folder.''')
code('''# Free the first model before reloading on the GPU.
del model
import gc
gc.collect(); torch.cuda.empty_cache()
model, source, target = load_bundle(OUT, device)
example = splits['validation'][0]['source']
assert len(source.encode(example)) <= MAX_SOURCE_TOKENS
print('Kapampangan:', example)
print('Filipino:', predict(model, source, target, [{'source':example}], device,
                          MAX_NEW_TOKENS, NUM_BEAMS)[0])
print('Saved adapter bundle:', OUT)''')
md('''## Scope and next experiments
- Translation control: plain BPE. Proposed condition: Morph-BPE. Both use the same recipe.
- Unigram-LM belongs to the separate intrinsic tokenizer comparison. This notebook does
  not compute morpheme boundary or morphological consistency F1 without validated gold data.
- Native NLLB is only a supplementary reference. Kapampangan has no native language tag;
  a proxy-tag evaluation must be labeled explicitly, not called native Kapampangan support.
- If embedding-only adaptation underfits, preregister an additional matched encoder/LoRA
  experiment. Do not improve only one condition's adaptation recipe.
- See README.md for conflicts and changes suggested for the manuscript.

Technical sources: [NLLB model card](https://huggingface.co/facebook/nllb-200-distilled-600M),
[NLLB tokenizer documentation](https://huggingface.co/docs/transformers/model_doc/nllb),
[SacreBLEU](https://github.com/mjpost/sacrebleu).''')
notebook = {"nbformat":4,"nbformat_minor":5,"metadata":{"colab":{"name":"NLLB_600M_Kapampangan_Training.ipynb","provenance":[]},"accelerator":"GPU","kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},"language_info":{"name":"python"}},"cells":cells}
for i,c in enumerate(cells): c['id'] = f'cell-{i:03d}'
(ROOT/'NLLB_600M_Kapampangan_Training.ipynb').write_text(json.dumps(notebook,indent=1,ensure_ascii=False),encoding='utf8')
print('Built notebook:',len(cells),'cells')
