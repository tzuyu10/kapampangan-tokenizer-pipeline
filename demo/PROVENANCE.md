# Provenance

Copied 2026-09-08 from the research repo
`kapampangan-morphbpe-paper-v1` (branch feat/kapampangan-morphbpe), byte-identical.

The runtime loader is `runtime/kapampangan_morphbpe_runtime/` from that repo.

## `morphbpe-penalty8/`  <-  `experiments/expanded_morphology_v4/artifacts/penalty-8/candidates/vocab-6080`

- artifact fingerprint: `f2ea195a970c387f5e5e3ba7fe5675bae9103853950d46d1072fd2685d151258`
- condition: `penalty-8`  |  vocab 6080  |  4488 merges
- lexicon used at runtime: `False`
- SHA-256 (all files as copied):

  - `b53af7cc7a158f617b56527df508396eaf7274163deeb5930da87aa4e25a18a6`  checksums.sha256
  - `5fbc9d3c68a22bc668e6c3de7d66782792f6dee9841d7b16948d07bb8b21735f`  merges.json
  - `93feac29893a18dfcb6c77e54ce5e02d10a5ebd57b4a5f0d83590bf21a231005`  normalization.json
  - `6315cf42d8aa53234fe3d31fee173be7fb7e382debe8b0e3d911ab8a9ecf0cda`  pretokenizer.json
  - `7735fa9451bc5d4b8495c2cc9aec21d3882b2f65d24e38577de3e6a5d6f0535c`  special_tokens.json
  - `f4af99ba64010ec48c7558bec73ee6791d2c13a62aeb15ecd634697306b7880d`  tokenizer-manifest.json
  - `b486a29333b738c454a23a7afe15d8d7391e1d0ae87a5de0b304d4041a134420`  tokenizer.json
  - `ea28f640643a6c390241e1bf413c2b24e43f6d0ff36d604a18e7714bef0706b3`  TOKENIZER_CARD.md
  - `0e14aa92c691c6bb62c564f9b983ff5c002c18f26f85ec18d8a58c967fbeb41d`  vocab.json

## `unigram-lm-6080/`  <-  `experiments/expanded_morphology_v4/artifacts/unigram-ablation/vocab-6080`

- artifact fingerprint: `454549cf07cc05ad5b8d6c8de9488126656da750a201bf5a360d71615f2a0662`
- condition: `unigram-ablation` (Unigram-LM, NLLB's subword algorithm)  |  vocab 6080
  |  trainer `tokenizers.trainers.UnigramTrainer` 0.23.1
- NOT byte-reproducible across independent runs (a property of the third-party
  Unigram/EM trainer); this is one frozen trained instance.
- lexicon used at runtime: `False`
- SHA-256 (all files as copied):

  - `cc9480d6fef93647eecf5730cd204e26c8c67b383640eee5c51c9138fd114e39`  tokenizer.json
  - `d792fe53961229977e210029a22cef94382de3cc65d2b24e028c45da2eebdaa4`  unigram-ablation-manifest.json

  (`tokenizer.json` is byte-identical to the source; `unigram-ablation-manifest.json`
  carries its own `tokenizer_sha256` field referencing the same digest.)

## `plain-bpe/`  <-  `experiments/expanded_morphology_v4/artifacts/plain/candidates/vocab-6080`

- artifact fingerprint: `005f6da948e787876732424df6f25efd6086e0a6d693918892683c346b57f478`
- condition: `plain`  |  vocab 6080  |  4488 merges
- lexicon used at runtime: `False`
- SHA-256 (all files as copied):

  - `623374c2e4ea381444520e63024350af1c746b5d9d9cfd368bcfc207e918ae98`  checksums.sha256
  - `fbff9bb14c5ec1d135a7790407cb7ba296ff15bbc6bdffbe771bb55ea7c70bc8`  merges.json
  - `93feac29893a18dfcb6c77e54ce5e02d10a5ebd57b4a5f0d83590bf21a231005`  normalization.json
  - `6315cf42d8aa53234fe3d31fee173be7fb7e382debe8b0e3d911ab8a9ecf0cda`  pretokenizer.json
  - `7735fa9451bc5d4b8495c2cc9aec21d3882b2f65d24e38577de3e6a5d6f0535c`  special_tokens.json
  - `ede62f5b1bb8d803d9738cd9d762c3bb6fcf7e6aba479b0936cd6c0582e71cc4`  tokenizer-manifest.json
  - `4098512366353a8d0d0793b11a62eb53f92ea442972b29bb042a4cef2069fa52`  tokenizer.json
  - `9922bcfdc82e321aa9b518a96eb0a3f8a53e169dcca282f71b307f993c6bbb06`  TOKENIZER_CARD.md
  - `1208f4505ce09fb833c7d1c3cc35673fcef8725dfc1f0d56b6ba1bbedc4c06df`  vocab.json

runtime `__init__.py` : `ce10d2717dc76d2f823448c8f791a11da37d5f48044470aff59f48d1470b8d41`
runtime `tokenizer.py` : `b78b9e0b6535e32063aecfbcc22bce2f4ff70bae25f23e264e081e9460f5d157`
