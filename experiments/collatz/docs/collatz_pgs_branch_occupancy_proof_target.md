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

The expected mechanism is divisor-count load. Branch 1 forces $w$ to be
divisible by $18$, so every branch-1 witness carries at least the prime-power
baseline from $2\cdot 3^2$. Branch 2 forces $w\equiv 14\pmod {18}$, so it is
even but not divisible by $3$. Since the prime-gap filter asks $w$ to minimize
divisor count inside its gap, branch 1 starts with a larger mandatory
small-prime divisor burden.

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

This line advances if the branch-occupancy imbalance reduces to a deterministic
divisor-count obstruction for branch 1 inside prime gaps.

It stops, or changes shape, if branch-2 dominance persists after controlling
for the forced divisor-count baseline and gap length. In that case the
occupancy signal is not explained by the modulo-18 divisor burden alone, and
the next mechanism must be isolated from the controlled residual.
