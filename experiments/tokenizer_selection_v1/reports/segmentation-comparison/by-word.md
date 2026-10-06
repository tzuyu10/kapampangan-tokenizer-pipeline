# v4 tokenizer segmentation - side by side

49 words, 25 candidates. `silver_gold` is the held-out reference used by Phase 3 selection - **silver, not native gold**. `==` marks an exact whole-word match.

## `kabukasan`  ((flagship, no ref gold), tier (custom))

**silver gold:** `kabukasan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kab+u+kasan` |  | 3 |
| plain@8192 | `kabu+kasan` |  | 2 |
| plain@16384 | `kabukasan` | OK | 1 |
| morphbpe@6080 | `ka+bukas+an` |  | 3 |
| morphbpe@8192 | `ka+bukas+an` |  | 3 |
| morphbpe@16384 | `ka+bukas+an` |  | 3 |
| penalty-1@6080 | `ka+bukas+an` |  | 3 |
| penalty-1@8192 | `ka+bukas+an` |  | 3 |
| penalty-1@16384 | `ka+bukas+an` |  | 3 |
| penalty-2@6080 | `ka+bukas+an` |  | 3 |
| penalty-2@8192 | `ka+bukas+an` |  | 3 |
| penalty-2@16384 | `ka+bukas+an` |  | 3 |
| penalty-4@6080 | `ka+bukas+an` |  | 3 |
| penalty-4@8192 | `ka+bukas+an` |  | 3 |
| penalty-4@16384 | `ka+bukas+an` |  | 3 |
| penalty-8@6080 | `ka+bukas+an` |  | 3 |
| penalty-8@8192 | `ka+bukas+an` |  | 3 |
| penalty-8@16384 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+bukas+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+bukas+an` |  | 3 |
| unigram-ablation@6080 | `ka+bukas+an` |  | 3 |

## `magpakalma`  ((flagship, no ref gold), tier (custom))

**silver gold:** `magpakalma`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+pakal+ma` |  | 3 |
| plain@8192 | `mag+pakal+ma` |  | 3 |
| plain@16384 | `mag+pakal+ma` |  | 3 |
| morphbpe@6080 | `mag+pakal+ma` |  | 3 |
| morphbpe@8192 | `mag+pakal+ma` |  | 3 |
| morphbpe@16384 | `mag+pakal+ma` |  | 3 |
| penalty-1@6080 | `mag+pakal+ma` |  | 3 |
| penalty-1@8192 | `mag+pakal+ma` |  | 3 |
| penalty-1@16384 | `mag+pakal+ma` |  | 3 |
| penalty-2@6080 | `magpa+kal+ma` |  | 3 |
| penalty-2@8192 | `magpa+kalma` |  | 2 |
| penalty-2@16384 | `magpa+kalma` |  | 2 |
| penalty-4@6080 | `magpa+kal+ma` |  | 3 |
| penalty-4@8192 | `magpa+kalma` |  | 2 |
| penalty-4@16384 | `magpa+kalma` |  | 2 |
| penalty-8@6080 | `magpa+kal+ma` |  | 3 |
| penalty-8@8192 | `magpa+kalma` |  | 2 |
| penalty-8@16384 | `magpa+kalma` |  | 2 |
| stochastic-p4-d0.1@6080 | `magpa+kal+ma` |  | 3 |
| stochastic-p4-d0.1@8192 | `magpa+kalma` |  | 2 |
| stochastic-p4-d0.1@16384 | `magpa+kalma` |  | 2 |
| stochastic-p4-d0.2@6080 | `mag+pakal+ma` |  | 3 |
| stochastic-p4-d0.2@8192 | `mag+pakal+ma` |  | 3 |
| stochastic-p4-d0.2@16384 | `mag+pakal+ma` |  | 3 |
| unigram-ablation@6080 | `magpa+kal+ma` |  | 3 |

## `mekipagapir`  ((flagship, no ref gold), tier (custom))

**silver gold:** `mekipagapir`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mek+ipag+ap+ir` |  | 4 |
| plain@8192 | `mek+ipag+ap+ir` |  | 4 |
| plain@16384 | `mek+ipag+ap+ir` |  | 4 |
| morphbpe@6080 | `mek+ipag+ap+ir` |  | 4 |
| morphbpe@8192 | `mek+ipag+ap+ir` |  | 4 |
| morphbpe@16384 | `mek+ipag+ap+ir` |  | 4 |
| penalty-1@6080 | `mek+ipag+ap+ir` |  | 4 |
| penalty-1@8192 | `mek+ipag+ap+ir` |  | 4 |
| penalty-1@16384 | `mek+ipag+ap+ir` |  | 4 |
| penalty-2@6080 | `meki+pag+ap+ir` |  | 4 |
| penalty-2@8192 | `meki+pag+ap+ir` |  | 4 |
| penalty-2@16384 | `meki+pag+ap+ir` |  | 4 |
| penalty-4@6080 | `meki+pag+ap+ir` |  | 4 |
| penalty-4@8192 | `meki+pag+ap+ir` |  | 4 |
| penalty-4@16384 | `meki+pag+ap+ir` |  | 4 |
| penalty-8@6080 | `meki+paga+pi+r` |  | 4 |
| penalty-8@8192 | `meki+paga+pir` |  | 3 |
| penalty-8@16384 | `meki+paga+pir` |  | 3 |
| stochastic-p4-d0.1@6080 | `meki+paga+pir` |  | 3 |
| stochastic-p4-d0.1@8192 | `meki+paga+pir` |  | 3 |
| stochastic-p4-d0.1@16384 | `meki+paga+pir` |  | 3 |
| stochastic-p4-d0.2@6080 | `meki+paga+pi+r` |  | 4 |
| stochastic-p4-d0.2@8192 | `meki+paga+pi+r` |  | 4 |
| stochastic-p4-d0.2@16384 | `meki+paga+pir` |  | 3 |
| unigram-ablation@6080 | `meki+pag+api+r` |  | 4 |

## `misamban`  ((flagship, no ref gold), tier (custom))

**silver gold:** `misamban`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mis+amban` |  | 2 |
| plain@8192 | `mis+amban` |  | 2 |
| plain@16384 | `mis+amban` |  | 2 |
| morphbpe@6080 | `mis+amban` |  | 2 |
| morphbpe@8192 | `mis+amban` |  | 2 |
| morphbpe@16384 | `mis+amban` |  | 2 |
| penalty-1@6080 | `mis+amban` |  | 2 |
| penalty-1@8192 | `mis+amban` |  | 2 |
| penalty-1@16384 | `mis+amban` |  | 2 |
| penalty-2@6080 | `mis+amban` |  | 2 |
| penalty-2@8192 | `mis+amban` |  | 2 |
| penalty-2@16384 | `mis+amban` |  | 2 |
| penalty-4@6080 | `mis+amban` |  | 2 |
| penalty-4@8192 | `mis+amban` |  | 2 |
| penalty-4@16384 | `mis+amban` |  | 2 |
| penalty-8@6080 | `mi+sam+ban` |  | 3 |
| penalty-8@8192 | `mi+sam+ban` |  | 3 |
| penalty-8@16384 | `mi+sam+ban` |  | 3 |
| stochastic-p4-d0.1@6080 | `mis+amban` |  | 2 |
| stochastic-p4-d0.1@8192 | `mis+amban` |  | 2 |
| stochastic-p4-d0.1@16384 | `mis+amban` |  | 2 |
| stochastic-p4-d0.2@6080 | `mi+sam+ban` |  | 3 |
| stochastic-p4-d0.2@8192 | `mi+sam+ban` |  | 3 |
| stochastic-p4-d0.2@16384 | `mi+sam+ban` |  | 3 |
| unigram-ablation@6080 | `mi+samban` |  | 2 |

## `pemalagyu`  ((flagship, no ref gold), tier (custom))

**silver gold:** `pemalagyu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pem+alag+yu` |  | 3 |
| plain@8192 | `pem+alag+yu` |  | 3 |
| plain@16384 | `pem+alagyu` |  | 2 |
| morphbpe@6080 | `pem+alag+yu` |  | 3 |
| morphbpe@8192 | `pem+alag+yu` |  | 3 |
| morphbpe@16384 | `pem+alag+yu` |  | 3 |
| penalty-1@6080 | `pem+alag+yu` |  | 3 |
| penalty-1@8192 | `pem+alag+yu` |  | 3 |
| penalty-1@16384 | `pem+alag+yu` |  | 3 |
| penalty-2@6080 | `pem+alag+yu` |  | 3 |
| penalty-2@8192 | `pem+alag+yu` |  | 3 |
| penalty-2@16384 | `pem+alag+yu` |  | 3 |
| penalty-4@6080 | `pem+alag+yu` |  | 3 |
| penalty-4@8192 | `pem+alag+yu` |  | 3 |
| penalty-4@16384 | `pem+alag+yu` |  | 3 |
| penalty-8@6080 | `pe+ma+lagyu` |  | 3 |
| penalty-8@8192 | `pe+ma+lagyu` |  | 3 |
| penalty-8@16384 | `pema+lagyu` |  | 2 |
| stochastic-p4-d0.1@6080 | `pe+ma+lagyu` |  | 3 |
| stochastic-p4-d0.1@8192 | `pe+ma+lagyu` |  | 3 |
| stochastic-p4-d0.1@16384 | `pema+lagyu` |  | 2 |
| stochastic-p4-d0.2@6080 | `pe+ma+lagyu` |  | 3 |
| stochastic-p4-d0.2@8192 | `pe+ma+lagyu` |  | 3 |
| stochastic-p4-d0.2@16384 | `pe+ma+lagyu` |  | 3 |
| unigram-ablation@6080 | `pe+ma+lagyu` |  | 3 |

## `sumulat`  ((flagship, no ref gold), tier (custom))

**silver gold:** `sumulat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sum+ulat` |  | 2 |
| plain@8192 | `sum+ulat` |  | 2 |
| plain@16384 | `sumulat` | OK | 1 |
| morphbpe@6080 | `sum+ulat` |  | 2 |
| morphbpe@8192 | `sum+ulat` |  | 2 |
| morphbpe@16384 | `sum+ulat` |  | 2 |
| penalty-1@6080 | `s+um+ulat` |  | 3 |
| penalty-1@8192 | `s+um+ulat` |  | 3 |
| penalty-1@16384 | `s+um+ulat` |  | 3 |
| penalty-2@6080 | `s+um+ulat` |  | 3 |
| penalty-2@8192 | `s+um+ulat` |  | 3 |
| penalty-2@16384 | `s+um+ulat` |  | 3 |
| penalty-4@6080 | `s+um+ulat` |  | 3 |
| penalty-4@8192 | `s+um+ulat` |  | 3 |
| penalty-4@16384 | `s+um+ulat` |  | 3 |
| penalty-8@6080 | `su+mu+lat` |  | 3 |
| penalty-8@8192 | `sumu+lat` |  | 2 |
| penalty-8@16384 | `sumu+lat` |  | 2 |
| stochastic-p4-d0.1@6080 | `su+mu+lat` |  | 3 |
| stochastic-p4-d0.1@8192 | `su+mu+lat` |  | 3 |
| stochastic-p4-d0.1@16384 | `sumu+lat` |  | 2 |
| stochastic-p4-d0.2@6080 | `su+mu+lat` |  | 3 |
| stochastic-p4-d0.2@8192 | `sumu+lat` |  | 2 |
| stochastic-p4-d0.2@16384 | `sumu+lat` |  | 2 |
| unigram-ablation@6080 | `sumul+at` |  | 2 |

## `pabustan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+bust+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pabustan` |  | 1 |
| plain@8192 | `pabustan` |  | 1 |
| plain@16384 | `pabustan` |  | 1 |
| morphbpe@6080 | `pabustan` |  | 1 |
| morphbpe@8192 | `pabustan` |  | 1 |
| morphbpe@16384 | `pabustan` |  | 1 |
| penalty-1@6080 | `pabustan` |  | 1 |
| penalty-1@8192 | `pabustan` |  | 1 |
| penalty-1@16384 | `pabustan` |  | 1 |
| penalty-2@6080 | `pabustan` |  | 1 |
| penalty-2@8192 | `pabustan` |  | 1 |
| penalty-2@16384 | `pabustan` |  | 1 |
| penalty-4@6080 | `pabustan` |  | 1 |
| penalty-4@8192 | `pabustan` |  | 1 |
| penalty-4@16384 | `pabustan` |  | 1 |
| penalty-8@6080 | `pabustan` |  | 1 |
| penalty-8@8192 | `pabustan` |  | 1 |
| penalty-8@16384 | `pabustan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pabustan` |  | 1 |
| stochastic-p4-d0.1@8192 | `pabustan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pabustan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pabustan` |  | 1 |
| stochastic-p4-d0.2@8192 | `pabustan` |  | 1 |
| stochastic-p4-d0.2@16384 | `pabustan` |  | 1 |
| unigram-ablation@6080 | `pabustan` |  | 1 |

## `kaluguran`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+lugur+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kaluguran` |  | 1 |
| plain@8192 | `kaluguran` |  | 1 |
| plain@16384 | `kaluguran` |  | 1 |
| morphbpe@6080 | `kaluguran` |  | 1 |
| morphbpe@8192 | `kaluguran` |  | 1 |
| morphbpe@16384 | `kaluguran` |  | 1 |
| penalty-1@6080 | `kaluguran` |  | 1 |
| penalty-1@8192 | `kaluguran` |  | 1 |
| penalty-1@16384 | `kaluguran` |  | 1 |
| penalty-2@6080 | `kaluguran` |  | 1 |
| penalty-2@8192 | `kaluguran` |  | 1 |
| penalty-2@16384 | `kaluguran` |  | 1 |
| penalty-4@6080 | `kaluguran` |  | 1 |
| penalty-4@8192 | `kaluguran` |  | 1 |
| penalty-4@16384 | `kaluguran` |  | 1 |
| penalty-8@6080 | `kaluguran` |  | 1 |
| penalty-8@8192 | `kaluguran` |  | 1 |
| penalty-8@16384 | `kaluguran` |  | 1 |
| stochastic-p4-d0.1@6080 | `kaluguran` |  | 1 |
| stochastic-p4-d0.1@8192 | `kaluguran` |  | 1 |
| stochastic-p4-d0.1@16384 | `kaluguran` |  | 1 |
| stochastic-p4-d0.2@6080 | `kaluguran` |  | 1 |
| stochastic-p4-d0.2@8192 | `kaluguran` |  | 1 |
| stochastic-p4-d0.2@16384 | `kaluguran` |  | 1 |
| unigram-ablation@6080 | `kaluguran` |  | 1 |

## `kailangan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+ilang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kailangan` |  | 1 |
| plain@8192 | `kailangan` |  | 1 |
| plain@16384 | `kailangan` |  | 1 |
| morphbpe@6080 | `kailangan` |  | 1 |
| morphbpe@8192 | `kailangan` |  | 1 |
| morphbpe@16384 | `kailangan` |  | 1 |
| penalty-1@6080 | `kailangan` |  | 1 |
| penalty-1@8192 | `kailangan` |  | 1 |
| penalty-1@16384 | `kailangan` |  | 1 |
| penalty-2@6080 | `kailangan` |  | 1 |
| penalty-2@8192 | `kailangan` |  | 1 |
| penalty-2@16384 | `kailangan` |  | 1 |
| penalty-4@6080 | `kailangan` |  | 1 |
| penalty-4@8192 | `kailangan` |  | 1 |
| penalty-4@16384 | `kailangan` |  | 1 |
| penalty-8@6080 | `kailangan` |  | 1 |
| penalty-8@8192 | `kailangan` |  | 1 |
| penalty-8@16384 | `kailangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kailangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kailangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kailangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kailangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kailangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kailangan` |  | 1 |
| unigram-ablation@6080 | `kailangan` |  | 1 |

## `kapulungan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+pulung+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+ulungan` |  | 2 |
| plain@8192 | `kap+ulungan` |  | 2 |
| plain@16384 | `kapulungan` |  | 1 |
| morphbpe@6080 | `kap+ulungan` |  | 2 |
| morphbpe@8192 | `kapulungan` |  | 1 |
| morphbpe@16384 | `kapulungan` |  | 1 |
| penalty-1@6080 | `kap+ulungan` |  | 2 |
| penalty-1@8192 | `kapulungan` |  | 1 |
| penalty-1@16384 | `kapulungan` |  | 1 |
| penalty-2@6080 | `kap+ulungan` |  | 2 |
| penalty-2@8192 | `kapulungan` |  | 1 |
| penalty-2@16384 | `kapulungan` |  | 1 |
| penalty-4@6080 | `kap+ulung+an` |  | 3 |
| penalty-4@8192 | `kapulungan` |  | 1 |
| penalty-4@16384 | `kapulungan` |  | 1 |
| penalty-8@6080 | `kap+ulung+an` |  | 3 |
| penalty-8@8192 | `kapulungan` |  | 1 |
| penalty-8@16384 | `kapulungan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kap+ulung+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapulungan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapulungan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kap+ulungan` |  | 2 |
| stochastic-p4-d0.2@8192 | `kap+ulungan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kapulungan` |  | 1 |
| unigram-ablation@6080 | `kapulungan` |  | 1 |

## `kapalaran`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+palar+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+al+aran` |  | 3 |
| plain@8192 | `kapal+aran` |  | 2 |
| plain@16384 | `kapal+aran` |  | 2 |
| morphbpe@6080 | `kapal+aran` |  | 2 |
| morphbpe@8192 | `kapal+aran` |  | 2 |
| morphbpe@16384 | `kapal+aran` |  | 2 |
| penalty-1@6080 | `ka+pal+aran` |  | 3 |
| penalty-1@8192 | `kapal+aran` |  | 2 |
| penalty-1@16384 | `kapal+aran` |  | 2 |
| penalty-2@6080 | `ka+pal+aran` |  | 3 |
| penalty-2@8192 | `kapal+aran` |  | 2 |
| penalty-2@16384 | `kapal+aran` |  | 2 |
| penalty-4@6080 | `ka+pal+aran` |  | 3 |
| penalty-4@8192 | `ka+pal+aran` |  | 3 |
| penalty-4@16384 | `kapal+aran` |  | 2 |
| penalty-8@6080 | `ka+pala+ran` |  | 3 |
| penalty-8@8192 | `ka+pala+ran` |  | 3 |
| penalty-8@16384 | `ka+palaran` |  | 2 |
| stochastic-p4-d0.1@6080 | `kapa+la+ran` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapa+la+ran` |  | 3 |
| stochastic-p4-d0.1@16384 | `kapa+la+ran` |  | 3 |
| stochastic-p4-d0.2@6080 | `kapa+la+ran` |  | 3 |
| stochastic-p4-d0.2@8192 | `kapa+la+ran` |  | 3 |
| stochastic-p4-d0.2@16384 | `kapa+laran` |  | 2 |
| unigram-ablation@6080 | `ka+pala+ran` |  | 3 |

## `kalaganapan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+laganap+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+agan+apan` |  | 3 |
| plain@8192 | `kal+agan+apan` |  | 3 |
| plain@16384 | `kal+agan+apan` |  | 3 |
| morphbpe@6080 | `kal+agan+apan` |  | 3 |
| morphbpe@8192 | `kal+agan+apan` |  | 3 |
| morphbpe@16384 | `kal+agan+apan` |  | 3 |
| penalty-1@6080 | `kal+agan+apan` |  | 3 |
| penalty-1@8192 | `kal+agan+apan` |  | 3 |
| penalty-1@16384 | `kal+agan+apan` |  | 3 |
| penalty-2@6080 | `kal+agan+apan` |  | 3 |
| penalty-2@8192 | `kal+agan+apan` |  | 3 |
| penalty-2@16384 | `kalagan+apan` |  | 2 |
| penalty-4@6080 | `kala+gan+apan` |  | 3 |
| penalty-4@8192 | `kala+gan+apan` |  | 3 |
| penalty-4@16384 | `kalagan+apan` |  | 2 |
| penalty-8@6080 | `ka+lag+ana+pan` |  | 4 |
| penalty-8@8192 | `ka+lag+ana+pan` |  | 4 |
| penalty-8@16384 | `ka+lag+ana+pan` |  | 4 |
| stochastic-p4-d0.1@6080 | `kala+gan+apan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kala+gan+apan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kala+gan+apan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+lag+ana+p+an` |  | 5 |
| stochastic-p4-d0.2@8192 | `ka+lag+anap+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `ka+lag+anap+an` |  | 4 |
| unigram-ablation@6080 | `ka+la+ganap+an` |  | 4 |

## `sinabi`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+abi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinabi` |  | 1 |
| plain@8192 | `sinabi` |  | 1 |
| plain@16384 | `sinabi` |  | 1 |
| morphbpe@6080 | `sin+abi` |  | 2 |
| morphbpe@8192 | `sin+abi` |  | 2 |
| morphbpe@16384 | `sin+abi` |  | 2 |
| penalty-1@6080 | `s+in+abi` | OK | 3 |
| penalty-1@8192 | `s+in+abi` | OK | 3 |
| penalty-1@16384 | `s+in+abi` | OK | 3 |
| penalty-2@6080 | `s+in+abi` | OK | 3 |
| penalty-2@8192 | `s+in+abi` | OK | 3 |
| penalty-2@16384 | `s+in+abi` | OK | 3 |
| penalty-4@6080 | `s+in+abi` | OK | 3 |
| penalty-4@8192 | `s+in+abi` | OK | 3 |
| penalty-4@16384 | `s+in+abi` | OK | 3 |
| penalty-8@6080 | `s+in+abi` | OK | 3 |
| penalty-8@8192 | `s+in+abi` | OK | 3 |
| penalty-8@16384 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.1@6080 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.1@8192 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.1@16384 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.2@6080 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.2@8192 | `s+in+abi` | OK | 3 |
| stochastic-p4-d0.2@16384 | `s+in+abi` | OK | 3 |
| unigram-ablation@6080 | `sinabi` |  | 1 |

## `minuna`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `m+in+una`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `minuna` |  | 1 |
| plain@8192 | `minuna` |  | 1 |
| plain@16384 | `minuna` |  | 1 |
| morphbpe@6080 | `minuna` |  | 1 |
| morphbpe@8192 | `minuna` |  | 1 |
| morphbpe@16384 | `minuna` |  | 1 |
| penalty-1@6080 | `minuna` |  | 1 |
| penalty-1@8192 | `minuna` |  | 1 |
| penalty-1@16384 | `minuna` |  | 1 |
| penalty-2@6080 | `minuna` |  | 1 |
| penalty-2@8192 | `minuna` |  | 1 |
| penalty-2@16384 | `minuna` |  | 1 |
| penalty-4@6080 | `minuna` |  | 1 |
| penalty-4@8192 | `minuna` |  | 1 |
| penalty-4@16384 | `minuna` |  | 1 |
| penalty-8@6080 | `minuna` |  | 1 |
| penalty-8@8192 | `minuna` |  | 1 |
| penalty-8@16384 | `minuna` |  | 1 |
| stochastic-p4-d0.1@6080 | `minuna` |  | 1 |
| stochastic-p4-d0.1@8192 | `minuna` |  | 1 |
| stochastic-p4-d0.1@16384 | `minuna` |  | 1 |
| stochastic-p4-d0.2@6080 | `minuna` |  | 1 |
| stochastic-p4-d0.2@8192 | `minuna` |  | 1 |
| stochastic-p4-d0.2@16384 | `minuna` |  | 1 |
| unigram-ablation@6080 | `minuna` |  | 1 |

## `kinuldas`  (infixation, tier A_strong_silver)

**silver gold:** `k+in+uldas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kinul+das` |  | 2 |
| plain@8192 | `kinul+das` |  | 2 |
| plain@16384 | `kinuldas` |  | 1 |
| morphbpe@6080 | `kin+ul+das` |  | 3 |
| morphbpe@8192 | `kin+uldas` |  | 2 |
| morphbpe@16384 | `kin+uldas` |  | 2 |
| penalty-1@6080 | `kin+ul+das` |  | 3 |
| penalty-1@8192 | `kin+uldas` |  | 2 |
| penalty-1@16384 | `kin+uldas` |  | 2 |
| penalty-2@6080 | `k+in+ul+das` |  | 4 |
| penalty-2@8192 | `k+in+uldas` | OK | 3 |
| penalty-2@16384 | `k+in+uldas` | OK | 3 |
| penalty-4@6080 | `k+in+ul+das` |  | 4 |
| penalty-4@8192 | `k+in+uldas` | OK | 3 |
| penalty-4@16384 | `k+in+uldas` | OK | 3 |
| penalty-8@6080 | `k+in+ul+das` |  | 4 |
| penalty-8@8192 | `k+in+uldas` | OK | 3 |
| penalty-8@16384 | `k+in+uldas` | OK | 3 |
| stochastic-p4-d0.1@6080 | `k+in+ul+das` |  | 4 |
| stochastic-p4-d0.1@8192 | `k+in+uldas` | OK | 3 |
| stochastic-p4-d0.1@16384 | `k+in+uldas` | OK | 3 |
| stochastic-p4-d0.2@6080 | `k+in+ul+das` |  | 4 |
| stochastic-p4-d0.2@8192 | `k+in+uldas` | OK | 3 |
| stochastic-p4-d0.2@16384 | `k+in+uldas` | OK | 3 |
| unigram-ablation@6080 | `kin+uldas` |  | 2 |

## `sinulat`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+ulat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinulat` |  | 1 |
| plain@8192 | `sinulat` |  | 1 |
| plain@16384 | `sinulat` |  | 1 |
| morphbpe@6080 | `sin+ulat` |  | 2 |
| morphbpe@8192 | `sin+ulat` |  | 2 |
| morphbpe@16384 | `sin+ulat` |  | 2 |
| penalty-1@6080 | `s+in+ulat` | OK | 3 |
| penalty-1@8192 | `s+in+ulat` | OK | 3 |
| penalty-1@16384 | `s+in+ulat` | OK | 3 |
| penalty-2@6080 | `s+in+ulat` | OK | 3 |
| penalty-2@8192 | `s+in+ulat` | OK | 3 |
| penalty-2@16384 | `s+in+ulat` | OK | 3 |
| penalty-4@6080 | `s+in+ulat` | OK | 3 |
| penalty-4@8192 | `s+in+ulat` | OK | 3 |
| penalty-4@16384 | `s+in+ulat` | OK | 3 |
| penalty-8@6080 | `s+in+ulat` | OK | 3 |
| penalty-8@8192 | `s+in+ulat` | OK | 3 |
| penalty-8@16384 | `s+in+ulat` | OK | 3 |
| stochastic-p4-d0.1@6080 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.1@8192 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.1@16384 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@6080 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@8192 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@16384 | `sinu+lat` |  | 2 |
| unigram-ablation@6080 | `sinulat` |  | 1 |

## `sumuyu`  (infixation, tier B_moderate_silver)

**silver gold:** `s+um+uyu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `su+mu+yu` |  | 3 |
| plain@8192 | `sumu+yu` |  | 2 |
| plain@16384 | `sumuyu` |  | 1 |
| morphbpe@6080 | `su+mu+yu` |  | 3 |
| morphbpe@8192 | `sumu+yu` |  | 2 |
| morphbpe@16384 | `sumuyu` |  | 1 |
| penalty-1@6080 | `su+mu+yu` |  | 3 |
| penalty-1@8192 | `sumu+yu` |  | 2 |
| penalty-1@16384 | `sumuyu` |  | 1 |
| penalty-2@6080 | `su+mu+yu` |  | 3 |
| penalty-2@8192 | `sumu+yu` |  | 2 |
| penalty-2@16384 | `sumuyu` |  | 1 |
| penalty-4@6080 | `su+mu+yu` |  | 3 |
| penalty-4@8192 | `sumu+yu` |  | 2 |
| penalty-4@16384 | `sumuyu` |  | 1 |
| penalty-8@6080 | `su+mu+yu` |  | 3 |
| penalty-8@8192 | `sumu+yu` |  | 2 |
| penalty-8@16384 | `sumuyu` |  | 1 |
| stochastic-p4-d0.1@6080 | `su+mu+yu` |  | 3 |
| stochastic-p4-d0.1@8192 | `su+mu+yu` |  | 3 |
| stochastic-p4-d0.1@16384 | `sumuyu` |  | 1 |
| stochastic-p4-d0.2@6080 | `su+mu+yu` |  | 3 |
| stochastic-p4-d0.2@8192 | `sumu+yu` |  | 2 |
| stochastic-p4-d0.2@16384 | `sumuyu` |  | 1 |
| unigram-ablation@6080 | `sumuyu` |  | 1 |

## `pinatubu`  (infixation, tier B_moderate_silver)

**silver gold:** `p+in+atubu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pin+at+ubu` |  | 3 |
| plain@8192 | `pin+at+ubu` |  | 3 |
| plain@16384 | `pin+at+ubu` |  | 3 |
| morphbpe@6080 | `pin+at+ubu` |  | 3 |
| morphbpe@8192 | `pin+at+ubu` |  | 3 |
| morphbpe@16384 | `pin+at+ubu` |  | 3 |
| penalty-1@6080 | `pin+at+ubu` |  | 3 |
| penalty-1@8192 | `pin+at+ubu` |  | 3 |
| penalty-1@16384 | `pin+at+ubu` |  | 3 |
| penalty-2@6080 | `pin+at+ubu` |  | 3 |
| penalty-2@8192 | `pin+at+ubu` |  | 3 |
| penalty-2@16384 | `pin+at+ubu` |  | 3 |
| penalty-4@6080 | `pin+atu+bu` |  | 3 |
| penalty-4@8192 | `pin+atu+bu` |  | 3 |
| penalty-4@16384 | `pin+atubu` |  | 2 |
| penalty-8@6080 | `pin+atu+bu` |  | 3 |
| penalty-8@8192 | `pin+atu+bu` |  | 3 |
| penalty-8@16384 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.1@6080 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.1@8192 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.1@16384 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.2@6080 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.2@8192 | `pin+atu+bu` |  | 3 |
| stochastic-p4-d0.2@16384 | `pin+atu+bu` |  | 3 |
| unigram-ablation@6080 | `pin+a+tubu` |  | 3 |

## `lingap`  (infixation, tier B_moderate_silver)

**silver gold:** `l+in+gap`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ling+ap` |  | 2 |
| plain@8192 | `lingap` |  | 1 |
| plain@16384 | `lingap` |  | 1 |
| morphbpe@6080 | `ling+ap` |  | 2 |
| morphbpe@8192 | `lingap` |  | 1 |
| morphbpe@16384 | `lingap` |  | 1 |
| penalty-1@6080 | `ling+ap` |  | 2 |
| penalty-1@8192 | `lingap` |  | 1 |
| penalty-1@16384 | `lingap` |  | 1 |
| penalty-2@6080 | `ling+ap` |  | 2 |
| penalty-2@8192 | `lingap` |  | 1 |
| penalty-2@16384 | `lingap` |  | 1 |
| penalty-4@6080 | `ling+ap` |  | 2 |
| penalty-4@8192 | `lingap` |  | 1 |
| penalty-4@16384 | `lingap` |  | 1 |
| penalty-8@6080 | `ling+ap` |  | 2 |
| penalty-8@8192 | `lingap` |  | 1 |
| penalty-8@16384 | `lingap` |  | 1 |
| stochastic-p4-d0.1@6080 | `li+ng+ap` |  | 3 |
| stochastic-p4-d0.1@8192 | `lingap` |  | 1 |
| stochastic-p4-d0.1@16384 | `lingap` |  | 1 |
| stochastic-p4-d0.2@6080 | `li+ng+ap` |  | 3 |
| stochastic-p4-d0.2@8192 | `lingap` |  | 1 |
| stochastic-p4-d0.2@16384 | `lingap` |  | 1 |
| unigram-ablation@6080 | `lingap` |  | 1 |

## `maguing`  (prefixation, tier B_moderate_silver)

**silver gold:** `mag+uing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `maguing` |  | 1 |
| plain@8192 | `maguing` |  | 1 |
| plain@16384 | `maguing` |  | 1 |
| morphbpe@6080 | `maguing` |  | 1 |
| morphbpe@8192 | `maguing` |  | 1 |
| morphbpe@16384 | `maguing` |  | 1 |
| penalty-1@6080 | `maguing` |  | 1 |
| penalty-1@8192 | `maguing` |  | 1 |
| penalty-1@16384 | `maguing` |  | 1 |
| penalty-2@6080 | `maguing` |  | 1 |
| penalty-2@8192 | `maguing` |  | 1 |
| penalty-2@16384 | `maguing` |  | 1 |
| penalty-4@6080 | `maguing` |  | 1 |
| penalty-4@8192 | `maguing` |  | 1 |
| penalty-4@16384 | `maguing` |  | 1 |
| penalty-8@6080 | `maguing` |  | 1 |
| penalty-8@8192 | `maguing` |  | 1 |
| penalty-8@16384 | `maguing` |  | 1 |
| stochastic-p4-d0.1@6080 | `maguing` |  | 1 |
| stochastic-p4-d0.1@8192 | `maguing` |  | 1 |
| stochastic-p4-d0.1@16384 | `maguing` |  | 1 |
| stochastic-p4-d0.2@6080 | `maguing` |  | 1 |
| stochastic-p4-d0.2@8192 | `maguing` |  | 1 |
| stochastic-p4-d0.2@16384 | `maguing` |  | 1 |
| unigram-ablation@6080 | `maguing` |  | 1 |

## `malugud`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lugud`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malugud` |  | 1 |
| plain@8192 | `malugud` |  | 1 |
| plain@16384 | `malugud` |  | 1 |
| morphbpe@6080 | `mal+ugud` |  | 2 |
| morphbpe@8192 | `mal+ugud` |  | 2 |
| morphbpe@16384 | `mal+ugud` |  | 2 |
| penalty-1@6080 | `mal+ugud` |  | 2 |
| penalty-1@8192 | `mal+ugud` |  | 2 |
| penalty-1@16384 | `mal+ugud` |  | 2 |
| penalty-2@6080 | `mal+ugud` |  | 2 |
| penalty-2@8192 | `mal+ugud` |  | 2 |
| penalty-2@16384 | `mal+ugud` |  | 2 |
| penalty-4@6080 | `mal+ugud` |  | 2 |
| penalty-4@8192 | `mal+ugud` |  | 2 |
| penalty-4@16384 | `mal+ugud` |  | 2 |
| penalty-8@6080 | `mal+ug+ud` |  | 3 |
| penalty-8@8192 | `mal+ug+ud` |  | 3 |
| penalty-8@16384 | `mal+ugud` |  | 2 |
| stochastic-p4-d0.1@6080 | `malu+gud` |  | 2 |
| stochastic-p4-d0.1@8192 | `malu+gud` |  | 2 |
| stochastic-p4-d0.1@16384 | `malu+gud` |  | 2 |
| stochastic-p4-d0.2@6080 | `mal+u+gud` |  | 3 |
| stochastic-p4-d0.2@8192 | `mal+u+gud` |  | 3 |
| stochastic-p4-d0.2@16384 | `malu+gud` |  | 2 |
| unigram-ablation@6080 | `ma+lugud` | OK | 2 |

## `malagung`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+lagung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malagung` |  | 1 |
| plain@8192 | `malagung` |  | 1 |
| plain@16384 | `malagung` |  | 1 |
| morphbpe@6080 | `malagung` |  | 1 |
| morphbpe@8192 | `malagung` |  | 1 |
| morphbpe@16384 | `malagung` |  | 1 |
| penalty-1@6080 | `malagung` |  | 1 |
| penalty-1@8192 | `malagung` |  | 1 |
| penalty-1@16384 | `malagung` |  | 1 |
| penalty-2@6080 | `malagung` |  | 1 |
| penalty-2@8192 | `malagung` |  | 1 |
| penalty-2@16384 | `malagung` |  | 1 |
| penalty-4@6080 | `malagung` |  | 1 |
| penalty-4@8192 | `malagung` |  | 1 |
| penalty-4@16384 | `malagung` |  | 1 |
| penalty-8@6080 | `malagung` |  | 1 |
| penalty-8@8192 | `malagung` |  | 1 |
| penalty-8@16384 | `malagung` |  | 1 |
| stochastic-p4-d0.1@6080 | `malagung` |  | 1 |
| stochastic-p4-d0.1@8192 | `malagung` |  | 1 |
| stochastic-p4-d0.1@16384 | `malagung` |  | 1 |
| stochastic-p4-d0.2@6080 | `malagung` |  | 1 |
| stochastic-p4-d0.2@8192 | `malagung` |  | 1 |
| stochastic-p4-d0.2@16384 | `malagung` |  | 1 |
| unigram-ablation@6080 | `malagung` |  | 1 |

## `mangmang`  (prefixation, tier A_strong_silver)

**silver gold:** `mang+mang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mang+mang` | OK | 2 |
| plain@8192 | `mang+mang` | OK | 2 |
| plain@16384 | `mangmang` |  | 1 |
| morphbpe@6080 | `mang+mang` | OK | 2 |
| morphbpe@8192 | `mangmang` |  | 1 |
| morphbpe@16384 | `mangmang` |  | 1 |
| penalty-1@6080 | `mang+mang` | OK | 2 |
| penalty-1@8192 | `mangmang` |  | 1 |
| penalty-1@16384 | `mangmang` |  | 1 |
| penalty-2@6080 | `mang+mang` | OK | 2 |
| penalty-2@8192 | `mangmang` |  | 1 |
| penalty-2@16384 | `mangmang` |  | 1 |
| penalty-4@6080 | `mang+mang` | OK | 2 |
| penalty-4@8192 | `mangmang` |  | 1 |
| penalty-4@16384 | `mangmang` |  | 1 |
| penalty-8@6080 | `mang+mang` | OK | 2 |
| penalty-8@8192 | `mangmang` |  | 1 |
| penalty-8@16384 | `mangmang` |  | 1 |
| stochastic-p4-d0.1@6080 | `mang+mang` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mangmang` |  | 1 |
| stochastic-p4-d0.1@16384 | `mangmang` |  | 1 |
| stochastic-p4-d0.2@6080 | `mang+mang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mangmang` |  | 1 |
| stochastic-p4-d0.2@16384 | `mangmang` |  | 1 |
| unigram-ablation@6080 | `mang+mang` | OK | 2 |

## `miglalang`  (prefixation, tier A_strong_silver)

**silver gold:** `mig+lalang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mig+lalang` | OK | 2 |
| plain@8192 | `mig+lalang` | OK | 2 |
| plain@16384 | `miglalang` |  | 1 |
| morphbpe@6080 | `mig+lalang` | OK | 2 |
| morphbpe@8192 | `mig+lalang` | OK | 2 |
| morphbpe@16384 | `mig+lalang` | OK | 2 |
| penalty-1@6080 | `mig+lalang` | OK | 2 |
| penalty-1@8192 | `mig+lalang` | OK | 2 |
| penalty-1@16384 | `mig+lalang` | OK | 2 |
| penalty-2@6080 | `mig+lalang` | OK | 2 |
| penalty-2@8192 | `mig+lalang` | OK | 2 |
| penalty-2@16384 | `mig+lalang` | OK | 2 |
| penalty-4@6080 | `mig+lalang` | OK | 2 |
| penalty-4@8192 | `mig+lalang` | OK | 2 |
| penalty-4@16384 | `mig+lalang` | OK | 2 |
| penalty-8@6080 | `mig+lalang` | OK | 2 |
| penalty-8@8192 | `mig+lalang` | OK | 2 |
| penalty-8@16384 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mig+lalang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mig+lalang` | OK | 2 |
| unigram-ablation@6080 | `miglala+ng` |  | 2 |

## `pamisip`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pam+isip`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pamisip` |  | 1 |
| plain@8192 | `pamisip` |  | 1 |
| plain@16384 | `pamisip` |  | 1 |
| morphbpe@6080 | `pamisip` |  | 1 |
| morphbpe@8192 | `pamisip` |  | 1 |
| morphbpe@16384 | `pamisip` |  | 1 |
| penalty-1@6080 | `pamisip` |  | 1 |
| penalty-1@8192 | `pamisip` |  | 1 |
| penalty-1@16384 | `pamisip` |  | 1 |
| penalty-2@6080 | `pamisip` |  | 1 |
| penalty-2@8192 | `pamisip` |  | 1 |
| penalty-2@16384 | `pamisip` |  | 1 |
| penalty-4@6080 | `pamisip` |  | 1 |
| penalty-4@8192 | `pamisip` |  | 1 |
| penalty-4@16384 | `pamisip` |  | 1 |
| penalty-8@6080 | `pamisip` |  | 1 |
| penalty-8@8192 | `pamisip` |  | 1 |
| penalty-8@16384 | `pamisip` |  | 1 |
| stochastic-p4-d0.1@6080 | `pamisip` |  | 1 |
| stochastic-p4-d0.1@8192 | `pamisip` |  | 1 |
| stochastic-p4-d0.1@16384 | `pamisip` |  | 1 |
| stochastic-p4-d0.2@6080 | `pamisip` |  | 1 |
| stochastic-p4-d0.2@8192 | `pamisip` |  | 1 |
| stochastic-p4-d0.2@16384 | `pamisip` |  | 1 |
| unigram-ablation@6080 | `pamisip` |  | 1 |

## `manuknangan`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `man+uknang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manuknangan` |  | 1 |
| plain@8192 | `manuknangan` |  | 1 |
| plain@16384 | `manuknangan` |  | 1 |
| morphbpe@6080 | `manuknangan` |  | 1 |
| morphbpe@8192 | `manuknangan` |  | 1 |
| morphbpe@16384 | `manuknangan` |  | 1 |
| penalty-1@6080 | `manuknangan` |  | 1 |
| penalty-1@8192 | `manuknangan` |  | 1 |
| penalty-1@16384 | `manuknangan` |  | 1 |
| penalty-2@6080 | `manuknangan` |  | 1 |
| penalty-2@8192 | `manuknangan` |  | 1 |
| penalty-2@16384 | `manuknangan` |  | 1 |
| penalty-4@6080 | `manuknangan` |  | 1 |
| penalty-4@8192 | `manuknangan` |  | 1 |
| penalty-4@16384 | `manuknangan` |  | 1 |
| penalty-8@6080 | `manuknangan` |  | 1 |
| penalty-8@8192 | `manuknangan` |  | 1 |
| penalty-8@16384 | `manuknangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `manuknangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `manuknangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `manuknangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `manuknangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `manuknangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `manuknangan` |  | 1 |
| unigram-ablation@6080 | `manuknanga+n` |  | 2 |

## `menuknangan`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `men+uknang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `men+uknangan` |  | 2 |
| plain@8192 | `menuknangan` |  | 1 |
| plain@16384 | `menuknangan` |  | 1 |
| morphbpe@6080 | `men+uknangan` |  | 2 |
| morphbpe@8192 | `menuknangan` |  | 1 |
| morphbpe@16384 | `menuknangan` |  | 1 |
| penalty-1@6080 | `men+uknangan` |  | 2 |
| penalty-1@8192 | `menuknangan` |  | 1 |
| penalty-1@16384 | `menuknangan` |  | 1 |
| penalty-2@6080 | `men+uknangan` |  | 2 |
| penalty-2@8192 | `menuknangan` |  | 1 |
| penalty-2@16384 | `menuknangan` |  | 1 |
| penalty-4@6080 | `men+uknangan` |  | 2 |
| penalty-4@8192 | `menuknangan` |  | 1 |
| penalty-4@16384 | `menuknangan` |  | 1 |
| penalty-8@6080 | `men+uknang+an` | OK | 3 |
| penalty-8@8192 | `menuknangan` |  | 1 |
| penalty-8@16384 | `menuknangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `men+uknang+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `menuknangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `menuknangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `men+uknang+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `menuknangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `menuknangan` |  | 1 |
| unigram-ablation@6080 | `m+enuknangan` |  | 2 |

## `menibatan`  (prefixation+suffixation, tier A_strong_silver)

**silver gold:** `men+ibat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `menibatan` |  | 1 |
| plain@8192 | `menibatan` |  | 1 |
| plain@16384 | `menibatan` |  | 1 |
| morphbpe@6080 | `menibatan` |  | 1 |
| morphbpe@8192 | `menibatan` |  | 1 |
| morphbpe@16384 | `menibatan` |  | 1 |
| penalty-1@6080 | `men+ibat+an` | OK | 3 |
| penalty-1@8192 | `men+ibat+an` | OK | 3 |
| penalty-1@16384 | `men+ibat+an` | OK | 3 |
| penalty-2@6080 | `men+ibat+an` | OK | 3 |
| penalty-2@8192 | `men+ibat+an` | OK | 3 |
| penalty-2@16384 | `men+ibat+an` | OK | 3 |
| penalty-4@6080 | `men+ibat+an` | OK | 3 |
| penalty-4@8192 | `men+ibat+an` | OK | 3 |
| penalty-4@16384 | `men+ibat+an` | OK | 3 |
| penalty-8@6080 | `men+ibat+an` | OK | 3 |
| penalty-8@8192 | `men+ibat+an` | OK | 3 |
| penalty-8@16384 | `men+ibat+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `men+ibat+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `men+ibat+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `men+ibat+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `menibatan` |  | 1 |
| stochastic-p4-d0.2@8192 | `menibatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `menibatan` |  | 1 |
| unigram-ablation@6080 | `me+nibatan` |  | 2 |

## `makanianman`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `maka+nianm+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makanian+man` |  | 2 |
| plain@8192 | `makanian+man` |  | 2 |
| plain@16384 | `makanian+man` |  | 2 |
| morphbpe@6080 | `makanian+man` |  | 2 |
| morphbpe@8192 | `makanian+man` |  | 2 |
| morphbpe@16384 | `makanian+man` |  | 2 |
| penalty-1@6080 | `makanian+man` |  | 2 |
| penalty-1@8192 | `makanian+man` |  | 2 |
| penalty-1@16384 | `makanian+man` |  | 2 |
| penalty-2@6080 | `makanian+man` |  | 2 |
| penalty-2@8192 | `makanian+man` |  | 2 |
| penalty-2@16384 | `makanian+man` |  | 2 |
| penalty-4@6080 | `makanian+man` |  | 2 |
| penalty-4@8192 | `makanian+man` |  | 2 |
| penalty-4@16384 | `makanian+man` |  | 2 |
| penalty-8@6080 | `makanian+man` |  | 2 |
| penalty-8@8192 | `makanian+man` |  | 2 |
| penalty-8@16384 | `makanian+man` |  | 2 |
| stochastic-p4-d0.1@6080 | `makan+ian+man` |  | 3 |
| stochastic-p4-d0.1@8192 | `makan+ian+man` |  | 3 |
| stochastic-p4-d0.1@16384 | `makan+ian+man` |  | 3 |
| stochastic-p4-d0.2@6080 | `makanian+man` |  | 2 |
| stochastic-p4-d0.2@8192 | `makanian+man` |  | 2 |
| stochastic-p4-d0.2@16384 | `makanian+man` |  | 2 |
| unigram-ablation@6080 | `makanian+man` |  | 2 |

## `magkailangan`  (prefixation+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `mag+kailangan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+kailangan` | OK | 2 |
| plain@8192 | `mag+kailangan` | OK | 2 |
| plain@16384 | `mag+kailangan` | OK | 2 |
| morphbpe@6080 | `mag+kailangan` | OK | 2 |
| morphbpe@8192 | `mag+kailangan` | OK | 2 |
| morphbpe@16384 | `mag+kailangan` | OK | 2 |
| penalty-1@6080 | `mag+kailangan` | OK | 2 |
| penalty-1@8192 | `mag+kailangan` | OK | 2 |
| penalty-1@16384 | `mag+kailangan` | OK | 2 |
| penalty-2@6080 | `mag+kailangan` | OK | 2 |
| penalty-2@8192 | `mag+kailangan` | OK | 2 |
| penalty-2@16384 | `mag+kailangan` | OK | 2 |
| penalty-4@6080 | `mag+kailangan` | OK | 2 |
| penalty-4@8192 | `mag+kailangan` | OK | 2 |
| penalty-4@16384 | `mag+kailangan` | OK | 2 |
| penalty-8@6080 | `mag+kailangan` | OK | 2 |
| penalty-8@8192 | `mag+kailangan` | OK | 2 |
| penalty-8@16384 | `mag+kailangan` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+ka+ilangan` |  | 3 |
| stochastic-p4-d0.1@8192 | `magka+ilangan` |  | 2 |
| stochastic-p4-d0.1@16384 | `magka+ilangan` |  | 2 |
| stochastic-p4-d0.2@6080 | `mag+ka+ilangan` |  | 3 |
| stochastic-p4-d0.2@8192 | `mag+ka+ilangan` |  | 3 |
| stochastic-p4-d0.2@16384 | `magka+ilangan` |  | 2 |
| unigram-ablation@6080 | `mag+kailangan` | OK | 2 |

## `pisamban`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `pi+samb+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pisamban` |  | 1 |
| plain@8192 | `pisamban` |  | 1 |
| plain@16384 | `pisamban` |  | 1 |
| morphbpe@6080 | `pisamban` |  | 1 |
| morphbpe@8192 | `pisamban` |  | 1 |
| morphbpe@16384 | `pisamban` |  | 1 |
| penalty-1@6080 | `pisamban` |  | 1 |
| penalty-1@8192 | `pisamban` |  | 1 |
| penalty-1@16384 | `pisamban` |  | 1 |
| penalty-2@6080 | `pisamban` |  | 1 |
| penalty-2@8192 | `pisamban` |  | 1 |
| penalty-2@16384 | `pisamban` |  | 1 |
| penalty-4@6080 | `pisamban` |  | 1 |
| penalty-4@8192 | `pisamban` |  | 1 |
| penalty-4@16384 | `pisamban` |  | 1 |
| penalty-8@6080 | `pisamban` |  | 1 |
| penalty-8@8192 | `pisamban` |  | 1 |
| penalty-8@16384 | `pisamban` |  | 1 |
| stochastic-p4-d0.1@6080 | `pisamban` |  | 1 |
| stochastic-p4-d0.1@8192 | `pisamban` |  | 1 |
| stochastic-p4-d0.1@16384 | `pisamban` |  | 1 |
| stochastic-p4-d0.2@6080 | `pisamban` |  | 1 |
| stochastic-p4-d0.2@8192 | `pisamban` |  | 1 |
| stochastic-p4-d0.2@16384 | `pisamban` |  | 1 |
| unigram-ablation@6080 | `pisamban` |  | 1 |

## `lalaki`  (reduplication, tier B_moderate_silver)

**silver gold:** `lalaki`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lalaki` | OK | 1 |
| plain@8192 | `lalaki` | OK | 1 |
| plain@16384 | `lalaki` | OK | 1 |
| morphbpe@6080 | `lalaki` | OK | 1 |
| morphbpe@8192 | `lalaki` | OK | 1 |
| morphbpe@16384 | `lalaki` | OK | 1 |
| penalty-1@6080 | `lalaki` | OK | 1 |
| penalty-1@8192 | `lalaki` | OK | 1 |
| penalty-1@16384 | `lalaki` | OK | 1 |
| penalty-2@6080 | `lalaki` | OK | 1 |
| penalty-2@8192 | `lalaki` | OK | 1 |
| penalty-2@16384 | `lalaki` | OK | 1 |
| penalty-4@6080 | `lalaki` | OK | 1 |
| penalty-4@8192 | `lalaki` | OK | 1 |
| penalty-4@16384 | `lalaki` | OK | 1 |
| penalty-8@6080 | `lalaki` | OK | 1 |
| penalty-8@8192 | `lalaki` | OK | 1 |
| penalty-8@16384 | `lalaki` | OK | 1 |
| stochastic-p4-d0.1@6080 | `lalaki` | OK | 1 |
| stochastic-p4-d0.1@8192 | `lalaki` | OK | 1 |
| stochastic-p4-d0.1@16384 | `lalaki` | OK | 1 |
| stochastic-p4-d0.2@6080 | `lalaki` | OK | 1 |
| stochastic-p4-d0.2@8192 | `lalaki` | OK | 1 |
| stochastic-p4-d0.2@16384 | `lalaki` | OK | 1 |
| unigram-ablation@6080 | `lalaki` | OK | 1 |

## `babaing`  (reduplication, tier B_moderate_silver)

**silver gold:** `babaing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `babaing` | OK | 1 |
| plain@8192 | `babaing` | OK | 1 |
| plain@16384 | `babaing` | OK | 1 |
| morphbpe@6080 | `babaing` | OK | 1 |
| morphbpe@8192 | `babaing` | OK | 1 |
| morphbpe@16384 | `babaing` | OK | 1 |
| penalty-1@6080 | `babaing` | OK | 1 |
| penalty-1@8192 | `babaing` | OK | 1 |
| penalty-1@16384 | `babaing` | OK | 1 |
| penalty-2@6080 | `babaing` | OK | 1 |
| penalty-2@8192 | `babaing` | OK | 1 |
| penalty-2@16384 | `babaing` | OK | 1 |
| penalty-4@6080 | `babaing` | OK | 1 |
| penalty-4@8192 | `babaing` | OK | 1 |
| penalty-4@16384 | `babaing` | OK | 1 |
| penalty-8@6080 | `babaing` | OK | 1 |
| penalty-8@8192 | `babaing` | OK | 1 |
| penalty-8@16384 | `babaing` | OK | 1 |
| stochastic-p4-d0.1@6080 | `babaing` | OK | 1 |
| stochastic-p4-d0.1@8192 | `babaing` | OK | 1 |
| stochastic-p4-d0.1@16384 | `babaing` | OK | 1 |
| stochastic-p4-d0.2@6080 | `babaing` | OK | 1 |
| stochastic-p4-d0.2@8192 | `babaing` | OK | 1 |
| stochastic-p4-d0.2@16384 | `babaing` | OK | 1 |
| unigram-ablation@6080 | `babaing` | OK | 1 |

## `lele`  (reduplication, tier A_strong_silver)

**silver gold:** `lele`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lele` | OK | 1 |
| plain@8192 | `lele` | OK | 1 |
| plain@16384 | `lele` | OK | 1 |
| morphbpe@6080 | `lele` | OK | 1 |
| morphbpe@8192 | `lele` | OK | 1 |
| morphbpe@16384 | `lele` | OK | 1 |
| penalty-1@6080 | `lele` | OK | 1 |
| penalty-1@8192 | `lele` | OK | 1 |
| penalty-1@16384 | `lele` | OK | 1 |
| penalty-2@6080 | `lele` | OK | 1 |
| penalty-2@8192 | `lele` | OK | 1 |
| penalty-2@16384 | `lele` | OK | 1 |
| penalty-4@6080 | `lele` | OK | 1 |
| penalty-4@8192 | `lele` | OK | 1 |
| penalty-4@16384 | `lele` | OK | 1 |
| penalty-8@6080 | `lele` | OK | 1 |
| penalty-8@8192 | `lele` | OK | 1 |
| penalty-8@16384 | `lele` | OK | 1 |
| stochastic-p4-d0.1@6080 | `lele` | OK | 1 |
| stochastic-p4-d0.1@8192 | `lele` | OK | 1 |
| stochastic-p4-d0.1@16384 | `lele` | OK | 1 |
| stochastic-p4-d0.2@6080 | `lele` | OK | 1 |
| stochastic-p4-d0.2@8192 | `lele` | OK | 1 |
| stochastic-p4-d0.2@16384 | `lele` | OK | 1 |
| unigram-ablation@6080 | `lele` | OK | 1 |

## `susuyu`  (reduplication, tier B_moderate_silver)

**silver gold:** `susuyu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sus+uyu` |  | 2 |
| plain@8192 | `susuyu` | OK | 1 |
| plain@16384 | `susuyu` | OK | 1 |
| morphbpe@6080 | `sus+uyu` |  | 2 |
| morphbpe@8192 | `susuyu` | OK | 1 |
| morphbpe@16384 | `susuyu` | OK | 1 |
| penalty-1@6080 | `sus+uyu` |  | 2 |
| penalty-1@8192 | `susuyu` | OK | 1 |
| penalty-1@16384 | `susuyu` | OK | 1 |
| penalty-2@6080 | `sus+uyu` |  | 2 |
| penalty-2@8192 | `susuyu` | OK | 1 |
| penalty-2@16384 | `susuyu` | OK | 1 |
| penalty-4@6080 | `susu+yu` |  | 2 |
| penalty-4@8192 | `susuyu` | OK | 1 |
| penalty-4@16384 | `susuyu` | OK | 1 |
| penalty-8@6080 | `sus+uyu` |  | 2 |
| penalty-8@8192 | `susuyu` | OK | 1 |
| penalty-8@16384 | `susuyu` | OK | 1 |
| stochastic-p4-d0.1@6080 | `susu+yu` |  | 2 |
| stochastic-p4-d0.1@8192 | `susuyu` | OK | 1 |
| stochastic-p4-d0.1@16384 | `susuyu` | OK | 1 |
| stochastic-p4-d0.2@6080 | `sus+uyu` |  | 2 |
| stochastic-p4-d0.2@8192 | `susuyu` | OK | 1 |
| stochastic-p4-d0.2@16384 | `susuyu` | OK | 1 |
| unigram-ablation@6080 | `susuyu` | OK | 1 |

## `lulugud`  (reduplication, tier A_strong_silver)

**silver gold:** `lulugud`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lul+ugud` |  | 2 |
| plain@8192 | `lul+ugud` |  | 2 |
| plain@16384 | `lulugud` | OK | 1 |
| morphbpe@6080 | `lul+ugud` |  | 2 |
| morphbpe@8192 | `lul+ugud` |  | 2 |
| morphbpe@16384 | `lul+ugud` |  | 2 |
| penalty-1@6080 | `lul+ugud` |  | 2 |
| penalty-1@8192 | `lul+ugud` |  | 2 |
| penalty-1@16384 | `lul+ugud` |  | 2 |
| penalty-2@6080 | `lul+ugud` |  | 2 |
| penalty-2@8192 | `lul+ugud` |  | 2 |
| penalty-2@16384 | `lul+ugud` |  | 2 |
| penalty-4@6080 | `lul+ugud` |  | 2 |
| penalty-4@8192 | `lul+ugud` |  | 2 |
| penalty-4@16384 | `lul+ugud` |  | 2 |
| penalty-8@6080 | `lu+lugud` |  | 2 |
| penalty-8@8192 | `lu+lugud` |  | 2 |
| penalty-8@16384 | `lu+lugud` |  | 2 |
| stochastic-p4-d0.1@6080 | `lulu+gud` |  | 2 |
| stochastic-p4-d0.1@8192 | `lulu+gud` |  | 2 |
| stochastic-p4-d0.1@16384 | `lulu+gud` |  | 2 |
| stochastic-p4-d0.2@6080 | `lu+lugud` |  | 2 |
| stochastic-p4-d0.2@8192 | `lu+lugud` |  | 2 |
| stochastic-p4-d0.2@16384 | `lu+lugud` |  | 2 |
| unigram-ablation@6080 | `lu+lugud` |  | 2 |

## `sasalikut`  (reduplication, tier A_strong_silver)

**silver gold:** `sasalikut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sas+alikut` |  | 2 |
| plain@8192 | `sas+alikut` |  | 2 |
| plain@16384 | `sasalikut` | OK | 1 |
| morphbpe@6080 | `sas+ali+kut` |  | 3 |
| morphbpe@8192 | `sas+alikut` |  | 2 |
| morphbpe@16384 | `sas+alikut` |  | 2 |
| penalty-1@6080 | `sas+ali+kut` |  | 3 |
| penalty-1@8192 | `sas+alikut` |  | 2 |
| penalty-1@16384 | `sas+alikut` |  | 2 |
| penalty-2@6080 | `sas+ali+kut` |  | 3 |
| penalty-2@8192 | `sas+alikut` |  | 2 |
| penalty-2@16384 | `sas+alikut` |  | 2 |
| penalty-4@6080 | `sa+salikut` |  | 2 |
| penalty-4@8192 | `sa+salikut` |  | 2 |
| penalty-4@16384 | `sa+salikut` |  | 2 |
| penalty-8@6080 | `sa+salikut` |  | 2 |
| penalty-8@8192 | `sa+salikut` |  | 2 |
| penalty-8@16384 | `sa+salikut` |  | 2 |
| stochastic-p4-d0.1@6080 | `sa+sali+kut` |  | 3 |
| stochastic-p4-d0.1@8192 | `sa+salikut` |  | 2 |
| stochastic-p4-d0.1@16384 | `sa+salikut` |  | 2 |
| stochastic-p4-d0.2@6080 | `sa+salikut` |  | 2 |
| stochastic-p4-d0.2@8192 | `sa+salikut` |  | 2 |
| stochastic-p4-d0.2@16384 | `sa+salikut` |  | 2 |
| unigram-ablation@6080 | `sa+salikut` |  | 2 |

## `sasabian`  (reduplication+suffixation, tier A_strong_silver)

**silver gold:** `sasabi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sasabian` |  | 1 |
| plain@8192 | `sasabian` |  | 1 |
| plain@16384 | `sasabian` |  | 1 |
| morphbpe@6080 | `sas+abian` |  | 2 |
| morphbpe@8192 | `sas+abian` |  | 2 |
| morphbpe@16384 | `sas+abian` |  | 2 |
| penalty-1@6080 | `sas+abian` |  | 2 |
| penalty-1@8192 | `sas+abian` |  | 2 |
| penalty-1@16384 | `sas+abian` |  | 2 |
| penalty-2@6080 | `sas+abian` |  | 2 |
| penalty-2@8192 | `sas+abian` |  | 2 |
| penalty-2@16384 | `sas+abian` |  | 2 |
| penalty-4@6080 | `sa+sabian` |  | 2 |
| penalty-4@8192 | `sa+sabian` |  | 2 |
| penalty-4@16384 | `sa+sabian` |  | 2 |
| penalty-8@6080 | `sa+sabian` |  | 2 |
| penalty-8@8192 | `sa+sabian` |  | 2 |
| penalty-8@16384 | `sa+sabian` |  | 2 |
| stochastic-p4-d0.1@6080 | `sa+sabi+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `sa+sabi+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `sa+sabi+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `sa+sabian` |  | 2 |
| stochastic-p4-d0.2@8192 | `sa+sabian` |  | 2 |
| stochastic-p4-d0.2@16384 | `sa+sabian` |  | 2 |
| unigram-ablation@6080 | `sasabian` |  | 1 |

## `mamangan`  (reduplication+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+mangan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mamangan` |  | 1 |
| plain@8192 | `mamangan` |  | 1 |
| plain@16384 | `mamangan` |  | 1 |
| morphbpe@6080 | `mamangan` |  | 1 |
| morphbpe@8192 | `mamangan` |  | 1 |
| morphbpe@16384 | `mamangan` |  | 1 |
| penalty-1@6080 | `mamangan` |  | 1 |
| penalty-1@8192 | `mamangan` |  | 1 |
| penalty-1@16384 | `mamangan` |  | 1 |
| penalty-2@6080 | `mamangan` |  | 1 |
| penalty-2@8192 | `mamangan` |  | 1 |
| penalty-2@16384 | `mamangan` |  | 1 |
| penalty-4@6080 | `mamangan` |  | 1 |
| penalty-4@8192 | `mamangan` |  | 1 |
| penalty-4@16384 | `mamangan` |  | 1 |
| penalty-8@6080 | `mamangan` |  | 1 |
| penalty-8@8192 | `mamangan` |  | 1 |
| penalty-8@16384 | `mamangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `mamangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `mamangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `mamangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `mamangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `mamangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `mamangan` |  | 1 |
| unigram-ablation@6080 | `ma+mangan` | OK | 2 |

## `sasabyan`  (reduplication+suffixation, tier B_moderate_silver)

**silver gold:** `sasaby+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sasabyan` |  | 1 |
| plain@8192 | `sasabyan` |  | 1 |
| plain@16384 | `sasabyan` |  | 1 |
| morphbpe@6080 | `sasabyan` |  | 1 |
| morphbpe@8192 | `sasabyan` |  | 1 |
| morphbpe@16384 | `sasabyan` |  | 1 |
| penalty-1@6080 | `sasabyan` |  | 1 |
| penalty-1@8192 | `sasabyan` |  | 1 |
| penalty-1@16384 | `sasabyan` |  | 1 |
| penalty-2@6080 | `sasabyan` |  | 1 |
| penalty-2@8192 | `sasabyan` |  | 1 |
| penalty-2@16384 | `sasabyan` |  | 1 |
| penalty-4@6080 | `sasabyan` |  | 1 |
| penalty-4@8192 | `sasabyan` |  | 1 |
| penalty-4@16384 | `sasabyan` |  | 1 |
| penalty-8@6080 | `sasabyan` |  | 1 |
| penalty-8@8192 | `sasabyan` |  | 1 |
| penalty-8@16384 | `sasabyan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sasabyan` |  | 1 |
| stochastic-p4-d0.1@8192 | `sasabyan` |  | 1 |
| stochastic-p4-d0.1@16384 | `sasabyan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sasabyan` |  | 1 |
| stochastic-p4-d0.2@8192 | `sasabyan` |  | 1 |
| stochastic-p4-d0.2@16384 | `sasabyan` |  | 1 |
| unigram-ablation@6080 | `sasabyan` |  | 1 |

## `sasamban`  (reduplication+suffixation, tier B_moderate_silver)

**silver gold:** `sasamb+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sas+amban` |  | 2 |
| plain@8192 | `sas+amban` |  | 2 |
| plain@16384 | `sasamban` |  | 1 |
| morphbpe@6080 | `sas+amban` |  | 2 |
| morphbpe@8192 | `sas+amban` |  | 2 |
| morphbpe@16384 | `sas+amban` |  | 2 |
| penalty-1@6080 | `sas+amban` |  | 2 |
| penalty-1@8192 | `sas+amban` |  | 2 |
| penalty-1@16384 | `sas+amban` |  | 2 |
| penalty-2@6080 | `sas+amban` |  | 2 |
| penalty-2@8192 | `sas+amban` |  | 2 |
| penalty-2@16384 | `sas+amban` |  | 2 |
| penalty-4@6080 | `sa+sam+ban` |  | 3 |
| penalty-4@8192 | `sa+sam+ban` |  | 3 |
| penalty-4@16384 | `sa+sam+ban` |  | 3 |
| penalty-8@6080 | `sa+sam+ban` |  | 3 |
| penalty-8@8192 | `sa+sam+ban` |  | 3 |
| penalty-8@16384 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.1@6080 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.1@8192 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.1@16384 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.2@6080 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.2@8192 | `sa+sam+ban` |  | 3 |
| stochastic-p4-d0.2@16384 | `sa+sam+ban` |  | 3 |
| unigram-ablation@6080 | `sa+samban` |  | 2 |

## `gugulutan`  (reduplication+suffixation, tier A_strong_silver)

**silver gold:** `gugulut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gug+ulutan` |  | 2 |
| plain@8192 | `gug+ulutan` |  | 2 |
| plain@16384 | `gugulutan` |  | 1 |
| morphbpe@6080 | `g+ug+ulut+an` |  | 4 |
| morphbpe@8192 | `gug+ulut+an` |  | 3 |
| morphbpe@16384 | `gug+ulut+an` |  | 3 |
| penalty-1@6080 | `g+ug+ulut+an` |  | 4 |
| penalty-1@8192 | `gug+ulut+an` |  | 3 |
| penalty-1@16384 | `gug+ulut+an` |  | 3 |
| penalty-2@6080 | `g+ug+ulut+an` |  | 4 |
| penalty-2@8192 | `g+ug+ulut+an` |  | 4 |
| penalty-2@16384 | `gug+ulut+an` |  | 3 |
| penalty-4@6080 | `g+ug+ulut+an` |  | 4 |
| penalty-4@8192 | `g+ug+ulut+an` |  | 4 |
| penalty-4@16384 | `gug+ulut+an` |  | 3 |
| penalty-8@6080 | `g+ug+ulu+tan` |  | 4 |
| penalty-8@8192 | `g+ug+ulu+tan` |  | 4 |
| penalty-8@16384 | `gug+ulu+tan` |  | 3 |
| stochastic-p4-d0.1@6080 | `gu+gulut+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `gu+gulut+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `gu+gulut+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `gu+gu+lutan` |  | 3 |
| stochastic-p4-d0.2@8192 | `gu+gu+lutan` |  | 3 |
| stochastic-p4-d0.2@16384 | `gu+gu+lutan` |  | 3 |
| unigram-ablation@6080 | `gugul+utan` |  | 2 |

## `naman`  (suffixation, tier B_moderate_silver)

**silver gold:** `nam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `naman` |  | 1 |
| plain@8192 | `naman` |  | 1 |
| plain@16384 | `naman` |  | 1 |
| morphbpe@6080 | `naman` |  | 1 |
| morphbpe@8192 | `naman` |  | 1 |
| morphbpe@16384 | `naman` |  | 1 |
| penalty-1@6080 | `naman` |  | 1 |
| penalty-1@8192 | `naman` |  | 1 |
| penalty-1@16384 | `naman` |  | 1 |
| penalty-2@6080 | `naman` |  | 1 |
| penalty-2@8192 | `naman` |  | 1 |
| penalty-2@16384 | `naman` |  | 1 |
| penalty-4@6080 | `naman` |  | 1 |
| penalty-4@8192 | `naman` |  | 1 |
| penalty-4@16384 | `naman` |  | 1 |
| penalty-8@6080 | `naman` |  | 1 |
| penalty-8@8192 | `naman` |  | 1 |
| penalty-8@16384 | `naman` |  | 1 |
| stochastic-p4-d0.1@6080 | `naman` |  | 1 |
| stochastic-p4-d0.1@8192 | `naman` |  | 1 |
| stochastic-p4-d0.1@16384 | `naman` |  | 1 |
| stochastic-p4-d0.2@6080 | `naman` |  | 1 |
| stochastic-p4-d0.2@8192 | `naman` |  | 1 |
| stochastic-p4-d0.2@16384 | `naman` |  | 1 |
| unigram-ablation@6080 | `naman` |  | 1 |

## `balayan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `balay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `balayan` |  | 1 |
| plain@8192 | `balayan` |  | 1 |
| plain@16384 | `balayan` |  | 1 |
| morphbpe@6080 | `balayan` |  | 1 |
| morphbpe@8192 | `balayan` |  | 1 |
| morphbpe@16384 | `balayan` |  | 1 |
| penalty-1@6080 | `balayan` |  | 1 |
| penalty-1@8192 | `balayan` |  | 1 |
| penalty-1@16384 | `balayan` |  | 1 |
| penalty-2@6080 | `balayan` |  | 1 |
| penalty-2@8192 | `balayan` |  | 1 |
| penalty-2@16384 | `balayan` |  | 1 |
| penalty-4@6080 | `balayan` |  | 1 |
| penalty-4@8192 | `balayan` |  | 1 |
| penalty-4@16384 | `balayan` |  | 1 |
| penalty-8@6080 | `balayan` |  | 1 |
| penalty-8@8192 | `balayan` |  | 1 |
| penalty-8@16384 | `balayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `balayan` |  | 1 |
| stochastic-p4-d0.1@8192 | `balayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `balayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `balayan` |  | 1 |
| stochastic-p4-d0.2@8192 | `balayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `balayan` |  | 1 |
| unigram-ablation@6080 | `balayan` |  | 1 |

## `gawan`  (suffixation, tier B_moderate_silver)

**silver gold:** `gaw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gawan` |  | 1 |
| plain@8192 | `gawan` |  | 1 |
| plain@16384 | `gawan` |  | 1 |
| morphbpe@6080 | `gawan` |  | 1 |
| morphbpe@8192 | `gawan` |  | 1 |
| morphbpe@16384 | `gawan` |  | 1 |
| penalty-1@6080 | `gawan` |  | 1 |
| penalty-1@8192 | `gawan` |  | 1 |
| penalty-1@16384 | `gawan` |  | 1 |
| penalty-2@6080 | `gawan` |  | 1 |
| penalty-2@8192 | `gawan` |  | 1 |
| penalty-2@16384 | `gawan` |  | 1 |
| penalty-4@6080 | `gawan` |  | 1 |
| penalty-4@8192 | `gawan` |  | 1 |
| penalty-4@16384 | `gawan` |  | 1 |
| penalty-8@6080 | `gawan` |  | 1 |
| penalty-8@8192 | `gawan` |  | 1 |
| penalty-8@16384 | `gawan` |  | 1 |
| stochastic-p4-d0.1@6080 | `gawan` |  | 1 |
| stochastic-p4-d0.1@8192 | `gawan` |  | 1 |
| stochastic-p4-d0.1@16384 | `gawan` |  | 1 |
| stochastic-p4-d0.2@6080 | `gawan` |  | 1 |
| stochastic-p4-d0.2@8192 | `gawan` |  | 1 |
| stochastic-p4-d0.2@16384 | `gawan` |  | 1 |
| unigram-ablation@6080 | `gawan` |  | 1 |

## `luklukan`  (suffixation, tier A_strong_silver)

**silver gold:** `lukluk+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `luklukan` |  | 1 |
| plain@8192 | `luklukan` |  | 1 |
| plain@16384 | `luklukan` |  | 1 |
| morphbpe@6080 | `luklukan` |  | 1 |
| morphbpe@8192 | `luklukan` |  | 1 |
| morphbpe@16384 | `luklukan` |  | 1 |
| penalty-1@6080 | `luklukan` |  | 1 |
| penalty-1@8192 | `luklukan` |  | 1 |
| penalty-1@16384 | `luklukan` |  | 1 |
| penalty-2@6080 | `luklukan` |  | 1 |
| penalty-2@8192 | `luklukan` |  | 1 |
| penalty-2@16384 | `luklukan` |  | 1 |
| penalty-4@6080 | `luklukan` |  | 1 |
| penalty-4@8192 | `luklukan` |  | 1 |
| penalty-4@16384 | `luklukan` |  | 1 |
| penalty-8@6080 | `luklukan` |  | 1 |
| penalty-8@8192 | `luklukan` |  | 1 |
| penalty-8@16384 | `luklukan` |  | 1 |
| stochastic-p4-d0.1@6080 | `luklukan` |  | 1 |
| stochastic-p4-d0.1@8192 | `luklukan` |  | 1 |
| stochastic-p4-d0.1@16384 | `luklukan` |  | 1 |
| stochastic-p4-d0.2@6080 | `luklukan` |  | 1 |
| stochastic-p4-d0.2@8192 | `luklukan` |  | 1 |
| stochastic-p4-d0.2@16384 | `luklukan` |  | 1 |
| unigram-ablation@6080 | `lukluk+an` | OK | 2 |

## `keraklan`  (suffixation, tier B_moderate_silver)

**silver gold:** `kerakl+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `keraklan` |  | 1 |
| plain@8192 | `keraklan` |  | 1 |
| plain@16384 | `keraklan` |  | 1 |
| morphbpe@6080 | `keraklan` |  | 1 |
| morphbpe@8192 | `keraklan` |  | 1 |
| morphbpe@16384 | `keraklan` |  | 1 |
| penalty-1@6080 | `keraklan` |  | 1 |
| penalty-1@8192 | `keraklan` |  | 1 |
| penalty-1@16384 | `keraklan` |  | 1 |
| penalty-2@6080 | `keraklan` |  | 1 |
| penalty-2@8192 | `keraklan` |  | 1 |
| penalty-2@16384 | `keraklan` |  | 1 |
| penalty-4@6080 | `keraklan` |  | 1 |
| penalty-4@8192 | `keraklan` |  | 1 |
| penalty-4@16384 | `keraklan` |  | 1 |
| penalty-8@6080 | `keraklan` |  | 1 |
| penalty-8@8192 | `keraklan` |  | 1 |
| penalty-8@16384 | `keraklan` |  | 1 |
| stochastic-p4-d0.1@6080 | `keraklan` |  | 1 |
| stochastic-p4-d0.1@8192 | `keraklan` |  | 1 |
| stochastic-p4-d0.1@16384 | `keraklan` |  | 1 |
| stochastic-p4-d0.2@6080 | `keraklan` |  | 1 |
| stochastic-p4-d0.2@8192 | `keraklan` |  | 1 |
| stochastic-p4-d0.2@16384 | `keraklan` |  | 1 |
| unigram-ablation@6080 | `keraklan` |  | 1 |

## `adwan`  (suffixation, tier B_moderate_silver)

**silver gold:** `adw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ad+wan` |  | 2 |
| plain@8192 | `ad+wan` |  | 2 |
| plain@16384 | `adwan` |  | 1 |
| morphbpe@6080 | `ad+wan` |  | 2 |
| morphbpe@8192 | `ad+wan` |  | 2 |
| morphbpe@16384 | `adwan` |  | 1 |
| penalty-1@6080 | `ad+wan` |  | 2 |
| penalty-1@8192 | `ad+wan` |  | 2 |
| penalty-1@16384 | `adwan` |  | 1 |
| penalty-2@6080 | `ad+wan` |  | 2 |
| penalty-2@8192 | `ad+wan` |  | 2 |
| penalty-2@16384 | `adwan` |  | 1 |
| penalty-4@6080 | `ad+wan` |  | 2 |
| penalty-4@8192 | `ad+wan` |  | 2 |
| penalty-4@16384 | `adwan` |  | 1 |
| penalty-8@6080 | `ad+wan` |  | 2 |
| penalty-8@8192 | `ad+wan` |  | 2 |
| penalty-8@16384 | `adwan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ad+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `ad+wan` |  | 2 |
| stochastic-p4-d0.1@16384 | `adwan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ad+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `ad+wan` |  | 2 |
| stochastic-p4-d0.2@16384 | `adwan` |  | 1 |
| unigram-ablation@6080 | `adwa+n` |  | 2 |

## `kealan`  (suffixation, tier B_moderate_silver)

**silver gold:** `keal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ke+alan` |  | 2 |
| plain@8192 | `ke+alan` |  | 2 |
| plain@16384 | `ke+alan` |  | 2 |
| morphbpe@6080 | `ke+alan` |  | 2 |
| morphbpe@8192 | `ke+alan` |  | 2 |
| morphbpe@16384 | `ke+alan` |  | 2 |
| penalty-1@6080 | `ke+alan` |  | 2 |
| penalty-1@8192 | `ke+alan` |  | 2 |
| penalty-1@16384 | `ke+alan` |  | 2 |
| penalty-2@6080 | `ke+alan` |  | 2 |
| penalty-2@8192 | `ke+alan` |  | 2 |
| penalty-2@16384 | `ke+alan` |  | 2 |
| penalty-4@6080 | `ke+alan` |  | 2 |
| penalty-4@8192 | `ke+alan` |  | 2 |
| penalty-4@16384 | `ke+alan` |  | 2 |
| penalty-8@6080 | `ke+alan` |  | 2 |
| penalty-8@8192 | `ke+alan` |  | 2 |
| penalty-8@16384 | `ke+alan` |  | 2 |
| stochastic-p4-d0.1@6080 | `ke+alan` |  | 2 |
| stochastic-p4-d0.1@8192 | `ke+alan` |  | 2 |
| stochastic-p4-d0.1@16384 | `ke+alan` |  | 2 |
| stochastic-p4-d0.2@6080 | `ke+alan` |  | 2 |
| stochastic-p4-d0.2@8192 | `ke+alan` |  | 2 |
| stochastic-p4-d0.2@16384 | `ke+alan` |  | 2 |
| unigram-ablation@6080 | `kea+lan` |  | 2 |
