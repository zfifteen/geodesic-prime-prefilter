# Core Insight Decisive Test Specification — GWR Local Correction vs. Packet Completion Correction Requirement

**Date:** 2026-05  
**Status:** Candidate experiment design under review. The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open. No obligation discharged.

**PGS objects first (per AGENTS.md):**  
- Ordered prime-gap state (consecutive endpoints p < q with interiors I).  
- Divisor-count field τ(n).  
- Zero-excess E(n) = (τ(n)/2 − 1) log n (E = 0 exactly at primes).  
- GWR / Leftmost Minimum-Divisor Rule (unique leftmost argmin E inside each chamber; maximizer of F = −E per PROOF.md).  
- Bridge load H(n) = log n + E(n).  
- Deconvolved signature λ = Λ(n) after Dirichlet deconvolution of H by D(s) = ζ(s)².  
- Centered packet measures, folded kernel contributions (1/(z + x²) kernels), and the completion corrections required by the existing reduction chain.  
- Live target: Chamber-Deconvolved Reciprocal Balance Lemma (obligations: deconvolution survival, reciprocal balance with no a ≠ 0 carriers, nonnegative folded mass as positive Stieltjes measure).

---

## 1. The Core Insight Hypothesis — Exact Statement

**Name:** Per-Chamber Positivity from the GWR Maximizer Identity.

**Claim (verbatim from originating context and 2026-05-25 ledger entry):**  
Local algebraic completion correction δ derived from E(g) at the unique GWR point g together with the endpoints p, q such that each sufficiently large chamber's corrected contribution to the folded kernel is ≥ k · log(q/p) for a fixed k > 0 independent of the chamber, *before any global summation*. This supplies a structurally direct local route to obligation 3 (nonnegative folded mass as positive Stieltjes measure) of the Chamber-Deconvolved Reciprocal Balance Lemma for large chambers (small chambers handled by finite direct verification).

**Falsifiable Prediction (operational form for this experiment):**  
For all chambers with log(q/p) above a fixed modest threshold (or n above a computable N0), the value of δ_GWR = E(g) · log(q/p) (or the minimal corrected functional form derived from the same GWR data) is sufficient to meet or exceed the local correction term required by the existing Folded Packet Drift Inequality and Aggregate Completion-Cost Bound after a high-fidelity *local* model of the deconvolution operator on the chamber packet, with the margin holding within explicit error bounds and without reliance on global cancellation from distant chambers.

**Disconfirmation Condition:**  
A single audited chamber (or explicit asymptotic family) in which, after application of the local deconvolution model with documented error bounds, the GWR-derived δ falls short of the correction required by the drift inequality (by more than the error margin) constitutes a falsification of the hypothesis in its stated simple local form.

---

## 2. Gap Analysis — Why the 2026-05-25 Proxy Was Insufficient for a Decisive Result

The lightweight probe (experiments/brainstorm/test_gwr_local_correction.py) used:
- Raw (non-deconvolved) packet sum only.
- Ad-hoc additive δ = E(g) · log(q/p) at fixed z = 1.0.
- No engagement with the actual objects appearing in the live reduction (deconvolved packet measure ν_{p,q}, completion corrections η, the precise drift inequality statements, required support separation for the negative folded-cost part).

Result on 2760 chambers: all ratios ≥ 4.4865 (positive measured result in the toy model).  
Limitation (recorded in the ledger entry): "It does not execute the actual Dirichlet deconvolution by D(s)=ζ(s)², does not apply analytic completion, and does not transport to the full Stieltjes representation on the completed side." Largest relative scales too modest.

The existing chain already contains the necessary framing:
- Local Control of Prime-Power Packets by GWR Ordering (GWR supplies concrete local control on deconvolved positive mass on P(p,q)).
- Folded Packet Drift Inequality (the exact inequality that must be satisfied after completion corrections cancel odd packet drift).
- Aggregate Completion-Cost Bound and Completion Localization Lemma (the "packet completion correction" term and its support requirements).

The Core Insight is a sharpened proposal for the *size and form* of precisely that completion correction term, derived locally from the already-proved GWR maximizer. A decisive test must compare the proposed δ directly against the correction *required by those inequalities* once a local model of deconvolution is included.

---

## 3. Staged Experimental Architecture (PGS-First, Falsification-Oriented)

**Stage 0 — Grounding & Baseline Diagnostics (short, low cost)**  
For every chamber in a chosen regime:
- Compute the numerical value of the "required completion correction" implied by the current statements of folded_packet_drift_inequality.md and aggregate_completion_cost_bound.md (or their direct numerical surrogates using the centered packet measure and K_z kernel).
- Compute δ_GWR = E(g) · log(q/p) using the exact GWR point.
- Record the ratio (required / δ_GWR) and the absolute difference.
- Produce diagnostic table + scatter (ratio vs. scale, ratio vs. E(g), etc.).

**Purpose:** Immediate quantification of how well the simple GWR form matches the correction already required by the existing theory. Any chamber where the ratio is consistently > 1 + ε with ε growing is an early warning.

**Stage 1 — Local Deconvolution Model (core engine)**  
Construct a high-fidelity but still *local* model of the effect of τ_Dir^{-1} on a single chamber packet P(p,q).
- Exploit the exact known action: λ(q) = log q, λ(r^a) = log r for interior prime powers.
- Use the GWR-selected minimum w to bound or approximate the inverse-D contributions on the interior support relative to the selected minimum (leveraging the local control already proved in local_control_of_prime_power_packets_by_gwr_ordering.md).
- For each chamber, compute (with explicit error bounds or interval arithmetic) the local contribution of the *deconvolved* packet to the folded drift before and after the proposed GWR δ.
- Test the concrete inequality: δ_GWR + (local deconvolved reserve) ≥ required drift cancellation term (from the existing inequality), within the documented error.

**Deliverable:** Reusable harness function that, given p, q (and optionally a z-grid), returns the comparison (margin, error bound, pass/fail at stated confidence).

**Stage 2 — Adversarial Search & Extreme Chambers (primary falsification engine)**  
- Ingest large-gap records (data/external/primegap_list_records_1e12_1e18.csv and extensions up to the largest feasible regime using C fallbacks when Python limits are hit).
- Prioritize stress-test chambers:
  - Record gaps at each scale.
  - Chambers with high τ contrast around the GWR point (possible small E(g) relative to width).
  - Chambers where the GWR point lies unusually close to one endpoint.
  - Any chambers near known difficult regions for explicit formulae or moment calculations.
- Run the Stage 1 model on the prioritized set.
- Any chamber in which the GWR δ is insufficient (margin negative beyond error) is a candidate falsifier. Each candidate receives a stricter-precision audit + cross-check against the exact text of the drift documents.

**Falsification Rule:** One audited counterexample in a documented regime, with the shortfall surviving stricter precision and exact-document cross-check, falsifies the hypothesis in its current simple form for that regime. The result is recorded as a measured falsification on that regime.

**Stage 3 — Theoretical Reduction & Chain Integration (the bridge to the lemma)**  
Using the numerical evidence:
- Attempt a short, PGS-native argument that the GWR maximizer property forces δ_GWR (or a minimal corrected form derived from the same objects) to be at least the local correction term required by the drift inequality.
- If successful, write the result as a new *candidate local lemma* ("GWR Local Completion Correction Lower Bound") with explicit hypotheses, cross-references to the four key docs, and the measured support from Stages 0–2.
- If the numerics indicate the simple E(g)·scale form is systematically short or requires an extra factor or different dependence on chamber geometry, propose the minimal corrected form and re-validate it through the same pipeline.
- Produce targeted updates or companion notes to folded_packet_drift_inequality.md, aggregate_completion_cost_bound.md, local_control_of_prime_power_packets_by_gwr_ordering.md, and completion_localization_lemma.md recording the outcome strictly as "candidate construction under test on regime X; observed on finite set; the live target remains fully open."

**Stage 4 — Scale & Partial Global Consistency (optional strengthening, not required for decisive local result)**  
For a small number of representative large chambers that survived Stages 1–3, embed the locally corrected packet into a truncated explicit-formula or short Dirichlet-series approximation and verify the sign of its contribution to a numerical proxy for S(z) or the measure. Document all limits honestly (as in prior Regime G reports). This stage can only strengthen confidence; a local falsification or local lemma from Stage 3 stands on its own.

---

## 4. Success / Falsification Criteria (Clear, Auditable, Respecting Separation)

**Falsification (decisive negative):**  
One (or more) audited chambers in a stated regime where, after the local deconvolution model with explicit error bounds, δ_GWR (or the best form derived from GWR data alone) is strictly insufficient relative to the correction required by the exact statements of the drift inequalities (shortfall > error margin). Recorded as: "Measured falsification of the simple local form on regime [description]; candidate refinement [if any] proposed; live target remains fully open."

**Support / Positive Measured Result (never overclaimed):**  
No counterexamples found up to a large stated regime + a proved (or candidate) short PGS-native lemma showing that the GWR maximizer forces the required local lower bound on the correction term. Recorded as: "Measured support on regime X + candidate local lemma Y (cross-referenced to existing drift documents); the live target (Chamber-Deconvolved Reciprocal Balance Lemma, all three obligations) remains fully open. No obligation discharged."

**Stopping Rules:**  
- Clear audited falsification in Stage 2 → halt search, write the falsification note, propose refinement if data suggests one, integrate into chain.
- Strong numerical support across regimes + successful short reduction in Stage 3 → write the candidate local lemma + integration notes.
- Computational limits reached before either outcome → honest "observed on finite set up to [limit]; no counterexample found; no local lemma proved; live target remains fully open."

All language in every artifact uses only the project's mandatory strict separation vocabulary.

---

## 5. Required New Artifacts (Minimal Scope)

**Primary Deliverable (this design's output):**  
`research/12-rh-bridge/docs/core_insight_decisive_test_spec.md` (this document, finalized after internal verification) or a companion self-contained HTML version if visual structure (tables, flow diagrams of the stages, comparison plots) is added.

**Minimal Supporting Code (harness interface sketch only — full implementation is future execution work):**  
- New or extended module (suggested location: research/12-rh-bridge/tools/gwr_delta_vs_drift_harness.py) exposing:
  - `compute_gwr_delta(p, q, tau)` → exact δ_GWR using the project's GWR selector.
  - `local_deconvolved_packet_contribution(p, q, z_grid, error_mode="bound"|"interval")` → approximation or bound on the local deconvolved contribution after the GWR δ.
  - `required_completion_correction_from_drift(p, q, z)` → numerical surrogate of the term required by the existing folded_packet_drift_inequality + aggregate bound statements.
  - `compare_margin(...)` → (margin, error_bound, pass/fail, diagnostics).
- Adversarial chamber sampler (prioritizing record gaps + structural extremes near GWR).
- Diagnostic CSV/JSONL + PNG generators (ratio vs. scale, absolute shortfall, etc.).

**Documentation Integration Artifacts (produced only on real outcome):**  
- Candidate local lemma note (if Stage 3 positive).
- Falsification or refinement note (if negative or partial).
- Targeted annotations or companion paragraphs for the four key docs.

**Verification Artifacts:**  
- Internal review records (verify-experiment-design pass, scientific-code-review, logic-check) attached to the final spec.
- Short execution ledger entry in the appropriate LOOP_LEDGER or proof-construction log.

**Explicitly Out of Scope for This Design Phase:**  
Full multi-stage numerical campaign on 10^6+ chambers, new C/GMP sieves (unless the pilot immediately requires them), updates to PROOF.md or the top-level README, any claim that the result closes any part of the lemma.

---

## 6. Verification Plan for This Specification Itself

Before the design is considered complete and handed off:

1. Fresh review of this spec using the experiment-design / verify-experiment-design lens: pre-specified regimes, exact predicates, honest limits, PGS-first structure, direct mapping to lemma obligations.
2. Miniature pilot of Stage 0 + Stage 1 entry point on the first ~100–200 chambers using existing tools + the harness sketch. Confirm output format and language match the spec.
3. scientific-code-review of the spec + cross-artifact alignment with the four key drift/control documents.
4. logic-check that the disconfirmation and support criteria are unambiguous and do not smuggle classical inference or overclaim.
5. Confirmation that the spec contains an explicit "Integration Plan" section showing how positive or negative results update the living chain without violating separation.

All verification artifacts themselves use strict language and PGS objects first.

---

## 7. Risks & Mitigations (Addressed in Design)

- Global transport intractability: Core test kept strictly local (deconvolution effect on one packet + direct comparison to already-local drift inequalities). Stage 4 global check is optional and clearly labeled as strengthening only.
- Simple δ form only approximately correct: Stage 3 explicitly includes "propose minimal corrected form derived from the same GWR data" as a first-class outcome.
- "Definitive" impossible for a fully analytic claim: The design defines "decisive within the project's standards" (clear audited counterexample or new candidate local lemma with measured support + explicit hypotheses). This matches the treatment of all prior toy/regime results.
- Language or scope drift: PGS Guardian (or automated checks) on every artifact; second-opinion gate on any claim that the result "advances the lemma" rather than "advances a local candidate lemma."
- Hypothesis true only via global cancellation: If numerics show repeated local shortfall, this directly falsifies the "before any global summation" clause and is recorded as such.

---

## 8. Integration & Handoff Plan

On completion of a decisive run (future execution of this spec):
- Positive local lemma or strong support → new candidate note + targeted updates to the four key docs + entry in the appropriate ledger + possible recommendation to the autonomous loop for further proof work on the candidate lemma.
- Falsification or clear shortfall → falsification/refinement note + same integration path.
- In all cases: the primary spec + all pilot data + verification records + ledger entry form the handoff package. The live target remains fully open unless and until a separate, audited proof artifact closes one or more obligations of the full lemma.

**Future executor note:** This spec is designed to be read and executed by the existing autonomous research loop infrastructure (or a subagent) without chat context. All decision points, language rules, and stop conditions are explicit.

---

**Live Target Statement (mandatory closing):**  
The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations: deconvolution survival, reciprocal balance with no a ≠ 0 carriers, nonnegative folded mass as positive Stieltjes measure) remains fully open. This document designs an experiment only. No obligation is discharged. No claim is made that the Core Insight has been validated or falsified at the level of the analytic lemma.

PGS objects surfaced at every decision point in this specification. All language is restricted to the project's strict separation vocabulary. 

---

*End of specification draft. Internal verification steps (phase 3 of the governing plan) to be executed on this document before final handoff.*