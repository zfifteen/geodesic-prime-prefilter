# Transport-Balance Invariant

## Finding

The clean measured exclusion law now has a direct transport form:

```text
public selected position of N
    filters endpoint cells whose right-following transport boundary is balanced
```

For the current wheel-open states, that balance condition is simply:

```text
max(a, b) = 4
```

where `a` is the first right-following open offset after `p`, and `b` is the
first right-following open offset after `q`.

Equivalently:

```text
max(right-following residue) = o4
```

or:

```text
right_boundary_defect = 0
```

## Building Blocks

Let:

```text
N = pq
```

The factor `p` has a first open position to its right. Call the offset from
`p` to that first open position `a`.

The factor `q` has a first open position to its right. Call the offset from
`q` to that first open position `b`.

In the current residue grammar, the right-following first-open offsets are:

```text
a, b in {2, 4, 6}
```

These three values have an ordered middle:

```text
2 < 4 < 6
```

The measured invariant is not a broad compatibility table. It only asks where
the larger of the two right-following factor offsets lands in that ordered
three-state set.

## Wheel-Residue Form

The first right-open offset is fixed by the endpoint residue modulo `30`:

| endpoint residue mod 30 | first right-open offset |
| ---: | ---: |
| `1` | `6` |
| `7` | `4` |
| `11` | `2` |
| `13` | `4` |
| `17` | `2` |
| `19` | `4` |
| `23` | `6` |
| `29` | `2` |

So the three endpoint families are:

```text
offset 2: {11, 17, 29}
offset 4: {7, 13, 19}
offset 6: {1, 23}
```

The clean exclusion surface:

```text
max(a, b) = 4
```

therefore has an even smaller endpoint-residue reading:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

In directed gap language:

```text
one right side reaches the middle open offset
neither right side reaches the high open offset
```

## Transport

Right movement at `p` and `q` transports through multiplication as:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The public composite `N` sits inside one public prime gap. When `N` sits at
the selected position inside that public gap, the measured stable exclusion
surface occurs exactly at the middle right-boundary state:

```text
max(a, b) = 4
```

The lower boundary:

```text
max(a, b) = 2
```

is a shortfall. The right side never reaches the middle open offset.

The upper boundary:

```text
max(a, b) = 6
```

is an overshoot. At least one side steps past the middle open offset.

The clean surface is the middle case:

```text
max(a, b) = 4
```

It reaches the middle open offset and does not cross it.

## Defect Form

Rank the right-following first-open states as:

```text
rank(o2) = 1
rank(o4) = 2
rank(o6) = 3
```

Define:

```text
right_boundary_defect =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

Then:

```text
max(a, b) = 2  <=>  right_boundary_defect = -1
max(a, b) = 4  <=>  right_boundary_defect =  0
max(a, b) = 6  <=>  right_boundary_defect = +1
```

The active candidate law is the zero-defect line:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and right_boundary_defect(E) = 0
    -> exclude E
```

In offset language:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and max(a_E, b_E) = 4
    -> exclude E
```

## Measured Evidence

Across the five strict-forward windows:

```text
21001..23000
23001..25000
25001..27000
27001..30000
30001..32000
```

the zero-defect line has:

```text
37834 / 37834 survived
0 / 37834 exact endpoint-pair falsifications
```

The off-balance lines leak:

```text
defect = -1: 2 / 11352 exact endpoint-pair falsifications
defect = +1: 24 / 4882 exact endpoint-pair falsifications
```

The same zero-defect condition stays clean inside the public grammar:

```text
public_containing_exact_type_count = 9
right_residue_max_o4_falsified_type_count = 0

full_public_word_testable_count = 143
right_residue_max_o4_falsified_public_word_count = 0
```

## Proof Target

The theorem should be stated as a transport-balance exclusion law:

```text
When N occupies the selected position inside its public prime gap,
supported prior absence becomes stable at the middle right-transport boundary.
```

The missing proof step is:

```text
public selected defect = 0
    -> stable absence at endpoint transport defect = 0
```

where:

```text
public selected defect =
    public_n_offset_from_left - public_gwr_winner_offset

endpoint transport defect =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

The measured rows used by the rule all satisfy:

```text
public selected defect = 0
endpoint transport defect = 0
```

The proof must explain why that zero-to-zero alignment stabilizes absence,
and why endpoint transport defects `-1` and `+1` are able to leak.

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = zero_falsification_candidate_invariant
mechanism_status = directed_transport_identity_audited
active_invariant = max(a,b)=4
```

This document does not claim that all true factor pairs under
`public_at_winner` have zero endpoint transport defect. Observed at-winner
factor pairs include all three defect classes. The claim is an endpoint-space
exclusion law over supported prior-absent cells.
