# Source Order

The object starts with divisor counts and prime-gap interiors because those are
the integer records that exist before any zeta or RH vocabulary is introduced.

The required order is:

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> source-to-spectral placement target
-> pole placement/RH sentence
```

## Arithmetic Objects First

Every positive integer has a divisor count. The zero-excess coordinate is

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For an integer `n > 1`, the prime state is the exact zero-excess return

$$
E(n)=0 \iff \tau(n)=2.
$$

Given a known prime `p`, the next prime `q` is the first later integer whose
zero-excess coordinate returns to `0`:

$$
q=\min\{n>p:E(n)=0\}
=\min\{n>p:\tau(n)=2\}.
$$

The integers between `p` and `q` form a finite ordered interior:

$$
I=\{p+1,\ldots,q-1\}.
$$

Each integer in that interior is composite, so each has positive excess. The
first location where the smallest interior divisor count occurs is the same
location where the smallest positive excess occurs:

$$
w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.
$$

These are the source objects: the divisor-count field, zero-excess returns,
the finite prime-gap interior, and the selected integer inside that interior.

## Local Theorem Authority

[PROOF.md](../../PROOF.md) controls local theorem status.

It proves two local PGS statements under their stated hypotheses:

| Statement | Status |
| --- | --- |
| Exact divisor-count traversal after a known prime returns the next prime, equivalently the next `n > p` with `E(n)=0`. | proved theorem |
| In a nonempty gap interior, the leftmost integer with minimum divisor count is the unique maximizer of `F(n)=(1-tau(n)/2)log(n)`. Since `F(n)=-E(n)`, this is the leftmost argmin of `E(n)`. | proved theorem |

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

In zero-excess notation, the bridge load is preserved as

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Equivalently, `H(n)=log n+E(n)=tau(n)log(n)/2`.

The numerator bridge is the `H(n)` load, equivalently the scaled
divisor-normalization load. It is not `E(n)` alone.

The bridge gives the exact compression

$$
\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

This layer has status: exact zeta compression.

## Source-Side Residual Target

After exact compression, the review question remains source-side. The current
residual test rules out bookkeeping failures in the bridge:

- a failed identity in `D,K,R`;
- independent endpoint or gap-length freedom;
- a chamber log-weight remainder;
- an additional divisor-count field.

[Off-critical pole exclusion](off-critical-pole-exclusion.md) records the
residual test and its current obstruction. The no-extra-carrier step does not
yet prove pole placement, because off-axis zeros of $\zeta(s)$ would be global
analytic properties of the same zeta-compressed source, not necessarily signs
of an extra source object.

This layer has status: unresolved proof target. Zero-excess is the integer-side
source coordinate used to name prime returns and chamber minimizers; it does
not by itself constrain the nontrivial pole locations of the continued DNI
ratio.

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
the unresolved source-to-spectral bridge. The RH sentence is the corresponding
analytic coordinate sentence:

all nontrivial poles of the continued DNI ratio lie on the critical line
`Re(s)=1/2`.

The zero-excess floor is integer-side. The critical line is zeta-side. The
analogy is permitted; identity is not.

Status: unresolved source-to-spectral placement target.

## Reading Rule

For this bundle, RH language enters after the ordered integer field:

1. divisor counts;
2. zero-excess returns with the `n > 1` prime guard;
3. local theorems for next-prime traversal and leftmost minimum-excess
   selection;
4. the exact DNI-to-zeta ratio with bridge load
   `H(n)=log n+E(n)=tau(n)log(n)/2`;
5. the source-side residual test and its current obstruction;
6. pole-placement/RH language.

This keeps the arithmetic source, local theorem status, exact compression, and
source-to-spectral target in their proper order. The explicit-formula bridge is
downstream translation, but an RH-strength placement theorem or equivalent
analytic constraint is still missing.

Back to the [bundle index](README.md).
