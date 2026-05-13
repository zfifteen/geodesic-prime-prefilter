# Square-Tail Halved-Quotient Lemma

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

where `ell` is the least prime factor of `x_m`. Then

```text
ell > M
```

and the near-root factor lemma gives

```text
ell = r - h
c = r + h + d
```

with

```text
h >= 1
d >= 0.
```

## Lemma

For every M-rough composite row under `2M < r`, both `h` and `d` are even.

Write

```text
h = 2a
d = 2b.
```

Then every such row has the centered form

```text
ell = r - 2a
c = r + 2a + 2b
m = 2a^2 - b ell.
```

The symmetric rows are exactly the rows with

```text
b = 0,
```

and therefore

```text
m = 2a^2.
```

The nonsymmetric rows are exactly the rows with

```text
b >= 1,
```

and therefore

```text
b ell = 2a^2 - m,
ell = (2a^2 - m) / b,
r = 2a + (2a^2 - m) / b.
```

## Proof

The row value is odd:

```text
x_m = r^2 - 2m.
```

Since `r` is odd, `r^2` is odd, and subtracting the even integer `2m` leaves an
odd integer. Therefore both factors `ell` and `c` are odd.

From

```text
ell = r - h
```

with `r` and `ell` odd, the difference `h` is even. Write

```text
h = 2a.
```

From

```text
c = r + h + d,
```

with `c` odd, `r` odd, and `h` even, the remaining term `d` is even. Write

```text
d = 2b.
```

Substitute these forms into the factorization:

```text
x_m = (r - 2a)(r + 2a + 2b).
```

Expanding gives

```text
(r - 2a)(r + 2a + 2b)
= r^2 + 2br - 4a^2 - 4ab.
```

Since this equals `r^2 - 2m`,

```text
r^2 - 2m = r^2 + 2br - 4a^2 - 4ab.
```

Cancel `r^2` and divide by `2`:

```text
m = 2a^2 + 2ab - br.
```

Because

```text
ell = r - 2a,
```

we have

```text
b ell = b(r - 2a) = br - 2ab.
```

Therefore

```text
m = 2a^2 - b ell.
```

If `b = 0`, then `d = 0`, so the row is symmetric and `m = 2a^2`.

If `b >= 1`, then the row is nonsymmetric and

```text
b ell = 2a^2 - m.
```

Thus `b` divides `2a^2 - m`, and

```text
ell = (2a^2 - m) / b
r = ell + 2a = 2a + (2a^2 - m) / b.
```

This proves the lemma.

## Converse

Conversely, suppose integers `m`, `a`, and `b` satisfy

```text
1 <= m <= M
a >= 1
b >= 0
```

and define

```text
ell = r - 2a.
```

If

```text
m = 2a^2 - b ell,
```

then

```text
(r - 2a)(r + 2a + 2b) = r^2 - 2m.
```

For `b >= 1`, the same statement can be written as

```text
b | (2a^2 - m),
ell = (2a^2 - m) / b,
r = 2a + (2a^2 - m) / b.
```

To produce an M-rough composite row in the square-tail obstruction word, the
additional conditions remain:

```text
r is an odd prime,
ell is prime,
ell > M,
ell is the least prime factor of r^2 - 2m,
x_m has no prime factor <= M.
```

The centered equation alone gives a factorization form. The obstruction word
records the least prime factor of an M-rough row.

## Consequence For Obstruction Words

Every M-rough composite row in a complete obstruction word has one centered
integer form:

```text
x_m = (r - 2a_m)(r + 2a_m + 2b_m)
m = 2a_m^2 - b_m(r - 2a_m).
```

The sparse symmetric rows are the subcase `b_m = 0`. All other rows satisfy
`b_m >= 1` and are governed by the divisor quotient

```text
r = 2a_m + (2a_m^2 - m) / b_m.
```

## Nonsymmetric Distance Corollary

For every nonsymmetric M-rough composite row under `2M < r`,

```text
b >= 1.
```

Therefore

```text
d = 2b >= 2.
```

Using the quotient equation

```text
d ell = h^2 - 2m
```

and `ell = r - h`, we get

```text
h^2 - 2m >= 2ell = 2(r - h).
```

Thus

```text
h^2 + 2h >= 2r + 2m.
```

Since `h = 2a`, this is equivalent to

```text
2a^2 + 2a >= r + m.
```

Consequently every nonsymmetric row satisfies

```text
a >= ceil((-1 + sqrt(1 + 2(r + m))) / 2)
```

and therefore

```text
ell <= r - 2 ceil((-1 + sqrt(1 + 2(r + m))) / 2).
```

In particular, because `m >= 1`, every nonsymmetric least factor is excluded
from the final band below `r` of width

```text
2 ceil((-1 + sqrt(1 + 2(r + 1))) / 2).
```

The symmetric rows are not covered by this corollary. They remain exactly the
rows `m = 2a^2`.

## Proof Boundary

This lemma does not prove that `O(r)` is impossible. It removes the parity
slack from the obstruction word and gives one centered integer equation for
both symmetric and nonsymmetric M-rough composite rows.

The remaining direct-impossibility proof must show that a positive-row prime
root cannot support this centered equation for every M-rough row.

## Second Opinion

Grok response `e1f53b81-e55b-4493-8600-5e9372baaace` confirmed the project
frame and requested explicit carrier definitions before reviewing the lemma.

Grok response `2ffd77ed-e1f8-99a8-a21e-be472516b364` agreed that parity forces
`h` and `d` even and that the centered form

```text
m = 2a^2 - b ell
```

is correct under the stated `2M < r` boundary. It also flagged the small-root
edge cases as already excluded by that hypothesis.

Grok response `e12a9f20-fbe3-e36f-1388-1e083fbfb232` agreed that the parity
corollary strengthens the nonsymmetric distance bound from the previous
near-root estimate. It also warned that the corollary applies only to
nonsymmetric rows under `2M < r`.
