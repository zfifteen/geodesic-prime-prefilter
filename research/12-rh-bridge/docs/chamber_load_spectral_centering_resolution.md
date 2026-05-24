# Chamber-Load Spectral Centering Resolution

Date: 2026-05-24

The Chamber-Load Spectral Centering target is not solved by the current PGS
chamber facts. The target reduces to an RH-equivalent positivity or summatory
bound, and the raw chamber-wise centering route is falsified by the first
nonempty chamber.

This is a proof-state result:

```text
proved: local PGS source theorems
proved: exact DNI-to-zeta compression
invalidated: raw chamber-wise spectral centering
unresolved: deconvolved reciprocal balance / RH-equivalent positivity
```

## Target Under Test

Let

$$
\Xi(u)=\xi\left(\frac12+u\right),
\qquad
z=u^2.
$$

Since $\Xi$ is even, define

$$
\Phi(z)=\Xi(\sqrt z).
$$

Then

$$
\frac{\Phi'(z)}{\Phi(z)}
=\frac{1}{2u}\frac{\Xi'(u)}{\Xi(u)}.
$$

The positive Stieltjes form of the desired centering theorem is:

$$
\frac{1}{2u}\frac{\Xi'(u)}{\Xi(u)}
=
\sum_{\gamma>0}\frac{m_\gamma}{z+\gamma^2}.
$$

This representation places all singularities at real negative points
`z = -gamma^2`. Equivalently, the zeros of $\Xi(u)$ are purely imaginary and
the zeros of $\zeta(s)$ lie on `Re(s)=1/2`.

Conversely, RH gives the Hadamard product

$$
\Xi(u)=\Xi(0)\prod_{\gamma>0}
\left(1+\frac{u^2}{\gamma^2}\right)^{m_\gamma},
$$

and therefore gives the same Stieltjes representation. Thus the Stieltjes
version of Chamber-Load Spectral Centering is RH-equivalent. It is not a
weaker intermediate lemma.

Equivalent forms include:

- $\Phi'(z)/\Phi(z)$ is a Stieltjes transform with positive discrete measure
  supported on `[0,infinity)`;
- $\Xi$ belongs to the relevant Laguerre-Polya real-zero class in the centered
  coordinate;
- all Li coefficients are nonnegative;
- the Weil quadratic form is positive for all admissible test functions;
- the downstream Chebyshev function satisfies an RH-strength bound such as
  $$
  \psi(x)-x=O_\varepsilon(x^{1/2+\varepsilon})
  $$
  for every $\varepsilon>0$.

## What The Current PGS Source Proves

The local source layer proves:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n,
$$

and, for `n > 1`,

$$
E(n)=0 \iff \tau(n)=2.
$$

Given a known prime `p`,

$$
q=\min\{n>p:E(n)=0\}.
$$

Inside a nonempty chamber, the selected interior integer is the leftmost
minimum-divisor integer, equivalently the leftmost minimum of $E(n)$.

The bridge load is exact:

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

The zeta compression is exact:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
$$

$$
B(s)=\sum_{n\ge1}\frac{H(n)}{n^s}
=-\frac12D'(s),
$$

and

$$
R(s)=\frac{B(s)}{D(s)}
=-\frac12\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

These statements identify the source and the quotient. They do not prove that
the completed quotient has centered spectral placement.

## Raw Chamber Centering Fails

The first nonempty chamber is

$$
p=3,\qquad q=5,\qquad I=\{4\}.
$$

Center it in log scale:

$$
t_n=\log n-\frac{\log p+\log q}{2}
=\log\frac{n}{\sqrt{pq}}.
$$

For `n = 4`, $\tau(4)=3$, so

$$
E(4)=\log 2,
\qquad
t_4=\log\frac{4}{\sqrt{15}}>0.
$$

A chamber-local centered spectral block would require the first odd centered
moment to vanish:

$$
M_1=\sum_{n\in I}E(n)t_n=0.
$$

But here

$$
M_1=\log 2\cdot\log\frac{4}{\sqrt{15}}>0.
$$

Numerically,

```text
M1 = 0.02236734698200787
```

So the route

```text
each raw chamber block is already centered
```

is false.

Plain finite Gram or Hankel positivity also does not solve the target. With
positive weights such as $E(n)$ or $H(n)$, matrices of the form

$$
G_{ij}=\sum_{n\in I}E(n)t_n^{i+j}
$$

are positive semidefinite because they are moment matrices of positive finite
measures. That positivity is too weak: it does not force singular support to
lie on the real negative `z` axis.

## Deconvolution Is The Actual Hinge

The quotient is not a raw chamber sum. It is the ratio

$$
R(s)=\frac{B(s)}{D(s)}.
$$

Let `lambda` be the Dirichlet-deconvolved coefficient sequence:

$$
\sum_{n\ge1}\frac{\lambda(n)}{n^s}
=
\frac{B(s)}{D(s)}.
$$

Since

$$
\frac{B(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)},
$$

the deconvolved chamber-load coefficients are exactly

$$
\lambda(n)=\Lambda(n).
$$

A direct finite check through `n = 16` gives exact agreement:

| `n` | `lambda(n)` | `Lambda(n)` |
| --- | --- | --- |
| 2 | `log 2` | `log 2` |
| 3 | `log 3` | `log 3` |
| 4 | `log 2` | `log 2` |
| 5 | `log 5` | `log 5` |
| 6 | `0` | `0` |
| 8 | `log 2` | `log 2` |
| 9 | `log 3` | `log 3` |
| 16 | `log 2` | `log 2` |

Thus any viable chamber-load centering proof must survive this step:

```text
raw chamber load H
-> Dirichlet deconvolution by D
-> Lambda
-> completion and removal of main/trivial terms
-> reciprocal-balanced positive kernel in z = u^2
```

The balance cannot be read off from raw finite chambers.

## Explicit-Formula Form

The downstream chain is

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n\ge1}\frac{\Lambda(n)}{n^s},
\qquad
\psi(x)=\sum_{n\le x}\Lambda(n).
$$

The explicit formula has the schematic form

$$
\psi(x)=x-\sum_\rho\frac{x^\rho}{\rho}+\text{elementary terms}.
$$

For an off-axis quartet

$$
\rho=\frac12+a+i\gamma,
\qquad a\ne0,
$$

factoring out $x^{1/2}$ leaves log-scale carriers

$$
e^{a\log x+i\gamma\log x}
\quad\text{and}\quad
e^{-a\log x+i\gamma\log x}.
$$

Therefore Chamber-Load Spectral Centering is equivalent to proving that no
nontrivial carrier with real exponent `a != 0` remains after completion.

In summatory language, this is an RH-strength theorem:

$$
\text{PGS chamber-load structure}
\Longrightarrow
\psi(x)-x=O_\varepsilon(x^{1/2+\varepsilon}).
$$

The current local chamber facts do not supply that cancellation estimate.

## Smallest Remaining PGS-Side Lemma

The smallest non-circular PGS-side target located by this pass is:

> **Chamber-Deconvolved Reciprocal Balance Lemma.**
> Let $\lambda=\tau_{\mathrm{Dir}}^{-1}*H$, so that
> $$
> \sum_{n\ge1}\lambda(n)n^{-s}=R(s).
> $$
> After completion and removal of the main and trivial terms, the
> deconvolved chamber residual decomposes into folded log-coordinate blocks
> whose mass is reciprocal-balanced and nonnegative in the `z=u^2`
> coordinate.

This is sharper than simply saying "prove RH" because it names the exact point
where PGS data must survive:

```text
through Dirichlet deconvolution,
through completion,
through main/trivial-term removal,
into a reciprocal-balanced positive z-kernel.
```

No current artifact proves that lemma.

## Proof-State Result

The Chamber-Load Spectral Centering target is unresolved.

The raw chamber-wise version is invalidated by the first nonempty chamber.
The Stieltjes, Laguerre-Polya, Li, Weil, de Branges, and explicit-formula
versions are RH-equivalent.

The next valid attack is not more RH-facing prose. It is the
[Chamber-Deconvolved Reciprocal Balance Lemma](chamber_deconvolved_reciprocal_balance_lemma.md).
