# Offset-540 Early-τ4 / Late-τ3 Dual Markers — RC15–RC17

**Date:** 2026-07-11  
**Job:** `offset-540-structural-audit`  
**Status:** residual audit holds; not theorem

## Executive Summary

On segment utilization maxima through `4e8–5e8` and the full `o_q ∈ {2,4,6}`
branch-max panel:

- **RC15 / P19 (late-τ3 trail tightness) holds.**  
  `trail_gap = D − last_τ4 ∈ [2, 20] ⊆ [1, 24]`.
- **RC16 / P20 (absolute early τ4 on full panel) holds.**  
  `first_τ4 ∈ [2, 16]` so `first_τ4 ≤ 16` on util maxima **and** o_q panel.
- **RC17 / P21 (near-540 dual marker) holds** as a conditional residual.  
  On the 4 rows with `|D − 540| ≤ 20`: `first_τ4 ≤ 10` and `trail_gap ≤ 20`.

Fixed near-540 band on utilization maxima (**RC2**) remains **falsified**
(`D = 738` at the `4e8–5e8` util max). d=4 SDA transfer is not revived.

Theorem status: **Prime-Square Proximity Theorem is proved** in `PROOF.md`.
This probe is residual chamber-structure audit only.

## Prediction Table

| ID | Prediction | Surface | Status |
| --- | --- | --- | --- |
| P19 | `1 ≤ D − last_τ4 ≤ 24` | util maxima + o_q panel | holds |
| P20 | `first_τ4 ≤ 16` | util maxima + o_q panel | holds |
| P21 | if `\|D−540\|≤20` then `first_τ4≤10` and trail `≤20` | conditional | holds |

## Residual Claims

| ID | Claim | Status |
| --- | --- | --- |
| RC15 | Late-τ3 trail tightness | holds |
| RC16 | Absolute early τ4 on full panel (tightens RC4 util-only ≤20) | holds |
| RC17 | Near-540 dual early/late marker (conditional residual) | holds |
| RC2 | Fixed near-540 band on util maxima is a law | **falsified (retained)** |
| RC12–RC14 | Quartile mass / median mid-band | retained holds |

## Key Numbers

| Quantity | Value |
| --- | --- |
| trail_gap range (all rows) | `[2, 20]` |
| first_τ4 range (all rows) | `[2, 16]` |
| near-540 row count | `4` |
| near-540 trail range | `[8, 20]` |
| near-540 first_τ4 range | `[4, 10]` |
| util-max escape row | `r=424,171,123`, `D=738`, `o_q=6` |

## Structural Reading

Early τ=4 opens the chamber; late τ=3 closes it at the selected square
endpoint. The trail between last τ4 support and `D` is short on every
evaluated extremal. When the recurring-540 band reappears, both the early
marker and the late trail tighten. Escape from 540 on the util max does not
break trail tightness or early opening.

## Reproduce / Falsify

```text
python3 experiments/square-branch-hourly-2026-07-11-rc15/offset_540_residual_rc15_probe.py
```

Inputs:

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Residual RC15–RC17 | measured holds; audit only |
| Residual RC2 fixed band | falsified |
| Invalidated d=4 SDA | remains invalidated |
