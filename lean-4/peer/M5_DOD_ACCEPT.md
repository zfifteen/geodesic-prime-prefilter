# M5 DoD acceptance — peer adversarial pass

**Date:** 2026-07-23  
**Milestone:** M5 (program Definition of Done exit)  
**Parent:** GitHub #53 · Sub-issue #59  
**Inventory:** `lean-4/SORRY_AXIOM_INVENTORY.md`  
**DoD:** `lean-4/DEFINITION_OF_DONE.md`  
**Peers:** feynman (kill-check), nie (honesty), grok (synthesis) · **Owner:** Hermes  

---

## Mechanical re-check (D7.2 required)

| Gate | Command / inspection | Result |
| --- | --- | --- |
| D2.1 zero `sorry` | `rg 'sorry' lean-4/PGS/*.lean` | **PASS** — no matches |
| D2.3 axiom allowlist | `rg -n '^\s*axiom ' lean-4/PGS/*.lean` | **PASS** — only `Placement.tau_prime_square_eq_three` (audit premise CL-003) |
| D4.4b non-vacuous PSP/UBC | Inspect `PGS.BoundedCompression.prime_square_proximity_theorem` and `universal_bounded_compression` | **PASS** — bound is `C(n) = max(64, ⌈½(log n)²⌉)`, not `∃ C, dist ≤ C := dist` |
| D1 build | `cd lean-4 && lake build` | **PASS** |
| D1 smoke | `lake env lean smoke-test.lean` | **PASS** |

---

## D1–D7 scoreboard (M5)

| ID | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| D1.1 | `lake build` green | **PASS** | M5 branch build (3072 jobs) |
| D1.2 | smoke test | **PASS** | `smoke-test.lean` loads library |
| D1.3 | README repro | **PASS** | `lean-4/README.md` one-command path matches |
| D2.1 | no core `sorry` | **PASS** | rg empty |
| D2.2 | scratch-only sorry | **PASS** | core clean; scratch non-blocking |
| D2.3 | axiom allowlist | **PASS** | one audit axiom inventoried |
| D3.1 | no axiom = proved law | **PASS** | core theorems are derived / packaged under hyps |
| D3.2 | finite-base packages | **PASS** | `PGS/FiniteBases.lean` named bundles |
| D3.3 | inventory mapping | **PASS** | inventory + HTML finite-base table |
| D3.4 | no pure axiom wrappers on D4 rows | **PASS** | replay discharged; UBC/PSP use named hyps + assembly |
| D4.1–D4.4b | core stack | **PASS** | M1–M4 closed |
| D4.5 | supporting lemmas mapped | **PASS** | traceability table in HTML (status labels honest) |
| D4.6 | finite bases packaged | **PASS** | `FiniteBaseBundle` + certificate ids/hashes |
| D5.1–D5.3 | traceability + HTML | **PASS** | headers + status surface; plain prose first |
| D6.1–D6.4 | contract | **PASS** | audit-only; no PROOF.md theorem rewrite; no 10^18 inflation |
| D7.1 | owner DONE pin | **PASS** | continuity note + this accept file with SHA at merge |
| D7.2 | peer pass | **PASS** | this document; H1 empty-shell counterexample retired |
| D7.3 | extensions optional | **PASS** | program DoD met; further formalization is extension |

---

## Retired kill-check counterexamples (feynman 2026-07-18)

| Historical attack | Status at M5 |
| --- | --- |
| H1 empty-shell PSP | **Retired** — theorem removed; non-vacuous `C(r*r)` assembly |
| H2 axiom-wrapped next-prime | **Retired** — M2 discharged replay axioms |
| H3 GWR placeholder | **Retired** — M3 maximizer packaging |

---

## Honesty residuals (nie)

- Finite bases remain **hypotheses** linked to certificates; Lean does not re-prove exhaustions.
- `SquareBranchCapacityContra` and `AnalyticUBCClosure` are named analytic packages for assembly, not silent smuggling of PROOF.md as an `axiom` named like a theorem.
- `tau_prime_square_eq_three` stays **audit premise** only.
- Program language: machine-checked **mirror** / assembly under premises — not program-level “validated” implementation claims.

---

## Owner record (D7.1)

**Status: DONE (program DoD for Lean core-stack formalization M0–M5).**  

| Field | Value |
| --- | --- |
| Main merge | `3d5b74c7` (PR #62) |
| Parent issue | #53 closed DONE |
| Sub-issue | #59 closed completed |
| Continuity pin | `TOP_PRIORITY_lean_core_stack_2026-07-18.md` |

*Peer adversarial pass: no open D1–D6 fail at M5.*
