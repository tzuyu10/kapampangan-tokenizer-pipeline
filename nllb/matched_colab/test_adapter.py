"""CPU integration test with a tiny M2M100; no pretrained download required."""
import ast
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import nbformat
import torch
from tokenizers import Tokenizer, models, pre_tokenizers, processors
from transformers import M2M100Config, M2M100ForConditionalGeneration, PreTrainedTokenizerFast

import nllb_source_adapter as a


def main():
    torch.set_num_threads(2)
    root = Path(__file__).parent
    nb = nbformat.read(root/'NLLB_600M_Kapampangan_Training.ipynb', as_version=4)
    nbformat.validate(nb)
    for cell in nb.cells:
        if cell.cell_type != 'code': continue
        code = cell.source
        if code.startswith('%%writefile'): code = '\n'.join(code.splitlines()[1:])
        else: code = '\n'.join(s for s in code.splitlines() if not s.startswith('%'))
        ast.parse(code)
    assert any(a_code.source.endswith((root/'nllb_source_adapter.py').read_text()) for a_code in nb.cells if a_code.cell_type=='code')
    print('PASS: notebook schema, Python syntax, embedded helper equality')
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        vocab = {'<s>':0,'<pad>':1,'</s>':2,'<unk>':3,'<kap>':4,
                 'a':5,'b':6,'c':7,'d':8,'e':9,'f':10,'g':11}
        backend = Tokenizer(models.WordLevel(vocab, unk_token='<unk>'))
        backend.pre_tokenizer = pre_tokenizers.Whitespace()
        tok_path = tmp/'tokenizer.json'; backend.save(str(tok_path))
        src = a.SourceTokenizer(tok_path, 12)
        assert src.encode('a b') == [4,5,6,2]
        try: a.SourceTokenizer(tok_path, 6080)
        except ValueError: pass
        else: raise AssertionError('size check absent')
        tv = {**vocab, 'tgl_Latn':12, **{f'x{i}':i for i in range(13,32)}}
        tb = Tokenizer(models.WordLevel(tv, unk_token='<unk>'))
        tb.pre_tokenizer = pre_tokenizers.Whitespace()
        tb.post_processor = processors.TemplateProcessing(single='tgl_Latn $A </s>', special_tokens=[('tgl_Latn',12),('</s>',2)])
        tgt = PreTrainedTokenizerFast(tokenizer_object=tb, unk_token='<unk>',pad_token='<pad>',bos_token='<s>',eos_token='</s>',additional_special_tokens=['tgl_Latn'])
        records = [dict(id=str(i),source=s,target='a b c d',split=split,group_id=str(i))
                   for i,(s,split) in enumerate([('a b','train'),('b c','train'),('a c','validation'),('d e','test')])]
        data_path = tmp/'data.jsonl'
        data_path.write_text('\n'.join(json.dumps(r) for r in records),encoding='utf8')
        splits = a.read_parallel(data_path)
        data,stats = a.prepare(splits,src,tgt,20,20)
        assert data['train'][0]['labels'][0] == 12
        bad = records + [{**records[0], 'id':'duplicate', 'split':'test'}]
        data_path.write_text('\n'.join(json.dumps(r) for r in bad),encoding='utf8')
        try: a.read_parallel(data_path)
        except ValueError: pass
        else: raise AssertionError('leakage not detected')
        try: a.prepare(splits,src,tgt,3,20)
        except ValueError: pass
        else: raise AssertionError('overlength not detected')
        print('PASS: tokenizer contract, target prefix, duplicate rejection, length guard')
        config = M2M100Config(vocab_size=32,d_model=16,encoder_layers=1,decoder_layers=1,
            encoder_attention_heads=2,decoder_attention_heads=2,encoder_ffn_dim=32,decoder_ffn_dim=32,
            dropout=0.,attention_dropout=0.,activation_dropout=0.,encoder_layerdrop=0.,decoder_layerdrop=0.,
            pad_token_id=1,bos_token_id=0,eos_token_id=2,decoder_start_token_id=2,max_position_embeddings=64)
        config._attn_implementation = 'eager'
        torch.manual_seed(0)
        base = M2M100ForConditionalGeneration(config)
        base_path = tmp/'base'; base.save_pretrained(base_path)
        original = {n:p.detach().clone() for n,p in base.named_parameters()}
        model = a.install_source_embedding(base,12,42)
        device = torch.device('cpu')
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
        a.preflight(model,data['train'][0],device)
        initial = model.get_encoder().embed_tokens.weight.detach().clone()
        cfg = dict(seed=42,epochs=3,lr=0.03,batch_size=1,accumulation=3)
        out = tmp/'run'; identity = {'tokenizer_sha256':a.digest(tok_path)}
        history = a.train(model,data,cfg,identity,out,device)
        assert not torch.equal(model.get_encoder().embed_tokens.weight,initial)
        for n,p in model.named_parameters():
            if not p.requires_grad: assert torch.equal(p,original[n]),n
        print('PASS: real forward/backward, checkpointed training, all frozen weights unchanged')
        # Simulate interruption before the second validation, then resume epoch 1 checkpoint.
        second = a.load_base(str(base_path),None,42,12)
        second.gradient_checkpointing_enable(gradient_checkpointing_kwargs={'use_reentrant':False})
        calls = [0]; real = a.validation_loss
        def interrupted(*args):
            calls[0] += 1
            if calls[0] == 2: raise RuntimeError('simulated interruption')
            return real(*args)
        resumed_path = tmp/'resumed'
        with patch.object(a,'validation_loss',interrupted):
            try: a.train(second,data,cfg,identity,resumed_path,device)
            except RuntimeError as e: assert str(e)=='simulated interruption'
        resumed = a.train(second,data,cfg,identity,resumed_path,device,resume=True)
        assert resumed == history
        assert torch.equal(second.get_encoder().embed_tokens.weight,model.get_encoder().embed_tokens.weight)
        print('PASS: interrupted/resumed training equals uninterrupted CPU run')
        import shutil
        shutil.copy2(tok_path,out/'source_tokenizer.json')
        tgt.save_pretrained(out/'target_tokenizer')
        a.save_json(out/'manifest.json',dict(model_id=str(base_path),revision=None,source_vocab_size=12,cfg=cfg,identity=identity))
        loaded,loaded_src,loaded_tgt = a.load_bundle(out)
        model.eval(); loaded.eval()
        batch = a.collate(data['test'])
        with torch.no_grad():
            assert torch.equal(model(**batch).logits,loaded(**batch).logits)
        pred = a.predict(loaded,loaded_src,loaded_tgt,splits['test'],device,max_new_tokens=6,beams=2)
        assert len(pred)==1
        scores = a.score_and_export(splits['test'],[splits['test'][0]['target']],out/'test')
        assert abs(scores['BLEU']['score']-100)<1e-6 and scores['chrF++']['score']==100
        print('PASS: adapter reload preserves logits, beam generation, BLEU/chrF++ exports')
    print('ALL CHECKS PASSED. Full 600M/Colab training has not been run.')


if __name__=='__main__': main()
