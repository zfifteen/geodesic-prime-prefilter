# Source Order

The object starts with divisor counts and prime-gap interiors because those are
the integer records that exist before any zeta or RH vocabulary is introduced.

The required order is:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

## Arithmetic Objects First

Every positive integer has a divisor count. For an integer `n > 1`, the prime
state is the exact condition

$$
\tau(n)=2.
$$

Given a known prime `p`, the next prime `q` is the first later integer whose
divisor count returns to `2`:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

The integers between `p` and `q` form a finite ordered interior:

$$
I=\{p+1,\ldots,q-1\}.
$$

Each integer in that interior is composite, so each has divisor count greater
than `2`. The first location where the smallest interior divisor count occurs
is the selected integer:

$$
w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.
$$

These are the source objects: the divisor-count field, the return to
`tau=2`, the finite prime-gap interior, and the selected integer inside that
interior.

## Local Theorem Authority

[PROOF.md](../../PROOF.md) controls local theorem status.

It proves two local PGS statements under their stated hypotheses:

| Statement | Status |
| --- | --- |
| Exact divisor-count traversal after a known prime returns the next prime. | proved theorem |
| In a nonempty gap interior, the leftmost integer with minimum divisor count is the unique maximizer of `F(n)=(1-tau(n)/2)log(n)`. | proved theorem |

Those theorems fix the arithmetic side of the bundle. If another document
speaks about local PGS theorem status differently, `PROOF.md` controls.

## DNI-To-Zeta Compression

The next layer compresses the same divisor-count source into zeta language.
The bridge document is
[DNI-to-Zeta Compression and the Riemann Hypothesis](../../research/12-rh-bridge/docs/dni_rh_bridge.md).

Start with the divisor-count Dirichlet series on `Re(s)>1`:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

Use the DNI divisor-normalization load

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}
$$

and its series

$$
K(s)=\sum_{n\ge1}\frac{\kappa(n)}{n^s}.
$$

The bridge gives the exact compression

$$
\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

This layer has status: exact zeta compression.

## Source-Side Residual Closure

After exact compression, the review question remains source-side. A nontrivial
off-critical pole of the continued ratio would need a surviving source
residual in the exact quotient:

- a failed identity in `D,K,R`;
- independent endpoint or gap-length freedom;
- a chamber log-weight remainder;
- an additional divisor-count field;
- or a conclusion-only assertion that names no carrier.

[Off-critical pole exclusion](off-critical-pole-exclusion.md) records the
residual test. The first four categories are closed by the source order and the
exact DNI quotient. The fifth is not a mathematical objection because it
restates the negation of the RH pole-placement sentence without identifying a
source object that can carry it.

This layer has status: source-side residual closure.

## Pole Placement Downstream

After continuation, the normalized DNI ratio is the classical zeta logarithmic
derivative:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The poles of `R(s)` record the zeros and pole of `zeta(s)`. The prime-number
theorem pole at `s=1`, the trivial zero poles, and the nontrivial zero poles
are analytic features of the compressed object.

That makes pole placement a downstream reading of the arithmetic source and
source-side residual closure. The RH sentence is the corresponding analytic
coordinate sentence:

all nontrivial poles of the continued DNI ratio lie on the critical line
`Re(s)=1/2`.

Status: source-side residual closure read in pole-placement language.

## Reading Rule

For this bundle, RH language enters after the ordered integer field:

1. divisor counts;
2. prime returns at `tau=2`;
3. prime-gap interiors;
4. the leftmost minimum-divisor selected integer;
5. the exact DNI-to-zeta ratio;
6. the source-side residual test;
7. pole-placement/RH language.

This keeps the arithmetic source, local theorem status, exact compression, and
source-side residual closure in their proper order. PGS is not an analytical
method, and the explicit-formula bridge is downstream translation, not a
prerequisite for the PGS-to-RH path.

Back to the [bundle index](README.md).
