"""First-pass text extraction for PDFs in pdf-dls/ that the original
runs/source-ocr/ pass never touched (Step 3 of the 2026-08-26 OCR work,
see AGENT_CONTEXT.md).

Mirrors the original pipeline's own approach (prefer the embedded text
layer; only render+OCR pages where it's too sparse) rather than blindly
OCR-ing every page -- using the same 20-non-whitespace-character threshold
`runs/source-ocr/source-manifest.json`'s `selection_rule` documents, and
the tools gained this session (pymupdf for real rendering, Tesseract 5.4.0
for OCR) in place of the original's Windows.Media.Ocr.

Output goes under runs/source-ocr-v2/ (gitignored, matching runs/source-ocr/'s
existing redistribution-rights posture) -- text per page plus a per-source
manifest entry and a combined report. Never touches runs/source-ocr/ or
pdf-dls/ themselves.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

import fitz
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = REPO_ROOT / "runs" / "source-ocr-v2"
EMBEDDED_TEXT_MIN_CHARS = 20  # matches the original pass's own threshold


def slugify(filename: str) -> str:
    name = filename
    if name.lower().endswith(".pdf"):
        name = name[:-4]
    name = re.sub(r"^ilide\.info-", "", name)
    # Keep a short fragment of the source hash as a disambiguator instead of
    # discarding it -- two distinct files with the same descriptive name
    # (e.g. two different "wikang-kapampangan" PDFs) previously collapsed
    # onto one slug and silently overwrote each other's output. Genuine
    # duplicate downloads (identical hash, one with a " (1)" suffix) still
    # collapse onto the same slug, which is correct since their content is
    # identical.
    hash_match = re.search(r"-pr_([0-9a-f]{32})(?:\s*\(\d+\))?$", name)
    hash_suffix = hash_match.group(1)[:8] if hash_match else None
    name = re.sub(r"-pr_[0-9a-f]{32}(\s*\(\d+\))?$", "", name)
    name = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    name = name or "unnamed"
    if hash_suffix:
        name = f"{name}-{hash_suffix}"
    return name


def extract_one(pdf_path: Path, source_id: str) -> dict:
    doc = fitz.open(str(pdf_path))
    n_pages = doc.page_count
    text_dir = OUTPUT_ROOT / "text" / source_id
    text_dir.mkdir(parents=True, exist_ok=True)

    pages_meta = []
    n_embedded = 0
    n_ocr = 0
    t0 = time.time()
    for i in range(n_pages):
        pg = i + 1
        page = doc[i]
        embedded = page.get_text()
        embedded_chars = len(embedded.strip())
        if embedded_chars >= EMBEDDED_TEXT_MIN_CHARS:
            final_text = embedded
            method = "embedded_text"
            n_embedded += 1
        else:
            pix = page.get_pixmap(dpi=300)
            tmp_img = text_dir / f"_tmp_page-{pg:04d}.png"
            tmp_img.write_bytes(pix.tobytes("png"))
            try:
                final_text = pytesseract.image_to_string(str(tmp_img), lang="eng")
            except Exception as exc:  # noqa: BLE001
                final_text = ""
                print(f"  [{source_id}] page {pg}: OCR ERROR: {exc}", flush=True)
            tmp_img.unlink(missing_ok=True)
            method = "tesseract_ocr"
            n_ocr += 1

        (text_dir / f"page-{pg:04d}.txt").write_text(final_text, encoding="utf-8", newline="\n")
        pages_meta.append(
            {
                "pdf_page": pg,
                "embedded_chars": embedded_chars,
                "selected_method": method,
                "final_chars": len(final_text.strip()),
            }
        )

    elapsed = time.time() - t0
    return {
        "source_id": source_id,
        "path": str(pdf_path),
        "bytes": pdf_path.stat().st_size,
        "pdf_pages": n_pages,
        "pages_using_embedded_text": n_embedded,
        "pages_using_ocr": n_ocr,
        "elapsed_seconds": round(elapsed, 1),
        "pages": pages_meta,
    }


def main() -> None:
    pdf_dir = Path(r"D:\Coding\thesis\pdf-dls")
    already_processed_names = {
        "A Case Grammar of Pampangan (Charles Monroe Richards) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "Bayung OrtograpiyaNG Kapampangan (Dr. Lucena P. Samson etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "Paggamit sa Apat a Pagsabi (coll.) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "SL-030-forman-kapampangan-grammar-notes.pdf",
        "Vocabulario De Pampango Fray DIEGO BERGA\u00d1O Translated by Venacio O. Samson (DIEGO BERGA\u00d1O) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "ilide.info-233458581-tagalog-ilocano-panggalatok-bicol-kapampangan-pr_90267df93eba53ba24b5b291ea07864d.pdf",
        "ilide.info-an-introduction-to-the-kapampangan-langu-pdf-pr_0f5aabe15f5d068f64c9a0185ad5b4cb.pdf",
        "ilide.info-b-pr_5ed9e563d92c49978a92f59bbc2ea2aa.pdf",
        "ilide.info-ka-pampanga-n-pr_0959b412ef3925dcd2be53c6e72cb13c.pdf",
        "ilide.info-kapampangan-grammar-notes-z-library-pr_21307bc8da0041a9d4245e8e415b2ecc.pdf",
        "ilide.info-kapampangandictionaryamongsamson-1-pr_8a0f2e64d024628a4ab7b876563dc425.pdf",
        "ilide.info-mga-salita-sa-iba-t-ibang-dayalekto-pr_bd7c44e778c5e655fc03d74663f66b5d.pdf",
        "ilide.info-paghahambing-ng-wikang-kapampangan-pr_69a3c87aa6fb68cc16d0b0c89adba32f.pdf",
    }

    targets = sorted(
        p for p in pdf_dir.iterdir() if p.suffix.lower() == ".pdf" and p.name not in already_processed_names
    )

    manifest = {"sources": []}
    grand_t0 = time.time()
    for idx, pdf_path in enumerate(targets, start=1):
        source_id = slugify(pdf_path.name)
        print(f"[{idx}/{len(targets)}] {source_id} <- {pdf_path.name}", flush=True)
        entry = extract_one(pdf_path, source_id)
        manifest["sources"].append(entry)
        print(
            f"  {entry['pdf_pages']} pages, {entry['pages_using_embedded_text']} embedded / "
            f"{entry['pages_using_ocr']} ocr, {entry['elapsed_seconds']}s",
            flush=True,
        )

    manifest_path = OUTPUT_ROOT / "new-pdfs-manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total_elapsed = time.time() - grand_t0
    print(f"\nDone: {len(targets)} files in {total_elapsed/60:.1f} min. Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
