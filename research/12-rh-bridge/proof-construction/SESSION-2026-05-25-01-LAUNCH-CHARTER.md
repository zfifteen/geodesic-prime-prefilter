# Exact Completion Assembly Theorem — Proof Construction
## SESSION-2026-05-25-01 LAUNCH CHARTER

**Date initiated:** 2026-05-25  
**Session type:** Time-boxed multi-agent research sprint (target 4–8 hours effective agent work per user direction)  
**Governing contract:** AGENTS.md (full scope), PROOF.md status rules, 12-rh-bridge README framing  

### User-Defined Success Criterion (exact quote of decision)
"Constructive algorithm + verification surface"

- Primary goal: Produce an **explicit construction (or algorithm)** for the packetwise measures `η_{p,q,z}` (or an equivalent practical method to generate them).
- Deliverable requirement: Accompanying **code** that verifies the four conditions of the Exact Completion Assembly Theorem on large finite sets of chambers.
- Must include: Clear, honest statement of the **bounds on what remains open** (especially regarding the infinite trivial-zero reservoir and the Transport Capacity Balance Identity).
- This is **not** a requirement for a complete infinite analytic proof at this stage.

### Operating Rules (user decisions)
1. **Progress model**: Time-boxed exploration. The team works toward a checkpoint deliverable, then pauses for user review and possible interruption.
2. **Team structure**: Standard 4-role team
   - **Analyst** — classical completion machinery, explicit formula, kernels, pole pair, Gamma factor, trivial zeros.
   - **PGS Guardian** — enforces PGS-native starting frame and full AGENTS.md contract on every reasoning step and artifact. Never allows classical methods to become the first frame.
   - **Numerics** — designs, implements, and runs verification experiments and diagnostics on finite chamber sets.
   - **Proof Architect** — maintains the evolving construction draft, enforces strict state separation in all public and internal outputs.
3. **Language strictness**: **Maximum strictness**. Every document, status update, reasoning trace, and internal message must use the project's exact separation vocabulary at all times:
   - theorem vs. strategy vs. measured result vs. unresolved target vs. invalidated rule
   - No optimistic language ("we have shown", "this works", "progress toward proof") even internally. Use "candidate construction", "under test", "observed on this regime", "remains open", etc.
4. **Starting point**: Begin work immediately from the existing strategy documents (no waiting for a separate charter review). This charter itself is the live operating agreement and can be updated at the first checkpoint.

### Mandatory Starting Documents (all agents must read first)
- `research/12-rh-bridge/docs/exact_completion_assembly_theorem.md`
- `research/12-rh-bridge/docs/exact_completion_assembly_strategy.md`
- `research/12-rh-bridge/docs/transport_reservoir_allocation_rule.md`
- `research/12-rh-bridge/docs/transport_capacity_balance_identity.md`
- `research/12-rh-bridge/docs/global_completion_negative_cost_conditions.md`
- `research/12-rh-bridge/docs/chamber_deconvolved_reciprocal_balance_lemma.md`
- Root `AGENTS.md` (especially PGS-First Reasoning Entrypoint and State Separation sections)
- `research/12-rh-bridge/README.md` (for overall framing)

### Artifact Locations for This Session
- Central coordination ledger: `research/12-rh-bridge/proof-construction/SESSION-2026-05-25-01-LEDGER.md`
- Role-specific working notes: subfolders or clearly prefixed files under `proof-construction/`
- Any experimental code: `research/12-rh-bridge/proof-construction/experiments/`
- All outputs must carry explicit status headers using the separation vocabulary.

### Interruption & Handoff Protocol
- User may interrupt at any time.
- Before any pause or user return, the team must produce:
  1. Updated central LEDGER with current status (using strict language).
  2. Clear "Recommended Next Direction for Next Session" section.
  3. List of all new artifacts created.
- Subagent IDs will be recorded so work can be resumed or inspected.

### Forbidden Moves (per AGENTS.md + user direction)
- Starting reasoning from classical methods before forming the PGS-native frame.
- Treating the target theorem as proved or "almost proved."
- Introducing fallback classical search, probabilistic methods, or external primality tests inside the construction.
- Downgrading the status of any already-proved PGS result.
- Producing artifacts without the required state-separation language.

### Initial Team Task (Session 01)
Each of the four agents, after reading the mandatory documents and this charter, shall produce within the time box:
- A role-specific assessment of the current obstruction (Transport Capacity Balance Identity + construction of η measures).
- One or more concrete, narrow, high-leverage proposals for a constructive step that can be tested on finite chambers.
- Explicit identification of where the infinite reservoir problem remains open.

All four agents write their initial contributions to the central LEDGER.

**This charter governs all work in this session and any resumption of these agents.**

---
**Recorded by:** Grok (orchestrator)  
**User confirmation of rules:** Received via structured answers on 2026-05-25.