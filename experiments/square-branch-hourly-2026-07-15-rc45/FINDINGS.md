# Offset-540 Structural Audit: RC45-RC47 (Mean-Floor / Dual-Per-Hit / Body Desert)

**Date:** 2026-07-15  
**Job id:** `offset-540-structural-audit`  
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How small the tightest successive Tau4 gap is relative to the **mean** gap
   (mean-unit packing floor).
2. How much Dual L1 isolation sits **per Tau4 hit** (mass-normalized Dual).
3. How large the peak successive desert is as a **share of Tau4 body span**
   between first and last Tau4.

Project terms: min/mean (RC45), dual/count (RC46), max/body (RC47).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- `min_over_mean = min_gap / mean_gap`
- `dual_per_hit = dual_l1 / tau4_count`
- `max_over_body = max_gap / tau4_body`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.  
Not restated as primary surface: RC42-RC44 min/median, max/min, dual/max_gap.  
Not used: open/max or trail/max (algebraic Dual split of RC44); dual/min
(collapses to absolute Dual L1 when min_gap = 1).

## New residual claims

| ID | Claim | Bound | Observed (7 unique chambers) | Status |
| --- | --- | --- | --- | --- |
| RC45 / P49 | Floor packing min/mean | `0.08 <= min/mean <= 0.30` | range `[0.112, 0.223]` | holds |
| RC46 / P50 | Dual L1 per Tau4 hit | `0.05 <= dual/count <= 0.50` | range `[0.077, 0.415]` | holds |
| RC47 / P51 | Peak desert / body span | `0.03 <= max/body <= 0.12` | range `[0.041, 0.085]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC42-RC44 (min/median, max/min, dual/max_gap) retained, not re-proved.
- RC45 places packing floor in **mean** units, complementary to RC42 (median).
- RC46 bounds Dual isolation **per hit**, distinct from dual/max_gap (RC44),
  dual/median (RC41), and hit density (RC21).
- RC47 scales peak desert by **Tau4 body support**, distinct from max/D (RC11)
  and max/min (RC43).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved. Residual holds do not empty `Annulus(r)` and do not force
`D(r) <= C_dyn(r)`.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC42 table retained as prior packing residual surface

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-15-rc45/offset_540_residual_rc45_probe.py
```

## Next pressure

Queue falsification `5e8-6e8` and re-check RC45-RC47 (and RC18-RC44) on any
new util maximum. Do not promote min/mean, dual/count, or max/body to theorem.
Do not revive fixed band 540 or d=4 SDA. Prefer holdout on a new band over
further ratio minting on the same 7 chambers.
