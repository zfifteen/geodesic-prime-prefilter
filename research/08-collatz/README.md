# Collatz Prime-Gap Divisor Experiments

## Migration Note

This chapter is the filesystem home for the Collatz PGS research family after
the repository reorganization.

## Object

Collatz-adjacent PGS experiments studying odd first-descent blocks against
divisor-count structure inside prime gaps.

## Invariant Or Rule

The chapter studies first-descent source states, same-gap backgrounds,
terminal-adjacent residue identities, and reset-carrier strata through
deterministic PGS-adjacent probes.

## Proof Status

Chapter-local Collatz proof material lives in `research/08-collatz/PROOF.md`
and `research/08-collatz/PROOF-ADDENDUM.md`. Root PGS theorem status continues
to live in `PROOF.md`.

## Measured Evidence

Measured outputs live under `research/08-collatz/output/`.

## Audit Status

The moved test suite passed after relocation:

```text
python3 -m pytest research/08-collatz/tests
55 passed in 0.42s
```

## Invalidated Rules

No invalidated-rule status changed during migration.

## Unresolved State

No unresolved-state status changed during migration.

## Reproduce

Use the commands in the quick demo and validation sections below.

## Provenance

Original home: legacy experiment-root pointer directory.

## Summary

This experiment bundle studies odd Collatz first-descent blocks against
divisor-count structure inside prime gaps.

The strongest supported finding is:

```text
Collatz first-descent source states hit the odd cells nearest prime-gap
divisor-count minima above same-gap background; witness-contact blocks have a
distinct reset profile; and the positive reset carrier localizes to
below-minimizer terminal adjacency.
```

At odd seeds `3 <= s <= 999999`, the same-gap source hit ratio is
`1.7637165846198448`. Witness-contact blocks have median reset strength
`2.078632113914513`, versus `1.8728822607686915` for no-witness-contact
blocks. Below-minimizer terminal hits beat above-minimizer terminal hits by
matched-weighted mean of stratum median reset delta `0.9934374958512522`, and
remain positive against no-witness blocks with delta `0.48311171458205104`.

The terminal-adjacent residue identity is the exact algebraic normal form for
that localized carrier. Across `15558` terminal adjacent rows, the divisor
minimizer residue identity, exact-`v2` check, recomputed step, and terminal
target all match at rate `1.0`.

## Layout

```text
research/08-collatz/
  scripts/   deterministic probes and the single-file public demo
  tests/     focused pytest coverage for the probes
  docs/      research notes, goal state, and X-post draft
  reviews/   external or second-pass reviews
  output/    committed summaries and compact row artifacts
  assets/    generated images and social graphics
```

## Definitions

- A first-descent block starts at an odd seed `s` and follows the accelerated
  odd Collatz map until the first odd target `t < s`.
- First-descent block length is the number of accelerated odd transitions in
  that block, including the final transition to `t`.
- Reset strength is `R(s)=s/t`, where `t` is the first odd target below `s`.
- The terminal source is the last odd source value in the block, immediately
  before the first target below `s`.
- For consecutive primes `p < q`, the leftmost divisor-count minimizer `w` is
  the first integer in `p < n < q` with minimal divisor count.
- The odd cells nearest the minimizer are the odd interior cells among
  `w - 1`, `w`, and `w + 1`.
- The same-gap background rate is computed by replacing each visited composite
  source with all odd interior cells of its own containing prime gap, excluding
  prime endpoints, and counting what share of those odd cells are nearest to
  the same `w`.

For a below-minimizer terminal source `n=w-1` with final exponent `k`, exactness
is:

$$3w \equiv 2 \pmod {2^{k}}$$

$$3w \not\equiv 2 \pmod {2^{k+1}}$$

## Quick Demo

The public gist-style demo has no third-party dependencies:

```text
python3 research/08-collatz/scripts/collatz_prime_gap_divisor_demo.py --limit 100000
```

For a fast smoke run:

```text
python3 research/08-collatz/scripts/collatz_prime_gap_divisor_demo.py --limit 20000
```

The demo recomputes first-descent blocks, prime gaps, divisor counts, same-gap
background controls, terminal adjacent residue checks, and compact summary
metrics.

## Raw Table Policy

The large same-gap scale raw table is intentionally excluded:

```text
research/08-collatz/output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It is reproducible from:

```text
python3 research/08-collatz/scripts/collatz_pgs_same_gap_scale_probe.py --limit 1000000
```

The committed output keeps durable summaries and compact rows. The huge raw
table is an intermediate artifact, not a durable finding.

## Current Research Target

The broad reset-certificate measurement phase is complete. The exact 3-step
terminal-residue family now has a closed algebraic note in `PROOF.md`. A
targeted inverse scan through odd seeds `<= 100000000` found both branches; the
live signal is the large branch-occupancy imbalance. Branch 2 produced `12218`
below-minimizer hits versus `41` branch-1 hits.

The proof-pressure question is:

```text
Why does branch 2 pass both filters--lower divisor-count load and composite
terminal-source eligibility--far more often than branch 1 among inverse-eligible
short-block witnesses?
```

Start with:

```text
research/08-collatz/PROOF.md
research/08-collatz/docs/collatz_pgs_goal.md
research/08-collatz/docs/collatz_pgs_short_block_reset_candidate_probe.md
research/08-collatz/docs/collatz_pgs_short_block_branch_counterexample_probe.md
research/08-collatz/docs/collatz_pgs_branch_occupancy_proof_target.md
research/08-collatz/docs/collatz_pgs_branch_occupancy_baseline_probe.md
research/08-collatz/docs/collatz_pgs_terminal_adjacent_residue_probe.md
research/08-collatz/docs/collatz_pgs_below_witness_family_probe.md
```
