# Off-Critical Pole Exclusion Status

The arithmetic source is the divisor-count field $\tau(n)$.

Define the zero-excess coordinate by

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For each integer `n > 1`, prime return means $E(n)=0$, equivalently
$\tau(n)=2$. Given a known prime `p`, the next endpoint is fixed by the first
later return to that value:

$$
q=\min\{n>p:E(n)=0\}
=\min\{n>p:\tau(n)=2\}.
$$

Between consecutive endpoints, the chamber interior is the finite ordered set

$$
I=\{p+1,\ldots,q-1\}.
$$

Inside a nonempty chamber, the local PGS theorem controlled by
[PROOF.md](../../PROOF.md) selects the leftmost minimum-divisor integer and
orders the chamber by

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

Since $F(n)=-E(n)$, the same source theorem says the selected integer is the
leftmost argmin of $E(n)$ in the chamber interior.

So the source order is fixed before any analytic vocabulary enters:

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> source-to-spectral placement target
-> pole placement/RH sentence
```

## The Objection

The critic says the exact source may still carry nontrivial off-critical poles
as a global property of the whole $\tau(n)$ sequence, even if no separate local
carrier is named. In that form, the objection accepts the divisor-count source,
the local PGS closures, and the DNI identities, but says that the continued
quotient might still have poles off $\mathrm{Re}(s)=1/2$ because the full
source sequence could carry them globally.

## Exact DNI Quotient

The divisor-count compression is

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The DNI load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2},
$$

with Dirichlet series

$$
K(s)=\sum_{n \ge 1}\frac{\kappa(n)}{n^s}.
$$

In zero-excess notation, the bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Equivalently, `H(n)=log n+E(n)=tau(n)log(n)/2`.

The zero-excess coordinate names the integer-side return and chamber
minimizer. It does not replace the `D,K,R` quotient, and it does not create a
new residual category.

Since

$$
D'(s)=-\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s},
$$

the DNI load satisfies

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

At the repository normalization $v=e^2/2$, the continued DNI ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The quotient is a function quotient after the two Dirichlet series have been
formed. It is not coefficientwise division.

## Local Pole Mechanism

Let $\rho$ be a zero of $\zeta(s)$ of multiplicity $m$. Locally write

$$
\zeta(s)=(s-\rho)^m g(s),
$$

where $g(\rho)\neq 0$.

Then

$$
\frac{\zeta'(s)}{\zeta(s)}
=\frac{m}{s-\rho}+\frac{g'(s)}{g(s)}.
$$

Therefore

$$
-\frac{\zeta'(s)}{\zeta(s)}
=-\frac{m}{s-\rho}-\frac{g'(s)}{g(s)}.
$$

The term $g'(s)/g(s)$ is holomorphic at $\rho$. The term $m/(s-\rho)$ has a
pole at $\rho$. Thus zeros of $\zeta(s)$ become poles of the continued DNI
ratio $R(s)$.

The exclusion question is therefore source-side and exact: what source
residual could carry a nontrivial pole of $R(s)$ away from
$\mathrm{Re}(s)=1/2$?

## Source-Side Residual Test

The residual test identifies the places where a bookkeeping or source-object
failure could enter the bridge:

| Residual category | Source-side test | Status in source order |
| --- | --- | --- |
| 1. Failed identity in $D,K,R$ | The compression would need $D(s)\neq\zeta(s)^2$, $K(s)\neq-D'(s)/e^2$, or $R(s)\neq-\zeta'(s)/\zeta(s)$. | Closed by exact identities. |
| 2. Independent prime-gap or gap-length freedom | The endpoint sequence would need degrees of freedom not fixed by $\tau(n)=2$ returns. | Closed by endpoint closure: $q=\min\{n>p:\tau(n)=2\}$ fixes every next endpoint from the divisor-count field. |
| 3. Chamber log-weight residual | The chamber ordering would need a log-weight term outside the DNI load. | Closed by the PGS chamber order and derivative identity: the log-weight source is $\tau(n)\log n$, equivalently $H(n)=\log n+E(n)=\tau(n)\log n/2$ after scaling, and that source is exactly the numerator load $K(s)=-D'(s)/e^2$. |
| 4. Multiplicative or divisor-count residual | The factor-pair source would need an additional multiplicative coefficient field outside $\tau(n)$. | Closed by $D(s)=\zeta(s)^2$: the ordered factor-pair count is exactly $\tau(n)$, and the quotient $K(s)/D(s)$ exhausts the divisor-count source used by the bridge. |
| 5. Global analytic carrier in the same source | The critic says the whole $\tau(n)$-generated zeta object could carry off-critical zeros after analytic continuation. | Live obstruction. This is a mathematical objection, not a conclusion-only residual. |

The first four categories are closed as bridge bookkeeping. They show that the
DNI compression uses the intended divisor-count source and no extra numerator
or endpoint field.

The fifth category is the remaining proof target. Zeros of a continued
Dirichlet series need not come from an additional coefficient field. They can
arise from global cancellation and analytic continuation of the same source
object. Therefore "the whole sequence carries it" is an actual analytic
obstruction to the no-extra-carrier proof route.

## Current Obstruction

After the local PGS source closures and the exact DNI compression, the
continued ratio is exactly

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

An off-critical pole would be a pole of this exact quotient. That does not
force a failed identity, an independent gap-length freedom, a chamber
log-weight remainder, or an additional divisor-count field. It can be a global
zero of the same $\zeta(s)$ whose square is generated by $\tau(n)$.

So the positive source-side bridge currently proves:

```text
tau(n) fixes prime returns -> endpoint closure fixes gap lengths
-> chamber order fixes the log-weight source
-> DNI quotient uses exactly tau(n) and H(n)=log n+E(n)=tau(n)log(n)/2
-> R(s)=-zeta'(s)/zeta(s)
```

It does not yet prove:

```text
paired off-axis zero -> impossible source-side carrier
```

The missing step is a **source-first** summatory law (if any) that, after exact
compression, forces a reading of continued $R$. That reading may coincide with
pole placement. Designing backward from pole placement into chamber geometry
is frame-wrong (see `research/19-rh-corpus/FRAME_CONTRACT.md`).

**Partial progress (2026-06).** For the dominant d=4 GWR carrier class,
proved corollaries now supply a gap-dependent fractional-position bound and
closure before the prime-square threat. See
[`d4_fractional_position_bound.md`](../../research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md)
and the [status ledger](status-ledger.md) d=4 section. This discharges part of
the draft transfer-lemma input; it does not close off-critical pole exclusion.

The current obstruction is recorded in
[Off-Axis Pair Carrier Lemma Resolution](../../research/12-rh-bridge/docs/off_axis_pair_carrier_lemma_resolution.md).

## Links

- [RH bundle README](README.md)
- [Source order](source-order.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Pole placement](pole-placement.md)
- [Critical line and zero geometry](critical-line-and-zero-geometry.md)
- [Root proof authority](../../PROOF.md)
