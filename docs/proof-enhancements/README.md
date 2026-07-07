# PROOF.md Enhancement Sub-Project

**Created:** 2026-07-07  
**Authority:** Subordinate to `PROOF.md` (single live proof reference) and `docs/AGENTS.md`  
**Status:** Active — audit and planning phase

## Purpose

This folder tracks work to **harden and enhance** `PROOF.md` so that its claims are:

1. **Mathematically complete** — no informal or density-heuristic steps presented as finished proofs
2. **Epistemically honest** — clear separation of proved / finite-certified / measured / hypothesis
3. **Formally portable** — structured so a gap-free Lean 4 mirror becomes feasible, not aspirational
4. **Reproducible** — finite bases and audit tables tied to pinned artifacts and verification commands

`PROOF.md` remains the single live proof document. This sub-project does not fork authority; it produces audits, enhancement proposals, and (eventually) targeted patches to `PROOF.md` itself.

## Relationship to Other Tracks

| Track | Role relative to this effort |
|-------|------------------------------|
| `PROOF.md` | Source of truth; receives hardened content |
| `lean-4/` | Downstream mirror; benefits from prose gaps being closed first |
| `research/02-gwr-dni/scripts/proof/` | Finite-base and certificate generators — should align with enhancement specs |
| `docs/lean-pgs-verification/` | Formalization status — should reflect honest prose status |

## Documents in This Folder

| File | Contents |
|------|----------|
| [shortcomings.md](./shortcomings.md) | Identified gaps, overclaims, and structural weaknesses in current `PROOF.md` |
| [goals.md](./goals.md) | Enhancement goals, acceptance criteria, and phased targets |

## Guiding Principles

- **PGS-first:** Objects → invariants → rule → resolved/unresolved/invalidated state
- **No status inflation:** A finite enumeration is *certified*, not *proved by pure divisor arithmetic*
- **Repair before formalize:** Close prose gaps before expecting Lean to close them
- **Traceability:** Every enhancement links to `PROOF.md` line ranges and supporting artifacts

## Current Phase

**Phase 0 — Audit & inventory** (this folder)

Next: prioritize shortcomings by severity, draft concrete `PROOF.md` patch plans per goal, and define certificate schemas for finite-base claims.