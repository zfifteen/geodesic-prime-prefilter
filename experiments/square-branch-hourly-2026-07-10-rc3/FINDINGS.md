# Offset-540 Residual Claims RC3–RC5 — 2026-07-10

## Executive Summary

After the prior-hour death of the fixed near-540 band (RC2 / P6 on
`D(r)=738`), this hour formalizes the **next residual chamber structure**
as three falsifiable claims. None of these is a theorem. d=4 SDA is not
revived. Prime-Square Proximity remains **proved** in `PROOF.md`.

| ID | Claim | Status on surface through `4e8-5e8` |
| --- | --- | --- |
| RC3 | τ4 density `rho4 = tau4_count / D(r) ∈ [0.10, 0.14]` on segment util maxima | **holds** |
| RC4 | Absolute early chamber `first_tau4_offset ≤ 20` on segment util maxima | **holds** |
| RC5 | Local o_q=2 near-540 attractor `\|D−540\| ≤ 20` (not a law) | **holds** (one branch max) |
| RC2 | Fixed band `[528, 552]` on segment util maxima is a law | **falsified** (retained) |

## Prediction Table (new surface)

| ID | Prediction | Primary surface | Status |
| --- | --- | --- | --- |
| P7 | `0.10 ≤ rho4 ≤ 0.14` | 5/5 segment util maxima | holds |
| P8 | `first_tau4_offset ≤ 20` | 5/5 segment util maxima | holds |
| P9 | o_q=2 branch max has `\|D−540\| ≤ 20` | 1/1 (`D=542`) | holds |

## Primary Rows (with computed o_q)

| Segment | r | D(r) | o_q | rho4 | first τ4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `3e7-1e8` | 82,357,433 | 540 | 4 | 0.1167 | 10 |
| `1e8-2e8` | 102,017,779 | 462 | 4 | 0.1126 | 2 |
| `2e8-3e8` | 251,066,071 | 540 | 6 | 0.1111 | 6 |
| `3e8-4e8` | 358,018,553 | 546 | 4 | 0.1172 | 4 |
| `4e8-5e8` | 424,171,123 | 738 | 6 | 0.1301 | 3 |

Exact `D=540` appears at o_q ∈ {4, 6}. So near-540 is **not** exclusive to
o_q=2. RC5 only claims the o_q=2 *branch maximum* on `4e8-5e8` stays local
to 540 while the global util max escapes.

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Fixed-band residual RC2 | falsified (prior hour; retained) |
| New residual RC3–RC5 | measured holds; open as residual only |
| Invalidated d=4 SDA | remains invalidated |

## Falsify

```text
python3 experiments/square-branch-hourly-2026-07-10-rc3/offset_540_residual_rc3_probe.py
```

Inputs: prior chamber table
`experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`,
falsification summary `.../square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json`,
and `prefix_tau_floor_probe.json` (SDA-invalidation note only).
