# Offset-540 Structural Audit: RC30-RC32 (Median Shape / Sub-Mean / Body Mass)

**Date:** 2026-07-13
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How the **median** successive gap sits relative to the mean gap (central
   shape of the gap list, not the peak or the CV).
2. What fraction of successive gaps are at most the mean (sub-mean majority).
3. How Tau4 hits split across the first half of the Tau4 **body**
   `[first_tau4, last_tau4]` (body-half mass, not D-half mass).

Project terms: successive median/mean ratio (RC30), sub-mean gap majority
(RC31), body early-mass balance (RC32).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- mean inter-hit gap `(last - first) / (tau4_count - 1)`
- `median_over_mean = median(successive_gaps) / mean_gap`
- `frac_le_mean = #{g : g <= mean_gap} / #{gaps}`
- body midpoint `(first_tau4 + last_tau4) / 2`
- `early_body_frac = #{Tau4 hits with offset < body midpoint} / tau4_count`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC30 / P34 | Tau4 successive median/mean | `0.65 <= med/mean <= 0.95` | range `[0.683, 0.891]` | holds |
| RC31 / P35 | Sub-mean successive gap majority | `frac(g <= mean) >= 0.50` | range `[0.549, 0.677]` | holds |
| RC32 / P36 | Tau4 body early-mass balance | `0.40 <= early_body_frac <= 0.55` | range `[0.415, 0.538]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC27-RC29 (max/mean, gap CV, Dual isolation in mean-gap units) retained, not
  re-proved.
- RC30 opens **central gap shape**: median below mean (positive skew), not the
  peak ratio and not the CV envelope.
- RC31 bounds the **count share** of sub-mean successive steps (majority rule),
  distinct from mean envelope (RC24) and CV (RC28).
- RC32 measures **body-half mass balance** on `[first, last]` Tau4 support,
  distinct from early-half mass of the full chamber length D (RC9) and from
  quartile D-mass (RC12-RC13).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC27 table retained as prior surface

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc30/offset_540_residual_rc30_probe.py
```

## Next pressure

Re-check RC30-RC32 (and RC18-RC29) on any new util maximum from `5e8-6e8`
dynamic-cutoff falsification. Do not promote median/mean, sub-mean majority, or
body early-mass to theorem. Do not revive fixed band 540 or d=4 SDA.
