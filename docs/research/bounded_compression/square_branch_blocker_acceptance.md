# Square Branch Blocker And Acceptance Criteria

## Status

The square branch is unresolved.

`PROOF.md` now records the exact reduction: the bounded dynamic cutoff theorem
is closed on the square branch exactly when the prime-square proximity theorem
below is proved.

## PGS Objects

Let `p < q` be consecutive primes with nonempty gap interior

```text
I = {p + 1, ..., q - 1}.
```

Let

```text
w = min{n in I : tau(n) = min_{m in I} tau(m)}.
```

The square branch is

```text
tau(w) = 3.
```

Since the integers with divisor count `3` are exactly prime squares, there is
a prime `r` with

```text
w = r^2.
```

The leftmost-minimum condition makes `r^2` the first prime square in `I`.

## Exact Theorem Obligation

The requested square-branch theorem is

```text
r^2 - p <= C(q)
```

where

```text
C(q) = max(64, ceil(0.5 * log(q)^2)).
```

Because `r^2 < q`, it is enough to prove the stronger proximity statement

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

This is the exact missing theorem.

## Blocker

The Interior Maximizer Theorem determines which interior integer wins after
the full gap interior is fixed. In the square branch it says that the first
interior prime square wins because divisor count `3` is lower than every
other composite divisor count.

That theorem does not bound the distance from `p` to the first interior prime
square. Divisor-count ordering has no lower-divisor-count carrier available
before a prime square, because `3` is the minimum composite divisor count.

Thus no current PGS theorem in `PROOF.md` supplies the square offset bound.
The missing input is a distance theorem for primes immediately before prime
squares.

## What The Square-Branch Hypothesis Gives

Let `s` be the prime immediately before `r`. If `r^2` is the selected
prime-square witness, then the previous prime `p` must satisfy

```text
s^2 < p < r^2.
```

Otherwise `s^2` would also lie in the same gap interior before `r^2`, and the
selected prime-square witness would be `s^2`, not `r^2`.

Therefore the square-branch hypothesis gives the deterministic bound

```text
r^2 - p < r^2 - s^2 = (r - s)(r + s).
```

Conversely, if the greatest prime below `r^2` lies between `s^2` and `r^2`,
then the prime gap after that greatest prime contains `r^2` and contains no
earlier prime square. In that gap, `r^2` is the selected prime-square witness.
This is the exact square-branch characterization recorded in `PROOF.md`.

This is a band bound between consecutive prime squares. It does not imply

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

The missing theorem must compress this prime-square band down to the dynamic
logarithmic-square cutoff.

## Known-Bound Boundary

The inspected unconditional short-interval theorem of Baker, Harman, and
Pintz gives prime occurrence in intervals of length `x^0.525` for large `x`.
That scale is far larger than `0.5 * log(x)^2`.

The logarithmic-square scale is the scale of Cramer-Granville type prime-gap
conjectures. The inspected sources do not supply an unconditional theorem at
that scale.

Therefore the square branch is not closed by known general prime-gap bounds
or by the current PGS maximizer theorem.

## Acceptance Criteria For A Real Proof

A valid proof of the square branch must provide one of the following:

1. A PGS-native theorem proving that the first interior prime square in every
   selected square branch satisfies

   ```text
   r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
   ```

2. A PGS-native theorem proving the weaker target directly:

   ```text
   r^2 - p <= C(q).
   ```

3. A finite reduction that leaves only a checked finite range, together with
   an exact deterministic verification of that finite range.

The following do not close the theorem:

- finite square-branch surfaces;
- maximum observed utilization below `1`;
- Cramer-style or density heuristics;
- average prime-gap estimates;
- the Interior Maximizer Theorem alone;
- a `d = 4` window theorem, because `d = 4` cannot undercut a prime square.

## Current Result

The finite base `q < exp(16)` is proved in `PROOF.md`.

The residual `K = 128` first-d4 branch-elimination theorem is proved in
`PROOF.md` under its stated finite residual hypotheses.

The square branch remains unresolved until the prime-square proximity theorem
above is proved.

## External Reference Points

- Baker, Harman, and Pintz, "The difference between consecutive primes, II":
  `https://www.cambridge.org/core/journals/proceedings-of-the-london-mathematical-society/article/abs/difference-between-consecutive-primes-ii/2EF13261B3B25458A25F41ED74AA2FC2`
- LeClair, "An asymptotic upper bound on prime gaps":
  `https://arxiv.org/abs/1506.03359`
