"""Select on frozen DEV, then report historical TEST and corpus diagnostics."""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO / "src"));sys.path.insert(0,str(REPO / "runtime"))
from kapampangan_morphbpe.pretokenizer import pretokenize_normalized
from kapampangan_morphbpe.runtime_bridge import load_runtime_tokenizer
from kapampangan_morphbpe.artifact import validate_artifact_files
from kapampangan_morphbpe.serialization import write_json,sha256_file,fingerprint

FAMILIES=("weighted32","infix_first48","plain","unigram")
SIZES=(6080,8192,16384)


class Model:
    def __init__(self,path,unigram=False):
        self.path=path;self.unigram=unigram
        if unigram:
            from tokenizers import Tokenizer, decoders
            self.tok=Tokenizer.from_file(str(path / "tokenizer.json"))
            # The historical control saved no decoder. Fusing pieces at runtime
            # preserves its unchanged segmentation and restores literal text.
            self.tok.decoder=decoders.Fuse()
            self.size=self.tok.get_vocab_size()
        else:
            validate_artifact_files(path)
            self.tok=load_runtime_tokenizer(path)
            self.size=self.tok.vocabulary_size
        self.cache={}
    def encode(self,surface):
        if surface not in self.cache:
            encoded=self.tok.encode(surface)
            pieces=list(encoded.tokens) if self.unigram else [t.token for t in encoded.tokens]
            ids=list(encoded.ids)
            unknown=ids.count(1)
            if not unknown:
                assert ''.join(pieces)==surface,(self.path,surface,pieces)
                if self.unigram:
                    assert self.tok.decode(ids,skip_special_tokens=False)==surface
                else:
                    assert self.tok.decode(ids)==surface
            self.cache[surface]=(pieces,unknown)
        return self.cache[surface]


def reference_score(model,rows,selection):
    encoded,predictions=[],[]
    for row in rows:
        pieces,unknown=model.encode(row['surface'])
        assert not unknown
        encoded.append(tuple(pieces))
        boundaries=set();position=0
        for piece in pieces[:-1]:
            position+=len(piece);boundaries.add(position)
        gold=row['gold_boundaries']
        predictions.append({'surface':row['surface'],'pieces':pieces,'reference':list(row['gold_pieces']),
            'tp':len(boundaries&gold),'fp':len(boundaries-gold),'fn':len(gold-boundaries),
            'exact':tuple(pieces)==row['gold_pieces'],'process':row['process'],'provenance':row['provenance']})
    metrics=selection._score(rows,encoded)
    counts={k:sum(r[k] for r in predictions) for k in ['tp','fp','fn','exact']}
    assert abs(metrics['boundary_f1']-2*counts['tp']/(2*counts['tp']+counts['fp']+counts['fn']))<1e-12
    infixes={}
    for infix in ['um','in']:
        detail=[r for r,row in zip(predictions,rows,strict=True) if row['process']=='infixation' and row['gold_boundaries']=={1,3} and row['gold_pieces'][1]==infix]
        isolated=0
        for row in detail:
            offset=0
            for piece in row['pieces']:
                if offset==1 and piece==infix:isolated+=1;break
                offset+=len(piece)
        infixes[infix]={'rows':len(detail),'isolated':isolated}
    return {'rows':len(rows),'metrics':metrics,'counts':counts,'infixes':infixes,'predictions':predictions}


def prepare_corpus(rows):
    counts=collections.Counter();row_surfaces=[]
    for row in rows:
        tokens=pretokenize_normalized(row['text'])
        counts.update((t.surface,t.kind) for t in tokens)
        row_surfaces.append({t.surface for t in tokens})
    return counts,row_surfaces


def corpus_score(model,prepared):
    counts,row_surfaces=prepared
    words=word_tokens=unknown=all_tokens=0;bad=set()
    for (surface,kind),frequency in counts.items():
        pieces,unk=model.encode(surface)
        all_tokens+=len(pieces)*frequency
        unknown+=unk*frequency
        if unk:bad.add(surface)
        if kind=='word':
            words+=frequency;word_tokens+=len(pieces)*frequency
    return {'records':len(row_surfaces),'word_occurrences':words,'word_tokens':word_tokens,'word_fertility':word_tokens/words,
        'total_tokens':all_tokens,'unknown_tokens':unknown,'rows_with_unknown':sum(bool(s&bad) for s in row_surfaces),
        'all_known_pretoken_roundtrips_verified':True}


def boot(left,right):
    assert [r['surface'] for r in left]==[r['surface'] for r in right]
    def f1(rows,indices):
        tp=sum(rows[i]['tp'] for i in indices);fp=sum(rows[i]['fp'] for i in indices);fn=sum(rows[i]['fn'] for i in indices)
        return 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0
    rng=random.Random(20261017);deltas=[]
    for _ in range(5000):
        indices=[rng.randrange(len(left)) for _ in left]
        deltas.append(f1(left,indices)-f1(right,indices))
    deltas.sort()
    return {'resamples':5000,'seed':20261017,'observed_difference':f1(left,range(len(left)))-f1(right,range(len(right))),
        'percentile95':[deltas[124],deltas[4874]],'scope':'exploratory word-type bootstrap, ignores root dependence, label uncertainty, multiple comparisons and DEV selection'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--results',type=Path,required=True)
    args=parser.parse_args();results=args.results.resolve()
    reports=results / 'reports';reports.mkdir(exist_ok=True)
    sys.path.insert(0,str(args.inputs))
    from train_tokenizer import verify_inputs
    manifest=verify_inputs(args.inputs)
    spec=importlib.util.spec_from_file_location('frozen_selection_metrics',REPO / 'experiments/tokenizer_selection_v1/run_selection.py')
    selection=importlib.util.module_from_spec(spec);spec.loader.exec_module(selection)
    dev_path=REPO / 'experiments/tokenizer_selection_v1/data/dev.csv'
    assert sha256_file(dev_path)=='c36f662b31d882503d7bde33a245cba6626e8b34c780a082628e1cd992b34275'
    dev=selection.load_split(dev_path)
    candidates=[(f'{family}_{size}',family,size,results / 'vocab_grid' / family / f'vocab-{size}',family=='unigram',True) for family in FAMILIES for size in SIZES]
    candidates.extend([
        ('original_weighted32_6080','weighted32',6080,REPO / 'webapp/backend/tokenizer/artifacts/morphbpe-penalty32',False,False),
        ('original_infix_first48_6080','infix_first48',6080,REPO / 'webapp/backend/tokenizer/variants/infix_first_penalty48/source_artifact',False,False),
        ('original_plain_6080','plain',6080,REPO / 'webapp/backend/tokenizer/artifacts/plain-bpe',False,False)])
    old_unigram=REPO / 'experiments/expanded_morphology_v4/artifacts/unigram-ablation/vocab-6080'
    if (old_unigram / 'tokenizer.json').exists():
        candidates.append(('original_unigram_6080','unigram',6080,old_unigram,True,False))
    scores={};models={}
    for name,family,size,path,unigram,is_new in candidates:
        model=Model(path,unigram);assert model.size==size
        models[name]=model
        score=reference_score(model,dev,selection)
        scores[name]={'family':family,'vocabulary_size':size,'new_augmented_training':is_new,'artifact':str(path),
            'tokenizer_sha256':sha256_file(path / 'tokenizer.json'),'dev':score}
        write_json(reports / f'{name}-dev.json',score)
        print(f'DEV {name}: F1={score["metrics"]["boundary_f1"]:.6f}',flush=True)
    def rank(name):
        m=scores[name]['dev']['metrics']
        return (m['boundary_f1'],m['exact_match'],-m['fertility'])
    names=[n for n,s in scores.items() if s['new_augmented_training']]
    ordered=sorted(names,key=rank,reverse=True)
    winner=ordered[0]
    per_family={f:max((n for n in names if scores[n]['family']==f),key=rank) for f in FAMILIES}
    selected={'criterion':'DEV boundary F1, then exact match, then lower DEV fertility','overall_winner':winner,'best_per_family':per_family,
        'ranking':ordered,'dev_csv_sha256':sha256_file(dev_path),'morphology_test_read_at_selection':False}
    write_json(reports / 'selection-before-test.json',selected)
    # This historical test has appeared in earlier project reports. Its reuse
    # is exploratory; keep rankings fixed before reading it in this run.
    test_path=REPO / 'experiments/tokenizer_selection_v1/data/test.csv'
    assert sha256_file(test_path)=='1eff199e25c8969aa9f2defebff2032702465019f927829f888217b40144ed8c'
    test=selection.load_split(test_path)
    csv.field_size_limit(2**31-1)
    with (results / 'evaluation_inputs/kapampangan_validation.csv').open(encoding='utf-8',newline='') as stream:
        kap_rows=list(csv.DictReader(stream))
    tag_rows=[json.loads(line) for line in (results / 'evaluation_inputs/tagalog_unseen_articles.jsonl').read_text(encoding='utf-8').splitlines()]
    corpora={'kapampangan_validation':prepare_corpus(kap_rows),'tagalog_unseen_articles':prepare_corpus(tag_rows)}
    train_words={json.loads(line)['surface'].casefold() for line in (args.inputs / 'prepared/training-stream.jsonl').read_text(encoding='utf-8').splitlines() if json.loads(line)['kind']=='word'}
    for name,score in scores.items():
        model=models[name]
        score['test']=reference_score(model,test,selection)
        write_json(reports / f'{name}-test.json',score['test'])
        score['corpus']={label:corpus_score(model,prepared) for label,prepared in corpora.items()}
        probes=['kumain','kuman','sumulat','sinulat','bumasa','magsasaka','bukid','sumikat']
        score['diagnostic_probes']={word:model.encode(word)[0] for word in probes}
        print(f'TEST/corpus complete: {name}',flush=True)
        model.cache.clear()
    comparisons={}
    for family in ['weighted32','infix_first48','plain','unigram']:
        new=f'{family}_6080';old=f'original_{family}_6080'
        if old in scores:comparisons[f'{new}_minus_{old}']=boot(scores[new]['dev']['predictions'],scores[old]['dev']['predictions'])
    comparisons['winner_minus_runner_up']=boot(scores[winner]['dev']['predictions'],scores[ordered[1]]['dev']['predictions'])
    body={'selection':selected,'scores':scores,'exploratory_dev_bootstrap':comparisons,'training_manifest_sha256':sha256_file(args.inputs / 'manifest.json'),
        'augmented_dataset_fingerprint':manifest['augmented_dataset_fingerprint'],'dev_rows':len(dev),'test_rows':len(test),
        'dev_words_seen_in_augmented_training':sum(r['surface'].casefold() in train_words for r in dev),
        'test_words_seen_in_augmented_training':sum(r['surface'].casefold() in train_words for r in test),
        'labels':'mixed silver and partial user adjudication; not independent native-speaker gold',
        'tagalog_morphology_gold_available':False,'tagalog_metric_scope':'article-disjoint text coverage and fertility only',
        'test_scope':'historical reference previously evaluated; exploratory reuse, ranking frozen on DEV first',
        'neural_training_or_bleu_chrf_evaluation':False}
    write_json(reports / 'comparison.json',{**body,'report_fingerprint':fingerprint(body)})
    fields=['configuration','family','vocabulary','new_training','dev_boundary_f1','dev_exact','dev_consistency_f1','dev_fertility','test_boundary_f1','kapampangan_word_fertility','tagalog_word_fertility','kapampangan_unknown_tokens','tagalog_unknown_tokens']
    with (reports / 'comparison.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for name in [*ordered,*[n for n in scores if n not in ordered]]:
            s=scores[name];m=s['dev']['metrics'];c=s['corpus']
            writer.writerow(dict(zip(fields,[name,s['family'],s['vocabulary_size'],s['new_augmented_training'],m['boundary_f1'],m['exact_match'],m['mcf1'],m['fertility'],s['test']['metrics']['boundary_f1'],c['kapampangan_validation']['word_fertility'],c['tagalog_unseen_articles']['word_fertility'],c['kapampangan_validation']['unknown_tokens'],c['tagalog_unseen_articles']['unknown_tokens']],strict=True)))
    lines=['# Kapampangan plus Tagalog tokenizer comparison','','12 newly trained configurations; all use the same augmented corpus. No neural model training.','',
        f'**DEV-selected winner: {winner}.** Ranking uses boundary F1, then exact match, then lower fertility.','',
        '| Configuration | Vocab | DEV boundary F1 (%) | Exact (%) | Consistency F1 (%) | TEST F1 (%) | PAM tokens/word | TL tokens/word |',
        '|---|---:|---:|---:|---:|---:|---:|---:|']
    for name in ordered:
        s=scores[name];m=s['dev']['metrics'];c=s['corpus']
        lines.append(f'| {name} | {s["vocabulary_size"]:,} | {100*m["boundary_f1"]:.3f} | {100*m["exact_match"]:.3f} | {100*m["mcf1"]:.3f} | {100*s["test"]["metrics"]["boundary_f1"]:.3f} | {c["kapampangan_validation"]["word_fertility"]:.4f} | {c["tagalog_unseen_articles"]["word_fertility"]:.4f} |')
    lines+=['','## Original 6,080-token references','','| Configuration | DEV F1 (%) | Exact (%) | PAM tokens/word | TL tokens/word |','|---|---:|---:|---:|---:|']
    for name,s in scores.items():
        if not s['new_augmented_training']:
            m=s['dev']['metrics'];c=s['corpus']
            lines.append(f'| {name} | {100*m["boundary_f1"]:.3f} | {100*m["exact_match"]:.3f} | {c["kapampangan_validation"]["word_fertility"]:.4f} | {c["tagalog_unseen_articles"]["word_fertility"]:.4f} |')
    lines+=['','## Scope and limits','',f'Morphology DEV has272 words and historical TEST262. {body["dev_words_seen_in_augmented_training"]}/272 DEV and {body["test_words_seen_in_augmented_training"]}/262 TEST word forms occur in tokenizer training. Root-family separation between reference splits does not make these unseen training words.',
        'Labels are mixed silver and partially user-derived, not independent native-speaker gold. Historical TEST has been used before; this is exploratory confirmation, not a new final test.',
        'Corpus diagnostics use all3,284 original Kapampangan validation records and1,000 Tagalog records from article titles absent from the added training subset. Tagalog has no validated morphology gold, so its fertility/coverage does not establish Tagalog morphological accuracy.',
        'Fertility measures sequence length; a lower value can coexist with worse morphological boundaries. The winner is specific to the declared DEV criterion. Bootstrap intervals and paired predictions are in comparison.json.',
        'Unigram is a newly trained matched control, separate from native NLLB target tokenization. Its independent EM runs can differ. All tokenizers retain6,080/8,192/16,384 tokens and matched initial characters/special tokens.',
        'No installed artifact or translation model was replaced. BLEU, chrF++, translation superiority and new source-embedding adaptation were not evaluated.']
    (reports / 'comparison.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'winner':winner,'best_per_family':per_family,'ranking':ordered},indent=2),flush=True)


if __name__=='__main__':
    main()
