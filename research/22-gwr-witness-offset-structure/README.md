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
- 84 percent of offsets are at most 5.
- 99 percent of offsets are at most 10.
- 99.98 percent of offsets are at most 20.
- Maximum observed offset equals 48.
- The proved bound max(64, 0.5 (ln q)^2) remains far above all measured points.

## Contents

- `docs/ANALYSIS.md` — detailed reading of the visual and numerical structure.
- `docs/HEURISTICS.md` — six concrete heuristics that exploit the observed concentration.
- `scripts/generate_witness_offset_plot.py` — reproducible generation code for the main plot and statistics.
- `data/offset_stats_1e6.json` — summary statistics for the 10 to 10^6 range.

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
