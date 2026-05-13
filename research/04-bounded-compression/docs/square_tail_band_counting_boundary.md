# Square-Tail Band-Counting Boundary

## Status

Invalidated proof route. Useful boundary.

## Object

The halved-quotient lemma proves that every nonsymmetric M-rough composite row
under `2M < r` has

```text
h = 2a
d = 2b
b >= 1.
```

Therefore

```text
h^2 + 2h >= 2r + 2m.
```

Equivalently, nonsymmetric least factors are excluded from the final roughly
`sqrt(2r)`-wide band below `r`.

The symmetric rows remain exactly

```text
m = 2a^2.
```

## Invalid Inference

The band exclusion does not imply that a complete obstruction word has only
symmetric rows.

It proves only this:

```text
if a nonsymmetric row is composite, its least factor is not in the final
sqrt(2r)-scale band below r.
```

It does not forbid nonsymmetric rows whose least factor is smaller:

```text
ell <= r - 2 ceil((-1 + sqrt(1 + 2(r + m))) / 2).
```

Therefore the following counting route is invalid:

```text
nonsymmetric rows are excluded from the final band
-> only symmetric rows remain
-> row count <= floor(sqrt(M / 2))
-> contradiction.
```

The second implication is false. Nonsymmetric rows can sit outside the final
band.

## Measured Calibration

The current high-utilization record

```text
r = 424171123
M = 395
```

has `62` composite M-rough rows. All `62` are nonsymmetric, and their least
factors range from

```text
419
```

to

```text
159673649.
```

They sit outside the final near-root band. This measurement does not prove the
boundary, but it shows the exact shape that the invalid counting route misses.

## Remaining Missing Invariant

The strengthened distance bound is a real deterministic constraint, but it is
not a global obstruction collapse.

The missing invariant is:

```text
a global constraint on small-ell nonsymmetric placements that prevents the
M-rough rows from being filled independently by row-private least factors.
```

Without such an invariant, row-private nonsymmetric placements outside the
near-root band remain compatible with the current local factorization
constraints.

## Second Opinion

Grok response `7519afb4-5675-988c-ae2e-85208635fac1` proposed a band-counting
route. The route is not adopted because it treats near-root band exclusion as
total nonsymmetric exclusion.

Grok response `d1bec1af-7b71-54b5-86aa-6f89f6e3aa67` agreed that the
band-counting inference is invalid. It identified the missing invariant as a
global constraint on admissible small-`ell` placements for nonsymmetric rows.
