# Core Gap Compatibility Evidence

## Evidence Chain

This folder contains the current strong evidence for PEDK gap compatibility.

Read in this order:

```text
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

The exact subtype all-`o6` boundary records:

```text
bands = factors 601..5500 split into eleven ranges
exact_subtype_cell_count = 51
all_o6_compatible_cell_count = 5
all_o6_not_observed_cell_count = 46
strongest_forward_cell = o4_d4_a4_d4_odd@early, rows 770, all-o6 0
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
