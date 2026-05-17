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

Under the already-proved mod-30 residue bridge, this is also a phase-lock
statement:

```text
{p mod 30, q mod 30} = {13, 19}
and
q - p = 0 mod 36
    =
p and q occupy the same mod-36 phase
```

Combining the mod-30 and mod-36 information places the observed replacements in
two mod-180 lanes:

```text
43|79
49|13
```

It also fixes the public product residue:

```text
N = 37 mod 60
```

Because the public selected offset is `6`, the public left endpoint is:

```text
31 mod 60
```

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
observed mod-180 lanes = 43|79 and 49|13
observed N mod 60 = 37
observed public left endpoint mod 60 = 31
```

For the old supported pair classes:

```text
prior pair support rows = 8253
prior span mod 36 = 0 rows = 1336
prior rows in observed mod-180 lanes = 42
prior rows in observed lanes with public left endpoint mod 60 = 31: 7
prior span-36 lower-terminal rows = 0
prior observed-lane lower-terminal rows = 0
prior observed-lane public-left-31 lower-twin rows = 0
```

So span divisibility alone is not the law. The mod-180 lane is not the law
either. The prior surface already contains rows with `q - p` divisible by `36`,
including rows in the same mod-180 lanes as the replacements. The missing lift
is the lower terminal twin.

## Sharper Proof Target

The proof object is now:

```text
public selected load 4
and
endpoint right boundary 4
and
supported prior absence
and
same factor phase mod 36
    -> lower-factor terminal-twin lift is the only observed reentry route
```

The terminal lift has a still more literal description:

```text
p is two units after the previous endpoint
and
the gap before that previous endpoint contains four interior wheel-open slots
```

The same-lane contrast isolates the threshold:

```text
observed lower twin preceding gap widths = 18 and 22
same-lane prior lower twin preceding gap widths = 4, 10, 12
same-lane prior maximum = 12
observed lower twin interior open slots = 4
same-lane prior lower twin interior open slots = 0 or 2
same-lane prior public-left-31 lower twins = 0
```

Equivalently, the old exact endpoint-pair class remains absent because:

```text
old supported pair class has span-36 rows
and even occupies the observed mod-180 lanes
and even has lower twin-distance rows
but no lower twin after a four-slot preceding gap
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
p is two units after the previous endpoint whose preceding gap contains four
interior wheel-open slots
```

inside the public selected `o6` residue-bridge trigger.

In the current reduction, `q - p = 0 mod 36` should be read as:

```text
the two factors have the same mod-36 phase after the mod-30 residue bridge has
forced them into the 13|19 bridge
```

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
