# parallel_extraction_v2 -- verified pair set (tiered)

**bible** is the PLOC Kapampangan<->Tagalog religious corpus (verse-aligned) -- the PRIMARY downstream dataset in the thesis proposal; committee translation, formal register, provenance via a groupmate (believed PLOC/DLSU LTL, LGPL -- unconfirmed). **gold_v1** is the 220 user-spot-checked v1 pairs, unchanged. **gold_stories** is native-authored connected narrative. **silver_a/b** are PLD full-pool sweep pairs adjudicated by three non-native passes (LaBSE+lexical sweep, the user's dictionary-alignment script, a Claude read-through). **silver_gemini** is Gemini-generated conversational/news sentences kept only if word-attested and free of flagged un-adapted Tagalog. **Nothing here is native-speaker gold** -- a native-speaker validation pass is still required before any thesis-gold claim. Usable now for Phase 5 as silver.

- **4230 pairs total**: bible 3084, gold_stories 174, gold_v1 220, silver_a 230, silver_b 92, silver_gemini 430
- bible pairs added: 3084
- gemini disposition: {'kept': 430, 'low_attestation': 69, 'tagalog_stoplist': 1, 'dup': 0}
- v2 sweep disposition: {'silver_a': 232, 'silver_b': 93, 'excluded': 516, 'dup_of_gold': 8}

## silver_a / silver_b pairs by PLD unit

| unit | silver_a | silver_b |
|---|---:|---:|
| Utt_News.txt | 112 | 27 |
| Utt_Educ.txt | 26 | 10 |
| Utt_CommonExpressions.txt | 6 | 25 |
| Utt_Medical.txt | 19 | 5 |
| STORY_folktales | 16 | 7 |
| Utt_Interrogatives.txt | 20 | 2 |
| Utt_Greetings.txt | 12 | 4 |
| Utt_Salawikain.txt | 8 | 5 |
| Utt_Essay.txt | 6 | 6 |
| Iso_Ordinal.txt | 3 | 1 |
| Utt_Letter.txt | 2 | 0 |
