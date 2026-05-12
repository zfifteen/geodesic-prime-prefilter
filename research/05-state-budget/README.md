# State Budget

## Object

State-budget carriers, `d4_count`, hidden-state probes, and ordering-carrier
evidence.

Primary homes:

- `research/05-state-budget/docs/state_budget_hidden_state_rollout/index.html`
- `research/05-state-budget/docs/state_budget_long_running_research_goal/index.html`
- `research/05-state-budget/docs/state_budget_observer_note/index.html`
- `research/05-state-budget/docs/d4_count_observer_note/index.html`
- `research/05-state-budget/docs/d4_count_project_implications/index.html`
- `research/05-state-budget/output/state_budget_long_running_catalog_8192/`
- `research/05-state-budget/output/state_budget_forbidden_transition_catalog_2048/`
- `research/05-state-budget/scripts/state_budget_*.py`

## Invariant Or Rule

The active measured carrier is `d4_count` under the
`mod30_prev_gap_exact` match mode. It compares current-chamber structure
against endpoint-tail controls after endpoint residue and prior-gap state are
fixed.

## Proof Status

No state-budget carrier is promoted to theorem status in this chapter.
`d4_count` remains measured unless a proof artifact is added.

## Measured Evidence

`research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json`
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
python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py research/05-state-budget/tests/test_state_budget_pairwise_ruler_test.py
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
python3 -m pytest research/05-state-budget/tests
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped state-budget chapter in
the state-budget filesystem migration.
