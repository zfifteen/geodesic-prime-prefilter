# Collatz Branch-Occupancy Proof Target

## Status

The short-block Collatz algebra is closed for its stated scope in
`../PROOF.md`.

The algebraic stack is:

```text
exact 3-step first-descent block
  -> two middle-exponent branches
  -> necessary modulo-18 terminal classes
  -> forward-consistent branch constructions
  -> exact reset formulas
```

The remaining live question is not whether the two branches exist. Both occur.
The remaining question is why the prime-gap divisor-count filter selects branch
2 far more often than branch 1 in the measured below-minimizer terminal
surface.

## Measured Occupancy Signal

The targeted inverse scan through odd seeds `s <= 100000000` found:

| Final exponent | Branch | Hits | First seed | Median reset |
|---:|---:|---:|---:|---:|
| `4` | `1` | `36` | `6000471` | `2.370370339879278` |
| `4` | `2` | `11510` | `9675` | `4.740740657317454` |
| `8` | `1` | `5` | `25957527` | `37.925925522691756` |
| `8` | `2` | `708` | `4171` | `75.85185042289021` |

Combined across the measured `k=4` and `k=8` surfaces, branch 2 produced
`12218` below-minimizer terminal hits versus `41` branch-1 hits.

## Theorem Candidate

Among inverse-eligible exact 3-step terminal witnesses, leftmost
divisor-count minimizers in prime gaps are strongly biased toward the branch-2
terminal residue class:

$$w \equiv 14 \pmod {18}$$

over the branch-1 terminal residue class:

$$w \equiv 0 \pmod {18}$$

The first measured mechanism is divisor-count load. Branch 1 forces $w$ to be
divisible by $18$, so every branch-1 witness carries at least the prime-power
baseline from $2\cdot 3^2$. Branch 2 forces $w\equiv 14\pmod {18}$, so it is
even but not divisible by $3$. Since the prime-gap filter asks $w$ to minimize
divisor count inside its gap, branch 1 starts with a larger mandatory
small-prime divisor burden.

The full baseline probe shows that this is real but incomplete. At
`s <= 100000000`, branch 2 is about `3.07x` more likely to make $w$ the
leftmost divisor-count minimizer, but about `596x` more likely to become a
below-minimizer terminal hit. The remaining factor appears in terminal-source
geometry: branch-1 minimizer successes mostly occur when `w-1` is prime, while
branch 2 retains a large composite-terminal surface.

The refined terminal-geometry rows show the concentration directly. Branch 1
has `20096` leftmost-minimizer successes, but only `41` have composite terminal
source `w-1`. The other `20055` have `w-1` prime, and `19887` of those prime
terminal cases sit in gap width `2`. Branch 2 has `30827` leftmost-minimizer
successes, of which `12218` have composite terminal source.

## First Pressure Test

For each inverse-eligible branch candidate in the committed `k=4` and `k=8`
surfaces, compare the divisor-count rank of $w$ inside its containing prime
gap, stratified by:

- branch;
- final exponent `k`;
- prime-gap length;
- exact divisor count of $w$;
- count of lower-divisor competitors in the same open gap.

The proof pressure is strongest if the observed branch-2 advantage is already
explained by the forced small-prime baseline:

```text
branch 1: w divisible by 18 -> higher divisor-count floor -> fewer minimizers
branch 2: w congruent to 14 mod 18 -> avoids factor 3 -> more minimizers
```

## Stop Condition

This line advanced to a two-filter target. The branch-occupancy imbalance does
not reduce to divisor-count obstruction alone.

The current stop condition is:

```text
Prove or falsify that branch 1's leftmost-minimizer successes concentrate in
terminal-prime twin-gap geometry, while branch 2 preserves composite terminal
source eligibility.
```

If this terminal-source geometry explains the residual, the proof target
becomes a combined divisor-load and terminal-eligibility theorem.
