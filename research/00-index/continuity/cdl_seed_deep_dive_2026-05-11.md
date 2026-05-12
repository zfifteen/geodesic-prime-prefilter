# CDL Seed Deep Dive

Date: 2026-05-11

Source inspected: `https://github.com/zfifteen/cognitive-distortion-layer` at commit `65fbc27`.

## Strongest Supported Reading

The Cognitive Distortion Layer began as a cognitive/perceptual curvature model, but its durable mathematical seed is exact divisor-count normalization.

The root object is an integer `n`, its divisor count `d(n)`, and the load

$$
\kappa(n)=\frac{d(n)\ln(n)}{e^2}.
$$

The forward normalization is

$$
Z(n)=\frac{n}{\exp(v\kappa(n))}.
$$

At the distinguished traversal rate

$$
v=\frac{e^2}{2},
$$

the expression collapses exactly to

$$
Z(n)=n^{1-d(n)/2}.
$$

This is the main seed that germinated into PGS. Every prime has `d(p)=2`, hence `Z(p)=1`. Every composite has `d(n)>2`, hence `Z(n)<1`. The fixed point is exact. The composite contraction is strict.

## Historical Layers In CDL

CDL carries several layers that should stay separated.

1. Cognitive metaphor layer: mathematical perception, cognitive load, geodesics, distortion, and participant-style traversal rate. This supplied the original language and intuition.
2. Integer curvature layer: `kappa(n)=d(n)ln(n)/e^2`, threshold classification, divisor-family bands, and Z-normalization.
3. Sweet-spot normalization layer: `v=e^2/2` and the exact divisor-weighted power transform.
4. Inverse traversal layer: recovery of `v` from observed `Z` sequences under explicit priors and sample regimes.
5. Continuous layer: `kappa_smooth(x)=((ln x+2gamma-1)ln x)/e^2`, useful as a large-scale average-order surrogate, not a replacement for exact integer curvature.
6. Legacy crypto prefilter layer: deterministic candidate streams, gated prime tables, fixed-base Miller-Rabin, and final `sympy.isprime` confirmation. This is a validated downstream engineering artifact, not a PGS inference mechanism.

## Important Falsification

The original fixed threshold `tau=1.5` was falsified as a prime diagnostic beyond the seed range.

On `n=50..10000`, the report records:

- accuracy `88.19%`,
- precision `100%`,
- recall `3.21%`,
- false negatives `1175`,
- prime mean `kappa=2.197`,
- composite mean `kappa=11.753`,
- separation ratio `5.35x`.

The important result is not that CDL failed. The fixed threshold failed while the curvature separation strengthened. The invariant survived and the surface rule was wrong.

That pattern matters for PGS work: when a surface heuristic breaks, first ask whether the underlying PGS or CDL invariant still holds in a sharper coordinate.

## Threshold And Band Seeds

The concept notes identify CDL as a banded scaling system.

For fixed divisor count `d(n)=k`,

$$
\kappa(n)=\frac{k\ln(n)}{e^2},
$$

so equal-divisor families move as separate logarithmic bands. Primes are the `k=2` band. Prime squares are the `k=3` upper composite envelope. Semiprimes and richer composites occupy higher bands.

This changes the threshold question from "which global cutoff works?" to "which divisor families is this cutoff merging at this scale?"

The adaptive threshold artifact records:

- `[2,49] -> tau=1.030084`, false positives `4,6,9`;
- `[50,999] -> tau=1.868096`, perfect local metrics;
- `[1000,9999] -> tau=2.492155`, perfect local metrics;
- `[10000,99999] -> tau=3.116183`, perfect local metrics.

The concept note `cdl_curvature_threshold.md` goes further and proposes a closed-form window threshold

$$
\tau=\frac{2\ln(b)}{e^2}
$$

for a window `[a,b]` under the geometric condition `a > sqrt(b)`. That claim should be treated as a promising CDL-side seed unless reproved inside PGS terms.

## Divisor-Weighted Power Transform Seeds

The draft reports on

$$
Z(n)=n^{1-d(n)/2}
$$

record exact tested separation through `100000`:

- `9592 / 9592` primes at `Z=1.0`;
- `90407 / 90407` composites below `1.0`;
- maximum composite value `0.5` at `n=4`;
- prime squares form the upper composite envelope because `d(p^2)=3`;
- high-divisor composites collapse toward zero.

Open mathematical seeds from those reports:

- level-set analysis of `Z_k(n)=n^{1-k/2}`;
- distributional asymptotics of `log Z(n)=(1-d(n)/2)log n`;
- smooth-number collapse under high divisor counts;
- inequalities or restricted quasi-multiplicativity for `Z`.

## Analytic Number Theory Seeds

The analytic bridge in CDL uses the average order of the divisor function:

$$
E[\kappa(n)]\sim\frac{(\ln n+2\gamma-1)\ln n}{e^2}.
$$

For primes,

$$
\kappa(p)=\frac{2\ln(p)}{e^2}.
$$

Recorded CDL-side evidence:

- up to `100000`: prime mean `2.813`, composite mean `18.213`, ratio `6.47x`, smooth error `0.19%`;
- up to `500000`: prime mean `3.254`, composite mean `23.608`, ratio `7.26x`, smooth error `0.13%`;
- smooth projection at `10^7`: `8.14x`.

This supports a concrete interpretation: average composite curvature grows like a quadratic logarithmic term, while prime curvature grows linearly in `ln n`.

## Inverse Traversal Seeds

CDL framed `v` first as a manual traversal parameter. Later experiments made it recoverable under explicit regimes.

The v-inference benchmark records:

- best aggregate cell: `mle`, random sequences, `M=5000`, MAE `0.0131`;
- fingerprint recovery on random sequences at `M=5000`: MAE `0.0157`;
- moment matching on prime-biased sequences at `M=5000`: MAE `0.0275`;
- composite-heavy sequences favor fingerprint recovery: MAE `0.0637`;
- `8` aggregate cells clear `90%` success.

The continuous extension records:

- continuous variance reduction `98.74%`;
- continuous fingerprint `v` recovery MAE `0.0064` at `M=5000` and `3%` noise.

The cognitive pilot records:

- `50` participants and `200` trials each;
- hybrid fingerprint recovery MAE `0.0705`;
- `90%` success at `|error| < 0.15`;
- recovered low-v cluster `0.80 +/- 0.16`;
- recovered high-v cluster `1.80 +/- 0.30`;
- psychophysical compression correlation `0.980`.

These are operational recovery results under stated priors and supports. They are not arbitrary inversion of unknown integers from `Z`.

## How CDL Connects To PGS

The direct lineage into PGS is:

```text
divisor count load -> sweet-spot Z fixed point -> exact prime/composite separation -> divisor-count interior ordering -> leftmost minimum-divisor selected integer -> prime-gap endpoint structure
```

PGS sharpens the CDL fixed-point observation into gap-local deterministic structure.

In PGS terms:

- `Z(p)=1` is the prime baseline.
- Interior composites satisfy `Z(n)<1`.
- Maximizing `log Z(n)=(1-d(n)/2)log n` inside a prime gap selects the leftmost interior integer with minimum divisor count.
- The endpoint `q` is the first later integer with divisor count `2`.

The CDL seed is therefore not "curvature as a classifier." The seed is divisor-count normalization as an invariant coordinate for reading integer structure.

## Boundaries To Preserve

Do not import the CDL crypto prefilter as PGS inference. It uses gated factor tables, `gcd`, Miller-Rabin, and `sympy.isprime` in a legacy downstream role. That is compatible as a historical engineering artifact, but not as a PGS generator mechanism.

Do not treat fixed-threshold CDL classification as a theorem. The fixed threshold was falsified. The banded family structure and exact sweet-spot transform are the stronger mathematical objects.

Do not replace exact integer curvature with `kappa_smooth(x)` when exact divisor structure matters. The smooth layer is an average-order bridge for continuous or large-scale support, not a substitute for PGS-native divisor counts.

## Fruit Still On The Tree

The most promising ungerminated seeds are:

1. Closed-form threshold geometry for narrow windows, especially the `a > sqrt(b)` condition.
2. Divisor-family band dynamics on log-log or equal-percentage axes.
3. Prime-square and semiprime envelope theory as the upper composite boundary beneath the prime fixed point.
4. Level-set and distribution theory for `Z_k(n)=n^{1-k/2}`.
5. Restricted quasi-multiplicativity or inequality structure of the divisor-weighted power transform.
6. Exact relationship between CDL band geometry and PGS chamber resets.
7. Transport of `v=e^2/2` fixed-point cancellation into endpoint-chain or modulus-link coordinates without using classical factor gates.
8. A rigorous distinction between exact integer curvature, average-order smooth curvature, and participant-style traversal recovery.

