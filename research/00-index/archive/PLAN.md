# Bootstrap Predictions Research Track

**Date**: 2026-05 (session initiating the effort)  
**Status**: Executing bootstrap per best judgment after user declined narrow scoping questions.  
**Goal**: Create a durable, PGS-native home for deterministic state-resolution research ("Predictions") without probabilistic framing, classical inference, or revival of invalidated paths.

## Context and Routing
- Newest request: "Let's begin a new research effort for this program: Predictions."
- Per research/00-index/continuity/START_HERE.md and status-map.md: request does not match pre-named targets, therefore route to most local PGS-native objects without sustained pressure (chain-horizon closure, endpoint-chain + modulus-link work, chamber reset / endpoint determinacy).
- "Predictions" interpreted strictly as deterministic forward resolution of future PGS chamber states, endpoints, and structural certificates using the established objects and invariants.
- This is **not** statistical forecasting, ML, density-based prediction, or classical candidate search.

## Mandatory Guardrails Applied
- PGS-first entry frame always: PGS objects → invariants → named rule/law → resolved / unresolved / invalidated state.
- All artifacts separate: theorem (from PROOF.md), measured, audited, hypothesis, unresolved, invalidated.
- No downgrade of proved theorems.
- Legacy "z_band_prime_predictor" naming and related language treated as documentation-correction concern (chapter 15) or future hygiene task inside the new track; not revived as active vocabulary.
- Documentation format: self-contained HTML for the primary contract surface (visual structure, tables, checklists).

## Numbered Bootstrap Steps (This Session)
1. **Directory skeleton**  
   Files: research/16-predictions/ and standard subdirs (docs/, output/, scripts/, tests/).  
   Command: mkdir -p ... (executed).  
   Verification: list_dir confirms structure.

2. **PLAN.md (this file)**  
   Written at repo root as the contract for the initiation work.  
   Verification: re-read after write.

3. **Primary research contract (HTML)**  
   File: research/16-predictions/index.html (self-contained, LF endings, embedded CSS, tables, no external assets).  
   Content requirements:  
   - Opens with observable PGS object description before any internal labels.  
   - States the 5 continuity questions (strongest claim, explicitly not proved, failed/must not revive, next session first action, reproduction command).  
   - Defines initial charter aligned to current center of gravity.  
   - Includes PGS Predictions Entry Frame and Shape Guardrails sections.  
   - Status separation table.  
   - Initial probe checklist.  
   Verification: re-read full file; open in browser (manual); confirm zero JS, zero external refs, clean rendering.

4. **Pointer README**  
   File: research/16-predictions/README.md (points to index.html, records bootstrap date and routing decision).  
   Verification: re-read.

5. **Status map registration**  
   File: research/00-index/status-map.md  
   Action: precise search_replace to add row under Phase 9 / migration table for `16-predictions`: "initialized from Predictions request, not-yet-gated".  
   Also add brief entry in the chapter map section if structure permits.  
   Verification: re-read the edited region; run grep for the new chapter name; confirm no breakage to existing rows.

6. **Report and handoff**  
   Text summary in chat: what was created, why the charter framing was chosen, open questions for user refinement, exact commands to view/reproduce the new surface.  
   No commits. New files remain untracked (existing untracked LWM literal-web work noted separately).  
   No experiments or code written, pure contract scaffolding.

## Open Questions / Risks (User Refinement Expected)
- Exact primary objects for first pressure (endpoint-chain traversal vs d4_count carrier extension vs chamber-reset geometry vs cross-chapter unification)?
- Desired first falsification experiment or certificate surface?
- Whether legacy predictor directory rename/audit should be pulled into 16-predictions or left in 15-documentation-correction.
- Any immediate tie-in to pgs-unsolved-problems/endpoint-determinacy/ or 06-cryptology-rsa structural certificates?
- Should the track own a dedicated test harness from day one, or remain documentation + probe scripts only until a concrete rule emerges?

## Success Criteria for This Bootstrap
- A future session (human or agent) can read research/16-predictions/index.html + status-map + PROOF.md + START_HERE.md and continue the Predictions effort at the correct epistemic level with no drift.
- All wording is PGS-deterministic; "prediction" is used only as shorthand for structural resolution / certificate closure.
- No classical gates, no probabilistic language, no revival of invalidated selectors.

## Next After User Review
- User approves or edits this plan and the created artifacts.
- Then execute first concrete probe (smallest high-leverage deterministic test on an existing carrier or chain-horizon surface).
- Add validation row to status-map only after a focused command exists and passes.

## Commands (Reproduction of Current Bootstrap State)
```bash
# View the contract
open research/16-predictions/index.html   # or xdg-open / browser

# Check registration
grep -n "16-predictions" research/00-index/status-map.md

# Full continuity bootstrap (always)
cat research/00-index/continuity/START_HERE.md
cat AGENTS.md
cat PROOF.md | head -100
git status --short --untracked-files=all
```

**End of plan.** This bootstrap was executed under best judgment after explicit decline of scoping questions. All content respects the full AGENTS.md (canonical + local) and research-continuity discipline.