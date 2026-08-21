"""Beam-search decoding for the held-out test set."""
from __future__ import annotations

import torch


@torch.no_grad()
def translate(
    model,
    src_tokenizer,
    nllb_tokenizer,
    sentences: list[str],
    tgt_lang: str = "tgl_Latn",
    batch_size: int = 8,
    num_beams: int = 5,
    max_new_tokens: int = 128,
    length_penalty: float = 1.0,
    device: str = "cuda",
    max_src_len: int = 128,
) -> list[str]:
    model.eval()
    forced_bos = nllb_tokenizer.convert_tokens_to_ids(tgt_lang)
    pad_id = getattr(src_tokenizer, "pad_id", None)
    if pad_id is None:
        pad_id = nllb_tokenizer.pad_token_id

    out: list[str] = []
    for i in range(0, len(sentences), batch_size):
        chunk = sentences[i : i + batch_size]
        enc = [src_tokenizer.encode(s, max_length=max_src_len) for s in chunk]
        m = max(len(e) for e in enc)
        ids = torch.tensor([e + [pad_id] * (m - len(e)) for e in enc], device=device)
        att = torch.tensor([[1] * len(e) + [0] * (m - len(e)) for e in enc], device=device)
        gen = model.generate(
            input_ids=ids,
            attention_mask=att,
            forced_bos_token_id=forced_bos,
            num_beams=num_beams,
            max_new_tokens=max_new_tokens,
            length_penalty=length_penalty,
            early_stopping=True,
        )
        out.extend(nllb_tokenizer.batch_decode(gen, skip_special_tokens=True))
        print(f"  decoded {min(i+batch_size, len(sentences))}/{len(sentences)}", end="\r")
    print()
    return out
