# RSA v2 40-Bit V1 Algorithm

This document defines the first clean factorizer algorithm before implementation.

The first run is a 40-bit calibration case, but the algorithm is written as the
smallest RSA-scale path. No step may rely on a low-bit shortcut that would need
to be replaced for RSA-260.

## Input

The inference runner reads a public case row containing:

- `case_id`;
- `N`;
- `bits`;
- `radius`;
- `balance_band`.

The inference runner does not read audit factors.

The first case is:

```text
case_id = rsa_v2_40bit_static_001
N = 1099507433251
bits = 40
radius = 1024
balance_band = 2
```

## Stage 1: Public Center

Compute `isqrt(N)`.

This is the public center of the semiprime chamber. It is not a factor and does
not reveal either endpoint. It gives the fixed point around which the lower and
upper factor chambers face each other.

## Stage 2: Candidate Band

Build the lower-side public candidate band:

```text
[isqrt(N) - radius, isqrt(N)]
```

The lower factor of a balanced semiprime lies on this side of the center. The
upper-side coordinate for a lower candidate `x` is the public reciprocal floor
`N // x`.

## Stage 3: Public Filters

Apply cheap public filters before any chamber measurement:

1. Keep candidates inside the declared balance band.
2. Keep lower candidates in wheel-open residue classes.
3. Compute `y = N // x`.
4. Keep pairs whose reciprocal floor `y` stays inside the upper balance band.
5. Keep pairs whose upper coordinate is also wheel-open.

These filters reduce the chamber without testing whether `x` divides `N`.

## Stage 4: PGSPG Chamber State

For each serious candidate pair `(x, y)`, derive local PGSPG chamber state on
both sides.

The lower side asks:

```text
previous PGS endpoint before x -> chamber reset -> does it return to x?
```

The upper side asks:

```text
previous PGS endpoint before y -> chamber reset -> does it return to y?
```

The state is derived by code from local public intervals. It is not supplied as
a fixture.

## Stage 5: Reciprocal Recursive Lock

Apply recursive reciprocal PGS stability for a fixed number of rounds.

Default depth:

```text
recursive_depth = 4
```

For each round:

1. Lock the lower side by previous endpoint plus chamber reset.
2. Lock the upper side by previous endpoint plus chamber reset.
3. Transport the lower and upper endpoints through the public reciprocal map.
4. Continue only if both sides remain stable.

A pair that fails local stability or reciprocal stability is eliminated.

## Stage 6: Product Closure

After PGS contraction and recursive lock, apply public product closure to the
remaining survivor set.

Product closure checks:

```text
x * y == N
```

This is certification after PGS contraction. It is not the mechanism that builds
the initial survivor set.

## Output

If exactly one unordered product-closed pair remains, emit a resolved row.

If no product-closed pair remains, or more than one unordered pair remains, emit
an explicit unresolved row.

The runner also emits survivor rows and a summary so the funnel can be reviewed
without relying on prose.

## Failure Mode

Every failure to resolve is an experiment result.

Do not add fallback paths, alternate algorithms, random retries, hidden widening,
or a direct factor search to force success.
