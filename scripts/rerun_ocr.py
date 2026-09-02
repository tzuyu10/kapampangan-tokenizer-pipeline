"""Second-pass OCR verification, using tools the original runs/source-ocr/
pass explicitly lacked (a real PDF rasterizer -- pymupdf -- and Tesseract
5.4.0, both newly available this session).

For each page of a given source PDF: render at 300dpi via pymupdf, run
Tesseract OCR (eng), and compare the fresh text's length against the
existing extracted text (runs/source-ocr/text/<source_id>/page-NNNN.txt)
already in the repo from the original pass. This is a comparison/QA pass,
not a replacement -- the original runs/source-ocr/ directory is never
modified. Output goes to this new, separate, gitignored runs/source-ocr-v2/
directory.

Flags two kinds of pages for review, not just a blanket "OCR everything and
trust the new output":
  - fresh_much_longer: the new OCR found substantially more text than the
    original extraction recorded -- a candidate for genuinely recovered
    content (e.g. the paggamit-apat-pagsabi page-5 mirrored-scan case found
    earlier this session).
  - fresh_much_shorter: the new OCR found substantially less -- a candidate
    where the *original* extraction (often the embedded text layer, which
    the evidence report already found generally reliable for some sources)
    should be trusted over this pass, not blindly overwritten.

Page images are only kept on disk for flagged pages (to save space across
a 1000+-page book); OCR text output is kept for every page.
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

import fitz
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

REPO_ROOT = Path(__file__).resolve().parent.parent
ORIGINAL_TEXT_DIR = REPO_ROOT / "runs" / "source-ocr" / "text"
OUTPUT_ROOT = REPO_ROOT / "runs" / "source-ocr-v2"

# Threshold: flag a page if the fresh/original character-count ratio is
# outside [1/FLAG_RATIO, FLAG_RATIO].
FLAG_RATIO = 1.8
# Minimum absolute character difference to bother flagging (avoids noise on
# already-tiny pages, e.g. 2 chars vs 5 chars).
MIN_ABS_DIFF = 40


def rerun_source(source_id: str, pdf_path: str, dpi: int = 300) -> None:
    doc = fitz.open(pdf_path)
    n_pages = doc.page_count
    print(f"[{source_id}] {n_pages} pages, dpi={dpi}", flush=True)

    text_out_dir = OUTPUT_ROOT / "text" / source_id
    image_out_dir = OUTPUT_ROOT / "flagged-images" / source_id
    text_out_dir.mkdir(parents=True, exist_ok=True)
    image_out_dir.mkdir(parents=True, exist_ok=True)

    original_text_dir = ORIGINAL_TEXT_DIR / source_id

    rows = []
    t0 = time.time()
    for i in range(n_pages):
        pg = i + 1
        page = doc[i]
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")

        # Write to a temp path for tesseract (pytesseract accepts bytes via
        # PIL too, but keep this simple and dependency-light).
        tmp_img = text_out_dir / f"_tmp_page-{pg:04d}.png"
        tmp_img.write_bytes(img_bytes)
        try:
            fresh_text = pytesseract.image_to_string(str(tmp_img), lang="eng")
        except Exception as exc:  # noqa: BLE001 - record and continue
            fresh_text = ""
            print(f"  page {pg}: OCR ERROR: {exc}", flush=True)

        fresh_text_path = text_out_dir / f"page-{pg:04d}.txt"
        fresh_text_path.write_text(fresh_text, encoding="utf-8", newline="\n")

        orig_path = original_text_dir / f"page-{pg:04d}.txt"
        orig_text = orig_path.read_text(encoding="utf-8", errors="replace") if orig_path.exists() else ""

        fresh_len = len(fresh_text.strip())
        orig_len = len(orig_text.strip())

        flag = ""
        keep_image = False
        if abs(fresh_len - orig_len) >= MIN_ABS_DIFF:
            if orig_len == 0 and fresh_len > 0:
                flag = "fresh_found_content_where_original_had_none"
                keep_image = True
            elif fresh_len == 0 and orig_len > 0:
                flag = "fresh_found_nothing_where_original_had_content"
            elif orig_len > 0 and fresh_len / orig_len >= FLAG_RATIO:
                flag = "fresh_much_longer"
                keep_image = True
            elif orig_len > 0 and fresh_len / orig_len <= 1 / FLAG_RATIO:
                flag = "fresh_much_shorter"

        if keep_image:
            (image_out_dir / f"page-{pg:04d}.png").write_bytes(img_bytes)

        tmp_img.unlink(missing_ok=True)

        rows.append(
            {
                "pdf_page": pg,
                "original_chars": orig_len,
                "fresh_chars": fresh_len,
                "flag": flag,
            }
        )

        if pg % 100 == 0:
            elapsed = time.time() - t0
            rate = elapsed / pg
            remaining = rate * (n_pages - pg)
            print(f"  ...page {pg}/{n_pages}, {elapsed:.0f}s elapsed, ~{remaining/60:.1f} min remaining", flush=True)

    report_csv = OUTPUT_ROOT / "reports" / f"{source_id}-comparison.csv"
    report_csv.parent.mkdir(parents=True, exist_ok=True)
    with report_csv.open("w", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=["pdf_page", "original_chars", "fresh_chars", "flag"])
        writer.writeheader()
        writer.writerows(rows)

    flagged = [r for r in rows if r["flag"]]
    print(f"[{source_id}] done in {(time.time()-t0)/60:.1f} min. {len(flagged)} flagged pages of {n_pages}.", flush=True)
    for r in flagged:
        print(f"  page {r['pdf_page']}: {r['flag']} (orig={r['original_chars']}, fresh={r['fresh_chars']})", flush=True)


if __name__ == "__main__":
    source_id = sys.argv[1]
    pdf_path = sys.argv[2]
    rerun_source(source_id, pdf_path)
