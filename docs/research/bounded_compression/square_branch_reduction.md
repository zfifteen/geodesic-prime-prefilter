# Square Branch Reduction

## Status

The square branch of bounded prefix attainment remains unresolved.

The finite base below `ceil(exp(16))` is closed in `PROOF.md`. The residual
`K = 128` first-d4 branch-elimination lemma is also recorded in `PROOF.md`.
The square-branch reduction below is now recorded in `PROOF.md` as the exact
remaining bounded-compression obligation. Neither the finite base nor the
residual K=128 theorem proves the all-scale square branch.

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

## Exact Reduction

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

Thus the square branch reduces to a prime-square proximity theorem:

```text
For every consecutive prime gap whose first interior prime square is r^2,
that first square occurs within max(64, ceil(0.5 * log(r^2)^2)) of the left
endpoint.
```

## Why GWR Alone Does Not Prove This

The Interior Maximizer Theorem identifies the selected witness after the full
gap interior is specified. In the square branch, it says that the first
interior prime square is the selected witness because divisor count `3` is
lower than every other composite divisor count.

That theorem does not bound the distance from `p` to the first interior prime
square. A later divisor-count-`4` integer cannot undercut a prime square. An
earlier divisor-count-`4` integer also cannot undercut it. The only way to
bound the square branch is to bound where the first interior prime square
appears relative to the left endpoint.

## Current Evidence

The retained square-branch search through prime roots `<= 100,000,000` found no
dynamic-cutoff counterexample. Its sharp row is:

```text
r = 82,357,433
r^2 = 6,782,746,770,349,489
p = 6,782,746,770,348,949
r^2 - p = 540
C(p) = 665
utilization = 0.8120300751879699
```

This is finite measured evidence. It is not an all-scale proof.

## Missing Theorem

The exact missing theorem is:

```text
For every prime gap whose first interior prime square is r^2,
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

A proof of this theorem closes the square branch. Without it, the all-scale
bounded dynamic cutoff theorem remains unresolved.
