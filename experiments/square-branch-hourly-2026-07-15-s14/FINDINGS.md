# Chamber-Reset Lemma Subsection S14 (Interior Tau4 Packing)

**Date:** 2026-07-15  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC42-RC44 audit only

## Plain object

After the chamber names Dual isolation in median-gap units (Claims S13-A /
S13-B / S13-C), look at the ordered successive Tau4 gaps for the complementary
interior packing package:

1. Packing floor of the tightest successive Tau4 gap relative to the median gap
   (`min_over_median = min_gap / median_gap`).
2. Body spacing dynamic range of the largest desert over the tightest step
   (`max_over_min = max_gap / min_gap`).
3. Dual L1 relative to the peak interior Tau4 desert
   (`dual_over_max_gap = dual_l1 / max_gap`).

Project terms: Claims S14-A / S14-B / S14-C, residual package RC42-RC44,
`InteriorPacking(r)`, `ResetResidual^P(r)`.

## Deliverable this activation

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S14** states:

- **S14-A** interior packing floor min over median (constructive)
- **S14-B** interior successive-gap dynamic range max over min (constructive)
- **S14-C** Dual L1 over peak desert; `InteriorPacking` + `ResetResidual^P`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior activation on the same
panel, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC42 | min_over_median | `0.10..0.35` | `[0.143, 0.250]` holds 8/8 |
| RC43 | max_over_min | `8..55` | `[14, 44]` holds 8/8 |
| RC44 | dual_over_max_gap | `0.10..1.10` | `[0.143, 0.923]` holds 8/8 |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | min/med | max/min | dual/max |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.167 | 44 | 0.545 |
| 4 | 482342527 | 486 | 0.143 | 26 | 0.846 |
| 6 | 424171123 | 738 | 0.167 | 30 | 0.367 |

## Relation to prior residual surface

- RC39-RC41 (open/median, trail/median, dual/median) retained.
- RC42 bounds the **interior packing floor**, complementary to RC37 max/median.
- RC43 bounds **body spacing dynamic range**, independent of Dual endpoint ratios.
- RC44 scales Dual L1 by **peak interior desert**, distinct from dual/median (RC41)
  and dual/mean (RC29).
- Prior residual audit package
  `experiments/square-branch-hourly-2026-07-14-rc42/` supplies the measured
  envelopes; this activation formalizes them as lemma subsection S14.

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S14 does not empty `Annulus(r)`. Bounded packing ratios do not force
`D(r) ≤ C_dyn(r)`. Invalidated d=4 SDA and fixed-band near-540 are not revived.
RC2 remains falsified at `D=738`.

## Hypotheses

Reuse H1-H6 from Subsections S1 / S3 / S4. No new hypothesis. Formulas under
`|Tau4(r)| >= 2`, `median_gap(r) > 0`, and `min_gap(r) > 0` (holds on every
measured residual row attached here).

## Minimal falsification commands

Target S1* (emptiness of every `Annulus(r)`):

```text
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8
```

Residual panel RC42-RC44 / Claims S14-A-S14-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-14-rc42/offset_540_residual_rc42_probe.py
```

## Not claiming

- No proof of Target S1*
- No packing theorem; no promotion of RC42-RC44 to theorem
- No density law `rho4`; packing ratios are not count density
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer
- No revival of fixed-band near-540 (RC2 remains falsified)

## Next pressure

Queue falsification `5e8-6e8` or H_CTC square-branch probe.
Re-check RC42-RC44 / `InteriorPacking` on any new util maximum. Keep S14 residual only.
