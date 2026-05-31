# Endpoint-Chain, Modulus-Link, Chamber-Reset, Reciprocal-Transport and Structural-Certificate Prediction Candidates

**PGS Predictions Catalogue • research/16-predictions/catalogue/**  
**Branch context:** predictions  
**Date of catalogue:** 2026-05-30  
**Governing contracts:**  
- research/16-predictions/pgs_predictions_v0.1_contract.html (definition of Predictions)  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/AGENTS.md (PGS-first reasoning, deterministic only, state separation)  
- research/00-index/continuity/START_HERE.md and continuity_and_shape_contract.md  
- PROOF.md (theorem status control)  
- research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ (primary measurement surfaces)  

**Scope:** Exhaustive search of endpoint-chain traversal, chamber-reset geometry (including carrier_w / reset signatures / tail / threat), modulus-link (floor transport + reciprocal endpoint closure), reciprocal transport, structural certificates (PGSPG reset certificates), and adjacent cryptology / unsolved-problem boundary surfaces for deterministic forward-resolution carrier laws.  

**Definition of a PGS Prediction (verbatim from contract):** A deterministic rule or measurable carrier law, built only from already-proved or explicitly measured PGS objects (divisor-count field, DNI coordinate E(n), GWR leftmost-minimizer w, endpoint chains, modulus links, chamber-reset signatures, reciprocal transport), that from the current chamber state (or a short, fully determined preceding window) either resolves one or more future PGS states exactly (position of next w, next gap type after w, next chamber-reset signature, next modulus-link residual, etc.), or returns an explicit unresolved state when the carrier does not decide.  

**Strict constraints observed:** Zero probabilistic language. Zero classical factoring framing as inference. All reasoning begins from PGS objects → invariants → rules → resolved / unresolved / invalidated state. Classical methods appear only in downstream audit or explicit comparison roles. All claims separated by: theorem proof (PROOF.md), implementation status, measured result (exact regime), audit result, hypothesis, unresolved state, invalidated rule.  

**Core proved foundation (PROOF.md):** Direct deterministic next-prime rule via exact divisor-count traversal; Interior Maximizer Theorem (GWR: w is the unique leftmost minimizer of τ inside the gap interval, equivalently unique maximizer of F(n) = −E(n)). No-Later-Simpler-Composite corollary. These are universal under stated hypotheses; finite surfaces (through 10^18) certify implementation only.  

**Precedent measured carrier (research/05-state-budget, referenced in predictions contract):** d4_count ordering carrier under mod30_prev_gap_exact match mode on retained 8192-row-per-power 10^12..10^18 surface yields ordering_carrier_found (decisive pairs 7881, edge +69 over control, 6/7 positive held-out folds). Uses exact match-mode + held-out protocol. This is the shape template for all Predictions-track carriers.  

**Primary active surfaces inventoried:**  
- research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ (README.md, ALGORITHM.md, PGS_CERTIFICATE.md, METRICS.md, RECURSIVE_ENDPOINT_CHAIN_DESIGN.md, STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md, SESSION_BOOTSTRAP.md, output/*.jsonl with live certificate rows).  
- pgs-unsolved-problems/endpoint-determinacy/ (boundary-drop probes tied to rsa-v2 survivors).  
- pgs-unsolved-problems/gilbreath/, divisor-field-extremals/, legendre/, brocard/, polignac-twin/ (reset/boundary/endpoint probes).  
- Generator emission sites: src/python/z_band_prime_predictor/simple_pgs_generator.py (pgs_chamber_reset_state_certificate + chamber_reset_fields), src/c/high-scale-pgs/include/pgs_high_scale.h (pgs_certificate_t), src/c/high-scale-pgs/src/pgs_chamber.c.  
- Governance / elevation: research/00-index/OBJECT_ELEVATION_PROCESS.md, FRAME_GOVERNANCE_REVIEW.md, TWO_TRACK_GOVERNANCE.md, research/00-index/status-map.md, PLAN.md, research/16-predictions/index.html and README.md, research/06-cryptology-rsa/README.md and docs/endpoint_structure_law.md and docs/cryptology/pgs_cryptologic_implications_whitepaper.md.  
- Chain-horizon open question: docs/unanswered-questions/chain-horizon-closure/00_question.md and related.  
- Additional mentions across research/00-index/, research/12-rh-bridge/README.md (archival routing), docs/ (lean plan, gap-structure-factor-brief-evidence, app-ideas).  

No GRAMMAR*.md at rsa-v2 root; grammar evidence lives in separate artifacts (PGS_GRAMMAR_EVIDENCE_FINDINGS.md etc.) under the grammar track and is treated as measured evidence only, not resolver.

---

## Catalogued Candidate Surfaces

### 1. w-Position Carrier from Current-Chamber d4_count + Carried Chamber-Reset Signature (Family 1)

**Exact PGS objects + invariant:** Ordered divisor-count field of the gap after p (specifically d4_count under square exclusion); GWR-selected w (carrier_w); square-phase flag; previous-gap tail length; active chamber-reset signature carried forward (carrier_d, lock_carrier_d, tail_after_reset_offsets, reset_deadline). The offset w − p is a deterministic function of the local structure visible before or at the first d(n)=4 arrival plus any active chamber-reset or modulus-link signature carried from the previous gap. Returns small integer set of possible offsets or explicit unresolved.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/pgs_predictions_v0.1_contract.html:84-86 (native statement and generator note: "The generator already computes carrier_w (or equivalent) as part of chamber-reset state").  
- Same file:71-77 (d4_count precedent), 105-107 (recommended first pick: Family 1 + d4 precedent on retained surfaces).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/index.html:122 (PGS objects including endpoint chains, chamber-reset geometry), 135 (chamber-reset determinacy rules), 175 (endpoint-chain + modulus-link closure).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/src/python/z_band_prime_predictor/simple_pgs_generator.py:142 (carrier_w emission in certificate), 32-166 (full pgs_chamber_reset_state_certificate and chamber_reset_fields).  

**Status (measured on what regime? hypothesis?):** Hypothesis / extension of measured precedent. d4_count ordering carrier already measured on retained 8192-row 10^12..10^18 surface (ordering_carrier_found verdict). Generator v1.1 emits carrier_w inside every chamber-reset certificate on all tested surfaces through 10^18+ (zero unresolved in core generator contract). No universal w-offset carrier rule yet proved or measured at scale in Predictions track. Explicitly "not proved" per contract section 5.

**Proposed first concrete test / falsification surface:** Instrument one of the existing retained-surface generators (or simple_pgs_generator path) to also emit w offset alongside d4_count and chamber metadata. Run identical match-mode + held-out fold protocol on modest retained window (e.g. 1024 rows per power 10^12..10^15). Record carrier strength for "next w offset lies in stated small integer set S" rules. Return verdict in d4_count language (ordering_carrier_found / does_not / unresolved). Reproduction: python3 -m pytest research/05-state-budget/tests/... (per contract). Falsify by exact hit-rate + unresolved-rate on ch05 surfaces; no probability claims.

**Why this is high-value for deterministic prediction:** Directly implements the "Recommended First Pick (Minimal Executable Path)" in the Predictions v0.1 contract. Leverages already-proved GWR + No-Later-Simpler-Composite + existing chamber-reset emission machinery. Smallest step that produces a new, publishable, fully auditable carrier surface using the exact established measurement contract. Supplies concrete forward resolution of next selected integer (w) position from prior-chamber invariants.

**Drift risks:** Reframing the carrier as a statistical model or "on average" predictor; beginning the rule derivation from classical density assumptions instead of the divisor-count field + carried reset signature; promoting finite-surface hit rates to universal theorem without PROOF.md entry; conflating with legacy z_band predictor directory.

### 2. Chamber Reset Carrier Cut / GWR Threat Closure (lock_carrier + lower_d_threat) — Object Elevation Candidate

**Exact PGS objects + invariant:** Inside pgs_chamber_reset_state_certificate: carrier_offset / carrier_d (first min-d>2 after p, i.e. GWR w); lock_carrier_offset / lock_carrier_d (first resolved-survivor that captured a carrier); lower_d_threat_offset (first post-lock offset with divisor_count >2 and strictly < lock_carrier_d). The threat forces tail rejection after lock (final_status = REJECTED for offsets > threat); this cut, combined with tail_after_reset_offsets and reset_deadline, closes the chamber or resolves the next reset point deterministically. "No later simpler composite" after w is already proved; the threat supplies the operational cut that realizes it under semiprime-shadow pressure.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/src/python/z_band_prime_predictor/simple_pgs_generator.py:48-95 (carrier computation loop 71-76, lock 80-87, threat 90-95; exact: "if divisor_count > 2 and divisor_count < lock_carrier_d"), 121 (carrier_w = p + carrier_offset), 127-149 (return of full certificate with carrier_w, lock_*, lower_d_threat_offset, tail_after_reset_offsets), 160-166 (chamber_reset_fields).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/src/c/high-scale-pgs/include/pgs_high_scale.h:55-62 (pgs_certificate_t: tail_after_reset_count, carrier_offset, carrier_d, lock_carrier_offset, lock_carrier_d, lower_d_threat_offset).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/src/c/high-scale-pgs/src/pgs_chamber.c:17-23 (candidate_state_t mirroring carriers), 26+ (certificate construction).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/00-index/OBJECT_ELEVATION_PROCESS.md:22 ("The carrier/lock_carrier/lower_d_threat logic inside pgs_chamber_reset_state_certificate meets all four triggers and is the first required candidate"), 17-22 (triggers: >10% chambers, multiple probes, difference in unresolved rate, Pressure Track mismatch).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/FRAME_GOVERNANCE_REVIEW.md:19 (exact cites to python 48–95 and C header 56–60; "performs the actual recovery work when semiprime-shadow structures appear. This logic is load-bearing in production. It has no dedicated research card, no named rule, and no entry in pgs-unsolved-problems/"), 25 (links to chain-horizon question figures 56.63% at 10^15 / 58.00% at 10^18; carrier-mediated cut was the working solution never elevated).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/00-index/TWO_TRACK_GOVERNANCE.md:80 (first Pressure Track exercise on this mechanism).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/ (survivor/inference rows contain the fields; e.g. coordinate_start... jsonl examples with "carrier_w", "reset_signature", "tail_after_reset_offsets", "lower_d_threat_offset": null in calibration rows).  

**Status (measured on what regime? hypothesis?):** Empirically Load-Bearing, No Proof Yet (per OBJECT_ELEVATION_PROCESS status categories). Active in production generator v1.1 and high-scale C path on all surfaces through 10^18+ (and 10^1233 endpoint in C). Responsible for near-zero unresolved rate in core contract. Multiple independent probes (simple_pgs_*_probe.py files, rsa-v2 transported probes) converge on carrier/threat patterns. No theorem in PROOF.md; no named object or unsolved-problems entry. Hypothesis for explicit "Chamber Reset Carrier Cut Rule" or "GWR Threat Closure" with provisional invariants. Invalidated old fixed-cutoff map {2:44,4:60,6:60} remains invalidated.

**Proposed first concrete test / falsification surface:** Execute Object Elevation Process (OBJECT_ELEVATION_PROCESS.md steps): provisional name + ordinary-language description + formal definition + provisional invariants + status declaration + dedicated pgs-unsolved-problems/ entry + one-page elevation card. Add falsification probe on retained ch05 surfaces: given lock_carrier state + local d-field, predict threat_offset location and tail rejection behavior exactly; measure exact match rate + unresolved rate. Cross-apply to rsa-v2 survivor rows (check whether transported threat discriminates true/false positives). Run narrow generator tests before/after any naming.

**Why this is high-value for deterministic prediction:** Directly supplies the operational mechanism that realizes proved No-Later-Simpler-Composite under shadow pressure; the actual load-bearing recovery rule inside every chamber reset. Its elevation would convert an unnamed impl detail into a first-class PGS object with research obligations, enabling explicit carriers for next reset point, threat presence, or tail length from current-chamber invariants. FRAME review identifies it as the concrete content behind the high-level "chain-horizon closure" open question. Predictions-track unification target for w-position, excess closure, and cross-modulus residual state.

**Drift risks:** Leaving it as "implementation detail" indefinitely (governance self-sealing per FRAME); classical reframing of the threat cut as a divisibility test or factor heuristic; using its empirical success to claim universal bounds without PROOF.md path; prompt-injection via archived rh-bridge material.

### 3. Reciprocal Deadline-Signature Correction (Endpoint-Class Resolver in Modulus-Linked Chains)

**Exact PGS objects + invariant:** PGSPG reset certificate (reset_endpoint, reset_deadline_value, reset_signature = "carrier_d=...;lock_carrier_d=...;threat=...;deadline=..."); oriented transport coordinate x (reset_endpoint if <= sqrt orientation else anchor); y = floor(N / x); upper certificate derived at previous public endpoint before y; correction: z = floor(N / upper.reset_endpoint), c = previous before z, d = upper.reset_deadline_value. Resolves to endpoint_class_by_reciprocal_deadline_signature_correction iff c < lower.anchor and d > upper.reset_endpoint and floor(N / c) == d and signatures match. Returns explicit unresolved otherwise.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/PGS_CERTIFICATE.md:53-60 (correction logic), 8-29 (full certificate fields including carrier_w, reset_deadline*, reset_signature).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ALGORITHM.md:149 ("for strict reset closure or nonzero endpoint-chain correction"), 176-200 (closure statuses including endpoint_class_by_reciprocal_deadline_signature_correction, unresolved_by_endpoint_chain_*).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/METRICS.md:46-49 (Resolved closure states), 18-42 (survivor rows carry full lower/upper/corrected certificates + rule_id).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/RECURSIVE_ENDPOINT_CHAIN_DESIGN.md:44-46 (closure predicates), 39-48 (latent PGS objects: previous public endpoint chain, PGSPG reset certificate, oriented transport, reciprocal floor transport).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/README.md:27 (required frame), 39-50 (Endpoint Structure Law: reciprocal deadline-signature correction).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/docs/endpoint_structure_law.md:35- (oriented transport + law).  
- pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility-probe.py:44-49 (selected_cell using "endpoint_class_by_reciprocal_deadline_signature_correction" and corrected_lower/upper_endpoint).  
- Same dir *.json: "public_closure_status", "promoted_by_boundary_drop", "boundary_drop_closure".  

**Status (measured on what regime? hypothesis?):** Measured implementation + hypothesis for stronger carrier. Live in rsa-v2 runner on public ladder_cases.jsonl (40/50/64-bit static cases and beyond). Survivor rows and summary.json record closure_status and full certificates. Boundary-drop admissibility probed on emitted deadline-signature cells (true in sampled 40/50/64-bit rows; "promoted_by_boundary_drop": true but "current_rows_export_boundary_drop": false). No universal modulus-link resolution theorem; explicit unresolved states emitted. Audit downstream only.

**Proposed first concrete test / falsification surface:** On expanded public RSA ladder or synthetic moduli derived from retained prime-gap chambers, measure exact rate of deadline-signature correction success vs unresolved_by_endpoint_chain_*; test whether adding transported carrier_w / tail overshoot (see candidate 6) increases resolution rate on the same surface. Propose boundary-drop promotion rule as extension and falsify on the probe data + new cases. Use only public inputs + PGS certificate derivation + floor arithmetic; downstream audit for factor presence.

**Why this is high-value for deterministic prediction:** Provides exact, scale-independent deterministic resolution of paired endpoints across a modulus link (floor transport) using only carried reset signatures and reciprocal conditions. The correction rule is already a concrete carrier that turns prior-chamber state (lower cert) into future endpoint class without search. Directly embodies the cryptology contract frame. Extensible to multi-step chain traversal and cross-gap modulus-link residuals in ordinary prime-gap sequences.

**Drift risks:** Treating floor(N / ·) transport as classical search or candidate generation; claiming "factors found" from closure_status instead of explicit unresolved + downstream audit separation; generalizing measured rates on small-bit ladder to RSA-scale without new surfaces; allowing legacy prefilter logic to leak into the certificate path.

### 4. Strict Mutual Reset Closure and Oriented Multi-Step Endpoint-Chain Traversal

**Exact PGS objects + invariant:** Previous-public-endpoint chain (a_{k+1} → previous before a_{k+1}); PGSPG reset certificate L_k at each (anchor, reset_endpoint, carrier_*, reset_signature, tail_*); oriented transport x_k; y_k = floor(N / x_k); upper cert; closure when floor(N / L.reset_endpoint) == U.reset_endpoint (and reverse) and signatures equal (strict mutual) or the deadline correction variant. Chain walker continues until documented closure predicate or explicit boundary/cycle unresolved state. Same predicates apply uniformly at every step.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/RECURSIVE_ENDPOINT_CHAIN_DESIGN.md:52-60 (unified recursive/iterative skeleton over oriented transported certificate chain state), 39-48 (object inventory), 20-34 (current OECC_LINEAR_V1 vs required scale-indep form).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/ALGORITHM.md:53-80 (Uniform Chain State, oriented lower transport coordinate choice), 176-200 (endpoint_class_by_oriented_endpoint_chain_closure, unresolved_by_endpoint_chain_boundary / cycle).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/SESSION_BOOTSTRAP.md:276 (endpoint-chain traversal for recursion layer), 448 (FrontierCommit from public endpoint-chain transport).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/coordinate_start_certificate_acquisition_probe/acquisition_rows.jsonl (concrete rows with "endpoint_chain_steps", full "coordinate_story" containing carrier_w, reset_signature, tail_after_reset_offsets, reset_endpoint).  
- research/16-predictions/* (multiple references to multi-step endpoint-chain traversal closure).  

**Status (measured on what regime? hypothesis?):** Measured on rsa-v2 ladder and diagnostic probes; design analysis exists for fully recursive scale-independent formulation (no bit-size branching). Current runner mixes direct-transport and while-loop chain walker. Grammar evidence track (component sharing, inverse recursive grammar, lag-2/3 exclusions) is separate measured evidence (48 solved rows etc.), not part of the resolver. Explicit unresolved states defined.

**Proposed first concrete test / falsification surface:** Implement the unified recursive/iterative skeleton from RECURSIVE_ENDPOINT_CHAIN_DESIGN.md on the existing runner; re-run on current ladder + larger-bit public cases; record exact step count to closure, unresolved rate, and whether transported carrier/tail fields (STEP2 analysis) predict closure success earlier in the chain. Falsify uniformity claim by checking identical relational rules on 40-bit vs 2048-bit synthetic cases. Add to Predictions-track retained-surface protocol.

**Why this is high-value for deterministic prediction:** The multi-step chain is the natural generalization of single reciprocal correction. A scale-independent carrier law here would resolve sequences of future endpoints (or certify structural certificates) from an initial locked chain state using only PGS certificate fields + floor arithmetic. Directly supports Predictions definition for "next modulus-link residual" and "subsequent endpoints".

**Drift risks:** Early-exit control flow that encodes bit-size logic instead of PGS object structure; reviving radius-first or budgeted-walk scaffolds already withdrawn; treating grammar exclusion findings as inference rules rather than measured evidence.

### 5. Transported Carrier_w / Tail Overshoot as Discriminator in Reciprocal Modulus-Link Closure

**Exact PGS objects + invariant:** Lower-certificate internal points (locked carrier_w, tail_after_reset_offsets) transported by floor(N / x) to upper side; comparison of transported position against upper_anchor and upper_carrier_w (overshoot distance). Differential overshoot (true-positive cases land +14..+16 above upper structures; false +30..+32) supplies deterministic signal for closure success or failure before full upper certificate evaluation.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/06-cryptology-rsa/experiments/live-solver/rsa-v2/STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md:1-20 (title, focus on "Reciprocal transport behavior of lower certificate internal points (carrier_w and tail offsets)", table with exact 50-bit false / 64-bit true overshoot numbers, observation on 2× differential).  
- Same file and rsa-v2/PGS_CERTIFICATE.md (carrier_w, tail fields defined and transported).  
- rsa-v2/output/ rows containing the fields for the analyzed cases.  
- Cross-references in RECURSIVE... and ALGORITHM to carrier inside certificates.  

**Status (measured on what regime? hypothesis?):** Measured observation on specific 50-bit false-positive and 64-bit true-positive rsa-v2 cases (and calibration rows). Hypothesis for carrier-transport discriminator usable in closure predicates or early pruning of chain steps. Not yet folded into main runner or Predictions measurement protocol.

**Proposed first concrete test / falsification surface:** Reproduce STEP2 analysis on full rsa-v2 survivor set + new ladder cases; quantify overshoot delta as function of lower carrier_d / lock state / tail length; test whether a threshold on overshoot (derived only from lower certificate) predicts correction success with exact hit/unresolved counts on held-out cases. Add the transported-carrier feature to the d4-style retained-surface protocol for ordinary gaps (map gap chambers to synthetic moduli).

**Why this is high-value for deterministic prediction:** Demonstrates that the already-emitted carrier_w and tail fields inside a chamber-reset certificate are not mere diagnostics; when reciprocally transported they carry forward-resolving information about the opposite-side structure. Supplies a concrete, arithmetic-only mechanism for "next modulus-link residual" state prediction. Bridges ordinary prime-gap chamber resets to cross-modulus endpoint-chain work.

**Drift risks:** Interpreting overshoot as a probabilistic confidence score; allowing the transport step to become a search over candidate offsets; drift from PGS certificate fields into classical remainder analysis.

### 6. Boundary-Drop Endpoint Promotion / Admissibility Rule for Reciprocal Cells

**Exact PGS objects + invariant:** Emitted (or corrected) endpoint cells (L, U) from deadline-signature correction; boundary-drop behavior under T_N = floor(N / ·) vs T_{N-1} = floor((N-1) / ·); if the N-minus-one images also satisfy mutual floor closure on the adjacent cell, the boundary-drop promotes the cell (or supplies an additional deterministic promotion rule for endpoint-class resolution).

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility-probe.py:43-60 (selected_cell on reciprocal_deadline... status using corrected_lower/upper_endpoint; bridge_lemma on N vs N-1).  
- Same dir 2026-05-20-boundary-drop-admissibility-probe.json:6- (rows with "boundary_drop_closure": true, "promoted_by_boundary_drop": true, "current_rows_export_boundary_drop": false, "T_N_lower", "T_N_minus_1_*", "mutual_floor_closure").  
- 2026-05-20-boundary-drop-admissibility.html (probe report title and findings).  
- Linked to rsa-v2 survivor rows and PGS_CERTIFICATE deadline correction.  

**Status (measured on what regime? hypothesis?):** Probe measured on three rsa_v2 static cases (40/50/64-bit). boundary_drop_closure true and promoted_by true in observed rows for deadline-signature cells; however current survivor rows do not export a boundary-drop or N-minus-one transport certificate field. Hypothesis for new public endpoint-cell promotion rule "unless the transported certificate law derives it." Inference boundary: probe measures already-emitted/rejected cells only; audit_only_residual not used for promotion.

**Proposed first concrete test / falsification surface:** Extend the probe to the full rsa-v2 survivor set and larger public cases; decide whether to add boundary-drop fields to the certificate emission (PGS_CERTIFICATE.md update); falsify admissibility by checking whether promoted cells remain consistent with strict reset-closure or deadline-correction predicates on new data. If admitted, measure resolution-rate lift on the same surfaces.

**Why this is high-value for deterministic prediction:** Directly tests whether an additional deterministic arithmetic relation (N vs N-1 floor cells) on already-resolved reciprocal endpoint cells supplies extra forward resolution power or tighter closure conditions. Lives entirely inside the transported-certificate / modulus-link frame. Natural extension of the existing deadline-signature law.

**Drift risks:** Using the probe to promote endpoints before the core certificate law is satisfied; conflating audit residuals with public certificate fields.

### 7. Chamber-Reset Signature Carried Forward for Next-Chamber Excess Closure or Reset Location (Family 2 extension)

**Exact PGS objects + invariant:** Cumulative excess ΣE(n) (or max local E) from w onward; square-phase terminal behavior; active chamber-reset lock (carrier state, tail policy); reset_deadline_value / margin. These force the next return to E=0 (next prime) or next reset point before a deterministic threshold derived only from divisor-field invariants and carried signature for that chamber type. Already-proved No-Later-Simpler-Composite supplies one exact closure; stronger type-specific bounds remain open.

**File:line citations:**  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/pgs_predictions_v0.1_contract.html:88-91 (Family 2 native statement; warning against classical O(log x) form), 49 (resolves next chamber-reset signature).  
- /Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/index.html:135 ("Chamber-reset determinacy rules that locate the next reset point from current-chamber invariants alone").  
- Generator certificate fields (simple_pgs_generator.py:140-146, 163) supply the carried signature (tail_after_reset, carrier_*, reset_deadline).  
- rsa-v2 certificate transport shows the same fields crossing modulus links.  

**Status (measured on what regime? hypothesis?):** Proved base (No-Later-Simpler-Composite) + measured carrier precedent (d4) + hypothesis for stronger carried-signature closure rules. Generator already closes every chamber using these fields. No type-specific deterministic threshold stated beyond the proved corollary.

**Proposed first concrete test / falsification surface:** On retained ch05 surfaces, given current d4_count + square-phase + incoming chamber-reset signature (carrier_d, tail length, deadline margin), predict exact upper bound on steps to next E=0 or next reset_offset; measure exact hit rate of the bound (or small set of possible offsets) vs unresolved. Use same match-mode protocol.

**Why this is high-value for deterministic prediction:** Extends the proved interior maximizer directly into forward prediction of closure using the very signature the generator already emits. Unifies ordinary gap closure with the reset-determinacy and modulus-link residual questions listed as open in 16-predictions/index.html.

**Drift risks:** Classical analytic framing of the bound; treating the carried signature as a statistical feature rather than deterministic carrier.

### 8–11. Additional Boundary / Reset / Reciprocal Surfaces in pgs-unsolved-problems/ (Falsification Regimes)

**Gilbreath Reset-Stop-Wall Classification (reset stop walls as chamber-reset boundary phenomena):**  
Objects: reset stop walls, classification via PGS chamber resets / carrier state.  
Citations: pgs-unsolved-problems/gilbreath/2026-05-20-reset-stop-wall-classification.html, 2026-05-20-reset_stop_wall_probe.py, summary.json.  
Status: Measured probe + classification on specific surfaces. Hypothesis for PGS-visible invariants governing stop-wall locations.  
Value: Independent falsification regime for any chamber-reset carrier or reset-determinacy rule.  
Drift: Conflating Gilbreath conjecture framing with PGS inference.

**Higher-Tau Reciprocal Blockers (divisor-field extremals):**  
Objects: higher-τ positions as reciprocal blockers in modulus links or endpoint chains.  
Citations: pgs-unsolved-problems/divisor-field-extremals/2026-05-20-higher-tau-reciprocal-blockers.html + probe.py + output json/csv.  
Status: Probe on reciprocal blockers.  
Value: Tests limits of reciprocal transport closure when high-τ positions appear in the divisor field.

**Legendre Residual-Endpoint Quarter-Frontier + NLSC-Deadline Bridge:**  
Objects: residual endpoints, quarter-frontier, NLSC-deadline bridge falsification, deadline values in certificates.  
Citations: pgs-unsolved-problems/legendre/ (2026-05-20-residual-endpoint-quarter.html, residual_endpoint_quarter_probe.py, 2026-05-14-nlsc-deadline-bridge-falsification.html).  
Status: Falsification probes on deadline and residual behavior.  
Value: Direct pressure on reset_deadline and residual endpoint carriers.

**Brocard / Polignac-Twin Boundary Exposure (half-wall endpoints, lag2 boundaries):**  
Objects: half-wall endpoints, lag-2 boundary exposure in twin/polignac settings, reciprocal transport within chambers.  
Citations: pgs-unsolved-problems/brocard/ (half-wall-endpoint-probe.*), polignac-twin/ (lag2_boundary_exposure_probe.py + output ranked_lag2_pairs.csv etc.).  
Status: Probes on boundary and lag phenomena.  
Value: Additional concrete regimes for testing carrier predictions of endpoint or boundary locations.

(Full indices and outputs in each subdir supply exact measured rows for falsification.)

### 12. d4_count Ordering Carrier Precedent + Unification Surface (Template + Cross-Chapter)

**Exact PGS objects + invariant:** Count of d(n)=4 positions in current chamber under fixed match mode; predicts ordering of next triad (or, by extension, w or reset signatures).  
Citations: research/16-predictions/pgs_predictions_v0.1_contract.html:71-77 (strongest existing precedent, exact verdict language); research/05-state-budget/ (retained surfaces and tests).  
Status: ordering_carrier_found on 10^12..10^18 retained surface.  
Value: Supplies the exact measurement protocol, match-mode discipline, and verdict language that every new carrier (w-position, threat cut, transported overshoot, reset-determinacy) must use. Unification target for Family 1/2/3/4 in the contract.  
Test: Extend the existing test_state_budget_divisor_carrier_sweep.py to the new carriers above.

---

## Top 5 Ranked Opportunities

**Rank 1: Chamber Reset Carrier Cut / GWR Threat Closure (Candidate 2)**  
Highest leverage because it is already load-bearing production logic (python lines 48–95 + C struct 56–60), responsible for the generator's near-zero unresolved rate under shadow pressure, and is explicitly called out by FRAME_GOVERNANCE_REVIEW.md and OBJECT_ELEVATION_PROCESS.md as the first required elevation target. Elevating it converts an unnamed detail into a named PGS object with invariants, directly addressing the operational solution to the chain-horizon-closure question (docs/unanswered-questions/chain-horizon-closure/00_question.md) while supplying a concrete carrier for next-reset location and tail behavior. All other carriers can be stated in terms of it. Citations across generator, governance, and rsa-v2 data are exact and recent (2026-05).

**Rank 2: w-Position Carrier from d4_count + Carried Reset Signature (Candidate 1)**  
The contract's own "Recommended First Pick (Minimal Executable Path)". Smallest delta from existing proved GWR + measured d4 precedent + generator emission (simple_pgs_generator.py:142). Uses the exact retained-surface + match-mode + held-out protocol already validated on 10^12..10^18. Delivers immediate forward resolution of the next selected integer (core PGS object) and is the natural unification point for Families 1–4. Lowest implementation risk, highest publishable output velocity.

**Rank 3: Reciprocal Deadline-Signature Correction + Transported Carrier_w Overshoot (Candidates 3 + 5)**  
The strongest existing concrete deterministic resolver across modulus links (rsa-v2/ALGORITHM.md, PGS_CERTIFICATE.md, STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md with exact differential overshoot data). Embodies the full cryptology contract frame (research/06-cryptology-rsa/README.md:27). The STEP2 transported-carrier observation shows that certificate-internal PGS fields (carrier_w, tail) already carry predictive power when reciprocally transported. High value for both RSA-scale structural certificates and ordinary gap cross-chamber modulus-link residuals. Falsifiable on public ladder + retained surfaces with zero classical search.

**Rank 4: Oriented Multi-Step Endpoint-Chain Traversal + Unified Recursive Skeleton (Candidate 4)**  
The natural generalization that turns single reciprocal corrections into full chain resolution. RECURSIVE_ENDPOINT_CHAIN_DESIGN.md gives the exact latent PGS object inventory and scale-independent skeleton required. Current runner (OECC_LINEAR_V1) is correct but non-uniform; completing the recursive form yields a carrier law for arbitrary-length future endpoint sequences. Directly supports Predictions-track open items on multi-step closure (16-predictions/index.html:134).

**Rank 5: Boundary-Drop Promotion Rule + Supporting Unsolved-Problems Falsification Surfaces (Candidates 6 + 8–11)**  
The endpoint-determinacy probe supplies a clean, narrow hypothesis (N vs N-1 floor behavior on already-resolved reciprocal cells) that is immediately testable against live rsa-v2 survivors. The full set of pgs-unsolved-problems/ reset/boundary probes (gilbreath reset-stop-wall, legendre residual-endpoint + NLSC-deadline, higher-tau reciprocal blockers, brocard half-wall, polignac lag2 boundaries) constitute independent, high-quality falsification regimes for any carrier law proposed on chamber-reset signatures, transported endpoints, or reciprocal residuals. Elevating or refuting on these surfaces protects the Predictions track from over-generalization while expanding the measured evidence base.

---

**Next actions (per contract and continuity files):**  
1. Read this catalogue + pgs_predictions_v0.1_contract.html + PROOF.md + AGENTS.md.  
2. Choose Rank 1 or 2 for first pressure (object elevation card or w-carrier instrumented probe).  
3. Run the narrow relevant test (generator pytest or rsa-v2 focused command per status-map) before claiming progress.  
4. Write important state (new invariants, falsification results, elevation card) into repository artifacts.  
5. Preserve separation: theorem / measured / hypothesis / unresolved at every step.

All claims subordinate to PROOF.md for theorem status and to AGENTS.md / local Agents.md for reasoning discipline. This catalogue itself is a measured research artifact, not a proof.

**Absolute path of this report:** /Users/velocityworks/IdeaProjects/prime-gap-structure/research/16-predictions/catalogue/endpoint-chain-modulus-link-prediction-candidates.md

**End of catalogue.**