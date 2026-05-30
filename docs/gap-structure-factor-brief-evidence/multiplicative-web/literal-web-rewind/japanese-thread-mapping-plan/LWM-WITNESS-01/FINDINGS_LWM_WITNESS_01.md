# FINDINGS_LWM_WITNESS_01 — Witness Completeness / GWR-DNI Coverage Signatures

**Experiment ID:** LWM-WITNESS-01  
**Branch:** literal-web-rewind (japanese-thread-mapping-plan isolated subdir)  
**Date run:** 2026-05-28 (autonomous subagent execution)  
**Baseline extended:** literal_web_hole_trace.py (flat public thread support cardinality)  
**Scope:** 4 toy cases + 19 ladder rungs (full up to 8009×10007, radius 48054)  

---

## RESULTS SUMMARY

**Status:** COMPLETE — Contract compliant. All artifacts public, frozen before any audit interpretation.

**Key Observations on Signatures:**
- Flat support cardinality (unchanged primary mechanism) already isolates true factor-distance offsets with perfect or near-perfect precision across the entire corpus: in 23/23 runs (4 toys + 19 ladder), the set of offsets reaching near-max support (≥ max_support-1 or ≥2) contained **zero false positives** (num_false_high_support = 0 in every discrimination_stats record).
- Consequently, GWR/DNI coverage signatures provided **no additional discriminating power for separating true vs. false high-support points** — because no false high-support points existed at the examined thresholds to discriminate.
- The signatures **did provide rich, deterministic, PGS-native structural certificate material** for every correctly nominated true high-support point:
  - Consistent recording of witness-composite count (often hundreds for larger radius), fraction tied to observed GWR-min-d composites (0–~20%+ depending on case), whether the global leftmost min-d composite participates in the coverage, and the avg/min DNI excess E(c) of the originating public composites.
  - Signature vectors for true recoveries are fully reproducible from public data alone.
  - Variation across true points (e.g., has_leftmost_gwr sometimes true for both p/q threads, sometimes false; num_gwr_min_witnesses varies) offers potential post-nomination "witness completeness" profile for structural certification, even if not needed for ranking here.
- In the Japanese analogy: the "completeness" (every term having witnesses in the "GWR/DNI band" of minimal-divisor public composites) is measurable as sidecar metadata on the literal thread crossings, but the primary geometric signal (raw crossing count) already suffices for nomination in these windows.

**Artifact Locations (absolute):**
- Isolated experiment dir: `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-WITNESS-01/`
- Runner: `.../LWM-WITNESS-01/lwm_witness_01.py` (self-contained extension; duplicates only the literal pure functions + PGS GWR/DNI sidecar logic)
- Outputs: `.../LWM-WITNESS-01/output/`
  - `lwm_witness_01_toys.json` (full per-case with all holes + signatures + discrimination_stats)
  - `lwm_witness_01_ladder.json` (19 rungs, identical structure)
  - `top_holes_toys.jsonl`, `near_high_toys.jsonl`, `ladder_rungs.jsonl`
  - `summary_toys.md`, `summary_ladder.md` (tables + per-case top-hole signatures)
  - `manifest.json`
- This findings: `.../LWM-WITNESS-01/FINDINGS_LWM_WITNESS_01.md`

**Contract Compliance Notes:**
- 100% literal multiplicative web + public-before-audit.
- PGS-first: started from ordered divisor-count field on public heldout composites → applied Leftmost Minimum-Divisor Rule (GWR) to select min-d attractor among them → DNI excess E(n) at those composites for the threads they generated.
- Signatures strictly sidecar: never read or used to filter, rank, or emit the primary top_holes (code path identical to baseline flat max-support).
- No ratio pruning, no candidate generation, no classical search as inference, no p/q leakage into public path, no residue/CRT.
- GWR/DNI derived exclusively from public composites already present in the web rows (divisor_count + value); no extra factoring or private data.
- All output files contain the raw public data + signatures; audit labels (p_thread/q_thread) used only for post-facto table construction in this findings.
- AGENTS.md honored: no downgrading of PGS theorems, no probabilistic reframing, PGS objects/invariants first.

**Recommendation from this run:** The signatures are valuable as a deterministic structural-certificate layer for any future nominated holes (e.g., for PROOF.md-style claims or cross-audit of witness completeness). They did not alter or improve the first-pass nomination on this corpus. If later LWM-BAND-01 or other refinements introduce additional high-support false positives, re-running the identical sidecar logic will immediately yield comparable vectors for true vs. false.

---

## Detailed Signature Vector Definition (PGS-Native, Deterministic)

For each supported offset (hole):
- Collect distinct public heldout composites whose factors intersect the supporting r threads for that offset. These are the "witness composites" generating the coverage.
- GWR on public data: global_min_d = min divisor_count over all heldout; leftmost_gwr_offset = min-offset among those achieving it.
- DNI: E(c) = (d(c)/2 − 1) × ln(c) for each witness c.
- Coverage signature (emitted as "coverage_signature" + compact "signature_vector"):
  - support (cardinality, for reference)
  - num_witness_composites
  - num_gwr_min_witnesses (count of witnesses with d == global_min_d)
  - has_leftmost_gwr (boolean: does the global leftmost min-d composite contribute a thread to this offset?)
  - avg_dni_excess, min_dni_excess over the witnesses
  - signature_vector = [support, num_witnesses, num_gwr_mins, has_leftmost(0/1), avg_E, min_E]

All values derived from public rows only. Reproducible.

---

## Toy Cases — Signature Table for True High-Support Points

(All emitted max-support holes were true; 0 false at ≥2 support.)

| case       | true offset | support | audit     | sig_vector                          | has_gwr | num_gwr_min_wit | avg_E     | min_E    | witnesses |
|------------|-------------|---------|-----------|-------------------------------------|---------|-----------------|-----------|----------|-----------|
| toy_23x31  | -23        | 3      | p_thread | [3, 36, 10, 1, 23.633213, 6.532334] | True   | 10             | 23.633213 | 6.532334 | 36       |
| toy_43x59  | 43         | 3      | p_thread | [3, 72, 15, 1, 34.456568, 7.818832] | True   | 15             | 34.456568 | 7.818832 | 72       |
| toy_61x83  | 61         | 3      | p_thread | [3, 101, 0, 0, 43.321908, 8.517393] | False  | 0              | 43.321908 | 8.517393 | 101      |
| toy_89x113 | 89         | 3      | p_thread | [3, 135, 22, 1, 51.712202, 9.206031]| True   | 22             | 51.712202 | 9.206031 | 135      |

**Observation:** True points exhibit varying GWR participation (0 to 22 min-d witnesses) and clean min_E values anchored near the global leftmost GWR excess. No false comparators at this support tier.

---

## Ladder Sample — True High-Support Signature Vectors (No False Counterparts)

| rung            | N          | max_supp | emitted | example true offsets (sig excerpts) |
|-----------------|------------|----------|---------|-------------------------------------|
| rung_01_43x59  | 2537      | 3       | 2      | +43: [3,363,71,1,35.45,7.73] has_gwr=True; -59: [3,354,68,1,35.92,7.73] has_gwr=True |
| rung_04_101x137| 13837     | 3       | 5      | +101: [3,811,126,0,55.48,9.49] has=False; +137: [3,818,126,0,55.25,9.49] has=False; +303: [3,784,126,1,56.11,9.49] has=True |
| rung_18_8009x10007 | 80146063 | 5     | 1      | +24027: [5,68444,0,0,204.65,18.20] has=False (large-N scaling: high witness count, zero GWR-min overlap in this instance) |

Across 19 ladder rungs: emitted counts 1–8, always composed exclusively of p_thread / q_thread audit kinds. false_high column remained 0 even when min_support_for_table reached 4 (for max_supp=5 cases).

---

## Interpretation (Outcome-First)

The literal web's raw thread support already performs the "nomination" work with no observed false positives intruding at high cardinality in the tested public windows. Adding the GWR/DNI witness-completeness signatures as sidecar did not change any emitted sets and supplied no extra filtering opportunity on this corpus.

However, the signatures constitute clean, contract-compliant structural certificate data:
- They precisely quantify how the supporting public threads are "covered" by the extremal (GWR) and normalized (DNI) properties of the very composites that made those threads visible.
- For every true recovery, one can now cite the exact vector (and the witness_offsets list) as part of a deterministic public proof artifact.
- This directly fulfills the "witness completeness" mapping from the Japanese line geometry plan (secondary experiment 3/4) without violating any guardrails.

No regression vs. baseline. No improvement to first-pass ranking observed (none was possible). Valuable certificate layer produced.

---

## Full Reproduction

```bash
cd .../japanese-thread-mapping-plan/LWM-WITNESS-01
python3 lwm_witness_01.py
# Artifacts land in ./output/ (public only)
```

All logic inside the isolated dir. SHA256 of runner + outputs can be computed from the frozen files for tamper evidence.

**End of findings.**