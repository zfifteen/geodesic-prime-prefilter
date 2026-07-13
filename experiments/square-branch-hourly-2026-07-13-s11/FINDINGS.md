# Chamber-Reset Lemma Subsection S11 (Robust Scale Residual)

**Date:** 2026-07-13  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC33-RC35 audit only

## Plain object

After the chamber names median/mean central shape, sub-mean successive-gap
majority, and Tau4 body early-mass (Claims S10-A / S10-B), look at the same
ordered successive-gap list, trail marker, and Dual body for robust scale and
late body mass:

1. Interquartile range of successive gaps over the median gap (`iqr_over_median`).
2. Trail from last τ4 to late τ=3 endpoint, scaled by mean gap (`trail_over_mean`).
3. Share of Tau4 hits in the last quartile of the Dual body
   `[first_tau4, last_tau4]` (`last_body_quartile_frac`).

Project terms: Claims S11-A / S11-B / S11-C, residual package RC33-RC35,
`RobustScale(r)`, `ResetResidual^R(r)`.

## Deliverable this hour

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S11** states:

- **S11-A** successive gap IQR and IQR-over-median robust scale (constructive)
- **S11-B** trail/mean closing isolation and Tau4 body last-quartile mass
  (constructive)
- **S11-C** robust-scale extended chamber-reset residual `ResetResidual^R`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior hour, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC33 | iqr_over_median | `[0.70, 1.55]` | `[0.833, 1.417]` holds 8/8 |
| RC34 | trail_over_mean | `[0.15, 2.50]` | `[0.223, 2.278]` holds 8/8 |
| RC35 | last_body_quartile_frac | `[0.18, 0.35]` | `[0.233, 0.297]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | IQR/med | trail/mean | last_Q |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 1.333 | 2.278 | 0.233 |
| 4 | 482342527 | 486 | 1.357 | 0.672 | 0.283 |
| 6 | 424171123 | 738 | 1.167 | 1.045 | 0.240 |

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S11 does not empty `Annulus(r)`. Invalidated d=4 SDA and fixed-band near-540
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

Residual panel RC33-RC35 / Claims S11-A-S11-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-13-rc33/offset_540_residual_rc33_probe.py
```

## Not claiming

- No proof of Target S1*
- No promotion of RC33-RC35 to theorem
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer

## Next pressure

Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe.
Re-check RC33-RC35 / `RobustScale` on any new util maximum. Keep S11 residual only.
