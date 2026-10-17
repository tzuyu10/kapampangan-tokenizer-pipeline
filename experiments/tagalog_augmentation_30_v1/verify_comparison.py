"""Recompute morphology arithmetic independently and verify all trained inventories."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO / 'src'))
from kapampangan_morphbpe.serialization import fingerprint,write_json


def naive_bpe(surface,document):
    ranks={(m['left'],m['right']):m['rank'] for m in document['merges']}
    pieces=list(surface)
    while True:
        pairs=[(ranks[(a,b)],a,b) for a,b in zip(pieces,pieces[1:]) if (a,b) in ranks]
        if not pairs:break
        _,left,right=min(pairs)
        merged=[];i=0
        while i<len(pieces):
            if i+1<len(pieces) and (pieces[i],pieces[i+1])==(left,right):
                merged.append(left+right);i+=2
            else:merged.append(pieces[i]);i+=1
        pieces=merged
    return pieces


def counts_from_rows(rows):
    counts=collections.Counter();pred_sets=[];gold_sets=[]
    for row in rows:
        assert ''.join(row['pieces'])==''.join(row['reference'])==row['surface']
        sets=[]
        for parts in [row['pieces'],row['reference']]:
            offset=0;positions=set()
            for part in parts[:-1]:offset+=len(part);positions.add(offset)
            sets.append(positions)
        pred,gold=sets
        local={'tp':len(pred&gold),'fp':len(pred-gold),'fn':len(gold-pred),'exact':row['pieces']==row['reference']}
        assert all(row[k]==v for k,v in local.items())
        counts.update(local)
        pred_sets.append({p for p in row['pieces'] if len(p)>=2})
        gold_sets.append({p for p in row['reference'] if len(p)>=2})
    pair_counts=collections.Counter()
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            same_gold=bool(gold_sets[i]&gold_sets[j]);same_pred=bool(pred_sets[i]&pred_sets[j])
            if same_gold and same_pred:pair_counts['tp']+=1
            elif same_gold:pair_counts['fn']+=1
            elif same_pred:pair_counts['fp']+=1
    counts['boundary_f1']=2*counts['tp']/(2*counts['tp']+counts['fp']+counts['fn'])
    denominator=2*pair_counts['tp']+pair_counts['fp']+pair_counts['fn']
    counts['mcf1']=2*pair_counts['tp']/denominator if denominator else 0
    return counts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results',type=Path,required=True)
    args=parser.parse_args();root=args.results
    report=json.loads((root / 'reports/comparison.json').read_text(encoding='utf-8'))
    assert fingerprint({k:v for k,v in report.items() if k!='report_fingerprint'})==report['report_fingerprint']
    new={n:s for n,s in report['scores'].items() if s['new_augmented_training']}
    assert len(new)==12
    assert {s['vocabulary_size'] for s in new.values()}=={6080,8192,16384}
    assert len({(s['family'],s['vocabulary_size']) for s in new.values()})==12
    cases=0
    for name,score in report['scores'].items():
        path=Path(score['artifact'])
        assert hashlib.sha256((path / 'tokenizer.json').read_bytes()).hexdigest()==score['tokenizer_sha256']
        document=json.loads((path / 'tokenizer.json').read_text(encoding='utf-8'))
        if score['family']=='unigram':
            from tokenizers import Tokenizer
            tok=Tokenizer.from_file(str(path / 'tokenizer.json'))
            encode=lambda word:tok.encode(word).tokens
            assert tok.get_vocab_size()==score['vocabulary_size']
        else:
            # Build pair ranks once; a deliberately simple whole-word encoder
            # verifies the optimized runtime's decisions without importing it.
            ranks={(m['left'],m['right']):m['rank'] for m in document['merges']}
            def encode(word):
                parts=list(word)
                while True:
                    available=[(ranks[(a,b)],a,b) for a,b in zip(parts,parts[1:]) if (a,b) in ranks]
                    if not available:return parts
                    _,a,b=min(available);out=[];i=0
                    while i<len(parts):
                        if i+1<len(parts) and (parts[i],parts[i+1])==(a,b):out.append(a+b);i+=2
                        else:out.append(parts[i]);i+=1
                    parts=out
            assert len(document['vocabulary'])==score['vocabulary_size']
        if score['new_augmented_training']:
            for line in (path / 'checksums.sha256').read_text(encoding='utf-8').splitlines():
                digest,relative=line.split('  ',1)
                assert hashlib.sha256((path / relative).read_bytes()).hexdigest()==digest
            if score['family']=='unigram':
                manifest=json.loads((path / 'unigram-manifest.json').read_text(encoding='utf-8'))
                assert manifest['character_inventory_size']==1588
            else:
                manifest=json.loads((path / 'tokenizer-manifest.json').read_text(encoding='utf-8'))
                assert manifest['protected_boundary_merge_violations']==0
                assert fingerprint({k:v for k,v in manifest.items() if k!='artifact_fingerprint'})==manifest['artifact_fingerprint']
            assert manifest['dataset_fingerprint']==report['augmented_dataset_fingerprint']
        for split in ['dev','test']:
            block=score[split];counts=counts_from_rows(block['predictions'])
            assert len(block['predictions'])==block['rows']
            for key in ['tp','fp','fn','exact']:assert counts[key]==block['counts'][key]
            assert abs(counts['boundary_f1']-block['metrics']['boundary_f1'])<1e-12
            assert abs(counts['mcf1']-block['metrics']['mcf1'])<1e-12
            assert abs(block['metrics']['exact_match']-counts['exact']/block['rows'])<1e-12
            for row in block['predictions']:
                assert encode(row['surface'])==row['pieces'],(name,row['surface'])
                cases+=1
        for c in score['corpus'].values():assert abs(c['word_fertility']-c['word_tokens']/c['word_occurrences'])<1e-12
    for family in ['weighted32','infix_first48','plain']:
        documents=[json.loads((root / 'vocab_grid' / family / f'vocab-{size}/tokenizer.json').read_text(encoding='utf-8')) for size in [6080,8192,16384]]
        for a,b in zip(documents,documents[1:]):
            assert a['vocabulary']==b['vocabulary'][:len(a['vocabulary'])]
            assert a['merges']==b['merges'][:len(a['merges'])]
        if family!='plain':
            single=json.loads((root / 'artifacts' / family / 'tokenizer.json').read_text(encoding='utf-8'))
            assert single['vocabulary']==documents[0]['vocabulary'] and single['merges']==documents[0]['merges']
    rank=lambda n:(new[n]['dev']['metrics']['boundary_f1'],new[n]['dev']['metrics']['exact_match'],-new[n]['dev']['metrics']['fertility'])
    assert sorted(new,key=rank,reverse=True)==report['selection']['ranking']
    assert report['selection']['morphology_test_read_at_selection'] is False
    before=json.loads((REPO / '.cache/tagalog30_comparison/installed_before.json').read_text(encoding='utf-8'))
    assert all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in before.items())
    output={'status':'passed','new_configurations':12,'evaluated_configurations':len(report['scores']),'independently_reencoded_reference_cases':cases,
        'checks':['all trained inventories and augmented identities','all DEV/TEST boundaries, exact matches, F1 and pairwise consistency independently recomputed',
            'BPE decisions independently reencoded by simple pair-rank encoder','all corpus fertility arithmetic','nested BPE vocabulary and merge prefixes',
            'independent6080 training reproduces grid6080 vocabulary and merges','DEV ranking precedes TEST','installed tokenizer and neural checkpoint snapshot unchanged'],
        'installed_files_verified':len(before),'neural_training_or_translation_quality_evaluation':False}
    write_json(root / 'reports/verification.json',output)
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
