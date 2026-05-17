# First-Minimum Balance Probe

## Finding

The public side has been reduced to a literal divisor-count statement.

For the active six-window corpus, the public selected-position condition is
exactly:

```text
N is the first interior point in its public prime gap whose divisor count is 3 or 4
```

Measured result:

```text
row_count = 138602
public_at_winner_count = 31679
literal_first_tau_3_or_4_matches_public_at_winner_count = 138602
literal_first_tau_3_or_4_mismatch_count = 0
```

For the selected public rows:

```text
public at selected position, selected divisor count 4: 31679
public at selected position, selected divisor count not 4: 0
```

This is the clean reduction we wanted. The public condition is not a separate
grammar mystery. In this distinct-prime semiprime corpus, it is the first
low-divisor-load event inside the public gap.

## Why This Is Simpler

The semiprime is:

```text
N = pq
```

with distinct prime factors, so:

```text
tau(N) = 4
```

The selected position inside a prime gap is the first interior integer where
the minimum divisor count is reached. Therefore, when `N` is selected, no
earlier interior point in the same public gap can have divisor count `3` or
`4`.

So the public side can now be stated without internal labels:

```text
N is the first low-divisor-load point in its public gap
```

The endpoint side has already reduced to:

```text
the two right endpoint openings reach the middle boundary
```

or:

```text
max(a, b) = 4
```

The live proof target is therefore:

```text
first low-divisor-load point in the public gap
and
middle right-open endpoint boundary
    -> stable absence for supported prior-absent endpoint cells
```

## Sharper Falsifiable Statement

The current theorem target can now be stated as a direct arithmetic exclusion
claim:

```text
If N is the first interior point of divisor count 3 or 4 in its public prime
gap, and an endpoint cell is supported, previously absent, and has
max(a, b) = 4, then that endpoint cell remains absent.
```

A falsification would be an exact forward row satisfying all of:

```text
N is the first divisor-count-3-or-4 point in its public gap
the endpoint cell is supported
the endpoint cell was absent in the prior surface
max(a, b) = 4
the exact endpoint pair appears in the forward surface
```

The current measured surface has:

```text
45337 testable rows
0 exact falsifications
```

## What Remains

The proof no longer has to explain a broad grammar correlation.

It has to explain one small incompatibility:

```text
previously absent balanced endpoint cell
cannot become present
while N remains the first low-divisor-load point in the public gap
```

That is the current mathematical core.

## Reproduction

Run:

```text
python3 first_minimum_balance_probe.py
```

Primary outputs:

```text
output/first_minimum_balance_probe/summary.json
output/first_minimum_balance_probe/literal_first_minimum_rows.jsonl
output/first_minimum_balance_probe/mismatch_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
