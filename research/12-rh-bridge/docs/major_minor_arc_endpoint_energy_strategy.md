# Major-Minor Arc Endpoint Energy Strategy

Date: 2026-05-24

Status: candidate Fourier strategy for the centered four-point endpoint energy.

The centered endpoint four-energy can be attacked by decomposing the
kernel-smoothed endpoint Fourier transform into major and minor arcs. The goal
is to prove the `L^2` convolution bound that gives the short-interval fourth
moment.

## Fourier Target

Let

$$
G_N(M)=
\sum_n\left(1_{\mathbb P}(n)-\frac1{\log X}\right)K_N(M-n),
$$

where

$$
K_N(t)=1_{0<t<2N}.
$$

On a finite cyclic model of length comparable to `X`,

$$
\widehat{G_N}(\alpha)=
\widehat b_X(\alpha)\widehat K_N(\alpha).
$$

The target is

$$
\|G_N\|_4^4
\asymp
\|\widehat G_N*\widehat G_N\|_2^2
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

Thus one must control the additive convolution of

$$
\widehat b_X(\alpha)\widehat K_N(\alpha).
$$

## Arc Decomposition

Choose major arcs around rationals

$$
\alpha=\frac aq+\beta,
\qquad
q\le Q_0,
\qquad
|\beta|\le \frac{Q_0}{X},
$$

with `Q_0` a polylogarithmic or small power threshold selected to match the
available prime exponential-sum estimates.

The interval kernel satisfies

$$
|\widehat K_N(\alpha)|
\ll
\min(N,\|\alpha\|^{-1}).
$$

Thus frequencies farther than `1/N` from a major rational are damped by the
kernel.

## Major Arc Input

On major arcs, one needs an asymptotic for the centered endpoint exponential
sum

$$
\widehat b_X(a/q+\beta)
=
\sum_n\left(1_{\mathbb P}(n)-\frac1{\log X}\right)
e(n(a/q+\beta)).
$$

The `q=1` main density is removed by the subtraction `1/log X`. For `q>1`,
the remaining major-arc structure records prime distribution in residue
classes modulo `q`.

The required major-arc theorem is:

```text
major arc contribution = diagonal plus local singular terms
                         + acceptable error;
after centering, the total contribution is Poisson-size.
```

Analytically, this asks for PNT-in-arithmetic-progressions strength for
`q <= Q_0`, with enough uniformity to insert the kernel and then square the
Fourier convolution.

## Minor Arc Requirement

On the minor arcs, the needed estimate is an endpoint exponential-sum bound
strong enough that

$$
\left\|
\left(\widehat b_X\widehat K_N\right)_{\mathfrak m}
*
\left(\widehat b_X\widehat K_N\right)
\right\|_2^2
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

A sufficient input is a large-sieve or Vaughan-type bound for

$$
\sum_{n\le X}
\left(1_{\mathbb P}(n)-\frac1{\log X}\right)e(\alpha n)
$$

on minor arcs, combined with the `L^2` and decay properties of
`\widehat K_N`.

The estimate must be uniform in the nontrivial range of `N`.

## Candidate Mechanism

1. **Major arcs.**
   Use residue-class prime asymptotics to compute the local contribution of
   `q <= Q_0`. Verify that the centered density removes the independent main
   term and leaves only diagonal/singular contributions at Poisson scale.

2. **Minor arcs.**
   Apply a prime exponential-sum estimate to `b_X`, then use kernel decay to
   control the convolution norm.

3. **Boundary and parity.**
   Work on the odd endpoint sequence and even center lattice. The prime `2`
   is removed as a finite contribution; odd moduli carry the live structure.

## Principal Obstacles

**Unweighted endpoint sums.**
Classical exponential-sum technology is cleaner for `Lambda(n)` than for
`1_P(n)`. Passing from weighted to unweighted endpoints requires partial
summation and prime-power control.

**Major-arc singular structure.**
Subtracting `1/log X` removes only the uniform density. Major arcs with
`q>1` still carry residue-class structure that must combine into the correct
singular/diagonal terms rather than being bounded crudely.

**Minor-arc strength.**
The minor-arc bound must remain strong after multiplication by the interval
kernel and convolution with itself.

**Uniformity in `N`.**
The kernel changes the effective frequency support. The arc width and minor
arc estimates must be compatible with all nontrivial `N <= X/2`.

**Dyadic finite model.**
Fourier analysis on a finite cyclic model introduces boundary terms. These
must be kept below the fourth-moment target.

## Minimal Major-Minor Lemma

The needed analytic input is:

> **Centered Endpoint Major-Minor Lemma.**
> For the centered endpoint weight `b_X` and interval kernel `K_N`,
> $$
> \|(\widehat b_X\widehat K_N)*(\widehat b_X\widehat K_N)\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C
> $$
> after separating major and minor arcs as above.

Equivalently, the centered four-point endpoint energy has Poisson-size
growth.

## Result

The major-minor route reduces the endpoint concentration problem to two
analytic inputs: residue-class control on major arcs and strong minor-arc
exponential-sum dispersion for the centered unweighted endpoint sequence,
both compatible with the interval kernel at scale `N`.
