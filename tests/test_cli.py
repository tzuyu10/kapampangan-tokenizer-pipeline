from __future__ import annotations

import json
from pathlib import Path

from kapampangan_morphbpe.cli import main


def test_validate_and_tokenize_cli(toy_artifact: Path, capsys: object) -> None:
    assert main(["validate-artifact", "--artifact", str(toy_artifact)]) == 0
    validate_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert validate_output["reload_succeeded"] is True

    assert (
        main(
            [
                "tokenize",
                "--artifact",
                str(toy_artifact),
                "--text",
                "ab  ñ!",
            ]
        )
        == 0
    )
    tokenize_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert tokenize_output["normalized_text"] == "ab  ñ!"
    ids = tokenize_output["ids"]

    assert (
        main(
            [
                "decode",
                "--artifact",
                str(toy_artifact),
                "--ids",
                json.dumps(ids),
            ]
        )
        == 0
    )
    decode_output = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert decode_output["text"] == "ab  ñ!"
