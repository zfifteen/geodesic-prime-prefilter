# Public Grammar Family Forward Results

## Claim

The apparent `o2:2|o4:2` / `mid:3|late:1` factor-family exclusion is
invalidated as a general public-grammar rule.

The family looked strong in the `7501..9000` top-25 targeted slice: all seven
candidate rows in that family survived. When isolated and tested on
`9001..11000`, six of the seven family candidates were falsified. The single
remaining public-word refinement then falsified on `11001..13000`.

## Top-25 Continuation

The old-track continuation tested the top `25` compressed public-grammar
candidate exclusions on the fresh band `7501..9000`.

```text
candidate_count = 25
fresh_band = factors 7501..9000
semiprime_rows = 13861
survived_fresh_public_slice = 13
falsified_fresh_public_slice = 12
falsification_row_count = 17
```

The strongest apparent survivor cluster was:

```text
factor_residue_multiset = o2:2|o4:2
factor_phase_multiset = mid:3|late:1
candidate_ranks = 7, 8, 9, 10, 11, 12, 13
7501..9000 status = all 7 survived
```

## Family Isolation Test

The exact family was then isolated and tested on the independent fresh band
`9001..11000`.

```text
candidate_count = 7
fresh_band = factors 9001..11000
semiprime_rows = 23653
survived_fresh_public_slice = 1
falsified_fresh_public_slice = 6
falsification_row_count = 8
```

The only surviving member was:

```text
candidate_rank = 8
public_word = prev=o2_d4_odd|d<=4|containing=o2_d4_a2_d4_odd@mid|next=o6_d4_odd|d<=4
factor_residue_multiset = o2:2|o4:2
factor_phase_multiset = mid:3|late:1
fresh_public_slice_row_count = 119
fresh_falsification_row_count = 0
```

## Single Public-Word Refinement

The remaining public-word refinement was tested on the next independent band
`11001..13000`.

```text
candidate_count = 1
fresh_band = factors 11001..13000
semiprime_rows = 22366
falsified_fresh_public_slice = 1
falsification_row_count = 1
fresh_public_slice_row_count = 95
```

The falsifying row was:

```text
case_id = small_semiprime_12457_12823
N = 159736111
p = 12457
q = 12823
public_word = prev=o2_d4_odd|d<=4|containing=o2_d4_a2_d4_odd@mid|next=o6_d4_odd|d<=4
factor_word = L=o2_higher_divisor_odd|d<=4@late|R=o4_higher_divisor_odd|d<=4@mid || L=o2_higher_divisor_odd|d<=4@mid|R=o4_higher_divisor_odd|d<=4@mid
```

## Interpretation

This result is useful because it prevents an attractive but false rule from
entering the evidence chain.

The `o2:2|o4:2` / `mid:3|late:1` factor family is not independently stable.
The survival in `7501..9000` was a finite-slice effect. The single surviving
public word in `9001..11000` was also not stable on the next band.

The result reinforces the prior lesson: compatibility is not carried by a
factor-side residue-phase family alone. The right object must include a richer
joint structure than:

```text
public word around N
factor residue multiset
factor phase multiset
```

## Reproduction

Run the top-25 continuation:

```text
python3 public_grammar_targeted_slice_check.py \
  --top-n 25 \
  --band 7501:9000 \
  --output-dir output/public_grammar_targeted_slice_check_top25_7501_9000
```

Run the isolated family test:

```text
python3 public_grammar_family_targeted_slice_check.py
```

Run the single public-word refinement:

```text
python3 public_grammar_family_targeted_slice_check.py \
  --public-word 'prev=o2_d4_odd|d<=4|containing=o2_d4_a2_d4_odd@mid|next=o6_d4_odd|d<=4' \
  --band 11001:13000 \
  --output-dir output/public_grammar_family_rank8_11001_13000
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
family_status = invalidated_as_general_exclusion_family
single_public_word_refinement_status = falsified
```
