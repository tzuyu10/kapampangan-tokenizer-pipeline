# v4 tokenizer segmentation - side by side

534 words, 25 candidates. `silver_gold` is the held-out reference used by Phase 3 selection - **silver, not native gold**. `==` marks an exact whole-word match.

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

## `kapampangan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+pampang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapampangan` |  | 1 |
| plain@8192 | `kapampangan` |  | 1 |
| plain@16384 | `kapampangan` |  | 1 |
| morphbpe@6080 | `kapampangan` |  | 1 |
| morphbpe@8192 | `kapampangan` |  | 1 |
| morphbpe@16384 | `kapampangan` |  | 1 |
| penalty-1@6080 | `kapampangan` |  | 1 |
| penalty-1@8192 | `kapampangan` |  | 1 |
| penalty-1@16384 | `kapampangan` |  | 1 |
| penalty-2@6080 | `kapampangan` |  | 1 |
| penalty-2@8192 | `kapampangan` |  | 1 |
| penalty-2@16384 | `kapampangan` |  | 1 |
| penalty-4@6080 | `kapampangan` |  | 1 |
| penalty-4@8192 | `kapampangan` |  | 1 |
| penalty-4@16384 | `kapampangan` |  | 1 |
| penalty-8@6080 | `kapampangan` |  | 1 |
| penalty-8@8192 | `kapampangan` |  | 1 |
| penalty-8@16384 | `kapampangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapampangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kapampangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapampangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapampangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kapampangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapampangan` |  | 1 |
| unigram-ablation@6080 | `kapampangan` |  | 1 |

## `kapakaluluan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+pakalulu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+akal+uluan` |  | 3 |
| plain@8192 | `kapakaluluan` |  | 1 |
| plain@16384 | `kapakaluluan` |  | 1 |
| morphbpe@6080 | `kap+akal+uluan` |  | 3 |
| morphbpe@8192 | `kapakaluluan` |  | 1 |
| morphbpe@16384 | `kapakaluluan` |  | 1 |
| penalty-1@6080 | `ka+pakal+uluan` |  | 3 |
| penalty-1@8192 | `kapakaluluan` |  | 1 |
| penalty-1@16384 | `kapakaluluan` |  | 1 |
| penalty-2@6080 | `kapa+kalulu+an` |  | 3 |
| penalty-2@8192 | `kapakaluluan` |  | 1 |
| penalty-2@16384 | `kapakaluluan` |  | 1 |
| penalty-4@6080 | `kapa+kalulu+an` |  | 3 |
| penalty-4@8192 | `kapakaluluan` |  | 1 |
| penalty-4@16384 | `kapakaluluan` |  | 1 |
| penalty-8@6080 | `ka+pakalulu+an` | OK | 3 |
| penalty-8@8192 | `kapakaluluan` |  | 1 |
| penalty-8@16384 | `kapakaluluan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapa+kalulu+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapakaluluan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapakaluluan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapa+ka+lulu+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `kapakaluluan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapakaluluan` |  | 1 |
| unigram-ablation@6080 | `ka+pakalulu+an` | OK | 3 |

## `katuliran`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+tulir+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `katuliran` |  | 1 |
| plain@8192 | `katuliran` |  | 1 |
| plain@16384 | `katuliran` |  | 1 |
| morphbpe@6080 | `katuliran` |  | 1 |
| morphbpe@8192 | `katuliran` |  | 1 |
| morphbpe@16384 | `katuliran` |  | 1 |
| penalty-1@6080 | `katuliran` |  | 1 |
| penalty-1@8192 | `katuliran` |  | 1 |
| penalty-1@16384 | `katuliran` |  | 1 |
| penalty-2@6080 | `katuliran` |  | 1 |
| penalty-2@8192 | `katuliran` |  | 1 |
| penalty-2@16384 | `katuliran` |  | 1 |
| penalty-4@6080 | `katuliran` |  | 1 |
| penalty-4@8192 | `katuliran` |  | 1 |
| penalty-4@16384 | `katuliran` |  | 1 |
| penalty-8@6080 | `katuliran` |  | 1 |
| penalty-8@8192 | `katuliran` |  | 1 |
| penalty-8@16384 | `katuliran` |  | 1 |
| stochastic-p4-d0.1@6080 | `katuliran` |  | 1 |
| stochastic-p4-d0.1@8192 | `katuliran` |  | 1 |
| stochastic-p4-d0.1@16384 | `katuliran` |  | 1 |
| stochastic-p4-d0.2@6080 | `katuliran` |  | 1 |
| stochastic-p4-d0.2@8192 | `katuliran` |  | 1 |
| stochastic-p4-d0.2@16384 | `katuliran` |  | 1 |
| unigram-ablation@6080 | `katuliran` |  | 1 |

## `kautusan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+utus+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kautusan` |  | 1 |
| plain@8192 | `kautusan` |  | 1 |
| plain@16384 | `kautusan` |  | 1 |
| morphbpe@6080 | `ka+utus+an` | OK | 3 |
| morphbpe@8192 | `ka+utus+an` | OK | 3 |
| morphbpe@16384 | `ka+utus+an` | OK | 3 |
| penalty-1@6080 | `ka+utus+an` | OK | 3 |
| penalty-1@8192 | `ka+utus+an` | OK | 3 |
| penalty-1@16384 | `ka+utus+an` | OK | 3 |
| penalty-2@6080 | `ka+utus+an` | OK | 3 |
| penalty-2@8192 | `ka+utus+an` | OK | 3 |
| penalty-2@16384 | `ka+utus+an` | OK | 3 |
| penalty-4@6080 | `ka+utus+an` | OK | 3 |
| penalty-4@8192 | `ka+utus+an` | OK | 3 |
| penalty-4@16384 | `ka+utus+an` | OK | 3 |
| penalty-8@6080 | `ka+utus+an` | OK | 3 |
| penalty-8@8192 | `ka+utus+an` | OK | 3 |
| penalty-8@16384 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+utus+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+utus+an` | OK | 3 |
| unigram-ablation@6080 | `kautusan` |  | 1 |

## `panuanan`  (circumfixation, tier A_strong_silver)

**silver gold:** `pa+nuan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+uanan` |  | 2 |
| plain@8192 | `pan+uanan` |  | 2 |
| plain@16384 | `panuanan` |  | 1 |
| morphbpe@6080 | `pan+uanan` |  | 2 |
| morphbpe@8192 | `pan+uanan` |  | 2 |
| morphbpe@16384 | `pan+uanan` |  | 2 |
| penalty-1@6080 | `pan+uanan` |  | 2 |
| penalty-1@8192 | `pan+uanan` |  | 2 |
| penalty-1@16384 | `pan+uanan` |  | 2 |
| penalty-2@6080 | `pan+uanan` |  | 2 |
| penalty-2@8192 | `pan+uanan` |  | 2 |
| penalty-2@16384 | `pan+uanan` |  | 2 |
| penalty-4@6080 | `pan+uanan` |  | 2 |
| penalty-4@8192 | `pan+uanan` |  | 2 |
| penalty-4@16384 | `pan+uanan` |  | 2 |
| penalty-8@6080 | `panu+anan` |  | 2 |
| penalty-8@8192 | `panu+anan` |  | 2 |
| penalty-8@16384 | `panuanan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pan+uan+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `pan+uan+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `pan+uanan` |  | 2 |
| stochastic-p4-d0.2@6080 | `panu+anan` |  | 2 |
| stochastic-p4-d0.2@8192 | `panu+anan` |  | 2 |
| stochastic-p4-d0.2@16384 | `panu+anan` |  | 2 |
| unigram-ablation@6080 | `pan+uanan` |  | 2 |

## `kapurian`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+puri+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapurian` |  | 1 |
| plain@8192 | `kapurian` |  | 1 |
| plain@16384 | `kapurian` |  | 1 |
| morphbpe@6080 | `kapurian` |  | 1 |
| morphbpe@8192 | `kapurian` |  | 1 |
| morphbpe@16384 | `kapurian` |  | 1 |
| penalty-1@6080 | `kapurian` |  | 1 |
| penalty-1@8192 | `kapurian` |  | 1 |
| penalty-1@16384 | `kapurian` |  | 1 |
| penalty-2@6080 | `kapurian` |  | 1 |
| penalty-2@8192 | `kapurian` |  | 1 |
| penalty-2@16384 | `kapurian` |  | 1 |
| penalty-4@6080 | `kapurian` |  | 1 |
| penalty-4@8192 | `kapurian` |  | 1 |
| penalty-4@16384 | `kapurian` |  | 1 |
| penalty-8@6080 | `kapurian` |  | 1 |
| penalty-8@8192 | `kapurian` |  | 1 |
| penalty-8@16384 | `kapurian` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapurian` |  | 1 |
| stochastic-p4-d0.1@8192 | `kapurian` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapurian` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapurian` |  | 1 |
| stochastic-p4-d0.2@8192 | `kapurian` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapurian` |  | 1 |
| unigram-ablation@6080 | `kapuri+an` |  | 2 |

## `kasalanan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+salan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kasalanan` |  | 1 |
| plain@8192 | `kasalanan` |  | 1 |
| plain@16384 | `kasalanan` |  | 1 |
| morphbpe@6080 | `kas+alanan` |  | 2 |
| morphbpe@8192 | `kas+alanan` |  | 2 |
| morphbpe@16384 | `kas+alanan` |  | 2 |
| penalty-1@6080 | `kasal+anan` |  | 2 |
| penalty-1@8192 | `kasal+anan` |  | 2 |
| penalty-1@16384 | `kasal+anan` |  | 2 |
| penalty-2@6080 | `kasal+anan` |  | 2 |
| penalty-2@8192 | `kasal+anan` |  | 2 |
| penalty-2@16384 | `kasal+anan` |  | 2 |
| penalty-4@6080 | `kasal+anan` |  | 2 |
| penalty-4@8192 | `kasal+anan` |  | 2 |
| penalty-4@16384 | `kasal+anan` |  | 2 |
| penalty-8@6080 | `kasal+anan` |  | 2 |
| penalty-8@8192 | `kasal+anan` |  | 2 |
| penalty-8@16384 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.1@6080 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.1@8192 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.2@6080 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.2@8192 | `kasal+anan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kasal+anan` |  | 2 |
| unigram-ablation@6080 | `kasalanan` |  | 1 |

## `pamangan`  (circumfixation, tier A_strong_silver)

**silver gold:** `pa+mang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pamangan` |  | 1 |
| plain@8192 | `pamangan` |  | 1 |
| plain@16384 | `pamangan` |  | 1 |
| morphbpe@6080 | `pamangan` |  | 1 |
| morphbpe@8192 | `pamangan` |  | 1 |
| morphbpe@16384 | `pamangan` |  | 1 |
| penalty-1@6080 | `pamangan` |  | 1 |
| penalty-1@8192 | `pamangan` |  | 1 |
| penalty-1@16384 | `pamangan` |  | 1 |
| penalty-2@6080 | `pamangan` |  | 1 |
| penalty-2@8192 | `pamangan` |  | 1 |
| penalty-2@16384 | `pamangan` |  | 1 |
| penalty-4@6080 | `pamangan` |  | 1 |
| penalty-4@8192 | `pamangan` |  | 1 |
| penalty-4@16384 | `pamangan` |  | 1 |
| penalty-8@6080 | `pamangan` |  | 1 |
| penalty-8@8192 | `pamangan` |  | 1 |
| penalty-8@16384 | `pamangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pamangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `pamangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pamangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pamangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `pamangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `pamangan` |  | 1 |
| unigram-ablation@6080 | `pamangan` |  | 1 |

## `kaligtasan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+ligtas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kaligtasan` |  | 1 |
| plain@8192 | `kaligtasan` |  | 1 |
| plain@16384 | `kaligtasan` |  | 1 |
| morphbpe@6080 | `kal+ig+t+asan` |  | 4 |
| morphbpe@8192 | `kal+ig+t+asan` |  | 4 |
| morphbpe@16384 | `kalig+tasan` |  | 2 |
| penalty-1@6080 | `kal+ig+tas+an` |  | 4 |
| penalty-1@8192 | `kal+igtas+an` |  | 3 |
| penalty-1@16384 | `kal+igtas+an` |  | 3 |
| penalty-2@6080 | `kal+ig+tas+an` |  | 4 |
| penalty-2@8192 | `kal+igtas+an` |  | 3 |
| penalty-2@16384 | `kal+igtas+an` |  | 3 |
| penalty-4@6080 | `kal+ig+tasan` |  | 3 |
| penalty-4@8192 | `kal+ig+tasan` |  | 3 |
| penalty-4@16384 | `kalig+tasan` |  | 2 |
| penalty-8@6080 | `ka+ligtas+an` | OK | 3 |
| penalty-8@8192 | `ka+ligtas+an` | OK | 3 |
| penalty-8@16384 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+ligtas+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+ligtas+an` | OK | 3 |
| unigram-ablation@6080 | `kaligtasan` |  | 1 |

## `kamatayan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+matay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kamatayan` |  | 1 |
| plain@8192 | `kamatayan` |  | 1 |
| plain@16384 | `kamatayan` |  | 1 |
| morphbpe@6080 | `kamatayan` |  | 1 |
| morphbpe@8192 | `kamatayan` |  | 1 |
| morphbpe@16384 | `kamatayan` |  | 1 |
| penalty-1@6080 | `kamatayan` |  | 1 |
| penalty-1@8192 | `kamatayan` |  | 1 |
| penalty-1@16384 | `kamatayan` |  | 1 |
| penalty-2@6080 | `kamatayan` |  | 1 |
| penalty-2@8192 | `kamatayan` |  | 1 |
| penalty-2@16384 | `kamatayan` |  | 1 |
| penalty-4@6080 | `kamatayan` |  | 1 |
| penalty-4@8192 | `kamatayan` |  | 1 |
| penalty-4@16384 | `kamatayan` |  | 1 |
| penalty-8@6080 | `kamatayan` |  | 1 |
| penalty-8@8192 | `kamatayan` |  | 1 |
| penalty-8@16384 | `kamatayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kamatayan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kamatayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kamatayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kamatayan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kamatayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kamatayan` |  | 1 |
| unigram-ablation@6080 | `kamatayan` |  | 1 |

## `pamamilatan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+mamilat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pamamilatan` |  | 1 |
| plain@8192 | `pamamilatan` |  | 1 |
| plain@16384 | `pamamilatan` |  | 1 |
| morphbpe@6080 | `pamam+ilatan` |  | 2 |
| morphbpe@8192 | `pamam+ilatan` |  | 2 |
| morphbpe@16384 | `pamam+ilatan` |  | 2 |
| penalty-1@6080 | `pam+am+ilatan` |  | 3 |
| penalty-1@8192 | `pam+am+ilatan` |  | 3 |
| penalty-1@16384 | `pam+am+ilatan` |  | 3 |
| penalty-2@6080 | `pam+am+ilatan` |  | 3 |
| penalty-2@8192 | `pam+am+ilatan` |  | 3 |
| penalty-2@16384 | `pam+am+ilatan` |  | 3 |
| penalty-4@6080 | `pam+am+ilatan` |  | 3 |
| penalty-4@8192 | `pam+am+ilatan` |  | 3 |
| penalty-4@16384 | `pam+am+ilatan` |  | 3 |
| penalty-8@6080 | `pam+am+ilatan` |  | 3 |
| penalty-8@8192 | `pam+am+ilatan` |  | 3 |
| penalty-8@16384 | `pam+am+ilatan` |  | 3 |
| stochastic-p4-d0.1@6080 | `pam+am+ilatan` |  | 3 |
| stochastic-p4-d0.1@8192 | `pam+am+ilatan` |  | 3 |
| stochastic-p4-d0.1@16384 | `pam+am+ilatan` |  | 3 |
| stochastic-p4-d0.2@6080 | `pam+ami+lat+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `pam+ami+lat+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `pamami+lat+an` |  | 3 |
| unigram-ablation@6080 | `pam+amilatan` |  | 2 |

## `kayanakan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+yanak+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kayanakan` |  | 1 |
| plain@8192 | `kayanakan` |  | 1 |
| plain@16384 | `kayanakan` |  | 1 |
| morphbpe@6080 | `kayanakan` |  | 1 |
| morphbpe@8192 | `kayanakan` |  | 1 |
| morphbpe@16384 | `kayanakan` |  | 1 |
| penalty-1@6080 | `kayanakan` |  | 1 |
| penalty-1@8192 | `kayanakan` |  | 1 |
| penalty-1@16384 | `kayanakan` |  | 1 |
| penalty-2@6080 | `kayanakan` |  | 1 |
| penalty-2@8192 | `kayanakan` |  | 1 |
| penalty-2@16384 | `kayanakan` |  | 1 |
| penalty-4@6080 | `kayanakan` |  | 1 |
| penalty-4@8192 | `kayanakan` |  | 1 |
| penalty-4@16384 | `kayanakan` |  | 1 |
| penalty-8@6080 | `kayanakan` |  | 1 |
| penalty-8@8192 | `kayanakan` |  | 1 |
| penalty-8@16384 | `kayanakan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kayanakan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kayanakan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kayanakan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kayanakan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kayanakan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kayanakan` |  | 1 |
| unigram-ablation@6080 | `kayanakan` |  | 1 |

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

## `katutuan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+tutu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `katutuan` |  | 1 |
| plain@8192 | `katutuan` |  | 1 |
| plain@16384 | `katutuan` |  | 1 |
| morphbpe@6080 | `katut+uan` |  | 2 |
| morphbpe@8192 | `katut+uan` |  | 2 |
| morphbpe@16384 | `katut+uan` |  | 2 |
| penalty-1@6080 | `katut+uan` |  | 2 |
| penalty-1@8192 | `katut+uan` |  | 2 |
| penalty-1@16384 | `katut+uan` |  | 2 |
| penalty-2@6080 | `katut+uan` |  | 2 |
| penalty-2@8192 | `katut+uan` |  | 2 |
| penalty-2@16384 | `katut+uan` |  | 2 |
| penalty-4@6080 | `ka+tutu+an` | OK | 3 |
| penalty-4@8192 | `ka+tutu+an` | OK | 3 |
| penalty-4@16384 | `ka+tutu+an` | OK | 3 |
| penalty-8@6080 | `ka+tutu+an` | OK | 3 |
| penalty-8@8192 | `ka+tutu+an` | OK | 3 |
| penalty-8@16384 | `ka+tutu+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+tutu+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+tutu+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+tutu+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `katu+tu+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `katu+tu+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `katu+tu+an` |  | 3 |
| unigram-ablation@6080 | `katutuan` |  | 1 |

## `pasbulan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pasbul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pas+bulan` |  | 2 |
| plain@8192 | `pas+bulan` |  | 2 |
| plain@16384 | `pasbulan` |  | 1 |
| morphbpe@6080 | `pas+bulan` |  | 2 |
| morphbpe@8192 | `pas+bulan` |  | 2 |
| morphbpe@16384 | `pas+bulan` |  | 2 |
| penalty-1@6080 | `pas+bulan` |  | 2 |
| penalty-1@8192 | `pas+bulan` |  | 2 |
| penalty-1@16384 | `pas+bulan` |  | 2 |
| penalty-2@6080 | `pas+bulan` |  | 2 |
| penalty-2@8192 | `pas+bulan` |  | 2 |
| penalty-2@16384 | `pas+bulan` |  | 2 |
| penalty-4@6080 | `pas+bulan` |  | 2 |
| penalty-4@8192 | `pas+bulan` |  | 2 |
| penalty-4@16384 | `pas+bulan` |  | 2 |
| penalty-8@6080 | `pas+bulan` |  | 2 |
| penalty-8@8192 | `pas+bulan` |  | 2 |
| penalty-8@16384 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.1@6080 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.1@8192 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.1@16384 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.2@6080 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.2@8192 | `pas+bulan` |  | 2 |
| stochastic-p4-d0.2@16384 | `pas+bulan` |  | 2 |
| unigram-ablation@6080 | `pasbul+an` | OK | 2 |

## `kabaldugan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+baldug+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kabaldugan` |  | 1 |
| plain@8192 | `kabaldugan` |  | 1 |
| plain@16384 | `kabaldugan` |  | 1 |
| morphbpe@6080 | `ka+baldug+an` | OK | 3 |
| morphbpe@8192 | `ka+baldug+an` | OK | 3 |
| morphbpe@16384 | `ka+baldugan` |  | 2 |
| penalty-1@6080 | `ka+baldug+an` | OK | 3 |
| penalty-1@8192 | `ka+baldug+an` | OK | 3 |
| penalty-1@16384 | `ka+baldug+an` | OK | 3 |
| penalty-2@6080 | `ka+baldug+an` | OK | 3 |
| penalty-2@8192 | `ka+baldug+an` | OK | 3 |
| penalty-2@16384 | `ka+baldug+an` | OK | 3 |
| penalty-4@6080 | `ka+baldug+an` | OK | 3 |
| penalty-4@8192 | `ka+baldug+an` | OK | 3 |
| penalty-4@16384 | `ka+baldug+an` | OK | 3 |
| penalty-8@6080 | `ka+baldug+an` | OK | 3 |
| penalty-8@8192 | `ka+baldug+an` | OK | 3 |
| penalty-8@16384 | `ka+baldug+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+baldu+gan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+baldu+gan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+baldu+gan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+baldug+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+baldug+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+baldug+an` | OK | 3 |
| unigram-ablation@6080 | `kabaldugan` |  | 1 |

## `kapayapan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+payap+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapayapan` |  | 1 |
| plain@8192 | `kapayapan` |  | 1 |
| plain@16384 | `kapayapan` |  | 1 |
| morphbpe@6080 | `kapayapan` |  | 1 |
| morphbpe@8192 | `kapayapan` |  | 1 |
| morphbpe@16384 | `kapayapan` |  | 1 |
| penalty-1@6080 | `kapayapan` |  | 1 |
| penalty-1@8192 | `kapayapan` |  | 1 |
| penalty-1@16384 | `kapayapan` |  | 1 |
| penalty-2@6080 | `kapayapan` |  | 1 |
| penalty-2@8192 | `kapayapan` |  | 1 |
| penalty-2@16384 | `kapayapan` |  | 1 |
| penalty-4@6080 | `kapayapan` |  | 1 |
| penalty-4@8192 | `kapayapan` |  | 1 |
| penalty-4@16384 | `kapayapan` |  | 1 |
| penalty-8@6080 | `kapayapan` |  | 1 |
| penalty-8@8192 | `kapayapan` |  | 1 |
| penalty-8@16384 | `kapayapan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapayapan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kapayapan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapayapan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapayapan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kapayapan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapayapan` |  | 1 |
| unigram-ablation@6080 | `kapayapan` |  | 1 |

## `kasakitan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+sakit+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kasakitan` |  | 1 |
| plain@8192 | `kasakitan` |  | 1 |
| plain@16384 | `kasakitan` |  | 1 |
| morphbpe@6080 | `kas+akit+an` |  | 3 |
| morphbpe@8192 | `kas+akitan` |  | 2 |
| morphbpe@16384 | `kas+akitan` |  | 2 |
| penalty-1@6080 | `kas+akit+an` |  | 3 |
| penalty-1@8192 | `kas+akit+an` |  | 3 |
| penalty-1@16384 | `kasakit+an` |  | 2 |
| penalty-2@6080 | `kas+akit+an` |  | 3 |
| penalty-2@8192 | `kas+akit+an` |  | 3 |
| penalty-2@16384 | `kasakit+an` |  | 2 |
| penalty-4@6080 | `ka+sakit+an` | OK | 3 |
| penalty-4@8192 | `ka+sakit+an` | OK | 3 |
| penalty-4@16384 | `ka+sakit+an` | OK | 3 |
| penalty-8@6080 | `ka+sakit+an` | OK | 3 |
| penalty-8@8192 | `ka+sakit+an` | OK | 3 |
| penalty-8@16384 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+sakit+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+sakit+an` | OK | 3 |
| unigram-ablation@6080 | `kasakit+an` |  | 2 |

## `panintunan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pan+intun+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `panintunan` |  | 1 |
| plain@8192 | `panintunan` |  | 1 |
| plain@16384 | `panintunan` |  | 1 |
| morphbpe@6080 | `pan+int+unan` |  | 3 |
| morphbpe@8192 | `pan+int+unan` |  | 3 |
| morphbpe@16384 | `pan+intunan` |  | 2 |
| penalty-1@6080 | `pan+intun+an` | OK | 3 |
| penalty-1@8192 | `pan+intun+an` | OK | 3 |
| penalty-1@16384 | `pan+intun+an` | OK | 3 |
| penalty-2@6080 | `pan+intun+an` | OK | 3 |
| penalty-2@8192 | `pan+intun+an` | OK | 3 |
| penalty-2@16384 | `pan+intun+an` | OK | 3 |
| penalty-4@6080 | `pan+intun+an` | OK | 3 |
| penalty-4@8192 | `pan+intun+an` | OK | 3 |
| penalty-4@16384 | `pan+intun+an` | OK | 3 |
| penalty-8@6080 | `pan+intun+an` | OK | 3 |
| penalty-8@8192 | `pan+intun+an` | OK | 3 |
| penalty-8@16384 | `pan+intun+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `pan+intun+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `pan+intun+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `pan+intun+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `p+an+intun+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `p+an+intun+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `p+an+intun+an` |  | 4 |
| unigram-ablation@6080 | `panintuna+n` |  | 2 |

## `palsintan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+lsint+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pal+sintan` |  | 2 |
| plain@8192 | `palsintan` |  | 1 |
| plain@16384 | `palsintan` |  | 1 |
| morphbpe@6080 | `pal+sintan` |  | 2 |
| morphbpe@8192 | `palsintan` |  | 1 |
| morphbpe@16384 | `palsintan` |  | 1 |
| penalty-1@6080 | `pal+sintan` |  | 2 |
| penalty-1@8192 | `palsintan` |  | 1 |
| penalty-1@16384 | `palsintan` |  | 1 |
| penalty-2@6080 | `pal+sintan` |  | 2 |
| penalty-2@8192 | `palsintan` |  | 1 |
| penalty-2@16384 | `palsintan` |  | 1 |
| penalty-4@6080 | `pal+sintan` |  | 2 |
| penalty-4@8192 | `palsintan` |  | 1 |
| penalty-4@16384 | `palsintan` |  | 1 |
| penalty-8@6080 | `palsintan` |  | 1 |
| penalty-8@8192 | `palsintan` |  | 1 |
| penalty-8@16384 | `palsintan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pal+sintan` |  | 2 |
| stochastic-p4-d0.1@8192 | `palsintan` |  | 1 |
| stochastic-p4-d0.1@16384 | `palsintan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pals+int+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `palsintan` |  | 1 |
| stochastic-p4-d0.2@16384 | `palsintan` |  | 1 |
| unigram-ablation@6080 | `palsintan` |  | 1 |

## `kanuanan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+nuan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kanu+anan` |  | 2 |
| plain@8192 | `kanu+anan` |  | 2 |
| plain@16384 | `kanuanan` |  | 1 |
| morphbpe@6080 | `kan+uanan` |  | 2 |
| morphbpe@8192 | `kan+uanan` |  | 2 |
| morphbpe@16384 | `kan+uanan` |  | 2 |
| penalty-1@6080 | `kan+uanan` |  | 2 |
| penalty-1@8192 | `kan+uanan` |  | 2 |
| penalty-1@16384 | `kan+uanan` |  | 2 |
| penalty-2@6080 | `kan+uanan` |  | 2 |
| penalty-2@8192 | `kan+uanan` |  | 2 |
| penalty-2@16384 | `kan+uanan` |  | 2 |
| penalty-4@6080 | `kan+uanan` |  | 2 |
| penalty-4@8192 | `kan+uanan` |  | 2 |
| penalty-4@16384 | `kan+uanan` |  | 2 |
| penalty-8@6080 | `kan+uan+an` |  | 3 |
| penalty-8@8192 | `kan+uanan` |  | 2 |
| penalty-8@16384 | `kan+uanan` |  | 2 |
| stochastic-p4-d0.1@6080 | `kan+uan+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kan+uan+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kan+uanan` |  | 2 |
| stochastic-p4-d0.2@6080 | `kanu+anan` |  | 2 |
| stochastic-p4-d0.2@8192 | `kanu+anan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kanu+anan` |  | 2 |
| unigram-ablation@6080 | `kan+uanan` |  | 2 |

## `katapatan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+tapat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kat+apatan` |  | 2 |
| plain@8192 | `katapatan` |  | 1 |
| plain@16384 | `katapatan` |  | 1 |
| morphbpe@6080 | `kat+apatan` |  | 2 |
| morphbpe@8192 | `katapatan` |  | 1 |
| morphbpe@16384 | `katapatan` |  | 1 |
| penalty-1@6080 | `kat+apatan` |  | 2 |
| penalty-1@8192 | `katapatan` |  | 1 |
| penalty-1@16384 | `katapatan` |  | 1 |
| penalty-2@6080 | `kat+apatan` |  | 2 |
| penalty-2@8192 | `katapatan` |  | 1 |
| penalty-2@16384 | `katapatan` |  | 1 |
| penalty-4@6080 | `kata+patan` |  | 2 |
| penalty-4@8192 | `katapatan` |  | 1 |
| penalty-4@16384 | `katapatan` |  | 1 |
| penalty-8@6080 | `ka+ta+patan` |  | 3 |
| penalty-8@8192 | `katapatan` |  | 1 |
| penalty-8@16384 | `katapatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kata+pat+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `katapatan` |  | 1 |
| stochastic-p4-d0.1@16384 | `katapatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kata+pat+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `katapatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `katapatan` |  | 1 |
| unigram-ablation@6080 | `katapatan` |  | 1 |

## `kawatasan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+watas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kawat+asan` |  | 2 |
| plain@8192 | `kawatasan` |  | 1 |
| plain@16384 | `kawatasan` |  | 1 |
| morphbpe@6080 | `kawat+asan` |  | 2 |
| morphbpe@8192 | `kawatasan` |  | 1 |
| morphbpe@16384 | `kawatasan` |  | 1 |
| penalty-1@6080 | `kawat+asan` |  | 2 |
| penalty-1@8192 | `kawatasan` |  | 1 |
| penalty-1@16384 | `kawatasan` |  | 1 |
| penalty-2@6080 | `ka+watasan` |  | 2 |
| penalty-2@8192 | `kawatasan` |  | 1 |
| penalty-2@16384 | `kawatasan` |  | 1 |
| penalty-4@6080 | `kawat+asan` |  | 2 |
| penalty-4@8192 | `kawatasan` |  | 1 |
| penalty-4@16384 | `kawatasan` |  | 1 |
| penalty-8@6080 | `kawatasan` |  | 1 |
| penalty-8@8192 | `kawatasan` |  | 1 |
| penalty-8@16384 | `kawatasan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kawat+asan` |  | 2 |
| stochastic-p4-d0.1@8192 | `kawatasan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kawatasan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+wat+asan` |  | 3 |
| stochastic-p4-d0.2@8192 | `kawatasan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kawatasan` |  | 1 |
| unigram-ablation@6080 | `kawatasan` |  | 1 |

## `kabiasnan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+biasn+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kabiasnan` |  | 1 |
| plain@8192 | `kabiasnan` |  | 1 |
| plain@16384 | `kabiasnan` |  | 1 |
| morphbpe@6080 | `kabiasnan` |  | 1 |
| morphbpe@8192 | `kabiasnan` |  | 1 |
| morphbpe@16384 | `kabiasnan` |  | 1 |
| penalty-1@6080 | `kabiasnan` |  | 1 |
| penalty-1@8192 | `kabiasnan` |  | 1 |
| penalty-1@16384 | `kabiasnan` |  | 1 |
| penalty-2@6080 | `kabiasnan` |  | 1 |
| penalty-2@8192 | `kabiasnan` |  | 1 |
| penalty-2@16384 | `kabiasnan` |  | 1 |
| penalty-4@6080 | `kabiasnan` |  | 1 |
| penalty-4@8192 | `kabiasnan` |  | 1 |
| penalty-4@16384 | `kabiasnan` |  | 1 |
| penalty-8@6080 | `kabiasnan` |  | 1 |
| penalty-8@8192 | `kabiasnan` |  | 1 |
| penalty-8@16384 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kabiasnan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kabiasnan` |  | 1 |
| unigram-ablation@6080 | `kabiasnan` |  | 1 |

## `panimanman`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pani+manman`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `panimanman` |  | 1 |
| plain@8192 | `panimanman` |  | 1 |
| plain@16384 | `panimanman` |  | 1 |
| morphbpe@6080 | `panimanman` |  | 1 |
| morphbpe@8192 | `panimanman` |  | 1 |
| morphbpe@16384 | `panimanman` |  | 1 |
| penalty-1@6080 | `panimanman` |  | 1 |
| penalty-1@8192 | `panimanman` |  | 1 |
| penalty-1@16384 | `panimanman` |  | 1 |
| penalty-2@6080 | `panimanman` |  | 1 |
| penalty-2@8192 | `panimanman` |  | 1 |
| penalty-2@16384 | `panimanman` |  | 1 |
| penalty-4@6080 | `panimanman` |  | 1 |
| penalty-4@8192 | `panimanman` |  | 1 |
| penalty-4@16384 | `panimanman` |  | 1 |
| penalty-8@6080 | `panimanman` |  | 1 |
| penalty-8@8192 | `panimanman` |  | 1 |
| penalty-8@16384 | `panimanman` |  | 1 |
| stochastic-p4-d0.1@6080 | `panimanman` |  | 1 |
| stochastic-p4-d0.1@8192 | `panimanman` |  | 1 |
| stochastic-p4-d0.1@16384 | `panimanman` |  | 1 |
| stochastic-p4-d0.2@6080 | `panimanman` |  | 1 |
| stochastic-p4-d0.2@8192 | `panimanman` |  | 1 |
| stochastic-p4-d0.2@16384 | `panimanman` |  | 1 |
| unigram-ablation@6080 | `panimanman` |  | 1 |

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

## `kaligaligan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+ligalig+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+ig+aligan` |  | 3 |
| plain@8192 | `kal+ig+aligan` |  | 3 |
| plain@16384 | `kaligaligan` |  | 1 |
| morphbpe@6080 | `kal+ig+aligan` |  | 3 |
| morphbpe@8192 | `kal+ig+aligan` |  | 3 |
| morphbpe@16384 | `kaligaligan` |  | 1 |
| penalty-1@6080 | `kal+ig+aligan` |  | 3 |
| penalty-1@8192 | `kal+ig+aligan` |  | 3 |
| penalty-1@16384 | `kaligaligan` |  | 1 |
| penalty-2@6080 | `kal+ig+aligan` |  | 3 |
| penalty-2@8192 | `kal+ig+aligan` |  | 3 |
| penalty-2@16384 | `kaligaligan` |  | 1 |
| penalty-4@6080 | `kal+ig+aligan` |  | 3 |
| penalty-4@8192 | `kal+ig+aligan` |  | 3 |
| penalty-4@16384 | `kaligaligan` |  | 1 |
| penalty-8@6080 | `ka+lig+aligan` |  | 3 |
| penalty-8@8192 | `ka+ligaligan` |  | 2 |
| penalty-8@16384 | `kaligaligan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+lig+aligan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+lig+aligan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kaligaligan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+lig+aligan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+ligaligan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kaligaligan` |  | 1 |
| unigram-ablation@6080 | `ka+ligalig+an` | OK | 3 |

## `kaisipan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+isip+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kaisipan` |  | 1 |
| plain@8192 | `kaisipan` |  | 1 |
| plain@16384 | `kaisipan` |  | 1 |
| morphbpe@6080 | `ka+isip+an` | OK | 3 |
| morphbpe@8192 | `ka+isip+an` | OK | 3 |
| morphbpe@16384 | `ka+isipan` |  | 2 |
| penalty-1@6080 | `ka+isip+an` | OK | 3 |
| penalty-1@8192 | `ka+isip+an` | OK | 3 |
| penalty-1@16384 | `ka+isip+an` | OK | 3 |
| penalty-2@6080 | `ka+isip+an` | OK | 3 |
| penalty-2@8192 | `ka+isip+an` | OK | 3 |
| penalty-2@16384 | `ka+isip+an` | OK | 3 |
| penalty-4@6080 | `ka+isip+an` | OK | 3 |
| penalty-4@8192 | `ka+isip+an` | OK | 3 |
| penalty-4@16384 | `ka+isip+an` | OK | 3 |
| penalty-8@6080 | `ka+isi+pan` |  | 3 |
| penalty-8@8192 | `ka+isi+pan` |  | 3 |
| penalty-8@16384 | `ka+isipan` |  | 2 |
| stochastic-p4-d0.1@6080 | `ka+isi+pan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+isi+pan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+isipan` |  | 2 |
| stochastic-p4-d0.2@6080 | `ka+isip+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+isip+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+isip+an` | OK | 3 |
| unigram-ablation@6080 | `kaisipan` |  | 1 |

## `kayatulan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+yatul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kay+atulan` |  | 2 |
| plain@8192 | `kay+atulan` |  | 2 |
| plain@16384 | `kayatulan` |  | 1 |
| morphbpe@6080 | `kay+at+ulan` |  | 3 |
| morphbpe@8192 | `kayat+ulan` |  | 2 |
| morphbpe@16384 | `kayatulan` |  | 1 |
| penalty-1@6080 | `kay+atul+an` |  | 3 |
| penalty-1@8192 | `kay+atul+an` |  | 3 |
| penalty-1@16384 | `kayatulan` |  | 1 |
| penalty-2@6080 | `ka+yat+ulan` |  | 3 |
| penalty-2@8192 | `ka+yatulan` |  | 2 |
| penalty-2@16384 | `kayatulan` |  | 1 |
| penalty-4@6080 | `ka+yatul+an` | OK | 3 |
| penalty-4@8192 | `ka+yatulan` |  | 2 |
| penalty-4@16384 | `kayatulan` |  | 1 |
| penalty-8@6080 | `ka+yat+ulan` |  | 3 |
| penalty-8@8192 | `ka+yatulan` |  | 2 |
| penalty-8@16384 | `kayatulan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kay+atul+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kay+atul+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kayatulan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kay+at+ul+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `kay+at+ul+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `kayatulan` |  | 1 |
| unigram-ablation@6080 | `ka+y+atulan` |  | 3 |

## `kalalaman`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+lalam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+al+aman` |  | 3 |
| plain@8192 | `kal+al+aman` |  | 3 |
| plain@16384 | `kalalaman` |  | 1 |
| morphbpe@6080 | `kal+al+aman` |  | 3 |
| morphbpe@8192 | `kal+al+aman` |  | 3 |
| morphbpe@16384 | `kal+al+aman` |  | 3 |
| penalty-1@6080 | `kal+al+aman` |  | 3 |
| penalty-1@8192 | `kal+al+aman` |  | 3 |
| penalty-1@16384 | `kal+al+aman` |  | 3 |
| penalty-2@6080 | `kal+al+aman` |  | 3 |
| penalty-2@8192 | `kal+al+aman` |  | 3 |
| penalty-2@16384 | `kal+al+aman` |  | 3 |
| penalty-4@6080 | `kal+al+aman` |  | 3 |
| penalty-4@8192 | `kal+al+aman` |  | 3 |
| penalty-4@16384 | `kal+al+aman` |  | 3 |
| penalty-8@6080 | `ka+lala+man` |  | 3 |
| penalty-8@8192 | `ka+lala+man` |  | 3 |
| penalty-8@16384 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.1@6080 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+lala+man` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+lala+man` |  | 3 |
| unigram-ablation@6080 | `ka+lalam+an` | OK | 3 |

## `pakibatan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pakibat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pak+ibatan` |  | 2 |
| plain@8192 | `pak+ibatan` |  | 2 |
| plain@16384 | `pakibatan` |  | 1 |
| morphbpe@6080 | `pak+ibatan` |  | 2 |
| morphbpe@8192 | `pak+ibatan` |  | 2 |
| morphbpe@16384 | `pak+ibatan` |  | 2 |
| penalty-1@6080 | `pakibat+an` | OK | 2 |
| penalty-1@8192 | `pakibat+an` | OK | 2 |
| penalty-1@16384 | `pakibat+an` | OK | 2 |
| penalty-2@6080 | `pakibat+an` | OK | 2 |
| penalty-2@8192 | `pakibat+an` | OK | 2 |
| penalty-2@16384 | `pakibat+an` | OK | 2 |
| penalty-4@6080 | `pakibat+an` | OK | 2 |
| penalty-4@8192 | `pakibat+an` | OK | 2 |
| penalty-4@16384 | `pakibat+an` | OK | 2 |
| penalty-8@6080 | `pakibat+an` | OK | 2 |
| penalty-8@8192 | `pakibat+an` | OK | 2 |
| penalty-8@16384 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pakibat+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `pakibat+an` | OK | 2 |
| unigram-ablation@6080 | `pakibat+an` | OK | 2 |

## `pagkeran`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+gker+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+ker+an` |  | 3 |
| plain@8192 | `pag+ker+an` |  | 3 |
| plain@16384 | `pagkeran` |  | 1 |
| morphbpe@6080 | `pag+ker+an` |  | 3 |
| morphbpe@8192 | `pag+ker+an` |  | 3 |
| morphbpe@16384 | `pag+ker+an` |  | 3 |
| penalty-1@6080 | `pag+ker+an` |  | 3 |
| penalty-1@8192 | `pag+ker+an` |  | 3 |
| penalty-1@16384 | `pag+ker+an` |  | 3 |
| penalty-2@6080 | `pag+ker+an` |  | 3 |
| penalty-2@8192 | `pag+ker+an` |  | 3 |
| penalty-2@16384 | `pag+ker+an` |  | 3 |
| penalty-4@6080 | `pag+ker+an` |  | 3 |
| penalty-4@8192 | `pag+ker+an` |  | 3 |
| penalty-4@16384 | `pag+ker+an` |  | 3 |
| penalty-8@6080 | `pag+ker+an` |  | 3 |
| penalty-8@8192 | `pag+ker+an` |  | 3 |
| penalty-8@16384 | `pag+ker+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `pag+ker+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `pag+ker+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `pag+ker+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `pag+k+er+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `pag+ker+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `pag+ker+an` |  | 3 |
| unigram-ablation@6080 | `pagkera+n` |  | 2 |

## `kalibakan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+libak+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kalib+akan` |  | 2 |
| plain@8192 | `kalib+akan` |  | 2 |
| plain@16384 | `kalib+akan` |  | 2 |
| morphbpe@6080 | `kal+ib+akan` |  | 3 |
| morphbpe@8192 | `kal+ib+akan` |  | 3 |
| morphbpe@16384 | `kalibakan` |  | 1 |
| penalty-1@6080 | `kal+ib+akan` |  | 3 |
| penalty-1@8192 | `kal+ib+akan` |  | 3 |
| penalty-1@16384 | `kalibakan` |  | 1 |
| penalty-2@6080 | `kal+ib+akan` |  | 3 |
| penalty-2@8192 | `kal+ib+akan` |  | 3 |
| penalty-2@16384 | `kalibakan` |  | 1 |
| penalty-4@6080 | `k+ali+ba+kan` |  | 4 |
| penalty-4@8192 | `k+ali+bakan` |  | 3 |
| penalty-4@16384 | `kalibakan` |  | 1 |
| penalty-8@6080 | `ka+li+ba+kan` |  | 4 |
| penalty-8@8192 | `kali+bakan` |  | 2 |
| penalty-8@16384 | `kalibakan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+li+ba+kan` |  | 4 |
| stochastic-p4-d0.1@8192 | `ka+li+bakan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kalibakan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+li+ba+kan` |  | 4 |
| stochastic-p4-d0.2@8192 | `kali+ba+kan` |  | 3 |
| stochastic-p4-d0.2@16384 | `kali+ba+kan` |  | 3 |
| unigram-ablation@6080 | `ka+li+bak+an` |  | 4 |

## `kayarian`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+yari+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kayarian` |  | 1 |
| plain@8192 | `kayarian` |  | 1 |
| plain@16384 | `kayarian` |  | 1 |
| morphbpe@6080 | `kayarian` |  | 1 |
| morphbpe@8192 | `kayarian` |  | 1 |
| morphbpe@16384 | `kayarian` |  | 1 |
| penalty-1@6080 | `kayarian` |  | 1 |
| penalty-1@8192 | `kayarian` |  | 1 |
| penalty-1@16384 | `kayarian` |  | 1 |
| penalty-2@6080 | `kayarian` |  | 1 |
| penalty-2@8192 | `kayarian` |  | 1 |
| penalty-2@16384 | `kayarian` |  | 1 |
| penalty-4@6080 | `kayarian` |  | 1 |
| penalty-4@8192 | `kayarian` |  | 1 |
| penalty-4@16384 | `kayarian` |  | 1 |
| penalty-8@6080 | `kayarian` |  | 1 |
| penalty-8@8192 | `kayarian` |  | 1 |
| penalty-8@16384 | `kayarian` |  | 1 |
| stochastic-p4-d0.1@6080 | `kayarian` |  | 1 |
| stochastic-p4-d0.1@8192 | `kayarian` |  | 1 |
| stochastic-p4-d0.1@16384 | `kayarian` |  | 1 |
| stochastic-p4-d0.2@6080 | `kayarian` |  | 1 |
| stochastic-p4-d0.2@8192 | `kayarian` |  | 1 |
| stochastic-p4-d0.2@16384 | `kayarian` |  | 1 |
| unigram-ablation@6080 | `kayari+an` |  | 2 |

## `kagutgutan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+gutgut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kag+ut+g+utan` |  | 4 |
| plain@8192 | `kag+ut+g+utan` |  | 4 |
| plain@16384 | `kagutgutan` |  | 1 |
| morphbpe@6080 | `kag+ut+g+utan` |  | 4 |
| morphbpe@8192 | `kag+ut+g+utan` |  | 4 |
| morphbpe@16384 | `kagutgutan` |  | 1 |
| penalty-1@6080 | `ka+g+ut+g+utan` |  | 5 |
| penalty-1@8192 | `kag+ut+g+utan` |  | 4 |
| penalty-1@16384 | `kagutgutan` |  | 1 |
| penalty-2@6080 | `kag+ut+g+utan` |  | 4 |
| penalty-2@8192 | `kag+ut+g+utan` |  | 4 |
| penalty-2@16384 | `kagutgutan` |  | 1 |
| penalty-4@6080 | `ka+gut+gut+an` |  | 4 |
| penalty-4@8192 | `ka+gut+gut+an` |  | 4 |
| penalty-4@16384 | `kagutgutan` |  | 1 |
| penalty-8@6080 | `ka+gut+gu+tan` |  | 4 |
| penalty-8@8192 | `ka+gut+gu+tan` |  | 4 |
| penalty-8@16384 | `kagutgutan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+gut+gu+tan` |  | 4 |
| stochastic-p4-d0.1@8192 | `ka+gut+gu+tan` |  | 4 |
| stochastic-p4-d0.1@16384 | `kagutgutan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+gut+gu+tan` |  | 4 |
| stochastic-p4-d0.2@8192 | `ka+gut+gu+tan` |  | 4 |
| stochastic-p4-d0.2@16384 | `kagutgutan` |  | 1 |
| unigram-ablation@6080 | `ka+gut+gut+an` |  | 4 |

## `kalinguan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+lingu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+inguan` |  | 2 |
| plain@8192 | `kal+inguan` |  | 2 |
| plain@16384 | `kalinguan` |  | 1 |
| morphbpe@6080 | `kaling+uan` |  | 2 |
| morphbpe@8192 | `kalinguan` |  | 1 |
| morphbpe@16384 | `kalinguan` |  | 1 |
| penalty-1@6080 | `kaling+uan` |  | 2 |
| penalty-1@8192 | `kalinguan` |  | 1 |
| penalty-1@16384 | `kalinguan` |  | 1 |
| penalty-2@6080 | `kaling+uan` |  | 2 |
| penalty-2@8192 | `kalinguan` |  | 1 |
| penalty-2@16384 | `kalinguan` |  | 1 |
| penalty-4@6080 | `kaling+uan` |  | 2 |
| penalty-4@8192 | `kalinguan` |  | 1 |
| penalty-4@16384 | `kalinguan` |  | 1 |
| penalty-8@6080 | `ka+linguan` |  | 2 |
| penalty-8@8192 | `kalinguan` |  | 1 |
| penalty-8@16384 | `kalinguan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.1@8192 | `kalinguan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kalinguan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.2@8192 | `kali+ng+uan` |  | 3 |
| stochastic-p4-d0.2@16384 | `kalinguan` |  | 1 |
| unigram-ablation@6080 | `kalingu+an` |  | 2 |

## `kakataskatasan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+kataskatas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ka+katas+katasan` |  | 3 |
| plain@8192 | `ka+katas+katasan` |  | 3 |
| plain@16384 | `kakataskatasan` |  | 1 |
| morphbpe@6080 | `ka+kat+as+katasan` |  | 4 |
| morphbpe@8192 | `kakat+as+katasan` |  | 3 |
| morphbpe@16384 | `kakataskatasan` |  | 1 |
| penalty-1@6080 | `ka+kat+as+katasan` |  | 4 |
| penalty-1@8192 | `kakat+as+katasan` |  | 3 |
| penalty-1@16384 | `kakataskatasan` |  | 1 |
| penalty-2@6080 | `ka+kat+as+katasan` |  | 4 |
| penalty-2@8192 | `kakat+as+katasan` |  | 3 |
| penalty-2@16384 | `kakataskatasan` |  | 1 |
| penalty-4@6080 | `ka+ka+tas+katasan` |  | 4 |
| penalty-4@8192 | `ka+kataskatasan` |  | 2 |
| penalty-4@16384 | `kakataskatasan` |  | 1 |
| penalty-8@6080 | `ka+ka+tas+ka+tas+an` |  | 6 |
| penalty-8@8192 | `ka+kataskatasan` |  | 2 |
| penalty-8@16384 | `kakataskatasan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+ka+tas+ka+tas+an` |  | 6 |
| stochastic-p4-d0.1@8192 | `ka+ka+tas+ka+tas+an` |  | 6 |
| stochastic-p4-d0.1@16384 | `kakataskatasan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+ka+tas+ka+tasan` |  | 5 |
| stochastic-p4-d0.2@8192 | `ka+ka+tas+ka+tasan` |  | 5 |
| stochastic-p4-d0.2@16384 | `kakataskatasan` |  | 1 |
| unigram-ablation@6080 | `k+akataskatasan` |  | 2 |

## `kamarinayan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+marinay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ka+mar+in+ayan` |  | 4 |
| plain@8192 | `ka+mar+in+ayan` |  | 4 |
| plain@16384 | `kamarinayan` |  | 1 |
| morphbpe@6080 | `ka+mar+in+ayan` |  | 4 |
| morphbpe@8192 | `ka+mar+in+ayan` |  | 4 |
| morphbpe@16384 | `kamarinayan` |  | 1 |
| penalty-1@6080 | `ka+mar+in+ayan` |  | 4 |
| penalty-1@8192 | `ka+mar+inayan` |  | 3 |
| penalty-1@16384 | `kamarinayan` |  | 1 |
| penalty-2@6080 | `ka+marin+ayan` |  | 3 |
| penalty-2@8192 | `ka+marin+ayan` |  | 3 |
| penalty-2@16384 | `kamarinayan` |  | 1 |
| penalty-4@6080 | `ka+marin+ayan` |  | 3 |
| penalty-4@8192 | `ka+marin+ayan` |  | 3 |
| penalty-4@16384 | `kamarinayan` |  | 1 |
| penalty-8@6080 | `ka+marin+ayan` |  | 3 |
| penalty-8@8192 | `ka+marin+ayan` |  | 3 |
| penalty-8@16384 | `kamarinayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+marin+ayan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+marin+ayan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kamarinayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+marin+ayan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+marin+ayan` |  | 3 |
| stochastic-p4-d0.2@16384 | `kamarinayan` |  | 1 |
| unigram-ablation@6080 | `ka+ma+rin+ayan` |  | 4 |

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

## `kayupayan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+yupay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kayupayan` |  | 1 |
| plain@8192 | `kayupayan` |  | 1 |
| plain@16384 | `kayupayan` |  | 1 |
| morphbpe@6080 | `kayupayan` |  | 1 |
| morphbpe@8192 | `kayupayan` |  | 1 |
| morphbpe@16384 | `kayupayan` |  | 1 |
| penalty-1@6080 | `kayupayan` |  | 1 |
| penalty-1@8192 | `kayupayan` |  | 1 |
| penalty-1@16384 | `kayupayan` |  | 1 |
| penalty-2@6080 | `kayupayan` |  | 1 |
| penalty-2@8192 | `kayupayan` |  | 1 |
| penalty-2@16384 | `kayupayan` |  | 1 |
| penalty-4@6080 | `kayupayan` |  | 1 |
| penalty-4@8192 | `kayupayan` |  | 1 |
| penalty-4@16384 | `kayupayan` |  | 1 |
| penalty-8@6080 | `kayupayan` |  | 1 |
| penalty-8@8192 | `kayupayan` |  | 1 |
| penalty-8@16384 | `kayupayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kayupayan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kayupayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kayupayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kayupayan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kayupayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kayupayan` |  | 1 |
| unigram-ablation@6080 | `kayupaya+n` |  | 2 |

## `pamintuan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+mintu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pam+intuan` |  | 2 |
| plain@8192 | `pam+intuan` |  | 2 |
| plain@16384 | `pamintuan` |  | 1 |
| morphbpe@6080 | `pamintuan` |  | 1 |
| morphbpe@8192 | `pamintuan` |  | 1 |
| morphbpe@16384 | `pamintuan` |  | 1 |
| penalty-1@6080 | `pamintuan` |  | 1 |
| penalty-1@8192 | `pamintuan` |  | 1 |
| penalty-1@16384 | `pamintuan` |  | 1 |
| penalty-2@6080 | `pamintuan` |  | 1 |
| penalty-2@8192 | `pamintuan` |  | 1 |
| penalty-2@16384 | `pamintuan` |  | 1 |
| penalty-4@6080 | `pamintuan` |  | 1 |
| penalty-4@8192 | `pamintuan` |  | 1 |
| penalty-4@16384 | `pamintuan` |  | 1 |
| penalty-8@6080 | `pamintuan` |  | 1 |
| penalty-8@8192 | `pamintuan` |  | 1 |
| penalty-8@16384 | `pamintuan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pam+intuan` |  | 2 |
| stochastic-p4-d0.1@8192 | `pamintuan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pamintuan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pam+intu+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `pam+intuan` |  | 2 |
| stochastic-p4-d0.2@16384 | `pamintuan` |  | 1 |
| unigram-ablation@6080 | `pamintu+an` |  | 2 |

## `kapasalamatan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+pa+salamat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+as+alamatan` |  | 3 |
| plain@8192 | `kapas+alamatan` |  | 2 |
| plain@16384 | `kapasalamatan` |  | 1 |
| morphbpe@6080 | `kap+asal+am+atan` |  | 4 |
| morphbpe@8192 | `kap+asal+am+atan` |  | 4 |
| morphbpe@16384 | `kapasalamatan` |  | 1 |
| penalty-1@6080 | `ka+pas+alam+atan` |  | 4 |
| penalty-1@8192 | `kapas+alam+atan` |  | 3 |
| penalty-1@16384 | `kapasalamatan` |  | 1 |
| penalty-2@6080 | `kapa+sal+am+atan` |  | 4 |
| penalty-2@8192 | `kapa+salam+atan` |  | 3 |
| penalty-2@16384 | `kapasalamatan` |  | 1 |
| penalty-4@6080 | `kapa+sal+am+atan` |  | 4 |
| penalty-4@8192 | `kapa+salam+atan` |  | 3 |
| penalty-4@16384 | `kapasalamatan` |  | 1 |
| penalty-8@6080 | `ka+pa+salamat+an` | OK | 4 |
| penalty-8@8192 | `ka+pa+salamat+an` | OK | 4 |
| penalty-8@16384 | `kapasalamatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapa+salamat+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapa+salamat+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kapasalamatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapa+salamat+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kapa+salamat+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `kapasalamatan` |  | 1 |
| unigram-ablation@6080 | `ka+pasalamat+an` |  | 3 |

## `kapupusan`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+pupus+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+up+usan` |  | 3 |
| plain@8192 | `kapup+usan` |  | 2 |
| plain@16384 | `kapupusan` |  | 1 |
| morphbpe@6080 | `kap+up+usan` |  | 3 |
| morphbpe@8192 | `kapup+usan` |  | 2 |
| morphbpe@16384 | `kapupusan` |  | 1 |
| penalty-1@6080 | `kap+up+usan` |  | 3 |
| penalty-1@8192 | `kapup+usan` |  | 2 |
| penalty-1@16384 | `kapupusan` |  | 1 |
| penalty-2@6080 | `ka+pupus+an` | OK | 3 |
| penalty-2@8192 | `ka+pupus+an` | OK | 3 |
| penalty-2@16384 | `kapupusan` |  | 1 |
| penalty-4@6080 | `ka+pu+pusan` |  | 3 |
| penalty-4@8192 | `kapu+pusan` |  | 2 |
| penalty-4@16384 | `kapupusan` |  | 1 |
| penalty-8@6080 | `ka+pu+pus+an` |  | 4 |
| penalty-8@8192 | `ka+pu+pusan` |  | 3 |
| penalty-8@16384 | `kapupusan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+pupus+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+pupus+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `kapupusan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+pu+pus+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `kapu+pusan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kapupusan` |  | 1 |
| unigram-ablation@6080 | `kapupusan` |  | 1 |

## `paimburisan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+imburis+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pa+imb+ur+isan` |  | 4 |
| plain@8192 | `pa+imb+ur+isan` |  | 4 |
| plain@16384 | `pa+imburisan` |  | 2 |
| morphbpe@6080 | `pa+im+bur+isan` |  | 4 |
| morphbpe@8192 | `pa+im+bur+isan` |  | 4 |
| morphbpe@16384 | `pa+imburisan` |  | 2 |
| penalty-1@6080 | `pa+im+bur+isan` |  | 4 |
| penalty-1@8192 | `pa+im+bur+isan` |  | 4 |
| penalty-1@16384 | `pa+imburisan` |  | 2 |
| penalty-2@6080 | `pa+im+bur+isan` |  | 4 |
| penalty-2@8192 | `pa+im+bur+isan` |  | 4 |
| penalty-2@16384 | `pa+imburisan` |  | 2 |
| penalty-4@6080 | `pa+im+bur+isan` |  | 4 |
| penalty-4@8192 | `pa+im+bur+isan` |  | 4 |
| penalty-4@16384 | `pa+imburisan` |  | 2 |
| penalty-8@6080 | `pa+im+bu+ris+an` |  | 5 |
| penalty-8@8192 | `pa+imbu+ris+an` |  | 4 |
| penalty-8@16384 | `pa+imburisan` |  | 2 |
| stochastic-p4-d0.1@6080 | `pa+im+bu+ris+an` |  | 5 |
| stochastic-p4-d0.1@8192 | `pa+imbu+ris+an` |  | 4 |
| stochastic-p4-d0.1@16384 | `paimburisan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pa+im+bu+ris+an` |  | 5 |
| stochastic-p4-d0.2@8192 | `pa+imbu+ris+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `paimburisan` |  | 1 |
| unigram-ablation@6080 | `paimburis+an` |  | 2 |

## `kalungkutan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+lungkut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+ung+kutan` |  | 3 |
| plain@8192 | `kalung+kutan` |  | 2 |
| plain@16384 | `kalungkutan` |  | 1 |
| morphbpe@6080 | `kal+ung+ku+tan` |  | 4 |
| morphbpe@8192 | `kal+ung+ku+tan` |  | 4 |
| morphbpe@16384 | `kal+ung+kutan` |  | 3 |
| penalty-1@6080 | `kal+ung+ku+tan` |  | 4 |
| penalty-1@8192 | `kal+ung+ku+tan` |  | 4 |
| penalty-1@16384 | `kal+ung+kutan` |  | 3 |
| penalty-2@6080 | `kal+ung+ku+tan` |  | 4 |
| penalty-2@8192 | `kal+ung+ku+tan` |  | 4 |
| penalty-2@16384 | `kal+ung+kutan` |  | 3 |
| penalty-4@6080 | `kal+ung+kut+an` |  | 4 |
| penalty-4@8192 | `kal+ung+kut+an` |  | 4 |
| penalty-4@16384 | `kal+ung+kut+an` |  | 4 |
| penalty-8@6080 | `ka+lungkut+an` | OK | 3 |
| penalty-8@8192 | `ka+lungkut+an` | OK | 3 |
| penalty-8@16384 | `ka+lungkut+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+lung+ku+tan` |  | 4 |
| stochastic-p4-d0.1@8192 | `ka+lung+kutan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+lung+kutan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+lungkut+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+lungkut+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+lungkut+an` | OK | 3 |
| unigram-ablation@6080 | `ka+lungkut+an` | OK | 3 |

## `kandungan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+ndung+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kand+ungan` |  | 2 |
| plain@8192 | `kand+ungan` |  | 2 |
| plain@16384 | `kandungan` |  | 1 |
| morphbpe@6080 | `kand+ungan` |  | 2 |
| morphbpe@8192 | `kand+ungan` |  | 2 |
| morphbpe@16384 | `kandungan` |  | 1 |
| penalty-1@6080 | `kan+d+ungan` |  | 3 |
| penalty-1@8192 | `kan+d+ungan` |  | 3 |
| penalty-1@16384 | `kandungan` |  | 1 |
| penalty-2@6080 | `kan+d+ungan` |  | 3 |
| penalty-2@8192 | `kan+d+ungan` |  | 3 |
| penalty-2@16384 | `kandungan` |  | 1 |
| penalty-4@6080 | `kan+dung+an` |  | 3 |
| penalty-4@8192 | `kan+dung+an` |  | 3 |
| penalty-4@16384 | `kandungan` |  | 1 |
| penalty-8@6080 | `kan+dung+an` |  | 3 |
| penalty-8@8192 | `kan+dung+an` |  | 3 |
| penalty-8@16384 | `kandungan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kan+dung+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kan+dung+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kandungan` |  | 1 |
| stochastic-p4-d0.2@6080 | `k+and+ungan` |  | 3 |
| stochastic-p4-d0.2@8192 | `k+and+ungan` |  | 3 |
| stochastic-p4-d0.2@16384 | `kandungan` |  | 1 |
| unigram-ablation@6080 | `kan+dung+an` |  | 3 |

## `kabyasnan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+byasn+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kab+yas+nan` |  | 3 |
| plain@8192 | `kab+yasnan` |  | 2 |
| plain@16384 | `kabyasnan` |  | 1 |
| morphbpe@6080 | `kab+yas+nan` |  | 3 |
| morphbpe@8192 | `kab+yasnan` |  | 2 |
| morphbpe@16384 | `kabyasnan` |  | 1 |
| penalty-1@6080 | `kab+yas+nan` |  | 3 |
| penalty-1@8192 | `kab+yasnan` |  | 2 |
| penalty-1@16384 | `kabyasnan` |  | 1 |
| penalty-2@6080 | `kab+yas+nan` |  | 3 |
| penalty-2@8192 | `kab+yasnan` |  | 2 |
| penalty-2@16384 | `kabyasnan` |  | 1 |
| penalty-4@6080 | `kab+yas+nan` |  | 3 |
| penalty-4@8192 | `kab+yasnan` |  | 2 |
| penalty-4@16384 | `kabyasnan` |  | 1 |
| penalty-8@6080 | `kab+yas+nan` |  | 3 |
| penalty-8@8192 | `kab+yasnan` |  | 2 |
| penalty-8@16384 | `kabyasnan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+b+yas+nan` |  | 4 |
| stochastic-p4-d0.1@8192 | `ka+byasnan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kabyasnan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+bya+s+nan` |  | 4 |
| stochastic-p4-d0.2@8192 | `ka+bya+s+nan` |  | 4 |
| stochastic-p4-d0.2@16384 | `kabyasnan` |  | 1 |
| unigram-ablation@6080 | `kabyasnan` |  | 1 |

## `pakamalan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+kamal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paka+malan` |  | 2 |
| plain@8192 | `pakamalan` |  | 1 |
| plain@16384 | `pakamalan` |  | 1 |
| morphbpe@6080 | `paka+malan` |  | 2 |
| morphbpe@8192 | `pakamalan` |  | 1 |
| morphbpe@16384 | `pakamalan` |  | 1 |
| penalty-1@6080 | `pakamal+an` |  | 2 |
| penalty-1@8192 | `pakamalan` |  | 1 |
| penalty-1@16384 | `pakamalan` |  | 1 |
| penalty-2@6080 | `pakamal+an` |  | 2 |
| penalty-2@8192 | `pakamalan` |  | 1 |
| penalty-2@16384 | `pakamalan` |  | 1 |
| penalty-4@6080 | `pakamal+an` |  | 2 |
| penalty-4@8192 | `pakamalan` |  | 1 |
| penalty-4@16384 | `pakamalan` |  | 1 |
| penalty-8@6080 | `pakamal+an` |  | 2 |
| penalty-8@8192 | `pakamalan` |  | 1 |
| penalty-8@16384 | `pakamalan` |  | 1 |
| stochastic-p4-d0.1@6080 | `paka+mal+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `pakamalan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pakamalan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pakamal+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `pakamalan` |  | 1 |
| stochastic-p4-d0.2@16384 | `pakamalan` |  | 1 |
| unigram-ablation@6080 | `paka+malan` |  | 2 |

## `parakalan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+rakal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `par+ak+alan` |  | 3 |
| plain@8192 | `par+ak+alan` |  | 3 |
| plain@16384 | `par+akalan` |  | 2 |
| morphbpe@6080 | `par+ak+alan` |  | 3 |
| morphbpe@8192 | `par+ak+alan` |  | 3 |
| morphbpe@16384 | `par+akalan` |  | 2 |
| penalty-1@6080 | `par+ak+alan` |  | 3 |
| penalty-1@8192 | `par+ak+alan` |  | 3 |
| penalty-1@16384 | `par+akalan` |  | 2 |
| penalty-2@6080 | `par+ak+alan` |  | 3 |
| penalty-2@8192 | `par+ak+alan` |  | 3 |
| penalty-2@16384 | `par+akalan` |  | 2 |
| penalty-4@6080 | `pa+rakal+an` | OK | 3 |
| penalty-4@8192 | `pa+rakal+an` | OK | 3 |
| penalty-4@16384 | `pa+rakal+an` | OK | 3 |
| penalty-8@6080 | `pa+rakal+an` | OK | 3 |
| penalty-8@8192 | `pa+rakal+an` | OK | 3 |
| penalty-8@16384 | `pa+rakal+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `pa+rakal+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `pa+rakal+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `pa+rakalan` |  | 2 |
| stochastic-p4-d0.2@6080 | `pa+raka+lan` |  | 3 |
| stochastic-p4-d0.2@8192 | `pa+raka+lan` |  | 3 |
| stochastic-p4-d0.2@16384 | `pa+rakalan` |  | 2 |
| unigram-ablation@6080 | `para+ka+lan` |  | 3 |

## `kayubuan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+yubu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kayu+b+uan` |  | 3 |
| plain@8192 | `kayu+b+uan` |  | 3 |
| plain@16384 | `kayu+buan` |  | 2 |
| morphbpe@6080 | `kayu+b+uan` |  | 3 |
| morphbpe@8192 | `kayu+b+uan` |  | 3 |
| morphbpe@16384 | `kayu+buan` |  | 2 |
| penalty-1@6080 | `kayu+b+uan` |  | 3 |
| penalty-1@8192 | `kayu+b+uan` |  | 3 |
| penalty-1@16384 | `kayu+buan` |  | 2 |
| penalty-2@6080 | `kayu+bu+an` |  | 3 |
| penalty-2@8192 | `kayu+bu+an` |  | 3 |
| penalty-2@16384 | `kayu+buan` |  | 2 |
| penalty-4@6080 | `kayu+bu+an` |  | 3 |
| penalty-4@8192 | `kayu+buan` |  | 2 |
| penalty-4@16384 | `kayu+buan` |  | 2 |
| penalty-8@6080 | `kayu+bu+an` |  | 3 |
| penalty-8@8192 | `kayu+buan` |  | 2 |
| penalty-8@16384 | `kayu+buan` |  | 2 |
| stochastic-p4-d0.1@6080 | `kayu+bu+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kayu+buan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kayu+buan` |  | 2 |
| stochastic-p4-d0.2@6080 | `kayu+bu+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kayu+buan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kayu+buan` |  | 2 |
| unigram-ablation@6080 | `kayu+bu+an` |  | 3 |

## `kalaraman`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+laram+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+ar+aman` |  | 3 |
| plain@8192 | `kal+ar+aman` |  | 3 |
| plain@16384 | `kalaraman` |  | 1 |
| morphbpe@6080 | `kal+ar+aman` |  | 3 |
| morphbpe@8192 | `kal+ar+aman` |  | 3 |
| morphbpe@16384 | `kalaraman` |  | 1 |
| penalty-1@6080 | `kal+ar+aman` |  | 3 |
| penalty-1@8192 | `kal+ar+aman` |  | 3 |
| penalty-1@16384 | `kalaraman` |  | 1 |
| penalty-2@6080 | `kal+ar+aman` |  | 3 |
| penalty-2@8192 | `kal+ar+aman` |  | 3 |
| penalty-2@16384 | `kalaraman` |  | 1 |
| penalty-4@6080 | `kal+ar+aman` |  | 3 |
| penalty-4@8192 | `kal+ar+aman` |  | 3 |
| penalty-4@16384 | `kalaraman` |  | 1 |
| penalty-8@6080 | `ka+lar+aman` |  | 3 |
| penalty-8@8192 | `ka+lar+aman` |  | 3 |
| penalty-8@16384 | `kalaraman` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+lar+aman` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+lar+aman` |  | 3 |
| stochastic-p4-d0.1@16384 | `kalaraman` |  | 1 |
| stochastic-p4-d0.2@6080 | `kala+ram+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kala+ram+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `kalaraman` |  | 1 |
| unigram-ablation@6080 | `ka+laram+an` | OK | 3 |

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

## `kapanayan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+panay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapanayan` |  | 1 |
| plain@8192 | `kapanayan` |  | 1 |
| plain@16384 | `kapanayan` |  | 1 |
| morphbpe@6080 | `kapanayan` |  | 1 |
| morphbpe@8192 | `kapanayan` |  | 1 |
| morphbpe@16384 | `kapanayan` |  | 1 |
| penalty-1@6080 | `kapanayan` |  | 1 |
| penalty-1@8192 | `kapanayan` |  | 1 |
| penalty-1@16384 | `kapanayan` |  | 1 |
| penalty-2@6080 | `kapanayan` |  | 1 |
| penalty-2@8192 | `kapanayan` |  | 1 |
| penalty-2@16384 | `kapanayan` |  | 1 |
| penalty-4@6080 | `kapanayan` |  | 1 |
| penalty-4@8192 | `kapanayan` |  | 1 |
| penalty-4@16384 | `kapanayan` |  | 1 |
| penalty-8@6080 | `kapanayan` |  | 1 |
| penalty-8@8192 | `kapanayan` |  | 1 |
| penalty-8@16384 | `kapanayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapanayan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kapanayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapanayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapanayan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kapanayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapanayan` |  | 1 |
| unigram-ablation@6080 | `kapanayan` |  | 1 |

## `karalumduman`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+ralumdum+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kar+alum+du+man` |  | 4 |
| plain@8192 | `kar+alum+duman` |  | 3 |
| plain@16384 | `karalumduman` |  | 1 |
| morphbpe@6080 | `kar+al+um+du+man` |  | 5 |
| morphbpe@8192 | `kar+alum+duman` |  | 3 |
| morphbpe@16384 | `karalumduman` |  | 1 |
| penalty-1@6080 | `kar+al+um+du+man` |  | 5 |
| penalty-1@8192 | `kar+alum+duman` |  | 3 |
| penalty-1@16384 | `karalumduman` |  | 1 |
| penalty-2@6080 | `kar+al+um+du+man` |  | 5 |
| penalty-2@8192 | `kar+alum+duman` |  | 3 |
| penalty-2@16384 | `karalumduman` |  | 1 |
| penalty-4@6080 | `kar+alum+du+man` |  | 4 |
| penalty-4@8192 | `kar+alum+duman` |  | 3 |
| penalty-4@16384 | `karalumduman` |  | 1 |
| penalty-8@6080 | `kar+al+um+du+man` |  | 5 |
| penalty-8@8192 | `kar+alum+duman` |  | 3 |
| penalty-8@16384 | `karalumduman` |  | 1 |
| stochastic-p4-d0.1@6080 | `kar+alum+du+man` |  | 4 |
| stochastic-p4-d0.1@8192 | `kar+alum+duman` |  | 3 |
| stochastic-p4-d0.1@16384 | `karalumduman` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+ral+umdu+man` |  | 4 |
| stochastic-p4-d0.2@8192 | `ka+ral+umdu+man` |  | 4 |
| stochastic-p4-d0.2@16384 | `karalumduman` |  | 1 |
| unigram-ablation@6080 | `kar+alumdum+an` |  | 3 |

## `karampatan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+rampat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `karampatan` |  | 1 |
| plain@8192 | `karampatan` |  | 1 |
| plain@16384 | `karampatan` |  | 1 |
| morphbpe@6080 | `karampatan` |  | 1 |
| morphbpe@8192 | `karampatan` |  | 1 |
| morphbpe@16384 | `karampatan` |  | 1 |
| penalty-1@6080 | `karampatan` |  | 1 |
| penalty-1@8192 | `karampatan` |  | 1 |
| penalty-1@16384 | `karampatan` |  | 1 |
| penalty-2@6080 | `karampatan` |  | 1 |
| penalty-2@8192 | `karampatan` |  | 1 |
| penalty-2@16384 | `karampatan` |  | 1 |
| penalty-4@6080 | `karampatan` |  | 1 |
| penalty-4@8192 | `karampatan` |  | 1 |
| penalty-4@16384 | `karampatan` |  | 1 |
| penalty-8@6080 | `karampatan` |  | 1 |
| penalty-8@8192 | `karampatan` |  | 1 |
| penalty-8@16384 | `karampatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `karampatan` |  | 1 |
| stochastic-p4-d0.1@8192 | `karampatan` |  | 1 |
| stochastic-p4-d0.1@16384 | `karampatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `karampatan` |  | 1 |
| stochastic-p4-d0.2@8192 | `karampatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `karampatan` |  | 1 |
| unigram-ablation@6080 | `karampatan` |  | 1 |

## `panamdaman`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pa+namdam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+amdaman` |  | 2 |
| plain@8192 | `pan+amdaman` |  | 2 |
| plain@16384 | `panamdaman` |  | 1 |
| morphbpe@6080 | `pan+amdaman` |  | 2 |
| morphbpe@8192 | `pan+amdaman` |  | 2 |
| morphbpe@16384 | `pan+amdaman` |  | 2 |
| penalty-1@6080 | `pan+amdaman` |  | 2 |
| penalty-1@8192 | `pan+amdaman` |  | 2 |
| penalty-1@16384 | `pan+amdaman` |  | 2 |
| penalty-2@6080 | `pan+amdaman` |  | 2 |
| penalty-2@8192 | `pan+amdaman` |  | 2 |
| penalty-2@16384 | `pan+amdaman` |  | 2 |
| penalty-4@6080 | `pan+amdam+an` |  | 3 |
| penalty-4@8192 | `pan+amdam+an` |  | 3 |
| penalty-4@16384 | `pan+amdam+an` |  | 3 |
| penalty-8@6080 | `pan+amdam+an` |  | 3 |
| penalty-8@8192 | `pan+amdam+an` |  | 3 |
| penalty-8@16384 | `pan+amdam+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `pan+am+daman` |  | 3 |
| stochastic-p4-d0.1@8192 | `pan+amdaman` |  | 2 |
| stochastic-p4-d0.1@16384 | `pan+amdaman` |  | 2 |
| stochastic-p4-d0.2@6080 | `p+an+amdam+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `p+an+amdam+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `p+an+amdam+an` |  | 4 |
| unigram-ablation@6080 | `panamdaman` |  | 1 |

## `kaligayan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+ligay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kal+igayan` |  | 2 |
| plain@8192 | `kaligayan` |  | 1 |
| plain@16384 | `kaligayan` |  | 1 |
| morphbpe@6080 | `kal+igayan` |  | 2 |
| morphbpe@8192 | `kaligayan` |  | 1 |
| morphbpe@16384 | `kaligayan` |  | 1 |
| penalty-1@6080 | `kal+igayan` |  | 2 |
| penalty-1@8192 | `kaligayan` |  | 1 |
| penalty-1@16384 | `kaligayan` |  | 1 |
| penalty-2@6080 | `kal+igayan` |  | 2 |
| penalty-2@8192 | `kaligayan` |  | 1 |
| penalty-2@16384 | `kaligayan` |  | 1 |
| penalty-4@6080 | `kal+igayan` |  | 2 |
| penalty-4@8192 | `kaligayan` |  | 1 |
| penalty-4@16384 | `kaligayan` |  | 1 |
| penalty-8@6080 | `ka+li+gayan` |  | 3 |
| penalty-8@8192 | `kaligayan` |  | 1 |
| penalty-8@16384 | `kaligayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+li+gayan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kaligayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kaligayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+li+gayan` |  | 3 |
| stochastic-p4-d0.2@8192 | `kaligayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kaligayan` |  | 1 |
| unigram-ablation@6080 | `ka+ligaya+n` |  | 3 |

## `kapanamdaman`  (circumfixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ka+panamdam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapan+amdaman` |  | 2 |
| plain@8192 | `kapan+amdaman` |  | 2 |
| plain@16384 | `kapanamdaman` |  | 1 |
| morphbpe@6080 | `kapan+amdaman` |  | 2 |
| morphbpe@8192 | `kapan+amdaman` |  | 2 |
| morphbpe@16384 | `kapanamdaman` |  | 1 |
| penalty-1@6080 | `kapan+amdaman` |  | 2 |
| penalty-1@8192 | `kapan+amdaman` |  | 2 |
| penalty-1@16384 | `kapanamdaman` |  | 1 |
| penalty-2@6080 | `kapan+amdaman` |  | 2 |
| penalty-2@8192 | `kapan+amdaman` |  | 2 |
| penalty-2@16384 | `kapanamdaman` |  | 1 |
| penalty-4@6080 | `kapan+amdam+an` |  | 3 |
| penalty-4@8192 | `kapan+amdam+an` |  | 3 |
| penalty-4@16384 | `kapanamdaman` |  | 1 |
| penalty-8@6080 | `kapan+amdam+an` |  | 3 |
| penalty-8@8192 | `kapan+amdam+an` |  | 3 |
| penalty-8@16384 | `kapanamdaman` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapan+am+daman` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapan+amdaman` |  | 2 |
| stochastic-p4-d0.1@16384 | `kapanamdaman` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapan+amdam+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kapan+amdam+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `kapanamdaman` |  | 1 |
| unigram-ablation@6080 | `ka+panamdaman` |  | 2 |

## `katipunan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+tipun+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kat+ipunan` |  | 2 |
| plain@8192 | `kat+ipunan` |  | 2 |
| plain@16384 | `kat+ipunan` |  | 2 |
| morphbpe@6080 | `kat+ip+unan` |  | 3 |
| morphbpe@8192 | `kat+ip+unan` |  | 3 |
| morphbpe@16384 | `kat+ip+unan` |  | 3 |
| penalty-1@6080 | `kat+ipun+an` |  | 3 |
| penalty-1@8192 | `kat+ipun+an` |  | 3 |
| penalty-1@16384 | `kat+ipun+an` |  | 3 |
| penalty-2@6080 | `kat+ip+unan` |  | 3 |
| penalty-2@8192 | `kat+ip+unan` |  | 3 |
| penalty-2@16384 | `kat+ip+unan` |  | 3 |
| penalty-4@6080 | `ka+tipun+an` | OK | 3 |
| penalty-4@8192 | `ka+tipun+an` | OK | 3 |
| penalty-4@16384 | `ka+tipun+an` | OK | 3 |
| penalty-8@6080 | `ka+tipun+an` | OK | 3 |
| penalty-8@8192 | `ka+tipun+an` | OK | 3 |
| penalty-8@16384 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+tipun+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+tipun+an` | OK | 3 |
| unigram-ablation@6080 | `ka+tipun+an` | OK | 3 |

## `kayatinan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+yatin+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kay+atin+an` |  | 3 |
| plain@8192 | `kay+atin+an` |  | 3 |
| plain@16384 | `kayatinan` |  | 1 |
| morphbpe@6080 | `kay+atin+an` |  | 3 |
| morphbpe@8192 | `kay+atin+an` |  | 3 |
| morphbpe@16384 | `kayatinan` |  | 1 |
| penalty-1@6080 | `kay+atin+an` |  | 3 |
| penalty-1@8192 | `kay+atin+an` |  | 3 |
| penalty-1@16384 | `kayatinan` |  | 1 |
| penalty-2@6080 | `kay+atin+an` |  | 3 |
| penalty-2@8192 | `kay+atin+an` |  | 3 |
| penalty-2@16384 | `kayatinan` |  | 1 |
| penalty-4@6080 | `kay+atin+an` |  | 3 |
| penalty-4@8192 | `kay+atin+an` |  | 3 |
| penalty-4@16384 | `kayatinan` |  | 1 |
| penalty-8@6080 | `kay+atin+an` |  | 3 |
| penalty-8@8192 | `kay+atin+an` |  | 3 |
| penalty-8@16384 | `kayatinan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kay+atin+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kay+atin+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kayatinan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kay+atin+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kay+atin+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `kayatinan` |  | 1 |
| unigram-ablation@6080 | `kaya+tin+an` |  | 3 |

## `pagnasan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+gnas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+nasan` |  | 2 |
| plain@8192 | `pagnasan` |  | 1 |
| plain@16384 | `pagnasan` |  | 1 |
| morphbpe@6080 | `pag+nasan` |  | 2 |
| morphbpe@8192 | `pag+nasan` |  | 2 |
| morphbpe@16384 | `pag+nasan` |  | 2 |
| penalty-1@6080 | `pag+nasan` |  | 2 |
| penalty-1@8192 | `pag+nasan` |  | 2 |
| penalty-1@16384 | `pag+nasan` |  | 2 |
| penalty-2@6080 | `pag+nasan` |  | 2 |
| penalty-2@8192 | `pag+nasan` |  | 2 |
| penalty-2@16384 | `pag+nasan` |  | 2 |
| penalty-4@6080 | `pag+nasan` |  | 2 |
| penalty-4@8192 | `pag+nasan` |  | 2 |
| penalty-4@16384 | `pag+nasan` |  | 2 |
| penalty-8@6080 | `pag+nasan` |  | 2 |
| penalty-8@8192 | `pag+nasan` |  | 2 |
| penalty-8@16384 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.1@6080 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.1@8192 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.1@16384 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.2@6080 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.2@8192 | `pag+nasan` |  | 2 |
| stochastic-p4-d0.2@16384 | `pag+nasan` |  | 2 |
| unigram-ablation@6080 | `pagnasan` |  | 1 |

## `kapagnasan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+pagnas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapagnasan` |  | 1 |
| plain@8192 | `kapagnasan` |  | 1 |
| plain@16384 | `kapagnasan` |  | 1 |
| morphbpe@6080 | `kapagnasan` |  | 1 |
| morphbpe@8192 | `kapagnasan` |  | 1 |
| morphbpe@16384 | `kapagnasan` |  | 1 |
| penalty-1@6080 | `kapagnasan` |  | 1 |
| penalty-1@8192 | `kapagnasan` |  | 1 |
| penalty-1@16384 | `kapagnasan` |  | 1 |
| penalty-2@6080 | `kapagnasan` |  | 1 |
| penalty-2@8192 | `kapagnasan` |  | 1 |
| penalty-2@16384 | `kapagnasan` |  | 1 |
| penalty-4@6080 | `kapagnasan` |  | 1 |
| penalty-4@8192 | `kapagnasan` |  | 1 |
| penalty-4@16384 | `kapagnasan` |  | 1 |
| penalty-8@6080 | `kapagnasan` |  | 1 |
| penalty-8@8192 | `kapagnasan` |  | 1 |
| penalty-8@16384 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kapagnasan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kapagnasan` |  | 1 |
| unigram-ablation@6080 | `kapagnasan` |  | 1 |

## `kasangkapan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+sangkap+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kasang+kapan` |  | 2 |
| plain@8192 | `kasangkapan` |  | 1 |
| plain@16384 | `kasangkapan` |  | 1 |
| morphbpe@6080 | `kas+ang+kapan` |  | 3 |
| morphbpe@8192 | `kas+ang+kapan` |  | 3 |
| morphbpe@16384 | `kas+ang+kapan` |  | 3 |
| penalty-1@6080 | `kas+ang+kapan` |  | 3 |
| penalty-1@8192 | `kas+ang+kapan` |  | 3 |
| penalty-1@16384 | `kas+ang+kapan` |  | 3 |
| penalty-2@6080 | `ka+sang+kapan` |  | 3 |
| penalty-2@8192 | `ka+sang+kapan` |  | 3 |
| penalty-2@16384 | `ka+sang+kapan` |  | 3 |
| penalty-4@6080 | `ka+sang+kapan` |  | 3 |
| penalty-4@8192 | `ka+sang+kapan` |  | 3 |
| penalty-4@16384 | `kasang+kapan` |  | 2 |
| penalty-8@6080 | `ka+sang+kapan` |  | 3 |
| penalty-8@8192 | `ka+sang+kapan` |  | 3 |
| penalty-8@16384 | `ka+sang+kapan` |  | 3 |
| stochastic-p4-d0.1@6080 | `ka+sang+kapan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+sang+kapan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+sang+kapan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+sangkap+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+sangkap+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+sangkap+an` | OK | 3 |
| unigram-ablation@6080 | `kasangkapan` |  | 1 |

## `kabilugan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+bilug+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kabilugan` |  | 1 |
| plain@8192 | `kabilugan` |  | 1 |
| plain@16384 | `kabilugan` |  | 1 |
| morphbpe@6080 | `kabilugan` |  | 1 |
| morphbpe@8192 | `kabilugan` |  | 1 |
| morphbpe@16384 | `kabilugan` |  | 1 |
| penalty-1@6080 | `ka+bilug+an` | OK | 3 |
| penalty-1@8192 | `ka+bilug+an` | OK | 3 |
| penalty-1@16384 | `ka+bilug+an` | OK | 3 |
| penalty-2@6080 | `ka+bilug+an` | OK | 3 |
| penalty-2@8192 | `ka+bilug+an` | OK | 3 |
| penalty-2@16384 | `ka+bilug+an` | OK | 3 |
| penalty-4@6080 | `ka+bilug+an` | OK | 3 |
| penalty-4@8192 | `ka+bilug+an` | OK | 3 |
| penalty-4@16384 | `ka+bilug+an` | OK | 3 |
| penalty-8@6080 | `ka+bilug+an` | OK | 3 |
| penalty-8@8192 | `ka+bilug+an` | OK | 3 |
| penalty-8@16384 | `ka+bilug+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `kabilugan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kabilugan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kabilugan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kabilugan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kabilugan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kabilugan` |  | 1 |
| unigram-ablation@6080 | `kabilugan` |  | 1 |

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

## `kapagalan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+pagal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapag+alan` |  | 2 |
| plain@8192 | `kapag+alan` |  | 2 |
| plain@16384 | `kapagalan` |  | 1 |
| morphbpe@6080 | `kapag+alan` |  | 2 |
| morphbpe@8192 | `kapag+alan` |  | 2 |
| morphbpe@16384 | `kapag+alan` |  | 2 |
| penalty-1@6080 | `kapag+alan` |  | 2 |
| penalty-1@8192 | `kapag+alan` |  | 2 |
| penalty-1@16384 | `kapag+alan` |  | 2 |
| penalty-2@6080 | `kapag+alan` |  | 2 |
| penalty-2@8192 | `kapag+alan` |  | 2 |
| penalty-2@16384 | `kapag+alan` |  | 2 |
| penalty-4@6080 | `kapag+alan` |  | 2 |
| penalty-4@8192 | `kapag+alan` |  | 2 |
| penalty-4@16384 | `kapag+alan` |  | 2 |
| penalty-8@6080 | `ka+pagal+an` | OK | 3 |
| penalty-8@8192 | `ka+pagal+an` | OK | 3 |
| penalty-8@16384 | `ka+pagal+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+pag+alan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+pag+alan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+pag+alan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+pag+alan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+pag+alan` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+pag+alan` |  | 3 |
| unigram-ablation@6080 | `kapag+alan` |  | 2 |

## `kapainawan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+painaw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ka+pain+awan` |  | 3 |
| plain@8192 | `ka+pain+awan` |  | 3 |
| plain@16384 | `kapainawan` |  | 1 |
| morphbpe@6080 | `ka+pa+ina+wan` |  | 4 |
| morphbpe@8192 | `kapa+inawan` |  | 2 |
| morphbpe@16384 | `kapainawan` |  | 1 |
| penalty-1@6080 | `ka+pa+ina+wan` |  | 4 |
| penalty-1@8192 | `ka+pa+inawan` |  | 3 |
| penalty-1@16384 | `kapainawan` |  | 1 |
| penalty-2@6080 | `kapa+ina+wan` |  | 3 |
| penalty-2@8192 | `kapa+inawan` |  | 2 |
| penalty-2@16384 | `kapainawan` |  | 1 |
| penalty-4@6080 | `kapa+in+awan` |  | 3 |
| penalty-4@8192 | `kapa+inawan` |  | 2 |
| penalty-4@16384 | `kapainawan` |  | 1 |
| penalty-8@6080 | `ka+pain+awan` |  | 3 |
| penalty-8@8192 | `ka+pain+awan` |  | 3 |
| penalty-8@16384 | `kapainawan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kapa+in+awan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapa+inawan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kapainawan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kapa+in+awan` |  | 3 |
| stochastic-p4-d0.2@8192 | `kapa+inawan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kapainawan` |  | 1 |
| unigram-ablation@6080 | `kapa+inawa+n` |  | 3 |

## `pagumasdan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+gumasd+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+umas+dan` |  | 3 |
| plain@8192 | `pag+umasdan` |  | 2 |
| plain@16384 | `pagumasdan` |  | 1 |
| morphbpe@6080 | `pag+umas+dan` |  | 3 |
| morphbpe@8192 | `pag+umasdan` |  | 2 |
| morphbpe@16384 | `pagumasdan` |  | 1 |
| penalty-1@6080 | `pag+u+masdan` |  | 3 |
| penalty-1@8192 | `pag+u+masdan` |  | 3 |
| penalty-1@16384 | `pagumasdan` |  | 1 |
| penalty-2@6080 | `pag+u+masdan` |  | 3 |
| penalty-2@8192 | `pagu+masdan` |  | 2 |
| penalty-2@16384 | `pagumasdan` |  | 1 |
| penalty-4@6080 | `pa+gu+masdan` |  | 3 |
| penalty-4@8192 | `pagu+masdan` |  | 2 |
| penalty-4@16384 | `pagumasdan` |  | 1 |
| penalty-8@6080 | `pa+gu+masdan` |  | 3 |
| penalty-8@8192 | `pa+gumasdan` |  | 2 |
| penalty-8@16384 | `pagumasdan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pa+gu+mas+dan` |  | 4 |
| stochastic-p4-d0.1@8192 | `pa+gu+masdan` |  | 3 |
| stochastic-p4-d0.1@16384 | `pagumasdan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pa+gu+mas+dan` |  | 4 |
| stochastic-p4-d0.2@8192 | `pa+gu+masdan` |  | 3 |
| stochastic-p4-d0.2@16384 | `pagumasdan` |  | 1 |
| unigram-ablation@6080 | `pa+gumasdan` |  | 2 |

## `kabilyan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+bily+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kabilyan` |  | 1 |
| plain@8192 | `kabilyan` |  | 1 |
| plain@16384 | `kabilyan` |  | 1 |
| morphbpe@6080 | `kabilyan` |  | 1 |
| morphbpe@8192 | `kabilyan` |  | 1 |
| morphbpe@16384 | `kabilyan` |  | 1 |
| penalty-1@6080 | `kabilyan` |  | 1 |
| penalty-1@8192 | `kabilyan` |  | 1 |
| penalty-1@16384 | `kabilyan` |  | 1 |
| penalty-2@6080 | `kabilyan` |  | 1 |
| penalty-2@8192 | `kabilyan` |  | 1 |
| penalty-2@16384 | `kabilyan` |  | 1 |
| penalty-4@6080 | `kabilyan` |  | 1 |
| penalty-4@8192 | `kabilyan` |  | 1 |
| penalty-4@16384 | `kabilyan` |  | 1 |
| penalty-8@6080 | `kabilyan` |  | 1 |
| penalty-8@8192 | `kabilyan` |  | 1 |
| penalty-8@16384 | `kabilyan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kabilyan` |  | 1 |
| stochastic-p4-d0.1@8192 | `kabilyan` |  | 1 |
| stochastic-p4-d0.1@16384 | `kabilyan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kabilyan` |  | 1 |
| stochastic-p4-d0.2@8192 | `kabilyan` |  | 1 |
| stochastic-p4-d0.2@16384 | `kabilyan` |  | 1 |
| unigram-ablation@6080 | `kabilyan` |  | 1 |

## `kaburian`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+buri+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kaburian` |  | 1 |
| plain@8192 | `kaburian` |  | 1 |
| plain@16384 | `kaburian` |  | 1 |
| morphbpe@6080 | `kab+urian` |  | 2 |
| morphbpe@8192 | `kab+urian` |  | 2 |
| morphbpe@16384 | `kab+urian` |  | 2 |
| penalty-1@6080 | `ka+bur+ian` |  | 3 |
| penalty-1@8192 | `ka+bur+ian` |  | 3 |
| penalty-1@16384 | `ka+bur+ian` |  | 3 |
| penalty-2@6080 | `ka+buri+an` | OK | 3 |
| penalty-2@8192 | `ka+buri+an` | OK | 3 |
| penalty-2@16384 | `ka+buri+an` | OK | 3 |
| penalty-4@6080 | `ka+buri+an` | OK | 3 |
| penalty-4@8192 | `ka+buri+an` | OK | 3 |
| penalty-4@16384 | `ka+buri+an` | OK | 3 |
| penalty-8@6080 | `ka+buri+an` | OK | 3 |
| penalty-8@8192 | `ka+buri+an` | OK | 3 |
| penalty-8@16384 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+buri+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+buri+an` | OK | 3 |
| unigram-ablation@6080 | `kaburian` |  | 1 |

## `kamulangan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+mulang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kam+ul+angan` |  | 3 |
| plain@8192 | `kam+ul+angan` |  | 3 |
| plain@16384 | `kam+ulangan` |  | 2 |
| morphbpe@6080 | `kam+ul+angan` |  | 3 |
| morphbpe@8192 | `kam+ul+angan` |  | 3 |
| morphbpe@16384 | `kam+ul+angan` |  | 3 |
| penalty-1@6080 | `kam+ul+angan` |  | 3 |
| penalty-1@8192 | `kam+ul+angan` |  | 3 |
| penalty-1@16384 | `kam+ul+angan` |  | 3 |
| penalty-2@6080 | `kam+ul+angan` |  | 3 |
| penalty-2@8192 | `kam+ul+angan` |  | 3 |
| penalty-2@16384 | `kam+ul+angan` |  | 3 |
| penalty-4@6080 | `kam+ulang+an` |  | 3 |
| penalty-4@8192 | `kam+ulang+an` |  | 3 |
| penalty-4@16384 | `kam+ulang+an` |  | 3 |
| penalty-8@6080 | `kam+ul+angan` |  | 3 |
| penalty-8@8192 | `kam+ul+angan` |  | 3 |
| penalty-8@16384 | `kam+ul+angan` |  | 3 |
| stochastic-p4-d0.1@6080 | `kam+ul+angan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kam+ul+angan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kam+ul+angan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+mu+langan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+mu+langan` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+mu+langan` |  | 3 |
| unigram-ablation@6080 | `ka+mu+langan` |  | 3 |

## `kapalaluan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+palalu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kap+alal+uan` |  | 3 |
| plain@8192 | `kap+alal+uan` |  | 3 |
| plain@16384 | `kap+alal+uan` |  | 3 |
| morphbpe@6080 | `kapal+al+uan` |  | 3 |
| morphbpe@8192 | `kapal+al+uan` |  | 3 |
| morphbpe@16384 | `kapal+aluan` |  | 2 |
| penalty-1@6080 | `ka+pal+al+uan` |  | 4 |
| penalty-1@8192 | `kapal+al+uan` |  | 3 |
| penalty-1@16384 | `kapal+aluan` |  | 2 |
| penalty-2@6080 | `ka+pal+al+uan` |  | 4 |
| penalty-2@8192 | `kapal+al+uan` |  | 3 |
| penalty-2@16384 | `kapal+aluan` |  | 2 |
| penalty-4@6080 | `ka+pal+al+uan` |  | 4 |
| penalty-4@8192 | `ka+pal+al+uan` |  | 4 |
| penalty-4@16384 | `kapal+aluan` |  | 2 |
| penalty-8@6080 | `ka+pa+lalu+an` |  | 4 |
| penalty-8@8192 | `ka+pa+lalu+an` |  | 4 |
| penalty-8@16384 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `kapa+lalu+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `kapa+lalu+an` |  | 3 |
| unigram-ablation@6080 | `kapa+lalu+an` |  | 3 |

## `kapatagan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+patag+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kapat+agan` |  | 2 |
| plain@8192 | `kapat+agan` |  | 2 |
| plain@16384 | `kapatagan` |  | 1 |
| morphbpe@6080 | `kapat+agan` |  | 2 |
| morphbpe@8192 | `kapat+agan` |  | 2 |
| morphbpe@16384 | `kapat+agan` |  | 2 |
| penalty-1@6080 | `ka+pat+agan` |  | 3 |
| penalty-1@8192 | `ka+pat+agan` |  | 3 |
| penalty-1@16384 | `ka+pat+agan` |  | 3 |
| penalty-2@6080 | `ka+pat+agan` |  | 3 |
| penalty-2@8192 | `ka+pat+agan` |  | 3 |
| penalty-2@16384 | `ka+pat+agan` |  | 3 |
| penalty-4@6080 | `ka+patag+an` | OK | 3 |
| penalty-4@8192 | `ka+patag+an` | OK | 3 |
| penalty-4@16384 | `ka+patag+an` | OK | 3 |
| penalty-8@6080 | `ka+patag+an` | OK | 3 |
| penalty-8@8192 | `ka+patag+an` | OK | 3 |
| penalty-8@16384 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `ka+patag+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+patag+an` | OK | 3 |
| unigram-ablation@6080 | `kapata+gan` |  | 2 |

## `katungkulan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+tungkul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kat+ungkulan` |  | 2 |
| plain@8192 | `katungkulan` |  | 1 |
| plain@16384 | `katungkulan` |  | 1 |
| morphbpe@6080 | `kat+ungkul+an` |  | 3 |
| morphbpe@8192 | `kat+ungkulan` |  | 2 |
| morphbpe@16384 | `kat+ungkulan` |  | 2 |
| penalty-1@6080 | `kat+ungkul+an` |  | 3 |
| penalty-1@8192 | `kat+ungkul+an` |  | 3 |
| penalty-1@16384 | `kat+ungkul+an` |  | 3 |
| penalty-2@6080 | `kat+ungkul+an` |  | 3 |
| penalty-2@8192 | `kat+ungkul+an` |  | 3 |
| penalty-2@16384 | `kat+ungkul+an` |  | 3 |
| penalty-4@6080 | `ka+tungkul+an` | OK | 3 |
| penalty-4@8192 | `ka+tungkul+an` | OK | 3 |
| penalty-4@16384 | `ka+tungkul+an` | OK | 3 |
| penalty-8@6080 | `ka+tungkul+an` | OK | 3 |
| penalty-8@8192 | `ka+tungkul+an` | OK | 3 |
| penalty-8@16384 | `ka+tungkul+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+tungkul+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `ka+tungkul+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+tungkul+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+tung+kulan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+tung+kulan` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+tung+kulan` |  | 3 |
| unigram-ablation@6080 | `ka+tungkul+an` | OK | 3 |

## `kawakasan`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+wakas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ka+wa+kasan` |  | 3 |
| plain@8192 | `kawakasan` |  | 1 |
| plain@16384 | `kawakasan` |  | 1 |
| morphbpe@6080 | `ka+wakas+an` | OK | 3 |
| morphbpe@8192 | `ka+wakas+an` | OK | 3 |
| morphbpe@16384 | `ka+wakas+an` | OK | 3 |
| penalty-1@6080 | `ka+wakas+an` | OK | 3 |
| penalty-1@8192 | `ka+wakas+an` | OK | 3 |
| penalty-1@16384 | `ka+wakas+an` | OK | 3 |
| penalty-2@6080 | `ka+wakas+an` | OK | 3 |
| penalty-2@8192 | `ka+wakas+an` | OK | 3 |
| penalty-2@16384 | `ka+wakas+an` | OK | 3 |
| penalty-4@6080 | `ka+wakas+an` | OK | 3 |
| penalty-4@8192 | `ka+wakas+an` | OK | 3 |
| penalty-4@16384 | `ka+wakas+an` | OK | 3 |
| penalty-8@6080 | `ka+wakas+an` | OK | 3 |
| penalty-8@8192 | `ka+wakas+an` | OK | 3 |
| penalty-8@16384 | `ka+wakas+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `ka+wa+kas+an` |  | 4 |
| stochastic-p4-d0.1@8192 | `ka+wakas+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `ka+wakas+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `ka+wa+kas+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `ka+wakas+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `ka+wakas+an` | OK | 3 |
| unigram-ablation@6080 | `kawaka+san` |  | 2 |

## `kayaldawan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `ka+yaldaw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kay+al+da+wan` |  | 4 |
| plain@8192 | `kay+alda+wan` |  | 3 |
| plain@16384 | `kayaldawan` |  | 1 |
| morphbpe@6080 | `kay+al+da+wan` |  | 4 |
| morphbpe@8192 | `kay+alda+wan` |  | 3 |
| morphbpe@16384 | `kayaldawan` |  | 1 |
| penalty-1@6080 | `kay+al+da+wan` |  | 4 |
| penalty-1@8192 | `kay+alda+wan` |  | 3 |
| penalty-1@16384 | `kayaldawan` |  | 1 |
| penalty-2@6080 | `kay+al+da+wan` |  | 4 |
| penalty-2@8192 | `kay+alda+wan` |  | 3 |
| penalty-2@16384 | `kayaldawan` |  | 1 |
| penalty-4@6080 | `kay+al+da+wan` |  | 4 |
| penalty-4@8192 | `kay+alda+wan` |  | 3 |
| penalty-4@16384 | `kayaldawan` |  | 1 |
| penalty-8@6080 | `kay+al+da+wan` |  | 4 |
| penalty-8@8192 | `kay+al+da+wan` |  | 4 |
| penalty-8@16384 | `kayaldawan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kay+alda+wan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kay+alda+wan` |  | 3 |
| stochastic-p4-d0.1@16384 | `kayaldawan` |  | 1 |
| stochastic-p4-d0.2@6080 | `kay+alda+wan` |  | 3 |
| stochastic-p4-d0.2@8192 | `kay+alda+wan` |  | 3 |
| stochastic-p4-d0.2@16384 | `kayaldawan` |  | 1 |
| unigram-ablation@6080 | `kayaldawan` |  | 1 |

## `kabengian`  (circumfixation, tier A_strong_silver)

**silver gold:** `ka+bengi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kab+eng+ian` |  | 3 |
| plain@8192 | `kab+eng+ian` |  | 3 |
| plain@16384 | `kabengian` |  | 1 |
| morphbpe@6080 | `kab+eng+ian` |  | 3 |
| morphbpe@8192 | `kab+eng+ian` |  | 3 |
| morphbpe@16384 | `kab+eng+ian` |  | 3 |
| penalty-1@6080 | `ka+beng+ian` |  | 3 |
| penalty-1@8192 | `ka+beng+ian` |  | 3 |
| penalty-1@16384 | `ka+beng+ian` |  | 3 |
| penalty-2@6080 | `ka+beng+ian` |  | 3 |
| penalty-2@8192 | `ka+beng+ian` |  | 3 |
| penalty-2@16384 | `ka+beng+ian` |  | 3 |
| penalty-4@6080 | `ka+beng+ian` |  | 3 |
| penalty-4@8192 | `ka+beng+ian` |  | 3 |
| penalty-4@16384 | `ka+beng+ian` |  | 3 |
| penalty-8@6080 | `ka+beng+ian` |  | 3 |
| penalty-8@8192 | `ka+beng+ian` |  | 3 |
| penalty-8@16384 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.1@6080 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+beng+ian` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+beng+ian` |  | 3 |
| unigram-ablation@6080 | `ka+bengi+an` | OK | 3 |

## `pasiknangan`  (circumfixation, tier B_moderate_silver)

**silver gold:** `pa+siknang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pas+iknangan` |  | 2 |
| plain@8192 | `pas+iknangan` |  | 2 |
| plain@16384 | `pasiknangan` |  | 1 |
| morphbpe@6080 | `pas+iknangan` |  | 2 |
| morphbpe@8192 | `pasiknangan` |  | 1 |
| morphbpe@16384 | `pasiknangan` |  | 1 |
| penalty-1@6080 | `pas+iknangan` |  | 2 |
| penalty-1@8192 | `pasiknangan` |  | 1 |
| penalty-1@16384 | `pasiknangan` |  | 1 |
| penalty-2@6080 | `pa+sik+nang+an` |  | 4 |
| penalty-2@8192 | `pasiknangan` |  | 1 |
| penalty-2@16384 | `pasiknangan` |  | 1 |
| penalty-4@6080 | `pasi+knangan` |  | 2 |
| penalty-4@8192 | `pasiknangan` |  | 1 |
| penalty-4@16384 | `pasiknangan` |  | 1 |
| penalty-8@6080 | `pasi+knangan` |  | 2 |
| penalty-8@8192 | `pasiknangan` |  | 1 |
| penalty-8@16384 | `pasiknangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pasi+k+nang+an` |  | 4 |
| stochastic-p4-d0.1@8192 | `pasiknangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pasiknangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pa+sik+nang+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `pa+sik+nang+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `pasiknangan` |  | 1 |
| unigram-ablation@6080 | `pasikna+ngan` |  | 2 |

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

## `binie`  (infixation, tier A_strong_silver)

**silver gold:** `b+in+ie`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `binie` |  | 1 |
| plain@8192 | `binie` |  | 1 |
| plain@16384 | `binie` |  | 1 |
| morphbpe@6080 | `bin+ie` |  | 2 |
| morphbpe@8192 | `bin+ie` |  | 2 |
| morphbpe@16384 | `bin+ie` |  | 2 |
| penalty-1@6080 | `b+in+ie` | OK | 3 |
| penalty-1@8192 | `b+in+ie` | OK | 3 |
| penalty-1@16384 | `b+in+ie` | OK | 3 |
| penalty-2@6080 | `b+in+ie` | OK | 3 |
| penalty-2@8192 | `b+in+ie` | OK | 3 |
| penalty-2@16384 | `b+in+ie` | OK | 3 |
| penalty-4@6080 | `b+in+ie` | OK | 3 |
| penalty-4@8192 | `b+in+ie` | OK | 3 |
| penalty-4@16384 | `b+in+ie` | OK | 3 |
| penalty-8@6080 | `b+in+ie` | OK | 3 |
| penalty-8@8192 | `b+in+ie` | OK | 3 |
| penalty-8@16384 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.1@6080 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.1@8192 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.1@16384 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.2@6080 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.2@8192 | `b+in+ie` | OK | 3 |
| stochastic-p4-d0.2@16384 | `b+in+ie` | OK | 3 |
| unigram-ablation@6080 | `binie` |  | 1 |

## `binili`  (infixation, tier A_strong_silver)

**silver gold:** `b+in+ili`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `binili` |  | 1 |
| plain@8192 | `binili` |  | 1 |
| plain@16384 | `binili` |  | 1 |
| morphbpe@6080 | `bin+ili` |  | 2 |
| morphbpe@8192 | `bin+ili` |  | 2 |
| morphbpe@16384 | `bin+ili` |  | 2 |
| penalty-1@6080 | `b+in+ili` | OK | 3 |
| penalty-1@8192 | `b+in+ili` | OK | 3 |
| penalty-1@16384 | `b+in+ili` | OK | 3 |
| penalty-2@6080 | `b+in+ili` | OK | 3 |
| penalty-2@8192 | `b+in+ili` | OK | 3 |
| penalty-2@16384 | `b+in+ili` | OK | 3 |
| penalty-4@6080 | `b+in+ili` | OK | 3 |
| penalty-4@8192 | `b+in+ili` | OK | 3 |
| penalty-4@16384 | `b+in+ili` | OK | 3 |
| penalty-8@6080 | `b+in+ili` | OK | 3 |
| penalty-8@8192 | `b+in+ili` | OK | 3 |
| penalty-8@16384 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.1@6080 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.1@8192 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.1@16384 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.2@6080 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.2@8192 | `b+in+ili` | OK | 3 |
| stochastic-p4-d0.2@16384 | `b+in+ili` | OK | 3 |
| unigram-ablation@6080 | `binil+i` |  | 2 |

## `dinatang`  (infixation, tier A_strong_silver)

**silver gold:** `d+in+atang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dinatang` |  | 1 |
| plain@8192 | `dinatang` |  | 1 |
| plain@16384 | `dinatang` |  | 1 |
| morphbpe@6080 | `din+atang` |  | 2 |
| morphbpe@8192 | `din+atang` |  | 2 |
| morphbpe@16384 | `din+atang` |  | 2 |
| penalty-1@6080 | `d+in+atang` | OK | 3 |
| penalty-1@8192 | `d+in+atang` | OK | 3 |
| penalty-1@16384 | `d+in+atang` | OK | 3 |
| penalty-2@6080 | `d+in+atang` | OK | 3 |
| penalty-2@8192 | `d+in+atang` | OK | 3 |
| penalty-2@16384 | `d+in+atang` | OK | 3 |
| penalty-4@6080 | `d+in+atang` | OK | 3 |
| penalty-4@8192 | `d+in+atang` | OK | 3 |
| penalty-4@16384 | `d+in+atang` | OK | 3 |
| penalty-8@6080 | `d+in+atang` | OK | 3 |
| penalty-8@8192 | `d+in+atang` | OK | 3 |
| penalty-8@16384 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.1@6080 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.1@8192 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.1@16384 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.2@6080 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.2@8192 | `d+in+atang` | OK | 3 |
| stochastic-p4-d0.2@16384 | `d+in+atang` | OK | 3 |
| unigram-ablation@6080 | `d+inatang` |  | 2 |

## `kinua`  (infixation, tier B_moderate_silver)

**silver gold:** `k+in+ua`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kinua` |  | 1 |
| plain@8192 | `kinua` |  | 1 |
| plain@16384 | `kinua` |  | 1 |
| morphbpe@6080 | `kinua` |  | 1 |
| morphbpe@8192 | `kinua` |  | 1 |
| morphbpe@16384 | `kinua` |  | 1 |
| penalty-1@6080 | `kinua` |  | 1 |
| penalty-1@8192 | `kinua` |  | 1 |
| penalty-1@16384 | `kinua` |  | 1 |
| penalty-2@6080 | `kinua` |  | 1 |
| penalty-2@8192 | `kinua` |  | 1 |
| penalty-2@16384 | `kinua` |  | 1 |
| penalty-4@6080 | `kinua` |  | 1 |
| penalty-4@8192 | `kinua` |  | 1 |
| penalty-4@16384 | `kinua` |  | 1 |
| penalty-8@6080 | `kinua` |  | 1 |
| penalty-8@8192 | `kinua` |  | 1 |
| penalty-8@16384 | `kinua` |  | 1 |
| stochastic-p4-d0.1@6080 | `kinua` |  | 1 |
| stochastic-p4-d0.1@8192 | `kinua` |  | 1 |
| stochastic-p4-d0.1@16384 | `kinua` |  | 1 |
| stochastic-p4-d0.2@6080 | `kinua` |  | 1 |
| stochastic-p4-d0.2@8192 | `kinua` |  | 1 |
| stochastic-p4-d0.2@16384 | `kinua` |  | 1 |
| unigram-ablation@6080 | `kinua` |  | 1 |

## `tinape`  (infixation, tier B_moderate_silver)

**silver gold:** `t+in+ape`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tinape` |  | 1 |
| plain@8192 | `tinape` |  | 1 |
| plain@16384 | `tinape` |  | 1 |
| morphbpe@6080 | `tinape` |  | 1 |
| morphbpe@8192 | `tinape` |  | 1 |
| morphbpe@16384 | `tinape` |  | 1 |
| penalty-1@6080 | `tinape` |  | 1 |
| penalty-1@8192 | `tinape` |  | 1 |
| penalty-1@16384 | `tinape` |  | 1 |
| penalty-2@6080 | `tinape` |  | 1 |
| penalty-2@8192 | `tinape` |  | 1 |
| penalty-2@16384 | `tinape` |  | 1 |
| penalty-4@6080 | `tinape` |  | 1 |
| penalty-4@8192 | `tinape` |  | 1 |
| penalty-4@16384 | `tinape` |  | 1 |
| penalty-8@6080 | `tinape` |  | 1 |
| penalty-8@8192 | `tinape` |  | 1 |
| penalty-8@16384 | `tinape` |  | 1 |
| stochastic-p4-d0.1@6080 | `tinape` |  | 1 |
| stochastic-p4-d0.1@8192 | `tinape` |  | 1 |
| stochastic-p4-d0.1@16384 | `tinape` |  | 1 |
| stochastic-p4-d0.2@6080 | `tinape` |  | 1 |
| stochastic-p4-d0.2@8192 | `tinape` |  | 1 |
| stochastic-p4-d0.2@16384 | `tinape` |  | 1 |
| unigram-ablation@6080 | `tinape` |  | 1 |

## `sinta`  (infixation, tier B_moderate_silver)

**silver gold:** `s+in+ta`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinta` |  | 1 |
| plain@8192 | `sinta` |  | 1 |
| plain@16384 | `sinta` |  | 1 |
| morphbpe@6080 | `sinta` |  | 1 |
| morphbpe@8192 | `sinta` |  | 1 |
| morphbpe@16384 | `sinta` |  | 1 |
| penalty-1@6080 | `sinta` |  | 1 |
| penalty-1@8192 | `sinta` |  | 1 |
| penalty-1@16384 | `sinta` |  | 1 |
| penalty-2@6080 | `sinta` |  | 1 |
| penalty-2@8192 | `sinta` |  | 1 |
| penalty-2@16384 | `sinta` |  | 1 |
| penalty-4@6080 | `sinta` |  | 1 |
| penalty-4@8192 | `sinta` |  | 1 |
| penalty-4@16384 | `sinta` |  | 1 |
| penalty-8@6080 | `sinta` |  | 1 |
| penalty-8@8192 | `sinta` |  | 1 |
| penalty-8@16384 | `sinta` |  | 1 |
| stochastic-p4-d0.1@6080 | `sinta` |  | 1 |
| stochastic-p4-d0.1@8192 | `sinta` |  | 1 |
| stochastic-p4-d0.1@16384 | `sinta` |  | 1 |
| stochastic-p4-d0.2@6080 | `sinta` |  | 1 |
| stochastic-p4-d0.2@8192 | `sinta` |  | 1 |
| stochastic-p4-d0.2@16384 | `sinta` |  | 1 |
| unigram-ablation@6080 | `sinta` |  | 1 |

## `miniabi`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+iabi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mini+abi` |  | 2 |
| plain@8192 | `miniabi` |  | 1 |
| plain@16384 | `miniabi` |  | 1 |
| morphbpe@6080 | `mini+abi` |  | 2 |
| morphbpe@8192 | `miniabi` |  | 1 |
| morphbpe@16384 | `miniabi` |  | 1 |
| penalty-1@6080 | `mini+abi` |  | 2 |
| penalty-1@8192 | `miniabi` |  | 1 |
| penalty-1@16384 | `miniabi` |  | 1 |
| penalty-2@6080 | `mini+abi` |  | 2 |
| penalty-2@8192 | `miniabi` |  | 1 |
| penalty-2@16384 | `miniabi` |  | 1 |
| penalty-4@6080 | `min+iabi` |  | 2 |
| penalty-4@8192 | `miniabi` |  | 1 |
| penalty-4@16384 | `miniabi` |  | 1 |
| penalty-8@6080 | `min+iabi` |  | 2 |
| penalty-8@8192 | `miniabi` |  | 1 |
| penalty-8@16384 | `miniabi` |  | 1 |
| stochastic-p4-d0.1@6080 | `min+iabi` |  | 2 |
| stochastic-p4-d0.1@8192 | `miniabi` |  | 1 |
| stochastic-p4-d0.1@16384 | `miniabi` |  | 1 |
| stochastic-p4-d0.2@6080 | `min+iabi` |  | 2 |
| stochastic-p4-d0.2@8192 | `miniabi` |  | 1 |
| stochastic-p4-d0.2@16384 | `miniabi` |  | 1 |
| unigram-ablation@6080 | `miniabi` |  | 1 |

## `linual`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+ual`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `linual` |  | 1 |
| plain@8192 | `linual` |  | 1 |
| plain@16384 | `linual` |  | 1 |
| morphbpe@6080 | `l+inu+al` |  | 3 |
| morphbpe@8192 | `l+inu+al` |  | 3 |
| morphbpe@16384 | `linu+al` |  | 2 |
| penalty-1@6080 | `l+inu+al` |  | 3 |
| penalty-1@8192 | `l+inu+al` |  | 3 |
| penalty-1@16384 | `linu+al` |  | 2 |
| penalty-2@6080 | `l+inu+al` |  | 3 |
| penalty-2@8192 | `l+inu+al` |  | 3 |
| penalty-2@16384 | `linu+al` |  | 2 |
| penalty-4@6080 | `l+inu+al` |  | 3 |
| penalty-4@8192 | `l+inu+al` |  | 3 |
| penalty-4@16384 | `linu+al` |  | 2 |
| penalty-8@6080 | `l+in+ual` | OK | 3 |
| penalty-8@8192 | `l+in+ual` | OK | 3 |
| penalty-8@16384 | `l+in+ual` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+ual` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+ual` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+ual` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+inu+al` |  | 3 |
| stochastic-p4-d0.2@8192 | `l+inu+al` |  | 3 |
| stochastic-p4-d0.2@16384 | `l+inu+al` |  | 3 |
| unigram-ablation@6080 | `linual` |  | 1 |

## `binang`  (infixation, tier B_moderate_silver)

**silver gold:** `b+in+ang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `binang` |  | 1 |
| plain@8192 | `binang` |  | 1 |
| plain@16384 | `binang` |  | 1 |
| morphbpe@6080 | `binang` |  | 1 |
| morphbpe@8192 | `binang` |  | 1 |
| morphbpe@16384 | `binang` |  | 1 |
| penalty-1@6080 | `binang` |  | 1 |
| penalty-1@8192 | `binang` |  | 1 |
| penalty-1@16384 | `binang` |  | 1 |
| penalty-2@6080 | `binang` |  | 1 |
| penalty-2@8192 | `binang` |  | 1 |
| penalty-2@16384 | `binang` |  | 1 |
| penalty-4@6080 | `binang` |  | 1 |
| penalty-4@8192 | `binang` |  | 1 |
| penalty-4@16384 | `binang` |  | 1 |
| penalty-8@6080 | `binang` |  | 1 |
| penalty-8@8192 | `binang` |  | 1 |
| penalty-8@16384 | `binang` |  | 1 |
| stochastic-p4-d0.1@6080 | `binang` |  | 1 |
| stochastic-p4-d0.1@8192 | `binang` |  | 1 |
| stochastic-p4-d0.1@16384 | `binang` |  | 1 |
| stochastic-p4-d0.2@6080 | `binang` |  | 1 |
| stochastic-p4-d0.2@8192 | `binang` |  | 1 |
| stochastic-p4-d0.2@16384 | `binang` |  | 1 |
| unigram-ablation@6080 | `binang` |  | 1 |

## `dinalan`  (infixation, tier A_strong_silver)

**silver gold:** `d+in+alan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dinalan` |  | 1 |
| plain@8192 | `dinalan` |  | 1 |
| plain@16384 | `dinalan` |  | 1 |
| morphbpe@6080 | `dinalan` |  | 1 |
| morphbpe@8192 | `dinalan` |  | 1 |
| morphbpe@16384 | `dinalan` |  | 1 |
| penalty-1@6080 | `dinalan` |  | 1 |
| penalty-1@8192 | `dinalan` |  | 1 |
| penalty-1@16384 | `dinalan` |  | 1 |
| penalty-2@6080 | `dinalan` |  | 1 |
| penalty-2@8192 | `dinalan` |  | 1 |
| penalty-2@16384 | `dinalan` |  | 1 |
| penalty-4@6080 | `d+in+alan` | OK | 3 |
| penalty-4@8192 | `dinalan` |  | 1 |
| penalty-4@16384 | `dinalan` |  | 1 |
| penalty-8@6080 | `d+in+alan` | OK | 3 |
| penalty-8@8192 | `d+in+alan` | OK | 3 |
| penalty-8@16384 | `d+in+alan` | OK | 3 |
| stochastic-p4-d0.1@6080 | `d+in+alan` | OK | 3 |
| stochastic-p4-d0.1@8192 | `d+in+alan` | OK | 3 |
| stochastic-p4-d0.1@16384 | `dinalan` |  | 1 |
| stochastic-p4-d0.2@6080 | `dinalan` |  | 1 |
| stochastic-p4-d0.2@8192 | `dinalan` |  | 1 |
| stochastic-p4-d0.2@16384 | `dinalan` |  | 1 |
| unigram-ablation@6080 | `dinalan` |  | 1 |

## `tinalakad`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+alakad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tinalakad` |  | 1 |
| plain@8192 | `tinalakad` |  | 1 |
| plain@16384 | `tinalakad` |  | 1 |
| morphbpe@6080 | `tin+alakad` |  | 2 |
| morphbpe@8192 | `tin+alakad` |  | 2 |
| morphbpe@16384 | `tin+alakad` |  | 2 |
| penalty-1@6080 | `t+in+alakad` | OK | 3 |
| penalty-1@8192 | `t+in+alakad` | OK | 3 |
| penalty-1@16384 | `t+in+alakad` | OK | 3 |
| penalty-2@6080 | `t+in+alakad` | OK | 3 |
| penalty-2@8192 | `t+in+alakad` | OK | 3 |
| penalty-2@16384 | `t+in+alakad` | OK | 3 |
| penalty-4@6080 | `t+in+alakad` | OK | 3 |
| penalty-4@8192 | `t+in+alakad` | OK | 3 |
| penalty-4@16384 | `t+in+alakad` | OK | 3 |
| penalty-8@6080 | `t+in+alakad` | OK | 3 |
| penalty-8@8192 | `t+in+alakad` | OK | 3 |
| penalty-8@16384 | `t+in+alakad` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+alakad` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+alakad` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+alakad` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+ala+kad` |  | 4 |
| stochastic-p4-d0.2@8192 | `t+in+ala+kad` |  | 4 |
| stochastic-p4-d0.2@16384 | `t+in+ala+kad` |  | 4 |
| unigram-ablation@6080 | `tin+alakad` |  | 2 |

## `tumula`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `t+um+ula`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tum+ula` |  | 2 |
| plain@8192 | `tumula` |  | 1 |
| plain@16384 | `tumula` |  | 1 |
| morphbpe@6080 | `tu+mula` |  | 2 |
| morphbpe@8192 | `tumula` |  | 1 |
| morphbpe@16384 | `tumula` |  | 1 |
| penalty-1@6080 | `tumu+la` |  | 2 |
| penalty-1@8192 | `tumula` |  | 1 |
| penalty-1@16384 | `tumula` |  | 1 |
| penalty-2@6080 | `tumu+la` |  | 2 |
| penalty-2@8192 | `tumula` |  | 1 |
| penalty-2@16384 | `tumula` |  | 1 |
| penalty-4@6080 | `tumu+la` |  | 2 |
| penalty-4@8192 | `tumula` |  | 1 |
| penalty-4@16384 | `tumula` |  | 1 |
| penalty-8@6080 | `tumu+la` |  | 2 |
| penalty-8@8192 | `tumula` |  | 1 |
| penalty-8@16384 | `tumula` |  | 1 |
| stochastic-p4-d0.1@6080 | `tu+mu+la` |  | 3 |
| stochastic-p4-d0.1@8192 | `tumula` |  | 1 |
| stochastic-p4-d0.1@16384 | `tumula` |  | 1 |
| stochastic-p4-d0.2@6080 | `tu+mu+la` |  | 3 |
| stochastic-p4-d0.2@8192 | `tumula` |  | 1 |
| stochastic-p4-d0.2@16384 | `tumula` |  | 1 |
| unigram-ablation@6080 | `tu+mula` |  | 2 |

## `dinapat`  (infixation, tier A_strong_silver)

**silver gold:** `d+in+apat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `din+apat` |  | 2 |
| plain@8192 | `dinapat` |  | 1 |
| plain@16384 | `dinapat` |  | 1 |
| morphbpe@6080 | `din+apat` |  | 2 |
| morphbpe@8192 | `din+apat` |  | 2 |
| morphbpe@16384 | `din+apat` |  | 2 |
| penalty-1@6080 | `d+in+apat` | OK | 3 |
| penalty-1@8192 | `d+in+apat` | OK | 3 |
| penalty-1@16384 | `d+in+apat` | OK | 3 |
| penalty-2@6080 | `d+in+apat` | OK | 3 |
| penalty-2@8192 | `d+in+apat` | OK | 3 |
| penalty-2@16384 | `d+in+apat` | OK | 3 |
| penalty-4@6080 | `d+in+apat` | OK | 3 |
| penalty-4@8192 | `d+in+apat` | OK | 3 |
| penalty-4@16384 | `d+in+apat` | OK | 3 |
| penalty-8@6080 | `d+in+apat` | OK | 3 |
| penalty-8@8192 | `d+in+apat` | OK | 3 |
| penalty-8@16384 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.1@6080 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.1@8192 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.1@16384 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.2@6080 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.2@8192 | `d+in+apat` | OK | 3 |
| stochastic-p4-d0.2@16384 | `d+in+apat` | OK | 3 |
| unigram-ablation@6080 | `din+apat` |  | 2 |

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

## `linub`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+ub`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `linub` |  | 1 |
| plain@8192 | `linub` |  | 1 |
| plain@16384 | `linub` |  | 1 |
| morphbpe@6080 | `lin+ub` |  | 2 |
| morphbpe@8192 | `lin+ub` |  | 2 |
| morphbpe@16384 | `lin+ub` |  | 2 |
| penalty-1@6080 | `l+in+ub` | OK | 3 |
| penalty-1@8192 | `l+in+ub` | OK | 3 |
| penalty-1@16384 | `l+in+ub` | OK | 3 |
| penalty-2@6080 | `l+in+ub` | OK | 3 |
| penalty-2@8192 | `l+in+ub` | OK | 3 |
| penalty-2@16384 | `l+in+ub` | OK | 3 |
| penalty-4@6080 | `l+in+ub` | OK | 3 |
| penalty-4@8192 | `l+in+ub` | OK | 3 |
| penalty-4@16384 | `l+in+ub` | OK | 3 |
| penalty-8@6080 | `l+in+ub` | OK | 3 |
| penalty-8@8192 | `l+in+ub` | OK | 3 |
| penalty-8@16384 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+ub` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+ub` | OK | 3 |
| unigram-ablation@6080 | `linub` |  | 1 |

## `dininan`  (infixation, tier B_moderate_silver)

**silver gold:** `d+in+inan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dininan` |  | 1 |
| plain@8192 | `dininan` |  | 1 |
| plain@16384 | `dininan` |  | 1 |
| morphbpe@6080 | `dininan` |  | 1 |
| morphbpe@8192 | `dininan` |  | 1 |
| morphbpe@16384 | `dininan` |  | 1 |
| penalty-1@6080 | `dininan` |  | 1 |
| penalty-1@8192 | `dininan` |  | 1 |
| penalty-1@16384 | `dininan` |  | 1 |
| penalty-2@6080 | `dininan` |  | 1 |
| penalty-2@8192 | `dininan` |  | 1 |
| penalty-2@16384 | `dininan` |  | 1 |
| penalty-4@6080 | `dininan` |  | 1 |
| penalty-4@8192 | `dininan` |  | 1 |
| penalty-4@16384 | `dininan` |  | 1 |
| penalty-8@6080 | `d+in+in+an` |  | 4 |
| penalty-8@8192 | `d+in+in+an` |  | 4 |
| penalty-8@16384 | `dininan` |  | 1 |
| stochastic-p4-d0.1@6080 | `d+in+in+an` |  | 4 |
| stochastic-p4-d0.1@8192 | `dininan` |  | 1 |
| stochastic-p4-d0.1@16384 | `dininan` |  | 1 |
| stochastic-p4-d0.2@6080 | `d+in+in+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `dininan` |  | 1 |
| stochastic-p4-d0.2@16384 | `dininan` |  | 1 |
| unigram-ablation@6080 | `dininan` |  | 1 |

## `ninumang`  (infixation, tier B_moderate_silver)

**silver gold:** `n+in+umang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ninumang` |  | 1 |
| plain@8192 | `ninumang` |  | 1 |
| plain@16384 | `ninumang` |  | 1 |
| morphbpe@6080 | `ninumang` |  | 1 |
| morphbpe@8192 | `ninumang` |  | 1 |
| morphbpe@16384 | `ninumang` |  | 1 |
| penalty-1@6080 | `ninumang` |  | 1 |
| penalty-1@8192 | `ninumang` |  | 1 |
| penalty-1@16384 | `ninumang` |  | 1 |
| penalty-2@6080 | `ninumang` |  | 1 |
| penalty-2@8192 | `ninumang` |  | 1 |
| penalty-2@16384 | `ninumang` |  | 1 |
| penalty-4@6080 | `ninumang` |  | 1 |
| penalty-4@8192 | `ninumang` |  | 1 |
| penalty-4@16384 | `ninumang` |  | 1 |
| penalty-8@6080 | `ninumang` |  | 1 |
| penalty-8@8192 | `ninumang` |  | 1 |
| penalty-8@16384 | `ninumang` |  | 1 |
| stochastic-p4-d0.1@6080 | `ninumang` |  | 1 |
| stochastic-p4-d0.1@8192 | `ninumang` |  | 1 |
| stochastic-p4-d0.1@16384 | `ninumang` |  | 1 |
| stochastic-p4-d0.2@6080 | `ninumang` |  | 1 |
| stochastic-p4-d0.2@8192 | `ninumang` |  | 1 |
| stochastic-p4-d0.2@16384 | `ninumang` |  | 1 |
| unigram-ablation@6080 | `ninuman+g` |  | 2 |

## `ninung`  (infixation, tier A_strong_silver)

**silver gold:** `n+in+ung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `n+inung` |  | 2 |
| plain@8192 | `ninung` |  | 1 |
| plain@16384 | `ninung` |  | 1 |
| morphbpe@6080 | `n+inung` |  | 2 |
| morphbpe@8192 | `n+inung` |  | 2 |
| morphbpe@16384 | `n+inung` |  | 2 |
| penalty-1@6080 | `n+inung` |  | 2 |
| penalty-1@8192 | `n+inung` |  | 2 |
| penalty-1@16384 | `n+inung` |  | 2 |
| penalty-2@6080 | `n+in+ung` | OK | 3 |
| penalty-2@8192 | `n+in+ung` | OK | 3 |
| penalty-2@16384 | `n+in+ung` | OK | 3 |
| penalty-4@6080 | `n+in+ung` | OK | 3 |
| penalty-4@8192 | `n+in+ung` | OK | 3 |
| penalty-4@16384 | `n+in+ung` | OK | 3 |
| penalty-8@6080 | `n+in+ung` | OK | 3 |
| penalty-8@8192 | `n+in+ung` | OK | 3 |
| penalty-8@16384 | `n+in+ung` | OK | 3 |
| stochastic-p4-d0.1@6080 | `nin+ung` |  | 2 |
| stochastic-p4-d0.1@8192 | `nin+ung` |  | 2 |
| stochastic-p4-d0.1@16384 | `nin+ung` |  | 2 |
| stochastic-p4-d0.2@6080 | `n+in+ung` | OK | 3 |
| stochastic-p4-d0.2@8192 | `n+in+ung` | OK | 3 |
| stochastic-p4-d0.2@16384 | `n+in+ung` | OK | 3 |
| unigram-ablation@6080 | `ninu+ng` |  | 2 |

## `linigtas`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+igtas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+igtas` |  | 2 |
| plain@8192 | `lin+igtas` |  | 2 |
| plain@16384 | `linigtas` |  | 1 |
| morphbpe@6080 | `lin+ig+tas` |  | 3 |
| morphbpe@8192 | `lin+igtas` |  | 2 |
| morphbpe@16384 | `lin+igtas` |  | 2 |
| penalty-1@6080 | `l+in+ig+tas` |  | 4 |
| penalty-1@8192 | `l+in+igtas` | OK | 3 |
| penalty-1@16384 | `l+in+igtas` | OK | 3 |
| penalty-2@6080 | `l+in+ig+tas` |  | 4 |
| penalty-2@8192 | `l+in+igtas` | OK | 3 |
| penalty-2@16384 | `l+in+igtas` | OK | 3 |
| penalty-4@6080 | `l+in+ig+tas` |  | 4 |
| penalty-4@8192 | `l+in+igtas` | OK | 3 |
| penalty-4@16384 | `l+in+igtas` | OK | 3 |
| penalty-8@6080 | `l+in+ig+tas` |  | 4 |
| penalty-8@8192 | `l+in+igtas` | OK | 3 |
| penalty-8@16384 | `l+in+igtas` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+ig+tas` |  | 4 |
| stochastic-p4-d0.1@8192 | `l+in+igtas` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+igtas` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+igtas` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+igtas` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+igtas` | OK | 3 |
| unigram-ablation@6080 | `lin+igtas` |  | 2 |

## `sumpa`  (infixation, tier B_moderate_silver)

**silver gold:** `s+um+pa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sum+pa` |  | 2 |
| plain@8192 | `sum+pa` |  | 2 |
| plain@16384 | `sumpa` |  | 1 |
| morphbpe@6080 | `sum+pa` |  | 2 |
| morphbpe@8192 | `sumpa` |  | 1 |
| morphbpe@16384 | `sumpa` |  | 1 |
| penalty-1@6080 | `s+umpa` |  | 2 |
| penalty-1@8192 | `sumpa` |  | 1 |
| penalty-1@16384 | `sumpa` |  | 1 |
| penalty-2@6080 | `s+umpa` |  | 2 |
| penalty-2@8192 | `sumpa` |  | 1 |
| penalty-2@16384 | `sumpa` |  | 1 |
| penalty-4@6080 | `s+umpa` |  | 2 |
| penalty-4@8192 | `sumpa` |  | 1 |
| penalty-4@16384 | `sumpa` |  | 1 |
| penalty-8@6080 | `sumpa` |  | 1 |
| penalty-8@8192 | `sumpa` |  | 1 |
| penalty-8@16384 | `sumpa` |  | 1 |
| stochastic-p4-d0.1@6080 | `s+umpa` |  | 2 |
| stochastic-p4-d0.1@8192 | `sumpa` |  | 1 |
| stochastic-p4-d0.1@16384 | `sumpa` |  | 1 |
| stochastic-p4-d0.2@6080 | `sum+pa` |  | 2 |
| stochastic-p4-d0.2@8192 | `sumpa` |  | 1 |
| stochastic-p4-d0.2@16384 | `sumpa` |  | 1 |
| unigram-ablation@6080 | `sumpa` |  | 1 |

## `sinampa`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+ampa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+ampa` |  | 2 |
| plain@8192 | `sin+ampa` |  | 2 |
| plain@16384 | `sinampa` |  | 1 |
| morphbpe@6080 | `sin+ampa` |  | 2 |
| morphbpe@8192 | `sin+ampa` |  | 2 |
| morphbpe@16384 | `sin+ampa` |  | 2 |
| penalty-1@6080 | `s+in+ampa` | OK | 3 |
| penalty-1@8192 | `s+in+ampa` | OK | 3 |
| penalty-1@16384 | `s+in+ampa` | OK | 3 |
| penalty-2@6080 | `s+in+ampa` | OK | 3 |
| penalty-2@8192 | `s+in+ampa` | OK | 3 |
| penalty-2@16384 | `s+in+ampa` | OK | 3 |
| penalty-4@6080 | `s+in+ampa` | OK | 3 |
| penalty-4@8192 | `s+in+ampa` | OK | 3 |
| penalty-4@16384 | `s+in+ampa` | OK | 3 |
| penalty-8@6080 | `s+in+am+pa` |  | 4 |
| penalty-8@8192 | `s+in+ampa` | OK | 3 |
| penalty-8@16384 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.1@6080 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.1@8192 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.1@16384 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.2@6080 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.2@8192 | `s+in+ampa` | OK | 3 |
| stochastic-p4-d0.2@16384 | `s+in+ampa` | OK | 3 |
| unigram-ablation@6080 | `s+inampa` |  | 2 |

## `kinanua`  (infixation, tier B_moderate_silver)

**silver gold:** `k+in+anua`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kin+anua` |  | 2 |
| plain@8192 | `kin+anua` |  | 2 |
| plain@16384 | `kinanua` |  | 1 |
| morphbpe@6080 | `k+inan+ua` |  | 3 |
| morphbpe@8192 | `k+inan+ua` |  | 3 |
| morphbpe@16384 | `kinanua` |  | 1 |
| penalty-1@6080 | `k+inan+ua` |  | 3 |
| penalty-1@8192 | `k+inan+ua` |  | 3 |
| penalty-1@16384 | `kinanua` |  | 1 |
| penalty-2@6080 | `k+in+an+ua` |  | 4 |
| penalty-2@8192 | `k+in+an+ua` |  | 4 |
| penalty-2@16384 | `kinanua` |  | 1 |
| penalty-4@6080 | `k+in+anua` | OK | 3 |
| penalty-4@8192 | `k+in+anua` | OK | 3 |
| penalty-4@16384 | `kinanua` |  | 1 |
| penalty-8@6080 | `k+in+an+ua` |  | 4 |
| penalty-8@8192 | `k+in+an+ua` |  | 4 |
| penalty-8@16384 | `kinanua` |  | 1 |
| stochastic-p4-d0.1@6080 | `k+in+an+ua` |  | 4 |
| stochastic-p4-d0.1@8192 | `k+in+an+ua` |  | 4 |
| stochastic-p4-d0.1@16384 | `kinanua` |  | 1 |
| stochastic-p4-d0.2@6080 | `k+in+anua` | OK | 3 |
| stochastic-p4-d0.2@8192 | `k+in+anua` | OK | 3 |
| stochastic-p4-d0.2@16384 | `kinanua` |  | 1 |
| unigram-ablation@6080 | `ki+nanu+a` |  | 3 |

## `linapit`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+apit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `linapit` |  | 1 |
| plain@8192 | `linapit` |  | 1 |
| plain@16384 | `linapit` |  | 1 |
| morphbpe@6080 | `lin+apit` |  | 2 |
| morphbpe@8192 | `lin+apit` |  | 2 |
| morphbpe@16384 | `lin+apit` |  | 2 |
| penalty-1@6080 | `l+in+apit` | OK | 3 |
| penalty-1@8192 | `l+in+apit` | OK | 3 |
| penalty-1@16384 | `l+in+apit` | OK | 3 |
| penalty-2@6080 | `l+in+apit` | OK | 3 |
| penalty-2@8192 | `l+in+apit` | OK | 3 |
| penalty-2@16384 | `l+in+apit` | OK | 3 |
| penalty-4@6080 | `l+in+apit` | OK | 3 |
| penalty-4@8192 | `l+in+apit` | OK | 3 |
| penalty-4@16384 | `l+in+apit` | OK | 3 |
| penalty-8@6080 | `l+in+apit` | OK | 3 |
| penalty-8@8192 | `l+in+apit` | OK | 3 |
| penalty-8@16384 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+apit` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+apit` | OK | 3 |
| unigram-ablation@6080 | `linap+it` |  | 2 |

## `binye`  (infixation, tier A_strong_silver)

**silver gold:** `b+in+ye`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bin+ye` |  | 2 |
| plain@8192 | `binye` |  | 1 |
| plain@16384 | `binye` |  | 1 |
| morphbpe@6080 | `bin+ye` |  | 2 |
| morphbpe@8192 | `bin+ye` |  | 2 |
| morphbpe@16384 | `bin+ye` |  | 2 |
| penalty-1@6080 | `b+in+ye` | OK | 3 |
| penalty-1@8192 | `b+in+ye` | OK | 3 |
| penalty-1@16384 | `b+in+ye` | OK | 3 |
| penalty-2@6080 | `b+in+ye` | OK | 3 |
| penalty-2@8192 | `b+in+ye` | OK | 3 |
| penalty-2@16384 | `b+in+ye` | OK | 3 |
| penalty-4@6080 | `b+in+ye` | OK | 3 |
| penalty-4@8192 | `b+in+ye` | OK | 3 |
| penalty-4@16384 | `b+in+ye` | OK | 3 |
| penalty-8@6080 | `b+in+ye` | OK | 3 |
| penalty-8@8192 | `b+in+ye` | OK | 3 |
| penalty-8@16384 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.1@6080 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.1@8192 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.1@16384 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.2@6080 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.2@8192 | `b+in+ye` | OK | 3 |
| stochastic-p4-d0.2@16384 | `b+in+ye` | OK | 3 |
| unigram-ablation@6080 | `bin+ye` |  | 2 |

## `linto`  (infixation, tier B_moderate_silver)

**silver gold:** `l+in+to`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `linto` |  | 1 |
| plain@8192 | `linto` |  | 1 |
| plain@16384 | `linto` |  | 1 |
| morphbpe@6080 | `linto` |  | 1 |
| morphbpe@8192 | `linto` |  | 1 |
| morphbpe@16384 | `linto` |  | 1 |
| penalty-1@6080 | `linto` |  | 1 |
| penalty-1@8192 | `linto` |  | 1 |
| penalty-1@16384 | `linto` |  | 1 |
| penalty-2@6080 | `linto` |  | 1 |
| penalty-2@8192 | `linto` |  | 1 |
| penalty-2@16384 | `linto` |  | 1 |
| penalty-4@6080 | `linto` |  | 1 |
| penalty-4@8192 | `linto` |  | 1 |
| penalty-4@16384 | `linto` |  | 1 |
| penalty-8@6080 | `linto` |  | 1 |
| penalty-8@8192 | `linto` |  | 1 |
| penalty-8@16384 | `linto` |  | 1 |
| stochastic-p4-d0.1@6080 | `linto` |  | 1 |
| stochastic-p4-d0.1@8192 | `linto` |  | 1 |
| stochastic-p4-d0.1@16384 | `linto` |  | 1 |
| stochastic-p4-d0.2@6080 | `linto` |  | 1 |
| stochastic-p4-d0.2@8192 | `linto` |  | 1 |
| stochastic-p4-d0.2@16384 | `linto` |  | 1 |
| unigram-ablation@6080 | `linto` |  | 1 |

## `pinili`  (infixation, tier A_strong_silver)

**silver gold:** `p+in+ili`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pinili` |  | 1 |
| plain@8192 | `pinili` |  | 1 |
| plain@16384 | `pinili` |  | 1 |
| morphbpe@6080 | `pin+ili` |  | 2 |
| morphbpe@8192 | `pin+ili` |  | 2 |
| morphbpe@16384 | `pin+ili` |  | 2 |
| penalty-1@6080 | `pin+ili` |  | 2 |
| penalty-1@8192 | `pin+ili` |  | 2 |
| penalty-1@16384 | `pin+ili` |  | 2 |
| penalty-2@6080 | `pin+ili` |  | 2 |
| penalty-2@8192 | `pin+ili` |  | 2 |
| penalty-2@16384 | `pin+ili` |  | 2 |
| penalty-4@6080 | `pin+ili` |  | 2 |
| penalty-4@8192 | `pin+ili` |  | 2 |
| penalty-4@16384 | `pin+ili` |  | 2 |
| penalty-8@6080 | `pin+ili` |  | 2 |
| penalty-8@8192 | `pin+ili` |  | 2 |
| penalty-8@16384 | `pin+ili` |  | 2 |
| stochastic-p4-d0.1@6080 | `pin+ili` |  | 2 |
| stochastic-p4-d0.1@8192 | `pin+ili` |  | 2 |
| stochastic-p4-d0.1@16384 | `pin+ili` |  | 2 |
| stochastic-p4-d0.2@6080 | `pin+ili` |  | 2 |
| stochastic-p4-d0.2@8192 | `pin+ili` |  | 2 |
| stochastic-p4-d0.2@16384 | `pin+ili` |  | 2 |
| unigram-ablation@6080 | `pinili` |  | 1 |

## `sintang`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `sintang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+tang` |  | 2 |
| plain@8192 | `sintang` | OK | 1 |
| plain@16384 | `sintang` | OK | 1 |
| morphbpe@6080 | `sint+ang` |  | 2 |
| morphbpe@8192 | `sintang` | OK | 1 |
| morphbpe@16384 | `sintang` | OK | 1 |
| penalty-1@6080 | `sint+ang` |  | 2 |
| penalty-1@8192 | `sintang` | OK | 1 |
| penalty-1@16384 | `sintang` | OK | 1 |
| penalty-2@6080 | `s+intang` |  | 2 |
| penalty-2@8192 | `s+intang` |  | 2 |
| penalty-2@16384 | `sintang` | OK | 1 |
| penalty-4@6080 | `s+intang` |  | 2 |
| penalty-4@8192 | `sintang` | OK | 1 |
| penalty-4@16384 | `sintang` | OK | 1 |
| penalty-8@6080 | `s+intang` |  | 2 |
| penalty-8@8192 | `sintang` | OK | 1 |
| penalty-8@16384 | `sintang` | OK | 1 |
| stochastic-p4-d0.1@6080 | `s+intang` |  | 2 |
| stochastic-p4-d0.1@8192 | `sintang` | OK | 1 |
| stochastic-p4-d0.1@16384 | `sintang` | OK | 1 |
| stochastic-p4-d0.2@6080 | `s+intang` |  | 2 |
| stochastic-p4-d0.2@8192 | `s+intang` |  | 2 |
| stochastic-p4-d0.2@16384 | `sintang` | OK | 1 |
| unigram-ablation@6080 | `sinta+ng` |  | 2 |

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

## `lumakad`  (infixation, tier A_strong_silver)

**silver gold:** `l+um+akad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `luma+kad` |  | 2 |
| plain@8192 | `luma+kad` |  | 2 |
| plain@16384 | `lumakad` |  | 1 |
| morphbpe@6080 | `lu+maka+d` |  | 3 |
| morphbpe@8192 | `lu+maka+d` |  | 3 |
| morphbpe@16384 | `lu+maka+d` |  | 3 |
| penalty-1@6080 | `lu+maka+d` |  | 3 |
| penalty-1@8192 | `lu+maka+d` |  | 3 |
| penalty-1@16384 | `lu+maka+d` |  | 3 |
| penalty-2@6080 | `lu+maka+d` |  | 3 |
| penalty-2@8192 | `lu+maka+d` |  | 3 |
| penalty-2@16384 | `lu+maka+d` |  | 3 |
| penalty-4@6080 | `lu+maka+d` |  | 3 |
| penalty-4@8192 | `lu+maka+d` |  | 3 |
| penalty-4@16384 | `lu+maka+d` |  | 3 |
| penalty-8@6080 | `lu+maka+d` |  | 3 |
| penalty-8@8192 | `lu+maka+d` |  | 3 |
| penalty-8@16384 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.1@6080 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.1@8192 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.1@16384 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.2@6080 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.2@8192 | `lu+maka+d` |  | 3 |
| stochastic-p4-d0.2@16384 | `lu+maka+d` |  | 3 |
| unigram-ablation@6080 | `luma+kad` |  | 2 |

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

## `tumakut`  (infixation, tier A_strong_silver)

**silver gold:** `t+um+akut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tum+akut` |  | 2 |
| plain@8192 | `tum+akut` |  | 2 |
| plain@16384 | `tum+akut` |  | 2 |
| morphbpe@6080 | `tum+ak+ut` |  | 3 |
| morphbpe@8192 | `tum+ak+ut` |  | 3 |
| morphbpe@16384 | `tum+akut` |  | 2 |
| penalty-1@6080 | `tu+ma+kut` |  | 3 |
| penalty-1@8192 | `tu+ma+kut` |  | 3 |
| penalty-1@16384 | `tu+ma+kut` |  | 3 |
| penalty-2@6080 | `tu+ma+kut` |  | 3 |
| penalty-2@8192 | `tu+ma+kut` |  | 3 |
| penalty-2@16384 | `tu+ma+kut` |  | 3 |
| penalty-4@6080 | `tu+ma+kut` |  | 3 |
| penalty-4@8192 | `tu+ma+kut` |  | 3 |
| penalty-4@16384 | `tu+ma+kut` |  | 3 |
| penalty-8@6080 | `tu+ma+kut` |  | 3 |
| penalty-8@8192 | `tu+ma+kut` |  | 3 |
| penalty-8@16384 | `tuma+kut` |  | 2 |
| stochastic-p4-d0.1@6080 | `tu+ma+kut` |  | 3 |
| stochastic-p4-d0.1@8192 | `tu+ma+kut` |  | 3 |
| stochastic-p4-d0.1@16384 | `tuma+kut` |  | 2 |
| stochastic-p4-d0.2@6080 | `tu+ma+kut` |  | 3 |
| stochastic-p4-d0.2@8192 | `tu+ma+kut` |  | 3 |
| stochastic-p4-d0.2@16384 | `tuma+kut` |  | 2 |
| unigram-ablation@6080 | `tum+aku+t` |  | 3 |

## `tinakas`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+akas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tin+a+kas` |  | 3 |
| plain@8192 | `tin+akas` |  | 2 |
| plain@16384 | `tinakas` |  | 1 |
| morphbpe@6080 | `t+ina+kas` |  | 3 |
| morphbpe@8192 | `t+ina+kas` |  | 3 |
| morphbpe@16384 | `t+ina+kas` |  | 3 |
| penalty-1@6080 | `t+ina+kas` |  | 3 |
| penalty-1@8192 | `t+ina+kas` |  | 3 |
| penalty-1@16384 | `tina+kas` |  | 2 |
| penalty-2@6080 | `t+ina+kas` |  | 3 |
| penalty-2@8192 | `t+ina+kas` |  | 3 |
| penalty-2@16384 | `tina+kas` |  | 2 |
| penalty-4@6080 | `t+in+akas` | OK | 3 |
| penalty-4@8192 | `t+in+akas` | OK | 3 |
| penalty-4@16384 | `t+in+akas` | OK | 3 |
| penalty-8@6080 | `t+in+a+kas` |  | 4 |
| penalty-8@8192 | `t+in+akas` | OK | 3 |
| penalty-8@16384 | `t+in+akas` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+akas` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+akas` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+akas` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+aka+s` |  | 4 |
| stochastic-p4-d0.2@8192 | `t+in+akas` | OK | 3 |
| stochastic-p4-d0.2@16384 | `t+in+akas` | OK | 3 |
| unigram-ablation@6080 | `ti+na+kas` |  | 3 |

## `tinas`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+as`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+inas` |  | 2 |
| plain@8192 | `t+inas` |  | 2 |
| plain@16384 | `tinas` |  | 1 |
| morphbpe@6080 | `tin+as` |  | 2 |
| morphbpe@8192 | `tin+as` |  | 2 |
| morphbpe@16384 | `tin+as` |  | 2 |
| penalty-1@6080 | `t+in+as` | OK | 3 |
| penalty-1@8192 | `t+in+as` | OK | 3 |
| penalty-1@16384 | `t+in+as` | OK | 3 |
| penalty-2@6080 | `t+in+as` | OK | 3 |
| penalty-2@8192 | `t+in+as` | OK | 3 |
| penalty-2@16384 | `t+in+as` | OK | 3 |
| penalty-4@6080 | `t+in+as` | OK | 3 |
| penalty-4@8192 | `t+in+as` | OK | 3 |
| penalty-4@16384 | `t+in+as` | OK | 3 |
| penalty-8@6080 | `t+in+as` | OK | 3 |
| penalty-8@8192 | `t+in+as` | OK | 3 |
| penalty-8@16384 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.2@8192 | `t+in+as` | OK | 3 |
| stochastic-p4-d0.2@16384 | `t+in+as` | OK | 3 |
| unigram-ablation@6080 | `tin+as` |  | 2 |

## `linawe`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `l+in+awe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+awe` |  | 2 |
| plain@8192 | `linawe` |  | 1 |
| plain@16384 | `linawe` |  | 1 |
| morphbpe@6080 | `lina+we` |  | 2 |
| morphbpe@8192 | `linawe` |  | 1 |
| morphbpe@16384 | `linawe` |  | 1 |
| penalty-1@6080 | `lina+we` |  | 2 |
| penalty-1@8192 | `linawe` |  | 1 |
| penalty-1@16384 | `linawe` |  | 1 |
| penalty-2@6080 | `lina+we` |  | 2 |
| penalty-2@8192 | `linawe` |  | 1 |
| penalty-2@16384 | `linawe` |  | 1 |
| penalty-4@6080 | `l+inawe` |  | 2 |
| penalty-4@8192 | `linawe` |  | 1 |
| penalty-4@16384 | `linawe` |  | 1 |
| penalty-8@6080 | `l+in+awe` | OK | 3 |
| penalty-8@8192 | `linawe` |  | 1 |
| penalty-8@16384 | `linawe` |  | 1 |
| stochastic-p4-d0.1@6080 | `l+in+awe` | OK | 3 |
| stochastic-p4-d0.1@8192 | `linawe` |  | 1 |
| stochastic-p4-d0.1@16384 | `linawe` |  | 1 |
| stochastic-p4-d0.2@6080 | `l+in+awe` | OK | 3 |
| stochastic-p4-d0.2@8192 | `linawe` |  | 1 |
| stochastic-p4-d0.2@16384 | `linawe` |  | 1 |
| unigram-ablation@6080 | `linawe` |  | 1 |

## `mumunang`  (infixation, tier B_moderate_silver)

**silver gold:** `m+um+unang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mumunang` |  | 1 |
| plain@8192 | `mumunang` |  | 1 |
| plain@16384 | `mumunang` |  | 1 |
| morphbpe@6080 | `mumunang` |  | 1 |
| morphbpe@8192 | `mumunang` |  | 1 |
| morphbpe@16384 | `mumunang` |  | 1 |
| penalty-1@6080 | `mumunang` |  | 1 |
| penalty-1@8192 | `mumunang` |  | 1 |
| penalty-1@16384 | `mumunang` |  | 1 |
| penalty-2@6080 | `mumunang` |  | 1 |
| penalty-2@8192 | `mumunang` |  | 1 |
| penalty-2@16384 | `mumunang` |  | 1 |
| penalty-4@6080 | `mumunang` |  | 1 |
| penalty-4@8192 | `mumunang` |  | 1 |
| penalty-4@16384 | `mumunang` |  | 1 |
| penalty-8@6080 | `mumunang` |  | 1 |
| penalty-8@8192 | `mumunang` |  | 1 |
| penalty-8@16384 | `mumunang` |  | 1 |
| stochastic-p4-d0.1@6080 | `mumunang` |  | 1 |
| stochastic-p4-d0.1@8192 | `mumunang` |  | 1 |
| stochastic-p4-d0.1@16384 | `mumunang` |  | 1 |
| stochastic-p4-d0.2@6080 | `mumunang` |  | 1 |
| stochastic-p4-d0.2@8192 | `mumunang` |  | 1 |
| stochastic-p4-d0.2@16384 | `mumunang` |  | 1 |
| unigram-ablation@6080 | `mumunang` |  | 1 |

## `sinugat`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+ugat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+ug+at` |  | 3 |
| plain@8192 | `sin+ugat` |  | 2 |
| plain@16384 | `sinugat` |  | 1 |
| morphbpe@6080 | `sin+ug+at` |  | 3 |
| morphbpe@8192 | `sin+ugat` |  | 2 |
| morphbpe@16384 | `sin+ugat` |  | 2 |
| penalty-1@6080 | `s+in+ug+at` |  | 4 |
| penalty-1@8192 | `s+in+ugat` | OK | 3 |
| penalty-1@16384 | `s+in+ugat` | OK | 3 |
| penalty-2@6080 | `s+in+ug+at` |  | 4 |
| penalty-2@8192 | `s+in+ugat` | OK | 3 |
| penalty-2@16384 | `s+in+ugat` | OK | 3 |
| penalty-4@6080 | `s+in+ug+at` |  | 4 |
| penalty-4@8192 | `s+in+ugat` | OK | 3 |
| penalty-4@16384 | `s+in+ugat` | OK | 3 |
| penalty-8@6080 | `s+in+ug+at` |  | 4 |
| penalty-8@8192 | `s+in+ugat` | OK | 3 |
| penalty-8@16384 | `s+in+ugat` | OK | 3 |
| stochastic-p4-d0.1@6080 | `s+in+ug+at` |  | 4 |
| stochastic-p4-d0.1@8192 | `s+in+ugat` | OK | 3 |
| stochastic-p4-d0.1@16384 | `s+in+ugat` | OK | 3 |
| stochastic-p4-d0.2@6080 | `s+in+ugat` | OK | 3 |
| stochastic-p4-d0.2@8192 | `s+in+ugat` | OK | 3 |
| stochastic-p4-d0.2@16384 | `s+in+ugat` | OK | 3 |
| unigram-ablation@6080 | `sin+u+g+at` |  | 4 |

## `sinuyu`  (infixation, tier B_moderate_silver)

**silver gold:** `s+in+uyu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinuyu` |  | 1 |
| plain@8192 | `sinuyu` |  | 1 |
| plain@16384 | `sinuyu` |  | 1 |
| morphbpe@6080 | `sinuyu` |  | 1 |
| morphbpe@8192 | `sinuyu` |  | 1 |
| morphbpe@16384 | `sinuyu` |  | 1 |
| penalty-1@6080 | `sinuyu` |  | 1 |
| penalty-1@8192 | `sinuyu` |  | 1 |
| penalty-1@16384 | `sinuyu` |  | 1 |
| penalty-2@6080 | `sinuyu` |  | 1 |
| penalty-2@8192 | `sinuyu` |  | 1 |
| penalty-2@16384 | `sinuyu` |  | 1 |
| penalty-4@6080 | `sinuyu` |  | 1 |
| penalty-4@8192 | `sinuyu` |  | 1 |
| penalty-4@16384 | `sinuyu` |  | 1 |
| penalty-8@6080 | `sinuyu` |  | 1 |
| penalty-8@8192 | `sinuyu` |  | 1 |
| penalty-8@16384 | `sinuyu` |  | 1 |
| stochastic-p4-d0.1@6080 | `sinuyu` |  | 1 |
| stochastic-p4-d0.1@8192 | `sinuyu` |  | 1 |
| stochastic-p4-d0.1@16384 | `sinuyu` |  | 1 |
| stochastic-p4-d0.2@6080 | `sinuyu` |  | 1 |
| stochastic-p4-d0.2@8192 | `sinuyu` |  | 1 |
| stochastic-p4-d0.2@16384 | `sinuyu` |  | 1 |
| unigram-ablation@6080 | `sinuyu` |  | 1 |

## `dinalung`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `d+in+alung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `din+alung` |  | 2 |
| plain@8192 | `din+alung` |  | 2 |
| plain@16384 | `din+alung` |  | 2 |
| morphbpe@6080 | `din+alung` |  | 2 |
| morphbpe@8192 | `din+alung` |  | 2 |
| morphbpe@16384 | `din+alung` |  | 2 |
| penalty-1@6080 | `d+inal+ung` |  | 3 |
| penalty-1@8192 | `d+inal+ung` |  | 3 |
| penalty-1@16384 | `dinal+ung` |  | 2 |
| penalty-2@6080 | `d+inal+ung` |  | 3 |
| penalty-2@8192 | `d+inal+ung` |  | 3 |
| penalty-2@16384 | `d+inal+ung` |  | 3 |
| penalty-4@6080 | `d+in+alung` | OK | 3 |
| penalty-4@8192 | `d+in+alung` | OK | 3 |
| penalty-4@16384 | `d+in+alung` | OK | 3 |
| penalty-8@6080 | `d+in+alung` | OK | 3 |
| penalty-8@8192 | `d+in+alung` | OK | 3 |
| penalty-8@16384 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.1@6080 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.1@8192 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.1@16384 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.2@6080 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.2@8192 | `d+in+alung` | OK | 3 |
| stochastic-p4-d0.2@16384 | `d+in+alung` | OK | 3 |
| unigram-ablation@6080 | `dinal+ung` |  | 2 |

## `dinam`  (infixation, tier A_strong_silver)

**silver gold:** `d+in+am`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `din+am` |  | 2 |
| plain@8192 | `din+am` |  | 2 |
| plain@16384 | `dinam` |  | 1 |
| morphbpe@6080 | `din+am` |  | 2 |
| morphbpe@8192 | `din+am` |  | 2 |
| morphbpe@16384 | `din+am` |  | 2 |
| penalty-1@6080 | `d+in+am` | OK | 3 |
| penalty-1@8192 | `d+in+am` | OK | 3 |
| penalty-1@16384 | `d+in+am` | OK | 3 |
| penalty-2@6080 | `d+in+am` | OK | 3 |
| penalty-2@8192 | `d+in+am` | OK | 3 |
| penalty-2@16384 | `d+in+am` | OK | 3 |
| penalty-4@6080 | `d+in+am` | OK | 3 |
| penalty-4@8192 | `d+in+am` | OK | 3 |
| penalty-4@16384 | `d+in+am` | OK | 3 |
| penalty-8@6080 | `d+in+am` | OK | 3 |
| penalty-8@8192 | `d+in+am` | OK | 3 |
| penalty-8@16384 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.1@6080 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.1@8192 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.1@16384 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.2@6080 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.2@8192 | `d+in+am` | OK | 3 |
| stochastic-p4-d0.2@16384 | `d+in+am` | OK | 3 |
| unigram-ablation@6080 | `di+na+m` |  | 3 |

## `minaus`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+aus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+aus` |  | 2 |
| plain@8192 | `min+aus` |  | 2 |
| plain@16384 | `minaus` |  | 1 |
| morphbpe@6080 | `m+inaus` |  | 2 |
| morphbpe@8192 | `m+inaus` |  | 2 |
| morphbpe@16384 | `minaus` |  | 1 |
| penalty-1@6080 | `min+aus` |  | 2 |
| penalty-1@8192 | `min+aus` |  | 2 |
| penalty-1@16384 | `minaus` |  | 1 |
| penalty-2@6080 | `min+aus` |  | 2 |
| penalty-2@8192 | `min+aus` |  | 2 |
| penalty-2@16384 | `minaus` |  | 1 |
| penalty-4@6080 | `min+aus` |  | 2 |
| penalty-4@8192 | `min+aus` |  | 2 |
| penalty-4@16384 | `minaus` |  | 1 |
| penalty-8@6080 | `min+aus` |  | 2 |
| penalty-8@8192 | `min+aus` |  | 2 |
| penalty-8@16384 | `minaus` |  | 1 |
| stochastic-p4-d0.1@6080 | `min+aus` |  | 2 |
| stochastic-p4-d0.1@8192 | `min+aus` |  | 2 |
| stochastic-p4-d0.1@16384 | `minaus` |  | 1 |
| stochastic-p4-d0.2@6080 | `min+aus` |  | 2 |
| stochastic-p4-d0.2@8192 | `min+aus` |  | 2 |
| stochastic-p4-d0.2@16384 | `minaus` |  | 1 |
| unigram-ablation@6080 | `m+inaus` |  | 2 |

## `minunang`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+unang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `minunang` |  | 1 |
| plain@8192 | `minunang` |  | 1 |
| plain@16384 | `minunang` |  | 1 |
| morphbpe@6080 | `minunang` |  | 1 |
| morphbpe@8192 | `minunang` |  | 1 |
| morphbpe@16384 | `minunang` |  | 1 |
| penalty-1@6080 | `minunang` |  | 1 |
| penalty-1@8192 | `minunang` |  | 1 |
| penalty-1@16384 | `minunang` |  | 1 |
| penalty-2@6080 | `minunang` |  | 1 |
| penalty-2@8192 | `minunang` |  | 1 |
| penalty-2@16384 | `minunang` |  | 1 |
| penalty-4@6080 | `minunang` |  | 1 |
| penalty-4@8192 | `minunang` |  | 1 |
| penalty-4@16384 | `minunang` |  | 1 |
| penalty-8@6080 | `minunang` |  | 1 |
| penalty-8@8192 | `minunang` |  | 1 |
| penalty-8@16384 | `minunang` |  | 1 |
| stochastic-p4-d0.1@6080 | `minunang` |  | 1 |
| stochastic-p4-d0.1@8192 | `minunang` |  | 1 |
| stochastic-p4-d0.1@16384 | `minunang` |  | 1 |
| stochastic-p4-d0.2@6080 | `minunang` |  | 1 |
| stochastic-p4-d0.2@8192 | `minunang` |  | 1 |
| stochastic-p4-d0.2@16384 | `minunang` |  | 1 |
| unigram-ablation@6080 | `minuna+ng` |  | 2 |

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

## `tinuki`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+uki`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tinuki` |  | 1 |
| plain@8192 | `tinuki` |  | 1 |
| plain@16384 | `tinuki` |  | 1 |
| morphbpe@6080 | `tin+uki` |  | 2 |
| morphbpe@8192 | `tin+uki` |  | 2 |
| morphbpe@16384 | `tin+uki` |  | 2 |
| penalty-1@6080 | `t+in+uki` | OK | 3 |
| penalty-1@8192 | `t+in+uki` | OK | 3 |
| penalty-1@16384 | `t+in+uki` | OK | 3 |
| penalty-2@6080 | `t+in+uki` | OK | 3 |
| penalty-2@8192 | `t+in+uki` | OK | 3 |
| penalty-2@16384 | `t+in+uki` | OK | 3 |
| penalty-4@6080 | `tinu+ki` |  | 2 |
| penalty-4@8192 | `tinu+ki` |  | 2 |
| penalty-4@16384 | `tinu+ki` |  | 2 |
| penalty-8@6080 | `t+in+uki` | OK | 3 |
| penalty-8@8192 | `t+in+uki` | OK | 3 |
| penalty-8@16384 | `t+in+uki` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.1@8192 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.1@16384 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@6080 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@8192 | `t+inu+ki` |  | 3 |
| stochastic-p4-d0.2@16384 | `t+inu+ki` |  | 3 |
| unigram-ablation@6080 | `tinuki` |  | 1 |

## `lumapit`  (infixation, tier A_strong_silver)

**silver gold:** `l+um+apit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lum+apit` |  | 2 |
| plain@8192 | `lumapit` |  | 1 |
| plain@16384 | `lumapit` |  | 1 |
| morphbpe@6080 | `lum+apit` |  | 2 |
| morphbpe@8192 | `lum+apit` |  | 2 |
| morphbpe@16384 | `lum+apit` |  | 2 |
| penalty-1@6080 | `lu+ma+pit` |  | 3 |
| penalty-1@8192 | `luma+pit` |  | 2 |
| penalty-1@16384 | `luma+pit` |  | 2 |
| penalty-2@6080 | `lu+ma+pit` |  | 3 |
| penalty-2@8192 | `luma+pit` |  | 2 |
| penalty-2@16384 | `luma+pit` |  | 2 |
| penalty-4@6080 | `lu+ma+pit` |  | 3 |
| penalty-4@8192 | `luma+pit` |  | 2 |
| penalty-4@16384 | `luma+pit` |  | 2 |
| penalty-8@6080 | `lu+ma+pit` |  | 3 |
| penalty-8@8192 | `lu+ma+pit` |  | 3 |
| penalty-8@16384 | `luma+pit` |  | 2 |
| stochastic-p4-d0.1@6080 | `lu+ma+pit` |  | 3 |
| stochastic-p4-d0.1@8192 | `lu+ma+pit` |  | 3 |
| stochastic-p4-d0.1@16384 | `luma+pit` |  | 2 |
| stochastic-p4-d0.2@6080 | `lu+ma+pit` |  | 3 |
| stochastic-p4-d0.2@8192 | `luma+pit` |  | 2 |
| stochastic-p4-d0.2@16384 | `luma+pit` |  | 2 |
| unigram-ablation@6080 | `luma+pit` |  | 2 |

## `minum`  (infixation, tier A_strong_silver)

**silver gold:** `m+in+um`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+um` |  | 2 |
| plain@8192 | `minum` |  | 1 |
| plain@16384 | `minum` |  | 1 |
| morphbpe@6080 | `minum` |  | 1 |
| morphbpe@8192 | `minum` |  | 1 |
| morphbpe@16384 | `minum` |  | 1 |
| penalty-1@6080 | `minum` |  | 1 |
| penalty-1@8192 | `minum` |  | 1 |
| penalty-1@16384 | `minum` |  | 1 |
| penalty-2@6080 | `minum` |  | 1 |
| penalty-2@8192 | `minum` |  | 1 |
| penalty-2@16384 | `minum` |  | 1 |
| penalty-4@6080 | `minum` |  | 1 |
| penalty-4@8192 | `minum` |  | 1 |
| penalty-4@16384 | `minum` |  | 1 |
| penalty-8@6080 | `minum` |  | 1 |
| penalty-8@8192 | `minum` |  | 1 |
| penalty-8@16384 | `minum` |  | 1 |
| stochastic-p4-d0.1@6080 | `minum` |  | 1 |
| stochastic-p4-d0.1@8192 | `minum` |  | 1 |
| stochastic-p4-d0.1@16384 | `minum` |  | 1 |
| stochastic-p4-d0.2@6080 | `min+um` |  | 2 |
| stochastic-p4-d0.2@8192 | `minum` |  | 1 |
| stochastic-p4-d0.2@16384 | `minum` |  | 1 |
| unigram-ablation@6080 | `minum` |  | 1 |

## `singsing`  (infixation, tier B_moderate_silver)

**silver gold:** `s+in+gsing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sing+sing` |  | 2 |
| plain@8192 | `sing+sing` |  | 2 |
| plain@16384 | `singsing` |  | 1 |
| morphbpe@6080 | `sing+sing` |  | 2 |
| morphbpe@8192 | `singsing` |  | 1 |
| morphbpe@16384 | `singsing` |  | 1 |
| penalty-1@6080 | `sing+sing` |  | 2 |
| penalty-1@8192 | `singsing` |  | 1 |
| penalty-1@16384 | `singsing` |  | 1 |
| penalty-2@6080 | `sing+sing` |  | 2 |
| penalty-2@8192 | `singsing` |  | 1 |
| penalty-2@16384 | `singsing` |  | 1 |
| penalty-4@6080 | `sing+sing` |  | 2 |
| penalty-4@8192 | `singsing` |  | 1 |
| penalty-4@16384 | `singsing` |  | 1 |
| penalty-8@6080 | `sing+sing` |  | 2 |
| penalty-8@8192 | `singsing` |  | 1 |
| penalty-8@16384 | `singsing` |  | 1 |
| stochastic-p4-d0.1@6080 | `si+ng+si+ng` |  | 4 |
| stochastic-p4-d0.1@8192 | `si+ng+si+ng` |  | 4 |
| stochastic-p4-d0.1@16384 | `singsing` |  | 1 |
| stochastic-p4-d0.2@6080 | `si+ng+si+ng` |  | 4 |
| stochastic-p4-d0.2@8192 | `si+ng+si+ng` |  | 4 |
| stochastic-p4-d0.2@16384 | `singsing` |  | 1 |
| unigram-ablation@6080 | `singsing` |  | 1 |

## `binutil`  (infixation, tier A_strong_silver)

**silver gold:** `b+in+util`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bin+ut+il` |  | 3 |
| plain@8192 | `bin+ut+il` |  | 3 |
| plain@16384 | `binutil` |  | 1 |
| morphbpe@6080 | `bin+ut+il` |  | 3 |
| morphbpe@8192 | `bin+ut+il` |  | 3 |
| morphbpe@16384 | `bin+util` |  | 2 |
| penalty-1@6080 | `b+in+ut+il` |  | 4 |
| penalty-1@8192 | `b+in+ut+il` |  | 4 |
| penalty-1@16384 | `b+in+util` | OK | 3 |
| penalty-2@6080 | `b+in+ut+il` |  | 4 |
| penalty-2@8192 | `b+in+ut+il` |  | 4 |
| penalty-2@16384 | `b+in+util` | OK | 3 |
| penalty-4@6080 | `b+in+ut+il` |  | 4 |
| penalty-4@8192 | `b+in+ut+il` |  | 4 |
| penalty-4@16384 | `b+in+util` | OK | 3 |
| penalty-8@6080 | `b+inu+til` |  | 3 |
| penalty-8@8192 | `b+inu+til` |  | 3 |
| penalty-8@16384 | `b+inu+til` |  | 3 |
| stochastic-p4-d0.1@6080 | `b+in+ut+il` |  | 4 |
| stochastic-p4-d0.1@8192 | `b+in+ut+il` |  | 4 |
| stochastic-p4-d0.1@16384 | `b+in+util` | OK | 3 |
| stochastic-p4-d0.2@6080 | `b+inu+til` |  | 3 |
| stochastic-p4-d0.2@8192 | `b+inu+til` |  | 3 |
| stochastic-p4-d0.2@16384 | `b+inu+til` |  | 3 |
| unigram-ablation@6080 | `binutil` |  | 1 |

## `kiniak`  (infixation, tier B_moderate_silver)

**silver gold:** `k+in+iak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `k+ini+ak` |  | 3 |
| plain@8192 | `k+ini+ak` |  | 3 |
| plain@16384 | `k+iniak` |  | 2 |
| morphbpe@6080 | `k+ini+ak` |  | 3 |
| morphbpe@8192 | `k+ini+ak` |  | 3 |
| morphbpe@16384 | `k+iniak` |  | 2 |
| penalty-1@6080 | `k+ini+ak` |  | 3 |
| penalty-1@8192 | `k+ini+ak` |  | 3 |
| penalty-1@16384 | `k+iniak` |  | 2 |
| penalty-2@6080 | `k+ini+ak` |  | 3 |
| penalty-2@8192 | `k+ini+ak` |  | 3 |
| penalty-2@16384 | `k+iniak` |  | 2 |
| penalty-4@6080 | `k+ini+ak` |  | 3 |
| penalty-4@8192 | `k+ini+ak` |  | 3 |
| penalty-4@16384 | `k+iniak` |  | 2 |
| penalty-8@6080 | `k+in+i+ak` |  | 4 |
| penalty-8@8192 | `k+in+i+ak` |  | 4 |
| penalty-8@16384 | `kini+ak` |  | 2 |
| stochastic-p4-d0.1@6080 | `k+in+i+ak` |  | 4 |
| stochastic-p4-d0.1@8192 | `k+in+i+ak` |  | 4 |
| stochastic-p4-d0.1@16384 | `k+in+i+ak` |  | 4 |
| stochastic-p4-d0.2@6080 | `k+ini+ak` |  | 3 |
| stochastic-p4-d0.2@8192 | `k+ini+ak` |  | 3 |
| stochastic-p4-d0.2@16384 | `k+iniak` |  | 2 |
| unigram-ablation@6080 | `ki+nia+k` |  | 3 |

## `minie`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+ie`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+ie` |  | 2 |
| plain@8192 | `minie` |  | 1 |
| plain@16384 | `minie` |  | 1 |
| morphbpe@6080 | `minie` |  | 1 |
| morphbpe@8192 | `minie` |  | 1 |
| morphbpe@16384 | `minie` |  | 1 |
| penalty-1@6080 | `minie` |  | 1 |
| penalty-1@8192 | `minie` |  | 1 |
| penalty-1@16384 | `minie` |  | 1 |
| penalty-2@6080 | `minie` |  | 1 |
| penalty-2@8192 | `minie` |  | 1 |
| penalty-2@16384 | `minie` |  | 1 |
| penalty-4@6080 | `minie` |  | 1 |
| penalty-4@8192 | `minie` |  | 1 |
| penalty-4@16384 | `minie` |  | 1 |
| penalty-8@6080 | `minie` |  | 1 |
| penalty-8@8192 | `minie` |  | 1 |
| penalty-8@16384 | `minie` |  | 1 |
| stochastic-p4-d0.1@6080 | `minie` |  | 1 |
| stochastic-p4-d0.1@8192 | `minie` |  | 1 |
| stochastic-p4-d0.1@16384 | `minie` |  | 1 |
| stochastic-p4-d0.2@6080 | `minie` |  | 1 |
| stochastic-p4-d0.2@8192 | `minie` |  | 1 |
| stochastic-p4-d0.2@16384 | `minie` |  | 1 |
| unigram-ablation@6080 | `mini+e` |  | 2 |

## `minta`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+ta`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `minta` |  | 1 |
| plain@8192 | `minta` |  | 1 |
| plain@16384 | `minta` |  | 1 |
| morphbpe@6080 | `minta` |  | 1 |
| morphbpe@8192 | `minta` |  | 1 |
| morphbpe@16384 | `minta` |  | 1 |
| penalty-1@6080 | `minta` |  | 1 |
| penalty-1@8192 | `minta` |  | 1 |
| penalty-1@16384 | `minta` |  | 1 |
| penalty-2@6080 | `minta` |  | 1 |
| penalty-2@8192 | `minta` |  | 1 |
| penalty-2@16384 | `minta` |  | 1 |
| penalty-4@6080 | `minta` |  | 1 |
| penalty-4@8192 | `minta` |  | 1 |
| penalty-4@16384 | `minta` |  | 1 |
| penalty-8@6080 | `minta` |  | 1 |
| penalty-8@8192 | `minta` |  | 1 |
| penalty-8@16384 | `minta` |  | 1 |
| stochastic-p4-d0.1@6080 | `minta` |  | 1 |
| stochastic-p4-d0.1@8192 | `minta` |  | 1 |
| stochastic-p4-d0.1@16384 | `minta` |  | 1 |
| stochastic-p4-d0.2@6080 | `minta` |  | 1 |
| stochastic-p4-d0.2@8192 | `minta` |  | 1 |
| stochastic-p4-d0.2@16384 | `minta` |  | 1 |
| unigram-ablation@6080 | `minta` |  | 1 |

## `tinikdo`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+ikdo`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tin+ikdo` |  | 2 |
| plain@8192 | `tin+ikdo` |  | 2 |
| plain@16384 | `tinikdo` |  | 1 |
| morphbpe@6080 | `tin+ikdo` |  | 2 |
| morphbpe@8192 | `tin+ikdo` |  | 2 |
| morphbpe@16384 | `tin+ikdo` |  | 2 |
| penalty-1@6080 | `t+in+ikdo` | OK | 3 |
| penalty-1@8192 | `t+in+ikdo` | OK | 3 |
| penalty-1@16384 | `t+in+ikdo` | OK | 3 |
| penalty-2@6080 | `t+in+ik+do` |  | 4 |
| penalty-2@8192 | `t+in+ikdo` | OK | 3 |
| penalty-2@16384 | `t+in+ikdo` | OK | 3 |
| penalty-4@6080 | `t+in+ik+do` |  | 4 |
| penalty-4@8192 | `t+in+ikdo` | OK | 3 |
| penalty-4@16384 | `t+in+ikdo` | OK | 3 |
| penalty-8@6080 | `t+in+ik+do` |  | 4 |
| penalty-8@8192 | `t+in+ikdo` | OK | 3 |
| penalty-8@16384 | `t+in+ikdo` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+ik+do` |  | 4 |
| stochastic-p4-d0.1@8192 | `t+in+ikdo` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+ikdo` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+ik+do` |  | 4 |
| stochastic-p4-d0.2@8192 | `t+in+ik+do` |  | 4 |
| stochastic-p4-d0.2@16384 | `t+in+ikdo` | OK | 3 |
| unigram-ablation@6080 | `tinikdo` |  | 1 |

## `kinagli`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `k+in+agli`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kin+ag+li` |  | 3 |
| plain@8192 | `kin+ag+li` |  | 3 |
| plain@16384 | `kin+agli` |  | 2 |
| morphbpe@6080 | `kin+ag+li` |  | 3 |
| morphbpe@8192 | `kin+ag+li` |  | 3 |
| morphbpe@16384 | `kin+agli` |  | 2 |
| penalty-1@6080 | `k+inag+li` |  | 3 |
| penalty-1@8192 | `k+inag+li` |  | 3 |
| penalty-1@16384 | `k+inag+li` |  | 3 |
| penalty-2@6080 | `k+inag+li` |  | 3 |
| penalty-2@8192 | `k+inag+li` |  | 3 |
| penalty-2@16384 | `k+inag+li` |  | 3 |
| penalty-4@6080 | `k+in+ag+li` |  | 4 |
| penalty-4@8192 | `k+in+ag+li` |  | 4 |
| penalty-4@16384 | `k+inag+li` |  | 3 |
| penalty-8@6080 | `k+in+ag+li` |  | 4 |
| penalty-8@8192 | `k+in+ag+li` |  | 4 |
| penalty-8@16384 | `k+inag+li` |  | 3 |
| stochastic-p4-d0.1@6080 | `k+in+ag+li` |  | 4 |
| stochastic-p4-d0.1@8192 | `k+in+ag+li` |  | 4 |
| stochastic-p4-d0.1@16384 | `k+inag+li` |  | 3 |
| stochastic-p4-d0.2@6080 | `k+in+ag+li` |  | 4 |
| stochastic-p4-d0.2@8192 | `k+in+ag+li` |  | 4 |
| stochastic-p4-d0.2@16384 | `k+inag+li` |  | 3 |
| unigram-ablation@6080 | `ki+na+g+li` |  | 4 |

## `ninuman`  (infixation, tier B_moderate_silver)

**silver gold:** `n+in+uman`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ninuman` |  | 1 |
| plain@8192 | `ninuman` |  | 1 |
| plain@16384 | `ninuman` |  | 1 |
| morphbpe@6080 | `ninuman` |  | 1 |
| morphbpe@8192 | `ninuman` |  | 1 |
| morphbpe@16384 | `ninuman` |  | 1 |
| penalty-1@6080 | `ninuman` |  | 1 |
| penalty-1@8192 | `ninuman` |  | 1 |
| penalty-1@16384 | `ninuman` |  | 1 |
| penalty-2@6080 | `ninuman` |  | 1 |
| penalty-2@8192 | `ninuman` |  | 1 |
| penalty-2@16384 | `ninuman` |  | 1 |
| penalty-4@6080 | `ninuman` |  | 1 |
| penalty-4@8192 | `ninuman` |  | 1 |
| penalty-4@16384 | `ninuman` |  | 1 |
| penalty-8@6080 | `ninuman` |  | 1 |
| penalty-8@8192 | `ninuman` |  | 1 |
| penalty-8@16384 | `ninuman` |  | 1 |
| stochastic-p4-d0.1@6080 | `ninuman` |  | 1 |
| stochastic-p4-d0.1@8192 | `ninuman` |  | 1 |
| stochastic-p4-d0.1@16384 | `ninuman` |  | 1 |
| stochastic-p4-d0.2@6080 | `ninuman` |  | 1 |
| stochastic-p4-d0.2@8192 | `ninuman` |  | 1 |
| stochastic-p4-d0.2@16384 | `ninuman` |  | 1 |
| unigram-ablation@6080 | `ninuman` |  | 1 |

## `sinumpa`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+umpa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+umpa` |  | 2 |
| plain@8192 | `sin+umpa` |  | 2 |
| plain@16384 | `sinumpa` |  | 1 |
| morphbpe@6080 | `sin+umpa` |  | 2 |
| morphbpe@8192 | `sin+umpa` |  | 2 |
| morphbpe@16384 | `sin+umpa` |  | 2 |
| penalty-1@6080 | `s+in+umpa` | OK | 3 |
| penalty-1@8192 | `s+in+umpa` | OK | 3 |
| penalty-1@16384 | `s+in+umpa` | OK | 3 |
| penalty-2@6080 | `s+in+umpa` | OK | 3 |
| penalty-2@8192 | `s+in+umpa` | OK | 3 |
| penalty-2@16384 | `s+in+umpa` | OK | 3 |
| penalty-4@6080 | `s+in+umpa` | OK | 3 |
| penalty-4@8192 | `s+in+umpa` | OK | 3 |
| penalty-4@16384 | `s+in+umpa` | OK | 3 |
| penalty-8@6080 | `s+in+umpa` | OK | 3 |
| penalty-8@8192 | `s+in+umpa` | OK | 3 |
| penalty-8@16384 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.1@6080 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.1@8192 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.1@16384 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.2@6080 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.2@8192 | `s+in+umpa` | OK | 3 |
| stochastic-p4-d0.2@16384 | `s+in+umpa` | OK | 3 |
| unigram-ablation@6080 | `s+inum+pa` |  | 3 |

## `linian`  (infixation, tier B_moderate_silver)

**silver gold:** `l+in+ian`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+ian` |  | 2 |
| plain@8192 | `lin+ian` |  | 2 |
| plain@16384 | `lin+ian` |  | 2 |
| morphbpe@6080 | `lin+ian` |  | 2 |
| morphbpe@8192 | `lin+ian` |  | 2 |
| morphbpe@16384 | `lin+ian` |  | 2 |
| penalty-1@6080 | `l+in+ian` | OK | 3 |
| penalty-1@8192 | `l+inian` |  | 2 |
| penalty-1@16384 | `l+inian` |  | 2 |
| penalty-2@6080 | `l+in+ian` | OK | 3 |
| penalty-2@8192 | `l+inian` |  | 2 |
| penalty-2@16384 | `l+inian` |  | 2 |
| penalty-4@6080 | `l+in+ian` | OK | 3 |
| penalty-4@8192 | `l+inian` |  | 2 |
| penalty-4@16384 | `l+inian` |  | 2 |
| penalty-8@6080 | `l+in+ian` | OK | 3 |
| penalty-8@8192 | `l+inian` |  | 2 |
| penalty-8@16384 | `l+inian` |  | 2 |
| stochastic-p4-d0.1@6080 | `l+in+ian` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+ian` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+inian` |  | 2 |
| stochastic-p4-d0.2@6080 | `l+in+ian` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+ian` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+inian` |  | 2 |
| unigram-ablation@6080 | `lin+ian` |  | 2 |

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

## `tinuknang`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+uknang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tin+uknang` |  | 2 |
| plain@8192 | `tin+uknang` |  | 2 |
| plain@16384 | `tinuknang` |  | 1 |
| morphbpe@6080 | `tin+uknang` |  | 2 |
| morphbpe@8192 | `tin+uknang` |  | 2 |
| morphbpe@16384 | `tin+uknang` |  | 2 |
| penalty-1@6080 | `t+in+uknang` | OK | 3 |
| penalty-1@8192 | `t+in+uknang` | OK | 3 |
| penalty-1@16384 | `t+in+uknang` | OK | 3 |
| penalty-2@6080 | `t+in+uknang` | OK | 3 |
| penalty-2@8192 | `t+in+uknang` | OK | 3 |
| penalty-2@16384 | `t+in+uknang` | OK | 3 |
| penalty-4@6080 | `t+in+uknang` | OK | 3 |
| penalty-4@8192 | `t+in+uknang` | OK | 3 |
| penalty-4@16384 | `t+in+uknang` | OK | 3 |
| penalty-8@6080 | `t+in+uknang` | OK | 3 |
| penalty-8@8192 | `t+in+uknang` | OK | 3 |
| penalty-8@16384 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.2@8192 | `t+in+uknang` | OK | 3 |
| stochastic-p4-d0.2@16384 | `t+in+uknang` | OK | 3 |
| unigram-ablation@6080 | `tinu+k+nang` |  | 3 |

## `sinag`  (infixation, tier B_moderate_silver)

**silver gold:** `s+in+ag`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sinag` |  | 1 |
| plain@8192 | `sinag` |  | 1 |
| plain@16384 | `sinag` |  | 1 |
| morphbpe@6080 | `sinag` |  | 1 |
| morphbpe@8192 | `sinag` |  | 1 |
| morphbpe@16384 | `sinag` |  | 1 |
| penalty-1@6080 | `sinag` |  | 1 |
| penalty-1@8192 | `sinag` |  | 1 |
| penalty-1@16384 | `sinag` |  | 1 |
| penalty-2@6080 | `sinag` |  | 1 |
| penalty-2@8192 | `sinag` |  | 1 |
| penalty-2@16384 | `sinag` |  | 1 |
| penalty-4@6080 | `s+in+ag` | OK | 3 |
| penalty-4@8192 | `s+in+ag` | OK | 3 |
| penalty-4@16384 | `sinag` |  | 1 |
| penalty-8@6080 | `s+in+ag` | OK | 3 |
| penalty-8@8192 | `s+in+ag` | OK | 3 |
| penalty-8@16384 | `sinag` |  | 1 |
| stochastic-p4-d0.1@6080 | `s+in+ag` | OK | 3 |
| stochastic-p4-d0.1@8192 | `s+in+ag` | OK | 3 |
| stochastic-p4-d0.1@16384 | `sinag` |  | 1 |
| stochastic-p4-d0.2@6080 | `s+in+ag` | OK | 3 |
| stochastic-p4-d0.2@8192 | `s+in+ag` | OK | 3 |
| stochastic-p4-d0.2@16384 | `sinag` |  | 1 |
| unigram-ablation@6080 | `sinag` |  | 1 |

## `tumakas`  (infixation, tier A_strong_silver)

**silver gold:** `t+um+akas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tu+makas` |  | 2 |
| plain@8192 | `tu+makas` |  | 2 |
| plain@16384 | `tu+makas` |  | 2 |
| morphbpe@6080 | `tu+makas` |  | 2 |
| morphbpe@8192 | `tu+makas` |  | 2 |
| morphbpe@16384 | `tu+makas` |  | 2 |
| penalty-1@6080 | `tu+maka+s` |  | 3 |
| penalty-1@8192 | `tu+maka+s` |  | 3 |
| penalty-1@16384 | `tu+makas` |  | 2 |
| penalty-2@6080 | `tu+maka+s` |  | 3 |
| penalty-2@8192 | `tu+maka+s` |  | 3 |
| penalty-2@16384 | `tu+makas` |  | 2 |
| penalty-4@6080 | `tu+maka+s` |  | 3 |
| penalty-4@8192 | `tu+maka+s` |  | 3 |
| penalty-4@16384 | `tu+makas` |  | 2 |
| penalty-8@6080 | `tu+maka+s` |  | 3 |
| penalty-8@8192 | `tu+maka+s` |  | 3 |
| penalty-8@16384 | `tu+makas` |  | 2 |
| stochastic-p4-d0.1@6080 | `tu+maka+s` |  | 3 |
| stochastic-p4-d0.1@8192 | `tu+maka+s` |  | 3 |
| stochastic-p4-d0.1@16384 | `tu+maka+s` |  | 3 |
| stochastic-p4-d0.2@6080 | `tu+maka+s` |  | 3 |
| stochastic-p4-d0.2@8192 | `tu+maka+s` |  | 3 |
| stochastic-p4-d0.2@16384 | `tu+maka+s` |  | 3 |
| unigram-ablation@6080 | `tu+maka+s` |  | 3 |

## `dinuku`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `d+in+uku`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `d+inu+ku` |  | 3 |
| plain@8192 | `d+inu+ku` |  | 3 |
| plain@16384 | `dinu+ku` |  | 2 |
| morphbpe@6080 | `d+inu+ku` |  | 3 |
| morphbpe@8192 | `d+inu+ku` |  | 3 |
| morphbpe@16384 | `dinu+ku` |  | 2 |
| penalty-1@6080 | `d+inu+ku` |  | 3 |
| penalty-1@8192 | `d+inu+ku` |  | 3 |
| penalty-1@16384 | `dinu+ku` |  | 2 |
| penalty-2@6080 | `d+inu+ku` |  | 3 |
| penalty-2@8192 | `d+inu+ku` |  | 3 |
| penalty-2@16384 | `dinu+ku` |  | 2 |
| penalty-4@6080 | `d+inu+ku` |  | 3 |
| penalty-4@8192 | `d+inu+ku` |  | 3 |
| penalty-4@16384 | `dinu+ku` |  | 2 |
| penalty-8@6080 | `d+inu+ku` |  | 3 |
| penalty-8@8192 | `d+inu+ku` |  | 3 |
| penalty-8@16384 | `dinu+ku` |  | 2 |
| stochastic-p4-d0.1@6080 | `d+inu+ku` |  | 3 |
| stochastic-p4-d0.1@8192 | `d+inu+ku` |  | 3 |
| stochastic-p4-d0.1@16384 | `dinu+ku` |  | 2 |
| stochastic-p4-d0.2@6080 | `d+inu+ku` |  | 3 |
| stochastic-p4-d0.2@8192 | `d+inu+ku` |  | 3 |
| stochastic-p4-d0.2@16384 | `dinu+ku` |  | 2 |
| unigram-ablation@6080 | `di+nu+ku` |  | 3 |

## `minuli`  (infixation, tier A_strong_silver)

**silver gold:** `m+in+uli`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+uli` |  | 2 |
| plain@8192 | `minuli` |  | 1 |
| plain@16384 | `minuli` |  | 1 |
| morphbpe@6080 | `min+uli` |  | 2 |
| morphbpe@8192 | `min+uli` |  | 2 |
| morphbpe@16384 | `min+uli` |  | 2 |
| penalty-1@6080 | `min+uli` |  | 2 |
| penalty-1@8192 | `min+uli` |  | 2 |
| penalty-1@16384 | `min+uli` |  | 2 |
| penalty-2@6080 | `min+uli` |  | 2 |
| penalty-2@8192 | `min+uli` |  | 2 |
| penalty-2@16384 | `min+uli` |  | 2 |
| penalty-4@6080 | `min+uli` |  | 2 |
| penalty-4@8192 | `min+uli` |  | 2 |
| penalty-4@16384 | `min+uli` |  | 2 |
| penalty-8@6080 | `min+uli` |  | 2 |
| penalty-8@8192 | `min+uli` |  | 2 |
| penalty-8@16384 | `min+uli` |  | 2 |
| stochastic-p4-d0.1@6080 | `min+uli` |  | 2 |
| stochastic-p4-d0.1@8192 | `min+uli` |  | 2 |
| stochastic-p4-d0.1@16384 | `min+uli` |  | 2 |
| stochastic-p4-d0.2@6080 | `min+uli` |  | 2 |
| stochastic-p4-d0.2@8192 | `min+uli` |  | 2 |
| stochastic-p4-d0.2@16384 | `min+uli` |  | 2 |
| unigram-ablation@6080 | `minuli` |  | 1 |

## `tinabi`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `t+in+abi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tin+abi` |  | 2 |
| plain@8192 | `tin+abi` |  | 2 |
| plain@16384 | `tinabi` |  | 1 |
| morphbpe@6080 | `tin+abi` |  | 2 |
| morphbpe@8192 | `tin+abi` |  | 2 |
| morphbpe@16384 | `tinabi` |  | 1 |
| penalty-1@6080 | `t+in+abi` | OK | 3 |
| penalty-1@8192 | `t+in+abi` | OK | 3 |
| penalty-1@16384 | `t+in+abi` | OK | 3 |
| penalty-2@6080 | `t+in+abi` | OK | 3 |
| penalty-2@8192 | `t+in+abi` | OK | 3 |
| penalty-2@16384 | `t+in+abi` | OK | 3 |
| penalty-4@6080 | `t+in+abi` | OK | 3 |
| penalty-4@8192 | `t+in+abi` | OK | 3 |
| penalty-4@16384 | `t+in+abi` | OK | 3 |
| penalty-8@6080 | `t+in+abi` | OK | 3 |
| penalty-8@8192 | `t+in+abi` | OK | 3 |
| penalty-8@16384 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.2@8192 | `t+in+abi` | OK | 3 |
| stochastic-p4-d0.2@16384 | `t+in+abi` | OK | 3 |
| unigram-ablation@6080 | `ti+na+bi` |  | 3 |

## `dinukit`  (infixation, tier A_strong_silver)

**silver gold:** `d+in+ukit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `din+uk+it` |  | 3 |
| plain@8192 | `din+ukit` |  | 2 |
| plain@16384 | `dinukit` |  | 1 |
| morphbpe@6080 | `din+uk+it` |  | 3 |
| morphbpe@8192 | `din+ukit` |  | 2 |
| morphbpe@16384 | `din+ukit` |  | 2 |
| penalty-1@6080 | `d+in+uk+it` |  | 4 |
| penalty-1@8192 | `d+in+ukit` | OK | 3 |
| penalty-1@16384 | `d+in+ukit` | OK | 3 |
| penalty-2@6080 | `d+in+uk+it` |  | 4 |
| penalty-2@8192 | `d+in+ukit` | OK | 3 |
| penalty-2@16384 | `d+in+ukit` | OK | 3 |
| penalty-4@6080 | `d+inu+kit` |  | 3 |
| penalty-4@8192 | `d+inu+kit` |  | 3 |
| penalty-4@16384 | `dinu+kit` |  | 2 |
| penalty-8@6080 | `d+inu+kit` |  | 3 |
| penalty-8@8192 | `d+inu+kit` |  | 3 |
| penalty-8@16384 | `dinu+kit` |  | 2 |
| stochastic-p4-d0.1@6080 | `d+in+uk+it` |  | 4 |
| stochastic-p4-d0.1@8192 | `d+in+uk+it` |  | 4 |
| stochastic-p4-d0.1@16384 | `d+in+ukit` | OK | 3 |
| stochastic-p4-d0.2@6080 | `d+in+uk+it` |  | 4 |
| stochastic-p4-d0.2@8192 | `d+in+uk+it` |  | 4 |
| stochastic-p4-d0.2@16384 | `d+in+ukit` | OK | 3 |
| unigram-ablation@6080 | `di+nu+kit` |  | 3 |

## `linabas`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+abas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+abas` |  | 2 |
| plain@8192 | `lin+abas` |  | 2 |
| plain@16384 | `linabas` |  | 1 |
| morphbpe@6080 | `lin+abas` |  | 2 |
| morphbpe@8192 | `lin+abas` |  | 2 |
| morphbpe@16384 | `lin+abas` |  | 2 |
| penalty-1@6080 | `l+in+abas` | OK | 3 |
| penalty-1@8192 | `l+in+abas` | OK | 3 |
| penalty-1@16384 | `l+in+abas` | OK | 3 |
| penalty-2@6080 | `l+in+abas` | OK | 3 |
| penalty-2@8192 | `l+in+abas` | OK | 3 |
| penalty-2@16384 | `l+in+abas` | OK | 3 |
| penalty-4@6080 | `l+in+a+bas` |  | 4 |
| penalty-4@8192 | `l+in+abas` | OK | 3 |
| penalty-4@16384 | `l+in+abas` | OK | 3 |
| penalty-8@6080 | `l+in+a+bas` |  | 4 |
| penalty-8@8192 | `l+in+abas` | OK | 3 |
| penalty-8@16384 | `l+in+abas` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+a+bas` |  | 4 |
| stochastic-p4-d0.1@8192 | `l+in+abas` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+abas` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+a+bas` |  | 4 |
| stochastic-p4-d0.2@8192 | `l+in+abas` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+abas` | OK | 3 |
| unigram-ablation@6080 | `linaba+s` |  | 2 |

## `linakad`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+akad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+a+kad` |  | 3 |
| plain@8192 | `lina+kad` |  | 2 |
| plain@16384 | `linakad` |  | 1 |
| morphbpe@6080 | `lina+kad` |  | 2 |
| morphbpe@8192 | `lina+kad` |  | 2 |
| morphbpe@16384 | `lina+kad` |  | 2 |
| penalty-1@6080 | `lina+kad` |  | 2 |
| penalty-1@8192 | `lina+kad` |  | 2 |
| penalty-1@16384 | `lina+kad` |  | 2 |
| penalty-2@6080 | `lina+kad` |  | 2 |
| penalty-2@8192 | `lina+kad` |  | 2 |
| penalty-2@16384 | `lina+kad` |  | 2 |
| penalty-4@6080 | `l+in+akad` | OK | 3 |
| penalty-4@8192 | `l+in+akad` | OK | 3 |
| penalty-4@16384 | `l+in+akad` | OK | 3 |
| penalty-8@6080 | `l+in+akad` | OK | 3 |
| penalty-8@8192 | `l+in+akad` | OK | 3 |
| penalty-8@16384 | `l+in+akad` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+aka+d` |  | 4 |
| stochastic-p4-d0.1@8192 | `l+in+akad` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+akad` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+akad` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+akad` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+akad` | OK | 3 |
| unigram-ablation@6080 | `li+na+kad` |  | 3 |

## `linukluk`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+ukluk`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+ukluk` |  | 2 |
| plain@8192 | `linukluk` |  | 1 |
| plain@16384 | `linukluk` |  | 1 |
| morphbpe@6080 | `lin+ukluk` |  | 2 |
| morphbpe@8192 | `lin+ukluk` |  | 2 |
| morphbpe@16384 | `lin+ukluk` |  | 2 |
| penalty-1@6080 | `l+in+ukluk` | OK | 3 |
| penalty-1@8192 | `l+in+ukluk` | OK | 3 |
| penalty-1@16384 | `l+in+ukluk` | OK | 3 |
| penalty-2@6080 | `l+in+ukluk` | OK | 3 |
| penalty-2@8192 | `l+in+ukluk` | OK | 3 |
| penalty-2@16384 | `l+in+ukluk` | OK | 3 |
| penalty-4@6080 | `l+in+ukluk` | OK | 3 |
| penalty-4@8192 | `l+in+ukluk` | OK | 3 |
| penalty-4@16384 | `l+in+ukluk` | OK | 3 |
| penalty-8@6080 | `l+in+ukluk` | OK | 3 |
| penalty-8@8192 | `l+in+ukluk` | OK | 3 |
| penalty-8@16384 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+ukluk` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+ukluk` | OK | 3 |
| unigram-ablation@6080 | `lin+ukluk` |  | 2 |

## `minic`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+ic`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+ic` |  | 2 |
| plain@8192 | `min+ic` |  | 2 |
| plain@16384 | `min+ic` |  | 2 |
| morphbpe@6080 | `min+ic` |  | 2 |
| morphbpe@8192 | `min+ic` |  | 2 |
| morphbpe@16384 | `min+ic` |  | 2 |
| penalty-1@6080 | `min+ic` |  | 2 |
| penalty-1@8192 | `min+ic` |  | 2 |
| penalty-1@16384 | `min+ic` |  | 2 |
| penalty-2@6080 | `min+ic` |  | 2 |
| penalty-2@8192 | `min+ic` |  | 2 |
| penalty-2@16384 | `min+ic` |  | 2 |
| penalty-4@6080 | `min+ic` |  | 2 |
| penalty-4@8192 | `min+ic` |  | 2 |
| penalty-4@16384 | `min+ic` |  | 2 |
| penalty-8@6080 | `min+ic` |  | 2 |
| penalty-8@8192 | `min+ic` |  | 2 |
| penalty-8@16384 | `min+ic` |  | 2 |
| stochastic-p4-d0.1@6080 | `min+ic` |  | 2 |
| stochastic-p4-d0.1@8192 | `min+ic` |  | 2 |
| stochastic-p4-d0.1@16384 | `min+ic` |  | 2 |
| stochastic-p4-d0.2@6080 | `min+ic` |  | 2 |
| stochastic-p4-d0.2@8192 | `min+ic` |  | 2 |
| stochastic-p4-d0.2@16384 | `min+ic` |  | 2 |
| unigram-ablation@6080 | `mini+c` |  | 2 |

## `minukiat`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+ukiat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+uki+at` |  | 3 |
| plain@8192 | `min+ukiat` |  | 2 |
| plain@16384 | `minukiat` |  | 1 |
| morphbpe@6080 | `min+uki+at` |  | 3 |
| morphbpe@8192 | `min+ukiat` |  | 2 |
| morphbpe@16384 | `minukiat` |  | 1 |
| penalty-1@6080 | `min+uki+at` |  | 3 |
| penalty-1@8192 | `min+ukiat` |  | 2 |
| penalty-1@16384 | `minukiat` |  | 1 |
| penalty-2@6080 | `min+uki+at` |  | 3 |
| penalty-2@8192 | `min+ukiat` |  | 2 |
| penalty-2@16384 | `minukiat` |  | 1 |
| penalty-4@6080 | `minu+kiat` |  | 2 |
| penalty-4@8192 | `minu+kiat` |  | 2 |
| penalty-4@16384 | `minukiat` |  | 1 |
| penalty-8@6080 | `min+uki+at` |  | 3 |
| penalty-8@8192 | `min+ukiat` |  | 2 |
| penalty-8@16384 | `minukiat` |  | 1 |
| stochastic-p4-d0.1@6080 | `min+uki+at` |  | 3 |
| stochastic-p4-d0.1@8192 | `min+uki+at` |  | 3 |
| stochastic-p4-d0.1@16384 | `minukiat` |  | 1 |
| stochastic-p4-d0.2@6080 | `minu+kiat` |  | 2 |
| stochastic-p4-d0.2@8192 | `minu+kiat` |  | 2 |
| stochastic-p4-d0.2@16384 | `minukiat` |  | 1 |
| unigram-ablation@6080 | `min+ukiat` |  | 2 |

## `tinipa`  (infixation, tier A_strong_silver)

**silver gold:** `t+in+ipa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tin+ipa` |  | 2 |
| plain@8192 | `tinipa` |  | 1 |
| plain@16384 | `tinipa` |  | 1 |
| morphbpe@6080 | `t+ini+pa` |  | 3 |
| morphbpe@8192 | `t+ini+pa` |  | 3 |
| morphbpe@16384 | `tini+pa` |  | 2 |
| penalty-1@6080 | `t+ini+pa` |  | 3 |
| penalty-1@8192 | `t+ini+pa` |  | 3 |
| penalty-1@16384 | `tini+pa` |  | 2 |
| penalty-2@6080 | `t+ini+pa` |  | 3 |
| penalty-2@8192 | `t+ini+pa` |  | 3 |
| penalty-2@16384 | `tini+pa` |  | 2 |
| penalty-4@6080 | `t+ini+pa` |  | 3 |
| penalty-4@8192 | `t+ini+pa` |  | 3 |
| penalty-4@16384 | `tini+pa` |  | 2 |
| penalty-8@6080 | `t+in+ipa` | OK | 3 |
| penalty-8@8192 | `t+in+ipa` | OK | 3 |
| penalty-8@16384 | `t+in+ipa` | OK | 3 |
| stochastic-p4-d0.1@6080 | `t+in+ipa` | OK | 3 |
| stochastic-p4-d0.1@8192 | `t+in+ipa` | OK | 3 |
| stochastic-p4-d0.1@16384 | `t+in+ipa` | OK | 3 |
| stochastic-p4-d0.2@6080 | `t+ini+pa` |  | 3 |
| stochastic-p4-d0.2@8192 | `t+ini+pa` |  | 3 |
| stochastic-p4-d0.2@16384 | `t+ini+pa` |  | 3 |
| unigram-ablation@6080 | `tini+pa` |  | 2 |

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

## `mingat`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+gat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ming+at` |  | 2 |
| plain@8192 | `ming+at` |  | 2 |
| plain@16384 | `mingat` |  | 1 |
| morphbpe@6080 | `ming+at` |  | 2 |
| morphbpe@8192 | `mingat` |  | 1 |
| morphbpe@16384 | `mingat` |  | 1 |
| penalty-1@6080 | `m+ingat` |  | 2 |
| penalty-1@8192 | `mingat` |  | 1 |
| penalty-1@16384 | `mingat` |  | 1 |
| penalty-2@6080 | `m+ingat` |  | 2 |
| penalty-2@8192 | `mingat` |  | 1 |
| penalty-2@16384 | `mingat` |  | 1 |
| penalty-4@6080 | `m+ingat` |  | 2 |
| penalty-4@8192 | `mingat` |  | 1 |
| penalty-4@16384 | `mingat` |  | 1 |
| penalty-8@6080 | `m+ingat` |  | 2 |
| penalty-8@8192 | `mingat` |  | 1 |
| penalty-8@16384 | `mingat` |  | 1 |
| stochastic-p4-d0.1@6080 | `mi+ng+at` |  | 3 |
| stochastic-p4-d0.1@8192 | `mingat` |  | 1 |
| stochastic-p4-d0.1@16384 | `mingat` |  | 1 |
| stochastic-p4-d0.2@6080 | `mi+ng+at` |  | 3 |
| stochastic-p4-d0.2@8192 | `ming+at` |  | 2 |
| stochastic-p4-d0.2@16384 | `mingat` |  | 1 |
| unigram-ablation@6080 | `ming+at` |  | 2 |

## `siniping`  (infixation, tier A_strong_silver)

**silver gold:** `s+in+iping`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+iping` |  | 2 |
| plain@8192 | `sin+iping` |  | 2 |
| plain@16384 | `sin+iping` |  | 2 |
| morphbpe@6080 | `sin+ip+ing` |  | 3 |
| morphbpe@8192 | `sin+ip+ing` |  | 3 |
| morphbpe@16384 | `sin+iping` |  | 2 |
| penalty-1@6080 | `s+in+ip+ing` |  | 4 |
| penalty-1@8192 | `s+inip+ing` |  | 3 |
| penalty-1@16384 | `s+inip+ing` |  | 3 |
| penalty-2@6080 | `s+in+ip+ing` |  | 4 |
| penalty-2@8192 | `s+in+ip+ing` |  | 4 |
| penalty-2@16384 | `s+in+iping` | OK | 3 |
| penalty-4@6080 | `s+in+ip+ing` |  | 4 |
| penalty-4@8192 | `s+in+ip+ing` |  | 4 |
| penalty-4@16384 | `s+in+iping` | OK | 3 |
| penalty-8@6080 | `s+in+i+ping` |  | 4 |
| penalty-8@8192 | `s+in+i+ping` |  | 4 |
| penalty-8@16384 | `sini+ping` |  | 2 |
| stochastic-p4-d0.1@6080 | `s+in+i+pi+ng` |  | 5 |
| stochastic-p4-d0.1@8192 | `s+in+i+pi+ng` |  | 5 |
| stochastic-p4-d0.1@16384 | `s+in+ipi+ng` |  | 4 |
| stochastic-p4-d0.2@6080 | `s+ini+pi+ng` |  | 4 |
| stochastic-p4-d0.2@8192 | `sini+pi+ng` |  | 3 |
| stochastic-p4-d0.2@16384 | `sini+pi+ng` |  | 3 |
| unigram-ablation@6080 | `s+ini+ping` |  | 3 |

## `linipul`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `l+in+ipul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+ip+ul` |  | 3 |
| plain@8192 | `lin+ip+ul` |  | 3 |
| plain@16384 | `lin+ipul` |  | 2 |
| morphbpe@6080 | `lin+ip+ul` |  | 3 |
| morphbpe@8192 | `lin+ip+ul` |  | 3 |
| morphbpe@16384 | `lin+ipul` |  | 2 |
| penalty-1@6080 | `l+in+ip+ul` |  | 4 |
| penalty-1@8192 | `l+inip+ul` |  | 3 |
| penalty-1@16384 | `linip+ul` |  | 2 |
| penalty-2@6080 | `l+in+ip+ul` |  | 4 |
| penalty-2@8192 | `l+in+ip+ul` |  | 4 |
| penalty-2@16384 | `l+inip+ul` |  | 3 |
| penalty-4@6080 | `l+in+ip+ul` |  | 4 |
| penalty-4@8192 | `l+in+ip+ul` |  | 4 |
| penalty-4@16384 | `l+inip+ul` |  | 3 |
| penalty-8@6080 | `l+in+i+pul` |  | 4 |
| penalty-8@8192 | `l+in+i+pul` |  | 4 |
| penalty-8@16384 | `lini+pul` |  | 2 |
| stochastic-p4-d0.1@6080 | `l+in+ip+ul` |  | 4 |
| stochastic-p4-d0.1@8192 | `l+in+ip+ul` |  | 4 |
| stochastic-p4-d0.1@16384 | `l+in+ip+ul` |  | 4 |
| stochastic-p4-d0.2@6080 | `l+in+ip+ul` |  | 4 |
| stochastic-p4-d0.2@8192 | `l+in+ip+ul` |  | 4 |
| stochastic-p4-d0.2@16384 | `l+in+ip+ul` |  | 4 |
| unigram-ablation@6080 | `lin+i+pul` |  | 3 |

## `sinira`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `s+in+ira`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sin+ira` |  | 2 |
| plain@8192 | `sin+ira` |  | 2 |
| plain@16384 | `sinira` |  | 1 |
| morphbpe@6080 | `sin+ira` |  | 2 |
| morphbpe@8192 | `sin+ira` |  | 2 |
| morphbpe@16384 | `sinira` |  | 1 |
| penalty-1@6080 | `s+ini+ra` |  | 3 |
| penalty-1@8192 | `sini+ra` |  | 2 |
| penalty-1@16384 | `sinira` |  | 1 |
| penalty-2@6080 | `sini+ra` |  | 2 |
| penalty-2@8192 | `sini+ra` |  | 2 |
| penalty-2@16384 | `sinira` |  | 1 |
| penalty-4@6080 | `s+ini+ra` |  | 3 |
| penalty-4@8192 | `sini+ra` |  | 2 |
| penalty-4@16384 | `sinira` |  | 1 |
| penalty-8@6080 | `s+in+ira` | OK | 3 |
| penalty-8@8192 | `s+in+ira` | OK | 3 |
| penalty-8@16384 | `sinira` |  | 1 |
| stochastic-p4-d0.1@6080 | `s+in+ira` | OK | 3 |
| stochastic-p4-d0.1@8192 | `s+in+ira` | OK | 3 |
| stochastic-p4-d0.1@16384 | `sinira` |  | 1 |
| stochastic-p4-d0.2@6080 | `s+ini+ra` |  | 3 |
| stochastic-p4-d0.2@8192 | `sini+ra` |  | 2 |
| stochastic-p4-d0.2@16384 | `sinira` |  | 1 |
| unigram-ablation@6080 | `s+ini+ra` |  | 3 |

## `sumiping`  (infixation, tier A_strong_silver)

**silver gold:** `s+um+iping`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sum+iping` |  | 2 |
| plain@8192 | `sum+iping` |  | 2 |
| plain@16384 | `sum+iping` |  | 2 |
| morphbpe@6080 | `su+mi+ping` |  | 3 |
| morphbpe@8192 | `su+mi+ping` |  | 3 |
| morphbpe@16384 | `su+mi+ping` |  | 3 |
| penalty-1@6080 | `su+mi+ping` |  | 3 |
| penalty-1@8192 | `su+mi+ping` |  | 3 |
| penalty-1@16384 | `su+mi+ping` |  | 3 |
| penalty-2@6080 | `su+mi+ping` |  | 3 |
| penalty-2@8192 | `su+mi+ping` |  | 3 |
| penalty-2@16384 | `su+mi+ping` |  | 3 |
| penalty-4@6080 | `su+mi+ping` |  | 3 |
| penalty-4@8192 | `su+mi+ping` |  | 3 |
| penalty-4@16384 | `su+mi+ping` |  | 3 |
| penalty-8@6080 | `su+mi+ping` |  | 3 |
| penalty-8@8192 | `su+mi+ping` |  | 3 |
| penalty-8@16384 | `su+mi+ping` |  | 3 |
| stochastic-p4-d0.1@6080 | `su+mi+pi+ng` |  | 4 |
| stochastic-p4-d0.1@8192 | `su+mi+pi+ng` |  | 4 |
| stochastic-p4-d0.1@16384 | `su+mi+pi+ng` |  | 4 |
| stochastic-p4-d0.2@6080 | `su+mi+pi+ng` |  | 4 |
| stochastic-p4-d0.2@8192 | `su+mi+pi+ng` |  | 4 |
| stochastic-p4-d0.2@16384 | `su+mi+pi+ng` |  | 4 |
| unigram-ablation@6080 | `su+mi+ping` |  | 3 |

## `dumpa`  (infixation, tier B_moderate_silver)

**silver gold:** `d+um+pa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dum+pa` |  | 2 |
| plain@8192 | `dum+pa` |  | 2 |
| plain@16384 | `dum+pa` |  | 2 |
| morphbpe@6080 | `dum+pa` |  | 2 |
| morphbpe@8192 | `dum+pa` |  | 2 |
| morphbpe@16384 | `dum+pa` |  | 2 |
| penalty-1@6080 | `d+umpa` |  | 2 |
| penalty-1@8192 | `d+umpa` |  | 2 |
| penalty-1@16384 | `d+umpa` |  | 2 |
| penalty-2@6080 | `d+umpa` |  | 2 |
| penalty-2@8192 | `d+umpa` |  | 2 |
| penalty-2@16384 | `d+umpa` |  | 2 |
| penalty-4@6080 | `d+umpa` |  | 2 |
| penalty-4@8192 | `d+umpa` |  | 2 |
| penalty-4@16384 | `d+umpa` |  | 2 |
| penalty-8@6080 | `dum+pa` |  | 2 |
| penalty-8@8192 | `dum+pa` |  | 2 |
| penalty-8@16384 | `dum+pa` |  | 2 |
| stochastic-p4-d0.1@6080 | `dum+pa` |  | 2 |
| stochastic-p4-d0.1@8192 | `dum+pa` |  | 2 |
| stochastic-p4-d0.1@16384 | `dum+pa` |  | 2 |
| stochastic-p4-d0.2@6080 | `dum+pa` |  | 2 |
| stochastic-p4-d0.2@8192 | `dum+pa` |  | 2 |
| stochastic-p4-d0.2@16384 | `dum+pa` |  | 2 |
| unigram-ablation@6080 | `du+m+pa` |  | 3 |

## `kumabsi`  (infixation, tier B_moderate_silver)

**silver gold:** `k+um+absi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ku+mab+si` |  | 3 |
| plain@8192 | `ku+mab+si` |  | 3 |
| plain@16384 | `kumab+si` |  | 2 |
| morphbpe@6080 | `ku+mab+si` |  | 3 |
| morphbpe@8192 | `ku+mab+si` |  | 3 |
| morphbpe@16384 | `kumab+si` |  | 2 |
| penalty-1@6080 | `ku+ma+b+si` |  | 4 |
| penalty-1@8192 | `kuma+b+si` |  | 3 |
| penalty-1@16384 | `kuma+b+si` |  | 3 |
| penalty-2@6080 | `ku+ma+b+si` |  | 4 |
| penalty-2@8192 | `kuma+b+si` |  | 3 |
| penalty-2@16384 | `kuma+bsi` |  | 2 |
| penalty-4@6080 | `ku+ma+b+si` |  | 4 |
| penalty-4@8192 | `ku+ma+b+si` |  | 4 |
| penalty-4@16384 | `kuma+bsi` |  | 2 |
| penalty-8@6080 | `ku+ma+b+si` |  | 4 |
| penalty-8@8192 | `kuma+b+si` |  | 3 |
| penalty-8@16384 | `kuma+bsi` |  | 2 |
| stochastic-p4-d0.1@6080 | `ku+ma+b+si` |  | 4 |
| stochastic-p4-d0.1@8192 | `kuma+b+si` |  | 3 |
| stochastic-p4-d0.1@16384 | `kuma+bsi` |  | 2 |
| stochastic-p4-d0.2@6080 | `ku+ma+b+si` |  | 4 |
| stochastic-p4-d0.2@8192 | `ku+ma+b+si` |  | 4 |
| stochastic-p4-d0.2@16384 | `kuma+bsi` |  | 2 |
| unigram-ablation@6080 | `ku+m+absi` |  | 3 |

## `linaban`  (infixation, tier A_strong_silver)

**silver gold:** `l+in+aban`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lin+aban` |  | 2 |
| plain@8192 | `lin+aban` |  | 2 |
| plain@16384 | `linaban` |  | 1 |
| morphbpe@6080 | `lin+aban` |  | 2 |
| morphbpe@8192 | `lin+aban` |  | 2 |
| morphbpe@16384 | `lin+aban` |  | 2 |
| penalty-1@6080 | `l+in+aban` | OK | 3 |
| penalty-1@8192 | `l+in+aban` | OK | 3 |
| penalty-1@16384 | `l+in+aban` | OK | 3 |
| penalty-2@6080 | `l+in+aban` | OK | 3 |
| penalty-2@8192 | `l+in+aban` | OK | 3 |
| penalty-2@16384 | `l+in+aban` | OK | 3 |
| penalty-4@6080 | `l+in+a+ban` |  | 4 |
| penalty-4@8192 | `l+in+aban` | OK | 3 |
| penalty-4@16384 | `l+in+aban` | OK | 3 |
| penalty-8@6080 | `l+in+a+ban` |  | 4 |
| penalty-8@8192 | `l+in+aban` | OK | 3 |
| penalty-8@16384 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.1@6080 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.1@8192 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.1@16384 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.2@6080 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.2@8192 | `l+in+aban` | OK | 3 |
| stochastic-p4-d0.2@16384 | `l+in+aban` | OK | 3 |
| unigram-ablation@6080 | `linaba+n` |  | 2 |

## `lumbe`  (infixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `lumbe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lum+be` |  | 2 |
| plain@8192 | `lum+be` |  | 2 |
| plain@16384 | `lumbe` | OK | 1 |
| morphbpe@6080 | `lum+be` |  | 2 |
| morphbpe@8192 | `lum+be` |  | 2 |
| morphbpe@16384 | `lumbe` | OK | 1 |
| penalty-1@6080 | `l+um+be` |  | 3 |
| penalty-1@8192 | `l+umbe` |  | 2 |
| penalty-1@16384 | `lumbe` | OK | 1 |
| penalty-2@6080 | `l+um+be` |  | 3 |
| penalty-2@8192 | `l+umbe` |  | 2 |
| penalty-2@16384 | `lumbe` | OK | 1 |
| penalty-4@6080 | `l+um+be` |  | 3 |
| penalty-4@8192 | `l+umbe` |  | 2 |
| penalty-4@16384 | `lumbe` | OK | 1 |
| penalty-8@6080 | `lum+be` |  | 2 |
| penalty-8@8192 | `lum+be` |  | 2 |
| penalty-8@16384 | `lumbe` | OK | 1 |
| stochastic-p4-d0.1@6080 | `lum+be` |  | 2 |
| stochastic-p4-d0.1@8192 | `lum+be` |  | 2 |
| stochastic-p4-d0.1@16384 | `lumbe` | OK | 1 |
| stochastic-p4-d0.2@6080 | `lum+be` |  | 2 |
| stochastic-p4-d0.2@8192 | `lum+be` |  | 2 |
| stochastic-p4-d0.2@16384 | `lumbe` | OK | 1 |
| unigram-ablation@6080 | `lum+be` |  | 2 |

## `minyabi`  (infixation, tier B_moderate_silver)

**silver gold:** `m+in+yabi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `min+ya+bi` |  | 3 |
| plain@8192 | `min+ya+bi` |  | 3 |
| plain@16384 | `minya+bi` |  | 2 |
| morphbpe@6080 | `min+ya+bi` |  | 3 |
| morphbpe@8192 | `min+ya+bi` |  | 3 |
| morphbpe@16384 | `minya+bi` |  | 2 |
| penalty-1@6080 | `min+ya+bi` |  | 3 |
| penalty-1@8192 | `min+ya+bi` |  | 3 |
| penalty-1@16384 | `minya+bi` |  | 2 |
| penalty-2@6080 | `min+ya+bi` |  | 3 |
| penalty-2@8192 | `min+ya+bi` |  | 3 |
| penalty-2@16384 | `minya+bi` |  | 2 |
| penalty-4@6080 | `min+ya+bi` |  | 3 |
| penalty-4@8192 | `min+ya+bi` |  | 3 |
| penalty-4@16384 | `minya+bi` |  | 2 |
| penalty-8@6080 | `min+ya+bi` |  | 3 |
| penalty-8@8192 | `min+ya+bi` |  | 3 |
| penalty-8@16384 | `minya+bi` |  | 2 |
| stochastic-p4-d0.1@6080 | `min+ya+bi` |  | 3 |
| stochastic-p4-d0.1@8192 | `min+ya+bi` |  | 3 |
| stochastic-p4-d0.1@16384 | `minya+bi` |  | 2 |
| stochastic-p4-d0.2@6080 | `min+ya+bi` |  | 3 |
| stochastic-p4-d0.2@8192 | `min+ya+bi` |  | 3 |
| stochastic-p4-d0.2@16384 | `min+ya+bi` |  | 3 |
| unigram-ablation@6080 | `min+ya+bi` |  | 3 |

## `nining`  (infixation, tier A_strong_silver)

**silver gold:** `n+in+ing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `n+ining` |  | 2 |
| plain@8192 | `n+ining` |  | 2 |
| plain@16384 | `nining` |  | 1 |
| morphbpe@6080 | `nin+ing` |  | 2 |
| morphbpe@8192 | `nin+ing` |  | 2 |
| morphbpe@16384 | `nin+ing` |  | 2 |
| penalty-1@6080 | `n+ining` |  | 2 |
| penalty-1@8192 | `n+ining` |  | 2 |
| penalty-1@16384 | `n+ining` |  | 2 |
| penalty-2@6080 | `n+ining` |  | 2 |
| penalty-2@8192 | `n+ining` |  | 2 |
| penalty-2@16384 | `n+ining` |  | 2 |
| penalty-4@6080 | `n+ining` |  | 2 |
| penalty-4@8192 | `n+ining` |  | 2 |
| penalty-4@16384 | `n+ining` |  | 2 |
| penalty-8@6080 | `n+ining` |  | 2 |
| penalty-8@8192 | `n+ining` |  | 2 |
| penalty-8@16384 | `n+ining` |  | 2 |
| stochastic-p4-d0.1@6080 | `nin+i+ng` |  | 3 |
| stochastic-p4-d0.1@8192 | `nin+i+ng` |  | 3 |
| stochastic-p4-d0.1@16384 | `nin+i+ng` |  | 3 |
| stochastic-p4-d0.2@6080 | `n+ini+ng` |  | 3 |
| stochastic-p4-d0.2@8192 | `n+ini+ng` |  | 3 |
| stochastic-p4-d0.2@16384 | `nini+ng` |  | 2 |
| unigram-ablation@6080 | `ni+ning` |  | 2 |

## `sumakup`  (infixation, tier A_strong_silver)

**silver gold:** `s+um+akup`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sum+akup` |  | 2 |
| plain@8192 | `sum+akup` |  | 2 |
| plain@16384 | `sum+akup` |  | 2 |
| morphbpe@6080 | `sum+akup` |  | 2 |
| morphbpe@8192 | `sum+akup` |  | 2 |
| morphbpe@16384 | `sum+akup` |  | 2 |
| penalty-1@6080 | `su+ma+kup` |  | 3 |
| penalty-1@8192 | `su+ma+kup` |  | 3 |
| penalty-1@16384 | `su+ma+kup` |  | 3 |
| penalty-2@6080 | `su+ma+kup` |  | 3 |
| penalty-2@8192 | `su+ma+kup` |  | 3 |
| penalty-2@16384 | `su+ma+kup` |  | 3 |
| penalty-4@6080 | `su+ma+kup` |  | 3 |
| penalty-4@8192 | `su+ma+kup` |  | 3 |
| penalty-4@16384 | `su+ma+kup` |  | 3 |
| penalty-8@6080 | `su+ma+kup` |  | 3 |
| penalty-8@8192 | `su+ma+kup` |  | 3 |
| penalty-8@16384 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.1@6080 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.1@8192 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.1@16384 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.2@6080 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.2@8192 | `su+ma+kup` |  | 3 |
| stochastic-p4-d0.2@16384 | `suma+kup` |  | 2 |
| unigram-ablation@6080 | `sum+akup` |  | 2 |

## `dumalan`  (infixation, tier A_strong_silver)

**silver gold:** `d+um+alan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dum+alan` |  | 2 |
| plain@8192 | `dum+alan` |  | 2 |
| plain@16384 | `dumalan` |  | 1 |
| morphbpe@6080 | `dum+alan` |  | 2 |
| morphbpe@8192 | `dum+alan` |  | 2 |
| morphbpe@16384 | `dum+alan` |  | 2 |
| penalty-1@6080 | `d+um+alan` | OK | 3 |
| penalty-1@8192 | `d+um+alan` | OK | 3 |
| penalty-1@16384 | `d+um+alan` | OK | 3 |
| penalty-2@6080 | `d+um+alan` | OK | 3 |
| penalty-2@8192 | `d+um+alan` | OK | 3 |
| penalty-2@16384 | `d+um+alan` | OK | 3 |
| penalty-4@6080 | `d+um+alan` | OK | 3 |
| penalty-4@8192 | `d+um+alan` | OK | 3 |
| penalty-4@16384 | `d+um+alan` | OK | 3 |
| penalty-8@6080 | `du+mal+an` |  | 3 |
| penalty-8@8192 | `du+mal+an` |  | 3 |
| penalty-8@16384 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `du+mal+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `du+mal+an` |  | 3 |
| unigram-ablation@6080 | `du+malan` |  | 2 |

## `kinaul`  (infixation, tier A_strong_silver)

**silver gold:** `k+in+aul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `k+ina+ul` |  | 3 |
| plain@8192 | `k+ina+ul` |  | 3 |
| plain@16384 | `kinaul` |  | 1 |
| morphbpe@6080 | `k+ina+ul` |  | 3 |
| morphbpe@8192 | `k+ina+ul` |  | 3 |
| morphbpe@16384 | `kina+ul` |  | 2 |
| penalty-1@6080 | `k+ina+ul` |  | 3 |
| penalty-1@8192 | `k+ina+ul` |  | 3 |
| penalty-1@16384 | `kina+ul` |  | 2 |
| penalty-2@6080 | `k+ina+ul` |  | 3 |
| penalty-2@8192 | `k+ina+ul` |  | 3 |
| penalty-2@16384 | `kina+ul` |  | 2 |
| penalty-4@6080 | `k+in+a+ul` |  | 4 |
| penalty-4@8192 | `k+in+aul` | OK | 3 |
| penalty-4@16384 | `k+in+aul` | OK | 3 |
| penalty-8@6080 | `k+in+a+ul` |  | 4 |
| penalty-8@8192 | `k+in+a+ul` |  | 4 |
| penalty-8@16384 | `k+in+aul` | OK | 3 |
| stochastic-p4-d0.1@6080 | `k+in+a+ul` |  | 4 |
| stochastic-p4-d0.1@8192 | `k+in+aul` | OK | 3 |
| stochastic-p4-d0.1@16384 | `k+in+aul` | OK | 3 |
| stochastic-p4-d0.2@6080 | `k+in+a+ul` |  | 4 |
| stochastic-p4-d0.2@8192 | `k+in+a+ul` |  | 4 |
| stochastic-p4-d0.2@16384 | `k+in+aul` | OK | 3 |
| unigram-ablation@6080 | `ki+na+ul` |  | 3 |

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

## `mabilug`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+bilug`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mabilug` |  | 1 |
| plain@8192 | `mabilug` |  | 1 |
| plain@16384 | `mabilug` |  | 1 |
| morphbpe@6080 | `mab+ilug` |  | 2 |
| morphbpe@8192 | `mab+ilug` |  | 2 |
| morphbpe@16384 | `mab+ilug` |  | 2 |
| penalty-1@6080 | `ma+bilug` | OK | 2 |
| penalty-1@8192 | `ma+bilug` | OK | 2 |
| penalty-1@16384 | `ma+bilug` | OK | 2 |
| penalty-2@6080 | `ma+bilug` | OK | 2 |
| penalty-2@8192 | `ma+bilug` | OK | 2 |
| penalty-2@16384 | `ma+bilug` | OK | 2 |
| penalty-4@6080 | `ma+bilug` | OK | 2 |
| penalty-4@8192 | `ma+bilug` | OK | 2 |
| penalty-4@16384 | `ma+bilug` | OK | 2 |
| penalty-8@6080 | `ma+bilug` | OK | 2 |
| penalty-8@8192 | `ma+bilug` | OK | 2 |
| penalty-8@16384 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+bilug` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+bilug` | OK | 2 |
| unigram-ablation@6080 | `mabilu+g` |  | 2 |

## `manibat`  (prefixation, tier A_strong_silver)

**silver gold:** `man+ibat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manibat` |  | 1 |
| plain@8192 | `manibat` |  | 1 |
| plain@16384 | `manibat` |  | 1 |
| morphbpe@6080 | `manibat` |  | 1 |
| morphbpe@8192 | `manibat` |  | 1 |
| morphbpe@16384 | `manibat` |  | 1 |
| penalty-1@6080 | `manibat` |  | 1 |
| penalty-1@8192 | `manibat` |  | 1 |
| penalty-1@16384 | `manibat` |  | 1 |
| penalty-2@6080 | `manibat` |  | 1 |
| penalty-2@8192 | `manibat` |  | 1 |
| penalty-2@16384 | `manibat` |  | 1 |
| penalty-4@6080 | `manibat` |  | 1 |
| penalty-4@8192 | `manibat` |  | 1 |
| penalty-4@16384 | `manibat` |  | 1 |
| penalty-8@6080 | `manibat` |  | 1 |
| penalty-8@8192 | `manibat` |  | 1 |
| penalty-8@16384 | `manibat` |  | 1 |
| stochastic-p4-d0.1@6080 | `manibat` |  | 1 |
| stochastic-p4-d0.1@8192 | `manibat` |  | 1 |
| stochastic-p4-d0.1@16384 | `manibat` |  | 1 |
| stochastic-p4-d0.2@6080 | `manibat` |  | 1 |
| stochastic-p4-d0.2@8192 | `manibat` |  | 1 |
| stochastic-p4-d0.2@16384 | `manibat` |  | 1 |
| unigram-ablation@6080 | `manibat` |  | 1 |

## `makanian`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `makanian`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makanian` | OK | 1 |
| plain@8192 | `makanian` | OK | 1 |
| plain@16384 | `makanian` | OK | 1 |
| morphbpe@6080 | `makanian` | OK | 1 |
| morphbpe@8192 | `makanian` | OK | 1 |
| morphbpe@16384 | `makanian` | OK | 1 |
| penalty-1@6080 | `makanian` | OK | 1 |
| penalty-1@8192 | `makanian` | OK | 1 |
| penalty-1@16384 | `makanian` | OK | 1 |
| penalty-2@6080 | `makanian` | OK | 1 |
| penalty-2@8192 | `makanian` | OK | 1 |
| penalty-2@16384 | `makanian` | OK | 1 |
| penalty-4@6080 | `makanian` | OK | 1 |
| penalty-4@8192 | `makanian` | OK | 1 |
| penalty-4@16384 | `makanian` | OK | 1 |
| penalty-8@6080 | `makanian` | OK | 1 |
| penalty-8@8192 | `makanian` | OK | 1 |
| penalty-8@16384 | `makanian` | OK | 1 |
| stochastic-p4-d0.1@6080 | `makanian` | OK | 1 |
| stochastic-p4-d0.1@8192 | `makanian` | OK | 1 |
| stochastic-p4-d0.1@16384 | `makanian` | OK | 1 |
| stochastic-p4-d0.2@6080 | `makanian` | OK | 1 |
| stochastic-p4-d0.2@8192 | `makanian` | OK | 1 |
| stochastic-p4-d0.2@16384 | `makanian` | OK | 1 |
| unigram-ablation@6080 | `makanian` | OK | 1 |

## `marawak`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rawak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `marawak` |  | 1 |
| plain@8192 | `marawak` |  | 1 |
| plain@16384 | `marawak` |  | 1 |
| morphbpe@6080 | `marawak` |  | 1 |
| morphbpe@8192 | `marawak` |  | 1 |
| morphbpe@16384 | `marawak` |  | 1 |
| penalty-1@6080 | `marawak` |  | 1 |
| penalty-1@8192 | `marawak` |  | 1 |
| penalty-1@16384 | `marawak` |  | 1 |
| penalty-2@6080 | `marawak` |  | 1 |
| penalty-2@8192 | `marawak` |  | 1 |
| penalty-2@16384 | `marawak` |  | 1 |
| penalty-4@6080 | `marawak` |  | 1 |
| penalty-4@8192 | `marawak` |  | 1 |
| penalty-4@16384 | `marawak` |  | 1 |
| penalty-8@6080 | `marawak` |  | 1 |
| penalty-8@8192 | `marawak` |  | 1 |
| penalty-8@16384 | `marawak` |  | 1 |
| stochastic-p4-d0.1@6080 | `marawak` |  | 1 |
| stochastic-p4-d0.1@8192 | `marawak` |  | 1 |
| stochastic-p4-d0.1@16384 | `marawak` |  | 1 |
| stochastic-p4-d0.2@6080 | `marawak` |  | 1 |
| stochastic-p4-d0.2@8192 | `marawak` |  | 1 |
| stochastic-p4-d0.2@16384 | `marawak` |  | 1 |
| unigram-ablation@6080 | `m+arawak` |  | 2 |

## `panaun`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+naun`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `panaun` |  | 1 |
| plain@8192 | `panaun` |  | 1 |
| plain@16384 | `panaun` |  | 1 |
| morphbpe@6080 | `panaun` |  | 1 |
| morphbpe@8192 | `panaun` |  | 1 |
| morphbpe@16384 | `panaun` |  | 1 |
| penalty-1@6080 | `panaun` |  | 1 |
| penalty-1@8192 | `panaun` |  | 1 |
| penalty-1@16384 | `panaun` |  | 1 |
| penalty-2@6080 | `panaun` |  | 1 |
| penalty-2@8192 | `panaun` |  | 1 |
| penalty-2@16384 | `panaun` |  | 1 |
| penalty-4@6080 | `panaun` |  | 1 |
| penalty-4@8192 | `panaun` |  | 1 |
| penalty-4@16384 | `panaun` |  | 1 |
| penalty-8@6080 | `panaun` |  | 1 |
| penalty-8@8192 | `panaun` |  | 1 |
| penalty-8@16384 | `panaun` |  | 1 |
| stochastic-p4-d0.1@6080 | `panaun` |  | 1 |
| stochastic-p4-d0.1@8192 | `panaun` |  | 1 |
| stochastic-p4-d0.1@16384 | `panaun` |  | 1 |
| stochastic-p4-d0.2@6080 | `panaun` |  | 1 |
| stochastic-p4-d0.2@8192 | `panaun` |  | 1 |
| stochastic-p4-d0.2@16384 | `panaun` |  | 1 |
| unigram-ablation@6080 | `panaun` |  | 1 |

## `matulid`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+tulid`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `matulid` |  | 1 |
| plain@8192 | `matulid` |  | 1 |
| plain@16384 | `matulid` |  | 1 |
| morphbpe@6080 | `mat+ulid` |  | 2 |
| morphbpe@8192 | `mat+ulid` |  | 2 |
| morphbpe@16384 | `mat+ulid` |  | 2 |
| penalty-1@6080 | `mat+ulid` |  | 2 |
| penalty-1@8192 | `mat+ulid` |  | 2 |
| penalty-1@16384 | `mat+ulid` |  | 2 |
| penalty-2@6080 | `mat+ulid` |  | 2 |
| penalty-2@8192 | `mat+ulid` |  | 2 |
| penalty-2@16384 | `mat+ulid` |  | 2 |
| penalty-4@6080 | `mat+ulid` |  | 2 |
| penalty-4@8192 | `mat+ulid` |  | 2 |
| penalty-4@16384 | `mat+ulid` |  | 2 |
| penalty-8@6080 | `mat+uli+d` |  | 3 |
| penalty-8@8192 | `mat+uli+d` |  | 3 |
| penalty-8@16384 | `matulid` |  | 1 |
| stochastic-p4-d0.1@6080 | `mat+uli+d` |  | 3 |
| stochastic-p4-d0.1@8192 | `mat+uli+d` |  | 3 |
| stochastic-p4-d0.1@16384 | `mat+ulid` |  | 2 |
| stochastic-p4-d0.2@6080 | `mat+uli+d` |  | 3 |
| stochastic-p4-d0.2@8192 | `mat+uli+d` |  | 3 |
| stochastic-p4-d0.2@16384 | `mat+uli+d` |  | 3 |
| unigram-ablation@6080 | `ma+tulid` | OK | 2 |

## `maragul`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+ragul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `maragul` |  | 1 |
| plain@8192 | `maragul` |  | 1 |
| plain@16384 | `maragul` |  | 1 |
| morphbpe@6080 | `maragul` |  | 1 |
| morphbpe@8192 | `maragul` |  | 1 |
| morphbpe@16384 | `maragul` |  | 1 |
| penalty-1@6080 | `maragul` |  | 1 |
| penalty-1@8192 | `maragul` |  | 1 |
| penalty-1@16384 | `maragul` |  | 1 |
| penalty-2@6080 | `maragul` |  | 1 |
| penalty-2@8192 | `maragul` |  | 1 |
| penalty-2@16384 | `maragul` |  | 1 |
| penalty-4@6080 | `maragul` |  | 1 |
| penalty-4@8192 | `maragul` |  | 1 |
| penalty-4@16384 | `maragul` |  | 1 |
| penalty-8@6080 | `maragul` |  | 1 |
| penalty-8@8192 | `maragul` |  | 1 |
| penalty-8@16384 | `maragul` |  | 1 |
| stochastic-p4-d0.1@6080 | `maragul` |  | 1 |
| stochastic-p4-d0.1@8192 | `maragul` |  | 1 |
| stochastic-p4-d0.1@16384 | `maragul` |  | 1 |
| stochastic-p4-d0.2@6080 | `maragul` |  | 1 |
| stochastic-p4-d0.2@8192 | `maragul` |  | 1 |
| stochastic-p4-d0.2@16384 | `maragul` |  | 1 |
| unigram-ablation@6080 | `maragul` |  | 1 |

## `meguing`  (prefixation, tier B_moderate_silver)

**silver gold:** `meg+uing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `meguing` |  | 1 |
| plain@8192 | `meguing` |  | 1 |
| plain@16384 | `meguing` |  | 1 |
| morphbpe@6080 | `meguing` |  | 1 |
| morphbpe@8192 | `meguing` |  | 1 |
| morphbpe@16384 | `meguing` |  | 1 |
| penalty-1@6080 | `meguing` |  | 1 |
| penalty-1@8192 | `meguing` |  | 1 |
| penalty-1@16384 | `meguing` |  | 1 |
| penalty-2@6080 | `meguing` |  | 1 |
| penalty-2@8192 | `meguing` |  | 1 |
| penalty-2@16384 | `meguing` |  | 1 |
| penalty-4@6080 | `meguing` |  | 1 |
| penalty-4@8192 | `meguing` |  | 1 |
| penalty-4@16384 | `meguing` |  | 1 |
| penalty-8@6080 | `meguing` |  | 1 |
| penalty-8@8192 | `meguing` |  | 1 |
| penalty-8@16384 | `meguing` |  | 1 |
| stochastic-p4-d0.1@6080 | `meguing` |  | 1 |
| stochastic-p4-d0.1@8192 | `meguing` |  | 1 |
| stochastic-p4-d0.1@16384 | `meguing` |  | 1 |
| stochastic-p4-d0.2@6080 | `meguing` |  | 1 |
| stochastic-p4-d0.2@8192 | `meguing` |  | 1 |
| stochastic-p4-d0.2@16384 | `meguing` |  | 1 |
| unigram-ablation@6080 | `megu+ing` |  | 2 |

## `manatili`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+atili`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manatili` |  | 1 |
| plain@8192 | `manatili` |  | 1 |
| plain@16384 | `manatili` |  | 1 |
| morphbpe@6080 | `manatili` |  | 1 |
| morphbpe@8192 | `manatili` |  | 1 |
| morphbpe@16384 | `manatili` |  | 1 |
| penalty-1@6080 | `manatili` |  | 1 |
| penalty-1@8192 | `manatili` |  | 1 |
| penalty-1@16384 | `manatili` |  | 1 |
| penalty-2@6080 | `manatili` |  | 1 |
| penalty-2@8192 | `manatili` |  | 1 |
| penalty-2@16384 | `manatili` |  | 1 |
| penalty-4@6080 | `manatili` |  | 1 |
| penalty-4@8192 | `manatili` |  | 1 |
| penalty-4@16384 | `manatili` |  | 1 |
| penalty-8@6080 | `manatili` |  | 1 |
| penalty-8@8192 | `manatili` |  | 1 |
| penalty-8@16384 | `manatili` |  | 1 |
| stochastic-p4-d0.1@6080 | `manatili` |  | 1 |
| stochastic-p4-d0.1@8192 | `manatili` |  | 1 |
| stochastic-p4-d0.1@16384 | `manatili` |  | 1 |
| stochastic-p4-d0.2@6080 | `manatili` |  | 1 |
| stochastic-p4-d0.2@8192 | `manatili` |  | 1 |
| stochastic-p4-d0.2@16384 | `manatili` |  | 1 |
| unigram-ablation@6080 | `manatili` |  | 1 |

## `pasibayu`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+sibayu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pasibayu` |  | 1 |
| plain@8192 | `pasibayu` |  | 1 |
| plain@16384 | `pasibayu` |  | 1 |
| morphbpe@6080 | `pasibayu` |  | 1 |
| morphbpe@8192 | `pasibayu` |  | 1 |
| morphbpe@16384 | `pasibayu` |  | 1 |
| penalty-1@6080 | `pasibayu` |  | 1 |
| penalty-1@8192 | `pasibayu` |  | 1 |
| penalty-1@16384 | `pasibayu` |  | 1 |
| penalty-2@6080 | `pasibayu` |  | 1 |
| penalty-2@8192 | `pasibayu` |  | 1 |
| penalty-2@16384 | `pasibayu` |  | 1 |
| penalty-4@6080 | `pasibayu` |  | 1 |
| penalty-4@8192 | `pasibayu` |  | 1 |
| penalty-4@16384 | `pasibayu` |  | 1 |
| penalty-8@6080 | `pasibayu` |  | 1 |
| penalty-8@8192 | `pasibayu` |  | 1 |
| penalty-8@16384 | `pasibayu` |  | 1 |
| stochastic-p4-d0.1@6080 | `pasibayu` |  | 1 |
| stochastic-p4-d0.1@8192 | `pasibayu` |  | 1 |
| stochastic-p4-d0.1@16384 | `pasibayu` |  | 1 |
| stochastic-p4-d0.2@6080 | `pasibayu` |  | 1 |
| stochastic-p4-d0.2@8192 | `pasibayu` |  | 1 |
| stochastic-p4-d0.2@16384 | `pasibayu` |  | 1 |
| unigram-ablation@6080 | `pasibayu` |  | 1 |

## `marangle`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rangle`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `marangle` |  | 1 |
| plain@8192 | `marangle` |  | 1 |
| plain@16384 | `marangle` |  | 1 |
| morphbpe@6080 | `marangle` |  | 1 |
| morphbpe@8192 | `marangle` |  | 1 |
| morphbpe@16384 | `marangle` |  | 1 |
| penalty-1@6080 | `marangle` |  | 1 |
| penalty-1@8192 | `marangle` |  | 1 |
| penalty-1@16384 | `marangle` |  | 1 |
| penalty-2@6080 | `marangle` |  | 1 |
| penalty-2@8192 | `marangle` |  | 1 |
| penalty-2@16384 | `marangle` |  | 1 |
| penalty-4@6080 | `marangle` |  | 1 |
| penalty-4@8192 | `marangle` |  | 1 |
| penalty-4@16384 | `marangle` |  | 1 |
| penalty-8@6080 | `marangle` |  | 1 |
| penalty-8@8192 | `marangle` |  | 1 |
| penalty-8@16384 | `marangle` |  | 1 |
| stochastic-p4-d0.1@6080 | `marangle` |  | 1 |
| stochastic-p4-d0.1@8192 | `marangle` |  | 1 |
| stochastic-p4-d0.1@16384 | `marangle` |  | 1 |
| stochastic-p4-d0.2@6080 | `marangle` |  | 1 |
| stochastic-p4-d0.2@8192 | `marangle` |  | 1 |
| stochastic-p4-d0.2@16384 | `marangle` |  | 1 |
| unigram-ablation@6080 | `marangle` |  | 1 |

## `panalangin`  (prefixation, tier B_moderate_silver)

**silver gold:** `pan+alangin`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `panalangin` |  | 1 |
| plain@8192 | `panalangin` |  | 1 |
| plain@16384 | `panalangin` |  | 1 |
| morphbpe@6080 | `panalangin` |  | 1 |
| morphbpe@8192 | `panalangin` |  | 1 |
| morphbpe@16384 | `panalangin` |  | 1 |
| penalty-1@6080 | `panalangin` |  | 1 |
| penalty-1@8192 | `panalangin` |  | 1 |
| penalty-1@16384 | `panalangin` |  | 1 |
| penalty-2@6080 | `panalangin` |  | 1 |
| penalty-2@8192 | `panalangin` |  | 1 |
| penalty-2@16384 | `panalangin` |  | 1 |
| penalty-4@6080 | `panalangin` |  | 1 |
| penalty-4@8192 | `panalangin` |  | 1 |
| penalty-4@16384 | `panalangin` |  | 1 |
| penalty-8@6080 | `panalangin` |  | 1 |
| penalty-8@8192 | `panalangin` |  | 1 |
| penalty-8@16384 | `panalangin` |  | 1 |
| stochastic-p4-d0.1@6080 | `panalangin` |  | 1 |
| stochastic-p4-d0.1@8192 | `panalangin` |  | 1 |
| stochastic-p4-d0.1@16384 | `panalangin` |  | 1 |
| stochastic-p4-d0.2@6080 | `panalangin` |  | 1 |
| stochastic-p4-d0.2@8192 | `panalangin` |  | 1 |
| stochastic-p4-d0.2@16384 | `panalangin` |  | 1 |
| unigram-ablation@6080 | `panalangin` |  | 1 |

## `makananu`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+nanu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makananu` |  | 1 |
| plain@8192 | `makananu` |  | 1 |
| plain@16384 | `makananu` |  | 1 |
| morphbpe@6080 | `makananu` |  | 1 |
| morphbpe@8192 | `makananu` |  | 1 |
| morphbpe@16384 | `makananu` |  | 1 |
| penalty-1@6080 | `makananu` |  | 1 |
| penalty-1@8192 | `makananu` |  | 1 |
| penalty-1@16384 | `makananu` |  | 1 |
| penalty-2@6080 | `makananu` |  | 1 |
| penalty-2@8192 | `makananu` |  | 1 |
| penalty-2@16384 | `makananu` |  | 1 |
| penalty-4@6080 | `makananu` |  | 1 |
| penalty-4@8192 | `makananu` |  | 1 |
| penalty-4@16384 | `makananu` |  | 1 |
| penalty-8@6080 | `makananu` |  | 1 |
| penalty-8@8192 | `makananu` |  | 1 |
| penalty-8@16384 | `makananu` |  | 1 |
| stochastic-p4-d0.1@6080 | `makananu` |  | 1 |
| stochastic-p4-d0.1@8192 | `makananu` |  | 1 |
| stochastic-p4-d0.1@16384 | `makananu` |  | 1 |
| stochastic-p4-d0.2@6080 | `makananu` |  | 1 |
| stochastic-p4-d0.2@8192 | `makananu` |  | 1 |
| stochastic-p4-d0.2@16384 | `makananu` |  | 1 |
| unigram-ablation@6080 | `makananu` |  | 1 |

## `makanyan`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+kanyan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makanyan` |  | 1 |
| plain@8192 | `makanyan` |  | 1 |
| plain@16384 | `makanyan` |  | 1 |
| morphbpe@6080 | `makanyan` |  | 1 |
| morphbpe@8192 | `makanyan` |  | 1 |
| morphbpe@16384 | `makanyan` |  | 1 |
| penalty-1@6080 | `makanyan` |  | 1 |
| penalty-1@8192 | `makanyan` |  | 1 |
| penalty-1@16384 | `makanyan` |  | 1 |
| penalty-2@6080 | `makanyan` |  | 1 |
| penalty-2@8192 | `makanyan` |  | 1 |
| penalty-2@16384 | `makanyan` |  | 1 |
| penalty-4@6080 | `makanyan` |  | 1 |
| penalty-4@8192 | `makanyan` |  | 1 |
| penalty-4@16384 | `makanyan` |  | 1 |
| penalty-8@6080 | `makanyan` |  | 1 |
| penalty-8@8192 | `makanyan` |  | 1 |
| penalty-8@16384 | `makanyan` |  | 1 |
| stochastic-p4-d0.1@6080 | `makanyan` |  | 1 |
| stochastic-p4-d0.1@8192 | `makanyan` |  | 1 |
| stochastic-p4-d0.1@16384 | `makanyan` |  | 1 |
| stochastic-p4-d0.2@6080 | `makanyan` |  | 1 |
| stochastic-p4-d0.2@8192 | `makanyan` |  | 1 |
| stochastic-p4-d0.2@16384 | `makanyan` |  | 1 |
| unigram-ablation@6080 | `makanyan` |  | 1 |

## `mangatua`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+atua`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mang+atua` | OK | 2 |
| plain@8192 | `mangatua` |  | 1 |
| plain@16384 | `mangatua` |  | 1 |
| morphbpe@6080 | `mangat+ua` |  | 2 |
| morphbpe@8192 | `mangatua` |  | 1 |
| morphbpe@16384 | `mangatua` |  | 1 |
| penalty-1@6080 | `mangat+ua` |  | 2 |
| penalty-1@8192 | `mangatua` |  | 1 |
| penalty-1@16384 | `mangatua` |  | 1 |
| penalty-2@6080 | `mangat+ua` |  | 2 |
| penalty-2@8192 | `mangatua` |  | 1 |
| penalty-2@16384 | `mangatua` |  | 1 |
| penalty-4@6080 | `mangat+ua` |  | 2 |
| penalty-4@8192 | `mangatua` |  | 1 |
| penalty-4@16384 | `mangatua` |  | 1 |
| penalty-8@6080 | `mangat+ua` |  | 2 |
| penalty-8@8192 | `mangatua` |  | 1 |
| penalty-8@16384 | `mangatua` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangat+ua` |  | 2 |
| stochastic-p4-d0.1@8192 | `mangatua` |  | 1 |
| stochastic-p4-d0.1@16384 | `mangatua` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangat+ua` |  | 2 |
| stochastic-p4-d0.2@8192 | `mangatua` |  | 1 |
| stochastic-p4-d0.2@16384 | `mangatua` |  | 1 |
| unigram-ablation@6080 | `mangatua` |  | 1 |

## `malyari`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+lyari`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malyari` |  | 1 |
| plain@8192 | `malyari` |  | 1 |
| plain@16384 | `malyari` |  | 1 |
| morphbpe@6080 | `malyari` |  | 1 |
| morphbpe@8192 | `malyari` |  | 1 |
| morphbpe@16384 | `malyari` |  | 1 |
| penalty-1@6080 | `malyari` |  | 1 |
| penalty-1@8192 | `malyari` |  | 1 |
| penalty-1@16384 | `malyari` |  | 1 |
| penalty-2@6080 | `malyari` |  | 1 |
| penalty-2@8192 | `malyari` |  | 1 |
| penalty-2@16384 | `malyari` |  | 1 |
| penalty-4@6080 | `malyari` |  | 1 |
| penalty-4@8192 | `malyari` |  | 1 |
| penalty-4@16384 | `malyari` |  | 1 |
| penalty-8@6080 | `malyari` |  | 1 |
| penalty-8@8192 | `malyari` |  | 1 |
| penalty-8@16384 | `malyari` |  | 1 |
| stochastic-p4-d0.1@6080 | `malyari` |  | 1 |
| stochastic-p4-d0.1@8192 | `malyari` |  | 1 |
| stochastic-p4-d0.1@16384 | `malyari` |  | 1 |
| stochastic-p4-d0.2@6080 | `malyari` |  | 1 |
| stochastic-p4-d0.2@8192 | `malyari` |  | 1 |
| stochastic-p4-d0.2@16384 | `malyari` |  | 1 |
| unigram-ablation@6080 | `malyari` |  | 1 |

## `pitung`  (prefixation, tier A_strong_silver)

**silver gold:** `pi+tung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pitung` |  | 1 |
| plain@8192 | `pitung` |  | 1 |
| plain@16384 | `pitung` |  | 1 |
| morphbpe@6080 | `pitung` |  | 1 |
| morphbpe@8192 | `pitung` |  | 1 |
| morphbpe@16384 | `pitung` |  | 1 |
| penalty-1@6080 | `pitung` |  | 1 |
| penalty-1@8192 | `pitung` |  | 1 |
| penalty-1@16384 | `pitung` |  | 1 |
| penalty-2@6080 | `pitung` |  | 1 |
| penalty-2@8192 | `pitung` |  | 1 |
| penalty-2@16384 | `pitung` |  | 1 |
| penalty-4@6080 | `pitung` |  | 1 |
| penalty-4@8192 | `pitung` |  | 1 |
| penalty-4@16384 | `pitung` |  | 1 |
| penalty-8@6080 | `pitung` |  | 1 |
| penalty-8@8192 | `pitung` |  | 1 |
| penalty-8@16384 | `pitung` |  | 1 |
| stochastic-p4-d0.1@6080 | `pitung` |  | 1 |
| stochastic-p4-d0.1@8192 | `pitung` |  | 1 |
| stochastic-p4-d0.1@16384 | `pitung` |  | 1 |
| stochastic-p4-d0.2@6080 | `pitung` |  | 1 |
| stochastic-p4-d0.2@8192 | `pitung` |  | 1 |
| stochastic-p4-d0.2@16384 | `pitung` |  | 1 |
| unigram-ablation@6080 | `pitung` |  | 1 |

## `pablasang`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+blasang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pablasang` |  | 1 |
| plain@8192 | `pablasang` |  | 1 |
| plain@16384 | `pablasang` |  | 1 |
| morphbpe@6080 | `pablasang` |  | 1 |
| morphbpe@8192 | `pablasang` |  | 1 |
| morphbpe@16384 | `pablasang` |  | 1 |
| penalty-1@6080 | `pablasang` |  | 1 |
| penalty-1@8192 | `pablasang` |  | 1 |
| penalty-1@16384 | `pablasang` |  | 1 |
| penalty-2@6080 | `pablasang` |  | 1 |
| penalty-2@8192 | `pablasang` |  | 1 |
| penalty-2@16384 | `pablasang` |  | 1 |
| penalty-4@6080 | `pablasang` |  | 1 |
| penalty-4@8192 | `pablasang` |  | 1 |
| penalty-4@16384 | `pablasang` |  | 1 |
| penalty-8@6080 | `pablasang` |  | 1 |
| penalty-8@8192 | `pablasang` |  | 1 |
| penalty-8@16384 | `pablasang` |  | 1 |
| stochastic-p4-d0.1@6080 | `pablasang` |  | 1 |
| stochastic-p4-d0.1@8192 | `pablasang` |  | 1 |
| stochastic-p4-d0.1@16384 | `pablasang` |  | 1 |
| stochastic-p4-d0.2@6080 | `pablasang` |  | 1 |
| stochastic-p4-d0.2@8192 | `pablasang` |  | 1 |
| stochastic-p4-d0.2@16384 | `pablasang` |  | 1 |
| unigram-ablation@6080 | `pablasa+ng` |  | 2 |

## `malyaring`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+lyaring`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malyaring` |  | 1 |
| plain@8192 | `malyaring` |  | 1 |
| plain@16384 | `malyaring` |  | 1 |
| morphbpe@6080 | `malyaring` |  | 1 |
| morphbpe@8192 | `malyaring` |  | 1 |
| morphbpe@16384 | `malyaring` |  | 1 |
| penalty-1@6080 | `malyaring` |  | 1 |
| penalty-1@8192 | `malyaring` |  | 1 |
| penalty-1@16384 | `malyaring` |  | 1 |
| penalty-2@6080 | `malyaring` |  | 1 |
| penalty-2@8192 | `malyaring` |  | 1 |
| penalty-2@16384 | `malyaring` |  | 1 |
| penalty-4@6080 | `malyaring` |  | 1 |
| penalty-4@8192 | `malyaring` |  | 1 |
| penalty-4@16384 | `malyaring` |  | 1 |
| penalty-8@6080 | `malyaring` |  | 1 |
| penalty-8@8192 | `malyaring` |  | 1 |
| penalty-8@16384 | `malyaring` |  | 1 |
| stochastic-p4-d0.1@6080 | `malyaring` |  | 1 |
| stochastic-p4-d0.1@8192 | `malyaring` |  | 1 |
| stochastic-p4-d0.1@16384 | `malyaring` |  | 1 |
| stochastic-p4-d0.2@6080 | `malyaring` |  | 1 |
| stochastic-p4-d0.2@8192 | `malyaring` |  | 1 |
| stochastic-p4-d0.2@16384 | `malyaring` |  | 1 |
| unigram-ablation@6080 | `malyari+ng` |  | 2 |

## `maiguit`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+iguit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ma+iguit` | OK | 2 |
| plain@8192 | `maiguit` |  | 1 |
| plain@16384 | `maiguit` |  | 1 |
| morphbpe@6080 | `ma+iguit` | OK | 2 |
| morphbpe@8192 | `maiguit` |  | 1 |
| morphbpe@16384 | `maiguit` |  | 1 |
| penalty-1@6080 | `ma+iguit` | OK | 2 |
| penalty-1@8192 | `maiguit` |  | 1 |
| penalty-1@16384 | `maiguit` |  | 1 |
| penalty-2@6080 | `ma+iguit` | OK | 2 |
| penalty-2@8192 | `maiguit` |  | 1 |
| penalty-2@16384 | `maiguit` |  | 1 |
| penalty-4@6080 | `ma+iguit` | OK | 2 |
| penalty-4@8192 | `maiguit` |  | 1 |
| penalty-4@16384 | `maiguit` |  | 1 |
| penalty-8@6080 | `ma+iguit` | OK | 2 |
| penalty-8@8192 | `maiguit` |  | 1 |
| penalty-8@16384 | `maiguit` |  | 1 |
| stochastic-p4-d0.1@6080 | `mai+guit` |  | 2 |
| stochastic-p4-d0.1@8192 | `maiguit` |  | 1 |
| stochastic-p4-d0.1@16384 | `maiguit` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+iguit` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maiguit` |  | 1 |
| stochastic-p4-d0.2@16384 | `maiguit` |  | 1 |
| unigram-ablation@6080 | `m+aiguit` |  | 2 |

## `magkang`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+kang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+kang` | OK | 2 |
| plain@8192 | `magkang` |  | 1 |
| plain@16384 | `magkang` |  | 1 |
| morphbpe@6080 | `mag+kang` | OK | 2 |
| morphbpe@8192 | `mag+kang` | OK | 2 |
| morphbpe@16384 | `mag+kang` | OK | 2 |
| penalty-1@6080 | `mag+kang` | OK | 2 |
| penalty-1@8192 | `mag+kang` | OK | 2 |
| penalty-1@16384 | `mag+kang` | OK | 2 |
| penalty-2@6080 | `mag+kang` | OK | 2 |
| penalty-2@8192 | `mag+kang` | OK | 2 |
| penalty-2@16384 | `mag+kang` | OK | 2 |
| penalty-4@6080 | `mag+kang` | OK | 2 |
| penalty-4@8192 | `mag+kang` | OK | 2 |
| penalty-4@16384 | `mag+kang` | OK | 2 |
| penalty-8@6080 | `mag+kang` | OK | 2 |
| penalty-8@8192 | `mag+kang` | OK | 2 |
| penalty-8@16384 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mag+kang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mag+kang` | OK | 2 |
| unigram-ablation@6080 | `mag+kang` | OK | 2 |

## `pasbul`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+sbul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pasbul` |  | 1 |
| plain@8192 | `pasbul` |  | 1 |
| plain@16384 | `pasbul` |  | 1 |
| morphbpe@6080 | `pasbul` |  | 1 |
| morphbpe@8192 | `pasbul` |  | 1 |
| morphbpe@16384 | `pasbul` |  | 1 |
| penalty-1@6080 | `pasbul` |  | 1 |
| penalty-1@8192 | `pasbul` |  | 1 |
| penalty-1@16384 | `pasbul` |  | 1 |
| penalty-2@6080 | `pasbul` |  | 1 |
| penalty-2@8192 | `pasbul` |  | 1 |
| penalty-2@16384 | `pasbul` |  | 1 |
| penalty-4@6080 | `pasbul` |  | 1 |
| penalty-4@8192 | `pasbul` |  | 1 |
| penalty-4@16384 | `pasbul` |  | 1 |
| penalty-8@6080 | `pasbul` |  | 1 |
| penalty-8@8192 | `pasbul` |  | 1 |
| penalty-8@16384 | `pasbul` |  | 1 |
| stochastic-p4-d0.1@6080 | `pasbul` |  | 1 |
| stochastic-p4-d0.1@8192 | `pasbul` |  | 1 |
| stochastic-p4-d0.1@16384 | `pasbul` |  | 1 |
| stochastic-p4-d0.2@6080 | `pasbul` |  | 1 |
| stochastic-p4-d0.2@8192 | `pasbul` |  | 1 |
| stochastic-p4-d0.2@16384 | `pasbul` |  | 1 |
| unigram-ablation@6080 | `pasbul` |  | 1 |

## `maniabi`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+iabi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `maniabi` |  | 1 |
| plain@8192 | `maniabi` |  | 1 |
| plain@16384 | `maniabi` |  | 1 |
| morphbpe@6080 | `maniabi` |  | 1 |
| morphbpe@8192 | `maniabi` |  | 1 |
| morphbpe@16384 | `maniabi` |  | 1 |
| penalty-1@6080 | `maniabi` |  | 1 |
| penalty-1@8192 | `maniabi` |  | 1 |
| penalty-1@16384 | `maniabi` |  | 1 |
| penalty-2@6080 | `maniabi` |  | 1 |
| penalty-2@8192 | `maniabi` |  | 1 |
| penalty-2@16384 | `maniabi` |  | 1 |
| penalty-4@6080 | `maniabi` |  | 1 |
| penalty-4@8192 | `maniabi` |  | 1 |
| penalty-4@16384 | `maniabi` |  | 1 |
| penalty-8@6080 | `maniabi` |  | 1 |
| penalty-8@8192 | `maniabi` |  | 1 |
| penalty-8@16384 | `maniabi` |  | 1 |
| stochastic-p4-d0.1@6080 | `maniabi` |  | 1 |
| stochastic-p4-d0.1@8192 | `maniabi` |  | 1 |
| stochastic-p4-d0.1@16384 | `maniabi` |  | 1 |
| stochastic-p4-d0.2@6080 | `maniabi` |  | 1 |
| stochastic-p4-d0.2@8192 | `maniabi` |  | 1 |
| stochastic-p4-d0.2@16384 | `maniabi` |  | 1 |
| unigram-ablation@6080 | `maniabi` |  | 1 |

## `pasalamat`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+salamat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pasalamat` |  | 1 |
| plain@8192 | `pasalamat` |  | 1 |
| plain@16384 | `pasalamat` |  | 1 |
| morphbpe@6080 | `pas+al+amat` |  | 3 |
| morphbpe@8192 | `pas+alamat` |  | 2 |
| morphbpe@16384 | `pas+alamat` |  | 2 |
| penalty-1@6080 | `pas+al+amat` |  | 3 |
| penalty-1@8192 | `pas+alamat` |  | 2 |
| penalty-1@16384 | `pas+alamat` |  | 2 |
| penalty-2@6080 | `pa+salamat` | OK | 2 |
| penalty-2@8192 | `pa+salamat` | OK | 2 |
| penalty-2@16384 | `pa+salamat` | OK | 2 |
| penalty-4@6080 | `pa+salamat` | OK | 2 |
| penalty-4@8192 | `pa+salamat` | OK | 2 |
| penalty-4@16384 | `pa+salamat` | OK | 2 |
| penalty-8@6080 | `pa+salamat` | OK | 2 |
| penalty-8@8192 | `pa+salamat` | OK | 2 |
| penalty-8@16384 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.1@6080 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.1@8192 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.1@16384 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.2@6080 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pa+salamat` | OK | 2 |
| stochastic-p4-d0.2@16384 | `pa+salamat` | OK | 2 |
| unigram-ablation@6080 | `pasalamat` |  | 1 |

## `mangan`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+ngan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangan` |  | 1 |
| plain@8192 | `mangan` |  | 1 |
| plain@16384 | `mangan` |  | 1 |
| morphbpe@6080 | `mangan` |  | 1 |
| morphbpe@8192 | `mangan` |  | 1 |
| morphbpe@16384 | `mangan` |  | 1 |
| penalty-1@6080 | `mangan` |  | 1 |
| penalty-1@8192 | `mangan` |  | 1 |
| penalty-1@16384 | `mangan` |  | 1 |
| penalty-2@6080 | `mangan` |  | 1 |
| penalty-2@8192 | `mangan` |  | 1 |
| penalty-2@16384 | `mangan` |  | 1 |
| penalty-4@6080 | `mangan` |  | 1 |
| penalty-4@8192 | `mangan` |  | 1 |
| penalty-4@16384 | `mangan` |  | 1 |
| penalty-8@6080 | `mang+an` |  | 2 |
| penalty-8@8192 | `mangan` |  | 1 |
| penalty-8@16384 | `mangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `mangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `mangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `mangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `mangan` |  | 1 |
| unigram-ablation@6080 | `mangan` |  | 1 |

## `pagamuamu`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+gamuamu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+amu+amu` |  | 3 |
| plain@8192 | `pag+amuamu` |  | 2 |
| plain@16384 | `pagamuamu` |  | 1 |
| morphbpe@6080 | `pag+amu+amu` |  | 3 |
| morphbpe@8192 | `pag+amuamu` |  | 2 |
| morphbpe@16384 | `pagamuamu` |  | 1 |
| penalty-1@6080 | `pag+amu+amu` |  | 3 |
| penalty-1@8192 | `pag+amuamu` |  | 2 |
| penalty-1@16384 | `pagamuamu` |  | 1 |
| penalty-2@6080 | `pag+amu+amu` |  | 3 |
| penalty-2@8192 | `pag+amuamu` |  | 2 |
| penalty-2@16384 | `pagamuamu` |  | 1 |
| penalty-4@6080 | `pag+amu+amu` |  | 3 |
| penalty-4@8192 | `pag+amuamu` |  | 2 |
| penalty-4@16384 | `pagamuamu` |  | 1 |
| penalty-8@6080 | `pag+amu+amu` |  | 3 |
| penalty-8@8192 | `pag+amuamu` |  | 2 |
| penalty-8@16384 | `pagamuamu` |  | 1 |
| stochastic-p4-d0.1@6080 | `pag+amu+amu` |  | 3 |
| stochastic-p4-d0.1@8192 | `pag+amu+amu` |  | 3 |
| stochastic-p4-d0.1@16384 | `pagamuamu` |  | 1 |
| stochastic-p4-d0.2@6080 | `pag+amu+amu` |  | 3 |
| stochastic-p4-d0.2@8192 | `pag+amu+amu` |  | 3 |
| stochastic-p4-d0.2@16384 | `pagamuamu` |  | 1 |
| unigram-ablation@6080 | `pa+gamuamu` | OK | 2 |

## `manaya`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+naya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manaya` |  | 1 |
| plain@8192 | `manaya` |  | 1 |
| plain@16384 | `manaya` |  | 1 |
| morphbpe@6080 | `man+aya` |  | 2 |
| morphbpe@8192 | `man+aya` |  | 2 |
| morphbpe@16384 | `man+aya` |  | 2 |
| penalty-1@6080 | `man+aya` |  | 2 |
| penalty-1@8192 | `man+aya` |  | 2 |
| penalty-1@16384 | `man+aya` |  | 2 |
| penalty-2@6080 | `man+aya` |  | 2 |
| penalty-2@8192 | `man+aya` |  | 2 |
| penalty-2@16384 | `man+aya` |  | 2 |
| penalty-4@6080 | `man+aya` |  | 2 |
| penalty-4@8192 | `man+aya` |  | 2 |
| penalty-4@16384 | `man+aya` |  | 2 |
| penalty-8@6080 | `man+aya` |  | 2 |
| penalty-8@8192 | `man+aya` |  | 2 |
| penalty-8@16384 | `man+aya` |  | 2 |
| stochastic-p4-d0.1@6080 | `man+aya` |  | 2 |
| stochastic-p4-d0.1@8192 | `man+aya` |  | 2 |
| stochastic-p4-d0.1@16384 | `man+aya` |  | 2 |
| stochastic-p4-d0.2@6080 | `man+aya` |  | 2 |
| stochastic-p4-d0.2@8192 | `man+aya` |  | 2 |
| stochastic-p4-d0.2@16384 | `man+aya` |  | 2 |
| unigram-ablation@6080 | `manaya` |  | 1 |

## `marayu`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rayu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `marayu` |  | 1 |
| plain@8192 | `marayu` |  | 1 |
| plain@16384 | `marayu` |  | 1 |
| morphbpe@6080 | `marayu` |  | 1 |
| morphbpe@8192 | `marayu` |  | 1 |
| morphbpe@16384 | `marayu` |  | 1 |
| penalty-1@6080 | `marayu` |  | 1 |
| penalty-1@8192 | `marayu` |  | 1 |
| penalty-1@16384 | `marayu` |  | 1 |
| penalty-2@6080 | `marayu` |  | 1 |
| penalty-2@8192 | `marayu` |  | 1 |
| penalty-2@16384 | `marayu` |  | 1 |
| penalty-4@6080 | `marayu` |  | 1 |
| penalty-4@8192 | `marayu` |  | 1 |
| penalty-4@16384 | `marayu` |  | 1 |
| penalty-8@6080 | `marayu` |  | 1 |
| penalty-8@8192 | `marayu` |  | 1 |
| penalty-8@16384 | `marayu` |  | 1 |
| stochastic-p4-d0.1@6080 | `marayu` |  | 1 |
| stochastic-p4-d0.1@8192 | `marayu` |  | 1 |
| stochastic-p4-d0.1@16384 | `marayu` |  | 1 |
| stochastic-p4-d0.2@6080 | `marayu` |  | 1 |
| stochastic-p4-d0.2@8192 | `marayu` |  | 1 |
| stochastic-p4-d0.2@16384 | `marayu` |  | 1 |
| unigram-ablation@6080 | `marayu` |  | 1 |

## `pangane`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pangane`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pangan+e` |  | 2 |
| plain@8192 | `pangan+e` |  | 2 |
| plain@16384 | `pangane` | OK | 1 |
| morphbpe@6080 | `pangan+e` |  | 2 |
| morphbpe@8192 | `pangan+e` |  | 2 |
| morphbpe@16384 | `pangane` | OK | 1 |
| penalty-1@6080 | `pangan+e` |  | 2 |
| penalty-1@8192 | `pangan+e` |  | 2 |
| penalty-1@16384 | `pangane` | OK | 1 |
| penalty-2@6080 | `pangan+e` |  | 2 |
| penalty-2@8192 | `pangan+e` |  | 2 |
| penalty-2@16384 | `pangane` | OK | 1 |
| penalty-4@6080 | `pangan+e` |  | 2 |
| penalty-4@8192 | `pangan+e` |  | 2 |
| penalty-4@16384 | `pangane` | OK | 1 |
| penalty-8@6080 | `pangan+e` |  | 2 |
| penalty-8@8192 | `pangan+e` |  | 2 |
| penalty-8@16384 | `pangane` | OK | 1 |
| stochastic-p4-d0.1@6080 | `pangan+e` |  | 2 |
| stochastic-p4-d0.1@8192 | `pangan+e` |  | 2 |
| stochastic-p4-d0.1@16384 | `pangane` | OK | 1 |
| stochastic-p4-d0.2@6080 | `pangan+e` |  | 2 |
| stochastic-p4-d0.2@8192 | `pangan+e` |  | 2 |
| stochastic-p4-d0.2@16384 | `pangane` | OK | 1 |
| unigram-ablation@6080 | `panga+ne` |  | 2 |

## `makapagmulala`  (prefixation, tier A_strong_silver)

**silver gold:** `makapag+mulala`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makapag+mulala` | OK | 2 |
| plain@8192 | `makapag+mulala` | OK | 2 |
| plain@16384 | `makapagmulala` |  | 1 |
| morphbpe@6080 | `makapag+mulala` | OK | 2 |
| morphbpe@8192 | `makapag+mulala` | OK | 2 |
| morphbpe@16384 | `makapag+mulala` | OK | 2 |
| penalty-1@6080 | `makapag+mulala` | OK | 2 |
| penalty-1@8192 | `makapag+mulala` | OK | 2 |
| penalty-1@16384 | `makapag+mulala` | OK | 2 |
| penalty-2@6080 | `makapag+mulala` | OK | 2 |
| penalty-2@8192 | `makapag+mulala` | OK | 2 |
| penalty-2@16384 | `makapag+mulala` | OK | 2 |
| penalty-4@6080 | `makapag+mulala` | OK | 2 |
| penalty-4@8192 | `makapag+mulala` | OK | 2 |
| penalty-4@16384 | `makapag+mulala` | OK | 2 |
| penalty-8@6080 | `makapag+mulala` | OK | 2 |
| penalty-8@8192 | `makapag+mulala` | OK | 2 |
| penalty-8@16384 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.1@6080 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.1@8192 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.1@16384 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.2@6080 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.2@8192 | `makapag+mulala` | OK | 2 |
| stochastic-p4-d0.2@16384 | `makapag+mulala` | OK | 2 |
| unigram-ablation@6080 | `makapagmulala` |  | 1 |

## `malagu`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lagu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malagu` |  | 1 |
| plain@8192 | `malagu` |  | 1 |
| plain@16384 | `malagu` |  | 1 |
| morphbpe@6080 | `malagu` |  | 1 |
| morphbpe@8192 | `malagu` |  | 1 |
| morphbpe@16384 | `malagu` |  | 1 |
| penalty-1@6080 | `malagu` |  | 1 |
| penalty-1@8192 | `malagu` |  | 1 |
| penalty-1@16384 | `malagu` |  | 1 |
| penalty-2@6080 | `malagu` |  | 1 |
| penalty-2@8192 | `malagu` |  | 1 |
| penalty-2@16384 | `malagu` |  | 1 |
| penalty-4@6080 | `malagu` |  | 1 |
| penalty-4@8192 | `malagu` |  | 1 |
| penalty-4@16384 | `malagu` |  | 1 |
| penalty-8@6080 | `malagu` |  | 1 |
| penalty-8@8192 | `malagu` |  | 1 |
| penalty-8@16384 | `malagu` |  | 1 |
| stochastic-p4-d0.1@6080 | `malagu` |  | 1 |
| stochastic-p4-d0.1@8192 | `malagu` |  | 1 |
| stochastic-p4-d0.1@16384 | `malagu` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+lagu` | OK | 2 |
| stochastic-p4-d0.2@8192 | `malagu` |  | 1 |
| stochastic-p4-d0.2@16384 | `malagu` |  | 1 |
| unigram-ablation@6080 | `malagu` |  | 1 |

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

## `manalig`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+alig`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+alig` | OK | 2 |
| plain@8192 | `man+alig` | OK | 2 |
| plain@16384 | `manalig` |  | 1 |
| morphbpe@6080 | `man+alig` | OK | 2 |
| morphbpe@8192 | `man+alig` | OK | 2 |
| morphbpe@16384 | `man+alig` | OK | 2 |
| penalty-1@6080 | `man+alig` | OK | 2 |
| penalty-1@8192 | `man+alig` | OK | 2 |
| penalty-1@16384 | `man+alig` | OK | 2 |
| penalty-2@6080 | `man+alig` | OK | 2 |
| penalty-2@8192 | `man+alig` | OK | 2 |
| penalty-2@16384 | `man+alig` | OK | 2 |
| penalty-4@6080 | `man+alig` | OK | 2 |
| penalty-4@8192 | `man+alig` | OK | 2 |
| penalty-4@16384 | `man+alig` | OK | 2 |
| penalty-8@6080 | `man+alig` | OK | 2 |
| penalty-8@8192 | `man+alig` | OK | 2 |
| penalty-8@16384 | `man+alig` | OK | 2 |
| stochastic-p4-d0.1@6080 | `man+alig` | OK | 2 |
| stochastic-p4-d0.1@8192 | `man+alig` | OK | 2 |
| stochastic-p4-d0.1@16384 | `man+alig` | OK | 2 |
| stochastic-p4-d0.2@6080 | `man+alig` | OK | 2 |
| stochastic-p4-d0.2@8192 | `man+alig` | OK | 2 |
| stochastic-p4-d0.2@16384 | `man+alig` | OK | 2 |
| unigram-ablation@6080 | `manalig` |  | 1 |

## `masikan`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+sikan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masikan` |  | 1 |
| plain@8192 | `masikan` |  | 1 |
| plain@16384 | `masikan` |  | 1 |
| morphbpe@6080 | `masikan` |  | 1 |
| morphbpe@8192 | `masikan` |  | 1 |
| morphbpe@16384 | `masikan` |  | 1 |
| penalty-1@6080 | `masikan` |  | 1 |
| penalty-1@8192 | `masikan` |  | 1 |
| penalty-1@16384 | `masikan` |  | 1 |
| penalty-2@6080 | `masikan` |  | 1 |
| penalty-2@8192 | `masikan` |  | 1 |
| penalty-2@16384 | `masikan` |  | 1 |
| penalty-4@6080 | `masikan` |  | 1 |
| penalty-4@8192 | `masikan` |  | 1 |
| penalty-4@16384 | `masikan` |  | 1 |
| penalty-8@6080 | `masikan` |  | 1 |
| penalty-8@8192 | `masikan` |  | 1 |
| penalty-8@16384 | `masikan` |  | 1 |
| stochastic-p4-d0.1@6080 | `masikan` |  | 1 |
| stochastic-p4-d0.1@8192 | `masikan` |  | 1 |
| stochastic-p4-d0.1@16384 | `masikan` |  | 1 |
| stochastic-p4-d0.2@6080 | `masikan` |  | 1 |
| stochastic-p4-d0.2@8192 | `masikan` |  | 1 |
| stochastic-p4-d0.2@16384 | `masikan` |  | 1 |
| unigram-ablation@6080 | `masikan` |  | 1 |

## `paninap`  (prefixation, tier B_moderate_silver)

**silver gold:** `pan+inap`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+inap` | OK | 2 |
| plain@8192 | `paninap` |  | 1 |
| plain@16384 | `paninap` |  | 1 |
| morphbpe@6080 | `paninap` |  | 1 |
| morphbpe@8192 | `paninap` |  | 1 |
| morphbpe@16384 | `paninap` |  | 1 |
| penalty-1@6080 | `paninap` |  | 1 |
| penalty-1@8192 | `paninap` |  | 1 |
| penalty-1@16384 | `paninap` |  | 1 |
| penalty-2@6080 | `paninap` |  | 1 |
| penalty-2@8192 | `paninap` |  | 1 |
| penalty-2@16384 | `paninap` |  | 1 |
| penalty-4@6080 | `paninap` |  | 1 |
| penalty-4@8192 | `paninap` |  | 1 |
| penalty-4@16384 | `paninap` |  | 1 |
| penalty-8@6080 | `paninap` |  | 1 |
| penalty-8@8192 | `paninap` |  | 1 |
| penalty-8@16384 | `paninap` |  | 1 |
| stochastic-p4-d0.1@6080 | `paninap` |  | 1 |
| stochastic-p4-d0.1@8192 | `paninap` |  | 1 |
| stochastic-p4-d0.1@16384 | `paninap` |  | 1 |
| stochastic-p4-d0.2@6080 | `paninap` |  | 1 |
| stochastic-p4-d0.2@8192 | `paninap` |  | 1 |
| stochastic-p4-d0.2@16384 | `paninap` |  | 1 |
| unigram-ablation@6080 | `paninap` |  | 1 |

## `manakit`  (prefixation, tier A_strong_silver)

**silver gold:** `man+akit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manakit` |  | 1 |
| plain@8192 | `manakit` |  | 1 |
| plain@16384 | `manakit` |  | 1 |
| morphbpe@6080 | `manakit` |  | 1 |
| morphbpe@8192 | `manakit` |  | 1 |
| morphbpe@16384 | `manakit` |  | 1 |
| penalty-1@6080 | `manakit` |  | 1 |
| penalty-1@8192 | `manakit` |  | 1 |
| penalty-1@16384 | `manakit` |  | 1 |
| penalty-2@6080 | `manakit` |  | 1 |
| penalty-2@8192 | `manakit` |  | 1 |
| penalty-2@16384 | `manakit` |  | 1 |
| penalty-4@6080 | `manakit` |  | 1 |
| penalty-4@8192 | `manakit` |  | 1 |
| penalty-4@16384 | `manakit` |  | 1 |
| penalty-8@6080 | `manakit` |  | 1 |
| penalty-8@8192 | `manakit` |  | 1 |
| penalty-8@16384 | `manakit` |  | 1 |
| stochastic-p4-d0.1@6080 | `manakit` |  | 1 |
| stochastic-p4-d0.1@8192 | `manakit` |  | 1 |
| stochastic-p4-d0.1@16384 | `manakit` |  | 1 |
| stochastic-p4-d0.2@6080 | `manakit` |  | 1 |
| stochastic-p4-d0.2@8192 | `manakit` |  | 1 |
| stochastic-p4-d0.2@16384 | `manakit` |  | 1 |
| unigram-ablation@6080 | `manakit` |  | 1 |

## `mangaragul`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+aragul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangaragul` |  | 1 |
| plain@8192 | `mangaragul` |  | 1 |
| plain@16384 | `mangaragul` |  | 1 |
| morphbpe@6080 | `mangaragul` |  | 1 |
| morphbpe@8192 | `mangaragul` |  | 1 |
| morphbpe@16384 | `mangaragul` |  | 1 |
| penalty-1@6080 | `mangaragul` |  | 1 |
| penalty-1@8192 | `mangaragul` |  | 1 |
| penalty-1@16384 | `mangaragul` |  | 1 |
| penalty-2@6080 | `mangaragul` |  | 1 |
| penalty-2@8192 | `mangaragul` |  | 1 |
| penalty-2@16384 | `mangaragul` |  | 1 |
| penalty-4@6080 | `mangaragul` |  | 1 |
| penalty-4@8192 | `mangaragul` |  | 1 |
| penalty-4@16384 | `mangaragul` |  | 1 |
| penalty-8@6080 | `mangaragul` |  | 1 |
| penalty-8@8192 | `mangaragul` |  | 1 |
| penalty-8@16384 | `mangaragul` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangaragul` |  | 1 |
| stochastic-p4-d0.1@8192 | `mangaragul` |  | 1 |
| stochastic-p4-d0.1@16384 | `mangaragul` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangaragul` |  | 1 |
| stochastic-p4-d0.2@8192 | `mangaragul` |  | 1 |
| stochastic-p4-d0.2@16384 | `mangaragul` |  | 1 |
| unigram-ablation@6080 | `mangaragul` |  | 1 |

## `menganak`  (prefixation, tier A_strong_silver)

**silver gold:** `meng+anak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `meng+anak` | OK | 2 |
| plain@8192 | `meng+anak` | OK | 2 |
| plain@16384 | `meng+anak` | OK | 2 |
| morphbpe@6080 | `meng+anak` | OK | 2 |
| morphbpe@8192 | `meng+anak` | OK | 2 |
| morphbpe@16384 | `meng+anak` | OK | 2 |
| penalty-1@6080 | `meng+anak` | OK | 2 |
| penalty-1@8192 | `meng+anak` | OK | 2 |
| penalty-1@16384 | `meng+anak` | OK | 2 |
| penalty-2@6080 | `meng+anak` | OK | 2 |
| penalty-2@8192 | `meng+anak` | OK | 2 |
| penalty-2@16384 | `meng+anak` | OK | 2 |
| penalty-4@6080 | `meng+anak` | OK | 2 |
| penalty-4@8192 | `meng+anak` | OK | 2 |
| penalty-4@16384 | `meng+anak` | OK | 2 |
| penalty-8@6080 | `meng+anak` | OK | 2 |
| penalty-8@8192 | `meng+anak` | OK | 2 |
| penalty-8@16384 | `meng+anak` | OK | 2 |
| stochastic-p4-d0.1@6080 | `meng+anak` | OK | 2 |
| stochastic-p4-d0.1@8192 | `meng+anak` | OK | 2 |
| stochastic-p4-d0.1@16384 | `meng+anak` | OK | 2 |
| stochastic-p4-d0.2@6080 | `me+ngan+ak` |  | 3 |
| stochastic-p4-d0.2@8192 | `mengan+ak` |  | 2 |
| stochastic-p4-d0.2@16384 | `mengan+ak` |  | 2 |
| unigram-ablation@6080 | `meng+anak` | OK | 2 |

## `makapayan`  (prefixation, tier B_moderate_silver)

**silver gold:** `maka+payan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makap+ayan` |  | 2 |
| plain@8192 | `makap+ayan` |  | 2 |
| plain@16384 | `makapayan` |  | 1 |
| morphbpe@6080 | `maka+payan` | OK | 2 |
| morphbpe@8192 | `maka+payan` | OK | 2 |
| morphbpe@16384 | `makapayan` |  | 1 |
| penalty-1@6080 | `maka+payan` | OK | 2 |
| penalty-1@8192 | `maka+payan` | OK | 2 |
| penalty-1@16384 | `makapayan` |  | 1 |
| penalty-2@6080 | `maka+payan` | OK | 2 |
| penalty-2@8192 | `maka+payan` | OK | 2 |
| penalty-2@16384 | `makapayan` |  | 1 |
| penalty-4@6080 | `maka+payan` | OK | 2 |
| penalty-4@8192 | `maka+payan` | OK | 2 |
| penalty-4@16384 | `makapayan` |  | 1 |
| penalty-8@6080 | `maka+payan` | OK | 2 |
| penalty-8@8192 | `maka+payan` | OK | 2 |
| penalty-8@16384 | `makapayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `maka+payan` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+payan` | OK | 2 |
| stochastic-p4-d0.1@16384 | `makapayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `maka+payan` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+payan` | OK | 2 |
| stochastic-p4-d0.2@16384 | `makapayan` |  | 1 |
| unigram-ablation@6080 | `makapa+yan` |  | 2 |

## `masanting`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+santing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masanting` |  | 1 |
| plain@8192 | `masanting` |  | 1 |
| plain@16384 | `masanting` |  | 1 |
| morphbpe@6080 | `masanting` |  | 1 |
| morphbpe@8192 | `masanting` |  | 1 |
| morphbpe@16384 | `masanting` |  | 1 |
| penalty-1@6080 | `masanting` |  | 1 |
| penalty-1@8192 | `masanting` |  | 1 |
| penalty-1@16384 | `masanting` |  | 1 |
| penalty-2@6080 | `masanting` |  | 1 |
| penalty-2@8192 | `masanting` |  | 1 |
| penalty-2@16384 | `masanting` |  | 1 |
| penalty-4@6080 | `masanting` |  | 1 |
| penalty-4@8192 | `masanting` |  | 1 |
| penalty-4@16384 | `masanting` |  | 1 |
| penalty-8@6080 | `masanting` |  | 1 |
| penalty-8@8192 | `masanting` |  | 1 |
| penalty-8@16384 | `masanting` |  | 1 |
| stochastic-p4-d0.1@6080 | `masanting` |  | 1 |
| stochastic-p4-d0.1@8192 | `masanting` |  | 1 |
| stochastic-p4-d0.1@16384 | `masanting` |  | 1 |
| stochastic-p4-d0.2@6080 | `masanting` |  | 1 |
| stochastic-p4-d0.2@8192 | `masanting` |  | 1 |
| stochastic-p4-d0.2@16384 | `masanting` |  | 1 |
| unigram-ablation@6080 | `masanting` |  | 1 |

## `magsaya`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+saya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+saya` | OK | 2 |
| plain@8192 | `mag+saya` | OK | 2 |
| plain@16384 | `magsaya` |  | 1 |
| morphbpe@6080 | `mag+saya` | OK | 2 |
| morphbpe@8192 | `magsaya` |  | 1 |
| morphbpe@16384 | `magsaya` |  | 1 |
| penalty-1@6080 | `mag+saya` | OK | 2 |
| penalty-1@8192 | `magsaya` |  | 1 |
| penalty-1@16384 | `magsaya` |  | 1 |
| penalty-2@6080 | `mag+saya` | OK | 2 |
| penalty-2@8192 | `magsaya` |  | 1 |
| penalty-2@16384 | `magsaya` |  | 1 |
| penalty-4@6080 | `mag+sa+ya` |  | 3 |
| penalty-4@8192 | `magsa+ya` |  | 2 |
| penalty-4@16384 | `magsaya` |  | 1 |
| penalty-8@6080 | `mag+sa+ya` |  | 3 |
| penalty-8@8192 | `magsa+ya` |  | 2 |
| penalty-8@16384 | `magsaya` |  | 1 |
| stochastic-p4-d0.1@6080 | `mag+sa+ya` |  | 3 |
| stochastic-p4-d0.1@8192 | `mag+sa+ya` |  | 3 |
| stochastic-p4-d0.1@16384 | `magsaya` |  | 1 |
| stochastic-p4-d0.2@6080 | `magsa+ya` |  | 2 |
| stochastic-p4-d0.2@8192 | `magsa+ya` |  | 2 |
| stochastic-p4-d0.2@16384 | `magsaya` |  | 1 |
| unigram-ablation@6080 | `mag+saya` | OK | 2 |

## `manintun`  (prefixation, tier A_strong_silver)

**silver gold:** `man+intun`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manintun` |  | 1 |
| plain@8192 | `manintun` |  | 1 |
| plain@16384 | `manintun` |  | 1 |
| morphbpe@6080 | `manintun` |  | 1 |
| morphbpe@8192 | `manintun` |  | 1 |
| morphbpe@16384 | `manintun` |  | 1 |
| penalty-1@6080 | `manintun` |  | 1 |
| penalty-1@8192 | `manintun` |  | 1 |
| penalty-1@16384 | `manintun` |  | 1 |
| penalty-2@6080 | `manintun` |  | 1 |
| penalty-2@8192 | `manintun` |  | 1 |
| penalty-2@16384 | `manintun` |  | 1 |
| penalty-4@6080 | `manintun` |  | 1 |
| penalty-4@8192 | `manintun` |  | 1 |
| penalty-4@16384 | `manintun` |  | 1 |
| penalty-8@6080 | `manintun` |  | 1 |
| penalty-8@8192 | `manintun` |  | 1 |
| penalty-8@16384 | `manintun` |  | 1 |
| stochastic-p4-d0.1@6080 | `manintun` |  | 1 |
| stochastic-p4-d0.1@8192 | `manintun` |  | 1 |
| stochastic-p4-d0.1@16384 | `manintun` |  | 1 |
| stochastic-p4-d0.2@6080 | `manintun` |  | 1 |
| stochastic-p4-d0.2@8192 | `manintun` |  | 1 |
| stochastic-p4-d0.2@16384 | `manintun` |  | 1 |
| unigram-ablation@6080 | `manintun` |  | 1 |

## `parang`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `parang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `parang` | OK | 1 |
| plain@8192 | `parang` | OK | 1 |
| plain@16384 | `parang` | OK | 1 |
| morphbpe@6080 | `parang` | OK | 1 |
| morphbpe@8192 | `parang` | OK | 1 |
| morphbpe@16384 | `parang` | OK | 1 |
| penalty-1@6080 | `parang` | OK | 1 |
| penalty-1@8192 | `parang` | OK | 1 |
| penalty-1@16384 | `parang` | OK | 1 |
| penalty-2@6080 | `parang` | OK | 1 |
| penalty-2@8192 | `parang` | OK | 1 |
| penalty-2@16384 | `parang` | OK | 1 |
| penalty-4@6080 | `parang` | OK | 1 |
| penalty-4@8192 | `parang` | OK | 1 |
| penalty-4@16384 | `parang` | OK | 1 |
| penalty-8@6080 | `parang` | OK | 1 |
| penalty-8@8192 | `parang` | OK | 1 |
| penalty-8@16384 | `parang` | OK | 1 |
| stochastic-p4-d0.1@6080 | `parang` | OK | 1 |
| stochastic-p4-d0.1@8192 | `parang` | OK | 1 |
| stochastic-p4-d0.1@16384 | `parang` | OK | 1 |
| stochastic-p4-d0.2@6080 | `parang` | OK | 1 |
| stochastic-p4-d0.2@8192 | `parang` | OK | 1 |
| stochastic-p4-d0.2@16384 | `parang` | OK | 1 |
| unigram-ablation@6080 | `para+ng` |  | 2 |

## `patutu`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+tutu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `patutu` |  | 1 |
| plain@8192 | `patutu` |  | 1 |
| plain@16384 | `patutu` |  | 1 |
| morphbpe@6080 | `pat+utu` |  | 2 |
| morphbpe@8192 | `pat+utu` |  | 2 |
| morphbpe@16384 | `pat+utu` |  | 2 |
| penalty-1@6080 | `pat+utu` |  | 2 |
| penalty-1@8192 | `pat+utu` |  | 2 |
| penalty-1@16384 | `pat+utu` |  | 2 |
| penalty-2@6080 | `pat+utu` |  | 2 |
| penalty-2@8192 | `pat+utu` |  | 2 |
| penalty-2@16384 | `pat+utu` |  | 2 |
| penalty-4@6080 | `patu+tu` |  | 2 |
| penalty-4@8192 | `patu+tu` |  | 2 |
| penalty-4@16384 | `patutu` |  | 1 |
| penalty-8@6080 | `pat+utu` |  | 2 |
| penalty-8@8192 | `pat+utu` |  | 2 |
| penalty-8@16384 | `pat+utu` |  | 2 |
| stochastic-p4-d0.1@6080 | `pat+utu` |  | 2 |
| stochastic-p4-d0.1@8192 | `pat+utu` |  | 2 |
| stochastic-p4-d0.1@16384 | `pat+utu` |  | 2 |
| stochastic-p4-d0.2@6080 | `pat+utu` |  | 2 |
| stochastic-p4-d0.2@8192 | `pat+utu` |  | 2 |
| stochastic-p4-d0.2@16384 | `pat+utu` |  | 2 |
| unigram-ablation@6080 | `patutu` |  | 1 |

## `malapit`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lapit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malapit` |  | 1 |
| plain@8192 | `malapit` |  | 1 |
| plain@16384 | `malapit` |  | 1 |
| morphbpe@6080 | `malapit` |  | 1 |
| morphbpe@8192 | `malapit` |  | 1 |
| morphbpe@16384 | `malapit` |  | 1 |
| penalty-1@6080 | `malapit` |  | 1 |
| penalty-1@8192 | `malapit` |  | 1 |
| penalty-1@16384 | `malapit` |  | 1 |
| penalty-2@6080 | `malapit` |  | 1 |
| penalty-2@8192 | `malapit` |  | 1 |
| penalty-2@16384 | `malapit` |  | 1 |
| penalty-4@6080 | `malapit` |  | 1 |
| penalty-4@8192 | `malapit` |  | 1 |
| penalty-4@16384 | `malapit` |  | 1 |
| penalty-8@6080 | `malapit` |  | 1 |
| penalty-8@8192 | `malapit` |  | 1 |
| penalty-8@16384 | `malapit` |  | 1 |
| stochastic-p4-d0.1@6080 | `malapit` |  | 1 |
| stochastic-p4-d0.1@8192 | `malapit` |  | 1 |
| stochastic-p4-d0.1@16384 | `malapit` |  | 1 |
| stochastic-p4-d0.2@6080 | `malapit` |  | 1 |
| stochastic-p4-d0.2@8192 | `malapit` |  | 1 |
| stochastic-p4-d0.2@16384 | `malapit` |  | 1 |
| unigram-ablation@6080 | `malapit` |  | 1 |

## `maligaya`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+ligaya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+igaya` |  | 2 |
| plain@8192 | `mal+igaya` |  | 2 |
| plain@16384 | `maligaya` |  | 1 |
| morphbpe@6080 | `mal+igaya` |  | 2 |
| morphbpe@8192 | `mal+igaya` |  | 2 |
| morphbpe@16384 | `maligaya` |  | 1 |
| penalty-1@6080 | `mal+igaya` |  | 2 |
| penalty-1@8192 | `mal+igaya` |  | 2 |
| penalty-1@16384 | `maligaya` |  | 1 |
| penalty-2@6080 | `mal+igaya` |  | 2 |
| penalty-2@8192 | `mal+igaya` |  | 2 |
| penalty-2@16384 | `maligaya` |  | 1 |
| penalty-4@6080 | `mal+igaya` |  | 2 |
| penalty-4@8192 | `mal+igaya` |  | 2 |
| penalty-4@16384 | `maligaya` |  | 1 |
| penalty-8@6080 | `m+aligaya` |  | 2 |
| penalty-8@8192 | `m+aligaya` |  | 2 |
| penalty-8@16384 | `maligaya` |  | 1 |
| stochastic-p4-d0.1@6080 | `mali+gaya` |  | 2 |
| stochastic-p4-d0.1@8192 | `mali+gaya` |  | 2 |
| stochastic-p4-d0.1@16384 | `maligaya` |  | 1 |
| stochastic-p4-d0.2@6080 | `mali+gaya` |  | 2 |
| stochastic-p4-d0.2@8192 | `mali+gaya` |  | 2 |
| stochastic-p4-d0.2@16384 | `maligaya` |  | 1 |
| unigram-ablation@6080 | `ma+ligaya` | OK | 2 |

## `menakit`  (prefixation, tier A_strong_silver)

**silver gold:** `men+akit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `menakit` |  | 1 |
| plain@8192 | `menakit` |  | 1 |
| plain@16384 | `menakit` |  | 1 |
| morphbpe@6080 | `menakit` |  | 1 |
| morphbpe@8192 | `menakit` |  | 1 |
| morphbpe@16384 | `menakit` |  | 1 |
| penalty-1@6080 | `menakit` |  | 1 |
| penalty-1@8192 | `menakit` |  | 1 |
| penalty-1@16384 | `menakit` |  | 1 |
| penalty-2@6080 | `menakit` |  | 1 |
| penalty-2@8192 | `menakit` |  | 1 |
| penalty-2@16384 | `menakit` |  | 1 |
| penalty-4@6080 | `menakit` |  | 1 |
| penalty-4@8192 | `menakit` |  | 1 |
| penalty-4@16384 | `menakit` |  | 1 |
| penalty-8@6080 | `menakit` |  | 1 |
| penalty-8@8192 | `menakit` |  | 1 |
| penalty-8@16384 | `menakit` |  | 1 |
| stochastic-p4-d0.1@6080 | `menakit` |  | 1 |
| stochastic-p4-d0.1@8192 | `menakit` |  | 1 |
| stochastic-p4-d0.1@16384 | `menakit` |  | 1 |
| stochastic-p4-d0.2@6080 | `menakit` |  | 1 |
| stochastic-p4-d0.2@8192 | `menakit` |  | 1 |
| stochastic-p4-d0.2@16384 | `menakit` |  | 1 |
| unigram-ablation@6080 | `menakit` |  | 1 |

## `matibe`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+tibe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `matibe` |  | 1 |
| plain@8192 | `matibe` |  | 1 |
| plain@16384 | `matibe` |  | 1 |
| morphbpe@6080 | `mat+ibe` |  | 2 |
| morphbpe@8192 | `mat+ibe` |  | 2 |
| morphbpe@16384 | `mat+ibe` |  | 2 |
| penalty-1@6080 | `mat+ibe` |  | 2 |
| penalty-1@8192 | `mat+ibe` |  | 2 |
| penalty-1@16384 | `mat+ibe` |  | 2 |
| penalty-2@6080 | `mat+ibe` |  | 2 |
| penalty-2@8192 | `mat+ibe` |  | 2 |
| penalty-2@16384 | `mat+ibe` |  | 2 |
| penalty-4@6080 | `mat+ib+e` |  | 3 |
| penalty-4@8192 | `mat+ibe` |  | 2 |
| penalty-4@16384 | `mat+ibe` |  | 2 |
| penalty-8@6080 | `mati+be` |  | 2 |
| penalty-8@8192 | `mati+be` |  | 2 |
| penalty-8@16384 | `mati+be` |  | 2 |
| stochastic-p4-d0.1@6080 | `mati+be` |  | 2 |
| stochastic-p4-d0.1@8192 | `mati+be` |  | 2 |
| stochastic-p4-d0.1@16384 | `mati+be` |  | 2 |
| stochastic-p4-d0.2@6080 | `m+ati+be` |  | 3 |
| stochastic-p4-d0.2@8192 | `m+ati+be` |  | 3 |
| stochastic-p4-d0.2@16384 | `mati+be` |  | 2 |
| unigram-ablation@6080 | `matibe` |  | 1 |

## `makatalakad`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+talakad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makatalakad` |  | 1 |
| plain@8192 | `makatalakad` |  | 1 |
| plain@16384 | `makatalakad` |  | 1 |
| morphbpe@6080 | `makat+alakad` |  | 2 |
| morphbpe@8192 | `makat+alakad` |  | 2 |
| morphbpe@16384 | `makat+alakad` |  | 2 |
| penalty-1@6080 | `makat+alakad` |  | 2 |
| penalty-1@8192 | `makat+alakad` |  | 2 |
| penalty-1@16384 | `makat+alakad` |  | 2 |
| penalty-2@6080 | `makat+alakad` |  | 2 |
| penalty-2@8192 | `makat+alakad` |  | 2 |
| penalty-2@16384 | `makat+alakad` |  | 2 |
| penalty-4@6080 | `maka+talakad` | OK | 2 |
| penalty-4@8192 | `maka+talakad` | OK | 2 |
| penalty-4@16384 | `maka+talakad` | OK | 2 |
| penalty-8@6080 | `maka+talakad` | OK | 2 |
| penalty-8@8192 | `maka+talakad` | OK | 2 |
| penalty-8@16384 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+talakad` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+talakad` | OK | 2 |
| unigram-ablation@6080 | `makata+lakad` |  | 2 |

## `makatua`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+katua`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makatua` |  | 1 |
| plain@8192 | `makatua` |  | 1 |
| plain@16384 | `makatua` |  | 1 |
| morphbpe@6080 | `makat+ua` |  | 2 |
| morphbpe@8192 | `makat+ua` |  | 2 |
| morphbpe@16384 | `makat+ua` |  | 2 |
| penalty-1@6080 | `makat+ua` |  | 2 |
| penalty-1@8192 | `makat+ua` |  | 2 |
| penalty-1@16384 | `makat+ua` |  | 2 |
| penalty-2@6080 | `makat+ua` |  | 2 |
| penalty-2@8192 | `makat+ua` |  | 2 |
| penalty-2@16384 | `makat+ua` |  | 2 |
| penalty-4@6080 | `maka+tua` |  | 2 |
| penalty-4@8192 | `maka+tua` |  | 2 |
| penalty-4@16384 | `maka+tua` |  | 2 |
| penalty-8@6080 | `maka+tua` |  | 2 |
| penalty-8@8192 | `maka+tua` |  | 2 |
| penalty-8@16384 | `maka+tua` |  | 2 |
| stochastic-p4-d0.1@6080 | `maka+tua` |  | 2 |
| stochastic-p4-d0.1@8192 | `maka+tua` |  | 2 |
| stochastic-p4-d0.1@16384 | `maka+tua` |  | 2 |
| stochastic-p4-d0.2@6080 | `maka+tua` |  | 2 |
| stochastic-p4-d0.2@8192 | `maka+tua` |  | 2 |
| stochastic-p4-d0.2@16384 | `maka+tua` |  | 2 |
| unigram-ablation@6080 | `makatua` |  | 1 |

## `makiramdam`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+kiramdam`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makiramdam` |  | 1 |
| plain@8192 | `makiramdam` |  | 1 |
| plain@16384 | `makiramdam` |  | 1 |
| morphbpe@6080 | `makiramdam` |  | 1 |
| morphbpe@8192 | `makiramdam` |  | 1 |
| morphbpe@16384 | `makiramdam` |  | 1 |
| penalty-1@6080 | `makiramdam` |  | 1 |
| penalty-1@8192 | `makiramdam` |  | 1 |
| penalty-1@16384 | `makiramdam` |  | 1 |
| penalty-2@6080 | `makiramdam` |  | 1 |
| penalty-2@8192 | `makiramdam` |  | 1 |
| penalty-2@16384 | `makiramdam` |  | 1 |
| penalty-4@6080 | `makiramdam` |  | 1 |
| penalty-4@8192 | `makiramdam` |  | 1 |
| penalty-4@16384 | `makiramdam` |  | 1 |
| penalty-8@6080 | `makiramdam` |  | 1 |
| penalty-8@8192 | `makiramdam` |  | 1 |
| penalty-8@16384 | `makiramdam` |  | 1 |
| stochastic-p4-d0.1@6080 | `makiramdam` |  | 1 |
| stochastic-p4-d0.1@8192 | `makiramdam` |  | 1 |
| stochastic-p4-d0.1@16384 | `makiramdam` |  | 1 |
| stochastic-p4-d0.2@6080 | `makiramdam` |  | 1 |
| stochastic-p4-d0.2@8192 | `makiramdam` |  | 1 |
| stochastic-p4-d0.2@16384 | `makiramdam` |  | 1 |
| unigram-ablation@6080 | `m+akiramdam` |  | 2 |

## `matula`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+tula`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `matula` |  | 1 |
| plain@8192 | `matula` |  | 1 |
| plain@16384 | `matula` |  | 1 |
| morphbpe@6080 | `matula` |  | 1 |
| morphbpe@8192 | `matula` |  | 1 |
| morphbpe@16384 | `matula` |  | 1 |
| penalty-1@6080 | `matula` |  | 1 |
| penalty-1@8192 | `matula` |  | 1 |
| penalty-1@16384 | `matula` |  | 1 |
| penalty-2@6080 | `matula` |  | 1 |
| penalty-2@8192 | `matula` |  | 1 |
| penalty-2@16384 | `matula` |  | 1 |
| penalty-4@6080 | `matula` |  | 1 |
| penalty-4@8192 | `matula` |  | 1 |
| penalty-4@16384 | `matula` |  | 1 |
| penalty-8@6080 | `matula` |  | 1 |
| penalty-8@8192 | `matula` |  | 1 |
| penalty-8@16384 | `matula` |  | 1 |
| stochastic-p4-d0.1@6080 | `matula` |  | 1 |
| stochastic-p4-d0.1@8192 | `matula` |  | 1 |
| stochastic-p4-d0.1@16384 | `matula` |  | 1 |
| stochastic-p4-d0.2@6080 | `matula` |  | 1 |
| stochastic-p4-d0.2@8192 | `matula` |  | 1 |
| stochastic-p4-d0.2@16384 | `matula` |  | 1 |
| unigram-ablation@6080 | `matula` |  | 1 |

## `miguising`  (prefixation, tier B_moderate_silver)

**silver gold:** `mig+uising`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mig+u+ising` |  | 3 |
| plain@8192 | `mig+u+ising` |  | 3 |
| plain@16384 | `miguising` |  | 1 |
| morphbpe@6080 | `mig+u+ising` |  | 3 |
| morphbpe@8192 | `migu+ising` |  | 2 |
| morphbpe@16384 | `miguising` |  | 1 |
| penalty-1@6080 | `mig+u+ising` |  | 3 |
| penalty-1@8192 | `migu+ising` |  | 2 |
| penalty-1@16384 | `miguising` |  | 1 |
| penalty-2@6080 | `mig+u+ising` |  | 3 |
| penalty-2@8192 | `migu+ising` |  | 2 |
| penalty-2@16384 | `miguising` |  | 1 |
| penalty-4@6080 | `mi+gu+ising` |  | 3 |
| penalty-4@8192 | `mi+gu+ising` |  | 3 |
| penalty-4@16384 | `miguising` |  | 1 |
| penalty-8@6080 | `mi+gu+ising` |  | 3 |
| penalty-8@8192 | `mi+gu+ising` |  | 3 |
| penalty-8@16384 | `miguising` |  | 1 |
| stochastic-p4-d0.1@6080 | `mi+gu+isi+ng` |  | 4 |
| stochastic-p4-d0.1@8192 | `mi+gu+isi+ng` |  | 4 |
| stochastic-p4-d0.1@16384 | `miguising` |  | 1 |
| stochastic-p4-d0.2@6080 | `mi+gu+isi+ng` |  | 4 |
| stochastic-p4-d0.2@8192 | `mi+gu+isi+ng` |  | 4 |
| stochastic-p4-d0.2@16384 | `miguising` |  | 1 |
| unigram-ablation@6080 | `mi+gui+s+ing` |  | 4 |

## `magsantung`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+santung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+sant+ung` |  | 3 |
| plain@8192 | `mag+sant+ung` |  | 3 |
| plain@16384 | `magsantung` |  | 1 |
| morphbpe@6080 | `mag+sant+ung` |  | 3 |
| morphbpe@8192 | `mag+santung` | OK | 2 |
| morphbpe@16384 | `mag+santung` | OK | 2 |
| penalty-1@6080 | `mag+sant+ung` |  | 3 |
| penalty-1@8192 | `mag+santung` | OK | 2 |
| penalty-1@16384 | `mag+santung` | OK | 2 |
| penalty-2@6080 | `mag+san+tung` |  | 3 |
| penalty-2@8192 | `mag+santung` | OK | 2 |
| penalty-2@16384 | `mag+santung` | OK | 2 |
| penalty-4@6080 | `mag+san+tung` |  | 3 |
| penalty-4@8192 | `mag+santung` | OK | 2 |
| penalty-4@16384 | `mag+santung` | OK | 2 |
| penalty-8@6080 | `mag+santung` | OK | 2 |
| penalty-8@8192 | `mag+santung` | OK | 2 |
| penalty-8@16384 | `mag+santung` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+san+tung` |  | 3 |
| stochastic-p4-d0.1@8192 | `mag+san+tung` |  | 3 |
| stochastic-p4-d0.1@16384 | `mag+santung` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mag+san+tung` |  | 3 |
| stochastic-p4-d0.2@8192 | `mag+santung` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mag+santung` | OK | 2 |
| unigram-ablation@6080 | `mag+santung` | OK | 2 |

## `makananung`  (prefixation, tier B_moderate_silver)

**silver gold:** `maka+nanung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makananung` |  | 1 |
| plain@8192 | `makananung` |  | 1 |
| plain@16384 | `makananung` |  | 1 |
| morphbpe@6080 | `makananung` |  | 1 |
| morphbpe@8192 | `makananung` |  | 1 |
| morphbpe@16384 | `makananung` |  | 1 |
| penalty-1@6080 | `makananung` |  | 1 |
| penalty-1@8192 | `makananung` |  | 1 |
| penalty-1@16384 | `makananung` |  | 1 |
| penalty-2@6080 | `makananung` |  | 1 |
| penalty-2@8192 | `makananung` |  | 1 |
| penalty-2@16384 | `makananung` |  | 1 |
| penalty-4@6080 | `makananung` |  | 1 |
| penalty-4@8192 | `makananung` |  | 1 |
| penalty-4@16384 | `makananung` |  | 1 |
| penalty-8@6080 | `makananung` |  | 1 |
| penalty-8@8192 | `makananung` |  | 1 |
| penalty-8@16384 | `makananung` |  | 1 |
| stochastic-p4-d0.1@6080 | `makananung` |  | 1 |
| stochastic-p4-d0.1@8192 | `makananung` |  | 1 |
| stochastic-p4-d0.1@16384 | `makananung` |  | 1 |
| stochastic-p4-d0.2@6080 | `makananung` |  | 1 |
| stochastic-p4-d0.2@8192 | `makananung` |  | 1 |
| stochastic-p4-d0.2@16384 | `makananung` |  | 1 |
| unigram-ablation@6080 | `makananu+ng` |  | 2 |

## `matudtud`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+tudtud`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `matudtud` |  | 1 |
| plain@8192 | `matudtud` |  | 1 |
| plain@16384 | `matudtud` |  | 1 |
| morphbpe@6080 | `matudtud` |  | 1 |
| morphbpe@8192 | `matudtud` |  | 1 |
| morphbpe@16384 | `matudtud` |  | 1 |
| penalty-1@6080 | `matudtud` |  | 1 |
| penalty-1@8192 | `matudtud` |  | 1 |
| penalty-1@16384 | `matudtud` |  | 1 |
| penalty-2@6080 | `matudtud` |  | 1 |
| penalty-2@8192 | `matudtud` |  | 1 |
| penalty-2@16384 | `matudtud` |  | 1 |
| penalty-4@6080 | `matudtud` |  | 1 |
| penalty-4@8192 | `matudtud` |  | 1 |
| penalty-4@16384 | `matudtud` |  | 1 |
| penalty-8@6080 | `matudtud` |  | 1 |
| penalty-8@8192 | `matudtud` |  | 1 |
| penalty-8@16384 | `matudtud` |  | 1 |
| stochastic-p4-d0.1@6080 | `matudtud` |  | 1 |
| stochastic-p4-d0.1@8192 | `matudtud` |  | 1 |
| stochastic-p4-d0.1@16384 | `matudtud` |  | 1 |
| stochastic-p4-d0.2@6080 | `matudtud` |  | 1 |
| stochastic-p4-d0.2@8192 | `matudtud` |  | 1 |
| stochastic-p4-d0.2@16384 | `matudtud` |  | 1 |
| unigram-ablation@6080 | `matudtu+d` |  | 2 |

## `menibat`  (prefixation, tier A_strong_silver)

**silver gold:** `men+ibat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `menibat` |  | 1 |
| plain@8192 | `menibat` |  | 1 |
| plain@16384 | `menibat` |  | 1 |
| morphbpe@6080 | `men+ibat` | OK | 2 |
| morphbpe@8192 | `men+ibat` | OK | 2 |
| morphbpe@16384 | `men+ibat` | OK | 2 |
| penalty-1@6080 | `men+ibat` | OK | 2 |
| penalty-1@8192 | `men+ibat` | OK | 2 |
| penalty-1@16384 | `men+ibat` | OK | 2 |
| penalty-2@6080 | `men+ibat` | OK | 2 |
| penalty-2@8192 | `men+ibat` | OK | 2 |
| penalty-2@16384 | `men+ibat` | OK | 2 |
| penalty-4@6080 | `men+ibat` | OK | 2 |
| penalty-4@8192 | `men+ibat` | OK | 2 |
| penalty-4@16384 | `men+ibat` | OK | 2 |
| penalty-8@6080 | `men+ibat` | OK | 2 |
| penalty-8@8192 | `men+ibat` | OK | 2 |
| penalty-8@16384 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.1@6080 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.1@8192 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.1@16384 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.2@6080 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.2@8192 | `men+ibat` | OK | 2 |
| stochastic-p4-d0.2@16384 | `men+ibat` | OK | 2 |
| unigram-ablation@6080 | `menibat` |  | 1 |

## `magdala`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+dala`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `magdala` |  | 1 |
| plain@8192 | `magdala` |  | 1 |
| plain@16384 | `magdala` |  | 1 |
| morphbpe@6080 | `magdala` |  | 1 |
| morphbpe@8192 | `magdala` |  | 1 |
| morphbpe@16384 | `magdala` |  | 1 |
| penalty-1@6080 | `magdala` |  | 1 |
| penalty-1@8192 | `magdala` |  | 1 |
| penalty-1@16384 | `magdala` |  | 1 |
| penalty-2@6080 | `magdala` |  | 1 |
| penalty-2@8192 | `magdala` |  | 1 |
| penalty-2@16384 | `magdala` |  | 1 |
| penalty-4@6080 | `magdala` |  | 1 |
| penalty-4@8192 | `magdala` |  | 1 |
| penalty-4@16384 | `magdala` |  | 1 |
| penalty-8@6080 | `magdala` |  | 1 |
| penalty-8@8192 | `magdala` |  | 1 |
| penalty-8@16384 | `magdala` |  | 1 |
| stochastic-p4-d0.1@6080 | `magdala` |  | 1 |
| stochastic-p4-d0.1@8192 | `magdala` |  | 1 |
| stochastic-p4-d0.1@16384 | `magdala` |  | 1 |
| stochastic-p4-d0.2@6080 | `magdala` |  | 1 |
| stochastic-p4-d0.2@8192 | `magdala` |  | 1 |
| stochastic-p4-d0.2@16384 | `magdala` |  | 1 |
| unigram-ablation@6080 | `magdala` |  | 1 |

## `malinis`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+linis`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malinis` |  | 1 |
| plain@8192 | `malinis` |  | 1 |
| plain@16384 | `malinis` |  | 1 |
| morphbpe@6080 | `mal+inis` |  | 2 |
| morphbpe@8192 | `mal+inis` |  | 2 |
| morphbpe@16384 | `mal+inis` |  | 2 |
| penalty-1@6080 | `mal+inis` |  | 2 |
| penalty-1@8192 | `mal+inis` |  | 2 |
| penalty-1@16384 | `mal+inis` |  | 2 |
| penalty-2@6080 | `mal+inis` |  | 2 |
| penalty-2@8192 | `mal+inis` |  | 2 |
| penalty-2@16384 | `mal+inis` |  | 2 |
| penalty-4@6080 | `mal+inis` |  | 2 |
| penalty-4@8192 | `mal+inis` |  | 2 |
| penalty-4@16384 | `mal+inis` |  | 2 |
| penalty-8@6080 | `mal+inis` |  | 2 |
| penalty-8@8192 | `mal+inis` |  | 2 |
| penalty-8@16384 | `mal+inis` |  | 2 |
| stochastic-p4-d0.1@6080 | `mal+inis` |  | 2 |
| stochastic-p4-d0.1@8192 | `mal+inis` |  | 2 |
| stochastic-p4-d0.1@16384 | `mal+inis` |  | 2 |
| stochastic-p4-d0.2@6080 | `mal+inis` |  | 2 |
| stochastic-p4-d0.2@8192 | `mal+inis` |  | 2 |
| stochastic-p4-d0.2@16384 | `mal+inis` |  | 2 |
| unigram-ablation@6080 | `ma+linis` | OK | 2 |

## `pilinan`  (prefixation, tier B_moderate_silver)

**silver gold:** `pi+linan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pil+inan` |  | 2 |
| plain@8192 | `pil+inan` |  | 2 |
| plain@16384 | `pilinan` |  | 1 |
| morphbpe@6080 | `pil+inan` |  | 2 |
| morphbpe@8192 | `pil+inan` |  | 2 |
| morphbpe@16384 | `pilinan` |  | 1 |
| penalty-1@6080 | `pil+inan` |  | 2 |
| penalty-1@8192 | `pil+inan` |  | 2 |
| penalty-1@16384 | `pilinan` |  | 1 |
| penalty-2@6080 | `pil+in+an` |  | 3 |
| penalty-2@8192 | `pil+in+an` |  | 3 |
| penalty-2@16384 | `pilinan` |  | 1 |
| penalty-4@6080 | `pil+in+an` |  | 3 |
| penalty-4@8192 | `pil+in+an` |  | 3 |
| penalty-4@16384 | `pilinan` |  | 1 |
| penalty-8@6080 | `pil+in+an` |  | 3 |
| penalty-8@8192 | `pil+in+an` |  | 3 |
| penalty-8@16384 | `pilinan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pil+in+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `pil+in+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `pilinan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pil+in+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `pil+in+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `pilinan` |  | 1 |
| unigram-ablation@6080 | `pi+lin+an` |  | 3 |

## `maluka`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+luka`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malu+ka` |  | 2 |
| plain@8192 | `maluka` |  | 1 |
| plain@16384 | `maluka` |  | 1 |
| morphbpe@6080 | `malu+ka` |  | 2 |
| morphbpe@8192 | `maluka` |  | 1 |
| morphbpe@16384 | `maluka` |  | 1 |
| penalty-1@6080 | `malu+ka` |  | 2 |
| penalty-1@8192 | `maluka` |  | 1 |
| penalty-1@16384 | `maluka` |  | 1 |
| penalty-2@6080 | `malu+ka` |  | 2 |
| penalty-2@8192 | `maluka` |  | 1 |
| penalty-2@16384 | `maluka` |  | 1 |
| penalty-4@6080 | `malu+ka` |  | 2 |
| penalty-4@8192 | `maluka` |  | 1 |
| penalty-4@16384 | `maluka` |  | 1 |
| penalty-8@6080 | `malu+ka` |  | 2 |
| penalty-8@8192 | `maluka` |  | 1 |
| penalty-8@16384 | `maluka` |  | 1 |
| stochastic-p4-d0.1@6080 | `malu+ka` |  | 2 |
| stochastic-p4-d0.1@8192 | `maluka` |  | 1 |
| stochastic-p4-d0.1@16384 | `maluka` |  | 1 |
| stochastic-p4-d0.2@6080 | `mal+uka` |  | 2 |
| stochastic-p4-d0.2@8192 | `maluka` |  | 1 |
| stochastic-p4-d0.2@16384 | `maluka` |  | 1 |
| unigram-ablation@6080 | `maluka` |  | 1 |

## `masaya`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+saya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masaya` |  | 1 |
| plain@8192 | `masaya` |  | 1 |
| plain@16384 | `masaya` |  | 1 |
| morphbpe@6080 | `masaya` |  | 1 |
| morphbpe@8192 | `masaya` |  | 1 |
| morphbpe@16384 | `masaya` |  | 1 |
| penalty-1@6080 | `masaya` |  | 1 |
| penalty-1@8192 | `masaya` |  | 1 |
| penalty-1@16384 | `masaya` |  | 1 |
| penalty-2@6080 | `masaya` |  | 1 |
| penalty-2@8192 | `masaya` |  | 1 |
| penalty-2@16384 | `masaya` |  | 1 |
| penalty-4@6080 | `ma+sa+ya` |  | 3 |
| penalty-4@8192 | `masaya` |  | 1 |
| penalty-4@16384 | `masaya` |  | 1 |
| penalty-8@6080 | `masaya` |  | 1 |
| penalty-8@8192 | `masaya` |  | 1 |
| penalty-8@16384 | `masaya` |  | 1 |
| stochastic-p4-d0.1@6080 | `masaya` |  | 1 |
| stochastic-p4-d0.1@8192 | `masaya` |  | 1 |
| stochastic-p4-d0.1@16384 | `masaya` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+sa+ya` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+sa+ya` |  | 3 |
| stochastic-p4-d0.2@16384 | `masaya` |  | 1 |
| unigram-ablation@6080 | `masaya` |  | 1 |

## `paburen`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+buren`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paburen` |  | 1 |
| plain@8192 | `paburen` |  | 1 |
| plain@16384 | `paburen` |  | 1 |
| morphbpe@6080 | `paburen` |  | 1 |
| morphbpe@8192 | `paburen` |  | 1 |
| morphbpe@16384 | `paburen` |  | 1 |
| penalty-1@6080 | `paburen` |  | 1 |
| penalty-1@8192 | `paburen` |  | 1 |
| penalty-1@16384 | `paburen` |  | 1 |
| penalty-2@6080 | `paburen` |  | 1 |
| penalty-2@8192 | `paburen` |  | 1 |
| penalty-2@16384 | `paburen` |  | 1 |
| penalty-4@6080 | `paburen` |  | 1 |
| penalty-4@8192 | `paburen` |  | 1 |
| penalty-4@16384 | `paburen` |  | 1 |
| penalty-8@6080 | `paburen` |  | 1 |
| penalty-8@8192 | `paburen` |  | 1 |
| penalty-8@16384 | `paburen` |  | 1 |
| stochastic-p4-d0.1@6080 | `paburen` |  | 1 |
| stochastic-p4-d0.1@8192 | `paburen` |  | 1 |
| stochastic-p4-d0.1@16384 | `paburen` |  | 1 |
| stochastic-p4-d0.2@6080 | `paburen` |  | 1 |
| stochastic-p4-d0.2@8192 | `paburen` |  | 1 |
| stochastic-p4-d0.2@16384 | `paburen` |  | 1 |
| unigram-ablation@6080 | `paburen` |  | 1 |

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

## `maranun`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+ranun`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mar+anun` |  | 2 |
| plain@8192 | `maranun` |  | 1 |
| plain@16384 | `maranun` |  | 1 |
| morphbpe@6080 | `mar+an+un` |  | 3 |
| morphbpe@8192 | `mar+an+un` |  | 3 |
| morphbpe@16384 | `mar+an+un` |  | 3 |
| penalty-1@6080 | `ma+ranun` | OK | 2 |
| penalty-1@8192 | `ma+ranun` | OK | 2 |
| penalty-1@16384 | `ma+ranun` | OK | 2 |
| penalty-2@6080 | `ma+ranun` | OK | 2 |
| penalty-2@8192 | `ma+ranun` | OK | 2 |
| penalty-2@16384 | `ma+ranun` | OK | 2 |
| penalty-4@6080 | `ma+ranun` | OK | 2 |
| penalty-4@8192 | `ma+ranun` | OK | 2 |
| penalty-4@16384 | `ma+ranun` | OK | 2 |
| penalty-8@6080 | `ma+ranun` | OK | 2 |
| penalty-8@8192 | `ma+ranun` | OK | 2 |
| penalty-8@16384 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+ranun` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+ranun` | OK | 2 |
| unigram-ablation@6080 | `maranun` |  | 1 |

## `mawala`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+wala`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ma+wala` | OK | 2 |
| plain@8192 | `mawala` |  | 1 |
| plain@16384 | `mawala` |  | 1 |
| morphbpe@6080 | `ma+wala` | OK | 2 |
| morphbpe@8192 | `mawala` |  | 1 |
| morphbpe@16384 | `mawala` |  | 1 |
| penalty-1@6080 | `ma+wala` | OK | 2 |
| penalty-1@8192 | `mawala` |  | 1 |
| penalty-1@16384 | `mawala` |  | 1 |
| penalty-2@6080 | `ma+wala` | OK | 2 |
| penalty-2@8192 | `mawala` |  | 1 |
| penalty-2@16384 | `mawala` |  | 1 |
| penalty-4@6080 | `ma+wala` | OK | 2 |
| penalty-4@8192 | `mawala` |  | 1 |
| penalty-4@16384 | `mawala` |  | 1 |
| penalty-8@6080 | `ma+wala` | OK | 2 |
| penalty-8@8192 | `mawala` |  | 1 |
| penalty-8@16384 | `mawala` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+wala` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mawala` |  | 1 |
| stochastic-p4-d0.1@16384 | `mawala` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+wala` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mawala` |  | 1 |
| stochastic-p4-d0.2@16384 | `mawala` |  | 1 |
| unigram-ablation@6080 | `ma+wala` | OK | 2 |

## `panayan`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `panaya+n`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+ayan` |  | 2 |
| plain@8192 | `panayan` |  | 1 |
| plain@16384 | `panayan` |  | 1 |
| morphbpe@6080 | `panayan` |  | 1 |
| morphbpe@8192 | `panayan` |  | 1 |
| morphbpe@16384 | `panayan` |  | 1 |
| penalty-1@6080 | `panayan` |  | 1 |
| penalty-1@8192 | `panayan` |  | 1 |
| penalty-1@16384 | `panayan` |  | 1 |
| penalty-2@6080 | `panayan` |  | 1 |
| penalty-2@8192 | `panayan` |  | 1 |
| penalty-2@16384 | `panayan` |  | 1 |
| penalty-4@6080 | `panayan` |  | 1 |
| penalty-4@8192 | `panayan` |  | 1 |
| penalty-4@16384 | `panayan` |  | 1 |
| penalty-8@6080 | `panayan` |  | 1 |
| penalty-8@8192 | `panayan` |  | 1 |
| penalty-8@16384 | `panayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `panayan` |  | 1 |
| stochastic-p4-d0.1@8192 | `panayan` |  | 1 |
| stochastic-p4-d0.1@16384 | `panayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `panayan` |  | 1 |
| stochastic-p4-d0.2@8192 | `panayan` |  | 1 |
| stochastic-p4-d0.2@16384 | `panayan` |  | 1 |
| unigram-ablation@6080 | `panayan` |  | 1 |

## `pilatan`  (prefixation, tier B_moderate_silver)

**silver gold:** `pi+latan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pilatan` |  | 1 |
| plain@8192 | `pilatan` |  | 1 |
| plain@16384 | `pilatan` |  | 1 |
| morphbpe@6080 | `pilatan` |  | 1 |
| morphbpe@8192 | `pilatan` |  | 1 |
| morphbpe@16384 | `pilatan` |  | 1 |
| penalty-1@6080 | `pilatan` |  | 1 |
| penalty-1@8192 | `pilatan` |  | 1 |
| penalty-1@16384 | `pilatan` |  | 1 |
| penalty-2@6080 | `pilatan` |  | 1 |
| penalty-2@8192 | `pilatan` |  | 1 |
| penalty-2@16384 | `pilatan` |  | 1 |
| penalty-4@6080 | `pilatan` |  | 1 |
| penalty-4@8192 | `pilatan` |  | 1 |
| penalty-4@16384 | `pilatan` |  | 1 |
| penalty-8@6080 | `pilatan` |  | 1 |
| penalty-8@8192 | `pilatan` |  | 1 |
| penalty-8@16384 | `pilatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pilatan` |  | 1 |
| stochastic-p4-d0.1@8192 | `pilatan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pilatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pilatan` |  | 1 |
| stochastic-p4-d0.2@8192 | `pilatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `pilatan` |  | 1 |
| unigram-ablation@6080 | `pilatan` |  | 1 |

## `malati`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lati`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malati` |  | 1 |
| plain@8192 | `malati` |  | 1 |
| plain@16384 | `malati` |  | 1 |
| morphbpe@6080 | `malati` |  | 1 |
| morphbpe@8192 | `malati` |  | 1 |
| morphbpe@16384 | `malati` |  | 1 |
| penalty-1@6080 | `malati` |  | 1 |
| penalty-1@8192 | `malati` |  | 1 |
| penalty-1@16384 | `malati` |  | 1 |
| penalty-2@6080 | `malati` |  | 1 |
| penalty-2@8192 | `malati` |  | 1 |
| penalty-2@16384 | `malati` |  | 1 |
| penalty-4@6080 | `malati` |  | 1 |
| penalty-4@8192 | `malati` |  | 1 |
| penalty-4@16384 | `malati` |  | 1 |
| penalty-8@6080 | `malati` |  | 1 |
| penalty-8@8192 | `malati` |  | 1 |
| penalty-8@16384 | `malati` |  | 1 |
| stochastic-p4-d0.1@6080 | `malati` |  | 1 |
| stochastic-p4-d0.1@8192 | `malati` |  | 1 |
| stochastic-p4-d0.1@16384 | `malati` |  | 1 |
| stochastic-p4-d0.2@6080 | `malati` |  | 1 |
| stochastic-p4-d0.2@8192 | `malati` |  | 1 |
| stochastic-p4-d0.2@16384 | `malati` |  | 1 |
| unigram-ablation@6080 | `malati` |  | 1 |

## `mayupaya`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+yupaya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mayu+paya` |  | 2 |
| plain@8192 | `mayupaya` |  | 1 |
| plain@16384 | `mayupaya` |  | 1 |
| morphbpe@6080 | `mayu+paya` |  | 2 |
| morphbpe@8192 | `mayupaya` |  | 1 |
| morphbpe@16384 | `mayupaya` |  | 1 |
| penalty-1@6080 | `mayu+paya` |  | 2 |
| penalty-1@8192 | `mayupaya` |  | 1 |
| penalty-1@16384 | `mayupaya` |  | 1 |
| penalty-2@6080 | `mayu+paya` |  | 2 |
| penalty-2@8192 | `mayupaya` |  | 1 |
| penalty-2@16384 | `mayupaya` |  | 1 |
| penalty-4@6080 | `mayu+paya` |  | 2 |
| penalty-4@8192 | `mayupaya` |  | 1 |
| penalty-4@16384 | `mayupaya` |  | 1 |
| penalty-8@6080 | `ma+yupaya` | OK | 2 |
| penalty-8@8192 | `mayupaya` |  | 1 |
| penalty-8@16384 | `mayupaya` |  | 1 |
| stochastic-p4-d0.1@6080 | `mayu+pa+ya` |  | 3 |
| stochastic-p4-d0.1@8192 | `mayupaya` |  | 1 |
| stochastic-p4-d0.1@16384 | `mayupaya` |  | 1 |
| stochastic-p4-d0.2@6080 | `mayu+paya` |  | 2 |
| stochastic-p4-d0.2@8192 | `mayupaya` |  | 1 |
| stochastic-p4-d0.2@16384 | `mayupaya` |  | 1 |
| unigram-ablation@6080 | `mayupaya` |  | 1 |

## `makapagmulalang`  (prefixation, tier B_moderate_silver)

**silver gold:** `makapag+mulalang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makapag+mul+alang` |  | 3 |
| plain@8192 | `makapag+mulalang` | OK | 2 |
| plain@16384 | `makapagmulalang` |  | 1 |
| morphbpe@6080 | `makapag+mul+alang` |  | 3 |
| morphbpe@8192 | `makapag+mulalang` | OK | 2 |
| morphbpe@16384 | `makapagmulalang` |  | 1 |
| penalty-1@6080 | `makapag+mul+alang` |  | 3 |
| penalty-1@8192 | `makapag+mulalang` | OK | 2 |
| penalty-1@16384 | `makapagmulalang` |  | 1 |
| penalty-2@6080 | `makapag+mul+alang` |  | 3 |
| penalty-2@8192 | `makapag+mulalang` | OK | 2 |
| penalty-2@16384 | `makapagmulalang` |  | 1 |
| penalty-4@6080 | `makapag+mul+alang` |  | 3 |
| penalty-4@8192 | `makapag+mulalang` | OK | 2 |
| penalty-4@16384 | `makapagmulalang` |  | 1 |
| penalty-8@6080 | `makapag+mu+lalang` |  | 3 |
| penalty-8@8192 | `makapag+mulalang` | OK | 2 |
| penalty-8@16384 | `makapagmulalang` |  | 1 |
| stochastic-p4-d0.1@6080 | `makapag+mu+lalang` |  | 3 |
| stochastic-p4-d0.1@8192 | `makapag+mulalang` | OK | 2 |
| stochastic-p4-d0.1@16384 | `makapagmulalang` |  | 1 |
| stochastic-p4-d0.2@6080 | `makapag+mu+lalang` |  | 3 |
| stochastic-p4-d0.2@8192 | `makapag+mu+lalang` |  | 3 |
| stochastic-p4-d0.2@16384 | `makapagmulalang` |  | 1 |
| unigram-ablation@6080 | `makapagmulala+ng` |  | 2 |

## `makipamuk`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+kipamuk`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mak+ipam+uk` |  | 3 |
| plain@8192 | `mak+ipamuk` |  | 2 |
| plain@16384 | `makipamuk` |  | 1 |
| morphbpe@6080 | `maki+pamuk` |  | 2 |
| morphbpe@8192 | `maki+pamuk` |  | 2 |
| morphbpe@16384 | `makipamuk` |  | 1 |
| penalty-1@6080 | `maki+pam+uk` |  | 3 |
| penalty-1@8192 | `maki+pamuk` |  | 2 |
| penalty-1@16384 | `makipamuk` |  | 1 |
| penalty-2@6080 | `maki+pam+uk` |  | 3 |
| penalty-2@8192 | `maki+pamuk` |  | 2 |
| penalty-2@16384 | `makipamuk` |  | 1 |
| penalty-4@6080 | `maki+pam+uk` |  | 3 |
| penalty-4@8192 | `maki+pam+uk` |  | 3 |
| penalty-4@16384 | `makipamuk` |  | 1 |
| penalty-8@6080 | `maki+pam+uk` |  | 3 |
| penalty-8@8192 | `maki+pam+uk` |  | 3 |
| penalty-8@16384 | `makipamuk` |  | 1 |
| stochastic-p4-d0.1@6080 | `maki+pam+uk` |  | 3 |
| stochastic-p4-d0.1@8192 | `maki+pam+uk` |  | 3 |
| stochastic-p4-d0.1@16384 | `makipamuk` |  | 1 |
| stochastic-p4-d0.2@6080 | `maki+pam+uk` |  | 3 |
| stochastic-p4-d0.2@8192 | `maki+pam+uk` |  | 3 |
| stochastic-p4-d0.2@16384 | `makipamuk` |  | 1 |
| unigram-ablation@6080 | `ma+kipamuk` | OK | 2 |

## `pangisnawa`  (prefixation, tier B_moderate_silver)

**silver gold:** `pang+isnawa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pang+isnawa` | OK | 2 |
| plain@8192 | `pang+isnawa` | OK | 2 |
| plain@16384 | `pangisnawa` |  | 1 |
| morphbpe@6080 | `pang+isnawa` | OK | 2 |
| morphbpe@8192 | `pang+isnawa` | OK | 2 |
| morphbpe@16384 | `pangisnawa` |  | 1 |
| penalty-1@6080 | `pang+isnawa` | OK | 2 |
| penalty-1@8192 | `pang+isnawa` | OK | 2 |
| penalty-1@16384 | `pangisnawa` |  | 1 |
| penalty-2@6080 | `pang+isnawa` | OK | 2 |
| penalty-2@8192 | `pang+isnawa` | OK | 2 |
| penalty-2@16384 | `pangisnawa` |  | 1 |
| penalty-4@6080 | `pang+isnawa` | OK | 2 |
| penalty-4@8192 | `pang+isnawa` | OK | 2 |
| penalty-4@16384 | `pangisnawa` |  | 1 |
| penalty-8@6080 | `pang+isnawa` | OK | 2 |
| penalty-8@8192 | `pang+isnawa` | OK | 2 |
| penalty-8@16384 | `pangisnawa` |  | 1 |
| stochastic-p4-d0.1@6080 | `pang+is+nawa` |  | 3 |
| stochastic-p4-d0.1@8192 | `pangis+nawa` |  | 2 |
| stochastic-p4-d0.1@16384 | `pangisnawa` |  | 1 |
| stochastic-p4-d0.2@6080 | `pang+is+nawa` |  | 3 |
| stochastic-p4-d0.2@8192 | `pang+is+nawa` |  | 3 |
| stochastic-p4-d0.2@16384 | `pangisnawa` |  | 1 |
| unigram-ablation@6080 | `pangisnawa` |  | 1 |

## `panlalawe`  (prefixation, tier B_moderate_silver)

**silver gold:** `pan+lalawe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+lalawe` | OK | 2 |
| plain@8192 | `pan+lalawe` | OK | 2 |
| plain@16384 | `panlalawe` |  | 1 |
| morphbpe@6080 | `pan+lalawe` | OK | 2 |
| morphbpe@8192 | `pan+lalawe` | OK | 2 |
| morphbpe@16384 | `panlalawe` |  | 1 |
| penalty-1@6080 | `pan+lalawe` | OK | 2 |
| penalty-1@8192 | `pan+lalawe` | OK | 2 |
| penalty-1@16384 | `panlalawe` |  | 1 |
| penalty-2@6080 | `pan+lalawe` | OK | 2 |
| penalty-2@8192 | `pan+lalawe` | OK | 2 |
| penalty-2@16384 | `panlalawe` |  | 1 |
| penalty-4@6080 | `pan+lalawe` | OK | 2 |
| penalty-4@8192 | `pan+lalawe` | OK | 2 |
| penalty-4@16384 | `panlalawe` |  | 1 |
| penalty-8@6080 | `pan+lalawe` | OK | 2 |
| penalty-8@8192 | `pan+lalawe` | OK | 2 |
| penalty-8@16384 | `panlalawe` |  | 1 |
| stochastic-p4-d0.1@6080 | `pan+lalawe` | OK | 2 |
| stochastic-p4-d0.1@8192 | `pan+lalawe` | OK | 2 |
| stochastic-p4-d0.1@16384 | `panlalawe` |  | 1 |
| stochastic-p4-d0.2@6080 | `p+an+lalawe` |  | 3 |
| stochastic-p4-d0.2@8192 | `p+an+lalawe` |  | 3 |
| stochastic-p4-d0.2@16384 | `panlalawe` |  | 1 |
| unigram-ablation@6080 | `pan+la+lawe` |  | 3 |

## `makalukluk`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+lukluk`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makalukluk` |  | 1 |
| plain@8192 | `makalukluk` |  | 1 |
| plain@16384 | `makalukluk` |  | 1 |
| morphbpe@6080 | `makal+ukluk` |  | 2 |
| morphbpe@8192 | `makal+ukluk` |  | 2 |
| morphbpe@16384 | `makal+ukluk` |  | 2 |
| penalty-1@6080 | `makal+ukluk` |  | 2 |
| penalty-1@8192 | `makal+ukluk` |  | 2 |
| penalty-1@16384 | `makal+ukluk` |  | 2 |
| penalty-2@6080 | `makal+ukluk` |  | 2 |
| penalty-2@8192 | `makal+ukluk` |  | 2 |
| penalty-2@16384 | `makal+ukluk` |  | 2 |
| penalty-4@6080 | `makal+ukluk` |  | 2 |
| penalty-4@8192 | `makal+ukluk` |  | 2 |
| penalty-4@16384 | `makal+ukluk` |  | 2 |
| penalty-8@6080 | `maka+lukluk` | OK | 2 |
| penalty-8@8192 | `maka+lukluk` | OK | 2 |
| penalty-8@16384 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+lukluk` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+lukluk` | OK | 2 |
| unigram-ablation@6080 | `maka+lukluk` | OK | 2 |

## `manases`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+ases`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+as+es` |  | 3 |
| plain@8192 | `man+as+es` |  | 3 |
| plain@16384 | `man+ases` | OK | 2 |
| morphbpe@6080 | `man+as+es` |  | 3 |
| morphbpe@8192 | `man+as+es` |  | 3 |
| morphbpe@16384 | `man+ases` | OK | 2 |
| penalty-1@6080 | `man+as+es` |  | 3 |
| penalty-1@8192 | `man+as+es` |  | 3 |
| penalty-1@16384 | `man+ases` | OK | 2 |
| penalty-2@6080 | `man+as+es` |  | 3 |
| penalty-2@8192 | `man+as+es` |  | 3 |
| penalty-2@16384 | `man+ases` | OK | 2 |
| penalty-4@6080 | `man+as+es` |  | 3 |
| penalty-4@8192 | `man+as+es` |  | 3 |
| penalty-4@16384 | `man+ases` | OK | 2 |
| penalty-8@6080 | `man+as+es` |  | 3 |
| penalty-8@8192 | `man+as+es` |  | 3 |
| penalty-8@16384 | `man+ases` | OK | 2 |
| stochastic-p4-d0.1@6080 | `man+as+es` |  | 3 |
| stochastic-p4-d0.1@8192 | `man+as+es` |  | 3 |
| stochastic-p4-d0.1@16384 | `man+ases` | OK | 2 |
| stochastic-p4-d0.2@6080 | `man+as+es` |  | 3 |
| stochastic-p4-d0.2@8192 | `man+as+es` |  | 3 |
| stochastic-p4-d0.2@16384 | `man+as+es` |  | 3 |
| unigram-ablation@6080 | `man+as+es` |  | 3 |

## `masampat`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+sampat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ampat` |  | 2 |
| plain@8192 | `masampat` |  | 1 |
| plain@16384 | `masampat` |  | 1 |
| morphbpe@6080 | `mas+ampat` |  | 2 |
| morphbpe@8192 | `masampat` |  | 1 |
| morphbpe@16384 | `masampat` |  | 1 |
| penalty-1@6080 | `mas+ampat` |  | 2 |
| penalty-1@8192 | `masampat` |  | 1 |
| penalty-1@16384 | `masampat` |  | 1 |
| penalty-2@6080 | `mas+ampat` |  | 2 |
| penalty-2@8192 | `masampat` |  | 1 |
| penalty-2@16384 | `masampat` |  | 1 |
| penalty-4@6080 | `mas+ampat` |  | 2 |
| penalty-4@8192 | `masampat` |  | 1 |
| penalty-4@16384 | `masampat` |  | 1 |
| penalty-8@6080 | `mas+ampat` |  | 2 |
| penalty-8@8192 | `masampat` |  | 1 |
| penalty-8@16384 | `masampat` |  | 1 |
| stochastic-p4-d0.1@6080 | `mas+am+pat` |  | 3 |
| stochastic-p4-d0.1@8192 | `masampat` |  | 1 |
| stochastic-p4-d0.1@16384 | `masampat` |  | 1 |
| stochastic-p4-d0.2@6080 | `mas+ampat` |  | 2 |
| stochastic-p4-d0.2@8192 | `masampat` |  | 1 |
| stochastic-p4-d0.2@16384 | `masampat` |  | 1 |
| unigram-ablation@6080 | `mas+amp+at` |  | 3 |

## `masayang`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+sayang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ayang` |  | 2 |
| plain@8192 | `masayang` |  | 1 |
| plain@16384 | `masayang` |  | 1 |
| morphbpe@6080 | `mas+a+yang` |  | 3 |
| morphbpe@8192 | `mas+ayang` |  | 2 |
| morphbpe@16384 | `mas+ayang` |  | 2 |
| penalty-1@6080 | `ma+sayang` | OK | 2 |
| penalty-1@8192 | `ma+sayang` | OK | 2 |
| penalty-1@16384 | `ma+sayang` | OK | 2 |
| penalty-2@6080 | `ma+sayang` | OK | 2 |
| penalty-2@8192 | `ma+sayang` | OK | 2 |
| penalty-2@16384 | `ma+sayang` | OK | 2 |
| penalty-4@6080 | `ma+sayang` | OK | 2 |
| penalty-4@8192 | `ma+sayang` | OK | 2 |
| penalty-4@16384 | `ma+sayang` | OK | 2 |
| penalty-8@6080 | `ma+sayang` | OK | 2 |
| penalty-8@8192 | `ma+sayang` | OK | 2 |
| penalty-8@16384 | `ma+sayang` | OK | 2 |
| stochastic-p4-d0.1@6080 | `masa+yang` |  | 2 |
| stochastic-p4-d0.1@8192 | `masa+yang` |  | 2 |
| stochastic-p4-d0.1@16384 | `masa+yang` |  | 2 |
| stochastic-p4-d0.2@6080 | `ma+sayang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+sayang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+sayang` | OK | 2 |
| unigram-ablation@6080 | `masaya+ng` |  | 2 |

## `magligtas`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+ligtas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+ligtas` | OK | 2 |
| plain@8192 | `mag+ligtas` | OK | 2 |
| plain@16384 | `magligtas` |  | 1 |
| morphbpe@6080 | `mag+ligtas` | OK | 2 |
| morphbpe@8192 | `mag+ligtas` | OK | 2 |
| morphbpe@16384 | `mag+ligtas` | OK | 2 |
| penalty-1@6080 | `mag+ligtas` | OK | 2 |
| penalty-1@8192 | `mag+ligtas` | OK | 2 |
| penalty-1@16384 | `mag+ligtas` | OK | 2 |
| penalty-2@6080 | `mag+ligtas` | OK | 2 |
| penalty-2@8192 | `mag+ligtas` | OK | 2 |
| penalty-2@16384 | `mag+ligtas` | OK | 2 |
| penalty-4@6080 | `mag+ligtas` | OK | 2 |
| penalty-4@8192 | `mag+ligtas` | OK | 2 |
| penalty-4@16384 | `mag+ligtas` | OK | 2 |
| penalty-8@6080 | `mag+ligtas` | OK | 2 |
| penalty-8@8192 | `mag+ligtas` | OK | 2 |
| penalty-8@16384 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mag+ligtas` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mag+ligtas` | OK | 2 |
| unigram-ablation@6080 | `mag+ligtas` | OK | 2 |

## `matuang`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+tuang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `matuang` |  | 1 |
| plain@8192 | `matuang` |  | 1 |
| plain@16384 | `matuang` |  | 1 |
| morphbpe@6080 | `matuang` |  | 1 |
| morphbpe@8192 | `matuang` |  | 1 |
| morphbpe@16384 | `matuang` |  | 1 |
| penalty-1@6080 | `matuang` |  | 1 |
| penalty-1@8192 | `matuang` |  | 1 |
| penalty-1@16384 | `matuang` |  | 1 |
| penalty-2@6080 | `matuang` |  | 1 |
| penalty-2@8192 | `matuang` |  | 1 |
| penalty-2@16384 | `matuang` |  | 1 |
| penalty-4@6080 | `matuang` |  | 1 |
| penalty-4@8192 | `matuang` |  | 1 |
| penalty-4@16384 | `matuang` |  | 1 |
| penalty-8@6080 | `matuang` |  | 1 |
| penalty-8@8192 | `matuang` |  | 1 |
| penalty-8@16384 | `matuang` |  | 1 |
| stochastic-p4-d0.1@6080 | `matuang` |  | 1 |
| stochastic-p4-d0.1@8192 | `matuang` |  | 1 |
| stochastic-p4-d0.1@16384 | `matuang` |  | 1 |
| stochastic-p4-d0.2@6080 | `matuang` |  | 1 |
| stochastic-p4-d0.2@8192 | `matuang` |  | 1 |
| stochastic-p4-d0.2@16384 | `matuang` |  | 1 |
| unigram-ablation@6080 | `matuang` |  | 1 |

## `pangatau`  (prefixation, tier B_moderate_silver)

**silver gold:** `pang+atau`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pangatau` |  | 1 |
| plain@8192 | `pangatau` |  | 1 |
| plain@16384 | `pangatau` |  | 1 |
| morphbpe@6080 | `pangatau` |  | 1 |
| morphbpe@8192 | `pangatau` |  | 1 |
| morphbpe@16384 | `pangatau` |  | 1 |
| penalty-1@6080 | `pangatau` |  | 1 |
| penalty-1@8192 | `pangatau` |  | 1 |
| penalty-1@16384 | `pangatau` |  | 1 |
| penalty-2@6080 | `pangatau` |  | 1 |
| penalty-2@8192 | `pangatau` |  | 1 |
| penalty-2@16384 | `pangatau` |  | 1 |
| penalty-4@6080 | `pangatau` |  | 1 |
| penalty-4@8192 | `pangatau` |  | 1 |
| penalty-4@16384 | `pangatau` |  | 1 |
| penalty-8@6080 | `pangatau` |  | 1 |
| penalty-8@8192 | `pangatau` |  | 1 |
| penalty-8@16384 | `pangatau` |  | 1 |
| stochastic-p4-d0.1@6080 | `pangatau` |  | 1 |
| stochastic-p4-d0.1@8192 | `pangatau` |  | 1 |
| stochastic-p4-d0.1@16384 | `pangatau` |  | 1 |
| stochastic-p4-d0.2@6080 | `pangatau` |  | 1 |
| stochastic-p4-d0.2@8192 | `pangatau` |  | 1 |
| stochastic-p4-d0.2@16384 | `pangatau` |  | 1 |
| unigram-ablation@6080 | `pangatau` |  | 1 |

## `patugut`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+tugut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `patugut` |  | 1 |
| plain@8192 | `patugut` |  | 1 |
| plain@16384 | `patugut` |  | 1 |
| morphbpe@6080 | `patugut` |  | 1 |
| morphbpe@8192 | `patugut` |  | 1 |
| morphbpe@16384 | `patugut` |  | 1 |
| penalty-1@6080 | `patugut` |  | 1 |
| penalty-1@8192 | `patugut` |  | 1 |
| penalty-1@16384 | `patugut` |  | 1 |
| penalty-2@6080 | `patugut` |  | 1 |
| penalty-2@8192 | `patugut` |  | 1 |
| penalty-2@16384 | `patugut` |  | 1 |
| penalty-4@6080 | `patugut` |  | 1 |
| penalty-4@8192 | `patugut` |  | 1 |
| penalty-4@16384 | `patugut` |  | 1 |
| penalty-8@6080 | `patugut` |  | 1 |
| penalty-8@8192 | `patugut` |  | 1 |
| penalty-8@16384 | `patugut` |  | 1 |
| stochastic-p4-d0.1@6080 | `patugut` |  | 1 |
| stochastic-p4-d0.1@8192 | `patugut` |  | 1 |
| stochastic-p4-d0.1@16384 | `patugut` |  | 1 |
| stochastic-p4-d0.2@6080 | `patugut` |  | 1 |
| stochastic-p4-d0.2@8192 | `patugut` |  | 1 |
| stochastic-p4-d0.2@16384 | `patugut` |  | 1 |
| unigram-ablation@6080 | `patugut` |  | 1 |

## `mabayat`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+bayat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mabayat` |  | 1 |
| plain@8192 | `mabayat` |  | 1 |
| plain@16384 | `mabayat` |  | 1 |
| morphbpe@6080 | `mabayat` |  | 1 |
| morphbpe@8192 | `mabayat` |  | 1 |
| morphbpe@16384 | `mabayat` |  | 1 |
| penalty-1@6080 | `mabayat` |  | 1 |
| penalty-1@8192 | `mabayat` |  | 1 |
| penalty-1@16384 | `mabayat` |  | 1 |
| penalty-2@6080 | `mabayat` |  | 1 |
| penalty-2@8192 | `mabayat` |  | 1 |
| penalty-2@16384 | `mabayat` |  | 1 |
| penalty-4@6080 | `mabayat` |  | 1 |
| penalty-4@8192 | `mabayat` |  | 1 |
| penalty-4@16384 | `mabayat` |  | 1 |
| penalty-8@6080 | `mabayat` |  | 1 |
| penalty-8@8192 | `mabayat` |  | 1 |
| penalty-8@16384 | `mabayat` |  | 1 |
| stochastic-p4-d0.1@6080 | `mabayat` |  | 1 |
| stochastic-p4-d0.1@8192 | `mabayat` |  | 1 |
| stochastic-p4-d0.1@16384 | `mabayat` |  | 1 |
| stochastic-p4-d0.2@6080 | `mabayat` |  | 1 |
| stochastic-p4-d0.2@8192 | `mabayat` |  | 1 |
| stochastic-p4-d0.2@16384 | `mabayat` |  | 1 |
| unigram-ablation@6080 | `mabayat` |  | 1 |

## `malalam`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lalam`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malalam` |  | 1 |
| plain@8192 | `malalam` |  | 1 |
| plain@16384 | `malalam` |  | 1 |
| morphbpe@6080 | `mal+alam` |  | 2 |
| morphbpe@8192 | `mal+alam` |  | 2 |
| morphbpe@16384 | `mal+alam` |  | 2 |
| penalty-1@6080 | `mal+alam` |  | 2 |
| penalty-1@8192 | `mal+alam` |  | 2 |
| penalty-1@16384 | `mal+alam` |  | 2 |
| penalty-2@6080 | `mal+alam` |  | 2 |
| penalty-2@8192 | `mal+alam` |  | 2 |
| penalty-2@16384 | `mal+alam` |  | 2 |
| penalty-4@6080 | `mal+alam` |  | 2 |
| penalty-4@8192 | `mal+alam` |  | 2 |
| penalty-4@16384 | `mal+alam` |  | 2 |
| penalty-8@6080 | `ma+lalam` | OK | 2 |
| penalty-8@8192 | `ma+lalam` | OK | 2 |
| penalty-8@16384 | `ma+lalam` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+lala+m` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+lala+m` |  | 3 |
| stochastic-p4-d0.1@16384 | `malala+m` |  | 2 |
| stochastic-p4-d0.2@6080 | `ma+lalam` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+lalam` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+lalam` | OK | 2 |
| unigram-ablation@6080 | `ma+lalam` | OK | 2 |

## `mapilan`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+pilan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mapilan` |  | 1 |
| plain@8192 | `mapilan` |  | 1 |
| plain@16384 | `mapilan` |  | 1 |
| morphbpe@6080 | `mapilan` |  | 1 |
| morphbpe@8192 | `mapilan` |  | 1 |
| morphbpe@16384 | `mapilan` |  | 1 |
| penalty-1@6080 | `mapilan` |  | 1 |
| penalty-1@8192 | `mapilan` |  | 1 |
| penalty-1@16384 | `mapilan` |  | 1 |
| penalty-2@6080 | `mapilan` |  | 1 |
| penalty-2@8192 | `mapilan` |  | 1 |
| penalty-2@16384 | `mapilan` |  | 1 |
| penalty-4@6080 | `mapilan` |  | 1 |
| penalty-4@8192 | `mapilan` |  | 1 |
| penalty-4@16384 | `mapilan` |  | 1 |
| penalty-8@6080 | `mapilan` |  | 1 |
| penalty-8@8192 | `mapilan` |  | 1 |
| penalty-8@16384 | `mapilan` |  | 1 |
| stochastic-p4-d0.1@6080 | `mapilan` |  | 1 |
| stochastic-p4-d0.1@8192 | `mapilan` |  | 1 |
| stochastic-p4-d0.1@16384 | `mapilan` |  | 1 |
| stochastic-p4-d0.2@6080 | `mapilan` |  | 1 |
| stochastic-p4-d0.2@8192 | `mapilan` |  | 1 |
| stochastic-p4-d0.2@16384 | `mapilan` |  | 1 |
| unigram-ablation@6080 | `mapilan` |  | 1 |

## `pakakalulu`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+kakalulu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paka+kalulu` |  | 2 |
| plain@8192 | `paka+kalulu` |  | 2 |
| plain@16384 | `pakakalulu` |  | 1 |
| morphbpe@6080 | `paka+kal+ulu` |  | 3 |
| morphbpe@8192 | `pakakal+ulu` |  | 2 |
| morphbpe@16384 | `pakakalulu` |  | 1 |
| penalty-1@6080 | `paka+kal+ulu` |  | 3 |
| penalty-1@8192 | `pakakal+ulu` |  | 2 |
| penalty-1@16384 | `pakakalulu` |  | 1 |
| penalty-2@6080 | `paka+kalulu` |  | 2 |
| penalty-2@8192 | `paka+kalulu` |  | 2 |
| penalty-2@16384 | `pakakalulu` |  | 1 |
| penalty-4@6080 | `paka+kalulu` |  | 2 |
| penalty-4@8192 | `paka+kalulu` |  | 2 |
| penalty-4@16384 | `pakakalulu` |  | 1 |
| penalty-8@6080 | `paka+ka+lulu` |  | 3 |
| penalty-8@8192 | `pakaka+lulu` |  | 2 |
| penalty-8@16384 | `pakakalulu` |  | 1 |
| stochastic-p4-d0.1@6080 | `paka+kalulu` |  | 2 |
| stochastic-p4-d0.1@8192 | `paka+kalulu` |  | 2 |
| stochastic-p4-d0.1@16384 | `pakakalulu` |  | 1 |
| stochastic-p4-d0.2@6080 | `paka+ka+lulu` |  | 3 |
| stochastic-p4-d0.2@8192 | `paka+ka+lulu` |  | 3 |
| stochastic-p4-d0.2@16384 | `pakakalulu` |  | 1 |
| unigram-ablation@6080 | `pakakalulu` |  | 1 |

## `panata`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `panata`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+ata` |  | 2 |
| plain@8192 | `pan+ata` |  | 2 |
| plain@16384 | `panata` | OK | 1 |
| morphbpe@6080 | `pan+ata` |  | 2 |
| morphbpe@8192 | `pan+ata` |  | 2 |
| morphbpe@16384 | `pan+ata` |  | 2 |
| penalty-1@6080 | `pan+ata` |  | 2 |
| penalty-1@8192 | `pan+ata` |  | 2 |
| penalty-1@16384 | `pan+ata` |  | 2 |
| penalty-2@6080 | `pan+ata` |  | 2 |
| penalty-2@8192 | `pan+ata` |  | 2 |
| penalty-2@16384 | `pan+ata` |  | 2 |
| penalty-4@6080 | `pan+ata` |  | 2 |
| penalty-4@8192 | `pan+ata` |  | 2 |
| penalty-4@16384 | `pan+ata` |  | 2 |
| penalty-8@6080 | `pan+ata` |  | 2 |
| penalty-8@8192 | `pan+ata` |  | 2 |
| penalty-8@16384 | `pan+ata` |  | 2 |
| stochastic-p4-d0.1@6080 | `pan+ata` |  | 2 |
| stochastic-p4-d0.1@8192 | `pan+ata` |  | 2 |
| stochastic-p4-d0.1@16384 | `pan+ata` |  | 2 |
| stochastic-p4-d0.2@6080 | `p+an+ata` |  | 3 |
| stochastic-p4-d0.2@8192 | `p+an+ata` |  | 3 |
| stochastic-p4-d0.2@16384 | `p+an+ata` |  | 3 |
| unigram-ablation@6080 | `pan+at+a` |  | 3 |

## `pisali`  (prefixation, tier A_strong_silver)

**silver gold:** `pi+sali`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pis+ali` |  | 2 |
| plain@8192 | `pis+ali` |  | 2 |
| plain@16384 | `pisali` |  | 1 |
| morphbpe@6080 | `pis+ali` |  | 2 |
| morphbpe@8192 | `pis+ali` |  | 2 |
| morphbpe@16384 | `pisali` |  | 1 |
| penalty-1@6080 | `pis+ali` |  | 2 |
| penalty-1@8192 | `pisali` |  | 1 |
| penalty-1@16384 | `pisali` |  | 1 |
| penalty-2@6080 | `pis+ali` |  | 2 |
| penalty-2@8192 | `pisali` |  | 1 |
| penalty-2@16384 | `pisali` |  | 1 |
| penalty-4@6080 | `pis+ali` |  | 2 |
| penalty-4@8192 | `pisali` |  | 1 |
| penalty-4@16384 | `pisali` |  | 1 |
| penalty-8@6080 | `pis+ali` |  | 2 |
| penalty-8@8192 | `pisali` |  | 1 |
| penalty-8@16384 | `pisali` |  | 1 |
| stochastic-p4-d0.1@6080 | `pis+ali` |  | 2 |
| stochastic-p4-d0.1@8192 | `pisali` |  | 1 |
| stochastic-p4-d0.1@16384 | `pisali` |  | 1 |
| stochastic-p4-d0.2@6080 | `pis+ali` |  | 2 |
| stochastic-p4-d0.2@8192 | `pis+ali` |  | 2 |
| stochastic-p4-d0.2@16384 | `pisali` |  | 1 |
| unigram-ablation@6080 | `pisali` |  | 1 |

## `makatungkul`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+tungkul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makat+ungkul` |  | 2 |
| plain@8192 | `makat+ungkul` |  | 2 |
| plain@16384 | `makatungkul` |  | 1 |
| morphbpe@6080 | `makat+ungkul` |  | 2 |
| morphbpe@8192 | `makat+ungkul` |  | 2 |
| morphbpe@16384 | `makat+ungkul` |  | 2 |
| penalty-1@6080 | `makat+ungkul` |  | 2 |
| penalty-1@8192 | `makat+ungkul` |  | 2 |
| penalty-1@16384 | `makat+ungkul` |  | 2 |
| penalty-2@6080 | `makat+ungkul` |  | 2 |
| penalty-2@8192 | `makat+ungkul` |  | 2 |
| penalty-2@16384 | `makat+ungkul` |  | 2 |
| penalty-4@6080 | `maka+tungkul` | OK | 2 |
| penalty-4@8192 | `maka+tungkul` | OK | 2 |
| penalty-4@16384 | `maka+tungkul` | OK | 2 |
| penalty-8@6080 | `maka+tungkul` | OK | 2 |
| penalty-8@8192 | `maka+tungkul` | OK | 2 |
| penalty-8@16384 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+tungkul` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+tungkul` | OK | 2 |
| unigram-ablation@6080 | `maka+tungkul` | OK | 2 |

## `mapalyari`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+palyari`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mapal+yari` |  | 2 |
| plain@8192 | `mapalyari` |  | 1 |
| plain@16384 | `mapalyari` |  | 1 |
| morphbpe@6080 | `mapal+yari` |  | 2 |
| morphbpe@8192 | `mapalyari` |  | 1 |
| morphbpe@16384 | `mapalyari` |  | 1 |
| penalty-1@6080 | `mapal+yari` |  | 2 |
| penalty-1@8192 | `mapalyari` |  | 1 |
| penalty-1@16384 | `mapalyari` |  | 1 |
| penalty-2@6080 | `mapal+yari` |  | 2 |
| penalty-2@8192 | `mapalyari` |  | 1 |
| penalty-2@16384 | `mapalyari` |  | 1 |
| penalty-4@6080 | `mapal+yari` |  | 2 |
| penalty-4@8192 | `mapalyari` |  | 1 |
| penalty-4@16384 | `mapalyari` |  | 1 |
| penalty-8@6080 | `mapal+yari` |  | 2 |
| penalty-8@8192 | `mapalyari` |  | 1 |
| penalty-8@16384 | `mapalyari` |  | 1 |
| stochastic-p4-d0.1@6080 | `mapal+yari` |  | 2 |
| stochastic-p4-d0.1@8192 | `mapalyari` |  | 1 |
| stochastic-p4-d0.1@16384 | `mapalyari` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+palyari` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mapalyari` |  | 1 |
| stochastic-p4-d0.2@16384 | `mapalyari` |  | 1 |
| unigram-ablation@6080 | `mapalyari` |  | 1 |

## `panugali`  (prefixation, tier A_strong_silver)

**silver gold:** `pan+ugali`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+ugali` | OK | 2 |
| plain@8192 | `panugali` |  | 1 |
| plain@16384 | `panugali` |  | 1 |
| morphbpe@6080 | `pan+ugali` | OK | 2 |
| morphbpe@8192 | `panugali` |  | 1 |
| morphbpe@16384 | `panugali` |  | 1 |
| penalty-1@6080 | `pan+ugali` | OK | 2 |
| penalty-1@8192 | `panugali` |  | 1 |
| penalty-1@16384 | `panugali` |  | 1 |
| penalty-2@6080 | `pan+ugali` | OK | 2 |
| penalty-2@8192 | `panugali` |  | 1 |
| penalty-2@16384 | `panugali` |  | 1 |
| penalty-4@6080 | `pan+ugali` | OK | 2 |
| penalty-4@8192 | `panugali` |  | 1 |
| penalty-4@16384 | `panugali` |  | 1 |
| penalty-8@6080 | `pan+ugali` | OK | 2 |
| penalty-8@8192 | `panugali` |  | 1 |
| penalty-8@16384 | `panugali` |  | 1 |
| stochastic-p4-d0.1@6080 | `pan+ugali` | OK | 2 |
| stochastic-p4-d0.1@8192 | `panugali` |  | 1 |
| stochastic-p4-d0.1@16384 | `panugali` |  | 1 |
| stochastic-p4-d0.2@6080 | `p+an+ugali` |  | 3 |
| stochastic-p4-d0.2@8192 | `panugali` |  | 1 |
| stochastic-p4-d0.2@16384 | `panugali` |  | 1 |
| unigram-ablation@6080 | `panugali` |  | 1 |

## `magbalik`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+balik`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+balik` | OK | 2 |
| plain@8192 | `magbalik` |  | 1 |
| plain@16384 | `magbalik` |  | 1 |
| morphbpe@6080 | `mag+balik` | OK | 2 |
| morphbpe@8192 | `mag+balik` | OK | 2 |
| morphbpe@16384 | `mag+balik` | OK | 2 |
| penalty-1@6080 | `mag+balik` | OK | 2 |
| penalty-1@8192 | `mag+balik` | OK | 2 |
| penalty-1@16384 | `mag+balik` | OK | 2 |
| penalty-2@6080 | `mag+balik` | OK | 2 |
| penalty-2@8192 | `mag+balik` | OK | 2 |
| penalty-2@16384 | `mag+balik` | OK | 2 |
| penalty-4@6080 | `mag+balik` | OK | 2 |
| penalty-4@8192 | `mag+balik` | OK | 2 |
| penalty-4@16384 | `mag+balik` | OK | 2 |
| penalty-8@6080 | `mag+balik` | OK | 2 |
| penalty-8@8192 | `mag+balik` | OK | 2 |
| penalty-8@16384 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mag+balik` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mag+balik` | OK | 2 |
| unigram-ablation@6080 | `magbalik` |  | 1 |

## `makasumami`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `maka+sumami`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makas+um+ami` |  | 3 |
| plain@8192 | `makas+um+ami` |  | 3 |
| plain@16384 | `makas+um+ami` |  | 3 |
| morphbpe@6080 | `maka+sum+ami` |  | 3 |
| morphbpe@8192 | `maka+sum+ami` |  | 3 |
| morphbpe@16384 | `maka+sum+ami` |  | 3 |
| penalty-1@6080 | `maka+s+um+ami` |  | 4 |
| penalty-1@8192 | `maka+s+um+ami` |  | 4 |
| penalty-1@16384 | `makas+um+ami` |  | 3 |
| penalty-2@6080 | `maka+s+um+ami` |  | 4 |
| penalty-2@8192 | `maka+s+um+ami` |  | 4 |
| penalty-2@16384 | `makas+um+ami` |  | 3 |
| penalty-4@6080 | `maka+s+um+ami` |  | 4 |
| penalty-4@8192 | `maka+s+um+ami` |  | 4 |
| penalty-4@16384 | `makas+um+ami` |  | 3 |
| penalty-8@6080 | `maka+s+um+ami` |  | 4 |
| penalty-8@8192 | `maka+s+um+ami` |  | 4 |
| penalty-8@16384 | `makas+um+ami` |  | 3 |
| stochastic-p4-d0.1@6080 | `maka+s+um+ami` |  | 4 |
| stochastic-p4-d0.1@8192 | `maka+s+um+ami` |  | 4 |
| stochastic-p4-d0.1@16384 | `maka+s+um+ami` |  | 4 |
| stochastic-p4-d0.2@6080 | `maka+su+mam+i` |  | 4 |
| stochastic-p4-d0.2@8192 | `maka+su+mam+i` |  | 4 |
| stochastic-p4-d0.2@16384 | `maka+su+mami` |  | 3 |
| unigram-ablation@6080 | `maka+suma+mi` |  | 3 |

## `malating`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+lating`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malating` |  | 1 |
| plain@8192 | `malating` |  | 1 |
| plain@16384 | `malating` |  | 1 |
| morphbpe@6080 | `malating` |  | 1 |
| morphbpe@8192 | `malating` |  | 1 |
| morphbpe@16384 | `malating` |  | 1 |
| penalty-1@6080 | `malating` |  | 1 |
| penalty-1@8192 | `malating` |  | 1 |
| penalty-1@16384 | `malating` |  | 1 |
| penalty-2@6080 | `malating` |  | 1 |
| penalty-2@8192 | `malating` |  | 1 |
| penalty-2@16384 | `malating` |  | 1 |
| penalty-4@6080 | `malating` |  | 1 |
| penalty-4@8192 | `malating` |  | 1 |
| penalty-4@16384 | `malating` |  | 1 |
| penalty-8@6080 | `malating` |  | 1 |
| penalty-8@8192 | `malating` |  | 1 |
| penalty-8@16384 | `malating` |  | 1 |
| stochastic-p4-d0.1@6080 | `malating` |  | 1 |
| stochastic-p4-d0.1@8192 | `malating` |  | 1 |
| stochastic-p4-d0.1@16384 | `malating` |  | 1 |
| stochastic-p4-d0.2@6080 | `malating` |  | 1 |
| stochastic-p4-d0.2@8192 | `malating` |  | 1 |
| stochastic-p4-d0.2@16384 | `malating` |  | 1 |
| unigram-ablation@6080 | `malating` |  | 1 |

## `maldang`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+ldang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+dang` |  | 2 |
| plain@8192 | `maldang` |  | 1 |
| plain@16384 | `maldang` |  | 1 |
| morphbpe@6080 | `mal+dang` |  | 2 |
| morphbpe@8192 | `maldang` |  | 1 |
| morphbpe@16384 | `maldang` |  | 1 |
| penalty-1@6080 | `mal+dang` |  | 2 |
| penalty-1@8192 | `maldang` |  | 1 |
| penalty-1@16384 | `maldang` |  | 1 |
| penalty-2@6080 | `mal+dang` |  | 2 |
| penalty-2@8192 | `maldang` |  | 1 |
| penalty-2@16384 | `maldang` |  | 1 |
| penalty-4@6080 | `mal+dang` |  | 2 |
| penalty-4@8192 | `maldang` |  | 1 |
| penalty-4@16384 | `maldang` |  | 1 |
| penalty-8@6080 | `mal+dang` |  | 2 |
| penalty-8@8192 | `maldang` |  | 1 |
| penalty-8@16384 | `maldang` |  | 1 |
| stochastic-p4-d0.1@6080 | `mal+d+ang` |  | 3 |
| stochastic-p4-d0.1@8192 | `mal+d+ang` |  | 3 |
| stochastic-p4-d0.1@16384 | `maldang` |  | 1 |
| stochastic-p4-d0.2@6080 | `mal+dang` |  | 2 |
| stochastic-p4-d0.2@8192 | `maldang` |  | 1 |
| stochastic-p4-d0.2@16384 | `maldang` |  | 1 |
| unigram-ablation@6080 | `malda+ng` |  | 2 |

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

## `maybug`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+ybug`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `may+bug` |  | 2 |
| plain@8192 | `may+bug` |  | 2 |
| plain@16384 | `maybug` |  | 1 |
| morphbpe@6080 | `may+bug` |  | 2 |
| morphbpe@8192 | `may+bug` |  | 2 |
| morphbpe@16384 | `maybug` |  | 1 |
| penalty-1@6080 | `may+bug` |  | 2 |
| penalty-1@8192 | `may+bug` |  | 2 |
| penalty-1@16384 | `maybug` |  | 1 |
| penalty-2@6080 | `may+bug` |  | 2 |
| penalty-2@8192 | `may+bug` |  | 2 |
| penalty-2@16384 | `maybug` |  | 1 |
| penalty-4@6080 | `may+bug` |  | 2 |
| penalty-4@8192 | `may+bug` |  | 2 |
| penalty-4@16384 | `maybug` |  | 1 |
| penalty-8@6080 | `may+bug` |  | 2 |
| penalty-8@8192 | `may+bug` |  | 2 |
| penalty-8@16384 | `maybug` |  | 1 |
| stochastic-p4-d0.1@6080 | `may+bug` |  | 2 |
| stochastic-p4-d0.1@8192 | `may+bug` |  | 2 |
| stochastic-p4-d0.1@16384 | `maybug` |  | 1 |
| stochastic-p4-d0.2@6080 | `may+bug` |  | 2 |
| stochastic-p4-d0.2@8192 | `may+bug` |  | 2 |
| stochastic-p4-d0.2@16384 | `maybug` |  | 1 |
| unigram-ablation@6080 | `may+bug` |  | 2 |

## `palalu`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+lalu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pal+alu` |  | 2 |
| plain@8192 | `pal+alu` |  | 2 |
| plain@16384 | `palalu` |  | 1 |
| morphbpe@6080 | `pal+alu` |  | 2 |
| morphbpe@8192 | `pal+alu` |  | 2 |
| morphbpe@16384 | `pal+alu` |  | 2 |
| penalty-1@6080 | `pal+alu` |  | 2 |
| penalty-1@8192 | `pal+alu` |  | 2 |
| penalty-1@16384 | `pal+alu` |  | 2 |
| penalty-2@6080 | `pal+alu` |  | 2 |
| penalty-2@8192 | `pal+alu` |  | 2 |
| penalty-2@16384 | `pal+alu` |  | 2 |
| penalty-4@6080 | `pal+alu` |  | 2 |
| penalty-4@8192 | `pal+alu` |  | 2 |
| penalty-4@16384 | `pal+alu` |  | 2 |
| penalty-8@6080 | `pa+lalu` | OK | 2 |
| penalty-8@8192 | `pa+lalu` | OK | 2 |
| penalty-8@16384 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.1@6080 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.1@8192 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.1@16384 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.2@6080 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pa+lalu` | OK | 2 |
| stochastic-p4-d0.2@16384 | `pa+lalu` | OK | 2 |
| unigram-ablation@6080 | `pa+lalu` | OK | 2 |

## `palang`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+lang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `p+alang` |  | 2 |
| plain@8192 | `palang` |  | 1 |
| plain@16384 | `palang` |  | 1 |
| morphbpe@6080 | `p+alang` |  | 2 |
| morphbpe@8192 | `palang` |  | 1 |
| morphbpe@16384 | `palang` |  | 1 |
| penalty-1@6080 | `p+alang` |  | 2 |
| penalty-1@8192 | `palang` |  | 1 |
| penalty-1@16384 | `palang` |  | 1 |
| penalty-2@6080 | `p+alang` |  | 2 |
| penalty-2@8192 | `palang` |  | 1 |
| penalty-2@16384 | `palang` |  | 1 |
| penalty-4@6080 | `p+alang` |  | 2 |
| penalty-4@8192 | `palang` |  | 1 |
| penalty-4@16384 | `palang` |  | 1 |
| penalty-8@6080 | `p+alang` |  | 2 |
| penalty-8@8192 | `palang` |  | 1 |
| penalty-8@16384 | `palang` |  | 1 |
| stochastic-p4-d0.1@6080 | `p+alang` |  | 2 |
| stochastic-p4-d0.1@8192 | `p+alang` |  | 2 |
| stochastic-p4-d0.1@16384 | `palang` |  | 1 |
| stochastic-p4-d0.2@6080 | `pa+lang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pa+lang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `palang` |  | 1 |
| unigram-ablation@6080 | `pa+lang` | OK | 2 |

## `pansin`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+nsin`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pan+sin` |  | 2 |
| plain@8192 | `pansin` |  | 1 |
| plain@16384 | `pansin` |  | 1 |
| morphbpe@6080 | `pan+sin` |  | 2 |
| morphbpe@8192 | `pansin` |  | 1 |
| morphbpe@16384 | `pansin` |  | 1 |
| penalty-1@6080 | `pans+in` |  | 2 |
| penalty-1@8192 | `pansin` |  | 1 |
| penalty-1@16384 | `pansin` |  | 1 |
| penalty-2@6080 | `pansin` |  | 1 |
| penalty-2@8192 | `pansin` |  | 1 |
| penalty-2@16384 | `pansin` |  | 1 |
| penalty-4@6080 | `pansin` |  | 1 |
| penalty-4@8192 | `pansin` |  | 1 |
| penalty-4@16384 | `pansin` |  | 1 |
| penalty-8@6080 | `pansin` |  | 1 |
| penalty-8@8192 | `pansin` |  | 1 |
| penalty-8@16384 | `pansin` |  | 1 |
| stochastic-p4-d0.1@6080 | `pansin` |  | 1 |
| stochastic-p4-d0.1@8192 | `pansin` |  | 1 |
| stochastic-p4-d0.1@16384 | `pansin` |  | 1 |
| stochastic-p4-d0.2@6080 | `pansin` |  | 1 |
| stochastic-p4-d0.2@8192 | `pansin` |  | 1 |
| stochastic-p4-d0.2@16384 | `pansin` |  | 1 |
| unigram-ablation@6080 | `pansin` |  | 1 |

## `payapa`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `payapa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paya+pa` |  | 2 |
| plain@8192 | `payapa` | OK | 1 |
| plain@16384 | `payapa` | OK | 1 |
| morphbpe@6080 | `paya+pa` |  | 2 |
| morphbpe@8192 | `payapa` | OK | 1 |
| morphbpe@16384 | `payapa` | OK | 1 |
| penalty-1@6080 | `paya+pa` |  | 2 |
| penalty-1@8192 | `payapa` | OK | 1 |
| penalty-1@16384 | `payapa` | OK | 1 |
| penalty-2@6080 | `paya+pa` |  | 2 |
| penalty-2@8192 | `payapa` | OK | 1 |
| penalty-2@16384 | `payapa` | OK | 1 |
| penalty-4@6080 | `paya+pa` |  | 2 |
| penalty-4@8192 | `payapa` | OK | 1 |
| penalty-4@16384 | `payapa` | OK | 1 |
| penalty-8@6080 | `pa+ya+pa` |  | 3 |
| penalty-8@8192 | `payapa` | OK | 1 |
| penalty-8@16384 | `payapa` | OK | 1 |
| stochastic-p4-d0.1@6080 | `pa+ya+pa` |  | 3 |
| stochastic-p4-d0.1@8192 | `paya+pa` |  | 2 |
| stochastic-p4-d0.1@16384 | `payapa` | OK | 1 |
| stochastic-p4-d0.2@6080 | `paya+pa` |  | 2 |
| stochastic-p4-d0.2@8192 | `payapa` | OK | 1 |
| stochastic-p4-d0.2@16384 | `payapa` | OK | 1 |
| unigram-ablation@6080 | `payapa` | OK | 1 |

## `mababa`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+baba`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mab+aba` |  | 2 |
| plain@8192 | `mababa` |  | 1 |
| plain@16384 | `mababa` |  | 1 |
| morphbpe@6080 | `mab+aba` |  | 2 |
| morphbpe@8192 | `mababa` |  | 1 |
| morphbpe@16384 | `mababa` |  | 1 |
| penalty-1@6080 | `ma+baba` | OK | 2 |
| penalty-1@8192 | `mababa` |  | 1 |
| penalty-1@16384 | `mababa` |  | 1 |
| penalty-2@6080 | `ma+baba` | OK | 2 |
| penalty-2@8192 | `mababa` |  | 1 |
| penalty-2@16384 | `mababa` |  | 1 |
| penalty-4@6080 | `mababa` |  | 1 |
| penalty-4@8192 | `mababa` |  | 1 |
| penalty-4@16384 | `mababa` |  | 1 |
| penalty-8@6080 | `mababa` |  | 1 |
| penalty-8@8192 | `mababa` |  | 1 |
| penalty-8@16384 | `mababa` |  | 1 |
| stochastic-p4-d0.1@6080 | `mababa` |  | 1 |
| stochastic-p4-d0.1@8192 | `mababa` |  | 1 |
| stochastic-p4-d0.1@16384 | `mababa` |  | 1 |
| stochastic-p4-d0.2@6080 | `mababa` |  | 1 |
| stochastic-p4-d0.2@8192 | `mababa` |  | 1 |
| stochastic-p4-d0.2@16384 | `mababa` |  | 1 |
| unigram-ablation@6080 | `mababa` |  | 1 |

## `makibat`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+kibat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mak+ibat` |  | 2 |
| plain@8192 | `mak+ibat` |  | 2 |
| plain@16384 | `makibat` |  | 1 |
| morphbpe@6080 | `mak+ibat` |  | 2 |
| morphbpe@8192 | `mak+ibat` |  | 2 |
| morphbpe@16384 | `makibat` |  | 1 |
| penalty-1@6080 | `mak+ibat` |  | 2 |
| penalty-1@8192 | `mak+ibat` |  | 2 |
| penalty-1@16384 | `makibat` |  | 1 |
| penalty-2@6080 | `mak+ibat` |  | 2 |
| penalty-2@8192 | `mak+ibat` |  | 2 |
| penalty-2@16384 | `makibat` |  | 1 |
| penalty-4@6080 | `ma+kibat` | OK | 2 |
| penalty-4@8192 | `ma+kibat` | OK | 2 |
| penalty-4@16384 | `makibat` |  | 1 |
| penalty-8@6080 | `maki+bat` |  | 2 |
| penalty-8@8192 | `maki+bat` |  | 2 |
| penalty-8@16384 | `makibat` |  | 1 |
| stochastic-p4-d0.1@6080 | `maki+bat` |  | 2 |
| stochastic-p4-d0.1@8192 | `maki+bat` |  | 2 |
| stochastic-p4-d0.1@16384 | `makibat` |  | 1 |
| stochastic-p4-d0.2@6080 | `maki+bat` |  | 2 |
| stochastic-p4-d0.2@8192 | `maki+bat` |  | 2 |
| stochastic-p4-d0.2@16384 | `makibat` |  | 1 |
| unigram-ablation@6080 | `maki+bat` |  | 2 |

## `mangarawak`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+arawak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangar+awak` |  | 2 |
| plain@8192 | `mangar+awak` |  | 2 |
| plain@16384 | `mangarawak` |  | 1 |
| morphbpe@6080 | `mangar+awak` |  | 2 |
| morphbpe@8192 | `mangar+awak` |  | 2 |
| morphbpe@16384 | `mangarawak` |  | 1 |
| penalty-1@6080 | `mangar+aw+ak` |  | 3 |
| penalty-1@8192 | `mangar+awak` |  | 2 |
| penalty-1@16384 | `mangarawak` |  | 1 |
| penalty-2@6080 | `mang+ar+aw+ak` |  | 4 |
| penalty-2@8192 | `mang+ar+awak` |  | 3 |
| penalty-2@16384 | `mangarawak` |  | 1 |
| penalty-4@6080 | `mang+ar+aw+ak` |  | 4 |
| penalty-4@8192 | `mang+ar+awak` |  | 3 |
| penalty-4@16384 | `mangarawak` |  | 1 |
| penalty-8@6080 | `mang+ara+wak` |  | 3 |
| penalty-8@8192 | `mang+ara+wak` |  | 3 |
| penalty-8@16384 | `mangarawak` |  | 1 |
| stochastic-p4-d0.1@6080 | `mang+ara+wak` |  | 3 |
| stochastic-p4-d0.1@8192 | `mang+ara+wak` |  | 3 |
| stochastic-p4-d0.1@16384 | `mangarawak` |  | 1 |
| stochastic-p4-d0.2@6080 | `manga+rawak` |  | 2 |
| stochastic-p4-d0.2@8192 | `manga+rawak` |  | 2 |
| stochastic-p4-d0.2@16384 | `mangarawak` |  | 1 |
| unigram-ablation@6080 | `mang+arawak` | OK | 2 |

## `mangatas`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `mang+atas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mang+atas` | OK | 2 |
| plain@8192 | `mang+atas` | OK | 2 |
| plain@16384 | `mangatas` |  | 1 |
| morphbpe@6080 | `mang+atas` | OK | 2 |
| morphbpe@8192 | `mang+atas` | OK | 2 |
| morphbpe@16384 | `mangatas` |  | 1 |
| penalty-1@6080 | `mang+atas` | OK | 2 |
| penalty-1@8192 | `mang+atas` | OK | 2 |
| penalty-1@16384 | `mangatas` |  | 1 |
| penalty-2@6080 | `mang+atas` | OK | 2 |
| penalty-2@8192 | `mang+atas` | OK | 2 |
| penalty-2@16384 | `mangatas` |  | 1 |
| penalty-4@6080 | `mang+atas` | OK | 2 |
| penalty-4@8192 | `mang+atas` | OK | 2 |
| penalty-4@16384 | `mangatas` |  | 1 |
| penalty-8@6080 | `mang+atas` | OK | 2 |
| penalty-8@8192 | `mang+atas` | OK | 2 |
| penalty-8@16384 | `mangatas` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangat+as` |  | 2 |
| stochastic-p4-d0.1@8192 | `mangat+as` |  | 2 |
| stochastic-p4-d0.1@16384 | `mangatas` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangat+as` |  | 2 |
| stochastic-p4-d0.2@8192 | `mangat+as` |  | 2 |
| stochastic-p4-d0.2@16384 | `mangatas` |  | 1 |
| unigram-ablation@6080 | `manga+tas` |  | 2 |

## `marinat`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rinat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mar+inat` |  | 2 |
| plain@8192 | `marinat` |  | 1 |
| plain@16384 | `marinat` |  | 1 |
| morphbpe@6080 | `mar+inat` |  | 2 |
| morphbpe@8192 | `marinat` |  | 1 |
| morphbpe@16384 | `marinat` |  | 1 |
| penalty-1@6080 | `mar+inat` |  | 2 |
| penalty-1@8192 | `marinat` |  | 1 |
| penalty-1@16384 | `marinat` |  | 1 |
| penalty-2@6080 | `marin+at` |  | 2 |
| penalty-2@8192 | `marinat` |  | 1 |
| penalty-2@16384 | `marinat` |  | 1 |
| penalty-4@6080 | `marin+at` |  | 2 |
| penalty-4@8192 | `marinat` |  | 1 |
| penalty-4@16384 | `marinat` |  | 1 |
| penalty-8@6080 | `marin+at` |  | 2 |
| penalty-8@8192 | `marinat` |  | 1 |
| penalty-8@16384 | `marinat` |  | 1 |
| stochastic-p4-d0.1@6080 | `marin+at` |  | 2 |
| stochastic-p4-d0.1@8192 | `marinat` |  | 1 |
| stochastic-p4-d0.1@16384 | `marinat` |  | 1 |
| stochastic-p4-d0.2@6080 | `marin+at` |  | 2 |
| stochastic-p4-d0.2@8192 | `marinat` |  | 1 |
| stochastic-p4-d0.2@16384 | `marinat` |  | 1 |
| unigram-ablation@6080 | `marinat` |  | 1 |

## `masakit`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+sakit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masakit` |  | 1 |
| plain@8192 | `masakit` |  | 1 |
| plain@16384 | `masakit` |  | 1 |
| morphbpe@6080 | `masakit` |  | 1 |
| morphbpe@8192 | `masakit` |  | 1 |
| morphbpe@16384 | `masakit` |  | 1 |
| penalty-1@6080 | `masakit` |  | 1 |
| penalty-1@8192 | `masakit` |  | 1 |
| penalty-1@16384 | `masakit` |  | 1 |
| penalty-2@6080 | `masakit` |  | 1 |
| penalty-2@8192 | `masakit` |  | 1 |
| penalty-2@16384 | `masakit` |  | 1 |
| penalty-4@6080 | `masakit` |  | 1 |
| penalty-4@8192 | `masakit` |  | 1 |
| penalty-4@16384 | `masakit` |  | 1 |
| penalty-8@6080 | `masakit` |  | 1 |
| penalty-8@8192 | `masakit` |  | 1 |
| penalty-8@16384 | `masakit` |  | 1 |
| stochastic-p4-d0.1@6080 | `masakit` |  | 1 |
| stochastic-p4-d0.1@8192 | `masakit` |  | 1 |
| stochastic-p4-d0.1@16384 | `masakit` |  | 1 |
| stochastic-p4-d0.2@6080 | `masakit` |  | 1 |
| stochastic-p4-d0.2@8192 | `masakit` |  | 1 |
| stochastic-p4-d0.2@16384 | `masakit` |  | 1 |
| unigram-ablation@6080 | `ma+sakit` | OK | 2 |

## `masalese`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+salese`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masalese` |  | 1 |
| plain@8192 | `masalese` |  | 1 |
| plain@16384 | `masalese` |  | 1 |
| morphbpe@6080 | `mas+al+ese` |  | 3 |
| morphbpe@8192 | `mas+al+ese` |  | 3 |
| morphbpe@16384 | `masal+ese` |  | 2 |
| penalty-1@6080 | `ma+salese` | OK | 2 |
| penalty-1@8192 | `ma+salese` | OK | 2 |
| penalty-1@16384 | `ma+salese` | OK | 2 |
| penalty-2@6080 | `ma+salese` | OK | 2 |
| penalty-2@8192 | `ma+salese` | OK | 2 |
| penalty-2@16384 | `ma+salese` | OK | 2 |
| penalty-4@6080 | `ma+salese` | OK | 2 |
| penalty-4@8192 | `ma+salese` | OK | 2 |
| penalty-4@16384 | `ma+salese` | OK | 2 |
| penalty-8@6080 | `ma+salese` | OK | 2 |
| penalty-8@8192 | `ma+salese` | OK | 2 |
| penalty-8@16384 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+salese` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+salese` | OK | 2 |
| unigram-ablation@6080 | `masalese` |  | 1 |

## `masant`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+sant`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ant` |  | 2 |
| plain@8192 | `mas+ant` |  | 2 |
| plain@16384 | `mas+ant` |  | 2 |
| morphbpe@6080 | `mas+ant` |  | 2 |
| morphbpe@8192 | `mas+ant` |  | 2 |
| morphbpe@16384 | `mas+ant` |  | 2 |
| penalty-1@6080 | `mas+ant` |  | 2 |
| penalty-1@8192 | `mas+ant` |  | 2 |
| penalty-1@16384 | `mas+ant` |  | 2 |
| penalty-2@6080 | `mas+ant` |  | 2 |
| penalty-2@8192 | `mas+ant` |  | 2 |
| penalty-2@16384 | `mas+ant` |  | 2 |
| penalty-4@6080 | `mas+ant` |  | 2 |
| penalty-4@8192 | `mas+ant` |  | 2 |
| penalty-4@16384 | `mas+ant` |  | 2 |
| penalty-8@6080 | `mas+ant` |  | 2 |
| penalty-8@8192 | `mas+ant` |  | 2 |
| penalty-8@16384 | `mas+ant` |  | 2 |
| stochastic-p4-d0.1@6080 | `mas+ant` |  | 2 |
| stochastic-p4-d0.1@8192 | `mas+ant` |  | 2 |
| stochastic-p4-d0.1@16384 | `masant` |  | 1 |
| stochastic-p4-d0.2@6080 | `mas+ant` |  | 2 |
| stochastic-p4-d0.2@8192 | `mas+ant` |  | 2 |
| stochastic-p4-d0.2@16384 | `mas+ant` |  | 2 |
| unigram-ablation@6080 | `mas+an+t` |  | 3 |

## `maslag`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+slag`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+lag` |  | 2 |
| plain@8192 | `maslag` |  | 1 |
| plain@16384 | `maslag` |  | 1 |
| morphbpe@6080 | `mas+lag` |  | 2 |
| morphbpe@8192 | `maslag` |  | 1 |
| morphbpe@16384 | `maslag` |  | 1 |
| penalty-1@6080 | `mas+lag` |  | 2 |
| penalty-1@8192 | `maslag` |  | 1 |
| penalty-1@16384 | `maslag` |  | 1 |
| penalty-2@6080 | `mas+lag` |  | 2 |
| penalty-2@8192 | `maslag` |  | 1 |
| penalty-2@16384 | `maslag` |  | 1 |
| penalty-4@6080 | `mas+lag` |  | 2 |
| penalty-4@8192 | `maslag` |  | 1 |
| penalty-4@16384 | `maslag` |  | 1 |
| penalty-8@6080 | `mas+lag` |  | 2 |
| penalty-8@8192 | `maslag` |  | 1 |
| penalty-8@16384 | `maslag` |  | 1 |
| stochastic-p4-d0.1@6080 | `mas+lag` |  | 2 |
| stochastic-p4-d0.1@8192 | `maslag` |  | 1 |
| stochastic-p4-d0.1@16384 | `maslag` |  | 1 |
| stochastic-p4-d0.2@6080 | `mas+lag` |  | 2 |
| stochastic-p4-d0.2@8192 | `maslag` |  | 1 |
| stochastic-p4-d0.2@16384 | `maslag` |  | 1 |
| unigram-ablation@6080 | `m+aslag` |  | 2 |

## `pagkalub`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+gkalub`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+kalub` |  | 2 |
| plain@8192 | `pag+kalub` |  | 2 |
| plain@16384 | `pagkalub` |  | 1 |
| morphbpe@6080 | `pag+kalub` |  | 2 |
| morphbpe@8192 | `pag+kalub` |  | 2 |
| morphbpe@16384 | `pagkalub` |  | 1 |
| penalty-1@6080 | `pag+kalub` |  | 2 |
| penalty-1@8192 | `pag+kalub` |  | 2 |
| penalty-1@16384 | `pagkalub` |  | 1 |
| penalty-2@6080 | `pag+kalub` |  | 2 |
| penalty-2@8192 | `pag+kalub` |  | 2 |
| penalty-2@16384 | `pagkalub` |  | 1 |
| penalty-4@6080 | `pag+kalub` |  | 2 |
| penalty-4@8192 | `pag+kalub` |  | 2 |
| penalty-4@16384 | `pagkalub` |  | 1 |
| penalty-8@6080 | `pagka+lub` |  | 2 |
| penalty-8@8192 | `pagkalub` |  | 1 |
| penalty-8@16384 | `pagkalub` |  | 1 |
| stochastic-p4-d0.1@6080 | `pagka+lub` |  | 2 |
| stochastic-p4-d0.1@8192 | `pagka+lub` |  | 2 |
| stochastic-p4-d0.1@16384 | `pagkalub` |  | 1 |
| stochastic-p4-d0.2@6080 | `pagka+lub` |  | 2 |
| stochastic-p4-d0.2@8192 | `pagkalub` |  | 1 |
| stochastic-p4-d0.2@16384 | `pagkalub` |  | 1 |
| unigram-ablation@6080 | `pagkalub` |  | 1 |

## `pagsalbat`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+gsalbat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pag+sal+bat` |  | 3 |
| plain@8192 | `pag+sal+bat` |  | 3 |
| plain@16384 | `pagsalbat` |  | 1 |
| morphbpe@6080 | `pag+sal+bat` |  | 3 |
| morphbpe@8192 | `pag+salbat` |  | 2 |
| morphbpe@16384 | `pagsalbat` |  | 1 |
| penalty-1@6080 | `pag+sal+bat` |  | 3 |
| penalty-1@8192 | `pag+salbat` |  | 2 |
| penalty-1@16384 | `pagsalbat` |  | 1 |
| penalty-2@6080 | `pag+sal+bat` |  | 3 |
| penalty-2@8192 | `pag+salbat` |  | 2 |
| penalty-2@16384 | `pagsalbat` |  | 1 |
| penalty-4@6080 | `pag+sal+bat` |  | 3 |
| penalty-4@8192 | `pag+salbat` |  | 2 |
| penalty-4@16384 | `pagsalbat` |  | 1 |
| penalty-8@6080 | `pag+sal+bat` |  | 3 |
| penalty-8@8192 | `pag+salbat` |  | 2 |
| penalty-8@16384 | `pagsalbat` |  | 1 |
| stochastic-p4-d0.1@6080 | `pag+sal+bat` |  | 3 |
| stochastic-p4-d0.1@8192 | `pag+salbat` |  | 2 |
| stochastic-p4-d0.1@16384 | `pagsalbat` |  | 1 |
| stochastic-p4-d0.2@6080 | `pag+sal+bat` |  | 3 |
| stochastic-p4-d0.2@8192 | `pag+salbat` |  | 2 |
| stochastic-p4-d0.2@16384 | `pagsalbat` |  | 1 |
| unigram-ablation@6080 | `p+agsalbat` |  | 2 |

## `paralan`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+ralan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paralan` |  | 1 |
| plain@8192 | `paralan` |  | 1 |
| plain@16384 | `paralan` |  | 1 |
| morphbpe@6080 | `paralan` |  | 1 |
| morphbpe@8192 | `paralan` |  | 1 |
| morphbpe@16384 | `paralan` |  | 1 |
| penalty-1@6080 | `paralan` |  | 1 |
| penalty-1@8192 | `paralan` |  | 1 |
| penalty-1@16384 | `paralan` |  | 1 |
| penalty-2@6080 | `paralan` |  | 1 |
| penalty-2@8192 | `paralan` |  | 1 |
| penalty-2@16384 | `paralan` |  | 1 |
| penalty-4@6080 | `paralan` |  | 1 |
| penalty-4@8192 | `paralan` |  | 1 |
| penalty-4@16384 | `paralan` |  | 1 |
| penalty-8@6080 | `paralan` |  | 1 |
| penalty-8@8192 | `paralan` |  | 1 |
| penalty-8@16384 | `paralan` |  | 1 |
| stochastic-p4-d0.1@6080 | `paralan` |  | 1 |
| stochastic-p4-d0.1@8192 | `paralan` |  | 1 |
| stochastic-p4-d0.1@16384 | `paralan` |  | 1 |
| stochastic-p4-d0.2@6080 | `paralan` |  | 1 |
| stochastic-p4-d0.2@8192 | `paralan` |  | 1 |
| stochastic-p4-d0.2@16384 | `paralan` |  | 1 |
| unigram-ablation@6080 | `paralan` |  | 1 |

## `pastul`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pastul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pas+tul` |  | 2 |
| plain@8192 | `pastul` | OK | 1 |
| plain@16384 | `pastul` | OK | 1 |
| morphbpe@6080 | `pas+tul` |  | 2 |
| morphbpe@8192 | `pastul` | OK | 1 |
| morphbpe@16384 | `pastul` | OK | 1 |
| penalty-1@6080 | `pas+tul` |  | 2 |
| penalty-1@8192 | `pastul` | OK | 1 |
| penalty-1@16384 | `pastul` | OK | 1 |
| penalty-2@6080 | `past+ul` |  | 2 |
| penalty-2@8192 | `pastul` | OK | 1 |
| penalty-2@16384 | `pastul` | OK | 1 |
| penalty-4@6080 | `past+ul` |  | 2 |
| penalty-4@8192 | `pastul` | OK | 1 |
| penalty-4@16384 | `pastul` | OK | 1 |
| penalty-8@6080 | `pas+tul` |  | 2 |
| penalty-8@8192 | `pastul` | OK | 1 |
| penalty-8@16384 | `pastul` | OK | 1 |
| stochastic-p4-d0.1@6080 | `pa+st+ul` |  | 3 |
| stochastic-p4-d0.1@8192 | `pastul` | OK | 1 |
| stochastic-p4-d0.1@16384 | `pastul` | OK | 1 |
| stochastic-p4-d0.2@6080 | `pas+tul` |  | 2 |
| stochastic-p4-d0.2@8192 | `pastul` | OK | 1 |
| stochastic-p4-d0.2@16384 | `pastul` | OK | 1 |
| unigram-ablation@6080 | `pastul` | OK | 1 |

## `malutu`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lutu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+utu` |  | 2 |
| plain@8192 | `malutu` |  | 1 |
| plain@16384 | `malutu` |  | 1 |
| morphbpe@6080 | `mal+utu` |  | 2 |
| morphbpe@8192 | `malutu` |  | 1 |
| morphbpe@16384 | `malutu` |  | 1 |
| penalty-1@6080 | `mal+utu` |  | 2 |
| penalty-1@8192 | `malutu` |  | 1 |
| penalty-1@16384 | `malutu` |  | 1 |
| penalty-2@6080 | `mal+utu` |  | 2 |
| penalty-2@8192 | `malutu` |  | 1 |
| penalty-2@16384 | `malutu` |  | 1 |
| penalty-4@6080 | `malu+tu` |  | 2 |
| penalty-4@8192 | `malutu` |  | 1 |
| penalty-4@16384 | `malutu` |  | 1 |
| penalty-8@6080 | `malutu` |  | 1 |
| penalty-8@8192 | `malutu` |  | 1 |
| penalty-8@16384 | `malutu` |  | 1 |
| stochastic-p4-d0.1@6080 | `malutu` |  | 1 |
| stochastic-p4-d0.1@8192 | `malutu` |  | 1 |
| stochastic-p4-d0.1@16384 | `malutu` |  | 1 |
| stochastic-p4-d0.2@6080 | `malutu` |  | 1 |
| stochastic-p4-d0.2@8192 | `malutu` |  | 1 |
| stochastic-p4-d0.2@16384 | `malutu` |  | 1 |
| unigram-ablation@6080 | `malutu` |  | 1 |

## `manalo`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+nalo`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+alo` |  | 2 |
| plain@8192 | `man+alo` |  | 2 |
| plain@16384 | `man+alo` |  | 2 |
| morphbpe@6080 | `man+alo` |  | 2 |
| morphbpe@8192 | `man+alo` |  | 2 |
| morphbpe@16384 | `man+alo` |  | 2 |
| penalty-1@6080 | `man+alo` |  | 2 |
| penalty-1@8192 | `man+alo` |  | 2 |
| penalty-1@16384 | `man+alo` |  | 2 |
| penalty-2@6080 | `man+alo` |  | 2 |
| penalty-2@8192 | `man+alo` |  | 2 |
| penalty-2@16384 | `man+alo` |  | 2 |
| penalty-4@6080 | `man+alo` |  | 2 |
| penalty-4@8192 | `man+alo` |  | 2 |
| penalty-4@16384 | `man+alo` |  | 2 |
| penalty-8@6080 | `man+alo` |  | 2 |
| penalty-8@8192 | `man+alo` |  | 2 |
| penalty-8@16384 | `man+alo` |  | 2 |
| stochastic-p4-d0.1@6080 | `man+alo` |  | 2 |
| stochastic-p4-d0.1@8192 | `man+alo` |  | 2 |
| stochastic-p4-d0.1@16384 | `man+alo` |  | 2 |
| stochastic-p4-d0.2@6080 | `man+alo` |  | 2 |
| stochastic-p4-d0.2@8192 | `man+alo` |  | 2 |
| stochastic-p4-d0.2@16384 | `man+alo` |  | 2 |
| unigram-ablation@6080 | `man+a+lo` |  | 3 |

## `mangalati`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+alati`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangal+ati` |  | 2 |
| plain@8192 | `mangal+ati` |  | 2 |
| plain@16384 | `mangalati` |  | 1 |
| morphbpe@6080 | `mangal+ati` |  | 2 |
| morphbpe@8192 | `mangal+ati` |  | 2 |
| morphbpe@16384 | `mangalati` |  | 1 |
| penalty-1@6080 | `mangal+ati` |  | 2 |
| penalty-1@8192 | `mangal+ati` |  | 2 |
| penalty-1@16384 | `mangalati` |  | 1 |
| penalty-2@6080 | `mangal+ati` |  | 2 |
| penalty-2@8192 | `mangal+ati` |  | 2 |
| penalty-2@16384 | `mangalati` |  | 1 |
| penalty-4@6080 | `mangal+ati` |  | 2 |
| penalty-4@8192 | `mangal+ati` |  | 2 |
| penalty-4@16384 | `mangalati` |  | 1 |
| penalty-8@6080 | `mangala+ti` |  | 2 |
| penalty-8@8192 | `mangala+ti` |  | 2 |
| penalty-8@16384 | `mangalati` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangala+ti` |  | 2 |
| stochastic-p4-d0.1@8192 | `mangala+ti` |  | 2 |
| stochastic-p4-d0.1@16384 | `mangalati` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangala+ti` |  | 2 |
| stochastic-p4-d0.2@8192 | `mangala+ti` |  | 2 |
| stochastic-p4-d0.2@16384 | `mangalati` |  | 1 |
| unigram-ablation@6080 | `mangalati` |  | 1 |

## `mapaling`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+paling`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `map+aling` |  | 2 |
| plain@8192 | `map+aling` |  | 2 |
| plain@16384 | `mapaling` |  | 1 |
| morphbpe@6080 | `map+aling` |  | 2 |
| morphbpe@8192 | `mapaling` |  | 1 |
| morphbpe@16384 | `mapaling` |  | 1 |
| penalty-1@6080 | `mapal+ing` |  | 2 |
| penalty-1@8192 | `mapaling` |  | 1 |
| penalty-1@16384 | `mapaling` |  | 1 |
| penalty-2@6080 | `mapal+ing` |  | 2 |
| penalty-2@8192 | `mapaling` |  | 1 |
| penalty-2@16384 | `mapaling` |  | 1 |
| penalty-4@6080 | `mapal+ing` |  | 2 |
| penalty-4@8192 | `mapaling` |  | 1 |
| penalty-4@16384 | `mapaling` |  | 1 |
| penalty-8@6080 | `mapal+ing` |  | 2 |
| penalty-8@8192 | `mapaling` |  | 1 |
| penalty-8@16384 | `mapaling` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+pali+ng` |  | 3 |
| stochastic-p4-d0.1@8192 | `mapali+ng` |  | 2 |
| stochastic-p4-d0.1@16384 | `mapaling` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+pali+ng` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+pali+ng` |  | 3 |
| stochastic-p4-d0.2@16384 | `mapaling` |  | 1 |
| unigram-ablation@6080 | `mapa+ling` |  | 2 |

## `matatag`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+tatag`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mat+atag` |  | 2 |
| plain@8192 | `mat+atag` |  | 2 |
| plain@16384 | `matatag` |  | 1 |
| morphbpe@6080 | `mat+atag` |  | 2 |
| morphbpe@8192 | `matatag` |  | 1 |
| morphbpe@16384 | `matatag` |  | 1 |
| penalty-1@6080 | `mat+atag` |  | 2 |
| penalty-1@8192 | `matatag` |  | 1 |
| penalty-1@16384 | `matatag` |  | 1 |
| penalty-2@6080 | `mat+atag` |  | 2 |
| penalty-2@8192 | `matatag` |  | 1 |
| penalty-2@16384 | `matatag` |  | 1 |
| penalty-4@6080 | `mat+atag` |  | 2 |
| penalty-4@8192 | `matatag` |  | 1 |
| penalty-4@16384 | `matatag` |  | 1 |
| penalty-8@6080 | `mat+atag` |  | 2 |
| penalty-8@8192 | `matatag` |  | 1 |
| penalty-8@16384 | `matatag` |  | 1 |
| stochastic-p4-d0.1@6080 | `mat+atag` |  | 2 |
| stochastic-p4-d0.1@8192 | `mat+atag` |  | 2 |
| stochastic-p4-d0.1@16384 | `matatag` |  | 1 |
| stochastic-p4-d0.2@6080 | `mat+atag` |  | 2 |
| stochastic-p4-d0.2@8192 | `matatag` |  | 1 |
| stochastic-p4-d0.2@16384 | `matatag` |  | 1 |
| unigram-ablation@6080 | `ma+tatag` | OK | 2 |

## `mayumu`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+yumu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mayu+mu` |  | 2 |
| plain@8192 | `mayumu` |  | 1 |
| plain@16384 | `mayumu` |  | 1 |
| morphbpe@6080 | `mayu+mu` |  | 2 |
| morphbpe@8192 | `mayu+mu` |  | 2 |
| morphbpe@16384 | `mayu+mu` |  | 2 |
| penalty-1@6080 | `mayu+mu` |  | 2 |
| penalty-1@8192 | `mayu+mu` |  | 2 |
| penalty-1@16384 | `mayu+mu` |  | 2 |
| penalty-2@6080 | `mayu+mu` |  | 2 |
| penalty-2@8192 | `mayu+mu` |  | 2 |
| penalty-2@16384 | `mayu+mu` |  | 2 |
| penalty-4@6080 | `mayu+mu` |  | 2 |
| penalty-4@8192 | `mayu+mu` |  | 2 |
| penalty-4@16384 | `mayu+mu` |  | 2 |
| penalty-8@6080 | `ma+yu+mu` |  | 3 |
| penalty-8@8192 | `mayu+mu` |  | 2 |
| penalty-8@16384 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.1@6080 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.1@8192 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.1@16384 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.2@6080 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.2@8192 | `mayu+mu` |  | 2 |
| stochastic-p4-d0.2@16384 | `mayu+mu` |  | 2 |
| unigram-ablation@6080 | `mayumu` |  | 1 |

## `parati`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+rati`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `parati` |  | 1 |
| plain@8192 | `parati` |  | 1 |
| plain@16384 | `parati` |  | 1 |
| morphbpe@6080 | `parati` |  | 1 |
| morphbpe@8192 | `parati` |  | 1 |
| morphbpe@16384 | `parati` |  | 1 |
| penalty-1@6080 | `parati` |  | 1 |
| penalty-1@8192 | `parati` |  | 1 |
| penalty-1@16384 | `parati` |  | 1 |
| penalty-2@6080 | `parati` |  | 1 |
| penalty-2@8192 | `parati` |  | 1 |
| penalty-2@16384 | `parati` |  | 1 |
| penalty-4@6080 | `parati` |  | 1 |
| penalty-4@8192 | `parati` |  | 1 |
| penalty-4@16384 | `parati` |  | 1 |
| penalty-8@6080 | `parati` |  | 1 |
| penalty-8@8192 | `parati` |  | 1 |
| penalty-8@16384 | `parati` |  | 1 |
| stochastic-p4-d0.1@6080 | `parati` |  | 1 |
| stochastic-p4-d0.1@8192 | `parati` |  | 1 |
| stochastic-p4-d0.1@16384 | `parati` |  | 1 |
| stochastic-p4-d0.2@6080 | `parati` |  | 1 |
| stochastic-p4-d0.2@8192 | `parati` |  | 1 |
| stochastic-p4-d0.2@16384 | `parati` |  | 1 |
| unigram-ablation@6080 | `parati` |  | 1 |

## `ipagamuamu`  (prefixation, tier B_moderate_silver)

**silver gold:** `ipa+gamuamu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ipag+amu+amu` |  | 3 |
| plain@8192 | `ipag+amuamu` |  | 2 |
| plain@16384 | `ipag+amuamu` |  | 2 |
| morphbpe@6080 | `ipag+amu+amu` |  | 3 |
| morphbpe@8192 | `ipag+amuamu` |  | 2 |
| morphbpe@16384 | `ipag+amuamu` |  | 2 |
| penalty-1@6080 | `ipag+amu+amu` |  | 3 |
| penalty-1@8192 | `ipag+amuamu` |  | 2 |
| penalty-1@16384 | `ipag+amuamu` |  | 2 |
| penalty-2@6080 | `ipag+amu+amu` |  | 3 |
| penalty-2@8192 | `ipag+amuamu` |  | 2 |
| penalty-2@16384 | `ipag+amuamu` |  | 2 |
| penalty-4@6080 | `ipag+amu+amu` |  | 3 |
| penalty-4@8192 | `ipag+amuamu` |  | 2 |
| penalty-4@16384 | `ipag+amuamu` |  | 2 |
| penalty-8@6080 | `ipag+amu+amu` |  | 3 |
| penalty-8@8192 | `ipag+amuamu` |  | 2 |
| penalty-8@16384 | `ipag+amuamu` |  | 2 |
| stochastic-p4-d0.1@6080 | `ipag+amu+amu` |  | 3 |
| stochastic-p4-d0.1@8192 | `ipag+amu+amu` |  | 3 |
| stochastic-p4-d0.1@16384 | `ipag+amuamu` |  | 2 |
| stochastic-p4-d0.2@6080 | `ipag+amu+amu` |  | 3 |
| stochastic-p4-d0.2@8192 | `ipag+amu+amu` |  | 3 |
| stochastic-p4-d0.2@16384 | `ipag+amuamu` |  | 2 |
| unigram-ablation@6080 | `ipa+gamuamu` | OK | 2 |

## `makimut`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+kimut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mak+imut` |  | 2 |
| plain@8192 | `mak+imut` |  | 2 |
| plain@16384 | `mak+imut` |  | 2 |
| morphbpe@6080 | `mak+imut` |  | 2 |
| morphbpe@8192 | `mak+imut` |  | 2 |
| morphbpe@16384 | `mak+imut` |  | 2 |
| penalty-1@6080 | `mak+imut` |  | 2 |
| penalty-1@8192 | `mak+imut` |  | 2 |
| penalty-1@16384 | `mak+imut` |  | 2 |
| penalty-2@6080 | `mak+imut` |  | 2 |
| penalty-2@8192 | `mak+imut` |  | 2 |
| penalty-2@16384 | `mak+imut` |  | 2 |
| penalty-4@6080 | `maki+mut` |  | 2 |
| penalty-4@8192 | `maki+mut` |  | 2 |
| penalty-4@16384 | `maki+mut` |  | 2 |
| penalty-8@6080 | `maki+mut` |  | 2 |
| penalty-8@8192 | `maki+mut` |  | 2 |
| penalty-8@16384 | `maki+mut` |  | 2 |
| stochastic-p4-d0.1@6080 | `maki+mut` |  | 2 |
| stochastic-p4-d0.1@8192 | `maki+mut` |  | 2 |
| stochastic-p4-d0.1@16384 | `maki+mut` |  | 2 |
| stochastic-p4-d0.2@6080 | `maki+mut` |  | 2 |
| stochastic-p4-d0.2@8192 | `maki+mut` |  | 2 |
| stochastic-p4-d0.2@16384 | `maki+mut` |  | 2 |
| unigram-ablation@6080 | `ma+kimut` | OK | 2 |

## `makudta`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+kudta`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mak+ud+ta` |  | 3 |
| plain@8192 | `mak+udta` |  | 2 |
| plain@16384 | `makudta` |  | 1 |
| morphbpe@6080 | `mak+udta` |  | 2 |
| morphbpe@8192 | `mak+udta` |  | 2 |
| morphbpe@16384 | `makudta` |  | 1 |
| penalty-1@6080 | `ma+kud+ta` |  | 3 |
| penalty-1@8192 | `ma+kud+ta` |  | 3 |
| penalty-1@16384 | `makudta` |  | 1 |
| penalty-2@6080 | `ma+kud+ta` |  | 3 |
| penalty-2@8192 | `ma+kud+ta` |  | 3 |
| penalty-2@16384 | `makudta` |  | 1 |
| penalty-4@6080 | `ma+kud+ta` |  | 3 |
| penalty-4@8192 | `ma+kud+ta` |  | 3 |
| penalty-4@16384 | `makudta` |  | 1 |
| penalty-8@6080 | `ma+kud+ta` |  | 3 |
| penalty-8@8192 | `ma+kud+ta` |  | 3 |
| penalty-8@16384 | `makudta` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+kud+ta` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+kud+ta` |  | 3 |
| stochastic-p4-d0.1@16384 | `makudta` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+kud+ta` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+kud+ta` |  | 3 |
| stochastic-p4-d0.2@16384 | `makudta` |  | 1 |
| unigram-ablation@6080 | `ma+kudta` | OK | 2 |

## `malale`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+lale`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+ale` |  | 2 |
| plain@8192 | `mal+ale` |  | 2 |
| plain@16384 | `malale` |  | 1 |
| morphbpe@6080 | `mal+ale` |  | 2 |
| morphbpe@8192 | `mal+ale` |  | 2 |
| morphbpe@16384 | `malale` |  | 1 |
| penalty-1@6080 | `mal+ale` |  | 2 |
| penalty-1@8192 | `mal+ale` |  | 2 |
| penalty-1@16384 | `malale` |  | 1 |
| penalty-2@6080 | `mal+ale` |  | 2 |
| penalty-2@8192 | `mal+ale` |  | 2 |
| penalty-2@16384 | `malale` |  | 1 |
| penalty-4@6080 | `mal+ale` |  | 2 |
| penalty-4@8192 | `mal+ale` |  | 2 |
| penalty-4@16384 | `malale` |  | 1 |
| penalty-8@6080 | `ma+la+le` |  | 3 |
| penalty-8@8192 | `mala+le` |  | 2 |
| penalty-8@16384 | `malale` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+la+le` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+la+le` |  | 3 |
| stochastic-p4-d0.1@16384 | `malale` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+la+le` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+la+le` |  | 3 |
| stochastic-p4-d0.2@16384 | `malale` |  | 1 |
| unigram-ablation@6080 | `mala+le` |  | 2 |

## `manenaya`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+enaya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+en+aya` |  | 3 |
| plain@8192 | `man+enaya` | OK | 2 |
| plain@16384 | `manenaya` |  | 1 |
| morphbpe@6080 | `man+en+aya` |  | 3 |
| morphbpe@8192 | `man+enaya` | OK | 2 |
| morphbpe@16384 | `manenaya` |  | 1 |
| penalty-1@6080 | `man+en+aya` |  | 3 |
| penalty-1@8192 | `man+enaya` | OK | 2 |
| penalty-1@16384 | `manenaya` |  | 1 |
| penalty-2@6080 | `man+en+aya` |  | 3 |
| penalty-2@8192 | `man+enaya` | OK | 2 |
| penalty-2@16384 | `manenaya` |  | 1 |
| penalty-4@6080 | `man+en+aya` |  | 3 |
| penalty-4@8192 | `man+enaya` | OK | 2 |
| penalty-4@16384 | `manenaya` |  | 1 |
| penalty-8@6080 | `man+ena+ya` |  | 3 |
| penalty-8@8192 | `man+enaya` | OK | 2 |
| penalty-8@16384 | `manenaya` |  | 1 |
| stochastic-p4-d0.1@6080 | `man+en+aya` |  | 3 |
| stochastic-p4-d0.1@8192 | `manen+aya` |  | 2 |
| stochastic-p4-d0.1@16384 | `manenaya` |  | 1 |
| stochastic-p4-d0.2@6080 | `man+en+aya` |  | 3 |
| stochastic-p4-d0.2@8192 | `man+en+aya` |  | 3 |
| stochastic-p4-d0.2@16384 | `manenaya` |  | 1 |
| unigram-ablation@6080 | `manenaya` |  | 1 |

## `matalik`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+talik`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mat+alik` |  | 2 |
| plain@8192 | `mat+alik` |  | 2 |
| plain@16384 | `matalik` |  | 1 |
| morphbpe@6080 | `mat+alik` |  | 2 |
| morphbpe@8192 | `mat+alik` |  | 2 |
| morphbpe@16384 | `mat+alik` |  | 2 |
| penalty-1@6080 | `mat+alik` |  | 2 |
| penalty-1@8192 | `mat+alik` |  | 2 |
| penalty-1@16384 | `mat+alik` |  | 2 |
| penalty-2@6080 | `mat+alik` |  | 2 |
| penalty-2@8192 | `mat+alik` |  | 2 |
| penalty-2@16384 | `mat+alik` |  | 2 |
| penalty-4@6080 | `mat+alik` |  | 2 |
| penalty-4@8192 | `mat+alik` |  | 2 |
| penalty-4@16384 | `mat+alik` |  | 2 |
| penalty-8@6080 | `mat+alik` |  | 2 |
| penalty-8@8192 | `mat+alik` |  | 2 |
| penalty-8@16384 | `mat+alik` |  | 2 |
| stochastic-p4-d0.1@6080 | `mat+alik` |  | 2 |
| stochastic-p4-d0.1@8192 | `mat+alik` |  | 2 |
| stochastic-p4-d0.1@16384 | `mat+alik` |  | 2 |
| stochastic-p4-d0.2@6080 | `mat+alik` |  | 2 |
| stochastic-p4-d0.2@8192 | `mat+alik` |  | 2 |
| stochastic-p4-d0.2@16384 | `mat+alik` |  | 2 |
| unigram-ablation@6080 | `ma+talik` | OK | 2 |

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

## `pampanga`  (prefixation, tier A_strong_silver)

**silver gold:** `pam+panga`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pampang+a` |  | 2 |
| plain@8192 | `pampang+a` |  | 2 |
| plain@16384 | `pampang+a` |  | 2 |
| morphbpe@6080 | `pam+panga` | OK | 2 |
| morphbpe@8192 | `pam+panga` | OK | 2 |
| morphbpe@16384 | `pam+panga` | OK | 2 |
| penalty-1@6080 | `pam+panga` | OK | 2 |
| penalty-1@8192 | `pam+panga` | OK | 2 |
| penalty-1@16384 | `pam+panga` | OK | 2 |
| penalty-2@6080 | `pam+panga` | OK | 2 |
| penalty-2@8192 | `pam+panga` | OK | 2 |
| penalty-2@16384 | `pam+panga` | OK | 2 |
| penalty-4@6080 | `pam+panga` | OK | 2 |
| penalty-4@8192 | `pam+panga` | OK | 2 |
| penalty-4@16384 | `pam+panga` | OK | 2 |
| penalty-8@6080 | `pam+panga` | OK | 2 |
| penalty-8@8192 | `pam+panga` | OK | 2 |
| penalty-8@16384 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.1@6080 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.1@8192 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.1@16384 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.2@6080 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pam+panga` | OK | 2 |
| stochastic-p4-d0.2@16384 | `pam+panga` | OK | 2 |
| unigram-ablation@6080 | `pampang+a` |  | 2 |

## `pangamate`  (prefixation, tier A_strong_silver)

**silver gold:** `panga+mate`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pang+amate` |  | 2 |
| plain@8192 | `pangamate` |  | 1 |
| plain@16384 | `pangamate` |  | 1 |
| morphbpe@6080 | `pang+amate` |  | 2 |
| morphbpe@8192 | `pangamate` |  | 1 |
| morphbpe@16384 | `pangamate` |  | 1 |
| penalty-1@6080 | `pang+amate` |  | 2 |
| penalty-1@8192 | `pangamate` |  | 1 |
| penalty-1@16384 | `pangamate` |  | 1 |
| penalty-2@6080 | `pang+amate` |  | 2 |
| penalty-2@8192 | `pangamate` |  | 1 |
| penalty-2@16384 | `pangamate` |  | 1 |
| penalty-4@6080 | `pang+amate` |  | 2 |
| penalty-4@8192 | `pangamate` |  | 1 |
| penalty-4@16384 | `pangamate` |  | 1 |
| penalty-8@6080 | `pang+amate` |  | 2 |
| penalty-8@8192 | `pangamate` |  | 1 |
| penalty-8@16384 | `pangamate` |  | 1 |
| stochastic-p4-d0.1@6080 | `pang+amate` |  | 2 |
| stochastic-p4-d0.1@8192 | `pangamate` |  | 1 |
| stochastic-p4-d0.1@16384 | `pangamate` |  | 1 |
| stochastic-p4-d0.2@6080 | `pang+amate` |  | 2 |
| stochastic-p4-d0.2@8192 | `pangamate` |  | 1 |
| stochastic-p4-d0.2@16384 | `pangamate` |  | 1 |
| unigram-ablation@6080 | `panga+mate` | OK | 2 |

## `pantas`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pantas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pant+as` |  | 2 |
| plain@8192 | `pantas` | OK | 1 |
| plain@16384 | `pantas` | OK | 1 |
| morphbpe@6080 | `pan+tas` |  | 2 |
| morphbpe@8192 | `pan+tas` |  | 2 |
| morphbpe@16384 | `pan+tas` |  | 2 |
| penalty-1@6080 | `pan+tas` |  | 2 |
| penalty-1@8192 | `pan+tas` |  | 2 |
| penalty-1@16384 | `pan+tas` |  | 2 |
| penalty-2@6080 | `pan+tas` |  | 2 |
| penalty-2@8192 | `pan+tas` |  | 2 |
| penalty-2@16384 | `pan+tas` |  | 2 |
| penalty-4@6080 | `pan+tas` |  | 2 |
| penalty-4@8192 | `pan+tas` |  | 2 |
| penalty-4@16384 | `pan+tas` |  | 2 |
| penalty-8@6080 | `pan+tas` |  | 2 |
| penalty-8@8192 | `pan+tas` |  | 2 |
| penalty-8@16384 | `pan+tas` |  | 2 |
| stochastic-p4-d0.1@6080 | `pan+tas` |  | 2 |
| stochastic-p4-d0.1@8192 | `pan+tas` |  | 2 |
| stochastic-p4-d0.1@16384 | `pan+tas` |  | 2 |
| stochastic-p4-d0.2@6080 | `panta+s` |  | 2 |
| stochastic-p4-d0.2@8192 | `panta+s` |  | 2 |
| stochastic-p4-d0.2@16384 | `panta+s` |  | 2 |
| unigram-ablation@6080 | `pan+tas` |  | 2 |

## `ipasiag`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ipa+siag`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ip+asi+ag` |  | 3 |
| plain@8192 | `ip+asiag` |  | 2 |
| plain@16384 | `ip+asiag` |  | 2 |
| morphbpe@6080 | `ip+asi+ag` |  | 3 |
| morphbpe@8192 | `ip+asi+ag` |  | 3 |
| morphbpe@16384 | `ip+asiag` |  | 2 |
| penalty-1@6080 | `ip+asi+ag` |  | 3 |
| penalty-1@8192 | `ip+asi+ag` |  | 3 |
| penalty-1@16384 | `ip+asiag` |  | 2 |
| penalty-2@6080 | `ipa+siag` | OK | 2 |
| penalty-2@8192 | `ipa+siag` | OK | 2 |
| penalty-2@16384 | `ipa+siag` | OK | 2 |
| penalty-4@6080 | `i+pasi+ag` |  | 3 |
| penalty-4@8192 | `i+pasiag` |  | 2 |
| penalty-4@16384 | `i+pasiag` |  | 2 |
| penalty-8@6080 | `i+pasi+ag` |  | 3 |
| penalty-8@8192 | `i+pasiag` |  | 2 |
| penalty-8@16384 | `i+pasiag` |  | 2 |
| stochastic-p4-d0.1@6080 | `i+pasi+ag` |  | 3 |
| stochastic-p4-d0.1@8192 | `i+pasi+ag` |  | 3 |
| stochastic-p4-d0.1@16384 | `i+pasiag` |  | 2 |
| stochastic-p4-d0.2@6080 | `i+pasi+ag` |  | 3 |
| stochastic-p4-d0.2@8192 | `i+pasi+ag` |  | 3 |
| stochastic-p4-d0.2@16384 | `i+pasiag` |  | 2 |
| unigram-ablation@6080 | `i+pasiag` |  | 2 |

## `mangalambut`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+alambut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangal+ambut` |  | 2 |
| plain@8192 | `mangal+ambut` |  | 2 |
| plain@16384 | `mangal+ambut` |  | 2 |
| morphbpe@6080 | `mangal+ambut` |  | 2 |
| morphbpe@8192 | `mangal+ambut` |  | 2 |
| morphbpe@16384 | `mangal+ambut` |  | 2 |
| penalty-1@6080 | `mangal+ambut` |  | 2 |
| penalty-1@8192 | `mangal+ambut` |  | 2 |
| penalty-1@16384 | `mangal+ambut` |  | 2 |
| penalty-2@6080 | `mangal+ambut` |  | 2 |
| penalty-2@8192 | `mangal+ambut` |  | 2 |
| penalty-2@16384 | `mangal+ambut` |  | 2 |
| penalty-4@6080 | `mangal+ambut` |  | 2 |
| penalty-4@8192 | `mangal+ambut` |  | 2 |
| penalty-4@16384 | `mangal+ambut` |  | 2 |
| penalty-8@6080 | `mangala+m+but` |  | 3 |
| penalty-8@8192 | `mangala+m+but` |  | 3 |
| penalty-8@16384 | `mangala+mbut` |  | 2 |
| stochastic-p4-d0.1@6080 | `mang+alam+but` |  | 3 |
| stochastic-p4-d0.1@8192 | `mang+alam+but` |  | 3 |
| stochastic-p4-d0.1@16384 | `mang+alambut` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mangala+m+but` |  | 3 |
| stochastic-p4-d0.2@8192 | `mangala+m+but` |  | 3 |
| stochastic-p4-d0.2@16384 | `mangala+m+but` |  | 3 |
| unigram-ablation@6080 | `manga+lambut` |  | 2 |

## `maniaman`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+iaman`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mani+aman` |  | 2 |
| plain@8192 | `mani+aman` |  | 2 |
| plain@16384 | `maniaman` |  | 1 |
| morphbpe@6080 | `mani+aman` |  | 2 |
| morphbpe@8192 | `maniaman` |  | 1 |
| morphbpe@16384 | `maniaman` |  | 1 |
| penalty-1@6080 | `mani+aman` |  | 2 |
| penalty-1@8192 | `maniaman` |  | 1 |
| penalty-1@16384 | `maniaman` |  | 1 |
| penalty-2@6080 | `mani+aman` |  | 2 |
| penalty-2@8192 | `maniaman` |  | 1 |
| penalty-2@16384 | `maniaman` |  | 1 |
| penalty-4@6080 | `mani+aman` |  | 2 |
| penalty-4@8192 | `maniaman` |  | 1 |
| penalty-4@16384 | `maniaman` |  | 1 |
| penalty-8@6080 | `mani+aman` |  | 2 |
| penalty-8@8192 | `maniaman` |  | 1 |
| penalty-8@16384 | `maniaman` |  | 1 |
| stochastic-p4-d0.1@6080 | `mani+aman` |  | 2 |
| stochastic-p4-d0.1@8192 | `mani+aman` |  | 2 |
| stochastic-p4-d0.1@16384 | `maniaman` |  | 1 |
| stochastic-p4-d0.2@6080 | `mani+aman` |  | 2 |
| stochastic-p4-d0.2@8192 | `mani+aman` |  | 2 |
| stochastic-p4-d0.2@16384 | `maniaman` |  | 1 |
| unigram-ablation@6080 | `maniaman` |  | 1 |

## `mantabe`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+tabe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+t+abe` |  | 3 |
| plain@8192 | `mant+abe` |  | 2 |
| plain@16384 | `mantabe` |  | 1 |
| morphbpe@6080 | `man+t+abe` |  | 3 |
| morphbpe@8192 | `mant+abe` |  | 2 |
| morphbpe@16384 | `mantabe` |  | 1 |
| penalty-1@6080 | `man+t+abe` |  | 3 |
| penalty-1@8192 | `mant+abe` |  | 2 |
| penalty-1@16384 | `mantabe` |  | 1 |
| penalty-2@6080 | `man+tabe` | OK | 2 |
| penalty-2@8192 | `man+tabe` | OK | 2 |
| penalty-2@16384 | `mantabe` |  | 1 |
| penalty-4@6080 | `man+tabe` | OK | 2 |
| penalty-4@8192 | `man+tabe` | OK | 2 |
| penalty-4@16384 | `mantabe` |  | 1 |
| penalty-8@6080 | `man+tabe` | OK | 2 |
| penalty-8@8192 | `man+tabe` | OK | 2 |
| penalty-8@16384 | `mantabe` |  | 1 |
| stochastic-p4-d0.1@6080 | `man+tabe` | OK | 2 |
| stochastic-p4-d0.1@8192 | `man+tabe` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mantabe` |  | 1 |
| stochastic-p4-d0.2@6080 | `man+ta+be` |  | 3 |
| stochastic-p4-d0.2@8192 | `man+tabe` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mantabe` |  | 1 |
| unigram-ablation@6080 | `m+antabe` |  | 2 |

## `mengari`  (prefixation, tier B_moderate_silver)

**silver gold:** `men+gari`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `meng+ari` |  | 2 |
| plain@8192 | `meng+ari` |  | 2 |
| plain@16384 | `mengari` |  | 1 |
| morphbpe@6080 | `meng+ari` |  | 2 |
| morphbpe@8192 | `meng+ari` |  | 2 |
| morphbpe@16384 | `meng+ari` |  | 2 |
| penalty-1@6080 | `meng+ari` |  | 2 |
| penalty-1@8192 | `meng+ari` |  | 2 |
| penalty-1@16384 | `meng+ari` |  | 2 |
| penalty-2@6080 | `meng+ari` |  | 2 |
| penalty-2@8192 | `meng+ari` |  | 2 |
| penalty-2@16384 | `meng+ari` |  | 2 |
| penalty-4@6080 | `meng+ari` |  | 2 |
| penalty-4@8192 | `meng+ari` |  | 2 |
| penalty-4@16384 | `meng+ari` |  | 2 |
| penalty-8@6080 | `meng+ari` |  | 2 |
| penalty-8@8192 | `meng+ari` |  | 2 |
| penalty-8@16384 | `meng+ari` |  | 2 |
| stochastic-p4-d0.1@6080 | `meng+ari` |  | 2 |
| stochastic-p4-d0.1@8192 | `meng+ari` |  | 2 |
| stochastic-p4-d0.1@16384 | `meng+ari` |  | 2 |
| stochastic-p4-d0.2@6080 | `me+ng+ari` |  | 3 |
| stochastic-p4-d0.2@8192 | `me+ng+ari` |  | 3 |
| stochastic-p4-d0.2@16384 | `me+ng+ari` |  | 3 |
| unigram-ablation@6080 | `menga+ri` |  | 2 |

## `malipul`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+lipul`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+ip+ul` |  | 3 |
| plain@8192 | `mal+ip+ul` |  | 3 |
| plain@16384 | `mal+ipul` |  | 2 |
| morphbpe@6080 | `mal+ip+ul` |  | 3 |
| morphbpe@8192 | `mal+ip+ul` |  | 3 |
| morphbpe@16384 | `mal+ipul` |  | 2 |
| penalty-1@6080 | `mal+ip+ul` |  | 3 |
| penalty-1@8192 | `mal+ip+ul` |  | 3 |
| penalty-1@16384 | `mal+ip+ul` |  | 3 |
| penalty-2@6080 | `mal+ip+ul` |  | 3 |
| penalty-2@8192 | `mal+ip+ul` |  | 3 |
| penalty-2@16384 | `mal+ip+ul` |  | 3 |
| penalty-4@6080 | `mal+ip+ul` |  | 3 |
| penalty-4@8192 | `mal+ip+ul` |  | 3 |
| penalty-4@16384 | `mal+ip+ul` |  | 3 |
| penalty-8@6080 | `m+ali+pul` |  | 3 |
| penalty-8@8192 | `m+ali+pul` |  | 3 |
| penalty-8@16384 | `m+ali+pul` |  | 3 |
| stochastic-p4-d0.1@6080 | `mali+pul` |  | 2 |
| stochastic-p4-d0.1@8192 | `mali+pul` |  | 2 |
| stochastic-p4-d0.1@16384 | `mali+pul` |  | 2 |
| stochastic-p4-d0.2@6080 | `mali+pul` |  | 2 |
| stochastic-p4-d0.2@8192 | `mali+pul` |  | 2 |
| stochastic-p4-d0.2@16384 | `mali+pul` |  | 2 |
| unigram-ablation@6080 | `mali+pul` |  | 2 |

## `malunus`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lunus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+unus` |  | 2 |
| plain@8192 | `mal+unus` |  | 2 |
| plain@16384 | `malunus` |  | 1 |
| morphbpe@6080 | `mal+un+us` |  | 3 |
| morphbpe@8192 | `mal+unus` |  | 2 |
| morphbpe@16384 | `mal+unus` |  | 2 |
| penalty-1@6080 | `mal+un+us` |  | 3 |
| penalty-1@8192 | `mal+un+us` |  | 3 |
| penalty-1@16384 | `mal+unus` |  | 2 |
| penalty-2@6080 | `mal+un+us` |  | 3 |
| penalty-2@8192 | `mal+unus` |  | 2 |
| penalty-2@16384 | `mal+unus` |  | 2 |
| penalty-4@6080 | `mal+un+us` |  | 3 |
| penalty-4@8192 | `mal+unus` |  | 2 |
| penalty-4@16384 | `mal+unus` |  | 2 |
| penalty-8@6080 | `mal+un+us` |  | 3 |
| penalty-8@8192 | `mal+un+us` |  | 3 |
| penalty-8@16384 | `mal+unus` |  | 2 |
| stochastic-p4-d0.1@6080 | `mal+un+us` |  | 3 |
| stochastic-p4-d0.1@8192 | `mal+unus` |  | 2 |
| stochastic-p4-d0.1@16384 | `mal+unus` |  | 2 |
| stochastic-p4-d0.2@6080 | `mal+un+us` |  | 3 |
| stochastic-p4-d0.2@8192 | `mal+un+us` |  | 3 |
| stochastic-p4-d0.2@16384 | `malun+us` |  | 2 |
| unigram-ablation@6080 | `ma+lunus` | OK | 2 |

## `mangga`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+ngga`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangga` |  | 1 |
| plain@8192 | `mangga` |  | 1 |
| plain@16384 | `mangga` |  | 1 |
| morphbpe@6080 | `mangga` |  | 1 |
| morphbpe@8192 | `mangga` |  | 1 |
| morphbpe@16384 | `mangga` |  | 1 |
| penalty-1@6080 | `mangga` |  | 1 |
| penalty-1@8192 | `mangga` |  | 1 |
| penalty-1@16384 | `mangga` |  | 1 |
| penalty-2@6080 | `mangga` |  | 1 |
| penalty-2@8192 | `mangga` |  | 1 |
| penalty-2@16384 | `mangga` |  | 1 |
| penalty-4@6080 | `mangga` |  | 1 |
| penalty-4@8192 | `mangga` |  | 1 |
| penalty-4@16384 | `mangga` |  | 1 |
| penalty-8@6080 | `mangga` |  | 1 |
| penalty-8@8192 | `mangga` |  | 1 |
| penalty-8@16384 | `mangga` |  | 1 |
| stochastic-p4-d0.1@6080 | `mangga` |  | 1 |
| stochastic-p4-d0.1@8192 | `mangga` |  | 1 |
| stochastic-p4-d0.1@16384 | `mangga` |  | 1 |
| stochastic-p4-d0.2@6080 | `mangga` |  | 1 |
| stochastic-p4-d0.2@8192 | `mangga` |  | 1 |
| stochastic-p4-d0.2@16384 | `mangga` |  | 1 |
| unigram-ablation@6080 | `mangga` |  | 1 |

## `marapat`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rapat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mar+apat` |  | 2 |
| plain@8192 | `marapat` |  | 1 |
| plain@16384 | `marapat` |  | 1 |
| morphbpe@6080 | `mar+apat` |  | 2 |
| morphbpe@8192 | `marapat` |  | 1 |
| morphbpe@16384 | `marapat` |  | 1 |
| penalty-1@6080 | `ma+rapat` | OK | 2 |
| penalty-1@8192 | `marapat` |  | 1 |
| penalty-1@16384 | `marapat` |  | 1 |
| penalty-2@6080 | `ma+rapat` | OK | 2 |
| penalty-2@8192 | `marapat` |  | 1 |
| penalty-2@16384 | `marapat` |  | 1 |
| penalty-4@6080 | `mara+pat` |  | 2 |
| penalty-4@8192 | `marapat` |  | 1 |
| penalty-4@16384 | `marapat` |  | 1 |
| penalty-8@6080 | `ma+rapat` | OK | 2 |
| penalty-8@8192 | `marapat` |  | 1 |
| penalty-8@16384 | `marapat` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+rapat` | OK | 2 |
| stochastic-p4-d0.1@8192 | `marapat` |  | 1 |
| stochastic-p4-d0.1@16384 | `marapat` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+rapat` | OK | 2 |
| stochastic-p4-d0.2@8192 | `marapat` |  | 1 |
| stochastic-p4-d0.2@16384 | `marapat` |  | 1 |
| unigram-ablation@6080 | `m+arapat` |  | 2 |

## `masias`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+sias`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ias` |  | 2 |
| plain@8192 | `mas+ias` |  | 2 |
| plain@16384 | `masias` |  | 1 |
| morphbpe@6080 | `masi+as` |  | 2 |
| morphbpe@8192 | `masi+as` |  | 2 |
| morphbpe@16384 | `masias` |  | 1 |
| penalty-1@6080 | `mas+ias` |  | 2 |
| penalty-1@8192 | `mas+ias` |  | 2 |
| penalty-1@16384 | `masias` |  | 1 |
| penalty-2@6080 | `masi+as` |  | 2 |
| penalty-2@8192 | `masi+as` |  | 2 |
| penalty-2@16384 | `masias` |  | 1 |
| penalty-4@6080 | `ma+si+as` |  | 3 |
| penalty-4@8192 | `masi+as` |  | 2 |
| penalty-4@16384 | `masias` |  | 1 |
| penalty-8@6080 | `ma+sias` | OK | 2 |
| penalty-8@8192 | `ma+sias` | OK | 2 |
| penalty-8@16384 | `masias` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+si+as` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+sias` | OK | 2 |
| stochastic-p4-d0.1@16384 | `masias` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+sias` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+sias` | OK | 2 |
| stochastic-p4-d0.2@16384 | `masias` |  | 1 |
| unigram-ablation@6080 | `mas+ias` |  | 2 |

## `mekamate`  (prefixation, tier A_strong_silver)

**silver gold:** `meka+mate`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `me+kamat+e` |  | 3 |
| plain@8192 | `me+kamat+e` |  | 3 |
| plain@16384 | `me+kamate` |  | 2 |
| morphbpe@6080 | `me+kamat+e` |  | 3 |
| morphbpe@8192 | `me+kamat+e` |  | 3 |
| morphbpe@16384 | `me+kamat+e` |  | 3 |
| penalty-1@6080 | `meka+mate` | OK | 2 |
| penalty-1@8192 | `meka+mate` | OK | 2 |
| penalty-1@16384 | `meka+mate` | OK | 2 |
| penalty-2@6080 | `meka+mate` | OK | 2 |
| penalty-2@8192 | `meka+mate` | OK | 2 |
| penalty-2@16384 | `meka+mate` | OK | 2 |
| penalty-4@6080 | `meka+mate` | OK | 2 |
| penalty-4@8192 | `meka+mate` | OK | 2 |
| penalty-4@16384 | `meka+mate` | OK | 2 |
| penalty-8@6080 | `meka+mate` | OK | 2 |
| penalty-8@8192 | `meka+mate` | OK | 2 |
| penalty-8@16384 | `meka+mate` | OK | 2 |
| stochastic-p4-d0.1@6080 | `meka+mat+e` |  | 3 |
| stochastic-p4-d0.1@8192 | `meka+mat+e` |  | 3 |
| stochastic-p4-d0.1@16384 | `meka+mat+e` |  | 3 |
| stochastic-p4-d0.2@6080 | `meka+mate` | OK | 2 |
| stochastic-p4-d0.2@8192 | `meka+mate` | OK | 2 |
| stochastic-p4-d0.2@16384 | `meka+mate` | OK | 2 |
| unigram-ablation@6080 | `meka+mate` | OK | 2 |

## `patingapun`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+tingapun`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pat+ing+apun` |  | 3 |
| plain@8192 | `pat+ing+apun` |  | 3 |
| plain@16384 | `patingapun` |  | 1 |
| morphbpe@6080 | `pat+ing+apun` |  | 3 |
| morphbpe@8192 | `pating+apun` |  | 2 |
| morphbpe@16384 | `patingapun` |  | 1 |
| penalty-1@6080 | `pat+ing+apun` |  | 3 |
| penalty-1@8192 | `pating+apun` |  | 2 |
| penalty-1@16384 | `patingapun` |  | 1 |
| penalty-2@6080 | `pat+ing+apun` |  | 3 |
| penalty-2@8192 | `pating+apun` |  | 2 |
| penalty-2@16384 | `patingapun` |  | 1 |
| penalty-4@6080 | `pat+ing+apun` |  | 3 |
| penalty-4@8192 | `pating+apun` |  | 2 |
| penalty-4@16384 | `patingapun` |  | 1 |
| penalty-8@6080 | `pat+ing+apun` |  | 3 |
| penalty-8@8192 | `pating+apun` |  | 2 |
| penalty-8@16384 | `patingapun` |  | 1 |
| stochastic-p4-d0.1@6080 | `pati+ng+apun` |  | 3 |
| stochastic-p4-d0.1@8192 | `pati+ng+apun` |  | 3 |
| stochastic-p4-d0.1@16384 | `patingapun` |  | 1 |
| stochastic-p4-d0.2@6080 | `pati+ng+apun` |  | 3 |
| stochastic-p4-d0.2@8192 | `pati+ng+apun` |  | 3 |
| stochastic-p4-d0.2@16384 | `patingapun` |  | 1 |
| unigram-ablation@6080 | `patingapun` |  | 1 |

## `pibatan`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pi+bata+n`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `p+ibatan` |  | 2 |
| plain@8192 | `p+ibatan` |  | 2 |
| plain@16384 | `pibatan` |  | 1 |
| morphbpe@6080 | `p+ibatan` |  | 2 |
| morphbpe@8192 | `p+ibatan` |  | 2 |
| morphbpe@16384 | `p+ibatan` |  | 2 |
| penalty-1@6080 | `p+ibat+an` |  | 3 |
| penalty-1@8192 | `p+ibat+an` |  | 3 |
| penalty-1@16384 | `p+ibat+an` |  | 3 |
| penalty-2@6080 | `p+ibat+an` |  | 3 |
| penalty-2@8192 | `p+ibat+an` |  | 3 |
| penalty-2@16384 | `p+ibat+an` |  | 3 |
| penalty-4@6080 | `p+ibat+an` |  | 3 |
| penalty-4@8192 | `p+ibat+an` |  | 3 |
| penalty-4@16384 | `p+ibat+an` |  | 3 |
| penalty-8@6080 | `pi+bat+an` |  | 3 |
| penalty-8@8192 | `pi+bat+an` |  | 3 |
| penalty-8@16384 | `pi+bat+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `pi+bat+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `pi+bat+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `pi+bat+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `pi+batan` |  | 2 |
| stochastic-p4-d0.2@8192 | `pi+batan` |  | 2 |
| stochastic-p4-d0.2@16384 | `pi+batan` |  | 2 |
| unigram-ablation@6080 | `pibata+n` |  | 2 |

## `magbili`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+bili`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+bili` | OK | 2 |
| plain@8192 | `mag+bili` | OK | 2 |
| plain@16384 | `mag+bili` | OK | 2 |
| morphbpe@6080 | `mag+bili` | OK | 2 |
| morphbpe@8192 | `mag+bili` | OK | 2 |
| morphbpe@16384 | `mag+bili` | OK | 2 |
| penalty-1@6080 | `mag+bili` | OK | 2 |
| penalty-1@8192 | `mag+bili` | OK | 2 |
| penalty-1@16384 | `mag+bili` | OK | 2 |
| penalty-2@6080 | `mag+bili` | OK | 2 |
| penalty-2@8192 | `mag+bili` | OK | 2 |
| penalty-2@16384 | `mag+bili` | OK | 2 |
| penalty-4@6080 | `mag+bili` | OK | 2 |
| penalty-4@8192 | `mag+bili` | OK | 2 |
| penalty-4@16384 | `mag+bili` | OK | 2 |
| penalty-8@6080 | `mag+bili` | OK | 2 |
| penalty-8@8192 | `mag+bili` | OK | 2 |
| penalty-8@16384 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mag+bili` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mag+bili` | OK | 2 |
| unigram-ablation@6080 | `mag+bili` | OK | 2 |

## `makasulat`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+sulat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makasulat` |  | 1 |
| plain@8192 | `makasulat` |  | 1 |
| plain@16384 | `makasulat` |  | 1 |
| morphbpe@6080 | `maka+sulat` | OK | 2 |
| morphbpe@8192 | `maka+sulat` | OK | 2 |
| morphbpe@16384 | `maka+sulat` | OK | 2 |
| penalty-1@6080 | `maka+sulat` | OK | 2 |
| penalty-1@8192 | `maka+sulat` | OK | 2 |
| penalty-1@16384 | `maka+sulat` | OK | 2 |
| penalty-2@6080 | `maka+sulat` | OK | 2 |
| penalty-2@8192 | `maka+sulat` | OK | 2 |
| penalty-2@16384 | `maka+sulat` | OK | 2 |
| penalty-4@6080 | `maka+sulat` | OK | 2 |
| penalty-4@8192 | `maka+sulat` | OK | 2 |
| penalty-4@16384 | `maka+sulat` | OK | 2 |
| penalty-8@6080 | `maka+sulat` | OK | 2 |
| penalty-8@8192 | `maka+sulat` | OK | 2 |
| penalty-8@16384 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+sulat` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+sulat` | OK | 2 |
| unigram-ablation@6080 | `ma+kasulat` |  | 2 |

## `makibalu`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+kibalu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makib+alu` |  | 2 |
| plain@8192 | `makib+alu` |  | 2 |
| plain@16384 | `makibalu` |  | 1 |
| morphbpe@6080 | `mak+ib+alu` |  | 3 |
| morphbpe@8192 | `mak+ib+alu` |  | 3 |
| morphbpe@16384 | `mak+ib+alu` |  | 3 |
| penalty-1@6080 | `maki+balu` |  | 2 |
| penalty-1@8192 | `maki+balu` |  | 2 |
| penalty-1@16384 | `maki+balu` |  | 2 |
| penalty-2@6080 | `maki+balu` |  | 2 |
| penalty-2@8192 | `maki+balu` |  | 2 |
| penalty-2@16384 | `maki+balu` |  | 2 |
| penalty-4@6080 | `maki+balu` |  | 2 |
| penalty-4@8192 | `maki+balu` |  | 2 |
| penalty-4@16384 | `maki+balu` |  | 2 |
| penalty-8@6080 | `maki+balu` |  | 2 |
| penalty-8@8192 | `maki+balu` |  | 2 |
| penalty-8@16384 | `maki+balu` |  | 2 |
| stochastic-p4-d0.1@6080 | `maki+balu` |  | 2 |
| stochastic-p4-d0.1@8192 | `maki+balu` |  | 2 |
| stochastic-p4-d0.1@16384 | `maki+balu` |  | 2 |
| stochastic-p4-d0.2@6080 | `maki+balu` |  | 2 |
| stochastic-p4-d0.2@8192 | `maki+balu` |  | 2 |
| stochastic-p4-d0.2@16384 | `maki+balu` |  | 2 |
| unigram-ablation@6080 | `maki+balu` |  | 2 |

## `makule`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+kule`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mak+ule` |  | 2 |
| plain@8192 | `mak+ule` |  | 2 |
| plain@16384 | `makule` |  | 1 |
| morphbpe@6080 | `mak+ule` |  | 2 |
| morphbpe@8192 | `mak+ule` |  | 2 |
| morphbpe@16384 | `makule` |  | 1 |
| penalty-1@6080 | `mak+ule` |  | 2 |
| penalty-1@8192 | `mak+ule` |  | 2 |
| penalty-1@16384 | `makule` |  | 1 |
| penalty-2@6080 | `ma+kule` | OK | 2 |
| penalty-2@8192 | `ma+kule` | OK | 2 |
| penalty-2@16384 | `makule` |  | 1 |
| penalty-4@6080 | `ma+kule` | OK | 2 |
| penalty-4@8192 | `ma+kule` | OK | 2 |
| penalty-4@16384 | `makule` |  | 1 |
| penalty-8@6080 | `ma+kule` | OK | 2 |
| penalty-8@8192 | `ma+kule` | OK | 2 |
| penalty-8@16384 | `makule` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+kule` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+kule` | OK | 2 |
| stochastic-p4-d0.1@16384 | `makule` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+ku+le` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+ku+le` |  | 3 |
| stochastic-p4-d0.2@16384 | `makule` |  | 1 |
| unigram-ablation@6080 | `ma+kule` | OK | 2 |

## `malambut`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lambut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+ambut` |  | 2 |
| plain@8192 | `mal+ambut` |  | 2 |
| plain@16384 | `malambut` |  | 1 |
| morphbpe@6080 | `mal+ambut` |  | 2 |
| morphbpe@8192 | `mal+ambut` |  | 2 |
| morphbpe@16384 | `malambut` |  | 1 |
| penalty-1@6080 | `mal+ambut` |  | 2 |
| penalty-1@8192 | `mal+ambut` |  | 2 |
| penalty-1@16384 | `malambut` |  | 1 |
| penalty-2@6080 | `mal+ambut` |  | 2 |
| penalty-2@8192 | `mal+ambut` |  | 2 |
| penalty-2@16384 | `malambut` |  | 1 |
| penalty-4@6080 | `mal+ambut` |  | 2 |
| penalty-4@8192 | `mal+ambut` |  | 2 |
| penalty-4@16384 | `malambut` |  | 1 |
| penalty-8@6080 | `ma+lam+but` |  | 3 |
| penalty-8@8192 | `ma+lambut` | OK | 2 |
| penalty-8@16384 | `malambut` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+lam+but` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+lam+but` |  | 3 |
| stochastic-p4-d0.1@16384 | `malambut` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+lam+but` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+lambut` | OK | 2 |
| stochastic-p4-d0.2@16384 | `malambut` |  | 1 |
| unigram-ablation@6080 | `ma+lambut` | OK | 2 |

## `malungkut`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lungkut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mal+ungkut` |  | 2 |
| plain@8192 | `mal+ungkut` |  | 2 |
| plain@16384 | `malungkut` |  | 1 |
| morphbpe@6080 | `mal+ung+kut` |  | 3 |
| morphbpe@8192 | `mal+ung+kut` |  | 3 |
| morphbpe@16384 | `mal+ung+kut` |  | 3 |
| penalty-1@6080 | `mal+ung+kut` |  | 3 |
| penalty-1@8192 | `mal+ung+kut` |  | 3 |
| penalty-1@16384 | `mal+ung+kut` |  | 3 |
| penalty-2@6080 | `mal+ung+kut` |  | 3 |
| penalty-2@8192 | `mal+ung+kut` |  | 3 |
| penalty-2@16384 | `mal+ung+kut` |  | 3 |
| penalty-4@6080 | `mal+ung+kut` |  | 3 |
| penalty-4@8192 | `mal+ung+kut` |  | 3 |
| penalty-4@16384 | `mal+ung+kut` |  | 3 |
| penalty-8@6080 | `mal+ung+kut` |  | 3 |
| penalty-8@8192 | `mal+ung+kut` |  | 3 |
| penalty-8@16384 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.1@6080 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.1@8192 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.1@16384 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.2@6080 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.2@8192 | `mal+ung+kut` |  | 3 |
| stochastic-p4-d0.2@16384 | `mal+ung+kut` |  | 3 |
| unigram-ablation@6080 | `ma+lungkut` | OK | 2 |

## `manganak`  (prefixation, tier A_strong_silver)

**silver gold:** `mang+anak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mangan+ak` |  | 2 |
| plain@8192 | `mangan+ak` |  | 2 |
| plain@16384 | `manganak` |  | 1 |
| morphbpe@6080 | `mang+anak` | OK | 2 |
| morphbpe@8192 | `mang+anak` | OK | 2 |
| morphbpe@16384 | `mang+anak` | OK | 2 |
| penalty-1@6080 | `mang+anak` | OK | 2 |
| penalty-1@8192 | `mang+anak` | OK | 2 |
| penalty-1@16384 | `mang+anak` | OK | 2 |
| penalty-2@6080 | `mang+anak` | OK | 2 |
| penalty-2@8192 | `mang+anak` | OK | 2 |
| penalty-2@16384 | `mang+anak` | OK | 2 |
| penalty-4@6080 | `mang+anak` | OK | 2 |
| penalty-4@8192 | `mang+anak` | OK | 2 |
| penalty-4@16384 | `mang+anak` | OK | 2 |
| penalty-8@6080 | `mang+anak` | OK | 2 |
| penalty-8@8192 | `mang+anak` | OK | 2 |
| penalty-8@16384 | `mang+anak` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mang+anak` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mang+anak` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mang+anak` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mangan+ak` |  | 2 |
| stochastic-p4-d0.2@8192 | `mangan+ak` |  | 2 |
| stochastic-p4-d0.2@16384 | `mangan+ak` |  | 2 |
| unigram-ablation@6080 | `mang+anak` | OK | 2 |

## `marangal`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+rangal`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `marang+al` |  | 2 |
| plain@8192 | `marangal` |  | 1 |
| plain@16384 | `marangal` |  | 1 |
| morphbpe@6080 | `marangal` |  | 1 |
| morphbpe@8192 | `marangal` |  | 1 |
| morphbpe@16384 | `marangal` |  | 1 |
| penalty-1@6080 | `marangal` |  | 1 |
| penalty-1@8192 | `marangal` |  | 1 |
| penalty-1@16384 | `marangal` |  | 1 |
| penalty-2@6080 | `marangal` |  | 1 |
| penalty-2@8192 | `marangal` |  | 1 |
| penalty-2@16384 | `marangal` |  | 1 |
| penalty-4@6080 | `marangal` |  | 1 |
| penalty-4@8192 | `marangal` |  | 1 |
| penalty-4@16384 | `marangal` |  | 1 |
| penalty-8@6080 | `marangal` |  | 1 |
| penalty-8@8192 | `marangal` |  | 1 |
| penalty-8@16384 | `marangal` |  | 1 |
| stochastic-p4-d0.1@6080 | `marangal` |  | 1 |
| stochastic-p4-d0.1@8192 | `marangal` |  | 1 |
| stochastic-p4-d0.1@16384 | `marangal` |  | 1 |
| stochastic-p4-d0.2@6080 | `marang+al` |  | 2 |
| stochastic-p4-d0.2@8192 | `marangal` |  | 1 |
| stochastic-p4-d0.2@16384 | `marangal` |  | 1 |
| unigram-ablation@6080 | `marangal` |  | 1 |

## `masipag`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+sipag`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ipag` |  | 2 |
| plain@8192 | `mas+ipag` |  | 2 |
| plain@16384 | `masipag` |  | 1 |
| morphbpe@6080 | `mas+ipag` |  | 2 |
| morphbpe@8192 | `mas+ipag` |  | 2 |
| morphbpe@16384 | `mas+ipag` |  | 2 |
| penalty-1@6080 | `mas+ipag` |  | 2 |
| penalty-1@8192 | `mas+ipag` |  | 2 |
| penalty-1@16384 | `mas+ipag` |  | 2 |
| penalty-2@6080 | `ma+sipag` | OK | 2 |
| penalty-2@8192 | `ma+sipag` | OK | 2 |
| penalty-2@16384 | `ma+sipag` | OK | 2 |
| penalty-4@6080 | `ma+si+pag` |  | 3 |
| penalty-4@8192 | `ma+sipag` | OK | 2 |
| penalty-4@16384 | `ma+sipag` | OK | 2 |
| penalty-8@6080 | `ma+sipag` | OK | 2 |
| penalty-8@8192 | `ma+sipag` | OK | 2 |
| penalty-8@16384 | `ma+sipag` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+si+pag` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+sipag` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+sipag` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+si+pag` |  | 3 |
| stochastic-p4-d0.2@8192 | `ma+si+pag` |  | 3 |
| stochastic-p4-d0.2@16384 | `ma+sipag` | OK | 2 |
| unigram-ablation@6080 | `ma+sipag` | OK | 2 |

## `matuling`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+tuling`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mat+uling` |  | 2 |
| plain@8192 | `matuling` |  | 1 |
| plain@16384 | `matuling` |  | 1 |
| morphbpe@6080 | `mat+uling` |  | 2 |
| morphbpe@8192 | `matuling` |  | 1 |
| morphbpe@16384 | `matuling` |  | 1 |
| penalty-1@6080 | `mat+uling` |  | 2 |
| penalty-1@8192 | `matuling` |  | 1 |
| penalty-1@16384 | `matuling` |  | 1 |
| penalty-2@6080 | `mat+uling` |  | 2 |
| penalty-2@8192 | `matuling` |  | 1 |
| penalty-2@16384 | `matuling` |  | 1 |
| penalty-4@6080 | `mat+uling` |  | 2 |
| penalty-4@8192 | `matuling` |  | 1 |
| penalty-4@16384 | `matuling` |  | 1 |
| penalty-8@6080 | `mat+uling` |  | 2 |
| penalty-8@8192 | `matuling` |  | 1 |
| penalty-8@16384 | `matuling` |  | 1 |
| stochastic-p4-d0.1@6080 | `mat+uli+ng` |  | 3 |
| stochastic-p4-d0.1@8192 | `matuling` |  | 1 |
| stochastic-p4-d0.1@16384 | `matuling` |  | 1 |
| stochastic-p4-d0.2@6080 | `mat+uli+ng` |  | 3 |
| stochastic-p4-d0.2@8192 | `matuling` |  | 1 |
| stochastic-p4-d0.2@16384 | `matuling` |  | 1 |
| unigram-ablation@6080 | `matuli+ng` |  | 2 |

## `menalig`  (prefixation, tier B_moderate_silver)

**silver gold:** `men+alig`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `men+alig` | OK | 2 |
| plain@8192 | `men+alig` | OK | 2 |
| plain@16384 | `men+alig` | OK | 2 |
| morphbpe@6080 | `men+alig` | OK | 2 |
| morphbpe@8192 | `men+alig` | OK | 2 |
| morphbpe@16384 | `men+alig` | OK | 2 |
| penalty-1@6080 | `men+alig` | OK | 2 |
| penalty-1@8192 | `men+alig` | OK | 2 |
| penalty-1@16384 | `men+alig` | OK | 2 |
| penalty-2@6080 | `men+alig` | OK | 2 |
| penalty-2@8192 | `men+alig` | OK | 2 |
| penalty-2@16384 | `men+alig` | OK | 2 |
| penalty-4@6080 | `men+alig` | OK | 2 |
| penalty-4@8192 | `men+alig` | OK | 2 |
| penalty-4@16384 | `men+alig` | OK | 2 |
| penalty-8@6080 | `men+alig` | OK | 2 |
| penalty-8@8192 | `men+alig` | OK | 2 |
| penalty-8@16384 | `men+alig` | OK | 2 |
| stochastic-p4-d0.1@6080 | `men+alig` | OK | 2 |
| stochastic-p4-d0.1@8192 | `men+alig` | OK | 2 |
| stochastic-p4-d0.1@16384 | `men+alig` | OK | 2 |
| stochastic-p4-d0.2@6080 | `men+alig` | OK | 2 |
| stochastic-p4-d0.2@8192 | `men+alig` | OK | 2 |
| stochastic-p4-d0.2@16384 | `men+alig` | OK | 2 |
| unigram-ablation@6080 | `me+na+lig` |  | 3 |

## `menatili`  (prefixation, tier B_moderate_silver)

**silver gold:** `men+atili`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `men+atili` | OK | 2 |
| plain@8192 | `men+atili` | OK | 2 |
| plain@16384 | `menatili` |  | 1 |
| morphbpe@6080 | `men+atili` | OK | 2 |
| morphbpe@8192 | `menatili` |  | 1 |
| morphbpe@16384 | `menatili` |  | 1 |
| penalty-1@6080 | `men+atili` | OK | 2 |
| penalty-1@8192 | `menatili` |  | 1 |
| penalty-1@16384 | `menatili` |  | 1 |
| penalty-2@6080 | `men+atili` | OK | 2 |
| penalty-2@8192 | `menatili` |  | 1 |
| penalty-2@16384 | `menatili` |  | 1 |
| penalty-4@6080 | `men+atili` | OK | 2 |
| penalty-4@8192 | `menatili` |  | 1 |
| penalty-4@16384 | `menatili` |  | 1 |
| penalty-8@6080 | `men+atili` | OK | 2 |
| penalty-8@8192 | `menatili` |  | 1 |
| penalty-8@16384 | `menatili` |  | 1 |
| stochastic-p4-d0.1@6080 | `men+atili` | OK | 2 |
| stochastic-p4-d0.1@8192 | `menatili` |  | 1 |
| stochastic-p4-d0.1@16384 | `menatili` |  | 1 |
| stochastic-p4-d0.2@6080 | `men+atili` | OK | 2 |
| stochastic-p4-d0.2@8192 | `men+atili` | OK | 2 |
| stochastic-p4-d0.2@16384 | `menatili` |  | 1 |
| unigram-ablation@6080 | `menatili` |  | 1 |

## `pakakak`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+kakak`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `paka+ka+k` |  | 3 |
| plain@8192 | `paka+kak` |  | 2 |
| plain@16384 | `pakakak` |  | 1 |
| morphbpe@6080 | `paka+ka+k` |  | 3 |
| morphbpe@8192 | `paka+ka+k` |  | 3 |
| morphbpe@16384 | `paka+kak` |  | 2 |
| penalty-1@6080 | `paka+ka+k` |  | 3 |
| penalty-1@8192 | `paka+kak` |  | 2 |
| penalty-1@16384 | `paka+kak` |  | 2 |
| penalty-2@6080 | `paka+ka+k` |  | 3 |
| penalty-2@8192 | `paka+ka+k` |  | 3 |
| penalty-2@16384 | `paka+kak` |  | 2 |
| penalty-4@6080 | `paka+ka+k` |  | 3 |
| penalty-4@8192 | `paka+ka+k` |  | 3 |
| penalty-4@16384 | `paka+kak` |  | 2 |
| penalty-8@6080 | `paka+ka+k` |  | 3 |
| penalty-8@8192 | `pakaka+k` |  | 2 |
| penalty-8@16384 | `pakaka+k` |  | 2 |
| stochastic-p4-d0.1@6080 | `paka+ka+k` |  | 3 |
| stochastic-p4-d0.1@8192 | `paka+ka+k` |  | 3 |
| stochastic-p4-d0.1@16384 | `paka+kak` |  | 2 |
| stochastic-p4-d0.2@6080 | `paka+ka+k` |  | 3 |
| stochastic-p4-d0.2@8192 | `paka+ka+k` |  | 3 |
| stochastic-p4-d0.2@16384 | `pakaka+k` |  | 2 |
| unigram-ablation@6080 | `paka+ka+k` |  | 3 |

## `pakibat`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+kibat`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pakibat` |  | 1 |
| plain@8192 | `pakibat` |  | 1 |
| plain@16384 | `pakibat` |  | 1 |
| morphbpe@6080 | `pakibat` |  | 1 |
| morphbpe@8192 | `pakibat` |  | 1 |
| morphbpe@16384 | `pakibat` |  | 1 |
| penalty-1@6080 | `pakibat` |  | 1 |
| penalty-1@8192 | `pakibat` |  | 1 |
| penalty-1@16384 | `pakibat` |  | 1 |
| penalty-2@6080 | `pakibat` |  | 1 |
| penalty-2@8192 | `pakibat` |  | 1 |
| penalty-2@16384 | `pakibat` |  | 1 |
| penalty-4@6080 | `pakibat` |  | 1 |
| penalty-4@8192 | `pakibat` |  | 1 |
| penalty-4@16384 | `pakibat` |  | 1 |
| penalty-8@6080 | `pakibat` |  | 1 |
| penalty-8@8192 | `pakibat` |  | 1 |
| penalty-8@16384 | `pakibat` |  | 1 |
| stochastic-p4-d0.1@6080 | `pakibat` |  | 1 |
| stochastic-p4-d0.1@8192 | `pakibat` |  | 1 |
| stochastic-p4-d0.1@16384 | `pakibat` |  | 1 |
| stochastic-p4-d0.2@6080 | `pakibat` |  | 1 |
| stochastic-p4-d0.2@8192 | `pakibat` |  | 1 |
| stochastic-p4-d0.2@16384 | `pakibat` |  | 1 |
| unigram-ablation@6080 | `pakibat` |  | 1 |

## `paldas`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+ldas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pal+das` |  | 2 |
| plain@8192 | `pal+das` |  | 2 |
| plain@16384 | `paldas` |  | 1 |
| morphbpe@6080 | `pal+das` |  | 2 |
| morphbpe@8192 | `paldas` |  | 1 |
| morphbpe@16384 | `paldas` |  | 1 |
| penalty-1@6080 | `pal+das` |  | 2 |
| penalty-1@8192 | `paldas` |  | 1 |
| penalty-1@16384 | `paldas` |  | 1 |
| penalty-2@6080 | `pal+das` |  | 2 |
| penalty-2@8192 | `paldas` |  | 1 |
| penalty-2@16384 | `paldas` |  | 1 |
| penalty-4@6080 | `pal+das` |  | 2 |
| penalty-4@8192 | `paldas` |  | 1 |
| penalty-4@16384 | `paldas` |  | 1 |
| penalty-8@6080 | `pal+das` |  | 2 |
| penalty-8@8192 | `paldas` |  | 1 |
| penalty-8@16384 | `paldas` |  | 1 |
| stochastic-p4-d0.1@6080 | `pal+das` |  | 2 |
| stochastic-p4-d0.1@8192 | `pal+das` |  | 2 |
| stochastic-p4-d0.1@16384 | `paldas` |  | 1 |
| stochastic-p4-d0.2@6080 | `pal+das` |  | 2 |
| stochastic-p4-d0.2@8192 | `pal+das` |  | 2 |
| stochastic-p4-d0.2@16384 | `paldas` |  | 1 |
| unigram-ablation@6080 | `paldas` |  | 1 |

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

## `pampang`  (prefixation, tier A_strong_silver)

**silver gold:** `pam+pang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pampang` |  | 1 |
| plain@8192 | `pampang` |  | 1 |
| plain@16384 | `pampang` |  | 1 |
| morphbpe@6080 | `pam+pang` | OK | 2 |
| morphbpe@8192 | `pam+pang` | OK | 2 |
| morphbpe@16384 | `pampang` |  | 1 |
| penalty-1@6080 | `pam+pang` | OK | 2 |
| penalty-1@8192 | `pam+pang` | OK | 2 |
| penalty-1@16384 | `pam+pang` | OK | 2 |
| penalty-2@6080 | `pam+pang` | OK | 2 |
| penalty-2@8192 | `pam+pang` | OK | 2 |
| penalty-2@16384 | `pam+pang` | OK | 2 |
| penalty-4@6080 | `pam+pang` | OK | 2 |
| penalty-4@8192 | `pam+pang` | OK | 2 |
| penalty-4@16384 | `pam+pang` | OK | 2 |
| penalty-8@6080 | `pam+pang` | OK | 2 |
| penalty-8@8192 | `pam+pang` | OK | 2 |
| penalty-8@16384 | `pam+pang` | OK | 2 |
| stochastic-p4-d0.1@6080 | `pampang` |  | 1 |
| stochastic-p4-d0.1@8192 | `pampang` |  | 1 |
| stochastic-p4-d0.1@16384 | `pampang` |  | 1 |
| stochastic-p4-d0.2@6080 | `pam+pang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `pam+pang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `pam+pang` | OK | 2 |
| unigram-ablation@6080 | `pampang` |  | 1 |

## `pilipinas`  (prefixation, tier B_moderate_silver)

**silver gold:** `pi+lipinas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `p+ilip+inas` |  | 3 |
| plain@8192 | `p+ilip+inas` |  | 3 |
| plain@16384 | `p+ilip+inas` |  | 3 |
| morphbpe@6080 | `p+ilipinas` |  | 2 |
| morphbpe@8192 | `p+ilipinas` |  | 2 |
| morphbpe@16384 | `p+ilipinas` |  | 2 |
| penalty-1@6080 | `p+ilipinas` |  | 2 |
| penalty-1@8192 | `p+ilipinas` |  | 2 |
| penalty-1@16384 | `p+ilipinas` |  | 2 |
| penalty-2@6080 | `p+ilipinas` |  | 2 |
| penalty-2@8192 | `p+ilipinas` |  | 2 |
| penalty-2@16384 | `p+ilipinas` |  | 2 |
| penalty-4@6080 | `p+ilipin+as` |  | 3 |
| penalty-4@8192 | `p+ilipin+as` |  | 3 |
| penalty-4@16384 | `p+ilipin+as` |  | 3 |
| penalty-8@6080 | `pili+pin+as` |  | 3 |
| penalty-8@8192 | `pili+pin+as` |  | 3 |
| penalty-8@16384 | `pili+pin+as` |  | 3 |
| stochastic-p4-d0.1@6080 | `pili+pinas` |  | 2 |
| stochastic-p4-d0.1@8192 | `pili+pinas` |  | 2 |
| stochastic-p4-d0.1@16384 | `pili+pinas` |  | 2 |
| stochastic-p4-d0.2@6080 | `pi+lipin+as` |  | 3 |
| stochastic-p4-d0.2@8192 | `pi+lipin+as` |  | 3 |
| stochastic-p4-d0.2@16384 | `pi+lipin+as` |  | 3 |
| unigram-ablation@6080 | `pi+li+pin+as` |  | 4 |

## `mabilis`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+bilis`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mabilis` |  | 1 |
| plain@8192 | `mabilis` |  | 1 |
| plain@16384 | `mabilis` |  | 1 |
| morphbpe@6080 | `mab+ilis` |  | 2 |
| morphbpe@8192 | `mab+ilis` |  | 2 |
| morphbpe@16384 | `mab+ilis` |  | 2 |
| penalty-1@6080 | `ma+bilis` | OK | 2 |
| penalty-1@8192 | `ma+bilis` | OK | 2 |
| penalty-1@16384 | `ma+bilis` | OK | 2 |
| penalty-2@6080 | `ma+bilis` | OK | 2 |
| penalty-2@8192 | `ma+bilis` | OK | 2 |
| penalty-2@16384 | `ma+bilis` | OK | 2 |
| penalty-4@6080 | `ma+bilis` | OK | 2 |
| penalty-4@8192 | `ma+bilis` | OK | 2 |
| penalty-4@16384 | `ma+bilis` | OK | 2 |
| penalty-8@6080 | `ma+bilis` | OK | 2 |
| penalty-8@8192 | `ma+bilis` | OK | 2 |
| penalty-8@16384 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+bilis` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+bilis` | OK | 2 |
| unigram-ablation@6080 | `mabilis` |  | 1 |

## `magaral`  (prefixation, tier A_strong_silver)

**silver gold:** `mag+aral`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `magaral` |  | 1 |
| plain@8192 | `magaral` |  | 1 |
| plain@16384 | `magaral` |  | 1 |
| morphbpe@6080 | `magaral` |  | 1 |
| morphbpe@8192 | `magaral` |  | 1 |
| morphbpe@16384 | `magaral` |  | 1 |
| penalty-1@6080 | `magaral` |  | 1 |
| penalty-1@8192 | `magaral` |  | 1 |
| penalty-1@16384 | `magaral` |  | 1 |
| penalty-2@6080 | `magaral` |  | 1 |
| penalty-2@8192 | `magaral` |  | 1 |
| penalty-2@16384 | `magaral` |  | 1 |
| penalty-4@6080 | `magaral` |  | 1 |
| penalty-4@8192 | `magaral` |  | 1 |
| penalty-4@16384 | `magaral` |  | 1 |
| penalty-8@6080 | `magaral` |  | 1 |
| penalty-8@8192 | `magaral` |  | 1 |
| penalty-8@16384 | `magaral` |  | 1 |
| stochastic-p4-d0.1@6080 | `magaral` |  | 1 |
| stochastic-p4-d0.1@8192 | `magaral` |  | 1 |
| stochastic-p4-d0.1@16384 | `magaral` |  | 1 |
| stochastic-p4-d0.2@6080 | `magaral` |  | 1 |
| stochastic-p4-d0.2@8192 | `magaral` |  | 1 |
| stochastic-p4-d0.2@16384 | `magaral` |  | 1 |
| unigram-ablation@6080 | `magaral` |  | 1 |

## `malagwa`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+lagwa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malag+wa` |  | 2 |
| plain@8192 | `malag+wa` |  | 2 |
| plain@16384 | `malagwa` |  | 1 |
| morphbpe@6080 | `malag+wa` |  | 2 |
| morphbpe@8192 | `malag+wa` |  | 2 |
| morphbpe@16384 | `malagwa` |  | 1 |
| penalty-1@6080 | `malag+wa` |  | 2 |
| penalty-1@8192 | `malag+wa` |  | 2 |
| penalty-1@16384 | `malagwa` |  | 1 |
| penalty-2@6080 | `malag+wa` |  | 2 |
| penalty-2@8192 | `malag+wa` |  | 2 |
| penalty-2@16384 | `malagwa` |  | 1 |
| penalty-4@6080 | `malag+wa` |  | 2 |
| penalty-4@8192 | `malag+wa` |  | 2 |
| penalty-4@16384 | `malagwa` |  | 1 |
| penalty-8@6080 | `malag+wa` |  | 2 |
| penalty-8@8192 | `malag+wa` |  | 2 |
| penalty-8@16384 | `malagwa` |  | 1 |
| stochastic-p4-d0.1@6080 | `ma+lag+wa` |  | 3 |
| stochastic-p4-d0.1@8192 | `ma+lag+wa` |  | 3 |
| stochastic-p4-d0.1@16384 | `malagwa` |  | 1 |
| stochastic-p4-d0.2@6080 | `malag+wa` |  | 2 |
| stochastic-p4-d0.2@8192 | `malag+wa` |  | 2 |
| stochastic-p4-d0.2@16384 | `malagwa` |  | 1 |
| unigram-ablation@6080 | `malagwa` |  | 1 |

## `malangi`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+langi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malang+i` |  | 2 |
| plain@8192 | `malang+i` |  | 2 |
| plain@16384 | `malangi` |  | 1 |
| morphbpe@6080 | `malang+i` |  | 2 |
| morphbpe@8192 | `malang+i` |  | 2 |
| morphbpe@16384 | `malangi` |  | 1 |
| penalty-1@6080 | `malang+i` |  | 2 |
| penalty-1@8192 | `malang+i` |  | 2 |
| penalty-1@16384 | `malangi` |  | 1 |
| penalty-2@6080 | `malang+i` |  | 2 |
| penalty-2@8192 | `malang+i` |  | 2 |
| penalty-2@16384 | `malangi` |  | 1 |
| penalty-4@6080 | `malang+i` |  | 2 |
| penalty-4@8192 | `malang+i` |  | 2 |
| penalty-4@16384 | `malangi` |  | 1 |
| penalty-8@6080 | `malang+i` |  | 2 |
| penalty-8@8192 | `malang+i` |  | 2 |
| penalty-8@16384 | `malangi` |  | 1 |
| stochastic-p4-d0.1@6080 | `mal+ang+i` |  | 3 |
| stochastic-p4-d0.1@8192 | `malang+i` |  | 2 |
| stochastic-p4-d0.1@16384 | `malangi` |  | 1 |
| stochastic-p4-d0.2@6080 | `ma+langi` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+langi` | OK | 2 |
| stochastic-p4-d0.2@16384 | `malangi` |  | 1 |
| unigram-ablation@6080 | `malangi` |  | 1 |

## `malino`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+lino`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `malino` |  | 1 |
| plain@8192 | `malino` |  | 1 |
| plain@16384 | `malino` |  | 1 |
| morphbpe@6080 | `mal+ino` |  | 2 |
| morphbpe@8192 | `mal+ino` |  | 2 |
| morphbpe@16384 | `mal+ino` |  | 2 |
| penalty-1@6080 | `mal+ino` |  | 2 |
| penalty-1@8192 | `mal+ino` |  | 2 |
| penalty-1@16384 | `mal+ino` |  | 2 |
| penalty-2@6080 | `mal+ino` |  | 2 |
| penalty-2@8192 | `mal+ino` |  | 2 |
| penalty-2@16384 | `mal+ino` |  | 2 |
| penalty-4@6080 | `mal+ino` |  | 2 |
| penalty-4@8192 | `mal+ino` |  | 2 |
| penalty-4@16384 | `mal+ino` |  | 2 |
| penalty-8@6080 | `mal+ino` |  | 2 |
| penalty-8@8192 | `mal+ino` |  | 2 |
| penalty-8@16384 | `mal+ino` |  | 2 |
| stochastic-p4-d0.1@6080 | `mal+ino` |  | 2 |
| stochastic-p4-d0.1@8192 | `mal+ino` |  | 2 |
| stochastic-p4-d0.1@16384 | `mal+ino` |  | 2 |
| stochastic-p4-d0.2@6080 | `mal+ino` |  | 2 |
| stochastic-p4-d0.2@8192 | `mal+ino` |  | 2 |
| stochastic-p4-d0.2@16384 | `mal+ino` |  | 2 |
| unigram-ablation@6080 | `malino` |  | 1 |

## `mangamate`  (prefixation, tier B_moderate_silver)

**silver gold:** `mang+amate`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mang+amate` | OK | 2 |
| plain@8192 | `mang+amate` | OK | 2 |
| plain@16384 | `mang+amate` | OK | 2 |
| morphbpe@6080 | `mang+amate` | OK | 2 |
| morphbpe@8192 | `mang+amate` | OK | 2 |
| morphbpe@16384 | `mang+amate` | OK | 2 |
| penalty-1@6080 | `mang+amate` | OK | 2 |
| penalty-1@8192 | `mang+amate` | OK | 2 |
| penalty-1@16384 | `mang+amate` | OK | 2 |
| penalty-2@6080 | `mang+amate` | OK | 2 |
| penalty-2@8192 | `mang+amate` | OK | 2 |
| penalty-2@16384 | `mang+amate` | OK | 2 |
| penalty-4@6080 | `mang+amate` | OK | 2 |
| penalty-4@8192 | `mang+amate` | OK | 2 |
| penalty-4@16384 | `mang+amate` | OK | 2 |
| penalty-8@6080 | `mang+amate` | OK | 2 |
| penalty-8@8192 | `mang+amate` | OK | 2 |
| penalty-8@16384 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mang+amate` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mang+amate` | OK | 2 |
| unigram-ablation@6080 | `manga+mate` |  | 2 |

## `maniabing`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+iabing`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mani+abing` |  | 2 |
| plain@8192 | `mani+abing` |  | 2 |
| plain@16384 | `maniabing` |  | 1 |
| morphbpe@6080 | `mani+abing` |  | 2 |
| morphbpe@8192 | `mani+abing` |  | 2 |
| morphbpe@16384 | `maniabing` |  | 1 |
| penalty-1@6080 | `mani+abing` |  | 2 |
| penalty-1@8192 | `mani+abing` |  | 2 |
| penalty-1@16384 | `maniabing` |  | 1 |
| penalty-2@6080 | `mani+abing` |  | 2 |
| penalty-2@8192 | `mani+abing` |  | 2 |
| penalty-2@16384 | `maniabing` |  | 1 |
| penalty-4@6080 | `mania+bing` |  | 2 |
| penalty-4@8192 | `mania+bing` |  | 2 |
| penalty-4@16384 | `maniabing` |  | 1 |
| penalty-8@6080 | `mania+bing` |  | 2 |
| penalty-8@8192 | `mania+bing` |  | 2 |
| penalty-8@16384 | `maniabing` |  | 1 |
| stochastic-p4-d0.1@6080 | `maniabi+ng` |  | 2 |
| stochastic-p4-d0.1@8192 | `maniabi+ng` |  | 2 |
| stochastic-p4-d0.1@16384 | `maniabing` |  | 1 |
| stochastic-p4-d0.2@6080 | `maniabi+ng` |  | 2 |
| stochastic-p4-d0.2@8192 | `maniabi+ng` |  | 2 |
| stochastic-p4-d0.2@16384 | `maniabing` |  | 1 |
| unigram-ablation@6080 | `maniabi+ng` |  | 2 |

## `maninap`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+inap`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+inap` | OK | 2 |
| plain@8192 | `man+inap` | OK | 2 |
| plain@16384 | `maninap` |  | 1 |
| morphbpe@6080 | `man+inap` | OK | 2 |
| morphbpe@8192 | `man+inap` | OK | 2 |
| morphbpe@16384 | `maninap` |  | 1 |
| penalty-1@6080 | `man+inap` | OK | 2 |
| penalty-1@8192 | `man+inap` | OK | 2 |
| penalty-1@16384 | `maninap` |  | 1 |
| penalty-2@6080 | `man+inap` | OK | 2 |
| penalty-2@8192 | `man+inap` | OK | 2 |
| penalty-2@16384 | `maninap` |  | 1 |
| penalty-4@6080 | `man+inap` | OK | 2 |
| penalty-4@8192 | `man+inap` | OK | 2 |
| penalty-4@16384 | `maninap` |  | 1 |
| penalty-8@6080 | `man+inap` | OK | 2 |
| penalty-8@8192 | `man+inap` | OK | 2 |
| penalty-8@16384 | `maninap` |  | 1 |
| stochastic-p4-d0.1@6080 | `man+inap` | OK | 2 |
| stochastic-p4-d0.1@8192 | `man+inap` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maninap` |  | 1 |
| stochastic-p4-d0.2@6080 | `man+inap` | OK | 2 |
| stochastic-p4-d0.2@8192 | `man+inap` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maninap` |  | 1 |
| unigram-ablation@6080 | `mani+na+p` |  | 3 |

## `manyawad`  (prefixation, tier A_strong_silver)

**silver gold:** `man+yawad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+ya+wad` |  | 3 |
| plain@8192 | `manya+wad` |  | 2 |
| plain@16384 | `manyawad` |  | 1 |
| morphbpe@6080 | `man+ya+wad` |  | 3 |
| morphbpe@8192 | `man+yawad` | OK | 2 |
| morphbpe@16384 | `man+yawad` | OK | 2 |
| penalty-1@6080 | `man+ya+wad` |  | 3 |
| penalty-1@8192 | `man+yawad` | OK | 2 |
| penalty-1@16384 | `man+yawad` | OK | 2 |
| penalty-2@6080 | `man+ya+wad` |  | 3 |
| penalty-2@8192 | `man+yawad` | OK | 2 |
| penalty-2@16384 | `man+yawad` | OK | 2 |
| penalty-4@6080 | `man+ya+wad` |  | 3 |
| penalty-4@8192 | `man+yawad` | OK | 2 |
| penalty-4@16384 | `man+yawad` | OK | 2 |
| penalty-8@6080 | `man+ya+wad` |  | 3 |
| penalty-8@8192 | `man+yawad` | OK | 2 |
| penalty-8@16384 | `man+yawad` | OK | 2 |
| stochastic-p4-d0.1@6080 | `man+ya+wad` |  | 3 |
| stochastic-p4-d0.1@8192 | `man+yawad` | OK | 2 |
| stochastic-p4-d0.1@16384 | `man+yawad` | OK | 2 |
| stochastic-p4-d0.2@6080 | `man+ya+wad` |  | 3 |
| stochastic-p4-d0.2@8192 | `man+yawad` | OK | 2 |
| stochastic-p4-d0.2@16384 | `man+yawad` | OK | 2 |
| unigram-ablation@6080 | `man+yawad` | OK | 2 |

## `mapait`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+pait`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `map+ait` |  | 2 |
| plain@8192 | `map+ait` |  | 2 |
| plain@16384 | `mapait` |  | 1 |
| morphbpe@6080 | `map+a+it` |  | 3 |
| morphbpe@8192 | `mapa+it` |  | 2 |
| morphbpe@16384 | `mapait` |  | 1 |
| penalty-1@6080 | `mapa+it` |  | 2 |
| penalty-1@8192 | `mapa+it` |  | 2 |
| penalty-1@16384 | `mapait` |  | 1 |
| penalty-2@6080 | `mapa+it` |  | 2 |
| penalty-2@8192 | `mapa+it` |  | 2 |
| penalty-2@16384 | `mapait` |  | 1 |
| penalty-4@6080 | `mapa+it` |  | 2 |
| penalty-4@8192 | `mapa+it` |  | 2 |
| penalty-4@16384 | `mapait` |  | 1 |
| penalty-8@6080 | `mapa+it` |  | 2 |
| penalty-8@8192 | `mapa+it` |  | 2 |
| penalty-8@16384 | `mapait` |  | 1 |
| stochastic-p4-d0.1@6080 | `mapa+it` |  | 2 |
| stochastic-p4-d0.1@8192 | `mapa+it` |  | 2 |
| stochastic-p4-d0.1@16384 | `mapait` |  | 1 |
| stochastic-p4-d0.2@6080 | `mapa+it` |  | 2 |
| stochastic-p4-d0.2@8192 | `mapa+it` |  | 2 |
| stochastic-p4-d0.2@16384 | `mapait` |  | 1 |
| unigram-ablation@6080 | `mapa+it` |  | 2 |

## `mayubu`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+yubu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `may+ubu` |  | 2 |
| plain@8192 | `may+ubu` |  | 2 |
| plain@16384 | `mayubu` |  | 1 |
| morphbpe@6080 | `may+ubu` |  | 2 |
| morphbpe@8192 | `may+ubu` |  | 2 |
| morphbpe@16384 | `may+ubu` |  | 2 |
| penalty-1@6080 | `mayu+bu` |  | 2 |
| penalty-1@8192 | `mayu+bu` |  | 2 |
| penalty-1@16384 | `mayu+bu` |  | 2 |
| penalty-2@6080 | `mayu+bu` |  | 2 |
| penalty-2@8192 | `mayu+bu` |  | 2 |
| penalty-2@16384 | `mayu+bu` |  | 2 |
| penalty-4@6080 | `mayu+bu` |  | 2 |
| penalty-4@8192 | `mayu+bu` |  | 2 |
| penalty-4@16384 | `mayu+bu` |  | 2 |
| penalty-8@6080 | `ma+yu+bu` |  | 3 |
| penalty-8@8192 | `ma+yubu` | OK | 2 |
| penalty-8@16384 | `ma+yubu` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mayu+bu` |  | 2 |
| stochastic-p4-d0.1@8192 | `mayu+bu` |  | 2 |
| stochastic-p4-d0.1@16384 | `mayu+bu` |  | 2 |
| stochastic-p4-d0.2@6080 | `mayu+bu` |  | 2 |
| stochastic-p4-d0.2@8192 | `mayu+bu` |  | 2 |
| stochastic-p4-d0.2@16384 | `mayu+bu` |  | 2 |
| unigram-ablation@6080 | `ma+yu+bu` |  | 3 |

## `pamilya`  (prefixation, tier B_moderate_silver)

**silver gold:** `pam+ilya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pamilya` |  | 1 |
| plain@8192 | `pamilya` |  | 1 |
| plain@16384 | `pamilya` |  | 1 |
| morphbpe@6080 | `pamilya` |  | 1 |
| morphbpe@8192 | `pamilya` |  | 1 |
| morphbpe@16384 | `pamilya` |  | 1 |
| penalty-1@6080 | `pamilya` |  | 1 |
| penalty-1@8192 | `pamilya` |  | 1 |
| penalty-1@16384 | `pamilya` |  | 1 |
| penalty-2@6080 | `pamilya` |  | 1 |
| penalty-2@8192 | `pamilya` |  | 1 |
| penalty-2@16384 | `pamilya` |  | 1 |
| penalty-4@6080 | `pamilya` |  | 1 |
| penalty-4@8192 | `pamilya` |  | 1 |
| penalty-4@16384 | `pamilya` |  | 1 |
| penalty-8@6080 | `pamilya` |  | 1 |
| penalty-8@8192 | `pamilya` |  | 1 |
| penalty-8@16384 | `pamilya` |  | 1 |
| stochastic-p4-d0.1@6080 | `pamilya` |  | 1 |
| stochastic-p4-d0.1@8192 | `pamilya` |  | 1 |
| stochastic-p4-d0.1@16384 | `pamilya` |  | 1 |
| stochastic-p4-d0.2@6080 | `pamilya` |  | 1 |
| stochastic-p4-d0.2@8192 | `pamilya` |  | 1 |
| stochastic-p4-d0.2@16384 | `pamilya` |  | 1 |
| unigram-ablation@6080 | `pamilya` |  | 1 |

## `pangaku`  (prefixation, tier B_moderate_silver)

**silver gold:** `pan+gaku`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pangaku` |  | 1 |
| plain@8192 | `pangaku` |  | 1 |
| plain@16384 | `pangaku` |  | 1 |
| morphbpe@6080 | `pangaku` |  | 1 |
| morphbpe@8192 | `pangaku` |  | 1 |
| morphbpe@16384 | `pangaku` |  | 1 |
| penalty-1@6080 | `pangaku` |  | 1 |
| penalty-1@8192 | `pangaku` |  | 1 |
| penalty-1@16384 | `pangaku` |  | 1 |
| penalty-2@6080 | `pangaku` |  | 1 |
| penalty-2@8192 | `pangaku` |  | 1 |
| penalty-2@16384 | `pangaku` |  | 1 |
| penalty-4@6080 | `pangaku` |  | 1 |
| penalty-4@8192 | `pangaku` |  | 1 |
| penalty-4@16384 | `pangaku` |  | 1 |
| penalty-8@6080 | `pangaku` |  | 1 |
| penalty-8@8192 | `pangaku` |  | 1 |
| penalty-8@16384 | `pangaku` |  | 1 |
| stochastic-p4-d0.1@6080 | `pangaku` |  | 1 |
| stochastic-p4-d0.1@8192 | `pangaku` |  | 1 |
| stochastic-p4-d0.1@16384 | `pangaku` |  | 1 |
| stochastic-p4-d0.2@6080 | `pangaku` |  | 1 |
| stochastic-p4-d0.2@8192 | `pangaku` |  | 1 |
| stochastic-p4-d0.2@16384 | `pangaku` |  | 1 |
| unigram-ablation@6080 | `pangaku` |  | 1 |

## `pangaras`  (prefixation, tier B_moderate_silver)

**silver gold:** `pang+aras`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pang+aras` | OK | 2 |
| plain@8192 | `pang+aras` | OK | 2 |
| plain@16384 | `pangaras` |  | 1 |
| morphbpe@6080 | `pang+aras` | OK | 2 |
| morphbpe@8192 | `pang+aras` | OK | 2 |
| morphbpe@16384 | `pangaras` |  | 1 |
| penalty-1@6080 | `pang+aras` | OK | 2 |
| penalty-1@8192 | `pang+aras` | OK | 2 |
| penalty-1@16384 | `pangaras` |  | 1 |
| penalty-2@6080 | `pang+aras` | OK | 2 |
| penalty-2@8192 | `pang+aras` | OK | 2 |
| penalty-2@16384 | `pangaras` |  | 1 |
| penalty-4@6080 | `pang+aras` | OK | 2 |
| penalty-4@8192 | `pang+aras` | OK | 2 |
| penalty-4@16384 | `pangaras` |  | 1 |
| penalty-8@6080 | `panga+ras` |  | 2 |
| penalty-8@8192 | `panga+ras` |  | 2 |
| penalty-8@16384 | `pangaras` |  | 1 |
| stochastic-p4-d0.1@6080 | `panga+ras` |  | 2 |
| stochastic-p4-d0.1@8192 | `panga+ras` |  | 2 |
| stochastic-p4-d0.1@16384 | `pangaras` |  | 1 |
| stochastic-p4-d0.2@6080 | `panga+ras` |  | 2 |
| stochastic-p4-d0.2@8192 | `panga+ras` |  | 2 |
| stochastic-p4-d0.2@16384 | `pangaras` |  | 1 |
| unigram-ablation@6080 | `panga+ras` |  | 2 |

## `pasibayung`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+sibayung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pas+ib+ayung` |  | 3 |
| plain@8192 | `pasibayung` |  | 1 |
| plain@16384 | `pasibayung` |  | 1 |
| morphbpe@6080 | `pasib+ayung` |  | 2 |
| morphbpe@8192 | `pasibayung` |  | 1 |
| morphbpe@16384 | `pasibayung` |  | 1 |
| penalty-1@6080 | `pas+ib+ayung` |  | 3 |
| penalty-1@8192 | `pasibayung` |  | 1 |
| penalty-1@16384 | `pasibayung` |  | 1 |
| penalty-2@6080 | `pas+ib+ayung` |  | 3 |
| penalty-2@8192 | `pasibayung` |  | 1 |
| penalty-2@16384 | `pasibayung` |  | 1 |
| penalty-4@6080 | `pasi+bayung` |  | 2 |
| penalty-4@8192 | `pasibayung` |  | 1 |
| penalty-4@16384 | `pasibayung` |  | 1 |
| penalty-8@6080 | `pasi+bayung` |  | 2 |
| penalty-8@8192 | `pasibayung` |  | 1 |
| penalty-8@16384 | `pasibayung` |  | 1 |
| stochastic-p4-d0.1@6080 | `pasi+bayung` |  | 2 |
| stochastic-p4-d0.1@8192 | `pasibayung` |  | 1 |
| stochastic-p4-d0.1@16384 | `pasibayung` |  | 1 |
| stochastic-p4-d0.2@6080 | `pasi+bayung` |  | 2 |
| stochastic-p4-d0.2@8192 | `pasibayung` |  | 1 |
| stochastic-p4-d0.2@16384 | `pasibayung` |  | 1 |
| unigram-ablation@6080 | `pasibayu+ng` |  | 2 |

## `patawad`  (prefixation, tier A_strong_silver)

**silver gold:** `pa+tawad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pat+awad` |  | 2 |
| plain@8192 | `pat+awad` |  | 2 |
| plain@16384 | `patawad` |  | 1 |
| morphbpe@6080 | `pat+aw+ad` |  | 3 |
| morphbpe@8192 | `pat+aw+ad` |  | 3 |
| morphbpe@16384 | `pat+awad` |  | 2 |
| penalty-1@6080 | `pataw+ad` |  | 2 |
| penalty-1@8192 | `pataw+ad` |  | 2 |
| penalty-1@16384 | `pataw+ad` |  | 2 |
| penalty-2@6080 | `pataw+ad` |  | 2 |
| penalty-2@8192 | `pataw+ad` |  | 2 |
| penalty-2@16384 | `pataw+ad` |  | 2 |
| penalty-4@6080 | `pataw+ad` |  | 2 |
| penalty-4@8192 | `pataw+ad` |  | 2 |
| penalty-4@16384 | `pataw+ad` |  | 2 |
| penalty-8@6080 | `pat+awa+d` |  | 3 |
| penalty-8@8192 | `pat+awa+d` |  | 3 |
| penalty-8@16384 | `pat+awad` |  | 2 |
| stochastic-p4-d0.1@6080 | `pat+awa+d` |  | 3 |
| stochastic-p4-d0.1@8192 | `pat+awa+d` |  | 3 |
| stochastic-p4-d0.1@16384 | `pat+awad` |  | 2 |
| stochastic-p4-d0.2@6080 | `pat+awad` |  | 2 |
| stochastic-p4-d0.2@8192 | `pat+awad` |  | 2 |
| stochastic-p4-d0.2@16384 | `pat+awad` |  | 2 |
| unigram-ablation@6080 | `patawa+d` |  | 2 |

## `ipaintulut`  (prefixation, tier B_moderate_silver)

**silver gold:** `ipa+intulut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ipa+int+ulut` |  | 3 |
| plain@8192 | `ipa+int+ulut` |  | 3 |
| plain@16384 | `ipa+intulut` | OK | 2 |
| morphbpe@6080 | `ipa+int+ulut` |  | 3 |
| morphbpe@8192 | `ipa+int+ulut` |  | 3 |
| morphbpe@16384 | `ipaintulut` |  | 1 |
| penalty-1@6080 | `ipa+int+ulut` |  | 3 |
| penalty-1@8192 | `ipa+int+ulut` |  | 3 |
| penalty-1@16384 | `ipa+intulut` | OK | 2 |
| penalty-2@6080 | `ipa+intulut` | OK | 2 |
| penalty-2@8192 | `ipa+intulut` | OK | 2 |
| penalty-2@16384 | `ipa+intulut` | OK | 2 |
| penalty-4@6080 | `ipa+intulut` | OK | 2 |
| penalty-4@8192 | `ipa+intulut` | OK | 2 |
| penalty-4@16384 | `ipaintulut` |  | 1 |
| penalty-8@6080 | `ipa+intu+lut` |  | 3 |
| penalty-8@8192 | `ipa+intu+lut` |  | 3 |
| penalty-8@16384 | `ipaintulut` |  | 1 |
| stochastic-p4-d0.1@6080 | `ipa+int+ulut` |  | 3 |
| stochastic-p4-d0.1@8192 | `ipa+int+ulut` |  | 3 |
| stochastic-p4-d0.1@16384 | `ipa+intulut` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ipa+intu+lut` |  | 3 |
| stochastic-p4-d0.2@8192 | `ipa+intu+lut` |  | 3 |
| stochastic-p4-d0.2@16384 | `ipa+intulut` | OK | 2 |
| unigram-ablation@6080 | `i+paintulut` |  | 2 |

## `maestro`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `maestro`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ma+estro` |  | 2 |
| plain@8192 | `ma+estro` |  | 2 |
| plain@16384 | `ma+estro` |  | 2 |
| morphbpe@6080 | `ma+estro` |  | 2 |
| morphbpe@8192 | `ma+estro` |  | 2 |
| morphbpe@16384 | `ma+estro` |  | 2 |
| penalty-1@6080 | `ma+estro` |  | 2 |
| penalty-1@8192 | `ma+estro` |  | 2 |
| penalty-1@16384 | `ma+estro` |  | 2 |
| penalty-2@6080 | `ma+estro` |  | 2 |
| penalty-2@8192 | `ma+estro` |  | 2 |
| penalty-2@16384 | `ma+estro` |  | 2 |
| penalty-4@6080 | `ma+estro` |  | 2 |
| penalty-4@8192 | `ma+estro` |  | 2 |
| penalty-4@16384 | `ma+estro` |  | 2 |
| penalty-8@6080 | `ma+estro` |  | 2 |
| penalty-8@8192 | `ma+estro` |  | 2 |
| penalty-8@16384 | `ma+estro` |  | 2 |
| stochastic-p4-d0.1@6080 | `ma+estro` |  | 2 |
| stochastic-p4-d0.1@8192 | `ma+estro` |  | 2 |
| stochastic-p4-d0.1@16384 | `ma+estro` |  | 2 |
| stochastic-p4-d0.2@6080 | `ma+estro` |  | 2 |
| stochastic-p4-d0.2@8192 | `ma+estro` |  | 2 |
| stochastic-p4-d0.2@16384 | `ma+estro` |  | 2 |
| unigram-ablation@6080 | `ma+e+stro` |  | 3 |

## `magari`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+gari`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mag+ari` |  | 2 |
| plain@8192 | `mag+ari` |  | 2 |
| plain@16384 | `magari` |  | 1 |
| morphbpe@6080 | `mag+ari` |  | 2 |
| morphbpe@8192 | `mag+ari` |  | 2 |
| morphbpe@16384 | `mag+ari` |  | 2 |
| penalty-1@6080 | `mag+ari` |  | 2 |
| penalty-1@8192 | `mag+ari` |  | 2 |
| penalty-1@16384 | `mag+ari` |  | 2 |
| penalty-2@6080 | `mag+ari` |  | 2 |
| penalty-2@8192 | `mag+ari` |  | 2 |
| penalty-2@16384 | `mag+ari` |  | 2 |
| penalty-4@6080 | `mag+ari` |  | 2 |
| penalty-4@8192 | `mag+ari` |  | 2 |
| penalty-4@16384 | `mag+ari` |  | 2 |
| penalty-8@6080 | `mag+ari` |  | 2 |
| penalty-8@8192 | `mag+ari` |  | 2 |
| penalty-8@16384 | `mag+ari` |  | 2 |
| stochastic-p4-d0.1@6080 | `mag+ari` |  | 2 |
| stochastic-p4-d0.1@8192 | `mag+ari` |  | 2 |
| stochastic-p4-d0.1@16384 | `mag+ari` |  | 2 |
| stochastic-p4-d0.2@6080 | `mag+ari` |  | 2 |
| stochastic-p4-d0.2@8192 | `mag+ari` |  | 2 |
| stochastic-p4-d0.2@16384 | `mag+ari` |  | 2 |
| unigram-ablation@6080 | `mag+ari` |  | 2 |

## `makalunus`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+lunus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makal+unus` |  | 2 |
| plain@8192 | `makal+unus` |  | 2 |
| plain@16384 | `makalunus` |  | 1 |
| morphbpe@6080 | `makal+un+us` |  | 3 |
| morphbpe@8192 | `makal+unus` |  | 2 |
| morphbpe@16384 | `makal+unus` |  | 2 |
| penalty-1@6080 | `makal+un+us` |  | 3 |
| penalty-1@8192 | `makal+un+us` |  | 3 |
| penalty-1@16384 | `makal+unus` |  | 2 |
| penalty-2@6080 | `makal+un+us` |  | 3 |
| penalty-2@8192 | `makal+unus` |  | 2 |
| penalty-2@16384 | `makal+unus` |  | 2 |
| penalty-4@6080 | `makal+un+us` |  | 3 |
| penalty-4@8192 | `makal+unus` |  | 2 |
| penalty-4@16384 | `makal+unus` |  | 2 |
| penalty-8@6080 | `maka+lunus` | OK | 2 |
| penalty-8@8192 | `maka+lunus` | OK | 2 |
| penalty-8@16384 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.1@8192 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+lunus` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+lunus` | OK | 2 |
| unigram-ablation@6080 | `maka+lunus` | OK | 2 |

## `makasalikut`  (prefixation, tier A_strong_silver)

**silver gold:** `maka+salikut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `makas+alikut` |  | 2 |
| plain@8192 | `makas+alikut` |  | 2 |
| plain@16384 | `makasalikut` |  | 1 |
| morphbpe@6080 | `maka+salikut` | OK | 2 |
| morphbpe@8192 | `maka+salikut` | OK | 2 |
| morphbpe@16384 | `maka+salikut` | OK | 2 |
| penalty-1@6080 | `maka+salikut` | OK | 2 |
| penalty-1@8192 | `maka+salikut` | OK | 2 |
| penalty-1@16384 | `maka+salikut` | OK | 2 |
| penalty-2@6080 | `maka+salikut` | OK | 2 |
| penalty-2@8192 | `maka+salikut` | OK | 2 |
| penalty-2@16384 | `maka+salikut` | OK | 2 |
| penalty-4@6080 | `maka+salikut` | OK | 2 |
| penalty-4@8192 | `maka+salikut` | OK | 2 |
| penalty-4@16384 | `maka+salikut` | OK | 2 |
| penalty-8@6080 | `maka+salikut` | OK | 2 |
| penalty-8@8192 | `maka+salikut` | OK | 2 |
| penalty-8@16384 | `maka+salikut` | OK | 2 |
| stochastic-p4-d0.1@6080 | `maka+sali+kut` |  | 3 |
| stochastic-p4-d0.1@8192 | `maka+salikut` | OK | 2 |
| stochastic-p4-d0.1@16384 | `maka+salikut` | OK | 2 |
| stochastic-p4-d0.2@6080 | `maka+salikut` | OK | 2 |
| stochastic-p4-d0.2@8192 | `maka+salikut` | OK | 2 |
| stochastic-p4-d0.2@16384 | `maka+salikut` | OK | 2 |
| unigram-ablation@6080 | `maka+salikut` | OK | 2 |

## `mamintu`  (prefixation, tier B_moderate_silver)

**silver gold:** `mam+intu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mam+intu` | OK | 2 |
| plain@8192 | `mamintu` |  | 1 |
| plain@16384 | `mamintu` |  | 1 |
| morphbpe@6080 | `mam+intu` | OK | 2 |
| morphbpe@8192 | `mam+intu` | OK | 2 |
| morphbpe@16384 | `mam+intu` | OK | 2 |
| penalty-1@6080 | `mam+intu` | OK | 2 |
| penalty-1@8192 | `mam+intu` | OK | 2 |
| penalty-1@16384 | `mam+intu` | OK | 2 |
| penalty-2@6080 | `mam+intu` | OK | 2 |
| penalty-2@8192 | `mam+intu` | OK | 2 |
| penalty-2@16384 | `mam+intu` | OK | 2 |
| penalty-4@6080 | `mam+intu` | OK | 2 |
| penalty-4@8192 | `mam+intu` | OK | 2 |
| penalty-4@16384 | `mam+intu` | OK | 2 |
| penalty-8@6080 | `mam+intu` | OK | 2 |
| penalty-8@8192 | `mam+intu` | OK | 2 |
| penalty-8@16384 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mam+intu` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mam+intu` | OK | 2 |
| unigram-ablation@6080 | `mamintu` |  | 1 |

## `manaliwang`  (prefixation, tier B_moderate_silver)

**silver gold:** `man+aliwang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+aliwang` | OK | 2 |
| plain@8192 | `man+aliwang` | OK | 2 |
| plain@16384 | `man+aliwang` | OK | 2 |
| morphbpe@6080 | `man+aliwang` | OK | 2 |
| morphbpe@8192 | `man+aliwang` | OK | 2 |
| morphbpe@16384 | `man+aliwang` | OK | 2 |
| penalty-1@6080 | `man+aliwang` | OK | 2 |
| penalty-1@8192 | `man+aliwang` | OK | 2 |
| penalty-1@16384 | `man+aliwang` | OK | 2 |
| penalty-2@6080 | `man+aliwang` | OK | 2 |
| penalty-2@8192 | `man+aliwang` | OK | 2 |
| penalty-2@16384 | `man+aliwang` | OK | 2 |
| penalty-4@6080 | `man+aliwang` | OK | 2 |
| penalty-4@8192 | `man+aliwang` | OK | 2 |
| penalty-4@16384 | `man+aliwang` | OK | 2 |
| penalty-8@6080 | `man+aliwang` | OK | 2 |
| penalty-8@8192 | `man+aliwang` | OK | 2 |
| penalty-8@16384 | `man+aliwang` | OK | 2 |
| stochastic-p4-d0.1@6080 | `man+ali+wang` |  | 3 |
| stochastic-p4-d0.1@8192 | `man+ali+wang` |  | 3 |
| stochastic-p4-d0.1@16384 | `man+ali+wang` |  | 3 |
| stochastic-p4-d0.2@6080 | `man+aliwang` | OK | 2 |
| stochastic-p4-d0.2@8192 | `man+aliwang` | OK | 2 |
| stochastic-p4-d0.2@16384 | `man+aliwang` | OK | 2 |
| unigram-ablation@6080 | `man+aliwang` | OK | 2 |

## `manyad`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+nyad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `man+yad` |  | 2 |
| plain@8192 | `man+yad` |  | 2 |
| plain@16384 | `manyad` |  | 1 |
| morphbpe@6080 | `man+yad` |  | 2 |
| morphbpe@8192 | `man+yad` |  | 2 |
| morphbpe@16384 | `manyad` |  | 1 |
| penalty-1@6080 | `man+yad` |  | 2 |
| penalty-1@8192 | `man+yad` |  | 2 |
| penalty-1@16384 | `manyad` |  | 1 |
| penalty-2@6080 | `man+yad` |  | 2 |
| penalty-2@8192 | `man+yad` |  | 2 |
| penalty-2@16384 | `manyad` |  | 1 |
| penalty-4@6080 | `man+yad` |  | 2 |
| penalty-4@8192 | `man+yad` |  | 2 |
| penalty-4@16384 | `manyad` |  | 1 |
| penalty-8@6080 | `man+yad` |  | 2 |
| penalty-8@8192 | `man+yad` |  | 2 |
| penalty-8@16384 | `manyad` |  | 1 |
| stochastic-p4-d0.1@6080 | `man+yad` |  | 2 |
| stochastic-p4-d0.1@8192 | `man+yad` |  | 2 |
| stochastic-p4-d0.1@16384 | `manyad` |  | 1 |
| stochastic-p4-d0.2@6080 | `man+yad` |  | 2 |
| stochastic-p4-d0.2@8192 | `man+yad` |  | 2 |
| stochastic-p4-d0.2@16384 | `manyad` |  | 1 |
| unigram-ablation@6080 | `man+ya+d` |  | 3 |

## `mapinu`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+pinu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `map+inu` |  | 2 |
| plain@8192 | `map+inu` |  | 2 |
| plain@16384 | `mapinu` |  | 1 |
| morphbpe@6080 | `map+inu` |  | 2 |
| morphbpe@8192 | `map+inu` |  | 2 |
| morphbpe@16384 | `map+inu` |  | 2 |
| penalty-1@6080 | `ma+pin+u` |  | 3 |
| penalty-1@8192 | `ma+pin+u` |  | 3 |
| penalty-1@16384 | `ma+pinu` | OK | 2 |
| penalty-2@6080 | `ma+pin+u` |  | 3 |
| penalty-2@8192 | `ma+pin+u` |  | 3 |
| penalty-2@16384 | `ma+pinu` | OK | 2 |
| penalty-4@6080 | `ma+pin+u` |  | 3 |
| penalty-4@8192 | `ma+pinu` | OK | 2 |
| penalty-4@16384 | `ma+pinu` | OK | 2 |
| penalty-8@6080 | `ma+pin+u` |  | 3 |
| penalty-8@8192 | `ma+pin+u` |  | 3 |
| penalty-8@16384 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.1@6080 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.1@8192 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.1@16384 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.2@6080 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.2@8192 | `ma+pinu` | OK | 2 |
| stochastic-p4-d0.2@16384 | `ma+pinu` | OK | 2 |
| unigram-ablation@6080 | `ma+pin+u` |  | 3 |

## `masala`  (prefixation, tier A_strong_silver)

**silver gold:** `ma+sala`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `masala` |  | 1 |
| plain@8192 | `masala` |  | 1 |
| plain@16384 | `masala` |  | 1 |
| morphbpe@6080 | `masala` |  | 1 |
| morphbpe@8192 | `masala` |  | 1 |
| morphbpe@16384 | `masala` |  | 1 |
| penalty-1@6080 | `masala` |  | 1 |
| penalty-1@8192 | `masala` |  | 1 |
| penalty-1@16384 | `masala` |  | 1 |
| penalty-2@6080 | `masala` |  | 1 |
| penalty-2@8192 | `masala` |  | 1 |
| penalty-2@16384 | `masala` |  | 1 |
| penalty-4@6080 | `masala` |  | 1 |
| penalty-4@8192 | `masala` |  | 1 |
| penalty-4@16384 | `masala` |  | 1 |
| penalty-8@6080 | `masala` |  | 1 |
| penalty-8@8192 | `masala` |  | 1 |
| penalty-8@16384 | `masala` |  | 1 |
| stochastic-p4-d0.1@6080 | `masala` |  | 1 |
| stochastic-p4-d0.1@8192 | `masala` |  | 1 |
| stochastic-p4-d0.1@16384 | `masala` |  | 1 |
| stochastic-p4-d0.2@6080 | `masala` |  | 1 |
| stochastic-p4-d0.2@8192 | `masala` |  | 1 |
| stochastic-p4-d0.2@16384 | `masala` |  | 1 |
| unigram-ablation@6080 | `masala` |  | 1 |

## `masquil`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+squil`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+qu+il` |  | 3 |
| plain@8192 | `mas+qu+il` |  | 3 |
| plain@16384 | `mas+quil` |  | 2 |
| morphbpe@6080 | `mas+qu+il` |  | 3 |
| morphbpe@8192 | `mas+quil` |  | 2 |
| morphbpe@16384 | `mas+quil` |  | 2 |
| penalty-1@6080 | `mas+qu+il` |  | 3 |
| penalty-1@8192 | `mas+quil` |  | 2 |
| penalty-1@16384 | `mas+quil` |  | 2 |
| penalty-2@6080 | `mas+qu+il` |  | 3 |
| penalty-2@8192 | `mas+quil` |  | 2 |
| penalty-2@16384 | `mas+quil` |  | 2 |
| penalty-4@6080 | `mas+qu+il` |  | 3 |
| penalty-4@8192 | `mas+quil` |  | 2 |
| penalty-4@16384 | `mas+quil` |  | 2 |
| penalty-8@6080 | `mas+qu+il` |  | 3 |
| penalty-8@8192 | `mas+qu+il` |  | 3 |
| penalty-8@16384 | `mas+quil` |  | 2 |
| stochastic-p4-d0.1@6080 | `mas+qu+il` |  | 3 |
| stochastic-p4-d0.1@8192 | `mas+quil` |  | 2 |
| stochastic-p4-d0.1@16384 | `mas+quil` |  | 2 |
| stochastic-p4-d0.2@6080 | `mas+qu+il` |  | 3 |
| stochastic-p4-d0.2@8192 | `mas+qu+il` |  | 3 |
| stochastic-p4-d0.2@16384 | `mas+quil` |  | 2 |
| unigram-ablation@6080 | `mas+qui+l` |  | 3 |

## `mayakit`  (prefixation, tier B_moderate_silver)

**silver gold:** `ma+yakit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `maya+kit` |  | 2 |
| plain@8192 | `maya+kit` |  | 2 |
| plain@16384 | `mayakit` |  | 1 |
| morphbpe@6080 | `maya+kit` |  | 2 |
| morphbpe@8192 | `maya+kit` |  | 2 |
| morphbpe@16384 | `mayakit` |  | 1 |
| penalty-1@6080 | `maya+kit` |  | 2 |
| penalty-1@8192 | `maya+kit` |  | 2 |
| penalty-1@16384 | `mayakit` |  | 1 |
| penalty-2@6080 | `maya+kit` |  | 2 |
| penalty-2@8192 | `maya+kit` |  | 2 |
| penalty-2@16384 | `mayakit` |  | 1 |
| penalty-4@6080 | `maya+kit` |  | 2 |
| penalty-4@8192 | `maya+kit` |  | 2 |
| penalty-4@16384 | `mayakit` |  | 1 |
| penalty-8@6080 | `maya+kit` |  | 2 |
| penalty-8@8192 | `maya+kit` |  | 2 |
| penalty-8@16384 | `mayakit` |  | 1 |
| stochastic-p4-d0.1@6080 | `maya+kit` |  | 2 |
| stochastic-p4-d0.1@8192 | `maya+kit` |  | 2 |
| stochastic-p4-d0.1@16384 | `mayakit` |  | 1 |
| stochastic-p4-d0.2@6080 | `maya+kit` |  | 2 |
| stochastic-p4-d0.2@8192 | `maya+kit` |  | 2 |
| stochastic-p4-d0.2@16384 | `mayakit` |  | 1 |
| unigram-ablation@6080 | `m+ayakit` |  | 2 |

## `menalakad`  (prefixation, tier B_moderate_silver)

**silver gold:** `men+alakad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `men+alakad` | OK | 2 |
| plain@8192 | `men+alakad` | OK | 2 |
| plain@16384 | `men+alakad` | OK | 2 |
| morphbpe@6080 | `men+alakad` | OK | 2 |
| morphbpe@8192 | `men+alakad` | OK | 2 |
| morphbpe@16384 | `men+alakad` | OK | 2 |
| penalty-1@6080 | `men+alakad` | OK | 2 |
| penalty-1@8192 | `men+alakad` | OK | 2 |
| penalty-1@16384 | `men+alakad` | OK | 2 |
| penalty-2@6080 | `men+alakad` | OK | 2 |
| penalty-2@8192 | `men+alakad` | OK | 2 |
| penalty-2@16384 | `men+alakad` | OK | 2 |
| penalty-4@6080 | `men+alakad` | OK | 2 |
| penalty-4@8192 | `men+alakad` | OK | 2 |
| penalty-4@16384 | `men+alakad` | OK | 2 |
| penalty-8@6080 | `men+alakad` | OK | 2 |
| penalty-8@8192 | `men+alakad` | OK | 2 |
| penalty-8@16384 | `men+alakad` | OK | 2 |
| stochastic-p4-d0.1@6080 | `men+alakad` | OK | 2 |
| stochastic-p4-d0.1@8192 | `men+alakad` | OK | 2 |
| stochastic-p4-d0.1@16384 | `men+alakad` | OK | 2 |
| stochastic-p4-d0.2@6080 | `men+ala+kad` |  | 3 |
| stochastic-p4-d0.2@8192 | `men+ala+kad` |  | 3 |
| stochastic-p4-d0.2@16384 | `men+ala+kad` |  | 3 |
| unigram-ablation@6080 | `men+alakad` | OK | 2 |

## `meninap`  (prefixation, tier B_moderate_silver)

**silver gold:** `men+inap`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `men+inap` | OK | 2 |
| plain@8192 | `men+inap` | OK | 2 |
| plain@16384 | `men+inap` | OK | 2 |
| morphbpe@6080 | `men+inap` | OK | 2 |
| morphbpe@8192 | `men+inap` | OK | 2 |
| morphbpe@16384 | `men+inap` | OK | 2 |
| penalty-1@6080 | `men+inap` | OK | 2 |
| penalty-1@8192 | `men+inap` | OK | 2 |
| penalty-1@16384 | `men+inap` | OK | 2 |
| penalty-2@6080 | `men+inap` | OK | 2 |
| penalty-2@8192 | `men+inap` | OK | 2 |
| penalty-2@16384 | `men+inap` | OK | 2 |
| penalty-4@6080 | `men+inap` | OK | 2 |
| penalty-4@8192 | `men+inap` | OK | 2 |
| penalty-4@16384 | `men+inap` | OK | 2 |
| penalty-8@6080 | `men+inap` | OK | 2 |
| penalty-8@8192 | `men+inap` | OK | 2 |
| penalty-8@16384 | `men+inap` | OK | 2 |
| stochastic-p4-d0.1@6080 | `men+inap` | OK | 2 |
| stochastic-p4-d0.1@8192 | `men+inap` | OK | 2 |
| stochastic-p4-d0.1@16384 | `men+inap` | OK | 2 |
| stochastic-p4-d0.2@6080 | `men+inap` | OK | 2 |
| stochastic-p4-d0.2@8192 | `men+inap` | OK | 2 |
| stochastic-p4-d0.2@16384 | `men+inap` | OK | 2 |
| unigram-ablation@6080 | `men+in+ap` |  | 3 |

## `migdala`  (prefixation, tier A_strong_silver)

**silver gold:** `mig+dala`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mig+dala` | OK | 2 |
| plain@8192 | `mig+dala` | OK | 2 |
| plain@16384 | `migdala` |  | 1 |
| morphbpe@6080 | `mig+dala` | OK | 2 |
| morphbpe@8192 | `mig+dala` | OK | 2 |
| morphbpe@16384 | `mig+dala` | OK | 2 |
| penalty-1@6080 | `mig+dala` | OK | 2 |
| penalty-1@8192 | `mig+dala` | OK | 2 |
| penalty-1@16384 | `mig+dala` | OK | 2 |
| penalty-2@6080 | `mig+dala` | OK | 2 |
| penalty-2@8192 | `mig+dala` | OK | 2 |
| penalty-2@16384 | `mig+dala` | OK | 2 |
| penalty-4@6080 | `mig+dala` | OK | 2 |
| penalty-4@8192 | `mig+dala` | OK | 2 |
| penalty-4@16384 | `mig+dala` | OK | 2 |
| penalty-8@6080 | `mig+dala` | OK | 2 |
| penalty-8@8192 | `mig+dala` | OK | 2 |
| penalty-8@16384 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.1@6080 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.1@8192 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.1@16384 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.2@6080 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.2@8192 | `mig+dala` | OK | 2 |
| stochastic-p4-d0.2@16384 | `mig+dala` | OK | 2 |
| unigram-ablation@6080 | `mig+dala` | OK | 2 |

## `pangaligtas`  (prefixation, tier A_strong_silver)

**silver gold:** `panga+ligtas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pangal+igtas` |  | 2 |
| plain@8192 | `pangal+igtas` |  | 2 |
| plain@16384 | `pangal+igtas` |  | 2 |
| morphbpe@6080 | `pang+alig+tas` |  | 3 |
| morphbpe@8192 | `pang+alig+tas` |  | 3 |
| morphbpe@16384 | `pang+aligtas` |  | 2 |
| penalty-1@6080 | `pang+alig+tas` |  | 3 |
| penalty-1@8192 | `pang+alig+tas` |  | 3 |
| penalty-1@16384 | `pang+aligtas` |  | 2 |
| penalty-2@6080 | `pang+alig+tas` |  | 3 |
| penalty-2@8192 | `pang+alig+tas` |  | 3 |
| penalty-2@16384 | `pang+aligtas` |  | 2 |
| penalty-4@6080 | `pang+alig+tas` |  | 3 |
| penalty-4@8192 | `pang+alig+tas` |  | 3 |
| penalty-4@16384 | `pang+aligtas` |  | 2 |
| penalty-8@6080 | `pang+alig+tas` |  | 3 |
| penalty-8@8192 | `pang+alig+tas` |  | 3 |
| penalty-8@16384 | `pang+aligtas` |  | 2 |
| stochastic-p4-d0.1@6080 | `pang+alig+tas` |  | 3 |
| stochastic-p4-d0.1@8192 | `pang+alig+tas` |  | 3 |
| stochastic-p4-d0.1@16384 | `pang+alig+tas` |  | 3 |
| stochastic-p4-d0.2@6080 | `pang+alig+tas` |  | 3 |
| stochastic-p4-d0.2@8192 | `pang+alig+tas` |  | 3 |
| stochastic-p4-d0.2@16384 | `pang+alig+tas` |  | 3 |
| unigram-ablation@6080 | `panga+ligtas` | OK | 2 |

## `parusa`  (prefixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pa+rusa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `par+usa` |  | 2 |
| plain@8192 | `parusa` |  | 1 |
| plain@16384 | `parusa` |  | 1 |
| morphbpe@6080 | `par+usa` |  | 2 |
| morphbpe@8192 | `parusa` |  | 1 |
| morphbpe@16384 | `parusa` |  | 1 |
| penalty-1@6080 | `par+usa` |  | 2 |
| penalty-1@8192 | `parusa` |  | 1 |
| penalty-1@16384 | `parusa` |  | 1 |
| penalty-2@6080 | `par+usa` |  | 2 |
| penalty-2@8192 | `parusa` |  | 1 |
| penalty-2@16384 | `parusa` |  | 1 |
| penalty-4@6080 | `par+usa` |  | 2 |
| penalty-4@8192 | `parusa` |  | 1 |
| penalty-4@16384 | `parusa` |  | 1 |
| penalty-8@6080 | `pa+rusa` | OK | 2 |
| penalty-8@8192 | `parusa` |  | 1 |
| penalty-8@16384 | `parusa` |  | 1 |
| stochastic-p4-d0.1@6080 | `pa+rusa` | OK | 2 |
| stochastic-p4-d0.1@8192 | `parusa` |  | 1 |
| stochastic-p4-d0.1@16384 | `parusa` |  | 1 |
| stochastic-p4-d0.2@6080 | `paru+sa` |  | 2 |
| stochastic-p4-d0.2@8192 | `parusa` |  | 1 |
| stochastic-p4-d0.2@16384 | `parusa` |  | 1 |
| unigram-ablation@6080 | `parusa` |  | 1 |

## `patutut`  (prefixation, tier B_moderate_silver)

**silver gold:** `pa+tutut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pat+ut+ut` |  | 3 |
| plain@8192 | `pat+utut` |  | 2 |
| plain@16384 | `pat+utut` |  | 2 |
| morphbpe@6080 | `pat+utut` |  | 2 |
| morphbpe@8192 | `pat+utut` |  | 2 |
| morphbpe@16384 | `pat+utut` |  | 2 |
| penalty-1@6080 | `pat+utut` |  | 2 |
| penalty-1@8192 | `pat+utut` |  | 2 |
| penalty-1@16384 | `pat+utut` |  | 2 |
| penalty-2@6080 | `pat+ut+ut` |  | 3 |
| penalty-2@8192 | `pat+utut` |  | 2 |
| penalty-2@16384 | `pat+utut` |  | 2 |
| penalty-4@6080 | `patu+tut` |  | 2 |
| penalty-4@8192 | `patu+tut` |  | 2 |
| penalty-4@16384 | `patu+tut` |  | 2 |
| penalty-8@6080 | `pat+utu+t` |  | 3 |
| penalty-8@8192 | `pat+utut` |  | 2 |
| penalty-8@16384 | `pat+utut` |  | 2 |
| stochastic-p4-d0.1@6080 | `pat+utu+t` |  | 3 |
| stochastic-p4-d0.1@8192 | `pat+utu+t` |  | 3 |
| stochastic-p4-d0.1@16384 | `pat+utut` |  | 2 |
| stochastic-p4-d0.2@6080 | `pat+utu+t` |  | 3 |
| stochastic-p4-d0.2@8192 | `pat+utut` |  | 2 |
| stochastic-p4-d0.2@16384 | `pat+utut` |  | 2 |
| unigram-ablation@6080 | `patutu+t` |  | 2 |

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

## `ingatan`  (prefixation+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ingat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ingatan` |  | 1 |
| plain@8192 | `ingatan` |  | 1 |
| plain@16384 | `ingatan` |  | 1 |
| morphbpe@6080 | `ingatan` |  | 1 |
| morphbpe@8192 | `ingatan` |  | 1 |
| morphbpe@16384 | `ingatan` |  | 1 |
| penalty-1@6080 | `ingatan` |  | 1 |
| penalty-1@8192 | `ingatan` |  | 1 |
| penalty-1@16384 | `ingatan` |  | 1 |
| penalty-2@6080 | `ingatan` |  | 1 |
| penalty-2@8192 | `ingatan` |  | 1 |
| penalty-2@16384 | `ingatan` |  | 1 |
| penalty-4@6080 | `ingatan` |  | 1 |
| penalty-4@8192 | `ingatan` |  | 1 |
| penalty-4@16384 | `ingatan` |  | 1 |
| penalty-8@6080 | `ingatan` |  | 1 |
| penalty-8@8192 | `ingatan` |  | 1 |
| penalty-8@16384 | `ingatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ingatan` |  | 1 |
| stochastic-p4-d0.1@8192 | `ingatan` |  | 1 |
| stochastic-p4-d0.1@16384 | `ingatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ingatan` |  | 1 |
| stochastic-p4-d0.2@8192 | `ingatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `ingatan` |  | 1 |
| unigram-ablation@6080 | `ingatan` |  | 1 |

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

## `pibandian`  (prefixation+suffixation, tier A_strong_silver)

**silver gold:** `pi+bandi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pibandian` |  | 1 |
| plain@8192 | `pibandian` |  | 1 |
| plain@16384 | `pibandian` |  | 1 |
| morphbpe@6080 | `pib+and+ian` |  | 3 |
| morphbpe@8192 | `pib+and+ian` |  | 3 |
| morphbpe@16384 | `pib+and+ian` |  | 3 |
| penalty-1@6080 | `pib+and+ian` |  | 3 |
| penalty-1@8192 | `pib+and+ian` |  | 3 |
| penalty-1@16384 | `pib+and+ian` |  | 3 |
| penalty-2@6080 | `pib+and+ian` |  | 3 |
| penalty-2@8192 | `pib+and+ian` |  | 3 |
| penalty-2@16384 | `pib+and+ian` |  | 3 |
| penalty-4@6080 | `pib+and+ian` |  | 3 |
| penalty-4@8192 | `pib+and+ian` |  | 3 |
| penalty-4@16384 | `pib+and+ian` |  | 3 |
| penalty-8@6080 | `pi+bandi+an` | OK | 3 |
| penalty-8@8192 | `pi+bandi+an` | OK | 3 |
| penalty-8@16384 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.1@6080 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.1@8192 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.1@16384 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.2@6080 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.2@8192 | `pi+bandi+an` | OK | 3 |
| stochastic-p4-d0.2@16384 | `pi+bandi+an` | OK | 3 |
| unigram-ablation@6080 | `pibandi+an` |  | 2 |

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

## `manibatan`  (prefixation+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `man+ibat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `manibatan` |  | 1 |
| plain@8192 | `manibatan` |  | 1 |
| plain@16384 | `manibatan` |  | 1 |
| morphbpe@6080 | `manibat+an` |  | 2 |
| morphbpe@8192 | `manibat+an` |  | 2 |
| morphbpe@16384 | `manibat+an` |  | 2 |
| penalty-1@6080 | `manibat+an` |  | 2 |
| penalty-1@8192 | `manibat+an` |  | 2 |
| penalty-1@16384 | `manibat+an` |  | 2 |
| penalty-2@6080 | `manibat+an` |  | 2 |
| penalty-2@8192 | `manibat+an` |  | 2 |
| penalty-2@16384 | `manibat+an` |  | 2 |
| penalty-4@6080 | `manibat+an` |  | 2 |
| penalty-4@8192 | `manibat+an` |  | 2 |
| penalty-4@16384 | `manibat+an` |  | 2 |
| penalty-8@6080 | `manibat+an` |  | 2 |
| penalty-8@8192 | `manibat+an` |  | 2 |
| penalty-8@16384 | `manibat+an` |  | 2 |
| stochastic-p4-d0.1@6080 | `manibat+an` |  | 2 |
| stochastic-p4-d0.1@8192 | `manibat+an` |  | 2 |
| stochastic-p4-d0.1@16384 | `manibat+an` |  | 2 |
| stochastic-p4-d0.2@6080 | `manibat+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `manibat+an` |  | 2 |
| stochastic-p4-d0.2@16384 | `manibat+an` |  | 2 |
| unigram-ablation@6080 | `manibat+an` |  | 2 |

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

## `macanian`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `ma+cani+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `macan+ian` |  | 2 |
| plain@8192 | `macan+ian` |  | 2 |
| plain@16384 | `macanian` |  | 1 |
| morphbpe@6080 | `ma+can+ian` |  | 3 |
| morphbpe@8192 | `macanian` |  | 1 |
| morphbpe@16384 | `macanian` |  | 1 |
| penalty-1@6080 | `macan+ian` |  | 2 |
| penalty-1@8192 | `macanian` |  | 1 |
| penalty-1@16384 | `macanian` |  | 1 |
| penalty-2@6080 | `macan+ian` |  | 2 |
| penalty-2@8192 | `macanian` |  | 1 |
| penalty-2@16384 | `macanian` |  | 1 |
| penalty-4@6080 | `macan+ian` |  | 2 |
| penalty-4@8192 | `macanian` |  | 1 |
| penalty-4@16384 | `macanian` |  | 1 |
| penalty-8@6080 | `mac+anian` |  | 2 |
| penalty-8@8192 | `macanian` |  | 1 |
| penalty-8@16384 | `macanian` |  | 1 |
| stochastic-p4-d0.1@6080 | `mac+anian` |  | 2 |
| stochastic-p4-d0.1@8192 | `macanian` |  | 1 |
| stochastic-p4-d0.1@16384 | `macanian` |  | 1 |
| stochastic-p4-d0.2@6080 | `mac+ani+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `macanian` |  | 1 |
| stochastic-p4-d0.2@16384 | `macanian` |  | 1 |
| unigram-ablation@6080 | `maca+ni+an` |  | 3 |

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

## `masikanan`  (prefixation+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ma+sikan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mas+ik+anan` |  | 3 |
| plain@8192 | `mas+ik+anan` |  | 3 |
| plain@16384 | `masikanan` |  | 1 |
| morphbpe@6080 | `masikan+an` |  | 2 |
| morphbpe@8192 | `masikan+an` |  | 2 |
| morphbpe@16384 | `masikan+an` |  | 2 |
| penalty-1@6080 | `masikan+an` |  | 2 |
| penalty-1@8192 | `masikan+an` |  | 2 |
| penalty-1@16384 | `masikan+an` |  | 2 |
| penalty-2@6080 | `masikan+an` |  | 2 |
| penalty-2@8192 | `masikan+an` |  | 2 |
| penalty-2@16384 | `masikan+an` |  | 2 |
| penalty-4@6080 | `masikan+an` |  | 2 |
| penalty-4@8192 | `masikan+an` |  | 2 |
| penalty-4@16384 | `masikan+an` |  | 2 |
| penalty-8@6080 | `masikan+an` |  | 2 |
| penalty-8@8192 | `masikan+an` |  | 2 |
| penalty-8@16384 | `masikan+an` |  | 2 |
| stochastic-p4-d0.1@6080 | `masikan+an` |  | 2 |
| stochastic-p4-d0.1@8192 | `masikan+an` |  | 2 |
| stochastic-p4-d0.1@16384 | `masikan+an` |  | 2 |
| stochastic-p4-d0.2@6080 | `masikan+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `masikan+an` |  | 2 |
| stochastic-p4-d0.2@16384 | `masikan+an` |  | 2 |
| unigram-ablation@6080 | `masikan+an` |  | 2 |

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

## `pilubluban`  (prefixation+suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `pi+lublub+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pil+ubluban` |  | 2 |
| plain@8192 | `pilubluban` |  | 1 |
| plain@16384 | `pilubluban` |  | 1 |
| morphbpe@6080 | `pil+ubluban` |  | 2 |
| morphbpe@8192 | `pilubluban` |  | 1 |
| morphbpe@16384 | `pilubluban` |  | 1 |
| penalty-1@6080 | `pilubluban` |  | 1 |
| penalty-1@8192 | `pilubluban` |  | 1 |
| penalty-1@16384 | `pilubluban` |  | 1 |
| penalty-2@6080 | `pilubluban` |  | 1 |
| penalty-2@8192 | `pilubluban` |  | 1 |
| penalty-2@16384 | `pilubluban` |  | 1 |
| penalty-4@6080 | `pilubluban` |  | 1 |
| penalty-4@8192 | `pilubluban` |  | 1 |
| penalty-4@16384 | `pilubluban` |  | 1 |
| penalty-8@6080 | `pilubluban` |  | 1 |
| penalty-8@8192 | `pilubluban` |  | 1 |
| penalty-8@16384 | `pilubluban` |  | 1 |
| stochastic-p4-d0.1@6080 | `pilubluban` |  | 1 |
| stochastic-p4-d0.1@8192 | `pilubluban` |  | 1 |
| stochastic-p4-d0.1@16384 | `pilubluban` |  | 1 |
| stochastic-p4-d0.2@6080 | `pi+lubluban` |  | 2 |
| stochastic-p4-d0.2@8192 | `pilubluban` |  | 1 |
| stochastic-p4-d0.2@16384 | `pilubluban` |  | 1 |
| unigram-ablation@6080 | `pilubluban` |  | 1 |

## `pikakasaman`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `pi+kakasam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pika+kas+aman` |  | 3 |
| plain@8192 | `pika+kas+aman` |  | 3 |
| plain@16384 | `pika+kasaman` |  | 2 |
| morphbpe@6080 | `pika+kas+aman` |  | 3 |
| morphbpe@8192 | `pika+kas+aman` |  | 3 |
| morphbpe@16384 | `pika+kasaman` |  | 2 |
| penalty-1@6080 | `pika+kas+aman` |  | 3 |
| penalty-1@8192 | `pika+kas+aman` |  | 3 |
| penalty-1@16384 | `pika+kasaman` |  | 2 |
| penalty-2@6080 | `pika+kas+aman` |  | 3 |
| penalty-2@8192 | `pika+kas+aman` |  | 3 |
| penalty-2@16384 | `pika+kasaman` |  | 2 |
| penalty-4@6080 | `pi+ka+kas+aman` |  | 4 |
| penalty-4@8192 | `pika+kas+aman` |  | 3 |
| penalty-4@16384 | `pika+kasaman` |  | 2 |
| penalty-8@6080 | `pika+kas+aman` |  | 3 |
| penalty-8@8192 | `pika+kas+aman` |  | 3 |
| penalty-8@16384 | `pika+kasaman` |  | 2 |
| stochastic-p4-d0.1@6080 | `pika+kas+aman` |  | 3 |
| stochastic-p4-d0.1@8192 | `pika+kas+aman` |  | 3 |
| stochastic-p4-d0.1@16384 | `pika+kasaman` |  | 2 |
| stochastic-p4-d0.2@6080 | `pika+kas+aman` |  | 3 |
| stochastic-p4-d0.2@8192 | `pika+kas+aman` |  | 3 |
| stochastic-p4-d0.2@16384 | `pika+kasaman` |  | 2 |
| unigram-ablation@6080 | `pi+ka+kasama+n` |  | 4 |

## `inatulan`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `i+natul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `in+atulan` |  | 2 |
| plain@8192 | `in+atulan` |  | 2 |
| plain@16384 | `inatulan` |  | 1 |
| morphbpe@6080 | `inat+ulan` |  | 2 |
| morphbpe@8192 | `inat+ulan` |  | 2 |
| morphbpe@16384 | `inatulan` |  | 1 |
| penalty-1@6080 | `in+atul+an` |  | 3 |
| penalty-1@8192 | `in+atul+an` |  | 3 |
| penalty-1@16384 | `inatulan` |  | 1 |
| penalty-2@6080 | `in+atul+an` |  | 3 |
| penalty-2@8192 | `in+atul+an` |  | 3 |
| penalty-2@16384 | `inatulan` |  | 1 |
| penalty-4@6080 | `in+atul+an` |  | 3 |
| penalty-4@8192 | `in+atul+an` |  | 3 |
| penalty-4@16384 | `inatulan` |  | 1 |
| penalty-8@6080 | `in+atul+an` |  | 3 |
| penalty-8@8192 | `in+atul+an` |  | 3 |
| penalty-8@16384 | `inatulan` |  | 1 |
| stochastic-p4-d0.1@6080 | `in+atul+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `in+atul+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `inatulan` |  | 1 |
| stochastic-p4-d0.2@6080 | `inat+ul+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `inat+ul+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `inatulan` |  | 1 |
| unigram-ablation@6080 | `in+atulan` |  | 2 |

## `pibandyan`  (prefixation+suffixation, tier B_moderate_silver)

**silver gold:** `pi+bandy+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `piband+yan` |  | 2 |
| plain@8192 | `piband+yan` |  | 2 |
| plain@16384 | `pibandyan` |  | 1 |
| morphbpe@6080 | `pib+and+yan` |  | 3 |
| morphbpe@8192 | `pib+and+yan` |  | 3 |
| morphbpe@16384 | `pibandyan` |  | 1 |
| penalty-1@6080 | `pib+and+yan` |  | 3 |
| penalty-1@8192 | `pib+and+yan` |  | 3 |
| penalty-1@16384 | `pibandyan` |  | 1 |
| penalty-2@6080 | `pib+and+yan` |  | 3 |
| penalty-2@8192 | `pib+and+yan` |  | 3 |
| penalty-2@16384 | `pibandyan` |  | 1 |
| penalty-4@6080 | `pib+and+yan` |  | 3 |
| penalty-4@8192 | `pib+and+yan` |  | 3 |
| penalty-4@16384 | `pibandyan` |  | 1 |
| penalty-8@6080 | `pi+band+yan` |  | 3 |
| penalty-8@8192 | `pi+band+yan` |  | 3 |
| penalty-8@16384 | `pibandyan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pi+ban+d+yan` |  | 4 |
| stochastic-p4-d0.1@8192 | `pi+band+yan` |  | 3 |
| stochastic-p4-d0.1@16384 | `pibandyan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pi+band+yan` |  | 3 |
| stochastic-p4-d0.2@8192 | `pi+band+yan` |  | 3 |
| stochastic-p4-d0.2@16384 | `pibandyan` |  | 1 |
| unigram-ablation@6080 | `pi+ban+d+yan` |  | 4 |

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

## `babai`  (reduplication, tier A_strong_silver)

**silver gold:** `babai`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `babai` | OK | 1 |
| plain@8192 | `babai` | OK | 1 |
| plain@16384 | `babai` | OK | 1 |
| morphbpe@6080 | `babai` | OK | 1 |
| morphbpe@8192 | `babai` | OK | 1 |
| morphbpe@16384 | `babai` | OK | 1 |
| penalty-1@6080 | `babai` | OK | 1 |
| penalty-1@8192 | `babai` | OK | 1 |
| penalty-1@16384 | `babai` | OK | 1 |
| penalty-2@6080 | `babai` | OK | 1 |
| penalty-2@8192 | `babai` | OK | 1 |
| penalty-2@16384 | `babai` | OK | 1 |
| penalty-4@6080 | `babai` | OK | 1 |
| penalty-4@8192 | `babai` | OK | 1 |
| penalty-4@16384 | `babai` | OK | 1 |
| penalty-8@6080 | `babai` | OK | 1 |
| penalty-8@8192 | `babai` | OK | 1 |
| penalty-8@16384 | `babai` | OK | 1 |
| stochastic-p4-d0.1@6080 | `babai` | OK | 1 |
| stochastic-p4-d0.1@8192 | `babai` | OK | 1 |
| stochastic-p4-d0.1@16384 | `babai` | OK | 1 |
| stochastic-p4-d0.2@6080 | `babai` | OK | 1 |
| stochastic-p4-d0.2@8192 | `babai` | OK | 1 |
| stochastic-p4-d0.2@16384 | `babai` | OK | 1 |
| unigram-ablation@6080 | `babai` | OK | 1 |

## `kekeng`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `kekeng`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kekeng` | OK | 1 |
| plain@8192 | `kekeng` | OK | 1 |
| plain@16384 | `kekeng` | OK | 1 |
| morphbpe@6080 | `kekeng` | OK | 1 |
| morphbpe@8192 | `kekeng` | OK | 1 |
| morphbpe@16384 | `kekeng` | OK | 1 |
| penalty-1@6080 | `kekeng` | OK | 1 |
| penalty-1@8192 | `kekeng` | OK | 1 |
| penalty-1@16384 | `kekeng` | OK | 1 |
| penalty-2@6080 | `kekeng` | OK | 1 |
| penalty-2@8192 | `kekeng` | OK | 1 |
| penalty-2@16384 | `kekeng` | OK | 1 |
| penalty-4@6080 | `kekeng` | OK | 1 |
| penalty-4@8192 | `kekeng` | OK | 1 |
| penalty-4@16384 | `kekeng` | OK | 1 |
| penalty-8@6080 | `kekeng` | OK | 1 |
| penalty-8@8192 | `kekeng` | OK | 1 |
| penalty-8@16384 | `kekeng` | OK | 1 |
| stochastic-p4-d0.1@6080 | `kekeng` | OK | 1 |
| stochastic-p4-d0.1@8192 | `kekeng` | OK | 1 |
| stochastic-p4-d0.1@16384 | `kekeng` | OK | 1 |
| stochastic-p4-d0.2@6080 | `kekeng` | OK | 1 |
| stochastic-p4-d0.2@8192 | `kekeng` | OK | 1 |
| stochastic-p4-d0.2@16384 | `kekeng` | OK | 1 |
| unigram-ablation@6080 | `ke+keng` |  | 2 |

## `tutu`  (reduplication, tier B_moderate_silver)

**silver gold:** `tutu`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tutu` | OK | 1 |
| plain@8192 | `tutu` | OK | 1 |
| plain@16384 | `tutu` | OK | 1 |
| morphbpe@6080 | `tutu` | OK | 1 |
| morphbpe@8192 | `tutu` | OK | 1 |
| morphbpe@16384 | `tutu` | OK | 1 |
| penalty-1@6080 | `tutu` | OK | 1 |
| penalty-1@8192 | `tutu` | OK | 1 |
| penalty-1@16384 | `tutu` | OK | 1 |
| penalty-2@6080 | `tutu` | OK | 1 |
| penalty-2@8192 | `tutu` | OK | 1 |
| penalty-2@16384 | `tutu` | OK | 1 |
| penalty-4@6080 | `tutu` | OK | 1 |
| penalty-4@8192 | `tutu` | OK | 1 |
| penalty-4@16384 | `tutu` | OK | 1 |
| penalty-8@6080 | `tutu` | OK | 1 |
| penalty-8@8192 | `tutu` | OK | 1 |
| penalty-8@16384 | `tutu` | OK | 1 |
| stochastic-p4-d0.1@6080 | `tutu` | OK | 1 |
| stochastic-p4-d0.1@8192 | `tutu` | OK | 1 |
| stochastic-p4-d0.1@16384 | `tutu` | OK | 1 |
| stochastic-p4-d0.2@6080 | `tutu` | OK | 1 |
| stochastic-p4-d0.2@8192 | `tutu` | OK | 1 |
| stochastic-p4-d0.2@16384 | `tutu` | OK | 1 |
| unigram-ablation@6080 | `tutu` | OK | 1 |

## `lalaking`  (reduplication, tier B_moderate_silver)

**silver gold:** `lalaking`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lalaking` | OK | 1 |
| plain@8192 | `lalaking` | OK | 1 |
| plain@16384 | `lalaking` | OK | 1 |
| morphbpe@6080 | `lalaking` | OK | 1 |
| morphbpe@8192 | `lalaking` | OK | 1 |
| morphbpe@16384 | `lalaking` | OK | 1 |
| penalty-1@6080 | `lalaking` | OK | 1 |
| penalty-1@8192 | `lalaking` | OK | 1 |
| penalty-1@16384 | `lalaking` | OK | 1 |
| penalty-2@6080 | `lalaking` | OK | 1 |
| penalty-2@8192 | `lalaking` | OK | 1 |
| penalty-2@16384 | `lalaking` | OK | 1 |
| penalty-4@6080 | `lalaking` | OK | 1 |
| penalty-4@8192 | `lalaking` | OK | 1 |
| penalty-4@16384 | `lalaking` | OK | 1 |
| penalty-8@6080 | `lalaking` | OK | 1 |
| penalty-8@8192 | `lalaking` | OK | 1 |
| penalty-8@16384 | `lalaking` | OK | 1 |
| stochastic-p4-d0.1@6080 | `lalaking` | OK | 1 |
| stochastic-p4-d0.1@8192 | `lalaking` | OK | 1 |
| stochastic-p4-d0.1@16384 | `lalaking` | OK | 1 |
| stochastic-p4-d0.2@6080 | `lalaking` | OK | 1 |
| stochastic-p4-d0.2@8192 | `lalaking` | OK | 1 |
| stochastic-p4-d0.2@16384 | `lalaking` | OK | 1 |
| unigram-ablation@6080 | `lalaki+ng` |  | 2 |

## `tatakut`  (reduplication, tier A_strong_silver)

**silver gold:** `tatakut`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tatakut` | OK | 1 |
| plain@8192 | `tatakut` | OK | 1 |
| plain@16384 | `tatakut` | OK | 1 |
| morphbpe@6080 | `tat+ak+ut` |  | 3 |
| morphbpe@8192 | `tatak+ut` |  | 2 |
| morphbpe@16384 | `tatak+ut` |  | 2 |
| penalty-1@6080 | `tat+ak+ut` |  | 3 |
| penalty-1@8192 | `tatak+ut` |  | 2 |
| penalty-1@16384 | `tatak+ut` |  | 2 |
| penalty-2@6080 | `tat+ak+ut` |  | 3 |
| penalty-2@8192 | `tatak+ut` |  | 2 |
| penalty-2@16384 | `tatak+ut` |  | 2 |
| penalty-4@6080 | `tat+aku+t` |  | 3 |
| penalty-4@8192 | `tat+aku+t` |  | 3 |
| penalty-4@16384 | `tat+akut` |  | 2 |
| penalty-8@6080 | `tat+aku+t` |  | 3 |
| penalty-8@8192 | `tat+aku+t` |  | 3 |
| penalty-8@16384 | `tat+akut` |  | 2 |
| stochastic-p4-d0.1@6080 | `tata+kut` |  | 2 |
| stochastic-p4-d0.1@8192 | `tata+kut` |  | 2 |
| stochastic-p4-d0.1@16384 | `tata+kut` |  | 2 |
| stochastic-p4-d0.2@6080 | `tata+kut` |  | 2 |
| stochastic-p4-d0.2@8192 | `tata+kut` |  | 2 |
| stochastic-p4-d0.2@16384 | `tata+kut` |  | 2 |
| unigram-ablation@6080 | `tatakut` | OK | 1 |

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

## `gagawan`  (reduplication, tier B_moderate_silver)

**silver gold:** `gagawan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gagawan` | OK | 1 |
| plain@8192 | `gagawan` | OK | 1 |
| plain@16384 | `gagawan` | OK | 1 |
| morphbpe@6080 | `gagawan` | OK | 1 |
| morphbpe@8192 | `gagawan` | OK | 1 |
| morphbpe@16384 | `gagawan` | OK | 1 |
| penalty-1@6080 | `gagawan` | OK | 1 |
| penalty-1@8192 | `gagawan` | OK | 1 |
| penalty-1@16384 | `gagawan` | OK | 1 |
| penalty-2@6080 | `gagawan` | OK | 1 |
| penalty-2@8192 | `gagawan` | OK | 1 |
| penalty-2@16384 | `gagawan` | OK | 1 |
| penalty-4@6080 | `gagawan` | OK | 1 |
| penalty-4@8192 | `gagawan` | OK | 1 |
| penalty-4@16384 | `gagawan` | OK | 1 |
| penalty-8@6080 | `gagawan` | OK | 1 |
| penalty-8@8192 | `gagawan` | OK | 1 |
| penalty-8@16384 | `gagawan` | OK | 1 |
| stochastic-p4-d0.1@6080 | `gagawan` | OK | 1 |
| stochastic-p4-d0.1@8192 | `gagawan` | OK | 1 |
| stochastic-p4-d0.1@16384 | `gagawan` | OK | 1 |
| stochastic-p4-d0.2@6080 | `gagawan` | OK | 1 |
| stochastic-p4-d0.2@8192 | `gagawan` | OK | 1 |
| stochastic-p4-d0.2@16384 | `gagawan` | OK | 1 |
| unigram-ablation@6080 | `gagawan` | OK | 1 |

## `babayi`  (reduplication, tier A_strong_silver)

**silver gold:** `babayi`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bab+ayi` |  | 2 |
| plain@8192 | `babayi` | OK | 1 |
| plain@16384 | `babayi` | OK | 1 |
| morphbpe@6080 | `babay+i` |  | 2 |
| morphbpe@8192 | `babayi` | OK | 1 |
| morphbpe@16384 | `babayi` | OK | 1 |
| penalty-1@6080 | `babay+i` |  | 2 |
| penalty-1@8192 | `babayi` | OK | 1 |
| penalty-1@16384 | `babayi` | OK | 1 |
| penalty-2@6080 | `babay+i` |  | 2 |
| penalty-2@8192 | `babayi` | OK | 1 |
| penalty-2@16384 | `babayi` | OK | 1 |
| penalty-4@6080 | `baba+yi` |  | 2 |
| penalty-4@8192 | `babayi` | OK | 1 |
| penalty-4@16384 | `babayi` | OK | 1 |
| penalty-8@6080 | `baba+yi` |  | 2 |
| penalty-8@8192 | `babayi` | OK | 1 |
| penalty-8@16384 | `babayi` | OK | 1 |
| stochastic-p4-d0.1@6080 | `baba+yi` |  | 2 |
| stochastic-p4-d0.1@8192 | `babayi` | OK | 1 |
| stochastic-p4-d0.1@16384 | `babayi` | OK | 1 |
| stochastic-p4-d0.2@6080 | `baba+yi` |  | 2 |
| stochastic-p4-d0.2@8192 | `babayi` | OK | 1 |
| stochastic-p4-d0.2@16384 | `babayi` | OK | 1 |
| unigram-ablation@6080 | `babayi` | OK | 1 |

## `lalakad`  (reduplication, tier A_strong_silver)

**silver gold:** `lalakad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lalakad` | OK | 1 |
| plain@8192 | `lalakad` | OK | 1 |
| plain@16384 | `lalakad` | OK | 1 |
| morphbpe@6080 | `l+alakad` |  | 2 |
| morphbpe@8192 | `l+alakad` |  | 2 |
| morphbpe@16384 | `l+alakad` |  | 2 |
| penalty-1@6080 | `l+alakad` |  | 2 |
| penalty-1@8192 | `l+alakad` |  | 2 |
| penalty-1@16384 | `l+alakad` |  | 2 |
| penalty-2@6080 | `lala+kad` |  | 2 |
| penalty-2@8192 | `lala+kad` |  | 2 |
| penalty-2@16384 | `lala+kad` |  | 2 |
| penalty-4@6080 | `lala+kad` |  | 2 |
| penalty-4@8192 | `lala+kad` |  | 2 |
| penalty-4@16384 | `lala+kad` |  | 2 |
| penalty-8@6080 | `lala+kad` |  | 2 |
| penalty-8@8192 | `lala+kad` |  | 2 |
| penalty-8@16384 | `lala+kad` |  | 2 |
| stochastic-p4-d0.1@6080 | `lala+kad` |  | 2 |
| stochastic-p4-d0.1@8192 | `lala+kad` |  | 2 |
| stochastic-p4-d0.1@16384 | `lala+kad` |  | 2 |
| stochastic-p4-d0.2@6080 | `lala+kad` |  | 2 |
| stochastic-p4-d0.2@8192 | `lala+kad` |  | 2 |
| stochastic-p4-d0.2@16384 | `lala+kad` |  | 2 |
| unigram-ablation@6080 | `la+lakad` |  | 2 |

## `tata`  (reduplication, tier A_strong_silver)

**silver gold:** `tata`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tata` | OK | 1 |
| plain@8192 | `tata` | OK | 1 |
| plain@16384 | `tata` | OK | 1 |
| morphbpe@6080 | `tata` | OK | 1 |
| morphbpe@8192 | `tata` | OK | 1 |
| morphbpe@16384 | `tata` | OK | 1 |
| penalty-1@6080 | `tata` | OK | 1 |
| penalty-1@8192 | `tata` | OK | 1 |
| penalty-1@16384 | `tata` | OK | 1 |
| penalty-2@6080 | `tata` | OK | 1 |
| penalty-2@8192 | `tata` | OK | 1 |
| penalty-2@16384 | `tata` | OK | 1 |
| penalty-4@6080 | `tata` | OK | 1 |
| penalty-4@8192 | `tata` | OK | 1 |
| penalty-4@16384 | `tata` | OK | 1 |
| penalty-8@6080 | `tata` | OK | 1 |
| penalty-8@8192 | `tata` | OK | 1 |
| penalty-8@16384 | `tata` | OK | 1 |
| stochastic-p4-d0.1@6080 | `tata` | OK | 1 |
| stochastic-p4-d0.1@8192 | `tata` | OK | 1 |
| stochastic-p4-d0.1@16384 | `tata` | OK | 1 |
| stochastic-p4-d0.2@6080 | `tata` | OK | 1 |
| stochastic-p4-d0.2@8192 | `tata` | OK | 1 |
| stochastic-p4-d0.2@16384 | `tata` | OK | 1 |
| unigram-ablation@6080 | `tata` | OK | 1 |

## `tutung`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tutung`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tutung` | OK | 1 |
| plain@8192 | `tutung` | OK | 1 |
| plain@16384 | `tutung` | OK | 1 |
| morphbpe@6080 | `tut+ung` |  | 2 |
| morphbpe@8192 | `tut+ung` |  | 2 |
| morphbpe@16384 | `tut+ung` |  | 2 |
| penalty-1@6080 | `tut+ung` |  | 2 |
| penalty-1@8192 | `tut+ung` |  | 2 |
| penalty-1@16384 | `tut+ung` |  | 2 |
| penalty-2@6080 | `tut+ung` |  | 2 |
| penalty-2@8192 | `tut+ung` |  | 2 |
| penalty-2@16384 | `tut+ung` |  | 2 |
| penalty-4@6080 | `tu+tung` |  | 2 |
| penalty-4@8192 | `tu+tung` |  | 2 |
| penalty-4@16384 | `tu+tung` |  | 2 |
| penalty-8@6080 | `tu+tung` |  | 2 |
| penalty-8@8192 | `tu+tung` |  | 2 |
| penalty-8@16384 | `tu+tung` |  | 2 |
| stochastic-p4-d0.1@6080 | `tu+tung` |  | 2 |
| stochastic-p4-d0.1@8192 | `tu+tung` |  | 2 |
| stochastic-p4-d0.1@16384 | `tu+tung` |  | 2 |
| stochastic-p4-d0.2@6080 | `tu+tung` |  | 2 |
| stochastic-p4-d0.2@8192 | `tu+tung` |  | 2 |
| stochastic-p4-d0.2@16384 | `tu+tung` |  | 2 |
| unigram-ablation@6080 | `tutung` | OK | 1 |

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

## `lulual`  (reduplication, tier A_strong_silver)

**silver gold:** `lulual`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lulu+al` |  | 2 |
| plain@8192 | `lulual` | OK | 1 |
| plain@16384 | `lulual` | OK | 1 |
| morphbpe@6080 | `lulu+al` |  | 2 |
| morphbpe@8192 | `lulu+al` |  | 2 |
| morphbpe@16384 | `lulu+al` |  | 2 |
| penalty-1@6080 | `lulu+al` |  | 2 |
| penalty-1@8192 | `lulu+al` |  | 2 |
| penalty-1@16384 | `lulu+al` |  | 2 |
| penalty-2@6080 | `lulu+al` |  | 2 |
| penalty-2@8192 | `lulu+al` |  | 2 |
| penalty-2@16384 | `lulu+al` |  | 2 |
| penalty-4@6080 | `lulu+al` |  | 2 |
| penalty-4@8192 | `lulu+al` |  | 2 |
| penalty-4@16384 | `lulu+al` |  | 2 |
| penalty-8@6080 | `lu+lual` |  | 2 |
| penalty-8@8192 | `lu+lual` |  | 2 |
| penalty-8@16384 | `lu+lual` |  | 2 |
| stochastic-p4-d0.1@6080 | `lulu+al` |  | 2 |
| stochastic-p4-d0.1@8192 | `lulu+al` |  | 2 |
| stochastic-p4-d0.1@16384 | `lulu+al` |  | 2 |
| stochastic-p4-d0.2@6080 | `lu+lual` |  | 2 |
| stochastic-p4-d0.2@8192 | `lu+lual` |  | 2 |
| stochastic-p4-d0.2@16384 | `lu+lual` |  | 2 |
| unigram-ablation@6080 | `lu+lual` |  | 2 |

## `nanan`  (reduplication, tier A_strong_silver)

**silver gold:** `nanan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `nan+an` |  | 2 |
| plain@8192 | `nanan` | OK | 1 |
| plain@16384 | `nanan` | OK | 1 |
| morphbpe@6080 | `nan+an` |  | 2 |
| morphbpe@8192 | `nan+an` |  | 2 |
| morphbpe@16384 | `nan+an` |  | 2 |
| penalty-1@6080 | `nan+an` |  | 2 |
| penalty-1@8192 | `nan+an` |  | 2 |
| penalty-1@16384 | `nan+an` |  | 2 |
| penalty-2@6080 | `nan+an` |  | 2 |
| penalty-2@8192 | `nan+an` |  | 2 |
| penalty-2@16384 | `nan+an` |  | 2 |
| penalty-4@6080 | `nan+an` |  | 2 |
| penalty-4@8192 | `nan+an` |  | 2 |
| penalty-4@16384 | `nan+an` |  | 2 |
| penalty-8@6080 | `nan+an` |  | 2 |
| penalty-8@8192 | `nan+an` |  | 2 |
| penalty-8@16384 | `nan+an` |  | 2 |
| stochastic-p4-d0.1@6080 | `nan+an` |  | 2 |
| stochastic-p4-d0.1@8192 | `nan+an` |  | 2 |
| stochastic-p4-d0.1@16384 | `nan+an` |  | 2 |
| stochastic-p4-d0.2@6080 | `nan+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `nan+an` |  | 2 |
| stochastic-p4-d0.2@16384 | `nanan` | OK | 1 |
| unigram-ablation@6080 | `na+nan` |  | 2 |

## `kakanan`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `kakan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kakanan` |  | 1 |
| plain@8192 | `kakanan` |  | 1 |
| plain@16384 | `kakanan` |  | 1 |
| morphbpe@6080 | `kakanan` |  | 1 |
| morphbpe@8192 | `kakanan` |  | 1 |
| morphbpe@16384 | `kakanan` |  | 1 |
| penalty-1@6080 | `kakanan` |  | 1 |
| penalty-1@8192 | `kakanan` |  | 1 |
| penalty-1@16384 | `kakanan` |  | 1 |
| penalty-2@6080 | `kakanan` |  | 1 |
| penalty-2@8192 | `kakanan` |  | 1 |
| penalty-2@16384 | `kakanan` |  | 1 |
| penalty-4@6080 | `kakanan` |  | 1 |
| penalty-4@8192 | `kakanan` |  | 1 |
| penalty-4@16384 | `kakanan` |  | 1 |
| penalty-8@6080 | `kakanan` |  | 1 |
| penalty-8@8192 | `kakanan` |  | 1 |
| penalty-8@16384 | `kakanan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+kan+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `ka+kan+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `ka+kan+an` |  | 3 |
| stochastic-p4-d0.2@6080 | `ka+kan+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `ka+kan+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `ka+kan+an` |  | 3 |
| unigram-ablation@6080 | `kakanan` |  | 1 |

## `tatang`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tatang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tatang` | OK | 1 |
| plain@8192 | `tatang` | OK | 1 |
| plain@16384 | `tatang` | OK | 1 |
| morphbpe@6080 | `tatang` | OK | 1 |
| morphbpe@8192 | `tatang` | OK | 1 |
| morphbpe@16384 | `tatang` | OK | 1 |
| penalty-1@6080 | `tatang` | OK | 1 |
| penalty-1@8192 | `tatang` | OK | 1 |
| penalty-1@16384 | `tatang` | OK | 1 |
| penalty-2@6080 | `tatang` | OK | 1 |
| penalty-2@8192 | `tatang` | OK | 1 |
| penalty-2@16384 | `tatang` | OK | 1 |
| penalty-4@6080 | `tatang` | OK | 1 |
| penalty-4@8192 | `tatang` | OK | 1 |
| penalty-4@16384 | `tatang` | OK | 1 |
| penalty-8@6080 | `tatang` | OK | 1 |
| penalty-8@8192 | `tatang` | OK | 1 |
| penalty-8@16384 | `tatang` | OK | 1 |
| stochastic-p4-d0.1@6080 | `tatang` | OK | 1 |
| stochastic-p4-d0.1@8192 | `tatang` | OK | 1 |
| stochastic-p4-d0.1@16384 | `tatang` | OK | 1 |
| stochastic-p4-d0.2@6080 | `tatang` | OK | 1 |
| stochastic-p4-d0.2@8192 | `tatang` | OK | 1 |
| stochastic-p4-d0.2@16384 | `tatang` | OK | 1 |
| unigram-ablation@6080 | `tatang` | OK | 1 |

## `mamagus`  (reduplication, tier B_moderate_silver)

**silver gold:** `mamagus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mam+agus` |  | 2 |
| plain@8192 | `mamagus` | OK | 1 |
| plain@16384 | `mamagus` | OK | 1 |
| morphbpe@6080 | `mam+agus` |  | 2 |
| morphbpe@8192 | `mam+agus` |  | 2 |
| morphbpe@16384 | `mam+agus` |  | 2 |
| penalty-1@6080 | `mam+agus` |  | 2 |
| penalty-1@8192 | `mam+agus` |  | 2 |
| penalty-1@16384 | `mam+agus` |  | 2 |
| penalty-2@6080 | `mam+agus` |  | 2 |
| penalty-2@8192 | `mam+agus` |  | 2 |
| penalty-2@16384 | `mam+agus` |  | 2 |
| penalty-4@6080 | `mam+agus` |  | 2 |
| penalty-4@8192 | `mam+agus` |  | 2 |
| penalty-4@16384 | `mam+agus` |  | 2 |
| penalty-8@6080 | `mam+agus` |  | 2 |
| penalty-8@8192 | `mam+agus` |  | 2 |
| penalty-8@16384 | `mam+agus` |  | 2 |
| stochastic-p4-d0.1@6080 | `mam+agus` |  | 2 |
| stochastic-p4-d0.1@8192 | `mam+agus` |  | 2 |
| stochastic-p4-d0.1@16384 | `mam+agus` |  | 2 |
| stochastic-p4-d0.2@6080 | `mam+agus` |  | 2 |
| stochastic-p4-d0.2@8192 | `mam+agus` |  | 2 |
| stochastic-p4-d0.2@16384 | `mam+agus` |  | 2 |
| unigram-ablation@6080 | `mamagu+s` |  | 2 |

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

## `lalawan`  (reduplication, tier B_moderate_silver)

**silver gold:** `lalawan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lala+wan` |  | 2 |
| plain@8192 | `lala+wan` |  | 2 |
| plain@16384 | `lalawan` | OK | 1 |
| morphbpe@6080 | `lala+wan` |  | 2 |
| morphbpe@8192 | `lala+wan` |  | 2 |
| morphbpe@16384 | `lala+wan` |  | 2 |
| penalty-1@6080 | `lala+wan` |  | 2 |
| penalty-1@8192 | `lala+wan` |  | 2 |
| penalty-1@16384 | `lala+wan` |  | 2 |
| penalty-2@6080 | `lala+wan` |  | 2 |
| penalty-2@8192 | `lala+wan` |  | 2 |
| penalty-2@16384 | `lala+wan` |  | 2 |
| penalty-4@6080 | `lala+wan` |  | 2 |
| penalty-4@8192 | `lala+wan` |  | 2 |
| penalty-4@16384 | `lala+wan` |  | 2 |
| penalty-8@6080 | `lala+wan` |  | 2 |
| penalty-8@8192 | `lala+wan` |  | 2 |
| penalty-8@16384 | `lala+wan` |  | 2 |
| stochastic-p4-d0.1@6080 | `lala+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `lala+wan` |  | 2 |
| stochastic-p4-d0.1@16384 | `lala+wan` |  | 2 |
| stochastic-p4-d0.2@6080 | `lala+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `lala+wan` |  | 2 |
| stochastic-p4-d0.2@16384 | `lala+wan` |  | 2 |
| unigram-ablation@6080 | `la+lawan` |  | 2 |

## `mamaus`  (reduplication, tier B_moderate_silver)

**silver gold:** `mamaus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mam+aus` |  | 2 |
| plain@8192 | `mam+aus` |  | 2 |
| plain@16384 | `mamaus` | OK | 1 |
| morphbpe@6080 | `mam+aus` |  | 2 |
| morphbpe@8192 | `mam+aus` |  | 2 |
| morphbpe@16384 | `mam+aus` |  | 2 |
| penalty-1@6080 | `mam+aus` |  | 2 |
| penalty-1@8192 | `mam+aus` |  | 2 |
| penalty-1@16384 | `mam+aus` |  | 2 |
| penalty-2@6080 | `mam+aus` |  | 2 |
| penalty-2@8192 | `mam+aus` |  | 2 |
| penalty-2@16384 | `mam+aus` |  | 2 |
| penalty-4@6080 | `mam+aus` |  | 2 |
| penalty-4@8192 | `mam+aus` |  | 2 |
| penalty-4@16384 | `mam+aus` |  | 2 |
| penalty-8@6080 | `mam+aus` |  | 2 |
| penalty-8@8192 | `mam+aus` |  | 2 |
| penalty-8@16384 | `mam+aus` |  | 2 |
| stochastic-p4-d0.1@6080 | `mam+aus` |  | 2 |
| stochastic-p4-d0.1@8192 | `mam+aus` |  | 2 |
| stochastic-p4-d0.1@16384 | `mam+aus` |  | 2 |
| stochastic-p4-d0.2@6080 | `mam+aus` |  | 2 |
| stochastic-p4-d0.2@8192 | `mam+aus` |  | 2 |
| stochastic-p4-d0.2@16384 | `mam+aus` |  | 2 |
| unigram-ablation@6080 | `mama+us` |  | 2 |

## `tatalakad`  (reduplication, tier A_strong_silver)

**silver gold:** `tatalakad`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tat+alakad` |  | 2 |
| plain@8192 | `tat+alakad` |  | 2 |
| plain@16384 | `tatalakad` | OK | 1 |
| morphbpe@6080 | `tat+alakad` |  | 2 |
| morphbpe@8192 | `tat+alakad` |  | 2 |
| morphbpe@16384 | `tat+alakad` |  | 2 |
| penalty-1@6080 | `tat+alakad` |  | 2 |
| penalty-1@8192 | `tat+alakad` |  | 2 |
| penalty-1@16384 | `tat+alakad` |  | 2 |
| penalty-2@6080 | `tat+alakad` |  | 2 |
| penalty-2@8192 | `tat+alakad` |  | 2 |
| penalty-2@16384 | `tat+alakad` |  | 2 |
| penalty-4@6080 | `tat+alakad` |  | 2 |
| penalty-4@8192 | `tat+alakad` |  | 2 |
| penalty-4@16384 | `tat+alakad` |  | 2 |
| penalty-8@6080 | `tat+alakad` |  | 2 |
| penalty-8@8192 | `tat+alakad` |  | 2 |
| penalty-8@16384 | `tat+alakad` |  | 2 |
| stochastic-p4-d0.1@6080 | `tat+alakad` |  | 2 |
| stochastic-p4-d0.1@8192 | `tat+alakad` |  | 2 |
| stochastic-p4-d0.1@16384 | `tat+alakad` |  | 2 |
| stochastic-p4-d0.2@6080 | `tat+ala+kad` |  | 3 |
| stochastic-p4-d0.2@8192 | `tat+ala+kad` |  | 3 |
| stochastic-p4-d0.2@16384 | `tatala+kad` |  | 2 |
| unigram-ablation@6080 | `tata+lakad` |  | 2 |

## `gagapang`  (reduplication, tier A_strong_silver)

**silver gold:** `gagapang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gag+apang` |  | 2 |
| plain@8192 | `gag+apang` |  | 2 |
| plain@16384 | `gagapang` | OK | 1 |
| morphbpe@6080 | `gag+apang` |  | 2 |
| morphbpe@8192 | `gag+apang` |  | 2 |
| morphbpe@16384 | `gag+apang` |  | 2 |
| penalty-1@6080 | `gag+apang` |  | 2 |
| penalty-1@8192 | `gag+apang` |  | 2 |
| penalty-1@16384 | `gag+apang` |  | 2 |
| penalty-2@6080 | `gag+apang` |  | 2 |
| penalty-2@8192 | `gag+apang` |  | 2 |
| penalty-2@16384 | `gag+apang` |  | 2 |
| penalty-4@6080 | `gaga+pang` |  | 2 |
| penalty-4@8192 | `gaga+pang` |  | 2 |
| penalty-4@16384 | `gaga+pang` |  | 2 |
| penalty-8@6080 | `ga+ga+pang` |  | 3 |
| penalty-8@8192 | `ga+gapang` |  | 2 |
| penalty-8@16384 | `ga+gapang` |  | 2 |
| stochastic-p4-d0.1@6080 | `ga+ga+pang` |  | 3 |
| stochastic-p4-d0.1@8192 | `ga+ga+pang` |  | 3 |
| stochastic-p4-d0.1@16384 | `ga+gapang` |  | 2 |
| stochastic-p4-d0.2@6080 | `ga+ga+pang` |  | 3 |
| stochastic-p4-d0.2@8192 | `ga+ga+pang` |  | 3 |
| stochastic-p4-d0.2@16384 | `ga+gapang` |  | 2 |
| unigram-ablation@6080 | `gaga+pang` |  | 2 |

## `lalawe`  (reduplication, tier A_strong_silver)

**silver gold:** `lalawe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lalawe` | OK | 1 |
| plain@8192 | `lalawe` | OK | 1 |
| plain@16384 | `lalawe` | OK | 1 |
| morphbpe@6080 | `lalawe` | OK | 1 |
| morphbpe@8192 | `lalawe` | OK | 1 |
| morphbpe@16384 | `lalawe` | OK | 1 |
| penalty-1@6080 | `lalawe` | OK | 1 |
| penalty-1@8192 | `lalawe` | OK | 1 |
| penalty-1@16384 | `lalawe` | OK | 1 |
| penalty-2@6080 | `lalawe` | OK | 1 |
| penalty-2@8192 | `lalawe` | OK | 1 |
| penalty-2@16384 | `lalawe` | OK | 1 |
| penalty-4@6080 | `lalawe` | OK | 1 |
| penalty-4@8192 | `lalawe` | OK | 1 |
| penalty-4@16384 | `lalawe` | OK | 1 |
| penalty-8@6080 | `lalawe` | OK | 1 |
| penalty-8@8192 | `lalawe` | OK | 1 |
| penalty-8@16384 | `lalawe` | OK | 1 |
| stochastic-p4-d0.1@6080 | `lalawe` | OK | 1 |
| stochastic-p4-d0.1@8192 | `lalawe` | OK | 1 |
| stochastic-p4-d0.1@16384 | `lalawe` | OK | 1 |
| stochastic-p4-d0.2@6080 | `lalawe` | OK | 1 |
| stochastic-p4-d0.2@8192 | `lalawe` | OK | 1 |
| stochastic-p4-d0.2@16384 | `lalawe` | OK | 1 |
| unigram-ablation@6080 | `la+lawe` |  | 2 |

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

## `tutula`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tutula`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tut+ula` |  | 2 |
| plain@8192 | `tut+ula` |  | 2 |
| plain@16384 | `tut+ula` |  | 2 |
| morphbpe@6080 | `tut+ula` |  | 2 |
| morphbpe@8192 | `tut+ula` |  | 2 |
| morphbpe@16384 | `tut+ula` |  | 2 |
| penalty-1@6080 | `tut+ula` |  | 2 |
| penalty-1@8192 | `tut+ula` |  | 2 |
| penalty-1@16384 | `tut+ula` |  | 2 |
| penalty-2@6080 | `tut+ula` |  | 2 |
| penalty-2@8192 | `tut+ula` |  | 2 |
| penalty-2@16384 | `tut+ula` |  | 2 |
| penalty-4@6080 | `tutu+la` |  | 2 |
| penalty-4@8192 | `tutu+la` |  | 2 |
| penalty-4@16384 | `tutu+la` |  | 2 |
| penalty-8@6080 | `tu+tula` |  | 2 |
| penalty-8@8192 | `tu+tula` |  | 2 |
| penalty-8@16384 | `tu+tula` |  | 2 |
| stochastic-p4-d0.1@6080 | `tutu+la` |  | 2 |
| stochastic-p4-d0.1@8192 | `tutu+la` |  | 2 |
| stochastic-p4-d0.1@16384 | `tutu+la` |  | 2 |
| stochastic-p4-d0.2@6080 | `tu+tula` |  | 2 |
| stochastic-p4-d0.2@8192 | `tu+tula` |  | 2 |
| stochastic-p4-d0.2@16384 | `tu+tula` |  | 2 |
| unigram-ablation@6080 | `tutu+la` |  | 2 |

## `gagalo`  (reduplication, tier A_strong_silver)

**silver gold:** `gagalo`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gag+alo` |  | 2 |
| plain@8192 | `gag+alo` |  | 2 |
| plain@16384 | `gagalo` | OK | 1 |
| morphbpe@6080 | `gag+alo` |  | 2 |
| morphbpe@8192 | `gag+alo` |  | 2 |
| morphbpe@16384 | `gag+alo` |  | 2 |
| penalty-1@6080 | `gag+alo` |  | 2 |
| penalty-1@8192 | `gag+alo` |  | 2 |
| penalty-1@16384 | `gag+alo` |  | 2 |
| penalty-2@6080 | `gag+alo` |  | 2 |
| penalty-2@8192 | `gag+alo` |  | 2 |
| penalty-2@16384 | `gag+alo` |  | 2 |
| penalty-4@6080 | `gag+alo` |  | 2 |
| penalty-4@8192 | `gag+alo` |  | 2 |
| penalty-4@16384 | `gag+alo` |  | 2 |
| penalty-8@6080 | `ga+galo` |  | 2 |
| penalty-8@8192 | `ga+galo` |  | 2 |
| penalty-8@16384 | `ga+galo` |  | 2 |
| stochastic-p4-d0.1@6080 | `ga+g+alo` |  | 3 |
| stochastic-p4-d0.1@8192 | `ga+g+alo` |  | 3 |
| stochastic-p4-d0.1@16384 | `gag+alo` |  | 2 |
| stochastic-p4-d0.2@6080 | `ga+g+alo` |  | 3 |
| stochastic-p4-d0.2@8192 | `ga+g+alo` |  | 3 |
| stochastic-p4-d0.2@16384 | `ga+g+alo` |  | 3 |
| unigram-ablation@6080 | `gagal+o` |  | 2 |

## `kukuldas`  (reduplication, tier A_strong_silver)

**silver gold:** `kukuldas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kukul+das` |  | 2 |
| plain@8192 | `kukul+das` |  | 2 |
| plain@16384 | `kukuldas` | OK | 1 |
| morphbpe@6080 | `ku+kuldas` |  | 2 |
| morphbpe@8192 | `ku+kuldas` |  | 2 |
| morphbpe@16384 | `ku+kuldas` |  | 2 |
| penalty-1@6080 | `ku+kuldas` |  | 2 |
| penalty-1@8192 | `ku+kuldas` |  | 2 |
| penalty-1@16384 | `ku+kuldas` |  | 2 |
| penalty-2@6080 | `ku+kuldas` |  | 2 |
| penalty-2@8192 | `ku+kuldas` |  | 2 |
| penalty-2@16384 | `ku+kuldas` |  | 2 |
| penalty-4@6080 | `ku+kuldas` |  | 2 |
| penalty-4@8192 | `ku+kuldas` |  | 2 |
| penalty-4@16384 | `ku+kuldas` |  | 2 |
| penalty-8@6080 | `ku+kuldas` |  | 2 |
| penalty-8@8192 | `ku+kuldas` |  | 2 |
| penalty-8@16384 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.1@6080 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.1@8192 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.1@16384 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.2@6080 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.2@8192 | `ku+kuldas` |  | 2 |
| stochastic-p4-d0.2@16384 | `ku+kuldas` |  | 2 |
| unigram-ablation@6080 | `ku+kuldas` |  | 2 |

## `tatas`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tatas`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tat+as` |  | 2 |
| plain@8192 | `tat+as` |  | 2 |
| plain@16384 | `tat+as` |  | 2 |
| morphbpe@6080 | `tat+as` |  | 2 |
| morphbpe@8192 | `tat+as` |  | 2 |
| morphbpe@16384 | `tat+as` |  | 2 |
| penalty-1@6080 | `tat+as` |  | 2 |
| penalty-1@8192 | `tat+as` |  | 2 |
| penalty-1@16384 | `tat+as` |  | 2 |
| penalty-2@6080 | `t+atas` |  | 2 |
| penalty-2@8192 | `t+atas` |  | 2 |
| penalty-2@16384 | `t+atas` |  | 2 |
| penalty-4@6080 | `tat+as` |  | 2 |
| penalty-4@8192 | `tat+as` |  | 2 |
| penalty-4@16384 | `tat+as` |  | 2 |
| penalty-8@6080 | `tat+as` |  | 2 |
| penalty-8@8192 | `tat+as` |  | 2 |
| penalty-8@16384 | `tat+as` |  | 2 |
| stochastic-p4-d0.1@6080 | `tat+as` |  | 2 |
| stochastic-p4-d0.1@8192 | `tat+as` |  | 2 |
| stochastic-p4-d0.1@16384 | `tat+as` |  | 2 |
| stochastic-p4-d0.2@6080 | `tat+as` |  | 2 |
| stochastic-p4-d0.2@8192 | `tat+as` |  | 2 |
| stochastic-p4-d0.2@16384 | `tat+as` |  | 2 |
| unigram-ablation@6080 | `tata+s` |  | 2 |

## `gagalgal`  (reduplication, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `gagalgal`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gag+al+gal` |  | 3 |
| plain@8192 | `gag+al+gal` |  | 3 |
| plain@16384 | `gagalgal` | OK | 1 |
| morphbpe@6080 | `gag+al+gal` |  | 3 |
| morphbpe@8192 | `gag+al+gal` |  | 3 |
| morphbpe@16384 | `gag+al+gal` |  | 3 |
| penalty-1@6080 | `gag+al+gal` |  | 3 |
| penalty-1@8192 | `gag+al+gal` |  | 3 |
| penalty-1@16384 | `gag+al+gal` |  | 3 |
| penalty-2@6080 | `gag+al+gal` |  | 3 |
| penalty-2@8192 | `gag+al+gal` |  | 3 |
| penalty-2@16384 | `gag+al+gal` |  | 3 |
| penalty-4@6080 | `gag+al+gal` |  | 3 |
| penalty-4@8192 | `gag+al+gal` |  | 3 |
| penalty-4@16384 | `gag+al+gal` |  | 3 |
| penalty-8@6080 | `ga+gal+gal` |  | 3 |
| penalty-8@8192 | `ga+gal+gal` |  | 3 |
| penalty-8@16384 | `ga+galgal` |  | 2 |
| stochastic-p4-d0.1@6080 | `ga+g+al+g+al` |  | 5 |
| stochastic-p4-d0.1@8192 | `ga+g+al+g+al` |  | 5 |
| stochastic-p4-d0.1@16384 | `gag+al+g+al` |  | 4 |
| stochastic-p4-d0.2@6080 | `ga+g+al+g+al` |  | 5 |
| stochastic-p4-d0.2@8192 | `ga+g+al+g+al` |  | 5 |
| stochastic-p4-d0.2@16384 | `ga+g+al+g+al` |  | 5 |
| unigram-ablation@6080 | `gagal+gal` |  | 2 |

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

## `yuyutus`  (reduplication, tier B_moderate_silver)

**silver gold:** `yuyutus`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `yu+y+utus` |  | 3 |
| plain@8192 | `yu+yutus` |  | 2 |
| plain@16384 | `yu+yutus` |  | 2 |
| morphbpe@6080 | `yu+y+utus` |  | 3 |
| morphbpe@8192 | `yu+yutus` |  | 2 |
| morphbpe@16384 | `yu+yutus` |  | 2 |
| penalty-1@6080 | `yu+y+utus` |  | 3 |
| penalty-1@8192 | `yu+yutus` |  | 2 |
| penalty-1@16384 | `yu+yutus` |  | 2 |
| penalty-2@6080 | `yu+y+utus` |  | 3 |
| penalty-2@8192 | `yu+yutus` |  | 2 |
| penalty-2@16384 | `yu+yutus` |  | 2 |
| penalty-4@6080 | `yu+yu+tus` |  | 3 |
| penalty-4@8192 | `yu+yutus` |  | 2 |
| penalty-4@16384 | `yu+yutus` |  | 2 |
| penalty-8@6080 | `yu+yu+tus` |  | 3 |
| penalty-8@8192 | `yu+yutus` |  | 2 |
| penalty-8@16384 | `yu+yutus` |  | 2 |
| stochastic-p4-d0.1@6080 | `yu+yu+tus` |  | 3 |
| stochastic-p4-d0.1@8192 | `yu+yutus` |  | 2 |
| stochastic-p4-d0.1@16384 | `yu+yutus` |  | 2 |
| stochastic-p4-d0.2@6080 | `yu+yu+tus` |  | 3 |
| stochastic-p4-d0.2@8192 | `yu+yu+tus` |  | 3 |
| stochastic-p4-d0.2@16384 | `yu+yutus` |  | 2 |
| unigram-ablation@6080 | `yu+y+utus` |  | 3 |

## `lalapit`  (reduplication, tier A_strong_silver)

**silver gold:** `lalapit`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lal+apit` |  | 2 |
| plain@8192 | `lalapit` | OK | 1 |
| plain@16384 | `lalapit` | OK | 1 |
| morphbpe@6080 | `lal+apit` |  | 2 |
| morphbpe@8192 | `lal+apit` |  | 2 |
| morphbpe@16384 | `lal+apit` |  | 2 |
| penalty-1@6080 | `lal+apit` |  | 2 |
| penalty-1@8192 | `lal+apit` |  | 2 |
| penalty-1@16384 | `lal+apit` |  | 2 |
| penalty-2@6080 | `lal+apit` |  | 2 |
| penalty-2@8192 | `lal+apit` |  | 2 |
| penalty-2@16384 | `lal+apit` |  | 2 |
| penalty-4@6080 | `lala+pit` |  | 2 |
| penalty-4@8192 | `lala+pit` |  | 2 |
| penalty-4@16384 | `lala+pit` |  | 2 |
| penalty-8@6080 | `lala+pit` |  | 2 |
| penalty-8@8192 | `lala+pit` |  | 2 |
| penalty-8@16384 | `lala+pit` |  | 2 |
| stochastic-p4-d0.1@6080 | `lala+pit` |  | 2 |
| stochastic-p4-d0.1@8192 | `lala+pit` |  | 2 |
| stochastic-p4-d0.1@16384 | `lala+pit` |  | 2 |
| stochastic-p4-d0.2@6080 | `lala+pit` |  | 2 |
| stochastic-p4-d0.2@8192 | `lala+pit` |  | 2 |
| stochastic-p4-d0.2@16384 | `lala+pit` |  | 2 |
| unigram-ablation@6080 | `la+lapit` |  | 2 |

## `mamamate`  (reduplication, tier B_moderate_silver)

**silver gold:** `mamamate`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mam+amate` |  | 2 |
| plain@8192 | `mam+amate` |  | 2 |
| plain@16384 | `mamamate` | OK | 1 |
| morphbpe@6080 | `mam+amate` |  | 2 |
| morphbpe@8192 | `mam+amate` |  | 2 |
| morphbpe@16384 | `mamamate` | OK | 1 |
| penalty-1@6080 | `mam+amate` |  | 2 |
| penalty-1@8192 | `mam+amate` |  | 2 |
| penalty-1@16384 | `mamamate` | OK | 1 |
| penalty-2@6080 | `mam+amate` |  | 2 |
| penalty-2@8192 | `mam+amate` |  | 2 |
| penalty-2@16384 | `mamamate` | OK | 1 |
| penalty-4@6080 | `mam+amate` |  | 2 |
| penalty-4@8192 | `mam+amate` |  | 2 |
| penalty-4@16384 | `mamamate` | OK | 1 |
| penalty-8@6080 | `mam+amate` |  | 2 |
| penalty-8@8192 | `mam+amate` |  | 2 |
| penalty-8@16384 | `mamamate` | OK | 1 |
| stochastic-p4-d0.1@6080 | `mam+amate` |  | 2 |
| stochastic-p4-d0.1@8192 | `mam+amate` |  | 2 |
| stochastic-p4-d0.1@16384 | `mamamate` | OK | 1 |
| stochastic-p4-d0.2@6080 | `mam+amate` |  | 2 |
| stochastic-p4-d0.2@8192 | `mam+amate` |  | 2 |
| stochastic-p4-d0.2@16384 | `mamamate` | OK | 1 |
| unigram-ablation@6080 | `mama+mate` |  | 2 |

## `sasalpantaya`  (reduplication, tier A_strong_silver)

**silver gold:** `sasalpantaya`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sas+alpantaya` |  | 2 |
| plain@8192 | `sas+alpantaya` |  | 2 |
| plain@16384 | `sas+alpantaya` |  | 2 |
| morphbpe@6080 | `sas+alpantaya` |  | 2 |
| morphbpe@8192 | `sas+alpantaya` |  | 2 |
| morphbpe@16384 | `sas+alpantaya` |  | 2 |
| penalty-1@6080 | `sas+alpantaya` |  | 2 |
| penalty-1@8192 | `sas+alpantaya` |  | 2 |
| penalty-1@16384 | `sas+alpantaya` |  | 2 |
| penalty-2@6080 | `sas+alpantaya` |  | 2 |
| penalty-2@8192 | `sas+alpantaya` |  | 2 |
| penalty-2@16384 | `sas+alpantaya` |  | 2 |
| penalty-4@6080 | `sa+salpantaya` |  | 2 |
| penalty-4@8192 | `sa+salpantaya` |  | 2 |
| penalty-4@16384 | `sa+salpantaya` |  | 2 |
| penalty-8@6080 | `sa+sal+pantaya` |  | 3 |
| penalty-8@8192 | `sa+sal+pantaya` |  | 3 |
| penalty-8@16384 | `sa+salpantaya` |  | 2 |
| stochastic-p4-d0.1@6080 | `sa+sal+pantaya` |  | 3 |
| stochastic-p4-d0.1@8192 | `sa+salpantaya` |  | 2 |
| stochastic-p4-d0.1@16384 | `sa+salpantaya` |  | 2 |
| stochastic-p4-d0.2@6080 | `sa+salpantaya` |  | 2 |
| stochastic-p4-d0.2@8192 | `sa+salpantaya` |  | 2 |
| stochastic-p4-d0.2@16384 | `sa+salpantaya` |  | 2 |
| unigram-ablation@6080 | `sasa+lpantay+a` |  | 3 |

## `bebe`  (reduplication, tier A_strong_silver)

**silver gold:** `bebe`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `b+ebe` |  | 2 |
| plain@8192 | `bebe` | OK | 1 |
| plain@16384 | `bebe` | OK | 1 |
| morphbpe@6080 | `bebe` | OK | 1 |
| morphbpe@8192 | `bebe` | OK | 1 |
| morphbpe@16384 | `bebe` | OK | 1 |
| penalty-1@6080 | `bebe` | OK | 1 |
| penalty-1@8192 | `bebe` | OK | 1 |
| penalty-1@16384 | `bebe` | OK | 1 |
| penalty-2@6080 | `bebe` | OK | 1 |
| penalty-2@8192 | `bebe` | OK | 1 |
| penalty-2@16384 | `bebe` | OK | 1 |
| penalty-4@6080 | `bebe` | OK | 1 |
| penalty-4@8192 | `bebe` | OK | 1 |
| penalty-4@16384 | `bebe` | OK | 1 |
| penalty-8@6080 | `bebe` | OK | 1 |
| penalty-8@8192 | `bebe` | OK | 1 |
| penalty-8@16384 | `bebe` | OK | 1 |
| stochastic-p4-d0.1@6080 | `bebe` | OK | 1 |
| stochastic-p4-d0.1@8192 | `bebe` | OK | 1 |
| stochastic-p4-d0.1@16384 | `bebe` | OK | 1 |
| stochastic-p4-d0.2@6080 | `bebe` | OK | 1 |
| stochastic-p4-d0.2@8192 | `bebe` | OK | 1 |
| stochastic-p4-d0.2@16384 | `bebe` | OK | 1 |
| unigram-ablation@6080 | `bebe` | OK | 1 |

## `gagalang`  (reduplication, tier A_strong_silver)

**silver gold:** `gagalang`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gag+alang` |  | 2 |
| plain@8192 | `gag+alang` |  | 2 |
| plain@16384 | `gag+alang` |  | 2 |
| morphbpe@6080 | `gag+alang` |  | 2 |
| morphbpe@8192 | `gag+alang` |  | 2 |
| morphbpe@16384 | `gag+alang` |  | 2 |
| penalty-1@6080 | `gag+alang` |  | 2 |
| penalty-1@8192 | `gag+alang` |  | 2 |
| penalty-1@16384 | `gag+alang` |  | 2 |
| penalty-2@6080 | `gag+alang` |  | 2 |
| penalty-2@8192 | `gag+alang` |  | 2 |
| penalty-2@16384 | `gag+alang` |  | 2 |
| penalty-4@6080 | `gag+alang` |  | 2 |
| penalty-4@8192 | `gag+alang` |  | 2 |
| penalty-4@16384 | `gag+alang` |  | 2 |
| penalty-8@6080 | `ga+galang` |  | 2 |
| penalty-8@8192 | `ga+galang` |  | 2 |
| penalty-8@16384 | `ga+galang` |  | 2 |
| stochastic-p4-d0.1@6080 | `ga+galang` |  | 2 |
| stochastic-p4-d0.1@8192 | `ga+galang` |  | 2 |
| stochastic-p4-d0.1@16384 | `ga+galang` |  | 2 |
| stochastic-p4-d0.2@6080 | `ga+galang` |  | 2 |
| stochastic-p4-d0.2@8192 | `ga+galang` |  | 2 |
| stochastic-p4-d0.2@16384 | `ga+galang` |  | 2 |
| unigram-ablation@6080 | `gaga+lang` |  | 2 |

## `gagawa`  (reduplication, tier A_strong_silver)

**silver gold:** `gagawa`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gag+awa` |  | 2 |
| plain@8192 | `gag+awa` |  | 2 |
| plain@16384 | `gagawa` | OK | 1 |
| morphbpe@6080 | `gaga+wa` |  | 2 |
| morphbpe@8192 | `gaga+wa` |  | 2 |
| morphbpe@16384 | `gagawa` | OK | 1 |
| penalty-1@6080 | `gaga+wa` |  | 2 |
| penalty-1@8192 | `gaga+wa` |  | 2 |
| penalty-1@16384 | `gagawa` | OK | 1 |
| penalty-2@6080 | `gaga+wa` |  | 2 |
| penalty-2@8192 | `gaga+wa` |  | 2 |
| penalty-2@16384 | `gagawa` | OK | 1 |
| penalty-4@6080 | `gaga+wa` |  | 2 |
| penalty-4@8192 | `gaga+wa` |  | 2 |
| penalty-4@16384 | `gagawa` | OK | 1 |
| penalty-8@6080 | `ga+gawa` |  | 2 |
| penalty-8@8192 | `ga+gawa` |  | 2 |
| penalty-8@16384 | `gagawa` | OK | 1 |
| stochastic-p4-d0.1@6080 | `ga+gawa` |  | 2 |
| stochastic-p4-d0.1@8192 | `gagawa` | OK | 1 |
| stochastic-p4-d0.1@16384 | `gagawa` | OK | 1 |
| stochastic-p4-d0.2@6080 | `ga+gawa` |  | 2 |
| stochastic-p4-d0.2@8192 | `gagawa` | OK | 1 |
| stochastic-p4-d0.2@16384 | `gagawa` | OK | 1 |
| unigram-ablation@6080 | `gagawa` | OK | 1 |

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

## `dalan`  (suffixation, tier B_moderate_silver)

**silver gold:** `dal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dalan` |  | 1 |
| plain@8192 | `dalan` |  | 1 |
| plain@16384 | `dalan` |  | 1 |
| morphbpe@6080 | `dalan` |  | 1 |
| morphbpe@8192 | `dalan` |  | 1 |
| morphbpe@16384 | `dalan` |  | 1 |
| penalty-1@6080 | `dalan` |  | 1 |
| penalty-1@8192 | `dalan` |  | 1 |
| penalty-1@16384 | `dalan` |  | 1 |
| penalty-2@6080 | `dalan` |  | 1 |
| penalty-2@8192 | `dalan` |  | 1 |
| penalty-2@16384 | `dalan` |  | 1 |
| penalty-4@6080 | `dalan` |  | 1 |
| penalty-4@8192 | `dalan` |  | 1 |
| penalty-4@16384 | `dalan` |  | 1 |
| penalty-8@6080 | `dalan` |  | 1 |
| penalty-8@8192 | `dalan` |  | 1 |
| penalty-8@16384 | `dalan` |  | 1 |
| stochastic-p4-d0.1@6080 | `dalan` |  | 1 |
| stochastic-p4-d0.1@8192 | `dalan` |  | 1 |
| stochastic-p4-d0.1@16384 | `dalan` |  | 1 |
| stochastic-p4-d0.2@6080 | `dalan` |  | 1 |
| stochastic-p4-d0.2@8192 | `dalan` |  | 1 |
| stochastic-p4-d0.2@16384 | `dalan` |  | 1 |
| unigram-ablation@6080 | `dalan` |  | 1 |

## `arapan`  (suffixation, tier A_strong_silver)

**silver gold:** `arap+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `arapan` |  | 1 |
| plain@8192 | `arapan` |  | 1 |
| plain@16384 | `arapan` |  | 1 |
| morphbpe@6080 | `arap+an` | OK | 2 |
| morphbpe@8192 | `arap+an` | OK | 2 |
| morphbpe@16384 | `arap+an` | OK | 2 |
| penalty-1@6080 | `arap+an` | OK | 2 |
| penalty-1@8192 | `arap+an` | OK | 2 |
| penalty-1@16384 | `arap+an` | OK | 2 |
| penalty-2@6080 | `arap+an` | OK | 2 |
| penalty-2@8192 | `arap+an` | OK | 2 |
| penalty-2@16384 | `arap+an` | OK | 2 |
| penalty-4@6080 | `arap+an` | OK | 2 |
| penalty-4@8192 | `arap+an` | OK | 2 |
| penalty-4@16384 | `arap+an` | OK | 2 |
| penalty-8@6080 | `arap+an` | OK | 2 |
| penalty-8@8192 | `arap+an` | OK | 2 |
| penalty-8@16384 | `arap+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `arap+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `arap+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `arap+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `arap+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `arap+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `arap+an` | OK | 2 |
| unigram-ablation@6080 | `arapan` |  | 1 |

## `sabian`  (suffixation, tier A_strong_silver)

**silver gold:** `sabi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sabian` |  | 1 |
| plain@8192 | `sabian` |  | 1 |
| plain@16384 | `sabian` |  | 1 |
| morphbpe@6080 | `sabian` |  | 1 |
| morphbpe@8192 | `sabian` |  | 1 |
| morphbpe@16384 | `sabian` |  | 1 |
| penalty-1@6080 | `sabian` |  | 1 |
| penalty-1@8192 | `sabian` |  | 1 |
| penalty-1@16384 | `sabian` |  | 1 |
| penalty-2@6080 | `sabian` |  | 1 |
| penalty-2@8192 | `sabian` |  | 1 |
| penalty-2@16384 | `sabian` |  | 1 |
| penalty-4@6080 | `sabian` |  | 1 |
| penalty-4@8192 | `sabian` |  | 1 |
| penalty-4@16384 | `sabian` |  | 1 |
| penalty-8@6080 | `sabian` |  | 1 |
| penalty-8@8192 | `sabian` |  | 1 |
| penalty-8@16384 | `sabian` |  | 1 |
| stochastic-p4-d0.1@6080 | `sabian` |  | 1 |
| stochastic-p4-d0.1@8192 | `sabian` |  | 1 |
| stochastic-p4-d0.1@16384 | `sabian` |  | 1 |
| stochastic-p4-d0.2@6080 | `sabian` |  | 1 |
| stochastic-p4-d0.2@8192 | `sabian` |  | 1 |
| stochastic-p4-d0.2@16384 | `sabian` |  | 1 |
| unigram-ablation@6080 | `sabian` |  | 1 |

## `dewakan`  (suffixation, tier B_moderate_silver)

**silver gold:** `dewak+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dewakan` |  | 1 |
| plain@8192 | `dewakan` |  | 1 |
| plain@16384 | `dewakan` |  | 1 |
| morphbpe@6080 | `dewakan` |  | 1 |
| morphbpe@8192 | `dewakan` |  | 1 |
| morphbpe@16384 | `dewakan` |  | 1 |
| penalty-1@6080 | `dewakan` |  | 1 |
| penalty-1@8192 | `dewakan` |  | 1 |
| penalty-1@16384 | `dewakan` |  | 1 |
| penalty-2@6080 | `dewakan` |  | 1 |
| penalty-2@8192 | `dewakan` |  | 1 |
| penalty-2@16384 | `dewakan` |  | 1 |
| penalty-4@6080 | `dewakan` |  | 1 |
| penalty-4@8192 | `dewakan` |  | 1 |
| penalty-4@16384 | `dewakan` |  | 1 |
| penalty-8@6080 | `dewakan` |  | 1 |
| penalty-8@8192 | `dewakan` |  | 1 |
| penalty-8@16384 | `dewakan` |  | 1 |
| stochastic-p4-d0.1@6080 | `dewakan` |  | 1 |
| stochastic-p4-d0.1@8192 | `dewakan` |  | 1 |
| stochastic-p4-d0.1@16384 | `dewakan` |  | 1 |
| stochastic-p4-d0.2@6080 | `dewakan` |  | 1 |
| stochastic-p4-d0.2@8192 | `dewakan` |  | 1 |
| stochastic-p4-d0.2@16384 | `dewakan` |  | 1 |
| unigram-ablation@6080 | `dewaka+n` |  | 2 |

## `depatan`  (suffixation, tier B_moderate_silver)

**silver gold:** `depat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `depatan` |  | 1 |
| plain@8192 | `depatan` |  | 1 |
| plain@16384 | `depatan` |  | 1 |
| morphbpe@6080 | `depatan` |  | 1 |
| morphbpe@8192 | `depatan` |  | 1 |
| morphbpe@16384 | `depatan` |  | 1 |
| penalty-1@6080 | `depatan` |  | 1 |
| penalty-1@8192 | `depatan` |  | 1 |
| penalty-1@16384 | `depatan` |  | 1 |
| penalty-2@6080 | `depatan` |  | 1 |
| penalty-2@8192 | `depatan` |  | 1 |
| penalty-2@16384 | `depatan` |  | 1 |
| penalty-4@6080 | `depatan` |  | 1 |
| penalty-4@8192 | `depatan` |  | 1 |
| penalty-4@16384 | `depatan` |  | 1 |
| penalty-8@6080 | `depatan` |  | 1 |
| penalty-8@8192 | `depatan` |  | 1 |
| penalty-8@16384 | `depatan` |  | 1 |
| stochastic-p4-d0.1@6080 | `depatan` |  | 1 |
| stochastic-p4-d0.1@8192 | `depatan` |  | 1 |
| stochastic-p4-d0.1@16384 | `depatan` |  | 1 |
| stochastic-p4-d0.2@6080 | `depatan` |  | 1 |
| stochastic-p4-d0.2@8192 | `depatan` |  | 1 |
| stochastic-p4-d0.2@16384 | `depatan` |  | 1 |
| unigram-ablation@6080 | `depat+an` | OK | 2 |

## `daptan`  (suffixation, tier B_moderate_silver)

**silver gold:** `dapt+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `daptan` |  | 1 |
| plain@8192 | `daptan` |  | 1 |
| plain@16384 | `daptan` |  | 1 |
| morphbpe@6080 | `daptan` |  | 1 |
| morphbpe@8192 | `daptan` |  | 1 |
| morphbpe@16384 | `daptan` |  | 1 |
| penalty-1@6080 | `daptan` |  | 1 |
| penalty-1@8192 | `daptan` |  | 1 |
| penalty-1@16384 | `daptan` |  | 1 |
| penalty-2@6080 | `daptan` |  | 1 |
| penalty-2@8192 | `daptan` |  | 1 |
| penalty-2@16384 | `daptan` |  | 1 |
| penalty-4@6080 | `daptan` |  | 1 |
| penalty-4@8192 | `daptan` |  | 1 |
| penalty-4@16384 | `daptan` |  | 1 |
| penalty-8@6080 | `daptan` |  | 1 |
| penalty-8@8192 | `daptan` |  | 1 |
| penalty-8@16384 | `daptan` |  | 1 |
| stochastic-p4-d0.1@6080 | `daptan` |  | 1 |
| stochastic-p4-d0.1@8192 | `daptan` |  | 1 |
| stochastic-p4-d0.1@16384 | `daptan` |  | 1 |
| stochastic-p4-d0.2@6080 | `daptan` |  | 1 |
| stochastic-p4-d0.2@8192 | `daptan` |  | 1 |
| stochastic-p4-d0.2@16384 | `daptan` |  | 1 |
| unigram-ablation@6080 | `daptan` |  | 1 |

## `purian`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `puri+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `p+urian` |  | 2 |
| plain@8192 | `purian` |  | 1 |
| plain@16384 | `purian` |  | 1 |
| morphbpe@6080 | `p+urian` |  | 2 |
| morphbpe@8192 | `purian` |  | 1 |
| morphbpe@16384 | `purian` |  | 1 |
| penalty-1@6080 | `p+urian` |  | 2 |
| penalty-1@8192 | `purian` |  | 1 |
| penalty-1@16384 | `purian` |  | 1 |
| penalty-2@6080 | `purian` |  | 1 |
| penalty-2@8192 | `purian` |  | 1 |
| penalty-2@16384 | `purian` |  | 1 |
| penalty-4@6080 | `purian` |  | 1 |
| penalty-4@8192 | `purian` |  | 1 |
| penalty-4@16384 | `purian` |  | 1 |
| penalty-8@6080 | `purian` |  | 1 |
| penalty-8@8192 | `purian` |  | 1 |
| penalty-8@16384 | `purian` |  | 1 |
| stochastic-p4-d0.1@6080 | `purian` |  | 1 |
| stochastic-p4-d0.1@8192 | `purian` |  | 1 |
| stochastic-p4-d0.1@16384 | `purian` |  | 1 |
| stochastic-p4-d0.2@6080 | `purian` |  | 1 |
| stochastic-p4-d0.2@8192 | `purian` |  | 1 |
| stochastic-p4-d0.2@16384 | `purian` |  | 1 |
| unigram-ablation@6080 | `puri+an` | OK | 2 |

## `laman`  (suffixation, tier B_moderate_silver)

**silver gold:** `lam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `laman` |  | 1 |
| plain@8192 | `laman` |  | 1 |
| plain@16384 | `laman` |  | 1 |
| morphbpe@6080 | `laman` |  | 1 |
| morphbpe@8192 | `laman` |  | 1 |
| morphbpe@16384 | `laman` |  | 1 |
| penalty-1@6080 | `laman` |  | 1 |
| penalty-1@8192 | `laman` |  | 1 |
| penalty-1@16384 | `laman` |  | 1 |
| penalty-2@6080 | `laman` |  | 1 |
| penalty-2@8192 | `laman` |  | 1 |
| penalty-2@16384 | `laman` |  | 1 |
| penalty-4@6080 | `laman` |  | 1 |
| penalty-4@8192 | `laman` |  | 1 |
| penalty-4@16384 | `laman` |  | 1 |
| penalty-8@6080 | `laman` |  | 1 |
| penalty-8@8192 | `laman` |  | 1 |
| penalty-8@16384 | `laman` |  | 1 |
| stochastic-p4-d0.1@6080 | `laman` |  | 1 |
| stochastic-p4-d0.1@8192 | `laman` |  | 1 |
| stochastic-p4-d0.1@16384 | `laman` |  | 1 |
| stochastic-p4-d0.2@6080 | `laman` |  | 1 |
| stochastic-p4-d0.2@8192 | `laman` |  | 1 |
| stochastic-p4-d0.2@16384 | `laman` |  | 1 |
| unigram-ablation@6080 | `laman` |  | 1 |

## `sikanan`  (suffixation, tier A_strong_silver)

**silver gold:** `sikan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sikanan` |  | 1 |
| plain@8192 | `sikanan` |  | 1 |
| plain@16384 | `sikanan` |  | 1 |
| morphbpe@6080 | `sikan+an` | OK | 2 |
| morphbpe@8192 | `sikan+an` | OK | 2 |
| morphbpe@16384 | `sikan+an` | OK | 2 |
| penalty-1@6080 | `sikan+an` | OK | 2 |
| penalty-1@8192 | `sikan+an` | OK | 2 |
| penalty-1@16384 | `sikan+an` | OK | 2 |
| penalty-2@6080 | `sikan+an` | OK | 2 |
| penalty-2@8192 | `sikan+an` | OK | 2 |
| penalty-2@16384 | `sikan+an` | OK | 2 |
| penalty-4@6080 | `sikan+an` | OK | 2 |
| penalty-4@8192 | `sikan+an` | OK | 2 |
| penalty-4@16384 | `sikan+an` | OK | 2 |
| penalty-8@6080 | `sikan+an` | OK | 2 |
| penalty-8@8192 | `sikan+an` | OK | 2 |
| penalty-8@16384 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `sikan+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `sikan+an` | OK | 2 |
| unigram-ablation@6080 | `sikanan` |  | 1 |

## `laban`  (suffixation, tier B_moderate_silver)

**silver gold:** `lab+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `laban` |  | 1 |
| plain@8192 | `laban` |  | 1 |
| plain@16384 | `laban` |  | 1 |
| morphbpe@6080 | `laban` |  | 1 |
| morphbpe@8192 | `laban` |  | 1 |
| morphbpe@16384 | `laban` |  | 1 |
| penalty-1@6080 | `laban` |  | 1 |
| penalty-1@8192 | `laban` |  | 1 |
| penalty-1@16384 | `laban` |  | 1 |
| penalty-2@6080 | `laban` |  | 1 |
| penalty-2@8192 | `laban` |  | 1 |
| penalty-2@16384 | `laban` |  | 1 |
| penalty-4@6080 | `laban` |  | 1 |
| penalty-4@8192 | `laban` |  | 1 |
| penalty-4@16384 | `laban` |  | 1 |
| penalty-8@6080 | `laban` |  | 1 |
| penalty-8@8192 | `laban` |  | 1 |
| penalty-8@16384 | `laban` |  | 1 |
| stochastic-p4-d0.1@6080 | `laban` |  | 1 |
| stochastic-p4-d0.1@8192 | `laban` |  | 1 |
| stochastic-p4-d0.1@16384 | `laban` |  | 1 |
| stochastic-p4-d0.2@6080 | `laban` |  | 1 |
| stochastic-p4-d0.2@8192 | `laban` |  | 1 |
| stochastic-p4-d0.2@16384 | `laban` |  | 1 |
| unigram-ablation@6080 | `laban` |  | 1 |

## `tuntunan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tuntun+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+untunan` |  | 2 |
| plain@8192 | `tuntunan` |  | 1 |
| plain@16384 | `tuntunan` |  | 1 |
| morphbpe@6080 | `tuntunan` |  | 1 |
| morphbpe@8192 | `tuntunan` |  | 1 |
| morphbpe@16384 | `tuntunan` |  | 1 |
| penalty-1@6080 | `tuntunan` |  | 1 |
| penalty-1@8192 | `tuntunan` |  | 1 |
| penalty-1@16384 | `tuntunan` |  | 1 |
| penalty-2@6080 | `tuntunan` |  | 1 |
| penalty-2@8192 | `tuntunan` |  | 1 |
| penalty-2@16384 | `tuntunan` |  | 1 |
| penalty-4@6080 | `tuntunan` |  | 1 |
| penalty-4@8192 | `tuntunan` |  | 1 |
| penalty-4@16384 | `tuntunan` |  | 1 |
| penalty-8@6080 | `tuntunan` |  | 1 |
| penalty-8@8192 | `tuntunan` |  | 1 |
| penalty-8@16384 | `tuntunan` |  | 1 |
| stochastic-p4-d0.1@6080 | `tuntunan` |  | 1 |
| stochastic-p4-d0.1@8192 | `tuntunan` |  | 1 |
| stochastic-p4-d0.1@16384 | `tuntunan` |  | 1 |
| stochastic-p4-d0.2@6080 | `tuntunan` |  | 1 |
| stochastic-p4-d0.2@8192 | `tuntunan` |  | 1 |
| stochastic-p4-d0.2@16384 | `tuntunan` |  | 1 |
| unigram-ablation@6080 | `tuntun+an` | OK | 2 |

## `kawan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `kawan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kawan` | OK | 1 |
| plain@8192 | `kawan` | OK | 1 |
| plain@16384 | `kawan` | OK | 1 |
| morphbpe@6080 | `kawan` | OK | 1 |
| morphbpe@8192 | `kawan` | OK | 1 |
| morphbpe@16384 | `kawan` | OK | 1 |
| penalty-1@6080 | `kawan` | OK | 1 |
| penalty-1@8192 | `kawan` | OK | 1 |
| penalty-1@16384 | `kawan` | OK | 1 |
| penalty-2@6080 | `kawan` | OK | 1 |
| penalty-2@8192 | `kawan` | OK | 1 |
| penalty-2@16384 | `kawan` | OK | 1 |
| penalty-4@6080 | `kawan` | OK | 1 |
| penalty-4@8192 | `kawan` | OK | 1 |
| penalty-4@16384 | `kawan` | OK | 1 |
| penalty-8@6080 | `ka+wan` |  | 2 |
| penalty-8@8192 | `kawan` | OK | 1 |
| penalty-8@16384 | `kawan` | OK | 1 |
| stochastic-p4-d0.1@6080 | `ka+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `kawan` | OK | 1 |
| stochastic-p4-d0.1@16384 | `kawan` | OK | 1 |
| stochastic-p4-d0.2@6080 | `kawan` | OK | 1 |
| stochastic-p4-d0.2@8192 | `kawan` | OK | 1 |
| stochastic-p4-d0.2@16384 | `kawan` | OK | 1 |
| unigram-ablation@6080 | `ka+wan` |  | 2 |

## `bulan`  (suffixation, tier B_moderate_silver)

**silver gold:** `bul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bulan` |  | 1 |
| plain@8192 | `bulan` |  | 1 |
| plain@16384 | `bulan` |  | 1 |
| morphbpe@6080 | `bulan` |  | 1 |
| morphbpe@8192 | `bulan` |  | 1 |
| morphbpe@16384 | `bulan` |  | 1 |
| penalty-1@6080 | `bulan` |  | 1 |
| penalty-1@8192 | `bulan` |  | 1 |
| penalty-1@16384 | `bulan` |  | 1 |
| penalty-2@6080 | `bulan` |  | 1 |
| penalty-2@8192 | `bulan` |  | 1 |
| penalty-2@16384 | `bulan` |  | 1 |
| penalty-4@6080 | `bulan` |  | 1 |
| penalty-4@8192 | `bulan` |  | 1 |
| penalty-4@16384 | `bulan` |  | 1 |
| penalty-8@6080 | `bulan` |  | 1 |
| penalty-8@8192 | `bulan` |  | 1 |
| penalty-8@16384 | `bulan` |  | 1 |
| stochastic-p4-d0.1@6080 | `bulan` |  | 1 |
| stochastic-p4-d0.1@8192 | `bulan` |  | 1 |
| stochastic-p4-d0.1@16384 | `bulan` |  | 1 |
| stochastic-p4-d0.2@6080 | `bulan` |  | 1 |
| stochastic-p4-d0.2@8192 | `bulan` |  | 1 |
| stochastic-p4-d0.2@16384 | `bulan` |  | 1 |
| unigram-ablation@6080 | `bulan` |  | 1 |

## `misan`  (suffixation, tier A_strong_silver)

**silver gold:** `mis+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `misan` |  | 1 |
| plain@8192 | `misan` |  | 1 |
| plain@16384 | `misan` |  | 1 |
| morphbpe@6080 | `misan` |  | 1 |
| morphbpe@8192 | `misan` |  | 1 |
| morphbpe@16384 | `misan` |  | 1 |
| penalty-1@6080 | `misan` |  | 1 |
| penalty-1@8192 | `misan` |  | 1 |
| penalty-1@16384 | `misan` |  | 1 |
| penalty-2@6080 | `misan` |  | 1 |
| penalty-2@8192 | `misan` |  | 1 |
| penalty-2@16384 | `misan` |  | 1 |
| penalty-4@6080 | `misan` |  | 1 |
| penalty-4@8192 | `misan` |  | 1 |
| penalty-4@16384 | `misan` |  | 1 |
| penalty-8@6080 | `misan` |  | 1 |
| penalty-8@8192 | `misan` |  | 1 |
| penalty-8@16384 | `misan` |  | 1 |
| stochastic-p4-d0.1@6080 | `misan` |  | 1 |
| stochastic-p4-d0.1@8192 | `misan` |  | 1 |
| stochastic-p4-d0.1@16384 | `misan` |  | 1 |
| stochastic-p4-d0.2@6080 | `misan` |  | 1 |
| stochastic-p4-d0.2@8192 | `misan` |  | 1 |
| stochastic-p4-d0.2@16384 | `misan` |  | 1 |
| unigram-ablation@6080 | `misan` |  | 1 |

## `wanan`  (suffixation, tier B_moderate_silver)

**silver gold:** `wan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `wanan` |  | 1 |
| plain@8192 | `wanan` |  | 1 |
| plain@16384 | `wanan` |  | 1 |
| morphbpe@6080 | `wanan` |  | 1 |
| morphbpe@8192 | `wanan` |  | 1 |
| morphbpe@16384 | `wanan` |  | 1 |
| penalty-1@6080 | `wanan` |  | 1 |
| penalty-1@8192 | `wanan` |  | 1 |
| penalty-1@16384 | `wanan` |  | 1 |
| penalty-2@6080 | `wanan` |  | 1 |
| penalty-2@8192 | `wanan` |  | 1 |
| penalty-2@16384 | `wanan` |  | 1 |
| penalty-4@6080 | `wanan` |  | 1 |
| penalty-4@8192 | `wanan` |  | 1 |
| penalty-4@16384 | `wanan` |  | 1 |
| penalty-8@6080 | `wanan` |  | 1 |
| penalty-8@8192 | `wanan` |  | 1 |
| penalty-8@16384 | `wanan` |  | 1 |
| stochastic-p4-d0.1@6080 | `wanan` |  | 1 |
| stochastic-p4-d0.1@8192 | `wanan` |  | 1 |
| stochastic-p4-d0.1@16384 | `wanan` |  | 1 |
| stochastic-p4-d0.2@6080 | `wanan` |  | 1 |
| stochastic-p4-d0.2@8192 | `wanan` |  | 1 |
| stochastic-p4-d0.2@16384 | `wanan` |  | 1 |
| unigram-ablation@6080 | `wanan` |  | 1 |

## `sisuan`  (suffixation, tier B_moderate_silver)

**silver gold:** `sisu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sis+uan` |  | 2 |
| plain@8192 | `sisuan` |  | 1 |
| plain@16384 | `sisuan` |  | 1 |
| morphbpe@6080 | `sisuan` |  | 1 |
| morphbpe@8192 | `sisuan` |  | 1 |
| morphbpe@16384 | `sisuan` |  | 1 |
| penalty-1@6080 | `sisuan` |  | 1 |
| penalty-1@8192 | `sisuan` |  | 1 |
| penalty-1@16384 | `sisuan` |  | 1 |
| penalty-2@6080 | `sisuan` |  | 1 |
| penalty-2@8192 | `sisuan` |  | 1 |
| penalty-2@16384 | `sisuan` |  | 1 |
| penalty-4@6080 | `sisuan` |  | 1 |
| penalty-4@8192 | `sisuan` |  | 1 |
| penalty-4@16384 | `sisuan` |  | 1 |
| penalty-8@6080 | `sisuan` |  | 1 |
| penalty-8@8192 | `sisuan` |  | 1 |
| penalty-8@16384 | `sisuan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sisuan` |  | 1 |
| stochastic-p4-d0.1@8192 | `sisuan` |  | 1 |
| stochastic-p4-d0.1@16384 | `sisuan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sisuan` |  | 1 |
| stochastic-p4-d0.2@8192 | `sisuan` |  | 1 |
| stochastic-p4-d0.2@16384 | `sisuan` |  | 1 |
| unigram-ablation@6080 | `s+isuan` |  | 2 |

## `tipan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `tipan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+ipan` |  | 2 |
| plain@8192 | `t+ipan` |  | 2 |
| plain@16384 | `tipan` | OK | 1 |
| morphbpe@6080 | `t+ipan` |  | 2 |
| morphbpe@8192 | `t+ipan` |  | 2 |
| morphbpe@16384 | `t+ipan` |  | 2 |
| penalty-1@6080 | `t+ipan` |  | 2 |
| penalty-1@8192 | `t+ipan` |  | 2 |
| penalty-1@16384 | `t+ipan` |  | 2 |
| penalty-2@6080 | `ti+pan` |  | 2 |
| penalty-2@8192 | `ti+pan` |  | 2 |
| penalty-2@16384 | `ti+pan` |  | 2 |
| penalty-4@6080 | `ti+pan` |  | 2 |
| penalty-4@8192 | `ti+pan` |  | 2 |
| penalty-4@16384 | `ti+pan` |  | 2 |
| penalty-8@6080 | `ti+pan` |  | 2 |
| penalty-8@8192 | `ti+pan` |  | 2 |
| penalty-8@16384 | `ti+pan` |  | 2 |
| stochastic-p4-d0.1@6080 | `ti+pan` |  | 2 |
| stochastic-p4-d0.1@8192 | `ti+pan` |  | 2 |
| stochastic-p4-d0.1@16384 | `ti+pan` |  | 2 |
| stochastic-p4-d0.2@6080 | `ti+p+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `ti+p+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `ti+p+an` |  | 3 |
| unigram-ablation@6080 | `ti+pan` |  | 2 |

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

## `nangan`  (suffixation, tier A_strong_silver)

**silver gold:** `nang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `nangan` |  | 1 |
| plain@8192 | `nangan` |  | 1 |
| plain@16384 | `nangan` |  | 1 |
| morphbpe@6080 | `nangan` |  | 1 |
| morphbpe@8192 | `nangan` |  | 1 |
| morphbpe@16384 | `nangan` |  | 1 |
| penalty-1@6080 | `nang+an` | OK | 2 |
| penalty-1@8192 | `nang+an` | OK | 2 |
| penalty-1@16384 | `nang+an` | OK | 2 |
| penalty-2@6080 | `nang+an` | OK | 2 |
| penalty-2@8192 | `nang+an` | OK | 2 |
| penalty-2@16384 | `nang+an` | OK | 2 |
| penalty-4@6080 | `nang+an` | OK | 2 |
| penalty-4@8192 | `nang+an` | OK | 2 |
| penalty-4@16384 | `nang+an` | OK | 2 |
| penalty-8@6080 | `nang+an` | OK | 2 |
| penalty-8@8192 | `nang+an` | OK | 2 |
| penalty-8@16384 | `nang+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `nangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `nangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `nangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `nangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `nangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `nangan` |  | 1 |
| unigram-ablation@6080 | `nang+an` | OK | 2 |

## `canaan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `canaan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `c+ana+an` |  | 3 |
| plain@8192 | `c+ana+an` |  | 3 |
| plain@16384 | `c+ana+an` |  | 3 |
| morphbpe@6080 | `c+ana+an` |  | 3 |
| morphbpe@8192 | `c+ana+an` |  | 3 |
| morphbpe@16384 | `c+ana+an` |  | 3 |
| penalty-1@6080 | `c+ana+an` |  | 3 |
| penalty-1@8192 | `c+ana+an` |  | 3 |
| penalty-1@16384 | `c+ana+an` |  | 3 |
| penalty-2@6080 | `c+ana+an` |  | 3 |
| penalty-2@8192 | `c+ana+an` |  | 3 |
| penalty-2@16384 | `c+ana+an` |  | 3 |
| penalty-4@6080 | `c+ana+an` |  | 3 |
| penalty-4@8192 | `c+ana+an` |  | 3 |
| penalty-4@16384 | `c+ana+an` |  | 3 |
| penalty-8@6080 | `cana+an` |  | 2 |
| penalty-8@8192 | `cana+an` |  | 2 |
| penalty-8@16384 | `cana+an` |  | 2 |
| stochastic-p4-d0.1@6080 | `cana+an` |  | 2 |
| stochastic-p4-d0.1@8192 | `cana+an` |  | 2 |
| stochastic-p4-d0.1@16384 | `cana+an` |  | 2 |
| stochastic-p4-d0.2@6080 | `cana+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `cana+an` |  | 2 |
| stochastic-p4-d0.2@16384 | `cana+an` |  | 2 |
| unigram-ablation@6080 | `ca+na+an` |  | 3 |

## `larawan`  (suffixation, tier B_moderate_silver)

**silver gold:** `laraw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `larawan` |  | 1 |
| plain@8192 | `larawan` |  | 1 |
| plain@16384 | `larawan` |  | 1 |
| morphbpe@6080 | `larawan` |  | 1 |
| morphbpe@8192 | `larawan` |  | 1 |
| morphbpe@16384 | `larawan` |  | 1 |
| penalty-1@6080 | `larawan` |  | 1 |
| penalty-1@8192 | `larawan` |  | 1 |
| penalty-1@16384 | `larawan` |  | 1 |
| penalty-2@6080 | `larawan` |  | 1 |
| penalty-2@8192 | `larawan` |  | 1 |
| penalty-2@16384 | `larawan` |  | 1 |
| penalty-4@6080 | `larawan` |  | 1 |
| penalty-4@8192 | `larawan` |  | 1 |
| penalty-4@16384 | `larawan` |  | 1 |
| penalty-8@6080 | `larawan` |  | 1 |
| penalty-8@8192 | `larawan` |  | 1 |
| penalty-8@16384 | `larawan` |  | 1 |
| stochastic-p4-d0.1@6080 | `larawan` |  | 1 |
| stochastic-p4-d0.1@8192 | `larawan` |  | 1 |
| stochastic-p4-d0.1@16384 | `larawan` |  | 1 |
| stochastic-p4-d0.2@6080 | `larawan` |  | 1 |
| stochastic-p4-d0.2@8192 | `larawan` |  | 1 |
| stochastic-p4-d0.2@16384 | `larawan` |  | 1 |
| unigram-ablation@6080 | `larawan` |  | 1 |

## `bandian`  (suffixation, tier A_strong_silver)

**silver gold:** `bandi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `band+ian` |  | 2 |
| plain@8192 | `band+ian` |  | 2 |
| plain@16384 | `band+ian` |  | 2 |
| morphbpe@6080 | `band+ian` |  | 2 |
| morphbpe@8192 | `band+ian` |  | 2 |
| morphbpe@16384 | `band+ian` |  | 2 |
| penalty-1@6080 | `band+ian` |  | 2 |
| penalty-1@8192 | `band+ian` |  | 2 |
| penalty-1@16384 | `band+ian` |  | 2 |
| penalty-2@6080 | `band+ian` |  | 2 |
| penalty-2@8192 | `band+ian` |  | 2 |
| penalty-2@16384 | `band+ian` |  | 2 |
| penalty-4@6080 | `bandi+an` | OK | 2 |
| penalty-4@8192 | `bandi+an` | OK | 2 |
| penalty-4@16384 | `bandi+an` | OK | 2 |
| penalty-8@6080 | `bandi+an` | OK | 2 |
| penalty-8@8192 | `bandi+an` | OK | 2 |
| penalty-8@16384 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `bandi+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `bandi+an` | OK | 2 |
| unigram-ablation@6080 | `bandi+an` | OK | 2 |

## `tuparan`  (suffixation, tier B_moderate_silver)

**silver gold:** `tupar+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tu+paran` |  | 2 |
| plain@8192 | `tu+paran` |  | 2 |
| plain@16384 | `tuparan` |  | 1 |
| morphbpe@6080 | `t+uparan` |  | 2 |
| morphbpe@8192 | `t+uparan` |  | 2 |
| morphbpe@16384 | `tuparan` |  | 1 |
| penalty-1@6080 | `t+uparan` |  | 2 |
| penalty-1@8192 | `t+uparan` |  | 2 |
| penalty-1@16384 | `tuparan` |  | 1 |
| penalty-2@6080 | `tu+paran` |  | 2 |
| penalty-2@8192 | `tu+paran` |  | 2 |
| penalty-2@16384 | `tuparan` |  | 1 |
| penalty-4@6080 | `tu+paran` |  | 2 |
| penalty-4@8192 | `tu+paran` |  | 2 |
| penalty-4@16384 | `tuparan` |  | 1 |
| penalty-8@6080 | `tu+paran` |  | 2 |
| penalty-8@8192 | `tu+paran` |  | 2 |
| penalty-8@16384 | `tuparan` |  | 1 |
| stochastic-p4-d0.1@6080 | `tu+paran` |  | 2 |
| stochastic-p4-d0.1@8192 | `tu+paran` |  | 2 |
| stochastic-p4-d0.1@16384 | `tuparan` |  | 1 |
| stochastic-p4-d0.2@6080 | `tu+paran` |  | 2 |
| stochastic-p4-d0.2@8192 | `tuparan` |  | 1 |
| stochastic-p4-d0.2@16384 | `tuparan` |  | 1 |
| unigram-ablation@6080 | `tu+paran` |  | 2 |

## `angganan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `anggan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `angganan` |  | 1 |
| plain@8192 | `angganan` |  | 1 |
| plain@16384 | `angganan` |  | 1 |
| morphbpe@6080 | `angg+anan` |  | 2 |
| morphbpe@8192 | `angg+anan` |  | 2 |
| morphbpe@16384 | `angg+anan` |  | 2 |
| penalty-1@6080 | `angg+anan` |  | 2 |
| penalty-1@8192 | `angg+anan` |  | 2 |
| penalty-1@16384 | `angg+anan` |  | 2 |
| penalty-2@6080 | `angg+anan` |  | 2 |
| penalty-2@8192 | `angg+anan` |  | 2 |
| penalty-2@16384 | `angg+anan` |  | 2 |
| penalty-4@6080 | `ang+gan+an` |  | 3 |
| penalty-4@8192 | `ang+gan+an` |  | 3 |
| penalty-4@16384 | `ang+ganan` |  | 2 |
| penalty-8@6080 | `ang+gan+an` |  | 3 |
| penalty-8@8192 | `ang+gan+an` |  | 3 |
| penalty-8@16384 | `ang+ganan` |  | 2 |
| stochastic-p4-d0.1@6080 | `ang+gan+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `ang+ganan` |  | 2 |
| stochastic-p4-d0.1@16384 | `ang+ganan` |  | 2 |
| stochastic-p4-d0.2@6080 | `ang+g+anan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ang+g+anan` |  | 3 |
| stochastic-p4-d0.2@16384 | `ang+ganan` |  | 2 |
| unigram-ablation@6080 | `angganan` |  | 1 |

## `jordan`  (suffixation, tier B_moderate_silver)

**silver gold:** `jord+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `jor+dan` |  | 2 |
| plain@8192 | `jor+dan` |  | 2 |
| plain@16384 | `jor+dan` |  | 2 |
| morphbpe@6080 | `jor+dan` |  | 2 |
| morphbpe@8192 | `jor+dan` |  | 2 |
| morphbpe@16384 | `jor+dan` |  | 2 |
| penalty-1@6080 | `jor+dan` |  | 2 |
| penalty-1@8192 | `jor+dan` |  | 2 |
| penalty-1@16384 | `jor+dan` |  | 2 |
| penalty-2@6080 | `jor+dan` |  | 2 |
| penalty-2@8192 | `jor+dan` |  | 2 |
| penalty-2@16384 | `jor+dan` |  | 2 |
| penalty-4@6080 | `jor+dan` |  | 2 |
| penalty-4@8192 | `jor+dan` |  | 2 |
| penalty-4@16384 | `jor+dan` |  | 2 |
| penalty-8@6080 | `jor+dan` |  | 2 |
| penalty-8@8192 | `jor+dan` |  | 2 |
| penalty-8@16384 | `jor+dan` |  | 2 |
| stochastic-p4-d0.1@6080 | `jor+dan` |  | 2 |
| stochastic-p4-d0.1@8192 | `jor+dan` |  | 2 |
| stochastic-p4-d0.1@16384 | `jor+dan` |  | 2 |
| stochastic-p4-d0.2@6080 | `j+ord+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `j+ord+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `j+ord+an` |  | 3 |
| unigram-ablation@6080 | `jo+r+d+an` |  | 4 |

## `tanaman`  (suffixation, tier A_strong_silver)

**silver gold:** `tanam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tanaman` |  | 1 |
| plain@8192 | `tanaman` |  | 1 |
| plain@16384 | `tanaman` |  | 1 |
| morphbpe@6080 | `tanaman` |  | 1 |
| morphbpe@8192 | `tanaman` |  | 1 |
| morphbpe@16384 | `tanaman` |  | 1 |
| penalty-1@6080 | `tanaman` |  | 1 |
| penalty-1@8192 | `tanaman` |  | 1 |
| penalty-1@16384 | `tanaman` |  | 1 |
| penalty-2@6080 | `tanaman` |  | 1 |
| penalty-2@8192 | `tanaman` |  | 1 |
| penalty-2@16384 | `tanaman` |  | 1 |
| penalty-4@6080 | `tanaman` |  | 1 |
| penalty-4@8192 | `tanaman` |  | 1 |
| penalty-4@16384 | `tanaman` |  | 1 |
| penalty-8@6080 | `tanaman` |  | 1 |
| penalty-8@8192 | `tanaman` |  | 1 |
| penalty-8@16384 | `tanaman` |  | 1 |
| stochastic-p4-d0.1@6080 | `tanaman` |  | 1 |
| stochastic-p4-d0.1@8192 | `tanaman` |  | 1 |
| stochastic-p4-d0.1@16384 | `tanaman` |  | 1 |
| stochastic-p4-d0.2@6080 | `tanaman` |  | 1 |
| stochastic-p4-d0.2@8192 | `tanaman` |  | 1 |
| stochastic-p4-d0.2@16384 | `tanaman` |  | 1 |
| unigram-ablation@6080 | `tanaman` |  | 1 |

## `bunduk-bundukan`  (suffixation, tier B_moderate_silver)

**silver gold:** `bunduk-bunduk+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bunduk+-+bunduk+an` |  | 4 |
| plain@8192 | `bunduk+-+bunduk+an` |  | 4 |
| plain@16384 | `bunduk-bundukan` |  | 1 |
| morphbpe@6080 | `bunduk+-+bunduk+an` |  | 4 |
| morphbpe@8192 | `bunduk+-+bunduk+an` |  | 4 |
| morphbpe@16384 | `bunduk-bundukan` |  | 1 |
| penalty-1@6080 | `bunduk+-+bunduk+an` |  | 4 |
| penalty-1@8192 | `bunduk+-+bunduk+an` |  | 4 |
| penalty-1@16384 | `bunduk-bundukan` |  | 1 |
| penalty-2@6080 | `bunduk+-+bunduk+an` |  | 4 |
| penalty-2@8192 | `bunduk+-+bunduk+an` |  | 4 |
| penalty-2@16384 | `bunduk-bundukan` |  | 1 |
| penalty-4@6080 | `bunduk+-+bun+du+kan` |  | 5 |
| penalty-4@8192 | `bunduk+-+bundu+kan` |  | 4 |
| penalty-4@16384 | `bunduk-bundukan` |  | 1 |
| penalty-8@6080 | `bunduk+-+bun+du+kan` |  | 5 |
| penalty-8@8192 | `bunduk+-+bundu+kan` |  | 4 |
| penalty-8@16384 | `bunduk-bundukan` |  | 1 |
| stochastic-p4-d0.1@6080 | `bunduk+-+bundu+kan` |  | 4 |
| stochastic-p4-d0.1@8192 | `bunduk+-+bundu+kan` |  | 4 |
| stochastic-p4-d0.1@16384 | `bunduk-bundukan` |  | 1 |
| stochastic-p4-d0.2@6080 | `bun+duk+-+bun+du+kan` |  | 6 |
| stochastic-p4-d0.2@8192 | `bun+duk+-+bundu+kan` |  | 5 |
| stochastic-p4-d0.2@16384 | `bunduk-bundukan` |  | 1 |
| unigram-ablation@6080 | `bunduk+-+bunduk+an` |  | 4 |

## `damdaman`  (suffixation, tier A_strong_silver)

**silver gold:** `damdam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `damdaman` |  | 1 |
| plain@8192 | `damdaman` |  | 1 |
| plain@16384 | `damdaman` |  | 1 |
| morphbpe@6080 | `dam+daman` |  | 2 |
| morphbpe@8192 | `dam+daman` |  | 2 |
| morphbpe@16384 | `dam+daman` |  | 2 |
| penalty-1@6080 | `dam+d+aman` |  | 3 |
| penalty-1@8192 | `dam+d+aman` |  | 3 |
| penalty-1@16384 | `dam+d+aman` |  | 3 |
| penalty-2@6080 | `dam+daman` |  | 2 |
| penalty-2@8192 | `dam+daman` |  | 2 |
| penalty-2@16384 | `dam+daman` |  | 2 |
| penalty-4@6080 | `damdam+an` | OK | 2 |
| penalty-4@8192 | `damdam+an` | OK | 2 |
| penalty-4@16384 | `damdam+an` | OK | 2 |
| penalty-8@6080 | `damdam+an` | OK | 2 |
| penalty-8@8192 | `damdam+an` | OK | 2 |
| penalty-8@16384 | `damdam+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `dam+daman` |  | 2 |
| stochastic-p4-d0.1@8192 | `dam+daman` |  | 2 |
| stochastic-p4-d0.1@16384 | `dam+daman` |  | 2 |
| stochastic-p4-d0.2@6080 | `damdam+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `damdam+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `damdam+an` | OK | 2 |
| unigram-ablation@6080 | `damdam+an` | OK | 2 |

## `lawan`  (suffixation, tier B_moderate_silver)

**silver gold:** `law+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lawan` |  | 1 |
| plain@8192 | `lawan` |  | 1 |
| plain@16384 | `lawan` |  | 1 |
| morphbpe@6080 | `la+wan` |  | 2 |
| morphbpe@8192 | `la+wan` |  | 2 |
| morphbpe@16384 | `lawan` |  | 1 |
| penalty-1@6080 | `la+wan` |  | 2 |
| penalty-1@8192 | `la+wan` |  | 2 |
| penalty-1@16384 | `la+wan` |  | 2 |
| penalty-2@6080 | `la+wan` |  | 2 |
| penalty-2@8192 | `la+wan` |  | 2 |
| penalty-2@16384 | `la+wan` |  | 2 |
| penalty-4@6080 | `la+wan` |  | 2 |
| penalty-4@8192 | `la+wan` |  | 2 |
| penalty-4@16384 | `la+wan` |  | 2 |
| penalty-8@6080 | `la+wan` |  | 2 |
| penalty-8@8192 | `la+wan` |  | 2 |
| penalty-8@16384 | `la+wan` |  | 2 |
| stochastic-p4-d0.1@6080 | `la+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `la+wan` |  | 2 |
| stochastic-p4-d0.1@16384 | `la+wan` |  | 2 |
| stochastic-p4-d0.2@6080 | `la+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `la+wan` |  | 2 |
| stochastic-p4-d0.2@16384 | `la+wan` |  | 2 |
| unigram-ablation@6080 | `lawan` |  | 1 |

## `ganakan`  (suffixation, tier B_moderate_silver)

**silver gold:** `ganak+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `gan+akan` |  | 2 |
| plain@8192 | `gan+akan` |  | 2 |
| plain@16384 | `ganakan` |  | 1 |
| morphbpe@6080 | `gan+akan` |  | 2 |
| morphbpe@8192 | `gan+akan` |  | 2 |
| morphbpe@16384 | `gan+akan` |  | 2 |
| penalty-1@6080 | `gan+akan` |  | 2 |
| penalty-1@8192 | `gan+akan` |  | 2 |
| penalty-1@16384 | `gan+akan` |  | 2 |
| penalty-2@6080 | `gan+akan` |  | 2 |
| penalty-2@8192 | `gan+akan` |  | 2 |
| penalty-2@16384 | `gan+akan` |  | 2 |
| penalty-4@6080 | `gan+akan` |  | 2 |
| penalty-4@8192 | `gan+akan` |  | 2 |
| penalty-4@16384 | `gan+akan` |  | 2 |
| penalty-8@6080 | `gan+akan` |  | 2 |
| penalty-8@8192 | `gan+akan` |  | 2 |
| penalty-8@16384 | `ganakan` |  | 1 |
| stochastic-p4-d0.1@6080 | `gan+akan` |  | 2 |
| stochastic-p4-d0.1@8192 | `gan+akan` |  | 2 |
| stochastic-p4-d0.1@16384 | `gan+akan` |  | 2 |
| stochastic-p4-d0.2@6080 | `gan+akan` |  | 2 |
| stochastic-p4-d0.2@8192 | `gan+akan` |  | 2 |
| stochastic-p4-d0.2@16384 | `gan+akan` |  | 2 |
| unigram-ablation@6080 | `ganakan` |  | 1 |

## `kuanan`  (suffixation, tier B_moderate_silver)

**silver gold:** `kuan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ku+anan` |  | 2 |
| plain@8192 | `kuanan` |  | 1 |
| plain@16384 | `kuanan` |  | 1 |
| morphbpe@6080 | `ku+anan` |  | 2 |
| morphbpe@8192 | `kuanan` |  | 1 |
| morphbpe@16384 | `kuanan` |  | 1 |
| penalty-1@6080 | `ku+anan` |  | 2 |
| penalty-1@8192 | `kuanan` |  | 1 |
| penalty-1@16384 | `kuanan` |  | 1 |
| penalty-2@6080 | `kuanan` |  | 1 |
| penalty-2@8192 | `kuanan` |  | 1 |
| penalty-2@16384 | `kuanan` |  | 1 |
| penalty-4@6080 | `ku+anan` |  | 2 |
| penalty-4@8192 | `ku+anan` |  | 2 |
| penalty-4@16384 | `kuanan` |  | 1 |
| penalty-8@6080 | `ku+anan` |  | 2 |
| penalty-8@8192 | `ku+anan` |  | 2 |
| penalty-8@16384 | `kuanan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ku+anan` |  | 2 |
| stochastic-p4-d0.1@8192 | `ku+anan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kuanan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ku+anan` |  | 2 |
| stochastic-p4-d0.2@8192 | `ku+anan` |  | 2 |
| stochastic-p4-d0.2@16384 | `kuanan` |  | 1 |
| unigram-ablation@6080 | `kuanan` |  | 1 |

## `leguan`  (suffixation, tier B_moderate_silver)

**silver gold:** `legu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `leg+uan` |  | 2 |
| plain@8192 | `leguan` |  | 1 |
| plain@16384 | `leguan` |  | 1 |
| morphbpe@6080 | `leg+uan` |  | 2 |
| morphbpe@8192 | `leguan` |  | 1 |
| morphbpe@16384 | `leguan` |  | 1 |
| penalty-1@6080 | `leg+uan` |  | 2 |
| penalty-1@8192 | `leguan` |  | 1 |
| penalty-1@16384 | `leguan` |  | 1 |
| penalty-2@6080 | `le+guan` |  | 2 |
| penalty-2@8192 | `leguan` |  | 1 |
| penalty-2@16384 | `leguan` |  | 1 |
| penalty-4@6080 | `leguan` |  | 1 |
| penalty-4@8192 | `leguan` |  | 1 |
| penalty-4@16384 | `leguan` |  | 1 |
| penalty-8@6080 | `leguan` |  | 1 |
| penalty-8@8192 | `leguan` |  | 1 |
| penalty-8@16384 | `leguan` |  | 1 |
| stochastic-p4-d0.1@6080 | `le+guan` |  | 2 |
| stochastic-p4-d0.1@8192 | `leguan` |  | 1 |
| stochastic-p4-d0.1@16384 | `leguan` |  | 1 |
| stochastic-p4-d0.2@6080 | `le+guan` |  | 2 |
| stochastic-p4-d0.2@8192 | `leguan` |  | 1 |
| stochastic-p4-d0.2@16384 | `leguan` |  | 1 |
| unigram-ablation@6080 | `legu+an` | OK | 2 |

## `daraptan`  (suffixation, tier B_moderate_silver)

**silver gold:** `darapt+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `daraptan` |  | 1 |
| plain@8192 | `daraptan` |  | 1 |
| plain@16384 | `daraptan` |  | 1 |
| morphbpe@6080 | `daraptan` |  | 1 |
| morphbpe@8192 | `daraptan` |  | 1 |
| morphbpe@16384 | `daraptan` |  | 1 |
| penalty-1@6080 | `daraptan` |  | 1 |
| penalty-1@8192 | `daraptan` |  | 1 |
| penalty-1@16384 | `daraptan` |  | 1 |
| penalty-2@6080 | `daraptan` |  | 1 |
| penalty-2@8192 | `daraptan` |  | 1 |
| penalty-2@16384 | `daraptan` |  | 1 |
| penalty-4@6080 | `daraptan` |  | 1 |
| penalty-4@8192 | `daraptan` |  | 1 |
| penalty-4@16384 | `daraptan` |  | 1 |
| penalty-8@6080 | `daraptan` |  | 1 |
| penalty-8@8192 | `daraptan` |  | 1 |
| penalty-8@16384 | `daraptan` |  | 1 |
| stochastic-p4-d0.1@6080 | `daraptan` |  | 1 |
| stochastic-p4-d0.1@8192 | `daraptan` |  | 1 |
| stochastic-p4-d0.1@16384 | `daraptan` |  | 1 |
| stochastic-p4-d0.2@6080 | `daraptan` |  | 1 |
| stochastic-p4-d0.2@8192 | `daraptan` |  | 1 |
| stochastic-p4-d0.2@16384 | `daraptan` |  | 1 |
| unigram-ablation@6080 | `daraptan` |  | 1 |

## `aslagan`  (suffixation, tier A_strong_silver)

**silver gold:** `aslag+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `aslagan` |  | 1 |
| plain@8192 | `aslagan` |  | 1 |
| plain@16384 | `aslagan` |  | 1 |
| morphbpe@6080 | `aslagan` |  | 1 |
| morphbpe@8192 | `aslagan` |  | 1 |
| morphbpe@16384 | `aslagan` |  | 1 |
| penalty-1@6080 | `aslagan` |  | 1 |
| penalty-1@8192 | `aslagan` |  | 1 |
| penalty-1@16384 | `aslagan` |  | 1 |
| penalty-2@6080 | `aslagan` |  | 1 |
| penalty-2@8192 | `aslagan` |  | 1 |
| penalty-2@16384 | `aslagan` |  | 1 |
| penalty-4@6080 | `aslagan` |  | 1 |
| penalty-4@8192 | `aslagan` |  | 1 |
| penalty-4@16384 | `aslagan` |  | 1 |
| penalty-8@6080 | `aslagan` |  | 1 |
| penalty-8@8192 | `aslagan` |  | 1 |
| penalty-8@16384 | `aslagan` |  | 1 |
| stochastic-p4-d0.1@6080 | `aslagan` |  | 1 |
| stochastic-p4-d0.1@8192 | `aslagan` |  | 1 |
| stochastic-p4-d0.1@16384 | `aslagan` |  | 1 |
| stochastic-p4-d0.2@6080 | `aslagan` |  | 1 |
| stochastic-p4-d0.2@8192 | `aslagan` |  | 1 |
| stochastic-p4-d0.2@16384 | `aslagan` |  | 1 |
| unigram-ablation@6080 | `aslagan` |  | 1 |

## `lelangan`  (suffixation, tier B_moderate_silver)

**silver gold:** `lelang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lelangan` |  | 1 |
| plain@8192 | `lelangan` |  | 1 |
| plain@16384 | `lelangan` |  | 1 |
| morphbpe@6080 | `lelangan` |  | 1 |
| morphbpe@8192 | `lelangan` |  | 1 |
| morphbpe@16384 | `lelangan` |  | 1 |
| penalty-1@6080 | `lelangan` |  | 1 |
| penalty-1@8192 | `lelangan` |  | 1 |
| penalty-1@16384 | `lelangan` |  | 1 |
| penalty-2@6080 | `lelangan` |  | 1 |
| penalty-2@8192 | `lelangan` |  | 1 |
| penalty-2@16384 | `lelangan` |  | 1 |
| penalty-4@6080 | `lelangan` |  | 1 |
| penalty-4@8192 | `lelangan` |  | 1 |
| penalty-4@16384 | `lelangan` |  | 1 |
| penalty-8@6080 | `lelangan` |  | 1 |
| penalty-8@8192 | `lelangan` |  | 1 |
| penalty-8@16384 | `lelangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `lelangan` |  | 1 |
| stochastic-p4-d0.1@8192 | `lelangan` |  | 1 |
| stochastic-p4-d0.1@16384 | `lelangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `lelangan` |  | 1 |
| stochastic-p4-d0.2@8192 | `lelangan` |  | 1 |
| stochastic-p4-d0.2@16384 | `lelangan` |  | 1 |
| unigram-ablation@6080 | `lelangan` |  | 1 |

## `sugatan`  (suffixation, tier A_strong_silver)

**silver gold:** `sugat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sug+atan` |  | 2 |
| plain@8192 | `sug+atan` |  | 2 |
| plain@16384 | `sugatan` |  | 1 |
| morphbpe@6080 | `sug+atan` |  | 2 |
| morphbpe@8192 | `sug+atan` |  | 2 |
| morphbpe@16384 | `sug+atan` |  | 2 |
| penalty-1@6080 | `sug+atan` |  | 2 |
| penalty-1@8192 | `sug+atan` |  | 2 |
| penalty-1@16384 | `sug+atan` |  | 2 |
| penalty-2@6080 | `sug+atan` |  | 2 |
| penalty-2@8192 | `sug+atan` |  | 2 |
| penalty-2@16384 | `sug+atan` |  | 2 |
| penalty-4@6080 | `sug+atan` |  | 2 |
| penalty-4@8192 | `sug+atan` |  | 2 |
| penalty-4@16384 | `sug+atan` |  | 2 |
| penalty-8@6080 | `sugat+an` | OK | 2 |
| penalty-8@8192 | `sugat+an` | OK | 2 |
| penalty-8@16384 | `sugat+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `sug+at+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `sug+at+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `sug+atan` |  | 2 |
| stochastic-p4-d0.2@6080 | `sugat+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `sugat+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `sugat+an` | OK | 2 |
| unigram-ablation@6080 | `sugat+an` | OK | 2 |

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

## `tuknangan`  (suffixation, tier A_strong_silver)

**silver gold:** `tuknang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tuknangan` |  | 1 |
| plain@8192 | `tuknangan` |  | 1 |
| plain@16384 | `tuknangan` |  | 1 |
| morphbpe@6080 | `tuknang+an` | OK | 2 |
| morphbpe@8192 | `tuknang+an` | OK | 2 |
| morphbpe@16384 | `tuknang+an` | OK | 2 |
| penalty-1@6080 | `tuknang+an` | OK | 2 |
| penalty-1@8192 | `tuknang+an` | OK | 2 |
| penalty-1@16384 | `tuknang+an` | OK | 2 |
| penalty-2@6080 | `tuknang+an` | OK | 2 |
| penalty-2@8192 | `tuknang+an` | OK | 2 |
| penalty-2@16384 | `tuknang+an` | OK | 2 |
| penalty-4@6080 | `tuknang+an` | OK | 2 |
| penalty-4@8192 | `tuknang+an` | OK | 2 |
| penalty-4@16384 | `tuknang+an` | OK | 2 |
| penalty-8@6080 | `tuknang+an` | OK | 2 |
| penalty-8@8192 | `tuknang+an` | OK | 2 |
| penalty-8@16384 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `tuknang+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `tuknang+an` | OK | 2 |
| unigram-ablation@6080 | `tuknangan` |  | 1 |

## `ausan`  (suffixation, tier A_strong_silver)

**silver gold:** `aus+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ausan` |  | 1 |
| plain@8192 | `ausan` |  | 1 |
| plain@16384 | `ausan` |  | 1 |
| morphbpe@6080 | `aus+an` | OK | 2 |
| morphbpe@8192 | `aus+an` | OK | 2 |
| morphbpe@16384 | `aus+an` | OK | 2 |
| penalty-1@6080 | `aus+an` | OK | 2 |
| penalty-1@8192 | `aus+an` | OK | 2 |
| penalty-1@16384 | `aus+an` | OK | 2 |
| penalty-2@6080 | `aus+an` | OK | 2 |
| penalty-2@8192 | `aus+an` | OK | 2 |
| penalty-2@16384 | `aus+an` | OK | 2 |
| penalty-4@6080 | `aus+an` | OK | 2 |
| penalty-4@8192 | `aus+an` | OK | 2 |
| penalty-4@16384 | `aus+an` | OK | 2 |
| penalty-8@6080 | `aus+an` | OK | 2 |
| penalty-8@8192 | `aus+an` | OK | 2 |
| penalty-8@16384 | `aus+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `aus+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `aus+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `aus+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `aus+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `aus+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `aus+an` | OK | 2 |
| unigram-ablation@6080 | `ausan` |  | 1 |

## `daralan`  (suffixation, tier B_moderate_silver)

**silver gold:** `daral+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `daralan` |  | 1 |
| plain@8192 | `daralan` |  | 1 |
| plain@16384 | `daralan` |  | 1 |
| morphbpe@6080 | `d+aralan` |  | 2 |
| morphbpe@8192 | `d+aralan` |  | 2 |
| morphbpe@16384 | `d+aralan` |  | 2 |
| penalty-1@6080 | `dar+alan` |  | 2 |
| penalty-1@8192 | `dar+alan` |  | 2 |
| penalty-1@16384 | `dar+alan` |  | 2 |
| penalty-2@6080 | `dar+alan` |  | 2 |
| penalty-2@8192 | `dar+alan` |  | 2 |
| penalty-2@16384 | `dar+alan` |  | 2 |
| penalty-4@6080 | `daral+an` | OK | 2 |
| penalty-4@8192 | `daral+an` | OK | 2 |
| penalty-4@16384 | `daral+an` | OK | 2 |
| penalty-8@6080 | `da+ralan` |  | 2 |
| penalty-8@8192 | `da+ralan` |  | 2 |
| penalty-8@16384 | `da+ralan` |  | 2 |
| stochastic-p4-d0.1@6080 | `da+ralan` |  | 2 |
| stochastic-p4-d0.1@8192 | `da+ralan` |  | 2 |
| stochastic-p4-d0.1@16384 | `da+ralan` |  | 2 |
| stochastic-p4-d0.2@6080 | `da+ral+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `daralan` |  | 1 |
| stochastic-p4-d0.2@16384 | `daralan` |  | 1 |
| unigram-ablation@6080 | `daralan` |  | 1 |

## `lipulan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `lipul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lip+ulan` |  | 2 |
| plain@8192 | `lip+ulan` |  | 2 |
| plain@16384 | `lip+ulan` |  | 2 |
| morphbpe@6080 | `lip+ulan` |  | 2 |
| morphbpe@8192 | `lip+ulan` |  | 2 |
| morphbpe@16384 | `lip+ulan` |  | 2 |
| penalty-1@6080 | `lip+ulan` |  | 2 |
| penalty-1@8192 | `lip+ulan` |  | 2 |
| penalty-1@16384 | `lip+ulan` |  | 2 |
| penalty-2@6080 | `lip+ulan` |  | 2 |
| penalty-2@8192 | `lip+ulan` |  | 2 |
| penalty-2@16384 | `lip+ulan` |  | 2 |
| penalty-4@6080 | `lip+ul+an` |  | 3 |
| penalty-4@8192 | `lip+ul+an` |  | 3 |
| penalty-4@16384 | `lip+ulan` |  | 2 |
| penalty-8@6080 | `li+pul+an` |  | 3 |
| penalty-8@8192 | `li+pul+an` |  | 3 |
| penalty-8@16384 | `li+pulan` |  | 2 |
| stochastic-p4-d0.1@6080 | `lip+ul+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `lip+ulan` |  | 2 |
| stochastic-p4-d0.1@16384 | `lip+ulan` |  | 2 |
| stochastic-p4-d0.2@6080 | `li+pul+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `li+pul+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `li+pulan` |  | 2 |
| unigram-ablation@6080 | `lip+ulan` |  | 2 |

## `timan`  (suffixation, tier B_moderate_silver)

**silver gold:** `tim+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `timan` |  | 1 |
| plain@8192 | `timan` |  | 1 |
| plain@16384 | `timan` |  | 1 |
| morphbpe@6080 | `timan` |  | 1 |
| morphbpe@8192 | `timan` |  | 1 |
| morphbpe@16384 | `timan` |  | 1 |
| penalty-1@6080 | `timan` |  | 1 |
| penalty-1@8192 | `timan` |  | 1 |
| penalty-1@16384 | `timan` |  | 1 |
| penalty-2@6080 | `timan` |  | 1 |
| penalty-2@8192 | `timan` |  | 1 |
| penalty-2@16384 | `timan` |  | 1 |
| penalty-4@6080 | `timan` |  | 1 |
| penalty-4@8192 | `timan` |  | 1 |
| penalty-4@16384 | `timan` |  | 1 |
| penalty-8@6080 | `timan` |  | 1 |
| penalty-8@8192 | `timan` |  | 1 |
| penalty-8@16384 | `timan` |  | 1 |
| stochastic-p4-d0.1@6080 | `timan` |  | 1 |
| stochastic-p4-d0.1@8192 | `timan` |  | 1 |
| stochastic-p4-d0.1@16384 | `timan` |  | 1 |
| stochastic-p4-d0.2@6080 | `timan` |  | 1 |
| stochastic-p4-d0.2@8192 | `timan` |  | 1 |
| stochastic-p4-d0.2@16384 | `timan` |  | 1 |
| unigram-ablation@6080 | `timan` |  | 1 |

## `sangkan`  (suffixation, tier B_moderate_silver)

**silver gold:** `sangk+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sangkan` |  | 1 |
| plain@8192 | `sangkan` |  | 1 |
| plain@16384 | `sangkan` |  | 1 |
| morphbpe@6080 | `sangkan` |  | 1 |
| morphbpe@8192 | `sangkan` |  | 1 |
| morphbpe@16384 | `sangkan` |  | 1 |
| penalty-1@6080 | `sangkan` |  | 1 |
| penalty-1@8192 | `sangkan` |  | 1 |
| penalty-1@16384 | `sangkan` |  | 1 |
| penalty-2@6080 | `sangkan` |  | 1 |
| penalty-2@8192 | `sangkan` |  | 1 |
| penalty-2@16384 | `sangkan` |  | 1 |
| penalty-4@6080 | `sangkan` |  | 1 |
| penalty-4@8192 | `sangkan` |  | 1 |
| penalty-4@16384 | `sangkan` |  | 1 |
| penalty-8@6080 | `sangkan` |  | 1 |
| penalty-8@8192 | `sangkan` |  | 1 |
| penalty-8@16384 | `sangkan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sangkan` |  | 1 |
| stochastic-p4-d0.1@8192 | `sangkan` |  | 1 |
| stochastic-p4-d0.1@16384 | `sangkan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sangkan` |  | 1 |
| stochastic-p4-d0.2@8192 | `sangkan` |  | 1 |
| stochastic-p4-d0.2@16384 | `sangkan` |  | 1 |
| unigram-ablation@6080 | `sangkan` |  | 1 |

## `legwan`  (suffixation, tier B_moderate_silver)

**silver gold:** `legw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `leg+wan` |  | 2 |
| plain@8192 | `legwan` |  | 1 |
| plain@16384 | `legwan` |  | 1 |
| morphbpe@6080 | `leg+wan` |  | 2 |
| morphbpe@8192 | `legwan` |  | 1 |
| morphbpe@16384 | `legwan` |  | 1 |
| penalty-1@6080 | `leg+wan` |  | 2 |
| penalty-1@8192 | `legwan` |  | 1 |
| penalty-1@16384 | `legwan` |  | 1 |
| penalty-2@6080 | `leg+wan` |  | 2 |
| penalty-2@8192 | `legwan` |  | 1 |
| penalty-2@16384 | `legwan` |  | 1 |
| penalty-4@6080 | `leg+wan` |  | 2 |
| penalty-4@8192 | `legwan` |  | 1 |
| penalty-4@16384 | `legwan` |  | 1 |
| penalty-8@6080 | `leg+wan` |  | 2 |
| penalty-8@8192 | `legwan` |  | 1 |
| penalty-8@16384 | `legwan` |  | 1 |
| stochastic-p4-d0.1@6080 | `leg+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `legwan` |  | 1 |
| stochastic-p4-d0.1@16384 | `legwan` |  | 1 |
| stochastic-p4-d0.2@6080 | `leg+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `legwan` |  | 1 |
| stochastic-p4-d0.2@16384 | `legwan` |  | 1 |
| unigram-ablation@6080 | `legwan` |  | 1 |

## `kanan`  (suffixation, tier A_strong_silver)

**silver gold:** `kan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kanan` |  | 1 |
| plain@8192 | `kanan` |  | 1 |
| plain@16384 | `kanan` |  | 1 |
| morphbpe@6080 | `kanan` |  | 1 |
| morphbpe@8192 | `kanan` |  | 1 |
| morphbpe@16384 | `kanan` |  | 1 |
| penalty-1@6080 | `kanan` |  | 1 |
| penalty-1@8192 | `kanan` |  | 1 |
| penalty-1@16384 | `kanan` |  | 1 |
| penalty-2@6080 | `kanan` |  | 1 |
| penalty-2@8192 | `kanan` |  | 1 |
| penalty-2@16384 | `kanan` |  | 1 |
| penalty-4@6080 | `kanan` |  | 1 |
| penalty-4@8192 | `kanan` |  | 1 |
| penalty-4@16384 | `kanan` |  | 1 |
| penalty-8@6080 | `kanan` |  | 1 |
| penalty-8@8192 | `kanan` |  | 1 |
| penalty-8@16384 | `kanan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kan+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `kan+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `kan+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `kan+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `kan+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `kan+an` | OK | 2 |
| unigram-ablation@6080 | `kanan` |  | 1 |

## `luguran`  (suffixation, tier B_moderate_silver)

**silver gold:** `lugur+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lug+uran` |  | 2 |
| plain@8192 | `luguran` |  | 1 |
| plain@16384 | `luguran` |  | 1 |
| morphbpe@6080 | `lug+uran` |  | 2 |
| morphbpe@8192 | `luguran` |  | 1 |
| morphbpe@16384 | `luguran` |  | 1 |
| penalty-1@6080 | `lug+uran` |  | 2 |
| penalty-1@8192 | `luguran` |  | 1 |
| penalty-1@16384 | `luguran` |  | 1 |
| penalty-2@6080 | `lug+uran` |  | 2 |
| penalty-2@8192 | `luguran` |  | 1 |
| penalty-2@16384 | `luguran` |  | 1 |
| penalty-4@6080 | `lug+uran` |  | 2 |
| penalty-4@8192 | `luguran` |  | 1 |
| penalty-4@16384 | `luguran` |  | 1 |
| penalty-8@6080 | `luguran` |  | 1 |
| penalty-8@8192 | `luguran` |  | 1 |
| penalty-8@16384 | `luguran` |  | 1 |
| stochastic-p4-d0.1@6080 | `luguran` |  | 1 |
| stochastic-p4-d0.1@8192 | `luguran` |  | 1 |
| stochastic-p4-d0.1@16384 | `luguran` |  | 1 |
| stochastic-p4-d0.2@6080 | `luguran` |  | 1 |
| stochastic-p4-d0.2@8192 | `luguran` |  | 1 |
| stochastic-p4-d0.2@16384 | `luguran` |  | 1 |
| unigram-ablation@6080 | `luguran` |  | 1 |

## `mitagan`  (suffixation, tier B_moderate_silver)

**silver gold:** `mitag+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mit+agan` |  | 2 |
| plain@8192 | `mitagan` |  | 1 |
| plain@16384 | `mitagan` |  | 1 |
| morphbpe@6080 | `mit+agan` |  | 2 |
| morphbpe@8192 | `mit+agan` |  | 2 |
| morphbpe@16384 | `mit+agan` |  | 2 |
| penalty-1@6080 | `mit+agan` |  | 2 |
| penalty-1@8192 | `mit+agan` |  | 2 |
| penalty-1@16384 | `mit+agan` |  | 2 |
| penalty-2@6080 | `mit+agan` |  | 2 |
| penalty-2@8192 | `mit+agan` |  | 2 |
| penalty-2@16384 | `mit+agan` |  | 2 |
| penalty-4@6080 | `mit+agan` |  | 2 |
| penalty-4@8192 | `mit+agan` |  | 2 |
| penalty-4@16384 | `mit+agan` |  | 2 |
| penalty-8@6080 | `mi+tagan` |  | 2 |
| penalty-8@8192 | `mi+tagan` |  | 2 |
| penalty-8@16384 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.1@6080 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.1@8192 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.1@16384 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.2@6080 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.2@8192 | `mi+tagan` |  | 2 |
| stochastic-p4-d0.2@16384 | `mi+tagan` |  | 2 |
| unigram-ablation@6080 | `mitagan` |  | 1 |

## `sabyan`  (suffixation, tier B_moderate_silver)

**silver gold:** `saby+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sabyan` |  | 1 |
| plain@8192 | `sabyan` |  | 1 |
| plain@16384 | `sabyan` |  | 1 |
| morphbpe@6080 | `sabyan` |  | 1 |
| morphbpe@8192 | `sabyan` |  | 1 |
| morphbpe@16384 | `sabyan` |  | 1 |
| penalty-1@6080 | `sabyan` |  | 1 |
| penalty-1@8192 | `sabyan` |  | 1 |
| penalty-1@16384 | `sabyan` |  | 1 |
| penalty-2@6080 | `sabyan` |  | 1 |
| penalty-2@8192 | `sabyan` |  | 1 |
| penalty-2@16384 | `sabyan` |  | 1 |
| penalty-4@6080 | `sabyan` |  | 1 |
| penalty-4@8192 | `sabyan` |  | 1 |
| penalty-4@16384 | `sabyan` |  | 1 |
| penalty-8@6080 | `sabyan` |  | 1 |
| penalty-8@8192 | `sabyan` |  | 1 |
| penalty-8@16384 | `sabyan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sabyan` |  | 1 |
| stochastic-p4-d0.1@8192 | `sabyan` |  | 1 |
| stochastic-p4-d0.1@16384 | `sabyan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sabyan` |  | 1 |
| stochastic-p4-d0.2@8192 | `sabyan` |  | 1 |
| stochastic-p4-d0.2@16384 | `sabyan` |  | 1 |
| unigram-ablation@6080 | `sabyan` |  | 1 |

## `atulan`  (suffixation, tier A_strong_silver)

**silver gold:** `atul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `atulan` |  | 1 |
| plain@8192 | `atulan` |  | 1 |
| plain@16384 | `atulan` |  | 1 |
| morphbpe@6080 | `at+ulan` |  | 2 |
| morphbpe@8192 | `at+ulan` |  | 2 |
| morphbpe@16384 | `at+ulan` |  | 2 |
| penalty-1@6080 | `atul+an` | OK | 2 |
| penalty-1@8192 | `atul+an` | OK | 2 |
| penalty-1@16384 | `atul+an` | OK | 2 |
| penalty-2@6080 | `atul+an` | OK | 2 |
| penalty-2@8192 | `atul+an` | OK | 2 |
| penalty-2@16384 | `atul+an` | OK | 2 |
| penalty-4@6080 | `atul+an` | OK | 2 |
| penalty-4@8192 | `atul+an` | OK | 2 |
| penalty-4@16384 | `atul+an` | OK | 2 |
| penalty-8@6080 | `atul+an` | OK | 2 |
| penalty-8@8192 | `atul+an` | OK | 2 |
| penalty-8@16384 | `atul+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `atul+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `atul+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `atul+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `at+ul+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `at+ul+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `at+ulan` |  | 2 |
| unigram-ablation@6080 | `atulan` |  | 1 |

## `basan`  (suffixation, tier B_moderate_silver)

**silver gold:** `bas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `b+asan` |  | 2 |
| plain@8192 | `b+asan` |  | 2 |
| plain@16384 | `basan` |  | 1 |
| morphbpe@6080 | `basan` |  | 1 |
| morphbpe@8192 | `basan` |  | 1 |
| morphbpe@16384 | `basan` |  | 1 |
| penalty-1@6080 | `basan` |  | 1 |
| penalty-1@8192 | `basan` |  | 1 |
| penalty-1@16384 | `basan` |  | 1 |
| penalty-2@6080 | `basan` |  | 1 |
| penalty-2@8192 | `basan` |  | 1 |
| penalty-2@16384 | `basan` |  | 1 |
| penalty-4@6080 | `basan` |  | 1 |
| penalty-4@8192 | `basan` |  | 1 |
| penalty-4@16384 | `basan` |  | 1 |
| penalty-8@6080 | `basan` |  | 1 |
| penalty-8@8192 | `basan` |  | 1 |
| penalty-8@16384 | `basan` |  | 1 |
| stochastic-p4-d0.1@6080 | `basan` |  | 1 |
| stochastic-p4-d0.1@8192 | `basan` |  | 1 |
| stochastic-p4-d0.1@16384 | `basan` |  | 1 |
| stochastic-p4-d0.2@6080 | `basan` |  | 1 |
| stochastic-p4-d0.2@8192 | `basan` |  | 1 |
| stochastic-p4-d0.2@16384 | `basan` |  | 1 |
| unigram-ablation@6080 | `bas+an` | OK | 2 |

## `beluan`  (suffixation, tier B_moderate_silver)

**silver gold:** `belu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `beluan` |  | 1 |
| plain@8192 | `beluan` |  | 1 |
| plain@16384 | `beluan` |  | 1 |
| morphbpe@6080 | `beluan` |  | 1 |
| morphbpe@8192 | `beluan` |  | 1 |
| morphbpe@16384 | `beluan` |  | 1 |
| penalty-1@6080 | `beluan` |  | 1 |
| penalty-1@8192 | `beluan` |  | 1 |
| penalty-1@16384 | `beluan` |  | 1 |
| penalty-2@6080 | `beluan` |  | 1 |
| penalty-2@8192 | `beluan` |  | 1 |
| penalty-2@16384 | `beluan` |  | 1 |
| penalty-4@6080 | `beluan` |  | 1 |
| penalty-4@8192 | `beluan` |  | 1 |
| penalty-4@16384 | `beluan` |  | 1 |
| penalty-8@6080 | `beluan` |  | 1 |
| penalty-8@8192 | `beluan` |  | 1 |
| penalty-8@16384 | `beluan` |  | 1 |
| stochastic-p4-d0.1@6080 | `beluan` |  | 1 |
| stochastic-p4-d0.1@8192 | `beluan` |  | 1 |
| stochastic-p4-d0.1@16384 | `beluan` |  | 1 |
| stochastic-p4-d0.2@6080 | `beluan` |  | 1 |
| stochastic-p4-d0.2@8192 | `beluan` |  | 1 |
| stochastic-p4-d0.2@16384 | `beluan` |  | 1 |
| unigram-ablation@6080 | `belu+an` | OK | 2 |

## `durulukan`  (suffixation, tier B_moderate_silver)

**silver gold:** `duruluk+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dur+ul+ukan` |  | 3 |
| plain@8192 | `dur+ul+ukan` |  | 3 |
| plain@16384 | `durulukan` |  | 1 |
| morphbpe@6080 | `d+ur+ul+ukan` |  | 4 |
| morphbpe@8192 | `dur+ul+ukan` |  | 3 |
| morphbpe@16384 | `dur+ul+ukan` |  | 3 |
| penalty-1@6080 | `d+ur+ul+ukan` |  | 4 |
| penalty-1@8192 | `dur+ul+ukan` |  | 3 |
| penalty-1@16384 | `dur+ul+ukan` |  | 3 |
| penalty-2@6080 | `d+ur+ul+uk+an` |  | 5 |
| penalty-2@8192 | `dur+ul+ukan` |  | 3 |
| penalty-2@16384 | `dur+ul+ukan` |  | 3 |
| penalty-4@6080 | `d+ur+ulu+kan` |  | 4 |
| penalty-4@8192 | `dur+ulu+kan` |  | 3 |
| penalty-4@16384 | `dur+ulu+kan` |  | 3 |
| penalty-8@6080 | `dur+ulu+kan` |  | 3 |
| penalty-8@8192 | `dur+ulu+kan` |  | 3 |
| penalty-8@16384 | `dur+ulu+kan` |  | 3 |
| stochastic-p4-d0.1@6080 | `dur+ulu+kan` |  | 3 |
| stochastic-p4-d0.1@8192 | `dur+ulu+kan` |  | 3 |
| stochastic-p4-d0.1@16384 | `dur+ulu+kan` |  | 3 |
| stochastic-p4-d0.2@6080 | `du+ru+lu+kan` |  | 4 |
| stochastic-p4-d0.2@8192 | `du+ru+lu+kan` |  | 4 |
| stochastic-p4-d0.2@16384 | `du+ru+lukan` |  | 3 |
| unigram-ablation@6080 | `duru+luk+an` |  | 3 |

## `kutkutan`  (suffixation, tier A_strong_silver)

**silver gold:** `kutkut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kutkutan` |  | 1 |
| plain@8192 | `kutkutan` |  | 1 |
| plain@16384 | `kutkutan` |  | 1 |
| morphbpe@6080 | `kut+ku+tan` |  | 3 |
| morphbpe@8192 | `kut+ku+tan` |  | 3 |
| morphbpe@16384 | `kut+kutan` |  | 2 |
| penalty-1@6080 | `kut+ku+tan` |  | 3 |
| penalty-1@8192 | `kut+ku+tan` |  | 3 |
| penalty-1@16384 | `kut+kutan` |  | 2 |
| penalty-2@6080 | `kut+ku+tan` |  | 3 |
| penalty-2@8192 | `kut+ku+tan` |  | 3 |
| penalty-2@16384 | `kut+kutan` |  | 2 |
| penalty-4@6080 | `kutkut+an` | OK | 2 |
| penalty-4@8192 | `kutkut+an` | OK | 2 |
| penalty-4@16384 | `kutkut+an` | OK | 2 |
| penalty-8@6080 | `kutkut+an` | OK | 2 |
| penalty-8@8192 | `kutkut+an` | OK | 2 |
| penalty-8@16384 | `kutkut+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `kut+ku+tan` |  | 3 |
| stochastic-p4-d0.1@8192 | `kut+kutan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kut+kutan` |  | 2 |
| stochastic-p4-d0.2@6080 | `kutkut+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `kutkut+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `kutkut+an` | OK | 2 |
| unigram-ablation@6080 | `kutkutan` |  | 1 |

## `likwan`  (suffixation, tier B_moderate_silver)

**silver gold:** `likw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lik+wan` |  | 2 |
| plain@8192 | `lik+wan` |  | 2 |
| plain@16384 | `likwan` |  | 1 |
| morphbpe@6080 | `lik+wan` |  | 2 |
| morphbpe@8192 | `lik+wan` |  | 2 |
| morphbpe@16384 | `likwan` |  | 1 |
| penalty-1@6080 | `lik+wan` |  | 2 |
| penalty-1@8192 | `lik+wan` |  | 2 |
| penalty-1@16384 | `likwan` |  | 1 |
| penalty-2@6080 | `lik+wan` |  | 2 |
| penalty-2@8192 | `lik+wan` |  | 2 |
| penalty-2@16384 | `likwan` |  | 1 |
| penalty-4@6080 | `lik+wan` |  | 2 |
| penalty-4@8192 | `lik+wan` |  | 2 |
| penalty-4@16384 | `likwan` |  | 1 |
| penalty-8@6080 | `lik+wan` |  | 2 |
| penalty-8@8192 | `lik+wan` |  | 2 |
| penalty-8@16384 | `likwan` |  | 1 |
| stochastic-p4-d0.1@6080 | `lik+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `lik+wan` |  | 2 |
| stochastic-p4-d0.1@16384 | `likwan` |  | 1 |
| stochastic-p4-d0.2@6080 | `lik+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `lik+wan` |  | 2 |
| stochastic-p4-d0.2@16384 | `likwan` |  | 1 |
| unigram-ablation@6080 | `lik+wan` |  | 2 |

## `santungan`  (suffixation, tier A_strong_silver)

**silver gold:** `santung+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sant+ungan` |  | 2 |
| plain@8192 | `sant+ungan` |  | 2 |
| plain@16384 | `santungan` |  | 1 |
| morphbpe@6080 | `sant+ungan` |  | 2 |
| morphbpe@8192 | `sant+ungan` |  | 2 |
| morphbpe@16384 | `sant+ungan` |  | 2 |
| penalty-1@6080 | `sant+ungan` |  | 2 |
| penalty-1@8192 | `sant+ungan` |  | 2 |
| penalty-1@16384 | `sant+ungan` |  | 2 |
| penalty-2@6080 | `san+tung+an` |  | 3 |
| penalty-2@8192 | `santung+an` | OK | 2 |
| penalty-2@16384 | `santung+an` | OK | 2 |
| penalty-4@6080 | `san+tung+an` |  | 3 |
| penalty-4@8192 | `santung+an` | OK | 2 |
| penalty-4@16384 | `santung+an` | OK | 2 |
| penalty-8@6080 | `santung+an` | OK | 2 |
| penalty-8@8192 | `santung+an` | OK | 2 |
| penalty-8@16384 | `santung+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `san+tung+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `san+tung+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `santung+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `san+tung+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `santung+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `santung+an` | OK | 2 |
| unigram-ablation@6080 | `santung+an` | OK | 2 |

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

## `sigatan`  (suffixation, tier B_moderate_silver)

**silver gold:** `sigat+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sig+atan` |  | 2 |
| plain@8192 | `sig+atan` |  | 2 |
| plain@16384 | `sig+atan` |  | 2 |
| morphbpe@6080 | `sig+atan` |  | 2 |
| morphbpe@8192 | `sig+atan` |  | 2 |
| morphbpe@16384 | `sig+atan` |  | 2 |
| penalty-1@6080 | `sig+atan` |  | 2 |
| penalty-1@8192 | `sig+atan` |  | 2 |
| penalty-1@16384 | `sig+atan` |  | 2 |
| penalty-2@6080 | `sig+atan` |  | 2 |
| penalty-2@8192 | `sig+atan` |  | 2 |
| penalty-2@16384 | `sig+atan` |  | 2 |
| penalty-4@6080 | `sig+atan` |  | 2 |
| penalty-4@8192 | `sig+atan` |  | 2 |
| penalty-4@16384 | `sig+atan` |  | 2 |
| penalty-8@6080 | `sig+atan` |  | 2 |
| penalty-8@8192 | `sig+atan` |  | 2 |
| penalty-8@16384 | `sig+atan` |  | 2 |
| stochastic-p4-d0.1@6080 | `sig+at+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `sig+at+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `sig+atan` |  | 2 |
| stochastic-p4-d0.2@6080 | `sig+at+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `sig+at+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `sig+atan` |  | 2 |
| unigram-ablation@6080 | `sig+at+an` |  | 3 |

## `alipan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `alipan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `alipan` | OK | 1 |
| plain@8192 | `alipan` | OK | 1 |
| plain@16384 | `alipan` | OK | 1 |
| morphbpe@6080 | `alipan` | OK | 1 |
| morphbpe@8192 | `alipan` | OK | 1 |
| morphbpe@16384 | `alipan` | OK | 1 |
| penalty-1@6080 | `alipan` | OK | 1 |
| penalty-1@8192 | `alipan` | OK | 1 |
| penalty-1@16384 | `alipan` | OK | 1 |
| penalty-2@6080 | `alipan` | OK | 1 |
| penalty-2@8192 | `alipan` | OK | 1 |
| penalty-2@16384 | `alipan` | OK | 1 |
| penalty-4@6080 | `alipan` | OK | 1 |
| penalty-4@8192 | `alipan` | OK | 1 |
| penalty-4@16384 | `alipan` | OK | 1 |
| penalty-8@6080 | `alipan` | OK | 1 |
| penalty-8@8192 | `alipan` | OK | 1 |
| penalty-8@16384 | `alipan` | OK | 1 |
| stochastic-p4-d0.1@6080 | `alipan` | OK | 1 |
| stochastic-p4-d0.1@8192 | `alipan` | OK | 1 |
| stochastic-p4-d0.1@16384 | `alipan` | OK | 1 |
| stochastic-p4-d0.2@6080 | `alipan` | OK | 1 |
| stochastic-p4-d0.2@8192 | `alipan` | OK | 1 |
| stochastic-p4-d0.2@16384 | `alipan` | OK | 1 |
| unigram-ablation@6080 | `alipan` | OK | 1 |

## `midian`  (suffixation, tier B_moderate_silver)

**silver gold:** `midi+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mid+ian` |  | 2 |
| plain@8192 | `mid+ian` |  | 2 |
| plain@16384 | `mid+ian` |  | 2 |
| morphbpe@6080 | `mid+ian` |  | 2 |
| morphbpe@8192 | `mid+ian` |  | 2 |
| morphbpe@16384 | `mid+ian` |  | 2 |
| penalty-1@6080 | `mi+d+ian` |  | 3 |
| penalty-1@8192 | `mid+ian` |  | 2 |
| penalty-1@16384 | `mid+ian` |  | 2 |
| penalty-2@6080 | `mi+dian` |  | 2 |
| penalty-2@8192 | `mi+dian` |  | 2 |
| penalty-2@16384 | `mi+dian` |  | 2 |
| penalty-4@6080 | `mi+dian` |  | 2 |
| penalty-4@8192 | `mi+dian` |  | 2 |
| penalty-4@16384 | `mi+dian` |  | 2 |
| penalty-8@6080 | `mi+dian` |  | 2 |
| penalty-8@8192 | `mi+dian` |  | 2 |
| penalty-8@16384 | `mi+dian` |  | 2 |
| stochastic-p4-d0.1@6080 | `mi+dian` |  | 2 |
| stochastic-p4-d0.1@8192 | `mi+dian` |  | 2 |
| stochastic-p4-d0.1@16384 | `mi+dian` |  | 2 |
| stochastic-p4-d0.2@6080 | `mi+dian` |  | 2 |
| stochastic-p4-d0.2@8192 | `mi+dian` |  | 2 |
| stochastic-p4-d0.2@16384 | `mi+dian` |  | 2 |
| unigram-ablation@6080 | `mi+di+an` |  | 3 |

## `capampangan`  (suffixation, tier B_moderate_silver)

**silver gold:** `capampang+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `cap+ampangan` |  | 2 |
| plain@8192 | `cap+ampangan` |  | 2 |
| plain@16384 | `capampangan` |  | 1 |
| morphbpe@6080 | `cap+ampangan` |  | 2 |
| morphbpe@8192 | `cap+ampangan` |  | 2 |
| morphbpe@16384 | `capampangan` |  | 1 |
| penalty-1@6080 | `cap+ampangan` |  | 2 |
| penalty-1@8192 | `cap+ampangan` |  | 2 |
| penalty-1@16384 | `capampangan` |  | 1 |
| penalty-2@6080 | `cap+ampangan` |  | 2 |
| penalty-2@8192 | `cap+ampangan` |  | 2 |
| penalty-2@16384 | `capampangan` |  | 1 |
| penalty-4@6080 | `ca+pampangan` |  | 2 |
| penalty-4@8192 | `ca+pampangan` |  | 2 |
| penalty-4@16384 | `capampangan` |  | 1 |
| penalty-8@6080 | `ca+pampangan` |  | 2 |
| penalty-8@8192 | `ca+pampangan` |  | 2 |
| penalty-8@16384 | `capampangan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ca+pam+pangan` |  | 3 |
| stochastic-p4-d0.1@8192 | `capam+pangan` |  | 2 |
| stochastic-p4-d0.1@16384 | `capampangan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ca+pampangan` |  | 2 |
| stochastic-p4-d0.2@8192 | `ca+pampangan` |  | 2 |
| stochastic-p4-d0.2@16384 | `capampangan` |  | 1 |
| unigram-ablation@6080 | `c+apampangan` |  | 2 |

## `myuman`  (suffixation, tier B_moderate_silver)

**silver gold:** `myum+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `m+yu+man` |  | 3 |
| plain@8192 | `m+yu+man` |  | 3 |
| plain@16384 | `m+yuman` |  | 2 |
| morphbpe@6080 | `m+yu+man` |  | 3 |
| morphbpe@8192 | `m+yu+man` |  | 3 |
| morphbpe@16384 | `myuman` |  | 1 |
| penalty-1@6080 | `m+yu+man` |  | 3 |
| penalty-1@8192 | `m+yu+man` |  | 3 |
| penalty-1@16384 | `myuman` |  | 1 |
| penalty-2@6080 | `m+yu+man` |  | 3 |
| penalty-2@8192 | `m+yu+man` |  | 3 |
| penalty-2@16384 | `myuman` |  | 1 |
| penalty-4@6080 | `m+yu+man` |  | 3 |
| penalty-4@8192 | `m+yu+man` |  | 3 |
| penalty-4@16384 | `myuman` |  | 1 |
| penalty-8@6080 | `m+yu+man` |  | 3 |
| penalty-8@8192 | `m+yu+man` |  | 3 |
| penalty-8@16384 | `myuman` |  | 1 |
| stochastic-p4-d0.1@6080 | `m+yu+man` |  | 3 |
| stochastic-p4-d0.1@8192 | `m+yu+man` |  | 3 |
| stochastic-p4-d0.1@16384 | `myuman` |  | 1 |
| stochastic-p4-d0.2@6080 | `m+yu+man` |  | 3 |
| stochastic-p4-d0.2@8192 | `m+yu+man` |  | 3 |
| stochastic-p4-d0.2@16384 | `myu+man` |  | 2 |
| unigram-ablation@6080 | `m+yu+man` |  | 3 |

## `batiawan`  (suffixation, tier B_moderate_silver)

**silver gold:** `batiaw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bat+ia+wan` |  | 3 |
| plain@8192 | `bat+ia+wan` |  | 3 |
| plain@16384 | `bat+iawan` |  | 2 |
| morphbpe@6080 | `bat+ia+wan` |  | 3 |
| morphbpe@8192 | `bat+ia+wan` |  | 3 |
| morphbpe@16384 | `batiawan` |  | 1 |
| penalty-1@6080 | `bat+ia+wan` |  | 3 |
| penalty-1@8192 | `bat+ia+wan` |  | 3 |
| penalty-1@16384 | `batiawan` |  | 1 |
| penalty-2@6080 | `bat+ia+wan` |  | 3 |
| penalty-2@8192 | `bat+ia+wan` |  | 3 |
| penalty-2@16384 | `batiawan` |  | 1 |
| penalty-4@6080 | `bat+ia+wan` |  | 3 |
| penalty-4@8192 | `bat+ia+wan` |  | 3 |
| penalty-4@16384 | `batiawan` |  | 1 |
| penalty-8@6080 | `bat+ia+wan` |  | 3 |
| penalty-8@8192 | `bat+ia+wan` |  | 3 |
| penalty-8@16384 | `batiawan` |  | 1 |
| stochastic-p4-d0.1@6080 | `bat+ia+wan` |  | 3 |
| stochastic-p4-d0.1@8192 | `bat+ia+wan` |  | 3 |
| stochastic-p4-d0.1@16384 | `bat+ia+wan` |  | 3 |
| stochastic-p4-d0.2@6080 | `bat+ia+wan` |  | 3 |
| stochastic-p4-d0.2@8192 | `bat+ia+wan` |  | 3 |
| stochastic-p4-d0.2@16384 | `batia+wan` |  | 2 |
| unigram-ablation@6080 | `bati+a+wan` |  | 3 |

## `dangalan`  (suffixation, tier A_strong_silver)

**silver gold:** `dangal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dang+alan` |  | 2 |
| plain@8192 | `dangalan` |  | 1 |
| plain@16384 | `dangalan` |  | 1 |
| morphbpe@6080 | `dang+alan` |  | 2 |
| morphbpe@8192 | `dang+alan` |  | 2 |
| morphbpe@16384 | `dang+alan` |  | 2 |
| penalty-1@6080 | `dang+alan` |  | 2 |
| penalty-1@8192 | `dang+alan` |  | 2 |
| penalty-1@16384 | `dang+alan` |  | 2 |
| penalty-2@6080 | `dang+alan` |  | 2 |
| penalty-2@8192 | `dang+alan` |  | 2 |
| penalty-2@16384 | `dang+alan` |  | 2 |
| penalty-4@6080 | `dang+alan` |  | 2 |
| penalty-4@8192 | `dang+alan` |  | 2 |
| penalty-4@16384 | `dang+alan` |  | 2 |
| penalty-8@6080 | `dangal+an` | OK | 2 |
| penalty-8@8192 | `dangal+an` | OK | 2 |
| penalty-8@16384 | `dangal+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `d+ang+alan` |  | 3 |
| stochastic-p4-d0.1@8192 | `d+ang+alan` |  | 3 |
| stochastic-p4-d0.1@16384 | `d+angalan` |  | 2 |
| stochastic-p4-d0.2@6080 | `dang+alan` |  | 2 |
| stochastic-p4-d0.2@8192 | `dang+alan` |  | 2 |
| stochastic-p4-d0.2@16384 | `dang+alan` |  | 2 |
| unigram-ablation@6080 | `dangalan` |  | 1 |

## `saupan`  (suffixation, tier A_strong_silver)

**silver gold:** `saup+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sa+upan` |  | 2 |
| plain@8192 | `saupan` |  | 1 |
| plain@16384 | `saupan` |  | 1 |
| morphbpe@6080 | `sa+u+pan` |  | 3 |
| morphbpe@8192 | `sa+upan` |  | 2 |
| morphbpe@16384 | `sa+upan` |  | 2 |
| penalty-1@6080 | `sa+u+pan` |  | 3 |
| penalty-1@8192 | `sa+upan` |  | 2 |
| penalty-1@16384 | `sa+upan` |  | 2 |
| penalty-2@6080 | `sa+u+pan` |  | 3 |
| penalty-2@8192 | `sa+upan` |  | 2 |
| penalty-2@16384 | `sa+upan` |  | 2 |
| penalty-4@6080 | `sa+u+pan` |  | 3 |
| penalty-4@8192 | `sa+upan` |  | 2 |
| penalty-4@16384 | `sa+upan` |  | 2 |
| penalty-8@6080 | `saup+an` | OK | 2 |
| penalty-8@8192 | `saup+an` | OK | 2 |
| penalty-8@16384 | `saup+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `sa+u+pan` |  | 3 |
| stochastic-p4-d0.1@8192 | `sau+pan` |  | 2 |
| stochastic-p4-d0.1@16384 | `sau+pan` |  | 2 |
| stochastic-p4-d0.2@6080 | `saup+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `saup+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `saup+an` | OK | 2 |
| unigram-ablation@6080 | `saupan` |  | 1 |

## `labanan`  (suffixation, tier A_strong_silver)

**silver gold:** `laban+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `labanan` |  | 1 |
| plain@8192 | `labanan` |  | 1 |
| plain@16384 | `labanan` |  | 1 |
| morphbpe@6080 | `laban+an` | OK | 2 |
| morphbpe@8192 | `laban+an` | OK | 2 |
| morphbpe@16384 | `laban+an` | OK | 2 |
| penalty-1@6080 | `laban+an` | OK | 2 |
| penalty-1@8192 | `laban+an` | OK | 2 |
| penalty-1@16384 | `laban+an` | OK | 2 |
| penalty-2@6080 | `laban+an` | OK | 2 |
| penalty-2@8192 | `laban+an` | OK | 2 |
| penalty-2@16384 | `laban+an` | OK | 2 |
| penalty-4@6080 | `laban+an` | OK | 2 |
| penalty-4@8192 | `laban+an` | OK | 2 |
| penalty-4@16384 | `laban+an` | OK | 2 |
| penalty-8@6080 | `laban+an` | OK | 2 |
| penalty-8@8192 | `laban+an` | OK | 2 |
| penalty-8@16384 | `laban+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `laban+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `laban+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `laban+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `la+ban+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `la+ban+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `la+banan` |  | 2 |
| unigram-ablation@6080 | `labanan` |  | 1 |

## `lakuan`  (suffixation, tier B_moderate_silver)

**silver gold:** `laku+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lak+uan` |  | 2 |
| plain@8192 | `lakuan` |  | 1 |
| plain@16384 | `lakuan` |  | 1 |
| morphbpe@6080 | `lakuan` |  | 1 |
| morphbpe@8192 | `lakuan` |  | 1 |
| morphbpe@16384 | `lakuan` |  | 1 |
| penalty-1@6080 | `lakuan` |  | 1 |
| penalty-1@8192 | `lakuan` |  | 1 |
| penalty-1@16384 | `lakuan` |  | 1 |
| penalty-2@6080 | `lakuan` |  | 1 |
| penalty-2@8192 | `lakuan` |  | 1 |
| penalty-2@16384 | `lakuan` |  | 1 |
| penalty-4@6080 | `lakuan` |  | 1 |
| penalty-4@8192 | `lakuan` |  | 1 |
| penalty-4@16384 | `lakuan` |  | 1 |
| penalty-8@6080 | `lakuan` |  | 1 |
| penalty-8@8192 | `lakuan` |  | 1 |
| penalty-8@16384 | `lakuan` |  | 1 |
| stochastic-p4-d0.1@6080 | `lakuan` |  | 1 |
| stochastic-p4-d0.1@8192 | `lakuan` |  | 1 |
| stochastic-p4-d0.1@16384 | `lakuan` |  | 1 |
| stochastic-p4-d0.2@6080 | `la+kuan` |  | 2 |
| stochastic-p4-d0.2@8192 | `lakuan` |  | 1 |
| stochastic-p4-d0.2@16384 | `lakuan` |  | 1 |
| unigram-ablation@6080 | `lakuan` |  | 1 |

## `liguran`  (suffixation, tier B_moderate_silver)

**silver gold:** `ligur+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lig+uran` |  | 2 |
| plain@8192 | `liguran` |  | 1 |
| plain@16384 | `liguran` |  | 1 |
| morphbpe@6080 | `lig+uran` |  | 2 |
| morphbpe@8192 | `liguran` |  | 1 |
| morphbpe@16384 | `liguran` |  | 1 |
| penalty-1@6080 | `lig+uran` |  | 2 |
| penalty-1@8192 | `liguran` |  | 1 |
| penalty-1@16384 | `liguran` |  | 1 |
| penalty-2@6080 | `lig+uran` |  | 2 |
| penalty-2@8192 | `liguran` |  | 1 |
| penalty-2@16384 | `liguran` |  | 1 |
| penalty-4@6080 | `lig+uran` |  | 2 |
| penalty-4@8192 | `liguran` |  | 1 |
| penalty-4@16384 | `liguran` |  | 1 |
| penalty-8@6080 | `lig+uran` |  | 2 |
| penalty-8@8192 | `liguran` |  | 1 |
| penalty-8@16384 | `liguran` |  | 1 |
| stochastic-p4-d0.1@6080 | `li+guran` |  | 2 |
| stochastic-p4-d0.1@8192 | `liguran` |  | 1 |
| stochastic-p4-d0.1@16384 | `liguran` |  | 1 |
| stochastic-p4-d0.2@6080 | `li+guran` |  | 2 |
| stochastic-p4-d0.2@8192 | `liguran` |  | 1 |
| stochastic-p4-d0.2@16384 | `liguran` |  | 1 |
| unigram-ablation@6080 | `lig+uran` |  | 2 |

## `akalinguan`  (suffixation, tier B_moderate_silver)

**silver gold:** `akalingu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `akal+inguan` |  | 2 |
| plain@8192 | `akal+inguan` |  | 2 |
| plain@16384 | `akalinguan` |  | 1 |
| morphbpe@6080 | `akal+ing+uan` |  | 3 |
| morphbpe@8192 | `akaling+uan` |  | 2 |
| morphbpe@16384 | `akalinguan` |  | 1 |
| penalty-1@6080 | `akal+ing+uan` |  | 3 |
| penalty-1@8192 | `akaling+uan` |  | 2 |
| penalty-1@16384 | `akalinguan` |  | 1 |
| penalty-2@6080 | `akal+ing+uan` |  | 3 |
| penalty-2@8192 | `akaling+uan` |  | 2 |
| penalty-2@16384 | `akalinguan` |  | 1 |
| penalty-4@6080 | `akal+ing+uan` |  | 3 |
| penalty-4@8192 | `akal+ing+uan` |  | 3 |
| penalty-4@16384 | `akalinguan` |  | 1 |
| penalty-8@6080 | `aka+linguan` |  | 2 |
| penalty-8@8192 | `aka+linguan` |  | 2 |
| penalty-8@16384 | `akalinguan` |  | 1 |
| stochastic-p4-d0.1@6080 | `aka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.1@8192 | `aka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.1@16384 | `akalinguan` |  | 1 |
| stochastic-p4-d0.2@6080 | `aka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.2@8192 | `aka+li+ng+uan` |  | 4 |
| stochastic-p4-d0.2@16384 | `akalinguan` |  | 1 |
| unigram-ablation@6080 | `a+kalingu+an` |  | 3 |

## `daramdaman`  (suffixation, tier B_moderate_silver)

**silver gold:** `daramdam+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `dar+amdaman` |  | 2 |
| plain@8192 | `daramdaman` |  | 1 |
| plain@16384 | `daramdaman` |  | 1 |
| morphbpe@6080 | `dar+amdaman` |  | 2 |
| morphbpe@8192 | `dar+amdaman` |  | 2 |
| morphbpe@16384 | `dar+amdaman` |  | 2 |
| penalty-1@6080 | `dar+amdaman` |  | 2 |
| penalty-1@8192 | `dar+amdaman` |  | 2 |
| penalty-1@16384 | `dar+amdaman` |  | 2 |
| penalty-2@6080 | `dar+amdaman` |  | 2 |
| penalty-2@8192 | `dar+amdaman` |  | 2 |
| penalty-2@16384 | `dar+amdaman` |  | 2 |
| penalty-4@6080 | `dar+amdam+an` |  | 3 |
| penalty-4@8192 | `dar+amdam+an` |  | 3 |
| penalty-4@16384 | `dar+amdam+an` |  | 3 |
| penalty-8@6080 | `da+ramdam+an` |  | 3 |
| penalty-8@8192 | `da+ramdam+an` |  | 3 |
| penalty-8@16384 | `da+ramdam+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `da+ram+daman` |  | 3 |
| stochastic-p4-d0.1@8192 | `da+ram+daman` |  | 3 |
| stochastic-p4-d0.1@16384 | `da+ram+daman` |  | 3 |
| stochastic-p4-d0.2@6080 | `da+ramdam+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `da+ramdam+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `da+ramdam+an` |  | 3 |
| unigram-ablation@6080 | `daramdaman` |  | 1 |

## `sikan`  (suffixation, tier B_moderate_silver)

**silver gold:** `sik+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sikan` |  | 1 |
| plain@8192 | `sikan` |  | 1 |
| plain@16384 | `sikan` |  | 1 |
| morphbpe@6080 | `sikan` |  | 1 |
| morphbpe@8192 | `sikan` |  | 1 |
| morphbpe@16384 | `sikan` |  | 1 |
| penalty-1@6080 | `sikan` |  | 1 |
| penalty-1@8192 | `sikan` |  | 1 |
| penalty-1@16384 | `sikan` |  | 1 |
| penalty-2@6080 | `sikan` |  | 1 |
| penalty-2@8192 | `sikan` |  | 1 |
| penalty-2@16384 | `sikan` |  | 1 |
| penalty-4@6080 | `sikan` |  | 1 |
| penalty-4@8192 | `sikan` |  | 1 |
| penalty-4@16384 | `sikan` |  | 1 |
| penalty-8@6080 | `sikan` |  | 1 |
| penalty-8@8192 | `sikan` |  | 1 |
| penalty-8@16384 | `sikan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sikan` |  | 1 |
| stochastic-p4-d0.1@8192 | `sikan` |  | 1 |
| stochastic-p4-d0.1@16384 | `sikan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sikan` |  | 1 |
| stochastic-p4-d0.2@8192 | `sikan` |  | 1 |
| stochastic-p4-d0.2@16384 | `sikan` |  | 1 |
| unigram-ablation@6080 | `sikan` |  | 1 |

## `tanggapan`  (suffixation, tier A_strong_silver)

**silver gold:** `tanggap+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tanggapan` |  | 1 |
| plain@8192 | `tanggapan` |  | 1 |
| plain@16384 | `tanggapan` |  | 1 |
| morphbpe@6080 | `tanggap+an` | OK | 2 |
| morphbpe@8192 | `tanggap+an` | OK | 2 |
| morphbpe@16384 | `tanggap+an` | OK | 2 |
| penalty-1@6080 | `tanggap+an` | OK | 2 |
| penalty-1@8192 | `tanggap+an` | OK | 2 |
| penalty-1@16384 | `tanggap+an` | OK | 2 |
| penalty-2@6080 | `tanggap+an` | OK | 2 |
| penalty-2@8192 | `tanggap+an` | OK | 2 |
| penalty-2@16384 | `tanggap+an` | OK | 2 |
| penalty-4@6080 | `tanggap+an` | OK | 2 |
| penalty-4@8192 | `tanggap+an` | OK | 2 |
| penalty-4@16384 | `tanggap+an` | OK | 2 |
| penalty-8@6080 | `tanggap+an` | OK | 2 |
| penalty-8@8192 | `tanggap+an` | OK | 2 |
| penalty-8@16384 | `tanggap+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `tang+ga+pan` |  | 3 |
| stochastic-p4-d0.1@8192 | `tang+ga+pan` |  | 3 |
| stochastic-p4-d0.1@16384 | `tang+ga+pan` |  | 3 |
| stochastic-p4-d0.2@6080 | `tanggap+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `tanggap+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `tanggap+an` | OK | 2 |
| unigram-ablation@6080 | `tanggapan` |  | 1 |

## `taguimpan`  (suffixation, tier B_moderate_silver)

**silver gold:** `taguimp+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+agu+impan` |  | 3 |
| plain@8192 | `t+aguimpan` |  | 2 |
| plain@16384 | `taguimpan` |  | 1 |
| morphbpe@6080 | `t+agu+impan` |  | 3 |
| morphbpe@8192 | `t+aguimpan` |  | 2 |
| morphbpe@16384 | `taguimpan` |  | 1 |
| penalty-1@6080 | `tag+u+impan` |  | 3 |
| penalty-1@8192 | `tag+u+impan` |  | 3 |
| penalty-1@16384 | `taguimpan` |  | 1 |
| penalty-2@6080 | `tag+u+impan` |  | 3 |
| penalty-2@8192 | `tag+u+impan` |  | 3 |
| penalty-2@16384 | `taguimpan` |  | 1 |
| penalty-4@6080 | `ta+gu+impan` |  | 3 |
| penalty-4@8192 | `tagu+impan` |  | 2 |
| penalty-4@16384 | `taguimpan` |  | 1 |
| penalty-8@6080 | `ta+gu+impan` |  | 3 |
| penalty-8@8192 | `tagu+impan` |  | 2 |
| penalty-8@16384 | `taguimpan` |  | 1 |
| stochastic-p4-d0.1@6080 | `tagu+impan` |  | 2 |
| stochastic-p4-d0.1@8192 | `tagu+impan` |  | 2 |
| stochastic-p4-d0.1@16384 | `taguimpan` |  | 1 |
| stochastic-p4-d0.2@6080 | `tagu+imp+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `tagu+imp+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `taguimpan` |  | 1 |
| unigram-ablation@6080 | `taguimpan` |  | 1 |

## `ubingan`  (suffixation, tier B_moderate_silver)

**silver gold:** `ubing+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ub+ingan` |  | 2 |
| plain@8192 | `ubingan` |  | 1 |
| plain@16384 | `ubingan` |  | 1 |
| morphbpe@6080 | `ub+ingan` |  | 2 |
| morphbpe@8192 | `ubingan` |  | 1 |
| morphbpe@16384 | `ubingan` |  | 1 |
| penalty-1@6080 | `ub+ingan` |  | 2 |
| penalty-1@8192 | `ubingan` |  | 1 |
| penalty-1@16384 | `ubingan` |  | 1 |
| penalty-2@6080 | `ub+ingan` |  | 2 |
| penalty-2@8192 | `ubingan` |  | 1 |
| penalty-2@16384 | `ubingan` |  | 1 |
| penalty-4@6080 | `ub+ingan` |  | 2 |
| penalty-4@8192 | `ubingan` |  | 1 |
| penalty-4@16384 | `ubingan` |  | 1 |
| penalty-8@6080 | `ub+ing+an` |  | 3 |
| penalty-8@8192 | `ubingan` |  | 1 |
| penalty-8@16384 | `ubingan` |  | 1 |
| stochastic-p4-d0.1@6080 | `u+bi+ngan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ubingan` |  | 1 |
| stochastic-p4-d0.1@16384 | `ubingan` |  | 1 |
| stochastic-p4-d0.2@6080 | `u+bi+ngan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ubingan` |  | 1 |
| stochastic-p4-d0.2@16384 | `ubingan` |  | 1 |
| unigram-ablation@6080 | `ubingan` |  | 1 |

## `sukulan`  (suffixation, tier A_strong_silver)

**silver gold:** `sukul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `suk+ulan` |  | 2 |
| plain@8192 | `sukulan` |  | 1 |
| plain@16384 | `sukulan` |  | 1 |
| morphbpe@6080 | `suk+ulan` |  | 2 |
| morphbpe@8192 | `suk+ulan` |  | 2 |
| morphbpe@16384 | `suk+ulan` |  | 2 |
| penalty-1@6080 | `sukul+an` | OK | 2 |
| penalty-1@8192 | `sukul+an` | OK | 2 |
| penalty-1@16384 | `sukul+an` | OK | 2 |
| penalty-2@6080 | `sukul+an` | OK | 2 |
| penalty-2@8192 | `sukul+an` | OK | 2 |
| penalty-2@16384 | `sukul+an` | OK | 2 |
| penalty-4@6080 | `sukul+an` | OK | 2 |
| penalty-4@8192 | `sukul+an` | OK | 2 |
| penalty-4@16384 | `sukul+an` | OK | 2 |
| penalty-8@6080 | `sukul+an` | OK | 2 |
| penalty-8@8192 | `sukul+an` | OK | 2 |
| penalty-8@16384 | `sukul+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `sukul+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `sukul+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `sukul+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `su+kulan` |  | 2 |
| stochastic-p4-d0.2@8192 | `su+kulan` |  | 2 |
| stochastic-p4-d0.2@16384 | `su+kulan` |  | 2 |
| unigram-ablation@6080 | `sukul+an` | OK | 2 |

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

## `bustan`  (suffixation, tier B_moderate_silver)

**silver gold:** `bust+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bus+tan` |  | 2 |
| plain@8192 | `bus+tan` |  | 2 |
| plain@16384 | `bustan` |  | 1 |
| morphbpe@6080 | `bus+tan` |  | 2 |
| morphbpe@8192 | `bus+tan` |  | 2 |
| morphbpe@16384 | `bustan` |  | 1 |
| penalty-1@6080 | `bus+tan` |  | 2 |
| penalty-1@8192 | `bus+tan` |  | 2 |
| penalty-1@16384 | `bustan` |  | 1 |
| penalty-2@6080 | `bustan` |  | 1 |
| penalty-2@8192 | `bustan` |  | 1 |
| penalty-2@16384 | `bustan` |  | 1 |
| penalty-4@6080 | `bustan` |  | 1 |
| penalty-4@8192 | `bustan` |  | 1 |
| penalty-4@16384 | `bustan` |  | 1 |
| penalty-8@6080 | `bustan` |  | 1 |
| penalty-8@8192 | `bustan` |  | 1 |
| penalty-8@16384 | `bustan` |  | 1 |
| stochastic-p4-d0.1@6080 | `bus+tan` |  | 2 |
| stochastic-p4-d0.1@8192 | `bus+tan` |  | 2 |
| stochastic-p4-d0.1@16384 | `bustan` |  | 1 |
| stochastic-p4-d0.2@6080 | `bustan` |  | 1 |
| stochastic-p4-d0.2@8192 | `bustan` |  | 1 |
| stochastic-p4-d0.2@16384 | `bustan` |  | 1 |
| unigram-ablation@6080 | `bus+tan` |  | 2 |

## `canian`  (suffixation, tier B_moderate_silver)

**silver gold:** `cani+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `can+ian` |  | 2 |
| plain@8192 | `can+ian` |  | 2 |
| plain@16384 | `canian` |  | 1 |
| morphbpe@6080 | `can+ian` |  | 2 |
| morphbpe@8192 | `canian` |  | 1 |
| morphbpe@16384 | `canian` |  | 1 |
| penalty-1@6080 | `can+ian` |  | 2 |
| penalty-1@8192 | `can+ian` |  | 2 |
| penalty-1@16384 | `canian` |  | 1 |
| penalty-2@6080 | `can+ian` |  | 2 |
| penalty-2@8192 | `can+ian` |  | 2 |
| penalty-2@16384 | `canian` |  | 1 |
| penalty-4@6080 | `can+ian` |  | 2 |
| penalty-4@8192 | `can+ian` |  | 2 |
| penalty-4@16384 | `canian` |  | 1 |
| penalty-8@6080 | `c+anian` |  | 2 |
| penalty-8@8192 | `c+anian` |  | 2 |
| penalty-8@16384 | `canian` |  | 1 |
| stochastic-p4-d0.1@6080 | `c+anian` |  | 2 |
| stochastic-p4-d0.1@8192 | `c+anian` |  | 2 |
| stochastic-p4-d0.1@16384 | `canian` |  | 1 |
| stochastic-p4-d0.2@6080 | `cani+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `cani+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `canian` |  | 1 |
| unigram-ablation@6080 | `can+ian` |  | 2 |

## `kaban`  (suffixation, tier B_moderate_silver)

**silver gold:** `kab+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `ka+ban` |  | 2 |
| plain@8192 | `ka+ban` |  | 2 |
| plain@16384 | `kaban` |  | 1 |
| morphbpe@6080 | `ka+ban` |  | 2 |
| morphbpe@8192 | `ka+ban` |  | 2 |
| morphbpe@16384 | `kaban` |  | 1 |
| penalty-1@6080 | `ka+ban` |  | 2 |
| penalty-1@8192 | `ka+ban` |  | 2 |
| penalty-1@16384 | `kaban` |  | 1 |
| penalty-2@6080 | `ka+ban` |  | 2 |
| penalty-2@8192 | `ka+ban` |  | 2 |
| penalty-2@16384 | `kaban` |  | 1 |
| penalty-4@6080 | `ka+ban` |  | 2 |
| penalty-4@8192 | `ka+ban` |  | 2 |
| penalty-4@16384 | `kaban` |  | 1 |
| penalty-8@6080 | `ka+ban` |  | 2 |
| penalty-8@8192 | `ka+ban` |  | 2 |
| penalty-8@16384 | `kaban` |  | 1 |
| stochastic-p4-d0.1@6080 | `ka+ban` |  | 2 |
| stochastic-p4-d0.1@8192 | `ka+ban` |  | 2 |
| stochastic-p4-d0.1@16384 | `kaban` |  | 1 |
| stochastic-p4-d0.2@6080 | `ka+ban` |  | 2 |
| stochastic-p4-d0.2@8192 | `ka+ban` |  | 2 |
| stochastic-p4-d0.2@16384 | `kaban` |  | 1 |
| unigram-ablation@6080 | `ka+ban` |  | 2 |

## `samban`  (suffixation, tier B_moderate_silver)

**silver gold:** `samb+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `s+amban` |  | 2 |
| plain@8192 | `samban` |  | 1 |
| plain@16384 | `samban` |  | 1 |
| morphbpe@6080 | `sam+ban` |  | 2 |
| morphbpe@8192 | `sam+ban` |  | 2 |
| morphbpe@16384 | `sam+ban` |  | 2 |
| penalty-1@6080 | `sam+ban` |  | 2 |
| penalty-1@8192 | `sam+ban` |  | 2 |
| penalty-1@16384 | `sam+ban` |  | 2 |
| penalty-2@6080 | `sam+ban` |  | 2 |
| penalty-2@8192 | `sam+ban` |  | 2 |
| penalty-2@16384 | `sam+ban` |  | 2 |
| penalty-4@6080 | `sam+ban` |  | 2 |
| penalty-4@8192 | `sam+ban` |  | 2 |
| penalty-4@16384 | `sam+ban` |  | 2 |
| penalty-8@6080 | `sam+ban` |  | 2 |
| penalty-8@8192 | `sam+ban` |  | 2 |
| penalty-8@16384 | `sam+ban` |  | 2 |
| stochastic-p4-d0.1@6080 | `sam+ban` |  | 2 |
| stochastic-p4-d0.1@8192 | `sam+ban` |  | 2 |
| stochastic-p4-d0.1@16384 | `sam+ban` |  | 2 |
| stochastic-p4-d0.2@6080 | `sam+ban` |  | 2 |
| stochastic-p4-d0.2@8192 | `sam+ban` |  | 2 |
| stochastic-p4-d0.2@16384 | `sam+ban` |  | 2 |
| unigram-ablation@6080 | `samban` |  | 1 |

## `aguman`  (suffixation, tier A_strong_silver)

**silver gold:** `agum+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `aguman` |  | 1 |
| plain@8192 | `aguman` |  | 1 |
| plain@16384 | `aguman` |  | 1 |
| morphbpe@6080 | `aguman` |  | 1 |
| morphbpe@8192 | `aguman` |  | 1 |
| morphbpe@16384 | `aguman` |  | 1 |
| penalty-1@6080 | `aguman` |  | 1 |
| penalty-1@8192 | `aguman` |  | 1 |
| penalty-1@16384 | `aguman` |  | 1 |
| penalty-2@6080 | `aguman` |  | 1 |
| penalty-2@8192 | `aguman` |  | 1 |
| penalty-2@16384 | `aguman` |  | 1 |
| penalty-4@6080 | `aguman` |  | 1 |
| penalty-4@8192 | `aguman` |  | 1 |
| penalty-4@16384 | `aguman` |  | 1 |
| penalty-8@6080 | `aguman` |  | 1 |
| penalty-8@8192 | `aguman` |  | 1 |
| penalty-8@16384 | `aguman` |  | 1 |
| stochastic-p4-d0.1@6080 | `aguman` |  | 1 |
| stochastic-p4-d0.1@8192 | `aguman` |  | 1 |
| stochastic-p4-d0.1@16384 | `aguman` |  | 1 |
| stochastic-p4-d0.2@6080 | `aguman` |  | 1 |
| stochastic-p4-d0.2@8192 | `aguman` |  | 1 |
| stochastic-p4-d0.2@16384 | `aguman` |  | 1 |
| unigram-ablation@6080 | `aguman` |  | 1 |

## `apalsintan`  (suffixation, tier B_moderate_silver)

**silver gold:** `apalsint+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `apal+sintan` |  | 2 |
| plain@8192 | `apal+sintan` |  | 2 |
| plain@16384 | `apal+sintan` |  | 2 |
| morphbpe@6080 | `apal+sintan` |  | 2 |
| morphbpe@8192 | `apal+sintan` |  | 2 |
| morphbpe@16384 | `apal+sintan` |  | 2 |
| penalty-1@6080 | `apal+sintan` |  | 2 |
| penalty-1@8192 | `apal+sintan` |  | 2 |
| penalty-1@16384 | `apal+sintan` |  | 2 |
| penalty-2@6080 | `apal+sintan` |  | 2 |
| penalty-2@8192 | `apal+sintan` |  | 2 |
| penalty-2@16384 | `apal+sintan` |  | 2 |
| penalty-4@6080 | `apal+sintan` |  | 2 |
| penalty-4@8192 | `apal+sintan` |  | 2 |
| penalty-4@16384 | `apal+sintan` |  | 2 |
| penalty-8@6080 | `apal+sintan` |  | 2 |
| penalty-8@8192 | `apal+sintan` |  | 2 |
| penalty-8@16384 | `apal+sintan` |  | 2 |
| stochastic-p4-d0.1@6080 | `apal+sintan` |  | 2 |
| stochastic-p4-d0.1@8192 | `apal+sintan` |  | 2 |
| stochastic-p4-d0.1@16384 | `apal+sintan` |  | 2 |
| stochastic-p4-d0.2@6080 | `apal+s+int+an` |  | 4 |
| stochastic-p4-d0.2@8192 | `apal+s+int+an` |  | 4 |
| stochastic-p4-d0.2@16384 | `apal+s+int+an` |  | 4 |
| unigram-ablation@6080 | `a+palsintan` |  | 2 |

## `siran`  (suffixation, tier B_moderate_silver)

**silver gold:** `sir+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `s+iran` |  | 2 |
| plain@8192 | `s+iran` |  | 2 |
| plain@16384 | `siran` |  | 1 |
| morphbpe@6080 | `s+iran` |  | 2 |
| morphbpe@8192 | `s+iran` |  | 2 |
| morphbpe@16384 | `siran` |  | 1 |
| penalty-1@6080 | `s+iran` |  | 2 |
| penalty-1@8192 | `s+iran` |  | 2 |
| penalty-1@16384 | `siran` |  | 1 |
| penalty-2@6080 | `s+iran` |  | 2 |
| penalty-2@8192 | `s+iran` |  | 2 |
| penalty-2@16384 | `siran` |  | 1 |
| penalty-4@6080 | `si+ran` |  | 2 |
| penalty-4@8192 | `si+ran` |  | 2 |
| penalty-4@16384 | `siran` |  | 1 |
| penalty-8@6080 | `siran` |  | 1 |
| penalty-8@8192 | `siran` |  | 1 |
| penalty-8@16384 | `siran` |  | 1 |
| stochastic-p4-d0.1@6080 | `si+ran` |  | 2 |
| stochastic-p4-d0.1@8192 | `si+ran` |  | 2 |
| stochastic-p4-d0.1@16384 | `siran` |  | 1 |
| stochastic-p4-d0.2@6080 | `si+ran` |  | 2 |
| stochastic-p4-d0.2@8192 | `si+ran` |  | 2 |
| stochastic-p4-d0.2@16384 | `siran` |  | 1 |
| unigram-ablation@6080 | `s+iran` |  | 2 |

## `mitakutan`  (suffixation, tier B_moderate_silver)

**silver gold:** `mitakut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mit+akutan` |  | 2 |
| plain@8192 | `mit+akutan` |  | 2 |
| plain@16384 | `mitakutan` |  | 1 |
| morphbpe@6080 | `mit+ak+utan` |  | 3 |
| morphbpe@8192 | `mit+ak+utan` |  | 3 |
| morphbpe@16384 | `mit+ak+utan` |  | 3 |
| penalty-1@6080 | `mit+ak+utan` |  | 3 |
| penalty-1@8192 | `mit+ak+utan` |  | 3 |
| penalty-1@16384 | `mit+ak+utan` |  | 3 |
| penalty-2@6080 | `mit+ak+utan` |  | 3 |
| penalty-2@8192 | `mit+ak+utan` |  | 3 |
| penalty-2@16384 | `mit+ak+utan` |  | 3 |
| penalty-4@6080 | `m+ita+kut+an` |  | 4 |
| penalty-4@8192 | `mita+kut+an` |  | 3 |
| penalty-4@16384 | `mita+kut+an` |  | 3 |
| penalty-8@6080 | `mi+takut+an` |  | 3 |
| penalty-8@8192 | `mi+takut+an` |  | 3 |
| penalty-8@16384 | `mi+takut+an` |  | 3 |
| stochastic-p4-d0.1@6080 | `mi+ta+ku+tan` |  | 4 |
| stochastic-p4-d0.1@8192 | `mi+ta+kutan` |  | 3 |
| stochastic-p4-d0.1@16384 | `mi+ta+kutan` |  | 3 |
| stochastic-p4-d0.2@6080 | `mi+takut+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `mi+takut+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `mi+takut+an` |  | 3 |
| unigram-ablation@6080 | `mi+takutan` |  | 2 |

## `tikpan`  (suffixation, tier B_moderate_silver)

**silver gold:** `tikp+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tik+pan` |  | 2 |
| plain@8192 | `tik+pan` |  | 2 |
| plain@16384 | `tik+pan` |  | 2 |
| morphbpe@6080 | `tik+pan` |  | 2 |
| morphbpe@8192 | `tik+pan` |  | 2 |
| morphbpe@16384 | `tik+pan` |  | 2 |
| penalty-1@6080 | `tik+pan` |  | 2 |
| penalty-1@8192 | `tik+pan` |  | 2 |
| penalty-1@16384 | `tik+pan` |  | 2 |
| penalty-2@6080 | `tik+pan` |  | 2 |
| penalty-2@8192 | `tik+pan` |  | 2 |
| penalty-2@16384 | `tik+pan` |  | 2 |
| penalty-4@6080 | `tik+pan` |  | 2 |
| penalty-4@8192 | `tik+pan` |  | 2 |
| penalty-4@16384 | `tik+pan` |  | 2 |
| penalty-8@6080 | `tik+pan` |  | 2 |
| penalty-8@8192 | `tik+pan` |  | 2 |
| penalty-8@16384 | `tik+pan` |  | 2 |
| stochastic-p4-d0.1@6080 | `tik+pan` |  | 2 |
| stochastic-p4-d0.1@8192 | `tik+pan` |  | 2 |
| stochastic-p4-d0.1@16384 | `tik+pan` |  | 2 |
| stochastic-p4-d0.2@6080 | `tik+p+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `tik+p+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `tik+p+an` |  | 3 |
| unigram-ablation@6080 | `tik+pan` |  | 2 |

## `tipunan`  (suffixation, tier A_strong_silver)

**silver gold:** `tipun+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+ipunan` |  | 2 |
| plain@8192 | `t+ipunan` |  | 2 |
| plain@16384 | `tipunan` |  | 1 |
| morphbpe@6080 | `tip+unan` |  | 2 |
| morphbpe@8192 | `tip+unan` |  | 2 |
| morphbpe@16384 | `tip+unan` |  | 2 |
| penalty-1@6080 | `tipun+an` | OK | 2 |
| penalty-1@8192 | `tipun+an` | OK | 2 |
| penalty-1@16384 | `tipun+an` | OK | 2 |
| penalty-2@6080 | `tipun+an` | OK | 2 |
| penalty-2@8192 | `tipun+an` | OK | 2 |
| penalty-2@16384 | `tipun+an` | OK | 2 |
| penalty-4@6080 | `tipun+an` | OK | 2 |
| penalty-4@8192 | `tipun+an` | OK | 2 |
| penalty-4@16384 | `tipun+an` | OK | 2 |
| penalty-8@6080 | `tipun+an` | OK | 2 |
| penalty-8@8192 | `tipun+an` | OK | 2 |
| penalty-8@16384 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.1@8192 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.1@16384 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.2@8192 | `tipun+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `tipun+an` | OK | 2 |
| unigram-ablation@6080 | `tipun+an` | OK | 2 |

## `capitan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `capitan`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `cap+itan` |  | 2 |
| plain@8192 | `cap+itan` |  | 2 |
| plain@16384 | `cap+itan` |  | 2 |
| morphbpe@6080 | `cap+itan` |  | 2 |
| morphbpe@8192 | `cap+itan` |  | 2 |
| morphbpe@16384 | `cap+itan` |  | 2 |
| penalty-1@6080 | `capit+an` |  | 2 |
| penalty-1@8192 | `capit+an` |  | 2 |
| penalty-1@16384 | `capit+an` |  | 2 |
| penalty-2@6080 | `capit+an` |  | 2 |
| penalty-2@8192 | `capit+an` |  | 2 |
| penalty-2@16384 | `capit+an` |  | 2 |
| penalty-4@6080 | `cap+itan` |  | 2 |
| penalty-4@8192 | `cap+itan` |  | 2 |
| penalty-4@16384 | `cap+itan` |  | 2 |
| penalty-8@6080 | `capit+an` |  | 2 |
| penalty-8@8192 | `capit+an` |  | 2 |
| penalty-8@16384 | `capit+an` |  | 2 |
| stochastic-p4-d0.1@6080 | `capit+an` |  | 2 |
| stochastic-p4-d0.1@8192 | `capit+an` |  | 2 |
| stochastic-p4-d0.1@16384 | `capit+an` |  | 2 |
| stochastic-p4-d0.2@6080 | `capit+an` |  | 2 |
| stochastic-p4-d0.2@8192 | `capit+an` |  | 2 |
| stochastic-p4-d0.2@16384 | `capit+an` |  | 2 |
| unigram-ablation@6080 | `cap+itan` |  | 2 |

## `kekaban`  (suffixation, tier B_moderate_silver)

**silver gold:** `kekab+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `keka+ban` |  | 2 |
| plain@8192 | `keka+ban` |  | 2 |
| plain@16384 | `kekaban` |  | 1 |
| morphbpe@6080 | `keka+ban` |  | 2 |
| morphbpe@8192 | `keka+ban` |  | 2 |
| morphbpe@16384 | `kekaban` |  | 1 |
| penalty-1@6080 | `keka+ban` |  | 2 |
| penalty-1@8192 | `keka+ban` |  | 2 |
| penalty-1@16384 | `kekaban` |  | 1 |
| penalty-2@6080 | `keka+ban` |  | 2 |
| penalty-2@8192 | `keka+ban` |  | 2 |
| penalty-2@16384 | `kekaban` |  | 1 |
| penalty-4@6080 | `keka+ban` |  | 2 |
| penalty-4@8192 | `keka+ban` |  | 2 |
| penalty-4@16384 | `kekaban` |  | 1 |
| penalty-8@6080 | `keka+ban` |  | 2 |
| penalty-8@8192 | `keka+ban` |  | 2 |
| penalty-8@16384 | `kekaban` |  | 1 |
| stochastic-p4-d0.1@6080 | `keka+ban` |  | 2 |
| stochastic-p4-d0.1@8192 | `keka+ban` |  | 2 |
| stochastic-p4-d0.1@16384 | `kekaban` |  | 1 |
| stochastic-p4-d0.2@6080 | `keka+ban` |  | 2 |
| stochastic-p4-d0.2@8192 | `keka+ban` |  | 2 |
| stochastic-p4-d0.2@16384 | `kekaban` |  | 1 |
| unigram-ablation@6080 | `keka+ban` |  | 2 |

## `kelinguan`  (suffixation, tier B_moderate_silver)

**silver gold:** `kelingu+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kel+inguan` |  | 2 |
| plain@8192 | `kel+inguan` |  | 2 |
| plain@16384 | `kelinguan` |  | 1 |
| morphbpe@6080 | `kel+ing+uan` |  | 3 |
| morphbpe@8192 | `kel+ing+uan` |  | 3 |
| morphbpe@16384 | `kelinguan` |  | 1 |
| penalty-1@6080 | `kel+ing+uan` |  | 3 |
| penalty-1@8192 | `kel+ing+uan` |  | 3 |
| penalty-1@16384 | `kelinguan` |  | 1 |
| penalty-2@6080 | `kel+ing+uan` |  | 3 |
| penalty-2@8192 | `kel+ing+uan` |  | 3 |
| penalty-2@16384 | `kelinguan` |  | 1 |
| penalty-4@6080 | `ke+ling+uan` |  | 3 |
| penalty-4@8192 | `ke+ling+uan` |  | 3 |
| penalty-4@16384 | `kelinguan` |  | 1 |
| penalty-8@6080 | `ke+linguan` |  | 2 |
| penalty-8@8192 | `ke+linguan` |  | 2 |
| penalty-8@16384 | `kelinguan` |  | 1 |
| stochastic-p4-d0.1@6080 | `ke+li+ng+uan` |  | 4 |
| stochastic-p4-d0.1@8192 | `ke+li+ng+uan` |  | 4 |
| stochastic-p4-d0.1@16384 | `kelinguan` |  | 1 |
| stochastic-p4-d0.2@6080 | `ke+li+ng+uan` |  | 4 |
| stochastic-p4-d0.2@8192 | `ke+li+ng+uan` |  | 4 |
| stochastic-p4-d0.2@16384 | `kelinguan` |  | 1 |
| unigram-ablation@6080 | `ke+ling+uan` |  | 3 |

## `nanuman`  (suffixation, tier B_moderate_silver)

**silver gold:** `nanum+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `nanuman` |  | 1 |
| plain@8192 | `nanuman` |  | 1 |
| plain@16384 | `nanuman` |  | 1 |
| morphbpe@6080 | `nanuman` |  | 1 |
| morphbpe@8192 | `nanuman` |  | 1 |
| morphbpe@16384 | `nanuman` |  | 1 |
| penalty-1@6080 | `nanuman` |  | 1 |
| penalty-1@8192 | `nanuman` |  | 1 |
| penalty-1@16384 | `nanuman` |  | 1 |
| penalty-2@6080 | `nanuman` |  | 1 |
| penalty-2@8192 | `nanuman` |  | 1 |
| penalty-2@16384 | `nanuman` |  | 1 |
| penalty-4@6080 | `nanuman` |  | 1 |
| penalty-4@8192 | `nanuman` |  | 1 |
| penalty-4@16384 | `nanuman` |  | 1 |
| penalty-8@6080 | `nanuman` |  | 1 |
| penalty-8@8192 | `nanuman` |  | 1 |
| penalty-8@16384 | `nanuman` |  | 1 |
| stochastic-p4-d0.1@6080 | `nanuman` |  | 1 |
| stochastic-p4-d0.1@8192 | `nanuman` |  | 1 |
| stochastic-p4-d0.1@16384 | `nanuman` |  | 1 |
| stochastic-p4-d0.2@6080 | `nanuman` |  | 1 |
| stochastic-p4-d0.2@8192 | `nanuman` |  | 1 |
| stochastic-p4-d0.2@16384 | `nanuman` |  | 1 |
| unigram-ablation@6080 | `nanuman` |  | 1 |

## `pilan`  (suffixation, tier B_moderate_silver)

**silver gold:** `pil+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `pilan` |  | 1 |
| plain@8192 | `pilan` |  | 1 |
| plain@16384 | `pilan` |  | 1 |
| morphbpe@6080 | `pilan` |  | 1 |
| morphbpe@8192 | `pilan` |  | 1 |
| morphbpe@16384 | `pilan` |  | 1 |
| penalty-1@6080 | `pilan` |  | 1 |
| penalty-1@8192 | `pilan` |  | 1 |
| penalty-1@16384 | `pilan` |  | 1 |
| penalty-2@6080 | `pilan` |  | 1 |
| penalty-2@8192 | `pilan` |  | 1 |
| penalty-2@16384 | `pilan` |  | 1 |
| penalty-4@6080 | `pilan` |  | 1 |
| penalty-4@8192 | `pilan` |  | 1 |
| penalty-4@16384 | `pilan` |  | 1 |
| penalty-8@6080 | `pilan` |  | 1 |
| penalty-8@8192 | `pilan` |  | 1 |
| penalty-8@16384 | `pilan` |  | 1 |
| stochastic-p4-d0.1@6080 | `pilan` |  | 1 |
| stochastic-p4-d0.1@8192 | `pilan` |  | 1 |
| stochastic-p4-d0.1@16384 | `pilan` |  | 1 |
| stochastic-p4-d0.2@6080 | `pilan` |  | 1 |
| stochastic-p4-d0.2@8192 | `pilan` |  | 1 |
| stochastic-p4-d0.2@16384 | `pilan` |  | 1 |
| unigram-ablation@6080 | `pilan` |  | 1 |

## `sibukan`  (suffixation, tier B_moderate_silver)

**silver gold:** `sibuk+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `sib+ukan` |  | 2 |
| plain@8192 | `sib+ukan` |  | 2 |
| plain@16384 | `sibukan` |  | 1 |
| morphbpe@6080 | `sib+ukan` |  | 2 |
| morphbpe@8192 | `sib+ukan` |  | 2 |
| morphbpe@16384 | `sibukan` |  | 1 |
| penalty-1@6080 | `sib+ukan` |  | 2 |
| penalty-1@8192 | `sib+ukan` |  | 2 |
| penalty-1@16384 | `sibukan` |  | 1 |
| penalty-2@6080 | `sib+uk+an` |  | 3 |
| penalty-2@8192 | `sib+ukan` |  | 2 |
| penalty-2@16384 | `sibukan` |  | 1 |
| penalty-4@6080 | `sib+u+kan` |  | 3 |
| penalty-4@8192 | `sib+ukan` |  | 2 |
| penalty-4@16384 | `sibukan` |  | 1 |
| penalty-8@6080 | `si+bukan` |  | 2 |
| penalty-8@8192 | `si+bukan` |  | 2 |
| penalty-8@16384 | `sibukan` |  | 1 |
| stochastic-p4-d0.1@6080 | `sibu+kan` |  | 2 |
| stochastic-p4-d0.1@8192 | `sibu+kan` |  | 2 |
| stochastic-p4-d0.1@16384 | `sibukan` |  | 1 |
| stochastic-p4-d0.2@6080 | `sibu+kan` |  | 2 |
| stochastic-p4-d0.2@8192 | `sibu+kan` |  | 2 |
| stochastic-p4-d0.2@16384 | `sibukan` |  | 1 |
| unigram-ablation@6080 | `s+ibukan` |  | 2 |

## `bamban`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `bamban`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `b+amban` |  | 2 |
| plain@8192 | `b+amban` |  | 2 |
| plain@16384 | `b+amban` |  | 2 |
| morphbpe@6080 | `b+amban` |  | 2 |
| morphbpe@8192 | `b+amban` |  | 2 |
| morphbpe@16384 | `b+amban` |  | 2 |
| penalty-1@6080 | `b+amban` |  | 2 |
| penalty-1@8192 | `b+amban` |  | 2 |
| penalty-1@16384 | `b+amban` |  | 2 |
| penalty-2@6080 | `b+amban` |  | 2 |
| penalty-2@8192 | `b+amban` |  | 2 |
| penalty-2@16384 | `b+amban` |  | 2 |
| penalty-4@6080 | `b+amban` |  | 2 |
| penalty-4@8192 | `b+amban` |  | 2 |
| penalty-4@16384 | `b+amban` |  | 2 |
| penalty-8@6080 | `b+amban` |  | 2 |
| penalty-8@8192 | `b+amban` |  | 2 |
| penalty-8@16384 | `b+amban` |  | 2 |
| stochastic-p4-d0.1@6080 | `b+amban` |  | 2 |
| stochastic-p4-d0.1@8192 | `b+amban` |  | 2 |
| stochastic-p4-d0.1@16384 | `b+amban` |  | 2 |
| stochastic-p4-d0.2@6080 | `b+amban` |  | 2 |
| stochastic-p4-d0.2@8192 | `b+amban` |  | 2 |
| stochastic-p4-d0.2@16384 | `b+amban` |  | 2 |
| unigram-ablation@6080 | `ba+m+ban` |  | 3 |

## `bayaran`  (suffixation, tier B_moderate_silver)

**silver gold:** `bayar+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `bay+aran` |  | 2 |
| plain@8192 | `bay+aran` |  | 2 |
| plain@16384 | `bayaran` |  | 1 |
| morphbpe@6080 | `bay+aran` |  | 2 |
| morphbpe@8192 | `bay+aran` |  | 2 |
| morphbpe@16384 | `bayaran` |  | 1 |
| penalty-1@6080 | `baya+ran` |  | 2 |
| penalty-1@8192 | `baya+ran` |  | 2 |
| penalty-1@16384 | `bayaran` |  | 1 |
| penalty-2@6080 | `baya+ran` |  | 2 |
| penalty-2@8192 | `baya+ran` |  | 2 |
| penalty-2@16384 | `bayaran` |  | 1 |
| penalty-4@6080 | `baya+ran` |  | 2 |
| penalty-4@8192 | `baya+ran` |  | 2 |
| penalty-4@16384 | `bayaran` |  | 1 |
| penalty-8@6080 | `baya+ran` |  | 2 |
| penalty-8@8192 | `baya+ran` |  | 2 |
| penalty-8@16384 | `bayaran` |  | 1 |
| stochastic-p4-d0.1@6080 | `baya+ran` |  | 2 |
| stochastic-p4-d0.1@8192 | `baya+ran` |  | 2 |
| stochastic-p4-d0.1@16384 | `bayaran` |  | 1 |
| stochastic-p4-d0.2@6080 | `baya+ran` |  | 2 |
| stochastic-p4-d0.2@8192 | `baya+ran` |  | 2 |
| stochastic-p4-d0.2@16384 | `bayaran` |  | 1 |
| unigram-ablation@6080 | `bayaran` |  | 1 |

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

## `kimutan`  (suffixation, tier A_strong_silver)

**silver gold:** `kimut+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `k+im+utan` |  | 3 |
| plain@8192 | `kim+utan` |  | 2 |
| plain@16384 | `kimutan` |  | 1 |
| morphbpe@6080 | `k+im+utan` |  | 3 |
| morphbpe@8192 | `k+im+utan` |  | 3 |
| morphbpe@16384 | `kim+utan` |  | 2 |
| penalty-1@6080 | `kimut+an` | OK | 2 |
| penalty-1@8192 | `kimut+an` | OK | 2 |
| penalty-1@16384 | `kimut+an` | OK | 2 |
| penalty-2@6080 | `kimut+an` | OK | 2 |
| penalty-2@8192 | `kimut+an` | OK | 2 |
| penalty-2@16384 | `kimut+an` | OK | 2 |
| penalty-4@6080 | `ki+mu+tan` |  | 3 |
| penalty-4@8192 | `ki+mu+tan` |  | 3 |
| penalty-4@16384 | `ki+mu+tan` |  | 3 |
| penalty-8@6080 | `ki+mu+tan` |  | 3 |
| penalty-8@8192 | `ki+mu+tan` |  | 3 |
| penalty-8@16384 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.1@6080 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.1@8192 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.1@16384 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.2@6080 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.2@8192 | `ki+mu+tan` |  | 3 |
| stochastic-p4-d0.2@16384 | `ki+mu+tan` |  | 3 |
| unigram-ablation@6080 | `kimut+an` | OK | 2 |

## `mipanuanan`  (suffixation, tier B_moderate_silver)

**silver gold:** `mipanuan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mip+anu+anan` |  | 3 |
| plain@8192 | `mip+anu+anan` |  | 3 |
| plain@16384 | `mipanu+anan` |  | 2 |
| morphbpe@6080 | `mipan+uanan` |  | 2 |
| morphbpe@8192 | `mipan+uanan` |  | 2 |
| morphbpe@16384 | `mipan+uanan` |  | 2 |
| penalty-1@6080 | `mipan+uanan` |  | 2 |
| penalty-1@8192 | `mipan+uanan` |  | 2 |
| penalty-1@16384 | `mipan+uanan` |  | 2 |
| penalty-2@6080 | `mipan+uanan` |  | 2 |
| penalty-2@8192 | `mipan+uanan` |  | 2 |
| penalty-2@16384 | `mipan+uanan` |  | 2 |
| penalty-4@6080 | `mi+pan+uanan` |  | 3 |
| penalty-4@8192 | `mipan+uanan` |  | 2 |
| penalty-4@16384 | `mipan+uanan` |  | 2 |
| penalty-8@6080 | `mi+panu+anan` |  | 3 |
| penalty-8@8192 | `mi+panu+anan` |  | 3 |
| penalty-8@16384 | `mi+panuanan` |  | 2 |
| stochastic-p4-d0.1@6080 | `mi+pan+uan+an` |  | 4 |
| stochastic-p4-d0.1@8192 | `mipan+uan+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `mipan+uanan` |  | 2 |
| stochastic-p4-d0.2@6080 | `mi+panu+anan` |  | 3 |
| stochastic-p4-d0.2@8192 | `mi+panu+anan` |  | 3 |
| stochastic-p4-d0.2@16384 | `mi+panu+anan` |  | 3 |
| unigram-ablation@6080 | `mi+pan+uanan` |  | 3 |

## `dasnan`  (suffixation, tier B_moderate_silver)

**silver gold:** `dasn+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `das+nan` |  | 2 |
| plain@8192 | `das+nan` |  | 2 |
| plain@16384 | `das+nan` |  | 2 |
| morphbpe@6080 | `das+nan` |  | 2 |
| morphbpe@8192 | `das+nan` |  | 2 |
| morphbpe@16384 | `dasnan` |  | 1 |
| penalty-1@6080 | `das+nan` |  | 2 |
| penalty-1@8192 | `das+nan` |  | 2 |
| penalty-1@16384 | `dasnan` |  | 1 |
| penalty-2@6080 | `das+nan` |  | 2 |
| penalty-2@8192 | `das+nan` |  | 2 |
| penalty-2@16384 | `dasnan` |  | 1 |
| penalty-4@6080 | `das+nan` |  | 2 |
| penalty-4@8192 | `das+nan` |  | 2 |
| penalty-4@16384 | `dasnan` |  | 1 |
| penalty-8@6080 | `das+nan` |  | 2 |
| penalty-8@8192 | `das+nan` |  | 2 |
| penalty-8@16384 | `dasnan` |  | 1 |
| stochastic-p4-d0.1@6080 | `das+nan` |  | 2 |
| stochastic-p4-d0.1@8192 | `das+nan` |  | 2 |
| stochastic-p4-d0.1@16384 | `dasnan` |  | 1 |
| stochastic-p4-d0.2@6080 | `das+nan` |  | 2 |
| stochastic-p4-d0.2@8192 | `das+nan` |  | 2 |
| stochastic-p4-d0.2@16384 | `dasnan` |  | 1 |
| unigram-ablation@6080 | `da+s+nan` |  | 3 |

## `degulan`  (suffixation, tier B_moderate_silver)

**silver gold:** `degul+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `de+g+ulan` |  | 3 |
| plain@8192 | `deg+ulan` |  | 2 |
| plain@16384 | `degulan` |  | 1 |
| morphbpe@6080 | `de+g+ulan` |  | 3 |
| morphbpe@8192 | `deg+ulan` |  | 2 |
| morphbpe@16384 | `degulan` |  | 1 |
| penalty-1@6080 | `de+g+ulan` |  | 3 |
| penalty-1@8192 | `deg+ulan` |  | 2 |
| penalty-1@16384 | `degulan` |  | 1 |
| penalty-2@6080 | `de+g+ulan` |  | 3 |
| penalty-2@8192 | `deg+ulan` |  | 2 |
| penalty-2@16384 | `degulan` |  | 1 |
| penalty-4@6080 | `de+gul+an` |  | 3 |
| penalty-4@8192 | `de+gul+an` |  | 3 |
| penalty-4@16384 | `degulan` |  | 1 |
| penalty-8@6080 | `de+g+ulan` |  | 3 |
| penalty-8@8192 | `deg+ulan` |  | 2 |
| penalty-8@16384 | `degulan` |  | 1 |
| stochastic-p4-d0.1@6080 | `de+gul+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `de+gul+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `degulan` |  | 1 |
| stochastic-p4-d0.2@6080 | `de+gul+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `de+gul+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `degulan` |  | 1 |
| unigram-ablation@6080 | `de+gul+an` |  | 3 |

## `haran`  (suffixation, tier B_moderate_silver)

**silver gold:** `har+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `h+aran` |  | 2 |
| plain@8192 | `h+aran` |  | 2 |
| plain@16384 | `h+aran` |  | 2 |
| morphbpe@6080 | `h+aran` |  | 2 |
| morphbpe@8192 | `h+aran` |  | 2 |
| morphbpe@16384 | `h+aran` |  | 2 |
| penalty-1@6080 | `h+aran` |  | 2 |
| penalty-1@8192 | `h+aran` |  | 2 |
| penalty-1@16384 | `h+aran` |  | 2 |
| penalty-2@6080 | `h+aran` |  | 2 |
| penalty-2@8192 | `h+aran` |  | 2 |
| penalty-2@16384 | `h+aran` |  | 2 |
| penalty-4@6080 | `h+aran` |  | 2 |
| penalty-4@8192 | `h+aran` |  | 2 |
| penalty-4@16384 | `h+aran` |  | 2 |
| penalty-8@6080 | `har+an` | OK | 2 |
| penalty-8@8192 | `har+an` | OK | 2 |
| penalty-8@16384 | `har+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `h+aran` |  | 2 |
| stochastic-p4-d0.1@8192 | `h+aran` |  | 2 |
| stochastic-p4-d0.1@16384 | `h+aran` |  | 2 |
| stochastic-p4-d0.2@6080 | `h+aran` |  | 2 |
| stochastic-p4-d0.2@8192 | `h+aran` |  | 2 |
| stochastic-p4-d0.2@16384 | `h+aran` |  | 2 |
| unigram-ablation@6080 | `har+an` | OK | 2 |

## `lasakan`  (suffixation, tier A_strong_silver)

**silver gold:** `lasak+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `las+akan` |  | 2 |
| plain@8192 | `las+akan` |  | 2 |
| plain@16384 | `las+akan` |  | 2 |
| morphbpe@6080 | `las+akan` |  | 2 |
| morphbpe@8192 | `las+akan` |  | 2 |
| morphbpe@16384 | `las+akan` |  | 2 |
| penalty-1@6080 | `las+akan` |  | 2 |
| penalty-1@8192 | `las+akan` |  | 2 |
| penalty-1@16384 | `las+akan` |  | 2 |
| penalty-2@6080 | `las+akan` |  | 2 |
| penalty-2@8192 | `las+akan` |  | 2 |
| penalty-2@16384 | `las+akan` |  | 2 |
| penalty-4@6080 | `lasa+kan` |  | 2 |
| penalty-4@8192 | `lasa+kan` |  | 2 |
| penalty-4@16384 | `lasa+kan` |  | 2 |
| penalty-8@6080 | `lasa+kan` |  | 2 |
| penalty-8@8192 | `lasa+kan` |  | 2 |
| penalty-8@16384 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.1@6080 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.1@8192 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.1@16384 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.2@6080 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.2@8192 | `lasa+kan` |  | 2 |
| stochastic-p4-d0.2@16384 | `lasa+kan` |  | 2 |
| unigram-ablation@6080 | `la+sak+an` |  | 3 |

## `talan`  (suffixation, tier A_strong_silver)

**silver gold:** `tal+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `t+alan` |  | 2 |
| plain@8192 | `talan` |  | 1 |
| plain@16384 | `talan` |  | 1 |
| morphbpe@6080 | `talan` |  | 1 |
| morphbpe@8192 | `talan` |  | 1 |
| morphbpe@16384 | `talan` |  | 1 |
| penalty-1@6080 | `talan` |  | 1 |
| penalty-1@8192 | `talan` |  | 1 |
| penalty-1@16384 | `talan` |  | 1 |
| penalty-2@6080 | `talan` |  | 1 |
| penalty-2@8192 | `talan` |  | 1 |
| penalty-2@16384 | `talan` |  | 1 |
| penalty-4@6080 | `talan` |  | 1 |
| penalty-4@8192 | `talan` |  | 1 |
| penalty-4@16384 | `talan` |  | 1 |
| penalty-8@6080 | `talan` |  | 1 |
| penalty-8@8192 | `talan` |  | 1 |
| penalty-8@16384 | `talan` |  | 1 |
| stochastic-p4-d0.1@6080 | `talan` |  | 1 |
| stochastic-p4-d0.1@8192 | `talan` |  | 1 |
| stochastic-p4-d0.1@16384 | `talan` |  | 1 |
| stochastic-p4-d0.2@6080 | `talan` |  | 1 |
| stochastic-p4-d0.2@8192 | `talan` |  | 1 |
| stochastic-p4-d0.2@16384 | `talan` |  | 1 |
| unigram-ablation@6080 | `talan` |  | 1 |

## `telanan`  (suffixation, tier B_moderate_silver)

**silver gold:** `telan+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `tel+anan` |  | 2 |
| plain@8192 | `tel+anan` |  | 2 |
| plain@16384 | `telanan` |  | 1 |
| morphbpe@6080 | `tel+anan` |  | 2 |
| morphbpe@8192 | `tel+anan` |  | 2 |
| morphbpe@16384 | `tel+anan` |  | 2 |
| penalty-1@6080 | `tel+anan` |  | 2 |
| penalty-1@8192 | `tel+anan` |  | 2 |
| penalty-1@16384 | `tel+anan` |  | 2 |
| penalty-2@6080 | `tel+anan` |  | 2 |
| penalty-2@8192 | `tel+anan` |  | 2 |
| penalty-2@16384 | `tel+anan` |  | 2 |
| penalty-4@6080 | `tel+anan` |  | 2 |
| penalty-4@8192 | `tel+anan` |  | 2 |
| penalty-4@16384 | `tel+anan` |  | 2 |
| penalty-8@6080 | `tel+anan` |  | 2 |
| penalty-8@8192 | `tel+anan` |  | 2 |
| penalty-8@16384 | `tel+anan` |  | 2 |
| stochastic-p4-d0.1@6080 | `te+lan+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `te+lan+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `te+lanan` |  | 2 |
| stochastic-p4-d0.2@6080 | `te+lan+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `te+lan+an` |  | 3 |
| stochastic-p4-d0.2@16384 | `te+lanan` |  | 2 |
| unigram-ablation@6080 | `te+lan+an` |  | 3 |

## `uvasan`  (suffixation, tier B_moderate_silver)

**silver gold:** `uvas+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `u+v+asan` |  | 3 |
| plain@8192 | `uv+asan` |  | 2 |
| plain@16384 | `uvasan` |  | 1 |
| morphbpe@6080 | `u+v+asan` |  | 3 |
| morphbpe@8192 | `uv+asan` |  | 2 |
| morphbpe@16384 | `uvasan` |  | 1 |
| penalty-1@6080 | `u+v+asan` |  | 3 |
| penalty-1@8192 | `u+v+asan` |  | 3 |
| penalty-1@16384 | `uvasan` |  | 1 |
| penalty-2@6080 | `u+v+asan` |  | 3 |
| penalty-2@8192 | `u+v+asan` |  | 3 |
| penalty-2@16384 | `uvasan` |  | 1 |
| penalty-4@6080 | `u+v+asan` |  | 3 |
| penalty-4@8192 | `u+v+asan` |  | 3 |
| penalty-4@16384 | `uvasan` |  | 1 |
| penalty-8@6080 | `u+vas+an` |  | 3 |
| penalty-8@8192 | `u+vas+an` |  | 3 |
| penalty-8@16384 | `uvasan` |  | 1 |
| stochastic-p4-d0.1@6080 | `u+v+asan` |  | 3 |
| stochastic-p4-d0.1@8192 | `u+v+asan` |  | 3 |
| stochastic-p4-d0.1@16384 | `uvasan` |  | 1 |
| stochastic-p4-d0.2@6080 | `u+v+asan` |  | 3 |
| stochastic-p4-d0.2@8192 | `uv+asan` |  | 2 |
| stochastic-p4-d0.2@16384 | `uvasan` |  | 1 |
| unigram-ablation@6080 | `u+va+san` |  | 3 |

## `akalingwan`  (suffixation, tier B_moderate_silver)

**silver gold:** `akalingw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `akal+ingwan` |  | 2 |
| plain@8192 | `akal+ingwan` |  | 2 |
| plain@16384 | `akal+ingwan` |  | 2 |
| morphbpe@6080 | `akal+ing+wan` |  | 3 |
| morphbpe@8192 | `akaling+wan` |  | 2 |
| morphbpe@16384 | `akalingwan` |  | 1 |
| penalty-1@6080 | `akal+ing+wan` |  | 3 |
| penalty-1@8192 | `akaling+wan` |  | 2 |
| penalty-1@16384 | `akalingwan` |  | 1 |
| penalty-2@6080 | `akal+ing+wan` |  | 3 |
| penalty-2@8192 | `akaling+wan` |  | 2 |
| penalty-2@16384 | `akalingwan` |  | 1 |
| penalty-4@6080 | `akal+ing+wan` |  | 3 |
| penalty-4@8192 | `akal+ing+wan` |  | 3 |
| penalty-4@16384 | `akalingwan` |  | 1 |
| penalty-8@6080 | `aka+lingwan` |  | 2 |
| penalty-8@8192 | `aka+lingwan` |  | 2 |
| penalty-8@16384 | `akalingwan` |  | 1 |
| stochastic-p4-d0.1@6080 | `aka+li+ng+wan` |  | 4 |
| stochastic-p4-d0.1@8192 | `aka+li+ng+wan` |  | 4 |
| stochastic-p4-d0.1@16384 | `akalingwan` |  | 1 |
| stochastic-p4-d0.2@6080 | `aka+li+ng+wan` |  | 4 |
| stochastic-p4-d0.2@8192 | `aka+li+ng+wan` |  | 4 |
| stochastic-p4-d0.2@16384 | `aka+li+ng+wan` |  | 4 |
| unigram-ablation@6080 | `a+kalingwan` |  | 2 |

## `albugan`  (suffixation, tier A_strong_silver)

**silver gold:** `albug+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `albugan` |  | 1 |
| plain@8192 | `albugan` |  | 1 |
| plain@16384 | `albugan` |  | 1 |
| morphbpe@6080 | `albugan` |  | 1 |
| morphbpe@8192 | `albugan` |  | 1 |
| morphbpe@16384 | `albugan` |  | 1 |
| penalty-1@6080 | `albugan` |  | 1 |
| penalty-1@8192 | `albugan` |  | 1 |
| penalty-1@16384 | `albugan` |  | 1 |
| penalty-2@6080 | `albugan` |  | 1 |
| penalty-2@8192 | `albugan` |  | 1 |
| penalty-2@16384 | `albugan` |  | 1 |
| penalty-4@6080 | `albugan` |  | 1 |
| penalty-4@8192 | `albugan` |  | 1 |
| penalty-4@16384 | `albugan` |  | 1 |
| penalty-8@6080 | `albugan` |  | 1 |
| penalty-8@8192 | `albugan` |  | 1 |
| penalty-8@16384 | `albugan` |  | 1 |
| stochastic-p4-d0.1@6080 | `albugan` |  | 1 |
| stochastic-p4-d0.1@8192 | `albugan` |  | 1 |
| stochastic-p4-d0.1@16384 | `albugan` |  | 1 |
| stochastic-p4-d0.2@6080 | `albugan` |  | 1 |
| stochastic-p4-d0.2@8192 | `albugan` |  | 1 |
| stochastic-p4-d0.2@16384 | `albugan` |  | 1 |
| unigram-ablation@6080 | `albugan` |  | 1 |

## `atbusan`  (suffixation, tier A_strong_silver)

**silver gold:** `atbus+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `at+b+usan` |  | 3 |
| plain@8192 | `at+b+usan` |  | 3 |
| plain@16384 | `at+busan` |  | 2 |
| morphbpe@6080 | `at+bus+an` |  | 3 |
| morphbpe@8192 | `atbus+an` | OK | 2 |
| morphbpe@16384 | `atbus+an` | OK | 2 |
| penalty-1@6080 | `at+bus+an` |  | 3 |
| penalty-1@8192 | `atbus+an` | OK | 2 |
| penalty-1@16384 | `atbus+an` | OK | 2 |
| penalty-2@6080 | `at+bus+an` |  | 3 |
| penalty-2@8192 | `atbus+an` | OK | 2 |
| penalty-2@16384 | `atbus+an` | OK | 2 |
| penalty-4@6080 | `at+bus+an` |  | 3 |
| penalty-4@8192 | `atbus+an` | OK | 2 |
| penalty-4@16384 | `atbus+an` | OK | 2 |
| penalty-8@6080 | `at+bus+an` |  | 3 |
| penalty-8@8192 | `atbus+an` | OK | 2 |
| penalty-8@16384 | `atbus+an` | OK | 2 |
| stochastic-p4-d0.1@6080 | `at+bus+an` |  | 3 |
| stochastic-p4-d0.1@8192 | `at+bus+an` |  | 3 |
| stochastic-p4-d0.1@16384 | `atbus+an` | OK | 2 |
| stochastic-p4-d0.2@6080 | `at+bus+an` |  | 3 |
| stochastic-p4-d0.2@8192 | `atbus+an` | OK | 2 |
| stochastic-p4-d0.2@16384 | `atbus+an` | OK | 2 |
| unigram-ablation@6080 | `at+bus+an` |  | 3 |

## `camatayan`  (suffixation, tier F_conflicts_with_reconciliation_evidence)

**silver gold:** `ca+matay+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `c+amat+ayan` |  | 3 |
| plain@8192 | `camat+ayan` |  | 2 |
| plain@16384 | `camatayan` |  | 1 |
| morphbpe@6080 | `c+amat+ayan` |  | 3 |
| morphbpe@8192 | `c+amatayan` |  | 2 |
| morphbpe@16384 | `camatayan` |  | 1 |
| penalty-1@6080 | `c+amat+ayan` |  | 3 |
| penalty-1@8192 | `c+amatayan` |  | 2 |
| penalty-1@16384 | `camatayan` |  | 1 |
| penalty-2@6080 | `c+amat+ayan` |  | 3 |
| penalty-2@8192 | `c+amatayan` |  | 2 |
| penalty-2@16384 | `camatayan` |  | 1 |
| penalty-4@6080 | `c+amat+ayan` |  | 3 |
| penalty-4@8192 | `camatayan` |  | 1 |
| penalty-4@16384 | `camatayan` |  | 1 |
| penalty-8@6080 | `cam+ata+yan` |  | 3 |
| penalty-8@8192 | `camatayan` |  | 1 |
| penalty-8@16384 | `camatayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `cam+ata+yan` |  | 3 |
| stochastic-p4-d0.1@8192 | `cam+atayan` |  | 2 |
| stochastic-p4-d0.1@16384 | `camatayan` |  | 1 |
| stochastic-p4-d0.2@6080 | `cam+at+ayan` |  | 3 |
| stochastic-p4-d0.2@8192 | `cam+at+ayan` |  | 3 |
| stochastic-p4-d0.2@16384 | `camatayan` |  | 1 |
| unigram-ablation@6080 | `camatayan` |  | 1 |

## `kibkuban`  (suffixation, tier B_moderate_silver)

**silver gold:** `kibkub+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `k+ib+ku+ban` |  | 4 |
| plain@8192 | `k+ib+ku+ban` |  | 4 |
| plain@16384 | `kib+kuban` |  | 2 |
| morphbpe@6080 | `k+ib+ku+ban` |  | 4 |
| morphbpe@8192 | `k+ib+ku+ban` |  | 4 |
| morphbpe@16384 | `kib+kuban` |  | 2 |
| penalty-1@6080 | `k+ib+ku+ban` |  | 4 |
| penalty-1@8192 | `k+ib+ku+ban` |  | 4 |
| penalty-1@16384 | `kib+kuban` |  | 2 |
| penalty-2@6080 | `k+ib+ku+ban` |  | 4 |
| penalty-2@8192 | `k+ib+ku+ban` |  | 4 |
| penalty-2@16384 | `kib+kuban` |  | 2 |
| penalty-4@6080 | `k+ib+ku+ban` |  | 4 |
| penalty-4@8192 | `k+ib+ku+ban` |  | 4 |
| penalty-4@16384 | `kib+kuban` |  | 2 |
| penalty-8@6080 | `ki+b+ku+ban` |  | 4 |
| penalty-8@8192 | `ki+b+ku+ban` |  | 4 |
| penalty-8@16384 | `kib+kuban` |  | 2 |
| stochastic-p4-d0.1@6080 | `ki+b+ku+ban` |  | 4 |
| stochastic-p4-d0.1@8192 | `ki+b+ku+ban` |  | 4 |
| stochastic-p4-d0.1@16384 | `kib+kuban` |  | 2 |
| stochastic-p4-d0.2@6080 | `ki+b+ku+ban` |  | 4 |
| stochastic-p4-d0.2@8192 | `ki+b+ku+ban` |  | 4 |
| stochastic-p4-d0.2@16384 | `ki+b+kuban` |  | 3 |
| unigram-ablation@6080 | `ki+b+ku+ban` |  | 4 |

## `kundiman`  (suffixation, tier B_moderate_silver)

**silver gold:** `kundim+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kund+i+man` |  | 3 |
| plain@8192 | `kund+iman` |  | 2 |
| plain@16384 | `kund+iman` |  | 2 |
| morphbpe@6080 | `kun+di+man` |  | 3 |
| morphbpe@8192 | `kun+di+man` |  | 3 |
| morphbpe@16384 | `kun+diman` |  | 2 |
| penalty-1@6080 | `kun+di+man` |  | 3 |
| penalty-1@8192 | `kun+di+man` |  | 3 |
| penalty-1@16384 | `kun+diman` |  | 2 |
| penalty-2@6080 | `kun+di+man` |  | 3 |
| penalty-2@8192 | `kun+di+man` |  | 3 |
| penalty-2@16384 | `kun+diman` |  | 2 |
| penalty-4@6080 | `kun+di+man` |  | 3 |
| penalty-4@8192 | `kun+di+man` |  | 3 |
| penalty-4@16384 | `kun+diman` |  | 2 |
| penalty-8@6080 | `kundi+man` |  | 2 |
| penalty-8@8192 | `kundi+man` |  | 2 |
| penalty-8@16384 | `kundi+man` |  | 2 |
| stochastic-p4-d0.1@6080 | `kun+di+man` |  | 3 |
| stochastic-p4-d0.1@8192 | `kun+di+man` |  | 3 |
| stochastic-p4-d0.1@16384 | `kun+di+man` |  | 3 |
| stochastic-p4-d0.2@6080 | `kun+di+man` |  | 3 |
| stochastic-p4-d0.2@8192 | `kun+di+man` |  | 3 |
| stochastic-p4-d0.2@16384 | `kun+di+man` |  | 3 |
| unigram-ablation@6080 | `kundi+man` |  | 2 |

## `kwayan`  (suffixation, tier B_moderate_silver)

**silver gold:** `kway+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `kw+ayan` |  | 2 |
| plain@8192 | `kw+ayan` |  | 2 |
| plain@16384 | `kw+ayan` |  | 2 |
| morphbpe@6080 | `kw+ayan` |  | 2 |
| morphbpe@8192 | `kw+ayan` |  | 2 |
| morphbpe@16384 | `kw+ayan` |  | 2 |
| penalty-1@6080 | `kw+ayan` |  | 2 |
| penalty-1@8192 | `kw+ayan` |  | 2 |
| penalty-1@16384 | `kw+ayan` |  | 2 |
| penalty-2@6080 | `kw+ayan` |  | 2 |
| penalty-2@8192 | `kw+ayan` |  | 2 |
| penalty-2@16384 | `kw+ayan` |  | 2 |
| penalty-4@6080 | `kw+ayan` |  | 2 |
| penalty-4@8192 | `kw+ayan` |  | 2 |
| penalty-4@16384 | `kwayan` |  | 1 |
| penalty-8@6080 | `k+wayan` |  | 2 |
| penalty-8@8192 | `k+wayan` |  | 2 |
| penalty-8@16384 | `kwayan` |  | 1 |
| stochastic-p4-d0.1@6080 | `kwa+yan` |  | 2 |
| stochastic-p4-d0.1@8192 | `kwa+yan` |  | 2 |
| stochastic-p4-d0.1@16384 | `kwa+yan` |  | 2 |
| stochastic-p4-d0.2@6080 | `k+wa+yan` |  | 3 |
| stochastic-p4-d0.2@8192 | `k+wa+yan` |  | 3 |
| stochastic-p4-d0.2@16384 | `k+wayan` |  | 2 |
| unigram-ablation@6080 | `k+wayan` |  | 2 |

## `lakwan`  (suffixation, tier B_moderate_silver)

**silver gold:** `lakw+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `lak+wan` |  | 2 |
| plain@8192 | `lak+wan` |  | 2 |
| plain@16384 | `lakwan` |  | 1 |
| morphbpe@6080 | `lak+wan` |  | 2 |
| morphbpe@8192 | `lakwan` |  | 1 |
| morphbpe@16384 | `lakwan` |  | 1 |
| penalty-1@6080 | `lak+wan` |  | 2 |
| penalty-1@8192 | `lakwan` |  | 1 |
| penalty-1@16384 | `lakwan` |  | 1 |
| penalty-2@6080 | `lak+wan` |  | 2 |
| penalty-2@8192 | `lakwan` |  | 1 |
| penalty-2@16384 | `lakwan` |  | 1 |
| penalty-4@6080 | `lak+wan` |  | 2 |
| penalty-4@8192 | `lakwan` |  | 1 |
| penalty-4@16384 | `lakwan` |  | 1 |
| penalty-8@6080 | `lakwan` |  | 1 |
| penalty-8@8192 | `lakwan` |  | 1 |
| penalty-8@16384 | `lakwan` |  | 1 |
| stochastic-p4-d0.1@6080 | `lak+wan` |  | 2 |
| stochastic-p4-d0.1@8192 | `lakwan` |  | 1 |
| stochastic-p4-d0.1@16384 | `lakwan` |  | 1 |
| stochastic-p4-d0.2@6080 | `lak+wan` |  | 2 |
| stochastic-p4-d0.2@8192 | `lakwan` |  | 1 |
| stochastic-p4-d0.2@16384 | `lakwan` |  | 1 |
| unigram-ablation@6080 | `lakwan` |  | 1 |

## `likuan`  (suffixation, tier B_moderate_silver)

**silver gold:** `liku+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `likuan` |  | 1 |
| plain@8192 | `likuan` |  | 1 |
| plain@16384 | `likuan` |  | 1 |
| morphbpe@6080 | `likuan` |  | 1 |
| morphbpe@8192 | `likuan` |  | 1 |
| morphbpe@16384 | `likuan` |  | 1 |
| penalty-1@6080 | `likuan` |  | 1 |
| penalty-1@8192 | `likuan` |  | 1 |
| penalty-1@16384 | `likuan` |  | 1 |
| penalty-2@6080 | `likuan` |  | 1 |
| penalty-2@8192 | `likuan` |  | 1 |
| penalty-2@16384 | `likuan` |  | 1 |
| penalty-4@6080 | `likuan` |  | 1 |
| penalty-4@8192 | `likuan` |  | 1 |
| penalty-4@16384 | `likuan` |  | 1 |
| penalty-8@6080 | `likuan` |  | 1 |
| penalty-8@8192 | `likuan` |  | 1 |
| penalty-8@16384 | `likuan` |  | 1 |
| stochastic-p4-d0.1@6080 | `likuan` |  | 1 |
| stochastic-p4-d0.1@8192 | `likuan` |  | 1 |
| stochastic-p4-d0.1@16384 | `likuan` |  | 1 |
| stochastic-p4-d0.2@6080 | `likuan` |  | 1 |
| stochastic-p4-d0.2@8192 | `likuan` |  | 1 |
| stochastic-p4-d0.2@16384 | `likuan` |  | 1 |
| unigram-ablation@6080 | `likuan` |  | 1 |

## `mirinan`  (suffixation, tier B_moderate_silver)

**silver gold:** `mirin+an`

| candidate | segmentation | == gold | n |
|---|---|:--:|--:|
| plain@6080 | `mirinan` |  | 1 |
| plain@8192 | `mirinan` |  | 1 |
| plain@16384 | `mirinan` |  | 1 |
| morphbpe@6080 | `mirinan` |  | 1 |
| morphbpe@8192 | `mirinan` |  | 1 |
| morphbpe@16384 | `mirinan` |  | 1 |
| penalty-1@6080 | `mirinan` |  | 1 |
| penalty-1@8192 | `mirinan` |  | 1 |
| penalty-1@16384 | `mirinan` |  | 1 |
| penalty-2@6080 | `mirinan` |  | 1 |
| penalty-2@8192 | `mirinan` |  | 1 |
| penalty-2@16384 | `mirinan` |  | 1 |
| penalty-4@6080 | `mirinan` |  | 1 |
| penalty-4@8192 | `mirinan` |  | 1 |
| penalty-4@16384 | `mirinan` |  | 1 |
| penalty-8@6080 | `mirinan` |  | 1 |
| penalty-8@8192 | `mirinan` |  | 1 |
| penalty-8@16384 | `mirinan` |  | 1 |
| stochastic-p4-d0.1@6080 | `mirinan` |  | 1 |
| stochastic-p4-d0.1@8192 | `mirinan` |  | 1 |
| stochastic-p4-d0.1@16384 | `mirinan` |  | 1 |
| stochastic-p4-d0.2@6080 | `mirinan` |  | 1 |
| stochastic-p4-d0.2@8192 | `mirinan` |  | 1 |
| stochastic-p4-d0.2@16384 | `mirinan` |  | 1 |
| unigram-ablation@6080 | `mirinan` |  | 1 |
