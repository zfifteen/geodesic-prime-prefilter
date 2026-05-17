# Exact Public Trigger Bridge

## Finding

The public-left residue was still too coarse.

The observed balanced reentry rows do not merely share:

```text
public left endpoint = 31 mod 60
```

They share one of two exact public trigger keys:

```text
prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner
prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner
```

Inside the same mod-180 factor lanes as the observed replacements, prior
support has no row with either exact public trigger.

## Measured Contrast

In the same observed factor lanes:

```text
prior rows = 42
prior rows with public left endpoint 31 mod 60 = 7
prior rows with observed exact public trigger = 0
```

For the observed replacement rows:

```text
observed rows = 2
observed rows with observed exact public trigger = 2
observed rows with lower twin distance = 2
```

So the current public-side object is:

```text
exact public trigger
```

not merely:

```text
public left endpoint 31 mod 60
```

## Reduced Bridge

The remaining bridge sharpens from:

```text
public-left-31/lower-twin conjunction
```

to:

```text
exact public trigger
and
same factor phase mod 36
and
balanced endpoint right boundary
    -> lower-twin conjunction
```

The public-left residue remains useful because the phase-lock lemma proves it
from the factor side. But the exact public trigger carries the actual
neighborhood condition that separates reentry from prior support.

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = reduced_to_exact_public_trigger_bridge
remaining_bridge = exact_public_trigger_to_lower_twin
```
