# Noncircular Major Validity in the Direct Route

Date: 2026-05-24

Status: clarification and proof strategy for major validity at `R_all` without
assuming the same kernel-weighted BDH estimate being proved.

The Direct Full-Radius BDH Lemma listed major validity at `R_all` as a
remaining quantitative input. In the averaged direct route, that validity is
not an independent assumption. It is the conclusion of the direct
continuous-frequency large-sieve estimate applied to the residual after major
packet subtraction.

## Avoiding Circularity

The following would be circular:

$$
\text{assume kernel-weighted BDH at }R_{\mathrm{all}}
\Rightarrow
\rho_{\mathrm{valid}}(c)\ge R_{\mathrm{all}}
\Rightarrow
\text{prove kernel-weighted BDH at }R_{\mathrm{all}}.
$$

The direct route avoids this by separating:

1. **major packet definition**, which is algebraic or explicit;
2. **residual estimate**, which is proved by direct continuous-frequency
   large sieve.

The major packet model is subtracted first. The large sieve then proves the
kernel-weighted residual error budget.

## Averaged Validity Conclusion

After subtraction, the direct large-sieve estimate proves

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{all}}}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{maj}}.
$$

This is the averaged statement

$$
\rho_{\mathrm{valid}}\ge R_{\mathrm{all}}
$$

in the only sense needed by the support-removal route.

## Remaining Independent Inputs

The direct averaged route needs these independent inputs:

1. explicit major packet model functions on `|beta| <= R_all`;
2. subtraction of principal and exceptional coherent components;
3. residual coefficient energy `A_2`;
4. rational separation `R_all <= cQ_0^{-2}`;
5. measure concentration after core removal.

It does not need a separate averaged BDH theorem as an input.

## Pointwise Exceptions

If the proof requires pointwise validity for specific centers not covered by
the averaged budget allocation, those centers must be handled independently by
PNT-in-AP or zero-density estimates. This is not circular because those inputs
are external to the averaged direct large-sieve estimate.

## Minimal Lemma

> **Noncircular Direct Major Validity Lemma.**  
> Given explicit major packet subtraction at radius `R_all`, rational
> separation, measure concentration, and residual coefficient energy `A_2`,
> the direct continuous-frequency large sieve proves the averaged
> kernel-weighted major validity estimate at `R_all`. Pointwise exceptional
> centers, if required, are handled separately by zero-density or PNT-in-AP
> input.

## Result

For the direct route, `rho_valid >= R_all` is not assumed from
kernel-weighted BDH. It is proved by the direct weighted additive large sieve
after major packet subtraction. The remaining independent tasks are packet
definition/subtraction, residual coefficient energy, rational separation, and
measure concentration.
