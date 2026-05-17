# Lower Terminal-Twin Orientation Probe

## Finding

The terminal-twin lift is lower-factor oriented.

In the public `o6` residue-bridge trigger rows, every terminal-twin row includes
the lower factor side `p`. In the two supported prior-absent replacement rows,
the lift is on `p` only.

The prior support rows for the old exact-pair classes contain no terminal-twin
lift at all.

## Measured Profile

Across the public `o6` residue-bridge trigger rows:

```text
trigger Rres=o4|o4 rows = 11
p < q false count = 0
terminal side none = 8
terminal side p = 2
terminal side p|q = 1
terminal side q only = 0
```

For the supported prior-absent replacement rows:

```text
observed replacement rows = 2
observed replacement p < q false count = 0
observed terminal side p = 2
observed terminal side q only = 0
observed terminal side p|q = 0
```

For the old supported pair classes:

```text
prior pair support rows = 8253
prior terminal side none = 8253
```

## Consequence

The current lift statement can be sharpened again:

```text
inside the supported prior-absent public o6 trigger cells,
the 13|19 residue bridge reenters only when the lower factor is the right
member of a terminal twin endpoint pair
```

This is stronger than "some factor has terminal-twin lift." The measured lift
is lower-factor directed.

## Current Proof Target

The current target is:

```text
For the two supported prior-absent public o6_d4_a6 balanced right-boundary
cells, the residue bridge forces residues 13 and 19, and any forward reentry
requires the lower factor to be the right endpoint of a terminal twin pair.
```

Then exact endpoint-pair absence follows because the old supported pair classes
have no terminal-twin lift in prior support.

## Reproduction

Run:

```text
python3 lower_terminal_twin_orientation_probe.py
```

Primary outputs:

```text
output/lower_terminal_twin_orientation_probe/summary.json
output/lower_terminal_twin_orientation_probe/trigger_orientation_rows.jsonl
output/lower_terminal_twin_orientation_probe/observed_replacement_rows.jsonl
output/lower_terminal_twin_orientation_probe/prior_support_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
