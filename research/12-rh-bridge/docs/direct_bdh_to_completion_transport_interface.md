# Direct BDH To Completion Transport Interface

Date: 2026-05-24

Status: interface note connecting the closed Direct Full-Radius BDH Assembly
to completion transport radius and Chamber-Deconvolved Reciprocal Balance.

The Direct Full-Radius BDH Assembly is closed in the explicit polylogarithmic
literal regime recorded in
`direct_full_radius_bdh_closure_certificate.md`. The closure supplies
kernel-weighted major validity at the unified aperture radius

$$
R_{\mathrm{all}}
=
\max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1},R_{\mathrm{LS}}).
$$

This note records exactly what that analytic closure contributes to the
completion-transport side.

## Input Supplied By Direct BDH

The closed direct route gives:

$$
R_{\mathrm{all}}\le
\min(\rho_{\mathrm{valid}}^0,c_1Q_0^{-2}),
$$

and the residual endpoint exponential sum satisfies the kernel-weighted
major-window bound

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

It also gives the linked consequences:

```text
Full-Radius Major Validity
-> Full Unified Major Aperture
-> kernel-band completion-energy control
-> projected reciprocal-congruence major-side closure
```

Thus the low-conductor major packets, high-`L` kernel bands, kernel-window
mass, and direct large-sieve measure concentration have all been paid for in
the assigned regime.

## What This Removes

The direct BDH closure removes a specific analytic obstruction:

```text
uncaptured low-conductor / high-kernel residual energy
```

It prevents such residual energy from becoming an unbudgeted local carrier in
the completed folded coordinate. Equivalently, the direct route supplies the
controlled-summation and major-aperture part of the Exact Completion Assembly
Theorem.

In the language of the Chamber-Deconvolved Reciprocal Balance route, it
supplies analytic control for the residual terms that remain after:

```text
lambda = Lambda
-> low-conductor major packet projection
-> completion
-> folding into z = u^2
```

## What It Does Not Supply

Direct BDH does not by itself prove the packetwise transport-radius
localization

$$
\operatorname{supp}(\eta^-_{p,q,z})
\subseteq
\{x:|x|\ge M_{p,q}\}.
$$

That condition is the source of

$$
\rho_{p,q}(z)\ge M_{p,q},
$$

which is the remaining completion-side input needed by the Aggregate
Completion-Cost Bound:

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z).
$$

Thus the direct BDH closure is an analytic major/residual control theorem. It
is not the completion-localization theorem.

## Interface Contract

The Direct BDH closure supplies the following pieces to the
Chamber-Deconvolved Reciprocal Balance Lemma:

1. **Major residual control.**
   Low-conductor major packets reproduce their amplitudes and the residual is
   square-mean controlled at `R_all`.

2. **Completion-energy control.**
   Kernel-band completion coefficients are inside the Poisson allowance, so
   the reciprocal-congruence major side is controlled.

3. **Summability input.**
   The residual analytic contribution is budgeted by `E_tot`, providing the
   controlled-summation side of packetwise completion assembly.

4. **Fallback equivalence.**
   Below the literal kernel-length threshold, the same interface is supplied
   only if the Unified Packet-Frame Source theorem proves the three residual
   captures.

The remaining bridge input is:

> **Packetwise Completion Localization.**  
> The pole, gamma, trivial-zero, and main-term completion correction can be
> assigned to chamber packets so that every negative folded-cost contribution
> used to cancel packet drift has transport radius at least
> `M_{p,q}`.

## Consequence

If Packetwise Completion Localization is proved, then for each packet

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

The weighted-average packet bound already gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z).
$$

Therefore

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z),
$$

the Folded Packet Drift Inequality holds, and the Chamber-Deconvolved
Reciprocal Balance Lemma reduces to exact completion assembly with
localization.

## Final Remaining Inputs

After Direct BDH closure, the remaining inputs are:

1. a packetwise decomposition of `C_comp(s)` compatible with the explicit
   formula;
2. no negative zero-radius leakage;
3. packetwise support localization at `|x|>=M_{p,q}`;
4. summable negative folded costs, using the Direct BDH completion-energy
   control already supplied;
5. if the literal kernel-length regime fails, the Unified Packet-Frame Source
   theorem in place of literal support removal.

## Result

The closed Direct Full-Radius BDH Assembly supplies the analytic
major-window and completion-energy input required by the completion transport
program. The remaining bridge is now sharply localized: prove packetwise
completion localization for the standard completion correction, or prove the
Unified Packet-Frame Source theorem in regimes where literal support removal
is not admissible.
