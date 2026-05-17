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

That single condition contains exactly the two previously clean classes:

```text
Rres=o2|o4
Rres=o4|o4
```

## Measured Boundary

The current boundary-law profile measures exact endpoint-pair falsifications
across five strict-forward windows:

```text
21001..23000
23001..25000
25001..27000
27001..30000
30001..32000
```

The clean maximum-residue condition has not falsified:

| right-following maximum residue | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `o4` | `0` | `37834` |

In balance language:

| right-boundary balance | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `middle_o4_balance` | `0` | `37834` |
| `shortfall_below_o4` | `2` | `11352` |
| `overshoot_above_o4` | `24` | `4882` |

Equivalently:

| right-boundary defect | exact-pair falsifications | tested exact-pair cells |
| ---: | ---: | ---: |
| `0` | `0` | `37834` |
| `-1` | `2` | `11352` |
| `+1` | `24` | `4882` |

The neighboring maximum-residue values are not clean:

| right-following maximum residue | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `o2` | `2` | `11352` |
| `o6` | `24` | `4882` |

The split by the older pair labels is:

| right-following class | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `Rres=o2|o4` | `0` | `27789` |
| `Rres=o4|o4` | `0` | `10045` |
| combined clean classes | `0` | `37834` |

All observed right-gated falsifications fall outside those clean classes:

| right-following class | exact-pair falsifications | tested exact-pair cells |
| --- | ---: | ---: |
| `Rres=o2|o2` | `2` | `11352` |
| `Rres=o2|o6` | `4` | `874` |
| `Rres=o4|o6` | `8` | `996` |
| `Rres=o6|o6` | `12` | `3012` |

This is the strongest current signal because it separates a zero-falsification
middle-maximum family from neighboring right-following families that do
falsify.

The middle-maximum family is also public-local. It has zero falsified exact
endpoint-pair cells inside all `9` public containing-gap exact types where it
is testable, and zero falsified exact endpoint-pair cells inside all `143`
full public words where it is testable. The complement falsifies inside `8` of
the `9` containing-gap exact types and inside `17` full public words.

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
