# Collatz Branch-Occupancy Proof Target

Proof status: proof target

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
The measured branch-occupancy explanation is now closed for odd seeds
`s <= 100000000` and final exponents `k=4` and `k=8`:

```text
Branch 1 concentration is explained by automatic twin-gap terminal-prime wins
plus a fully enumerated small composite-terminal exception family; branch 2's
composite-terminal surface persists across nontrivial gaps.
```

The remaining open work is theorem conversion, not explanation discovery. The
next theorem-pressure task is branch-1 only: explain the symbolic structure of
the composite-terminal exception family before returning to branch 2.

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

Among leftmost-minimizer successes, the terminal geometry is:

| Branch | Automatic twin terminal-prime | Terminal-prime non-twin | Composite below-minimizer | Total leftmost |
|---:|---:|---:|---:|---:|
| `1` | `19887` | `168` | `41` | `20096` |
| `2` | `0` | `18609` | `12218` | `30827` |

The branch-1 composite-terminal exception family is fully enumerated in
`../output/collatz_pgs_branch_occupancy_baseline_probe/branch1_composite_exception_rows.jsonl`.
It has `41` rows. All have `terminal_geometry = composite_below_minimizer` and
`witness_tau = 12`. The symbolic analyzer confirms that every row has:

$$w=18u$$

with $u$ prime.

| Gap width | Branch-1 composite-terminal exceptions |
|---:|---:|
| `6` | `37` |
| `8` | `3` |
| `10` | `1` |

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

## Result Of The Focused Pressure Test

The focused terminal-geometry obstruction test supports the two-channel
explanation on the measured surface:

```text
branch 1: mostly automatic twin-gap wins, where w is the only interior integer
          and w-1 is a prime endpoint
branch 2: nontrivial-gap wins remain abundant, so w-1 is often composite and
          remains inside the gap
```

## Stop Condition

The explanation stop condition is met for the committed measured regime. The
bounded certificate is:

```text
automatic twin-gap terminal-prime channel
+ 41 fully enumerated branch-1 composite-terminal exceptions
+ 12218 branch-2 composite-terminal leftmost successes
```

The focused branch-1 theorem stop condition remains open:

```text
Prove symbolically that the branch-1 composite-terminal exception family is
restricted to w=18u with u prime, divisor count 12, and gap width 6, 8, or 10.
```

Only after that branch-1 obstruction is converted into symbolic structure
should the branch-2 nontrivial-gap occupancy mechanism become the active target.
