# Alpha-Split Normalization Candidates

Date: 2026-05-24

Status: candidate-normalization note for the Canonical Symmetric
Trivial-Zero Transport Lemma.

The symmetric trivial-zero capacity route introduces nonnegative split
parameters

$$
\alpha_m(z)\ge0
$$

through

$$
\delta_{y_m}
=
(1+\alpha_m(z))\delta_{y_m}
-
\alpha_m(z)\delta_{y_m},
\qquad
y_m=-2m-\frac12.
$$

The split preserves exact assembly atom by atom. The unresolved question is
which rule, if any, determines the `alpha_m(z)` canonically.

## Required Positive-Capacity Amount

Let

$$
A_+(z)=D_-(z)-T_+^{\mathrm{pole}}(z).
$$

If the pole capacity is used without further regularization, the
trivial-zero split must satisfy

$$
\sum_{m\ge0}\alpha_m(z)|J_z(y_m)|=A_+(z).
$$

This requires

$$
A_+(z)\ge0.
$$

If `A_+(z) < 0`, positive trivial-zero capacity cannot repair the sidewise
balance. The representation must also regularize the pole capacity or revise
the rule that all raw pole capacity is assigned as usable transport capacity.

The negative side has the corresponding formal requirement

$$
T_-^{\mathrm{pole}}(z)
+
T_-^{\mathrm{triv,sym}}(z)
=D_+(z),
$$

but the raw trivial-zero negative side is divergent, so this condition cannot
be read before a finite-part rule is chosen.

## Candidate 1: Nearest-Atom Demand Match

Use only the nearest trivial-zero atom:

$$
\alpha_0(z)=\frac{A_+(z)}{|J_z(-1/2)|},
\qquad
\alpha_m(z)=0\quad(m\ge1),
$$

when `A_+(z) >= 0`.

This gives

$$
T_+^{\mathrm{triv,sym}}(z)=A_+(z),
$$

and

$$
C_-^{\mathrm{triv,sym}}(z)
=
\alpha_0(z)K_z(-1/2).
$$

The transport radius is exactly

$$
\frac{T_+^{\mathrm{triv,sym}}(z)}
{C_-^{\mathrm{triv,sym}}(z)}
=
\frac12.
$$

This is enough for packet localization because `M_{p,q}<1/2`.

**Difficulty.** The rule is deterministic and controlled, but it is
demand-matched rather than completion-intrinsic. It chooses the nearest
trivial-zero atom because that is convenient for localization, not because the
gamma factor selects it.

## Candidate 2: Folded-Kernel Proportional Match

Let

$$
H(z)=\sum_{m\ge0}K_z(y_m),
$$

which converges because `K_z(y_m) ~ 1/(4m^2)`. Define

$$
\beta_m(z)=\frac{K_z(y_m)}{H(z)}.
$$

For `A_+(z) >= 0`, set

$$
\alpha_m(z)
=
\frac{A_+(z)\beta_m(z)}{|J_z(y_m)|}.
$$

Then

$$
\sum_{m\ge0}\alpha_m(z)|J_z(y_m)|=A_+(z),
$$

and

$$
C_-^{\mathrm{triv,sym}}(z)
=
A_+(z)\sum_{m\ge0}\frac{\beta_m(z)}{|y_m|}.
$$

Since `|y_m| >= 1/2`,

$$
C_-^{\mathrm{triv,sym}}(z)\le2A_+(z).
$$

**Difficulty.** This rule is deterministic from the folded kernel, but it
still uses the packet-demand scalar `A_+(z)`. It is canonical only after the
sidewise packet demand has already been accepted as an input.

## Candidate 3: Abel-Regularized Raw-Capacity Proportion

Introduce an Abel cutoff

$$
\beta_{m,\varepsilon}(z)
=
\frac{e^{-\varepsilon |y_m|}|J_z(y_m)|}
{\sum_{\ell\ge0}e^{-\varepsilon |y_\ell|}|J_z(y_\ell)|}.
$$

Then set

$$
\alpha_{m,\varepsilon}(z)
=
\frac{A_+(z)\beta_{m,\varepsilon}(z)}{|J_z(y_m)|}.
$$

This matches the required positive capacity for every `epsilon > 0`.

**Difficulty.** As `epsilon -> 0+`, the normalizing denominator diverges
logarithmically and the probability mass escapes to arbitrarily large
trivial-zero radii. The folded negative cost tends toward zero rather than to
a canonical nonzero limit. This degeneracy shows that raw-capacity
proportionality does not by itself define a stable normalization.

## Candidate 4: Variational Minimal-Cost Rule

Minimize

$$
\sum_{m\ge0}\alpha_m(z)K_z(y_m)
$$

subject to

$$
\sum_{m\ge0}\alpha_m(z)|J_z(y_m)|=A_+(z),
\qquad
\alpha_m(z)\ge0.
$$

Since

$$
\frac{K_z(y_m)}{|J_z(y_m)|}=\frac1{|y_m|},
$$

the cost per unit capacity decreases as `m` grows. The infimum is `0`, reached
only by sending capacity to infinite trivial-zero height.

**Difficulty.** The unconstrained variational rule has no minimizer. Any
usable variational normalization requires an additional moment or height
constraint, and that extra constraint is not supplied by the current
completion data.

## Candidate 5: Gamma-Finite-Part Balance

Determine `alpha_m(z)` together with the finite part of the negative
trivial-zero side so that both sidewise identities hold:

$$
T_+^{\mathrm{pole}}(z)+
\sum_{m\ge0}\alpha_m(z)|J_z(y_m)|
=D_-(z),
$$

and

$$
T_-^{\mathrm{pole}}(z)
+
\operatorname{F.p.}
\sum_{m\ge0}(1+\alpha_m(z))|J_z(y_m)|
=D_+(z).
$$

**Difficulty.** This is the strongest candidate because it ties the split to
the completed gamma finite part. It is also essentially the sidewise Transport
Capacity Balance Identity itself. Proving it would close the completion-side
obstruction, but the current notes do not yet supply the finite-part theorem.

## Result

The concrete deterministic rules show that positive trivial-zero capacity can
be supplied without changing exact assembly and without violating
localization. They do not yet prove the bridge because their normalization is
not intrinsic enough.

The next required statement is:

> **Canonical Alpha Normalization Lemma.**
> The split parameters `alpha_m(z)` are determined by the completed gamma
> finite-part structure, not by an arbitrary capacity gauge, and the resulting
> sign-regularized trivial-zero reservoir satisfies the sidewise Transport
> Capacity Balance Identity with controlled folded negative cost.

This lemma is now the precise completion-side obstruction.
