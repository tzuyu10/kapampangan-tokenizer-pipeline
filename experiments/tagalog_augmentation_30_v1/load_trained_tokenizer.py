"""Load a delivered BPE or Unigram source tokenizer without a neural model."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


class SourceTokenizer:
    def __init__(self,artifact: Path):
        root=Path(__file__).resolve().parent
        sys.path.insert(0,str(root / 'code/source'))
        sys.path.insert(0,str(root / 'code/runtime'))
        from kapampangan_morphbpe.pretokenizer import pretokenize
        self.pretokenize=pretokenize
        self.unigram=(artifact / 'unigram-manifest.json').is_file()
        if self.unigram:
            from tokenizers import Tokenizer
            self.tokenizer=Tokenizer.from_file(str(artifact / 'tokenizer.json'))
        else:
            from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
            self.tokenizer=load_runtime_tokenizer(artifact)
    def encode(self,text):
        if not self.unigram:
            result=self.tokenizer.encode(text)
            return {'normalized_text':result.normalized_text,'pieces':[t.token for t in result.tokens],'ids':list(result.ids)}
        normalized,pretokens=self.pretokenize(text)
        pieces=[];ids=[]
        for token in pretokens:
            encoded=self.tokenizer.encode(token.surface,add_special_tokens=False)
            pieces.extend(encoded.tokens);ids.extend(encoded.ids)
        return {'normalized_text':normalized,'pieces':pieces,'ids':ids}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact',type=Path,required=True)
    parser.add_argument('--text',required=True)
    args=parser.parse_args()
    print(json.dumps(SourceTokenizer(args.artifact).encode(args.text),ensure_ascii=True,indent=2))
