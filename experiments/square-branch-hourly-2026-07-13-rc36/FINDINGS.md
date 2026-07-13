# Offset-540 Structural Audit: RC36-RC38 (Open/Mean / Max/Med / IQR/Mean)

**Date:** 2026-07-13
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How many mean gaps fit into the opening run from the left prime to the first
   `tau = 4` hit (opening isolation only, not trail closing).
2. How tall the largest successive Tau4 desert is relative to the median gap
   (peak vs central scale, not vs mean).
3. How wide the middle half of successive gaps is relative to the mean gap
   (mean-relative robust scale, not median-relative IQR).

Project terms: open/mean (RC36), max/median (RC37), IQR/mean (RC38).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- mean inter-hit gap `(last - first) / (tau4_count - 1)`
- median successive gap
- `IQR = Q3 - Q1` of successive gaps (linear-interpolation percentiles)
- `open_over_mean = first_tau4 / mean_gap`
- `max_over_median = max_gap / median_gap`
- `iqr_over_mean = IQR / mean_gap`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC36 / P40 | Opening isolation / mean | `0.15 <= open/mean <= 2.00` | range `[0.223, 1.793]` | holds |
| RC37 / P41 | Peak successive gap / median | `2.50 <= max/med <= 8.00` | range `[3.143, 7.333]` | holds |
| RC38 / P42 | IQR scaled by mean | `0.50 <= IQR/mean <= 1.20` | range `[0.594, 1.065]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC33-RC35 (IQR/median, trail/mean, body last-quartile) retained, not
  re-proved.
- RC36 opens **opening isolation** in mean-gap units, distinct from trail
  closing isolation (RC34) and Dual L1 / mean (RC29).
- RC37 scales **peak successive gap by median**, distinct from max/mean (RC27).
- RC38 measures **IQR relative to mean**, distinct from IQR/median (RC33) and
  mean-based CV (RC28).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC33 table retained as prior surface

## Branch-max panel snapshot

| o_q | r | D | first | trail | open/mean | max/med | IQR/mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 4 | 20 | ~0.456 | ~7.333 | ~0.911 |
| 4 | 482342527 | 486 | 16 | 6 | ~1.793 | ~3.714 | ~1.065 |
| 6 | 424171123 | 738 | 3 | 8 | ~0.392 | ~5.000 | ~0.915 |

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc36/offset_540_residual_rc36_probe.py
```

## Next pressure

Queue falsification `5e8-6e8` and re-check RC36-RC38 (and RC18-RC35) on any
new util maximum. Do not promote open/mean, max/median, or IQR/mean to theorem.
Do not revive fixed band 540 or d=4 SDA.
