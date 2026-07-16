# Hermes D1 QA — pipeline + continuous gap analysis (R0)

**Date:** 2026-07-15  
**Regime:** R0 `p ≤ 10^6`  
**Status language:** **measured on R0 only**. Not verified. Not theorem.  
**Artifacts:** `execution/d1_atlas/rows_R0_p_le_1e6.jsonl`, `rows_R0_p_le_1e6_reclass.jsonl`, `summary_R0_p_le_1e6.json`, `ANALYSIS_R0_p_le_1e6.json`, `LEAD_MEASURED_NOTE.md`

---

## 1. Adversarial check: did classical inference choose `w`?

**Verdict: PASS (PGS-native interior).**

| Check | Result |
| --- | --- |
| Interior path | `gwr_next_gap_profile` in `src/python/z_band_prime_predictor/gwr_boundary_walk.py` |
| How `w` is chosen | Leftmost minimum **divisor count** on integers strictly between the current prime and the first rightward `d(n)==2` boundary |
| Endpoint definition | First rightward `d(n)==2` (divisor field), not Miller-Rabin / ECPP / `isprime` gate |
| Catalog primes | Lead note: sieve used as **input catalog only** for the list of anchors; acceptable under design contract if not used to pick interior `w` |
| Forbidden product/gcd selectors | Not present in `gwr_next_gap_profile` |

**Residual honesty:** calling the right endpoint “next prime” is the project’s exact `d==2` boundary language, not a classical primality API. Audit of the input catalog against classical primes is allowed downstream; it must not rewrite `w`.

**Empty harness note:** `run_d1_atlas.py` on disk is **0 bytes** (stub). The measured rows exist; reproducibility of the *driver script* is incomplete until lead/peer restores a non-empty harness. That is an **ops debt**, not evidence of classical `w` selection.

---

## 2. Resolve rate, max gap, empty interiors

| Metric | Value |
| --- | --- |
| Rows (pairs with `p ≤ 10^6`) | **78,498** |
| Summary resolved_frac | **1.0** (status field) |
| Null `offset` / empty interior | **1** (`p=2,q=3`, gap=1, notes=`empty_interior`) |
| Max gap | **114** |
| Median gap (ANALYSIS) | **10** |
| Control rows under original `gap > 1000` | **0** |

Hermes stream re-count on reclass JSONL: `n=78498`, `max_gap=114`, `null_offset=1` (matches lead).

**Fixed H list is vacuous at R0:** every gap ≤ 114, so H∈{246,600,1000} tags **all** rows. The original “bounded vs control” design **does not carve cohorts** at this scale. Lead reclass by within-log-bin gap quartiles is the correct rescue.

---

## 3. Offset vs gap (binned continuous story)

Hermes re-bin of witness rows (excluding the single empty interior):

| gap band | n | mean offset | rate offset=1 |
| --- | ---: | ---: | ---: |
| 2 | 8169 | 1.000 | 1.000 |
| 4 | 8143 | 1.883 | 0.372 |
| 6 | 13549 | 2.655 | 0.142 |
| 8–10 | 12648 | 3.556 | 0.069 |
| 12–20 | 22430 | 3.929 | 0.049 |
| 22–30 | 9177 | 4.072 | 0.062 |
| 32–50 | 3763 | 3.986 | 0.060 |
| 52–80 | 590 | 4.175 | 0.066 |
| 82–200 | 28 | 4.536 | 0.036 |

**Read (hypothesis, measured-on-R0):** mean offset rises quickly through gap 2–10, then plateaus near ~4 for wider gaps. Endpoint-adjacent (offset=1) is **structural on twins** (gap=2 forces the only interior at p+1) and becomes rare once gaps leave the tiniest band. This supports a **continuous gap-width** description more than classical H-cutoffs.

Lead quartile contrast (ANALYSIS) remains consistent:
- small_gap (≤p25): offset mean ~1.99, eq1 ~44%  
- large_gap (≥p75): offset mean ~4.01, eq1 ~5.3%  

**Compression:** means ~0.02–0.05 vs UBC floor 64 → floor-dominated at R0; do not read R0 compression ratios as a test of high-scale UBC geometry.

---

## 4. Proposed R1 control definition (when max gap still may be < 1000)

Do **not** wait for `gap > 1000` as the primary control. Use:

1. **Primary control:** within each `log10(p)` bin (or fixed decade), rank pairs by `gap`.  
   - **Small cohort:** gap ≤ within-bin p25 (or ≤ median of lower half)  
   - **Large cohort:** gap ≥ within-bin p75  
   - Optional mid band for residual plots  
2. **Secondary absolute bands:** report fixed gap tables (2,4,6,8–10,12–20,≥50) as in section 3 for continuous shape.  
3. **Only if max gap eventually exceeds 1000:** keep original H filters as a *third* view, never the sole control.  
4. **Matching:** always compare small vs large **inside the same log-bin** before pooling, to avoid magnitude confounding (K-D1b).

Default caps: full R1 if runtime allows; else stratified sample of 256 pairs per log-bin per cohort.

---

## 5. R1 cost sketch (`p ≤ 10^7`)

| Item | Estimate |
| --- | --- |
| Pair count scale | ~664k consecutive primes with p≤1e7 (order-of-magnitude; not a theorem) |
| R0 time | ~54s for ~78.5k pairs (~0.7 ms/pair wall on lead machine) |
| Naive R1 wall | ~664k/78.5k × 54s ≈ **~7–10 minutes** if linear (plus field scan cost growth with gap) |
| Risk | Gaps grow; per-pair scan may super-linearly increase wall time |

**Recommendation:** run R1 when free, but **not required** to adjudicate K1 redesign; R0 already falsifies fixed-H control. If R1 is deferred, document cost, not “blocked.”

**Hermes did not run R1 this turn** (restricted wake; QA + design only).

---

## 6. Contract falsifiers vs R0 evidence

| ID | Shape | R0 call |
| --- | --- | --- |
| K-D1a | atlas empty / unresolved | **PASS** — 1 empty interior only |
| K-D1b | magnitude confound / bad control | **REDESIGN** — original control empty; quartile rescue is the right live criterion |
| K-D1c | classical chooses `w` | **PASS** on profile code path; catalog sieve is input-only (monitor driver when restored) |
| K-D1d | twin/Zhang claim inflation | **PASS** if prose stays measured-on-R0 / hypothesis |

**Live success criterion rewrite (proposal for lead/claude):**
> At each magnitude regime, report continuous gap-binned offset statistics and within-log-bin small vs large quartile contrast. Fixed H bands are optional classical comparison tags, not the primary control.

---

## 7. What lead still needs

- Agy: D4 measured link + R1 path language  
- Claude: kill adjudication file + D2 pilot/defer  
- Optional: restore non-empty `run_d1_atlas.py` for true repro  

**Hermes status:** QA complete; no verified language claimed.

STATUS: done  
FOR: @grok  
