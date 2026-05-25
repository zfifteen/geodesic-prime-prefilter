# Direct Full-Radius BDH Assembly

Date: 2026-05-24

Status: assembly note for the direct continuous-frequency large-sieve proof
at the unified aperture radius.

This note assembles the direct route to the Direct Full-Radius BDH Lemma.

## Inputs

The route uses five inputs.

**1. Coefficient-level major projection.**
The low-conductor packet frame defines a bounded projection

$$
P_{\mathrm{maj}}
$$

and residual

$$
a^{\perp}=a-P_{\mathrm{maj}}a.
$$

**2. Amplitude reproduction.**
Projection coefficients reproduce the classical major packet amplitudes on
`|beta| <= R_all`, with AP-error and cross-packet leakage inside the major
budget.

**3. Residual energy.**
Orthogonal projection gives

$$
\mathcal A_2=\|a^{\perp}\|_2^2\le \|a\|_2^2.
$$

**4. Measure concentration after core removal.**
At aperture radius `R_all`, the kernel-weighted measure satisfies

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\ll
B_{\mathrm{ov}}(R_{\mathrm{all}}^{-2}+R_{\mathrm{all}}^{-1}).
$$

**5. Unified radius condition.**

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
$$

for every relevant low-conductor center.

## Proof Assembly

The direct continuous-frequency large sieve gives

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)\mathcal A_2.
$$

By measure concentration,

$$
\le
B_{\mathrm{ov}}(R_{\mathrm{all}}^{-2}+R_{\mathrm{all}}^{-1})\mathcal A_2.
$$

Since `R_all` includes `R_LS`,

$$
B_{\mathrm{ov}}(R_{\mathrm{all}}^{-2}+R_{\mathrm{all}}^{-1})\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

Therefore

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

After endpoint normalization, this is the kernel-weighted major-window
residual estimate required by the Full-Radius Major Validity Lemma.

## Consequence

The Direct Full-Radius BDH Lemma closes under the five inputs above. It gives
averaged major validity at `R_all`, which closes literal support removal for
the Full Unified Major Aperture Lemma.

## Remaining Quantitative Gaps

The assembly leaves four quantitative gaps to prove or assign:

1. **Frame regime.**
   Verify the low-conductor packet frame is conditioned in the chosen `Q_0`
   range.

2. **Amplitude AP error.**
   Prove the projection amplitudes match the major packet amplitudes with
   error inside `E_maj`.

3. **Budget consistency.**
   Fix `E_maj`, `E_shift`, `L_crit`, `M_Omega`, and `R_LS` so that `R_all`
   is defined without circular dependence.

4. **Radius feasibility.**
   Verify
   $$
   R_{\mathrm{all}}\le c_1Q_0^{-2}
   $$
   and the major validity/error budget on the same radius.

## Minimal Assembly Lemma

> **Direct Full-Radius BDH Assembly Lemma.**  
> If the low-conductor frame is conditioned, its projected amplitudes match
> the classical major packet amplitudes within budget, the residual energy
> and measure concentration bounds hold, and `R_all` satisfies rational
> separation and major validity, then the direct continuous-frequency large
> sieve proves the kernel-weighted maximal BDH estimate at `R_all`.

## Result

The direct route is assembled. The large-sieve step itself is no longer the
open problem once `R_all` includes `R_LS`; the remaining work is quantitative
budget and major-packet verification.
