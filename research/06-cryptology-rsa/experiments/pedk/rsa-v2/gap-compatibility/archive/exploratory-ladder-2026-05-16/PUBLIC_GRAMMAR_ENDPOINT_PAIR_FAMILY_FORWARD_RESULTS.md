# Public Grammar Endpoint-Pair Family Forward Results

## Claim

The first role-preserving endpoint-pair family compression did not survive as a
general rule layer.

This is a useful negative result. It shows that preserving directed
endpoint-pair structure is necessary, but not sufficient, for a compact
compatibility law. The individual endpoint-pair exclusion surface remains
stronger than the tested family abstraction.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Source Surface

The source surface was the rolling endpoint-pair candidate exclusion table:

```text
public_word_gwr_side -> unordered_endpoint_pair_residue_phase
```

The source bands were:

```text
train = factors 11001..13000
calibration = factors 13001..15000
prior_forward = factors 15001..17000
strict_forward = factors 17001..19000
```

The source extraction produced:

```text
candidate_clean_absent_cell_count = 236066
forward_testable_cell_count = 161450
survived_forward_cell_count = 157888
falsified_forward_cell_count = 3562
not_testable_forward_cell_count = 74616
strict_falsification_rate = 22 per mille
```

## Role-Preserving Compression

The family profiler grouped only by transformations that preserve the directed
endpoint-pair arrangement. It did not collapse the factor side into a token
multiset.

The tested factor projections were:

```text
endpoint_pair_exact
endpoint_pair_residue
endpoint_pair_phase
endpoint_pair_left_residue_right_phase
endpoint_pair_left_phase_right_residue
```

The tested public projections were:

```text
word_side
containing_side
prev_containing_side
containing_next_side
```

At `min_survived = 20`, the source profile found:

```text
profile_count = 33348
clean_fully_tested_role_family_count = 1973
clean_partially_tested_role_family_count = 13778
mixed_falsified_role_family_count = 17597
```

Only the `1973` clean fully-tested families were promoted to the independent
forward test.

## Independent Forward Test

The independent forward band was:

```text
forward_band = factors 19001..21000
forward_row_count = 20301
```

The `1973` clean fully-tested role families from the previous surface were
tested strictly: any fresh matching row falsified the family. A family was
counted as survived only when its public part and endpoint-pair part both
appeared in the fresh band and no matching row appeared.

Measured result:

```text
selected_profile_count = 1973
survived_forward_family_count = 665
falsified_forward_family_count = 1308
not_testable_forward_family_count = 0
strict_falsification_rate = 662 per mille
```

The family compression therefore fails as a general rule layer.

## Axis Breakdown

The best surviving axis was still too weak:

| axis | survived | falsified | strict falsification rate |
| --- | ---: | ---: | ---: |
| `word_side__endpoint_pair_left_residue_right_phase` | `159` | `139` | `466` per mille |
| `containing_next_side__endpoint_pair_residue` | `116` | `181` | `609` per mille |
| `containing_next_side__endpoint_pair_left_phase_right_residue` | `94` | `185` | `663` per mille |
| `prev_containing_side__endpoint_pair_residue` | `90` | `178` | `664` per mille |
| `prev_containing_side__endpoint_pair_left_phase_right_residue` | `82` | `158` | `658` per mille |

The comparison point is the uncompressed endpoint-pair candidate surface:

```text
unordered_endpoint_pair_residue_phase strict rate = 22 per mille
```

The family layer is much weaker. It should not be promoted.

## Interpretation

The failure is not evidence against the gap-compatibility hypothesis. It is
evidence against this compression step.

The active evidence says:

```text
public/endpoint-pair cells are stable enough to produce a strong exclusion
surface

role-preserving family compression still merges structures that must remain
separate
```

The law is therefore sharper than:

```text
public projection -> simplified directed endpoint-pair projection
```

The next rule search should either:

1. remain closer to exact public word plus exact endpoint-pair cells; or
2. add a second invariant that distinguishes the falsified and survived
   role-preserving families before attempting compression again.

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = role_preserving_family_compression_invalidated
surviving_object = individual public_word_gwr_side ->
                   unordered_endpoint_pair_residue_phase cells
invalidated_object = first role-preserving endpoint-pair family compression
next_required_step = find the missing invariant that separates the 665
                     surviving families from the 1308 falsified families
```

## Reproduction

Profile role-preserving families:

```text
python3 endpoint_pair_family_profile.py
```

Build the fresh forward band:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 19001:21000 \
  --output-dir output/enriched_multiplication_map_corpus_19001_21000
```

Forward-test the clean fully-tested role families:

```text
python3 endpoint_pair_family_forward_test.py
```

The output files are:

```text
output/endpoint_pair_family_profile_17001_19000_rolling/summary.json
output/endpoint_pair_family_profile_17001_19000_rolling/family_profile_rows.jsonl
output/enriched_multiplication_map_corpus_19001_21000/summary.json
output/enriched_multiplication_map_corpus_19001_21000/enriched_rows.jsonl
output/endpoint_pair_family_forward_test_19001_21000/summary.json
output/endpoint_pair_family_forward_test_19001_21000/family_forward_rows.jsonl
```
