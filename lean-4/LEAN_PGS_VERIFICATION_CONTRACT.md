# LEAN_PGS_VERIFICATION_CONTRACT.md

**Version**: 1.0 (Initial Skeleton)  
**Date**: 2026-05-27  
**Authority**: This document is binding for all work inside `lean-4/`. It is a direct extension of `docs/AGENTS.md`, `research/00-index/continuity/continuity_and_shape_contract.md`, and `research/00-index/continuity/START_HERE.md`.

## Purpose

This contract exists to prevent the four canonical failure modes when adding a formal verification track to the PGS project:

1. The formalization becoming the de-facto reasoning engine or source of truth.
2. Classical number theory, probabilistic methods, or Mathlib "tactics as oracles" leaking into the core PGS inference path.
3. Downgrading the proved status of theorems in `PROOF.md` because "they are now in Lean."
4. Scope creep that turns the Lean effort into a general number theory library instead of a narrow, high-fidelity mirror of the existing prose proofs.

## Core Tenets (PGS-First, Downstream Only)

**PGS objects → PGS invariants → PGS rule/law → resolved/unresolved/invalidated state**

The Lean formalization must **always** enter through the same entrypoint required of every other artifact in this repository:

- Ordered prime-gap state
- Divisor-count field `tau(n)`
- Divisor Normalization Identity (DNI) and zero-excess `E(n) = (d(n)/2 − 1) ln n`
- Leftmost Minimum-Divisor Rule / GWR (selected composite `w` = first interior min-tau integer, unique maximizer of `F(n) = −E(n)`)
- Chamber state, endpoint chains, reciprocal transport, etc. (as they are introduced)

**Never begin formalization from**:
- `Nat.Prime` as a black box primitive for selection
- Miller-Rabin style statements
- Probabilistic claims
- Factorization search
- Classical "next prime" existence via Euclid or Dirichlet without the PGS tau-scan mechanism

Mathlib's `Nat.Prime`, `Nat.divisors`, `Finset`, etc. are **tools for faithful translation**, not inference mechanisms.

## State Separation (Mandatory in Every Artifact)

Every file, theorem, comment, and status document inside `lean-4/` **must** explicitly separate:

- **Proved** (directly mirrors a theorem in `PROOF.md`)
- **Measured** (empirical surfaces from `docs/RESULTS.md`)
- **Audit** (implementation or translation verification only)
- **Hypothesis** (separate research targets)
- **Unresolved**
- **Invalidated** (with clear reference to the invalidated rule)

The Lean code must never collapse these categories. The Lean formalization provides an independent machine-checked mirror of the proofs established in `PROOF.md`.

## Traceability Requirement

Every definition, lemma, and theorem **must** carry a header comment of the following form:

```lean
/-
PROOF.md Reference: Lines XXX-YYY (or specific theorem name + paragraph)
Supporting prose: docs/core/DIVISOR_NORMALIZATION_IDENTITY.md §Z, docs/core/LEFTMOST... §W
Status: Proved / Audit-only / ...
-/
```

A central mapping table must live in the planning document and be mirrored in an HTML status surface under `docs/`.

No "drive-by" formalization of convenient Mathlib facts is allowed without an explicit PGS justification and mapping.

## What Lean Is Allowed To Do

- Provide machine-checked translations of the two core universal theorems in `PROOF.md`:
  1. Direct deterministic next-prime via tau-scan.
  2. GWR / leftmost minimum-divisor maximizer theorem.
- Support lemmas that are strictly necessary to express the above faithfully.
- Serve as a high-fidelity audit surface for future large-scale verification of the 100% exact surfaces in `docs/RESULTS.md`.

## What Lean Is Strictly Forbidden From Doing (Inside This Project)

- Being used to select the next prime `q` for any input `p` in any generator.
- Introducing new PGS rules, conjectures, or "discovered" lemmas that are then fed back into the Python/C generators as authority.
- Using probabilistic tactics, random search, or external oracles in the core proof paths.
- Formalizing classical number theory results (Bertrand's postulate, prime number theorem bounds, etc.) unless they are explicitly required as a *comparison* layer and clearly labeled as such.
- Treating the Lean development as the primary research surface. The prose in `PROOF.md` + the Python reference implementation in `src/python/z_band_prime_composite_field/field.py` remain authoritative for understanding and for generator behavior.

## Interaction With Other Layers

- The Python `divisor_counts_segment` + gmpy2 implementation remains the reference field computation.
- Lean may be used later for cross-verification of specific large intervals, but only after the core theorems are mirrored.
- The legacy Z-band prefilter (Miller-Rabin + sympy) stays in its historical lane and is never mixed into the Lean core.
- Any RH-related work remains strictly downstream of PGS theorems (see archived `research/12-rh-bridge` rationale).

## Installation and Build Hygiene

- Use `elan` + `lake` only.
- Pin to exact Lean + Mathlib revisions in `lean-toolchain` and `lakefile.lean`.
- Build artifacts (`.lake/`, `lake-packages/`) must be gitignored.
- No `sorry` in production theorems. `sorry` is allowed only in clearly marked "work-in-progress / hypothesis" sections with explicit TODO markers.

## Enforcement

Any contribution that violates this contract must be rejected at review time, even if the Lean code is mathematically elegant.

When in doubt, reread:
- `docs/AGENTS.md` (especially "PGS-First Reasoning Entrypoint" and "Shape Warnings")
- `research/00-index/continuity/continuity_and_shape_contract.md`
- `PROOF.md` (the single live proof reference)
- This contract

**Shape feels wrong** signals for this track:
- Starting a Lean file with `theorem next_prime_exists ...` before defining the PGS tau-scan mechanism.
- Using Mathlib's `Nat.exists_infinite_primes` as the "proof" of the next-prime theorem.
- Adding general-purpose number theory lemmas without a PGS mapping.
- Describing the Lean work as "proving PGS" instead of "mechanically verifying the existing prose proofs in PROOF.md."

## Revision History

- 2026-05-27: Initial skeleton version. Created alongside top-level `lean-4/` folder.

---

This contract is part of the project's permanent operational surface. It travels with the Lean effort.
