# Final Completion Verification Matrix

Date: 2026-05-24

Status: consolidated verification matrix for the Direct Full-Radius BDH
Assembly and its packet-frame alternative.

`PROOF.md` proves the local PGS source theorems: deterministic next-prime
return and the interior maximizer theorem. It does not prove the downstream
RH-facing completion estimates. The direct full-radius BDH route therefore
has a clean status: it is reduced to the completion-side estimates listed
below.

## Literal Route Matrix

The polylogarithmic literal route uses

$$
Q_0=(\log X)^B,
\qquad
B\le {1\over2}-\varepsilon
$$

when the major budget is only a fixed fraction of residual coefficient
energy.

| Source | Required Estimate | Role |
| --- | --- | --- |
| Major radius | `rho_valid^0 >= c1 Q0^-2` | permits valid low-conductor major windows |
| Frame | `Q0^4/X -> 0` | stabilizes coefficient-level major projection |
| Amplitude | `N Q0^2 log^{-2A} X <= E_tail` | reproduces major packet amplitudes |
| Kernel band | `P_{d,N}^2 >= E_band^req(d,N)` | gives `L_crit >= C Q0^2` |
| Shift kernel | `E_shift >= E_shift^req` | pays residual divisor-shift kernel |
| Major window | `E_maj >= E_maj^req` | pays direct large-sieve residual |
| Tail | `E_tail` absorbs smoothing, Gram leakage, and AP amplitude errors | closes technical losses |
| Total split | `E_tot >= E_band^req + E_shift^req + E_maj^req + E_tail` | closes the literal assembly |

The three required payments are:

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}(d,N)
=
C_Ld^{-1}\mathcal B_dQ_0^6
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)
(\log X)^C,
$$

summed over the relevant dyadic slices,

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
=
C_S\mathcal A_{\min}Q_0^2
\min(H,Q_0^2)\log Q_0,
$$

and

$$
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
=
C_M\mathcal A_2{Q_0^4\over(\log X)^2}.
$$

The literal route closes exactly when these estimates fit inside
`E_tot` after the external polylog major-radius input and the low-conductor
frame/amplitude inputs are fixed.

## Packet-Frame Alternative Matrix

If the literal split fails, the replacement is one simultaneous projection
theorem:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\min}},
$$

and

$$
\left(
X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

The first inequality lowers `E_band^req`; the second lowers
`E_shift^req`; the third lowers `E_maj^req`. The theorem must hold for the
same major packet projection `P_maj`, the same endpoint normalization, and
the same conductor scale `Q0`.

## Final Quantities To Verify

The literal route needs the following concrete quantities:

1. total completion allowance `E_tot`;
2. dyadic Poisson allowances `P_{d,N}`;
3. kernel-band support and norm data:
   `B_d,H_d,T_d,K_d,U,E_v(d),R_spec`;
4. projected band transform control for `W_{N,L}^perp`;
5. shift-kernel data: `A_min,H,rho_max,Omega_N^perp`;
6. major-window data: `A_2,B_ov,mu,E_maj`;
7. tail budget for smoothing, Gram leakage, and amplitude error.

The packet-frame route needs the same quantities plus simultaneous lower
frame estimates for:

1. high-`L` kernel bands;
2. kernel-window mass;
3. weighted residual measure concentration.

## Closure Statement

> **Direct Full-Radius Completion Verification.**  
> In the polylogarithmic conductor range, the Direct Full-Radius BDH Assembly
> closes if the literal route matrix holds. If any literal payment exceeds
> the available completion allowance, the assembly closes only if the
> Unified Packet-Frame Source theorem supplies the three simultaneous
> residual bounds above.

## Result

The bridge has reached a finite completion verification matrix. The remaining
work is not another categorical reduction. It is the computation or proof of
the listed completion quantities against `E_tot`, or the proof of the single
packet-frame theorem that replaces all three literal payments.
