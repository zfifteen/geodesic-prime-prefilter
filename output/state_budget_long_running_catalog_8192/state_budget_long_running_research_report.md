# State-Budget Long-Running Research Run

breakthrough: ordering carrier found

The 8192-row-per-power retained `10^12..10^18` surface found one current-chamber ordering carrier beyond the endpoint-tail control under the required held-out checks. Inside cells matched by current PGS chamber facts, endpoint residue modulo `30`, and exact previous gap width, the current chamber's `d4_count` orders the next triad state with `7881` decisive matched pairs, all seven held-out powers above `100` decisive pairs, six positive held-out folds, `299` oriented signed wins, and a `69` signed-win edge over the endpoint-tail control. The required edge on this support is `50`.

## Commands

```sh
python3 benchmarks/python/predictor/gwr_dni_gap_type_catalog.py --output-dir output/state_budget_long_running_catalog_8192 --exact-max-right-prime 1000 --min-power 12 --max-power 18 --window-steps 8192
python3 benchmarks/python/predictor/state_budget_pairwise_ruler_test.py --detail-csv output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv --output-dir output/state_budget_long_running_catalog_8192 --min-power 12 --max-power 18
python3 benchmarks/python/predictor/state_budget_residue_matched_pair_test.py --detail-csv output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv --output-dir output/state_budget_long_running_catalog_8192 --min-power 12 --max-power 18
python3 benchmarks/python/predictor/state_budget_forbidden_transition_test.py --detail-csv output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv --output-dir output/state_budget_long_running_catalog_8192 --min-power 12 --max-power 18
python3 benchmarks/python/predictor/state_budget_divisor_carrier_sweep.py --detail-csv output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv --output-dir output/state_budget_long_running_catalog_8192 --min-power 12 --max-power 18
pytest -q tests/python/predictor/test_state_budget_divisor_carrier_sweep.py
```

## Input Catalog

- Path: `output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv`
- Deterministic retained rows: `57344`
- Powers: `10^12..10^18`
- Rows per power: `8192`
- Current `d=4` transition rows scored by the sweep: `45603`
- Catalog construction runtime: `1385.1610699999146` seconds

## Evidence Artifacts

- Catalog summary JSON: `output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_summary.json`
- Catalog detail CSV: `output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv`
- Divisor-carrier summary JSON: `output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json`
- Divisor-carrier per-fold CSV: `output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_folds.csv`
- Forbidden-transition summary JSON: `output/state_budget_long_running_catalog_8192/state_budget_forbidden_transition_summary.json`
- Forbidden-transition per-fold CSV: `output/state_budget_long_running_catalog_8192/state_budget_forbidden_transition_folds.csv`
- Residue-matched pairwise summary JSON: `output/state_budget_long_running_catalog_8192/state_budget_residue_matched_pair_summary.json`
- Residue-matched pairwise per-power CSV: `output/state_budget_long_running_catalog_8192/state_budget_residue_matched_pair_per_power.csv`
- Pairwise square/tail summary JSON: `output/state_budget_long_running_catalog_8192/state_budget_pairwise_ruler_summary.json`
- Pairwise square/tail per-power CSV: `output/state_budget_long_running_catalog_8192/state_budget_pairwise_ruler_per_power.csv`

## Breakthrough Carrier

The carrier is `d4_count`, the number of divisor-count `4` positions inside the current ordered prime-gap chamber. It is defined only from current PGS chamber objects: the current left endpoint, current right endpoint, selected integer context, and current chamber divisor-count field. It does not use the next chamber label to define the quantity.

The decisive stop-condition row from `state_budget_divisor_carrier_sweep_summary.json` is:

```json
{
  "match_mode": "mod30_prev_gap_exact",
  "measure": "d4_count",
  "fold_count": 7,
  "folds_with_min_support": 7,
  "positive_oriented_folds": 6,
  "negative_oriented_folds": 1,
  "eligible_cells": 3646,
  "decisive_pairs": 7881,
  "oriented_signed_advantage": 299,
  "tail_control_signed_advantage": 230,
  "edge_over_tail_control": 69,
  "required_edge": 50,
  "ordering_carrier_stop_condition_met": true
}
```

## Control Results

Square-room side remains invalidated as an exclusion carrier on the 8192 surface. After both endpoint residue and exact tail controls, `mod30_exact_tail` has `17842` eligible held-out rows, `2961` violations, and violation rate `0.1659567313081493`, above the exclusion-carrier limit.

The strongest non-breakthrough candidates either failed directional consistency or failed the required edge over tail. In the broad `mod30` cells, `tail_mod30`, `divisor_sum`, and `divisor_mean` showed positive edge over the oriented tail control, but none reached the required six-of-seven directional condition.

## Strongest Supported Claim

On the deterministic retained `8192`-row-per-power `10^12..10^18` surface, the current chamber's count of `d=4` divisor-field positions is a measured PGS-native ordering carrier for the next triad state under the contract's ordering-carrier gate. The result is not a proof theorem. It is a held-out measured carrier on the retained catalog surface, after matching current chamber facts, endpoint residue modulo `30`, exact previous gap width, and comparing against endpoint tail length.

## Stop Condition

breakthrough: ordering carrier found
