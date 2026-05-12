# Square-Tail CRT Model Arrival-Order Audit For Root 509 Representative

## Status

Invalidated proof route.

## Finding

The full-cutoff CRT model has an ordered first-arrival cover for every rough
row by carrier `14741`.

The assigned singleton carrier is not always the first arrival in the model's
own residue class, but every rough row has some first arrival before or at the
last assigned carrier.

| Quantity | Value |
|---|---:|
| `M` | `4444` |
| Rough rows | `569` |
| Last assigned carrier | `14741` |
| Row assigned final carrier | `m = 4434`, offset `8868` |
| Final carrier before row square-root boundary | `true` |
| Rough rows arrived by last assigned carrier | `569` |
| Rough rows unarrived by last assigned carrier | `0` |
| Assigned carrier is first arrival | `547` |
| Assigned carrier is not first arrival | `22` |

The first mismatch is:

| `m` | Offset | Assigned carrier | First arrival |
|---:|---:|---:|---:|
| `432` | `864` | `5179` | `4969` |

## Boundary

This rules out another local proof route:

```text
first-arrival ordering of singleton carriers
-> contradiction
```

No such contradiction exists at the local CRT level. The model's residue class
has a complete ordered arrival cover through the full cutoff.

This is still not a square-tail counterexample. It does not prove that the CRT
residue class contains a selected-square prime root with the same ordered
closure state. It proves only that the ordered arrival condition itself is not
enough unless it is coupled to a stronger PGS invariant.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_crt_model_arrival_order_audit_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_crt_model_arrival_order_audit.py
```
