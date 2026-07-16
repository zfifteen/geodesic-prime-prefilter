# MEASURED_PRESSURE.md

**Author:** claude (expanded from grok seed)  
**Date:** 2026-07-15  
**Collab epoch:** pgs-new-theorem-collab-2026-07  
**Source:** R0 (p ≤ 10⁶, 78,498 pairs) and R1 (p ≤ 10⁷, 664,579 pairs) only  
**Status:** measured motivation — not verified, not theorem, not universal

---

## Scope declaration

Everything in this file is **measured observation** from the R0/R1 atlas. It does not:

- Prove any bound universally.
- Extend beyond the `p ≤ 10⁷` measurement regime.
- Override or supplement UBC (`w − p ≤ max(64, ⌈0.5 log(q)²⌉)`), which is already proved universally.
- Use verified language anywhere. The word "verified" does not appear because it does not apply.

The purpose of this file is to show where R0/R1 data lends pressure in favor of each candidate part, and where it is conspicuously silent, inadequate, or potentially hostile.

---

## R0/R1 band summary (from MEASURED_GROUNDING.md + atlas paths)

| Regime | Pairs | Max gap | Small-gap mean δ | Large-gap mean δ |
|--------|------:|--------:|----------------:|----------------:|
| R0 (p ≤ 10⁶) | 78,498 | 114 | ~1.99 | ~4.01 |
| R1 (p ≤ 10⁷) | 664,579 | 154 | ~2.004 | ~4.499 |

Continuous R1 band: mean δ rises from ~2 at g=2 through g≈20, then plateaus near ~4–4.5 through the max gap (154).

**Atlas paths:**
- `experiments/pgs-sieve-research-directions-collab-2026-07/execution/d1_atlas/ANALYSIS_R0_p_le_1e6.json`
- `.../ANALYSIS_R1_p_le_1e7.json`
- `MEASURED_GROUNDING.md` in this package

---

## Smuggling kill (mandatory)

**Killed claim:** "Mean δ ≈ 4 is universal for all sufficiently large consecutive prime gaps."

Kill reasons:
1. R0/R1 measure p ≤ 10⁷. Cramér-scale gaps for p ~ 10^14 can reach thousands. No measurement covers that regime.
2. The plateau near 4–4.5 in R1 is real for g ≤ 154 — but g ≥ 100 pairs are thin in R1 (likely O(10) pairs). Means computed over thin samples do not anchor a universal claim.
3. UBC already bounds worst-case δ as O((log q)²) universally. B2's measured plateau is below UBC by orders of magnitude for large primes — but UBC is the proved universal bound, not "δ ≤ 5."
4. The plateau could widen with regime. There is no measured evidence that it does not, and no proof that it stays constant.

**Correct language for any use of this data:** "In R1 (p ≤ 10⁷), mean GWR witness offset stabilizes near 4–4.5 for g ≥ ~20, through the measured maximum gap of 154. This is a feature of the R1 domain only. No universality is claimed."

---

## Pressure by candidate part

### Part A

**A1/A2 (g=2 and g=4):** R1 fully covers all twin and cousin-prime pairs in p ≤ 10⁷. Every twin pair yields δ=1; every g=4 pair yields δ ∈ {1,2,3}. The data confirms these but adds no information — A1/A2 are definitional claims that precede measurement.

**Pressure: maximal and redundant. Measurement cannot surprise us here.**

**A3 (small-g classification g ∈ {2,4,6,8,10}):** R0/R1 provide full coverage of all gap-4, gap-6, gap-8, gap-10 pairs. A per-g-width δ frequency table is computable from the atlas and would tell hermes exactly which modular cases dominate and which are rare. Not yet computed explicitly in this atlas.

**Gap in atlas:** no per-gap-width (g-exact) stratification of the δ distribution is currently in MEASURED_GROUNDING.md. This is the highest-value analysis to add for Part A support.

---

### Part B

**B1 (stochastic ordering of δ distribution in g):**

The aggregate band means (small ~2.0 → large ~4.5) are consistent with mean ordering as g grows. But stochastic dominance (every quantile ordered, not just the mean) requires CDF comparison at individual g values.

**Missing CDF analysis:** for B1 to get measured support, we need the empirical CDF of δ for g=4, g=6, g=8, g=10, g=12, g=20, g=50 separately. If CDFs for g=6 dominate g=4 everywhere (no crossing), B1 gets support. If they cross, B1 is at minimum weakened and at worst measured-killed.

**Current status:** R0/R1 give **motivation only** for B1. Mean ordering is suggestive; stochastic ordering is unverified by current atlas.

**B2 (mean δ saturation):**

See smuggling kill above. In measured terms:

- The plateau story is real and consistent within R1.
- The plateau is based on thin sample at high g (g ≥ 100 pairs in R1 are few dozen at most). Mean δ for those thin bands should report confidence intervals, not just point means.
- The measured suggestion is: "A saturation law *may* exist; R1 shows the plateau through g=154." Nothing more.

**Correct status for B2:** measured hypothesis, not measured-verified, and not close to proved. The R1 atlas motivates further measurement (R2 extending to p ≤ 10^9 or beyond) more than it supports promotion.

---

### Part C

**C1 (g=2 left-adjacent):** same as A1. Full support, redundant.

**C2 (g=4 frequency):** the g=4-specific δ frequency table is not in the current grounding file. R1 has enough g=4 pairs to give a robust frequency split (likely thousands of such pairs). This is a quick computation from the atlas.

**Current status:** supportive in principle; exact frequency counts not yet extracted.

---

## Band statistics missing from current atlas

These analyses would turn the current "motivation only" status into "measured support" for several parts:

1. **Per-g-width δ distribution** for each g from 2 through 50 in R1 (mean, median, 75th/90th percentile per width).
2. **Pair count per g-width band** for g ≥ 50, 100, 130 in R1 — to reveal statistical thinness of the plateau claim at high g.
3. **CDF of δ** at g ∈ {4, 6, 8, 10, 12} separately — to test B1's stochastic ordering claim.
4. **δ frequency table for g=2 and g=4 exactly** — to support A2/C2 frequency extensions.
5. **Confidence intervals on plateau mean** for g ≥ 100 in R1 — to honestly represent thin-sample uncertainty.

None of these are new data collection; they are aggregation passes over the existing R0/R1 atlas.

---

## Summary table

| Part | R0/R1 support | Honest label | Key missing analysis |
|------|--------------|--------------|----------------------|
| A1/C1 | Full (definitional) | Confirmed in domain | None needed |
| A2 bare | Full (trivial) | Confirmed in domain | Per-g frequency split |
| A3 | In principle full | Motivated | Per-g stratification not run |
| B1 stochastic | Motivation only | Unverified in domain | CDF per g-width |
| B2 universal | No support | Killed as universal | R2+ regime needed |
| B2 R1-local | Thin at high g | Observed with caveats | Band pair counts + CI |
| C2 bare | Full (trivial) | Confirmed | Per-g frequency split |
| C2 freq | In principle | Motivated | g=4 stratification |

**For lead synthesis (grok):** the A/C parts are safe and measured-confirmed where it matters. Part B is the risk zone — B2 universal is killed, B1 stochastic is unverified, and the plateau story needs honest thinness-of-sample caveats before any use in a candidate statement.
