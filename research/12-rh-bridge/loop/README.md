# PGS-RH Bridge Autonomous Research Loop

**Purpose:** Persistent, self-directed execution engine that autonomously drives the central bridge obstruction (currently the Chamber-Deconvolved Reciprocal Balance Lemma and its reduction chain documented in the parent README and the two chamber_*_resolution.md files) until resolved or a fundamental blocker is isolated — without ever prompting the user for direction. User monitors via artifacts and the dedicated agent-bus topic and interrupts externally.

**PGS Objects First (non-negotiable entrypoint for every cycle and artifact):**
- Ordered prime-gap state (consecutive endpoints p < q with q fixed by first return to E(n)=0).
- Divisor-count field τ(n).
- Zero-excess E(n) = (τ(n)/2 − 1) log n; primes exactly at E(n)=0 (n>1).
- GWR / Leftmost Minimum-Divisor Rule (proved in PROOF.md): leftmost argmin E(n) in nonempty chamber interior uniquely maximizes F(n) = −E(n).
- Bridge load H(n) = log n + E(n) = τ(n) log n / 2.
- Exact DNI-to-zeta compression: D(s) = ζ(s)^2, R(s) = (e²/2) K(s)/D(s) = −ζ'(s)/ζ(s).
- Deconvolved load λ = τ_Dir^{−1} ∗ H yielding λ(n) = Λ(n).
- Live lemma target: after deconvolution, completion, and folding into centered z = u², the residual determines a nonnegative Stieltjes measure (reciprocal balance + nonnegativity). This is the precise source-side step required for source-to-spectral placement of the nontrivial poles of R(s).

**Current Live Target (read from resolution documents at start of every cycle):**
See research/12-rh-bridge/docs/chamber_deconvolved_reciprocal_balance_lemma.md and chamber_load_spectral_centering_resolution.md (and the living reduction chain in the parent research/12-rh-bridge/README.md). The loop treats the single narrowest open item in the current verification matrix or "remains open" list as the locked sub-goal for that cycle.

**Strict Separation Vocabulary (mandatory in every output, report, ledger entry, bus message, and dashboard):**
- Proved / exact (only for items controlled by PROOF.md or the exact compression identities).
- Candidate construction under test on regime X.
- Observed on finite set.
- Measured result / audit result.
- Unresolved / remains fully open.
- Invalidated rule.
- PGS Guardian review: passed / vetoed.
- Shape warning (if drift detected).

No optimistic language. Classical completion / analytic machinery is used only after the PGS frame is formed and only for technical analysis of downstream objects.

**Architecture (high-level, per approved plan):**
- Orchestrator (research_loop.py): always-on loop, state load, interrupt check, cycle dispatch, dashboard + bus refresh, clean handoff.
- Autonomous Decider: rule-based first (narrowest falsifiable item from current target's verification matrix); falls back to guarded insight-ooda / novel-insight-engine sub-cycles when needed. Produces one Action Card per cycle.
- 4-Role Engine (roles.py + execution): PGS Guardian (first pass, contract enforcement), Analyst, Numerics (harness runs), Proof Architect (draft + ledger + possible resolution updates only on real status change).
- Generalized Harness (bridge_proof_harness.py): accepts target_lemma_id + regime parameters; reuses/extends the verified eta-allocation regime logic (packet construction from GWR/τ/λ, candidate_allocate, strict reporting, honest limits). Supports numerical and (later) symbolic modes. Falls back to C/GMP scaffolds when Python limits are hit.
- Persistence: this directory + parent proof-construction/ for reports; dedicated agent-bus topic "pgs-rh-bridge-autonomous-loop" (durable, threaded, searchable, with explicit PGS guardrails); self-contained HTML dashboard.
- Interrupt / Resume: HALT file or bus "interrupt" message → clean atomic finish + handoff package. Resume from latest ledger + bus cursor + files (no chat context required).

**Contract Enforcement:**
- AGENTS.md, PROOF.md status rules, continuity files, and the approved plan are read at every loop start and enforced by the PGS Guardian role on every Action Card and artifact.
- Second-opinion skill required before any live target change or major path retirement.
- research-continuity + scientific-code-review + logic-check invoked on new artifacts before status claims.
- Shape warnings surfaced immediately to ledger + bus.

**How to Launch (once scaffold complete):**
See the main research_loop.py for CLI flags (target, regime, max-cycles, mock, etc.). Long-running via nohup, scheduler, or manual. User monitors via:
- tail -f on LOOP_LEDGER.md
- Open research/12-rh-bridge/loop/bridge_research_dashboard.html (file://)
- agent-bus tools (sync / messages_search on the dedicated topic)
- Periodic research-continuity reports

**Status:** Scaffold in progress (Phase 1 of approved plan). No autonomous research cycles executed yet. All infrastructure will be written to enforce the PGS objects → invariants → rule → resolved/unresolved/invalidated frame and the strict separation vocabulary from the first line.

See LOOP_LEDGER.md for the living execution record.

Back to parent: research/12-rh-bridge/README.md (the strategy notebook that supplies the live target and verification matrices the loop reads).