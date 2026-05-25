# Four-Tuple Selberg Bound Strategy

Date: 2026-05-24

Status: candidate analytic route for the Four-Tuple Sifted Moment Bound.

The fourth-moment extinction strategy needs uniform upper bounds for up to four
shifted odd linear forms

$$
M-(2s_i+1)
$$

as `M` ranges over even centers in `[X,2X]`. This is a fixed-dimension
Selberg-sieve problem with dimension at most four.

## Local Residue Data

Fix a tuple

$$
\mathbf s=(s_1,\ldots,s_k),
\qquad
k\le 4.
$$

Let `S` be the set of distinct offsets in the tuple and set

$$
r=|S|.
$$

Repeated offsets do not create new linear forms, so the sieve dimension is
`r`, not `k`.

For an odd prime `p`, define

$$
\nu_p(S)=
\#\{2s+1\pmod p:s\in S\}.
$$

This is the number of forbidden residue classes for the even center `M mod p`.
For squarefree odd `d`, define multiplicatively

$$
\nu_d(S)=\prod_{p\mid d}\nu_p(S).
$$

The residue count in the dyadic block is

$$
\#\{M\in[X,2X]:2\mid M,\ M\equiv a\pmod d\}
=
\frac{X}{2d}+O(1)
$$

for each odd modulus `d` and residue class `a`.

Thus the tuple has the standard sieve local density

$$
\frac{\nu_p(S)}p
$$

at each odd prime `p`.

## Singular Series

The singular factor for the distinct offset set `S` is

$$
\mathfrak S(S)=
\prod_{p>2}
\left(1-\frac{\nu_p(S)}p\right)
\left(1-\frac1p\right)^{-r}.
$$

If `nu_p(S)=p` for some odd prime `p`, then every center hits at least one
forbidden class modulo `p`, so the sifted count is zero. In that case the
tuple is inadmissible and contributes nothing.

For admissible tuples, collisions `s_i congruent s_j mod p` increase
`\mathfrak S(S)`. These are exactly the small-prime dependency factors that
must be controlled when the fourth moment is summed over all offset tuples.

## Selberg Upper-Bound Target

Let

$$
\mathcal N_S(X)
$$

be the number of even centers `M in [X,2X]` such that every form

$$
M-(2s+1),
\qquad s\in S,
$$

has no odd divisor `p <= sqrt(2X)`.

The needed fixed-tuple estimate is:

> **Four-Form Selberg Upper Bound.**
> For every distinct offset set `S` with `r <= 4`,
> $$
> \mathcal N_S(X)
> \ll_r
> X\mathfrak S(S)/(\log X)^r
> +E_S(X),
> $$
> where the total contribution of the errors `E_S(X)` over all
> `s_i < N` is absorbed by `X N^r(\log X)^C/(\log X)^r`.

Since `Y=sqrt(2X)`, replacing `log Y` by `log X` changes only the absolute
constant.

## Selberg-Sieve Mechanism

For the set of even centers, the sifted condition is

$$
M\not\equiv 2s+1\pmod p
\qquad
(s\in S,\ p\le Y,\ p\text{ odd}).
$$

Selberg's upper-bound sieve gives

$$
\mathcal N_S(X)
\le
\frac{X}{2G_S(Y)}
+\text{remainder},
$$

where the sieve denominator has dimension `r`:

$$
G_S(Y)
\gg_r
\mathfrak S(S)^{-1}(\log Y)^r.
$$

Therefore

$$
\mathcal N_S(X)
\ll_r
X\mathfrak S(S)/(\log X)^r
+\text{remainder}.
$$

This is exactly the tuple input needed by the fourth-moment note.

## Uniformity Obligations

**Offset size.**
The shifts `2s+1` can range up to the active odd-offset length. The proof must
be uniform for all `0 <= s < N` in the tail range under consideration.

**Dyadic positivity.**
If `M-(2s+1) <= 1`, the form is outside the prime-endpoint regime. These
terms must be removed as boundary contributions before applying the sieve.

**Parity.**
The center `M` is even and all forms are odd. The prime `2` is therefore not a
sieving prime; it contributes a fixed harmless factor.

**Remainder control.**
The product of all prime moduli up to `sqrt X` is too large for direct
periodic counting. The Selberg weights must use a finite level whose remainder
sum is uniform for dimensions `r <= 4`.

**Admissibility zeros.**
If a tuple covers all residues modulo an odd prime, the contribution is zero.
The proof should detect this locally rather than assigning a singular factor
with the wrong sign.

## What Remains After Fixed-Tuple Bounds

The fixed-tuple Selberg upper bound does not by itself prove the fourth moment.
One must still average the singular factors:

$$
\sum_{0\le s_1,\ldots,s_k<N}
\mathfrak S(\{s_1,\ldots,s_k\})
\ll_k
N^k(\log X)^C
\qquad (k\le4).
$$

That average is the next distinct task. It is a finite combinatorial estimate
over offset collisions modulo small primes.

## Result

The Four-Tuple Sifted Moment Bound splits into two clean pieces:

```text
fixed tuple -> Selberg upper-bound sieve with singular factor;
all tuples  -> singular-series average over offset collisions.
```

The fixed-tuple part is a standard dimension-at-most-four upper-bound sieve
shape. The remaining arithmetic burden is uniform remainder control and the
average singular-series estimate over offset tuples.
