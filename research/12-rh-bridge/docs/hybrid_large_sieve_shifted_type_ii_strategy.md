# Hybrid Large-Sieve Shifted Type II Strategy

Date: 2026-05-24

Status: candidate strategy for the mean-square input behind shifted Type II
bounds.

The shifted Type II estimate reduces to a hybrid large-sieve problem for
product phases

$$
(\theta+a/q)mn
$$

in the balanced range. The small rational `a/q` imposes congruence structure;
the shifted minor condition must supply spacing.

## Mean-Square Object

For

$$
S_{A,B}^{a/q}(\theta)=
\sum_{m\sim A}\alpha_m
\sum_{n\sim B}\beta_n e((\theta+a/q)mn),
\qquad
AB\asymp X,
$$

the required mean-square input has the form

$$
\int_{\Theta_{q,a}}
|S_{A,B}^{a/q}(\theta)|^2
w_N(\theta)\,d\theta
\ll
X(\log X)^{-A_0},
$$

after summing over the dyadic decomposition pieces and kernel bands in the
minor-arc contribution. Here `Theta_{q,a}` excludes the major arc attached to
`a/q`.

The weight `w_N` is produced by the kernel band and is largest near the major
center.

## Cauchy And Product Spacing

After Cauchy-Schwarz in `m`, one must control inner sums

$$
\sum_{n\sim B}\beta_n e(nm(\theta+a/q)).
$$

The relevant frequencies are

$$
\lambda_m(\theta)=m\theta+\frac{am}{q}\pmod1.
$$

A hybrid large-sieve estimate must show that, as `m` varies and `theta` ranges
over the shifted minor set, the frequencies `lambda_m(theta)` are sufficiently
spaced on average.

The small modulus creates clusters when

$$
m\equiv m'\pmod q,
$$

so the estimate should first split `m` into residue classes modulo `q` and
then apply spacing inside each class.

## Congruence-Split Large Sieve

For each residue class `r mod q`, estimate

$$
\int_{\Theta_{q,a}}
\left|
\sum_{\substack{m\sim A\\m\equiv r(q)}}
\alpha_m
\sum_{n\sim B}\beta_n e(nm\theta)
\right|^2
w_N(\theta)\,d\theta.
$$

Since `q <= Q_0`, summing over `r` costs only polylogarithmically. The main
question is whether the shifted minor exclusion gives enough spacing among
the frequencies `m theta`.

## Product-Difference Form

Expanding the mean square gives terms with phase

$$
(\theta+a/q)(mn-m'n').
$$

The `theta` integral with kernel weight localizes product differences:

$$
mn-m'n'
$$

to a window determined by the reciprocal width of the band. The rational
factor imposes the congruence phase

$$
e(a(mn-m'n')/q).
$$

Thus the estimate can also be viewed as a weighted count of near-equal
products with congruence oscillation modulo `q`. This is the bilinear
dispersion form.

## Required Inputs

**Hybrid large sieve with small moduli.**
An estimate for product phases `mn theta` after splitting one variable modulo
`q`, uniform for `q <= Q_0`.

**Major-exclusion spacing.**
The proof must use that `theta+a/q` is outside the assigned major arc. Without
that exclusion, the frequencies can cluster and create the major contribution.

**Kernel-weighted product-difference bound.**
The near-equal product count after the `theta` integral must have enough
cancellation from coefficients and the rational phase to stay below
Poisson scale.

**Coefficient control.**
The Vaughan or Heath-Brown coefficients must be divisor-bounded uniformly in
the congruence split.

## Principal Obstacles

**Balanced product energy.**
For `A ~ B ~ X^{1/2}`, the equation

$$
mn\approx m'n'
$$

has many near-solutions. The proof must exploit oscillation and congruence,
not only count spacing crudely.

**Residue clustering modulo `q`.**
The rational shift makes frequencies with the same `m mod q` closer. Splitting
modulo `q` is necessary but not sufficient; one still needs spacing in
`m theta`.

**Kernel weight near major arcs.**
The largest weights occur exactly where major exclusion is most delicate.
Transition estimates must prevent leakage.

**Convolution strength.**
The mean-square estimate must feed into the convolution norm, so it needs
enough saving after summing over paired frequency bands.

## Minimal Hybrid Large-Sieve Lemma

The shifted Type II route needs:

> **Shifted Product Large-Sieve Lemma.**
> For `A B ~ X`, `A ~ B ~ X^{1/2}`, `q <= Q_0`, and shifted minor
> `theta+a/q`, the Type II sum satisfies a kernel-weighted mean-square and
> bilinear dispersion estimate strong enough to imply
> $$
> \sum_{L_1,L_2}
> \left\|
> L_1S_{A,B}^{a/q}1_{\mathfrak m_{L_1}}
> *
> L_2(\cdot)1_{\mathfrak b_{L_2}}
> \right\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C.
> $$

## Result

The shifted Type II estimate has been reduced to a hybrid large-sieve problem
for balanced product phases with small-modulus congruence splitting and
kernel-weighted near-product dispersion. This is the precise mean-square core
of the minor-major resonance route.
