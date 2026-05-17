# Core Gap Compatibility Evidence

## Evidence Chain

This folder contains the current strong evidence for PEDK gap compatibility.

Read in this order:

```text
CURRENT_STATE_OF_GAP_COMPATIBILITY_LAW.md
GAP_COMPATIBILITY_HYPOTHESIS.md
FIRST_GAP_COMPATIBILITY_RESULTS.md
PRELIMINARY_CANDIDATE_EXCLUSION_RULE.md
HELDOUT_PHASE_EXCLUSION_RESULTS.md
FORWARD_STABLE_SURVIVOR_RESULTS.md
PUBLIC_AXIS_STABILITY_RESULTS.md
PUBLIC_WIDTH_QUANTILE_RESULTS.md
SYMBOLIC_SURVIVOR_COMPRESSION.md
SYMBOLIC_RULE_FORWARD_RESULTS.md
ALL_O6_CANDIDATE_RULE_RESULTS.md
FIVE_STATE_ALL_O6_REFINEMENT_RESULTS.md
FIVE_STATE_POSITIVE_SIGNATURE_MAP.md
POSITIVE_SIGNATURE_COMPRESSION.md
UNIFORM_CORNER_TEST_RESULTS.md
FOUR_STATE_ALL_O6_CANDIDATE_RESULTS.md
PUBLIC_FEATURE_ALL_O6_BOUNDARY.md
ALL_O6_BOUNDARY_REFINEMENT_601_5500.md
EXACT_SUBTYPE_ALL_O6_BOUNDARY.md
GWR_RELATIVE_ALL_O6_BOUNDARY.md
MULTIPLICATION_MAP_LAW_SURFACE.md
PUBLIC_GRAMMAR_PIVOT.md
PUBLIC_GRAMMAR_FACTOR_EXCLUSION_PIVOT.md
PUBLIC_GRAMMAR_TARGETED_SLICE_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_SPACE_REDUCTION.md
PUBLIC_GRAMMAR_TRANSPORTED_CANDIDATE_FILTER.md
PUBLIC_GRAMMAR_WORD_CONDITIONED_TRANSPORTED_FILTER.md
PUBLIC_GRAMMAR_FAMILY_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_REPRESENTATION_RESET.md
PUBLIC_GRAMMAR_FORWARD_STABLE_INCOMPATIBILITIES.md
PUBLIC_GRAMMAR_PROTO_FAMILY_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_SLOT_LOCK_PROBE_RESULTS.md
PUBLIC_GRAMMAR_DIRECTION_LOCK_PROBE_RESULTS.md
PUBLIC_GRAMMAR_ROLLING_FORWARD_17001_19000_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_PAIR_FAMILY_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_PAIR_PREDICATE_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_RIGHT_BOUNDARY_SURFACE_RESULTS.md
PUBLIC_GRAMMAR_HYBRID_ENDPOINT_PAIR_SURFACE_RESULTS.md
```

Run:

```text
python3 first_gap_compatibility_check.py
```

The script writes:

```text
output/gap_compatibility_search/
```

## Canonical Experiment

The canonical experiment is PGS-native:

- endpoints come from exact divisor-count structure;
- gap grammar comes from the existing PGS grammar machinery;
- `p` and `q` are downstream labels for corpus construction;
- no primality APIs, random sampling, `gcd`, factor APIs, or divisibility
  selectors are used as inference mechanisms.

## Current Measured Signal

The strongest measured object is:

```text
F(p, q) = unordered factor-neighborhood signature
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The current run records:

```text
semiprime_triple_count = 3834
factor_neighborhood_signature_count = 45
phased_n_state_count = 33
supported_phased_n_state_count = 12
candidate_phased_exclusion_count = 64
```

The first held-out check records:

```text
stable_survivor_count = 40
total_surviving_exclusion_rows = 266
total_falsified_exclusion_rows = 207
```

The fresh-band forward check records:

```text
fresh_band = factors 601..1000
semiprime_triple_count = 1711
tested_pair_count = 40
survived_pair_count = 27
falsified_pair_count = 13
falsifying_forward_row_count = 18
```

The first public-axis stability check records:

```text
public_axis = n_containing_gap_width
forward_survivor_count = 27
tested_pair_width_cell_count = 104
untested_pair_width_cell_count = 4
falsified_pair_width_cell_count = 0
falsifying_forward_row_count = 0
```

The fresh state-local public width quantile check records:

```text
fresh_band = factors 1001..1400
forward_survivor_count = 27
tested_pair_quantile_cell_count = 108
falsified_pair_count = 13
falsifying_forward_row_count = 29
stable_quantile_survivor_count = 14
```

The symbolic compression of the `14` survivors records:

```text
minimum_o6_residue_count = 2
all_survivors_have_at_least_two_o6_residues = true
all_o6_signature_count = 6
has_all_o6_factor_neighborhood_count = 10
both_factor_neighborhoods_touch_o6_count = 13
```

The symbolic rule forward check records:

```text
fresh_band = factors 1401..1800
candidate_rule_count = 2
survived_candidate_rule_count = 1
falsified_candidate_rule_count = 1
narrow_all_o6_falsifying_row_count = 0
broad_two_o6_falsifying_row_count = 143
```

The all-`o6` candidate rule check records:

```text
fresh_band = factors 1801..2200
tested_forward_row_count = 486
falsifying_forward_row_count = 1
survived_public_phase_state_count = 5
falsified_public_phase_state_count = 1
```

The five-state all-`o6` refinement check records:

```text
fresh_band = factors 2201..2600
tested_forward_row_count = 502
falsifying_forward_row_count = 0
survived_public_phase_state_count = 5
```

The next-band five-state refinement extension records:

```text
fresh_band = factors 2601..3000
tested_forward_row_count = 517
falsifying_forward_row_count = 0
survived_public_phase_state_count = 5
```

The five-state positive signature map records:

```text
bands = factors 601..2600 split into five fresh ranges
all_o6_observed_count = 0
stable_positive_signature_count = 72
```

The positive signature compression records:

```text
stable_positive_signature_count = 72
residue_multiset_count = 12
all_state_intersection_signature_count = 0
all_o6_positive_signature_count = 0
all_positive_signatures_have_non_o6_residue = true
```

The uniform corner test records:

```text
fresh_bands = factors 3001..3500 and 3501..4000
five_state_forward_row_count = 1410
five_state_uniform_observation_count = 95
five_state_uniform_corner_status = falsified_uniform_observation_present
five_state_all_o6_observation_count = 2
```

The four-state all-`o6` candidate check records:

```text
fresh_band = factors 4001..4500
tested_forward_row_count = 317
falsifying_forward_row_count = 1
falsified_public_phase_state = o6_d4_odd|d<=4@late
```

The public feature all-`o6` boundary records:

```text
bands = factors 601..4500 split into nine ranges
all_o6_compatible_state_count = 3
all_o6_not_observed_state_count = 3
all_o6_observation_count = 4
```

The all-`o6` boundary refinement records:

```text
bands = factors 601..5500 split into eleven ranges
all_o6_compatible_state_count = 4
all_o6_not_observed_state_count = 2
all_o6_observation_count = 6
surviving_not_observed_states = o2_d4_odd|d<=4@late, o4_d4_odd|d<=4@early
```

The public grammar endpoint-pair prevalence baseline records:

```text
fresh_bands = factors 5501..6500 and 6501..7500
endpoint_pair_count = 12564
individual_endpoint_count = 225
selected_survived_rule_count = 2
rank_4_eliminated_endpoint_pair_count = 484
rank_4_eliminated_endpoint_pair_fraction = 3.8523%
rank_4_fully_eliminated_individual_endpoint_count = 0
rank_2_eliminated_endpoint_pair_count = 480
rank_2_eliminated_endpoint_pair_fraction = 3.8204%
rank_2_fully_eliminated_individual_endpoint_count = 0
fresh_public_slice_actual_eliminated_count = 0 for both rules
endpoint_space_kind = unordered_endpoint_pair_space
```

The fixed-`N` transported candidate bridge records:

```text
fresh_bands = factors 5501..6500 and 6501..7500
semiprime_rows = 12564
candidate_x_count = 569104
transported_endpoint_candidate_count = 72869
compatibility_eliminated_candidate_count = 11
true_p_eliminated_by_compatibility_count = 0
rank_4_public_word_reduction_over_transported_endpoints = 3.7344%
rank_2_public_word_reduction_over_transported_endpoints = 1.7391%
candidate_space_kind = fixed_N_public_endpoint_x_with_floor_transport_y
transported_class_boundary = existing_endpoint_endpoint_class_only_when_y_is_endpoint
```

The word-conditioned transported filter records:

```text
baseline_bands = factors 5501..6500 and 6501..7500
fresh_band = factors 7501..9000
selected_public_word_count = 2
fresh_selected_rows = 81
fresh_candidate_x_count = 4368
fresh_transported_endpoint_candidate_count = 550
fresh_compatibility_eliminated_candidate_count = 11
fresh_endpoint_reduction = 2.0000%
true_p_eliminated_by_compatibility_count = 3
outcome_status = falsified_true_p_eliminated
```

The public grammar family forward tests record:

```text
top25_fresh_band = factors 7501..9000
top25_candidate_count = 25
top25_survived_count = 13
top25_falsified_count = 12
apparent_family = factor_residue_multiset o2:2|o4:2 and factor_phase_multiset mid:3|late:1
apparent_family_7501_9000_status = 7 / 7 survived
family_fresh_band = factors 9001..11000
family_candidate_count = 7
family_survived_count = 1
family_falsified_count = 6
single_public_word_fresh_band = factors 11001..13000
single_public_word_status = falsified
family_status = invalidated_as_general_exclusion_family
```

The representation reset records:

```text
band_7501_9000_row_count = 13861
band_7501_9000_current_compressed_collision_keys = 763
band_7501_9000_factor_phased_word_collision_keys = 157
band_7501_9000_factor_positioned_word_collision_keys = 4
band_9001_11000_row_count = 23653
band_9001_11000_current_compressed_collision_keys = 1786
band_9001_11000_factor_phased_word_collision_keys = 466
band_9001_11000_factor_positioned_word_collision_keys = 14
next_object = GWR-enriched public word -> factor phased word with orientation tracked
```

The intermediate projection stability check records the frozen working
representation:

```text
active_representation = public_word_gwr_side -> oriented_factor_phase_word
7501_9000_to_9001_11000_min3_rank = 1
7501_9000_to_9001_11000_min5_rank = 2
9001_11000_to_11001_13000_min3_rank = 1
9001_11000_to_11001_13000_min5_rank = 2
9001_11000_to_11001_13000_min5_testable_absent_cells = 476566
9001_11000_to_11001_13000_min5_falsified_cells = 5960
9001_11000_to_11001_13000_min5_falsification_rate = 12 per mille
```

The forward-stable incompatibility check records:

```text
train_band = factors 9001..11000
calibration_band = factors 11001..13000
forward_band = factors 13001..15000
selected_candidate_cell_count_top200 = 200
top200_supported_falsification_count = 0
selected_candidate_cell_count_top500 = 500
top500_supported_falsification_count = 0
selected_candidate_cell_count_top1000 = 1000
top1000_supported_falsification_count = 0
selected_candidate_cell_count_top5000 = 5000
top5000_forward_testable_cell_count = 4951
top5000_survived_absent_count = 4601
top5000_thin_observation_count = 350
top5000_supported_falsification_count = 0
top5000_supported_falsification_rate = 0 per mille
```

The stable absent family profile records:

```text
input_row_count = 5000
profile_count = 556
clean_proto_family_count = 192
mixed_proto_family_count = 364
min_survived = 10
```

The proto-family forward test records:

```text
forward_band = factors 15001..17000
forward_row_count = 21115
selected_clean_proto_family_count = 192
forward_testable_family_count = 185
survived_forward_family_count = 6
falsified_forward_family_count = 179
not_testable_forward_family_count = 7
strict_falsification_rate = 967 per mille
proto_family_status = invalidated_as_rule_compression
```

The full-public/factor-token middle compression diagnostic records:

```text
axis = public_word_gwr_side__factor_token_multiset
min_survived = 3
selected_profile_count = 463
forward_testable_family_count = 458
survived_forward_family_count = 224
falsified_forward_family_count = 234
not_testable_forward_family_count = 5
strict_falsification_rate = 510 per mille
middle_compression_status = insufficient_for_rule_layer
```

The slot-lock probe records:

```text
train_band = factors 9001..11000
calibration_band = factors 11001..13000
prior_forward_band = factors 13001..15000
strict_forward_band = factors 15001..17000
strongest_surface = public_word_gwr_side -> slot_residue_phase
strongest_surface_testable_cells = 213222
strongest_surface_survived_cells = 209863
strongest_surface_falsified_cells = 3359
strongest_surface_strict_falsification_rate = 15 per mille
unordered_endpoint_pair_rate = 21 per mille
unordered_endpoint_lr_multiset_rate = 37 per mille
slot_residue_phase_multiset_rate = 49 per mille
slot_lock_status = supported_by_forward_probe
```

The direction-lock probe records:

```text
public_side = public_word_gwr_side
strict_forward_band = factors 15001..17000
slot_residue_phase_rate = 15 per mille
unordered_endpoint_pair_residue_phase_rate = 21 per mille
left_right_boundary_multiset_residue_phase_rate = 24 per mille
unordered_endpoint_lr_multiset_residue_phase_rate = 37 per mille
slot_residue_phase_multiset_rate = 49 per mille
direction_lock_status = refined_to_oriented_endpoint_pair_grammar
```

The rolling forward endpoint-pair confirmation records:

```text
train_band = factors 11001..13000
calibration_band = factors 13001..15000
prior_forward_band = factors 15001..17000
strict_forward_band = factors 17001..19000
fresh_forward_row_count = 19503
slot_residue_phase_rate = 16 per mille
unordered_endpoint_pair_residue_phase_rate = 22 per mille
left_right_boundary_multiset_residue_phase_rate = 24 per mille
unordered_endpoint_lr_multiset_residue_phase_rate = 35 per mille
slot_residue_phase_multiset_rate = 43 per mille
endpoint_pair_candidate_clean_absent_cell_count = 236066
endpoint_pair_forward_testable_cell_count = 161450
endpoint_pair_survived_forward_cell_count = 157888
endpoint_pair_falsified_forward_cell_count = 3562
endpoint_pair_status = extracted_candidate_exclusion_surface
```

The endpoint-pair family forward test records:

```text
source_surface = public_word_gwr_side -> unordered_endpoint_pair_residue_phase
profile_source_band = factors 17001..19000 rolling test
forward_band = factors 19001..21000
profile_count = 33348
clean_fully_tested_role_family_count = 1973
selected_clean_role_family_count = 1973
survived_forward_family_count = 665
falsified_forward_family_count = 1308
not_testable_forward_family_count = 0
strict_falsification_rate = 662 per mille
family_status = invalidated_as_general_rule_layer
```

The endpoint-pair predicate forward test records:

```text
source_family_forward_band = factors 19001..21000
contrast_input_survived_family_count = 665
contrast_input_falsified_family_count = 1308
zero_falsified_contrast_predicate_count = 48
predicate_forward_band = factors 21001..23000
predicate_forward_row_count = 20706
survived_forward_predicate_count = 46
falsified_forward_predicate_count = 2
not_testable_forward_predicate_count = 0
active_candidate_invariant = public at-winner containing grammar ->
                             endpoint-pair right-boundary values
```

The direct right-boundary surface records:

```text
train_band = factors 15001..17000
calibration_band = factors 17001..19000
prior_forward_band = factors 19001..21000
strict_forward_band = factors 21001..23000
containing_type_at_winner_to_endpoint_left_right_values_rate = 48 per mille
containing_phase_at_winner_to_endpoint_left_right_values_rate = 53 per mille
containing_type_at_winner_to_endpoint_right_values_rate = 83 per mille
containing_type_at_winner_to_endpoint_left_values_rate = 173 per mille
right_boundary_status = discriminator_supported_but_incomplete
```

The shifted direct right-boundary surface records:

```text
train_band = factors 17001..19000
calibration_band = factors 19001..21000
prior_forward_band = factors 21001..23000
strict_forward_band = factors 23001..25000
containing_phase_at_winner_to_endpoint_right_values_rate = 56 per mille
containing_type_at_winner_to_endpoint_right_values_rate = 59 per mille
containing_phase_at_winner_to_endpoint_left_right_values_rate = 82 per mille
containing_type_at_winner_to_endpoint_left_right_values_rate = 89 per mille
right_boundary_status = active_discriminator_not_complete_law_object
```

The hybrid endpoint-pair surface records:

```text
window_21001_23000_public_word_gwr_side_exact_endpoint_pair_rate = 19 per mille
window_23001_25000_public_word_gwr_side_exact_endpoint_pair_rate = 29 per mille
window_25001_27000_public_word_gwr_side_exact_endpoint_pair_rate = 23 per mille
window_21001_23000_public_word_at_winner_right_values_only_rate = 30 per mille
window_23001_25000_public_word_at_winner_right_values_only_rate = 16 per mille
window_25001_27000_public_word_at_winner_right_values_only_rate = 33 per mille
broad_carrier = public_word_gwr_side -> exact_endpoint_pair
thin_discriminator = public_word_at_winner -> right_values_only
hybrid_status = measured_but_not_complete_law_object
```

The joint endpoint-pair/right-boundary surface records:

```text
object = exact endpoint-pair exclusion gated by at-winner right-residue absence
window_21001_23000 = 4 / 12765 exact-pair falsifications, 313 per million
window_23001_25000 = 3 / 9383 exact-pair falsifications, 319 per million
window_25001_27000 = 4 / 9584 exact-pair falsifications, 417 per million
window_27001_30000 = 12 / 12404 exact-pair falsifications, 967 per million
top_1000_21001_23000 = 0 / 913
top_1000_23001_25000 = 0 / 896
top_1000_25001_27000 = 2 / 840
top_1000_27001_30000 = 3 / 1000
joint_status = current_best_measured_rule_extraction_surface
```

The directional boundary comparison records:

```text
window_27001_30000_right_residues = 12 / 12404, 967 per million
window_27001_30000_right_residue_phases = 180 / 19119, 9414 per million
window_27001_30000_both_residues = 280 / 20619, 13579 per million
window_27001_30000_left_residue_phases = 220 / 10947, 20096 per million
window_27001_30000_left_residues = 10 / 479, 20876 per million
direction_status = right_following_boundary_gate_is_active_discriminator
```

The exact subtype all-`o6` boundary records:

```text
bands = factors 601..5500 split into eleven ranges
exact_subtype_cell_count = 51
all_o6_compatible_cell_count = 5
all_o6_not_observed_cell_count = 46
strongest_forward_cell = o4_d4_a4_d4_odd@early, rows 770, all-o6 0
```

The GWR-relative all-`o6` boundary records:

```text
bands = factors 601..5500 split into eleven ranges
relation_cell_count = 72
distance_cell_count = 530
all_o6_observation_count = 6
all_o6_distance_counts = 0:1, 2:1, 14:1, 24:1, 26:1, 37:1
all_o6_side_counts = at_winner:1, after_winner:5
```

The multiplication map law surface records:

```text
bands = factors 601..5500 split into eleven ranges
public_word_count = 5178
factor_word_count = 2048
observed_cell_count = 16710
supported_public_word_count = 23
supported_factor_word_count = 198
candidate_exclusion_count = 3741
```

The public grammar pivot records:

```text
pivot_public_word_count = 23
supported_factor_word_count = 198
candidate_exclusion_count = 3741
```

The public grammar factor exclusion pivot records:

```text
factor_class_cell_count = 1644
candidate_class_exclusion_count = 531
top broad residue families = o2:4, o2:2|o6:2, o2:3|o6:1, o2:3|o4:1, o4:4
```

The public grammar targeted slice check records:

```text
fresh_bands = factors 5501..6500 and 6501..7500
candidate_count = 5
survived_fresh_public_slice = 2
falsified_fresh_public_slice = 3
falsification_row_count = 8
```

## Rule Status

The preliminary rule is:

```text
pedk_phase_gap_exclusion_candidate_v1
```

It excludes factor-neighborhood signature classes as sidecar hypotheses. It
does not identify `p` or `q`, does not close a factor pair, and is not live PEDK
inference.

The held-out survivor surface is a stronger measured sidecar than the raw
full-corpus absence list. It is still not a live PEDK inference rule.

The forward survivor surface is stronger than the nested held-out survivor
surface. It removes `13` finite-band artifacts and leaves `27` forward-stable
candidate exclusions.

The public gap-width stability check is stronger than the aggregate forward
surface. It shows the `27` forward survivors persist across `104` tested
public width cells in the fresh band.

The state-local public width quantile check is stronger than the first
public-axis split because it uses a second fresh factor band. It reduces the
candidate rule surface from `27` to `14`.

The symbolic compression shows the remaining `14` candidates are not arbitrary:
all are `o6`-heavy factor-neighborhood exclusions, and the all-`o6` signature
is the strongest repeated subfamily.

The symbolic forward check promotes the all-`o6` subfamily to the current
strongest measured candidate rule and invalidates the broader two-or-more-`o6`
envelope as overbroad.

The fourth-band all-`o6` check invalidates the exact six-state rule and refines
the current strongest candidate to a five-state all-`o6` exclusion. The
falsified public phase state is `o4_d4_even|d<=4@mid`.

The five-state refinement survives the next two fresh bands after the
six-state rule was falsified and is now the strongest measured sidecar
candidate rule in this evidence chain.

The positive signature map records the compatible side of the same public
states: `72` state-signature pairs appear in every supported fresh band, while
the all-`o6` signature remains absent for the refined five-state rule.

The positive signature compression shows those compatible signatures are
mixed-residue signatures. The all-`o6` signature is a missing corner of the
observed compatibility surface. The exact positive signatures are state
specific: no single factor-neighborhood signature appears in all five public
phase states.

The uniform corner test invalidates the broad diversity-law form. The five
public states do not exclude every uniform factor-neighborhood signature:
all-`o2` and all-`o4` occur frequently. It also invalidates the five-state
all-`o6` rule by finding two all-`o6` rows in `o4_d4_odd|d<=4@mid`. The current
surviving all-`o6` candidate was therefore narrowed to four non-mid public
phase states.

The four-state all-`o6` candidate is also falsified by
`o6_d4_odd|d<=4@late`. The surviving all-`o6` exclusion surface is now three
public phase states: `o2_d4_odd|d<=4@late`, `o4_d4_odd|d<=4@early`, and
`o4_d4_odd|d<=4@late`.

The public feature boundary comparison showed the all-`o6` compatible target
states were the mid-phase `o4` states and the `o6` first-open late state across
factors `601..4500`. The next fresh band invalidated the coarse `o2/o4`
non-mid rule by finding an all-`o6` row in `o4_d4_odd|d<=4@late`.

The current measured all-`o6` exclusion surface across factors `601..5500` is:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
```

The exact-subtype split shows the next public grammar object is
`exact_type(gap(N)) @ phase(N inside gap(N))`. The strongest current exact cell
is `o4_d4_a4_d4_odd@early`, with `770` rows and no all-`o6` observation, while
`o4_d4_a4_d4_odd@mid` has admitted all-`o6`.

The GWR-relative split shows the next coordinate is the signed distance from
the containing gap's GWR winner:

```text
gwr_signed_distance = n_offset_from_left - winner_offset
```

The compatibility object is now:

```text
exact_type(gap(N)) @ phase(N inside gap(N)) @ distance_from_GWR_winner
```

The broad multiplication-map surface turns the research target into a table:

```text
public N word -> unordered factor-neighborhood word
```

The next compression problem is to derive the grammar rules that explain the
`3741` absent cells between supported public words and supported factor words.

The first compression reduces the raw absent-cell surface to `531` candidate
factor-class exclusions. The broad map's strongest first family is not the
sparse all-`o6` corner; it is mixed or uniform residue classes under specific
factor winner-phase multisets, especially `mid:3|late:1`, conditioned by the
public grammar word.

The first targeted slice check tests the top five compressed candidates on
fresh public slices. It falsifies three and leaves two surviving candidates:

```text
prev=o4_higher_divisor_even|5<=d<=16
containing=o2_d4_a2_d4_odd@mid
next=o2_d4_odd|d<=4
excludes residue o2:1|o4:2|o6:1 with phase mid:3|late:1

prev=o2_d4_odd|d<=4
containing=o2_d4_a2_d4_odd@early
next=o4_d4_odd|d<=4
excludes residue o2:1|o4:1|o6:2 with phase mid:3|late:1
```

That compressed residue/phase track was later treated as too lossy for the
main rule layer. The current strongest measured incompatibility surface is:

```text
public_word_gwr_side -> oriented_factor_phase_word
```

Under support `5/5`, the top `5000` cells that were independently supported
but jointly absent in both `9001..11000` and `11001..13000` produced zero
supported falsifications in `13001..15000`. This shifts the active rule object
from one broad residue/phase candidate to clean proto-families extracted from
stable absent cells.

The first proto-family compression was then forward-tested on `15001..17000`
and invalidated. This does not invalidate the stable individual-cell surface.
It shows that the attempted compression discarded necessary oriented
factor-neighborhood structure. The next compact grammar must preserve more of
the full oriented factor phase word than a token multiset or one-sided p/q
summary preserves.

The slot-lock probe identifies the next stable grammar object:

```text
public_word_gwr_side -> slot_residue_phase
```

This keeps the four factor-neighborhood slots `p-left`, `p-right`, `q-left`,
and `q-right`, while reducing each slot to residue plus phase. It sharply
outperforms factor-side multiset compression and shows that slot position is a
measured compatibility variable.

The direction-lock probe refines the object again. The strongest compact
factor object is the directed left/right boundary pair belonging to each hidden
factor. Collapsing the downstream `p/q` labels is cheap compared with erasing
left/right direction inside each factor endpoint. The next target is the
inner/outer boundary role split: `pL` and `qR` as outer boundaries, `pR` and
`qL` as inner boundaries.

The endpoint-pair family compression failed as a general rule layer. The
failure did not erase the exact endpoint-pair surface; it showed that the next
coordinate had to be inside the directed endpoint pair rather than a looser
family label.

Predicate contrast and direct boundary tests then isolated the right boundary
as the strongest active discriminator. Collapsing to right-boundary values by
itself was too thin and too lossy, but using the right boundary as a gate on
exact endpoint-pair exclusions produced the current strongest measured
surface.

The current best measured object is:

```text
public at-winner grammar
    gates
exact unordered directed endpoint-pair exclusions
    by
right-boundary residue class
```

Across four rolling strict-forward windows, the right-residue gated exact-pair
surface measured:

```text
21001..23000: 4 / 12765 exact-pair falsifications, 313 per million
23001..25000: 3 / 9383 exact-pair falsifications, 319 per million
25001..27000: 4 / 9584 exact-pair falsifications, 417 per million
27001..30000: 12 / 12404 exact-pair falsifications, 967 per million
```

The top support-ranked cells were especially strong:

```text
21001..23000: top 1000 = 0 / 913
23001..25000: top 1000 = 0 / 896
25001..27000: top 1000 = 2 / 840
27001..30000: top 1000 = 3 / 1000
```

This is now the active rule-extraction surface. The right boundary is not the
factor-side law object by itself. It is the gate that selects unusually stable
exact directed endpoint-pair absences.

The directional boundary gate check confirms that this is specifically a
right-following factor-boundary effect. On `27001..30000`, the right-residue
gate measured `967` per million, while left-residue gating measured `20876`
per million and both-side residue gating measured `13579` per million.
