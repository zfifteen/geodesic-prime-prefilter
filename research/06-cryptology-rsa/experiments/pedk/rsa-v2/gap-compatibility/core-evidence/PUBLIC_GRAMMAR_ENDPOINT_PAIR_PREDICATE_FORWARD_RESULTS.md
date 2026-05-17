# Public Grammar Endpoint-Pair Predicate Forward Results

## Claim

The next contrast exposed a sharper candidate invariant: public `at_winner`
states constrain the right-boundary values of directed factor endpoint pairs.

The first endpoint-pair family compression failed as a broad rule layer. The
survived-versus-falsified contrast inside that failure produced a small set of
structural predicates. Those predicates were then tested on a fresh independent
band. Most survived.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Source Contrast

The source labeled set was the endpoint-pair family forward test:

```text
source_family_forward_band = factors 19001..21000
source_family_count = 1973
source_survived_forward_family_count = 665
source_falsified_forward_family_count = 1308
```

The contrast extractor searched structural predicates over:

```text
public containing type and phase
public previous and following reduced gap states
public GWR side
directed endpoint-pair left and right values
endpoint-pair projection axis
```

It selected predicates with:

```text
min_survived = 10
falsified_forward_count = 0
max_width = 3
```

The contrast found:

```text
zero_falsified_predicate_count = 48
```

## Fresh Forward Test

The independent predicate forward band was:

```text
forward_band = factors 21001..23000
forward_row_count = 20706
```

Measured result:

```text
input_predicate_count = 48
survived_forward_predicate_count = 46
falsified_forward_predicate_count = 2
not_testable_forward_predicate_count = 0
```

The two falsified predicates were:

```text
factor_endpoint_pair_a_right=o4
public_containing_type=o4_d4_a4_d4_odd
public_side=at_winner

factor_endpoint_right_values=o2|o4
public_next=o4_d4_odd|d<=4
public_side=at_winner
```

## Strong Surviving Predicates

The strongest survived predicates were:

| predicate | matched families | fresh falsifications |
| --- | ---: | ---: |
| `factor_endpoint_right_values=o2|o4 && public_containing_type=o2_d4_a2_d4_odd && public_side=at_winner` | `42` | `0` |
| `factor_endpoint_right_values=o2|o4 && public_containing_type=o4_d4_a6_d4_odd && public_side=at_winner` | `36` | `0` |
| `factor_endpoint_right_values=o2|o4 && public_containing=o2_d4_a2_d4_odd@early && public_side=at_winner` | `33` | `0` |
| `factor_endpoint_right_values=o2|o4 && public_containing=o4_d4_a6_d4_odd@mid && public_side=at_winner` | `21` | `0` |
| `factor_endpoint_right_values=o2|o2 && public_containing_type=o4_d4_a4_d4_odd && public_side=at_winner` | `20` | `0` |

These are still candidate predicates, not laws. Their importance is that they
point to a repeated structural form:

```text
public containing type + GWR winner position
    constrains
right-boundary residue pattern of the two directed factor endpoint pairs
```

## Interpretation

The family-level failure showed that merely preserving directed endpoint-pair
structure is not enough. The predicate-level result suggests the missing
invariant is more specific:

```text
right boundary of the endpoint pair
```

The strongest surviving predicates do not primarily use the left-boundary
values. They repeatedly use:

```text
factor_endpoint_right_values
public_containing_type
public_side=at_winner
```

This shifts the active candidate law object from:

```text
public grammar -> endpoint-pair grammar
```

to:

```text
public at-winner containing grammar -> directed endpoint-pair right-boundary grammar
```

The exact law is unresolved. The next test should isolate this candidate
directly, rather than mixing it with all role-preserving family projections.

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = endpoint_pair_right_boundary_predicate_signal
surviving_object = public at-winner containing type ->
                   endpoint-pair right-boundary values
invalidated_object = broad role-preserving endpoint-pair family compression
next_required_step = build a direct right-boundary compatibility surface and
                     test it across fresh bands
```

## Reproduction

Run the structural contrast:

```text
python3 endpoint_pair_family_survival_contrast.py
```

Build the fresh predicate forward band:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 21001:23000 \
  --output-dir output/enriched_multiplication_map_corpus_21001_23000
```

Run the predicate forward test:

```text
python3 endpoint_pair_predicate_forward_test.py
```

The output files are:

```text
output/endpoint_pair_family_survival_contrast_19001_21000/summary.json
output/endpoint_pair_family_survival_contrast_19001_21000/predicate_rows.jsonl
output/enriched_multiplication_map_corpus_21001_23000/summary.json
output/enriched_multiplication_map_corpus_21001_23000/enriched_rows.jsonl
output/endpoint_pair_predicate_forward_test_21001_23000/summary.json
output/endpoint_pair_predicate_forward_test_21001_23000/predicate_forward_rows.jsonl
```
