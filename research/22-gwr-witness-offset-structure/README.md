# GWR Witness Offset Structure

## Purpose

This folder records an empirical observation of strong structure in the GWR witness offsets.

The Gap Winner Rule selects the leftmost integer of minimum divisor count inside each prime gap.
The distance from the left prime p to that winner is the witness offset w - p.

Plots of these offsets against ln(q) reveal clear horizontal layering and extreme concentration at small integers.

## Scope

Data covers every consecutive prime gap from 10 to 10^6.
This yields 78 493 gaps.

## Key Empirical Facts

- Median offset equals 2.
- Mean offset approximately 3.15.
- 84 percent of offsets are at most 5.
- 99 percent of offsets are at most 10.
- 99.98 percent of offsets are at most 20.
- Maximum observed offset equals 48.
- The proved bound max(64, 0.5 (ln q)^2) remains far above all measured points.

Full numeric summary (from exact GWR selection on the surface):

```json
{
  "num_gaps": 78493,
  "max_offset": 48,
  "mean_offset": 3.153313034283312,
  "median_offset": 2.0,
  "p90": 6.0,
  "p95": 7.0,
  "p99": 10.0,
  "fraction_offset_le_5": 0.8427757889238531,
  "fraction_offset_le_10": 0.9919738065814786,
  "fraction_offset_le_20": 0.9998471201253615,
  "max_lnq": 13.815493557819773,
  "range": "primes 10 to 1e6"
}
```

## Contents

- `docs/ANALYSIS.md` — detailed reading of the visual and numerical structure.
- `docs/HEURISTICS.md` — six concrete heuristics that exploit the observed concentration.
- `docs/PROVENANCE.md` — session origin.
- `scripts/generate_witness_offset_plot.py` — reproducible generation code for the main plot and statistics.

## Relation to Existing Work

This observation sits downstream of the proved universal bounded compression theorem in research/04-bounded-compression and the GWR maximizer theorem.

The plots confirm the theorem holds with large practical margin on the tested range.
The structure itself supplies new heuristic levers for search and generation.

## Next Steps

1. Extend the measurement ladder past 10^7 and 10^8.
2. Fit a tighter empirical envelope to the upper edge of the offset cloud.
3. Implement and time the early-window priority scan heuristic.
4. Test whether the same concentration persists for the reduced gap-type surface.

## Provenance

Observation arose from visual inspection of the bounded-compression scatter plot generated during a 2026-08 research session.
All numbers above are computed from exact divisor counts via the standard GWR selection rule.
