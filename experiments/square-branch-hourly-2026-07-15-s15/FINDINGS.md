# Chamber-Reset Lemma Subsection S15 (Mean-Body Packing)

**Date:** 2026-07-16  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC45-RC47 audit only

## Plain object

After the chamber names interior Tau4 packing in median units, successive-gap
dynamic range, and Dual against the peak interior desert (Claims S14-A / S14-B /
S14-C), keep the same ordered successive Tau4 gaps and re-scale them on mean
spacing, hit count, and Tau4 body span:

1. Packing floor of the tightest successive Tau4 gap relative to the mean gap
   (`min_over_mean = min_gap / mean_gap`).
2. Dual L1 isolation per Tau4 hit
   (`dual_per_hit = dual_l1 / |Tau4|`).
3. Peak successive desert as a share of Tau4 body support
   (`max_over_body = max_gap / body`).

Project terms: Claims S15-A / S15-B / S15-C, residual package RC45-RC47,
`MeanBodyPacking(r)`, `ResetResidual^B(r)`.

## Deliverable this activation

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S15** states:

- **S15-A** mean-unit packing floor min over mean (constructive)
- **S15-B** Dual L1 per Tau4 hit (constructive)
- **S15-C** peak desert body-share; `MeanBodyPacking` + `ResetResidual^B`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior activation on the same
panel, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC45 | min_over_mean | `0.08..0.30` | `[0.112, 0.223]` holds 8/8 |
| RC46 | dual_per_hit | `0.05..0.50` | `[0.077, 0.415]` holds 8/8 |
| RC47 | max_over_body | `0.03..0.12` | `[0.041, 0.085]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | min/mean | dual/count | max/body |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.114 | 0.400 | 0.085 |
| 4 | 482342527 | 486 | 0.112 | 0.415 | 0.056 |
| 6 | 424171123 | 738 | 0.131 | 0.115 | 0.041 |

## Relation to prior residual surface

- RC42-RC44 (min/median, max/min, dual/max_gap) retained as S14 primary surface.
- RC45 places packing floor in **mean** units, complementary to RC42 (median).
- RC46 bounds Dual isolation **per hit**, distinct from dual/max_gap (RC44),
  dual/median (RC41), dual/mean (RC29), and hit density (RC21).
- RC47 scales peak desert by **Tau4 body support**, distinct from max/D (RC11)
  and max/min (RC43).
- Prior residual audit package
  `experiments/square-branch-hourly-2026-07-15-rc45/` supplies the measured
  envelopes; this activation formalizes them as lemma subsection S15.

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S15 does not empty `Annulus(r)`. Bounded mean-body ratios do not force
`D(r) ≤ C_dyn(r)`. Invalidated d=4 SDA and fixed-band near-540 are not revived.
RC2 remains falsified at `D=738`.

## Hypotheses

Reuse H1-H6 from Subsections S1 / S3 / S4. No new hypothesis. Formulas under
`|Tau4(r)| >= 2`, `mean_gap(r) > 0`, and `body(r) > 0` for S15-A/C; S15-B under
`|Tau4(r)| >= 1` (joint package evaluated under `|Tau4| >= 2` on the measured
panel). Holds on every measured residual row attached here.

## Minimal falsification commands

Target S1* (emptiness of every `Annulus(r)`):

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8
```

Residual panel RC45-RC47 / Claims S15-A-S15-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-15-rc45/offset_540_residual_rc45_probe.py
```

## Not claiming

- No proof of Target S1*
- No packing theorem; no promotion of RC45-RC47 to theorem
- No density law `rho4`; dual/count is Dual L1 per hit, not hit rate over D
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer
- No revival of fixed-band near-540 (RC2 remains falsified)

## Next pressure

Queue falsification `5e8-6e8` (preferred holdout) or H_CTC square-branch probe.
Re-check RC45-RC47 / `MeanBodyPacking` on any new util maximum. Prefer new-band
holdout over further ratio minting on the same 7 chambers. Keep S15 residual only.
