# Offset-540 Structural Audit: RC48-RC50 (Multiset Occupancy / Desert Locus)

**Date:** 2026-07-16  
**Job id:** `offset-540-structural-audit`  
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, form the ordered list of successive gaps between those hits, then
measure:

1. How much of the gap multiset sits at the packing floor (`g ≤ 2`).
2. Where the largest successive desert sits on the Tau4 body (midpoint locus).
3. How much of the multiset is a large-desert tail (`g ≥ 2 · median`).

Project terms: tight_frac (RC48), desert_pos_frac (RC49), large_frac (RC50).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- ordered Tau4 set and successive gap multiset
- peak successive desert index `i*` (leftmost max)
- Dual markers retained as side labels only

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.  
Not restated as primary surface: RC45-RC47 min/mean, dual/count, max/body.  
Not used: affine renorms of the same envelope scalars alone.

## New residual claims

| ID | Claim | Bound | Observed (7 unique chambers) | Status |
| --- | --- | --- | --- | --- |
| RC48 / P52 | Tight-pair mass | `0.08 ≤ tight_frac ≤ 0.30` | range `[0.113, 0.231]` | holds |
| RC49 / P53 | Peak-desert body locus | `0.25 ≤ desert_pos ≤ 0.98` | range `[0.347, 0.933]` | holds |
| RC50 / P54 | Large-desert tail share | `0.08 ≤ large_frac ≤ 0.35` | range `[0.118, 0.288]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}`
branch-max panel (8 evaluation rows; 7 unique chambers).

All seven unique chambers have peak desert strictly interior
(`0 < i* < n_gaps-1`).

## Relation to prior residual surface

- RC45-RC47 (min/mean, dual/count, max/body) retained, not re-proved.
- RC48 measures **multiset mass at the floor**, complementary to min alone.
- RC49 measures **where** the peak desert sits, distinct from max/body size.
- RC50 measures **tail occupancy**, distinct from max/median height (RC37).
- RC2 remains falsified at `D=738`.
- 540 is not formalized as a law (historical clustering only).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity remains unresolved.
These claims are residual audit only. Direct next-prime and Interior Maximizer
remain proved. Residual holds do not empty `Annulus(r)` and do not force
`D(r) <= C_dyn(r)`.

## Inputs read

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
- prior chamber table `experiments/square-branch-hourly-2026-07-10/`
- RC45 table retained as prior packing residual surface

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-16-rc48/offset_540_residual_rc48_probe.py
```

## Next pressure

Queue falsification `5e8-6e8` (preferred holdout). Re-check RC48-RC50 (and
RC45-RC47) on any new util maximum. Do not promote tight_frac, desert_pos, or
large_frac to theorem. Do not revive fixed band 540 or d=4 SDA. Prefer new-band
holdout over further residual minting on the same 7 chambers.
