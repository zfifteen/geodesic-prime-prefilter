# Twin-Prime Chamber Experiment

This experiment studies twin-prime gaps as repeated one-cell chambers in the
prime-gap chamber sequence.

A twin-prime gap has the form `p, p+2`. Its open interval contains exactly one
integer:

$$p < p+1 < p+2$$

Therefore the interior selected integer is forced:

$$w=p+1$$

There is no competing interior divisor count, no tie, and no later simpler
interior integer. In PGS terms, a twin-prime gap is the smallest nonempty
prime-gap chamber and the selected integer is automatic.

## Strongest Current Finding

The PGSPG-style width-2 chamber side probe gives an exact one-cell closure
contract on the measured surface `q <= 1000000`. For each eligible prime `q`,
the generated record contains only:

```json
{"q": 47, "candidate": 49, "status": "excluded"}
```

or:

```json
{"q": 41, "candidate": 43, "status": "unresolved"}
```

Downstream audit found `21257 / 21257` excluded candidates were composite and
`8167 / 8167` unresolved candidates were prime closures. There were `0` false
exclusions and `0` unresolved composites.

The first decision-knob ablation found that the exact width-2 contract collapses
to the endpoint fixed-point condition in this chamber. At `q <= 1000000`,
`pgs_width2_full` and `endpoint_fixed_point` both passed with `0` false
exclusions and `0` unresolved composites. The coarse proxies failed:
`endpoint_below_forced_load` left `20484` composites unresolved, and
`forced_interior_carrier` falsely excluded all `8167` prime closures.

The PGS-native one-cell closure probe through `q <= 10000000` found that
composite failures of the candidate twin chamber almost always expose immediate
continued-chamber pressure: `189167 / 190252` composite obstructions
(`0.9942970376132708`) have a later interior integer with divisor count less
than or equal to the forced one-cell load `tau(q+1)`.

The dominant later-pressure offsets are:

| Offset from `q` | Count |
|---:|---:|
| `3` | `146351` |
| `4` | `28963` |
| `5` | `10845` |

This replaces the earlier transition-signature path as the active research
surface. The transition table is retained as a negative sanity check.

## Current Scope

This experiment does not claim a proof of the twin-prime conjecture. The current
question is narrower:

```text
Can the recurrence of twin-prime gaps be studied as recurrence of the one-cell
selected-minimizer chamber inside the prime-gap chamber sequence?
```

## Artifact Map

| Path | Role |
|---|---|
| `scripts/gwr_dni_gap_type_probe.py` | Classifies exact PGS gap winners into deterministic gap types. |
| `scripts/gwr_dni_twin_prime_gap_type_probe.py` | Classifies the preceding and following gap types around twin-prime chambers. |
| `scripts/twin_prime_chamber_return_gate_probe.py` | Negative sanity-check harness for completed-chamber transition signatures. |
| `scripts/twin_prime_one_cell_closure_probe.py` | Measures one-cell chamber closure and continued-chamber obstruction geometry. |
| `scripts/twin_prime_width2_pgs_generator_probe.py` | PGSPG-style width-2 chamber exclusion generator with downstream audit. |
| `tests/test_gwr_dni_twin_prime_gap_type_probe.py` | Focused tests for the twin-prime chamber probe. |
| `tests/test_twin_prime_chamber_return_gate_probe.py` | Focused tests for the return-gate harness and no-leakage contract. |
| `tests/test_twin_prime_one_cell_closure_probe.py` | Focused tests for the one-cell closure probe. |
| `tests/test_twin_prime_width2_pgs_generator_probe.py` | Focused tests for the width-2 PGS generator side probe. |
| `output/gwr_dni_twin_prime_gap_type_probe_summary.json` | Committed `q <= 1000000` summary. |
| `output/gwr_dni_twin_prime_gap_type_probe_details.csv` | Committed `q <= 1000000` twin-pair rows. |
| `docs/twin_prime_chamber_recurrence_target.md` | Current research target. |

## Quick Commands

Run the focused tests:

```text
python3 -m pytest experiments/twin-primes/tests
```

Regenerate the committed-scale probe:

```text
python3 experiments/twin-primes/scripts/gwr_dni_twin_prime_gap_type_probe.py --max-right-prime 1000000 --output-dir experiments/twin-primes/output
```

Run a small smoke probe:

```text
python3 experiments/twin-primes/scripts/gwr_dni_twin_prime_gap_type_probe.py --max-right-prime 1000 --output-dir /tmp/twin_prime_chamber_probe
```

Run the return-gate harness smoke test:

```text
python3 experiments/twin-primes/scripts/twin_prime_chamber_return_gate_probe.py --max-right-prime 1000 --train-max-right-prime 500 --output-dir /tmp/twin_prime_return_gate_probe
```

The return-gate harness emits:

```text
summary.json
exact_signature_rows.csv
type_pair_signature_rows.csv
family_width_signature_rows.csv
current_type_signature_rows.csv
```

Run the PGS-native one-cell closure probe:

```text
python3 experiments/twin-primes/scripts/twin_prime_one_cell_closure_probe.py --max-right-prime 1000000 --output-dir /tmp/twin_prime_one_cell_closure_probe_1e6
```

Run the width-2 PGS generator side probe:

```text
python3 experiments/twin-primes/scripts/twin_prime_width2_pgs_generator_probe.py --max-right-prime 1000000 --output-dir /tmp/twin_prime_width2_pgs_generator_probe_1e6
```

The width-2 side probe emits:

```text
generated_records.jsonl
audit_rows.csv
decision_knob_rows.csv
summary.json
```
