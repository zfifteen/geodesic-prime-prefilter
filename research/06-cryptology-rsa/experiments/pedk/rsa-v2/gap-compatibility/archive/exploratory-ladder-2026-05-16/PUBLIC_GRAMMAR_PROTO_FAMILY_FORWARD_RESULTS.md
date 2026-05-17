# Public Grammar Proto-Family Forward Results

## Claim

The stable individual-cell surface survived, but the first proto-family
compression did not.

The previous result showed that individual cells under

```text
public_word_gwr_side -> oriented_factor_phase_word
```

were highly stable across fresh bands: the top `5000` selected absent cells had
`0` supported falsifications in `13001..15000`.

The next question was whether those stable cells could be compressed into
compact families. The answer, under the tested family language, is no. The
family abstraction merged compatible structures back into the excluded surface.

## Tested Forward Band

The independent forward band was:

```text
forward_band = factors 15001..17000
forward_row_count = 21115
```

The enriched corpus status was:

```text
status = measured_enriched_multiplication_map_corpus
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
```

## Strict Proto-Family Test

The input proto-families came from the clean family profile over the top `5000`
stable absent cells from the previous forward test.

The tested family axes were:

```text
public_containing_side__factor_token_multiset
public_containing_side__factor_p_word
public_containing_side__factor_q_word
public_prev_containing_side__factor_token_multiset
public_containing_next_side__factor_token_multiset
```

The strict boundary was:

```text
a proto-family exclusion is falsified by any forward row matching both
its public condition and its factor condition
```

Measured result:

```text
selected_clean_proto_family_count = 192
forward_testable_family_count = 185
survived_forward_family_count = 6
falsified_forward_family_count = 179
not_testable_forward_family_count = 7
strict_falsification_rate = 967 per mille
```

At a diagnostic threshold of `5` matching forward rows:

```text
forward_testable_family_count = 185
survived_forward_family_count = 70
falsified_forward_family_count = 115
falsification_rate = 621 per mille
```

The strict result controls the rule status. A general exclusion family is
falsified by one matching row.

## What Failed

The failed step was the family abstraction, not the stable individual-cell
surface.

The stable cell object keeps:

```text
full public word with GWR side
full oriented factor phase word
```

The proto-family abstraction dropped part of that structure. It replaced the
full oriented factor word with broader factor summaries such as token multisets
or one-sided p/q factor words. That compression admitted forward rows that the
individual cell surface had kept separated.

The measurement therefore invalidates this rule-derivation method:

```text
derive clean proto-rules by grouping stable absent cells only by
containing subtype/GWR side and broad factor token or one-sided factor words
```

## Surviving Strict Families

Only six clean proto-families survived the strict `15001..17000` test. All six
use a factor token multiset and an explicit public previous or following gap
context.

```text
surviving_constrained_axis_count = 6
public_prev_containing_side__factor_token_multiset survivors = 2
public_containing_next_side__factor_token_multiset survivors = 4
```

The six survivors were:

```text
prev=o4_d4_odd|d<=4
containing=o2_d4_a2_d4_odd@mid
side=after_winner
factor_tokens=o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@late:1,
              o6_higher_divisor_odd@mid:1

containing=o2_d4_a2_d4_odd@mid
next=o4_d4_odd|d<=4
side=after_winner
factor_tokens=o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@late:1,
              o6_higher_divisor_odd@mid:1

containing=o4_d4_a4_d4_odd@early
next=o4_d4_odd|d<=4
side=at_winner
factor_tokens=o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@mid:2

containing=o6_d4_a2_d4_odd@mid
next=o4_d4_odd|d<=4
side=after_winner
factor_tokens=o2_higher_divisor_odd@mid:1,
              o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@mid:1

containing=o4_d4_a4_d4_odd@mid
next=o4_d4_odd|d<=4
side=after_winner
factor_tokens=o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@late:1,
              o6_higher_divisor_odd@mid:1

prev=o2_d4_odd|d<=4
containing=o2_d4_a2_d4_odd@early
side=at_winner
factor_tokens=o4_higher_divisor_odd@mid:2,
              o6_higher_divisor_odd@late:1,
              o6_higher_divisor_odd@mid:1
```

These survivors are not promoted to laws. They are thin survivors after a
mostly failed compression test.

## Middle Compression Diagnostic

A tighter middle object was also tested:

```text
public_word_gwr_side -> factor_token_multiset
```

This keeps the full public word and GWR side, but compresses the factor side to
the token multiset.

Using `min_survived = 3`, the profile contained:

```text
public_word_gwr_side__factor_token_multiset_profile_count = 559
clean_public_word_gwr_side__factor_token_multiset_count = 463
mixed_public_word_gwr_side__factor_token_multiset_count = 96
```

Forward result on `15001..17000`:

```text
selected_profile_count = 463
forward_testable_family_count = 458
survived_forward_family_count = 224
falsified_forward_family_count = 234
not_testable_forward_family_count = 5
strict_falsification_rate = 510 per mille
```

This is better than the broad proto-family language but still not stable
enough to serve as a rule layer. Compressing the factor side from the full
oriented factor phase word down to token multiset loses necessary structure.

## Current Boundary

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = family_compression_invalidated
surviving_object = individual stable absent cells under
                   public_word_gwr_side -> oriented_factor_phase_word
invalidated_object = broad proto-family compression over containing side,
                     p/q side summaries, and factor token multisets
unresolved_object = a compact grammar that preserves enough oriented
                    factor-neighborhood structure to remain stable
```

The research direction is now clearer. The compatibility signal is real at the
individual cell level. The next representation must compress the factor side
without discarding orientation-specific left/right structure.

## Reproduction

Build the forward enriched band:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 15001:17000 \
  --output-dir output/enriched_multiplication_map_corpus_15001_17000
```

Run the strict proto-family test:

```text
python3 proto_family_forward_test.py
```

Run the diagnostic threshold test:

```text
python3 proto_family_forward_test.py \
  --observation-threshold 5 \
  --output-dir output/proto_family_forward_test_15001_17000_threshold5
```

Run the tighter middle-object profile:

```text
python3 stable_absent_family_profile.py \
  --min-survived 3 \
  --output-dir output/stable_absent_family_profile_9001_11000_to_11001_13000_to_13001_15000_top5000_min3
```

Run the full-public/factor-token test:

```text
python3 proto_family_forward_test.py \
  --profile-dir output/stable_absent_family_profile_9001_11000_to_11001_13000_to_13001_15000_top5000_min3 \
  --axis public_word_gwr_side__factor_token_multiset \
  --output-dir output/proto_family_forward_test_15001_17000_public_word_factor_tokens_min3
```
