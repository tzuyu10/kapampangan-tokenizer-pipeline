"""Three-way comparison using the selected tokenizer and matched-size controls.

Everything computed here reuses:
  - each selected catalog tokenizer's actual encode() implementation
  - the scoring functions in reference_data.py (also verbatim from demo.py)
  - reference_data.rows_for(), for turning "|"-marked gold morphemes into
    the same boundary/piece representation demo.py itself uses

`_bpe_groups`, `groups_by_tokenizer`, and `split_word` are straight ports of
the same-named functions in the team's own demo.py.

The Comparison tab always compares whatever text you last tokenized on the
Tokenizer tab (there is no separate example showcase or static input box
here anymore) — `custom_compare()` is the single entry point, called for
every request.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from kapampangan_morphbpe_runtime import Tokenizer

import reference_data as ref
import scoring_explain
import tokenizer_variants
from unigram_lm import UnigramLM

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"

MORPH = Tokenizer(ARTIFACTS / "morphbpe-penalty32")
PLAIN = Tokenizer(ARTIFACTS / "plain-bpe")
UNI = UnigramLM(ARTIFACTS / "unigram-lm-6080" / "tokenizer.json")
NAMES = ("MorphBPE", "Plain BPE", "Unigram-LM")
DEFAULT_COMPARISON_TOKENIZER = "variant:pam_tl_infix_first48_6080"
COMPARISON_VOCAB_SIZES = {6080, 8192}

SKIP_KINDS = {"whitespace"}


def _bpe_groups(tok: Tokenizer, text: str) -> list[list[str]]:
    groups: list[list[str]] = [[]]
    for t in tok.encode(text).tokens:
        if t.pretoken_kind in SKIP_KINDS:
            if groups[-1]:
                groups.append([])
            continue
        groups[-1].append(t.token)
    return [g for g in groups if g]


def groups_by_tokenizer(
    text: str, tokenizer_id: str | None = None, *, models: dict[str, Any] | None = None,
) -> dict[str, list[tuple[str, ...]]]:
    """Per-word piece tuples for each tokenizer, aligned word-for-word."""
    models = configuration(tokenizer_id)["models"] if models is None else models
    # Catalog adapters expose each saved tokenizer's actual encoder,
    # including Unigram's Viterbi path and its own pretoken boundaries.
    return {name: [tuple(g) for g in _bpe_groups(models[name], text)] for name in NAMES}


def split_word(
    word: str, tokenizer_id: str | None = None, *, models: dict[str, Any] | None = None,
) -> dict[str, list[str]]:
    models = configuration(tokenizer_id)["models"] if models is None else models
    return {name: [t.token for t in models[name].encode(word).tokens] for name in NAMES}


def _comparison_tokenizers(
    tokenizer_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Keep the selected encoder in its correct row, with same-size controls.

    A Plain or Unigram selection never becomes a row labeled MorphBPE.
    Those selections compare against the new infix-first48 of the same size.
    An explicit existing MorphBPE selection remains the MorphBPE row.
    """
    selected_id = DEFAULT_COMPARISON_TOKENIZER if tokenizer_id is None else tokenizer_id
    selected, _pretokenize, selected_info = tokenizer_variants.load(selected_id)
    size = selected_info["source_vocab_size"]
    if type(size) is not int or size not in COMPARISON_VOCAB_SIZES:
        raise ValueError("Matched tokenizer comparisons support vocabularies of 6,080 or 8,192.")
    variant = selected_info["tokenizer_variant"].lower()
    if "unigram" in variant or selected_id.startswith("unigram-lm-"):
        selected_row = "Unigram-LM"
    elif variant in {"plain", "plain_bpe"} or selected_id.startswith("variant:pam_tl_plain_"):
        selected_row = "Plain BPE"
    else:
        selected_row = "MorphBPE"

    row_ids = {
        "MorphBPE": f"variant:pam_tl_infix_first48_{size}",
        "Plain BPE": f"variant:pam_tl_plain_{size}",
        "Unigram-LM": f"unigram-lm-{size}",
    }
    tokenizers, identities = {}, {}
    for name, identifier in row_ids.items():
        if name == selected_row:
            tok, info = selected, selected_info
        else:
            tok, _pretokenize, info = tokenizer_variants.load(identifier)
        if info["source_vocab_size"] != size:
            raise ValueError("Comparison controls must have the same vocabulary size.")
        tokenizers[name], identities[name] = tok, info
    return tokenizers, {
        "selected": selected_info,
        "source_vocab_size": size,
        "tokenizers": identities,
    }


def configuration(tokenizer_id: str | None = None) -> dict[str, Any]:
    """Resolve immutable encoders and identities once for a diagnostic batch."""
    models, metadata = _comparison_tokenizers(tokenizer_id)
    return {"models": models, "metadata": metadata}


def custom_compare(raw_text: str, tokenizer_id: str | None = None) -> dict[str, Any] | None:
    """3-way comparison for whatever text was just tokenized on the
    Tokenizer tab: same '|' gold-boundary convention as trace_service.analyze
    (mark gold morpheme boundaries with e.g. `s|in|ulat`), scored against all
    three tokenizers side by side instead of just MorphBPE.
    """
    if not isinstance(raw_text, str):
        raise ValueError("`text` must be a string")
    tokenizers, comparison = _comparison_tokenizers(tokenizer_id)
    if not raw_text or not raw_text.strip():
        return None
    raw_tokens = raw_text.split()
    sentence = [(t.replace("|", ""), t if "|" in t else "") for t in raw_tokens]
    text = " ".join(surface for surface, _ in sentence)
    has_gold = any(spec for _surface, spec in sentence)

    enc = groups_by_tokenizer(text, models=tokenizers)
    result: dict[str, Any] = {
        "input": raw_text,
        "clean_text": text,
        "splits": {n: [list(g) for g in enc[n]] for n in NAMES},
        "fertility": {
            n: {
                "tokens": sum(len(g) for g in enc[n]),
                "words": len(sentence),
                "score": (sum(len(g) for g in enc[n]) / len(sentence)) if sentence else 0.0,
            }
            for n in NAMES
        },
        "gold": None,
        "gold_unavailable_reason": None,
        "comparison": comparison,
    }
    aligned = all(
        len(enc[n]) == len(sentence)
        and all("".join(pieces) == surface for pieces, (surface, _spec) in zip(enc[n], sentence))
        for n in NAMES
    )
    has_unknown = has_gold and any(
        token.identifier == model.special_by_role["unk"][1]
        for model in tokenizers.values()
        for token in model.encode(text).tokens
    )
    if has_gold and aligned and not has_unknown:
        rows = ref.rows_for(sentence)
        shared_pairs = int(ref.mcf1(rows, enc["MorphBPE"])["mcf1_gold_pairs"])
        metrics = {n: ref.score(rows, enc[n]) for n in NAMES}
        explain = {
            n: {
                "boundary": scoring_explain.explain_boundary(rows, enc[n]),
                "consistency": scoring_explain.explain_consistency(rows, enc[n]),
            }
            for n in NAMES
        }
        result["gold"] = {
            "gold_pieces": [list(r["gold_pieces"]) for r in rows],
            "shared_pairs": shared_pairs,
            "metrics": metrics,
            "explain": explain,
        }
    elif has_gold:
        result["gold_unavailable_reason"] = (
            "Gold boundaries cannot be scored because a tokenizer output contains unknown token IDs."
            if has_unknown else
            "Gold boundaries cannot be scored because a tokenizer output "
            "does not align losslessly with the annotated words."
        )
    return result


def verify_scoring_fidelity() -> tuple[int, int]:
    """Cross-check scoring_explain's precision/recall/F1 against
    reference_data.score()/mcf1() on the project's own gold data (pooled
    SENTENCES for boundary+consistency, FAMILIES forms for consistency),
    for all three tokenizers. Raises AssertionError on any mismatch.
    """
    checks = 0
    models = configuration()["models"]

    pooled_rows: list[dict[str, Any]] = []
    pooled_enc: dict[str, list[tuple[str, ...]]] = {n: [] for n in NAMES}
    for sentence in ref.SENTENCES:
        text = " ".join(w for w, _ in sentence)
        rows = ref.rows_for(sentence)
        enc = groups_by_tokenizer(text, models=models)
        pooled_rows += rows
        for n in NAMES:
            pooled_enc[n] += enc[n]

    for n in NAMES:
        real = ref.score(pooled_rows, pooled_enc[n])
        mine_b = scoring_explain.explain_boundary(pooled_rows, pooled_enc[n])
        mine_c = scoring_explain.explain_consistency(pooled_rows, pooled_enc[n])
        assert math.isclose(real["boundary_precision"], mine_b["precision"], abs_tol=1e-9), n
        assert math.isclose(real["boundary_recall"], mine_b["recall"], abs_tol=1e-9), n
        assert math.isclose(real["boundary_f1"], mine_b["f1"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_precision"], mine_c["precision"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_recall"], mine_c["recall"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1"], mine_c["f1"], abs_tol=1e-9), n
        assert int(real["mcf1_gold_pairs"]) == mine_c["shared_morpheme_pairs"], n
        checks += 1

    family_rows: list[dict[str, Any]] = []
    family_enc: dict[str, list[tuple[str, ...]]] = {n: [] for n in NAMES}
    for _root, _gloss, forms in ref.FAMILIES:
        for surface, seg in forms:
            family_rows.append(
                {"surface": surface, "gold_boundaries": set(), "gold_pieces": tuple(seg.split("|"))}
            )
        splits = {n: [tuple(split_word(s, models=models)[n]) for s, _ in forms] for n in NAMES}
        for n in NAMES:
            family_enc[n] += splits[n]

    for n in NAMES:
        real = ref.mcf1(family_rows, family_enc[n])
        mine_c = scoring_explain.explain_consistency(family_rows, family_enc[n])
        assert math.isclose(real["mcf1_precision"], mine_c["precision"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1_recall"], mine_c["recall"], abs_tol=1e-9), n
        assert math.isclose(real["mcf1"], mine_c["f1"], abs_tol=1e-9), n
        checks += 1

    return checks, checks
