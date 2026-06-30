# CORRELATION_REPORT — Remainder-Gap-Prime Placement Analysis

**Date of first run:** 2026-06-30 (initial skeleton + tiny validation)
**Regime:** First validated collection surface (p <= 600, 108 gaps, 490 records, max observed g=18). Moduli M_v1.
**Collector raw source:** research/remainders/output/tiny_val/raw_records.jsonl
**Exact commands logged below and in collector RUN_LOG.**

## Review of Plan — Choices Made (per Next Action)
- Preferred initial gap sample size/range for first correlation run: the already-validated tiny_val set (108 gaps / 490 records, p<=600) for rapid skeleton validation and engine bring-up. Followed immediately by production of a modestly larger surface (example target --max-p 20000) once descriptive primitives are solid. Later Phase-5 will use disjoint ranges (<1e6 full + sample 1e9+).
- Additional derived remainder features: plan-specified (num_zeros_in_vector, residue_sum_parity, dist_nearest_zero_mod30, dist_nearest_zero_mod210, coprime_to_210) plus the two minimal "coprime_to_210" (already) and residue_sum_parity already covered.
- Prioritization order: Descriptive surfaces + H1 (entropy vs g), H4 (GWR signature), marginals and sequential patterns first. Predictive modeling (H3 logistic delta) and formal tests second, after descriptive reproducibility is proven on the set. This matches incremental discipline and protects against small-sample modeling artifacts.

Enrichment command used:
python research/remainders/enrich_remainder_records.py --input .../tiny_val/raw_records.jsonl --output .../correlations/enriched/tiny_enriched.jsonl

(490 records produced.)

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
Computed on enriched tiny_val (first 490 records). 37 populated (pos_bin, gap_bin) groups.

Example (mod-2 / slot 0 frequencies, truncated):

| pos_bin | gap_bin | res | count | freq |
|---------|---------|-----|-------|------|
| pos0 | g3 | 0 | 7 | 1.000 |
| pos0 | g4 | 0 | 1 | 1.000 |
| pos1 | g1 | 0 | 31 | 1.000 |
| pos1 | g2 | 0 | 16 | 1.000 |
| pos1 | g3 | 1 | 7 | 1.000 |
| pos1 | g4 | 0 | 1 | 0.500 |
| pos1 | g4 | 1 | 1 | 0.500 |
| pos2 | g1 | 0 | 26 | 1.000 |

Full table written to `tiny_demo/mod2_marginal_sample.md` (reproducible from the enriched file + code at the git commit of this report).

### Mutual information remainder → termination
(placeholder — next increment)

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
