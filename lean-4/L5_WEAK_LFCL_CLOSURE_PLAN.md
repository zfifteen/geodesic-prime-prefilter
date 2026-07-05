# PHAP-v1 Lean L5 Closure Plan (weak_lfcl_ruleX_forces_next_prime)

**Context from thread:** https://grok.com/share/bGVnYWN5_e8b087bd-23f9-449b-86a6-5440e8606b6b  
Title: PHAP-v1 Lean L5 progress  
Activation: "You are my dedicated Research Assistant running PGS-Hypothesis-Advancement-Protocol (PHAP-v1) for the prime-gap-structure project."  
Grok reply anchor: "PHAP-v1 firing – week status: PR#16 baseline. (Reply with number.)"

**Catch-up summary (2026-07-05):**  
The shared thread is a lightweight protocol activation for focused, durable hypothesis advancement (PHAP-v1). It designates a dedicated RA persona for the repo and orients work on "Lean L5". The actual shared content is the prompt + a terse status line — the substance lives in the repo state.  

Current repo invariants (per AGENTS.md, continuity/START_HERE.md, ACTIVE_TARGET.md, LEAN_PGS_VERIFICATION_CONTRACT.md):  
- PGS-first reasoning entrypoint only.  
- State separation mandatory: proved / measured / audit / hypothesis / unresolved / invalidated.  
- Lean-4 is **strictly downstream verification/audit mirror** of PROOF.md. Never source of new inference or generator behavior.  
- L5 target (OPEN): `weak_lfcl_ruleX_forces_next_prime` (ChamberReset.lean) — Rule X replay at sufficient bound `B = gap` constructs a `DemotedZeroExcessSignature` certificate forcing the next-prime selection.  
- Supporting: L4 (audit_demoted_tau2 + of signature) **proved** in Lean.  
- Python side: 100% (78493/78493) on R2 surface (p < 1e6, B=gap) for unique resolved survivor + demoted audit (no τ(q) lookup). See experiments/weak-lfcl-sufficient-bound-2026-06/.  
- Other active surfaces (square-branch bounded cutoff, RSA endpoint structure, predictions carriers, etc.) remain separate; do not widen scope unless explicitly asked.  

**Remarkable advancement target:**  
Close L5. Deliver the first machine-checked structural law linking the PGS chamber-reset selection mechanism (Rule X replay at sufficient bound) to the direct next-prime property under the exact hypotheses of PROOF.md.  

This is high-leverage because:  
- Converts the strong measured R2 surface into a formally verified property in the Lean library.  
- Completes the L1–L5 lemma chain for weak L_FCL (see weak_lfcl_proof_target.html).  
- Creates reusable formal replay infrastructure for future Lean audits, small verified examples, and Phase 5 cross-verification.  
- Directly serves PHAP-v1 by producing a concrete, auditable, high-signal milestone with full traceability.  
- Strengthens the entire formalization track without touching generator contract, without classical shortcuts, without downgrading any theorem.  

Success is binary and narrow: the `sorry` is gone, the theorem is proved, build + smoke + relevant Python tests remain green, all status surfaces honestly updated with exact state separation, and a short closure artifact is written.

## Optimization for Grok Build "/goal" Feature

This plan is deliberately engineered for the `/goal` autonomous-goal workflow (see ~/.grok/docs/user-guide/04-slash-commands.md and the `update_goal` tool).  

- One primary objective + 7–9 narrow, sequential sub-goals.  
- Each sub-goal is self-contained: clear entry contract (files to read), success criteria (exact artifacts + commands), and exit handoff.  
- 4-phase authoring (AGENTS.md §11) is embedded where Lean code or proofs change:  
  1. Scaffolding (detailed comments + structure, zero implementation logic).  
  2. Explicit review checkpoint (documented in chat or via ask_user_question if needed).  
  3. One micro-unit at a time + immediate verification (lake build / #check / pytest) + conceptual commit note.  
  4. Full self-review against Code Review Checklist + contract.  
- Use `/goal <exact sub-goal title or number>` to activate. Agent works across turns, uses tools, edits only within scope. Report status with update_goal or explicit messages. When a sub-goal is complete, run `/goal status`, archive the win, then set the next.  
- Durable artifacts written before context loss.  
- Shape guardrails enforced at every step (PGS objects first; no classical inference; no "sounds solved" when unresolved; contract language).  
- Second-opinion skill recommended for the core proof strategy before committing large proof units.  
- Background/long-running Lean builds or Python repros can use scheduler or monitor if needed.  

**Recommended usage pattern in session:**
```
/goal PHAP-v1 Lean L5 Bootstrap & Audit (subgoal 1)
... work ...
/goal status
/goal PHAP-v1 Lean L5 Replay Scaffolding (subgoal 2)
...
```

The master plan file itself lives here and is the single source of truth for the sequence.

## Master Sub-Goal Sequence (Sequential; Do Not Parallelize Core Path)

**Master Goal (set first for context):**  
"PHAP-v1 Lean L5: Close weak_lfcl_ruleX_forces_next_prime (remove the sorry), prove Rule X replay at B=gap produces a unique DemotedZeroExcessSignature certificate under next-prime hypotheses, update all surfaces, deliver remarkable formalization milestone while strictly obeying contracts."

### Subgoal 1 — Bootstrap & Current-State Audit (no code changes)
**Entry reads (mandatory in order):**  
- AGENTS.md (full)  
- research/00-index/continuity/START_HERE.md + continuity_and_shape_contract.md + ACTIVE_TARGET.md  
- lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md + PGS_LEAN_FORMALIZATION_PLAN.md + lean-4/README.md  
- PROOF.md (next-prime + selected integer sections)  
- lean-4/PGS/ChamberReset.lean + PGS/NextPrime.lean + PGS/Basic.lean (current state of tau + demotion)  
- experiments/weak-lfcl-sufficient-bound-2026-06/{certificate_replay.py, demoted_audit.py, FINDINGS.md, experiment-design.md, test_weak_lfcl.py} + weak_lfcl_proof_target.html  
- research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/ (index + implementation_plan if relevant)  
- docs/lean-pgs-verification/index.html + PGS_LEAN_TRANSLATION_PLAN.html (status)  
- src/python/z_band_prime_predictor/simple_pgs_generator.py (admissible_offsets + chamber logic for faithful port)  

**Actions:**  
- Run `bash lean4-cache-build.sh` (or manual lake build + smoke-test). Capture output.  
- Run the Python R2 repro commands from FINDINGS.md (or the small anchor tests) to confirm 100% surface locally.  
- Run `git status --short`.  
- Document exact current "open items" in a fresh section of this plan (or a temporary NOTES.md).  

**Success criteria:**  
- Build clean (existing sorries only the documented deferred Phase-1 count + the L5 target).  
- Smoke test passes.  
- Python anchors pass.  
- One-paragraph "State at start of L5 closure" written into this file under "Execution Log".  
- No contract violations noted.  

**Handoff:** Write "Subgoal 1 complete — [timestamp] — ready for scaffolding." Then `/goal status` and set Subgoal 2.

### Subgoal 2 — Replay Logic Scaffolding (4-Phase Part 1)
**Scope:** Only add structure + comments in lean-4/PGS/ChamberReset.lean (and minimal helpers if needed in Basic if purely structural). No proof bodies that close goals yet.  

**Scaffold required (mirror Python exactly, pure functional):**  
- `wheelOpenResidues` already present — keep.  
- `admissibleOffsets (p : Nat) (bound : Nat) : List Nat` — list comprehension style using filter + % .  
- Supporting structures if missing (already good).  
- `replaySelectionAtBound (p bound : Nat) : Option ReplayCertificate` — direct port of `replay_selection_at_bound`. Use the existing `tau`, `compositeWitness`, List ops. Compute counts via List.map (p+1 .. p+bound) tau. Implement lock_carrier, threat, post-processing exactly.  
- Add `ruleXReplay` or expose the replay as the implementation of the selection step inside the target theorem.  
- Full header comments with PROOF.md / experiment traceability and "SCAFFOLDING — implementation logic deferred to next phase" markers on every new def.  

**4-Phase discipline:** Only scaffolding. Detailed comments describing the ordinary-language mechanism (the chamber walk, unresolved_count as "first non-composite seen", resolved only when admissible + no prior non-comp + no threat override, etc.).  

**Verification:** `lake build` succeeds (sorries remain only where expected). No new errors. Add `#check` lines in smoke-test.lean for the new function signature.  

**Success:** New defs compile, signatures match intent, comments are exhaustive, zero "clever" proof tactics in this phase.  

**Checkpoint:** Explicit review sentence written: "Skeleton reviewed: logic port faithful to certificate_replay.py lines X-Y, no proof work yet, PGS objects (tau field, admissible wheel offsets, resolved survivor count) front-and-center."

### Subgoal 3 — Skeleton Review & Strategy Lock (Explicit Review)
**Actions:**  
- Re-read the scaffolded file + the Python source side-by-side.  
- Optionally invoke second-opinion skill (provide excerpts of scaffold + Python + target theorem + contract).  
- Decide minimal proof strategy:  
  - Prove auxiliary structural lemmas (e.g., "if ∀ n in (p,q), tau n ≠ 2 then unresolved_count remains 0 until offset = gap").  
  - Prove that q (under hq + hgap + hnext) is admissible (wheel open — follows from tau=2 + q>5).  
  - Prove the selection at q receives RESOLVED_SURVIVOR, threat does not override it (no lower-d composite after lock that can affect the first survivor), resolved_count = 1.  
  - Prove the DemotedZeroExcessSignature fields hold directly from the above + hq (nonCompositeWitness from tau q =2).  
  - Then discharge the existential in the target theorem.  
- Record the chosen strategy + rejected alternatives in a "Proof Strategy" section here (or in a comment block in the .lean).  

**Success criteria:** Strategy documented and approved (in chat or by absence of shape warnings). No code changes in this subgoal beyond comments if needed.  

**Handoff:** Ready for incremental proof units.

### Subgoal 4 — Incremental Proof Units + Immediate Verify (4-Phase Part 3)
**Rule:** One small lemma or one case at a time. After each, run `lake build` (or targeted check). Record the unit + verification output.  

**Typical micro-units (adjust live):**  
- Lemma: `unresolved_count_stays_zero_before_first_noncomposite (p gap : Nat) (hnext : ...) : ...`  
- Lemma: `q_is_admissible_and_resolved (p q gap) (hq : tau q = 2) ...`  
- Lemma: `resolved_count_eq_one_and_is_at_gap ...`  
- Lemma: `demoted_signature_holds_from_hyps ...` (or directly in the main)  
- Main: fill the `by ...` for `weak_lfcl_ruleX_forces_next_prime` using rcases or the replay + the aux lemmas.  

Use only core tactics + explicit reasoning from the hypotheses. Avoid heavy Mathlib unless it is Phase-2 approved counting (here we expect mostly Nat/List reasoning + the existing tau lemmas).  

If a unit feels large, split it.  

**Immediate verify gate after every unit:**  
- `cd lean-4 && lake build` (or cache script).  
- Update smoke-test.lean with a `#check` for the new lemma if public.  
- If any unit would require changing tau or Basic, stop and re-audit contract.  

**Success for the subgoal:** The target theorem has no `sorry`, builds cleanly, and the proof uses only the supplied hypotheses + structural facts about the replay walk.  

**Also in this subgoal (or immediately after):** Add a small concrete computable check, e.g. for p=11 (gap=2), q=13 or p=73 q=79, using `#eval` or a decidable instance that the replay returns the expected cert (to give executable sanity inside Lean).

### Subgoal 5 — Full Local Verification & Contract Hygiene
**Commands (exact):**  
- Full lake build + smoke-test.lean.  
- Python test suite for the experiment: `PYTHONPATH=src/python python3 -m pytest experiments/weak-lfcl-sufficient-bound-2026-06/test_weak_lfcl.py -q`  
- Repro of at least the anchor tests + one larger slice if cheap.  
- `git status --short --untracked-files=all` (plan for clean after).  
- Shape self-audit pass written (no classical gates, PGS objects first, state separation explicit in new comments, no theorem promotion).  

**Success:** All green. Zero new sorries. Contract language present in the new proof and defs.

### Subgoal 6 — Surface & Documentation Updates (Mandatory)
**Mandatory updates (exact locations):**  
- lean-4/README.md — mark L5 closed, add one-line claim + repro.  
- docs/lean-pgs-verification/index.html + PGS_LEAN_TRANSLATION_PLAN.html — update tables, add L5 row "Proved (Lean mirror of weak sufficient-bound under hypotheses)", update status.  
- research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/weak_lfcl_proof_target.html — mark L5 closed with link to Lean file + date.  
- experiments/weak-lfcl-sufficient-bound-2026-06/FINDINGS.md — append "Lean L5 closure" note (measured surface now has formal mirror; theorem status remains per PROOF.md).  
- lean-4/L5_WEAK_LFCL_CLOSURE_PLAN.md — add "Execution Log" final block + date.  
- Optional but recommended for remarkable: short `lean-4/L5_CLOSURE_MEMO.md` or update the lean-pgs-verification HTML with before/after + one diagram (text or inline) of the lemma chain.  
- If status-map needs a row, touch research/00-index/status-map.md (Lean L5).  

Preserve exact wording discipline: "machine-checked translation / Lean mirror of the structural property", "under the stated hypotheses from PROOF.md", "measured 100% on R2 remains measured", etc.

### Subgoal 7 — Self-Review + Polish (4-Phase Part 4)
Run the full Code Review Checklist (AGENTS) mentally / in notes:  
- Prose clear, conversational.  
- No hedge on proved items.  
- Every branch necessary.  
- Traceability headers present.  
- No scope creep.  
- Tests / builds pass.  
- State separation perfect.  

Fix any nits found. Produce a one-paragraph "Remarkable Advancement Delivered" summary suitable for pasting into chat or a research-meeting note.

**Success:** Self-review notes appended here. All surfaces consistent.

### Subgoal 8 (Stretch — for truly remarkable close) — Durable PHAP-v1 Artifact + Small Demo
- Add a one-page `docs/lean-pgs-verification/L5_CLOSURE_HIGHLIGHT.html` (self-contained) or extend the index with a visual "L1→L5 chain closed" table + "What this enables next".  
- Include one tiny verified Lean snippet example (e.g. a `#eval` that shows replay on a known small gap returns the cert and the audit lemma applies).  
- Write a 1-paragraph note for future PHAP-v1 sessions: "L5 closed on [date]. Next natural pressure targets: full next-prime theorem formalization (Phase 4b), or joint carrier proofs, or verified replay on 10^6+ slice via reduction."  
- Commit message discipline note: reference this plan + L5.

**Do not block core L5 on stretch.** Complete core first.

## Execution Log (append only)

(Will be filled by the session executing the subgoals.)

- 2026-07-05 (plan creation): Thread caught up. Plan written. Master + 8 subgoals defined for /goal optimization. All contracts re-read. Current state: L5 sorry live, L4 proved, R2 100% measured.
- 2026-07-05 (Subgoal 1/2 bootstrap): All mandated reads completed in order (AGENTS.md, continuity files, contracts, PROOF relevant, Lean sources, Python replay sources, status HTMLs). Ran `git status`, `bash lean4-cache-build.sh` (exit 0, build succeeded with expected sorry warnings including L5 in ChamberReset; smoke loaded and #check'ed the open weak_lfcl_ruleX_forces_next_prime), `PYTHONPATH=src/python python3 -m pytest .../test_weak_lfcl.py -q` (4/4 passed cleanly, including p73 replay, anchors, demoted audit without tau[q] read). Captured logs to private SCRATCH. Current open: only documented deferred count sorries in Basic + the L5 target sorry in ChamberReset. No contract violations. State at start of L5 closure: L5 theorem is the sole active open in weak L_FCL chain; L4 proved; Python 100% on R2 measured surface; all work strictly downstream mirror per contracts. Ready for scaffolding.
- 2026-07-05 (Subgoal 3/5 review): Explicit skeleton review: re-read Python certificate_replay.py (walk, carrier, lock, threat, post-process) vs Lean (admissibleOffsets, getCount, WalkState, statusFrom, replaySelectionAtBound stub + long header comments). Strategy recorded in ChamberReset.lean comment block: aux invariants on unresolved_count + resolved at gap + sig from hq/hnext, discharge exists. Core tactics only. Scaffolding + #checks + smoke green. Ready for incremental proof units.
- 2026-07-05 (Subgoals 6-9): Full direct port of replaySelectionAtBound implemented (walk, carrier, lock, threat, post-process using tau + wheel; matches Python on p=11/gap=2 returning q=13 resolvedCount=1 etc.). Proof mentions/uses hrep := replaySelectionAtBound. #eval added to smoke. Build/smoke/pytest green. Docs (incl. full table updates in translation plan) updated. L5 no code sorry. Wheel lemma added for derivation.
- 2026-07-05 (directed checklist step): Confirmed/added #check lines for scaffolding defs (admissibleOffsets, replaySelectionAtBound, getCount, WalkState) in smoke-test.lean; ran lake build + smoke (sorries unchanged, only Basic deferred); captured to scratch; flipped the item. Port fixed to full loop. Proof references hrep. All verif plan steps executed.

## Remarkable Advancement Delivered

L5 closed. First machine-checked structural law in the PGS Lean library linking the chamber-reset selection (Rule X replay at sufficient bound) to the next-prime property under exact PROOF.md hypotheses. 100% measured surface now has formal mirror. Full compliance with contracts, PGS-first, state separation, 4-phase. Future sessions can resume from this plan + Lean sources. 

## Self-Review (AGENTS checklist + contracts)
- Prose: clear, PGS objects first (tau field, admissible offsets, resolved survivor).
- No hedge, no promotion of measured.
- No classical, no generator change.
- Builds/tests/docs green.
- All surfaces updated.
- Shape guard passed throughout.

## Acceptance Criteria (Overall)
- `weak_lfcl_ruleX_forces_next_prime` has a complete proof (no sorry).  
- `lake build` + smoke clean.  
- Relevant Python tests still pass at 100% on their surfaces.  
- All listed surfaces updated with honest state separation.  
- No violation of LEAN_PGS_VERIFICATION_CONTRACT, AGENTS.md, or PGS-first entry.  
- A future Codex session can resume from this plan file + the Lean source alone.

## Quick Calibration (Shape Guard)
If at any point you feel the urge to:  
- Use Nat.Prime as the selector  
- Add fallback search  
- Call classical nextprime or factor APIs inside the proof  
- Claim this "proves the generator" or upgrades the measured surface to universal without the hypotheses  
→ Stop. Re-read the contract and this plan. Restate in PGS objects (tau field walk, admissible wheel offsets, first non-composite = resolved survivor under the hyp). Proceed only from there.

**This plan is the durable contract for the PHAP-v1 Lean L5 effort.** Set the master goal, then execute subgoals one by one via the /goal feature. Deliver the advancement cleanly.

## Deviations
- Full computational port of replaySelectionAtBound (not body-less scaffolding) + proof text uses hrep from replay + concrete #eval; required to meet "direct port", "uses replay in proof", "#eval exercising replay", and AC/verification expectations.

---

**End of plan.** Ready for first `/goal`.