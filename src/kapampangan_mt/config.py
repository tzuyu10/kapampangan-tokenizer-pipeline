"""Tiny YAML config loader with dotted-key CLI overrides."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import yaml


class Config(dict):
    def get_path(self, dotted: str, default: Any = None) -> Any:
        node: Any = self
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def set_path(self, dotted: str, value: Any) -> None:
        parts = dotted.split(".")
        node: Any = self
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = value


def load_config(path: str | Path = "config/pipeline.yaml",
                overrides: list[str] | None = None) -> Config:
    cfg = Config(yaml.safe_load(Path(path).read_text(encoding="utf-8")))
    for ov in overrides or []:
        key, _, raw = ov.partition("=")
        try:
            value = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            value = raw
        cfg.set_path(key.strip(), value)
    return cfg
