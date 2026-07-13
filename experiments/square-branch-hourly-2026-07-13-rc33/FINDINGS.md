# Offset-540 Structural Audit: RC33-RC35 (IQR Scale / Trail Mean-Units / Body Q4 Mass)

**Date:** 2026-07-13
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How wide the middle half of successive gaps is relative to the median gap
   (robust scale: IQR over median, not mean-based CV).
2. How many mean gaps fit into the trail from the last `tau = 4` hit to the
   late `tau = 3` endpoint (closing isolation only, not full Dual L1).
3. What share of Tau4 hits sit in the last quarter of the Tau4 **body**
   `[first_tau4, last_tau4]` (body-quartile mass, not D-quartile mass).

Project terms: successive IQR/median (RC33), trail/mean closing isolation
(RC34), body last-quartile mass (RC35).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- median successive gap
- `IQR = Q3 - Q1` of successive gaps (linear-interpolation percentiles)
- `iqr_over_median = IQR / median(gaps)`
- mean inter-hit gap `(last - first) / (tau4_count - 1)`
- `trail_over_mean = trail_gap / mean_gap`
- body Q3 cut `first_tau4 + 0.75 * (last_tau4 - first_tau4)`
- `last_body_quartile_frac = #{Tau4 hits with offset >= body Q3 cut} / tau4_count`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC33 / P37 | Tau4 successive IQR/median | `0.70 <= IQR/med <= 1.55` | range `[0.833, 1.417]` | holds |
| RC34 / P38 | Trail closing isolation / mean | `0.15 <= trail/mean <= 2.50` | range `[0.223, 2.278]` | holds |
| RC35 / P39 | Tau4 body last-quartile mass | `0.18 <= last_Q_frac <= 0.35` | range `[0.233, 0.297]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC30-RC32 (median/mean, sub-mean majority, body early-mass) retained, not
  re-proved.
- RC33 opens **robust gap scale**: IQR relative to median, distinct from
  mean-based CV (RC28) and from median/mean central skew (RC30).
- RC34 scales **trail alone** by mean gap (closing component), distinct from
  absolute trail tightness (RC19) and Dual L1 / mean (RC29).
- RC35 measures **body last-quartile mass** on `[first, last]` Tau4 support,
  distinct from D last-quarter mass (RC17), body-half early mass (RC32), and
  body support span (RC23).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC30 table retained as prior surface

## Branch-max panel snapshot

| o_q | r | D | trail | IQR/med | trail/mean | last_Q_frac |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 20 | ~1.333 | ~2.278 | ~0.233 |
| 4 | 482342527 | 486 | 6 | ~1.357 | ~0.672 | ~0.283 |
| 6 | 424171123 | 738 | 8 | ~1.167 | ~1.045 | ~0.240 |

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc33/offset_540_residual_rc33_probe.py
```

## Next pressure

Re-check RC33-RC35 (and RC18-RC32) on any new util maximum from `5e8-6e8`
dynamic-cutoff falsification. Do not promote IQR/median, trail/mean, or body
last-quartile mass to theorem. Do not revive fixed band 540 or d=4 SDA.
