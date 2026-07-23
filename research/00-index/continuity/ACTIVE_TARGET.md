# Active Research Target

**Updated:** 2026-07-23  
**Program center:** Lean 4 core-stack formalization **program DoD met (M0–M5)**; public readability remains second priority.

> **Principal directive (2026-07-18, #Prime-Gap-Structure):**  
> Lean core-stack machine-checked mirror of `PROOF.md` (now **DONE** under D1–D7).  
> Continuity pin: [notes/TOP_PRIORITY_lean_core_stack_2026-07-18.md](notes/TOP_PRIORITY_lean_core_stack_2026-07-18.md)  
> Status HTML: [docs/lean-pgs-verification/index.html](../../../docs/lean-pgs-verification/index.html)  
> Peer accept: [lean-4/peer/M5_DOD_ACCEPT.md](../../../lean-4/peer/M5_DOD_ACCEPT.md)

## Lean core stack (DONE)

```text
Machine-checked Lean 4 mirror of the core stack already proved in PROOF.md:

  - Direct deterministic next-prime (tau-scan) — M2
  - GWR / Interior Maximizer (leftmost min-divisor) — M3
  - Universal bounded compression + Prime-Square Proximity — M4
  - Finite-base packages as named hypotheses — M5
  - Classical imports as audit premises only
```

| Field | Value |
| --- | --- |
| Status of laws in `PROOF.md` | **theorem** (unchanged) |
| Lean track status | **program DoD DONE** (M0–M5); extensions optional under D7.3 |
| Home | `lean-4/` |
| Plan | `lean-4/PGS_LEAN_FORMALIZATION_PLAN.md` |
| Contract | `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md` |
| Immediate next | Extensions only (analytic discharge of named packages); or second-priority public docs |
| Definition of Done | `lean-4/DEFINITION_OF_DONE.md` |
| Effort owner | **Hermes** |
| Owner charter | `research/00-index/continuity/notes/LEAN_CORE_STACK_OWNER_CHARTER_2026-07-18.md` |
| Peer accept | `lean-4/peer/M5_DOD_ACCEPT.md` |
| Hourly heartbeat | `scripts/lean-heartbeat/HEARTBEAT.md` (auto-off on DONE) |

Lean **never** chooses primes, never edits theorem status, never replaces generators.

## Second priority (public-facing readability)

**Principal directive (2026-07-18):** overall readability and ease of access of
**public-facing documentation** — second only to the Lean core-stack priority.

| Rule | Meaning |
| --- | --- |
| Scope | Public-facing docs (README, research HTML, continuity briefs, docs/* guides, gallery copy, etc.) |
| **Exception** | **`PROOF.md` keeps its current tone** — do not rewrite it into dual-layer style |
| Open | Every public doc **starts** in easy, conversational prose a typical tenth-grader can follow (picture the object, plain mechanism, then names) |
| Then | Same doc **continues** into full technical depth (PhD-level precision, definitions, status separation) |
| Never label | Do **not** put labels like “grade 10,” “PhD section,” “simple version,” or “advanced version” in the doc itself |
| Access | Prefer formats people can open easily (`file://` HTML where structure helps; clear nav; no gatekeeping jargon before the plain open) |

Continuity pin: [notes/SECOND_PRIORITY_public_readability_2026-07-18.md](notes/SECOND_PRIORITY_public_readability_2026-07-18.md).

Aligns with AGENTS.md Writing Standard (observable object → ordinary language → project term → formal → status → limits) without exposing reading-level meta-labels.

## Secondary tracks (alive, not top or second)

### 50-bit residual (hypothesis / unresolved)

50-bit fixture remains **unresolved**. Measured residual migration on rsa-v3:
carrier misalignment → first-tail (dual-gap D) → joint cell
`unresolved_by_joint_cell_C1T2L1` (residual vector R, pinch_S = 54). Residual
maps stay **hypothesis**. Continuity pin:
[notes/ACTIVE_GOAL_50bit_residual_discriminator.md](notes/ACTIVE_GOAL_50bit_residual_discriminator.md).
Package:
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1/`.

### Square-branch audit relay

Rotating queue in `hourly_queue.json`. Cadence and ops:
`HOURLY_RELAY_CONTRACT.md`. Status class: audit corroboration only — does not
bound universal theorems.

## Central obligation: CLOSED 2026-07-05 (do not re-litigate)

The square-branch prime-square proximity theorem is **proved** in
[PROOF.md](../../../PROOF.md) §Prime-Square Proximity Theorem. Universal bounded
compression at Cramér scale is established across all prime-gap branches per
`PROOF.md` Document Status.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [PROVED]
w - p <= max(64, ceil(0.5 * log(q)^2))       [PROVED, all branches]
```

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)
- **Prime-Square Proximity Theorem** (`PROOF.md`, 2026-07-05)
- **Universal bounded compression** (`PROOF.md`, 2026-07-05)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)

## Last measured surface (audit corroboration only)

| Field | Value |
| --- | --- |
| Segment | `4·10^8 .. 5·10^8` |
| Prime roots tested | `5,019,541` |
| First counterexample | `none` |
| Max utilization | `0.9341772151898734` |
| Extremal root `r` | `424,171,123` |
| Offset `D(r)` | `738` |
| Local artifacts | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/` |

## Read-first (every session on this priority)

1. `AGENTS.md` (repo root)
2. `PROOF.md` (theorem status only)
3. This file
4. `notes/TOP_PRIORITY_lean_core_stack_2026-07-18.md`
5. `lean-4/README.md` + `lean-4/PGS_LEAN_FORMALIZATION_PLAN.md`
6. `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md`

## Repro gates (Lean)

```text
bash scripts/lean4-cache-build.sh
# or
cd lean-4 && lake build && lake env lean smoke-test.lean
```

*Principal top-priority pin 2026-07-18 · Hermes.*
