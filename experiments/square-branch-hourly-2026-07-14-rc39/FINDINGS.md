# Offset-540 Structural Audit: RC39-RC41 (Dual Isolation / Median Units)

**Date:** 2026-07-14
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
ordered gaps between successive `tau = 4` hits. From those marks, measure how
many **median** successive Tau4 gaps fit into:

1. The opening run from the left prime to the first `tau = 4` hit
   (opening isolation only).
2. The trail from the last `tau = 4` hit to the late `tau = 3` endpoint
   (closing isolation only).
3. The Dual sum of opening and trail (combined Dual L1 isolation).

Project terms: open/median (RC39), trail/median (RC40), dual/median (RC41).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- successive inter-hit gaps on the ordered Tau4 set
- median successive gap
- `open_over_median = first_tau4 / median_gap`
- `trail_over_median = trail_gap / median_gap`
- `dual_over_median = dual_l1 / median_gap`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC39 / P43 | Opening isolation / median | `0.20 <= open/med <= 2.50` | range `[0.250, 2.286]` | holds |
| RC40 / P44 | Trail closing isolation / median | `0.20 <= trail/med <= 3.50` | range `[0.250, 3.333]` | holds |
| RC41 / P45 | Dual L1 isolation / median | `0.40 <= dual/med <= 4.50` | range `[0.500, 4.000]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

## Relation to prior residual surface

- RC36-RC38 (open/mean, max/med, IQR/mean) retained, not re-proved.
- RC39 scales **opening** by median, distinct from open/mean (RC36).
- RC40 scales **trail** by median, distinct from trail/mean (RC34).
- RC41 scales **Dual L1** by median, distinct from dual/mean (RC29).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC36 table retained as prior surface

## Branch-max panel snapshot

| o_q | r | D | first | trail | open/med | trail/med | dual/med |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 4 | 20 | ~0.667 | ~3.333 | ~4.000 |
| 4 | 482342527 | 486 | 16 | 6 | ~2.286 | ~0.857 | ~3.143 |
| 6 | 424171123 | 738 | 3 | 8 | ~0.500 | ~1.333 | ~1.833 |

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-14-rc39/offset_540_residual_rc39_probe.py
```

## Next pressure

Queue falsification `5e8-6e8` and re-check RC39-RC41 (and RC18-RC38) on any
new util maximum. Do not promote open/median, trail/median, or dual/median to
theorem. Do not revive fixed band 540 or d=4 SDA.
