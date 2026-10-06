from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .constants import DATASET_FINGERPRINT, SCHEMA_VERSION
from .dataset import read_id_text
from .lexicon import load_lexicon
from .morphology import MorphologicalSegmenter
from .pretokenizer import pretokenize_normalized
from .rust_bridge import RustMorphologicalSegmenter
from .serialization import fingerprint, write_json


def verify_python_rust_parity(
    dataset_root: Path,
    lexicon_path: Path,
    output_path: Path,
) -> dict[str, object]:
    lexicon = load_lexicon(lexicon_path)
    python_segmenter = MorphologicalSegmenter(lexicon)
    rust_segmenter = RustMorphologicalSegmenter(lexicon)
    word_types: set[str] = set()
    records = 0
    for role in ("train", "validation"):
        for record in read_id_text(dataset_root / f"data/{role}.csv", role=role):
            records += 1
            word_types.update(
                token.surface
                for token in pretokenize_normalized(record.text)
                if token.kind == "word"
            )
    ordered = sorted(word_types)
    python_outputs = python_segmenter.segment_many(ordered)
    rust_outputs = rust_segmenter.segment_many(ordered)
    discrepancies: list[dict[str, object]] = []
    for token, python_output, rust_output in zip(
        ordered, python_outputs, rust_outputs, strict=True
    ):
        if python_output != rust_output:
            discrepancies.append(
                {
                    "token": token,
                    "python": python_output.to_dict(),
                    "rust": rust_output.to_dict(),
                }
            )
            if len(discrepancies) >= 20:
                break
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "records_scanned": records,
        "word_types_compared": len(ordered),
        "exact_matches": len(ordered) if not discrepancies else len(ordered) - len(discrepancies),
        "discrepancy_count_capped": len(discrepancies),
        "discrepancies": discrepancies,
        "passed": not discrepancies,
        "held_out_test_used": False,
    }
    document = {**body, "report_fingerprint": fingerprint(body)}
    write_json(output_path, document)
    if discrepancies:
        raise AssertionError(
            f"Python-Rust segmentation parity failed for {len(discrepancies)} tokens"
        )
    return document


def verify_clean_runtime(
    artifact_dir: Path,
    runtime_root: Path,
    output_path: Path,
) -> dict[str, object]:
    runtime_package = runtime_root / "kapampangan_morphbpe_runtime"
    if not runtime_package.is_dir():
        raise ValueError("standalone runtime package missing")
    with tempfile.TemporaryDirectory(prefix="kapampangan-morphbpe-runtime-") as temporary:
        clean_root = Path(temporary)
        clean_runtime = clean_root / "runtime"
        clean_artifact = clean_root / "artifact"
        shutil.copytree(runtime_package, clean_runtime / runtime_package.name)
        shutil.copytree(artifact_dir, clean_artifact)
        script = """
import json
import sys
import unicodedata
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from kapampangan_morphbpe_runtime import Tokenizer
tokenizer = Tokenizer(Path(sys.argv[2]))
samples = ["", "Masánting! ñ", "kuman", "Dacal a salamat.  "]
rows = []
for sample in samples:
    encoding = tokenizer.encode(sample)
    decoded = tokenizer.decode(encoding.ids)
    expected = unicodedata.normalize("NFC", sample)
    if decoded != expected:
        raise SystemExit(f"round trip mismatch: {sample!r} -> {decoded!r}")
    rows.append(
        {
            "input": sample,
            "tokens": list(encoding.token_strings),
            "ids": list(encoding.ids),
        }
    )
unknown_input = "\U0010ffff"
unknown = tokenizer.encode(unknown_input)
if list(unknown.ids) != [1] or list(unknown.token_strings) != ["<unk>"]:
    raise SystemExit("unknown fallback did not use the fixed <unk> token ID")
print(
    json.dumps(
        {
            "samples": rows,
            "unknown_input_codepoint": "U+10FFFF",
            "unknown_ids": list(unknown.ids),
            "vocabulary_size": tokenizer.vocabulary_size,
        },
        ensure_ascii=True,
        sort_keys=True,
    )
)
"""
        environment = {
            **os.environ,
            "KAPAMPANGAN_MORPHBPE_DATASET": str(clean_root / "DENIED_DATASET"),
            "KAPAMPANGAN_MORPHBPE_LEXICON": str(clean_root / "DENIED_LEXICON"),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
        completed = subprocess.run(
            [sys.executable, "-I", "-c", script, str(clean_runtime), str(clean_artifact)],
            cwd=clean_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "clean runtime failed: " + (completed.stderr or completed.stdout).strip()
            )
        details = json.loads(completed.stdout)
        if not isinstance(details, dict):
            raise ValueError("clean runtime returned malformed details")
    body: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_fingerprint": DATASET_FINGERPRINT,
        "passed": True,
        "copied_items": ["standalone runtime package", "selected tokenizer artifact"],
        "training_resources_present": False,
        "dataset_path_denied": True,
        "lexicon_path_denied": True,
        "details": details,
    }
    document = {**body, "report_fingerprint": fingerprint(body)}
    write_json(output_path, document)
    return document
