# Minor-Arc Bilinear Kernel Bound Strategy

Date: 2026-05-24

Status: candidate strategy for the convolution-strength minor-arc estimate.

The minor-arc endpoint estimate must control

$$
\|(B_XK_N)_{\mathfrak m}*(B_XK_N)\|_2^2
$$

at Poisson scale. A pointwise exponential-sum bound is not enough unless it
survives the interval kernel and the additive convolution. The natural route
is a dyadic kernel decomposition plus bilinear large-sieve estimates.

## Target

Let

$$
H_N(\alpha)=B_X(\alpha)K_N(\alpha),
$$

where `B_X` is the centered endpoint exponential sum and `K_N` is the interval
kernel. The target is

$$
\|(H_N)_{\mathfrak m}*H_N\|_2^2
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

## Dyadic Kernel Bands

Use

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}).
$$

Decompose the minor arcs into bands

$$
\mathfrak m_L=
\{\alpha\in\mathfrak m:L<|K_N(\alpha)|\le2L\},
\qquad
1\le L\le N,
$$

with dyadic `L`. On each band,

$$
H_N(\alpha)\approx L\,B_X(\alpha).
$$

The convolution splits into bilinear pieces

$$
(H_N1_{\mathfrak m_{L_1}})*
(H_N1_{\mathfrak b_{L_2}}),
$$

where the second factor may lie on either major or minor arcs depending on the
full decomposition.

## Required Mean-Square Input

The first input is a kernel-weighted mean-square bound:

$$
\int_{\mathfrak m}
|B_X(\alpha)|^2|K_N(\alpha)|^2\,d\alpha
\ll
X\frac{N}{\log X}(\log X)^C.
$$

In dyadic form, this asks for

$$
\sum_L
L^2
\int_{\mathfrak m_L}|B_X(\alpha)|^2\,d\alpha
\ll
X\frac{N}{\log X}(\log X)^C.
$$

This is a weighted large-sieve estimate for centered endpoint sums.

## Required Bilinear Input

The convolution norm needs more than mean square. A sufficient bilinear
estimate is:

$$
\sum_{L_1,L_2}
\left\|
L_1B_X1_{\mathfrak m_{L_1}}
*
L_2B_X1_{\mathfrak b_{L_2}}
\right\|_2^2
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C,
$$

where `b_L2` ranges over the relevant major/minor partner bands and major
pieces are replaced by their explicit approximants.

This estimate is the convolution-strength form of minor-arc cancellation.

## Candidate Proof Inputs

**Weighted large sieve.**
For each band, prove

$$
\int_{\mathfrak m_L}|B_X(\alpha)|^2\,d\alpha
\ll
\frac{X}{\log X}\,|\mathfrak m_L|(\log X)^C
+X(\log X)^{-A}
$$

or a comparable estimate strong enough after multiplying by `L^2` and summing
over `L`.

**Type I/II bilinear estimates.**
Apply Vaughan or Heath-Brown decomposition to `B_X`, then estimate the
frequency convolution piece by piece. Type II sums are the likely bottleneck
because they control correlations between two endpoint-frequency packets.

**Transition-zone zero-density input.**
For bands close to major arcs with larger denominators, use zero-density or
Bombieri-Vinogradov style estimates to prevent residue-class structure from
leaking into the minor term.

## Pointwise Bounds Are Insufficient

A bound of the form

$$
\sup_{\alpha\in\mathfrak m}|B_X(\alpha)|
\ll
X(\log X)^{-A}
$$

helps, but by itself it does not control

$$
(B_XK_N)_{\mathfrak m}*(B_XK_N)
$$

unless paired with strong `L^1` or `L^2` kernel-weighted estimates. The
convolution can concentrate along frequency pairs even when individual
frequencies are controlled.

## Principal Obstacles

**Kernel-band summation.**
The largest kernel values occur near major arcs. The minor arcs must be
defined so that high-`L` bands are either major-controlled or have strong
transition estimates.

**Endpoint centering.**
The sequence is `1_P - 1/log X`, not `Lambda - 1`. The proof must keep the
centering through Vaughan decomposition or partial summation.

**Bilinear frequency coupling.**
The fourth moment couples two frequency variables through convolution.
Mean-square estimates for single sums do not automatically control this
coupling.

**Uniformity across `N`.**
The dyadic kernel bands depend on `N`, and the final estimate must remain
valid throughout the nontrivial range.

## Minimal Bilinear Lemma

The minor-arc route needs:

> **Kernel-Band Bilinear Endpoint Lemma.**
> The centered endpoint sum satisfies the dyadic band convolution bound
> $$
> \sum_{L_1,L_2}
> \left\|
> L_1B_X1_{\mathfrak m_{L_1}}
> *
> L_2B_X1_{\mathfrak b_{L_2}}
> \right\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C.
> $$

This lemma implies the kernel-weighted minor-arc estimate required by the
centered endpoint four-energy strategy.

## Result

The minor-arc problem has sharpened to a bilinear large-sieve estimate over
dyadic kernel bands. The main technical burden is controlling frequency-pair
coupling for the centered unweighted endpoint sequence after the interval
kernel is applied.
