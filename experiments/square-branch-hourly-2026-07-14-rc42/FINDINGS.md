# Offset-540 Structural Audit: RC42-RC44 (Interior Tau4 Packing)

**Date:** 2026-07-14
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure:

1. How small the tightest successive Tau4 gap is relative to the median gap
   (packing floor).
2. How wide the interior spacing dynamic range is (`max_gap / min_gap`).
3. How large Dual L1 endpoint isolation is relative to the largest interior
   Tau4 desert (`dual_l1 / max_gap`).

Project terms: min/median (RC42), max/min (RC43), dual/max_gap (RC44).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- `min_over_median = min_gap / median_gap`
- `max_over_min = max_gap / min_gap`
- `dual_over_max_gap = dual_l1 / max_gap`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.
Not restated as primary surface: RC39-RC41 open/trail/dual median isolation.
Not used: body/median (algebraically `D/med - dual/med`).

## New residual claims

| ID | Claim | Bound | Observed (7 unique chambers) | Status |
| --- | --- | --- | --- | --- |
| RC42 / P46 | Floor packing min/med | `0.10 <= min/med <= 0.35` | range `[0.143, 0.250]` | holds |
| RC43 / P47 | Dynamic range max/min | `8 <= max/min <= 55` | range `[14, 44]` | holds |
| RC44 / P48 | Dual vs peak desert | `0.10 <= dual/max_gap <= 1.10` | range `[0.143, 0.923]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC39-RC41 (open/median, trail/median, dual/median) retained, not re-proved.
- RC42 bounds the **interior packing floor**, complementary to RC37 max/median.
- RC43 bounds **body spacing dynamic range**, independent of Dual endpoint ratios.
- RC44 scales Dual L1 by **peak interior desert**, distinct from dual/median (RC41)
  and dual/mean (RC29).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC39 table retained as prior Dual-median surface

## Branch-max panel snapshot

| o_q | r | D | min | max | med | dual | min/med | max/min | dual/max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 1 | 44 | 6 | 24 | ~0.167 | 44 | ~0.545 |
| 4 | 482342527 | 486 | 1 | 26 | 7 | 22 | ~0.143 | 26 | ~0.846 |
| 6 | 424171123 | 738 | 1 | 30 | 6 | 11 | ~0.167 | 30 | ~0.367 |

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-14-rc42/offset_540_residual_rc42_probe.py
```

## Next pressure

Queue falsification `5e8-6e8` and re-check RC42-RC44 (and RC18-RC41) on any
new util maximum. Do not promote min/median, max/min, or dual/max_gap to
theorem. Do not revive fixed band 540 or d=4 SDA.
