# Formalization Proposal — Derived Half-Coefficient Finding

**Date:** 2026-07-08  
**Chapter:** `research/18-derived-half-coefficient/`  
**Authority:** `PROOF.md` (universal bounded compression, proved 2026-07-05)

---

## 1. What We Are Formalizing

The **program breakthrough** is not the bound itself (already proved in
`04-bounded-compression`). It is the **derivation narrative**:

> The factor `0.5` in `C(q) = max(64, ⌈0.5 · log(q)²⌉)` emerges from
> divisor-average geometry (`H ≲ L²/8`), not from fitting Cramér's conjecture
> or the critical line.

Three layers must stay separated in every artifact:

| Layer | ID | Status | Must not be conflated with |
|-------|-----|--------|----------------------------|
| Derived coefficient | F18-001 | **proved** | RH, Cramér conjecture |
| Independent audit | F18-002 | **measured** | Universal proof |
| Critical-line rhyme | F18-003 | **hypothesis** | F18-001 |

---

## 2. Formalization Options

### Option A — Minimal pointer (low effort, weak stewardship)

Add one paragraph to `research/04-bounded-compression/README.md` and link
`PROOF.md`. No new chapter.

**Verdict:** Insufficient for a breakthrough finding.

### Option B — Layered research chapter (recommended)

Dedicated chapter with finding statement, derivation digest, external validation,
hypothesis lane, and 30/30/30 bundle.

**Verdict:** **Recommended** (this folder).

### Option C — Lean-first extraction

New Lean module `PGS.BoundedCompression.HalfScale`.

**Verdict:** Phase 3 follow-on.

### Option D — Standalone publication note

PDF-ready note sourced from the 30/30/30 bundle.

**Verdict:** Phase 4 deliverable.

---

## 3. Phased Execution Plan

### Phase 1 — Canon (complete)

- [x] Chapter scaffold + docs + 30/30/30 bundle
- [x] Git commit (persistence fix)

### Phase 2 — Reproducible audit (next)

- [ ] `scripts/gwr_bound_audit.py`
- [ ] `output/gwr_bound_audit_summary.json`
- [ ] Pytest gate

### Phase 3 — Formal mirror

- [ ] Lean `half_scale_emergence` in `PGS.Analysis`

### Phase 4 — External dissemination

- [ ] Standalone publication note

---

## 4. Acceptance Criteria

**F18-001:** Finding locatable in `FINDING_STATEMENT.md`; `0.5` traceable to
`PROOF.md` in ≤2 hops; no RH claims without correct status label.

**F18-002:** Pinned audit script reproduces zero-violation table.

**F18-003:** Hypothesis doc lists falsifiable predictions; boundaries explicit.