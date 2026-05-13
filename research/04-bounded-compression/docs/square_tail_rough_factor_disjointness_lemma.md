# Square-Tail Rough-Factor Disjointness Lemma

## Status

Proved lemma. Not a complete square-tail proof.

## Object

Let `r` be an odd prime root and let

```text
S = r^2.
```

Fix a positive integer `M`. For each row

```text
1 <= m <= M
```

define

```text
x_m = r^2 - 2m.
```

The M-rough rows are the rows for which `x_m` has no prime factor at most
`M`.

## Lemma

If `p > M` is an odd prime, then `p` divides at most one row `x_m` with
`1 <= m <= M`.

## Proof

Suppose `p` divides two rows:

```text
p | x_m
p | x_n
```

Then `p` divides their difference:

```text
x_m - x_n = (r^2 - 2m) - (r^2 - 2n) = 2(n - m).
```

Since `p` is odd, `p` does not divide `2`, so

```text
p | (n - m).
```

But `m` and `n` both lie between `1` and `M`, so if `m != n`,

```text
0 < |n - m| < M < p.
```

No positive integer smaller than `p` is divisible by `p`. Therefore `m = n`.

Thus `p` divides at most one row.

## Consequence For M-Rough Obstruction Words

In an M-rough row, every prime factor is greater than `M`. Therefore every
prime factor of every M-rough row is private to that row. No prime factor from
one M-rough row appears in another M-rough row in the same parent window.

For a complete obstruction

```text
O(r): every M-rough row is composite,
```

the obstruction word is not only a list of least factors. It is a row-private
factorization object:

```text
x_m = ell_m * c_m,
```

where every prime factor of `ell_m * c_m` occurs in no other M-rough row.

Equivalently, under `O(r)`, the prime factors of the full M-rough obstruction
word form a row partition:

```text
PrimeFactors(x_m) cap PrimeFactors(x_n) = empty set
```

for every pair of distinct M-rough rows `m != n`.

The rows are odd because `r^2` is odd and `2m` is even, so the factor `2` does
not enter the obstruction word.

## Proof Boundary

This lemma does not prove that `O(r)` is impossible. It rules out any proof
route that needs a large prime factor to propagate across two different
M-rough rows in the same parent window.

Grok response `4a92923b-5565-91d4-96fe-37cdcf8c652e` agreed that the lemma is
correct and identified the row-partition form as the useful strengthening. The
partition property alone still permits a complete obstruction word, so it is a
building block rather than a completed proof.

The remaining theorem must use this row-private factor structure to prove one
of the following:

```text
O(r) is impossible for positive-row prime roots.
```

or

```text
O(r) forces a smaller actual obstruction O(ell).
```
