# Budget Consistency and Radius Feasibility Strategy

Date: 2026-05-24

Status: parameter-assignment strategy for the final two gaps in the Direct
Full-Radius BDH Assembly.

The remaining quantities are

$$
L_{\mathrm{crit}},\quad
M_{\Omega},\quad
R_{\mathrm{LS}},\quad
\mathcal E_{\mathrm{maj}},\quad
\mathcal E_{\mathrm{shift}},\quad
Q_0.
$$

They must be assigned without circular dependence and must yield

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}).
$$

## Dependency Graph

The combined radius is

$$
R_{\mathrm{all}}
=
\max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1},R_{\mathrm{LS}}).
$$

The components depend on:

$$
L_{\mathrm{crit}}
\leftarrow
\text{Completion Energy Bound data},
$$

$$
M_{\Omega}
=
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\mathrm{min}}},
$$

$$
R_{\mathrm{LS}}
\leftarrow
(\mathcal A_2,\mathcal E_{\mathrm{maj}},B_{\mathrm{ov}}).
$$

To avoid circularity, `rho_max` must be bounded using an external major-radius
input

$$
\rho_{\mathrm{valid}}^{0}(c)
$$

from PNT-in-AP, Siegel-Walfisz, zero-density, or a separately proved
major-arc theorem, not from the direct BDH conclusion being assembled.

## Assignment Order

Use this order:

1. choose `Q_0`;
2. choose external major-validity lower bounds `rho_valid^0(c)`;
3. allocate budgets `E_maj` and `E_shift` from the available Poisson budget;
4. compute or bound `A_2` and `A_min`;
5. compute `L_crit`, `M_Omega`, and `R_LS`;
6. form `R_all`;
7. verify
   $$
   R_{\mathrm{all}}
   \le
   \min(\rho_{\mathrm{valid}}^{0}(c),c_1Q_0^{-2}).
   $$

If the final inequality holds, the direct assembly is noncircular.

## Clean Polylogarithmic Regime

For

$$
Q_0\le(\log X)^B,
$$

the frame and amplitude inputs are supplied by diagonal dominance and
Siegel-Walfisz. Then `rho_valid^0(c)` is fixed before the direct
large-sieve proof. The final feasibility check is purely quantitative.

## Failure Modes

There are three possible failures.

**Budget failure.**
`E_maj` or `E_shift` is too small, making `M_Omega^{-1}` or `R_LS` too large.

**Radius failure.**
`R_all` exceeds `rho_valid^0(c)` for some relevant center.

**Separation failure.**
`R_all` exceeds `c_1Q_0^{-2}`.

The first calls for a different budget split. The second calls for stronger
major-arc input. The third calls for smaller `Q_0` or a packet-frame route
that does not require disjoint support apertures.

## Minimal Lemma

> **Budget-Radius Feasibility Lemma.**  
> There is a noncircular assignment of `Q_0`, external major-validity radii,
> and budgets `E_maj,E_shift` such that the derived radius
> `R_all=max(c0/L_crit,M_Omega^{-1},R_LS)` satisfies
> \[
> R_{\mathrm{all}}
> \le
> \min(\rho_{\mathrm{valid}}^{0}(c),c_1Q_0^{-2})
> \]
> for every relevant packet center.

## Result

Budget consistency and radius feasibility are now one parameter-assignment
problem. The direct assembly closes only after `R_all` is computed from
external inputs and then checked against external major validity and rational
separation.
