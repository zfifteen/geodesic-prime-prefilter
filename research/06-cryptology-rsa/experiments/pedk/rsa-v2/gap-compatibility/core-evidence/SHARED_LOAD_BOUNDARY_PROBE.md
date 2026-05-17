# Shared Load-Boundary Probe

## Finding

The clean endpoint condition has a simpler arithmetic form:

```text
endpoint right boundary = public selected divisor count
```

On the active candidate surface, the public selected divisor count is always:

```text
4
```

The clean endpoint condition is:

```text
max(a, b) = 4
```

So the clean cell is not merely a residue label. It is a shared load-boundary
match:

```text
first public load 4
and
right endpoint boundary 4
```

## Measured Result

The shared boundary probe reads the public selected divisor count from the
public containing-gap type and reads the endpoint right boundary from the
right-following endpoint residues.

It emits:

```text
candidate_row_count = 101538
public_selected_divisor_counts = [4]
load_delta_endpoint_defect_mismatch_count = 0
selected public and endpoint boundary matches load = 45337
exact falsifications = 0
rate ppm = 0
```

The old endpoint defect is exactly the signed load-boundary delta divided by
two on this surface:

```text
shared load-boundary delta = endpoint right boundary - public selected divisor count
endpoint transport defect = shared load-boundary delta / 2
```

There are no mismatches between these two descriptions. The defect language can
therefore be replaced by:

```text
endpoint right boundary - public selected divisor count = 0
```

The same surface by signed load-boundary delta is:

| public side | endpoint right boundary minus public load | testable cells | exact falsifications |
| --- | ---: | ---: | ---: |
| after selected | `-2` | `1824` | `25` |
| after selected | `0` | `1810` | `25` |
| after selected | `+2` | `5562` | `80` |
| at selected | `-2` | `14232` | `3` |
| at selected | `0` | `45337` | `0` |
| at selected | `+2` | `5663` | `27` |

The only clean measured cell is:

```text
at selected public position
and
endpoint right boundary equals public selected divisor count
```

## Why This Matters

The previous statement used two separate labels:

```text
public selected defect zero
endpoint transport defect zero
```

The simpler statement uses one shared quantity:

```text
the divisor-load boundary 4
```

The public side says:

```text
N is the first interior point whose divisor count reaches 3 or 4
```

For distinct-prime semiprimes, `N` has divisor count `4`, and the selected
public rows all have selected divisor count `4`.

The endpoint side says:

```text
the first right-opening endpoint boundary reaches 4 and does not cross to 6
```

So the current invariant candidate is:

```text
first public load equals right endpoint boundary
```

In the active surface, that common value is `4`.

## Sharper Proof Target

The proof target can now be stated without defect language:

```text
If N is the first low-divisor-load point in its public prime gap,
and a supported prior-absent endpoint cell has right endpoint boundary equal
to that public selected load, then the endpoint cell remains absent.
```

Equivalently:

```text
If N is at the first public low-load point
and shared load-boundary delta is 0,
then supported prior absence is stable.
```

For the current distinct-prime semiprime surface:

```text
If N is the first divisor-count-3-or-4 point in its public gap,
and max(a, b) = 4,
then supported prior absence is stable.
```

A falsification is now equally simple:

```text
N is at the selected public point
endpoint right boundary equals the public selected divisor count
the cell is supported and previously absent
the exact endpoint pair appears in the forward surface
```

The current measured count is:

```text
45337 testable rows
0 exact falsifications
```

## Reproduction

Run:

```text
python3 shared_load_boundary_probe.py
```

Primary outputs:

```text
output/shared_load_boundary_probe/summary.json
output/shared_load_boundary_probe/shared_load_boundary_rows.jsonl
output/shared_load_boundary_probe/grouped_rows.jsonl
output/shared_load_boundary_probe/load_delta_mismatch_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
