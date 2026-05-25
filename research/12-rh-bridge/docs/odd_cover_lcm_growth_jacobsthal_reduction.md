# Odd Cover LCM-Growth Jacobsthal Reduction

Date: 2026-05-24

Status: candidate closure of the Odd Cover LCM-Growth Lemma, conditional on a
Jacobsthal window bound.

The odd-offset cover has a direct combinatorial form. Once a center `2m` has a
complete proper-divisor cover of the odd offsets

$$
1,3,\ldots,2N-1,
$$

the radical of the certificate LCM creates a modulus whose reduced residues
avoid a whole interval of length `N`. That is a shifted Jacobsthal gap.

## Certificate Radical

Let a full cover assign an odd proper divisor

$$
d_j\mid 2m-j
$$

to every odd offset

$$
j=1,3,\ldots,2N-1.
$$

Set

$$
L=\operatorname{lcm}_j d_j,
\qquad
R=\operatorname{rad}(L).
$$

For each covered offset, some prime divisor of `R` divides `2m-j`, so

$$
\gcd(2m-j,R)>1.
$$

Thus the full cover is already controlled by the squarefree odd modulus `R`.
Prime powers in the chosen divisors are irrelevant for coverage; the radical
is the covering object.

## Shift To Consecutive Integers

Write

$$
j=2s+1,
\qquad
0\le s<N.
$$

For each prime `p | R`,

$$
p\mid 2m-(2s+1)
$$

is equivalent to

$$
s\equiv m-2^{-1}\pmod p.
$$

By the Chinese remainder theorem there is a single residue class

$$
a_R\pmod R
$$

with

$$
a_R\equiv m-2^{-1}\pmod p
\qquad (p\mid R).
$$

Therefore the full cover implies

$$
\gcd(s-a_R,R)>1
\qquad
(0\le s<N).
$$

The odd-offset cover is exactly a block of `N` consecutive integers with no
integer coprime to `R`, after a fixed shift.

## Jacobsthal Form

Let `J(R)` be the least integer such that every interval of `J(R)` consecutive
integers contains an integer coprime to `R`. The previous section gives

$$
N < J(R).
$$

Thus a low-LCM full cover can exist only if the squarefree radical `R` has a
large Jacobsthal gap.

The imported analytic input that would close the LCM-growth lemma is:

> **Jacobsthal Window Bound.**
> If `R` is squarefree and has
> $$
> r=\omega(R)
> $$
> distinct prime factors, then
> $$
> J(R)\ll r^2(\log r)^2.
> $$

This is the standard Iwaniec-type Jacobsthal estimate. The source is H.
Iwaniec, "On the problem of Jacobsthal", Demonstratio Mathematica 11:1
(1978), 225-232, DOI: https://doi.org/10.1515/dema-1978-0121.

Combining `N < J(R)` with this estimate gives

$$
r\gg \frac{\sqrt N}{\log N}.
$$

Since the least odd squarefree integer with `r` prime factors is the product
of the first `r` odd primes,

$$
R\ge \prod_{i=1}^{r}p_{i+1}
\ge \exp(c\,r\log r)
$$

for an absolute constant `c > 0` outside a finite base. Hence

$$
R\ge \exp\!\left(c'\frac{\sqrt N}{\log N}\log\frac{\sqrt N}{\log N}\right).
$$

This dominates every fixed power of `N` for large `N`. In particular, after
adjusting the finite base and the logarithmic exponent,

$$
L\ge R\gg \frac{H^2}{(\log X)^B}
$$

for the odd-offset length `H=2N+O(1)` in the regime where the right side is
nontrivial. When `H` is polylogarithmically small, the inequality is absorbed
by the finite base and by choosing `B` large enough.

## Candidate Lemma Closure

The LCM-growth sublemma can therefore be stated in the following conditional
form.

> **Odd Cover LCM-Growth From Jacobsthal.**
> Assume the Jacobsthal Window Bound. Then every complete proper-divisor cover
> of odd offsets of length `H` has full certificate LCM satisfying
> $$
> L\ge cH^2/(\log X)^B
> $$
> after finite-base normalization.

The proof does not need to find a smaller subcertificate. The full certificate
already has large radical. A subcertificate may still be needed later for
entropy or counting, but not for the pure LCM-growth statement.

## What This Does Not Yet Prove

This reduction closes only the LCM-growth obstruction, not the full
Odd Divisor-Covering Tail Theorem.

The remaining counting problem is separate:

```text
large LCM per realized cover
does not by itself bound the number of possible realized cover words.
```

To get the tail

$$
\#\{2m\in[X,2X]:a(2m)\ge H\}
\ll
X(\log X)^B/H^2,
$$

one still needs a canonical-word entropy or compatibility theorem showing that
the union over realized low-density certificates does not erase the `X/L`
saving.

## Principal Obstacles

**Imported theorem status.**
The Jacobsthal bound is not currently proved in `PROOF.md`. If the RH bridge
must remain fully PGS-internal, this becomes a new local theorem obligation:
prove the required shifted Jacobsthal window bound for divisor-channel covers.

**Odd-offset normalization.**
The reduction uses the invertibility of `2 mod R`. This is why the certificate
must use odd divisors. That condition is natural here because the covered
integers `2m-j` are odd.

**Finite-base bookkeeping.**
Small `H`, small `R`, and the previous endpoint at the left boundary must be
handled by an explicit finite-base clause. This is bookkeeping, not the main
obstruction.

**Entropy remains outside the lemma.**
LCM growth says every full cover carries a large modulus. The later tail bound
still requires a deterministic way to count realized certificates or canonical
least-divisor words.

## Result

The Odd Cover LCM-Growth Lemma reduces cleanly to a shifted Jacobsthal window
bound for the radical of the certificate LCM. With the standard Iwaniec
Jacobsthal estimate imported, the LCM-growth portion is closed. Without that
import, the smallest remaining combinatorial obligation is the same
Jacobsthal window bound specialized to PGS odd divisor-channel covers.
