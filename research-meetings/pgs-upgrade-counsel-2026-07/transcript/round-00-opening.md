# Research Meeting Opening Prompt

## Meeting Title

PGS Research Program Strategic Upgrade Counsel

## Created

2026-07-03

## Instructions For All Participants

This is a formal counsel of 12 specialized agents convened to answer one question with maximum rigor:

**What would be the most significant, single upgrade to the PGS research program?**

### Strict Frame (from AGENTS.md and continuity contract)
- Begin from PGS-native objects and invariants.
- PGS is deterministic. Do not reframe as probabilistic, heuristic, or empirical for inference.
- PROOF.md is the single live proof reference. Do not downgrade proved theorems.
- Current active project is PGS research broadly. The v1.1 generator is a completed milestone, not the whole program.
- Active frontiers include: endpoint-chain traversal, modulus-link probes, floor transport, reciprocal closure, chamber reset, endpoint determinacy, square-branch dynamic cutoff closure, structural certificates, high-scale generation, Lean formalization.
- Classical methods (Miller-Rabin, gcd, trial division, sieves, nextprime) are allowed only for downstream audit, benchmark comparison, or explicit legacy prefilter. They must never choose PGS outputs or serve as the first reasoning frame.
- State separations required in every contribution: theorem proof vs. implementation status vs. measured result vs. audit result vs. hypothesis vs. unresolved state vs. invalidated rule.

### Process
Each agent will:
1. State their persona and primary lens.
2. Propose exactly one primary upgrade (the single most significant in their view).
3. Provide 1-2 runner-up candidates.
4. Give concrete rationale tied to current artifacts (e.g. ACTIVE_TARGET.md, square-branch blocker, RSA v2 unresolved 50-bit, Lean status, etc.).
5. Identify risks and opportunity cost.
6. In later rounds: critique others' proposals, surface hidden assumptions, converge or dissent.

The counsel must produce:
- Full list of candidate upgrades considered.
- Detailed rationale for the selection of the winner.
- Lengthy explanation of the winner, including how it advances specific PGS objects/invariants and what it unlocks.

After individual proposals, the group will converge on a ranked shortlist and a single winner.

## Agenda

Convene a counsel of 12 agents with distinct expertise domains inside the PGS program. Through structured debate, identify, rank, and select the single most significant upgrade to the overall PGS research program. Record verbatim contributions, all candidates, selection rationale, and a complete explanation of the winning upgrade. Deliver auditable meeting minutes and transcripts suitable for research-continuity.

## Starting Material (verbatim user query)

"I want you to assemble a counsel on 12 agents to debate one question: What would be the most significant, single upgrade to the PGS research program? I want you to record detailed meeting minutes and capture all candidate upgrades that were considered, the rationale for determining which became the winner and a lengthy explanation of the winner."

## Current Evidence And Boundaries (program snapshot as of 2026-07-03)

**Proved (do not re-litigate, PROOF.md controls):**
- Direct deterministic next-prime theorem: given known prime p, exact divisor counts on p+1, p+2, ... yield q = first n with tau(n)=2.
- Interior maximizer / GWR / Leftmost Minimum-Divisor Rule: in any prime gap (p, q), the leftmost minimum-divisor integer maximizes F(n) = (1 - tau(n)/2) log n (or equivalently minimizes E(n) zero-excess).
- DNI (Divisor Normalization Identity) and related coordinate systems are exact reformulations.

**Current Production Milestone:**
- Minimal PGS Generator v1.1 (PGS-only): outputs clean {"p": ..., "q": ...} records. Verified exact on 11..1e6 (78494/78494) and sampled 1e8..1e18 surfaces with 0 unresolved, 0 audit failures in committed ladders. Recursive walk exact on hundreds of thousands of steps.

**Active Unresolved / High-Leverage Targets (from ACTIVE_TARGET.md, status-map, RESULTS):**
- Square-branch proximity closure for bounded dynamic cutoff: Prove or close D(r) = r^2 - previous_prime(r^2) <= C(r) where C(q) = max(64, ceil(0.5 * log(q)^2)) on square-branch gaps. Current empirical surface clean through tested hundreds of millions; remains the central obligation.
- RSA v2 / cryptologic endpoint structure: Reciprocal deadline-signature correction + oriented endpoint-chain closure + floor transport + reciprocal transport. 40-bit and 64-bit rungs resolved publicly in some cases; 50-bit rung currently unresolved_by_reciprocal_carrier_misalignment (measured, not theorem). Modulus-link residual state and structural certificates.
- Chamber reset mechanics, endpoint determinacy, boundary behavior, chain-horizon closure.
- High-scale practical generation: C/GMP implementation for 1000+ bit and beyond (src/c/high-scale-pgs).
- Lean-4 formalization of core theorems (lean-4/ directory, PGS_LEAN_FORMALIZATION_PLAN.md).
- Reduced gap-type model (14-state core, semiprime wheel attractor) — measured surfaces, not universal theorems.
- Bounded compression rule (empirical, not unconditional theorem).
- Predictions track (research/16-predictions) and pgs-unsolved-problems catalogue.

**Invalidated (preserve as false):**
- Fixed cutoff theorem {2:44, 4:60, 6:60} — falsified at q=24,098,209.
- Certain SDA transfers on square branch (see experiments/square-branch-sda-invalidation-2026-06/).

**Boundaries:**
- RH-bridge work is sensitive to classical drift; current guidance routes primary effort to local PGS objects first (divisor counts, GWR, chambers, endpoint chains, modulus links) before spectral readings.
- Legacy prefilter (Z-band) is validated engineering surface using PGS normalization downstream; Miller-Rabin lives only there for confirmation.
- All contributions must separate: proved theorem / implementation status / measured regime / audit / hypothesis / unresolved / invalidated.
- No fallback classical search inside PGS generation or inference.

**Key Artifacts for Reference:**
- PROOF.md, RESULTS.md, AGENTS.md, PRIME_GAP_GENERATOR.md
- research/00-index/continuity/START_HERE.md, ACTIVE_TARGET.md, status-map.md
- research/04-bounded-compression/ (square branch)
- research/06-cryptology-rsa/ (endpoint structure, modulus-link, semiprime)
- research/01-generator/, 02-gwr-dni/, lean-4/, research/16-predictions/
- Various experiment FINDINGS.md for falsification surfaces.

## Participants (The Counsel of 12 Agents)

The following 12 agent personas will participate. Each receives a dedicated subagent instance with role-specific instructions enforcing PGS contracts.

1. **PGS Theorem Guardian** — Guardian of PROOF.md. Prioritizes anything that strengthens, extends, or formalizes the core deterministic theorems without dilution.
2. **Cryptologic Strategist** — RSA endpoint structure, modulus-link closure, reciprocal transport, structural certificates, PGS-native factorization pressure. Current live RSA v2 surfaces.
3. **Bounded Compression Lead** — Owner of current active target. Square-branch dynamic cutoff, D(r) proximity, bounded walker honesty.
4. **High-Scale Systems Engineer** — Practical scaling: C implementation, GMP/MPFR, chamber reset at 1000+ bits, generator throughput for real cryptologic sizes.
5. **Formal Methods Specialist** — Lean-4 translation, machine-checked proofs of PGS theorems, verification contracts.
6. **Experimental Design Auditor** — Falsification specialist. Designs decisive tests, stress surfaces, adversarial probes. Protects against overclaim.
7. **Continuity & Shape Keeper** — Enforcer of AGENTS.md, PGS-first reasoning, continuity files. Detects drift, classical re-framing, progress theater.
8. **Gap Structure Theorist** — Gap types, reduced generative model, semiprime wheel attractor, interior geometry, 14-state core.
9. **State Budget & Efficiency Analyst** — Divisor-count distributions, chamber budgets, d(n) carriers, state compression economics, d=4 dominance surfaces.
10. **Predictions & Open Problems Curator** — Maintains unsolved-problems catalogue, long-horizon deterministic predictions, cross-chapter implications (Collatz, exponents, twins).
11. **Classical Number Theory Comparator** — External lens only. Brings classical context (PNT, RH, sieves, analytic) strictly for comparison/audit/benchmark framing. Never as inference engine.
12. **Documentation & Public Framing Guardian** — Ensures all public artifacts, whitepapers, READMEs, substack, Zenodo drafts preserve source order (PGS objects before zeta/RH/PNT). Audits wording drift.

## Negotiated Deliverable (to be confirmed in process)

A complete, self-contained meeting record containing:
- Verbatim or faithful capture of all 12 agents' opening proposals (primary upgrade + rationale + runners-up).
- Consolidated list of all distinct candidate upgrades considered.
- Debate summary: key critiques, points of convergence, points of dissent.
- Selection of a single winner upgrade.
- Rigorous rationale for why that upgrade was judged most significant.
- Lengthy, multi-paragraph explanation of the winner: what PGS object/invariant it advances, current blocker it removes, concrete next artifacts it enables, risks of delay, and how it maintains or strengthens the deterministic PGS frame.
- Explicit statement of the 2nd and 3rd place and why they ranked lower.
- Recommended immediate next research move(s) tied to the winner.

All language must respect the state-separation contract and PGS-first entry point.
