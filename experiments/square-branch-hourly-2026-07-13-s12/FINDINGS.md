# Chamber-Reset Lemma Subsection S12 (Opening-Scale Residual)

**Date:** 2026-07-13  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC36-RC38 audit only

## Plain object

After the chamber names IQR/median robust scale, trail/mean closing isolation,
and Tau4 body last-quartile mass (Claims S11-A / S11-B), look at the same
ordered successive-gap list, early marker, and mean gap for the complementary
opening-scale package:

1. Opening isolation of the first τ4 marker in mean-gap units
   (`open_over_mean = first_tau4 / mean_gap`).
2. Peak successive Tau4 desert relative to the median gap
   (`max_over_median = max_gap / median_gap`).
3. Interquartile width of successive gaps relative to the mean gap
   (`iqr_over_mean = IQR / mean_gap`).

Project terms: Claims S12-A / S12-B / S12-C, residual package RC36-RC38,
`OpeningScale(r)`, `ResetResidual^O(r)`.

## Deliverable this activation

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S12** states:

- **S12-A** opening isolation in mean-gap units (constructive)
- **S12-B** peak successive gap over median and IQR scaled by mean (constructive)
- **S12-C** opening-scale extended chamber-reset residual `ResetResidual^O`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior activation on the same
panel, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC36 | open_over_mean | `0.15..2.00` | `[0.223, 1.793]` holds 8/8 |
| RC37 | max_over_median | `2.50..8.00` | `[3.143, 7.333]` holds 8/8 |
| RC38 | iqr_over_mean | `0.50..1.20` | `[0.594, 1.065]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | open/mean | max/med | IQR/mean |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.456 | 7.333 | 0.911 |
| 4 | 482342527 | 486 | 1.793 | 3.714 | 1.065 |
| 6 | 424171123 | 738 | 0.392 | 5.000 | 0.915 |

## Relation to prior residual surface

- RC33-RC35 (IQR/median, trail/mean, body last-quartile) retained.
- RC36 is **opening** isolation in mean units, distinct from trail/mean (RC34)
  and Dual L1 / mean (RC29).
- RC37 is peak / **median**, distinct from max/mean (RC27).
- RC38 is IQR / **mean**, distinct from IQR/median (RC33).

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S12 does not empty `Annulus(r)`. Invalidated d=4 SDA and fixed-band near-540
are not revived. RC2 remains falsified at `D=738`.

## Hypotheses

Reuse H1-H6 from Subsections S1 / S3 / S4. No new hypothesis. Formulas under
`|Tau4(r)| >= 2` (holds on every measured residual row attached here).

## Minimal falsification commands

Target S1* (emptiness of every `Annulus(r)`):

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8
```

Residual panel RC36-RC38 / Claims S12-A-S12-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-13-rc36/offset_540_residual_rc36_probe.py
```

## Not claiming

- No proof of Target S1*
- No promotion of RC36-RC38 to theorem
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer

## Next pressure

Queue falsification `5e8-6e8` or H_CTC square-branch probe.
Re-check RC36-RC38 / `OpeningScale` on any new util maximum. Keep S12 residual only.
