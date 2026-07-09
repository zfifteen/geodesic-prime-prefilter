# PROOF.md Enhancement Goals

**Created:** 2026-07-07  
**Parent:** [README.md](./README.md) · **Inputs:** [shortcomings.md](./shortcomings.md)

---

## Mission Statement

Produce a hardened `PROOF.md` where every universal claim is established as:

1. **Analytically proved** with no informal steps, or  
2. **Explicitly finite-certified** with pinned, reproducible artifacts.

…and where a gap-free Lean 4 mirror is a realistic downstream target, not a contradiction of the prose.

---

## Status Vocabulary (Target)

Enhancement work should migrate `PROOF.md` to a consistent multi-axis status model:

| Axis | Values | Meaning |
|------|--------|---------|
| **Logical status** | `proved` · `finite-certified` | How the claim is established |
| **Scope** | `universal` · `finite` · `residual` · `corollary` | Quantifier range |
| **Formalization** | `lean-mirrored` · `lean-partial` · `in progress` · `not-started` | Downstream Lean state |

Example:

> **Interior Maximizer Theorem** — logical: `proved` (finite base + analytic closure) · scope: `universal` · formalization: in progress

---

## Goals by Priority

### Tier A — Unblock formalization and external review

#### G1 — Close the Prime-Square Proximity analytic gap (S1)

**Objective:** Replace lines 665–666 with a complete proof of the square-branch bound

```text
r² - p ≤ max(64, ceil(0.5 · log(r²)²))
```

**Acceptance criteria:**

- [x] Modulus-link / tiling collision step has formal definitions (M-rough rows, admissible ℓ, collision predicate)
- [x] Counting or density argument is explicit inequalities, not prose metaphor
- [x] Lean `prime_square_proximity_theorem` can state the real bound (not trivial `C = r² - p`)
- [x] `near_root_exclusion_bound` integrates as a named sub-lemma with cross-reference

**Deliverables:** `PROOF.md` patch · optional `docs/proof-enhancements/psp-closure/` working notes

---

#### G2 — Harden or reclassify Twin-Prime Resonance (S2)

**Objective:** Either prove rigorously or downgrade status.

**Acceptance criteria (if kept as theorem):**

- [x] “4+ zeros ⟺ w ≡ 0 (mod 30)” proved by exhaustive case analysis on the defined remainder vector
- [x] Step 3 replaced: explicit lemma that if g > 2 and w ≡ 0 (mod 30), then ∃ n ∈ I with τ(n) < τ(w)
- [x] No “overwhelmingly” / “inevitably” language in proof body

**Acceptance criteria (if reclassified):**

- [ ] Moved to separate “Derived Signals” section with `measured` or `hypothesis` status
- [ ] Theorem stack table updated

---

#### G3 — Epistemic separation of finite bases (S3, P1)

**Objective:** Restructure `PROOF.md` so universal theorems cite finite bases as **certified premises**, not inline prose.

**Acceptance criteria:**

- [x] New section: **Certified Finite Bases** with uniform statement template
- [x] Each base lists: range, count checked, failure count, artifact path, reproduction command, date/hash
- [x] Theorem stack uses multi-axis status (see vocabulary above)
- [x] Headline section distinguishes three pillars from two certified finite inputs

---

### Tier B — Reproducibility infrastructure

#### G4 — Unified finite-lemma certificate schema (R2)

**Objective:** Define a JSON (or similar) certificate format for all finite-base claims.

**Minimum fields:**

```json
{
  "lemma_id": "gwr_finite_base_v1",
  "range": { "p_min": 2, "p_max_exclusive": 5000000001 },
  "counts": { "gaps": 220336055, "earlier_integers": 826172972, "failures": 0 },
  "generator": { "script": "...", "commit": "...", "params": {} },
  "artifact_hash": "sha256:...",
  "verified_at": "ISO-8601"
}
```

**Acceptance criteria:**

- [ ] Schema documented in `docs/proof-enhancements/certificate-schema.md`
- [ ] At least one existing script emits conforming certificates
- [ ] `PROOF.md` references certificates by `lemma_id`

---

#### G5 — Pin reproduction commands in PROOF.md (R1, R3)

**Objective:** Every audit table row links to a one-command reproduction.

**Acceptance criteria:**

- [ ] GWR finite base table → command + artifact
- [ ] Bounded-compression base → command + artifact
- [ ] K=128 residual table → command + artifact
- [ ] 10¹² stress sample → command + artifact
- [ ] CI or makefile target `verify-proof-certificates` (optional stretch)

---

### Tier C — Structural hardening (clarity, Lean portability)

#### G6 — Explicit classical lemma appendix (S5, S6)

**Objective:** Collect imported classical facts with audit labels.

**Candidates:**

- Bertrand postulate (for `q < 2p`)
- τ(n) ≤ 2√n (divisor-pair bound)
- τ(r²) = 3 for prime r > 1
- Infinitude of primes / existence of next prime

**Acceptance criteria:**

- [x] Appendix section with statement, usage locations, audit status (`classical-import`) — Bertrand CL-001 in `PROOF.md` §Imported Classical Lemmas (#31)
- [x] No classical lemma buried inline without pointer — Bertrand usages link to CL-001 (#31)
- [x] CL-002 divisor-pair bound in `PROOF.md` §Imported Classical Lemmas (#32)
- [x] CL-003 `τ(r²)=3` for prime `r` in `PROOF.md` §Imported Classical Lemmas (prose); Lean discharge pending M1

---

#### G7 — Proof spine map (navigation)

**Objective:** One-page dependency graph: which lemmas depend on which finite bases and classical imports.

**Acceptance criteria:**

- [ ] `docs/proof-enhancements/proof-spine.md` with DAG or table
- [ ] Linked from `PROOF.md` document status section
- [ ] Mirrors planned Lean module hierarchy

---

#### G8 — Boundary and claims discipline (P2, P4)

**Objective:** Make limitations visible at point of use, not only in disclaimer.

**Acceptance criteria:**

- [ ] Pillar 3 repeats prefix-attainment boundary at theorem statement
- [ ] Document status footer tracks enhancement phase (e.g., “PSP analytic closure: open”)
- [ ] Cramér-scale wording paired with “selected witness offset w − p” every time

---

#### G9 — Residual K=128 scope fencing (S4)

**Objective:** Prevent over-interpretation of K=128 as global.

**Acceptance criteria:**

- [ ] Hypothesis block at theorem statement listing exact windows and divisor-count pairs
- [ ] Explicit “does not imply” list retained and echoed in theorem stack
- [ ] Cross-link to elimination artifact table with certificate ids (G4)

---

### Tier D — Lean alignment (downstream of prose hardening)

#### G10 — Lean feasibility gate per theorem

**Objective:** Before Lean work on a `PROOF.md` section, prose must pass a gate.

| Gate | Requirement |
|------|-------------|
| L-G1 | No informal steps in prose |
| L-G2 | Finite claims have certificates (G4) |
| L-G3 | Classical imports listed (G6) |
| L-G4 | `proof-spine.md` entry exists |

**Acceptance criteria:**

- [ ] `docs/proof-enhancements/lean-readiness.md` table maintained
- [ ] `docs/lean-pgs-verification/` updated from this table, not ahead of it

---

## Phased Roadmap

| Phase | Focus | Goals | Exit criterion |
|-------|-------|-------|----------------|
| **0** | Audit | Shortcomings + goals documented | This folder complete |
| **1** | Epistemic hygiene | G3, G6, G8, G9 | `PROOF.md` status model + appendix draft |
| **2** | Reproducibility | G4, G5 | Certificates exist for all finite tables |
| **3** | Mathematical closure | G1, G2 | PSP + twin-prime resolved (prove or reclassify) |
| **4** | Navigation | G7, G10 | Spine map + Lean readiness table green for pillars 1–2 |
| **5** | Lean mirror | (separate track) | Gap-free Lean for proved spine |

**Rule:** Phase 5 does not start on a section until Phase 3 or honest reclassification clears that section.

---

## Non-Goals (Explicit Scope Boundaries)

- **Not** rewriting proofs that are already sound (ordered comparison, divisor tail, short average lemma, etc.)
- **Not** proving RH, PNT, or classical Cramér for raw gaps — boundary stays
- **Not** merging cryptology/RSA endpoint work into `PROOF.md`
- **Not** using Lean to discover new mathematics — prose leads, Lean mirrors
- **Not** replacing finite bases with unverified analytic shortcuts unless a new proof is actually written

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Informal proof steps in universal claims | 0 |
| Finite tables with pinned certificates | 100% |
| Theorem stack rows with multi-axis status | 100% |
| Items with Lean formalization in progress | 100% |
| External reviewer can reproduce finite bases in one command | Yes |

---

## Immediate Next Actions

1. Review and prioritize S1 vs G3 (mathematical closure vs epistemic hygiene first)
2. Draft `certificate-schema.md` when starting G4
3. Create `lean-readiness.md` stub mapping each `PROOF.md` section to shortcomings IDs
4. Open `PROOF.md` patch PR only after Phase 1 goals have agreed wording for status vocabulary