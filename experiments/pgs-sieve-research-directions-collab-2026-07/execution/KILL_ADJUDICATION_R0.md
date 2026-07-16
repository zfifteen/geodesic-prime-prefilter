# Kill adjudication — D1 R0 measured

**Author:** claude  
**Date:** 2026-07-15  
**Status language:** measured on R0 only (`p ≤ 10^6`). Not verified. Not theorem.  
**Inputs:** `ANALYSIS_R0_p_le_1e6.json`, `LEAD_MEASURED_NOTE.md`, `KILL_SHAPES.md`  
**Epoch:** pgs-sieve-execution-2026-07

---

## What we are adjudicating

K1-a through K1-e from KILL_SHAPES.md applied to the 78,498-row R0 measured run. Each shape gets a verdict: **PASS** (shape did not fire), **REDESIGN** (shape fired; direction survives with changes), or **KILL** (direction is not salvageable as stated).

---

## K1-a — No compression signal across H bands

**Shape:** Compression ratios for gap ≤ 246 are statistically indistinguishable from randomly sampled gaps of similar width.

Measured numbers (from ANALYSIS_R0_p_le_1e6.json):

- small_gap (≤p25, n=29,555): compression_mean 0.0244, offset_mean 1.987
- mid_gap (n=27,108): compression_mean 0.0452, offset_mean 3.733
- large_gap (≥p75, n=21,835): compression_mean 0.0484, offset_mean 4.013
- gap ≥ 50 (n=724): compression_mean 0.0487, offset_mean 4.206

**Assessment:** There is a real monotone gradient — compression mean goes from 0.024 in the small-gap quartile to 0.048 in the large-gap quartile (roughly 2× ratio); offset mean moves from ~2.0 to ~4.0. The direction has signal. However, the H-band framing is vacuous at R0: max gap is 114, so every row satisfies H=246 and H=1000. H-band contrast cannot be tested because there are no rows outside H=246. The signal is continuous gap-width signal within the envelope — which is a different (and stronger) finding than the original atlas framing.

**Verdict: PASS on compression-signal existence; REDESIGN triggered on H-band framing (see K1-b).** The direction has empirical content. The H-threshold atlas contract as written cannot execute at R0.

---

## K1-b — H boundary is artificial for interior structure

**Shape:** Witness offsets vary continuously with gap width; sharp H cutoffs (246, 600) do not carve coherent regimes.

Measured numbers:

- gap ≤ 20 (n=64,939): offset_mean 2.97, offset=1 rate 23.2%
- gap ≤ 30 (n=74,116): offset_mean 3.10, offset=1 rate 21.1%
- gap ≥ 50 (n=724): offset_mean 4.21, offset=1 rate 5.5%
- gap ≥ 80 (n=31): offset_mean 4.42, offset=1 rate 3.2%

**Assessment:** Interior geometry evolves monotonically with gap width with no visible cliff at any threshold. At R0, H=246 includes 100% of rows — it carves nothing. The data points to raw gap width as the correct primary axis, not H membership.

**Verdict: REDESIGN — this shape fires.**

Revised live D1 success criterion for execution:

> Measure GWR interior geometry (offset, compression, endpoint-adjacency) stratified by continuous gap width (raw q−p) within regime R, using log-bin gap percentile cohorts (small ≤p25, mid, large ≥p75) as the primary comparison axis. H=246/600/1000 values are retained as historical labels only — not used as the primary stratification axis.

The direction is not killed. The restructured question — does interior geometry vary continuously with gap width and how does it compress? — is well-posed, cleanly PGS-first, and has a real measured answer already at R0.

---

## K1-c — Compression bound saturates at floor constant

**Shape:** The UBC floor (max(64, ⌈0.5·(log q)²⌉)) constant-floor term dominates for all q in R0; compression ratio carries no H-specific signal because the theorem trivially explains it.

**Assessment:** For p ≤ 10^6, log(p) ≈ 6–14; 0.5·(log q)² ≈ 18–98. The constant floor 64 dominates for most of the range. Measured compression ratios are small (mean 0.038, median 0.031); the UBC bound is satisfied trivially for almost all rows regardless of gap structure. The LEAD_MEASURED_NOTE explicitly calls this out: "Compression ratios are tiny vs UBC floor 64 (floor dominates at this magnitude) — K1-c relevant."

**Verdict: REDESIGN — K1-c fires as an interpretation constraint.** The compression column is valid for measuring relative geometry within gaps, but the claim "bounded-gap compression is PGS-predicted tighter than typical gaps" is not testable at R0 because the floor dominates across the board. To get past K1-c, the run needs p large enough that the log² term competes with the floor — practically R1 (p ≤ 10^7) at minimum for the larger gaps. The offset geometry signal is independent of this and remains valid at R0.

---

## K1-d — Interior empty for dominant fraction of small bounded gaps

**Shape:** Twin prime degeneracy dominates the H≤246 sample; atlas is mostly degenerate empty-interior entries.

**Measured numbers:**

- empty_interior_n = 1 out of 78,498 (rate 0.0013%)
- small_gap cohort: empty_interior_n = 1, rate 3.4e-5
- large_gap cohort: empty_interior_n = 0

**Assessment:** The empty interior problem is essentially absent at R0. One row is empty across all 78,498. K1-d does not fire.

**Verdict: PASS.**

---

## K1-e — GWR witness collapses to endpoint-adjacent

**Shape:** Interior structure collapses to endpoint-adjacent for most small bounded gaps; the atlas is measuring endpoint proximity, not free interior phenomenon.

Measured numbers:

| Cohort | offset=1 rate | offset=gap-1 rate |
|---|---|---|
| small_gap (≤p25) | 44.2% | 37.0% |
| mid_gap | 6.3% | 0.6% |
| large_gap (≥p75) | 5.2% | 0.0% |
| all with witness | 20.3% | — |

**Assessment:** K1-e fires within the small-gap cohort (44% left-adjacent, 37% right-adjacent — together effectively the entire small-gap cohort is endpoint-concentrated). This drops sharply for mid and large gaps. The endpoint concentration is genuine interior structure in a low-degrees-of-freedom setting (gap=4 has only positions p+1,p+2,p+3), not a design flaw. But it needs explicit layering.

**Verdict: REDESIGN (partial) — K1-e fires for small-gap cohort.** Recommended change: stratify small-gap rows into three sub-classes — left-endpoint-adjacent (offset=1), right-endpoint-adjacent (offset=gap−1), genuine interior (offset strictly between 1 and gap−1). This is the recovery path as written in KILL_SHAPES: "separate endpoint-touching hits from genuine interior witnesses."

---

## Summary adjudication table

| Kill shape | Verdict | Action |
|---|---|---|
| K1-a: No compression signal | PASS | Signal exists; H-band framing needs redesign (K1-b) |
| K1-b: H boundary artificial | REDESIGN | Success criterion → continuous gap-width stratification |
| K1-c: UBC floor dominates | REDESIGN | Interpretation constraint; compression claims need R1+ |
| K1-d: Interior mostly empty | PASS | Empty rate ~0.001%; non-issue |
| K1-e: Witness endpoint-adjacent | REDESIGN (partial) | Add left/right/interior sub-classification for small-gap cohort |

No kill verdicts. Direction survives with three redesigns, all recoverable within the PGS-first frame.

---

## D2 pilot — defer with concrete blocker

K1-b and K1-c firing together create a prerequisite gap. D2 (constellation-anchor vs. control interior comparison) requires gap-width-matched controls (the K2-b confound). Until D1 has a working continuous gap-width stratification protocol — specifically until D1 R1 establishes the reclass methodology at scale where some constellation anchors will have larger gaps — D2 cannot execute gap-width-matched controls correctly.

Running D2 at R0 would produce a confounded comparison: constellation anchors (especially twin-prime anchors) automatically have small gaps; any interior difference would be indistinguishable from the K1-b gap-width effect.

**D2 is deferred until D1 R1 (p ≤ 10^7) establishes a continuous gap-width stratification protocol.** At that point D2 imports the control design directly. This is a concrete blocker, not a soft skip.

---

## D3 and D5 — one sentence each

**D3:** Defer — K3-d fires before any run: the sieve weight comparison object ("sieve weight for a prime p") is not stably defined without choosing a variant (Selberg vs. Bombieri–Vinogradov) in ways that can change the correlation sign, so there is nothing well-posed to measure against yet.

**D5:** Defer — D1 is still in redesign (K1-b/K1-c); D5 uses similar modular-residual machinery and the wait rule applies: do not layer D5 until D1 R1 is clean.

---

*STATUS: done*  
*FOR: @grok*  
*EPOCH: pgs-sieve-execution-2026-07*
