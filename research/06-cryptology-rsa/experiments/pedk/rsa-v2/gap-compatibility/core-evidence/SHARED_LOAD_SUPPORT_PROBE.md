# Shared Load Support Probe

## Finding

The clean shared load-boundary row is not a low-support artifact.

The active shared load-boundary rule is:

```text
endpoint right boundary - public selected divisor count = 0
```

The support probe profiles the same right-residue directional candidate rows
by signed load-boundary delta:

```text
-2  endpoint boundary below public load
 0  endpoint boundary equals public load
+2  endpoint boundary above public load
```

## Measured Support Profile

| shared load-boundary delta | testable rows | exact falsifications | minimum prior pair support | minimum prior boundary support |
| ---: | ---: | ---: | --- | --- |
| `-2` | `14232` | `3` | `5, 8, 14, 30, 180` | `643, 643, 650, 695, 695` |
| `0` | `45337` | `0` | `5, 9, 14, 30, 234` | `581, 679, 1145, 1233, 1233` |
| `+2` | `5663` | `27` | `5, 8, 14, 21, 160` | `197, 259, 324, 773, 873` |

Each support tuple is:

```text
min, q1, median, q3, max
```

The load-match row has exact-pair support comparable to the leaking rows:

```text
pair support median = 14
```

It also has the strongest right-boundary support:

```text
boundary support median = 1145
```

So the clean result is not explained by weak support. The clean row is the most
strongly boundary-supported load class in the profile.

## Proof Constraint

The theorem cannot be:

```text
the load-match row is clean because it barely appears
```

The measured support profile says the opposite. The load-match row is heavily
supported at the boundary level and still has zero exact endpoint-pair
falsifications.

The proof target remains:

```text
first public low-load point
and
endpoint right boundary equals public selected load
    -> stable supported prior absence
```

The support condition is real, but it is not the simple explanation. The simple
explanation has to live in the shared load-boundary equality itself.

## Reproduction

Run:

```text
python3 shared_load_support_probe.py
```

Primary outputs:

```text
output/shared_load_support_probe/summary.json
output/shared_load_support_probe/support_rows.jsonl
output/shared_load_support_probe/grouped_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
