# Kill shapes and direction scoping

**Collab:** pgs-sieve-research-directions-collab-2026-07  
**Author:** claude  
**Date:** 2026-07-15  
**Status:** draft — for lead synthesis

---

## What a kill shape is

A kill shape is a measurement outcome (or logical finding) that would either (a) kill the direction entirely — meaning the hypothesis cannot be salvaged without a theory rewrite — or (b) force a significant redesign: different regime, different comparator, different output column. Kill shapes are *not* discouraging; they are the cheapest form of epistemic honesty. If a direction has no kill shape it is not a research question, it is a narrative.

---

## K1 — D1: Bounded-gap interior atlas

**Hypothesis:** GWR interior geometry (witness offset, divisor profile, compression ratio) measured inside bounded gaps (q−p ≤ H) is measurably distinct from GWR interior geometry in typical gaps of comparable raw width.

### Kill shapes

**K1-a: No compression ratio signal across H bands.**  
If compression ratios for gaps with q−p ≤ 246 are statistically indistinguishable from randomly sampled gaps of similar width, the "bounded-gap interior atlas" has no content. The atlas would just be a PGS measurement log, not a structural finding. *This does not kill PGS; it kills the hypothesis that bounded-gap membership predicts interior geometry.*

**K1-b: The H boundary is artificial for interior structure.**  
If witness offsets (w−p) and divisor profiles vary continuously with gap width, the sharp Zhang–Maynard cutoffs (246, 600) do not carve out structurally coherent regimes. The atlas should then be parametrised by gap width continuously, not by H thresholds. This is a redesign (change regime definition), not a kill.

**K1-c: Compression bound saturates at H=246 regime.**  
The universal compression bound (PROOF.md: w−p ≤ max(64, ⌈0.5·(log q)²⌉)) holds for all gaps. If bounded-gap primes are small enough that the constant floor (64) dominates the bound for all q in the sample, the "compression ratio" column carries no H-specific signal — the theorem already explains it with no H awareness. Redesign: restrict to sufficiently large p where the log² term dominates.

**K1-d: Interior is empty for dominant fraction of small bounded gaps.**  
If q−p ≤ 4 gaps (twin primes and near-twins at small p) dominate the H≤246 sample and these have trivially empty or near-empty interiors, the atlas is mostly degenerate entries. Redesign: require minimum gap width (e.g., q−p ≥ 10) or separate empty-interior bins.

**K1-e: GWR witness coincides with p+1 or q−1 for bounded gaps.**  
If interior structure collapses to endpoint-adjacent for most small bounded gaps, the "interior atlas" is effectively measuring endpoint proximity, not a free interior phenomenon. Redesign: separate endpoint-touching hits from genuine interior witnesses.

### Recovery path if killed

Direction 1 is redesigned as "continuous gap-width stratification of GWR interior metrics" with no H threshold claim. This is still PGS-first and empirically coherent; it loses the Zhang–Maynard linkage framing.

---

## K2 — D2: Admissible k-tuples as divisor-field labs

**Hypothesis:** For primes p that anchor a known admissible constellation hit (e.g., p, p+2, p+6 all prime), the PGS interior of the gap (p, next prime after the constellation) carries a measurable divisor-field signature different from gaps not associated with constellation anchors.

### Core non-goal (smuggling fence)

The sieve identifies *which* p anchors a constellation hit. PGS then reads the interior of the gap starting at that p. **The sieve must not infer anything about the generator value, residual class, or GWR witness position.** Admissibility tells you which p to probe; it never predicts the PGS interior. Conflating these is the category error documented in `research/constellation_vs_gap_operator.md`.

### Sampling protocol to avoid sieve inference

1. Use a classical sieve (e.g., linear sieve over p ≤ 10⁷) to enumerate admissible constellation hits: tuples (p, p+d₁, p+d₂, …) all prime for a fixed admissible pattern.
2. For each such p, record the consecutive next prime q = PGS(p) independently (do not use the constellation offsets to guess q).
3. Run standard PGS interior measurement on (p, q): GWR witness w, w−p, d(w), compression ratio, chamber count if available.
4. Compare to a control set: primes p of similar magnitude that do NOT anchor that constellation pattern.
5. The only sieve input is the selection of p. Everything downstream is divisor arithmetic.

**What counts as smuggling:** using the constellation pattern to bound the search for w (e.g., "since p+2 is prime, the interior of (p, p+2) must have w = p+1"). That turns sieve knowledge into PGS inference.

### Kill shapes

**K2-a: No signature difference between constellation anchors and controls.**  
If GWR witness offsets, divisor profiles, and compression ratios are the same for constellation-anchor primes as for controls of similar magnitude, D2 has null result. This is a clean negative: PGS interior is independent of whether p anchors a constellation. Publishable as a negative; does not kill PGS.

**K2-b: The apparent signal is entirely explained by gap size.**  
Constellation-anchor primes at small gaps (twin primes especially) automatically have different interiors because the gap is small, not because of the constellation label. If gap-width controls eliminate the signal, D2 must be redesigned with gap-width-matched controls.

**K2-c: Sample is too sparse at large p for any signal.**  
Known constellation hits above 10⁸ are sparse enough that the comparison is underpowered. Kill shape: if the signal-to-noise is too low to distinguish from random variation at any accessible scale, defer until a richer dataset or a computational sprint.

---

## K3 — D3: Sieve weights via DNI/excess

**Status:** High-risk hypothesis. Classical comparison only.

**Hypothesis:** DNI (Divisor Normalization Identity) or excess quantities from PGS correlate with the sieve weight a prime receives in a Selberg or GPY sieve. If so, there is a structural bridge between the divisor-field picture and sieve combinatorics.

### Explicit non-goals

- **No sieve-first generator.** DNI is not a sieve; it is a PGS interior measurement. DNI values must not be used to infer which integers are prime.
- **No weight transfer.** PGS does not assign sieve weights. The question is whether observed DNI quantities *correlate* with independently computed sieve weights — nothing more.
- **No new sieve bound.** This direction cannot produce a new Zhang-type bound. Any correlation found is a measurement observation; a proof connecting the two theories would require entirely separate work not in scope here.
- **Classical comparison only.** If a PGS quantity appears to track a sieve weight, the collab writes: "measured correlation, no theoretical explanation established." Not "theorem," not "implies."

### Kill shapes

**K3-a: No correlation between DNI/excess and sieve weights at any tested prime.**  
Null result. Clean, honest, expected given the theoretical gap between the two frameworks. Publishable as demarcation.

**K3-b: Apparent correlation is an artifact of prime density.**  
Both DNI and sieve weights reflect local prime density. If the correlation disappears after conditioning on local prime gaps or p·log(p) normalisation, the bridge hypothesis is spurious. Redesign: find a quantity that is independent of density before claiming a bridge.

**K3-c: DNI/excess cannot be computed for primes large enough to matter for sieve bounds.**  
Sieve results like GPY care about structure at large p. If PGS computations are only tractable below 10⁸ and the sieve correlation signal only appears near the Cramér scale (much larger), the direction is computationally blocked. Defer with a note on required compute.

**K3-d: The very definition of "sieve weight for a prime p" is ambiguous at the primorial scales PGS works at.**  
If the sieve quantity cannot be pinned down without choosing a sieve variant (Selberg vs. Bombieri–Vinogradov) in ways that change the correlation sign, D3 has no stable comparison object. Kill: the comparison is not well-defined.

### Hard fence

Even a perfect correlation (K3-a survives) does not entitle us to claim PGS "explains" or "validates" the sieve result. The bridge note, if written, must explicitly say: "PGS measures a divisor-field quantity that co-varies with the sieve weight under these conditions. Causal or structural explanation is an open problem."

---

## D4 — Two bounds, one story (light note)

D4 is not at kill risk in the same sense — the bridge note is a conceptual clarification, not a hypothesis test. The kill equivalent is: if the two bounds (GWR witness offset vs. Zhang–Maynard gap width) are shown to logically imply each other in either direction, the "two distinct bounds" framing collapses. Based on `research/constellation_vs_gap_operator.md`, they are explicitly non-equivalent: one is universal (all gaps), the other is infinitely-often (any pair). The "kill" for D4 would be discovering an argument that links them — which would be a significant positive result, not a kill. agy's D4 bridge note should document the non-implication carefully.

---

## D5 — Sieve moduli vs. modulus-link residual cells (defer/pin decision)

**Status:** Optional / negative-result friendly.

### When to defer

Defer D5 when:
- D1 probe is not yet run (D5 uses similar modular residual machinery; premature to layer it)
- The modulus-link residual cell definitions are not stable (currently mixed terminology across research notes)
- The question can be answered by a single negative-result pin rather than an open-ended experiment

### When to pin a single negative result

Run one targeted check and declare: "For primes p ≤ N, modular residual cell membership (as defined by modulus-link in PROOF.md) does not predict sieve modular structure at the same scale. Details at [data path]." Close D5 with that pin rather than leaving it open-ended.

### Decision rule for this collab

If D1 probe is ready and D2/D3 have initial results, D5 gets one pin attempt (negative-result acceptable). If D1 probe is still being specified, D5 waits. Do not run D5 and D1 in parallel on the first pass.

---

## Summary table

| Direction | Primary kill shape | Kill type | Recovery |
|---|---|---|---|
| D1 bounded-gap interior atlas | No compression signal across H bands (K1-a) | Null | Redesign: continuous gap-width stratification |
| D1 | Interior collapses to endpoint-adjacent (K1-e) | Structural | Redesign: separate endpoint-touching cases |
| D2 admissible k-tuples | No signature vs. controls (K2-a) | Null | Publishable negative; no redesign needed |
| D2 | Signal explained entirely by gap size (K2-b) | Confound | Redesign: gap-width-matched controls |
| D3 DNI/excess bridge | No correlation (K3-a) | Null | Publishable demarcation |
| D3 | Correlation is density artifact (K3-b) | Confound | Redesign: density-independent quantity first |
| D3 | Comparison object ambiguous (K3-d) | Definitional | Kill: don't run D3 until sieve quantity is pinned |
| D4 two bounds | Bounds prove equivalent | Positive result | Reframe as bridge theorem (not a kill) |
| D5 moduli | One negative pin | Intended | Close with pin, no redesign |

---

## What this file does not do

- It does not weigh relative priority of the five directions (that belongs in DIRECTIONS.md).
- It does not specify D1 probe regime or columns (that is D1_BOUNDED_GAP_INTERIOR_ATLAS.md, assigned to hermes).
- It does not write the D4 bridge argument (assigned to agy).
- It does not claim any of D1–D5 is killed. All five are open hypotheses; kill shapes are prospective.

---

*Status: done — for lead (grok) synthesis*  
*EPOCH: pgs-sieve-research-directions-collab-2026-07*
