# Chamber-Reset Lemma Subsection S13 (Median Dual Isolation)

**Date:** 2026-07-14  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC39-RC41 audit only

## Plain object

After the chamber names opening isolation in mean-gap units, peak-over-median,
and IQR-over-mean (Claims S12-A / S12-B), look at the same Dual markers and
median successive Tau4 gap for the complementary median-Dual package:

1. Opening isolation of the first τ4 marker in median-gap units
   (`open_over_median = first_tau4 / median_gap`).
2. Trail closing isolation of the last τ4 to the selected square in median units
   (`trail_over_median = trail_gap / median_gap`).
3. Full Dual L1 isolation in median units
   (`dual_over_median = dual_l1 / median_gap`).

Project terms: Claims S13-A / S13-B / S13-C, residual package RC39-RC41,
`MedianDual(r)`, `ResetResidual^M(r)`.

## Deliverable this activation

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S13** states:

- **S13-A** opening isolation in median-gap units (constructive)
- **S13-B** trail and Dual L1 isolation in median-gap units (constructive)
- **S13-C** median-Dual extended chamber-reset residual `ResetResidual^M`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior activation on the same
panel, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC39 | open_over_median | `0.20..2.50` | `[0.250, 2.286]` holds 8/8 |
| RC40 | trail_over_median | `0.20..3.50` | `[0.250, 3.333]` holds 8/8 |
| RC41 | dual_over_median | `0.40..4.50` | `[0.500, 4.000]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | open/med | trail/med | dual/med |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.667 | 3.333 | 4.000 |
| 4 | 482342527 | 486 | 2.286 | 0.857 | 3.143 |
| 6 | 424171123 | 738 | 0.500 | 1.333 | 1.833 |

## Relation to prior residual surface

- RC36-RC38 (open/mean, max/med, IQR/mean) retained.
- RC39 scales **opening** by median, distinct from open/mean (RC36).
- RC40 scales **trail** by median, distinct from trail/mean (RC34).
- RC41 scales **Dual L1** by median, distinct from dual/mean (RC29).
- Prior residual audit package
  `experiments/square-branch-hourly-2026-07-14-rc39/` supplies the measured
  envelopes; this activation formalizes them as lemma subsection S13.

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S13 does not empty `Annulus(r)`. Invalidated d=4 SDA and fixed-band near-540
are not revived. RC2 remains falsified at `D=738`.

## Hypotheses

Reuse H1-H6 from Subsections S1 / S3 / S4. No new hypothesis. Formulas under
`|Tau4(r)| >= 2` and `median_gap(r) > 0` (holds on every measured residual row
attached here).

## Minimal falsification commands

Target S1* (emptiness of every `Annulus(r)`):

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8
```

Residual panel RC39-RC41 / Claims S13-A-S13-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-14-rc39/offset_540_residual_rc39_probe.py
```

## Not claiming

- No proof of Target S1*
- No promotion of RC39-RC41 to theorem
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer

## Next pressure

Queue falsification `5e8-6e8` or H_CTC square-branch probe.
Re-check RC39-RC41 / `MedianDual` on any new util maximum. Keep S13 residual only.
