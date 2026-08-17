from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from .runtime_bridge import RuntimeTokenizer, load_runtime_tokenizer
from .serialization import read_json


@dataclass(frozen=True, slots=True)
class SourceBatchEncoding:
    input_ids: tuple[tuple[int, ...], ...]
    attention_mask: tuple[tuple[int, ...], ...]
    token_strings: tuple[tuple[str, ...], ...]
    normalized_offsets: tuple[tuple[tuple[int, int], ...], ...]
    normalized_texts: tuple[str, ...]
    truncated: tuple[bool, ...]
    vocabulary_size: int
    special_tokens: dict[str, dict[str, str | int]]
    artifact_fingerprint: str

    def to_dict(self) -> dict[str, object]:
        return {
            "input_ids": [list(row) for row in self.input_ids],
            "attention_mask": [list(row) for row in self.attention_mask],
            "token_strings": [list(row) for row in self.token_strings],
            "normalized_offsets": [
                [list(offset) for offset in row] for row in self.normalized_offsets
            ],
            "normalized_texts": list(self.normalized_texts),
            "truncated": list(self.truncated),
            "vocabulary_size": self.vocabulary_size,
            "special_tokens": self.special_tokens,
            "artifact_fingerprint": self.artifact_fingerprint,
        }


class SourceTokenizerAdapter:
    """Framework-neutral future NLLB source-side batching contract."""

    def __init__(self, artifact_dir: Path) -> None:
        self.artifact_dir = artifact_dir.resolve()
        self.tokenizer: RuntimeTokenizer = load_runtime_tokenizer(self.artifact_dir)
        manifest_raw: Any = read_json(self.artifact_dir / "tokenizer-manifest.json")
        specials_raw: Any = read_json(self.artifact_dir / "special_tokens.json")
        if not isinstance(manifest_raw, dict) or not isinstance(specials_raw, dict):
            raise ValueError("tokenizer artifact contract files must be objects")
        manifest = cast(dict[str, Any], manifest_raw)
        specials = cast(dict[str, Any], specials_raw)
        fingerprint = manifest.get("artifact_fingerprint")
        entries = specials.get("special_tokens")
        if not isinstance(fingerprint, str) or not isinstance(entries, list):
            raise ValueError("tokenizer artifact contract is incomplete")
        self.artifact_fingerprint = fingerprint
        self.special_tokens: dict[str, dict[str, str | int]] = {}
        for entry_raw in entries:
            if not isinstance(entry_raw, dict):
                raise ValueError("special-token entry must be an object")
            entry = cast(dict[str, Any], entry_raw)
            role, token, identifier = entry.get("role"), entry.get("token"), entry.get("id")
            if (
                not isinstance(role, str)
                or not isinstance(token, str)
                or not isinstance(identifier, int)
            ):
                raise ValueError("special-token entry is malformed")
            self.special_tokens[role] = {"token": token, "id": identifier}
        if self.special_tokens.get("pad", {}).get("id") != 0:
            raise ValueError("adapter contract requires pad token ID 0")

    def encode_batch(
        self,
        texts: list[str] | tuple[str, ...],
        *,
        add_special_tokens: bool = True,
        padding: bool = True,
        max_length: int | None = None,
        truncation: bool = False,
    ) -> SourceBatchEncoding:
        if max_length is not None and max_length <= 0:
            raise ValueError("max_length must be positive")
        encodings = [
            self.tokenizer.encode(text, add_special_tokens=add_special_tokens) for text in texts
        ]
        natural_lengths = [len(encoding.ids) for encoding in encodings]
        if (
            max_length is not None
            and not truncation
            and any(length > max_length for length in natural_lengths)
        ):
            raise ValueError("input exceeds max_length while truncation is disabled")
        effective_lengths = [
            min(length, max_length) if max_length is not None else length
            for length in natural_lengths
        ]
        target_length = (
            max_length
            if padding and max_length is not None
            else max(effective_lengths, default=0)
            if padding
            else None
        )
        pad_id = cast(int, self.special_tokens["pad"]["id"])
        pad_token = cast(str, self.special_tokens["pad"]["token"])

        id_rows: list[tuple[int, ...]] = []
        mask_rows: list[tuple[int, ...]] = []
        token_rows: list[tuple[str, ...]] = []
        offset_rows: list[tuple[tuple[int, int], ...]] = []
        truncated_rows: list[bool] = []
        for encoding, natural_length, effective_length in zip(
            encodings, natural_lengths, effective_lengths, strict=True
        ):
            ids = list(encoding.ids[:effective_length])
            token_strings = [token.token for token in encoding.tokens[:effective_length]]
            offsets = [(token.start, token.end) for token in encoding.tokens[:effective_length]]
            mask = [1] * effective_length
            if target_length is not None:
                pad_count = target_length - effective_length
                ids.extend([pad_id] * pad_count)
                token_strings.extend([pad_token] * pad_count)
                offsets.extend([(0, 0)] * pad_count)
                mask.extend([0] * pad_count)
            id_rows.append(tuple(ids))
            mask_rows.append(tuple(mask))
            token_rows.append(tuple(token_strings))
            offset_rows.append(tuple(offsets))
            truncated_rows.append(effective_length < natural_length)
        return SourceBatchEncoding(
            input_ids=tuple(id_rows),
            attention_mask=tuple(mask_rows),
            token_strings=tuple(token_rows),
            normalized_offsets=tuple(offset_rows),
            normalized_texts=tuple(encoding.normalized_text for encoding in encodings),
            truncated=tuple(truncated_rows),
            vocabulary_size=self.tokenizer.vocabulary_size,
            special_tokens=self.special_tokens,
            artifact_fingerprint=self.artifact_fingerprint,
        )
