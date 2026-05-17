# Terminal Twin Lift Probe

## Finding

The shared-load blocked lift reduces to a terminal-twin lift.

The old load-match candidate pair classes have prior support, but none of their
prior support rows contain the lift that appears in the forward replacement
rows.

The lift is:

```text
immediate-left endpoint distance = 2
and
factor-left bridge width >= 20
```

This is the endpoint-distance form of the earlier `very_late` phase shift. For
a factor-left bridge whose selected point is the immediate previous endpoint,
distance `2` becomes a `very_late` selected point once the bridge width is at
least `20`.

Equivalently:

```text
the factor is the right member of a twin endpoint pair
and
the gap before that twin pair has width at least 18
```

## Measured Profile

The probe compares:

1. The supported prior rows for the old load-match candidate pair classes.
2. The forward exact replacement rows that occupy the reentered load-match
   right-boundary cells.

Measured result:

```text
candidate load-match reentry rows = 90
prior pair support rows = 8253
prior pair support rows with terminal-twin lift = 0
observed replacement rows = 2
observed replacement rows with terminal-twin lift = 2
```

The two observed replacements have one terminal-twin side each:

```text
width=20, immediate-left distance=2
width=24, immediate-left distance=2
```

In endpoint geometry:

```text
preceding gap before twin pair = 18
preceding gap before twin pair = 22
```

The prior support rows do contain immediate-left distance `2` in shorter
bridges:

```text
width=6,  distance=2
width=8,  distance=2
width=12, distance=2
width=14, distance=2
width=18, distance=2
```

But none contain the terminal-twin lift:

```text
distance=2 inside bridge width >= 20
```

## Consequence

The proof target is now sharper:

```text
first public load 4
and
right endpoint boundary 4
and
right-boundary reentry
    -> terminal-twin lift
```

where:

```text
terminal-twin lift =
    one replacement factor has immediate-left endpoint distance 2
    inside a factor-left bridge of width at least 20
```

Equivalently:

```text
terminal-twin lift =
    one replacement factor is the right endpoint of a twin endpoint pair
    whose preceding gap has width at least 18
```

The old supported candidate pair classes do not contain this lift in their
prior support. The forward reentry rows require it. That is the measured
blocked-lift mechanism.

## Current Proof Target

The theorem target is no longer a broad compatibility grammar statement.

It is:

```text
Shared load equality forces any reentered balanced right-boundary cell through
a terminal-twin lift.
```

Then exact endpoint-pair absence follows because the old supported pair class
does not contain that lift.

## Reproduction

Run:

```text
python3 terminal_twin_lift_probe.py
```

Primary outputs:

```text
output/terminal_twin_lift_probe/summary.json
output/terminal_twin_lift_probe/candidate_rows.jsonl
output/terminal_twin_lift_probe/prior_pair_support_rows.jsonl
output/terminal_twin_lift_probe/observed_replacement_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
