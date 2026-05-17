# Public Grammar Rolling Forward Results, 17001..19000

## Claim

The directed endpoint-pair signal reproduced on the next fresh factor band.

Using the same public side,

```text
public_word_gwr_side
```

and rolling the training window forward by one band, the ordering of
factor-side projections remained stable:

```text
full four-slot factor grammar
    beats
unordered directed endpoint-pair grammar
    beats
left/right or multiset collapses
```

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Test Design

The rolling bands were:

```text
train = factors 11001..13000
calibration = factors 13001..15000
prior_forward = factors 15001..17000
strict_forward = factors 17001..19000
```

The fresh enriched corpus contains:

```text
fresh_band = factors 17001..19000
fresh_row_count = 19503
public_word_count = 6019
factor_residue_phase_class_count = 232
factor_phased_word_count = 1577
factor_positioned_word_count = 13557
```

A candidate cell had to be:

1. supported on the public side and factor side in the train band;
2. jointly absent in the train band;
3. still supported and jointly absent in the calibration band;
4. still supported and jointly absent in the prior-forward band.

Any observed matching cell in `17001..19000` strictly falsified the candidate.

## Rolling Forward Result

| factor projection | preserved structure | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `slot_residue_phase` | `pL`, `pR`, `qL`, `qR` all preserved | `185266` | `3127` | `16` per mille |
| `unordered_endpoint_pair_residue_phase` | endpoint L/R pairs preserved, `p/q` collapsed | `161450` | `3562` | `22` per mille |
| `left_right_boundary_multiset_residue_phase` | global left and right multisets preserved | `165297` | `4082` | `24` per mille |
| `unordered_endpoint_lr_multiset_residue_phase` | endpoint pairing preserved, L/R inside endpoints collapsed | `103992` | `3658` | `35` per mille |
| `slot_residue_phase_multiset` | all four slots collapsed | `80044` | `3460` | `43` per mille |

The previous strict-forward test into `15001..17000` gave:

| factor projection | prior strict rate |
| --- | ---: |
| `slot_residue_phase` | `15` per mille |
| `unordered_endpoint_pair_residue_phase` | `21` per mille |
| `left_right_boundary_multiset_residue_phase` | `24` per mille |
| `unordered_endpoint_lr_multiset_residue_phase` | `37` per mille |
| `slot_residue_phase_multiset` | `49` per mille |

The new band therefore preserves the measured hierarchy. The full four-slot
surface remains strongest. The unordered directed endpoint-pair representation
remains the best compact candidate. Collapsing factor-side roles remains
weaker.

## Interpretation

The useful structure is not just which residue/phase tokens appear around the
two factors. The useful structure is which tokens occupy the directed boundary
roles around the same endpoint.

The fresh-band ordering is the important result:

```text
slot identity retained: 16 per mille
endpoint-pair direction retained, p/q removed: 22 per mille
endpoint pairing or direction partially erased: 24 to 35 per mille
all slot roles erased: 43 per mille
```

This strengthens the current law shape:

```text
public composite-gap grammar
    constrains
directed factor-endpoint-pair grammar
```

It also narrows the next rule-extraction target. Candidate rules should be
derived from the slot-preserving surface, then compressed only through
transformations that preserve each factor endpoint's directed left/right pair.

## Endpoint-Pair Candidate Exclusion Surface

The rolling test was then converted into an explicit endpoint-pair candidate
exclusion table using the active compact candidate:

```text
public_word_gwr_side -> unordered_endpoint_pair_residue_phase
```

The extractor records every public word and directed endpoint-pair word that
was supported on both axes and jointly absent across the three previous bands,
then marks whether it survived or was falsified in `17001..19000`.

Measured result:

```text
candidate_clean_absent_cell_count = 236066
forward_testable_cell_count = 161450
survived_forward_cell_count = 157888
falsified_forward_cell_count = 3562
not_testable_forward_cell_count = 74616
strict_falsification_rate = 22 per mille
```

The highest-ranked survived endpoint-pair exclusion has:

```text
public_key = prev=o2_d4_odd|d<=4|
             containing=o4_d4_a4_d4_odd@mid|
             next=o2_d4_odd|d<=4|
             after_winner

factor_key = L=o4@mid|R=o2@mid ||
             L=o4@mid|R=o4@mid

min_public_support_across_bands = 81
min_factor_support_across_bands = 110
rank_score = 8910
forward_observed_count = 0
```

This is now a concrete exclusion-surface artifact. It is still measured, not
proved. Its value is that the law target has moved from rate tables to a
specific list of public/endpoint-pair incompatibility candidates.

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = rolling_forward_confirmation
active_surface = public_word_gwr_side -> slot_residue_phase
active_compact_candidate = public_word_gwr_side ->
                           unordered_endpoint_pair_residue_phase
candidate_exclusion_surface = extracted for 17001..19000 rolling test
next_required_step = compress survived endpoint-pair exclusions into
                     role-preserving rule families
```

## Reproduction

Build the fresh enriched corpus:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 17001:19000 \
  --output-dir output/enriched_multiplication_map_corpus_17001_19000
```

Run the rolling forward test:

```text
python3 slot_factor_public_quotient_test.py \
  --train-dir output/enriched_multiplication_map_corpus_11001_13000 \
  --calibration-dir output/enriched_multiplication_map_corpus_13001_15000 \
  --prior-forward-dir output/enriched_multiplication_map_corpus_15001_17000 \
  --forward-dir output/enriched_multiplication_map_corpus_17001_19000 \
  --public-mode public_word_gwr_side \
  --factor-mode slot_residue_phase \
  --factor-mode unordered_endpoint_pair_residue_phase \
  --factor-mode left_right_boundary_multiset_residue_phase \
  --factor-mode unordered_endpoint_lr_multiset_residue_phase \
  --factor-mode slot_residue_phase_multiset \
  --output-dir output/slot_factor_public_quotient_test_17001_19000_rolling
```

Extract the endpoint-pair candidate exclusion surface:

```text
python3 endpoint_pair_candidate_exclusions.py
```

The output files are:

```text
output/enriched_multiplication_map_corpus_17001_19000/summary.json
output/enriched_multiplication_map_corpus_17001_19000/enriched_rows.jsonl
output/slot_factor_public_quotient_test_17001_19000_rolling/summary.json
output/slot_factor_public_quotient_test_17001_19000_rolling/public_quotient_rows.jsonl
output/slot_factor_public_quotient_test_17001_19000_rolling/public_quotient_sample_cells.jsonl
output/endpoint_pair_candidate_exclusions_17001_19000_rolling/summary.json
output/endpoint_pair_candidate_exclusions_17001_19000_rolling/candidate_exclusion_rows.jsonl
```
