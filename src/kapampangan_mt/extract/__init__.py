"""Source-faithful extraction of Kapampangan dictionary entries into JSONL.

EXTRACTION ONLY. No morphological analysis, no guessed roots or affixes, no
translation. Syllable information stays under ``syllables``; it is never
reinterpreted as prefix/infix/suffix. Morphological annotation is a separate,
later stage.
"""
from .schema import Entry, Source, assess_ocr, make_id, new_entry

__all__ = ["Entry", "Source", "new_entry", "assess_ocr", "make_id"]
