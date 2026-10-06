# v4 tokenizer segmentation - side by side

8 words, 25 candidates. `silver_gold` is the held-out reference used by Phase 3 selection - **silver, not native gold**. `==` marks an exact whole-word match.

## `sumulat`  ((flagship, no ref gold), tier (custom))

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sum+ulat` |  | 2 |
| plain@8192 | `sum+ulat` |  | 2 |
| plain@16384 | `sumulat` |  | 1 |
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

## `misamban`  ((flagship, no ref gold), tier (custom))

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

## `kabukasan`  ((flagship, no ref gold), tier (custom))

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kab+u+kasan` |  | 3 |
| plain@8192 | `kabu+kasan` |  | 2 |
| plain@16384 | `kabukasan` |  | 1 |
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

## `sinulat`  (infixation, tier A_strong_silver)

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinulat` |  | 1 |
| plain@8192 | `sinulat` |  | 1 |
| plain@16384 | `sinulat` |  | 1 |
| morphbpe@6080 | `sin+ulat` |  | 2 |
| morphbpe@8192 | `sin+ulat` |  | 2 |
| morphbpe@16384 | `sin+ulat` |  | 2 |
| penalty-1@6080 | `s+in+ulat` |  | 3 |
| penalty-1@8192 | `s+in+ulat` |  | 3 |
| penalty-1@16384 | `s+in+ulat` |  | 3 |
| penalty-2@6080 | `s+in+ulat` |  | 3 |
| penalty-2@8192 | `s+in+ulat` |  | 3 |
| penalty-2@16384 | `s+in+ulat` |  | 3 |
| penalty-4@6080 | `s+in+ulat` |  | 3 |
| penalty-4@8192 | `s+in+ulat` |  | 3 |
| penalty-4@16384 | `s+in+ulat` |  | 3 |
| penalty-8@6080 | `s+in+ulat` |  | 3 |
| penalty-8@8192 | `s+in+ulat` |  | 3 |
| penalty-8@16384 | `s+in+ulat` |  | 3 |
| stochastic-p4-d0.1@6080 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.1@8192 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.1@16384 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@6080 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@8192 | `sinu+lat` |  | 2 |
| stochastic-p4-d0.2@16384 | `sinu+lat` |  | 2 |
| unigram-ablation@6080 | `sinulat` |  | 1 |

## `magpakalma`  ((flagship, no ref gold), tier (custom))

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

## `tinuki`  (infixation, tier A_strong_silver)

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tinuki` |  | 1 |
| plain@8192 | `tinuki` |  | 1 |
| plain@16384 | `tinuki` |  | 1 |
| morphbpe@6080 | `tin+uki` |  | 2 |
| morphbpe@8192 | `tin+uki` |  | 2 |
| morphbpe@16384 | `tin+uki` |  | 2 |
| penalty-1@6080 | `t+in+uki` |  | 3 |
| penalty-1@8192 | `t+in+uki` |  | 3 |
| penalty-1@16384 | `t+in+uki` |  | 3 |
| penalty-2@6080 | `t+in+uki` |  | 3 |
| penalty-2@8192 | `t+in+uki` |  | 3 |
| penalty-2@16384 | `t+in+uki` |  | 3 |
| penalty-4@6080 | `tinu+ki` |  | 2 |
| penalty-4@8192 | `tinu+ki` |  | 2 |
| penalty-4@16384 | `tinu+ki` |  | 2 |
| penalty-8@6080 | `t+in+uki` |  | 3 |
| penalty-8@8192 | `t+in+uki` |  | 3 |
| penalty-8@16384 | `t+in+uki` |  | 3 |
| stochastic-p4-d0.1@6080 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.1@8192 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.1@16384 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@6080 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@8192 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@16384 | `t+inu+ki` |  | 3 |
| unigram-ablation@6080 | `tinuki` |  | 1 |

## `pemalagyu`  ((flagship, no ref gold), tier (custom))

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
