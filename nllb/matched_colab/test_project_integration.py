"""Regression checks using real project artifacts and a tiny actual M2M100 model."""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import torch
from transformers import M2M100Config, M2M100ForConditionalGeneration, PreTrainedTokenizerFast
from tokenizers import Tokenizer, models, pre_tokenizers, processors

import nllb_source_adapter as a


def main():
    torch.set_num_threads(2)
    root = Path(__file__).parent/'project_inputs'
    sys.path.insert(0,str(root/'runtime'))
    data,meta,audit = a.read_project_bundle(root/'bundle')
    print('PASS: frozen bundle hashes, row counts, cross-split duplicate guard')
    for condition in ['plain_bpe','morph_bpe']:
        source = a.SourceTokenizer(root/'artifacts'/condition)
        assert source.size == 6080 and source.special == {'<pad>':1,'<unk>':0,'<s>':2,'</s>':3}
        for rows in data.values():
            for row in rows:
                mapped = a.source_ids_for(condition,row)
                assert mapped == source.encode(row['source'])
                restored = [source.to_model_id(i) for i in mapped]
                assert tuple(restored) == source.backend.encode(row['source'],add_special_tokens=True).ids
        print('PASS:',condition,'exact runtime/bundle ID parity for all 4227 records')
    try: a.source_ids_for('typo',data['train'][0])
    except ValueError: pass
    else: raise AssertionError('Unknown condition fallback')
    assert a.source_ids_for('bpe6080',data['train'][0]) == a.source_ids_for('plain_bpe',data['train'][0])

    # Position/mask regression: unknown=0 is a real input, padding=1 is not.
    vocab={'<s>':0,'<pad>':1,'</s>':2,'<unk>':3,'tgl_Latn':4,'a':5,'b':6,'c':7}
    backend=Tokenizer(models.WordLevel(vocab,unk_token='<unk>'))
    backend.pre_tokenizer=pre_tokenizers.Whitespace()
    backend.post_processor=processors.TemplateProcessing(single='tgl_Latn $A </s>',special_tokens=[('tgl_Latn',4),('</s>',2)])
    target=PreTrainedTokenizerFast(tokenizer_object=backend,unk_token='<unk>',pad_token='<pad>',bos_token='<s>',eos_token='</s>',additional_special_tokens=['tgl_Latn'])
    config=M2M100Config(vocab_size=8,d_model=8,encoder_layers=1,decoder_layers=1,
        encoder_attention_heads=2,decoder_attention_heads=2,encoder_ffn_dim=16,decoder_ffn_dim=16,
        pad_token_id=1,bos_token_id=0,eos_token_id=2,decoder_start_token_id=2,
        dropout=0.,attention_dropout=0.,activation_dropout=0.,encoder_layerdrop=0.,decoder_layerdrop=0.)
    config._attn_implementation='eager'
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        model=M2M100ForConditionalGeneration(config)
        model.save_pretrained(tmp/'base')
        frozen={n:p.detach().clone() for n,p in model.named_parameters()}
        embedding_type=type(model.get_encoder().embed_tokens)
        scale=model.get_encoder().embed_tokens.embed_scale
        a.install_source_embedding(model,6080,42)
        a.warm_start(model,source,target)
        assert type(model.get_encoder().embed_tokens)==embedding_type
        assert model.get_encoder().embed_tokens.embed_scale==scale
        sw=model.get_encoder().embed_tokens.weight
        dw=model.get_decoder().embed_tokens.weight
        assert torch.equal(sw[0],dw[target.unk_token_id])
        assert torch.equal(sw[2],dw[target.bos_token_id])
        assert torch.equal(sw[3],dw[target.eos_token_id])
        assert torch.count_nonzero(sw[1])==0
        rows=[{'input_ids':[2,0,15,3],'labels':[4,5,6,7,2]},
              {'input_ids':[2,0,3],'labels':[4,5,2]}]
        batch=a.collate(rows)
        assert batch['attention_mask'].tolist()==[[1,1,1,1],[1,1,1,0]]
        model.eval()
        with torch.no_grad():
            single=model(**a.collate(rows[:1])).logits[0]
            padded=model(**batch).logits[0]
            torch.testing.assert_close(single,padded,atol=1e-6,rtol=1e-5)
        a.preflight(model,rows[0],torch.device('cpu'))
        for n,p in model.named_parameters():
            if not p.requires_grad: assert torch.equal(p,frozen[n])
        print('PASS: padding/unknown positions, scaled embedding, warm-start control rows, frozen target weights')
        from safetensors.torch import save_file
        out=tmp/'export';out.mkdir()
        shutil.copytree(source.artifact_dir,out/'source_artifact')
        shutil.copytree(root/'runtime',out/'runtime')
        target.save_pretrained(out/'target_tokenizer')
        save_file({'weight':sw.detach().contiguous()},str(out/'best_source.safetensors'))
        a.save_json(out/'manifest.json',dict(model_id=str(tmp/'base'),revision=None,source_vocab_size=6080,
            source_format='kapampangan_project',cfg={'seed':42},
            identity={'tokenizer_sha256':a.digest(source.artifact_dir/'tokenizer.json')}))
        loaded,reloaded_source,_=a.load_bundle(out)
        model.eval()
        with torch.no_grad(): torch.testing.assert_close(model(**batch).logits,loaded(**batch).logits,atol=0,rtol=0)
        assert reloaded_source.encode('Kasulatan ya.')==source.encode('Kasulatan ya.')
        print('PASS: project artifact + adapter save/reload preserves IDs and logits')
    print('ALL PROJECT CHECKS PASSED; full 600M GPU training not executed.')


if __name__=='__main__': main()
