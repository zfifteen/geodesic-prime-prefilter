# Span-36 Terminal-Lift Probe

## Finding

The current public `o6` residue-bridge surface has a smaller arithmetic
description:

```text
factor span divisible by 36
and
lower-factor terminal-twin lift
```

The two observed supported prior-absent replacement rows satisfy both
conditions.

## Measured Profile

Across the 11 public `o6` residue-bridge trigger rows:

```text
span mod 36 = 0 rows = 2
span mod 36 != 0 rows = 9
span-36 lower-terminal rows = 2
```

For the supported prior-absent replacement rows:

```text
observed replacement rows = 2
observed span mod 36 = 0 rows = 2
observed span-36 lower-terminal rows = 2
```

For the old supported pair classes:

```text
prior pair support rows = 8253
prior span mod 36 = 0 rows = 1336
prior span-36 lower-terminal rows = 0
```

So span divisibility alone is not the law. The prior surface already contains
many rows with `q - p` divisible by `36`. The missing lift is the lower terminal
twin.

## Sharper Proof Target

The proof object is now:

```text
public selected load 4
and
endpoint right boundary 4
and
supported prior absence
and
factor span divisible by 36
    -> lower-factor terminal-twin lift is the only observed reentry route
```

Equivalently, the old exact endpoint-pair class remains absent because:

```text
old supported pair class has span-36 rows
but no lower-terminal rows
```

while the observed replacements are:

```text
span-36 lower-terminal rows
```

## Role

This does not prove the terminal-twin lift lemma. It makes the remaining
statement smaller. The live question is no longer a broad grammar question.
It is the arithmetic reason that the balanced reentry surface selects:

```text
q - p = 0 mod 36
and
p is two units after the previous endpoint
```

inside the public selected `o6` residue-bridge trigger.

## Reproduction

Run:

```text
python3 span36_terminal_lift_probe.py
```

Primary outputs:

```text
output/span36_terminal_lift_probe/summary.json
output/span36_terminal_lift_probe/trigger_rows.jsonl
output/span36_terminal_lift_probe/observed_replacement_rows.jsonl
output/span36_terminal_lift_probe/prior_support_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
