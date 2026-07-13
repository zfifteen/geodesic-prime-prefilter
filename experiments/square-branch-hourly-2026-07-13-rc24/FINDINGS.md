# Offset-540 Structural Audit: RC24-RC26 (Mean Gap / Signed Dual / Open Frac)

**Date:** 2026-07-13
**Job id:** `offset-540-structural-audit`
**Status:** residual claims hold (audit only)

## Plain object

Start at a selected prime square `w = r^2` and look backward through the chamber
prefix of length `D(r)`. Mark every interior integer with divisor count
`tau = 4`, the late prime-square endpoint with `tau = 3` at offset `D`, and the
trail from the last `tau = 4` hit to that endpoint. From those marks, measure:

1. How regularly the `tau = 4` hits sit between the first and last such hit.
2. Whether the early Dual mark or the late Dual trail is longer (signed
   imbalance).
3. How much of the full chamber length is already open after the first
   `tau = 4` mark.

Project terms for those three measured objects: mean inter-hit gap (RC24), Dual
signed imbalance (RC25), chamber open fraction (RC26).

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late `tau = 3` at `D`
- Tau4 body `last_tau4 - first_tau4`
- mean inter-hit gap `(last - first) / (tau4_count - 1)`
- Dual signed imbalance `(trail - first) / Dual L1`
- chamber open fraction `(D - first_tau4) / D`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC24 / P28 | Tau4 mean inter-hit gap envelope | `7.0 <= mean_gap <= 10.0` | range `[7.653, 8.980]` | holds |
| RC25 / P29 | Dual signed imbalance envelope | `-0.55 <= signed <= 0.70` | range `[-0.455, 0.667]` | holds |
| RC26 / P30 | Chamber open fraction | `(D - first_tau4)/D >= 0.96` | range `[0.9671, 0.9959]` | holds |

Surface: segment utilization maxima through `4e8-5e8` plus full `o_q in {2,4,6}` branch-max panel (8 rows).

## Relation to prior residual surface

- RC21-RC23 (tau4 density, Dual max-component share, near-540 Dual L1 floor) retained, not re-proved.
- RC24 opens **mean spacing** of Tau4 hits inside the body between Dual markers (regularity, not density or span).
- RC25 bounds **signed** early/late Dual asymmetry (direction of imbalance), not only the absolute max-component share (RC22).
- RC26 formalizes early-tau4 / late-tau3 **open length** relative to `D`: the chamber opens early and the late `tau = 3` endpoint sits near full offset.

## Theorem boundary

`PROOF.md`: prime-square proximity remains unresolved. These claims are residual
audit only. Direct next-prime and Interior Maximizer remain proved.

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc24/offset_540_residual_rc24_probe.py
```

## Next pressure

Re-check RC24-RC26 (and RC18-RC23) on any new util maximum from `5e8-6e8`
dynamic-cutoff falsification, or run a prefix-tau probe variant on newest
extremal rows. Do not promote mean gap, signed Dual, or open fraction to theorem.
