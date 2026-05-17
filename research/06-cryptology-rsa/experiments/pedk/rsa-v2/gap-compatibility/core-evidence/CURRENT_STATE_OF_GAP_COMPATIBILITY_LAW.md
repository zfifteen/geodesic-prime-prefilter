# Current State Of The Gap Compatibility Law

## Control Statement

The current evidence supports the gap compatibility hypothesis in a sharper
form than the earlier representation-search ladder.

The active object is:

```text
public at-winner condition
    selects the middle right-following factor endpoint maximum
        max(right residues)=o4
        max(first right-open offsets)=4
    which exclude exact endpoint-pair cells
```

The evidence does not yet prove the theorem and does not yet implement live
factor recovery. It does show a stable measured compatibility law candidate:
the public position of `N` inside its containing prime gap filters the
right-following gap grammar around the hidden factor endpoints.

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = strong_forward_stable_compatibility_signal
active_surface = public_at_winner -> right_following_endpoint_residue_maximum
candidate_law = zero right-boundary defect excludes exact endpoint-pair cells
rule_status = endpoint_space_exclusion_rule_not_factor_recovery
```

## The Object

Start with the public composite number `N`. It lies between two consecutive
primes, so it has a public containing gap. Inside that public gap there is a
distinguished minimum-divisor position, the GWR winner. The active public
condition is whether `N` is at that selected position.

Each hidden factor endpoint has a gap immediately before it and a gap
immediately after it. The strongest current signal is not the unordered pile of
all those gaps. It is directed: the gap after each factor endpoint behaves
differently from the gap before it.

The active factor-side coordinate is therefore:

```text
right-following endpoint residue class
```

For the two factor endpoints together, the clean condition is:

```text
max(right endpoint residue)=o4
```

In the first-open offset form, this is:

```text
max(a, b)=4
```

The transport identity is:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The first right-open offsets are fixed by endpoint residue modulo `30`:

```text
offset 2: {11, 17, 29}
offset 4: {7, 13, 19}
offset 6: {1, 23}
```

So the clean condition says:

```text
both endpoint slots avoid {1, 23}
and at least one endpoint slot lands in {7, 13, 19}
```

This is not a rule about `N mod 30` by itself. The two clean endpoint
families, `low|middle` and `middle|middle`, cover all reduced residues of
`N` modulo `30` when multiplied through. The selector is the public selected
position of `N` inside its containing gap, paired with the directed endpoint
transport boundary.

The contrast probe confirms that this public condition is active. The compact
endpoint predicate has `0 / 45337` exact endpoint-pair falsifications under
`at_winner`, but `25 / 1810` exact endpoint-pair falsifications under
`after_winner`.

The active invariant candidate is therefore:

```text
public_selected_defect = 0
and endpoint_transport_defect = 0
```

This zero-to-zero cell is the only supported public-side by endpoint-defect
cell in the current contrast matrix with zero exact endpoint-pair
falsifications.

The executable rule kernel is:

```text
zero_to_zero_exclusion_rule.py
```

It emits `45337` excluded endpoint-space cells with `0` exact falsifications.

That single condition contains exactly the two previously clean classes:

```text
Rres=o2|o4
Rres=o4|o4
```

## Measured Boundary

The current boundary-law profile measures exact endpoint-pair falsifications
across six strict-forward windows:

```text
21001..23000
23001..25000
25001..27000
27001..30000
30001..32000
32001..34000
```

The clean maximum-residue condition has not falsified:

| right-following maximum residue | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `o4` | `0` | `45337` |

In balance language:

| right-boundary balance | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `middle_o4_balance` | `0` | `45337` |
| `shortfall_below_o4` | `3` | `14232` |
| `overshoot_above_o4` | `27` | `5663` |

Equivalently:

| right-boundary defect | exact-pair falsifications | tested exact-pair cells |
| ---: | ---: | ---: |
| `0` | `0` | `45337` |
| `-1` | `3` | `14232` |
| `+1` | `27` | `5663` |

The neighboring maximum-residue values are not clean:

| right-following maximum residue | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `o2` | `3` | `14232` |
| `o6` | `27` | `5663` |

The split by the older pair labels is:

| right-following class | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `Rres=o2|o4` | `0` | `33318` |
| `Rres=o4|o4` | `0` | `12019` |
| combined clean classes | `0` | `45337` |

All observed right-gated falsifications fall outside those clean classes:

| right-following class | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `Rres=o2|o2` | `3` | `14232` |
| `Rres=o2|o6` | `4` | `1060` |
| `Rres=o4|o6` | `11` | `1143` |
| `Rres=o6|o6` | `12` | `3460` |

This is the strongest current signal because it separates a zero-falsification
middle-maximum family from neighboring right-following families that do
falsify.

The middle-maximum family is also public-local. It has zero falsified exact
endpoint-pair cells inside all `9` public containing-gap exact types where it
is testable, and zero falsified exact endpoint-pair cells inside all `149`
full public words where it is testable. The complement falsifies inside `8` of
the `9` containing-gap exact types and inside `19` full public words.

## Why The Older Ladder Was Moved

The earlier branch tried many coarser representations:

```text
raw gap type alone
position alone
all-o6 rules
symbolic survivor compression
public-axis and width quantile filters
slot-collapsing multisets
family compression
transported candidate filters
```

Those experiments were useful because they showed what fails. They also
identified the direction that now matters: preserve the factor endpoint role
and separate the right-following side from the left-following side.

Those files now live in:

```text
../archive/exploratory-ladder-2026-05-16/
```

## Active Evidence Notes

The current root keeps only the notes needed to reconstruct the active law
surface:

```text
PUBLIC_GRAMMAR_FORWARD_BOUNDARY_LAW_PROFILE.md
SIMPLE_RIGHT_RESIDUE_INVARIANT.md
SIMPLE_ENDPOINT_EXCLUSION_RULE.md
PUBLIC_SELECTED_POSITION_FILTER_MECHANISM.md
TRANSPORT_BALANCE_INVARIANT.md
PUBLIC_TO_ENDPOINT_BALANCE_BRIDGE.md
PUBLIC_SELECTED_CONTRAST_PROBE.md
ZERO_TO_ZERO_INVARIANT_CANDIDATE.md
ZERO_TO_ZERO_EXCLUSION_RULE.md
ZERO_DEFECT_THEOREM_TARGET.md
DIRECTED_TRANSPORT_AUDIT.md
PUBLIC_GRAMMAR_DIRECTIONAL_BOUNDARY_GATE_RESULTS.md
PUBLIC_GRAMMAR_JOINT_ENDPOINT_PAIR_RIGHT_BOUNDARY_RESULTS.md
PUBLIC_GRAMMAR_HYBRID_ENDPOINT_PAIR_SURFACE_RESULTS.md
PUBLIC_GRAMMAR_RIGHT_BOUNDARY_SURFACE_RESULTS.md
```

## Active Scripts

The newest profile is generated by:

```text
python3 forward_boundary_law_profile.py
python3 simple_invariant_probe.py
```

Its immediate dependencies are kept in the same directory so the script remains
directly runnable:

```text
directional_boundary_gate_surface.py
endpoint_pair_family_profile.py
enriched_multiplication_map_corpus.py
first_gap_compatibility_check.py
forward_boundary_law_profile.py
gwr_relative_all_o6_boundary.py
hybrid_endpoint_pair_surface.py
intermediate_projection_surface.py
joint_endpoint_pair_right_boundary_surface.py
multiplication_map_law_surface.py
public_feature_all_o6_boundary.py
public_grammar_pivot.py
right_boundary_compatibility_surface.py
simple_invariant_probe.py
slot_factor_public_quotient_test.py
```

## Next Research Move

The next step is to test whether the zero-falsification clean classes are the
visible face of a smaller exact rule.

The direct target is:

```text
public_at_winner
    plus public containing-gap grammar
    determines whether the right-boundary defect is zero
```

The rule must stay endpoint-space native: it excludes endpoint-pair cells by
public gap grammar and directed factor-neighborhood grammar, without candidate
divisibility, product checks, `gcd`, factor APIs, or classical factoring.
