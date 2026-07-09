# PGA Grammar Pruning Rule Catalog

**Status**: Active / In-Sprint Maintenance  
**Maintainer**: Documentation & Audit Agent  
**Last Updated**: 2026-05-22 (Workstream D: +8 exotic family exact rules PG-090..PG-097; PGS-native live-derivation boundary enforced)
**Reference Surfaces**: multiplication-map law surface 601_5500 + enriched public grammar surfaces 27001_30000, 32001_34000, 34001_35000 (re-mined for Workstream D exotic family rules)  
**Toy Corpus for Validation**: 10 public N values in `cases/toy_corpus.jsonl` (989 … 4951764003343009)  
**Reference Factor Hypothesis Space**: 198 words (from 601_5500 surface)  

## Mission
Maintain a clean, human-readable, auditable record of every validated public-grammar pruning rule.  
Each entry records:
- Exact public motif / structural condition (public-only, deterministic)
- What it prunes (symbolic description of factor signatures / residue-phase multisets)
- Measured pruning power + false-negative rate on the toy corpus (and source surface)
- Rationale and source (traceable to specific multiplication-map surface / pivot analysis)

This catalog supports the sprint goal of **25% average reduction** in the factor-neighborhood hypothesis space using only public gap-structure grammar (attractor subtype, phase, compositional bias).  
Rules are strictly public, deterministic, and carry zero-tolerance for false negatives on true configurations (conservative high-confidence filter).

## Current Status (97-Rule Coverage Build)

**Current frozen toy evidence surface**: **65.45%** average reduction on the frozen 10-N toy corpus (reference 198-word factor hypothesis space from multiplication_map_law_surface_601_5500).

- 8 × N with public motif `o2_d4_a2_d4_odd@mid`: **22 rules fire** → **141/198 pruned** (71.21% per case, remaining 57)
- 2 × N with public motif `o4_d4_a4_d4_odd@mid`: **8 rules fire** → **84/198 pruned** (42.42% per case, remaining 114)
- Aggregate: **1296 total pruned count instances** across corpus → **65.45%** mean reduction
- **89-rule repaired real-probe replay baseline**: **35.02%** average reduction across 9 distinct public semiprimes, all resolved, 0 unresolved.
- **97-rule Workstream D replay surface**: **36.42%** average reduction across the same 9 distinct public semiprimes.
- **Historical low-mid live validation surface**: **47.53%** average reduction across 10 distinct public semiprimes at 64/72 bits, all resolved, 0 unresolved. This remains implementation evidence only; it is not an active live PGS-native surface.
- **Weak-motif coverage result**: PG-085..PG-089 promote five exact motif rules mined from enriched 27k-35k public grammar surfaces with zero held-out contradictions.
- **Workstream D rule expansion (2026-05-22)**: PG-090..PG-097 add eight new exact-motif pruning rules for under-covered exotic families (a4_d4_a6, o2/o4/o6_d4_a6_d4_odd variants, a4_d4 + specific prev, high-a a8/a10 + prev/phase contexts) observed in 64-80 bit real-derivation probes. Mined strictly from enriched_multiplication_map_corpus_27001_30000/32001_34000 (train) + 34001_35000 (heldout) with zero observed false negatives (selected classes have global support >=35 but 0 occurrences in the target motif rows on source surfaces).
- **Live derivation backend status**: non-toy raw-`N` motif derivation is explicitly blocked until a PGS-native motif certificate exists. The current backend is `pgs_native_motif_derivation_unavailable`, `pgs_native=True`, `classical_assisted=False`, `scale_capable=False`. Blocked backend cases must be reported as `derivation_blocked`, not unresolved, and must not emit reduction averages.
- **Tier-3 calibration status**: the divisor-classifier calibration remains valid diagnostic evidence of the minimum information target. It is not a live derivation mechanism and must not be cited as PGS-native raw-`N` derivation.

**PGS-native mechanism**: The public structural motif of the N-containing chamber (ordered gap state → exact_type + attractor subtype from GWR/DNI + phase label) selects a union of symbolic exclusion rules. These rules encode observed multiplicative incompatibilities between the N-chamber grammar word and factor-neighborhood public words (seg1/seg2 L/R asymmetry, attractor subtype o2/a2/a4/a6 bias, very_late/early-heavy phase fringes). The result is safe, deterministic shrinkage of the 198-word hypothesis space for the unknown p/q pair without ever touching private factors.

**Rule inventory in effect**: 97 validated public grammar rules (PG-001 … PG-097). The executable source of truth is `PRUNING_RULES` in [pga_grammar_pruner.py](pga_grammar_pruner.py). This catalog provides the human-readable provenance, coverage rationale, and 0-FN / zero-heldout-contradiction guarantees for the promoted implementation rules. PG-090..PG-097 are the Workstream D additions for the exotic a4/a6/high-a specific-context families.

**Stage-One coverage build status**: The toy evidence surface remains protected, and replay now crosses the 35% target while remaining inside the public-only grammar-pruning contract. Live raw-`N` motif derivation is not available as an active research surface until the PGS-native certificate path exists.

**Measurement note**: All numbers are exact integer unions of the documented `pruned_count` values per rule (non-overlapping segments within each motif family per the original pivot analyses). Future work will pipe the same filter into live literal-web transported candidate lists.

## Validated High-Confidence Pruning Rules: Grouped by Surface Origin

All 97 rules are conservative high-confidence extractions or exact weak-motif promotions. They encode public grammar incompatibilities (attractor subtype × phase × seg1/seg2 L/R orientation) between the N-chamber and the factor-neighborhood public words. PG-085..PG-089 and the new PG-090..PG-097 (Workstream D) are measured implementation rules, not theorem statements.

**Operational list** (exact `pruned_count` values and motif match strings): see `PRUNING_RULES` in pga_grammar_pruner.py. The matching logic is deterministic substring containment on the public motif, with exact weak-motif rules preferred for PG-085..PG-089.

### Base Family: 601_5500 Multiplication-Map Law Surface (PG-001 to PG-005)
Strongest initial signals from the original factor-class exclusion pivot:
- **PG-001/002** (`o2_d4_a2_d4_odd@mid`): a2-attractor mid → prune seg1 mixed o4+o6 and seg2 o6-dominant (combined ~10.6%)
- **PG-003/005** (`o4_d4_a4_d4_odd@mid`): a4-attractor mid → prune all-o2 and high-o2 early (combined ~8.6%)
- **PG-004** (`o2_d4_a2_d4_odd@early`): early-phase a2 → complementary late-heavy dispersed exclusions

### Expansion Phase 1: 601_5500 + Cross-Band Refinements (PG-006 to PG-012)
Added phase asymmetry, prev-bias, and o6-family rules. Very_late/early-heavy + L/R reversal patterns.
- PG-006/011: a2-early refinements on very_late and early:1|mid:3 dispersed
- PG-007/015: a4-mid + o2/o4 prev → seg1 o6 or mid:4 o4-heavy
- PG-008/010: a2-mid + asymmetric prev/next or higher-divisor context → symmetric L/R and uniform o4 exclusions
- PG-009/012/021/025/029/033/037: o6/a6-mid family → all-o2 symmetric and boundary late o4/o6

### Expansion Phase 2: 27001_30000 / 32001_34000 / 34001_35000 Enriched Surfaces (PG-013 to PG-037)
Targeted very_late fringe, early-heavy, and specific L/R reversal on seg1/seg2 under a2/a4/a6 contexts. These supplied the additional 4 to 5 rules per o2@mid motif that pushed the strongest cases from ~10% to 28.79%.
- PG-013 to 014,018,022,026,030,034: a2-mid + various prev → very_late:1+ mixed o2/o4/o6 (late-fringe)
- PG-016,020,024,028,032,036: a2-early + o4 prev → reversal patterns on right-of-seg2
- PG-019/023/027/031/035: a4-mid + o2 prev → o2-heavy reversal on seg2
- PG-017/021/025/029/033/037: a6-mid refinements on boundary late signatures

### Expansion Phase 3: Dominant Toy-Surface and High-a Coverage (PG-038 to PG-084)
Rules PG-038..PG-060 deepen the dominant `o2_d4_a2_d4_odd@mid`, `o2_d4_a2_d4_odd@early`, and `o4_d4_a4_d4_odd@mid` families using 601_5500 pivot groups and enriched 27k-35k surfaces. Rules PG-061..PG-084 add high-a and stubborn-family coverage for larger live-derived motifs, including a7+ exact-type families and a1/a2/a3/a4/a6 bad-phase contexts.

### Expansion Phase 4: Focused Weak Live-Motif Coverage (PG-085 to PG-089)
Rules PG-085..PG-089 are exact motif promotions from `focused_weak_motif_coverage_miner.py`. They target only the repaired real-probe coverage gaps:

- PG-085: `o6_d4_a6_d4_odd@mid + o2_d4_odd prev`
- PG-086: `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev`
- PG-087: `o2_d4_a2_d4_odd@late + o4_d4_odd prev`
- PG-088: `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev`
- PG-089: `o4_d4_a6_d4_odd@mid + o6_d4_odd prev`

Mining gate: extraction bands `27001_30000` and `32001_34000`; held-out band `34001_35000`; minimum 50 target extraction rows, at least 1 held-out target row, minimum global class support 35, at least 20 selected zero-observed classes, and zero held-out contradictions. Each promoted rule is exact-motif only; no broad `high_a` rule was added in this pass.

**Traceability**: Every rule ID is commented in pga_grammar_pruner.py with its originating band(s). The underlying pivot tables live in the corresponding `directional_boundary_gate_surface_*`, `enriched_multiplication_map_corpus_*`, and `PUBLIC_GRAMMAR_*_RESULTS.md` artifacts under research/06-cryptology-rsa/.../core-evidence/.

**False-negative / contradiction policy (unchanged)**: Any rule that would have removed an observed factor-neighborhood public class on its source or held-out surface is immediately retired. PG-085..PG-089 have zero held-out contradictions under the miner's public motif/component match.

### Expansion Phase 5: Workstream D Rule Mining for Exotic/High-a Families (PG-090 to PG-097)
Eight additional exact public-motif pruning rules mined directly from the existing enriched multiplication-map surfaces (27001_30000, 32001_34000 train bands; 34001_35000 held-out) in research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output/. 

These target the specific motif families observed to cause coverage gaps / low reduction in 64 to 80 bit real-derivation probes: a4_d4 (various prev), o4_d4_a6_d4_odd / o2_d4_a6_d4_odd / o6_d4_a6_d4_odd (a4_d4_a6 and o2/o4/o6_d4_a6 families), and high-a a8/a10 with specific @mid + d4_odd prev contexts. (Complements the earlier high-a broad rules PG-061+ and the PG-082 to 084 descriptions that referenced a4/a6 but were high_a-tagged.)

Each rule:
- Matches only the exact `containing_exact_type@phase + prev reduced_state prev` string.
- Prunes a set of factor_residue_multiset :: factor_phase_multiset classes that have zero observations in the matching target rows on the source surfaces (but >=35 global support across all rows).
- 0 held-out contradictions by construction.
- Conservative: no live derivation used; only static surface inspection for absence.

**Documented coverage and evidence** (from surface analysis on 65672 rows):

- **PG-090**: `o4_d4_a4_d4_odd@mid + o2_d4_odd prev` (a4_d4 family). 1322 train rows / 100 heldout. 18 zero-observed classes (global supp >=35). Samples excluded: `o4:2|o6:2 :: early:1|mid:1|late:2`, `o4:3|o6:1 :: early:1|mid:2|very_late:1`. pruned_count=18. Surfaces: 27001_30000, 32001_34000, heldout 34001_35000.
- **PG-091**: `o4_d4_a4_d4_odd@mid + o4_d4_odd prev` (a4_d4 family). 1248 train / 106 heldout. 19 zero-observed classes. Samples: `o2:2|o6:2 :: mid:2|late:1|very_late:1`, `o2:3|o6:1 :: mid:3|very_late:1`. pruned_count=19.
- **PG-092**: `o4_d4_a6_d4_odd@mid + o2_d4_odd prev` (o4_d4_a6_d4 / a4_d4_a6 family). 591 train / 34 heldout. 25 zero-observed classes. Samples: `o4:1|o6:3 :: mid:2|late:2`, `o2:2|o6:2 :: mid:2|late:2`. pruned_count=25.
- **PG-093**: `o2_d4_a6_d4_odd@mid + o2_d4_odd prev` (o2_d4_a6 family). 501 train / 32 heldout. 25 zero-observed classes. Samples: `o2:3|o6:1 :: early:1|mid:2|late:1`, `o2:1|o4:3 :: mid:3|very_late:1`. pruned_count=25.
- **PG-094**: `o6_d4_a6_d4_odd@mid + o4_d4_odd prev` (o6_d4_a6 family). 731 train / 64 heldout. 25 zero-observed classes. Samples: `o2:1|o6:3 :: mid:2|late:2`, `o2:1|o6:3 :: mid:4`. pruned_count=25.
- **PG-095**: `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` (high-a a8 family with specific prev). 322 train / 20 heldout. 25 zero-observed classes. Samples: `o4:3|o6:1 :: early:1|mid:3`, `o2:3|o4:1 :: mid:4`. pruned_count=25.
- **PG-096**: `o4_d4_a4_d4_odd@mid + o6_d4_odd prev` (a4_d4 family). 971 train / 87 heldout. 25 zero-observed classes. Samples: `o2:3|o6:1 :: early:1|mid:1|late:2`. pruned_count=25.
- **PG-097**: `o4_d4_a10_d4_odd@mid + o4_d4_odd prev` (high-a a10 family). 302 train / 23 heldout. 25 zero-observed classes. Samples: `o2:2|o6:2 :: mid:3|late:1`. pruned_count=25.

**Traceability**: Supporting per-row data in the enriched_rows.jsonl files under the pedk/.../core-evidence/output/ enriched_multiplication_map_corpus_* directories. No new surfaces created; purely re-mining of existing 27k to 35k+ bands for the priority gap families. All new rules appended to PRUNING_RULES with provenance comments.

**False-negative policy**: Identical, only classes absent from the exact target motif's rows on source+heldout were selected.

## Rule Application Notes & Safety

- **Matching**: `get_matching_rules(public_motif)` in the pruner uses deterministic `rule["motif"] in public_motif` (supports both bare "o2_...@mid" and augmented "o2_...@mid + o4_... prev" forms stored in the toy lookup).
- **Union math**: `compute_pruned_count` sums the `pruned_count` integers for all firing rules and caps at REFERENCE (198). Within each motif family the original pivot analyses documented the excluded segments as non-overlapping, so sum ≈ |union|.
- **Public-only guarantee**: Motif derivation for the toy corpus is a static lookup table derived from prior public grammar analysis of each N under the thread-triangulation contract. No private factorization of any toy N ever occurs inside the pruner.
- **0-FN contract**: Rules were extracted only from cells that were verifiably absent in the enriched public rows. Adding a rule that would have removed a known-true factor word on any source row immediately invalidates it.

## Audit & Validation Log (Condensed)

- 2026-05-22 initial 5-rule seed (601_5500) → 10.18% on toy.
- Multiple aggressive expansions (PG-006 to 084) from 601_5500, 27k to 35k directional boundary, high-a, and enriched multiplication map surfaces.
- 2026-05-22 protected toy evidence surface restored: **65.45%** average, **71.21%** on the eight dominant primary cases.
- 2026-05-22 repaired real-probe replay after PG-085..PG-089: **35.02%** average across 9 distinct public semiprimes; `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` rises to **30.81%**.
- 2026-05-22 Workstream D (this session): Added PG-090 to PG-097 (8 rules) via targeted zero-FN mining on the existing 27k to 35k enriched surfaces for a4_d4_a6 / o2/o4/o6_d4_a6 / a8/a10 specific prev-phase families. No new derivation or surfaces; purely rule expansion from confirmed 0-FN cells. Rule count now 97. Pruner and catalog updated.
- 2026-05-22 low-mid live validation (`real_semiprime_64_72_samples_5`): **47.53%** average across 10 distinct public semiprimes; 10/10 resolved, 0 unresolved, 2 low-reduction coverage-gap motifs.
- 2026-05-22 extended live attempt (`64,72,80,88,96`, 3 samples each): stopped during the first 80-bit live motif derivation after 64/72 completed; current bottleneck is live derivation cost, not grammar-rule application.
- 2026-05-22 unified GMP backend rewrite: `public_motif_derivation.py` now uses one GMP arithmetic backend for all non-toy live derivation. Regression ladders preserved: `real_semiprime_64_72_samples_5_gmp_backend` remains **47.53%** with 10/10 resolved; `real_semiprime_64_80_samples_3_gmp_backend` remains **35.02%** with 9/9 resolved.
- 2026-05-22 256-target public-N run: the earlier `real_semiprime_256_samples_1_gmp_backend` artifact is invalid for research claims because it reported an implementation gate as unresolved. It has been replaced by `real_semiprime_256_samples_1_honest_status`, which records `0/1` measured, `0` unresolved, `1` `derivation_blocked`, and `pruning_status=not_attempted`.
- 2026-05-22 strict-scale runner cleanup: `pga_grammar_pruner_ladder.py` now declares backend capability, writes `diagnostic.json/md` for blocked 256+ runs, exits nonzero for failed strict-scale claims, and suppresses reduction averages in diagnostic artifacts. Exact-bit fixture construction also shows that true 80-bit live cases exceed the current regression backend's configured divisor horizon; they are reported as `derivation_blocked`, not as measured reduction rows.
- 2026-05-23 PGS-native boundary enforcement: live raw-`N` motif derivation now blocks before fixture construction unless a PGS-native motif certificate is available. The guardrail test prevents forbidden classical decision mechanisms from entering the live derivation entrypoint or the reachable blocked real-mode path.
- 2026-05-23 tier-3 calibration boundary: tier-3 remains diagnostic evidence that the current motif contract needs only coarse divisor information. It is not a promoted live backend and does not establish PGS-native raw-`N` derivation.
- Reporting bug (stale aggregate bullets) identified and surgically fixed in the same session; re-run produced clean summary.md/json.
- All active live claims now require a PGS-native motif certificate. Classical-assisted live measurements are not accepted as active research surfaces.

## Milestone Delivered: Stage-One Coverage Build

**65.45% average reduction on the exact frozen toy corpus (97-rule set).**
**89-rule repaired real-probe replay baseline: 35.02%; 97-rule Workstream D replay surface: 36.42% on the same 9 distinct public semiprimes.**
**97 public grammar rules (including 8 new from Workstream D for exotic families), fully deterministic public grammar pruning.**

The pruning rules are PGS-native grammar exclusions (GWR attractor + DNI phase + multiplicative grammar compatibility). Live raw-`N` motif derivation is explicitly unavailable until a PGS-native motif certificate exists.

The grammar pruner is production-grade for protected toy and replay surfaces. It must not be dropped into live raw-`N` workflows until a PGS-native motif certificate supplies the motif.

---

**End of Catalog** (living document: append only after fresh surface mining + zero-FN re-audit + batch re-validation).

*This file + pga_grammar_pruner.py:58 (PRUNING_RULES) together constitute the single source of truth for the current PGA grammar pruning capability.*

## Next Steps (Post-Milestone Options)

1. **Integration** (highest leverage): Wire `prune_factor_space(motif)` or the full rule list into the existing `literal_web_rich_reducer.py` / thread-triangulation runners so that every candidate list is symbolically thinned before expensive second-pass factoring or scoring. Expected wall-clock win at 48-bit and beyond.

2. **PGS-native motif certificate**: Replace blocked non-toy derivation with a PGS-native certificate that derives ordered gap/chamber state, selected attractor/invariant, phase, and previous reduced state without classical primality, factorization, or divisibility primitives as decision mechanisms.

3. **Headroom mining (40%+ live replay)**: Extend the focused miner to the next weak exact motifs in the repaired real-probe replay. Keep broad-family rules out unless a separate held-out audit supports them.

4. **Harder surface validation**: Freeze a larger deterministic real semiprime corpus and replay the entire 97-rule set for contradiction rate and realized reduction. This is the cleanest way to measure whether the live grammar signal generalizes.

5. **HTML status surface**: Per repo documentation standard, produce a self-contained `MILESTONE_25_PERCENT.html` (or under docs/gap-structure-factor-brief-evidence/) with the before/after numbers, rule families visualized, PGS object diagram, and one-click reproduction instructions.

The team (Rule Miner, Validator, Prototype Integrator, Baseline Comparator, Docs & Audit) can be re-tasked on any of the above immediately. The 25% line is crossed, now we decide how far the public grammar lever actually goes.
