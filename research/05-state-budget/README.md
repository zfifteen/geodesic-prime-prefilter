# State Budget

## Object

State-budget carriers, `d4_count`, hidden-state probes, and ordering-carrier
evidence.

Primary homes:

- `docs/research/predictor/state_budget_hidden_state_rollout/index.html`
- `docs/research/predictor/state_budget_long_running_research_goal/index.html`
- `docs/research/predictor/state_budget_observer_note/index.html`
- `docs/research/predictor/d4_count_observer_note/index.html`
- `docs/research/predictor/d4_count_project_implications/index.html`
- `output/state_budget_long_running_catalog_8192/`
- `output/state_budget_forbidden_transition_catalog_2048/`
- `benchmarks/python/predictor/state_budget_*.py`

## Invariant Or Rule

The active measured carrier is `d4_count` under the
`mod30_prev_gap_exact` match mode. It compares current-chamber structure
against endpoint-tail controls after endpoint residue and prior-gap state are
fixed.

## Proof Status

No state-budget carrier is promoted to theorem status in this chapter.
`d4_count` remains measured unless a proof artifact is added.

## Measured Evidence

`output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json`
records the strongest current carrier:

```text
match_mode: mod30_prev_gap_exact
measure: d4_count
positive_oriented_folds: 6
negative_oriented_folds: 1
decisive_pairs: 7881
edge_over_tail_control: 69
ordering_carrier_stop_condition_met: True
```

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest tests/python/predictor/test_bounded_compression_falsification_runner.py tests/python/predictor/test_d4_fallback_falsification_runner.py tests/python/predictor/test_d4_no_square_fallback_falsification_runner.py tests/python/predictor/test_square_branch_dynamic_cutoff_search.py tests/python/predictor/test_state_budget_divisor_carrier_sweep.py tests/python/predictor/test_state_budget_pairwise_ruler_test.py
20 passed in 5.73s
```

## Invalidated Rules

No state-budget rule was promoted or invalidated by this reorganization. Failed
candidate measures remain measured non-carriers unless a specific artifact
states otherwise.

## Unresolved State

The carrier is not a resolved theorem or generator rule. Its current role is a
measured ordering signal that still requires proof or further structural
closure before inference use.

## Reproduce

Run the focused state-budget validation:

```text
python3 -m pytest tests/python/predictor/test_state_budget_divisor_carrier_sweep.py tests/python/predictor/test_state_budget_pairwise_ruler_test.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped state-budget chapter in
Phase 4 of the repository reorganization.
