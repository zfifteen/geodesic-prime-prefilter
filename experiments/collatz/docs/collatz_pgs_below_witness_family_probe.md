# Collatz-PGS Below-Witness Family Probe

## Summary

The below-witness reset effect is not spread evenly across first-descent
blocks. At odd seeds `3 <= s <= 999999`, the positive median contribution
comes from a small set of nontrivial exact carrier families, while the upper
tail reversal comes from a different set of families.

The probe decomposes the existing below-vs-no-witness stability rows by exact
`(odd_steps_to_first_descent, final_v2)` family. It preserves the same matched
comparison already used by the stability probe and only redistributes the
matched-weighted mean of per-family deltas.

## Input

```text
output/collatz_pgs_below_witness_stability_probe/stability_rows.jsonl
```

Each row already contains an exact
`(odd_steps_to_first_descent, final_v2)` stratum and the matched comparison
between:

- terminal below-witness blocks, where the final source is `witness - 1`;
- no-witness-contact blocks.

## Aggregate Result

| Measurement | Value |
|---|---:|
| Matched family count | `175` |
| Matched weight total | `12813` |
| Overall median reset-strength delta contribution | `0.48311171458205115` |
| Overall P90 reset-strength delta contribution | `-0.06565152576687669` |
| Overall P99 reset-strength delta contribution | `-0.08685398078967059` |

The family decomposition exactly conserves the stability-probe result:
the median stays positive, and the P90/P99 tails stay negative against
no-witness blocks.

## Carrier Families

The largest positive odd-step contribution is exact step `3`.

| Odd steps | Matched weight | Weight share | Median contribution | P90 contribution | P99 contribution |
|---:|---:|---:|---:|---:|---:|
| `3` | `1064` | `0.08304066182783111` | `0.2734251548497368` | `0.00000009225410491254391` | `-0.0000000486560089499999` |
| `4` | `274` | `0.02138453133536252` | `0.06043249894869892` | `-0.00000005039141072261268` | `-0.0000000764312570614039` |
| `5` | `399` | `0.031140248185436665` | `0.04932929333329974` | `-0.02104856202662328` | `-0.021048731051695243` |
| `8` | `141` | `0.011004448606883634` | `0.028550253312036186` | `-0.012473040966013003` | `-0.01247364847300876` |

Exact step `1` carries most of the matched weight, but its contribution is
near zero. It is background mass, not the reset carrier.

The largest positive final-`v2` groups are mixed. Final `v2=4` and `v2=8`
are median-positive and tail-positive. Final `v2=7`, `v2=9`, and `v2=11`
are median-positive but tail-negative.

| Final `v2` | Matched weight | Weight share | Median contribution | P90 contribution | P99 contribution |
|---:|---:|---:|---:|---:|---:|
| `9` | `60` | `0.004682744088035589` | `0.07779006073959656` | `-0.005852927321912092` | `-0.015207933146195049` |
| `11` | `19` | `0.00148286896121127` | `0.07364946250246057` | `-0.010544212581619678` | `-0.010544245131813557` |
| `8` | `140` | `0.010926402872083041` | `0.06937187766326004` | `0.0046042029416856365` | `0.0046035875096389735` |
| `7` | `235` | `0.01834074767813939` | `0.06048469278044245` | `-0.019173348053108902` | `-0.02410148440372383` |
| `4` | `1682` | `0.13127292593459766` | `0.051951155793730296` | `0.0015440760376007525` | `0.0012022023743742324` |

## Sign Pattern

The positive median reset effect is carried by three sign-pattern families.

| Sign pattern | Matched weight | Weight share | Median contribution | P90 contribution | P99 contribution |
|---|---:|---:|---:|---:|---:|
| `positive_positive_positive` | `728` | `0.056817294934831813` | `0.2199992755453345` | `0.05122454628436955` | `0.05122416092527163` |
| `positive_positive_negative` | `466` | `0.03636931241707641` | `0.173908935768486` | `0.011235318371430195` | `-0.00000020519497792648056` |
| `positive_negative_negative` | `355` | `0.027706235854210566` | `0.13747025916175537` | `-0.03490249237932025` | `-0.04112854505304973` |

The negative tail is mostly carried by:

| Sign pattern | Matched weight | Weight share | Median contribution | P90 contribution | P99 contribution |
|---|---:|---:|---:|---:|---:|
| `negative_negative_negative` | `3646` | `0.28455474908296263` | `-0.05155563121895146` | `-0.09401911579771685` | `-0.09483951129888446` |

## Interpretation

The reset-certificate signal has structure, not just enrichment. Below-witness
terminal contact splits into at least two regimes:

- a short-block regime, led by exact step `3`, where below-witness contact
  produces the main positive median reset contribution;
- a longer or higher-variance regime where the median can remain positive
  while the upper tail reverses.

The broad reset-profile experiment has done its job. The next useful move is
not another generic enrichment probe. The next useful move is algebra on the
short-block residue families, especially exact step `3` with final `v2=4` and
final `v2=8`.

## Output

```text
output/collatz_pgs_below_witness_family_probe/summary.json
output/collatz_pgs_below_witness_family_probe/family_rows.jsonl
output/collatz_pgs_below_witness_family_probe/odd_step_rows.jsonl
output/collatz_pgs_below_witness_family_probe/final_v2_rows.jsonl
output/collatz_pgs_below_witness_family_probe/sign_pattern_rows.jsonl
```
