# parallel_extraction_v2 -- PLD full-pool alignment (candidate sweep)

Model: `sentence-transformers/LaBSE`. Thresholds: emb_cosine >= 0.62 OR token_jaccard >= 0.3, top-3 FIL per PAM.

**Every row is a CANDIDATE for human review, not a verified pair.** Same discipline as parallel_extraction_v1: nothing here enters a dataset until reviewed. `mutual_best` (reciprocal nearest neighbour) is the highest-precision subset; `emb_cosine >= 0.80` is a strong secondary signal.

- candidate rows: **849**
- of which mutual-best: **314**
- of which emb_cosine >= 0.80: **154**

| unit | PAM | FIL | candidates | mutual-best |
|---|---:|---:|---:|---:|
| Iso_Kinship.txt | 10 | 2 | 1 | 1 |
| Iso_MinPairs.txt | 22 | 56 | 10 | 4 |
| Iso_Ordinal.txt | 41 | 30 | 24 | 4 |
| Iso_Time.txt | 5 | 1 | 0 | 0 |
| Iso_Weather.txt | 4 | 4 | 5 | 3 |
| Utt_CommonExpressions.txt | 96 | 95 | 100 | 11 |
| Utt_Educ.txt | 318 | 351 | 92 | 39 |
| Utt_Essay.txt | 124 | 139 | 16 | 12 |
| Utt_Greetings.txt | 78 | 77 | 68 | 13 |
| Utt_Interrogatives.txt | 82 | 77 | 132 | 28 |
| Utt_Letter.txt | 34 | 54 | 3 | 2 |
| Utt_Medical.txt | 136 | 127 | 90 | 25 |
| Utt_News.txt | 325 | 360 | 246 | 135 |
| Utt_Salawikain.txt | 141 | 159 | 16 | 11 |
| STORY_folktales(PAM 5 files vs FIL Utt_Story.txt) | 190 | 193 | 46 | 26 |
