# Public Left-Neighbor Gate Reduction

## Finding

The exact public trigger has compressed again.

The two observed replacement rows were previously described by their full
public gap-neighborhood keys:

```text
prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner
prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner
```

Inside the same mod-180 factor lanes, that full public key is stronger than
needed. The separating public object is the two-part left-neighbor gate:

```text
previous public first-open offset = o4
and
containing public exact type = o6_d4_a6_d4_odd
```

The following public gap, the public phase bucket, the public side label, and
the public-left endpoint residue are not needed for this measured separation.

## Measured Contrast

Inside the same observed factor lanes:

```text
prior rows = 42
prior rows with containing type o6_d4_a6_d4_odd = 5
prior rows with previous first-open offset o4 = 10
prior rows with both = 0
```

For the observed replacement rows:

```text
observed rows = 2
observed rows with both = 2
```

So neither single public feature is sufficient. The conjunction is the active
gate.

## Reduced Bridge

The remaining bridge sharpens from:

```text
exact public trigger
and
same factor phase mod 36
and
balanced endpoint right boundary
    -> lower-twin conjunction
```

to:

```text
public left-neighbor gate
and
same factor phase mod 36
and
balanced endpoint right boundary
    -> lower-twin conjunction
```

where:

```text
public left-neighbor gate =
    previous public first-open offset o4
    and containing public exact type o6_d4_a6_d4_odd
```

## Why This Is Simpler

The public containing gap supplies the selected public shape:

```text
o6_d4_a6_d4_odd
```

The previous public gap supplies only its first open offset:

```text
o4
```

That is enough to separate the observed reentry rows from same-lane prior
support. The exact parity of the previous public gap, the next public gap, and
the early/mid position labels are measured detail at this stage, not part of
the current minimal gate.

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = reduced_to_public_left_neighbor_gate
remaining_bridge = public_left_neighbor_gate_to_lower_twin
```

## Reproduction

```text
python3 public_left_neighbor_gate_probe.py
```

Output:

```text
observed rows in gate = 2
prior same-lane rows in gate = 0
prior same-lane rows with observed containing type = 5
prior same-lane rows with observed previous first-open = 10
```
