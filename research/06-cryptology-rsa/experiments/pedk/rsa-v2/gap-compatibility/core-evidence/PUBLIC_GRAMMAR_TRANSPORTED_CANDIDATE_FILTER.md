# Public Grammar Transported Candidate Filter

## Claim

The public-grammar exclusion pipeline now has a fixed-`N` search-space
reduction bridge. For each semiprime `N`, the measurement builds public
candidate endpoints `x`, transports each candidate through `floor(N / x)`, and
applies survived public-grammar exclusions only when the transported coordinate
is also a public endpoint.

In the fresh bands `5501..7500`, the current survived rules remove a small
number of fixed-`N` transported candidates without removing the true factor.

## Measurement Contract

For each known semiprime row, `p` and `q` are labels for corpus construction and
audit only. The filter uses:

```text
N
public word around N
public endpoint candidate x
y = floor(N / x)
public endpoint status and gap grammar around x and y
```

The filter does not use:

```text
N % x
candidate multiplication
hidden factor lookup
gcd
primality APIs
factor APIs
```

The existing factor-neighborhood exclusions were learned on endpoint-endpoint
classes. Therefore this first bridge applies them only when the transported
coordinate `y = floor(N / x)` is itself a public endpoint. Non-endpoint
transported coordinates are counted in the candidate denominator, but they are
not classified by the current endpoint-endpoint exclusion vocabulary.

## Fresh-Band Result

The run covers:

```text
bands = factors 5501..6500 and 6501..7500
semiprime_rows = 12564
candidate_x_count = 569104
transported_endpoint_candidate_count = 72869
compatibility_eliminated_candidate_count = 11
true_p_eliminated_by_compatibility_count = 0
```

Aggregate reduction:

```text
fraction_of_all_public_x_candidates = 11 / 569104 = 0.001933%
fraction_of_transported_endpoint_candidates = 11 / 72869 = 0.015096%
```

The current effect is concentrated in the two public words whose rules survived
the fresh targeted slice:

| public rule | rows | public `x` candidates | transported endpoint candidates | eliminated | reduction over all `x` | reduction over transported endpoints | true `p` removed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Rank 4 public word | `42` | `1935` | `241` | `9` | `0.4651%` | `3.7344%` | `0` |
| Rank 2 public word | `23` | `1042` | `115` | `2` | `0.1919%` | `1.7391%` | `0` |

## Interpretation

The earlier `3.8%` endpoint-pair number measured the corpus-wide prevalence of
the excluded endpoint-endpoint classes. It did not measure fixed-`N` candidate
removal.

This transported-candidate filter is the first fixed-`N` bridge. It answers a
different question:

```text
Given a public N with public word W, how many public endpoint candidates x
are removed after floor transport and public endpoint-neighborhood
classification?
```

The current answer is modest. Across the full fresh corpus the reduction is
near zero because the survived rules apply to only two public words and because
the existing exclusions were not learned on transported coordinate classes. In
the matching public-word slices, the reduction reaches `1.7%..3.7%` of the
transported endpoint subset with zero observed loss of the true factor.

## Boundary

This is measured search-space reduction inside the current small-band
close-factor corpus model. It is not theorem status, not live factor recovery,
and not an RSA-scale claim.

The transported classification is deliberately strict:

```text
apply existing endpoint-endpoint exclusions only when y = floor(N / x)
is also a public endpoint
```

A broader transported-coordinate grammar is still unresolved. That grammar
would classify non-endpoint transported coordinates by the containing gap,
offset, adjacent gaps, and selected point. Until that vocabulary is defined and
validated, the current bridge reports a conservative endpoint-endpoint
transport measurement.

## Reproduction

Run:

```text
python3 public_grammar_transported_candidate_filter.py
```

The script writes:

```text
output/public_grammar_transported_candidate_filter_5501_7500/summary.json
output/public_grammar_transported_candidate_filter_5501_7500/transported_candidate_rows.jsonl
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
status = measured_public_grammar_transported_candidate_filter
candidate_space_kind = fixed_N_public_endpoint_x_with_floor_transport_y
transported_class_boundary = existing_endpoint_endpoint_class_only_when_y_is_endpoint
```
