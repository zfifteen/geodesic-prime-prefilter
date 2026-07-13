# Chamber-Reset Lemma Subsection S10 (Gap Shape Residual)

**Date:** 2026-07-13  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC30-RC32 audit only

## Plain object

After the chamber names successive Tau4 gaps, peak-to-mean ratio, gap CV, and
Dual isolation in mean-gap units (Claims S9-A / S9-B), look at the same ordered
gap list and Dual body for central shape and body-half mass:

1. Median successive gap over mean gap (`median_over_mean`).
2. Fraction of successive gaps at most the mean (`frac_le_mean`).
3. Share of Tau4 hits strictly before the Dual-body midpoint
   (`early_body_frac` on `[first_tau4, last_tau4]`, not on half of `D`).

Project terms: Claims S10-A / S10-B / S10-C, residual package RC30-RC32,
`GapShape(r)`, `ResetResidual^S(r)`.

## Deliverable this hour

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S10** states:

- **S10-A** successive median gap and median-to-mean ratio (constructive)
- **S10-B** sub-mean successive-gap majority and Tau4 body early-mass
  (constructive)
- **S10-C** gap-shape extended chamber-reset residual `ResetResidual^S`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior hour, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC30 | median_over_mean | `[0.65, 0.95]` | `[0.683, 0.891]` holds 8/8 |
| RC31 | frac_le_mean | `>= 0.50` | `[0.549, 0.677]` holds 8/8 |
| RC32 | early_body_frac | `[0.40, 0.55]` | `[0.415, 0.538]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | med/mean | frac_le_mean | early_body_frac |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.683 | 0.644 | 0.500 |
| 4 | 482342527 | 486 | 0.784 | 0.577 | 0.415 |
| 6 | 424171123 | 738 | 0.784 | 0.632 | 0.469 |

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S10 does not empty `Annulus(r)`. Invalidated d=4 SDA and fixed-band near-540
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

Residual panel RC30-RC32 / Claims S10-A-S10-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-13-rc30/offset_540_residual_rc30_probe.py
```

## Not claiming

- No proof of Target S1*
- No promotion of RC30-RC32 to theorem
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer

## Next pressure

Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe.
Re-check RC30-RC32 / `GapShape` on any new util maximum. Keep S10 residual only.
