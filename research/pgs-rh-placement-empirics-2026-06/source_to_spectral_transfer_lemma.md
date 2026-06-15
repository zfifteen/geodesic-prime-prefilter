# Source-to-Spectral Transfer Lemma (Draft)

**Date**: 2026-06-15  
**Status**: Draft lemma statement with proof strategy. Not proved. Not RH.

This note names the first PGS-native bridge from chamber geometry to an
RH-strength summatory constraint on the continued DNI ratio. It is downstream
of `PROOF.md` local theorems and exact DNI compression.

---

## 1. Source objects (integer side)

For consecutive primes `p < q`, define the chamber interior

$$
I(p,q)=\{p+1,\ldots,q-1\}.
$$

Skip empty chambers (`q = p + 1`).

Zero-excess coordinate:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

GWR carrier (proved Interior Maximizer Theorem):

$$
w(p,q)=\min\{n\in I(p,q):\tau(n)=\min_{m\in I(p,q)}\tau(m)\}.
$$

Chamber invariants:

$$
B(p,q)=\sum_{n\in I(p,q)} E(n),
\qquad
\delta(p,q)=\log\frac{q}{p},
$$

$$
\mathrm{frac\_pos}(p,q)=\frac{w(p,q)-p}{q-p}\in(0,1).
$$

Packet label at the carrier:

$$
\mathrm{packet}(p,q)=\mathrm{classify}(\tau(w(p,q)),\,w(p,q)).
$$

Dominant class in measured regimes: `d4_semiprime`.

---

## 2. Spectral object (compressed side)

DNI compression (exact on `Re(s)>1`, continued through zeta):

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
$$

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2},
\qquad
B(s)=\sum_{n\ge1}\frac{H(n)}{n^s}=-\frac12 D'(s),
$$

$$
R(s)=\frac{B(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)}.
$$

Downstream Chebyshev function:

$$
\psi(x)=\sum_{n\le x}\Lambda(n).
$$

For a nontrivial zero $\rho=\tfrac12+a+i\gamma$ with $a\neq0$, the explicit
formula contributes the log-scale carrier $x^\rho/\rho$; after factoring
$x^{1/2}$, the obstruction is a term $x^{a+i\gamma}$ with $a\neq0$.

The placement target requires proving no such carrier survives after
deconvolution and completion.

---

## 3. Per-chamber kernel model

Fix a smooth test weight $\Phi$ with compact Fourier support (classical
explicit-formula normalization). For chamber $(p,q)$ define the **chamber
kernel increment**

$$
\mathcal{K}(p,q;\Phi)
=
\sum_{n\in I(p,q)} H(n)\,\Phi\!\left(\frac{\log n-\log\sqrt{pq}}{\delta(p,q)}\right)\,
\frac{\Lambda(n)}{n^{1/2}}
$$

and the **centered chamber moment**

$$
M_1(p,q)=\sum_{n\in I(p,q)} E(n)\left(\log n-\frac{\log p+\log q}{2}\right).
$$

Remarks:

- $\mathcal{K}$ is a model per-chamber contribution to a smoothed
  $\psi(x)-x$ block, not the raw finite chamber sum (deconvolution is
  mandatory).
- $M_1$ is the raw first centered moment; it need not vanish per chamber
  (falsified already at $p=3,q=5$). The transfer uses **left bias** and
  **budget**, not per-chamber centering.

---

## 4. Proved local inputs

See `d4_fractional_position_bound.md` for full proofs.

| Input | Status |
| --- | --- |
| $T(4,5)=4$, $p>4 \Rightarrow p^1>2^2$ | **Proved** (`PGS/Placement.lean`) |
| First interior $\tau=4$ when $\tau(w)=4$ | **Proved** (GWR prefix exclusion) |
| Closure $q\le S_+(w)$ for $\tau(w)=4$ | **Proved** (suffix exclusion) |
| Combined bound $\mathrm{frac\_pos}\le\min(R_{SDA}(p)/g,\,1-m/g)$ | **Proved** (algebra + SDA) |
| Pointwise $\mathrm{frac\_pos}\le 1/2$ | **Invalidated** (8505 d=4 chambers at $10^6$) |

**Measured invariants (reproducible).** `pgs_chamber_budget_summary_1000000.md`;
structural falsification: `pgs_d4_frac_pos_falsification_1000000.json` (0 structural
violations on 58,304 d=4 chambers at $10^6$) and
`pgs_d4_frac_pos_falsification_10000000.json` (0 structural violations on 499,896
d=4 chambers at $10^7$).

---

## 5. Draft transfer lemma

> **Lemma (Chamber-Invariants-to-Kernel-Discrepancy, draft).**  
> There exist absolute constants $C_1>0$, $C_2>0$, $C_3>0$ such that for
> every nonempty d=4 chamber $(p,q)$ with offsets $r=w-p$, $m=q-w$, $g=q-p$,
> and analytic arrival envelope $R_{SDA}(p)$:
>
> $$
> \left|\mathcal{K}(p,q;\Phi)\right|
> \le
> C_1\,B(p,q)\,\exp\!\Big(-C_2\,\min\!\big(R_{SDA}(p)/g,\,1-m/g\big)\Big)
> + C_3\,\mathbf{1}_{\mathrm{packet}=d4\_semiprime}\,\delta(p,q)^{3/2}.
> $$
>
> Summing over chambers with $p\le x$:
>
> $$
> \sum_{p<q\le x}
> \left|\mathcal{K}(p,q;\Phi)\right|
> =
> O_\Phi\!\left(x^{1/2}\log x\right).
> $$

**Interpretation (not yet proved).**

- $B(p,q)$ grows linearly with gap length in measured regimes, so total mass
  is controlled by additive excess budget, not by unconstrained oscillation.
- Left bias uses the **proved gap-dependent** bound
  $\mathrm{frac\_pos}\le\min(R_{SDA}(p)/g,\,1-m/g)$ (mean $\approx 0.33$ at
  $10^6$), yielding exponential savings via
  $\exp(-C_2\cdot\min(R_{SDA}(p)/g,\,1-m/g))$.
- d=4 semiprime dominance ($\approx 74\%$ of carriers) pairs the endpoint clock
  $q\le S_+(w)$ (proved) with Short Divisor-Average left arrival. A uniform
  $\mathrm{frac\_pos}\le\frac12$ is **invalidated** (8,505 d=4 counterexamples
  at $10^6$).

**Placement consequence (target corollary, RH-strength).**

If the summed bound holds for a family of test weights $\Phi$ rich enough to
detect off-axis zero terms, then every nontrivial log-scale carrier in the
completed quotient has real exponent $0$. Equivalently, every nontrivial pole
of $R(s)$ lies on $\mathrm{Re}(s)=\tfrac12$.

This corollary is the **source-to-spectral placement theorem**. The lemma
above is the first finite-chamber bridge step toward it.

---

## 6. Proof strategy (checklist)

| Step | Obligation | Status |
| --- | --- | --- |
| 1 | Formalize $\mathcal{K}(p,q;\Phi)$ from explicit-formula bridge | Draft |
| 2 | Prove d=4 first-$\tau=4$ arrival + closure $q\le S_+(w)$ | **Proved** (`d4_fractional_position_bound.md`, Lean) |
| 3 | Derive gap-dependent $\mathrm{frac\_pos}\le\min(R_{SDA}(p)/g,\,1-m/g)$ | **Proved**; uniform $\theta_4=\frac12$ **invalidated** |
| 4 | Prove $B(p,q)\asymp |I(p,q)|$ with explicit constants from $E(n)\ge0$ | Measured + lemma |
| 5 | Show deconvolution survival: chamber blocks map to $\Lambda(n)$ coefficients | Archive hinge |
| 6 | Sum over chambers and forbid $x^{a+i\gamma}$ with $a\neq0$ | Open (RH-strength) |

---

## 7. Falsification hooks

The draft lemma is false if any of the following hold on a measured surface:

1. $\mathrm{frac\_pos}(p,q)$ has no uniform upper bound on the d=4 carrier class.
2. $B(p,q)$ fails linear scaling with $|I(p,q)|$ at scale.
3. A single chamber produces kernel mass scaling as $x^{1/2+a}$ with $a>0$ under
   the explicit-formula model.
4. d=4 carrier share collapses at scale (contradicting packet dominance).

The analyzer in `pgs_chamber_budget_analyzer.py` is the primary certificate
generator for items 1–2 and packet share.

---

## 8. Status separation

| Item | Label |
| --- | --- |
| Interior Maximizer / next-prime theorems | proved (`PROOF.md`) |
| $R(s)=-\zeta'/\zeta$ | exact compression |
| Draft lemma in §5 | hypothesis / draft |
| RH pole-placement sentence | unresolved |
| Raw per-chamber centering | invalidated |