# Family 1 Initial Baseline: w-Offset vs Current-Chamber d4_count

**Date**: 2026-05-30  
**Branch**: `predictions`  
**Probe**: `research/16-predictions/scripts/w_offset_carrier_probe.py` (v0.1)  
**Surface**: 10^12  to  10^13 (modest window for first signal)  
**Transitions analyzed**: 392 d=4 current chambers

## Experiment
Within cells matched on the same protocol used for the proven d4_count ordering carrier (`previous_reduced_state + current_winner_parity + current_carrier_family + current_winner_offset + first_open_offset + endpoint_mod30`, plus exact previous gap width in the strongest mode), does lower current `d4_count` predict an earlier arrival of the GWR-selected integer `w` (smaller `current_winner_offset`)?

This is a within-chamber baseline sanity check before investing in the cross-chamber version (previous chamber invariants → next chamber's w position), which is the actual Family 1 target recommended in the master catalogue.

## Result

| Match Mode              | Eligible Cells | Decisive Pairs | Signed Advantage | Advantage per Pair |
|-------------------------|----------------|----------------|------------------|--------------------|
| `mod30`                 | 54             | 63             | 0                | 0.0                |
| `mod30_prev_gap_exact`  | 9              | 9              | 0                | 0.0                |

**Verdict on this surface**: No detectable directional relationship between current-chamber `d4_count` and the earliness of `w` arrival within the matched cells.

## Interpretation (PGS-Native)

- On this small window, `d4_count` (while an excellent carrier for *next-triad state* after the current chamber) does not appear to be a strong carrier for the *position of w inside the current chamber itself*.
- This is consistent with the physics: `d4_count` counts how many early semiprimes appear after the previous prime; the exact location of the single leftmost minimum-τ integer (`w`) may be more strongly governed by other local invariants (square-phase utilization `U_□`, first-open offset details, carried reset/lock state from the previous chamber, higher-divisor pressure, etc.).
- The null result is useful data. It narrows the search space for a w-position carrier and increases the relative importance of the features the agent catalogues already flagged as promising (square-phase budget bit, reset signatures, previous-chamber lock/transport).

## Next Actions (Recommended)

1. Expand the surface to the full 8192-row 10^12 to 10^18 retained catalog used for the d4_count breakthrough (higher statistical power).
2. Add square-phase utilization (`U_□(w, q)`) and any available reset-signature / lock fields as additional candidate measures.
3. Implement the true cross-chamber target (`previous chamber invariants → next chamber's w-offset`) using a more robust row-linking strategy.
4. Record results in the unified master catalogue and the 16-predictions index only after the full held-out protocol is applied.

**Reproduction of this run**:
```bash
python3 research/16-predictions/scripts/w_offset_carrier_probe.py \
  --detail-csv research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv \
  --min-power 12 --max-power 13 \
  --output-dir research/16-predictions/output/w_offset_probe
```

All work remains strictly inside the PGS Predictions definition and the project contracts. No probabilistic claims were made.

*Findings archived on the predictions branch.*