# Remaining Bridge Inventory

## Current State

The proof target has been reduced to one remaining bridge.

The stable absence surface began as:

```text
public selected defect zero
and
endpoint transport defect zero
    -> exact endpoint-pair absence remains stable
```

The current local form is:

```text
public selected load 4
and
endpoint right boundary 4
and
same factor phase mod 36
and
supported prior absence
    -> public-left-31/lower-twin conjunction
```

Once that conjunction appears, the lower endpoint chain is:

```text
four-slot lower-twin chain
```

## Bridges Already Crossed

### 1. Residue Bridge

Proved modular lemma:

```text
public o6 selected offset
and
Rres=o4|o4
    -> {p mod 30, q mod 30} = {13, 19}
```

Reference:

```text
PUBLIC_O6_RESIDUE_BRIDGE_LEMMA.md
```

### 2. Phase-Lock Public Residue Bridge

Proved modular lemma:

```text
{p mod 30, q mod 30} = {13, 19}
and
p mod 36 = q mod 36
    -> N = 37 mod 60
```

Since the selected public offset is `6`:

```text
public left endpoint = 31 mod 60
```

Reference:

```text
PHASE_LOCK_PUBLIC_LEFT_RESIDUE_LEMMA.md
```

### 3. Four-Slot Chain Reduction

Measured reduction:

```text
public-left-31/lower-twin conjunction
    -> four-slot lower-twin chain
```

Observed replacement rows:

```text
19 -> 41 -> 43
29 -> 47 -> 49
```

Same-lane prior lower twins have only zero or two interior open slots before
the twin. Observed replacements have four.

Reference:

```text
PHASE_LOCK_FOUR_SLOT_REDUCTION.md
```

## Remaining Bridge

The remaining bridge is:

```text
public selected load 4
and
endpoint right boundary 4
and
same factor phase mod 36
and
supported prior absence
    -> public-left-31/lower-twin conjunction
```

This is the one live proof obligation.

## Why It Is One Bridge

The same-lane prior support separates the two events:

```text
same-lane prior rows in observed mod-180 lanes = 42
same-lane prior rows with public left endpoint 31 mod 60 = 7
same-lane prior rows with lower twin distance = 8
same-lane prior rows with both = 0
```

The observed replacement rows join them:

```text
observed rows = 2
observed rows with public left endpoint 31 mod 60 = 2
observed rows with lower twin distance = 2
observed rows with both = 2
```

So the remaining theorem is not:

```text
public-left 31 alone
```

and it is not:

```text
lower twin alone
```

It is the conjunction:

```text
public-left 31 and lower twin
```

## Current Proof Question

The proof question is:

```text
Why does shared load equality make the public-left anchor and the lower-twin
event coincide?
```

Equivalently:

```text
Why do the prior supported endpoint-pair classes reach public-left 31 and
lower twin distance separately, while balanced reentry reaches both at once?
```

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = one_remaining_bridge
remaining_bridge = public_left_31_lower_twin_conjunction
```
