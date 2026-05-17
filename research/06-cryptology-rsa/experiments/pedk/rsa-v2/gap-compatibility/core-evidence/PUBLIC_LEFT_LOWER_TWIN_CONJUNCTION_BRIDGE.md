# Public-Left Lower-Twin Conjunction Bridge

## Finding

The current obstruction is the conjunction of two simple events:

```text
public left endpoint = 31 mod 60
and
lower factor closes a twin endpoint pair
```

In the observed phase-locked replacement rows, both events occur together.
In the same-lane prior support, each event occurs separately, but never
together.

## Measured Contrast

Inside the same mod-180 lanes as the observed replacements:

```text
prior rows = 42
prior rows with public left endpoint 31 mod 60 = 7
prior rows with lower twin distance = 8
prior rows with both = 0
```

For the observed replacements:

```text
observed rows = 2
observed rows with public left endpoint 31 mod 60 = 2
observed rows with lower twin distance = 2
observed rows with both = 2
```

This is now the smallest measured separation between prior support and
balanced reentry.

## Consequence

The previous two bridge questions:

```text
why public-left 31 selects lower twin
why lower twin expands to the four-slot chain
```

are coupled in the measured surface. The prior rows show:

```text
public-left 31 alone is not enough
lower twin alone is not enough
```

The reentry surface requires:

```text
public-left 31 and lower twin together
```

Once that conjunction appears in the observed lanes, the preceding gap has four
interior wheel-open slots:

```text
four-slot lower-twin chain
```

## Current Proof Target

The next proof bridge is:

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

Then the measured four-slot chain is the local endpoint form of that
conjunction in the observed lanes.

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = reduced_to_public_left_lower_twin_conjunction
```

The next proof step is to explain why shared load equality makes the public
left endpoint anchor and the lower twin event coincide instead of appearing
separately as they do in prior support.
