# Offset-540 Chamber Geometry Audit — 2026-06-19

## Executive Summary

Six falsifiable chamber-geometry predictions **hold** on the new `3e8-4e8`
extremal row (`r = 358,018,553`, offset `546`, utilization `0.7036`). Early
τ=4 chamber / late τ=3 prime-square separation persists; offset sits in the
`[528, 552]` band near recurring `540`. The square-branch proximity theorem
remains **unresolved**; d=4 SDA transfer stays **invalidated**.

## Prediction Table

| ID | Prediction | Prior (3 rows) | New extremal | Status |
| --- | --- | --- | --- | --- |
| P1 | selected square branch `s² < p < r²` | 3/3 | holds | measured |
| P2 | `prefix_min_tau = 4` | 3/3 | holds | measured |
| P3 | `first_tau3_offset = D(r)` | 3/3 | `546 = 546` | measured |
| P4 | `first_tau4_offset ≤ 0.05·D(r)` | 3/3 | `4 ≤ 27` | measured |
| P5 | `tau5_count = 0` in prefix | 3/3 | holds | measured |
| P6 | `D(r) ∈ [528, 552]` | 2/3 exact 540, 1/3 is 462 | `546` | measured |

## New Row Anatomy

| Field | Value |
| --- | --- |
| `r` | `358,018,553` |
| `D(r)` | `546` |
| `first_tau4_offset` | `4` |
| `first_tau3_offset` | `546` |
| `tau4_count` | `64` |
| `tau5_count` | `0` |

## Reproduce

```text
python3 experiments/square-branch-hourly-2026-06-19/offset_540_chamber_geometry_probe.py
```