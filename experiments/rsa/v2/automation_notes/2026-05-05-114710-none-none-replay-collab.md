# None/None Replay Collab

Run time: 2026-05-05 11:47:10 EDT.

## Goal

Isolate the survivor rows whose directed PGSPG reset replay has no divergence
in either direction, then use Grok as an external reviewer for the artifact
shape and next falsification step.

## Artifact Added

The validator now writes:

```text
none_none_replay_alias_rows.csv
```

The artifact contains only survivor rows whose directed replay is clean in both
directions:

```text
lower_to_upper first_divergence_stage = none
upper_to_lower first_divergence_stage = none
```

Columns include:

```text
audit_role
selected_p
selected_q
audit_p
audit_q
survivor_count
diagonal_echo_count
off_diagonal_count
mixed_topology_collision
selected_row_topology
replay_cycle_kind
same_reset_signature
same_lock_carrier_d
same_tail_offsets
both_chambers_inside
one_sided_chamber_containment
```

This remains validator-only. No resolver rule was promoted.

## Measured Result

```text
<=99:  rows=26,  false_alias=14,  true_pair=12
<=149: rows=46,  false_alias=29,  true_pair=17
<=199: rows=78,  false_alias=52,  true_pair=26
<=251: rows=101, false_alias=70,  true_pair=31
<=397: rows=201, false_alias=157, true_pair=44
```

`<=397` topology split:

```text
false_alias diagonal_self_cycle diagonal_echo mixed=True: 78
false_alias off_diagonal_two_cycle off_diagonal mixed=False: 67
false_alias off_diagonal_two_cycle off_diagonal mixed=True: 12
true_pair diagonal_self_cycle diagonal_echo mixed=False: 2
true_pair diagonal_self_cycle diagonal_echo mixed=True: 25
true_pair off_diagonal_two_cycle off_diagonal mixed=False: 15
true_pair off_diagonal_two_cycle off_diagonal mixed=True: 2
```

`<=397` echo/context fields:

```text
true_pair:
  same_reset_signature: True=43, False=1
  same_lock_carrier_d: True=44
  same_tail_offsets: True=43, False=1
  both_chambers_inside: True=9, False=35
  one_sided_chamber_containment: True=10, False=34

false_alias:
  same_reset_signature: True=154, False=3
  same_lock_carrier_d: True=157
  same_tail_offsets: True=154, False=3
  both_chambers_inside: True=13, False=144
  one_sided_chamber_containment: True=36, False=121
```

The known 199 staged upper-width false alias `(89,181)` is not in this class.
It remains exposed by directed replay:

```text
lower_to_upper divergence: deadline_transport
upper_to_lower divergence: deadline_kind
```

## Grok Review

Grok could not access or run local files through the available MCP harness. The
only exposed xAI tool in this session was `xai_second_opinion`, so the file-run
portion of the user request is blocked by tool surface, not by repository state.

First Grok response:

```text
Grok agreed the validator-only artifact shape is methodologically sound and
recommended cycle-context analysis, but mistakenly suggested that (89,181)
should remain inside none_none_replay_alias_rows.csv.
```

Follow-up correction:

```text
Grok accepted the correction that (89,181) is absent from none/none because it
diverges in directed_reset_replay_matrix.csv. Grok recommended asserting the
absence in tests and continuing with cycle-context analysis.
```

The test suite now locks that corrected behavior.

## Tests Run

```text
python3 -m py_compile experiments/rsa/toy_pgs_factorizer/pgs_factorizer.py experiments/rsa/toy_pgs_factorizer/validator.py experiments/rsa/toy_pgs_factorizer/controller.py
python3 experiments/rsa/toy_pgs_factorizer/controller.py --max-audit-factor 99 --output-dir experiments/rsa/toy_pgs_factorizer/output
python3 experiments/rsa/toy_pgs_factorizer/controller.py --max-audit-factor 149 --output-dir experiments/rsa/toy_pgs_factorizer/output_le_149
python3 experiments/rsa/toy_pgs_factorizer/controller.py --max-audit-factor 199 --output-dir experiments/rsa/toy_pgs_factorizer/output_le_199
python3 experiments/rsa/toy_pgs_factorizer/controller.py --max-audit-factor 251 --output-dir experiments/rsa/toy_pgs_factorizer/output_le_251
python3 experiments/rsa/toy_pgs_factorizer/controller.py --max-audit-factor 397 --output-dir experiments/rsa/toy_pgs_factorizer/output_le_397
pytest -q tests/python/test_toy_pgs_factorizer.py
python3 experiments/rsa/v2/build_ladder_fixtures.py
python3 experiments/rsa/v2/run_experiment.py
python3 experiments/rsa/v2/audit_experiment.py
pytest -q tests/python/test_rsa_v2_scripts.py
```

Results:

```text
tests/python/test_toy_pgs_factorizer.py: 6 passed in 19.62s
tests/python/test_rsa_v2_scripts.py: 15 passed in 0.49s
```

## Interpretation

The `none/none` class is the current hard alias set. These rows are not caught
by one-pass directed replay. They mostly form two public cycle types:

```text
diagonal self-cycles inside mixed survivor sets
off-diagonal two-cycles, mostly outside mixed survivor sets
```

The next valid probe should be cycle-context analysis, not a selector:

```text
For each none/none row, compare the whole survivor-set cycle graph and classify
whether the row is part of a diagonal/off-diagonal collision, an isolated
off-diagonal two-cycle, or a repeated diagonal self-cycle.
```

No RSA v2 resolver rule should be changed from this result.
