# Current State Of The Gap Compatibility Law

## Control Statement

The current law target is a compatibility rule between the public prime-gap
neighborhood containing a composite number `N` and the hidden prime-gap
neighborhoods around its two prime factors `p` and `q`.

The measured evidence supports the core hypothesis: these structures do not
combine freely. Public composite-gap words exclude large regions of
factor-neighborhood grammar, and those exclusions remain stable across fresh
forward bands when the representation preserves the right factor-side roles.

This is the current control boundary:

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = strong_forward_stable_compatibility_signal
active_surface = public_word_gwr_side -> slot_residue_phase
active_compact_candidate = public_word_gwr_side ->
                           unordered_endpoint_pair_residue_phase
current_research_action = extract and validate candidate incompatibility rules
                          from the active surface
```

## The Object

Start with the public number `N`. It lies between two consecutive primes, so it
has a public containing gap. That gap has neighboring gaps on its left and
right, a residue structure, a subtype, and a position for `N` inside the gap.
The selected public word also records whether `N` is before, at, or after the
GWR winner point inside the containing gap. In this branch, GWR names the
Leftmost Minimum-Divisor Rule point used by the gap grammar.

That public side is currently named:

```text
public_word_gwr_side
```

The hidden factor side starts at the two factor endpoints. The factor `p` has a
gap immediately to its left and a gap immediately to its right. The factor `q`
has the same. The current strongest measured surface preserves all four
factor-side slots:

```text
pL, pR, qL, qR
```

Each slot records residue and phase information. That full four-slot surface is
currently named:

```text
slot_residue_phase
```

The best compact candidate drops the artificial `p/q` assignment while keeping
the directed left/right boundary pair around each factor endpoint. It treats
the two factor endpoints as an unordered pair of directed endpoint
neighborhoods:

```text
unordered_endpoint_pair_residue_phase
```

The central object is therefore not a loose multiset of gap labels. It is an
oriented endpoint-pair grammar.

## Strongest Measured Surface

The current strongest measured result is the slot-preserving surface:

```text
public_word_gwr_side -> slot_residue_phase
```

It was tested using:

```text
train_band = factors 9001..11000
calibration_band = factors 11001..13000
prior_forward_band = factors 13001..15000
strict_forward_band = factors 15001..17000
```

Candidate cells had to be supported and absent across the first three bands.
Any matching observation in `15001..17000` strictly falsified the candidate.

| factor projection | preserved structure | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `slot_residue_phase` | all four factor slots preserved | `213222` | `3359` | `15` per mille |
| `unordered_endpoint_pair_residue_phase` | directed endpoint pairs preserved, `p/q` collapsed | `189195` | `4128` | `21` per mille |
| `left_right_boundary_multiset_residue_phase` | global left and right sides preserved | `197195` | `4851` | `24` per mille |
| `unordered_endpoint_lr_multiset_residue_phase` | endpoint pairing preserved, left/right collapsed | `112867` | `4286` | `37` per mille |
| `slot_residue_phase_multiset` | all four slots collapsed | `88973` | `4429` | `49` per mille |

The ordering is the result. Preserving the directed left/right pair belonging
to each factor endpoint is much stronger than treating factor-side structure as
a multiset. Full four-slot identity is strongest. The best compact object is
the unordered directed endpoint-pair representation.

## Latest Rolling Confirmation

The same active public side and factor projections were then rolled forward by
one band:

```text
train_band = factors 11001..13000
calibration_band = factors 13001..15000
prior_forward_band = factors 15001..17000
strict_forward_band = factors 17001..19000
```

The fresh corpus for `17001..19000` contains `19503` rows. The rolling forward
test preserved the same measured hierarchy:

| factor projection | testable cells | falsified cells | strict falsification rate |
| --- | ---: | ---: | ---: |
| `slot_residue_phase` | `185266` | `3127` | `16` per mille |
| `unordered_endpoint_pair_residue_phase` | `161450` | `3562` | `22` per mille |
| `left_right_boundary_multiset_residue_phase` | `165297` | `4082` | `24` per mille |
| `unordered_endpoint_lr_multiset_residue_phase` | `103992` | `3658` | `35` per mille |
| `slot_residue_phase_multiset` | `80044` | `3460` | `43` per mille |

The result confirms that the active object did not depend on the particular
`15001..17000` strict-forward band. Slot-preserving structure remains strongest,
and unordered directed endpoint-pair grammar remains the best compact
candidate.

The compact endpoint-pair surface has now been extracted as concrete candidate
exclusion rows:

```text
candidate_clean_absent_cell_count = 236066
forward_testable_cell_count = 161450
survived_forward_cell_count = 157888
falsified_forward_cell_count = 3562
not_testable_forward_cell_count = 74616
strict_falsification_rate = 22 per mille
```

This extraction is the first direct bridge from the measured law surface to an
endpoint-pair exclusion mechanism. It is not yet a proved law.

The first role-preserving family compression over that endpoint-pair surface
was tested on the independent `19001..21000` band. It failed as a general rule
layer:

```text
selected_clean_role_family_count = 1973
survived_forward_family_count = 665
falsified_forward_family_count = 1308
not_testable_forward_family_count = 0
strict_falsification_rate = 662 per mille
```

This invalidates the first compact family language. It does not invalidate the
individual endpoint-pair exclusion surface. The next missing object is the
invariant that separates the `665` surviving role families from the `1308`
falsified role families.

That contrast was then converted into structural predicates and tested on the
fresh `21001..23000` band:

```text
zero_falsified_contrast_predicate_count = 48
fresh_forward_predicate_count = 48
survived_forward_predicate_count = 46
falsified_forward_predicate_count = 2
not_testable_forward_predicate_count = 0
```

The strongest surviving predicates repeatedly use:

```text
public_side = at_winner
public_containing_type
factor_endpoint_right_values
```

This shifts the active candidate invariant toward:

```text
public at-winner containing grammar
    constrains
directed endpoint-pair right-boundary grammar
```

A direct right-boundary surface then tested that interpretation on the same
`21001..23000` forward band. The right-boundary coordinate remained useful but
was not sufficient by itself:

```text
containing_type_at_winner -> endpoint_left_right_values = 48 per mille
containing_phase_at_winner -> endpoint_left_right_values = 53 per mille
containing_type_at_winner -> endpoint_right_values = 83 per mille
containing_type_at_winner -> endpoint_left_values = 173 per mille
```

This means the right boundary is a discriminator inside the endpoint-pair law,
not the whole law object.

The direct surface was then shifted forward into `23001..25000`:

```text
containing_phase_at_winner -> endpoint_right_values = 56 per mille
containing_type_at_winner -> endpoint_right_values = 59 per mille
containing_phase_at_winner -> endpoint_left_right_values = 82 per mille
containing_type_at_winner -> endpoint_left_right_values = 89 per mille
```

This confirms that the right-boundary coordinate remains active, but the
paired left-boundary context is not yet represented correctly in the direct
surface.

The hybrid endpoint-pair surface then tested exact endpoint-pair identity
against right-boundary class rewrites. The broad carrier remained:

```text
public_word_gwr_side -> exact_endpoint_pair
```

with rates:

```text
19 per mille on 21001..23000
29 per mille on 23001..25000
```

The strongest thin discriminator was:

```text
public_word_at_winner -> right_values_only
```

with rates:

```text
30 per mille on 21001..23000 with 194 testable cells
16 per mille on 23001..25000 with 180 testable cells
```

This gives the current working split:

```text
broad carrier = exact directed endpoint-pair identity
thin discriminator = at-winner right-boundary values
```

The next experiment kept the exact directed endpoint pair as the primary
exclusion object and used the at-winner right-boundary residue class only as a
gate. This produced the current sharpest measured surface:

```text
public at-winner grammar
    gates
exact unordered directed endpoint-pair exclusions
    by
right-boundary residue class
```

It was tested across three rolling strict-forward windows:

| strict forward band | joint candidates | testable exact cells | exact falsifications | rate per million | top 1000 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `21001..23000` | `15641` | `12765` | `4` | `313` | `0 / 913` |
| `23001..25000` | `15023` | `9383` | `3` | `319` | `0 / 896` |
| `25001..27000` | `12572` | `9584` | `4` | `417` | `2 / 840` |
| `27001..30000` | `13185` | `12404` | `12` | `967` | `3 / 1000` |

This is the first surface in this branch that keeps exact endpoint-pair
identity while reducing strict exact-pair falsification below one per mille
across consecutive rolling windows.

The result also clarifies the role of the right boundary. A collapsed
right-boundary projection is not the law object. The right boundary is a gate
that selects high-survival exact endpoint-pair exclusions.

The directional boundary comparison then tested whether this gate is a generic
boundary effect or a right-following effect. On the non-overlapping
`27001..30000` forward band, exact-pair falsification rates were:

```text
right_residues = 967 per million
right_residue_phases = 9414 per million
both_residues = 13579 per million
left_residue_phases = 20096 per million
left_residues = 20876 per million
```

The right-following boundary gate is the active directional object. Adding the
left boundary weakens it. Using the left boundary alone weakens it much more.

## Stable Individual-Cell Evidence

Before the slot-lock probe, the strongest stable surface used the full public
word with GWR side and the full oriented factor phase word:

```text
public_word_gwr_side -> oriented_factor_phase_word
```

The top `5000` selected absent cells were tested forward from
`9001..11000` and `11001..13000` into `13001..15000`.

| selected cells | forward testable | stayed absent | thin observations | supported falsifications | supported falsification rate |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `200` | `200` | `170` | `30` | `0` | `0` per mille |
| `500` | `500` | `427` | `73` | `0` | `0` per mille |
| `1000` | `999` | `875` | `124` | `0` | `0` per mille |
| `5000` | `4951` | `4601` | `350` | `0` | `0` per mille |

The same top `5000` selection was also tested directly against the later
`15001..17000` band:

```text
forward_testable = 4458
survived_absent = 4177
thin_observation = 281
supported_falsification = 0
supported_falsification_rate = 0 per mille
any_observation_rate = 63 per mille
```

This means the full individual-cell surface remains strong. The current problem
is not whether a signal exists. The current problem is finding the compact
grammar that preserves the signal.

## Invalidated Or Insufficient Objects

The following objects have been tested and are not the current rule layer:

| object | status | reason |
| --- | --- | --- |
| raw gap type alone | too coarse | does not separate the observed compatibility structure |
| position alone | too coarse | useful as a feature, insufficient as the law object |
| broad all-`o6` rules | invalidated or boundary-only | early all-`o6` compressions admitted counterexamples |
| broad proto-family compression | invalidated | `179 / 185` strict forward-testable families falsified |
| public containing side plus broad factor summaries | invalidated | collapsed public/factor details that later mattered |
| `public_word_gwr_side -> factor_token_multiset` | insufficient | `234 / 458` strict forward-testable profiles falsified, `510` per mille |
| all four factor slots as a multiset | insufficient | `49` per mille, weaker than slot-preserving and endpoint-pair surfaces |
| inner/outer proximity as replacement for endpoint pairs | insufficient | corrected proximity test stayed at `21` per mille, not below the compact endpoint-pair rate |
| transported endpoint candidate filter | sidecar guide only | measured endpoint-space reduction was small and does not define the law object |

The invalidations are useful. They show that the grammar is not a bag of
tokens. It is role-sensitive.

## Current Interpretation

The public gap around `N` interacts with the factor side through boundary
roles. The role of a factor-side gap is not only its residue or phase. Its
meaning depends on which endpoint it belongs to and whether it sits on the left
or right side of that endpoint.

In the current measurements, the `p/q` labels carry less signal than the
directed endpoint-pair structure. The jump from `15` per mille to `21` per
mille measures the current cost of dropping the downstream `p/q` assignment.
The larger jumps to `37` and `49` per mille measure the cost of erasing
directed endpoint-pair structure.

This is the active law shape:

```text
public composite-gap grammar
    constrains
unordered directed factor-endpoint-pair grammar
```

The full slot surface remains the best extraction surface. The unordered
directed endpoint-pair surface is the best compact law candidate.

## Current Findings

The strongest current findings are:

- The multiplication map contains stable absent cells, not just noisy sparse
  data.
- Individual public/factor grammar cells survive repeated fresh-band tests
  with `0` supported falsifications across the strongest selected cuts.
- Factor-side slot identity is strongly measured: preserving `pL`, `pR`, `qL`,
  and `qR` beats collapsing the factor side.
- Directed endpoint-pair structure is the best compact candidate found so far:
  it keeps left/right order at each factor endpoint while dropping the
  downstream `p/q` label.
- Coarse family compression failed, which means the law is sharper than the
  first broad proto-family language.

The current state is positive but not final:

```text
proved_law = no
measured_gap_correlation = yes
compact_rule_layer = right_residue_gated_endpoint_pair_surface_measured
live_factor_recovery = no
next_required_step = derive the formal compatibility rule that explains why
                     the right-residue gate selects stable exact endpoint-pair
                     absences
```

## Next Rule-Extraction Step

The next experiment should stay on the active object. Do not return to broad
token multisets or coarse public-side summaries.

Use:

```text
public_word_gwr_side -> slot_residue_phase
```

as the extraction surface, then compare candidate rules against:

```text
public_word_gwr_side -> unordered_endpoint_pair_residue_phase
```

as the compact law candidate.

The next concrete work is:

1. Extract the highest-support absent cells from the active slot-preserving
   surface.
2. Group them only by transformations that preserve directed endpoint-pair
   roles.
3. Test those candidate rules on a fresh band, preferably `17001..19000`.
4. Promote a compact rule only if it stays near the slot-preserving surface and
   materially beats the known insufficient objects.

Promotion criteria:

```text
strict_falsification_rate materially below 510 per mille
strict_falsification_rate below slot_residue_phase_multiset rate of 49 per mille
preferred target at or below unordered_endpoint_pair rate of 21 per mille
no promotion if the representation collapses directed endpoint-pair structure
```

## Source Evidence

Primary result notes:

```text
PUBLIC_GRAMMAR_FORWARD_STABLE_INCOMPATIBILITIES.md
PUBLIC_GRAMMAR_PROTO_FAMILY_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_SLOT_LOCK_PROBE_RESULTS.md
PUBLIC_GRAMMAR_DIRECTION_LOCK_PROBE_RESULTS.md
PUBLIC_GRAMMAR_ROLLING_FORWARD_17001_19000_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_PAIR_FAMILY_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_PAIR_PREDICATE_FORWARD_RESULTS.md
PUBLIC_GRAMMAR_RIGHT_BOUNDARY_SURFACE_RESULTS.md
PUBLIC_GRAMMAR_HYBRID_ENDPOINT_PAIR_SURFACE_RESULTS.md
PUBLIC_GRAMMAR_JOINT_ENDPOINT_PAIR_RIGHT_BOUNDARY_RESULTS.md
PUBLIC_GRAMMAR_DIRECTIONAL_BOUNDARY_GATE_RESULTS.md
PUBLIC_GRAMMAR_ENDPOINT_SPACE_REDUCTION.md
PUBLIC_GRAMMAR_TRANSPORTED_CANDIDATE_FILTER.md
PUBLIC_GRAMMAR_WORD_CONDITIONED_TRANSPORTED_FILTER.md
```

Primary scripts:

```text
enriched_multiplication_map_corpus.py
absent_cell_forward_stability.py
stable_absent_family_profile.py
proto_family_forward_test.py
slot_factor_public_quotient_test.py
public_grammar_endpoint_space_reduction.py
endpoint_pair_candidate_exclusions.py
endpoint_pair_family_profile.py
endpoint_pair_family_forward_test.py
endpoint_pair_family_survival_contrast.py
endpoint_pair_predicate_forward_test.py
right_boundary_compatibility_surface.py
hybrid_endpoint_pair_surface.py
joint_endpoint_pair_right_boundary_surface.py
directional_boundary_gate_surface.py
```

Primary outputs:

```text
output/absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000_top5000/summary.json
output/absent_cell_forward_stability_9001_11000_to_11001_13000_to_15001_17000_top5000/summary.json
output/proto_family_forward_test_15001_17000/summary.json
output/proto_family_forward_test_15001_17000_public_word_factor_tokens_min3/summary.json
output/slot_factor_public_quotient_test_15001_17000_factor_modes/summary.json
output/direction_lock_probe_15001_17000/summary.json
output/proximity_endpoint_pair_probe_15001_17000_fixed/summary.json
output/enriched_multiplication_map_corpus_17001_19000/summary.json
output/slot_factor_public_quotient_test_17001_19000_rolling/summary.json
output/endpoint_pair_candidate_exclusions_17001_19000_rolling/summary.json
output/endpoint_pair_family_profile_17001_19000_rolling/summary.json
output/enriched_multiplication_map_corpus_19001_21000/summary.json
output/endpoint_pair_family_forward_test_19001_21000/summary.json
output/endpoint_pair_family_survival_contrast_19001_21000/summary.json
output/enriched_multiplication_map_corpus_21001_23000/summary.json
output/endpoint_pair_predicate_forward_test_21001_23000/summary.json
output/right_boundary_compatibility_surface_21001_23000/summary.json
output/enriched_multiplication_map_corpus_23001_25000/summary.json
output/right_boundary_compatibility_surface_23001_25000/summary.json
output/hybrid_endpoint_pair_surface_21001_23000/summary.json
output/hybrid_endpoint_pair_surface_23001_25000/summary.json
output/hybrid_endpoint_pair_surface_25001_27000/summary.json
output/enriched_multiplication_map_corpus_25001_27000/summary.json
output/enriched_multiplication_map_corpus_27001_30000/summary.json
output/joint_endpoint_pair_right_boundary_surface_21001_23000/summary.json
output/joint_endpoint_pair_right_boundary_surface_23001_25000/summary.json
output/joint_endpoint_pair_right_boundary_surface_25001_27000/summary.json
output/joint_endpoint_pair_right_boundary_surface_27001_30000/summary.json
output/directional_boundary_gate_surface_21001_23000/summary.json
output/directional_boundary_gate_surface_23001_25000/summary.json
output/directional_boundary_gate_surface_25001_27000/summary.json
output/directional_boundary_gate_surface_27001_30000/summary.json
```

## Guardrails

Do not claim theorem status from these measured surfaces.

Do not describe the current result as live factor recovery.

Do not use candidate divisibility, product checks, `gcd`, factor APIs, or
classical factoring as the inference route.

Do not promote a compression that collapses the factor-side slots before
testing the role-preserving version.

Do not treat thin observations as supported falsifications unless they meet
the stated support threshold for that experiment.
