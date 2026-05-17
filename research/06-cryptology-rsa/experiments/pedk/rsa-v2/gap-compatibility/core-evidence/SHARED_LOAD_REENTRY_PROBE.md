# Shared Load Reentry Probe

## Finding

The shared load-boundary match does not keep the coarse right-boundary cell
absent.

Instead, it blocks the lift from right-boundary reentry to exact endpoint-pair
reentry.

That is a sharper proof target.

## Measured Reentry Profile

The probe profiles right-residue directional candidate rows by shared
load-boundary delta:

```text
endpoint right boundary - public selected divisor count
```

| shared load-boundary delta | testable exact-pair rows | boundary reentry rows | exact-pair reentry rows | exact reentry inside boundary reentry |
| ---: | ---: | ---: | ---: | ---: |
| `-2` | `14232` | `116` | `3` | `3` |
| `0` | `45337` | `90` | `0` | `0` |
| `+2` | `5663` | `1009` | `27` | `27` |

The load-match row has:

```text
boundary reentry rows = 90
exact-pair reentry rows = 0
exact given boundary reentry rate ppm = 0
```

The off-load rows leak exactly through boundary reentry:

```text
delta -2: 3 exact reentries, all inside boundary reentry
delta +2: 27 exact reentries, all inside boundary reentry
```

## Consequence

The proof cannot be:

```text
the shared load boundary remains absent
```

That is false in the measured surface. The boundary does reenter under load
match.

The sharper statement is:

```text
when endpoint right boundary equals public selected divisor count,
right-boundary reentry does not lift to exact endpoint-pair reentry
```

This explains why the rule is exact-pair stable even though the coarser
boundary grammar is not fully stable.

## Current Proof Target

The theorem target is now:

```text
first public low-load point
and
endpoint right boundary equals public selected load
and
supported prior exact-pair absence
    -> boundary reentry cannot select the previously absent exact endpoint pair
```

For the current distinct-prime semiprime surface:

```text
first public load 4
and
right endpoint boundary 4
    -> no exact endpoint-pair lift from boundary reentry
```

This is narrower than the previous target. It does not require the right
boundary itself to stay absent. It only requires the exact endpoint pair to
remain absent when the boundary reappears.

## Reproduction

Run:

```text
python3 shared_load_reentry_probe.py
```

Primary outputs:

```text
output/shared_load_reentry_probe/summary.json
output/shared_load_reentry_probe/reentry_rows.jsonl
output/shared_load_reentry_probe/grouped_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
