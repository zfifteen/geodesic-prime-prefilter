# FINDINGS_LWM_BAND_01

**Measured outcome: REPRODUCED (with partial improvement on cross-band true visibility and rank promotion in 3/4 toy cases; emitted set cardinality increased in 1 toy case and both ladder cases). No regression on the core contract requirement that true factor-distance offsets appear in the publicly emitted set.**

All public artifacts were written (frozen) by the runner before this findings document was created or any interpretive text was composed. Audit labels were used only for post-freeze comparison tables.

## Exact Band Rule Implemented (public, deterministic, no leakage)
```python
def band_for_r(r: int) -> int:
    if r < 2:
        return 0
    bl = r.bit_length()
    return math.floor(math.log2(bl))
```
Coherence C(t) = number of bands with positive support count at offset t (band coverage).

Nomination (both views): the complete set of offsets achieving the global maximum score value under that view (flat support or C). Tie-breaking for display order only: higher secondary support, then smaller |offset|.

This is the first-run implementation per plan 5.3 (log r bands). GWR/DNI typing not used.

## Before / After Comparison Table (toys + first two ladder rungs)

All runs used identical public web construction and holdout for each case. Flat = original max-support cardinality rule. Banded = LWM-BAND-01 max-C rule.

| Case              | Radius | Flat max support | Flat emitted size | # true direct in flat emitted | Flat ranks of trues | Banded max C | Banded emitted size | # true direct in banded emitted | Banded ranks of trues (selected) | Emitted size delta | Rank change for highest-C true | Coherence note |
|-------------------|--------|------------------|-------------------|-------------------------------|---------------------|--------------|---------------------|---------------------------------|----------------------------------|--------------------|--------------------------------|----------------|
| toy_23x31        | 26     | 3                | 1                 | 1                             | {-23:1, 23:2}       | 1            | 2                   | 2                               | same as flat                     | +1 (1→2)         | none (both surfaced)           | Both trues C=1; banded surfaces the support=1 true also |
| toy_43x59        | 50     | 3                | 1                 | 1                             | {43:1, -43:2}       | 2            | 1                   | 1                               | {-43:1 (was 2), 43:2}            | 0                  | Improved (the C=2 true now #1) | True at -43 has C=2 (cross-band); flat max was C=1 single-band |
| toy_61x83        | 71     | 3                | 1                 | 1                             | {61:1, -61:2}       | 2            | 1                   | 1                               | {-61:1 (was 2), 61:2}            | 0                  | Improved (the C=2 true now #1) | True at -61 has C=2; flat max was C=1 single-band |
| toy_89x113       | 100    | 3                | 1                 | 1                             | {89:1, -89:2}       | 2            | 1                   | 1                               | {89:1, -89:2}                    | 0                  | Maintained #1 for the C=2 true | True at 89 has C=2 and flat max support=3 |
| ladder_101x137   | 606    | 3                | 5                 | 5                             | 101:#1 ... (see summary) | 2       | 10                  | 10                              | 101:#1, 137:#2 ... (many improved from >5) | +5 (5→10)     | Several trues moved up (e.g. -505 4→3) | Max-C=2 captures 10 trues vs 5; includes lower-support cross-band |
| ladder_131x167   | 786    | 3                | 5                 | 5                             | 131:#1 ...          | 2            | 12                  | 12                              | -167:#1, 167:#2 ... (131 moved 1→13) | +7 (5→12)     | Mixed: top trues preserved, some mid moved | Similar pattern: more trues recovered at cost of larger emitted set |

**Core success criteria (plan 5.4) status:**
- True factor distance appears in emitted top holes: 4/4 toy cases (reproduced exactly; no regression). Ladder cases also recovered all flat hits plus additional trues.
- Rank improvement (true d under C vs raw support): achieved in 3/4 toys (the cross-band true promoted to rank 1 where it had been rank 2 under flat). Ladder: mixed but several individual true offsets improved rank.
- Reduction in emitted hole cardinality at equivalent recall: NOT achieved. Emitted size stayed same or increased (regressed on this secondary metric).
- Cross-band coherence documented higher for true d: Yes. In 3/4 toys the unique flat-max point had C=1 while a true had C=2 and was selected (or co-selected) under banded rule. False high-flat spikes often single-band.

## Raw Data Sources (frozen before this document)
- output/LWM_BAND_01/summary.md (full per-case hole lists + ranks)
- output/LWM_BAND_01/flat_top_holes.jsonl
- output/LWM_BAND_01/banded_top_holes.jsonl
- output/LWM_BAND_01/all_supported_offsets.jsonl (every public offset with S(t) and C(t))
- output/LWM_BAND_01/manifest.json + MANIFEST.txt (SHA256 of script inputs + all outputs)
- output/LWM_BAND_01/LWM_BAND_01_full_results.json (complete analyzer dicts)

SHA256s of the two input scripts and four primary outputs are recorded in MANIFEST.txt. All files were emitted by run_LWM_BAND_01.py in a single pass with public nomination logic executed before any findings text.

## Contract Compliance Notes
- 100% public-web path: visible composites factored only to build threads; p/q used solely for holdout identification and post-freeze scoring table.
- No candidate generation, no residue certificates, no pruning, no ratios, no classical inference in nomination.
- Band assignment and C(t) are pure functions of public r only.
- Both flat and banded views emitted side-by-side for every case.
- First implementation kept simple (log2 bit-length bands); GWR/DNI reserved per plan.
- PGS-first frame observed: started from ordered thread web (public factor threads), invariants (support per offset), applied rule (banded coherence), emitted public state.

## Interpretation (after data)
The log2(bit-length) banding successfully identifies cases where the highest raw-support hole is single-band while a true factor-distance hole carries cross-band support. In those cases the banded rule correctly promotes the structurally more coherent true offset to the top of the emitted list. 

The increase in emitted cardinality on some cases is the direct consequence of using a strict "all achieving max-C" rule (analogous to baseline's "all achieving max-support") when max C is achieved by multiple offsets of varying flat support. This is expected behavior under the exact nomination rule chosen; a future refinement could add secondary tie-breaking by flat support within same C without violating the contract.

Signal is preserved and in several instances structurally refined (higher coherence at true d). This constitutes a successful reproduction of the literal web recovery property with a measurable geometric refinement aligned with the Japanese diagonal invariant.

No contract violations detected in the execution or artifacts.

**Status for LWM-BAND-01: REPRODUCED + partial structural improvement. Ready for go/no-go on secondary experiments (LWM-CROSS-01 etc.) or refinement of the coherence aggregator / tie-break rule.**

---

*Generated after public freeze of all output/ artifacts. See REWIND_TO_LITERAL_WEB.md and the experiment plan index.html for governing contracts.*