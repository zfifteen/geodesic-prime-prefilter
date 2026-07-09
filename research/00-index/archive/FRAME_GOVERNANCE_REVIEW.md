FRAME_GOVERNANCE_REVIEW.md

Date: 2026-05-27
Status: Draft for review
Purpose: This document diagnoses a structural problem in the prime-gap-structure program and proposes concrete changes to governance. It operates at the program level only.

1. Diagnosis

The prime-gap-structure program has developed a self-sealing dynamic. Operational success in the generator, combined with strong purity enforcement and an archival reflex against material that risks "steering," has produced measurable stagnation in the rate at which new PGS objects and invariants are named and consolidated.

The program continues to generate correct deterministic next-prime records and maintain zero-failure audit surfaces. At the same time, empirically powerful mechanisms that emerged from the code are not being elevated to the status of first-class objects. The system is effective at reproducing and protecting its current frame while becoming progressively less effective at expanding or stress-testing that frame.

This is not a failure of individual reasoning or effort. It is an expected outcome of the current governance design.

2. Evidence of Symptoms

The following are observable and checkable:

- The carrier/lock_carrier/lower_d_threat mechanism inside pgs_chamber_reset_state_certificate (src/python/z_band_prime_predictor/simple_pgs_generator.py, lines 48 to 95) and its direct counterpart in pgs_certificate_t (src/c/high-scale-pgs/include/pgs_high_scale.h, lines 56 to 60) performs the actual recovery work when semiprime-shadow structures appear. This logic is load-bearing in production. It has no dedicated research card, no named rule, and no entry in pgs-unsolved-problems/.

- Dozens of narrow probe scripts have been written to mine variations of carrier, shadow seed recovery, transported threat, and boundary certificate behavior (examples: simple_pgs_carrier_boundary_certificate_probe.py, simple_pgs_shadow_seed_recovery_displacement_probe.py, simple_pgs_recursive_shadow_chain_state_mine.py, and multiple transported-sidecar probes in research/06-cryptology-rsa/). These probes generate data but have not produced corresponding named objects or invariants.

- The 2026-05 external archival of the entire research/12-rh-bridge track removed a large body of material on the explicit grounds that it created "persistent steering" and "prompt injection" (see research/00-index/status-map.md lines 32 to 34 and ARCHIVAL_HANDOFF.md in the external archive). No mechanism was left in place to keep the pressure visible inside the repository.

- The highest-level open question document (docs/unanswered-questions/chain-horizon-closure/00_question.md) describes the need for a divisor-horizon law and states specific performance figures (56.63% at 10^15, 58.00% at 10^18). The actual working solution path that the generator took (carrier-mediated cut after lock) was never abstracted or added to the unsolved-problems scaffold as a distinct object.

- Current routing documents (research/00-index/continuity/START_HERE.md and status-map.md) continue to list "chain-horizon closure / endpoint-chain / chamber reset" as the center of gravity, while the most interesting operational content of the chamber reset rule remains an unnamed implementation detail.

3. Root Cause Analysis

The self-sealing arises from three interacting design choices:

First, AGENTS.md and the continuity contracts successfully prevent the four canonical failures they were written to stop. They do this by making "PGS-native objects and invariants" the mandatory first frame for almost all reasoning. When combined with the archival reflex, this creates a strong negative feedback loop against naming mechanisms that first appear in code rather than in prior theoretical work.

Second, there is no sanctioned intermediate status between "implementation detail inside the generator" and "theorem recorded in PROOF.md." As a result, a working recovery rule such as the carrier/threat cut can remain in production for years without ever becoming a named PGS object with its own research obligations.

Third, generator correctness on large surfaces is treated, in practice, as validation of the broader theoretical frame. This reduces the felt urgency to consolidate or challenge the current object inventory even when the code has already moved beyond it.

The system is rational given its history of classical contamination. The cost of that rationality is the progressive narrowing of what counts as legitimate progress.

4. Trade-off Statement

Any structural change that increases the rate of object elevation and frame stress will increase the probability of classical drift, loss of PGS-native reasoning, and contamination of the generator contract.

The current system has protected the core contract ({"p": p, "q": q} output only, no source labels, no classical inference in selection) and has prevented the documented failure modes. There is no proposal that simultaneously accelerates theoretical consolidation and preserves the current level of protection. Any honest intervention requires accepting a higher short-term risk of the problems AGENTS.md was written to block.

5. Proposed Structural Interventions

Intervention A: Two-Track Governance
Create two explicitly separate rule sets.
- Purity Track: Current AGENTS.md and continuity rules remain in force. Owns the generator, PROOF.md, and all production artifacts.
- Pressure Track: Explicitly permitted to examine whether the current PGS object inventory is sufficient, using whatever methods surface the mismatch. All output must carry a "Pressure Track" label and cannot modify the generator or core theorems without a formal crossing review.

Intervention B: Mandatory Object Elevation Process
Create a required process (new document: research/00-index/object-elevation-process.md). Any mechanism that demonstrably affects generator behavior at scale (such as the carrier/threat cut) must be given a provisional name, a set of invariants (even if unproved), and an entry in pgs-unsolved-problems/ within a fixed time after its empirical importance is established. Status categories must include "empirically load-bearing, no proof yet."

Intervention C: Internal Quarantine Instead of External Archival
Replace external archival with a strict internal quarantine directory. Quarantined material remains searchable and citable by Pressure Track work. It is blocked from Purity Track influence without explicit review. The 2026-05 rh-bridge material would be the first candidate for return under this rule.

Intervention D: Periodic Frame Stress Tests
Add a recurring obligation (tied to major generator version freezes) to run deliberate exercises whose sole purpose is to find prime-gap phenomena that resist clean expression using the current listed PGS objects. Output format must include a mismatch table and a recommendation on whether the object inventory needs expansion.

6. Risks of Each Intervention

- Two-Track Governance: Risk of label leakage, eventual normalization of classical framing inside the main line, and increased coordination cost.
- Object Elevation Process: Risk of premature naming of weak patterns and creation of bureaucratic overhead that slows real work.
- Internal Quarantine: Risk that quarantined material still exerts steering through repeated reading and citation.
- Frame Stress Tests: Risk that the exercises become performative or are quickly routed back into existing objects.

7. Risks of Doing Nothing

If no structural change is made, the expected trajectory is continued growth in the number of specialized probes and diagnostic scripts, stable or slowly declining rate of new named objects, and gradual accumulation of unnamed but load-bearing mechanisms inside the generator. The program will remain capable of producing correct records while becoming less capable of understanding why they are correct at the level of explicit PGS laws.

8. Success Criteria and Measurement

After 12 months, the following would indicate the intervention is having effect:
- At least two mechanisms currently embedded in code (starting with the carrier/threat cut) have received provisional names and dedicated research cards with defined invariants.
- Pressure Track material exists and is being referenced without triggering automatic archival.
- The next major generator version freeze includes an explicit statement separating audit correctness from theoretical completeness.
- Frame Stress Test output has produced at least one documented proposal to expand the core PGS object list.

9. Implementation Path: Minimal First Step

The smallest real test is to draft and adopt the two-track rule set as a standalone document (research/00-index/two-track-governance.md) and run one Object Elevation trial on the carrier/threat mechanism inside the existing chamber reset rule.

This single action would force the program to decide, in public, whether the current most powerful recovery logic is allowed to become a named object or must remain an implementation detail.

10. Safeguards That Must Be Preserved

Even under any revised governance:
- The generator contract remains strict: only clean {"p": p, "q": q} records. No source labels, no confidence fields, no classical inference in selection.
- PROOF.md remains the sole authoritative source for theorem status.
- Purity Track work continues to follow AGENTS.md rules without exception.
- Any crossing from Pressure Track to Purity Track requires explicit, documented review.