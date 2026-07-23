# TOP PRIORITY — Full Lean 4 core theorem stack (principal 2026-07-18)

**Status:** **DONE (program DoD M0–M5)** — recorded 2026-07-23  
**Set:** 2026-07-18 · **Exit:** M5 peer accept `lean-4/peer/M5_DOD_ACCEPT.md`  
**Source share:** https://grok.com/share/bGVnYWN5_281f9afa-6f68-4981-9e49-27781caa0b9b  
**Authority for theorems:** `PROOF.md` only (Lean is audit/verification, never promotes)  
**Program pin:** [ACTIVE_TARGET.md](../ACTIVE_TARGET.md)  
**Execution plan:** [lean-4/PGS_LEAN_FORMALIZATION_PLAN.md](../../../../lean-4/PGS_LEAN_FORMALIZATION_PLAN.md)  
**Contract:** [lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md](../../../../lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md)  
**HTML status:** [docs/lean-pgs-verification/index.html](../../../../docs/lean-pgs-verification/index.html)  
**HTML brief:** [../reports/lean-core-stack-priority/index.html](../reports/lean-core-stack-priority/index.html)
**Effort owner:** Hermes (principal 2026-07-18)  
**Definition of Done:** [lean-4/DEFINITION_OF_DONE.md](../../../../lean-4/DEFINITION_OF_DONE.md)  
**Inventory:** [lean-4/SORRY_AXIOM_INVENTORY.md](../../../../lean-4/SORRY_AXIOM_INVENTORY.md)  
**Owner charter:** [LEAN_CORE_STACK_OWNER_CHARTER_2026-07-18.md](LEAN_CORE_STACK_OWNER_CHARTER_2026-07-18.md)

## Owner DONE pin (D7.1)

| Field | Value |
| --- | --- |
| Program | Lean 4 core-stack formalization (GitHub #53) |
| Exit milestone | M5 (#59) |
| Status | **DONE** under D1–D7 |
| Peer accept | `lean-4/peer/M5_DOD_ACCEPT.md` |
| Merge SHA | `3d5b74c7` (PR #62 merge on `main`) |
| Date | 2026-07-23 |

Further analytic discharge of named packages is **extension** (DoD D7.3), not a reopening of this pin unless hollow-shell or silent-axiom regressions reappear.

## One-line goal

Complete a **machine-checked Lean 4 formalization of the entire core theorem stack** already proved in prose in `PROOF.md`, so the July 2026 foundation is auditable end-to-end without classical drift.

## In scope (core stack)

| Block | PROOF.md object | Lean home (current) |
| --- | --- | --- |
| Next-prime / tau-scan | Direct deterministic next-prime | `lean-4/PGS/NextPrime.lean`, ChamberReset weak L_FCL |
| GWR / Interior Maximizer | Leftmost min-divisor maximizer | `lean-4/PGS/GWR.lean` (**M3 closed**) |
| Universal bounded compression + PSP | Prime-Square Proximity + all-branch bound | `PGS/BoundedCompression.lean` (**M4 closed**, non-vacuous `C(n)`) |
| Supporting lemmas | Ordered Comparison, Witness Threshold, Short Divisor-Average, Large-Divisor Adjacent Closure, … | Basic + Placement + GWR (mapped; some still packaged) |
| Classical imports used as **audit premises** only | Bertrand, divisor-pair bound, prime-square divisor count | `Placement.lean` (Bertrand theorem; one audit axiom) |
| Finite bases (integration, not re-proof of bases as “Lean discovers” them) | gwr_finite_base_v1, bounded_compression_base_v1, residual_k128_v1 | `PGS/FiniteBases.lean` (**M5 closed**) |

## Explicit out of scope (do not steal this priority)

- Re-litigating proved theorems in `PROOF.md`
- Classical RH / PNT completion frames
- Claiming Lean output chooses primes (forbidden)
- Unilateral promotion of measured residuals to theorems
- Program-level “verified/validated” language without executed `10^18` surfaces where that policy applies
- RSA 50-bit residual discriminator (secondary track; see below)
- Agency revenue work (separate room)

## Secondary tracks (alive but not top)

| Track | Pin |
| --- | --- |
| 50-bit residual / joint cell C1T2L1 | [ACTIVE_GOAL_50bit_residual_discriminator.md](ACTIVE_GOAL_50bit_residual_discriminator.md) |
| Square-branch audit relay | `HOURLY_RELAY_CONTRACT.md` |
| New-theorem collab A/B/C | `experiments/pgs-new-theorem-collab-2026-07/` (hypothesis only) |

## Honest Lean state (implementation, not theorem status)

- Skeleton + smoke build path exists (`lean-4/README.md`).
- Some core statements still **axioms** / **sorry** / reflexivity stubs (e.g. PSP path, parts of Basic.tau characterization).
- L4 audit demotion and weak L_FCL exports exist as Lean mirrors under hypotheses.
- Mathlib usage is partial and must stay translation-only.

## Immediate next execution slices (ordered)

1. **Inventory:** machine-readable map of every `sorry` / `axiom` in `lean-4/PGS/*.lean` vs PROOF.md sections.
2. **Close Basic characterization:** `tau = 2` ↔ divisors `{1,n}` without sorry (gates GWR and next-prime).
3. **Discharge ChamberReset axioms** that are pure bookkeeping under existing hyps; keep PSP as derived only when modulus-link density lemmas are real, not fake.
4. **GWR Phase 3:** leftmost minimizer statement + ordered comparison chain mirroring PROOF.md.
5. **Certificate packaging:** types that *import* finite-base facts as hypotheses (not “proved by Lean from nothing”).
6. **HTML status surface** under `docs/lean-pgs-verification/` updated each milestone (theorem vs Lean-checked vs sorry).

## Status vocabulary (mandatory)

| Layer | Label |
| --- | --- |
| Core laws in PROOF.md | **theorem** (unchanged) |
| Lean mirror complete for a law | **implementation** / machine-checked audit |
| `sorry` / `axiom` remaining | **unresolved** Lean obligation |
| Priority choice | principal directive (this note) |

## Do not

- Edit `PROOF.md` theorem status without human-approved promotion.
- Flatten residual honesty to make Lean look green.
- Start from classical number-theory scratchpads before PGS objects.

*Principal: “I want this to be the top priority for the project” + Grok share URL, #Prime-Gap-Structure 2026-07-18. Hermes continuity pin.*
