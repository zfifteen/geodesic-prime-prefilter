# Dual d(n) and zero-excess E(n) field

## Observable object

Take one concrete gap, for example from `89` to `97`. Draw divisor counts as bars. Underneath, draw the zero-excess score

`E(n) = (d(n)/2 - 1) ln n`.

## Mechanism

Primes are exactly the integers with `d(n)=2`, which forces `E(n)=0`. Composites lift above zero excess. Minimizing `E` on the interior is the same selection problem as maximizing `Z=e^{-E}` or maximizing `F=-E`.

## Project terms

- **DNI**: Divisor Normalization Identity.
- **Zero excess**: prime-centered coordinate used throughout PGS.
- **GWR witness**: marked on both panels as the leftmost minimum-divisor interior point.

## Status and limits

- Status: **mixed** (toy illustration of the DNI coordinate identity and GWR selection; theorems live in `PROOF.md`).
- Regime: one small gap. Not an evidence ladder.
- Dual coordinate `Z` is an exact reformulation, not a separate law.
