# CORRELATION_REPORT — Remainder-Gap-Prime Placement Analysis

**Date of first run:** 2026-06-30 (initial skeleton + tiny validation)
**Regime:** First validated collection surface (p <= 600, 108 gaps, 490 records, max observed g=18). Moduli M_v1.
**Collector raw source:** research/remainders/output/tiny_val/raw_records.jsonl
**Exact commands logged below and in collector RUN_LOG.**

## PGS Frame (repeated for every report)
Ordered gap interiors → divisor-count field + GWR leftmost min-d → remainder vector R(n, M) attached as coordinate.
All numbers below are empirical measurements on this surface. They are not theorems.

## Parameters Used (first run)
- Sample: existing tiny_val (reproducible, no new collection needed for skeleton)
- Binning: norm_position_bin = floor(10 * k/g) ; gap_size_bin = floor(g/4) or similar (exact scheme recorded in tables)
- Derived features computed: 
  - num_zeros_in_vector
  - residue_sum_parity
  - dist_nearest_zero_mod30
  - dist_nearest_zero_mod210
  - coprime_to_210
- Random seeds: none for descriptive; any for sampling or CV noted.
- Disjoint later validation: planned for <1e6 vs higher.

## Phase 1 Data Prep Status
[To be filled after enrichment step]

## Phase 2 Descriptive Correlations
### Marginal residue distributions
(Heatmap / table placeholder)

### Mutual information remainder → termination
(placeholder)

### H1: Remainder entropy vs realized g
(placeholder — measured correlation or null)

### H4: GWR vector distinct from gap average
(placeholder)

## Phase 3 Hypothesis Tests (initial)
- H1 result + p-value (permutation) + effect size
- ...

## Phase 4 Visuals & Ranking
- Tables
- Text heatmaps
- Summary ranking

## Phase 5 Feedback Proposals
Any signal above threshold → concrete suggestion (e.g. "add residue != X mod 210 near end as early reject in chamber").

## Reproducibility
- All numbers generated from the exact raw_records.jsonl listed above.
- Python version / platform in linked RUN_LOG.
- Binning and feature code version pinned by git commit of this report + scripts.

## Next Steps
See PLAN.md continuation table.

**End of current report section.** (Append new dated blocks for larger runs.)
