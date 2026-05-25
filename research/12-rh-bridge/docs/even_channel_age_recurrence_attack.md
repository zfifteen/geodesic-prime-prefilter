# Even-Channel Age Recurrence Attack

Date: 2026-05-24

Status: focused sub-approach for the Zero-Excess Return Square-Moment
Theorem.

The most promising sub-approach inside the Age-Divisor Recurrence route is the
even-channel recurrence problem. It removes the growing-modulus complication:
the divisor channel `d = 2` alone is equivalent to the dyadic gap-square
bound.

## Even-Channel Age

Define

$$
A_2(X)=
\sum_{\substack{X<n\le2X\\ 2\mid n}}
(n-p(n)).
$$

For an odd-prime chamber `(p,q]` with

$$
g=q-p=2h,
$$

the even integers inside the chamber occur at offsets

$$
1,3,5,\ldots,2h-1.
$$

Their age sum is

$$
1+3+\cdots+(2h-1)=h^2=\frac{g^2}{4}.
$$

Therefore

$$
A_2(X)
\asymp
\frac14
\sum_{X<q\le2X}g(q)^2
$$

up to dyadic boundary terms.

Thus the Zero-Excess Return Square-Moment Theorem is equivalent to

$$
\boxed{
A_2(X)\ll X(\log X)^B.
}
$$

## Concrete Attack Plan

The even-channel theorem asks:

```text
average backward distance from an even integer to the previous zero-excess
endpoint is polylogarithmic.
```

The attack plan has three steps.

1. **Even-center decomposition.**
   Rewrite the square-moment theorem entirely as an estimate over even
   centers:
   $$
   \sum_{X/2<m\le X}(2m-p(2m))
   \ll
   X(\log X)^B.
   $$

2. **Local divisor-field profile around even centers.**
   For each even `2m`, inspect the positive-excess profile on the odd offsets
   between `p(2m)` and `2m`. A long age means every odd position in that
   backward interval is composite and has positive excess.

3. **Odd-offset persistence estimate.**
   Prove that long backward positive-excess intervals ending at even centers
   have square-summable tail:
   $$
   \#\{2m\in[X,2X]:2m-p(2m)\ge H\}
   \ll
   X(\log X)^B/H^2.
   $$

This is the parity-specialized form of the positive-excess persistence
estimate.

## PGS Structure Available

The even channel has three advantages.

1. **It is canonical.**
   Every prime endpoint greater than `2` is odd, so every nontrivial chamber
   crosses the even lattice in a fixed alternating pattern.

2. **It removes modulus growth.**
   No uniformity over `d <= sqrt(2X)` is needed.

3. **It preserves the zero-excess frame.**
   The problem is exactly about distances from even composite centers back to
   the previous prime endpoint.

## Primary Obstruction

The even-channel problem is still a global return-time theorem.

Current GWR machinery can analyze the chamber after the endpoints are known.
It does not prove that even centers have previous prime endpoints within
polylogarithmic average distance.

Equivalently, it does not prove the tail bound

$$
\#\{2m\in[X,2X]:2m-p(2m)\ge H\}
\ll
X(\log X)^B/H^2.
$$

This is the deepest obstruction in its stripped-down form.

## Result

The next theorem to attack is:

> **Even-Channel Age Recurrence Theorem.**
> $$
> \sum_{\substack{X<n\le2X\\ 2\mid n}}
> (n-p(n))
> \ll
> X(\log X)^B.
> $$

Proving this theorem closes the dyadic square-moment obstruction. It is the
smallest concrete subproblem currently visible in the endpoint-chain route.
