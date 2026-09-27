# MT smoke-test data — NOT thesis evidence

`parallel_pam_tgl_smoketest.csv` is a **21-row, hand-authored placeholder
corpus** written by an AI assistant to exercise the NLLB fine-tuning /
evaluation / statistics code paths end to end. It exists purely to prove the
pipeline in `src/kapampangan_morphbpe/mt/` runs without errors on real
tensors and produces real BLEU/chrF++/statistical-test output shapes.

## Do not use this file as thesis data

- It was **not** collected from the Philippine Languages Online Corpora, any
  religious text, any native-speaker consultation, or any web source named in
  the thesis proposal.
- It was **not** validated by a Kapampangan speaker or linguist.
- It contains 21 pairs, not the ~13,000 the thesis methodology requires, and
  most rows are number words or short fixed phrases, not natural sentences.
- Any BLEU/chrF++/fertility/F1/p-value produced by running the pipeline on
  this file is a **code-path check**, not evidence for or against either
  null hypothesis in the thesis. Every report the pipeline writes from this
  file is stamped `"evidence_status": "fabricated_smoketest_not_thesis_data"`
  for this reason — treat any report without that stamp as suspect.

## Provenance

Kapampangan number words (`metung`..`apulu`) and the greeting/thanks pair
(`Kumusta ka?`, `Masalamat.`) are commonly attested basic vocabulary items.
Everything beyond single words (the short combined sentences) is an assistant
-authored concatenation for length/variety, not an attested natural sentence.
Treat all of it as synthetic test fixture data, equivalent to `"foo bar baz"`
in an English unit test.

## When real data is available

Replace this file with the real corpus in the same schema
(`id,pam_text,tgl_text,split`) and re-run the pipeline — no code changes
required. See `docs/MT_PIPELINE_README.md` for the schema contract and the
full command sequence.
