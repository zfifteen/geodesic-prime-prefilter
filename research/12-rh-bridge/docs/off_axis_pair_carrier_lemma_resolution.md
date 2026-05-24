# Off-Axis Pair Carrier Lemma Resolution

Date: 2026-05-24

The Off-Axis Pair Carrier Lemma is invalidated as stated.

The exact obstruction is that a paired off-axis zero does not require an
additional source-side coefficient field, a failed `D,K,R` identity,
independent endpoint freedom, or a chamber log-weight remainder. It is carried
by the same continued quotient

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The route

```text
off-axis pole -> extra source-side carrier -> no carrier remains -> excluded
```

therefore fails at the first implication.

## Status

| Object | Status |
| --- | --- |
| Local PGS source theorems | Proved in `PROOF.md` under their stated hypotheses. |
| DNI-to-zeta compression | Exact identity on `Re(s)>1`, continued through the zeta identity. |
| Off-Axis Pair Carrier Lemma | Invalidated as stated. |
| Replacement bridge target | Unresolved: a chamber-load spectral-centering theorem. |

This is a proof-state change, not a wording change.

## Exact Source And Quotient

The divisor-count source is

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

The DNI load series satisfies

$$
K(s)=-\frac{1}{e^2}D'(s),
$$

so the normalized quotient is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

These identities are exact. They identify the analytic object, but they do not
place its nontrivial poles.

## Off-Axis Pair Contribution

Assume an off-axis nontrivial zero

$$
\rho=\frac12+a+i\gamma,
\qquad a\neq 0,
$$

with multiplicity `m`. The functional equation and conjugation give the quartet

$$
Q=\{\rho,\bar\rho,1-\rho,1-\bar\rho\}.
$$

The contribution of that quartet to the continued DNI ratio is

$$
R_Q(s)=-m\sum_{\alpha\in Q}\frac{1}{s-\alpha}.
$$

Since $D(s)=\zeta(s)^2$, each zero $\alpha$ of $\zeta$ is a zero of $D$ of
order `2m`. Therefore

$$
-\frac12\frac{D'(s)}{D(s)}
$$

has principal part

$$
-\frac{m}{s-\alpha}
$$

at each $\alpha\in Q$. The off-axis pole is already present in the same exact
quotient. It does not require a second source field.

## Centered Geometry

Let

$$
\Xi(u)=\xi\left(\frac12+u\right).
$$

The completed function is even in the centered coordinate:

$$
\Xi(u)=\Xi(-u).
$$

An off-axis zero corresponds to

$$
\nu=a+i\gamma,
\qquad a\neq 0,
$$

and therefore to the quartet

$$
a+i\gamma,\quad a-i\gamma,\quad -a+i\gamma,\quad -a-i\gamma.
$$

Its multiplicity-`m` contribution to $-\Xi'(u)/\Xi(u)$ is

$$
L_{a,\gamma}(u)
=-m\sum_{\epsilon=\pm1,\eta=\pm1}
\frac{1}{u-(\epsilon a+i\eta\gamma)}.
$$

Equivalently,

$$
L_{a,\gamma}(u)=
-\frac{4m\,u\,(u^2+\gamma^2-a^2)}
{u^4+2(\gamma^2-a^2)u^2+(a^2+\gamma^2)^2}.
$$

In the squared centered coordinate $z=u^2$, a critical-line pair gives only a
real negative pole. An off-axis quartet gives conjugate nonreal `z`-poles:

$$
-m\left(
\frac{1}{z-(a+i\gamma)^2}
+\frac{1}{z-(a-i\gamma)^2}
\right).
$$

Thus the needed placement theorem is exactly:

```text
the PGS source-derived completed logarithmic derivative has only real
negative singularities in z = u^2.
```

That statement is not supplied by functional-equation symmetry. The model
factor

$$
[(u-a)^2+\gamma^2][(u+a)^2+\gamma^2]
$$

is even, real-symmetric, and compatible with the quartet geometry while still
having `a != 0`.

## Explicit-Formula Carrier

On the downstream explicit-formula side, the same quartet contributes

$$
\Psi_Q(x)=
-m\sum_{\alpha\in Q}\frac{x^\alpha}{\alpha}
=
-2m\,\Re\left(
\frac{x^{1/2+a+i\gamma}}{1/2+a+i\gamma}
+\frac{x^{1/2-a+i\gamma}}{1/2-a+i\gamma}
\right).
$$

For `a > 0`, the dominant envelope is order

$$
x^{1/2+a}/|\rho|.
$$

Across a chamber interval `(p,q]`, the same zero-term contributes

$$
\Delta_Q(p,q)=
-m\sum_{\alpha\in Q}\frac{q^\alpha-p^\alpha}{\alpha}.
$$

This is a global log-scale oscillatory carrier of the same quotient. It is not
an extra divisor-count field.

## Exact Failure

The invalid implication is

$$
\text{off-axis pole}
\Longrightarrow
\text{extra source-side carrier}.
$$

The correct statement is:

```text
off-axis pole
-> global singularity of the same continued D,K,R quotient
-> hyperbolic log-scale carrier in the explicit-formula shadow
-> no contradiction unless chamber geometry proves spectral centering
```

The objection that "the whole source sequence carries it" is therefore a real
mathematical objection. It names the analytic continuation of the exact same
source object. It is not merely conclusion-only wording.

## Replacement Theorem

The bridge that would close the RH-facing sentence is:

> **Chamber-Load Spectral Centering Theorem.**
> Decompose the continued DNI quotient
> $$
> R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
> $$
> into the cumulative chamber-load residual determined by zero-excess endpoint
> returns, leftmost minimum-divisor chamber order, and
> $$
> H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
> $$
> After factoring the critical scale $x^{1/2}$, every nontrivial log-scale
> carrier of that residual has real exponent `0`. Equivalently, no
> chamber-load residual contains a term
> $$
> e^{a\log x+i\gamma\log x}
> $$
> with `a != 0`.

Equivalent forms include:

- the completed source-derived logarithmic derivative has only real negative
  singularities in `z = u^2`;
- the PGS chamber-load source proves a square-root-scale bound for the
  downstream Chebyshev residual;
- the PGS chamber-load source supplies a positivity, self-adjointness, or
  de Branges-type kernel strong enough to place all nontrivial poles on
  `Re(s)=1/2`.

Until one of those statements is proved from PGS source structure, the
Off-Axis Pair Carrier route remains invalidated.

The follow-up Chamber-Load Spectral Centering pass is recorded in
[Chamber-Load Spectral Centering Resolution](chamber_load_spectral_centering_resolution.md).
That pass invalidates raw chamber-wise centering and isolates the
Chamber-Deconvolved Reciprocal Balance Lemma as the next non-circular PGS-side
target.

## Subagent Convergence

Four independent subagents were assigned the analytic carrier, functional
equation geometry, PGS chamber-load transmission, and adversarial referee
roles. They converged on the same result:

```text
exact compression is real;
off-axis pairs are compatible with the same quotient;
the current carrier lemma is invalid as stated;
the remaining bridge is chamber-load spectral centering.
```
