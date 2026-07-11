# Offset-540 Residual Claims RC12–RC14 — 2026-07-11

## Executive Summary

After RC9–RC11 (early-half τ4 mass, late-span presence, max desert), this hour
formalizes the **next residual chamber structure** on the **quartile geometry**
of the interior τ4 offset set for segment utilization maxima through `4e8–5e8`
and the full per-`o_q` branch-max panel. None of these is a theorem. d=4 SDA is
not revived. Fixed-band RC2 remains falsified. Prime-Square Proximity remains
**proved** in `PROOF.md`.

| ID | Claim | Status on surface through `4e8–5e8` |
| --- | --- | --- |
| RC12 | First-quarter τ4 mass `≥ 0.15` | **holds** (min observed `0.1833`) |
| RC13 | Last-quarter τ4 mass `≥ 0.15` | **holds** (min observed `0.2000`) |
| RC14 | Median τ4 mid-band `median/D ∈ [0.40, 0.65]` | **holds** (range `[0.448, 0.572]`) |
| RC2 | Fixed band `[528, 552]` on segment util maxima is a law | **falsified** (retained) |
| RC9–RC11 | Prior residual surface | **retained holds** (not primary surface) |

## Prediction Table (new surface)

| ID | Prediction | Primary surface | Status |
| --- | --- | --- | --- |
| P16 | first-quarter τ4 mass `≥ 0.15` | 5 util maxima + 3 o_q rows | holds |
| P17 | last-quarter τ4 mass `≥ 0.15` | same | holds |
| P18 | `0.40 ≤ median(Tau4)/D ≤ 0.65` | same | holds |

## What is new vs RC9–RC11

Prior residual claims only used:

- early-half mass (`≤ D/2`),
- last τ4 / D span,
- max consecutive desert including lead/trail.

RC12–RC14 open **quartile balance** of the same Tau4 set:

1. **Early quarter** — at least 15% of τ4 land in `[1, floor(D/4)]` (finer than half).
2. **Late quarter** — at least 15% of τ4 land past `floor(3D/4)` (mass, not only endpoint presence).
3. **Median location** — the median τ4 offset sits in the chamber mid-band.

Together with early-half / late-span / desert (RC9–RC11), this says the chamber
is a **balanced scattered τ4 field** under a hard late τ=3 endpoint: outer
quarters both carry mass, and the median is not piled against either wall.

## Key observed extremes

| Quantity | Value | Row |
| --- | ---: | --- |
| min first-quarter mass | `0.1833` | util max `r=251,066,071`, `D=540` (`2e8–3e8`) |
| min last-quarter mass | `0.2000` | o_q=2 branch max `r=468,917,503`, `D=542` |
| median frac range | `[0.448, 0.572]` | min `1e8–2e8`; max `2e8–3e8` |
| util-max row | `D=738`, firstQ `0.2917`, lastQ `0.2396`, med `0.5271` | `r=424,171,123` |

## Separation Of Concerns

| Layer | Status |
| --- | --- |
| Theorem (prime-square proximity) | proved (`PROOF.md`) |
| Fixed-band residual RC2 | falsified (retained) |
| Prior residual RC9–RC11 | measured holds; retained |
| New residual RC12–RC14 | measured holds; open as residual only |
| Invalidated d=4 SDA | remains invalidated |

## Falsify

```text
python3 experiments/square-branch-hourly-2026-07-11-rc12/offset_540_residual_rc12_probe.py
```

Inputs: prior chamber table
`experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`,
RC9 table (retained note),
falsification summary `.../square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json`,
and `prefix_tau_floor_probe.json` (SDA-invalidation note only).
