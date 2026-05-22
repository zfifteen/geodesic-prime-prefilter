# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-22T19:18:37.978634+00:00
**Reference factor space**: 198 words
**Samples per level**: 15

## Results by Bit Length

| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |
|------|---------------|---------|-----|-----|------------|
| 48 | 38.42% | 24.75% | 0.0% | 71.7% | 0 |
| 56 | 35.89% | 29.66% | 0.0% | 69.2% | 0 |
| 64 | 34.11% | 19.97% | 0.0% | 72.7% | 0 |
| 72 | 27.91% | 26.82% | 0.0% | 72.7% | 0 |

## Interpretation

This ladder measures the raw power of the current public grammar rule set 
when applied to realistic public structural motifs at different scales. 
It assumes the public motif (GWR/DNI attractor + phase) has been obtained 
via public means for each N. The reduction % is therefore the amount of 
factor-neighborhood hypothesis space that can be safely excluded *before* 
any private factorization work.

Stable or increasing reduction as bit length grows indicates that the 
multiplicative grammar incompatibilities captured by the rules are 
structural and scale-invariant.

## Notes

- Motifs were sampled from the empirical distribution observed on 
  previous multiplication-map surfaces (heavily o2_a2@mid dominant).
- Unresolved cases (0% reduction) occur when a motif outside the current 
  rule coverage is sampled. In real use these would be handled by 
  extending the rule set or falling back to other methods.

Run with `--samples 100` for tighter statistics.
