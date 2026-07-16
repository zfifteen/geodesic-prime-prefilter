# D4 Measured Link (R0 Execution)

**Status:** measured on R0 only (`p ≤ 10^6`). Not verified.

## 1. Mapping Measured Ratios to the Two-Bounds Story

The D4 bridge proposed that extreme structure in the divisor-field interior (a lower bound on witnesses) could compress the required sieve search space enough to theoretically cross the D.A.G. upper-bound limit.

From our `p ≤ 10^6` (R0) measurements in `d1_atlas/ANALYSIS_R0_p_le_1e6.json`:
- The overall mean compression ratio is **~0.038**.
- In the `small_gap` (≤ p25) cohort, the mean compression ratio is even tighter at **~0.024**.
- In the `large_gap` (≥ p75) cohort, the mean compression ratio is **~0.048**.

These measurements confirm the expected geometric correlation: smaller gaps exhibit tighter offsets (mean ~2.0) and lower compression ratios, pushing the lower bound deeper. However, **non-implication still holds**: a measured geometric offset does not force the next prime to exist unconditionally—it merely describes the divisor field where the prime was found.

## 2. UBC Floor Dominance at R0

At this magnitude (`p ≤ 10^6`), the absolute gap widths are tiny (max gap = 114). The classical unbridled sieve floor (the $K_1^c$ floor) strictly dominates. Even a compression ratio of 0.02 is applied to an already trivially small number of candidates. The theoretical "crossing" of bounds required by D4 is not visible at R0 because the lower bound is dwarfed by the UBC floor requirement. This means we cannot validate D4's collision mechanics at this scale, only observe the continuous compression scaling.

## 3. R1 Path: Next Magnitude Step

To test the geometry without waiting for gaps $> 1000$ to naturally emerge as controls, we must move away from fixed-$H$ definitions (like $H=1000$) and adopt the continuous percentile tracking observed in R0.

**Next Step (R1):**
- **Scale:** A decade slice at $10^9$ or $10^{10}$ (or a small random sample of gaps in that slice if the whole slice is too costly).
- **Control:** Instead of a fixed $H$, use within-log-bin gap percentiles. "Large-gap controls" will be defined as the top quartile ($\ge \text{p}75$) of gap widths at that magnitude, and "small-gap targets" as the bottom quartile ($\le \text{p}25$).
- **Goal:** Check if the offset mean divergence ($\sim 2.0$ vs $\sim 4.0$) and the compression ratio disparity ($\sim 0.024$ vs $\sim 0.048$) remain stable or drift as the absolute magnitude of the gaps increases, demonstrating that interior geometry scales with relative gap width rather than fixed numerical bounds.
