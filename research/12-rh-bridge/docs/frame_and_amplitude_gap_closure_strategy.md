# Frame and Amplitude Gap Closure Strategy

Date: 2026-05-24

Status: strategy for closing the first two quantitative gaps in the Direct
Full-Radius BDH Assembly.

The first two remaining gaps are:

1. low-conductor frame conditioning;
2. amplitude reproduction for `P_maj a`.

## Frame Conditioning Gap

The packet centers satisfy rational spacing at scale

$$
\delta\asymp Q_0^{-2}.
$$

The Gram matrix has diagonal `asymp X` and off-diagonal `<< Q_0^2`. With

$$
|\mathcal C_{Q_0}|\asymp Q_0^2,
$$

diagonal dominance follows from

$$
Q_0^4\ll X.
$$

In this regime, the packet vectors form a bounded Riesz sequence on
`X<n<=2X`, and the coefficient projection is stable.

If `Q_0` is larger, use a sharper additive large-sieve/Riesz estimate rather
than the crude diagonal-dominance bound.

## Amplitude Reproduction Gap

For each center `a/q`, the packet coefficient is controlled by

$$
\sum_{X<n\le2X}\Lambda(n)e(an/q).
$$

PNT in AP gives

$$
\sum_{X<n\le2X}\Lambda(n)e(an/q)
=
{\mu(q)\over\varphi(q)}X
+
O(E_q(X)).
$$

After partial summation and endpoint normalization, this yields the
`mu(q)/phi(q)` major amplitude for the endpoint coefficient.

The required error condition is

$$
{E_q(X)^2\over(\log X)^2}
I_N(a/q,R_{\mathrm{all}})
\le
\mathcal E_{a,q,N},
$$

plus the Gram cross-packet correction.

## Clean Closure Regime

If

$$
Q_0\le(\log X)^B,
$$

then:

1. `Q_0^4 << X` holds for large `X`;
2. Siegel-Walfisz strength PNT in AP supplies `E_q(X)` with logarithmic
   saving;
3. Gram cross-packet leakage is controlled by rational separation and
   `R_all <= cQ_0^{-2}`.

Thus the frame and amplitude gaps close in the polylogarithmic
low-conductor regime, subject to the already stated budget inequality.

## Larger `Q_0`

For larger `Q_0`, the required replacements are:

1. a Riesz/frame bound sharper than diagonal dominance;
2. Bombieri-Vinogradov or BDH for averaged amplitude reproduction;
3. zero-density estimates for exceptional or transition centers;
4. a budget allocation that absorbs Gram cross-packet leakage.

## Minimal Lemma

> **Frame-Amplitude Closure Lemma.**  
> If `Q_0^4 << X` and PNT-in-AP gives the packet correlation errors
> `E_q(X)` small enough that
> \[
> {E_q(X)^2\over(\log X)^2}
> I_N(a/q,R_{\mathrm{all}})
> \le
> \mathcal E_{a,q,N},
> \]
> then the low-conductor projection is stable and its coefficients reproduce
> the classical major packet amplitudes on `|beta|<=R_all`.

## Result

The first two direct-assembly gaps close cleanly for polylogarithmic
`Q_0`. In larger conductor ranges, the same roles must be played by sharper
frame estimates and averaged/zero-density AP inputs.
