"""Surface-preserving Tagalog morphology for the separate mixed-corpus experiment."""
from __future__ import annotations

import sys
from pathlib import Path


def tagalog_segmenter(package: Path):
    sys.path.insert(0, str(package / "vendor"))
    from filipino_tokenizer.tagalog.segmenter import TagalogSegmenter

    return TagalogSegmenter()


def surface_analysis(segmenter, surface: str):
    """Convert underlying infix/root order into lossless surface spans.

    Upstream returns ['um', 'kain'] for kumain. BPE needs k|um|ain instead.
    Unsupported non-concatenative analyses fall back to an intact word.
    Case and every original character are preserved.
    """
    lower = surface.lower()
    if len(lower) != len(surface):
        return (), (), "case_length_fallback"
    parts = segmenter.segment(lower)
    roles = ["affix"] * len(parts)
    if "".join(parts) != lower:
        if len(parts) >= 2 and parts[-2] in segmenter.affixes.get_infixes():
            prefix, infix, root = parts[:-2], parts[-2], parts[-1]
            reconstructed = "".join(prefix) + root[:1] + infix + root[1:]
            if reconstructed == lower:
                parts = prefix + [root[:1], infix, root[1:]]
                roles = ["affix"] * len(prefix) + ["root", "infix", "root"]
            else:
                return (), (), "nonconcatenative_fallback"
        else:
            return (), (), "nonconcatenative_fallback"
    else:
        roles = [
            "root" if segmenter.roots.is_root(p) else
            "infix" if p in segmenter.affixes.get_infixes() else "affix"
            for p in parts
        ]
    if not parts or any(not part for part in parts):
        return (), (), "empty_fallback"
    if len(parts) == 1:
        spans = ((0, len(surface), "root"),) if segmenter.roots.is_root(lower) else ()
        return (), spans, "whole_word"
    boundaries, spans, offset = [], [], 0
    for part, role in zip(parts, roles, strict=True):
        end = offset + len(part)
        spans.append((offset, end, role))
        boundaries.append(end)
        offset = end
    assert offset == len(surface)
    return tuple(boundaries[:-1]), tuple(spans), "segmented"
