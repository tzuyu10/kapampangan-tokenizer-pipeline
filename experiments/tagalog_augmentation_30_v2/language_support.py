"""Lossless Tagalog preparation, including verified shared roots and hyphens.

Root access is supplied by the separately frozen vendor dictionary. Only roots
already in the 993 additions or verified against the existing Kapampangan roots
are available. This module adds no runtime segmentation or generated corpus text.
"""
from __future__ import annotations

import sys
from pathlib import Path


def tagalog_segmenter(package: Path):
    sys.path.insert(0, str(package / 'vendor'))
    from filipino_tokenizer.tagalog.segmenter import TagalogSegmenter
    return TagalogSegmenter()


def _ordinary_analysis(segmenter, surface):
    lower = surface.lower()
    parts = segmenter.segment(lower)
    if ''.join(parts) != lower:
        if len(parts) >= 2 and parts[-2] in segmenter.affixes.get_infixes():
            prefix, infix, root = parts[:-2], parts[-2], parts[-1]
            if ''.join(prefix) + root[:1] + infix + root[1:] != lower:
                return (), (), 'nonconcatenative_fallback'
            parts = prefix + [root[:1], infix, root[1:]]
            roles = ['affix'] * len(prefix) + ['root', 'infix', 'root']
        else:
            return (), (), 'nonconcatenative_fallback'
    else:
        roles = ['root' if segmenter.roots.is_root(part) else
                 'infix' if part in segmenter.affixes.get_infixes() else 'affix'
                 for part in parts]
    if not parts or any(not part for part in parts):
        return (), (), 'empty_fallback'
    if len(parts) == 1:
        spans = ((0, len(surface), 'root'),) if segmenter.roots.is_root(lower) else ()
        return (), spans, 'whole_word'
    boundaries, spans, offset = [], [], 0
    for part, role in zip(parts, roles, strict=True):
        end = offset + len(part)
        spans.append((offset, end, role))
        boundaries.append(end)
        offset = end
    assert offset == len(surface)
    return tuple(boundaries[:-1]), tuple(spans), 'segmented'


def surface_analysis(segmenter, surface: str):
    """Preserve surface characters; never guess an unverified root.

The upstream analyzer already handles literal prefix/suffix/circumfix rules.
For an explicit prefix-hyphen-stem spelling, analyze the stem with those same
rules and retain the hyphen as its own surface span. Unknown stems fall back
intact. No deletion, spelling correction or synthetic training example occurs.
"""
    lower = surface.lower()
    if len(lower) != len(surface):
        return (), (), 'case_length_fallback'
    ordinary = _ordinary_analysis(segmenter, surface)
    if ordinary[0] or segmenter.roots.is_root(lower) or '-' not in lower:
        return ordinary
    prefix, stem = lower.split('-', 1)
    if not stem or prefix not in segmenter.affixes.get_prefixes():
        return ordinary
    boundaries, spans, _status = _ordinary_analysis(segmenter, stem)
    if not spans or not any(role == 'root' for _start, _end, role in spans):
        return ordinary
    offset = len(prefix) + 1
    return (tuple([len(prefix), offset, *(offset + value for value in boundaries)]),
            ((0, len(prefix), 'affix'), (len(prefix), offset, 'separator'),
             *((offset + start, offset + end, role) for start, end, role in spans)),
            'segmented_hyphenated_prefix')
