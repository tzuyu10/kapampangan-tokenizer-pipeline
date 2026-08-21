# NLLB-200-Distilled-600M vs. local tokenizers (encode-time only)

- NLLB source: `facebook/nllb-200-distilled-600M` @ `f8d333a098d19b4fd9a8b18f94170487ad3f821d` (tokenizer files only, model weights excluded)
- Local vocabulary size: 8192
- Local MorphBPE condition: penalty-4 (not selected; representative mid-grid penalty)
- Unigram ablation: fresh Unigram-LM tokenizer trained on this project's own corpus at matched vocabulary size (8192) -- **not NLLB's tokenizer**; isolates the algorithm effect from NLLB's vocab-size/corpus-exposure confound (see train_unigram_ablation.py)
- NLLB retrained on this corpus: False

Encode-time comparison only; NLLB-200's tokenizer is not retrained on this corpus (this repo has no PAM-Filipino parallel data at the scale needed to retrain or fine-tune it -- see AGENT_CONTEXT.md). Fertility Rate is this project's own T/W formula, computed identically for all four tokenizers. NLLB-200's vocabulary (256,204 entries) is over 30x the local vocabulary (8,192); vocabulary size alone strongly drives fertility, so NLLB's lower fertility must not be read as evidence of better morphological alignment. The 'unigram_ablation' condition (matched vocab, same corpus, same Unigram-LM algorithm family as NLLB, but NOT NLLB's actual tokenizer) exists specifically to isolate that confound: see its 'purpose' field above and reports/nllb-baseline-comparison.md for the interpretation. '*_pieces_equal_*' counts are near-guaranteed to be 0 for NLLB because NLLB draws from an entirely different, much larger vocabulary with a different whitespace convention (Metaspace '▁' prefix vs. this project's literal space pieces); treat them as a sanity check that the vocabularies are incompatible at the string level, not as a segmentation-agreement metric. Do not read any of this as comparable to a downstream BLEU/chrF++ translation evaluation, which remains a separate, unresolved blocker.

**Caveat:** NLLB-200's vocabulary (256,204 entries) is over 30x this project's local vocabulary (8,192). Vocabulary size alone strongly drives Fertility Rate -- a larger vocabulary needs fewer pieces per word regardless of morphological alignment -- so NLLB's lower fertility below must not be read as evidence of better morphological segmentation; the Unigram-ablation column (matched vocab, same corpus, same Unigram-LM algorithm family as NLLB) is what isolates that effect instead.

| input | source | NLLB pieces | NLLB fert. | Unigram-ablation pieces | Unigram fert. | Plain BPE pieces | Plain fert. | MorphBPE pieces | MorphBPE fert. |
|---|---|---|---|---|---|---|---|---|---|
| misamban | fixed_test_sentence | ▁mis + amban | 2.00 | mi + samban | 2.00 | mis + amban | 2.00 | mis + amban | 2.00 |
| Sumulat ako ng tula | fixed_test_sentence | ▁Sum + ulat + ▁ako + ▁ng + ▁tula | 1.25 | Sumul + at + a + ko + ng + tula | 1.50 | Sum + ulat + ako + ng + tula | 1.25 | S + um + ulat + ako + ng + tula | 1.50 |
| Dumalan ka keni. | fixed_test_sentence | ▁Dum + alan + ▁ka + ▁keni + . | 1.33 | Du + malan + ka + keni + . | 1.33 | Dum + alan + ka + keni + . | 1.33 | D + um + alan + ka + keni + . | 1.67 |
| AGKATAN | resegmentation_audit_sample | ▁AG + K + ATA + N | 4.00 | A + G + KA + TAN | 4.00 | A + G + KA + T + AN | 5.00 | A + G + KA + T + AN | 5.00 |
| ALALAYAN | resegmentation_audit_sample | ▁AL + ALA + Y + AN | 4.00 | AL + AL + AYAN | 3.00 | AL + ALA + YAN | 3.00 | A + LA + LA + YAN | 4.00 |
| AUSAN | resegmentation_audit_sample | ▁A + US + AN | 3.00 | A + U + SAN | 3.00 | A + US + AN | 3.00 | A + US + AN | 3.00 |
| Aalma | resegmentation_audit_sample | ▁A + alma | 2.00 | A + al + ma | 3.00 | A + al + ma | 3.00 | A + al + ma | 3.00 |
| Agkatan | resegmentation_audit_sample | ▁Ag + katan | 2.00 | Ag + ka + tan | 3.00 | Ag + kat + an | 3.00 | Ag + ka + tan | 3.00 |
| Agusan | resegmentation_audit_sample | ▁Ag + usan | 2.00 | Agus + an | 2.00 | Ag + usan | 2.00 | Ag + us + an | 3.00 |
| Akakit | resegmentation_audit_sample | ▁Ak + akit | 2.00 | A + kakit | 2.00 | A + ka + kit | 3.00 | A + ka + kit | 3.00 |
| Akitan | resegmentation_audit_sample | ▁Ak + itan | 2.00 | Akit + an | 2.00 | Ak + itan | 2.00 | A + kit + an | 3.00 |
| Alacan | resegmentation_audit_sample | ▁Ala + can | 2.00 | Ala + can | 2.00 | A + lac + an | 3.00 | Ala + can | 2.00 |
| Alala | resegmentation_audit_sample | ▁Ala + la | 2.00 | Ala + la | 2.00 | A + lala | 2.00 | A + lala | 2.00 |
| Alalaya | resegmentation_audit_sample | ▁Ala + laya | 2.00 | Ala + la + ya | 3.00 | A + lala + ya | 3.00 | A + lala + ya | 3.00 |
| Alalayan | resegmentation_audit_sample | ▁Ala + layan | 2.00 | Ala + layan | 2.00 | Al + al + ayan | 3.00 | A + lala + yan | 3.00 |
| Alan | resegmentation_audit_sample | ▁Alan | 1.00 | Al + an | 2.00 | Al + an | 2.00 | Al + an | 2.00 |
| Albuganan | resegmentation_audit_sample | ▁Al + bu + ganan | 3.00 | Albugan + an | 2.00 | Albugan + an | 2.00 | Albug + anan | 2.00 |
| Aminan | resegmentation_audit_sample | ▁Am + inan | 2.00 | A + min + an | 3.00 | A + min + an | 3.00 | Am + in + an | 3.00 |
| Ananang | resegmentation_audit_sample | ▁An + anang | 2.00 | Ana + nang | 2.00 | An + an + ang | 3.00 | A + nan + ang | 3.00 |
| Ananta | resegmentation_audit_sample | ▁An + anta | 2.00 | An + an + ta | 3.00 | An + an + ta | 3.00 | A + nan + ta | 3.00 |
| Aninagan | resegmentation_audit_sample | ▁An + in + agan | 3.00 | A + ni + na + gan | 4.00 | An + in + agan | 3.00 | An + in + agan | 3.00 |
| Apaya | resegmentation_audit_sample | ▁Ap + aya | 2.00 | A + pa + ya | 3.00 | A + paya | 2.00 | A + paya | 2.00 |
| Arena | resegmentation_audit_sample | ▁Arena | 1.00 | A + re + na | 3.00 | Ar + ena | 2.00 | Ar + ena | 2.00 |

## Summary

- Items compared: 23
- Average fertility (NLLB, native pretrained, 256,204 vocab): 2.1558
- Average fertility (Unigram ablation, matched 8192 vocab, this corpus): 2.5145
- Average fertility (Plain BPE, matched 8192 vocab, this corpus): 2.5906
- Average fertility (MorphBPE penalty-4, matched 8192 vocab, this corpus): 2.7029
- Items where NLLB pieces are byte-identical to Plain BPE: 0/23
- Items where NLLB pieces are byte-identical to MorphBPE: 0/23
- Items where NLLB pieces are byte-identical to the Unigram ablation: 0/23

**Isolating the algorithm effect:** the Unigram-ablation row holds vocabulary size, training corpus, character inventory, and special tokens fixed against Plain BPE, changing only the subword algorithm (Unigram-LM, NLLB's family, vs. BPE). If Unigram-ablation's fertility sits close to Plain BPE/MorphBPE (both far above NLLB's), that points to vocabulary size/corpus exposure -- not the Unigram algorithm -- as the main driver of NLLB's lower fertility above.

Fertility Rate = word-subword token count / Unicode word-pretoken count (this project's own formula), computed identically for all four tokenizers. NLLB word attribution is approximated by character-offset overlap against this project's own word-pretoken spans, since NLLB has no native pretoken concept. This is a silver/approximate measurement, not an independent evaluation. The Unigram-ablation tokenizer's training is not verified byte-reproducible across runs (third-party EM trainer); see its artifact manifest.
