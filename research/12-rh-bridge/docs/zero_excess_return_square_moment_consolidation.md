# Zero-Excess Return Square-Moment Consolidation

Date: 2026-05-24

Status: consolidation note for the endpoint-chain obstruction.

The endpoint-side work has now reduced three independent routes to the same
global arithmetic principle: a square-moment bound for zero-excess return
times.

## Common Target

For consecutive prime endpoints `p < q`, write

$$
g(q)=q-p.
$$

The common target is:

> **Zero-Excess Return Square-Moment Principle.**
> For every dyadic block `[X,2X]`,
> $$
> \boxed{
> \sum_{X<q\le2X}g(q)^2
> \le
> C X(\log X)^B.
> }
> $$

Equivalently, the reciprocal gap-energy sum converges:

$$
\sum_q\frac{g(q)^2\log q}{q^2}<\infty.
$$

This is a global return-time theorem for the zero-excess endpoint chain.

## Route 1: Endpoint Occupancy

The endpoint log-gap summatory law needs the right-endpoint samples

$$
\sum_{q\le X}g(q)\frac{\log q}{q}
$$

to have the same finite part as

$$
\sum_{2<n\le X}\frac{\log n}{n}.
$$

The sampling error is controlled by

$$
\sum_q\frac{g(q)^2\log q}{q^2}.
$$

Thus endpoint occupancy reduces to reciprocal gap-energy convergence, hence
to the square-moment principle.

## Route 2: Persistence Energy

Define zero-excess age

$$
a(n)=n-p(n).
$$

Inside a chamber of width `g`, accumulated age is quadratic:

$$
\sum_{j=1}^{g-1}j=\frac{g(g-1)}2.
$$

The age-divisor recurrence potential

$$
\Phi(n)=a(n)(\tau(n)-2)
$$

dominates age inside every positive-excess chamber. A dyadic bound on

$$
\sum_{X<n\le2X}\Phi(n)
$$

would imply the square-moment principle.

Thus the persistence route also reduces to the same dyadic gap-square bound.

## Route 3: Modulus-Link / Endpoint-Lattice Closure

For a divisor channel `d`, define lattice crossing energy

$$
\mathfrak C_d(X)
=
\sum_{X<q\le2X}
\sum_{\substack{1\le j<g(q)\\ p(q)+j\equiv0\pmod d}}
j.
$$

For `d = 2`, every odd prime gap has even width `g=2h`, and the even-channel
crossing energy is

$$
\mathfrak C_2(X)
=
\frac14
\sum_{X<q\le2X}g(q)^2
$$

up to boundary exceptions.

Thus endpoint-lattice closure also requires the square-moment principle before
uniform growing-modulus issues even enter.

## Minimal New Principle

The minimal new global arithmetic principle is therefore not a selector
refinement, not an alpha-normalization rule, and not a local packet dominance
lemma.

It is:

```text
zero-excess return times have dyadic square moment O(X log^B X).
```

This principle would supply:

- reciprocal endpoint occupancy;
- finite endpoint drift counterterm;
- the first global input for the Chamber-Centered Von Mangoldt Finite-Part
  Principle;
- the endpoint-chain energy needed by divisor-channel and modulus-link
  formulations.

## What It Does Not Yet Close

The square-moment principle is necessary for the endpoint-chain side. It does
not by itself prove the full Chamber-Centered Von Mangoldt finite part.

After it is proved, the remaining tasks are still:

- nonlinear endpoint kernel remainder control;
- interior prime-power compensation;
- identification of the combined finite part with the centered digamma value;
- canonical distribution of any sign-regularized alpha split.

But without the square-moment principle, all current endpoint-side routes stop
at the same obstruction.

## Proof-State Result

The live endpoint-chain theorem obligation is now:

> **Zero-Excess Return Square-Moment Theorem.**
> Consecutive zero-excess endpoint returns satisfy
> $$
> \sum_{X<q\le2X}(q-p(q))^2
> \ll
> X(\log X)^B.
> $$

This theorem is global. It is not currently supplied by `PROOF.md`, the GWR
selector theorem, zero-excess coordinate reformulation, grammar/motif measured
surfaces, or RSA modulus-link experiments.
