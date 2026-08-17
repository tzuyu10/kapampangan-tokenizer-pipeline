# Reproducibility

## Environment

The completed local run used Windows, Python 3.13.3, Rust/Cargo 1.97.1, and a
project-local `.venv`. The pinned build/test tools are maturin 1.9.4,
pytest 8.4.1, Hypothesis 6.138.15, mypy 1.17.1, and Ruff 0.12.10. Training is a
CPU/corpus workload; no GPU is required.

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-lock.txt
uv pip install --python .venv\Scripts\python.exe -e .
```

## End-to-end Windows commands

Set an explicit immutable dataset path; no command relies on a hidden local
default.

```powershell
$D = '<DATASET_ROOT>/kapampangan-general-corpus-v1'
$K = '.\.venv\Scripts\kapampangan-morphbpe.exe'

& $K verify-dataset --dataset-root $D --output .\reports\dataset-verification-final.json
& $K build-lexicon --dataset-root $D --output-dir .\resources
& $K verify-segmentation-parity --dataset-root $D --lexicon .\resources\training-lexicon.json --output .\reports\segmentation-parity.json
& $K prepare-training --dataset-root $D --lexicon .\resources\training-lexicon.json --output-dir .\runs\prepared --engine rust
& $K freeze-candidates --prepared-manifest .\runs\prepared\training-stream-manifest.json --output .\configs\candidate-grid.json
& $K train-candidates --prepared-stream .\runs\prepared\training-stream.jsonl --prepared-manifest .\runs\prepared\training-stream-manifest.json --grid .\configs\candidate-grid.json --lexicon-manifest .\resources\training-lexicon-manifest.json --output-dir .\artifacts\candidates
& $K evaluate-validation --dataset-root $D --lexicon .\resources\training-lexicon.json --candidates-dir .\artifacts\candidates --grid .\configs\candidate-grid.json --reports-dir .\reports\validation
& $K select-candidate --grid .\configs\candidate-grid.json --validation-report .\reports\validation\validation-candidates.json --output .\configs\selected-candidate.json
& $K finalize-tokenizer --prepared-stream .\runs\prepared\training-stream.jsonl --selection .\configs\selected-candidate.json --lexicon-manifest .\resources\training-lexicon-manifest.json --prepared-manifest .\runs\prepared\training-stream-manifest.json --output-dir .\artifacts\selected-tokenizer --rebuild-dir .\artifacts\determinism-rebuild
& $K validate-artifact --artifact .\artifacts\selected-tokenizer
& $K verify-runtime-independence --artifact .\artifacts\selected-tokenizer --runtime-root .\runtime --output .\reports\runtime-independence.json
& $K export-nllb-contract --artifact .\artifacts\selected-tokenizer --output-dir .\nllb
```

Grid freezing occurs before validation evaluation. Finalization consumes train
only and trains twice internally. No manual JSON edit occurs between stages.

## Validation commands

```powershell
.\.venv\Scripts\pytest.exe -q -p no:cacheprovider --basetemp=.test-tmp
.\.venv\Scripts\ruff.exe check src runtime tests scripts
.\.venv\Scripts\mypy.exe src runtime
cargo test --manifest-path rust\Cargo.toml
python -m json.tool notebooks\tokenizer-training-colab.ipynb > $null
```

`notebooks/tokenizer-training-colab.ipynb` provides the same staged workflow
for an uploaded or mounted package and uses only generic `/content` paths.

## Dataset validator note

The package's derived-view validator passes. The shipped full validator reports
an extra unchecksummed `HANDOFF.md` portability-policy failure. Without changing
the package, its validator core passed all 127 canonical checksummed files when
that one noncanonical extra path was excluded from file iteration. This project
then independently checks every required input hash/count and never uses a
derived training representation.
