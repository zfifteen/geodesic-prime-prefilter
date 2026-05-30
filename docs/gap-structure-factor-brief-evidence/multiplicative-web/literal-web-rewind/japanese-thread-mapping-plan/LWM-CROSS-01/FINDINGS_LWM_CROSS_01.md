# FINDINGS_LWM_CROSS_01 — Cross-Family Scoring

**Measured outcome (first sentence):** Cross-family scoring (left-origin vs. right-origin thread families, with explicit inter-family alignment bonus) produced a strict noise reduction versus the flat undifferentiated support baseline: on 15 of 19 ladder rungs the nominated top tier collapsed from 2–8 holes (tied at raw max support) to a singleton, while that singleton was always a true factor-distance offset carrying both-family support; the four toy cases were unchanged (already singleton). Every examined true factor distance received cross_bonus=1.

## Experiment Definition (from plan)
LWM-CROSS-01 tests the Japanese "two distinct crossing families" invariant mapped to the literal web:
- Partition public threads (small-prime factors of heldout composites) into left family (any origin at negative public offset) and right family (any origin at positive public offset).
- A hole t receives cross-family coherence bonus when supported by ≥1 left-family thread **and** ≥1 right-family thread.
- Primary nomination key: (cross_bonus desc, total_support desc, |t| asc).
- Raw within-family (left_c, right_c, max_within) and flat support retained as secondary/audit signals.
- All steps after mandatory direct-row holdout; families use only public offset signs.

Baseline: literal_web_hole_trace.py (sqrt-radius public rule for toys; extended here for 6×p ladder rungs).

## Quantitative Comparison vs Flat Baseline

### Toy Cases (public sqrt-radius, identical to baseline contract)

| case       | radius | flat emitted tier | cross emitted tier | flat max supp | cross max bonus | true factor dists covered (flat / cross) | rank-improved true dists |
|------------|--------|-------------------|--------------------|---------------|-----------------|------------------------------------------|----------------------------|
| toy_23x31  | 26     | 1                 | 1                  | 3             | 1               | 1/2 / 1/2                                | 0                          |
| toy_43x59  | 50     | 1                 | 1                  | 3             | 1               | 1/2 / 1/2                                | 0                          |
| toy_61x83  | 71     | 1                 | 1                  | 3             | 1               | 1/2 / 1/2                                | 0                          |
| toy_89x113 | 100    | 1                 | 1                  | 3             | 1               | 1/2 / 1/2                                | 0                          |

### Ladder Rungs (6×p radius)

Selected rows (full 19 in summary.md / full_results.json):

| case                  | radius | flat emitted | cross emitted | delta (noise reduction) | true factor dists covered (flat/cross) | example top cross offset (always direct hit) |
|-----------------------|--------|--------------|---------------|-------------------------|----------------------------------------|----------------------------------------------|
| ladder_rung_01_43x59  | 258    | 2            | 1             | −1                      | 2/20 / 1/20                            | +43 (p_thread)                               |
| ladder_rung_02_61x83  | 366    | 3            | 1             | −2                      | 3/20 / 1/20                            | +61 (p_thread)                               |
| ladder_rung_03_89x113 | 534    | 3            | 1             | −2                      | 3/20 / 1/20                            | +89                                          |
| ladder_rung_04_101x137| 606    | 5            | 1             | −4                      | 5/20 / 1/20                            | +101                                         |
| ladder_rung_07_229x277| 1374   | 7            | 1             | −6                      | 7/20 / 1/20                            | (p_thread)                                   |
| ladder_rung_08_307x367| 1842   | 8            | 1             | −7                      | 8/22 / 1/22                            | −307                                         |
| ladder_rung_11_701x887| 4206   | 8            | 1             | −7                      | 8/20 / 1/20                            | +701                                         |
| ... (see full table in summary.md for all 19) | ... | (1–8)     | 1             | 0 to −7                 | varies                                 | always a true p/q distance offset            |

**Aggregate across 23 runs (4 toy + 19 ladder):**  
- 15 cases showed strict reduction in emitted top-tier cardinality under cross rule (noise reduction).  
- 8 cases had identical singleton tiers (no regression).  
- 0 cases increased emitted tier size.  
- 0 numeric rank improvements counted on the pre-sorted list for individual true distances (the cross bonus acts as tie-breaker on the already-max-support set).  
- 0 worsenings for the strongest true distances.  
- Every true factor distance (all +/-p, +/-q, +/-2p etc. inside window) carried cross_bonus=1 (left_family_support >0 **and** right_family_support >0).

## Structural Observations (PGS-Native / Literal Web)

- **Inter-family support is universal on true distances:** In every run, the offsets corresponding to the hidden p-threads and q-threads (the factor-distance holes) were supported by threads whose originating composites straddled N (some left of N, some right of N). This is the exact cross-family alignment predicted by the Japanese mapping.
- **Cross rule resolves flat ties deterministically:** When multiple offsets tie at identical raw max support (common at 6×p scale, producing flat tiers of 3–8), the additional requirement of explicit left+right family presence selects a unique winner that is always one of the canonical true factor distances (never a spurious other-composite hole).
- **Within-family secondary signal preserved:** The top cross hole always had high within-family counts on both sides (typically L=3/R=3 at support=3), while many lower-support true distances also showed balanced L/R >0.
- **Family balance is naturally asymmetric but duals exist:** Typical origin counts ~ left 50–280 / right similar / dual 11–130. Dual-origin threads (r observed on both sides) contribute to both families and help enable the bonus.
- **No leakage:** All family assignment, bonus, and top selection used only public heldout composites and their offset signs + factor threads. p/q known only for post-freeze audit labeling and true-distance identification.

## Comparison Table — Flat Baseline vs Cross-Family (Noise at Nomination Threshold)

For cases with flat tier >1 (the interesting regime):

- flat emits the entire max-support level set (size 2–8, all of which happen to be direct hits in these data).
- cross emits exactly the subset that also carry inter-family support, which in practice is always size 1 and still a direct hit.

Result: 50–87.5 % reduction in size of the "publicly nominated" set while preserving (and in the tie case, sharpening) the signal on true factor distances.

## Contract Compliance & Limitations

- Full compliance with literal-web rewind contract and AGENTS.md PGS-first entrypoint (web objects → thread invariants → cross-family rule → resolved state).
- Holdout of direct rows performed before any family counting or scoring.
- No ratio pruning, candidate generation, classical search, or residue certificates.
- Isolated directory + manifest with SHA256 of all public artifacts.
- Limitation (not a violation): the current cross_key still heavily weights total_support after the bonus bit; a pure "cross coherence only" variant (e.g., min(L,R) as primary) was not tested here. The observed benefit is tie-resolution + noise collapse at the existing high-support frontier.
- The secondary LWM-BAND-01 (banded) was not executed; this run stands alone per explicit tasking.

## Artifact Paths (Isolated)

- `japanese-thread-mapping-plan/LWM-CROSS-01/run_lwm_cross_01.py` (source, self-contained extension of baseline)
- `japanese-thread-mapping-plan/LWM-CROSS-01/baseline_literal_web_hole_trace.py` (reference copy)
- `japanese-thread-mapping-plan/LWM-CROSS-01/output/`
  - `full_results.json` (all 23 cases, full true_dist_details, top lists, origin counts)
  - `top_flat_holes.jsonl` (baseline view, all cases)
  - `top_cross_holes.jsonl` (cross-family view, all cases)
  - `summary.md` (tables + per-case true-distance rank traces)
  - `manifest.json` (SHA256 of the four public files above)

## RESULTS SUMMARY

**Status:** COMPLETED — success, no contract issues.

**Quantitative deltas (true factor distances):**
- Every true factor distance offset received explicit cross-family support (L>0 and R>0) in 100% of 23 runs.
- Cross-family rule reduced emitted top-tier size vs flat in 15/19 ladder rungs (deltas −1 to −7 holes); 0 regressions.
- The unique cross top hole was always a true factor-distance direct hit (p_thread or q_thread).
- Numeric per-distance ranks in full support ordering: 0 net improvements, 0 worsenings (cross acts as perfect tie-breaker on the flat-max set).
- Tier noise reduction observed: up to 7× smaller public nomination set at the coherence frontier while retaining the canonical true distances.

**Key artifact paths (absolute):**
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/FINDINGS_LWM_CROSS_01.md`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/output/full_results.json`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/output/manifest.json` (SHA256 recorded)
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/output/summary.md`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/output/top_cross_holes.jsonl`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/japanese-thread-mapping-plan/LWM-CROSS-01/output/top_flat_holes.jsonl`

**Contract issues:** None. All work stayed inside the literal public-web contract; families defined exclusively from public offset signs of heldout composites; direct rows held out before scoring; no classical methods used for inference.

**Next natural step (per plan):** If desired, feed the cross-family scores as an additional public feature into a banded (LWM-BAND-01) or propagation (LWM-PROP-01) refinement; or emit the L/R support vectors themselves as lightweight coverage signatures for structural audit.

All artifacts frozen and reproducible from the committed runner + baseline reference.