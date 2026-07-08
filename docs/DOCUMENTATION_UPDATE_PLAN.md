# Documentation Update Implementation Plan

**Branch**: `documentation-updates-2026-07`
**Created**: 2026-07-08
**Base**: Current `main` (commit f01dc2ed9d04b243e72a97139e094929c8090619)
**Purpose**: Implement the documentation and presentation improvements identified in the 2026-07-08 review while preserving all rigor, proofs, examples, and technical depth.

---

## Goals

- Make the repository significantly more scannable, approachable, and professional for serious readers (number theorists, computational mathematicians, independent researchers) without any loss of rigor or substance.
- Explicitly separate proved local theorems from exploratory reading paths (especially RH bridge).
- Add clear entry points, tiered reading paths, a Key Concepts glossary, and a Quick Start section.
- Improve navigation across `docs/` and add standard repository files.
- Maintain the existing narrative voice and all concrete examples.

## Overall Verdict Alignment (from review)

| Area                    | Current Level | Room for Improvement | Effort | Priority |
|-------------------------|---------------|----------------------|--------|----------|
| Core content & proofs   | Excellent     | Low                  | -      | -        |
| Examples                | Very good     | Medium               | Low    | Medium   |
| Onboarding & clarity    | Good          | High                 | Medium | **High** |
| Navigation & structure  | Good          | High                 | Medium | **High** |
| GitHub polish           | Average       | High                 | Low    | High     |

Biggest gains: README tiering + glossary + proven/exploratory boundary + docs/ navigation hub.

---

## Phased Implementation Plan (Incremental & Testable)

### Phase 0: Branch Setup & Baseline (Done)
- [x] Create branch `documentation-updates-2026-07` from current main.
- [x] Place this plan file (`docs/DOCUMENTATION_UPDATE_PLAN.md`).
- Snapshot current state of README.md and PROOF.md (already reviewed via tools).
- Verify no breaking changes to existing code, proofs, or links.

### Phase 1: README.md Structural Overhaul (Highest Impact)
**Target file**: `README.md` (major edit on this branch)

**Sub-steps**:
1. Add badge row at top (MIT license, last updated, optional Python version or verification status).
2. Keep/promote hero image; add short **Abstract / Elevator Pitch** (2–4 sentences) immediately below it, including one-line status: "Local theorems proved + verified to 10¹⁸; RH bridge is a proposed reading path."
3. Add **Table of Contents** with anchor links.
4. Restructure into clear tiers:
   - **1. Quick Intuitive Understanding** (keep/improve existing contradiction + 23–29 and 89–97 examples; add plain-English takeaway for each).
   - **Key Concepts (Mini-Glossary)** — one-line definitions + intuition for GWR, DNI / zero-excess E(n), raw-Z maximizer, selected interior witness, bounded compression, Prime-Square Proximity Theorem, GWR super-signal.
   - **2. Core Results — What Is Proved** (explicit callout box or section: list GWR, next-prime rule, bounded compression, Prime-Square Proximity Theorem (2026-07-05), No-Later-Simpler-Composite Theorem (zero violations to 10¹⁸). Link to PROOF.md. State clearly what is formally proved vs. exploratory).
   - **3. Getting Started / Quick Start** (early, runnable commands: git clone, pip install -e ./src/python, example script that demonstrates the 23→29 gap or similar minimal demo).
   - **4. Deeper Theory & Formal Proofs** (links to PROOF.md + docs/core/ files with one-line purposes).
   - **5. PGS-to-RH Reading Path & Open Questions** (short bridge description; explicit status language: "Local source theorems proved. Downstream analytic consequences documented in docs/rh/ as a proposed path, not a claimed result." Link to docs/rh/README.md and pgs-unsolved-problems/).
5. Add **Repository Map** section (simple bullet list or ASCII tree describing src/, docs/core/, research/, visualizations/, lean-4/, experiments/, etc.).
6. Improve visual hierarchy throughout: shorter paragraphs, more bullets, horizontal rules, callout boxes for status/proved statements.
7. Keep all original examples, narrative, and technical depth intact.
8. Update Python API / installation section at end if needed for clarity.

**Success criteria for Phase 1**:
- New reader can grasp core claim + proved status in < 2 minutes.
- Proven vs. exploratory boundary is unambiguous on first read.
- All internal links remain valid.
- GitHub preview renders cleanly.

**Estimated effort**: Medium. Can be done in one or two focused commits.

### Phase 2: Standard Repository Files (Low Effort, High Polish)
Create on this branch:

- `CONTRIBUTING.md` — minimal but clear: signals openness to discussion/PRs even while primarily solo research; reference coding style from AGENTS.md or existing patterns; note preference for reproducible steps and rigorous validation.
- `CHANGELOG.md` — start with recent activity (theorem locking in PROOF.md, code optimizations) + this documentation update as the first entry under "Unreleased" or a new version section.
- `CITATION.cff` — standard Citation File Format for citable research software (title, authors, abstract, keywords from topics, license, repository URL, etc.). Useful for future referencing.

**Success criteria**: Files exist, are minimal but professional, and follow common open-source conventions without adding bureaucracy.

### Phase 3: docs/ Navigation Hub
Create:

- `docs/OVERVIEW.md` (or `docs/INDEX.md`) — master navigation document:
  - "Start here for core theorems and proofs"
  - "For the PGS-to-RH reading path, go to docs/rh/"
  - "Definitions and vocabulary live in ..." (link to any existing vocabulary/ or core/ files)
  - Brief one-paragraph map of each major subfolder (core/, rh/, research/, visualizations/, etc.)
  - Quick links to PROOF.md, AGENTS.md, visualizations/index.html, research/00-index/continuity/START_HERE.md

Update any top-level docs/README or index if present.

**Success criteria**: A new reader landing in docs/ immediately knows where to go for different depths.

### Phase 4: Visual, Accessibility & Minor Polish
- Review hero image and consider making it more prominent or adding a caption.
- Evaluate adding 1–2 small embedded visuals or links to key GIFs/plots from visualizations/ directly in the new README tiers (e.g., divisor-count progression).
- Add light audience framing if helpful (e.g., "For readers primarily interested in deterministic local theorems..." or keep minimal to avoid bloat).
- Audit all links in README and new docs/OVERVIEW.md.
- Optional: Minor wording tweaks in PROOF.md or AGENTS.md only if status language needs perfect synchronization (avoid substantive changes).

### Phase 5: Validation, Review & Merge Preparation
1. Run any existing tests or assertion scripts (`assert_results.tsv` context, scripts/ if relevant) to confirm no breakage.
2. Full self-review + agent review (following AGENTS.md contract) for consistency, link integrity, and tone.
3. Update this plan file with completion checkboxes.
4. Create pull request from `documentation-updates-2026-07` → `main` (or direct push if preferred for solo flow).
5. After merge: optional short note in research-meetings/ or continuity docs.

**Success criteria**: Merged cleanly; new structure measurably improves first-time comprehension and navigation while every original claim and proof reference remains untouched.

---

## Files to Create or Modify

**Modify**:
- `README.md` (primary target)

**Create**:
- `docs/DOCUMENTATION_UPDATE_PLAN.md` (this file — already done)
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `CITATION.cff`
- `docs/OVERVIEW.md` (or INDEX.md)

**Possibly minor touch**:
- `AGENTS.md` (only if new doc standards need referencing)
- `PROOF.md` (only status language sync if required — prefer not)

---

## Risks & Mitigations

- **Risk**: Over-editing reduces rigor or changes voice. **Mitigation**: All original examples, proofs, and technical content stay verbatim or minimally rephrased for flow. New sections are additive.
- **Risk**: Link breakage or navigation confusion during transition. **Mitigation**: Audit every link before merge; keep old paths working where possible.
- **Risk**: Scope creep into code or proofs. **Mitigation**: This branch is documentation-only. Any proof changes stay on main or separate branches.
- **Risk**: New files feel bureaucratic. **Mitigation**: Keep CONTRIBUTING/CHANGELOG/CITATION minimal and useful.

---

## Next Actions (After This Plan Is in Place)

1. Review this plan on the new branch.
2. Begin Phase 1: Draft revised README.md content (can be done here in conversation first, then committed to branch, or direct edit via tools).
3. Proceed phase-by-phase with incremental commits.
4. Full review + merge when ready.

---

**Status**: Plan created. Branch ready for implementation. Awaiting direction on whether to proceed with drafting the revised README.md content next.
