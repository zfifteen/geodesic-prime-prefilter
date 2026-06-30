# PLAN.md — Remainder Statistics Collection for Prime Gap Structure

**Task:** Quantify remainder (residue) distributions and correlations inside prime gaps relative to GWR positions, minimum-d(n) carriers, and gap termination points. Produce auditable Python artifacts, datasets, and measured surfaces while strictly preserving PGS deterministic framing and state separation.

**Date:** 2026-06-30
**Agent:** Grok (xAI)
**Branch:** (current session; no branch change yet)
**Status:** Phase 1 scaffolding initiated per user catch-up plan + full AGENTS.md + local contract.

## 1. Objectives
- Deliver pure-stdlib `remainder_utils.py` with `compute_residues`.
- Produce collector `collect_remainder_stats.py` that reuses existing gap/d(n) walk logic to emit per-interior records.
- Generate reproducible line-delimited JSON raw records + aggregate summaries for initial bounds.
- Run clean on 100-gap test set, then produce first real surface for >=10^5 gaps.
- Document measured correlations (or their absence) with proper effect sizes; keep as hypothesis/measured layer.
- Create `research/remainders/` with plan, scripts, RUN_LOG.md, later summary (prefer HTML for visuals).
- Preserve all PGS invariants and contracts.

## 2. Background & Constraints
- Full read of canonical code-style/AGENTS/AGENTS.md (incl. phased authoring 1-4, prose style, PLAN contract, python/math satellites).
- Full read of local Agents.md (PGS-first: start from ordered prime-gap state, divisor-count field, GWR/leftmost min-divisor rule, endpoint, unresolved state; deterministic only; classical % allowed only for audit/feature extraction downstream, never for choosing q).
- Read: PROOF.md (GWR and direct next-prime theorems universal under hypotheses; tau=2 defines termination), RESULTS.md (current surfaces, state separation required), PRIME_GAP_GENERATOR.md, gwr_boundary_walk.py, predictor.py, z_band_prime_composite_field/field.py, z_band_prime_invariant/core.py.
- User-provided plan is the detailed spec (Phase 1-5).
- Reuse existing gap iteration and d(n) (prefer divisor_counts_segment for speed on validation bound; exact_divisor_count for reference cross-checks).
- Remainder module: **pure Python, stdlib only** (no numpy/gmpy/sympy inside remainder_utils.py).
- Moduli list and binning versioned.
- All research outputs separate: proved (PROOF), measured (this), hypothesis, audit, unresolved.
- Do not downgrade theorems, do not reframe GWR or next-prime as statistical.
- Incremental: each script validated on 100-gap set before scale.
- Hand verification on small fully-known gaps (e.g. after 113,139,199).
- Python 3.11+ (project).
- Later integration path feeds high-signal patterns only as candidate prefilter features or for theorem-tightening exploration (kept separate).
- Documentation: use self-contained HTML under research/remainders/ or docs/ when visuals/checklists benefit.

## 3. Open Questions / Risks
1. Preferred exact initial moduli list and version tag?
   - Current proposal (from plan): [2, 3, 5, 7, 30, 210, 2310] (primorial sequence). 
   - Will default to this; record "M_v1" in outputs.
2. Max starting prime p for first full collection run after tiny validation?
   - Plan: <= 10^7 left endpoint for fast validation.
   - Practical first real: 10^6 (covers >>10^5 gaps; pi(10^6) ~78k, cumulative gaps sufficient).
   - 10^7 available for stratified follow-up.
3. Reuse strategy for gap iteration in collector?
   - Primary: import and drive from gwr_boundary_walk.gwr_next_gap_profile or build streaming interior emitter that reuses divisor_counts_segment + tracks is_current_min_d and distance_to_next.
   - Pure-slow reference path using invariant.exact_divisor_count for cross-checks on <1e6.
   - Ensure no classical primality inside generation path.
4. Should collector emit full raw records even for large runs, or stream aggregates only?
   - Plan: raw append-only JSONL for reproducibility; aggregates separate. For 10^7 may need sampling flag.
5. Interaction with existing prefix-based pruning / wheel logic (mod-30 in generator)?
   - This will be measured post-hoc; captured as hypothesis for integration step.
6. Statistical package choice for Phase 3?
   - Keep minimal initially (stdlib or numpy for counts/corrs since collector env has deps). Pure post-processing script separate.
7. Risk of shape drift: statistical language used for measurement layer only. Will enforce explicit "measured on regime X", "hypothesis H1 under test", never "GWR works because...".

## 4. Detailed Execution Steps

Use strict 4-phase code authoring for every new/modified module.

| Step | Description | Files/Commands | Verification Method | Status |
|------|-------------|----------------|---------------------|--------|
| 0 | Bootstrap reads + PLAN creation | Read all listed continuity + code + plan files; write this PLAN.md | Re-read PLAN.md; git status; todo status | IN PROGRESS |
| 1 | Create research/remainders/ skeleton dirs + PLAN | mkdir via write or terminal; this file | list_dir research/remainders; re-read | PENDING |
| 2 | Phase 1 scaffold: remainder_utils.py (pure) | research/remainders/remainder_utils.py : only signatures, full docstrings, detailed inside-body comments describing intended logic. No executable arithmetic body. | read_file after write; python -m py_compile succeeds (skeleton) | PENDING |
| 3 | Phase 2: self-review scaffold | Internal: check against plan Step1, PGS frame, prose style, types, error handling. Update comments if needed. | Document review notes in chat + update file if changes | PENDING |
| 4 | Phase 3a: implement + test compute_residues | Implement body; add or update minimal test (e.g. research/remainders/test_remainder_utils.py or inline). Run on known small n. Commit-granular mindset. | Run the test function; cross-check residues by hand (113%2==1 etc); pytest if structure; ruff/mypy if configured | PENDING |
| 5 | Phase 3b/4 + collector scaffold + tiny validation | Scaffold then implement collector script (reusing gap logic); 100-gap test driver. Must run cleanly producing expected JSONL shape + basic aggregates. | Execute collector --max-p 300 or equivalent on first ~100 gaps; inspect output records vs hand computation for 5-10 gaps (e.g. p=113 gap); verify is_current_min_d and distance fields | PENDING |
| 6 | Basic aggregation + RUN_LOG | Add post-processing in collector or separate; create RUN_LOG.md with command, python --version, machine note (M1 Max), moduli version. | Repro: re-run same command on same tiny set yields identical records | PENDING |
| 7 | Scale to first 10^5+ gaps (or 10^6 bound) | With --sample-rate if needed; produce dataset + marginals + simple corrs. | Record exact command + counts (gaps processed, records emitted); verify no crashes; basic chi2 or count tables produced | PENDING |
| 8 | Hand verification + cross check | Explicit checks on gaps after 113,139,199 and <1e6 full factor match. | Script or manual table in remainders/VERIFICATION.md or output | PENDING |
| 9 | Initial hypothesis measurement writeup | Measured surfaces + any significant (or null) findings for H1/H2; effect sizes. Separate from proof language. | New file or section in research/remainders/ | PENDING |
| 10 | Update RESULTS.md + create initial summary (HTML if visual) | Append pointer + high-level measured result. research/remainders/index.html or summary.md | Re-read updated files; confirm separation of concerns | PENDING |
| 11 | Final self code review + lint/test | Full checklist; ruff, mypy (or equiv), run all local tests for touched pieces | Zero errors; checklist notes | PENDING |

## 5. Deliverables
- research/remainders/PLAN.md (this)
- research/remainders/remainder_utils.py (pure, tested)
- research/remainders/collect_remainder_stats.py (CLI per plan: --max-p, --moduli, --output-dir, --sample-rate)
- Small test/validation scripts or functions
- Raw JSONL + aggregate outputs for validated regime
- RUN_LOG.md entries
- Later: VERIFICATION.md, measured findings, integration notes
- Updates to top-level RESULTS.md
- (optional) research/remainders/index.html for visual summary

## 6. Success Criteria
- 100-gap test passes cleanly for skeleton + first collector before any larger run.
- >= first 10^5 gaps (or equivalent) produce reproducible dataset.
- At least one documented measured correlation (or clear quantified absence) with effect size between remainder features and (GWR label or termination).
- Code reads as conversational English; follows prose, types, phased procedure.
- No violation of local PGS contract (deterministic framing preserved; stats kept as measurement).
- Future researcher can `python collect... --max-p 100000 ...` and obtain matching results from RUN_LOG.

## Commands (Reproduction)
```bash
# After each change
cd /Users/velocityworks/IdeaProjects/prime-gap-structure
python -m py_compile research/remainders/remainder_utils.py
python research/remainders/collect_remainder_stats.py --help
# Tiny validation example (to be finalized in impl)
python research/remainders/collect_remainder_stats.py --max-p 2000 --output-dir research/remainders/output/tiny/
# Full first run (example)
python research/remainders/collect_remainder_stats.py --max-p 1000000 --output-dir research/remainders/output/1e6/
cat research/remainders/RUN_LOG.md
```

## PGS-Native Framing for This Work (Mandatory)
Start frame for analysis:
ordered prime-gap state (p, interiors n=p+1..q-1, q) -> divisor-count field on interiors -> GWR rule selects leftmost min d(n) carrier w -> remainder vector of each interior relative to M -> measured frequency / conditional / MI of residue vs GWR-winner flag vs termination distance.

All output records will carry gap_id/p , relative k, d(n), is_current_min_d, distance_to_next, remainder_vector.

Classical residue computation is feature extraction for post-analysis only.

## Approval
This plan adopts the user's detailed 5-phase collection plan as primary spec. Operator may approve via edit or "proceed", or request changes.

**End of plan.**
