# Public Grammar Word-Conditioned Transported Filter

## Claim

The public-word-conditioned transported filter is falsified as a safe exclusion
method under the current strict endpoint-endpoint vocabulary.

The baseline band `5501..7500` selected two public words with positive
transported endpoint elimination and zero true-factor loss. On the fresh band
`7501..9000`, the same selected words eliminated `11` transported endpoint
candidates, but also eliminated the true factor in `3` rows.

## Measurement Contract

The experiment tests this pipeline:

```text
baseline bands 5501..7500
  -> select public words with positive elimination and zero true-p loss
fresh band 7501..9000
  -> apply only those selected public-word filters
  -> measure transported endpoint candidate elimination
  -> audit true-p loss
```

The transported class boundary is unchanged:

```text
apply existing endpoint-endpoint exclusions only when y = floor(N / x)
is also a public endpoint
```

The experiment does not use divisibility, product closure, `gcd`, primality
APIs, or hidden factors as inference. The true factor is used only as an audit
label after filtering.

## Baseline Selection

The baseline selected two public words:

| public word | rows | public `x` candidates | transported endpoint candidates | eliminated | endpoint reduction | true `p` removed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `prev=o2_d4_odd\|d<=4\|containing=o2_d4_a2_d4_odd@early\|next=o4_d4_odd\|d<=4` | `42` | `1935` | `241` | `9` | `3.7344%` | `0` |
| `prev=o4_higher_divisor_even\|5<=d<=16\|containing=o2_d4_a2_d4_odd@mid\|next=o2_d4_odd\|d<=4` | `23` | `1042` | `115` | `2` | `1.7391%` | `0` |

Baseline aggregate:

```text
selected_rows = 65
candidate_x_count = 2977
transported_endpoint_candidate_count = 356
compatibility_eliminated_candidate_count = 11
endpoint_reduction = 3.0899%
true_p_eliminated_by_compatibility_count = 0
```

## Fresh Test

The fresh band `7501..9000` produced:

```text
selected_rows = 81
candidate_x_count = 4368
transported_endpoint_candidate_count = 550
compatibility_eliminated_candidate_count = 11
endpoint_reduction = 2.0000%
true_p_eliminated_by_compatibility_count = 3
outcome_status = falsified_true_p_eliminated
```

Per selected public word:

| public word | rows | public `x` candidates | transported endpoint candidates | eliminated | endpoint reduction | true `p` removed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `prev=o2_d4_odd\|d<=4\|containing=o2_d4_a2_d4_odd@early\|next=o4_d4_odd\|d<=4` | `44` | `2510` | `329` | `2` | `0.6079%` | `1` |
| `prev=o4_higher_divisor_even\|5<=d<=16\|containing=o2_d4_a2_d4_odd@mid\|next=o2_d4_odd\|d<=4` | `37` | `1858` | `221` | `9` | `4.0724%` | `2` |

The higher-reduction public word is not usable as an exclusion rule because it
removed the true factor twice.

## Falsifying Rows

The true-factor losses are:

| case | `N` | public word |
| --- | ---: | --- |
| `small_semiprime_7687_8761` | `67345807` | `prev=o2_d4_odd\|d<=4\|containing=o2_d4_a2_d4_odd@early\|next=o4_d4_odd\|d<=4` |
| `small_semiprime_7703_8209` | `63233927` | `prev=o4_higher_divisor_even\|5<=d<=16\|containing=o2_d4_a2_d4_odd@mid\|next=o2_d4_odd\|d<=4` |
| `small_semiprime_7907_8689` | `68703923` | `prev=o4_higher_divisor_even\|5<=d<=16\|containing=o2_d4_a2_d4_odd@mid\|next=o2_d4_odd\|d<=4` |

## Interpretation

The public-word-conditioned direction produced a real reduction signal, but it
failed the safety condition. A reduction that removes the true factor is not an
exclusion rule.

The result does not invalidate the gap-compatibility hypothesis. It invalidates
this particular transfer:

```text
endpoint-endpoint factor class exclusion
  -> strict transported endpoint candidate exclusion
  -> selected by public word alone
```

The selected public word is not enough. The next object is the falsifying
transported configuration: the full public structure around `N`, the eliminated
true endpoint `x = p`, and the transported endpoint `y = floor(N / x)`.

## Next Concrete Goal

Inspect the three falsifying rows and extract public features that distinguish
unsafe eliminations from safe eliminations. The next candidate guardrail should
come from public data only:

```text
public word around N
candidate endpoint x neighborhood
transported endpoint y neighborhood
relative position of N
relative position of y
floor-transport relation between x and y
```

The goal is not to rescue the falsified rule by hand. The goal is to identify
the missing public feature needed before transported candidate exclusions can be
made safe.

## Reproduction

Run:

```text
python3 public_grammar_word_conditioned_transported_filter.py
```

The script writes:

```text
output/public_grammar_word_conditioned_transported_filter_7501_9000/summary.json
output/public_grammar_word_conditioned_transported_filter_7501_9000/baseline_public_word_stats.jsonl
output/public_grammar_word_conditioned_transported_filter_7501_9000/selected_public_word_rows.jsonl
output/public_grammar_word_conditioned_transported_filter_7501_9000/fresh_public_word_stats.jsonl
output/public_grammar_word_conditioned_transported_filter_7501_9000/fresh_selected_candidate_rows.jsonl
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
status = measured_public_grammar_word_conditioned_transported_filter
outcome_status = falsified_true_p_eliminated
```
