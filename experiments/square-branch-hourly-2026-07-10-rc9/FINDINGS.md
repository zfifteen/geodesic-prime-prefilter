# Offset-540 Residual Claims RC9–RC11 — 2026-07-10

## Executive Summary

After RC6–RC8 (o_q-panel phase order, late-dominant phase_gap, near-540
exclusivity), this hour formalizes the **next residual chamber structure** on
the **interior τ4 offset set** of segment utilization maxima through `4e8–5e8`
and the full per-`o_q` branch-max panel. None of these is a theorem. d=4 SDA is
not revived. Fixed-band RC2 remains falsified. Prime-Square Proximity remains
**proved** in `PROOF.md`.

| ID | Claim | Status on surface through `4e8–5e8` |
| --- | --- | --- |
| RC9 | Early-half τ4 mass `≥ 0.40` | **holds** (min observed `0.4151`) |
| RC10 | Late-span τ4 `last_τ4 / D ≥ 0.95` | **holds** (min observed `0.9631`) |
| RC11 | No large τ4 desert `max_gap / D ≤ 0.10` | **holds** (max observed `0.0812`) |
| RC2 | Fixed band `[528, 552]` on segment util maxima is a law | **falsified** (retained) |
| RC6–RC8 | Prior residual surface | **retained holds** (not primary surface) |

## Prediction Table (new surface)

| ID | Prediction | Primary surface | Status |
| --- | --- | --- | --- |
| P13 | early-half τ4 mass `≥ 0.40` | 5 util maxima + 3 o_q rows | holds |
| P14 | `last_τ4 / D ≥ 0.95` | same | holds |
| P15 | `max_gap / D ≤ 0.10` (lead + interior + trail) | same | holds |

## What is new vs RC6–RC8

Prior residual claims only used:

- first τ4 offset,
- density `rho4`,
- phase order / phase_gap,
- near-540 exclusivity by `o_q`.

RC9–RC11 open the **full τ4 offset set** geometry:

1. **Mass location** — at least 40% of τ4 land in the early half of the chamber.
2. **Span** — the last τ4 still occurs past 95% of `D(r)` (not early-only).
3. **Spacing** — no consecutive τ4 desert larger than 10% of `D(r)`.

Together with early-τ4 / late-τ3 phase order (RC1 / RC6), this says the
chamber is a **scattered τ4 field under a hard late τ=3 endpoint**, not a
single early burst followed by a τ4 desert.

## Key observed extremes

| Quantity | Value | Row |
| --- | ---: | --- |
| min early-half mass | `0.4151` | o_q=4 branch max `r=482,342,527`, `D=486` |
| min late-span | `0.9631` | o_q=2 branch max `r=468,917,503`, `D=542` |
| max gap fraction | `0.0812` | same o_q=2 row (max consecutive gap `44`) |
| util-max row | `D=738`, early mass `0.469`, late span `0.989`, max gap frac `0.041` | `r=424,171,123` |

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Fixed-band residual RC2 | falsified (retained) |
| Prior residual RC3–RC8 | measured holds; retained |
| New residual RC9–RC11 | measured holds; open as residual only |
| Invalidated d=4 SDA | remains invalidated |

## Falsify

```text
python3 experiments/square-branch-hourly-2026-07-10-rc9/offset_540_residual_rc9_probe.py
```

Inputs: prior chamber table
`experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`,
RC6 table (retained note),
falsification summary `.../square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json`,
and `prefix_tau_floor_probe.json` (SDA-invalidation note only).
