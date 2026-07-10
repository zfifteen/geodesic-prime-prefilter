# Offset-540 Chamber Geometry Audit — 2026-07-10

## Executive Summary

On the new `4e8-5e8` utilization maximum (`r = 424,171,123`, offset `738`,
utilization `0.9341772151898734`):

- **P1–P5 (early τ=4 / late τ=3 chamber separation) hold.**
- **P6 (fixed near-540 band `D(r) ∈ [528, 552]`) is falsified.**

The fixed-band residual claim is not a law on segment utilization maxima.
Chamber geometry (prefix min τ = 4, first τ≤3 at `D(r)`, early τ=4, zero τ=5)
persists at the new scale.

Theorem status: **Prime-Square Proximity Theorem is proved** in `PROOF.md`.
This probe is residual chamber-structure audit only. d=4 SDA transfer remains
**invalidated** and was not revived.

## Prediction Table (primary surface)

| ID | Prediction | Prior (4 segment maxima) | New `4e8-5e8` max | Status |
| --- | --- | --- | --- | --- |
| P1 | selected square branch `s² < p < r²` | 4/4 | holds | measured |
| P2 | `prefix_min_tau = 4` | 4/4 | holds | measured |
| P3 | `first_tau3_offset = D(r)` | 4/4 | `738 = 738` | measured |
| P4 | `first_tau4_offset ≤ 0.05·D(r)` | 4/4 | `3 ≤ 36` | measured |
| P5 | `tau5_count = 0` in prefix | 4/4 | holds | measured |
| P6 | `D(r) ∈ [528, 552]` | 3/4 (462 outside) | **738 falsifies** | **falsified** |

## Residual Claims

| ID | Claim | Status |
| --- | --- | --- |
| RC1 | Early τ=4 / late τ=3 chamber separation (P1–P5) holds through `4e8-5e8` | holds |
| RC2 | Fixed near-540 band on utilization maxima is a law | **falsified** |

## New Row Anatomy

| Field | Value |
| --- | --- |
| segment | `4e8-5e8` |
| `r` | `424,171,123` |
| `D(r)` | `738` |
| dynamic cutoff | `790` |
| utilization | `0.9341772151898734` |
| `o_q` | `6` |
| `first_tau4_offset` | `3` |
| `first_tau3_offset` | `738` |
| `tau4_count` | `96` |
| `tau5_count` | `0` |

## Secondary Surface (same segment, per-`o_q` maxima)

Chamber checks only (P1–P5). All three hold. Not utilization-global law claims.

| `o_q` | `r` | `D(r)` | first τ=4 | first τ=3 | τ4 count | τ5 count |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | `468,917,503` | 542 | 4 | 542 | 60 | 0 |
| 4 | `482,342,527` | 486 | 16 | 486 | 53 | 0 |
| 6 | `424,171,123` | 738 | 3 | 738 | 96 | 0 |

Full rows: `offset_540_prediction_table.json`.

## Reproduce / Falsify

```text
python3 experiments/square-branch-hourly-2026-07-10/offset_540_chamber_geometry_probe.py
```

Required inputs:

- `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
- Prior chamber baselines from `experiments/square-branch-hourly-2026-06-19/` and
  `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`
  (source clone; d=4 SDA not re-run)

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Implementation / audit surface | `4e8-5e8` no counterexample (prior hour) |
| Residual chamber claim RC1 | measured holds on new max |
| Residual fixed-band claim RC2 / P6 | **falsified** on new max |
| Invalidated d=4 SDA | remains invalidated |
