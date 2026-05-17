# Public Selected Position Filter Mechanism

## Mechanism Candidate

The public selected position of `N` filters endpoint space by forcing a
right-boundary balance condition.

The selected public position is the at-winner position inside the prime gap
that contains `N`. In this branch, "winner" means the GWR selected
minimum-divisor position of that containing gap.

The directed factor-side object is the pair of gaps immediately to the right
of the two factor endpoints. Each right-following gap has a first-open residue:

```text
o2, o4, o6
```

Ordered as a three-state boundary:

```text
o2 < o4 < o6
```

the current simple invariant is:

```text
max(p_right_residue, q_right_residue) = o4
```

This is the middle boundary state. The other two cases are:

```text
max = o2  -> shortfall below the middle boundary
max = o6  -> overshoot above the middle boundary
```

## Zero-Defect Form

The same condition has a scalar form. Assign ranks:

```text
rank(o2) = 1
rank(o4) = 2
rank(o6) = 3
```

Define the right-boundary defect:

```text
right_boundary_defect(E) =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

Then:

```text
defect = -1  -> shortfall_below_o4
defect =  0  -> middle_o4_balance
defect = +1  -> overshoot_above_o4
```

The measured invariant is the zero-defect condition:

```text
right_boundary_defect(E) = 0
```

## Why This Explains The Filter

The rule is not a statement about every observed true factor pair. It is a
statement about candidate endpoint-pair cells that are absent for a public
at-winner word across prior measured bands.

For those absent cells, the public selected position filters the endpoint-pair
space as follows:

```text
public_at_winner
    keeps the exclusion stable only when
right_boundary_balance = middle_o4_balance
```

The shortfall and overshoot cases do not remain clean. They are exactly where
forward observations re-enter the candidate surface as falsifications.

Measured over the current six strict-forward windows:

| right-boundary balance | condition | testable endpoint cells | falsifications |
| --- | --- | ---: | ---: |
| `middle_o4_balance` | `max=o4` | `45337` | `0` |
| `shortfall_below_o4` | `max=o2` | `14232` | `3` |
| `overshoot_above_o4` | `max=o6` | `5663` | `27` |

In zero-defect form:

| right-boundary defect | testable endpoint cells | falsifications |
| ---: | ---: | ---: |
| `0` | `45337` | `0` |
| `-1` | `14232` | `3` |
| `+1` | `5663` | `27` |

The public selected position therefore does not merely prefer a residue label.
It separates the candidate endpoint cells into a middle boundary state that
stays excluded and two off-balance states where actual endpoint observations
appear.

## PGS-Native Rule Form

Let `W` be a public at-winner composite-gap word. Let `E` be a directed
endpoint-pair cell around the two factor endpoints.

Define:

```text
right_boundary_balance(E) =
    shortfall_below_o4    if max(right_residue(E)) = o2
    middle_o4_balance    if max(right_residue(E)) = o4
    overshoot_above_o4   if max(right_residue(E)) = o6
```

The current exclusion rule is:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and right_boundary_defect(E) = 0
    -> exclude E
```

This is PGS-native because it uses only:

```text
public gap grammar of N
directed prime-gap grammar around endpoint cells
prior absence/support in the grammar surface
```

It does not use candidate divisibility, product checks, `gcd`, factor APIs, or
classical factoring as inference.

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = fresh_forward_supported_mechanism_candidate
tested_windows = 6
excluded_endpoint_cell_count = 45337
exact_falsifications = 0
```

The remaining theorem task is to prove why the at-winner public position
selects the zero-defect right-boundary state. The measured mechanism has the
right shape for that proof: a selected public position filters the directed
factor-side boundary to zero signed deviation from the middle available
residue state.

The proof target is stated in:

```text
ZERO_DEFECT_THEOREM_TARGET.md
```
