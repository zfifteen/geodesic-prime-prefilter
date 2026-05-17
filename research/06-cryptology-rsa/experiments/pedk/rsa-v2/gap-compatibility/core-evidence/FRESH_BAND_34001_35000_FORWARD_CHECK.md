# Fresh Band 34001..35000 Forward Check

## Purpose

The active proof target is intentionally small:

```text
public selected load 4
and
endpoint right boundary 4
    -> supported prior absence remains stable
```

The earlier measurement reduced the hard part to the terminal-twin lift:

```text
inside the supported prior-absent public o6 trigger cells,
the forced 13|19 balanced residue bridge reenters only when the lower factor is
the right endpoint of a terminal twin endpoint pair
```

This fresh-band check asks whether the next clean band changes that object.

## Fresh Corpus

The fresh band was generated from:

```text
34001..35000
```

Measured corpus size:

```text
semiprime rows = 4371
public words = 2423
oriented factor-position keys = 4371
```

Generated output:

```text
output/enriched_multiplication_map_corpus_34001_35000/
```

## Boundary Surface Result

Using:

```text
train            = 27001..30000
calibration      = 30001..32000
prior forward    = 32001..34000
fresh forward    = 34001..35000
```

the right-residue boundary stayed clean:

```text
boundary mode = right_residues
forward testable cells = 1201
falsified forward cells = 0
strict falsification rate = 0 ppm
```

The left-residue boundary also stayed clean, but with much smaller coverage:

```text
boundary mode = left_residues
forward testable cells = 9
falsified forward cells = 0
strict falsification rate = 0 ppm
```

The more decorated phase surfaces leaked:

```text
right_residue_phases: 1370 testable, 1 falsified
both_residues:        1394 testable, 6 falsified
left_residue_phases:   441 testable, 3 falsified
```

## Interpretation

The fresh band preserves the simplification:

```text
right endpoint residue boundary carries the stable signal
extra phase decoration introduces leakage
```

So the proof should stay on the smaller object:

```text
public selected load
endpoint right boundary
directed product transport
terminal-twin lift
```

The fresh band does not support expanding the law back into a large grammar
catalog.

## Terminal-Twin Trigger Status

After adding the fresh band, the terminal-twin probes still report:

```text
candidate load-match reentry rows = 90
observed replacement rows = 2
observed replacement rows with terminal-twin lift = 2
prior pair support rows = 8253
prior pair support rows with terminal-twin lift = 0
```

Lower orientation remains unchanged:

```text
observed replacement terminal side p = 2
observed replacement terminal side q only = 0
```

The replacement lower residue remains trigger-specific:

```text
o4 even -> o6@mid -> o4 odd: lower terminal residue = 13
o4 odd  -> o6@early -> o6 odd: lower terminal residue = 19
```

So this fresh band adds no new terminal-twin replacement event. It preserves
the existing proof reduction rather than replacing it.

## Current State

```text
theorem_status = hypothesis_not_proved
measured_status = fresh right-residue forward check passed
proof_reduction_status = still reduced to lower-factor terminal-twin lift
```

The simplest remaining explanation is still:

```text
shared load equality forces the only possible balanced reentry through a
lower-factor terminal twin, and that lift is outside the old supported
endpoint-pair class
```

That is the next proof object.
