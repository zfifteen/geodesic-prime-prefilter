# Remainder Statistics (research/remainders/)

This directory holds the implementation and measured surfaces for remainder/residue pattern collection inside prime gaps.

See `PLAN.md` for the full contract, phases, and success criteria.

## Quick Start (after validation)

```bash
# 100-gap scale validation set (already clean per tests)
python research/remainders/collect_remainder_stats.py \
  --max-p 600 \
  --output-dir research/remainders/output/tiny_val/

# First serious surface (>>10^5 gaps)
python research/remainders/collect_remainder_stats.py \
  --max-p 1000000 \
  --output-dir research/remainders/output/1e6/
```

## Current Status (2026-06-30)
- remainder_utils.py: pure stdlib compute_residues (M_v1 = [2,3,5,7,30,210,2310])
- collect_remainder_stats.py: full emitter + CLI
- 11 tests, including dedicated 100-gap validation gate
- Reproducible raw_records.jsonl + summary + RUN_LOG.md per run
- Hand-checked on p=113 (GWR at 121), p=3 etc.

All artifacts follow:
- PGS objects first (gap state, d(n) field, GWR winner)
- Strict separation (measured/hypothesis only)
- Incremental validation rule

Next: Phase 3 target statistics (entropy, enrichment at GWR, mutual info) + HTML summary report.
