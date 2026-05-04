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

The committed `q <= 1000000` twin-prime chamber probe found `8169` twin-prime
pairs and classified the PGS gap types immediately before and after each pair.
The surface contains `1312` distinct outer-pair signatures, so twin gaps recur
inside a rich neighboring chamber grammar rather than one rigid outer pattern.

The top observed outer signature is:

| Preceding type | Following type | Count |
|---|---|---:|
| `o2_d4_a2_odd_semiprime` | `o4_d4_a4_odd_semiprime` | `315` |

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
| `scripts/twin_prime_chamber_return_gate_probe.py` | Tests completed chamber signatures as predictors of the next width-2 chamber. |
| `tests/test_gwr_dni_twin_prime_gap_type_probe.py` | Focused tests for the twin-prime chamber probe. |
| `tests/test_twin_prime_chamber_return_gate_probe.py` | Focused tests for the return-gate harness and no-leakage contract. |
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
