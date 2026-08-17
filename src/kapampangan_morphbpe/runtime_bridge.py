from __future__ import annotations

import sys
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import Protocol, cast


class RuntimeEncodedToken(Protocol):
    token: str
    identifier: int
    start: int
    end: int
    pretoken_kind: str
    vocabulary_kind: str


class RuntimeEncoding(Protocol):
    normalized_text: str
    tokens: tuple[RuntimeEncodedToken, ...]
    ids: tuple[int, ...]


class RuntimeTokenizer(Protocol):
    def encode(self, text: str, *, add_special_tokens: bool = False) -> RuntimeEncoding: ...

    def decode(
        self, identifiers: list[int] | tuple[int, ...], *, skip_special_tokens: bool = True
    ) -> str: ...

    @property
    def vocabulary_size(self) -> int: ...


def load_runtime_tokenizer(artifact_dir: Path) -> RuntimeTokenizer:
    runtime_root = Path(__file__).resolve().parents[2] / "runtime"
    runtime_text = str(runtime_root)
    if runtime_text not in sys.path:
        sys.path.insert(0, runtime_text)
    module = import_module("kapampangan_morphbpe_runtime")
    factory = cast(Callable[[Path], RuntimeTokenizer], module.Tokenizer)
    return factory(artifact_dir)
