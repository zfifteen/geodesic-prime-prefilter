# Zero-Defect Theorem Target

## Target

The measured invariant has reached a simple form:

```text
right_boundary_defect(E) = 0
```

The theorem target is to prove why this zero-defect condition is selected by
the public at-winner position.

In formal rule shape:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and right_boundary_defect(E) = 0
    -> exclude E
```

where `W` is a public composite-gap word and `E` is a directed endpoint-pair
cell around the two factor endpoints.

## Objects

The public object is the prime gap containing `N`. Inside that gap, GWR selects
the minimum-divisor position. The active public condition is:

```text
public_at_winner(W)
```

The factor-side object is directed. For each factor endpoint, take the gap
immediately to the right and record its first-open residue:

```text
p_right_residue
q_right_residue
```

Rank the right residues:

```text
rank(o2) = 1
rank(o4) = 2
rank(o6) = 3
```

Define:

```text
right_boundary_defect(E) =
    max(rank(p_right_residue), rank(q_right_residue)) - 2
```

The three cases are:

```text
defect = -1  shortfall
defect =  0  balanced
defect = +1  overshoot
```

## Mechanism

Multiplication sends a movement at a factor endpoint into a directed movement
of the composite:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

This is not a factor-recovery procedure. It is the arithmetic bridge that
explains why directed endpoint gaps can leave a trace in the public gap
containing `N`.

The right-following endpoint residues encode the first available outward
movement on the factor side. The public at-winner condition is a selected
position inside the public containing gap. The measured law says that stable
endpoint-cell exclusion occurs when the outward factor-side boundary has zero
signed deviation from the middle residue:

```text
public selected position
    aligns with
right_boundary_defect = 0
```

The off-balance cases have measured leakage:

```text
defect = -1  -> 2 / 11352 falsifications
defect = +1  -> 24 / 4882 falsifications
```

The balanced case has no measured leakage:

```text
defect = 0 -> 0 / 37834 falsifications
```

## Proof Obligations

The proof should be small. It should not introduce a compatibility table.

### Obligation 1: Directed Transport

Show that the right-following endpoint residues determine the first outward
transport class of the composite under multiplication.

Required shape:

```text
right endpoint movement at p and q
    -> directed outward movement of pq
    -> public containing-gap boundary class
```

Current audit:

```text
DIRECTED_TRANSPORT_AUDIT.md
```

The audit verifies the arithmetic transport object:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

It also confirms the important boundary: observed at-winner factor pairs
include all three defect classes. The theorem is therefore an endpoint-space
absence law, not a universal description of true factor-pair defect.

### Obligation 2: Winner Balance

Show that the public at-winner condition selects the zero signed deviation of
that outward boundary class:

```text
public_at_winner(W)
    -> right_boundary_defect(E) = 0
```

for supported absent endpoint cells.

This is the core theorem step.

### Obligation 3: Off-Balance Leakage

Show why the two nonzero defect classes are not stable exclusions:

```text
defect = -1  shortfall
defect = +1  overshoot
```

The measured falsifications already identify the off-balance classes as
leaking surfaces. The proof must explain why those classes can re-enter the
public surface while zero defect cannot.

## Current Evidence

The current measured evidence is:

```text
tested_windows = 5
defect_zero_testable_endpoint_cells = 37834
defect_zero_exact_falsifications = 0
defect_negative_one_exact_falsifications = 2
defect_positive_one_exact_falsifications = 24
```

This evidence supports the theorem target. It does not prove it.

## Boundary

This theorem target does not claim live factor recovery.

It also does not claim that every true factor pair under a public at-winner
word has zero right-boundary defect.

It claims an endpoint-space exclusion law:

```text
public_at_winner
and supported prior absence
and zero right-boundary defect
    -> excluded endpoint-pair cell
```

The proof must stay PGS-native: public gap grammar, directed endpoint grammar,
and exact support/absence conditions. It must not use candidate divisibility,
product checks, `gcd`, factor APIs, or classical factoring as inference.
