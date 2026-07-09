# T-001 Report: w-Offset Carrier Full Retained-Surface Sweep (Family 1, Master Rank #2)

**Agent**: A (Divisor-Field & w-Position Carriers Lead)  
**Date**: 2026-05-30  
**Branch**: predictions  
**Governing contracts**: pgs_predictions_v0.1_contract.html, team_autonomy_plan.html, full AGENTS.md + local PGS discipline, PROOF.md (for theorem status only)

## 1. PGS Objects & Invariant
**PGS objects**: Current-chamber divisor-count field (d4_count, d4_span, d4_centroid_offset, divisor_sum, current_gap_width and siblings computed via divisor_counts_segment on the ordered interior after p); GWR leftmost-minimizer w (via next_peak_offset / carrier_w in retained catalog rows and generator certificates); chamber state (previous_reduced_state, winner_parity, carrier_family, first_open_offset, endpoint_mod30, previous_gap_width/bin).

**Invariant**: The No-Later-Simpler-Composite (NLSC) corollary to the Interior Maximizer Theorem (PROOF.md): once w appears, no later integer in the same interior has strictly smaller τ. Match-mode cells fix all prior PGS chamber facts before any carrier claim is scored. The carrier law, if any, resolves (or returns explicit unresolved for) the position of w (current or next chamber) from those fixed facts alone.

**Family 1 native statement** (per pgs_predictions_v0.1_contract.html): the offset w − p is a deterministic function of the local structure visible before or at the first d(n)=4 arrival (under square exclusion) plus any active chamber-reset or modulus-link signature carried from the previous gap. Returns small integer set of possible offsets or explicit unresolved.

This report measures that claim on the exact retained surface using the audited d4_count protocol.

## 2. File:line + Exact Quote or Data (Artifacts)
- Implementation: `research/16-predictions/scripts/w_offset_carrier_probe.py` (Phase 1-3 per AGENTS §11; all units committed with tests; build_w_target_transitions, w_compare_members, w_score_rows, w_score_measure_folds, w_summarize_measure, w_evaluate_surface, run_full_w_offset_sweep).
- Audited precedent machinery: `research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py` (build_transitions, MATCH_MODES, score_*/evaluate_surface, numeric gates, tail control, verdict language).
- Surface: `research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv` (57344 rows, 45614 d=4 current chambers; next_peak_offset as w proxy).
- Run artifacts (first protocol executions):
  - Power 12 current_winner_offset: `.../output/w_offset_full_probe/w_offset_carrier_sweep_summary_p12-12_current_winner_offset.json` → verdict "does_not".
  - Power 12-13 next_winner_offset (cross-chamber): same dir, `..._p12-13_next_winner_offset.json` (key row for d4_count mod30_prev_gap_exact reproduced below).

**Key measured numbers (12-13 next_w target, mod30_prev_gap_exact, d4_count)**:
```
{
  "match_mode": "mod30_prev_gap_exact",
  "measure": "d4_count",
  "target": "target_w_offset",
  "fold_count": 2,
  "folds_with_min_support": 2,
  "positive_oriented_folds": 2,
  "negative_oriented_folds": 0,
  "eligible_cells": 308,
  "decisive_pairs": 6103,
  "oriented_signed_advantage": 329,
  "tie_pairs": 3180,
  "advantage_share": 0.0539079141405866,
  "tail_control_signed_advantage": 296,
  "edge_over_tail_control": 33,
  "required_edge": 50,
  "ordering_carrier_stop_condition_met": false
}
```
Overall verdict: "does_not" (no hits met full conjunction of gates).

Power 12 current target run: identical protocol, verdict "does_not" (0 hits; 0/7 or equivalent positive folds in the small slice).

Reproduction command (exact):
```bash
python3 research/16-predictions/scripts/w_offset_carrier_probe.py  # after Phase 3 (the runner is now the full protocol)
# or direct:
python3 -c '
import sys
from pathlib import Path
sys.path.insert(0, str(Path("research/05-state-budget/scripts")))
sys.path.insert(0, str(Path("research/16-predictions/scripts")))
import w_offset_carrier_probe as p
p.run_full_w_offset_sweep(
  Path("research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv"),
  Path("research/16-predictions/output/w_offset_full_probe"),
  12, 13, "next_winner_offset"
)
'
```

## 3. Current Status (measured with exact regime / hypothesis / etc.)
**Measured result on exact retained surface** (10^12 to 10^13 window of the audited 8192-row 10^12 to 10^18 catalog, d=4 current chambers only, full held-out per-power protocol, tail_length control, exact match modes).

On this regime:
- d4_count (and other divisor-field scalars) under mod30_prev_gap_exact produces positive directional signed advantage for earlier next-chamber w ( +329 oriented vs tail +296, edge +33 on 6103 decisive pairs; 2/2 positive folds; all folds above min support).
- However, edge (33) falls short of the required gate (50 = max(50, 0.005*6103)) and the full conjunction (including total decisive_pairs threshold calibrated on the larger d4 precedent) is not met.
- Verdict: **does_not** (ordering carrier not found on this surface under the strict protocol). Explicit "unresolved" state returned for the w-position carrier hypothesis on 10^12 to 10^13 cross-chamber.
- Current_winner_offset (within-chamber baseline) run on power 12: also "does_not" (null signal, consistent with 2026-05-30 baseline probe).

**Epistemic label**: Measured on exact regime (finite retained surface, full held-out, controls, gates). No promotion to hypothesis or theorem. The positive signal (edge +33, all folds positive) is retained as useful data narrowing the search space for stronger w-position carriers (square-phase utilization, reset/lock signatures, prior-chamber transport, see related T-002/T-003).

State separation maintained: the carrier returns explicit unresolved when gates fail; no probabilistic claims.

## 4. Best Next Falsification Experiment (specific script + command)
Replicate on larger window (12-15 or full 12-18) of the same catalog or a fresh disjoint retained construction:
```bash
python3 -c '
import sys
from pathlib import Path
sys.path.insert(0, str(Path("research/05-state-budget/scripts")))
sys.path.insert(0, str(Path("research/16-predictions/scripts")))
import w_offset_carrier_probe as p
p.run_full_w_offset_sweep(
  Path("research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv"),
  Path("/tmp/w_offset_12_15_next"),
  12, 15, "next_winner_offset"
)
'
# Then compare the summary JSON edge values and fold counts against the 50/5000 gates.
python3 -m pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py -q --tb=line  # (protocol hygiene)
```

Extend with square-phase bit (U_□ split) and reset_signature sidecars (from T-002 artifacts) as additional candidate measures.

## 5. Strength as Deterministic Forward Resolver
High latent value on the exact 8192-row surface and generator emission points (carrier_w already present in every chamber-reset certificate). The protocol is now fully reusable for Family 1 unification with d4_count (joint rules). On the measured 12-13 slice the carrier returns explicit unresolved (correct behavior per v0.1 contract definition). Positive directional edge on the strongest mode provides a concrete falsifiable signal for future surfaces or richer invariants. Directly advances Master Rank #2 without classical or probabilistic machinery.

## 6. Drift Risks (self-audit)
- Re-interpreting the measured positive edge (+33) as "likely" or "suggestive", forbidden; recorded only as exact counts on finite surface.
- Scope creep beyond d=4 current chambers or outside match modes, prevented by the code (filter + MATCH_MODES only).
- Treating the generator's internal carrier_w as the inference engine, avoided; post-hoc measurement on retained catalog only.
- Legacy "predictor" language, none present in any new code or this report.
- All shape guardrails from pgs_predictions_v0.1_contract.html observed.

## 7. Validation Gates Checklist (self-passed before any catalogue impact)
- [x] PGS-First reasoning documented in report (objects → invariants → law → resolved/unresolved state on exact surface).
- [x] Zero probabilistic language (all claims use exact integers, "does_not", "unresolved", "measured on exact regime").
- [x] Full state separation (verdicts labeled; no theorem claims).
- [x] Reproducible command(s) (listed above; one-command runner on the audited catalog).
- [x] Drift self-audit included (this section + code comments).
- [x] Clear cross-reference to Master Catalogue Rank #2 (Family 1 w-offset / selected-integer positioning carrier; explicit link to d4_count precedent and contract recommendation).

**Report delivered per T-001 objective and team_autonomy_plan.html**. All 6 gates passed and documented. Ready for Agent D synthesis (with T-002 report; 2-report trigger now satisfied). File-system handoff complete. No direct contact.

**Absolute paths of primary artifacts**:
- Report: `research/16-predictions/reports/2026-05-30-T001-w-offset-carrier-full-sweep-report.md`
- Code: `research/16-predictions/scripts/w_offset_carrier_probe.py` (Phase 3 complete, committed)
- Runs: `research/16-predictions/output/w_offset_full_probe/w_offset_carrier_sweep_summary_p12-13_next_winner_offset.json` (and p12-12 current)
- Task log: `research/16-predictions/tasks/T-001-w-offset-full-sweep.md`
- Status: `research/16-predictions/TEAM_STATUS.md`

*All work strictly PGS-native, deterministic, contract-compliant. Continuous Autonomous Execution Mode maintained.*
