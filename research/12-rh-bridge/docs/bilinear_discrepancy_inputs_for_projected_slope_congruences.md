# Bilinear Discrepancy Inputs for Projected Slope Congruences

Date: 2026-05-24

Status: candidate input ledger for proving projected coprime-slope
cancellation.

The projected linear family is

$$
un-vn'=t,\qquad (u,v)=1,\qquad t\ne0.
$$

The congruence form

$$
u n\equiv t\pmod v
$$

and the reciprocal form

$$
n'\equiv -t\overline v\pmod u
$$

give two routes to the same average-cancellation target. This note records
the precise discrepancy inputs needed for Poisson-scale saving after
major-exclusion.

## Graph Discrepancy Form

For fixed `u,v,t`, write

$$
L_{u,v}(t)
=
\sum_{\substack{n\sim B\\ n\equiv \overline u t\pmod v\\
(un-t)/v\sim B}}
\beta_n\overline{\beta_{(un-t)/v}} .
$$

This is not an ordinary arithmetic-progression count. It is a weighted graph
sum on the affine line

$$
n'={un-t\over v}.
$$

Let `M_{u,v,d}(t)` be the part removed by the major-exclusion projector. The
basic discrepancy is

$$
D_{u,v,d}(t)=L_{u,v}(t)-M_{u,v,d}(t).
$$

The required estimate is

$$
\sum_d
\sum_{\substack{u,v\sim A/d\\(u,v)=1}}
\alpha_{du}\overline{\alpha_{dv}}
\sum_{t\ne0}
e(adt/q)W_N(dt)D_{u,v,d}(t)
\ll \mathcal P_N,
$$

where `P_N` is the Poisson-scale allowance for the kernel band. This is the
most direct bilinear discrepancy input.

## Average Over Slopes

For fixed `d` and `t`, the graph has length about `B/v`. In the balanced
range this is sparse for small `d`, so the proof cannot rely on long
progressions for each pair `u,v`. The saving must come from the average over
the coprime slope family.

The natural second-moment target is

$$
\sum_{v\sim V}
\left|
\sum_{\substack{u\sim U\\(u,v)=1}}
\alpha_{du}
\sum_t K_{d,q,N}(t)D_{u,v,d}(t)
\right|^2
\ll \mathcal P_{d,N}^{(2)} ,
$$

with

$$
U\asymp V\asymp A/d,\qquad
K_{d,q,N}(t)=e(adt/q)W_N(dt).
$$

Expanding this second moment produces correlations between two affine graphs.
Those correlations are the place where dispersion or Kloosterman estimates
must enter.

## Reciprocal Kloosterman Form

From

$$
v n'\equiv -t\pmod u
$$

and `(u,v)=1`,

$$
n'\equiv -t\overline v\pmod u.
$$

After additive completion in `n'`, averages over `v mod u` contain sums of
the schematic shape

$$
\sum_{v\bmod u}^{*}
c_v\,
e\!\left({h\overline v+kv\over u}\right),
$$

with `h` tied to `t` and the completed `n'` frequency, and `k` tied to the
remaining slope weight. The needed input is a bilinear average of these
Kloosterman-type sums over `u`, `v`, and kernel frequencies.

A usable form is:

$$
\sum_{u\sim U}
\left|
\sum_{h,k}
A_{u,h,k}
\sum_{v\bmod u}^{*}
c_v e\!\left({h\overline v+kv\over u}\right)
\right|
\ll \mathcal P_{d,N}^{K},
$$

with the right side summable over `d` and kernel bands.

## Major-Projector Compatibility

The discrepancy estimate requires the projector to remove exactly the
components that the bilinear estimates cannot cancel:

1. exact product diagonal;
2. residue-class means for the conductor `q_1=q/(d,q)`;
3. frequency clusters near low-denominator rationals;
4. boundary main terms caused by the finite intervals `n,n' sim B`.

After these removals, `D_{u,v,d}(t)` must have zero local mean in every
small-conductor class. Without this compatibility, a Kloosterman or large
sieve estimate leaves an uncancelled main term.

## Minimal Input Alternatives

Any one of the following would supply the next bridge.

**Direct bilinear graph discrepancy.**
Prove the weighted bound for `D_{u,v,d}(t)` directly after slope averaging.

**Hybrid large-sieve proof.**
Prove the same bound through spacing of the frequencies
`(xi+ad/q)u` after the major clusters are removed.

**Bilinear Kloosterman proof.**
Complete one graph variable, convert the reciprocal slope dependence into
Kloosterman sums, and prove an average bound strong enough after summing over
`d` and kernel bands.

These are not separate bridge requirements. They are three possible routes to
the same projected discrepancy estimate.

## Result

The remaining cancellation problem has a concrete local form: show that the
mean-zero graph sums

$$
n'={un-t\over v}
$$

cancel on average over coprime balanced slopes after kernel weighting. The
principal analytic tools are hybrid large-sieve spacing, bilinear graph
dispersion, and averaged Kloosterman cancellation.
