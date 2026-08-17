from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Any, Literal, cast

PretokenKind = Literal["word", "whitespace", "punctuation", "symbol"]


@dataclass(frozen=True, slots=True)
class _Pretoken:
    surface: str
    start: int
    end: int
    kind: PretokenKind


@dataclass(frozen=True, slots=True)
class _Unit:
    surface: str
    start: int
    end: int
    vocabulary_kind: str


@dataclass(frozen=True, slots=True)
class EncodedToken:
    token: str
    identifier: int
    start: int
    end: int
    pretoken_kind: str
    vocabulary_kind: str

    def to_dict(self) -> dict[str, object]:
        return {
            "token": self.token,
            "id": self.identifier,
            "start": self.start,
            "end": self.end,
            "pretoken_kind": self.pretoken_kind,
            "vocabulary_kind": self.vocabulary_kind,
        }


@dataclass(frozen=True, slots=True)
class Encoding:
    normalized_text: str
    tokens: tuple[EncodedToken, ...]

    @property
    def ids(self) -> tuple[int, ...]:
        return tuple(token.identifier for token in self.tokens)

    @property
    def token_strings(self) -> tuple[str, ...]:
        return tuple(token.token for token in self.tokens)

    @property
    def offsets(self) -> tuple[tuple[int, int], ...]:
        return tuple((token.start, token.end) for token in self.tokens)

    @property
    def attention_mask(self) -> tuple[int, ...]:
        return tuple(1 for _ in self.tokens)

    def to_dict(self) -> dict[str, object]:
        return {
            "normalized_text": self.normalized_text,
            "tokens": [token.to_dict() for token in self.tokens],
            "ids": list(self.ids),
            "attention_mask": list(self.attention_mask),
            "offsets": [list(offset) for offset in self.offsets],
        }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _is_word_core(character: str) -> bool:
    return unicodedata.category(character)[0] in {"L", "M", "N"}


def _pretokenize(normalized: str) -> tuple[_Pretoken, ...]:
    tokens: list[_Pretoken] = []
    joiners = {"'", "\u2019", "-"}
    index = 0
    while index < len(normalized):
        character = normalized[index]
        if character.isspace():
            end = index + 1
            while end < len(normalized) and normalized[end].isspace():
                end += 1
            tokens.append(_Pretoken(normalized[index:end], index, end, "whitespace"))
            index = end
            continue
        if _is_word_core(character):
            end = index + 1
            while end < len(normalized):
                current = normalized[end]
                if _is_word_core(current):
                    end += 1
                    continue
                if (
                    current in joiners
                    and end + 1 < len(normalized)
                    and _is_word_core(normalized[end - 1])
                    and _is_word_core(normalized[end + 1])
                ):
                    end += 1
                    continue
                break
            tokens.append(_Pretoken(normalized[index:end], index, end, "word"))
            index = end
            continue
        kind: PretokenKind = (
            "punctuation" if unicodedata.category(character).startswith("P") else "symbol"
        )
        tokens.append(_Pretoken(character, index, index + 1, kind))
        index += 1
    if "".join(token.surface for token in tokens) != normalized:
        raise AssertionError("runtime pre-tokenization was not lossless")
    return tuple(tokens)


class Tokenizer:
    def __init__(self, artifact_dir: Path) -> None:
        self.artifact_dir = artifact_dir.resolve()
        self._validate_checksums()
        raw: Any = json.loads((self.artifact_dir / "tokenizer.json").read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("tokenizer.json must contain an object")
        document = cast(dict[str, Any], raw)
        if document.get("schema_version") != "1.0.0":
            raise ValueError("unsupported tokenizer schema version")
        if document.get("artifact_type") != "kapampangan_morphbpe":
            raise ValueError("unexpected tokenizer artifact type")
        normalization = document.get("normalization")
        if normalization != {"unicode_normalization": "NFC", "spelling_mappings": []}:
            raise ValueError("unsupported normalization configuration")

        vocabulary = document.get("vocabulary")
        merges = document.get("merges")
        specials = document.get("special_tokens")
        if not isinstance(vocabulary, list) or not isinstance(merges, list):
            raise ValueError("tokenizer vocabulary or merges malformed")
        if not isinstance(specials, list):
            raise ValueError("tokenizer special tokens malformed")

        self.id_to_token: list[str] = []
        self.vocabulary_kind: list[str] = []
        for expected_id, entry_raw in enumerate(vocabulary):
            if not isinstance(entry_raw, dict):
                raise ValueError("vocabulary entry must be an object")
            entry = cast(dict[str, Any], entry_raw)
            if entry.get("id") != expected_id:
                raise ValueError("vocabulary IDs must be contiguous and ordered")
            token = entry.get("token")
            kind = entry.get("kind")
            if not isinstance(token, str) or not token or not isinstance(kind, str):
                raise ValueError("invalid vocabulary entry")
            self.id_to_token.append(token)
            self.vocabulary_kind.append(kind)
        if len(self.id_to_token) != len(set(self.id_to_token)):
            raise ValueError("duplicate token surface in vocabulary")
        self.token_to_id = {token: index for index, token in enumerate(self.id_to_token)}

        self.special_by_role: dict[str, tuple[str, int]] = {}
        for entry_raw in specials:
            if not isinstance(entry_raw, dict):
                raise ValueError("special-token entry must be an object")
            entry = cast(dict[str, Any], entry_raw)
            role, token, identifier = entry.get("role"), entry.get("token"), entry.get("id")
            if (
                not isinstance(role, str)
                or not isinstance(token, str)
                or not isinstance(identifier, int)
            ):
                raise ValueError("invalid special-token entry")
            if self.token_to_id.get(token) != identifier:
                raise ValueError("special-token mapping conflicts with vocabulary")
            self.special_by_role[role] = (token, identifier)
        for required in ("pad", "unk", "bos", "eos"):
            if required not in self.special_by_role:
                raise ValueError(f"required special token missing: {required}")

        self.merge_ranks: dict[tuple[str, str], tuple[int, str]] = {}
        for expected_rank, entry_raw in enumerate(merges):
            if not isinstance(entry_raw, dict):
                raise ValueError("merge entry must be an object")
            entry = cast(dict[str, Any], entry_raw)
            left, right, result, rank = (
                entry.get("left"),
                entry.get("right"),
                entry.get("result"),
                entry.get("rank"),
            )
            if (
                not isinstance(left, str)
                or not isinstance(right, str)
                or not isinstance(result, str)
                or rank != expected_rank
                or result != left + right
                or result not in self.token_to_id
            ):
                raise ValueError("invalid merge rule")
            pair = (left, right)
            if pair in self.merge_ranks:
                raise ValueError("duplicate merge pair")
            self.merge_ranks[pair] = (expected_rank, result)

    def _validate_checksums(self) -> None:
        checksum_path = self.artifact_dir / "checksums.sha256"
        if not checksum_path.is_file():
            raise ValueError("artifact checksums.sha256 is missing")
        expected: dict[str, str] = {}
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            digest, separator, relative = line.partition("  ")
            if not separator or len(digest) != 64 or not relative:
                raise ValueError("malformed artifact checksum line")
            if Path(relative).is_absolute() or ".." in Path(relative).parts:
                raise ValueError("unsafe artifact checksum path")
            expected[relative] = digest
        actual_files = {
            path.relative_to(self.artifact_dir).as_posix(): path
            for path in self.artifact_dir.rglob("*")
            if path.is_file() and path.name != "checksums.sha256"
        }
        if set(expected) != set(actual_files):
            raise ValueError("artifact checksum inventory mismatch")
        for relative, path in actual_files.items():
            if _sha256_file(path) != expected[relative]:
                raise ValueError(f"artifact checksum mismatch: {relative}")

    def _encode_pretoken(self, pretoken: _Pretoken) -> list[EncodedToken]:
        full_id = self.token_to_id.get(pretoken.surface)
        if full_id is not None and self.vocabulary_kind[full_id] != "special":
            return [
                EncodedToken(
                    pretoken.surface,
                    full_id,
                    pretoken.start,
                    pretoken.end,
                    pretoken.kind,
                    self.vocabulary_kind[full_id],
                )
            ]

        unknown_token, unknown_id = self.special_by_role["unk"]
        units: list[_Unit] = []
        for relative, character in enumerate(pretoken.surface):
            identifier = self.token_to_id.get(character)
            if identifier is None:
                units.append(_Unit(unknown_token, relative, relative + 1, "special"))
            else:
                units.append(
                    _Unit(character, relative, relative + 1, self.vocabulary_kind[identifier])
                )

        while len(units) > 1:
            available: list[tuple[int, str, str]] = []
            for left, right in pairwise(units):
                ranked = self.merge_ranks.get((left.surface, right.surface))
                if ranked is not None:
                    available.append((ranked[0], left.surface, right.surface))
            if not available:
                break
            _rank, selected_left, selected_right = min(available)
            merged_units: list[_Unit] = []
            index = 0
            while index < len(units):
                if (
                    index + 1 < len(units)
                    and units[index].surface == selected_left
                    and units[index + 1].surface == selected_right
                ):
                    result = selected_left + selected_right
                    result_id = self.token_to_id.get(result)
                    if result_id is None:
                        raise ValueError("merge result is absent from vocabulary")
                    merged_units.append(
                        _Unit(
                            result,
                            units[index].start,
                            units[index + 1].end,
                            self.vocabulary_kind[result_id],
                        )
                    )
                    index += 2
                else:
                    merged_units.append(units[index])
                    index += 1
            units = merged_units

        encoded: list[EncodedToken] = []
        for unit in units:
            identifier = (
                unknown_id if unit.surface == unknown_token else self.token_to_id[unit.surface]
            )
            encoded.append(
                EncodedToken(
                    unit.surface,
                    identifier,
                    pretoken.start + unit.start,
                    pretoken.start + unit.end,
                    pretoken.kind,
                    unit.vocabulary_kind,
                )
            )
        return encoded

    def encode(self, text: str, *, add_special_tokens: bool = False) -> Encoding:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        normalized = unicodedata.normalize("NFC", text)
        encoded: list[EncodedToken] = []
        if add_special_tokens:
            token, identifier = self.special_by_role["bos"]
            encoded.append(EncodedToken(token, identifier, 0, 0, "special", "special"))
        for pretoken in _pretokenize(normalized):
            encoded.extend(self._encode_pretoken(pretoken))
        if add_special_tokens:
            token, identifier = self.special_by_role["eos"]
            encoded.append(
                EncodedToken(
                    token,
                    identifier,
                    len(normalized),
                    len(normalized),
                    "special",
                    "special",
                )
            )
        return Encoding(normalized, tuple(encoded))

    def decode(
        self,
        identifiers: list[int] | tuple[int, ...],
        *,
        skip_special_tokens: bool = True,
    ) -> str:
        output: list[str] = []
        unknown_token, unknown_id = self.special_by_role["unk"]
        special_ids = {identifier for _token, identifier in self.special_by_role.values()}
        for identifier in identifiers:
            if (
                not isinstance(identifier, int)
                or identifier < 0
                or identifier >= len(self.id_to_token)
            ):
                raise ValueError(f"token ID out of range: {identifier}")
            if identifier == unknown_id:
                output.append("�")
            elif skip_special_tokens and identifier in special_ids:
                continue
            else:
                token = self.id_to_token[identifier]
                output.append("�" if token == unknown_token else token)
        return "".join(output)

    @property
    def vocabulary_size(self) -> int:
        return len(self.id_to_token)
