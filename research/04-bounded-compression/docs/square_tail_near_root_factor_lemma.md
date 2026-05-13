# Square-Tail Near-Root Factor Lemma

## Status

Proved lemma. Not a complete square-tail proof.

## Object

Let `r` be an odd prime root. Fix a positive integer `M` with

```text
2M < r.
```

For each row

```text
1 <= m <= M
```

define

```text
x_m = r^2 - 2m.
```

Assume `x_m` is M-rough and composite. Let

```text
ell = least prime factor of x_m
```

and write

```text
x_m = ell * c.
```

## Root-Straddling Factor Pair

The least factor satisfies

```text
M < ell < r.
```

The lower bound follows from M-roughness. The upper bound follows because
`ell <= sqrt(x_m)` and `x_m < r^2`.

The cofactor satisfies

```text
c > r.
```

Indeed,

```text
c = x_m / ell > x_m / r >= (r^2 - 2M) / r > r - 1.
```

Since `c` is an integer and `r` does not divide `x_m`, this gives `c > r`.

Thus every M-rough composite row has a factor pair straddling the parent root:

```text
ell < r < c.
```

## Near-Root Equation

Define positive integers `h` and `t` by

```text
ell = r - h
c = r + t.
```

Then

```text
r^2 - 2m = (r - h)(r + t),
```

so

```text
2m = r(h - t) + ht.
```

Since `2m <= 2M < r`, the case `h > t` is impossible: if `h > t`, then
`r(h - t) + ht >= r`.

Therefore

```text
t >= h.
```

Write

```text
d = t - h >= 0.
```

Then the row equation becomes

```text
2m = h^2 - d(r - h).
```

Equivalently,

```text
h^2 == 2m mod ell.
```

Since `d >= 0`, every M-rough composite row also satisfies

```text
2m <= h^2.
```

Thus the least factor distance from the root obeys

```text
h >= ceil(sqrt(2m)).
```

## Near-Root Exclusion

For an M-rough composite row under `2M < r`, exactly one of the following
holds:

1. `d = 0`, so

   ```text
   2m = h^2
   ```

   and the factorization is symmetric around `r`:

   ```text
   x_m = (r - h)(r + h).
   ```

2. `d >= 1`, so

   ```text
   h^2 >= r - h + 2m.
   ```

   Equivalently,

   ```text
   h^2 + h >= r + 2m.
   ```

Thus a least factor with

```text
h^2 + h < r + 2m
```

is possible only in the exact symmetric case `2m = h^2`. Outside that case,
the distance from the root satisfies the explicit lower bound

```text
h^2 + h >= r + 2m.
```

Equivalently, every nonsymmetric M-rough composite row satisfies

```text
h >= ceil((sqrt(1 + 4(r + 2m)) - 1) / 2).
```

In terms of the least factor `ell = r - h`,

```text
ell <= r - ceil((sqrt(1 + 4(r + 2m)) - 1) / 2).
```

Thus the nonsymmetric least factor cannot occupy the final square-root-width
band immediately below `r`.

The symmetric case is possible only at rows

```text
m = 2a^2
```

with

```text
h = 2a.
```

Therefore the number of symmetric candidate rows inside `1 <= m <= M` is at
most

```text
floor(sqrt(M / 2)).
```

The full symmetric-row structure is recorded in:

```text
research/04-bounded-compression/docs/square_tail_symmetric_row_lemma.md
```

The nonsymmetric quotient form is recorded in:

```text
research/04-bounded-compression/docs/square_tail_nonsymmetric_quotient_lemma.md
```

## Consequence For Obstruction Words

In a complete M-rough obstruction word with `2M < r`, every composite rough
row has a row-private straddling factorization:

```text
r^2 - 2m = (r - h_m)(r + t_m),
```

with

```text
t_m >= h_m
```

and

```text
2m = h_m^2 - (t_m - h_m)(r - h_m).
```

The obstruction word is therefore constrained by near-root arithmetic, not
only by residue cover.

It also splits into two row types:

```text
symmetric rows:     m = 2a^2
nonsymmetric rows:  ell_m <= r - ceil((sqrt(1 + 4(r + 2m)) - 1) / 2)
```

Only the symmetric rows can place a least factor in the final square-root-width
band below the root.

Therefore, under a complete obstruction `O(r)`, at most

```text
floor(sqrt(M / 2))
```

M-rough rows can have their least factor in that final band. Every other
composite rough row has its least factor bounded by the nonsymmetric inequality
above.

## Current Cutoff Boundary

For the current dynamic cutoff

```text
C = max(64, ceil(0.5 * log(r^2)^2))
M = floor(C / 2),
```

the condition `2M < r` holds for every odd prime root `r >= 67`.

For `67 <= r < 293`, the cutoff is `C = 64`, so `2M = 64 < r`. For
`r >= 293`,

```text
2M <= C <= 2 log(r)^2 + 1 < r.
```

The final inequality holds at `r = 293`, and the difference

```text
r - 2 log(r)^2 - 1
```

is increasing for `r >= 293`.

The remaining odd prime roots below `67` are finite cases.

## Proof Boundary

This lemma does not prove that `O(r)` is impossible. It gives a deterministic
shape that every M-rough composite row must have in the infinite tail:

```text
private factor pair
+ root-straddling
+ near-root equation
```

The direct impossibility proof must use this shape, or a stronger invariant,
to rule out a complete row-private obstruction word.

Grok response `b963dfc6-cf5d-9ebe-a9aa-2b57131e7481` agreed that the lemma,
cutoff boundary, and proof boundary are correct. The useful strengthening is
the explicit root-distance lower bound `2m <= h^2`, which follows from
`d >= 0`.

Grok response `7b107015-5944-9bd7-9903-7ff26c63a381` agreed that the
symmetric/nonsymmetric split and the symmetric row count are correct. The
result remains a building block: the band restriction alone still permits a
complete obstruction word.
