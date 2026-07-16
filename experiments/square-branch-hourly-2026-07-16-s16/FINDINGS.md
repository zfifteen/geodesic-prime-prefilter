# Chamber-Reset Lemma Subsection S16 (Multiset Occupancy Residual)

**Date:** 2026-07-16  
**Job id:** `chamber-reset-lemma-draft`  
**Status:** constructive subsection drafted; Target S1* remains UNRESOLVED

## Plain object

On the selected-square chamber prefix of length `D(r)`, form the ordered Tau4
hit list and the successive-gap multiset. This subsection names:

1. Floor multiset mass at `g ≤ 2` (`tight_frac`, Claim S16-A / RC48).
2. Body locus of the leftmost peak successive desert (`desert_pos_frac`, S16-B / RC49).
3. Large-desert tail share at `g ≥ 2 · median` (`large_frac`, S16-C / RC50).

Package: `MultisetOccupancy(r)` extending chamber-reset residual to
`ResetResidual^U(r) = (ResetResidual^B(r), MultisetOccupancy(r))`.

## Frame

PGS-native only: ordered chamber prefix, divisor-count field `tau`, endpoint
`D(r)`, ordered Tau4 successive gaps, Dual markers as side labels.

Not revived: fixed-band near-540 (RC2 falsified at D=738), d=4 SDA transfer.  
Not primary surface: RC45–RC47 MeanBodyPacking (remain S15).

## Constructive claims (lemma HTML)

| Claim | Object | Status |
| --- | --- | --- |
| S16-A | `tight_frac = #{g≤2}/n_gaps` | constructive residual |
| S16-B | `desert_pos_frac = (mid(i*)−first)/body` | constructive residual |
| S16-C | `large_frac`; MultisetOccupancy; ResetResidual^U | constructive residual |

Document:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`

## Attached measured residual (audit only)

| ID | Bound | Observed (7 unique chambers) | Status |
| --- | --- | --- | --- |
| RC48 | `0.08 ≤ tight_frac ≤ 0.30` | `[0.113, 0.231]` | holds |
| RC49 | `0.25 ≤ desert_pos ≤ 0.98` | `[0.347, 0.933]` | holds; all peaks interior |
| RC50 | `0.08 ≤ large_frac ≤ 0.35` | `[0.118, 0.288]` | holds |

Surface: util maxima through `4e8–5e8` + `o_q ∈ {2,4,6}` branch-max panel.
Source measurements: `experiments/square-branch-hourly-2026-07-16-rc48/`.

## Theorem boundary

`PROOF.md` §Square-Branch Reduction: prime-square proximity / Target S1* remains
**UNRESOLVED**. Direct next-prime and Interior Maximizer remain **PROVED**.
Residual holds do not empty `Annulus(r)` and do not force `D(r) ≤ C_dyn(r)`.

## Falsification commands

```text
# Target S1* (primary)
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000001 \
  --max-prime 600000000 \
  --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_5e8_6e8

# Residual panel RC48–RC50 / S16-A–C (does not prove S1*)
python3 experiments/square-branch-hourly-2026-07-16-rc48/offset_540_residual_rc48_probe.py
```

## Next pressure

Queue falsification `5e8–6e8` (preferred holdout). Re-check RC48–RC50 on any new
util maximum. Prefer proximity-slack `u(r)=D(r)/C_dyn(r)` or new-band pressure
over further multiset minting on the same 7 chambers.
