# DNI-to-Zeta Compression and the Riemann Hypothesis

The bridge between the **Divisor Normalization Identity** (DNI) and the Riemann
Hypothesis begins with the exact integer source, not with zeta zeros:

every positive integer has a divisor count `d(n)`, primes are exactly the
returns to `d(n)=2`, and prime gaps are the finite interiors between
consecutive returns. The arithmetic structure inside prime gaps identifies the
integer-level source that the zeta function later records in compressed form.

In this repository, the DNI is

$$
Z(n) = n^{1 - d(n)/2}
$$

at the normalization scaling parameter

$$
v = \frac{e^2}{2},
$$

with divisor normalization load

$$
\kappa(n) = \frac{d(n)\ln n}{e^2}.
$$

That is the coefficient-side arithmetic surface of the project.

The Riemann Hypothesis is the classical pole-placement target for the same
source after zeta compression. The shared structure is not a loose resemblance:
the exact quotient can be written down, while pole placement remains a
separate source-to-spectral proof target.

## Status And Direction

This bridge does not turn PGS into a zeta-side restatement of RH. PGS is the
source-side arithmetic mechanism. The pole-placement sentence is the classical
compressed target attached to that source structure.

- Explanatory status: PGS supplies the upstream divisor-count structure whose
  analytic compression produces the RH pole-placement language.
- Bridge status: the DNI Dirichlet-series objects recover
  `R(s) = -zeta'(s)/zeta(s)` exactly on `Re(s) > 1`, with the same
  meromorphic continuation through the zeta identity.
- Formal artifact status: `PROOF.md` proves the local next-prime and
  gap-interior theorems. The RH-facing program records how the exact
  integer-level source is read after zeta compression. Pole placement is the
  downstream zeta-language target, not the object that defines PGS.

The controlling direction is:

```text
divisor counts -> DNI/GWR prime placement -> zeta compression
-> source-to-spectral placement target -> RH pole-placement language
```

Classical approaches begin with the analytic shadow. This bridge identifies
the arithmetic structure casting it.

## Exact Dirichlet-Series Bridge

Start with the divisor-count Dirichlet series on the half-plane
$\mathrm{Re}(s) > 1$:

$$
D(s) = \sum_{n \ge 1} \frac{d(n)}{n^s} = \zeta(s)^2.
$$

Now build the generating series for the DNI divisor normalization load:

$$
K(s) = \sum_{n \ge 1} \frac{\kappa(n)}{n^s}
= \frac{1}{e^2}\sum_{n \ge 1} \frac{d(n)\ln n}{n^s}.
$$

Differentiate $D(s)$ termwise on the same half-plane:

$$
D'(s)
= -\sum_{n \ge 1} \frac{d(n)\ln n}{n^s}.
$$

So the divisor normalization series is

$$
K(s) = -\frac{1}{e^2}D'(s).
$$

At the normalization scaling parameter $v = e^2/2$, the normalized load-to-divisor
ratio is therefore

$$
v \frac{K(s)}{D(s)}
= \frac{e^2}{2}\frac{K(s)}{D(s)}
= -\frac{1}{2}\frac{D'(s)}{D(s)}
= -\frac{\zeta'(s)}{\zeta(s)}.
$$

The classical Euler-product identity then gives

$$
-\frac{\zeta'(s)}{\zeta(s)}
= \sum_{n \ge 1} \frac{\Lambda(n)}{n^s},
$$

where $\Lambda(n)$ is the von Mangoldt function.

This is the exact arithmetic bridge:

- the DNI begins from `d(n)` and `kappa(n)`,
- their native Dirichlet series recover $\zeta(s)^2$ and its logarithmic derivative,
- and the fixed-parameter DNI normalization lands directly on the classical
  prime-power detector $-\zeta'/\zeta$.

That bridge is already present before any spectral interpretation is added.

## Proposition

On the half-plane $\mathrm{Re}(s) > 1$,

$$
D(s) = \zeta(s)^2,
\qquad
K(s) = -\frac{1}{e^2}D'(s),
\qquad
\frac{e^2}{2}\frac{K(s)}{D(s)} = -\frac{\zeta'(s)}{\zeta(s)}
= \sum_{n \ge 1} \frac{\Lambda(n)}{n^s}.
$$

Since $D(s)=\zeta(s)^2$ on that half-plane, the same identities determine
the meromorphic continuation of the DNI-built objects:

- $D(s)$ continues as $\zeta(s)^2$,
- $K(s)$ continues as $-D'(s)/e^2$,
- and the normalized ratio continues as $-\zeta'(s)/\zeta(s)$.

So the DNI does not merely resemble an analytic prime detector.

Its native generating objects reconstruct the standard one exactly.

## Why the Normalization Scaling Parameter Is Native Here

The role of the repository constant

$$
v = \frac{e^2}{2}
$$

has two exact meanings in this project.

On the integer-score side, it is the normalization scaling parameter at which the DNI
collapses to

$$
Z(n) = n^{1-d(n)/2}.
$$

On the Dirichlet-series side, the same scalar is the one that cancels the
factor $2$ coming from differentiating

$$
D(s)=\zeta(s)^2.
$$

That is,

$$
\frac{e^2}{2}\frac{K(s)}{D(s)}
= \frac{e^2}{2}\left(-\frac{1}{e^2}\frac{D'(s)}{D(s)}\right)
= -\frac{1}{2}\frac{D'(s)}{D(s)}
= -\frac{\zeta'(s)}{\zeta(s)}.
$$

If the divisor normalization were rescaled, this scalar would change with
it. Under the repository's fixed definition
$\kappa(n)=d(n)\ln n/e^2$, $v=e^2/2$ is the exact native scalar on both
sides of the bridge.

## Coefficient-Side and Spectral-Side Collapse

The DNI and the Riemann Hypothesis each collapse arithmetic structure onto a
one-dimensional invariant endpoint.

For the DNI:

- if $p$ is prime, then $d(p)=2$,
- so $Z(p)=1$ exactly,
- and primes lie on the fixed-point locus $Z = 1.0$.

For the Riemann Hypothesis in classical zeta language:

- the nontrivial zeros of $\zeta(s)$ satisfy the pole-language condition
  $\mathrm{Re}(s)=1/2$,
- so the zero set collapses onto one vertical line in the complex plane.

These are different objects, but they have the same formal shape:

- DNI gives a coefficient-side collapse on the integer score function,
- RH asks for a spectral-side collapse on the analytic continuation of the
  generating object after zeta compression,
- both single out one invariant locus rather than a diffuse region.

This is the most compact conceptual narrative for the synergy:

the DNI fixes where primes sit in the arithmetic score function generated by
divisor structure, while RH is the zeta-language placement target for the same
source after analytic compression.

## RH as Pole Placement of the DNI Ratio

The continued ratio

$$
R(s) = \frac{e^2}{2}\frac{K(s)}{D(s)}
$$

is not a new auxiliary object. It is exactly

$$
R(s) = -\frac{\zeta'(s)}{\zeta(s)}.
$$

That gives the downstream classical translation of the RH connection. PGS is
the source-side arithmetic mechanism whose analytic compression produces the
ratio. The pole-placement sentence is the classical wording of that
compression, not the object that defines PGS.

- the simple pole at $s=1$ is the prime-number-theorem pole,
- the trivial zeros of $\zeta$ become trivial poles of $R(s)$,
- the nontrivial zeros of $\zeta$ become nontrivial poles of $R(s)$.

So the Riemann Hypothesis is read as a pole-placement statement for the
continued DNI ratio:

all nontrivial poles of
$\frac{e^2}{2}\frac{K(s)}{D(s)}$ lie on the critical line
$\mathrm{Re}(s)=1/2$.

This is a precise analytic reading, not a metaphor.

It also clarifies the presentation surface:

- DNI supplies the coefficient-side construction of the ratio,
- meromorphic continuation is the zeta-language compression surface,
- RH pole language records the nontrivial pole placement of that same ratio.

## Why the Near-Endpoint Raw-Z Peak Program Fits Naturally Beside RH

Prime gaps have two endpoints and a composite interior.

The Riemann Hypothesis matters most when prime locations are studied in short
intervals, because zeta-zero geometry governs how sharply prime counts can
fluctuate around their main term.

The DNI near-endpoint raw-Z peak program studies the complementary part of that same local
picture:

- once the prime endpoints are fixed,
- which interior composites sit closest to the prime locus,
- and what arithmetic structure determines the local raw-`Z` peak.

The current repository already has exact and tested interior structure for that
question:

- the gap-local raw-`Z` maximum is enriched at edge distance `2`,
- the integer is overwhelmingly `d(n)=4`,
- and on the tested surface the peak agrees exactly with the lexicographic rule
  "smallest `d(n)`, then leftmost".

Those results are documented in:

- [research/11-gap-ridge/docs/dni_gap_ridge.md](../../11-gap-ridge/docs/dni_gap_ridge.md)
- [research/11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md](../../11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md)
- [research/11-gap-ridge/docs/findings/lexicographic_winner_take_all_peak_rule.md](../../11-gap-ridge/docs/findings/lexicographic_winner_take_all_peak_rule.md)

This creates a natural division of labor.

On the endpoint side, RH and explicit-formula methods describe the analytic
shadow of prime endpoint behavior after zeta compression.

On the interior side, the DNI score function ranks the composites that fill the gap
between those endpoints.

That is a genuine structural fit:

- RH records prime-gap endpoint behavior through zeta-zero geometry,
- DNI organizes prime-gap interior behavior through divisor-normalization geometry.

## Why the `d(n)=4` Ridge Matters

The prime locus is the `d(n)=2` layer.

The first composite layer adjacent to it is the `d(n)=4` layer, including
numbers such as $pq$ with distinct primes $p$ and $q$, and also prime
cubes $p^3$. For that layer,

$$
d(n)=4
\qquad\Longrightarrow\qquad
Z(n)=n^{-1}.
$$

That layer is not rare decoration in the current repository. It is the
dominant integer of the gap-local raw-`Z` peak on the tested surface.

The same divisor count belongs naturally to the $\zeta(s)^2$ side of the
bridge because `d(n)` is exactly the coefficient sequence of that square.

This gives a precise arithmetic reading of the observed ridge:

- primes form the fixed-point `d=2` locus,
- the strongest composite layer adjacent to that locus is the `d=4` layer,
- and the near-endpoint raw-Z peak result says that this first composite layer dominates the
  interior peak geometry.

So the DNI near-endpoint raw-Z peak is not only a spatial statement about where the interior
peak sits. It is also a statement about which divisor-complexity layer sits
closest to the prime locus inside the exact integer score function.

## Residue-Class Structure and the L-Function Direction

The current repository also shows that the orientation of the near-edge ridge
depends materially on the left endpoint prime modulo `30`.

That result is documented in
[research/11-gap-ridge/docs/gap_ridge/residue_mod30_ridge_orientation_note.md](../../11-gap-ridge/docs/gap_ridge/residue_mod30_ridge_orientation_note.md)
and
[research/11-gap-ridge/docs/findings/residue_mod30_ridge_orientation.md](../../11-gap-ridge/docs/findings/residue_mod30_ridge_orientation.md).

This matters because congruence classes are already the natural language for
Dirichlet characters and L-functions.

The arithmetic progression direction of prime-distribution theory does not
replace the zeta function. It refines it by splitting the integer line into
residue-conditioned subfamilies.

That means the residue-modulated ridge orientation has a natural next analytic
home:

- the global DNI score function sits beside $\zeta(s)$,
- residue-conditioned DNI subregimes sit beside character-weighted L-series.

The current repository does not need to widen its production path to use that
fact. It is already enough that the same organizing variable appears on both
sides:

- residue class on the arithmetic-score side,
- character decomposition on the analytic side.

## What This Suggests Technically

The strongest next research path is to keep the source order intact: treat the
DNI as a coefficient-side geometry whose native generating functions already
recover the classical zeta detector.

That yields several concrete PGS-side tasks.

1. Study the DNI divisor series $D(s)=\zeta(s)^2$ and normalization series
   $K(s)=-(1/e^2)D'(s)$ as the canonical analytic envelope of the DNI score function.
2. Express gap-local DNI observables against short-interval prime statistics,
   especially interior peak location and `d(n)=4` selected-divisor-count share.
3. Build residue-conditioned versions of those observables and compare them to
   the arithmetic-progression side of prime distribution.
4. State the PGS integer structure before translating it into Hilbert-space,
   transfer-operator, or pole-placement language.

This order keeps the arithmetic facts in front:

- first identify the exact generating objects,
- then identify the tested local observables,
- then identify which PGS invariant is being carried into the analytic object,
- then read the classical pole-placement statement as the downstream
  zeta-language description of that integer-level structure.

## Scope

This repository already establishes:

- the exact DNI at $v = e^2/2$,
- the deterministic production prefilter built from that invariant,
- and the exact raw-DNI near-endpoint raw-Z peak observables developed in the committed notes
  and benchmark artifacts.

This note records why those objects identify the exact zeta-language object
whose pole placement is the Riemann Hypothesis.

The exact bridge is the formula

$$
\frac{e^2}{2}\frac{K(s)}{D(s)} = -\frac{\zeta'(s)}{\zeta(s)}.
$$

That identity is enough to make the relationship precise:

- DNI supplies a local integer-score geometry built from divisor structure,
- RH is the zero-geometry placement target for the analytic detector recovered
  from that same divisor-normalization envelope.

## Input prime Documents

For the exact DNI and production path:

- [research/06-cryptology-rsa/legacy-prefilter/docs/dni_prefilter.md](../../06-cryptology-rsa/legacy-prefilter/docs/dni_prefilter.md)
- [research/06-cryptology-rsa/legacy-prefilter/technical-note/technical_note.md](../../06-cryptology-rsa/legacy-prefilter/technical-note/technical_note.md)
- [spec/contract.md](../../../spec/contract.md)
- [the RH bridge helpers](../../../src/python/z_band_prime_rh_bridge/bridge.py)

For the exact near-endpoint raw-Z peak research surface:

- [research/11-gap-ridge/docs/dni_gap_ridge.md](../../11-gap-ridge/docs/dni_gap_ridge.md)
- [research/11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md](../../11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md)
- [research/11-gap-ridge/docs/gap_ridge/residue_mod30_ridge_orientation_note.md](../../11-gap-ridge/docs/gap_ridge/residue_mod30_ridge_orientation_note.md)
- [research/11-gap-ridge/docs/findings/lexicographic_winner_take_all_peak_rule.md](../../11-gap-ridge/docs/findings/lexicographic_winner_take_all_peak_rule.md)
