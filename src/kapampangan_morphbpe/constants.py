from __future__ import annotations

PACKAGE_VERSION = "0.1.0"
SCHEMA_VERSION = "1.0.0"

DATASET_NAME = "kapampangan-general-corpus-v1"
DATASET_VERSION = "1.0.0"
DATASET_FINGERPRINT = "aff5de7b8fc158f144eaec4af3e3c22faa3b184859925130a04604a2aa9c5d17"
PORTABLE_ZIP_SHA256 = "9f45ba35ac48147677d269870c52d9f2244ddc3fb60703011c11f640daa6186f"

EXPECTED_COUNTS = {
    "neutral": 32_836,
    "train": 26_268,
    "validation": 3_284,
    "test": 3_284,
    "code_switched_optional": 981,
    "parallel_pam_eng": 2_484,
    "parallel_pam_tgl": 45,
    "linguistic_evidence": 806,
    "morphology_reference": 2_212,
}

PREFIXES = (
    "ma",
    "me",
    "pa",
    "maka",
    "ka",
    "mag",
    "meg",
    "mang",
    "meng",
    "i",
    "ipa",
    "makapag",
    "mig",
    "meka",
    "mekapag",
)
INFIXES = ("in", "um")
SUFFIXES = ("an",)
CIRCUMFIXES = (("ka", "an"), ("pa", "an"), ("pang", "an"))
CLITICS = ("na", "pa", "mu", "ku", "ya", "la", "ra", "ne", "no")
PANG_VARIANTS = ("pam", "pan", "panga")

SPECIAL_TOKENS = (
    ("<pad>", 0, "pad"),
    ("<unk>", 1, "unk"),
    ("<s>", 2, "bos"),
    ("</s>", 3, "eos"),
)

ROOT_REFERENCE_TYPES = frozenset(
    {
        "root",
        "lemma_or_root_candidate",
        "lexical_root_validation_candidate",
        "root_or_dictionary_headword",
    }
)
