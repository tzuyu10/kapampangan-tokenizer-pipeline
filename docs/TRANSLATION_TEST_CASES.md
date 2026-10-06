# Translation test cases

Run each input using both Plain BPE and Morph-BPE, then repeat through Translator A/B. Record the input, selected condition, generated output, source/output token counts, cache flag, latency, and reviewer decision. These are manual test specifications; they have not all been executed.

Functional success means the intended model ran and the UI behaved correctly. Linguistic success requires an approved Filipino reference or bilingual review. Different outputs are allowed; equal outputs are also allowed. Neither model must win every case.

## Linguistic spot checks

The dataset examples below come from the historical kpm_tgl_cleaned.csv test sample. They are supplied references, not independently verified gold. Their held-out status for the currently installed 30-epoch dataset has not been established. Use them for demonstrations, not a new scientific evaluation. Keep test data out of tuning decisions.

| ID | Input | Check |
| --- | --- | --- |
| L01 | Masanting ya ing abak. | Short-sentence meaning and natural Filipino wording; reviewer supplies/approves reference. |
| L02 | nung ikayu pu Dios ko, | Short fragment and politeness; supplied reference: kung kayo po, Diyos ko, |
| L03 | At pangayari nang mekisabi kea, minukiat ya ing Dios ibat kang Abraham. | Sequence of events and name preservation. Supplied reference: At pagkatapos niyang makipag-usap sa kanya, ay umakyat ang Diyos mula kay Abraham. |
| L04 | Uling yang Saresa matbud yang talaga. | Cause, emphasis, and name preservation. Supplied reference: Dahil ang Saresa ay marupok talaga. |
| L05 | At sinabi nang Esau, Atin kung labis-labis, kapatad ku; bandian mu ing keka. | Speaker, direct speech, repetition and punctuation. Supplied reference: At sinabi ni Esau, Mayroon akong sagana, kapatid ko; ariin mo ang iyo. |
| L06 | At milyari king panaun a iti, a linub ya king bale banang daptan ing keang dapat; at karin alalu ding tau king kilub ning bale. | Long input, clause relationships and omissions. Supplied reference: At nangyari nang panahong ito, na pumasok siya sa bahay upang gawin ang kanyang gawain; at wala roon ang mga tao sa loob ng bahay. |
| L07 | Ding anggang bansa a lelangan mu dating la at samba king arapan mu, Oh Guinu. At paligayan de ing laguiu mu. | Multiple sentences; no omitted or invented clause. |
| L08 | King e ku kuma metung a kasinuldan ni metung mang panali ning tapakan ni king nanumang atiu keka, magkang sabian mu, Pepabandian ke i Abram: | Negation, quantities, name and quoted meaning. |
| L09 | Kabang mabie ku purian ke I Jehova: | Time/aspect and culturally appropriate handling of the named entity. Supplied dataset reference uses PANGINOON instead of literal Jehova; a reviewer must decide whether this is acceptable. |
| L10 | A nung ninu ding sinabi, Lasakan ya, lasakan ya, Angga pin king pitatalakaran na. | Repeated instruction and clause completeness; repetition should be evaluated for meaning, not blindly deduplicated. |
| L11 | Pakiramdaman me i Tom. | Everyday instruction and name preservation. Historical reference Paqnggan mo si Tom. contains a suspicious spelling error; obtain a corrected approved reference before scoring. |
| L12 | A validator-approved pair of sentences differing only in a negator, affix, or pronoun | The Filipino meaning should reflect the controlled grammatical change. Use actual approved Kapampangan forms; tokenizer boundaries alone do not establish semantic accuracy. |

## Functional cases

| ID | Input/action | Expected behavior |
| --- | --- | --- |
| F01 | Empty input | Translate/Compare disabled; direct API returns a clear input error. |
| F02 | Spaces/tabs/newlines only | No translation is submitted; direct API rejects it. |
| F03 | Masanting ya ing abak. with leading/trailing spaces and multiple internal spaces | Same normalized source tokens as the single-space version; identical cached output within the running backend. |
| F04 | Same text with decomposed versus composed accented characters | Normalized tokenization agrees; unsupported characters may become UNK. |
| F05 | Masanting ya ing abak. 😀 | No crash; inspect UNK in Show tokens. Evaluate emoji handling separately from linguistic correctness. |
| F06 | A 500-character string | UI permits the character limit; it may still exceed the separate source-token limit and should then show a clear error. |
| F07 | A 501-character request sent directly to the API | Rejected. The UI limits entry to 500 characters. |
| F08 | A source encoding above 256 tokens, within 500 characters | Rejected with the source-token-limit message; no silent truncation. Construct/verify the length using Show tokens. |
| F09 | Run a sentence with Plain BPE, change dropdown to Morph-BPE | Old output/tokens clear; new request uses morph_bpe and its matching tokenizer. |
| F10 | Run Translator A/B | Same source goes to both models; both outputs and process IDs belong to the correct condition. No fabricated outputs. |
| F11 | Run the same model/text twice | Second result is marked cached; output matches. Cache latency is not a speed benchmark. |
| F12 | Edit input after generating output | Old translation/process data clear. |
| F13 | Clear after Show tokens or Translate | Input, output and token display clear. |
| F14 | Expand process sections | Actual tokenization IDs/mask match input; target tokens/IDs match that result. Decoder/encoder explanation is distinguished from measured internal activations. |
| F15 | Copy translation | Copies Filipino output, not the source. A clipboard failure produces a useful message. |
| F16 | Stop backend and retry/check connection | Connection error appears; no fabricated translation. Restart backend to recover. |
| F17 | Submit while a request is pending | No duplicate request from repeated button clicks; loading state and input disabling are consistent. |
| F18 | Inspect at desktop and narrow/mobile widths | Equal desktop columns; Morph-BPE above Plain BPE; readable stacked mobile view; process below; no horizontal overflow. |

## Thesis evaluation

Use the exact dataset hash and saved held-out split for both current bundles, with identical decoding settings. Compute corpus BLEU and chrF++ against approved references and retain metric signatures. Human review should check preserved meaning, grammar, omissions/additions, names/numbers and negation. Add the sentence-level paired analysis required by the manuscript; the web UI and a handful of examples cannot establish significance.

Do not invent absolute pass thresholds or expected exact model strings. The previous integration smoke output for L01 was Plain BPE: Maliwanag ang umaga.; Morph-BPE: Mabilis ang umaga. These are observed outputs, not approved translations.
