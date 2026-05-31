# GWR/DNI/Generator Deterministic Prediction Candidates

**PGS Predictions Track • research/16-predictions/catalogue**  
**Generated:** 2026-05-30 (predictions branch)  
**Scope:** Exhaustive extraction of deterministic carrier laws and structural resolution rules from core GWR/DNI mathematics (PROOF.md, LEFTMOST_MINIMUM_DIVISOR_RULE.md, DIVISOR_NORMALIZATION_IDENTITY.md), the Minimal PGS Generator surfaces, and supporting measured/hypothesis artifacts in research/01-generator/, research/02-gwr-dni/, research/05-state-budget/, pgs-unsolved-problems/, and related code (src/python/z_band_prime_predictor/*, research scripts).  

**Entry frame (PGS-first, per AGENTS.md and pgs_predictions_v0.1_contract.html):**  
PGS objects (ordered prime-gap state, divisor-count field τ(n), DNI E(n)/Z(n), GWR leftmost min-τ integer w / selected integer, chamber-reset signatures, lock_carrier, tail_after_reset, reset_signature, modulus-link residuals, endpoint chains, reciprocal transport) → PGS invariants (Interior Maximizer theorem, No-Later-Simpler-Composite corollary, dominant d=4 under square exclusion on measured surfaces, wheel-admissible carrier tracking) → PGS rule/law (carrier or resolution) → resolved / unresolved / invalidated PGS state (next w offset or small set, next gap-type/triad state after w, next reset signature, closure offset, transported lock state, etc.).  

**Definition of prediction candidate (verbatim from contract):** A deterministic rule or measurable carrier law, built only from already-proved or explicitly measured PGS objects, that from the current chamber state (or short fully-determined preceding window) either resolves one or more future PGS states exactly or returns explicit "unresolved".  

**Strict discipline observed:** No probabilistic language. No classical-first framing (isprime/nextprime/Miller-Rabin/gcd/sieves/li(x)/Cramér as inference engine). All candidates begin from PGS objects. State separation enforced at every entry: proved (in PROOF.md), measured (exact regime + artifact), hypothesis, unresolved, invalidated. Legacy z_band_prime_predictor naming treated as historical; production surfaces and retained catalogs preferred.  

**Sources surveyed (mandatory first + deep dive):**  
- research/16-predictions/pgs_predictions_v0.1_contract.html (definition + families)  
- PROOF.md (GWR/Interior Maximizer theorem lines 145-156, NLSC corollary, Ordered Comparison Lemma)  
- RESULTS.md (No-Later-Simpler-Composite zero violations to 10^18, d4_count precedent, generator surfaces)  
- research/00-index/continuity/START_HERE.md + AGENTS.md (local + canonical prose/discipline)  
- research/02-gwr-dni/ (README, docs/dominant_d4_arrival_reduction_findings.md, closure_constraint_findings.md, gwr_interval_presieve_optimization_note.md, gwr_dni_exact_recursive_prime_walk_note.md, output/*_summary.json, scripts/gwr_dni_recursive_walk.py and proof/*)  
- research/01-generator/ (README, docs/ on boundary_law_00*, pgs_chamber_reset_v1_*, previous_to_current_carrier_shift_lock_hardening.md, rule_x_consistency_collapse_logic_engine.md; output/rule_x_logic_engine/* reports; scripts/prime_inference_generator/* probes)  
- src/python/z_band_prime_predictor/ (simple_pgs_generator.py:118-149 carrier_w/lock_carrier logic; gwr_boundary_walk.py:67-69 winner update; gpe_nlsc_selector.py, gpe_boundary_selector.py)  
- src/c/high-scale-pgs/ (integer chamber certificate emission)  
- tests/ (generator + gwr walk tests)  
- PRIME_GAP_GENERATOR.md (chamber reset surfaces)  
- pgs-unsolved-problems/endpoint-determinacy/ + gilbreath/ (boundary drop, reset-stop-wall)  
- research/05-state-budget/ (d4_count breakthrough, state_budget_divisor_carrier_sweep.py:42-54 measures, long-running 8192-row catalog)  
- research/03-gap-types/ (gap-type catalog + triad probes feeding carrier tests)  

**How candidates were extracted:** Every location was scanned for PGS objects (w/selected/carrier_w, d4_count or first-d=4, chamber reset/lock_carrier/reset_signature, tail, square-phase, previous-chamber transport, NLSC threat, gap-type/triad) that constrain future states (next w offset/set, post-w gap type, next reset sig, closure threshold, transported modulus residual). Only exact, auditable, deterministic surfaces retained. Drift self-corrected on sight (e.g., any averaging language rewritten to exact retained-surface protocol).

---

## Proved Foundations (Source Layer — Subordinate Only to PROOF.md)

**GWR / Interior Maximizer Theorem (PROOF.md:145-156):**  
Given prime p, q = min{n > p : τ(n)=2}, I = {p+1 … q-1} (nonempty).  
w = min {n ∈ I : τ(n) = min_{m∈I} τ(m)}.  
Then w is the unique integer in I maximizing F(n) = −E(n) (equivalently minimizing excess E(n) = (τ(n)/2 − 1) log n).  
Primary objects: ordered divisor-count field, GWR w/selected integer.  
Epistemic: **proved** (universal under hypotheses; finite base + exact arithmetic closure).  
Prediction relevance: Any carrier law may use current-chamber w position or d(w) as invariant to resolve next-chamber w or reset state.  
Falsification surface: N/A (theorem).  

**No-Later-Simpler-Composite (exact corollary, PROOF.md:186-224 + RESULTS.md):**  
Once w appears, no later integer t (w < t < q) satisfies τ(t) < τ(w).  
Stress surface: full 10^18, zero violations (RESULTS.md).  
Primary objects: w, divisor-count field, endpoint q.  
Epistemic: **proved** (corollary of maximizer + tail closure).  
Prediction relevance: Supplies exact post-w closure invariant; base for stronger type-specific closure carriers (d4_count + square-phase + lock).  

**Direct deterministic next-prime (PROOF.md headline):** Exact divisor-count traversal returns q.  
Epistemic: **proved**.  

---

## Measured Carrier Laws (Exact Retained Surfaces + Held-Out Protocol)

**1. d4_count ordering carrier for next-triad (reduced gap-type) state**  
Primary PGS objects: current-chamber divisor-count field (specifically count of d(n)=4 positions), previous-gap tail length, endpoint residue mod 30, GWR context, next reduced gap-type triad state.  
File:line: research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py:42-54 (CANDIDATE_MEASURES), 106-115 (d4_count computation from catalog); research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_long_running_research_report.md:44-80 (breakthrough row); catalog generator research/03-gap-types/scripts/gwr_dni_gap_type_catalog.py.  
Epistemic: **measured** — ordering_carrier_found on deterministic retained 8192-row-per-power 10^12..10^18 surface (57344 rows total, 45603 d=4 transitions scored).  
Concrete verdict (mod30_prev_gap_exact match mode): 7881 decisive matched pairs, 7/7 held-out powers >100 decisive, 6/7 positive oriented folds, +299 oriented signed advantage, +69 edge over endpoint-tail control (required +50).  
Falsification/measurement surface: Re-run `python3 research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py --detail-csv ...` on fresh retained catalog; held-out ruler tests (state_budget_pairwise_ruler_test.py etc.); pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py.  
Why strong deterministic prediction candidate: Exactly matches contract definition and precedent. Uses only current-chamber PGS objects under explicit match discipline; returns decisive carrier strength or unresolved; no probabilistic claim. Directly resolves/constrains future PGS state (next triad/gap-type after current w-bearing chamber).  
Drift risks: None in current artifacts (strictly measured + held-out); risk only if later prose drops the "measured on exact X surface" qualifier.  

**2. First d=4 arrival equals GWR w under square exclusion (no interior prime square)**  
Primary PGS objects: divisor-count field of gap after p, GWR w, square-phase flag (presence/absence of interior prime square before or at w), d(w).  
File:line: research/02-gwr-dni/docs/dominant_d4_arrival_reduction_findings.md:10-15 (statement), 60-99 (results table + counterexamples); runner research/11-gap-ridge/scripts/gwr_d4_arrival_validation.py; outputs research/02-gwr-dni/output/gwr_d4_arrival_validation_exact.csv + summary.json; even-band ladder 10^8..10^18.  
Epistemic: **measured** — exact full scans to 2×10^7 + deterministic even-band windows (2 per decade 10^8..10^18, 2×10^6 width). 0 interior-square violations in all d(w)=4 gaps. first-d=4 match rate = 1.0 on every regime. 8 prime-cube (d=4 but not semiprime) exceptions per high decade (first explicit: 6859=19^3 in gap (6857,6863)).  
Falsification/measurement surface: Re-execute the gwr_d4_arrival_validation runner on extended ladder or full high-scale C generator output; compare against square-branch probes in research/04-bounded-compression/.  
Why strong: Supplies deterministic rule for w position itself ("the offset w−p is the offset of the first d=4 when square flag = false"). Dominant regime (d(w)=4 in ~80-85% of gaps on surface). Directly usable as carrier from visible pre-w structure.  
Drift risks: Must always qualify "under square exclusion on this surface"; semiprime-only strengthening already invalidated by prime-cube family.  

**3. NLSC threat horizon / lock_carrier_d closure after w (generator certificates)**  
Primary PGS objects: GWR w / carrier_w, lock_carrier_offset/d, lower_d_threat_offset, tail_after_reset_offsets, chamber-reset signature, square-phase terminal.  
File:line: src/python/z_band_prime_predictor/simple_pgs_generator.py:71-95 (carrier min-d tracking + threat scan), 120-146 (carrier_w, lock_carrier, threat in certificate); gpe_nlsc_selector.py:151-178 (d4_closure_ceiling for d(w)=4 branch); C equivalent in src/c/high-scale-pgs/src/pgs_chamber.c + tests/test_integer_chamber.c.  
Epistemic: **proved base (NLSC) + measured** (exact on all generator validation surfaces 11..10^18 decade windows + 10^1233 integer-start certificate path; zero audit failures).  
Falsification/measurement surface: Run generator probes (research/01-generator/scripts/simple_pgs_generator_scale_sweep.py, minimal_pgs_scale_probe.py); C `make -C src/c/high-scale-pgs test`; retained catalog checks for threat_horizon utilization.  
Why strong: NLSC already gives exact post-w "no simpler composite before q". Generator emits explicit lock_carrier and threat as runtime state; d4-specific ceiling (predictor.d4_closure_ceiling) supplies type-specific horizon. Directly constrains future zero-excess return (q) from w onward.  
Drift risks: Bounded-compression dynamic-cutoff strengthenings remain unresolved/invalidated in parts (research/04-bounded-compression/ square-tail pause); keep separate from core proved NLSC.  

---

## Generator + Chamber-Reset Carrier Hypotheses (Candidate-Grade, Probe Surfaces)

**4. w-offset carrier from current-chamber d4_count + square-phase flag + previous-gap tail (under fixed match)**  
Primary PGS objects: current d4_count, square-phase flag, previous-gap tail length, mod-30 residue, GWR w offset (carrier_w emitted), next w offset (small integer set or unresolved).  
File:line: research/16-predictions/pgs_predictions_v0.1_contract.html:84-86 (explicit Family 1 recommendation); simple_pgs_generator.py:142 (carrier_w emission in certificate); research/05-state-budget carrier sweep machinery (extendable to w_offset).  
Epistemic: **hypothesis** (generator already computes and emits carrier_w as part of every chamber-reset certificate; d4_count precedent exists on identical retained surfaces; no dedicated w_offset sweep executed yet).  
Concrete first falsification: Instrument retained catalog emitter or simple_pgs_generator path to also emit w_offset alongside d4_count; run identical mod30_prev_gap_exact + held-out protocol on 1024-row-per-power 10^12..10^15 window; apply same decisive-pairs / edge-over-control / unresolved-rate verdict language.  
Why strong: Smallest executable step per contract; re-uses exact 05-state-budget protocol and generator emission point; directly addresses "position of next w" resolution target.  
Drift risks: Must emit explicit "unresolved" when carrier does not decide; never promote to theorem without PROOF.md artifact.  

**5. Previous-chamber carrier shift / reset-lock / higher-divisor pressure as carrier for current w or boundary**  
Primary PGS objects: previous-chamber carrier_w / lock_carrier_d / reset_signature, current-chamber GWR w, boundary offset q, higher-divisor pressure lock state, transported previous selected-integer shift.  
File:line: research/01-generator/docs/previous_to_current_carrier_shift_lock_hardening.md:1-40 (status of 005B lead); research/01-generator/docs/boundary_law_00*.md family (multiple candidates); scripts/prime_inference_generator/previous_to_current_carrier_shift_lock_hardening.py, previous_chamber_reset_lock_probe.py, lock_near_miss_profile.py, higher_divisor_pressure_lock_hardening.md; output/rule_x_logic_engine/ reports.  
Epistemic: **hypothesis** (candidate-grade "Next-Prime Law 005*" family; zero-wrong on tested surfaces in some probes; abstentions recorded; not integrated into production generator; some blocked for pure-generator use).  
Falsification/measurement surface: Re-execute the listed previous_to_current_* and lock_* probe scripts on extended decade ladder; compare against chamber-reset certificate fields (carrier_w, lock_carrier_offset, reset_signature) emitted by generator; check absorption_lock_action_population_audit.  
Why strong: Explicit transport of PGS chamber-reset state (lock, carrier_d, signature) across consecutive chambers; directly constrains current w position or q from preceding invariants. Matches "chamber reset" and "previous-to-current" PGS objects.  
Drift risks: Previous-search-interval evidence is history-dependent; must keep audit-after-generation separation; some laws already graded "candidate-grade only / milestone blocked".  

**6. reset_signature (carrier_d / lock_carrier_d / threat / deadline) as deterministic modulator of next-chamber gap-type or w-class**  
Primary PGS objects: reset_signature string or tuple (e.g. "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail"), current d4_count / w d-class, next triad or w d-class.  
File:line: research/06-cryptology-rsa/experiments/proof-workbenches/rsa-v2/output/.../acquisition_rows.jsonl (example signatures with carrier_w values); simple_pgs_generator.py:142-146 (signature fields in certificate); rsa-v2 live-solver SESSION_BOOTSTRAP.md and related.  
Epistemic: **measured** (exact signatures emitted and archived on RSA v2 ladders + generator probes; used in endpoint-structure law certificates).  
Falsification/measurement surface: Mine generator output or retained gap-type catalogs for signature → next-chamber state correlations under same match-mode discipline as d4_count; extend state_budget_divisor_carrier_sweep to include signature components.  
Why strong: Compact, fully determined PGS object exported from every chamber; already audited in cryptology endpoint work; natural extension of d4_count precedent to richer reset state.  
Drift risks: RSA context must not leak into generic generator framing; signatures are diagnostic sidecars, never inside minimal {"p","q"} records.  

---

## Additional Strong Surfaces from GWR/DNI + Generator Probes

**7. Post-w excess accumulation + square-phase terminal + active lock → type-specific closure offset sets**  
Primary PGS objects: w, cumulative ΣE(n) or max local E from w onward, square-phase terminal behavior, lock_carrier, next E=0 return (q).  
File:line: research/16-predictions/pgs_predictions_v0.1_contract.html:88-91 (Family 2); research/04-bounded-compression/ docs + falsification runners (C(q) empirical rule, square-branch characterization); gpe_nlsc_selector.py square_ceiling_margin.  
Epistemic: **proved base (NLSC) + measured** (dynamic cutoff C(q) = max(64, ceil(0.5 log(q)^2)) empirical on surfaces; many square-branch probes; some sub-rules invalidated e.g. fixed {2:44,4:60,6:60}).  
Falsification/measurement surface: research/04-bounded-compression/scripts/bounded_compression_falsification_runner.py + d4_* variants; compare exact unbounded GWR witness against C(q).  
Why strong: Directly from contract Family 2; uses post-w invariants to constrain future zero-excess return.  
Drift risks: Any O(log x · …) framing forbidden; must stay at exact integer offsets or small finite sets on concrete surfaces.  

**8. d4_span / d4_last_to_endpoint / d4_centroid_offset and other chamber scalars as weaker ordering carriers**  
Primary PGS objects: current-chamber d4_span etc (derived from d4_offsets in divisor-count field), next triad state.  
File:line: research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py:44-46, 112-115 (other CANDIDATE_MEASURES beyond d4_count).  
Epistemic: **measured** (tested on same 8192-row 10^12..10^18 surface; only d4_count met full ordering_carrier_found gate; others returned does_not or unresolved under held-out).  
Falsification/measurement surface: Same sweep script + pairwise ruler tests; inspect per-power CSVs for any sub-regime strength.  
Why strong: Exhaustive enumeration of divisor-field scalar carriers; documents what did not rise to carrier status (prevents revival).  

**9. Gap-type grammar / reduced 14-state core transitions constrained by current d4_count or w d-class**  
Primary PGS objects: current reduced gap-type (from 03-gap-types), d4_count or w d(w), next reduced state (Semiprime Wheel Attractor core).  
File:line: research/03-gap-types/ probes + long-horizon controller; PRIME_GAP_GENERATIVE_MODEL.md (14-state core + transition rules); state-budget forbidden_transition tests (invalidated exact exclusion but retained weak ordering).  
Epistemic: **measured** (local fidelity / concentration metrics on pooled windows; forbidden-transition exact exclusion invalidated on 2048+ row surfaces).  
Falsification/measurement surface: research/03-gap-types/scripts + tests; state_budget_forbidden_transition_test.py on expanded catalogs.  
Why strong: Connects GWR/DNI chamber objects directly to the reduced generative model state machine; d4_count already shown to order triad subset.  

**10. Endpoint-chain / modulus-link residual + reciprocal transport from current reset state**  
Primary PGS objects: current chamber reset_signature / tail_after_reset / carrier_w, endpoint-chain traversal, modulus-link closure, next reset or structural certificate (resolved/unresolved).  
File:line: pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility.html (boundary-drop lemma on public cells); research/06-cryptology-rsa/ live-solver/rsa-v2/ (reciprocal deadline-signature correction, public certificate closure); research/01-generator/output/simple_pgs_chain_horizon_closure_* probes.  
Epistemic: **measured** (40-bit/64-bit RSA v2 ladders audit-confirmed after PGS carriers; 50-bit unresolved_by_reciprocal_carrier_misalignment; many chain-horizon probes).  
Falsification/measurement surface: rsa-v2 run_experiment.py + METRICS.md; endpoint-determinacy probe.py; chain-horizon closure scripts.  
Why strong: Full transport of PGS chamber invariants across modulus; resolves or returns explicit unresolved on structural certificates.  

**11. Special-form chamber unification (exponent walls, integer-start, Mersenne candidates)**  
Primary PGS objects: special-form chamber (exponent wall or integer-start), same d4_count / reset_signature / w d-class carriers as generic, next w or gap-type.  
File:line: research/09-exponents/ (PGS experiments on walls); research/01-generator/docs/integer_start_pgs_chamber_task.md + output/integer_start_pgs_chamber_probe/; pgs_predictions_v0.1_contract.html:98-100 (Family 4 unification).  
Epistemic: **measured** (on dedicated probes; same carrier signatures apply).  
Falsification/measurement surface: Extend 05-state-budget retained catalog protocol to exponent-wall subsets; integer-start C probes.  
Why strong: Treats special forms as ordinary chamber types carrying identical PGS objects; unifies rather than special-cases.  

**12. Reset-stop-wall and boundary-drop admissibility (gilbreath + endpoint-determinacy)**  
Primary PGS objects: chamber reset, stop-wall classification, boundary drop across N-1 floor map, endpoint cell promotion.  
File:line: pgs-unsolved-problems/gilbreath/2026-05-20-reset-stop-wall-classification.html + probe.py; endpoint-determinacy/2026-05-20-boundary-drop-admissibility.html (bridge lemma).  
Epistemic: **hypothesis / advance** (deterministic probe + proof sketch; conditional on public boundary-drop field).  
Falsification/measurement surface: The listed .py probes + summary JSON.  
Why strong: Extends chamber-reset signatures into endpoint-determinacy resolution rules.  

---

## Invalidated Rules (Must Not Be Revived as Prediction Carriers)

- Fixed cutoff map {2:44, 4:60, 6:60} (RESULTS.md, 04-bounded-compression).  
- Square-room-side as hard next-state exclusion / forbidden-transition (invalidated on 2048-row+ retained surfaces in 05-state-budget).  
- Any universal "G(x) = O(...)" closure presented as PGS prediction (classical shape; contract warning).  
- Legacy z_band "predictor" framing or confidence-bearing outputs inside generator stream.  

---

## Ranked Top 5 Strongest Candidates

1. **d4_count ordering carrier for next-triad state (mod30_prev_gap_exact)** — Strongest existing measured precedent. Exact surface, held-out protocol, decisive edge, fully PGS-native, ready for immediate extension to w-offset. Highest immediate publishable value.

2. **First-d=4 = GWR w under square exclusion** — Dominant regime, zero violations on massive ladder, direct w-position rule from visible pre-w structure. Extremely clean falsification surface.

3. **NLSC + lock_carrier / threat horizon post-w closure (type-specific)** — Proved foundation + generator runtime emission + d4-specific ceilings. Constrains the most important future state (next q after w).

4. **w-offset carrier from d4_count + square-phase + previous tail** — Explicitly recommended in the predictions contract as the minimal executable next step. Leverages existing generator emission (carrier_w) and 05 machinery.

5. **Previous-chamber reset-lock / carrier-shift / higher-divisor pressure transport** — Rich family of probe-supported hypotheses directly using transported PGS chamber invariants (lock, signature, shift) to constrain current w/boundary. Highest density of existing artifacts among open hypotheses.

All others (reset_signature modulation, excess-accumulation closure, gap-type grammar extensions, endpoint-chain transport, special-chamber unification, boundary-drop) are strong supporting surfaces that can be measured on the same retained catalogs or probe outputs.

---

**Path forward (per contract continuity question 4):** Instrument one retained-surface path (05-state-budget catalog or simple_pgs_generator) to emit w offset + square flag + reset_signature components. Run the exact d4_count held-out protocol on w-offset rules ("next w offset ∈ small set S or unresolved"). Record verdicts in identical language. All work stays inside research/16-predictions/ + parent chapter retained artifacts. Update this catalogue and the predictions index.html with new measured rows only after the gate passes.

**Reproduction of current state:**  
`python3 -m pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py -q`  
`cat research/16-predictions/pgs_predictions_v0.1_contract.html | grep -A 20 "Recommended First Pick"`  
`git status --short research/16-predictions/ research/05-state-budget/output/ research/01-generator/output/rule_x_logic_engine/`

All claims subordinate to PROOF.md for theorem status, AGENTS.md (local + canonical) for reasoning discipline, and exact artifact paths for measured status. No new theorems asserted here.

---

*End of catalogue. This document is the structured output of the mandated exhaustive GWR/DNI/generator prediction-candidate dive.*