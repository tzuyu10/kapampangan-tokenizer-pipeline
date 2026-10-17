"""Portable Viterbi encoder for the saved fresh Unigram control artifacts.

The Hugging Face exports contain no normalizer or pretokenizer. This adapter
applies the webapp's shared NFC and atomic-pretoken policy, then runs the saved
Unigram model independently on each pretoken. It does not approximate Unigram
with BPE merge rules and does not require the optional ``tokenizers`` package.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import unicodedata
from typing import Any

from kapampangan_morphbpe_runtime.tokenizer import (
    EncodedToken,
    Encoding,
    _pretokenize,
    _sha256_file,
)


class Tokenizer:
    algorithm = "unigram_lm"

    def __init__(self, artifact_dir: Path) -> None:
        self.artifact_dir = Path(artifact_dir).resolve()
        self._validate_checksums()
        document = json.loads((self.artifact_dir / "tokenizer.json").read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError("Unigram tokenizer.json must contain an object")
        if any(document.get(key) is not None for key in (
            "normalizer", "pre_tokenizer", "post_processor", "truncation", "padding",
        )):
            raise ValueError("unsupported Unigram preprocessing configuration")
        if document.get("decoder") != {"type": "Fuse"}:
            raise ValueError("unsupported Unigram decoder")
        model = document.get("model")
        if not isinstance(model, dict) or model.get("type") != "Unigram":
            raise ValueError("not a Unigram tokenizer.json")
        if model.get("byte_fallback", False) is not False:
            raise ValueError("Unigram byte fallback is not supported")
        vocabulary = model.get("vocab")
        if not isinstance(vocabulary, list) or not vocabulary:
            raise ValueError("Unigram vocabulary is missing")

        self.id_to_token: list[str] = []
        self.scores: list[float] = []
        for entry in vocabulary:
            if (not isinstance(entry, list) or len(entry) != 2
                    or not isinstance(entry[0], str) or not entry[0]
                    or type(entry[1]) not in (int, float)
                    or not math.isfinite(entry[1])):
                raise ValueError("invalid Unigram vocabulary entry")
            self.id_to_token.append(entry[0])
            self.scores.append(float(entry[1]))
        if len(set(self.id_to_token)) != len(self.id_to_token):
            raise ValueError("duplicate token surface in Unigram vocabulary")
        self.token_to_id = {piece: index for index, piece in enumerate(self.id_to_token)}
        self.special_by_role: dict[str, tuple[str, int]] = {}
        for role, piece in (("pad", "<pad>"), ("unk", "<unk>"), ("bos", "<s>"), ("eos", "</s>")):
            if piece not in self.token_to_id:
                raise ValueError(f"required Unigram special token missing: {role}")
            self.special_by_role[role] = (piece, self.token_to_id[piece])
        unknown_id = model.get("unk_id")
        if type(unknown_id) is not int or unknown_id != self.special_by_role["unk"][1]:
            raise ValueError("Unigram unknown ID conflicts with its vocabulary")
        self._special_ids = {identifier for _, identifier in self.special_by_role.values()}
        added_tokens = document.get("added_tokens")
        if not isinstance(added_tokens, list) or len(added_tokens) != len(self._special_ids):
            raise ValueError("invalid Unigram added special tokens")
        actual_added = set()
        for entry in added_tokens:
            if (not isinstance(entry, dict) or entry.get("special") is not True
                    or type(entry.get("id")) is not int
                    or self.token_to_id.get(entry.get("content")) != entry["id"]):
                raise ValueError("Unigram added-token mapping conflicts with vocabulary")
            actual_added.add((entry["content"], entry["id"]))
        if actual_added != set(self.special_by_role.values()):
            raise ValueError("Unigram added special tokens are inconsistent")
        self.vocabulary_kind = [
            "special" if index in self._special_ids else "character" if len(piece) == 1 else "unigram"
            for index, piece in enumerate(self.id_to_token)
        ]
        self._validate_manifest()

        # The terminal key is None, which cannot collide with a character.
        self._trie: dict[Any, Any] = {}
        for identifier, piece in enumerate(self.id_to_token):
            if identifier in self._special_ids:
                continue
            node = self._trie
            for character in piece:
                node = node.setdefault(character, {})
            node[None] = identifier
        self._unknown_score = min(self.scores) - 10.0

    @property
    def vocabulary_size(self) -> int:
        return len(self.id_to_token)

    def _validate_checksums(self) -> None:
        path = self.artifact_dir / "checksums.sha256"
        if not path.is_file():
            raise ValueError("Unigram artifact checksums.sha256 is missing")
        expected: dict[str, str] = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            digest, separator, relative = line.partition("  ")
            if (not separator or len(digest) != 64 or not relative
                    or any(character not in "0123456789abcdef" for character in digest)):
                raise ValueError("malformed Unigram artifact checksum line")
            posix = PurePosixPath(relative)
            windows = PureWindowsPath(relative)
            if (posix.is_absolute() or windows.drive or windows.is_absolute()
                    or ".." in posix.parts or ".." in windows.parts
                    or relative != posix.as_posix() or "\\" in relative):
                raise ValueError("unsafe Unigram artifact checksum path")
            if relative in expected:
                raise ValueError("duplicate Unigram artifact checksum entry")
            expected[relative] = digest
        actual = {
            file.relative_to(self.artifact_dir).as_posix(): file
            for file in self.artifact_dir.rglob("*")
            if file.is_file() and file != path
        }
        if set(expected) != set(actual) or not {"tokenizer.json", "unigram-manifest.json"} <= set(expected):
            raise ValueError("Unigram artifact checksum inventory mismatch")
        for relative, file in actual.items():
            if not file.resolve().is_relative_to(self.artifact_dir):
                raise ValueError("unsafe Unigram artifact checksum path")
            if _sha256_file(file) != expected[relative]:
                raise ValueError(f"Unigram artifact checksum mismatch: {relative}")

    def _validate_manifest(self) -> None:
        manifest = json.loads((self.artifact_dir / "unigram-manifest.json").read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("Unigram manifest must contain an object")
        if (manifest.get("algorithm") != self.algorithm
                or manifest.get("artifact_type") != "matched_fresh_unigram"
                or type(manifest.get("actual_vocabulary_size")) is not int
                or manifest["actual_vocabulary_size"] != self.vocabulary_size
                or manifest.get("tokenizer_sha256") != _sha256_file(self.artifact_dir / "tokenizer.json")
                or manifest.get("normalizer") is not None
                or manifest.get("pre_tokenizer") is not None
                or manifest.get("decoder") != "Fuse"
                or manifest.get("special_tokens") != ["<pad>", "<unk>", "<s>", "</s>"]):
            raise ValueError("Unigram manifest conflicts with its tokenizer")
        payload = {key: value for key, value in manifest.items() if key != "artifact_fingerprint"}
        canonical = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        if manifest.get("artifact_fingerprint") != hashlib.sha256(canonical.encode("utf-8")).hexdigest():
            raise ValueError("Unigram manifest fingerprint mismatch")

    def _encode_pretoken(self, pretoken: Any) -> list[EncodedToken]:
        surface = pretoken.surface
        size = len(surface)
        best = [-math.inf] * (size + 1)
        previous = [-1] * (size + 1)
        identifiers = [-1] * (size + 1)
        best[0] = 0.0
        unknown_id = self.special_by_role["unk"][1]
        for start in range(size):
            node = self._trie
            end = start
            has_character = False
            while end < size and surface[end] in node:
                node = node[surface[end]]
                end += 1
                identifier = node.get(None)
                if identifier is None:
                    continue
                if end == start + 1:
                    has_character = True
                candidate = best[start] + self.scores[identifier]
                # Earlier starting nodes win exact ties, matching HF's
                # deterministic best-path order (longest final piece).
                if candidate > best[end]:
                    best[end] = candidate
                    previous[end] = start
                    identifiers[end] = identifier
            if not has_character:
                end = start + 1
                candidate = best[start] + self._unknown_score
                if candidate > best[end]:
                    best[end] = candidate
                    previous[end] = start
                    identifiers[end] = unknown_id
        spans = []
        end = size
        while end > 0:
            start, identifier = previous[end], identifiers[end]
            if start < 0:
                raise AssertionError("Unigram best path did not cover its input")
            spans.append((start, end, identifier))
            end = start
        spans.reverse()
        merged: list[tuple[int, int, int]] = []
        for start, end, identifier in spans:
            if merged and identifier == unknown_id and merged[-1][2] == unknown_id:
                merged[-1] = (merged[-1][0], end, unknown_id)
            else:
                merged.append((start, end, identifier))
        return [EncodedToken(
            surface[start:end], identifier, pretoken.start + start, pretoken.start + end,
            pretoken.kind, self.vocabulary_kind[identifier],
        ) for start, end, identifier in merged]

    def encode(self, text: str, *, add_special_tokens: bool = False) -> Encoding:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        normalized = unicodedata.normalize("NFC", text)
        tokens: list[EncodedToken] = []
        if add_special_tokens:
            piece, identifier = self.special_by_role["bos"]
            tokens.append(EncodedToken(piece, identifier, 0, 0, "special", "special"))
        for pretoken in _pretokenize(normalized):
            tokens.extend(self._encode_pretoken(pretoken))
        if add_special_tokens:
            piece, identifier = self.special_by_role["eos"]
            tokens.append(EncodedToken(piece, identifier, len(normalized), len(normalized), "special", "special"))
        return Encoding(normalized, tuple(tokens))

    def decode(self, identifiers: list[int] | tuple[int, ...], *, skip_special_tokens: bool = True) -> str:
        pieces = []
        for identifier in identifiers:
            if type(identifier) is not int or not 0 <= identifier < self.vocabulary_size:
                raise ValueError(f"token ID out of range: {identifier}")
            if skip_special_tokens and identifier in self._special_ids:
                continue
            pieces.append(self.id_to_token[identifier])
        return "".join(pieces)

    def trace_word(self, surface: str) -> dict[str, Any]:
        encoding = self.encode(surface)
        return {
            "algorithm": self.algorithm,
            "surface": encoding.normalized_text,
            "characters": list(encoding.normalized_text),
            "initial_units": list(encoding.normalized_text),
            "shortcut": False,
            "steps": [],
            "final_tokens": [{
                "token": token.token, "id": token.identifier, "kind": token.vocabulary_kind,
                "start": token.start, "end": token.end,
            } for token in encoding.tokens],
        }
