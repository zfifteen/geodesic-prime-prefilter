# Offset-540 Structural Audit: RC27-RC29 (Gap Regularity / Dual Isolation Units)

**Date:** 2026-07-13
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How large the biggest successive `tau = 4` gap is relative to the mean gap.
2. How variable the successive gaps are (coefficient of variation).
3. How many mean gaps fit into the Dual isolation `first_tau4 + trail_gap`.

Project terms: successive max/mean ratio (RC27), gap CV envelope (RC28), Dual
isolation in mean-gap units (RC29).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- mean inter-hit gap `(last - first) / (tau4_count - 1)`
- `max_over_mean = max_successive_gap / mean_gap`
- `gap_cv = pstdev(successive_gaps) / mean_gap`
- `dual_over_mean = dual_l1 / mean_gap`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC27 / P31 | Tau4 successive max/mean ratio | `max_gap / mean <= 5.5` | range `[2.605, 5.012]` | holds |
| RC28 / P32 | Tau4 successive gap CV | `0.55 <= CV <= 1.0` | range `[0.663, 0.891]` | holds |
| RC29 / P33 | Dual isolation in mean-gap units | `0.30 <= L1/mean <= 3.0` | range `[0.445, 2.744]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC24-RC26 (mean gap envelope, Dual signed imbalance, chamber open fraction)
  retained, not re-proved.
- RC27 opens **peak spacing regularity**: the largest successive gap is a
  bounded multiple of the mean, not an absolute gap bound.
- RC28 bounds **full-body spacing variability** via CV (not only the mean).
- RC29 scales Dual L1 by the body's mean spacing, so early/late isolation is
  read in the same units as Tau4 regularity (distinct from absolute Dual L1
  RC18 and signed component share RC25).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC24 table retained as prior surface

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py
```

## Next pressure

Re-check RC27-RC29 (and RC18-RC26) on any new util maximum from `5e8-6e8`
dynamic-cutoff falsification. Do not promote max/mean, CV, or Dual/mean to
theorem. Do not revive fixed band 540 or d=4 SDA.
