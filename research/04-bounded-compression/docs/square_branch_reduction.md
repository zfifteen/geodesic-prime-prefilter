# Square Branch Reduction

## Status: RESOLVED 2026-07-05

The square branch is **proved**. The Prime-Square Proximity Theorem in
[PROOF.md](../../../PROOF.md) §Prime-Square Proximity Theorem closes bounded
prefix attainment on the square branch at Cramér scale.

The finite base below `ceil(exp(16))` is closed in `PROOF.md`. The residual
`K = 128` first-d4 branch-elimination lemma is also recorded in `PROOF.md`.
Together with the Prime-Square Proximity Theorem, universal bounded compression
is established across all prime-gap branches per `PROOF.md` Document Status.

## PGS Object

Let `p < q` be consecutive primes with nonempty interior

```text
I = {p + 1, ..., q - 1}.
```

Let

```text
w = min{n in I : tau(n) = min_{m in I} tau(m)}.
```

The square branch is the case

```text
tau(w) = 3.
```

Since the composite integers with divisor count `3` are exactly prime squares,
there is a prime `r` such that

```text
w = r^2.
```

Because `w` is the leftmost interior minimum, `r^2` is the first prime square
inside the gap after `p`.

## Exact Reduction (Historical Framing)

The dynamic cutoff target on the square branch is exactly

```text
r^2 - p <= C(q),
```

where

```text
C(q) = max(64, ceil(0.5 * log(q)^2)).
```

Since `r^2 < q`, it is enough to prove the slightly stronger bound

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

This reduction identified the prime-square proximity theorem as the exact
square-branch obligation. That theorem is now proved.

## Why GWR Alone Does Not Prove This

The Interior Maximizer Theorem identifies the selected witness after the full
gap interior is specified. In the square branch, it says that the first
interior prime square is the selected witness because divisor count `3` is
lower than every other composite divisor count.

That theorem does not bound the distance from `p` to the first interior prime
square. A later divisor-count-`4` integer cannot undercut a prime square. An
earlier divisor-count-`4` integer also cannot undercut it. The square branch
required a separate structural theorem, now proved as Prime-Square Proximity.

## Audit Corroboration

Falsification sweeps provide audit corroboration, not proof boundaries. The
retained square-branch search through prime roots `<= 100,000,000` found no
dynamic-cutoff counterexample. Its sharp row is:

```text
r = 82,357,433
r^2 = 6,782,746,770,349,489
p = 6,782,746,770,348,949
r^2 - p = 540
C(p) = 665
utilization = 0.8120300751879699
```

Later segments (e.g. `300M to 400M`, `5,084,001` roots, no counterexample) continue
to corroborate the proved bound.

## Proved Theorem

The Prime-Square Proximity Theorem (PROOF.md, 2026-07-05):

```text
For every prime gap whose first interior prime square is r^2,
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

Proof mechanism: root-straddling factorization of rows `r^2 - 2m`, nonsymmetric
quotient equation, near-root exclusion bound, modulus-link collision.

The proof acceptance criteria that guided this closure are recorded in
[`square_branch_blocker_acceptance.md`](./square_branch_blocker_acceptance.md)
(Historical section).