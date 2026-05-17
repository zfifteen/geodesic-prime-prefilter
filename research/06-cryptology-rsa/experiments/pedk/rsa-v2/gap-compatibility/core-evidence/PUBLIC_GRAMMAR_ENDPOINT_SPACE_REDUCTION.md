# Public Grammar Endpoint-Space Reduction

## Claim

The public-grammar exclusion pipeline has a measured endpoint-pair prevalence
baseline. The current surviving rules correspond to about `3.8%` of unordered
endpoint pairs in the fresh factor bands `5501..7500`.

This is not the fixed-`N` search-space reduction metric. The fixed-`N`
transported candidate bridge is measured separately in
`PUBLIC_GRAMMAR_TRANSPORTED_CANDIDATE_FILTER.md`.

## Measurement

The prior stage found two candidate class exclusions that survived the fresh
targeted public-slice check:

```text
candidate_rank = 2
public_word = prev=o4_higher_divisor_even|5<=d<=16|containing=o2_d4_a2_d4_odd@mid|next=o2_d4_odd|d<=4
excluded_factor_class = residue o2:1|o4:2|o6:1, phase mid:3|late:1

candidate_rank = 4
public_word = prev=o2_d4_odd|d<=4|containing=o2_d4_a2_d4_odd@early|next=o4_d4_odd|d<=4
excluded_factor_class = residue o2:1|o4:1|o6:2, phase mid:3|late:1
```

The endpoint-space bridge treats each surviving exclusion as a rule over the
unordered endpoint-pair space in the selected bands. It counts all endpoint
pairs in the fresh bands, classifies their factor-neighborhood residue and
phase multisets, and counts the pairs removed by each survived rule.

## Result

The fresh endpoint-pair space contains:

```text
bands = factors 5501..6500 and 6501..7500
endpoint_pair_count = 12564
individual_endpoint_count = 225
```

The measured reductions are:

| candidate | eliminated endpoint pairs | eliminated fraction | surviving fraction | touched endpoints | fully removed endpoints | fresh public rows | actual eliminated rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Rank 4 | `484 / 12564` | `3.8523%` | `96.1477%` | `116 / 225` | `0` | `42` | `0` |
| Rank 2 | `480 / 12564` | `3.8204%` | `96.1796%` | `128 / 225` | `0` | `23` | `0` |

Both survived the endpoint-space audit because the excluded classes did not
remove the actual factor-neighborhood rows in the matching fresh public slices.
The current rules touch many individual endpoints, but they do not fully remove
any individual endpoint value. At this stage the measured reduction is pair
space, not standalone `p` or `q` endpoint deletion.

## Interpretation

This is a prevalence baseline for the excluded endpoint-endpoint classes. It
answers how common those classes are in the fresh endpoint-pair universe. It
does not answer how many candidates are removed for a specific public `N`.

The fixed-`N` bridge now reports the linked metric:

```text
rule survival on fresh public slices
fixed-N transported candidate reduction
```

The milestone target is not merely finding survived class exclusions. The
milestone target is a survived exclusion surface whose endpoint-pair reduction
is larger than a comparable classical search reduction at comparable cost.

## Reproduction

Run:

```text
python3 public_grammar_endpoint_space_reduction.py
```

The script writes:

```text
output/public_grammar_endpoint_space_reduction_5501_7500/summary.json
output/public_grammar_endpoint_space_reduction_5501_7500/endpoint_space_reduction_rows.jsonl
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
endpoint_space_kind = unordered_endpoint_pair_space
status = measured_public_grammar_endpoint_space_reduction
```
