# Chamber-Reset Lemma Subsection S9 (Gap Regularity Residual)

**Date:** 2026-07-13  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; residual RC27-RC29 audit only

## Plain object

After the chamber names mean spacing of consecutive `tau = 4` hits inside the
Dual body (Claim S8-A), look at the full ordered list of successive gaps between
those hits. Measure:

1. Peak successive gap over mean gap (`max_over_mean`).
2. Coefficient of variation of successive gaps (`gap_cv`).
3. Dual L1 scaled into mean-gap units (`dual_over_mean`).

Project terms: Claims S9-A / S9-B / S9-C, residual package RC27-RC29,
`GapRegularity(r)`, `ResetResidual^G(r)`.

## Deliverable this hour

One new constructive lemma subsection under

```text
research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html
```

Subsection **S9** states:

- **S9-A** successive Tau4 gap list and peak-to-mean ratio (constructive)
- **S9-B** gap CV and Dual isolation in mean-gap units (constructive)
- **S9-C** gap-regularity extended chamber-reset residual `ResetResidual^G`
  (constructive residual-state identification)

Attached residual claims (audit only, measured prior hour, not theorems):

| ID | Claim | Bound | Observed on util max / o_q panel through 4e8-5e8 |
| --- | --- | --- | --- |
| RC27 | max_over_mean | `<= 5.5` | `[2.605, 5.012]` holds 8/8 |
| RC28 | gap_cv | `[0.55, 1.0]` | `[0.663, 0.891]` holds 8/8 |
| RC29 | dual_over_mean | `[0.30, 3.0]` | `[0.445, 2.744]` holds 8/8 |

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1*
remains **UNRESOLVED**. Direct next-prime and Interior Maximizer remain proved.
S9 does not empty `Annulus(r)`. Invalidated d=4 SDA and fixed-band near-540
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

Residual panel RC27-RC29 / Claims S9-A-S9-C (does not prove S1*):

```text
python3 experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py
```

## Not claiming

- No proof of Target S1*
- No promotion of RC27-RC29 to theorem
- No classical primality / sieve / gcd / Miller-Rabin as PGS inference
- No revival of fixed cutoff map or d=4 SDA transfer

## Next pressure

Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe.
Re-check RC27-RC29 / `GapRegularity` on any new util maximum.
