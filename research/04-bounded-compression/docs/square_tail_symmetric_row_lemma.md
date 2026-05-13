# Square-Tail Symmetric Row Lemma

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

Assume `x_m` is M-rough and composite. In the near-root factor lemma, write

```text
x_m = (r - h)(r + t)
```

with `t >= h`.

## Lemma

The symmetric case is exactly:

```text
m = 2a^2
```

for some positive integer `a`, with

```text
h = t = 2a
```

and

```text
x_m = (r - 2a)(r + 2a).
```

The two factors are coprime. If the row is M-rough, then both factors have no
prime factor at most `M`.

## Proof

In the symmetric case, `t = h`. The near-root equation gives

```text
2m = h^2.
```

Since `2m` is even, `h` is even. Write

```text
h = 2a.
```

Then

```text
2m = 4a^2
```

so

```text
m = 2a^2.
```

The factorization becomes

```text
x_m = (r - 2a)(r + 2a).
```

The factors are odd. Any common divisor of `r - 2a` and `r + 2a` divides both

```text
2r
```

and

```text
4a.
```

Since the common divisor is odd, it divides `r` and `a`. But

```text
a^2 = m / 2 <= M / 2 < r / 4,
```

so `0 < a < r`. Because `r` is prime, no divisor greater than `1` can divide
both `r` and `a`. Thus

```text
gcd(r - 2a, r + 2a) = 1.
```

If the row is M-rough, then `x_m` has no prime factor at most `M`. Since every
prime factor of either `r - 2a` or `r + 2a` is a prime factor of `x_m`, both
factors have no prime factor at most `M`.

## Consequence For Obstruction Words

The symmetric rows in a complete M-rough obstruction word are exactly the rows

```text
m = 2a^2 <= M.
```

Each such row contributes a centered coprime M-rough pair:

```text
(r - 2a, r + 2a).
```

There are at most

```text
floor(sqrt(M / 2))
```

such rows.

All other M-rough composite rows are nonsymmetric and obey the near-root
distance bound from the near-root factor lemma.

## Proof Boundary

This lemma does not prove that `O(r)` is impossible. It isolates the sparse
exceptional rows whose least factor can occupy the final square-root-width
band below `r`.

The remaining direct-impossibility proof must rule out a complete obstruction
word after separating:

```text
sparse centered coprime rows
```

from

```text
nonsymmetric rows with least factors bounded away from r.
```

Grok response `52a93027-6348-948c-8540-71ffb884d7de` agreed that the lemma,
coprime proof, row count, and proof boundary are correct. Coprimeness alone
does not forbid a complete obstruction word.
