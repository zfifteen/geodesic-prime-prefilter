# Phase-Lock Four-Slot Reduction

## Reduction

The current balanced reentry obstruction has reduced to a local endpoint chain:

```text
same factor phase mod 36
and
lower factor closes a twin endpoint pair
and
the gap before that twin contains four interior wheel-open slots
```

This is smaller than the previous terminal-twin label. It names the literal
chain around the lower factor.

## Wheel-Local Form

The residue bridge already proves:

```text
public o6 selected offset
and
Rres=o4|o4
    -> {p mod 30, q mod 30} = {13, 19}
```

The span condition:

```text
q - p = 0 mod 36
```

is therefore a shared mod-36 phase condition. In the observed replacement
surface, this leaves two lower-factor lanes:

```text
p mod 180 = 43
p mod 180 = 49
```

If the lower factor closes a twin pair, the immediate previous endpoint is:

```text
p - 2
```

So the two observed lower chains are:

```text
19 -> 41 -> 43
29 -> 47 -> 49
```

The first arrow is the gap before the twin. The second arrow is the twin gap.

## Four-Slot Meaning

For the `43` lane:

```text
19 -> 41
```

has four interior wheel-open slots:

```text
23, 29, 1, 7
```

For the `49` lane:

```text
29 -> 47
```

has four interior wheel-open slots:

```text
1, 7, 11, 13
```

Same-lane prior lower twins stop earlier:

```text
37 -> 41 -> 43
43 -> 47 -> 49
29 -> 41 -> 43
```

Those preceding gaps contain zero, zero, and two interior wheel-open slots.
Across all same-lane prior lower twins in the measured support:

```text
interior open slots = 0 or 2
```

Across the observed replacements:

```text
interior open slots = 4
```

## Current Proof Target

The proof target is now:

```text
public selected load 4
and
endpoint right boundary 4
and
same factor phase mod 36
and
supported prior absence
    -> balanced reentry must use the four-slot lower-twin chain
```

The old supported exact endpoint-pair class remains absent because it occupies
the same mod-180 lanes but never reaches the four-slot lower-twin chain.

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = reduced_to_four_slot_lower_twin_chain
```

The next proof step is to explain why the product transport at shared load
equality selects the four-slot lower-twin chain rather than the shorter
same-lane lower-twin chains.
