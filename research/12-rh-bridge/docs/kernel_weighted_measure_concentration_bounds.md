# Kernel-Weighted Measure Concentration Bounds

Date: 2026-05-24

Status: deterministic mass and local concentration strategy for the weighted
measure in the direct continuous-frequency large sieve.

The measure is

$$
d\mu(\alpha)
=
\sum_{q\le Q_0}\sum_{(a,q)=1}
|K_N(\alpha)|^2
\psi_{a,q}\!\left(\alpha-{a\over q}\right)d\alpha,
$$

with smooth windows supported on

$$
\left|\alpha-{a\over q}\right|\le R_{\mathrm{req}}.
$$

The direct large-sieve constant is controlled by

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1]).
$$

## Bounded Overlap

If

$$
R_{\mathrm{req}}\le cQ_0^{-2},
$$

then rational spacing gives bounded overlap of the windows. Let the overlap
multiplicity be `B_ov`. Then

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\psi_{a,q}\!\left(\alpha-{a\over q}\right)
\le
B_{\mathrm{ov}}.
$$

## Total Mass

Using bounded overlap,

$$
\mu([0,1])
\le
B_{\mathrm{ov}}\int_0^1 |K_N(\alpha)|^2\,d\alpha.
$$

For the interval kernel,

$$
\int_0^1 |K_N(\alpha)|^2\,d\alpha
\asymp N.
$$

Therefore

$$
\mu([0,1])\ll B_{\mathrm{ov}}N.
$$

## Local `1/X` Concentration

For any interval `I` of length `1/X`,

$$
\mu(I)
\le
B_{\mathrm{ov}}
\int_I |K_N(\alpha)|^2\,d\alpha.
$$

Using

$$
|K_N(\alpha)|\le N,
$$

gives

$$
\mathfrak C_{\mu}(1/X)
\ll
B_{\mathrm{ov}}{N^2\over X}.
$$

Thus the crude large-sieve constant is

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\ll
B_{\mathrm{ov}}(N^2+N).
$$

## Improvement from Core Removal

If the major projector removes the kernel peak core to radius
`rho_core`, then on the residual support

$$
|K_N(\alpha)|^2\ll \rho_{\mathrm{core}}^{-2}.
$$

The total mass improves to

$$
\mu([0,1])
\ll
B_{\mathrm{ov}}\rho_{\mathrm{core}}^{-1},
$$

and local concentration improves to

$$
\mathfrak C_{\mu}(1/X)
\ll
B_{\mathrm{ov}}{1\over X\rho_{\mathrm{core}}^2}.
$$

The corresponding large-sieve constant is

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\ll
B_{\mathrm{ov}}
\left(
\rho_{\mathrm{core}}^{-2}
+
\rho_{\mathrm{core}}^{-1}
\right).
$$

If `rho_core >= M_Omega^{-1}`, this is

$$
\ll
B_{\mathrm{ov}}(M_{\Omega}^2+M_{\Omega}).
$$

## Closure Condition

The direct continuous-frequency route closes if

$$
B_{\mathrm{ov}}(M_{\Omega}^2+M_{\Omega})\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

Without core removal, the sufficient condition is the cruder

$$
B_{\mathrm{ov}}(N^2+N)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

## Minimal Lemma

> **Kernel-Weighted Measure Concentration Lemma.**  
> Under rational-window bounded overlap and aperture-core removal to radius
> `rho_core`, the weighted measure satisfies
> \[
> \mu([0,1])\ll B_{\mathrm{ov}}\rho_{\mathrm{core}}^{-1},
> \qquad
> \mathfrak C_{\mu}(1/X)\ll
> B_{\mathrm{ov}}(X\rho_{\mathrm{core}}^2)^{-1}.
> \]

## Result

The direct additive large-sieve constant is deterministic once rational
overlap and core removal are fixed. Bounded overlap gives total mass `O(N)`;
removing the kernel peak core improves the operator constant to the
annular-tail scale `rho_core^{-2}+rho_core^{-1}`.
