# Lead measured note — D1 R0 (execution collab)

**Status:** measured on R0 only (`p ≤ 10^6`). Not verified. Not theorem.

## What ran

- Interior via `z_band_prime_predictor.gwr_boundary_walk.gwr_next_gap_profile` (divisor field).
- Prime catalog via sieve as **input only**.
- Regimes: smoke `p≤1e5` (~5s), full R0 `p≤1e6` (~54s).
- Artifacts: `execution/d1_atlas/rows_R0_p_le_1e6.jsonl`, `summary_R0_p_le_1e6.json`, `ANALYSIS_R0_p_le_1e6.json`.

## Key measured facts

- **78,498** consecutive pairs with `p ≤ 10^6`; **100%** profile resolved; max gap **114**.
- Original control `gap > 1000` is **empty** at this scale (design miss in fixed-H control for R0).
- Reclass by within-log-bin gap quartiles:
  - **small_gap** (≤p25): offset mean **~1.99**, median **2**; offset=1 rate **~44%**
  - **large_gap** (≥p75): offset mean **~4.01**, median **4**; offset=1 rate **~5.3%**
  - gap≥50 (n=724): offset mean **~4.21**, offset=1 rate **~5.5%**
- Empty interior: **1** row (the twin-adjacent / empty case near start).
- Compression ratios are tiny vs UBC floor 64 (floor dominates at this magnitude) — K1-c relevant.

## Provisional read (hypothesis, for peer pressure)

Interior geometry **does** track gap width continuously: smaller gaps → smaller GWR offsets and more endpoint-adjacent winners. Fixed classical H∈{246,600,1000} does **not** carve structure at R0 because almost every gap is ≤114. This leans **K1-b redesign** (continuous gap-width stratification) more than “H-band atlas as written.”

## Peer pressure needed

Hermes QA, agy D4 link + R1 plan, claude kill adjudication + D2 pilot.
