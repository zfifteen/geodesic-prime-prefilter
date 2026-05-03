# Collatz-PGS Below-Witness Stability Probe

## Strongest Measured Result

Below-witness terminal contact is stable against above-witness terminal contact
across median, P90, and P99 reset comparisons. Against no-witness blocks, it is
a median-reset carrier but not a tail-stable carrier.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It reused the adjacent-side classes:

- below-witness terminal hit: final source equals `witness - 1`;
- above-witness terminal hit: final source equals `witness + 1`;
- no-witness contact.

All comparisons were matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata. For each matched stratum, the
probe measured median, P90, and P99 reset-strength deltas, then reported exact
two-sided sign tests on stratum signs and matched-weighted mean deltas.

## Below Versus Above

| Quantile | Positive strata | Negative strata | Positive weight share | Weighted mean delta | Sign-test p |
|---|---:|---:|---:|---:|---:|
| Median | `73` | `39` | `0.7870452528837621` | `0.9934374958512522` | `0.0016946822547182485` |
| P90 | `86` | `26` | `0.6921029281277729` | `0.9997759684812527` | `1.1009223084560129e-08` |
| P99 | `90` | `22` | `0.5856255545696539` | `0.9754731838240228` | `5.974214670852322e-11` |

The below-witness side beats the above-witness side across the measured reset
profile. This preserves the one-sided adjacent geometry result.

## Below Versus No-Witness

| Quantile | Positive strata | Negative strata | Positive weight share | Weighted mean delta | Sign-test p |
|---|---:|---:|---:|---:|---:|
| Median | `112` | `63` | `0.15304768594396317` | `0.48311171458205104` | `0.00026216812968672166` |
| P90 | `70` | `105` | `0.10746897682041677` | `-0.06565152576687666` | `0.009963042948026038` |
| P99 | `40` | `135` | `0.6383360649340514` | `-0.08685398078967067` | `3.014376828086386e-13` |

The median signal survives by stratum sign count and weighted mean delta, but
its matched weight is concentrated in median-negative strata. The tail reverses
against no-witness blocks: P90 and P99 both have negative weighted mean deltas,
and both have more negative than positive strata.

## Disposition

This sharpens the story. The below-witness cell is a real carrier relative to
the above-witness cell, and that side preference is stable through the upper
reset quantiles. The comparison against no-witness blocks is narrower. It says
the below-witness state can produce a stronger median reset profile, but the
effect is concentrated in a smaller matched-weight subset and does not survive
as an upper-tail advantage.

That makes the next question concrete: identify which exact-step and
final-`v2` carrier families create the positive median contribution, and which
families reverse the P90/P99 tail.

## Second-Opinion Check

A second-opinion pressure pass agreed that the estimand supports this read. It
also flagged the main residual risk: unweighted sign tests do not reflect
matched-weight concentration, so the positive median sign count should be read
beside the low positive matched-weight share. The recommended next action is
to decompose below-vs-no-witness stratum deltas by exact carrier family.

## Artifact Surface

- Probe: `benchmarks/python/predictor/collatz_pgs_below_witness_stability_probe.py`
- Contract test: `tests/python/predictor/test_collatz_pgs_below_witness_stability_probe.py`
- Summary: `output/collatz_pgs_below_witness_stability_probe/summary.json`
- Stability rows: `output/collatz_pgs_below_witness_stability_probe/stability_rows.jsonl`
