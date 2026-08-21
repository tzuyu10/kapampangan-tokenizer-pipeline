# Internet Root Reconciliation V1

This isolated evidence pass covers every distinct `word` pretoken in the
preserved source-adjudicated training stream. It does not modify a training
lexicon, a tokenizer artifact, or an existing experiment.

The audit separates three questions that must not be conflated:

1. Is the complete word attested in a Kapampangan lexical source?
2. Is a mechanically reconstructed host attested?
3. Does a source actually organize that host as a root or stem?

Only the third question supports nomination as a provisional root candidate. A
dictionary headword alone can be derived or inflected, so Samson, Bergaño, ACD,
UCLA, and Wiktionary/Kaikki matches remain corroborating lexical evidence unless
the source explicitly identifies a root. Forman is root-oriented because its
introduction describes approximately 3,500 roots and places derived/inflected
forms under them. The extractor still excludes Forman cross-reference entries
and its explicitly unaffixable particles/substitutes from root evidence.

## Inputs

The runner verifies the preserved stream and operational resources before
processing. Large downloads, extracted headword indexes, and full CSV reports
stay under ignored `runs/` or ignored report paths because source redistribution
rights differ.

Expected online downloads:

```powershell
curl.exe -L 'https://kaikki.org/dictionary/Kapampangan/kaikki.org-dictionary-Kapampangan.jsonl' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/kaikki-kapampangan.jsonl'
curl.exe -L 'https://raw.githubusercontent.com/lexibank/acd/v1.2/cldf/forms.csv' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/acd-forms-v1.2.csv'
curl.exe -L 'https://raw.githubusercontent.com/lexibank/acd/v1.2/cldf/languages.csv' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/acd-languages-v1.2.csv'
curl.exe -L 'https://archive.phonetics.ucla.edu/Language/PAM/pam_word-list_1974_01.html' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/ucla-pam-1974.html'
curl.exe -L 'https://archive.phonetics.ucla.edu/Language/PAM/pam_word-list_1987_01.html' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/ucla-pam-1987.html'
curl.exe -L 'https://archive.phonetics.ucla.edu/Language/PAM/pam_word-list_1994_01.html' -o 'experiments/internet_root_reconciliation_v1/runs/downloads/ucla-pam-1994.html'
```

Run with the bundled document Python runtime, which provides `pypdf`:

```powershell
& 'C:\Users\Ken Audie\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  '.\experiments\internet_root_reconciliation_v1\run_reconciliation.py' `
  --forman-pdf 'D:\Downloads\Forman-KapampanganDictionary-1971.pdf' `
  --bergano-pdf 'D:\Downloads\Vocabulario De Pampango Fray DIEGO BERGAÑO Translated by Venacio O. Samson (DIEGO BERGAÑO) (z-library.sk, 1lib.sk, z-lib.sk).pdf' `
  --samson-pdf 'D:\Coding\thesis\pdf-dls\ilide.info-kapampangandictionaryamongsamson-1-pr_8a0f2e64d024628a4ab7b876563dc425.pdf' `
  --kaikki-jsonl '.\experiments\internet_root_reconciliation_v1\runs\downloads\kaikki-kapampangan.jsonl' `
  --acd-forms '.\experiments\internet_root_reconciliation_v1\runs\downloads\acd-forms-v1.2.csv' `
  --acd-languages '.\experiments\internet_root_reconciliation_v1\runs\downloads\acd-languages-v1.2.csv' `
  --ucla-html-dir '.\experiments\internet_root_reconciliation_v1\runs\downloads'
```

## Outputs

- `reports/word-evidence.csv`: exactly one row per dataset word type.
- `reports/candidate-evidence.csv`: every direct-root and frozen-rule mechanical
  hypothesis for every word type.
- `reports/reconciliation-summary.md`: concise counts, source limitations, and
  retraining recommendations.
- `reports/reconciliation-manifest.json`: input/output hashes and preservation
  checks.
- `runs/source-indexes/*.jsonl`: page/record-addressable extracted source forms.

The output is an adjudication queue, not a gold morphology reference. Retraining
must happen only after reviewing conflicts, orthographic variants, corpus noise,
and the closed-set limitations of standard BPE inference.
