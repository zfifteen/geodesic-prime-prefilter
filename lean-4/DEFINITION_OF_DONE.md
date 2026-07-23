# Lean 4 core stack — Definition of Done

**Owner:** Hermes (principal 2026-07-18)  
**Program:** machine-checked mirror of the **proved** core stack in `PROOF.md`  
**Authority:** `PROOF.md` for theorem status · this file for **when the Lean effort is done**  
**Contract:** `LEAN_PGS_VERIFICATION_CONTRACT.md`  
**Plan:** `PGS_LEAN_FORMALIZATION_PLAN.md`  
**Continuity:** `research/00-index/continuity/notes/TOP_PRIORITY_lean_core_stack_2026-07-18.md`

## Plain open

We are done when a cold checkout can build the Lean library and every core law
that is already proved in prose has a machine-checked statement with **no**
`sorry` and **no** hidden axiom that smuggles the theorem. Finite computational
bases stay **hypotheses** with clear names; Lean does not pretend to re-discover
them. `PROOF.md` is never rewritten by a green build.

---

## Definition of Done (program-level)

All of the following must hold together.

### D1 — Build gate

| ID | Criterion |
| --- | --- |
| D1.1 | `bash scripts/lean4-cache-build.sh` (or `cd lean-4 && lake build`) succeeds on a clean tree |
| D1.2 | `lake env lean smoke-test.lean` succeeds |
| D1.3 | CI or documented one-command repro in `lean-4/README.md` matches reality |

### D2 — Zero `sorry` on core path

| ID | Criterion |
| --- | --- |
| D2.1 | `rg 'sorry' lean-4/PGS/*.lean` returns **no** matches in core modules (`Basic`, `GWR`, `NextPrime`, `ChamberReset`, `Placement` as used by core) |
| D2.2 | Any remaining `sorry` lives only in explicitly labeled **scratch/** or **out-of-scope** files and is listed in the inventory as non-blocking |
| D2.3 | `rg -n '^\s*axiom ' lean-4/PGS/*.lean` returns **only** names listed in the current inventory as **audit premise** or **finite-base hypothesis**. Any other axiom → not done |

### D3 — Axiom policy (honest premises only)

| ID | Criterion |
| --- | --- |
| D3.1 | No `axiom` whose proposition is already marked **proved** in `PROOF.md` (headline stack **or** supporting lemmas in the core DAG: next-prime, GWR maximizer, UBC/PSP, and named supporting laws used to close them). Those must be **derived** `theorem`s with non-axiom proof bodies. |
| D3.2 | Allowed axioms/hypotheses only for: (a) classical comparison premises explicitly labeled audit (e.g. Bertrand if required) that PROOF.md itself treats as external, (b) **named finite-base packages** (`gwr_finite_base_v1`, `bounded_compression_base_v1`, `residual_k128_v1`) imported as hypothesis bundles, (c) pure definitional packaging that cannot smuggle a gap law |
| D3.3 | Every remaining axiom appears in `docs/lean-pgs-verification/` inventory with PROOF.md / RESULTS.md mapping and label **audit premise** or **finite-base hypothesis** |
| D3.4 | A core-stack row (D4.1–D4.5) is **not** closed if its proof is solely `exact <axiom>` / `apply <axiom>` with no further discharge. Such theorems count as **packaging wrappers** until the axiom is removed or reclassified under D3.2 and the row is re-proved |

### D4 — Core stack coverage (PROOF.md mirror)

Each row must be a Lean `theorem` (or equivalent) with proof, traced to PROOF.md:

| ID | Stack block | Done when |
| --- | --- | --- |
| D4.1 | **tau / DNI coordinates** | `tau`, prime characterization via `tau = 2`, and needed E/F/Z hooks without sorry |
| D4.2 | **Direct next-prime** | Statement mirrors PROOF.md hypotheses; proof closed under those hyps (weak L_FCL path discharged or replaced by full tau-scan mirror); not a pure axiom wrapper (D3.4) |
| D4.3 | **GWR / Interior Maximizer** | Leftmost min-tau maximizer formalized; Ordered Comparison (or equivalent) not sorry |
| D4.4 | **UBC + Prime-Square Proximity** | PSP and all-branch bound statements proved in Lean under the same finite premises PROOF.md uses — not reflexivity stubs |
| D4.4b | **Non-vacuous bounds** | Bound / proximity statements must match PROOF.md’s **non-vacuous** shape (fixed constant or explicitly named finite-base bound). Witnesses of the form `∃ C, dist ≤ C := ⟨dist, le_refl _⟩` (or `by rfl` on an unconstrained existential) are **empty shells** and fail DoD even if `sorry`-free |
| D4.5 | **Supporting lemmas** named in PROOF.md for the above | Witness Threshold, Short Divisor-Average (where still used), Large-Divisor Adjacent Closure, etc., as required by the proof DAG — each mapped; each is `theorem` with proof (D3.1) |
| D4.6 | **Finite bases** | Types/hypotheses package the certified bases; Lean does not claim to have proved the finite exhaustions from nothing |

### D5 — Traceability and status surface

| ID | Criterion |
| --- | --- |
| D5.1 | Every public theorem has a header: PROOF.md ref · supporting prose · status (proved mirror / audit premise / finite-base hyp) |
| D5.2 | Living map: `sorry`/`axiom` inventory file under `lean-4/` **and** HTML status under `docs/lean-pgs-verification/` |
| D5.3 | HTML opens in plain prose then technical detail (**second priority** readability); **no** reading-level meta-labels; does not rewrite `PROOF.md` |

### D6 — Contract compliance (non-negotiable)

| ID | Criterion |
| --- | --- |
| D6.1 | Lean never selects primes or feeds generators |
| D6.2 | No theorem status change in `PROOF.md` without human-approved promotion |
| D6.3 | No classical candidate-testing frame as PGS inference |
| D6.4 | No program-level “verified/validated” language that violates the `10^18` evidence policy for implementation claims |

### D7 — Owner acceptance

| ID | Criterion |
| --- | --- |
| D7.1 | Hermes records **DONE** on continuity pin + ACTIVE_TARGET with commit SHA / date |
| D7.2 | Peer adversarial pass (feynman kill-check + nie residual honesty + grok synthesis) finds **no open D1–D6 fail**. Peer kill-check at DONE must re-run D2.1 + D2.3 and spot-check D4.4b on PSP/UBC statements before accepting |
| D7.3 | Principal may still request more work; **program DoD** is met when D1–D7.2 hold even if principal asks for extensions later |

---

## Not done if

- Build is green but core theorems are axioms named like theorems
- PSP is “proved” by `rfl` / empty shell
- Existential bound is witnessed by the distance itself (`C := r^2 - p` and kin) — fails D4.4b
- Core `theorem` is only a wrapper around an `axiom` that carries the PROOF.md obligation (fails D3.4)
- Finite bases are silently assumed without labels
- Public status page claims Lean replaced `PROOF.md`
- `sorry` hidden behind `omit` or unbuilt files
- Unlisted `axiom` remains on core path (fails D2.3)

---

## Phased exit (milestones toward DoD)

| Milestone | Exit |
| --- | --- |
| **M0** | Inventory complete (this epoch) |
| **M1** | Basic tau characterization: **0 sorry** in `Basic.lean` for D4.1 |
| **M2** | ChamberReset / next-prime path: replay axioms discharged or reduced to D3-allowed hyps; D4.2 |
| **M3** | GWR maximizer closed (D4.3) |
| **M4** | UBC/PSP closed under honest premises (D4.4–D4.5) |
| **M5** | Finite-base packaging + HTML status + D1–D7 green |

Milestones are **implementation** exits, not new theorems.

---

## Baseline inventory (2026-07-18, pre-M1)

| Location | Obligation |
| --- | --- |
| `PGS/Basic.lean` | **M1 CLOSED** — 0 `sorry` (tau characterization path proved, 2026-07-20). No entry here. |
| `PGS/ChamberReset.lean` | **M2 CLOSED** — 0 `sorry`, 0 `axiom` (replay axioms discharged into proved theorems, commit `a96cb3e7`). |
| `PGS/Placement.lean` | axiom `tau_prime_square_eq_three` |
| `PGS/GWR.lean` | Phase 3 placeholder (coverage gap D4.3) |
| `PGS/NextPrime.lean` | **M2 CLOSED** — `weak_lfcl_sufficient_bound` fully proved and exported. |

Exact line map: `lean-4/SORRY_AXIOM_INVENTORY.md` (maintained each milestone).

---

*Owner: Hermes. Collab peers: grok (synthesis), feynman (mechanism kill-check), nie (honesty/residual of claims), agy (status HTML / dual-layer public surface). Principal confirmed priorities 2026-07-18.*
