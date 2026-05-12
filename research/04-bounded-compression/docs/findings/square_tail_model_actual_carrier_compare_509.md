# Square-Tail Modeled-Vs-Actual Carrier Comparison For Root 509 Representative

## Status

Audit evidence. Not a proof.

## Finding

The full-cutoff CRT model uses artificial singleton carriers. Those carriers do
not match the representative's actual least factors in the measured dynamic
tail.

For the `12` composite rough-tail rows before the representative's prime
closure:

| Quantity | Value |
|---|---:|
| Actual composite rough-tail rows | `12` |
| Same-position carrier matches | `0` |
| Matches anywhere in assigned singleton carrier set | `0` |

Example:

| `m` | Offset | Actual least factor | Modeled singleton carrier |
|---:|---:|---:|---:|
| `40` | `80` | `6736351` | `4451` |
| `57` | `114` | `1714849` | `4483` |
| `64` | `128` | `665241324811967767` | `4513` |
| `66` | `132` | `7541` | `4517` |

## Boundary

The full-cutoff CRT model rules out congruence-only contradiction. This
comparison records why it is not an actual factorization model: its singleton
carriers are valid local residues, but they are not the least factors that
occur in the representative's integer line.

The next proof-bearing condition must therefore use actual least-factor
minimality or another ordered PGS invariant, not arbitrary singleton carrier
existence.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_model_actual_carrier_compare_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_model_actual_carrier_compare.py
```
