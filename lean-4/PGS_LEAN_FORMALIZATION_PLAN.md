# PGS Lean 4 Formalization Plan

**Document Status**: Living plan. Version 1.0 (Skeleton Phase)  
**Created**: 2026-05-27  
**Owner**: PGS Project (with formalization sub-track)  
**Related Contracts**:
- `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md` (binding)
- `docs/AGENTS.md`
- `research/00-index/continuity/continuity_and_shape_contract.md`
- `PROOF.md` (single source of truth for theorem status)

---

## 1. Purpose of This Plan

This document provides the phased roadmap, scope boundaries, traceability strategy, and success criteria for the Lean 4 formalization effort.

Its existence is required by project documentation standards: any significant new track (especially one involving proof assistants) must have an explicit planning artifact before substantial code is written.

## 2. High-Level Goal

Produce a high-fidelity, machine-checked mirror of the two core universal theorems proved in `PROOF.md`:

1. **Direct deterministic next-prime theorem via tau-scan**: Given a prime `p`, there exists a unique next prime `q` that is selected by the ordered divisor-count chamber state and the PGS selection rule.
2. **GWR / Leftmost Minimum-Divisor Rule maximizer theorem**: The selected composite `w` inside a prime gap is the unique leftmost interior integer that minimizes `tau(n)` (equivalently, uniquely maximizes `F(n) = −E(n)`).

The Lean work is **verification and audit only**. It increases confidence in the existing prose proofs and provides a foundation for future large-scale mechanical checking of the empirical surfaces in `docs/RESULTS.md`. It does **not** replace `PROOF.md`, the Python reference implementation, or the generator contract.

## 3. Guiding Principles (Repeated for Emphasis)

- **PGS-First Entry Point** at every layer of the formalization.
- **Strict state separation** in all artifacts and comments.
- **1:1 traceability** back to exact locations in `PROOF.md` + supporting prose documents.
- **No classical drift**: Mathlib is a translation tool, not an oracle that chooses PGS outputs.
- **Narrow scope**: We formalize what is already proved in prose, plus only the minimal supporting infrastructure required to express it faithfully.
- **HTML status surface required** for any public or review-facing documentation of this track.

## 4. Detailed Outline of the Formalization Effort

This section is the master outline. It will be expanded into actual Lean modules and mirrored in the required HTML status document.

### 4.1 Phase 0: Scaffolding & Contracts (Current: Skeleton Complete)

**Deliverables**:
- Top-level `lean-4/` folder
- `lean-toolchain` + `lakefile.lean` (pinned to v4.30.0 + Mathlib)
- `LEAN_PGS_VERIFICATION_CONTRACT.md`
- `PGS_LEAN_FORMALIZATION_PLAN.md` (this document)
- Minimal `PGS/Basic.lean` with `tau`, `E`, `F`, `Z`
- `lean-4/README.md`
- Updates to root `.gitignore`
- Supporting entry in `research/00-index/status-map.md`
- Optional: initial self-contained `docs/lean-pgs-verification/index.html` skeleton

**Acceptance Criteria**:
- `lake build` succeeds (once environment is set up).
- All new files contain explicit PGS-first and state-separation language.
- No `sorry` in any "proved" section.

### 4.2 Phase 1: Foundational Definitions & Basic Lemmas

**Core Objects to Formalize** (with PROOF.md mapping):

- `tau(n)` (divisor count), exact translation of the function used throughout the project.
- Zero-excess `E(n)` and dual forms `Z(n)`, `F(n)`.
- Prime characterization: `Nat.Prime n ↔ tau n = 2` (for n > 1), with explicit link to the prose statement.
- Finite intervals and ordered divisor-count fields over `[a, b]`.
- Basic ordering and comparison lemmas for `E` and `F` on finite sets.

**Supporting Mathlib Usage** (restricted):
- `Nat.divisors`, `Finset`, `List`, `Real.log` (noncomputable where necessary).
- Avoid heavy use of `Nat.Prime` theorems until they are explicitly required as audit comparisons.

**Status Vocabulary in This Phase**:
- Most lemmas will initially be marked "Audit / Translation of prose in ..."

**Deliverable**: `PGS/Basic.lean` significantly expanded + first test file `PGS/BasicTest.lean` or `#check` examples.

### 4.3 Phase 2: Interval Machinery & Chamber State

**Objects**:
- Prime-gap intervals (start after known prime `p`, end at next prime-square boundary or explicit horizon).
- Ordered divisor-count sequences.
- "Selected integer" `w` definition.
- Chamber reset and horizon concepts (as they appear in current research).

**Key Lemmas**:
- Every interval between consecutive primes contains exactly one leftmost minimum-tau interior point under the GWR rule (translation of existing prose).
- Basic closure properties of the "first interior min-tau" operator.

**PROOF.md Mapping**: Sections describing the tau-scan process and the definition of the selected composite inside the gap.

### 4.4 Phase 3: GWR Maximizer Theorem (Core Theorem #2)

**Target Theorem** (direct mirror):

> In any interval between two consecutive primes, the leftmost interior integer that achieves the global minimum divisor count is the unique maximizer of `F(n) = −E(n)`.

This is the "Leftmost Minimum-Divisor Rule / GWR maximizer theorem" declared universal under its hypotheses in `PROOF.md`.

**Approach**:
- Define the "first interior min-tau" selector as a total function on finite intervals.
- Prove uniqueness of the maximizer.
- Prove that this selector is exactly the one used by the prose GWR rule.

**Status**: Once completed, this theorem moves from "Proved in prose" + "Python measurement" to "Machine-checked translation."

### 4.5 Phase 4: Direct Deterministic Next-Prime Theorem (Core Theorem #1)

**Target Theorem** (direct mirror):

> For every prime `p`, the PGS chamber state constructed from the ordered divisor-count field over the subsequent search interval resolves to a unique next prime `q` via the GWR selection rule.

This is the "direct deterministic next-prime theorem via tau-scan."

**Dependencies**: Requires Phase 3 (GWR) plus the interval/chamber machinery.

**Special Requirements**:
- The formal statement must preserve the generator contract: input `p`, output exactly the pair `{"p": p, "q": q}` with no extra metadata in the core theorem.
- Any diagnostics, certificates, or audit fields must live in separate sidecar structures.

### 4.6 Phase 5: Cross-Verification Infrastructure

- Mechanisms to import or mirror large-scale empirical results from `docs/RESULTS.md` (e.g., the 78,494/78,494 and decade-window 100% exact surfaces).
- Optional: decidable procedures for small intervals that can be run inside Lean (for sanity checking).
- Explicit "audit only" modules that compare Lean-evaluated `tau` values against the Python `divisor_counts_segment` implementation on known test vectors.

**Warning**: This phase must not be used to "discover" new behavior. It only verifies already-measured surfaces.

### 4.7 Phase 6: Documentation, Status Surfaces, and Maintenance

**Mandatory Deliverables**:
- Self-contained `docs/lean-pgs-verification/index.html` (or equivalent under `docs/`) containing:
  - Visual status table (Proved / In Progress / Audit / Hypothesis)
  - Full mapping from `PROOF.md` paragraphs to Lean identifiers
  - Before/after evidence paths
  - Checklist for future Codex/Hermes sessions
- Regular updates to `research/00-index/status-map.md`
- This planning document kept in sync

**Maintenance Rule**: Any change to a "Proved" theorem in Lean requires a corresponding review of the prose in `PROOF.md` (or an explicit note that the Lean version is a stricter formalization of the same statement).

## 5. Traceability & Mapping Strategy

A central table will be maintained (initially in this document, later promoted to the HTML surface):

| PROOF.md Location          | Supporting Docs                  | Lean Identifier(s)          | Status     | Notes |
|---------------------------|----------------------------------|-----------------------------|------------|-------|
| Direct next-prime theorem | ...                              | `PGS.NextPrime.direct_next_prime` | Planned   | ... |
| GWR maximizer theorem     | docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md | `PGS.GWR.leftmost_min_tau_maximizer` | Planned | ... |
| tau(n) = 2 characterization | DIVISOR...                       | `PGS.Basic.prime_iff_tau_eq_two` | In Progress | ... |

Every Lean file will open with a "References" block listing the exact prose locations it mirrors.

## 6. Risks and Mitigations

- **Risk**: Lean development culture pulls the team toward "proving new things in Lean" instead of mirroring existing prose.
  **Mitigation**: This plan + the verification contract + mandatory shape checks in every review.
- **Risk**: Over-use of Mathlib's powerful number theory results hides the PGS-specific mechanism.
  **Mitigation**: Explicit "PGS-native first" comments and restricted import lists in core modules.
- **Risk**: Performance / decidability issues on large intervals.
  **Mitigation**: Keep large-scale work in the Python reference implementation. Lean is for theorem structure, not for 10^18-scale computation.
- **Risk**: "sorry" pollution.
  **Mitigation**: Strict policy : `sorry` only in clearly marked hypothesis/work-in-progress sections with TODOs.

## 7. Success Criteria

The formalization effort can be considered "mature for its phase" when:

- Both core theorems from `PROOF.md` have machine-checked Lean statements with no `sorry` in the proof bodies.
- A complete mapping table exists and is reflected in an HTML status document.
- A future session can read the HTML + this plan + the contract and continue the work without reconstructing context from chat history.
- The Python generators and `docs/RESULTS.md` surfaces remain completely untouched by the existence of the Lean track (except for optional audit cross-checks).

## 8. Tooling & Environment

- Primary: `elan` (Lean version manager) + `lake`
- Recommended first step for any new environment: `elan install v4.30.0 && lake exe cache get` (once Mathlib is fetched)
- Editor: VS Code + Lean 4 extension (or any LSP-capable editor)
- No reliance on external classical oracles or AI-assisted proof search in the core theorems.

## 9. Open Questions (to be resolved in later plan revisions)

- Exact granularity of "chamber state" formalization (how much of the runtime Python chamber logic needs a Lean mirror?).
- Whether to formalize any of the modulus-link / endpoint-chain work from the cryptology track (likely later, and only after the core two theorems).
- Long-term: Should there be a "PGS in Mathlib" contribution path, or must everything stay in this private `lean-4/` mirror?

## 10. Next Immediate Actions (Post-Skeleton)

1. User reviews and approves this plan + the contract.
2. Update root `.gitignore` and project status maps.
3. Create initial `docs/lean-pgs-verification/` HTML status skeleton (per project HTML preference).
4. Begin Phase 1 work on `PGS/Basic.lean` expansions, starting with the prime ↔ tau=2 characterization.
5. First real build test once Lean is installed on the target machine.

---

**This plan is not a contract in the legal sense, but it is an operational commitment.** Deviations must be documented here with clear rationale and must still respect the binding `LEAN_PGS_VERIFICATION_CONTRACT.md`.

Update this document before starting any new phase.

## Relationship to the Detailed Plan

The authoritative detailed technical translation roadmap (with full PROOF.md line mappings, module hierarchy, per-lemma strategies, and expanded traceability matrix) now lives at:

**`docs/lean-pgs-verification/PGS_LEAN_TRANSLATION_PLAN.html`**

This Markdown file remains the short executive overview and high-level phase list. All new detailed work, risks, and traceability tables are maintained in the HTML version.
