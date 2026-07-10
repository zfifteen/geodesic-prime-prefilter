# Offset-540 Residual Claims RC6–RC8 — 2026-07-10

## Executive Summary

After RC3–RC5 (τ4 density, absolute early τ4, o_q=2 local near-540 attractor),
this hour formalizes the **next residual chamber structure** on the full
`4e8–5e8` per-o_q branch-max panel. None of these is a theorem. d=4 SDA is not
revived. Fixed-band RC2 remains falsified. Prime-Square Proximity remains
**proved** in `PROOF.md`.

| ID | Claim | Status on surface through `4e8–5e8` |
| --- | --- | --- |
| RC6 | S2-A phase order on full o_q panel `{2,4,6}` | **holds** |
| RC7 | Late-dominant phase gap `(D − first_τ4)/D ≥ 0.95` on util max + o_q panel | **holds** |
| RC8 | Near-540 exclusivity: only o_q=2 branch max stays in `\|D−540\|≤20` | **holds** |
| RC2 | Fixed band `[528, 552]` on segment util maxima is a law | **falsified** (retained) |
| RC3–RC5 | Prior residual surface | **retained holds** (not primary surface) |

## Prediction Table (new surface)

| ID | Prediction | Primary surface | Status |
| --- | --- | --- | --- |
| P10 | `1 ≤ first_τ4 < first_τ3 = D(r)`, `prefix_min_τ=4`, `tau5=0` | 3/3 o_q branch maxima | holds |
| P11 | phase_gap ≥ 0.95 | 5 util maxima + 3 o_q rows | holds |
| P12 | only o_q=2 near 540 on branch-max panel | panel exclusivity | holds |

## 4e8–5e8 o_q Branch-Max Panel

| o_q | r | D(r) | first τ4 | phase_gap | \|D−540\| | near-540? |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 468,917,503 | 542 | 4 | 0.9926 | 2 | yes |
| 4 | 482,342,527 | 486 | 16 | 0.9671 | 54 | no (escapes) |
| 6 | 424,171,123 | 738 | 3 | 0.9959 | 198 | no (escapes) |

Minimum phase_gap on the evaluated surface (5 util maxima + 3 o_q rows) is
on the o_q=4 branch max (`0.9671 ≥ 0.95`).

RC8 strengthens RC5: near-540 is not only present on o_q=2, but **exclusive**
to o_q=2 among the three branch maxima on this segment. Exact `D=540` still
appears on non-o_q=2 *utilization* maxima in earlier segments; RC8 is
panel-exclusivity residual, not a universal offset law.

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Fixed-band residual RC2 | falsified (retained) |
| Prior residual RC3–RC5 | measured holds; retained |
| New residual RC6–RC8 | measured holds; open as residual only |
| Invalidated d=4 SDA | remains invalidated |

## Falsify

```text
python3 experiments/square-branch-hourly-2026-07-10-rc6/offset_540_residual_rc6_probe.py
```

Inputs: prior chamber table
`experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`,
RC3 table (retained note),
falsification summary `.../square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json`,
and `prefix_tau_floor_probe.json` (SDA-invalidation note only).
