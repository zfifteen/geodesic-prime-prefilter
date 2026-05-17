# Zero-To-Zero Exclusion Rule

## Rule

The current compact PGS-native endpoint-space exclusion rule is:

```text
public_selected_defect(W) = 0
and prior_absent(W, E)
and supported(E)
and endpoint_transport_defect(E) = 0
    -> exclude E
```

The public defect is:

```text
public_selected_defect(W) =
    public_n_offset_from_left - public_gwr_winner_offset
```

The endpoint transport defect is:

```text
endpoint_transport_defect(E) = max(a_E, b_E) - 4
```

where `a_E` and `b_E` are the first right-open offsets after the two endpoint
slots described by `E`.

## Endpoint Predicate

The endpoint defect-zero condition is:

```text
max(a_E, b_E) = 4
```

In endpoint residue form:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

The residue families are:

```text
offset 2: {11, 17, 29}
offset 4: {7, 13, 19}
offset 6: {1, 23}
```

## Measured Rule Output

The rule kernel emits:

```text
excluded_endpoint_cell_count = 45337
exact_falsification_count = 0
falsification_rate_ppm = 0
```

The source surface contains:

```text
source_candidate_rows = 101538
```

The zero-to-zero rule is the only clean supported public-side by
endpoint-defect cell currently measured:

```text
at_winner, endpoint defect -1 -> 3 / 14232 falsified
at_winner, endpoint defect  0 -> 0 / 45337 falsified
at_winner, endpoint defect +1 -> 27 / 5663 falsified

after_winner, endpoint defect -1 -> 25 / 1824 falsified
after_winner, endpoint defect  0 -> 25 / 1810 falsified
after_winner, endpoint defect +1 -> 80 / 5562 falsified
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = exact_zero_falsification_endpoint_space_exclusion_rule
```

The rule is not live factor recovery. It is an endpoint-space exclusion rule
over supported prior-absent cells.

## Reproduction

Run:

```text
python3 public_selected_contrast_probe.py
python3 zero_to_zero_exclusion_rule.py
```

Primary outputs:

```text
output/zero_to_zero_exclusion_rule/summary.json
output/zero_to_zero_exclusion_rule/excluded_endpoint_cell_rows.jsonl
```
