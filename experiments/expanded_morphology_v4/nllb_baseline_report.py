"""One-off tokenizer-level report: real NLLB-200-Distilled-600M tokenizer vs.
this experiment's Plain-BPE and weighted-penalty MorphBPE conditions, plus a
matched-vocabulary Unigram-LM ablation trained on this project's own corpus.

This is an encode-time-only comparison. NLLB-200's tokenizer (a pretrained
SentencePiece unigram-LM model) is loaded as-is and is never retrained on
this project's Kapampangan corpus, unlike every other condition here. See
`resources/nllb-tokenizer-manifest.json` (written by this script) for exact
NLLB provenance: repo, pinned revision, per-file SHA-256.

NLLB's vocabulary (256,204) is over 30x the local vocabulary (8,192) used by
Plain-BPE/MorphBPE, which confounds any fertility comparison against NLLB:
lower fertility could come from the Unigram-LM algorithm, or just from the
larger vocabulary/multilingual training. The `unigram_ablation` condition
(see `train_unigram_ablation.py`) isolates the algorithm: a fresh Unigram-LM
tokenizer trained on this project's own corpus at the *same* vocabulary size
as Plain-BPE/MorphBPE. It is NOT NLLB's tokenizer.

Run with the NLLB tokenizer files already fetched into
`resources/nllb-tokenizer/` (see README.md for the pinned
`huggingface_hub.snapshot_download` command used to fetch them -- tokenizer
files only, model weights excluded) and the Unigram ablation already trained
(`python train_unigram_ablation.py`).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = EXPERIMENT_ROOT.parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from tokenizers import Tokenizer  # noqa: E402

from kapampangan_morphbpe.normalization import normalize_text  # noqa: E402
from kapampangan_morphbpe.pretokenizer import pretokenize  # noqa: E402
from kapampangan_morphbpe.runtime_bridge import (  # noqa: E402
    RuntimeTokenizer,
    load_runtime_tokenizer,
)
from kapampangan_morphbpe.serialization import sha256_file, write_json  # noqa: E402

NLLB_REPO_ID = "facebook/nllb-200-distilled-600M"
NLLB_REVISION = "f8d333a098d19b4fd9a8b18f94170487ad3f821d"
NLLB_TOKENIZER_DIR = EXPERIMENT_ROOT / "resources/nllb-tokenizer"
NLLB_TOKENIZER_FILES = (
    "tokenizer.json",
    "tokenizer_config.json",
    "special_tokens_map.json",
    "sentencepiece.bpe.model",
)

VOCAB_SIZE = 8192
CROSSING_PENALTY = 4
PLAIN_ARTIFACT = EXPERIMENT_ROOT / f"artifacts/plain/candidates/vocab-{VOCAB_SIZE}"
MORPH_ARTIFACT = (
    EXPERIMENT_ROOT / f"artifacts/penalty-{CROSSING_PENALTY}/candidates/vocab-{VOCAB_SIZE}"
)
# NOT NLLB's tokenizer -- a fresh SentencePiece-style Unigram-LM model
# trained on this project's own corpus at the same vocabulary size as the
# Plain-BPE/MorphBPE conditions above, to isolate the Unigram-vs-BPE
# algorithm effect from NLLB's vocabulary-size/corpus-exposure confound.
# See train_unigram_ablation.py.
UNIGRAM_ABLATION_DIR = EXPERIMENT_ROOT / f"artifacts/unigram-ablation/vocab-{VOCAB_SIZE}"
UNIGRAM_ABLATION_TOKENIZER_PATH = UNIGRAM_ABLATION_DIR / "tokenizer.json"
UNIGRAM_ABLATION_MANIFEST_PATH = UNIGRAM_ABLATION_DIR / "unigram-ablation-manifest.json"

RESEGMENTATION_AUDIT_PATH = EXPERIMENT_ROOT / "runs/segmentations/resegmentation-audit.jsonl"
AUDIT_SAMPLE_SIZE = 20

FIXED_SENTENCES = ("misamban", "Sumulat ako ng tula", "Dumalan ka keni.")

REPORTS_DIR = EXPERIMENT_ROOT / "reports"
REPORT_JSON_PATH = REPORTS_DIR / "nllb-baseline-comparison.json"
REPORT_MARKDOWN_PATH = REPORTS_DIR / "nllb-baseline-comparison.md"
PROVENANCE_MANIFEST_PATH = EXPERIMENT_ROOT / "resources/nllb-tokenizer-manifest.json"

PLAIN_KEY = f"plain_bpe_vocab_{VOCAB_SIZE}"
MORPH_KEY = f"morphbpe_penalty_{CROSSING_PENALTY}_vocab_{VOCAB_SIZE}"
NLLB_KEY = "nllb_200_distilled_600m"
UNIGRAM_KEY = f"unigram_ablation_vocab_{VOCAB_SIZE}"


def _write_provenance_manifest() -> dict[str, Any]:
    files: dict[str, Any] = {}
    for name in NLLB_TOKENIZER_FILES:
        file_path = NLLB_TOKENIZER_DIR / name
        if not file_path.exists():
            raise FileNotFoundError(f"expected downloaded NLLB tokenizer file missing: {file_path}")
        files[name] = {"size_bytes": file_path.stat().st_size, "sha256": sha256_file(file_path)}
    manifest = {
        "repo_id": NLLB_REPO_ID,
        "revision": NLLB_REVISION,
        "source_url": f"https://huggingface.co/{NLLB_REPO_ID}/tree/{NLLB_REVISION}",
        "fetch_method": "huggingface_hub.snapshot_download",
        "fetch_scope": "tokenizer_files_only_model_weights_excluded",
        "excluded_file": "pytorch_model.bin (~2.4GB model weights; never downloaded)",
        "files": files,
    }
    write_json(PROVENANCE_MANIFEST_PATH, manifest)
    return manifest


def _load_nllb_tokenizer() -> Tokenizer:
    tokenizer = Tokenizer.from_file(str(NLLB_TOKENIZER_DIR / "tokenizer.json"))
    # The shipped post-processor appends a generic placeholder id for the
    # language-code special token (normally resolved per-language by
    # transformers' NllbTokenizerFast.src_lang wrapper, which is not used
    # here). Disabling it isolates content subword pieces, matching this
    # project's own lexicon-free BPE runtime output, which likewise reports
    # content pieces without added control tokens.
    tokenizer.post_processor = None
    return tokenizer


def _word_spans(normalized: str) -> list[tuple[int, int]]:
    _, pretokens = pretokenize(normalized)
    return [(p.start, p.end) for p in pretokens if p.kind == "word"]


def _overlaps_any(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    start, end = span
    return any(start < w_end and end > w_start for w_start, w_end in spans)


def _encode_nllb(tokenizer: Tokenizer, text: str) -> dict[str, Any]:
    normalized = normalize_text(text)
    encoding = tokenizer.encode(normalized)
    word_spans = _word_spans(normalized)
    pieces = list(encoding.tokens)
    offsets = list(encoding.offsets)
    word_token_count = sum(
        1 for (start, end) in offsets if end > start and _overlaps_any((start, end), word_spans)
    )
    word_pretoken_count = len(word_spans)
    return {
        "normalized_text": normalized,
        "pieces": pieces,
        "display_pieces": pieces,
        "ids": list(encoding.ids),
        "token_count": len(pieces),
        "word_token_count": word_token_count,
        "word_pretoken_count": word_pretoken_count,
        "fertility_rate": (word_token_count / word_pretoken_count if word_pretoken_count else 0.0),
    }


def _encode_local(tokenizer: RuntimeTokenizer, text: str) -> dict[str, Any]:
    encoding = tokenizer.encode(text)
    tokens = list(encoding.tokens)
    pieces = [token.token for token in tokens]
    # Display pieces drop whitespace-pretoken tokens (this project's BPE
    # tokenizes whitespace as its own piece; NLLB's Metaspace pre-tokenizer
    # folds the leading space into the following word piece instead, so it
    # never emits a separate whitespace piece). Dropping them here only
    # affects the human-readable table; `pieces`/`ids`/counts below remain
    # the full, untouched encoding.
    display_pieces = [token.token for token in tokens if token.pretoken_kind != "whitespace"]
    word_token_count = sum(1 for token in tokens if token.pretoken_kind == "word")
    _, pretokens = pretokenize(text)
    word_pretoken_count = sum(1 for pretoken in pretokens if pretoken.kind == "word")
    return {
        "normalized_text": encoding.normalized_text,
        "pieces": pieces,
        "display_pieces": display_pieces,
        "ids": list(encoding.ids),
        "token_count": len(pieces),
        "word_token_count": word_token_count,
        "word_pretoken_count": word_pretoken_count,
        "fertility_rate": (word_token_count / word_pretoken_count if word_pretoken_count else 0.0),
    }


def _encode_unigram_ablation(tokenizer: Tokenizer, text: str) -> dict[str, Any]:
    # This tokenizer's pre_tokenizer was disabled at training time (each
    # training stream surface was already an atomic pretoken), so it must be
    # driven the same way here: pretokenize first, then encode each segment
    # independently -- mirroring how this project's own Plain-BPE/MorphBPE
    # runtime never merges across a word/whitespace/punctuation boundary.
    normalized, pretokens = pretokenize(text)
    pieces: list[str] = []
    display_pieces: list[str] = []
    ids: list[int] = []
    word_token_count = 0
    for pretoken in pretokens:
        segment_encoding = tokenizer.encode(pretoken.surface)
        pieces.extend(segment_encoding.tokens)
        ids.extend(segment_encoding.ids)
        if pretoken.kind == "word":
            word_token_count += len(segment_encoding.tokens)
            display_pieces.extend(segment_encoding.tokens)
        elif pretoken.kind != "whitespace":
            display_pieces.extend(segment_encoding.tokens)
    word_pretoken_count = sum(1 for pretoken in pretokens if pretoken.kind == "word")
    return {
        "normalized_text": normalized,
        "pieces": pieces,
        "display_pieces": display_pieces,
        "ids": ids,
        "token_count": len(pieces),
        "word_token_count": word_token_count,
        "word_pretoken_count": word_pretoken_count,
        "fertility_rate": (word_token_count / word_pretoken_count if word_pretoken_count else 0.0),
    }


def _load_audit_sample() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with RESEGMENTATION_AUDIT_PATH.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle):
            if line_number >= AUDIT_SAMPLE_SIZE:
                break
            rows.append(json.loads(line))
    return rows


def _test_items() -> list[dict[str, str]]:
    items = [{"text": sentence, "source": "fixed_test_sentence"} for sentence in FIXED_SENTENCES]
    for row in _load_audit_sample():
        items.append({"text": row["surface"], "source": "resegmentation_audit_sample"})
    return items


def _average_fertility(rows: list[dict[str, Any]], key: str) -> float:
    values = [row[key]["fertility_rate"] for row in rows if row[key]["word_pretoken_count"]]
    return sum(values) / len(values) if values else 0.0


def _write_markdown(report: dict[str, Any]) -> None:
    lines = [
        "# NLLB-200-Distilled-600M vs. local tokenizers (encode-time only)",
        "",
        f"- NLLB source: `{report['nllb_tokenizer_source']['repo_id']}` "
        f"@ `{report['nllb_tokenizer_source']['revision']}` "
        "(tokenizer files only, model weights excluded)",
        f"- Local vocabulary size: {report['local_vocabulary_size']}",
        f"- Local MorphBPE condition: penalty-{report['local_morphbpe_crossing_penalty']} "
        "(not selected; representative mid-grid penalty)",
        f"- Unigram ablation: fresh Unigram-LM tokenizer trained on this project's "
        f"own corpus at matched vocabulary size ({report['local_vocabulary_size']}) -- "
        "**not NLLB's tokenizer**; isolates the algorithm effect from NLLB's "
        "vocab-size/corpus-exposure confound (see train_unigram_ablation.py)",
        f"- NLLB retrained on this corpus: {report['nllb_retrained_on_corpus']}",
        "",
        report["note"],
        "",
        "**Caveat:** NLLB-200's vocabulary (256,204 entries) is over 30x this "
        "project's local vocabulary (8,192). Vocabulary size alone strongly "
        "drives Fertility Rate -- a larger vocabulary needs fewer pieces per "
        "word regardless of morphological alignment -- so NLLB's lower "
        "fertility below must not be read as evidence of better "
        "morphological segmentation; the Unigram-ablation column (matched "
        "vocab, same corpus, same Unigram-LM algorithm family as NLLB) is "
        "what isolates that effect instead.",
        "",
        "| input | source | NLLB pieces | NLLB fert. | Unigram-ablation pieces "
        "| Unigram fert. | Plain BPE pieces | Plain fert. | MorphBPE pieces | MorphBPE fert. |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in report["rows"]:
        nllb = row[NLLB_KEY]
        unigram = row[UNIGRAM_KEY]
        plain = row[PLAIN_KEY]
        morph = row[MORPH_KEY]
        lines.append(
            "| {text} | {source} | {nllb_pieces} | {nllb_fert:.2f} | {unigram_pieces} | "
            "{unigram_fert:.2f} | {plain_pieces} | {plain_fert:.2f} | {morph_pieces} "
            "| {morph_fert:.2f} |".format(
                text=row["input_text"],
                source=row["source"],
                nllb_pieces=" + ".join(nllb["display_pieces"]),
                nllb_fert=nllb["fertility_rate"],
                unigram_pieces=" + ".join(unigram["display_pieces"]),
                unigram_fert=unigram["fertility_rate"],
                plain_pieces=" + ".join(plain["display_pieces"]),
                plain_fert=plain["fertility_rate"],
                morph_pieces=" + ".join(morph["display_pieces"]),
                morph_fert=morph["fertility_rate"],
            )
        )
    summary = report["summary"]
    lines += [
        "",
        "## Summary",
        "",
        f"- Items compared: {summary['item_count']}",
        f"- Average fertility (NLLB, native pretrained, 256,204 vocab): "
        f"{summary['average_fertility'][NLLB_KEY]:.4f}",
        f"- Average fertility (Unigram ablation, matched {VOCAB_SIZE} vocab, "
        f"this corpus): {summary['average_fertility'][UNIGRAM_KEY]:.4f}",
        f"- Average fertility (Plain BPE, matched {VOCAB_SIZE} vocab, this corpus): "
        f"{summary['average_fertility'][PLAIN_KEY]:.4f}",
        f"- Average fertility (MorphBPE penalty-{CROSSING_PENALTY}, matched "
        f"{VOCAB_SIZE} vocab, this corpus): {summary['average_fertility'][MORPH_KEY]:.4f}",
        f"- Items where NLLB pieces are byte-identical to Plain BPE: "
        f"{summary['nllb_pieces_equal_plain_count']}/{summary['item_count']}",
        f"- Items where NLLB pieces are byte-identical to MorphBPE: "
        f"{summary['nllb_pieces_equal_morphbpe_count']}/{summary['item_count']}",
        f"- Items where NLLB pieces are byte-identical to the Unigram ablation: "
        f"{summary['nllb_pieces_equal_unigram_ablation_count']}/{summary['item_count']}",
        "",
        "**Isolating the algorithm effect:** the Unigram-ablation row holds "
        "vocabulary size, training corpus, character inventory, and special "
        "tokens fixed against Plain BPE, changing only the subword algorithm "
        "(Unigram-LM, NLLB's family, vs. BPE). If Unigram-ablation's fertility "
        "sits close to Plain BPE/MorphBPE (both far above NLLB's), that points "
        "to vocabulary size/corpus exposure -- not the Unigram algorithm -- as "
        "the main driver of NLLB's lower fertility above.",
        "",
        "Fertility Rate = word-subword token count / Unicode word-pretoken count "
        "(this project's own formula), computed identically for all four "
        "tokenizers. NLLB word attribution is approximated by character-offset "
        "overlap against this project's own word-pretoken spans, since NLLB has "
        "no native pretoken concept. This is a silver/approximate measurement, "
        "not an independent evaluation. The Unigram-ablation tokenizer's "
        "training is not verified byte-reproducible across runs (third-party "
        "EM trainer); see its artifact manifest.",
    ]
    REPORT_MARKDOWN_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MARKDOWN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    if not NLLB_TOKENIZER_DIR.exists():
        raise SystemExit(
            f"NLLB tokenizer files not found at {NLLB_TOKENIZER_DIR}; fetch them first "
            "(see README.md for the pinned huggingface_hub.snapshot_download command)."
        )
    if not UNIGRAM_ABLATION_TOKENIZER_PATH.exists():
        raise SystemExit(
            f"Unigram ablation tokenizer not found at {UNIGRAM_ABLATION_TOKENIZER_PATH}; "
            "run train_unigram_ablation.py first."
        )
    provenance = _write_provenance_manifest()
    unigram_manifest: Any = json.loads(
        UNIGRAM_ABLATION_MANIFEST_PATH.read_text(encoding="utf-8-sig")
    )
    nllb_tokenizer = _load_nllb_tokenizer()
    unigram_tokenizer = Tokenizer.from_file(str(UNIGRAM_ABLATION_TOKENIZER_PATH))
    plain_tokenizer = load_runtime_tokenizer(PLAIN_ARTIFACT)
    morph_tokenizer = load_runtime_tokenizer(MORPH_ARTIFACT)
    if plain_tokenizer.vocabulary_size != VOCAB_SIZE or morph_tokenizer.vocabulary_size != (
        VOCAB_SIZE
    ):
        raise AssertionError("local artifact vocabulary size does not match VOCAB_SIZE constant")
    if unigram_tokenizer.get_vocab_size() != VOCAB_SIZE:
        raise AssertionError("unigram ablation vocabulary size does not match VOCAB_SIZE constant")

    rows: list[dict[str, Any]] = []
    for item in _test_items():
        text = item["text"]
        nllb = _encode_nllb(nllb_tokenizer, text)
        unigram = _encode_unigram_ablation(unigram_tokenizer, text)
        plain = _encode_local(plain_tokenizer, text)
        morph = _encode_local(morph_tokenizer, text)
        rows.append(
            {
                "input_text": text,
                "source": item["source"],
                NLLB_KEY: nllb,
                UNIGRAM_KEY: unigram,
                PLAIN_KEY: plain,
                MORPH_KEY: morph,
                "nllb_pieces_equal_plain": nllb["pieces"] == plain["pieces"],
                "nllb_pieces_equal_morphbpe": nllb["pieces"] == morph["pieces"],
                "nllb_pieces_equal_unigram_ablation": nllb["pieces"] == unigram["pieces"],
            }
        )

    summary = {
        "item_count": len(rows),
        "average_fertility": {
            NLLB_KEY: _average_fertility(rows, NLLB_KEY),
            UNIGRAM_KEY: _average_fertility(rows, UNIGRAM_KEY),
            PLAIN_KEY: _average_fertility(rows, PLAIN_KEY),
            MORPH_KEY: _average_fertility(rows, MORPH_KEY),
        },
        "nllb_pieces_equal_plain_count": sum(row["nllb_pieces_equal_plain"] for row in rows),
        "nllb_pieces_equal_morphbpe_count": sum(row["nllb_pieces_equal_morphbpe"] for row in rows),
        "nllb_pieces_equal_unigram_ablation_count": sum(
            row["nllb_pieces_equal_unigram_ablation"] for row in rows
        ),
    }

    report = {
        "comparison_mode": "nllb200_pretrained_tokenizer_vs_local_encode_time_only",
        "nllb_retrained_on_corpus": False,
        "nllb_tokenizer_source": provenance,
        "local_vocabulary_size": VOCAB_SIZE,
        "local_morphbpe_crossing_penalty": CROSSING_PENALTY,
        "local_morphbpe_penalty_selected": False,
        "unigram_ablation": {
            "purpose": (
                "Isolates the Unigram-LM-vs-BPE algorithm effect from the "
                "vocabulary-size/corpus-exposure confound between NLLB and this "
                "project's Plain-BPE/MorphBPE. NOT NLLB's tokenizer: a fresh "
                "Unigram-LM model trained on this project's own corpus at the "
                "same vocabulary size as Plain-BPE/MorphBPE."
            ),
            "manifest": unigram_manifest,
        },
        "note": (
            "Encode-time comparison only; NLLB-200's tokenizer is not retrained "
            "on this corpus (this repo has no PAM-Filipino parallel data at the "
            "scale needed to retrain or fine-tune it -- see AGENT_CONTEXT.md). "
            "Fertility Rate is this project's own T/W formula, computed "
            "identically for all four tokenizers. NLLB-200's vocabulary "
            "(256,204 entries) is over 30x the local vocabulary (8,192); "
            "vocabulary size alone strongly drives fertility, so NLLB's lower "
            "fertility must not be read as evidence of better morphological "
            "alignment. The 'unigram_ablation' condition (matched vocab, same "
            "corpus, same Unigram-LM algorithm family as NLLB, but NOT NLLB's "
            "actual tokenizer) exists specifically to isolate that confound: "
            "see its 'purpose' field above and reports/nllb-baseline-comparison.md "
            "for the interpretation. "
            "'*_pieces_equal_*' counts are near-guaranteed to be 0 for NLLB "
            "because NLLB draws from an entirely different, much larger "
            "vocabulary with a different whitespace convention (Metaspace '▁' "
            "prefix vs. this project's literal space pieces); treat them as a "
            "sanity check that the vocabularies are incompatible at the "
            "string level, not as a segmentation-agreement metric. Do not "
            "read any of this as comparable to a downstream BLEU/chrF++ "
            "translation evaluation, which remains a separate, unresolved "
            "blocker."
        ),
        "rows": rows,
        "summary": summary,
    }
    write_json(REPORT_JSON_PATH, report)
    _write_markdown(report)
    print(f"Wrote {REPORT_JSON_PATH}")
    print(f"Wrote {REPORT_MARKDOWN_PATH}")
    print(f"Wrote {PROVENANCE_MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
