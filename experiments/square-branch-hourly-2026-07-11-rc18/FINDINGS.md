# Offset-540 Structural Audit: RC18–RC20 (Dual L1 / Tau4 Span)

**Date:** 2026-07-11  
**Job id:** `offset-540-structural-audit`  
**Status:** residual claims hold (audit only)

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late tau=3 at `D`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC18 / P22 | Dual L1 envelope | `first + trail ≤ 24` | range `[4, 24]` | holds |
| RC19 / P23 | Tau4 support span fraction | `(last−first)/(D−1) ≥ 0.95` | min `0.9567` | holds |
| RC20 / P24 | Relative Dual L1 | `(first+trail)/D ≤ 0.05` | max `0.0453` | holds |

Surface: segment utilization maxima through `4e8–5e8` plus full `o_q ∈ {2,4,6}` branch-max panel.

## Relation to prior residual surface

- RC15–RC17 (componentwise trail / early / near-540 dual) retained, not re-proved.
- RC18 is joint L1 on the Dual, tighter than the product of independent early/late bounds on the joint surface.
- RC19 formalizes almost-full tau4 support span across the chamber.
- RC20 scales Dual L1 by `D`.

## Theorem boundary

`PROOF.md`: prime-square proximity remains unresolved. These claims are residual
audit only. Direct next-prime and Interior Maximizer remain proved.

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-11-rc18/offset_540_residual_rc18_probe.py
```

## Next pressure

Re-check RC18–RC20 (and RC15–RC17) on any new util maximum from `5e8–6e8`
dynamic-cutoff falsification. Do not promote Dual L1 or span fraction to theorem.
