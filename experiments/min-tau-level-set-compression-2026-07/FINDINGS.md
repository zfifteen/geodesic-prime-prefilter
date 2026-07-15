# Findings: Min-tau Level-Set Compression Residual

**Date:** 2026-07-11  
**Status:** insight candidate + measured residual map. **Not a theorem.**  
**PROOF.md:** universal leftmost bound `w - p <= C(q)` is unchanged.

## Plain object

Start at a known prime `p`. Walk integers upward by exact divisor count `tau`.
Stop at the first `tau = 2`; that endpoint is the next prime `q`.

Inside the open gap, the GWR witness `w` is the **leftmost** integer with the
smallest divisor count. The proved bound controls only that leftmost offset:

```text
w - p <= C(q) = max(64, ceil(0.5 * log(q)^2))
```

Other interior integers can share the same minimal divisor count. Call that set
the **co-minimal level set** `L`, and call its rightmost member `w_R`.

## Core insight (hypothesis)

**Level-Set Compression Dichotomy (LSCD).**

1. **Full level-set compression (LSC)** would say every co-minimal sits inside
   the same Cramér window: `n - p <= C(q)` for all `n in L`.
2. LSC is **false** as a universal claim: late co-minimals can spill past
   `C(q)` while the leftmost witness stays deep inside the window.
3. On the measured regime, that spill is **not** free-form. It concentrates on
   one residual branch:
   - `tau(w) = 4` (dominant GWR branch),
   - early lock (`alpha = w - p` small; all spills had `alpha <= 6`),
   - multi-tie level set (`n_ties >= 2`, required for `w_R > w`).
4. Square branch (`tau(w) = 3`) and high-tau branches (`tau(w) >= 6`) showed
   **zero** spill on `11..2e6`.

Mechanism in ordinary language: the proved bound freezes the **first** min-tau
arrival. When the min level is the common `tau = 4` semiprime class and it
arrives early, the same low divisor load can reappear much later in a long
gap, past the witness cutoff window. Higher min levels and prime-square mins
did not produce that late reappearance on the tested surface.

## Relation to PROOF.md

| Object | Status in PROOF.md | Role here |
| --- | --- | --- |
| Direct next-prime (`tau=2` stop) | proved | builds `(p, q)` |
| GWR leftmost min-tau | proved | defines `w` and `L` |
| `w - p <= C(q)` | proved | leftmost only |
| Full level set inside `C(q)` | **not claimed** | LSC hypothesis, invalidated |
| Spill only on early `d=4` | **not claimed** | LSCD residual hypothesis |

This is a residual geometry **after** the three universal pillars, not a repair
of historical z≥4⇒g=2 claim and not a promotion of measured spill structure to theorem.

## Measured surface (local / mid scale only)

**Regime:** consecutive gaps with left prime `>= 11` and endpoint `q <= 2e6`.

| Quantity | Value |
| --- | ---: |
| Gaps scanned | 148928 |
| Spills (`w_R - p > C(q)`) | 17 |
| Global spill rate | ~0.000114 |
| Spills with `tau(w)=4` | 17 |
| Spills with `tau(w)=3` | 0 |
| Spills with `tau(w)>=6` | 0 |
| Leftmost theorem breaks | 0 |
| Max `alpha` among spills | 6 |
| Max right utilization ` (w_R-p)/C ` | ~1.325 |

Spill alpha histogram (all 17):

| `alpha = w-p` | count |
| ---: | ---: |
| 1 | 2 |
| 2 | 8 |
| 4 | 4 |
| 6 | 3 |

First spill row:

```text
p=31397  q=31469  g=72
w=31399  w_R=31466  tau(w)=4  n_ties=20
alpha=2  right_off=69  C=64  util_L=0.031  util_R=1.078
```

## Status labels (strict)

| Claim | Label |
| --- | --- |
| `w - p <= C(q)` for leftmost GWR | **theorem** (`PROOF.md`) |
| Full LSC for every co-minimal | **invalidated** on `11..2e6` |
| LSCD: spill only on `tau(w)=4` | **hypothesis**, measured hold on `11..2e6` |
| LSCD: no spill on square / high-tau | **hypothesis**, measured hold on `11..2e6` |
| Spill only when `alpha <= 6` | **hypothesis**, measured hold on `11..2e6` |
| Program-level verified / validated | **not claimed** (no executed `10^18` surface) |

## Prior-art separation

| Prior surface | Overlap | Difference |
| --- | --- | --- |
| historical z≥4⇒g=2 claim / residual A/B/C (`z>=4` classes) | modular zeros vs twin | here the residual is **co-minimal geometry vs `C(q)`**, not remainder zeros |
| Hypothesis U (unique + z4 => twin) | already invalidated | LSCD does not revive twin locks |
| CLHT / chamber-reset horizon | chamber tail envelopes | LSCD is consecutive-gap level-set vs proved cutoff |
| Square-branch utilization audits | high `util_L` on square | LSCD concerns **right** co-minimal utilization spill on **d=4** |

## Falsification rules (next pressure)

LSCD fails if any of the following appears on an extended regime:

1. A spill with `tau(w) = 3` (square branch).
2. A spill with `tau(w) >= 6`.
3. A spill with large early lock, e.g. `alpha > 32` while still `w_R - p > C(q)`.

LSC stays invalidated once one spill exists; do not revive full LSC without a
new statement.

## Repro

```bash
python3 -m pytest experiments/min-tau-level-set-compression-2026-07/test_level_set_compression_probe.py -q
python3 experiments/min-tau-level-set-compression-2026-07/level_set_compression_probe.py --q-max 2000000
```

Artifacts: `results_2e6_stratified.json`, `results_100000.json`,
`results_1000000.json`, and probe JSON under the same folder.

## What the Auditor / Verifier must check

1. No claim promotes LSCD to theorem or uses verified/validated language.
2. Leftmost bound remains theorem; spill language never demotes it.
3. Inference path is tau-scan + leftmost min; classical gates only if present
   as field prep, not as selectors.
4. Exact regime `11..2e6` is stated wherever measured hold is asserted.
5. Tests pass; repro command regenerates matching spill counts.
