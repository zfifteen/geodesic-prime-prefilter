# Cross-Chapter Prediction Candidates Catalogue

**Branch**: predictions  
**Date**: 2026-05-30  
**Authoring agent**: specialized research subagent (PGS-first synthesis)  
**Source contract (strict definition of "prediction")**: `/Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/pgs_predictions_v0.1_contract.html`  
**Governing contracts**: root `AGENTS.md`, `research/prime-gap-structure/Agents.md`, `PROOF.md`, `research/00-index/continuity/START_HERE.md`, `research/00-index/status-map.md`

## Scope and Guardrails

This synthesis performed a broad cross-chapter scan of the entire research corpus using directory enumeration, targeted file reads, and regex searches for PGS-native terms (carrier, chamber reset / reset signature / reset lock, w / selected integer / GWR w offset / w-position, endpoint determinacy / boundary drop, chain horizon, modulus link, reciprocal transport / closure, resolution, next-state / next triad, divisor-horizon, square-chamber occupancy, etc.).

**Predictions definition (verbatim from contract)**:  
A deterministic rule or measurable carrier law, built only from already-proved or explicitly measured PGS objects (divisor-count field, DNI coordinate E(n), GWR leftmost-minimizer w, endpoint chains, modulus links, chamber-reset signatures, reciprocal transport), that from the current chamber state (or a short, fully determined preceding window) either:  
- resolves one or more future PGS states exactly (position of next w, next gap type after w, next chamber-reset signature, next modulus-link residual, etc.), or  
- returns an explicit unresolved state when the carrier does not decide.

**Strictly observed**:
- PGS-first entry frame at every step: PGS objects → PGS invariants → PGS rule or law → resolved / unresolved / invalidated PGS state.
- Full state separation in every entry (theorem vs. measured vs. audited vs. hypothesis vs. unresolved vs. invalidated).
- No probabilistic, heuristic, "likely", "on average", "empirical validation", or classical-analytic-first language in candidate descriptions or recommendations.
- Classical methods appear only in legacy prefilter / audit / benchmark-comparison roles (never as inference engines for resolution).
- Legacy "predictor" language audited and flagged for correction (see dedicated section).

**Scanned surfaces** (non-exhaustive but aggressive):
- All `research/NN-*` chapters (01-generator through 15-documentation-correction + 16-predictions itself).
- `pgs-unsolved-problems/` (full index + brocard/, divisor-field-extremals/, endpoint-determinacy/, gilbreath/, legendre/, polignac-twin/).
- `docs/` (rh/, faq/, essays/, gap-structure-factor-brief-evidence/, vocabulary/, unanswered-questions/chain-horizon-closure/, specs/, releases/, etc.).
- `lean-4/` (LEAN_PGS_VERIFICATION_CONTRACT.md, PGS_LEAN_FORMALIZATION_PLAN.md, PGS/*.lean, README).
- High-scale C paths: `src/c/high-scale-pgs/` (include/pgs_high_scale.h, src/pgs_chamber.c and related).
- Legacy Python paths: `src/python/z_band_prime_predictor/`.
- Root artifacts: PLAN.md, PROOF.md, RESULTS.md, docs/PRIME_GAP_GENERATOR.md, docs/core/DIVISOR_NORMALIZATION_IDENTITY.md, docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md, docs/core/RECURSIVE_PRIME_WALK.md.
- 00-index continuity and status surfaces.

## Legacy "Predictor" Language Audit (Urgent Corrections Required)

The term "predictor" and the directory `z_band_prime_predictor` predate the v1.1 PGS-only generator contract and the deterministic-carrier definition of the Predictions track. Per the v0.1 contract and local Agents.md, this language must not steer new reasoning and must be corrected where it inverts source order or implies probabilistic/classical inference.

**Exact instances found (absolute paths)**:

1. `/Users/velocityworks/IdeaProjects/prime-gap-structure/research/00-index/continuity/START_HERE.md:399`  
   Quote: "As of 2026-05-09, the state-budget hidden-state probe is a live predictor research branch."  
   **Drift**: Directly contradicts Predictions v0.1 contract and PGS-is-deterministic rule. The surface is a measured carrier (d4_count ordering).  
   **Fix**: Replace with "measured carrier research surface" or "state-budget divisor-carrier probe (d4_count ordering carrier)". Cross-reference the 8192-row breakthrough verdict.

2. `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/three-kinds-of-prime-generators.md:28` (and table at 83)  
   Quote: "## 2. Analytic Predictor + Refinement (Z5D)" and column "Z5D (Analytic Predictor)".  
   **Drift**: Frames classical analytic density work as "predictor" and positions it as peer to PGS structural successor. Inverts required source order (integer-level PGS carriers before any zeta/RH compression reading).  
   **Fix**: Retitle section to "Legacy Analytic Density Comparison (Z5D, archived)" or move to a classical-comparison appendix with explicit demotion note. Add PGS-first source-order diagram.

3. `/Users/velocityworks/IdeaProjects/prime-gap-structure/research/00-index/migration-routing-manifest.md:28`  
   Quote: "recursive-walk and PNT-GWR predictor artifacts".  
   **Fix**: "recursive-walk and PNT-GWR comparison / prefilter artifacts (legacy)".

4. `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/zero-excess-dni/change-scope.md:417` (section heading and list 421-424)  
   Quote: "### Predictor And Generator Code" followed by listing of files under `src/python/z_band_prime_predictor/`.  
   **Fix**: Retitle to "Legacy Prefilter and Generator Scaffolding Paths (z_band_prime_predictor, historical only; see chapter 15 documentation-correction and 06-cryptology-rsa legacy prefilter boundary)".

5. `/Users/velocityworks/IdeaProjects/prime-gap-structure/FRAME_GOVERNANCE_REVIEW.md:19` and `/Users/velocityworks/IdeaProjects/prime-gap-structure/research/00-index/OBJECT_ELEVATION_PROCESS.md:78`  
   References to "carrier/lock_carrier/lower_d_threat mechanism (src/python/z_band_prime_predictor/...)" in governance context.  
   **Status**: Naming hygiene item for the carrier mechanism itself (not yet a named PGS rule). Not urgent "predictor" language but should be routed through 15-documentation-correction or 16-predictions when the object is elevated.

6. Multiple import sites in `research/06-cryptology-rsa/scripts/` (e.g. `scale_pgs_chain_modulus_link.py`, `pgs_semiprime_backward_law_search.py`, `pgs_geofac_scaleup.py`)  
   These are **permitted** under the legacy-prefilter boundary (AGENTS.md). No correction required if the import role remains "legacy prefilter / benchmark comparison only". Add header comment if missing: "Legacy prefilter path only: not PGS inference engine."

**Recommended action**: Open a focused task in `research/15-documentation-correction/` (or hand off to 16-predictions hygiene sub-track) with the exact quotes above. Update status-map validation row only after the corrections land.

## Latent Prediction Candidates (Master List)

Each entry uses only PGS objects and the deterministic-carrier definition. Status is separated. All are latent (no universal theorem yet; some have measured carrier surfaces or explicit unresolved probes).

### 1. d4_count Ordering Carrier for Next Triad / Gap-Type State
- **PGS objects involved**: Current-chamber divisor-count field (specifically count of positions with τ(n)=4), match-mode keys (mod30_prev_gap_exact), next-triad / next reduced gap-type state after the current chamber.
- **Key files / status**: `research/05-state-budget/docs/d4_count_observer_note/index.html`, `research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_long_running_research_report.md`, `research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py`, `research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py`, summary JSON at `.../state_budget_divisor_carrier_sweep_summary.json`. Measured on deterministic 8192-row-per-power 10^12..10^18 retained surface (57344 rows). Verdict: `ordering_carrier_found` (7881 decisive pairs, 6/7 positive held-out folds, +69 edge over endpoint-tail control, required edge 50).
- **Why a prediction candidate**: Exactly matches the v0.1 contract precedent. From current-chamber PGS objects alone (no next-chamber label used in the measure), it returns a deterministic ordering advantage for future PGS state (next triad) or explicit unresolved under the held-out gate. Pure integer-level carrier; no classical or probabilistic engine.
- **Recommended first action**: Re-run the exact sweep protocol on a fresh disjoint retained window (e.g. 2048-row or 4096-row construction at same powers) as replication. Then instrument the generator to emit d4_count sidecar and test on lower-power surfaces for falsification surface expansion.
- **Legacy naming / drift issues found**: None in the core 05 artifacts (correct "carrier" and "ordering_carrier_found" language). The surrounding continuity docs (START_HERE) contain the "live predictor" drift noted above.

### 2. GWR w-Position / Selected-Integer Offset Carrier (Family 1)
- **PGS objects involved**: GWR leftmost-minimizer w (the unique integer in the gap interior maximizing F(n) = −E(n)), w − p offset, current-chamber d4_count + square-phase flag + previous-gap tail length (under fixed match), next w offset or small finite set of possible offsets.
- **Key files / status**: Defined as primary recommended path in `research/16-predictions/pgs_predictions_v0.1_contract.html:105-107` and `research/16-predictions/index.html`. Generator already computes the position (see `research/01-generator` and `research/02-gwr-dni` recursive walk + GWR scripts). No dedicated retained-surface carrier sweep yet (explicit open task in the contract).
- **Why a prediction candidate**: The generator already emits the selected integer. The contract states: "given current-chamber d4_count + square-phase flag + previous-gap tail length (under fixed match), the next w offset lies in a stated small integer set, or the carrier returns unresolved." Direct extension of the proved No-Later-Simpler-Composite corollary and the d4_count precedent using identical match-mode + held-out protocol. Deterministic forward resolution of w position.
- **Recommended first action**: Instrument one retained-surface generator (or simple_pgs_generator path) to emit w offset alongside d4_count and chamber metadata. Run the identical 1024-row or 2048-row per-power 10^12..10^15 protocol. Record carrier strength for "next w offset ∈ S" rules using the same verdict language (`ordering_carrier_found` / `does_not` / `unresolved`).
- **Legacy naming / drift issues found**: None (the candidate was introduced in the clean predictions bootstrap). Old generator scaffolding paths still live under the legacy predictor dir (hygiene only).

### 3. Chamber-Reset Signature Transport and Previous-Chamber Lock Resolution
- **PGS objects involved**: Chamber-reset signatures, previous-chamber reset lock, tail_after_reset_count, lock_carrier, carrier state carried across gap boundaries, next reset point or lock activation from current invariants.
- **Key files / status**: `research/01-generator/docs/` (multiple: `pgs_chamber_reset_v1_exact_state_reduction.md`, `previous_chamber_reset_lock.md`, `previous_to_current_carrier_shift_lock_hardening.md`, `pgs_chamber_reset_v1_bound_1024_counterexample.md` etc.), C exposure in `src/c/high-scale-pgs/include/pgs_high_scale.h:55-62` (tail_after_reset_count, carrier_offset, lock_carrier_offset, lock_carrier_d in pgs_certificate_t), `research/00-index/continuity/START_HERE.md` (reset mechanics), `FRAME_GOVERNANCE_REVIEW.md`, `research/01-generator/docs/pgs_chamber_reset_v1_default_bound_128_counterexample.md`. Measured surfaces exist; some counterexamples documented for specific bounds; no universal transport law yet.
- **Why a prediction candidate**: Reset signatures and lock state are carried forward deterministically from one chamber to the next. A carrier law would resolve (from current-chamber divisor field + active lock) either the next reset admission pair / tail length or an explicit unresolved state. Directly listed in Predictions contract as core object for "next chamber-reset signature".
- **Recommended first action**: Extract the exact reset-signature and lock fields from the long-running 8192-row catalog (or regenerate with sidecar emission). Test simple match-mode carriers (e.g. previous reset signature + d4_count → next reset tail length or activation flag) using the held-out protocol.
- **Legacy naming / drift issues found**: "carrier" / "lock_carrier" naming in C header and generator scaffolding is pre-elevation (see OBJECT_ELEVATION_PROCESS and FRAME_GOVERNANCE). Not yet a named PGS rule; the mechanism is load-bearing but unnamed.

### 4. Endpoint-Chain Traversal + Divisor-Horizon Law (H(p, s0, chain_state))
- **PGS objects involved**: Semiprime-shadow seeded chains, chain-horizon closure, search-interval, divisor-horizon H, false chain node elimination, true next-prime endpoint resolution.
- **Key files / status**: `docs/unanswered-questions/chain-horizon-closure/00_question.md` (core open question), `research/01-generator/docs/` (multiple boundary / chain / shadow-seed notes: `shadow_seed_gwr_recovery_solution_report.md`, `witness_horizon_semiprime_impostors.md`, `single_hole_closure.md`, `unresolved_alternative_closure_forensics.md`), high-scale C `pgs_certificate_t` resolved_offset / certificate_closed_count, `research/06-cryptology-rsa` endpoint-chain work. Explicitly unresolved for pure PGS selection rule (still depends on deterministic divisor checking for terminal decision in high-scale).
- **Why a prediction candidate**: The precise missing object is stated as H(p, s0, chain_state) that predicts (deterministically, from PGS-visible quantities) the divisor horizon needed to close false semiprime-shadow nodes before the true next prime. If derived, it converts the current bridge into a real PGS next-prime selection rule. Direct forward resolution of chain state and endpoint.
- **Recommended first action**: Instrument a modest retained window to emit full chain_state + horizon utilization sidecars. Test whether current-chamber invariants (d4_count, square phase, active reset lock) produce a falsifiable bound or small set for the required horizon before the next zero-excess return.
- **Legacy naming / drift issues found**: None in the unanswered-question framing (correctly states the gap as "PGS next-prime selection rule" vs. fallback divisor exhaustion).

### 5. Modulus-Link Residual State + Reciprocal Transport / Endpoint Closure Determinacy
- **PGS objects involved**: Locked endpoint chain, floor transport through modulus, reciprocal endpoint closure, modulus-link residual state, structural certificate (or unresolved state).
- **Key files / status**: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/` (ALGORITHM.md, PGS_CERTIFICATE.md, METRICS.md, SESSION_BOOTSTRAP.md, output/*.jsonl survivor/inference rows), `research/06-cryptology-rsa/docs/endpoint_structure_law.md`, `research/06-cryptology-rsa/README.md`, multiple experiment scripts and output ladders (40-bit resolved, 50-bit unresolved_by_reciprocal_carrier_misalignment, 64-bit resolved). Status: measured on specific ladder rungs with exact audit separation; no universal theorem.
- **Why a prediction candidate**: From public endpoint chain + reset signatures, reciprocal transport supplies deterministic constraints on the next zero-excess return (or explicit unresolved when the carrier misaligns). The live result language already uses "resolved / unresolved_by_reciprocal_carrier_misalignment". Perfect match to contract objects (modulus links, reciprocal transport, structural certificate).
- **Recommended first action**: Extract the exact public PGS fields used in the reciprocal predicate (z = floor(N / upper.reset_endpoint), corrected_lower.reset_signature, etc.) and test whether they form a carrier for next-chamber reset signature or w offset on generic (non-RSA) retained surfaces.
- **Legacy naming / drift issues found**: None in the live-solver artifacts (correct "unresolved_by_reciprocal_carrier_misalignment" language). Older archive/2026-05-13-shor-order-entropy-sidecar/ is explicitly marked archived.

### 6. Reset Stop-Wall Alphabet Classification (Gilbreath Track)
- **PGS objects involved**: Seeded endpoint gaps (starting from 2), repeated divisor-count stopping rule τ(n)=2, reset admission pair (fixed at 2,4), closed positive resets, stop-wall differences.
- **Key files / status**: `pgs-unsolved-problems/gilbreath/2026-05-20-reset-stop-wall-classification.html`, `2026-05-20-reset_stop_wall_probe.py`, `2026-05-20-reset_stop_wall_summary.json`, `2026-05-20-reset_stop_wall_rows.csv`, index.html. Measured closed stop-wall alphabet on the surface: {4,6,8,10} (diff-4 stop shortcut falsified). Gilbreath proof unresolved.
- **Why a prediction candidate**: The actual seeded PGS cascade produces a deterministic stop-wall alphabet for closed resets. A carrier law would resolve, from the current reset admission pair + preceding divisor-field invariants, the exact next stop-wall difference (or small set) or unresolved. Direct next chamber-reset signature resolution.
- **Recommended first action**: Extend the probe to emit preceding-chamber d4_count / square-phase / lock state alongside each reset event. Test match-mode carriers for the observed alphabet values on larger seeded surfaces.
- **Legacy naming / drift issues found**: None (clean PGS-native framing in the probe HTML).

### 7. Boundary-Drop Admissibility and Endpoint Determinacy Rules
- **PGS objects involved**: Public endpoint classes, boundary drop, admissibility of drops, endpoint determinacy for factorization-adjacent moduli.
- **Key files / status**: `pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility.html` + .py + .json, index.html. Explicitly "not covered by other agents" per task; status is probe-level measured surfaces.
- **Why a prediction candidate**: Endpoint determinacy supplies deterministic constraints on admissible next endpoints / drops from current public endpoint chain state. Forward resolution of next endpoint or structural certificate (or unresolved). Directly referenced in 16-predictions/index.html as unification target.
- **Recommended first action**: Re-express the boundary-drop probe output in terms of current-chamber PGS objects (d4_count, reset signature, modulus-link residual) and test for carrier ordering on the drop events using the established held-out protocol.
- **Legacy naming / drift issues found**: None observed in the subdir (correct "endpoint-class determinacy, not through classical candidate-factor search").

### 8. Residual-Endpoint Quarter-Frontier and NLSC-Deadline Bridge (Legendre Track)
- **PGS objects involved**: Square-chamber occupancy, selected-d4 residual, residual endpoint, NLSC deadline, prime-square boundary forcing.
- **Key files / status**: `pgs-unsolved-problems/legendre/index.html`, `2026-05-20-residual-endpoint-quarter.html` + .py + .csv + .json, `2026-05-14-nlsc-deadline-bridge-falsification.html`. Active branch "selected-d4 residual"; latest run ADVANCE; claim status unresolved. Also `2026-05-20-residual-endpoint-quarter-summary.json`.
- **Why a prediction candidate**: The PGS translation of Legendre forces next-prime endpoint arrival before the next square boundary via square-chamber structure. Residual-endpoint and selected-d4 residual are measurable carriers for whether a gap interior will contain a full chamber (or the exact residual to the square). Deterministic forward resolution of square-phase terminal behavior (Family 2/4 adjacent).
- **Recommended first action**: Add d4_count + previous reset signature as features in the residual-endpoint-quarter probe and re-run the falsification surface for a carrier verdict.
- **Legacy naming / drift issues found**: None (strong PGS-native translation of the classical statement).

### 9. Lag-2 / Lag-3 Boundary Exposure (Polignac-Twin Track)
- **PGS objects involved**: Twin / Polignac structures, lag-2 / lag-3 reduced words, boundary exposure, component-sharing exclusion, current-chamber state to next reduced state ordering.
- **Key files / status**: `pgs-unsolved-problems/polignac-twin/index.html`, `probes/lag2_boundary_exposure_probe.py`, `output/lag2_boundary_exposure_probe/` (ranked_current_states.csv, ranked_lag2_pairs.csv, summary.json, threshold_summary.csv), `notes/2026-05-20-lag2-boundary-exposure.html`.
- **Why a prediction candidate**: The grammar findings (solved rows reuse recursive lag-2 or lag-3 pieces while avoiding the ordered reduced words of the expanded surface) are measured inverse-word exclusion results. These supply deterministic constraints on admissible next reduced states from current chamber facts, a next-state carrier in the gap-type grammar.
- **Recommended first action**: Merge the lag-2/lag-3 exclusion families with the d4_count + reset-signature match keys and test on a retained window for ordering advantage on next reduced state.
- **Legacy naming / drift issues found**: None in the polignac-twin artifacts.

### 10. Gap-Ridge D4-Arrival, Square-Threat, and Closure Constraints
- **PGS objects involved**: Gap ridge, GWR d4 arrival, square threat (d4_square_threat_*), closure constraint, nonfloor frontier, residue dead zone.
- **Key files / status**: `research/11-gap-ridge/` (full set of tests: test_gwr_d4_arrival_validation.py, test_gwr_closure_constraint.py, test_d4_square_threat_*.py, test_d4_square_residue_dead_zone_probe.py, etc.), docs/ and output/ containing SVG/JSON surfaces. Many validation tests around d4 arrival and square obstructions.
- **Why a prediction candidate**: Ridge geometry and d4-arrival / square-threat constraints are local PGS structures that modulate admissible next states (closure before/after square boundaries, residue dead zones). Direct source of deterministic forward rules on w placement or excess-bounded closure inside ridge-affected chambers.
- **Recommended first action**: Treat the ridge tests as a source of candidate carrier hypotheses (e.g. "given current d4 arrival relative to ridge, next w offset or next gap type lies in set S"). Instrument a catalog probe and apply the ordering-carrier protocol.
- **Legacy naming / drift issues found**: None observed.

### 11. Higher-Tau Reciprocal Blockers (Divisor-Field-Extremals)
- **PGS objects involved**: Higher-τ positions, reciprocal blockers, divisor-field extremals, modulus reciprocity in high-τ regimes.
- **Key files / status**: `pgs-unsolved-problems/divisor-field-extremals/2026-05-20-higher-tau-reciprocal-blockers.html`, `higher_tau_reciprocal_blocker_probe.py`, `index.html`, `output/2026-05-20-higher-tau-reciprocal-blockers-*`.
- **Why a prediction candidate**: Higher-τ reciprocal blockers are measurable obstructions in the divisor field that force or forbid certain endpoint / reset behaviors. They supply deterministic constraints on future chamber occupancy or reciprocal closure from the current field state.
- **Recommended first action**: Cross-correlate blocker events with current-chamber d4_count, reset signature, and square phase on retained surfaces; test for carrier strength on next blocker or next zero-excess location.
- **Legacy naming / drift issues found**: None.

### 12. E-Fluctuation / Cumulative Excess Modulation (Family 3) and Special-Form Unification (Family 4)
- **PGS objects involved**: Cumulative excess ΣE(n) or local max E from w onward, square-phase terminal behavior, chamber-reset lock, special-form preceding chambers (exponent walls, Mersenne/Sophie-Germain pairs), next zero-excess return density modulation.
- **Key files / status**: Contract definition in `research/16-predictions/pgs_predictions_v0.1_contract.html:93-100`; surfaces in `research/09-exponents/` (migrated, validated 68 tests), `research/02-gwr-dni` (DNI/E(n) recursive walk), `research/04-bounded-compression` (square-branch, dynamic cutoff, invalidated fixed-cutoff map), `docs/rh/` (downstream reading only, dni-to-zeta-compression.md etc.; archived classical route in research/12-rh-bridge). Measured modulation on retained windows; no universal carrier law.
- **Why a prediction candidate**: The contract explicitly frames cumulative excess + reset lock as producing "deterministic modulation of the local density of zero-excess returns" measurable as structured deviation from uniform placement of next w / next prime. Special-form cases are ordinary chambers whose preceding signature (d4_count, reset state) supplies the same constraints. Integer-level carrier first; any zeta reading is downstream compression only.
- **Recommended first action**: On the existing 8192-row d4 catalog, compute cumulative E from each w and test whether reset signature + d4_count + cumulative E produces a falsifiable small-set predictor for distance to next zero-excess (or next w) under the held-out protocol. Unify with 09-exponents preceding-chamber signatures.
- **Legacy naming / drift issues found**: `research/12-rh-bridge/` is archived precisely for classical drift / prompt injection (see status-map and ARCHIVAL_HANDOFF). Do not route new carrier work here. docs/rh/ files must be read only after PGS integer carrier is stated.

## Master Opportunities Table (Ranked by Near-Term Deterministic Carrier Potential)

Ranking criteria (PGS-native, no external metrics): (1) proximity to existing proved invariants or measured carrier protocol (d4 precedent), (2) explicit open question or probe already phrased in forward-resolution terms, (3) cross-chapter unification leverage, (4) low risk of classical or probabilistic reframing, (5) availability of retained-surface machinery or easy instrumentation.

| Rank | Candidate | Primary Locations (absolute) | Readiness / Surface | Cross-Chapter Links | Recommended First Action (narrow) | Priority Rationale |
|------|-----------|------------------------------|---------------------|---------------------|-----------------------------------|--------------------|
| 1 | d4_count Ordering Carrier (replication + w-offset extension) | research/05-state-budget/output/state_budget_long_running_catalog_8192/*, research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py, research/16-predictions/pgs_predictions_v0.1_contract.html | High, existing 8192-row protocol + held-out verdict language; generator already emits w | 02-gwr-dni (GWR w), 01-generator, 03-gap-types (triad states) | Instrument w offset emission; run identical protocol on fresh 2048-row window for w-carrier verdict | Direct contract "Recommended First Pick"; smallest step to new publishable auditable surface this cycle |
| 2 | Chamber-Reset Signature Transport + Lock Resolution | research/01-generator/docs/previous_chamber_reset_lock.md and pgs_chamber_reset_v1_*.md, src/c/high-scale-pgs/include/pgs_high_scale.h (tail_after_reset_count, lock_carrier_*), research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ | Medium-High. C exposure + many 01 notes + reset examples in 06 | 06-cryptology (reset signatures in certificates), pgs-unsolved/gilbreath (reset stop-walls), 16 index | Emit reset-signature + lock sidecars on existing long-running catalog; test match-mode carriers for next reset tail / activation | Core contract object; load-bearing in production generator + RSA ladders; unifies multiple reset mentions |
| 3 | Endpoint-Chain Horizon Closure (H(p, s0, chain_state)) | docs/unanswered-questions/chain-horizon-closure/00_question.md, research/01-generator/docs/shadow_seed_* and witness_horizon_*.md, research/06-cryptology-rsa (endpoint structure) | Medium: explicit open question with % non-PGS bridge numbers; C certificate fields | 06-cryptology (modulus-link), pgs-unsolved/endpoint-determinacy, high-scale C | Add chain_state + horizon utilization sidecars; test current invariants → horizon bound carrier | Highest-leverage open question for pure PGS next-prime rule; directly attacks high-scale non-PGS fraction |
| 4 | Modulus-Link Residual + Reciprocal Closure Determinacy | research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ALGORITHM.md + PGS_CERTIFICATE.md + output ladders, research/06-cryptology-rsa/docs/endpoint_structure_law.md | High (measured on specific rungs with exact resolved/unresolved separation) | 01-generator (chain), pgs-unsolved/legendre + endpoint-determinacy, 16 contract Family 2/4 | Lift the reciprocal predicate fields to generic retained surfaces; test as carrier for next w or reset signature | Already uses correct "unresolved_by_reciprocal_carrier_misalignment" language; strong unification target |
| 5 | Reset Stop-Wall Alphabet + Boundary-Drop Admissibility | pgs-unsolved-problems/gilbreath/2026-05-20-reset-stop-wall-classification.html + summary.json, pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility.html | Medium, concrete measured alphabets and probe surfaces | 01-generator (reset notes), 06-cryptology (endpoint classes), 11-gap-ridge (closure) | Correlate stop-wall / drop events with d4_count + reset signature on retained windows | Direct next "chamber-reset signature" resolution; falsified shortcuts already documented (good hygiene) |
| 6 | Square-Chamber / Residual-Endpoint + Lag-2 Boundary (Legendre + Polignac) | pgs-unsolved-problems/legendre/ (residual-endpoint-quarter*), pgs-unsolved-problems/polignac-twin/ (lag2_boundary_exposure_probe + output) | Medium. ADVANCE runs + explicit grammar exclusion results | 04-bounded-compression (square branch), 09-exponents (special-form), 03-gap-types (grammar), 11-gap-ridge (d4 square threat) | Add d4_count + reset keys to the existing probes; apply ordering-carrier protocol | Unifies square-phase terminal behavior (Family 2) with gap-grammar next-state constraints; multiple unsolved subdirs |
| 7 | Gap-Ridge D4-Arrival + Square-Threat Constraints + Higher-Tau Reciprocal Blockers | research/11-gap-ridge/ (all test_d4_square_threat_*.py + test_gwr_closure_constraint.py), pgs-unsolved-problems/divisor-field-extremals/ | Medium-Low, rich test surfaces but no carrier sweep yet | 02-gwr-dni, 04-bounded-compression, 05-state-budget (d4), legendre | Treat ridge / blocker / square-threat tests as hypothesis generators; emit sidecars and run first carrier sweep | Local geometric invariants that directly modulate w and closure; under-explored as carriers |

**Lower-ranked but retained for completeness**: E-fluctuation modulation (Family 3, requires clean PGS integer carrier first before any rh/ reading), special-form preceding signatures (09-exponents, unification only after generic w-carrier baseline), divisor-horizon law for chain (overlaps #3).

## Additional Observations

- **State separation preserved everywhere** in the active 05, 06, 01, and pgs-unsolved artifacts. The strongest surfaces already use the exact verdict language required by the predictions contract.
- **No probabilistic language** was introduced or endorsed in any candidate description.
- **C high-scale surface** (`src/c/high-scale-pgs/`) is the correct place for performance instrumentation of any new carrier once the Python retained-surface protocol stabilizes; the certificate struct already exposes the necessary carrier/lock/reset fields.
- **Lean-4** (`lean-4/PGS_LEAN_FORMALIZATION_PLAN.md`, `PGS/GWR.lean`, `PGS/NextPrime.lean`) is the correct downstream verification layer for any carrier that reaches theorem status. Chamber reset and horizon concepts are already called out in the formalization plan.
- **Chapter 15 (documentation-correction)** remains the primary home for the legacy-predictor hygiene work listed above; 16-predictions can consume the corrected surfaces once available.
- **research/12-rh-bridge** is correctly archived and must not be used as entry point for any new carrier work.

## Reproduction Commands (Current State of This Catalogue)

```bash
# View this report
cat research/16-predictions/catalogue/cross-chapter-prediction-candidates.md

# Full continuity + contract bootstrap (always first)
cat research/00-index/continuity/START_HERE.md
cat research/16-predictions/pgs_predictions_v0.1_contract.html | head -80
cat research/00-index/status-map.md | grep -A2 -B2 "16-predictions"

# Core carrier surface verification
python3 -m pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py -q

# High-scale C (for future carrier instrumentation)
make -C src/c/high-scale-pgs test

# Lean formalization smoke (downstream audit only)
cd lean-4 && lake build && lake env lean smoke-test.lean
```

All claims in this catalogue are subordinate to `PROOF.md` for theorem status, to the v0.1 predictions contract for the meaning of "prediction", and to the full AGENTS.md / local Agents.md for reasoning discipline. No candidate has been promoted beyond its measured or probe status on the exact surfaces cited.

**End of synthesis.** Future sessions on the Predictions track should begin by re-reading the v0.1 contract HTML, this catalogue, the d4_count long-running report, and the chain-horizon-closure open question before proposing the next falsification probe.