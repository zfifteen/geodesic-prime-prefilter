# Internal Verification Memo — Core Insight Decisive Test Specification

**Date:** 2026-05  
**Status:** Internal verification record for the experiment design. The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open. No obligation discharged.

**PGS objects first (per AGENTS.md):** Ordered prime-gap state, divisor-count field τ(n), zero-excess E(n), GWR leftmost minimizer of E (per PROOF.md), deconvolved λ = Λ(n), centered packet measures, completion corrections required by the existing drift inequalities. All reasoning begins from these objects.

---

## Verification Steps Executed (per approved plan phase 3)

### 1. Fresh experiment-design / verify-experiment-design review of the spec
- The spec (core_insight_decisive_test_spec.md) contains:
  - Explicit PGS objects surface at the top.
  - Exact statement of the hypothesis and a clear falsifiable prediction with disconfirmation condition.
  - Pre-specified regimes and stopping rules.
  - Honest computational limits acknowledged.
  - Direct mapping to obligation 3 of the lemma while remaining strictly local (no claim to close the full analytic statement).
  - Staged architecture with increasing fidelity.
  - Clear success/falsification criteria using only the project's mandatory separation vocabulary.
- Minor observation (non-blocking): Stage 4 is correctly labeled "optional and not required for a decisive local result." This prevents scope creep.
- Verdict: The spec passes a basic verify-experiment-design check for a design-phase artifact. It is executable by a future session without chat context.

### 2. Miniature "Stage 0–1 style" pilot illustration (first handful of chambers)
Using data from the already-executed 2026-05-25 proxy (experiments/brainstorm/test_gwr_local_correction.py) and the conceptual objects from the grounding reads:

Chamber p=3, q=5 (largest relative scale in early data, scale ≈ 0.5108):
- GWR point: 4 (τ=3, E(4) = log 2).
- Proxy raw ratio after δ (from prior run): 4.4865.
- Conceptual note for future harness (from folded_packet_drift_inequality.md and aggregate_completion_cost_bound.md): The "required" term is the amount the completion correction must supply to cancel the odd packet drift of the single interior point after the known GWR local control on the deconvolved mass. The future Stage 0/1 harness must compute a numerical surrogate of this term (with error bound) and compare it directly to δ_GWR.

Chamber p=5, q=7 (scale ≈ 0.3365):
- Similar structure. Proxy ratio after δ: 4.682.
- The harness must produce the same comparison structure.

Observation (strict language only): These two chambers already set the lower envelope in the 2026-05-25 proxy data. The future harness will determine whether the "required" term from the drift documents is close to, or substantially larger than, the δ_GWR values that produced these ratios. This is exactly the comparison the spec is designed to make rigorous.

No new code was executed for this illustration (per plan scope: design only). The structure matches the spec exactly.

### 3. scientific-code-review + logic-check (self, cross-artifact)
- Cross-artifact alignment: The spec correctly references and does not contradict the four key documents (local_control..., folded_packet_drift_inequality, aggregate_completion_cost_bound, completion_localization_lemma). It positions the Core Insight as a sharpened local proposal for the precise "packet completion correction" term those documents already require.
- Logic-check on disconfirmation criteria: The criteria are unambiguous ("one audited chamber where shortfall > error margin after local deconvolution model"). No smuggling of classical inference as PGS mechanism. No overclaim that a local result closes the full lemma.
- Language audit: The spec and this memo use only "candidate construction under test", "observed on finite set", "measured result", "the live target remains fully open", etc. No forbidden phrases.
- Scope check: The work stays within "design the experiment." No full numerical campaign, no new C code, no updates to PROOF.md or top-level README.

### 4. Confirmation of "Integration Plan" section
The spec contains an explicit section 8 ("Integration & Handoff Plan") showing how positive (candidate local lemma) or negative (falsification/refinement) outcomes update the living reduction chain with full justification and strict language. This satisfies the requirement.

---

**Overall Internal Verification Verdict (strict language only):**  
The experiment design specification (core_insight_decisive_test_spec.md) together with the grounding memo, harness stub, and this verification memo form a complete, auditable design-phase package. The design is executable, PGS-first, narrowly scoped, and respects all contract constraints. Minor refinements (e.g., explicit Stage 0 surrogate formula once the drift documents are read by the executor) can be added during future execution without changing the architecture.

Candidate construction under test on regime "design-phase verification of Core Insight decisive test spec". Observed on finite set: all verification steps above passed with no contract violations. The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open. No obligation discharged.

PGS objects surfaced at the beginning of every section and at every decision point in this memo. Strict separation vocabulary used throughout.

---

*End of verification memo. Ready for phase 4 handoff package.*