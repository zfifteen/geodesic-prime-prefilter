# PLAN — T-002: Chamber-Reset Signature + Lock Transport Carrier Hypothesis (Agent B)

**Date created**: 2026-05-30  
**Branch**: predictions  
**Governing contracts**: pgs_predictions_v0.1_contract.html, team_autonomy_plan.html, full AGENTS.md (canonical + local), PROOF.md (for any theorem claims)  
**Master Catalogue target**: Rank #3 — Chamber-Reset Signature / Lock / Threat Transport & Carrier Cut  
**Task file**: research/16-predictions/tasks/T-002-reset-lock-transport.md  

## Purpose (PGS-First Frame)
Begin from PGS-native objects only:
- Ordered prime-gap chamber state after known prime p (divisor-count field τ(n) for n = p+1 … q-1).
- GWR leftmost minimum-τ integer (selected integer w / carrier_w).
- Chamber-reset state certificate (pgs_chamber_reset_state_certificate): carrier_offset/d (first min-d>2 post-p), lock_carrier_offset/d (first resolved-survivor that captured a carrier), lower_d_threat_offset (first post-lock offset with 2 < τ < lock_d), tail_after_reset_offsets, reset_deadline semantics.
- Previous-to-current chamber transport of the above (carrier shift, lock hardening, reset signature carried forward).
- Explicit resolved / unresolved / invalidated states for any carrier law.

The objective is to instrument emission of the full richer sidecar set (reset_signature as compact deterministic encoding, lock_carrier_*, lower_d_threat_*, tail counts, carrier_d) onto the exact 8192-row-per-power retained surface already used for d4_count (10^12..10^18), then derive the first explicit deterministic carrier hypothesis for next-chamber reset activation, tail policy, or boundary behavior from those objects.

All language: deterministic only. Every claim labeled with exact epistemic status + supporting artifact. No classical inference engine; no probabilistic framing.

## High-Level Steps (Numbered Contract)

1. **Mandatory Onboarding & Audit (COMPLETE)**  
   - Read team_autonomy_plan.html, predictions_master_catalogue.html (Rank #3 emphasis), pgs_predictions_v0.1_contract.html, T-002 task file, TEAM_STATUS.md.  
   - Review four catalogues (especially reset/lock/transport mentions in endpoint-chain-modulus-link... and gwr-dni-generator... from Agents 1/3/4).  
   - Review generator emission: src/python/z_band_prime_predictor/simple_pgs_generator.py (pgs_chamber_reset_state_certificate lines 32-149, carrier/lock/threat scan 48-95, chamber_reset_fields).  
   - Review C exposure: src/c/high-scale-pgs/include/pgs_high_scale.h (pgs_certificate_t fields 55-62).  
   - Review key 01-generator docs (previous_to_current_carrier_shift_lock_hardening.md, previous_chamber_reset_lock.md, pgs_chamber_reset_v1_*.md, boundary_law family).  
   - Review ch05 retained machinery + recent w_offset baseline probe (null within-chamber result increases value of carried reset/lock features).  
   - Self-audit against shape guardrails in v0.1 contract and local Agents.md (PGS objects first; no legacy z_band framing as active engine; state separation).  
   - Update todo tracker and this PLAN.

2. **Create This PLAN.md (Current Step)**  
   Document full dependency tree, risks, validation gates, 4-phase code authoring for any new script, reproduction commands, exact artifacts to produce.  
   This PLAN is the contract; execution follows it exactly with FS artifacts for every handoff.

3. **Phase 1 — Scaffolding Only (Mandatory per canonical AGENTS.md §11)**  
   - Create new file research/16-predictions/scripts/reset_lock_transport_sidecar_emitter.py (modeled on audited w_offset_carrier_probe.py + state_budget_divisor_carrier_sweep.py transition logic for hygiene).  
   - Full signatures + type annotations for every function.  
   - Detailed docstrings and inline comments (conversational technical English prose per §10) describing exact responsibilities, control flow, edge cases, PGS object mappings, state-separation invariants, and why each piece exists — **zero executable implementation logic** (pass, NotImplemented, or comment placeholders only in bodies).  
   - CLI entrypoint, CSV/JSONL writers, certificate wrapper (thin), signature builder, transition augmenter, held-out friendly structure.  
   - No changes to any existing catalog builder or core generator. Sidecar-only.  
   - Include reproduction comment block at top.  
   - Commit the skeleton as a distinct git commit labeled "T-002 Phase 1 scaffolding: reset/lock sidecar emitter skeleton (comments only)".

4. **Phase 2 — Explicit Skeleton Review (Mandatory)**  
   - Read the full skeleton file.  
   - Walk every function comment for logical consistency, missing PGS invariants, boundary errors, drift risk, alignment with T-002 objective and Rank #3 recommended action.  
   - Verify: emission path calls only pgs_chamber_reset_state_certificate (pure PGS-native, no classical); output is strictly sidecar (no mutation of retained details.csv); match-mode reuse from audited code; explicit "unresolved" paths documented.  
   - Revise comments/structure if gaps found; record review findings as comment block or separate audit note in docs/.  
   - Only after documented self-review pass: proceed.

5. **Phase 3 — Incremental Implementation + Immediate Test + Commit (Mandatory)**  
   Implement **one small unit at a time**:
   - Unit A: thin deterministic wrapper around pgs_chamber_reset_state_certificate + reset_signature compact encoder (string of form "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=3"). Immediate pytest or inline smoke test calling on known small p values (e.g., 3,11,101). Commit.
   - Unit B: detail-row loader + per-chamber p extraction (reusing phase_probe logic for hygiene). Test. Commit.
   - Unit C: transition augmentation that attaches previous-chamber carried fields + current reset sidecars (for transport hypothesis). Test round-trip on 10^12-10^13 subset. Commit.
   - Unit D: CSV/JSONL writer + CLI driver (modeled exactly on existing probes). Test full emission on modest window. Commit.
   - Each commit message references T-002 + phase + unit. Use `git add` + `git commit` via tools. No batching of logic.
   - After each, run `python -m pyright` or project type/lint if configured; fix before next unit.
   - Produce enriched sidecar artifact: e.g. research/16-predictions/output/reset_lock_sidecars_8192_subset/ or on full if time permits (use 12-15 first for velocity, note exact surface).

6. **Analysis & First Carrier Hypothesis Formulation**  
   - Using emitted sidecars on the retained surface, compute exact counts under the same match modes as d4_count precedent (mod30_prev_gap_exact etc.).  
   - Identify any deterministic relation from (current d4_count + carried lock_carrier_d + lower_d_threat presence + tail policy from prior reset) → (next-chamber reset_signature components, or next tail_after_reset length category, or boundary drop behavior).  
   - State only what the surface resolves exactly or leaves unresolved. Example shape (never probabilistic): "Under mod30_prev_gap_exact match on the 10^12..10^18 8192-row surface, when prior-chamber lock_carrier_d==4 and lower_d_threat_offset is None, the next chamber reset_signature.lock_carrier_d resolves to 4 on N decisive pairs (exact count), returns unresolved on M pairs; no other values observed."  
   - Label epistemic status: measured result on exact regime (cite the emitted CSV + script command).  
   - Cross-reference prior 01-generator docs on previous-to-current shift (no downgrade of any candidate laws).  
   - Record raw numbers + reproduction command.

7. **Produce Structured Report in reports/**  
   - Filename: research/16-predictions/reports/2026-05-30-T002-chamber-reset-lock-transport-carrier.md (or .html per local docs preference for visual structure).  
   - Use 7-field format derived from original agent catalogues (PGS Objects & Invariant; Citations & Surfaces; Status (measured/hypothesis); Explicit Carrier Hypothesis (deterministic rule + unresolved cases); Reproducible Emission & Analysis Commands; Validation Gates Checklist (all 6 from team plan); Drift Self-Audit + Cross-Reference to Rank #3 + impact on other ranks).  
   - Embed or link exact counts/tables from run.  
   - Lead with concrete PGS object description before any labels.  
   - End with clear "Next Action for synthesis" only after gates.

8. **Task & Status Updates (FS Handoffs Only)**  
   - Update research/16-predictions/tasks/T-002-reset-lock-transport.md : mark gates, add links to report + enriched data + reproduction, record hypothesis summary.  
   - Update TEAM_STATUS.md : set T-002 status to "Report delivered; awaiting Agent D synthesis after gates"; list new artifacts (report path, sidecar CSV path, PLAN, script). Note "synthesis request via FS update".  
   - No direct messages; file system is the handoff.

9. **Phase 4 — Full Structured Self-Review Against Code Review Checklist**  
   - After all code + report, run the canonical checklist (prose style, structure, testing, edges, correctness, lint/types, docs, conventions, AGENTS adherence including 4-phase execution).  
   - Fix every non-affirmative item.  
   - Append signed self-review summary (with date) to the report or a docs/ note.  
   - Run full project-relevant tests that touch the new script or generator (e.g. pytest research/01-generator/tests/test_simple_pgs_generator.py research/05-state-budget/tests/... -q).

10. **Final Validation Gate Pass + Close**  
    - Explicitly confirm all 6 validation gates in TEAM_STATUS and report.  
    - Only then note "Agent B requests synthesis round from Agent D (T-002 complete; gates passed)".  
    - Do not touch Master Catalogue (Agent D only).  
    - Archive any blocks in blocks/ if any (none expected).

## Reproduction Commands (Must Remain Valid)
```bash
# Emission (after script complete)
python3 research/16-predictions/scripts/reset_lock_transport_sidecar_emitter.py \
  --detail-csv research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv \
  --min-power 12 --max-power 13 \
  --output-dir research/16-predictions/output/reset_lock_sidecars_12_13

# Analysis (will be added to script or separate tiny reporter)
python3 -c "
from pathlib import Path
import csv
# ... load and count under match mode ...
print('exact counts...')
"

# Generator contract smoke (no change)
python3 -c '
from src.python.z_band_prime_predictor.simple_pgs_generator import pgs_chamber_reset_state_certificate
cert = pgs_chamber_reset_state_certificate(11)
print(cert and cert.get("lock_carrier_d"))
'

# Existing tests (must still pass)
python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py -q
```

## Risks & Mitigations
- Risk: Temptation to mutate core catalog or call non-PGS paths. Mitigation: sidecar-only design; all new code lives under 16-predictions/; import only the generator certificate function + audited transition helpers.
- Risk: Time on full 8192 (8 powers × 8192). Mitigation: start with 12-14 (or 12-13 as in baseline), document exact window; full run only if cheap. Note regime precisely.
- Risk: Formulating hypothesis that leaks probabilistic language. Mitigation: template sentences pre-written in PLAN; mandatory prose pass in Phase 4.
- Risk: Drift from previous-to-current 005B candidates in 01-generator. Mitigation: cite exactly; label as separate measured surface; do not integrate or promote.
- Risk: Violating 4-phase by writing logic too early. Mitigation: this PLAN + todo + explicit read-back of skeleton before any body code.

## Artifacts to Produce (All via FS)
- PLAN_T002_....md (this)
- Skeleton + incremental commits for the emitter script
- Enriched sidecar CSV/JSONL + summary JSON on at least one power window (12-13 minimum)
- 7-field report in reports/
- Updated T-002 task file + TEAM_STATUS.md
- (Optional) small analysis note in docs/ if numbers warrant
- Self-review appendix

## Open Questions at PLAN Time (None Blocking)
- Exact 7-field column order: will mirror the dominant pattern in catalogue/*.md (Objects/Invariant, Citations, Status, Proposed surface/test, Value, Drift, plus explicit hypothesis statement as 7th). Confirmed in report.
- Whether to also emit a compact previous_carrier_signature for direct transport measurement: yes, as part of augmentation (links consecutive transitions).

**Execution begins only after this PLAN is written and internal review confirms alignment with all contracts. All subsequent work will reference numbered steps above.**

*This PLAN was authored under full PGS-first, deterministic, state-separation discipline. No implementation logic present.*