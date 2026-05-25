# Bilinear Kloosterman Average Strategy

Date: 2026-05-24

Status: candidate analytic strategy for the reciprocal-congruence branch of
the projected slope-dispersion estimate.

The reciprocal form of the projected congruence family is

$$
n'\equiv -t\overline v\pmod u,\qquad (u,v)=1.
$$

After additive completion in `n'`, the dependence on the slope `v` enters
through `vbar mod u`. Averaging over coprime slopes therefore produces
Kloosterman-type sums.

## Completed Reciprocal Form

Start from the graph sum

$$
L_{u,v}(t)
=
\sum_{\substack{n'\sim B\\ n'\equiv -t\overline v\pmod u}}
\overline{\beta_{n'}}
\beta_{(t+vn')/u}.
$$

Smooth the interval `n' sim B` and complete the congruence modulo `u`. The
completed expansion has schematic terms

$$
\sum_h
\widehat \beta_{u,h}
e\!\left(-{h t\overline v\over u}\right)
\cdot
\operatorname{Amp}_{u,v,t,h},
$$

where `h=0` is the local mean and nonzero `h` carries the reciprocal phase.
The major-exclusion projector must remove the `h=0` contribution and every
low-conductor packet coupled to it.

## Slope Average

The slope average then contains sums of the form

$$
\sum_{v\sim V}^{(v,u)=1}
c_v\,
e\!\left(-{h t\overline v\over u}\right)
\operatorname{Amp}_{u,v,t,h}.
$$

Completing the finite `v`-interval introduces an additive frequency `k`, so
the inner complete sums have the shape

$$
S(-ht,k;u)
=
\sum_{v\bmod u}^{*}
e\!\left({-ht\overline v+kv\over u}\right).
$$

Thus the Kloosterman branch reduces the projected discrepancy estimate to a
bilinear average over

$$
u\sim U,\qquad h,\qquad t,\qquad k,
$$

with kernel weight `K_{d,q,N}(t)=e(adt/q)W_N(dt)`.

## Required Spectral Input

The needed bound is a spectral or bilinear large-sieve estimate for weighted
Kloosterman sums:

$$
\sum_{u\sim U}
\sum_{h,t,k}
A_{u,h,t,k}\,
S(-ht,k;u)
\ll \mathcal P_{d,N}^{K}.
$$

The coefficient `A_{u,h,t,k}` contains:

1. the Type II coefficients;
2. completion weights from `n'` and `v`;
3. the kernel factor `e(adt/q)W_N(dt)`;
4. the major-projected mean-zero condition.

The estimate must be average in `u`, `h`, `t`, and `k`. A pointwise Weil bound
for each `S(-ht,k;u)` is not enough if the number of completed frequencies is
too large after summing over kernel bands.

## Zero-Frequency and Low-Conductor Pieces

The dangerous pieces are explicit.

**`h=0`.**
The reciprocal phase disappears and the Kloosterman sum becomes a Ramanujan
or additive main term. This must be part of `Maj`.

**`k=0`.**
The completed slope interval loses one oscillatory direction. This can still
be controlled if `ht` is nonzero and the spectral input covers one-sided
Kloosterman sums; otherwise it belongs to the major projection.

**`ht=0 mod u`.**
The reciprocal phase degenerates modulo `u`. These residue classes must be
removed or shown to be inside the diagonal/residue-average main term.

**Small conductor from `q_1=q/(d,q)`.**
If the rational phase has no effective conductor, the Kloosterman estimate
must operate on the projected coefficients alone.

## Candidate Analytic Tools

**Kuznetsov or spectral large sieve.**
Use a spectral formula for the average over moduli `u` of
`S(-ht,k;u)` with smooth modulus weight.

**Deshouillers-Iwaniec type bilinear Kloosterman bounds.**
Use bilinear forms in Kloosterman sums to handle divisor-bounded Type II
coefficients and completed slope weights.

**Hybrid large sieve for additive characters.**
Before full spectral input, use large-sieve spacing to control ranges where
the completed frequencies are well separated.

**Projector-first decomposition.**
Apply the major projector before completion, so zero-frequency main terms do
not re-enter as uncancelled Kloosterman degeneracies.

## Minimal Kloosterman Input

The reciprocal branch closes if the following estimate is available.

> **Projected Bilinear Kloosterman Bound.**  
> For each dyadic `d`-slice and kernel band, after removing the exact diagonal,
> local residue means, zero-frequency completion terms, and low-conductor
> packets, the completed reciprocal-congruence contribution
> \[
> \sum_{u\sim U}\sum_{h,t,k} A_{u,h,t,k}S(-ht,k;u)
> \]
> is bounded by the assigned Poisson allowance, uniformly for `q <= Q_0`.

## Result

The reciprocal congruence route has been reduced to a projected bilinear
Kloosterman average. The decisive external analytic input is a spectral or
bilinear large-sieve estimate strong enough after summing over the completed
frequencies and kernel bands, with all zero-frequency and low-conductor main
terms removed before the estimate is applied.
