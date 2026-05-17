# Public Grammar Right-Boundary Surface Results

## Claim

The right-boundary signal is real, but right-boundary values alone are not the
law object.

The predicate contrast showed that many survived endpoint-pair family
predicates use:

```text
public_side = at_winner
public_containing_type
factor_endpoint_right_values
```

A direct surface test was then run to isolate that structure. The result
improves over the failed broad family layer, but it does not beat the full
endpoint-pair surface.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Test Design

The tested rolling bands were:

```text
train = factors 15001..17000
calibration = factors 17001..19000
prior_forward = factors 19001..21000
strict_forward = factors 21001..23000
```

The public projections were:

```text
containing_type_side
containing_phase_side
containing_type_at_winner
containing_phase_at_winner
```

The factor projections were:

```text
endpoint_right_values
endpoint_left_values
endpoint_left_right_values
```

Each factor projection preserved endpoint-pair boundary roles at the level
being tested. The direct question was whether public containing grammar,
especially at the GWR winner point, excludes right-boundary patterns.

## Results

| public projection | factor projection | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `containing_type_at_winner` | `endpoint_left_right_values` | `1296` | `63` | `48` per mille |
| `containing_phase_at_winner` | `endpoint_left_right_values` | `2414` | `130` | `53` per mille |
| `containing_phase_side` | `endpoint_left_right_values` | `44578` | `2684` | `60` per mille |
| `containing_phase_at_winner` | `endpoint_right_values` | `594` | `43` | `72` per mille |
| `containing_type_side` | `endpoint_left_right_values` | `14081` | `1116` | `79` per mille |
| `containing_type_at_winner` | `endpoint_right_values` | `337` | `28` | `83` per mille |
| `containing_phase_side` | `endpoint_right_values` | `2749` | `339` | `123` per mille |
| `containing_type_side` | `endpoint_right_values` | `854` | `114` | `133` per mille |
| `containing_phase_side` | `endpoint_left_values` | `2298` | `374` | `162` per mille |
| `containing_type_side` | `endpoint_left_values` | `638` | `110` | `172` per mille |
| `containing_type_at_winner` | `endpoint_left_values` | `167` | `29` | `173` per mille |
| `containing_phase_at_winner` | `endpoint_left_values` | `323` | `59` | `182` per mille |

The best direct surface was:

```text
public containing type at GWR winner
    ->
endpoint left/right boundary values

strict_falsification_rate = 48 per mille
```

The right-boundary-only surface was weaker:

```text
public containing type at GWR winner
    ->
endpoint right-boundary values

strict_falsification_rate = 83 per mille
```

## Interpretation

The contrast result was pointing at a real coordinate, but not at a complete
law object.

Right-boundary values help distinguish survived predicate families from
falsified families. When tested directly as the whole factor-side object,
right-boundary values lose too much information. Retaining both endpoint left
and right boundary values under the public `at_winner` containing type performs
better.

The current hierarchy is:

```text
full endpoint-pair surface:
22 per mille

direct at-winner left/right boundary surface:
48 per mille

direct at-winner right-boundary-only surface:
83 per mille

first broad role-preserving family layer:
662 per mille
```

The active interpretation is therefore:

```text
public at-winner containing grammar constrains endpoint boundary grammar,
with right-boundary values acting as an important discriminator rather than
as the full law object.
```

## Grok Peer Review

Grok reviewed the predicate and direct-surface results through the local Grok
CLI after the `21001..23000` test.

The useful pressure points were:

- predicates that name `endpoint_pair_a` or `endpoint_pair_b` are not invariant,
  because the endpoint pairs are unordered and the `a/b` names come from string
  ordering;
- predicates built on `public_next` are likely neighbor noise, because the
  strongest candidate object is the containing gap at the GWR winner point;
- right-boundary values are a discriminator, but the full directed endpoint
  pair remains the PGS-native object.

The resulting next test should preserve:

```text
public containing type at GWR winner
directed endpoint-pair identity
right-boundary class marked inside the endpoint pair
```

and should avoid promoting:

```text
endpoint_pair_a / endpoint_pair_b order artifacts
public-next-only predicates
pure right-boundary multisets
```

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = right_boundary_discriminator_supported_but_incomplete
surviving_object = individual public_word_gwr_side ->
                   unordered_endpoint_pair_residue_phase cells
candidate_invariant = public at-winner containing type plus endpoint
                      left/right boundary values
invalidated_object = right-boundary-only direct law surface
next_required_step = test a hybrid surface that retains endpoint-pair identity
                     while marking right-boundary compatibility classes
```

## Reproduction

Build the fresh forward band:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 21001:23000 \
  --output-dir output/enriched_multiplication_map_corpus_21001_23000
```

Run the direct surface:

```text
python3 right_boundary_compatibility_surface.py
```

The output files are:

```text
output/right_boundary_compatibility_surface_21001_23000/summary.json
output/right_boundary_compatibility_surface_21001_23000/surface_rows.jsonl
output/right_boundary_compatibility_surface_21001_23000/candidate_rows.jsonl
```

## Rolling Extension

The same direct surface was shifted forward:

```text
train = factors 17001..19000
calibration = factors 19001..21000
prior_forward = factors 21001..23000
strict_forward = factors 23001..25000
```

The fresh corpus contained:

```text
forward_row_count = 19503
```

The top rolling surfaces were:

| public projection | factor projection | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `containing_phase_at_winner` | `endpoint_right_values` | `637` | `36` | `56` per mille |
| `containing_type_at_winner` | `endpoint_right_values` | `352` | `21` | `59` per mille |
| `containing_phase_side` | `endpoint_left_right_values` | `35951` | `2620` | `72` per mille |
| `containing_phase_side` | `endpoint_right_values` | `3718` | `299` | `80` per mille |
| `containing_phase_at_winner` | `endpoint_left_right_values` | `2355` | `195` | `82` per mille |
| `containing_type_at_winner` | `endpoint_left_right_values` | `1274` | `114` | `89` per mille |

In the first direct surface, `endpoint_left_right_values` was stronger than
`endpoint_right_values`. In the shifted surface, the right-boundary-only
projection was stronger.

The stable statement is narrower:

```text
public at-winner containing grammar repeatedly interacts with endpoint
right-boundary values, but the correct way to carry paired left-boundary
context remains unresolved.
```

Additional output files:

```text
output/enriched_multiplication_map_corpus_23001_25000/summary.json
output/right_boundary_compatibility_surface_23001_25000/summary.json
```
