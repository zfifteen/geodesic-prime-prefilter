# Offset-540 Structural Audit: RC21–RC23 (Density / Dual Share / Near-540 Floor)

**Date:** 2026-07-13  
**Job id:** `offset-540-structural-audit`  
**Status:** residual claims hold (audit only)

## Frame

PGS-native objects only:

- ordered chamber prefix before selected square `w = r^2`
- divisor-count field `tau`
- offset `D(r)`
- Dual markers `(first_tau4_offset, trail_gap)` with late tau=3 at `D`
- tau4 density `tau4_count / (D - 1)`
- Dual max-component share `max(first, trail) / Dual L1`

Not revived: fixed-band near-540 law (RC2 falsified), d=4 SDA transfer.

## New residual claims

| ID | Claim | Bound | Observed | Status |
| --- | --- | --- | --- | --- |
| RC21 / P25 | Tau4 density envelope | `0.10 ≤ dens ≤ 0.135` | range `[0.1093, 0.1303]` | holds |
| RC22 / P26 | Dual max-component share | `max(first, trail)/L1 ≤ 0.85` | range `[0.50, 0.833]` | holds |
| RC23 / P27 | Near-540 Dual L1 floor | if `\|D−540\|≤20` then `L1 ≥ 14` | near range `[14, 24]` (n=4) | holds |

Surface: segment utilization maxima through `4e8–5e8` plus full `o_q ∈ {2,4,6}` branch-max panel.

## Relation to prior residual surface

- RC18–RC20 (Dual L1 absolute/relative, tau4 span fraction) retained, not re-proved.
- RC21 opens **hit density** of Tau4 across the chamber prefix (mass rate, not span).
- RC22 bounds **asymmetry** of early/late Dual markers (neither side monopolizes Dual).
- RC23 re-reads recurring offset 540 as a **conditional Dual floor** on the near-540 band, not as a law for `D(r)` itself (RC2 stays falsified by `r=424171123`, `D=738`).

## Theorem boundary

`PROOF.md`: prime-square proximity remains unresolved. These claims are residual
audit only. Direct next-prime and Interior Maximizer remain proved.

## Falsification command

```text
python3 experiments/square-branch-hourly-2026-07-13-rc21/offset_540_residual_rc21_probe.py
```

## Next pressure

Re-check RC21–RC23 (and RC18–RC20) on any new util maximum from `5e8–6e8`
dynamic-cutoff falsification, or run a prefix-tau probe variant on newest
extremal rows. Do not promote density or Dual share to theorem.
