"""NLLB-200 Distilled 600M translation pipeline (thesis Chapter 3, System Architecture).

This subpackage is optional: importing `kapampangan_morphbpe` does not import
`kapampangan_morphbpe.mt`, and the tokenizer install (`pip install
kapampangan-morphbpe`) does not pull in torch/transformers/sacrebleu/scipy.
Install the `mt` extra to use this subpackage; see
`docs/MT_PIPELINE_README.md`.
"""

from __future__ import annotations
