# Square-Tail Nonsymmetric Quotient Lemma

## Status

Proved lemma. Not a complete square-tail proof.

## Object

Let `r` be an odd prime root and let `M` be a positive integer with

```text
2M < r.
```

For

```text
1 <= m <= M
```

set

```text
x_m = r^2 - 2m.
```

Assume `x_m` is M-rough and composite. Let

```text
x_m = ell * c
```

where `ell` is the least prime factor of `x_m`. By the near-root factor lemma,
write

```text
ell = r - h
c = r + h + d
```

with

```text
h >= 1
d >= 0.
```

The symmetric case is `d = 0`. This lemma describes the nonsymmetric case
`d >= 1`.

## Lemma

For every nonsymmetric M-rough composite row,

```text
d * ell = h^2 - 2m.
```

Therefore

```text
ell = (h^2 - 2m) / d
```

and

```text
r = h + (h^2 - 2m) / d.
```

Thus `d` is a positive divisor of `h^2 - 2m`, and the least factor is a
divisor quotient below `h^2`.

## Proof

The near-root equation gives

```text
2m = h^2 - d(r - h).
```

Since

```text
ell = r - h,
```

this becomes

```text
2m = h^2 - d ell.
```

Rearranging gives

```text
d ell = h^2 - 2m.
```

Since the row is nonsymmetric, `d >= 1`. Hence `d` divides `h^2 - 2m`, and

```text
ell = (h^2 - 2m) / d.
```

Finally,

```text
r = ell + h = h + (h^2 - 2m) / d.
```

This proves the lemma.

## Converse

Conversely, suppose integers `m`, `h`, and `d` satisfy

```text
1 <= m <= M
h >= 1
d >= 1
d | (h^2 - 2m)
```

and define

```text
ell = (h^2 - 2m) / d
r = ell + h
c = r + h + d.
```

Then

```text
ell * c = r^2 - 2m.
```

Indeed,

```text
ell * c = ell(ell + 2h + d)
        = (ell + h)^2 - h^2 + d ell
        = r^2 - h^2 + (h^2 - 2m)
        = r^2 - 2m.
```

To produce an M-rough composite row of the square-tail type, the additional
conditions are exactly:

```text
r is an odd prime,
ell is prime,
ell > M,
ell is the least prime factor of r^2 - 2m.
```

The last condition is essential. The quotient equation produces a divisor
factorization; the square-tail obstruction word records the least prime factor.

## Consequence For Obstruction Words

Every nonsymmetric row in a complete M-rough obstruction word is governed by
an integer quotient `d >= 1`:

```text
r = h + (h^2 - 2m) / d.
```

The row-private least factor is not arbitrary. It is a prime quotient of
`h^2 - 2m`.

Together with the symmetric row lemma, the complete obstruction word splits
into:

```text
symmetric rows:     m = 2a^2
nonsymmetric rows:  d | (h^2 - 2m), ell = (h^2 - 2m) / d
```

## Proof Boundary

This lemma does not prove that `O(r)` is impossible. It converts every
nonsymmetric M-rough composite row into an exact divisor equation. The remaining
direct-impossibility proof must show that a positive-row prime root cannot
support such divisor equations for every M-rough row.

Grok response `54bff914-3f49-9de6-967f-42ba79d0f98b` agreed that the lemma,
converse, and proof boundary are correct. The response also flagged the least
factor condition as essential: quotient data alone gives a divisor, not
automatically the least prime factor in the obstruction word.
