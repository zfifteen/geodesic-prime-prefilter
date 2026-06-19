# Experiment Design: Weak L_FCL Demoted-Audit Extension

**Date:** 2026-06-19  
**Revision:** 1 (initial skeleton — ready for pilot & detail fill)  
**Hypothesis artifact:** `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html` + Lean `PGS/ChamberReset/DemotedZeroExcessSignature`  
**Status:** Draft skeleton — pre-specified structure; pilot data & exact metrics to be inserted after small-scale run  
**PGS frame:** objects → invariants → rule → resolved / falsified / unresolved

---

## Design Review Summary

### Revision 0 (this skeleton)

| Issue | Severity | Finding | Revision |
| --- | --- | --- | --- |
| **Demotion layer underspecified** | Major | Previous weak L_FCL sufficient-bound used implicit audit; explicit `DemotedZeroExcessSignature` from Lean L4 now available. | Introduce explicit demoted-audit lane and selector variant. |
| **Integration with Rule X replay (L5)** | Critical | L5 (`ruleXReplay`) still open `sorry`. Demoted audit should feed directly into replay certificate. | Make L5 closure a co-objective; pre-register demoted signature match in replay path. |
| **Scale & invariant preservation** | Major | June 15 work showed persistent left bias, d=4 dominance, linear B(I) at 10^7. Demoted audit must not break these. | Add invariant-preservation metrics to success criteria. |
| **Strong vs weak distinction** | Major | Strong early-forcing signals largely absent; weak sufficient-bound + demotion is the live lane. | Focus this experiment exclusively on strengthening the weak form. |

**Validity verdict (rev 1):** Skeleton is structurally sound. No critical defects in the pre-specification framework. Pilot run on small consecutive-gap sample required before full R2 execution.

---

## Hypothesis (Tiered)

### Parent framing (updated for demoted audit)

**Weak L_FCL:** On a sufficient bound *B = gap*, chamber excess geometry produces a unique reset *q* whose zero-excess audit signature can be *demoted* (explicit `DemotedZeroExcessSignature` after composite-witness filtering). The demoted signature is necessary and sufficient for unique closure under the weak form; it is not required to appear as a live selector branch.

**Strong form reminder (for contrast):** Early prefix forcing (*B < gap*) or non-demoted early prediction. Largely retired / under pressure from prior probes (L2 falsified, prefix forcing absent).

### Testable tiers (this experiment)

| Tier | Claim under test | Lane | What would falsify it |
| --- | --- | --- | --- |
| **Weak-L_FCL-D1** (demoted signature necessity) | Unique reset at *B = gap* requires the demoted zero-excess signature; without explicit demotion the sufficient-bound law collapses or produces non-unique survivors. | Demoted-F2 + V | `unique_reset_rate < 1.0` or `demoted_signature_match < threshold` on R2 when demotion layer is active vs control. |
| **Weak-L_FCL-D2** (demoted audit integration) | DemotedZeroExcessSignature composes cleanly with Rule X replay (L5 target); replay certificate preserves the demoted audit without introducing new mismatches. | Replay-Demoted + Lean V | L5 remains open after integration attempt, or replay produces `q_replay ≠ q_ref` on demoted path. |
| **Weak-L_FCL-D3** (invariant preservation) | Introduction of explicit demoted audit does not degrade known chamber invariants (left bias, d=4 dominance, linear B(I), GWR pruning advantage). | All lanes + invariant monitor | Statistically significant degradation in any pre-registered invariant on 10^6–10^7 surface. |

**L_FCL (forward closure law)** remains the target. This experiment supplies the first explicit demoted-audit empirical + Lean-backed test of the weak form.

---

## Objective

On the R2 sufficient-bound regime, decide:

1. Does explicit demoted audit improve or stabilize unique reset rate under *B = gap*?
2. Can the demoted signature be fed directly into an updated Rule X replay path (progress toward closing L5)?
3. Does the demoted layer preserve (or enhance) the chamber invariants established at 10^6–10^7 scale?
4. Is the demoted audit a net positive for audit precision without introducing forbidden dependencies or performance cost?

One sentence: **Does the explicit demoted-audit layer strengthen the weak L_FCL sufficient-bound law while remaining compatible with existing PGS machinery and invariants?**

---

## Scope

### In scope

- Consecutive prime gaps with `p ≥ 11`, focus on R2 (*B = gap*).
- Explicit `DemotedZeroExcessSignature` (Lean-proved) applied after composite-witness filtering.
- Integration test with Rule X replay certificate (target L5 closure).
- Invariant monitoring: left bias, d=4 dominance, linear B(I), GWR minimum-divisor pruning advantage.
- Lanes that use or withhold the demoted layer for controlled comparison.
- Small pilot (≤ 10k gaps) then full R2 up to 10^6 (or 10^7 if resources allow).

### Out of scope

- Re-testing strong/early-forcing claims (already under pressure).
- Full 10^18 ladder (separate existing plan).
- RH / zeta consequences.
- New composite-exclusion engines (reuse existing where possible).
- Performance benchmarking beyond audit-precision delta.

---

## Method

### Lanes (core comparison)

| Lane | Role | Uses Demoted Signature? | Tests Tier |
| --- | --- | --- | --- |
| **R** | Reference ground truth: `q_ref = min{n>p : τ(n)=2}` | N/A (audit only) | All |
| **Control-F2** | Weak sufficient-bound without explicit demotion (baseline from prior weak-lfcl probe) | No | D1 baseline |
| **Demoted-F2** | Weak sufficient-bound *with* explicit `DemotedZeroExcessSignature` after composite filtering | Yes (post-composite) | D1, D3 |
| **Replay-Demoted** | Demoted-F2 output fed into updated Rule X replay certificate | Yes | D2 |
| **V** | Post-hoc verification: demoted signature match + `q == q_ref` + invariant checks | Yes (verification) | All |

**Lane isolation:** Demoted layer must be applied only after composite-witness stage; never as live `if τ <= 2` branch.

### Demoted audit layer specification (to be implemented in selector)

```python
# After composite_witness filtering and unresolved_count == 0
if is_demoted_zero_excess(p, offset, prefix_state):
    status = RESOLVED_SURVIVOR_WITH_DEMOTED_AUDIT
```

`is_demoted_zero_excess` implements (or calls Lean theorem for) `DemotedZeroExcessSignature`.
Forbidden: any literal τ==2 / τ<=2 in the selection decision itself.

### Allowed vs forbidden use of demotion

| Use | Demoted-F2 / Replay-Demoted | Control-F2 |
| --- | --- | --- |
| `DemotedZeroExcessSignature` as post-filter audit | Allowed & required | Forbidden (control) |
| `DemotedZeroExcessSignature` as live selection branch | **Forbidden** | N/A |
| Feeding demoted signature into replay certificate | Allowed (D2 lane) | N/A |

### Invariant monitoring (pre-registered)

For every gap / bucket:
- Left-bias persistence
- d=4 dominance in chamber population
- Linearity / slope of B(I)
- GWR pruning advantage (divisor-count reduction %)

Compare Demoted-F2 vs Control-F2; flag any statistically significant degradation.

### Decision-offset & uniqueness metrics (extension of prior)

- `unique_reset_rate` under demoted vs control
- `demoted_signature_match_rate` (V lane)
- `replay_match_rate` (D2 lane)
- `decision_offset_eq_gap_rate` (should remain high)

### Regimes

| Regime | Prime surface | Bound `B` | Primary lanes |
| --- | --- | --- | --- |
| **R2-Demoted** | Consecutive gaps `11 ≤ p < 10^6` (pilot first ≤ 10k) | `gap` (sufficient) | Demoted-F2, Control-F2, Replay-Demoted |
| **R2-Invariant** | Same + 10^7 extension if pilot clean | `gap` | All + invariant monitor |

### Reproducibility

- Same generator freeze and wheel as prior weak-lfcl experiment.
- Lean theorems referenced via lake export or manual proof replay for V lane.
- Deterministic; no RNG.

### Commands (skeleton — update paths after implementation)

```bash
# Pilot run (small consecutive sample)
PYTHONPATH=src/python python3 \
  experiments/weak-lfcl-demoted-audit-2026-06/weak_lfcl_demoted_probe.py \
  --regime R2-pilot --output-dir experiments/weak-lfcl-demoted-audit-2026-06/output/pilot

# Full R2 with demoted layer
PYTHONPATH=src/python python3 \
  experiments/weak-lfcl-demoted-audit-2026-06/weak_lfcl_demoted_probe.py \
  --regime R2 --output-dir experiments/weak-lfcl-demoted-audit-2026-06/output/R2

# Invariant comparison script (to be added)
python3 experiments/weak-lfcl-demoted-audit-2026-06/invariant_monitor.py \
  --demoted-summary output/R2/summary.json \
  --control-summary ../weak-lfcl-sufficient-bound-2026-06/output/R2/summary.json
```

---

## Success / Falsification Criteria

### Harness & integration gate (must pass first)

| Check | Condition |
| --- | --- | --- |
| Demoted layer implementation | Clean AST (no forbidden τ<=2 branches); Lean theorem call or equivalent succeeds | 
| Control vs Demoted parity on non-demoted metrics | `unique_reset_rate` and `decision_offset_eq_gap_rate` within tolerance of prior weak probe |
| Replay integration | D2 lane produces `q_replay == q_ref` on pilot; L5 progress measurable |

### Tier D1 (demoted signature necessity)

| Outcome | Condition |
| --- | --- | --- |
| **Supported** | `unique_reset_rate` significantly higher or more stable with demoted layer vs control; `demoted_signature_match_rate` high | 
| **Falsified** | Demoted layer produces *lower* unique reset rate or introduces new non-unique survivors | 
| **Unresolved** | No statistically meaningful difference; demotion is neutral | 

### Tier D2 (demoted audit integration with replay)

| Outcome | Condition |
| --- | --- | --- |
| **Supported / L5 progress** | Demoted signature feeds cleanly into replay certificate; measurable reduction in open `sorry` surface or new proved lemmas | 
| **Falsified** | Integration causes replay mismatches or breaks existing Rule X guarantees | 

### Tier D3 (invariant preservation)

| Outcome | Condition |
| --- | --- | --- |
| **Supported** | No significant degradation in left bias, d=4 dominance, B(I) linearity, or GWR pruning % | 
| **Falsified** | Statistically significant degradation in any pre-registered invariant | 

### Parent weak L_FCL aggregation

| Verdict | Rule |
| --- | --- | --- |
| **Weak L_FCL strengthened** | D1 or D2 supported + D3 holds | 
| **Weak L_FCL neutral / needs refinement** | All tiers unresolved or mixed | 
| **Weak L_FCL challenged** | D1 or D3 falsified | 

---

## Expected Artifacts

```
experiments/weak-lfcl-demoted-audit-2026-06/
  experiment-design.md          # this file
  weak_lfcl_demoted_probe.py    # main selector + demoted layer
  invariant_monitor.py          # optional
  FINDINGS.md                   # post-run
  output/
    pilot/ R2/
      summary.json
      demoted_vs_control.csv
      invariant_report.json
  Lean/
    updated ChamberReset/WeakLFCL.lean  # L5 progress + demoted integration
```

---

## Failure Modes & Mitigations

| Failure mode | Mitigation |
| --- | --- | --- |
| Demoted signature implementation drift from Lean theorem | Reference Lean export or re-prove in Python mirror for V lane | 
| Pilot shows no signal | Extend to full R2 or adjust demotion threshold; document as neutral result | 
| Invariant degradation | Halt full run; investigate interaction with d=4 / B(I) modules first | 
| L5 integration breaks replay | Roll back to control replay; treat as separate Lean task | 
| Performance cost of demotion | Measure but do not gate success on speed (audit precision is primary) | 

---

## Implementation Roadmap

1. Implement `weak_lfcl_demoted_probe.py` with Control-F2 and Demoted-F2 lanes + explicit demoted layer.
2. Small pilot run (≤ 10k consecutive gaps) — validate harness, collect initial unique_reset and demoted_match rates.
3. Update Lean `PGS/ChamberReset` with demoted integration points for L5.
4. Full R2 run + invariant monitoring.
5. Produce `FINDINGS.md` with tier verdicts and invariant delta table.
6. Draft updates to `PROOF.md` and `chamber_tension_closure_hypothesis` HTML incorporating demoted-audit results.
7. (Stretch) Close L5 `sorry` using the new demoted replay path.

**Successor work:** Integration of strengthened weak L_FCL into broader PGS next-prime bound theorems, GWR/DNI pruning, and 10^7+ empirics.

---

## Rollback

```bash
rm -rf experiments/weak-lfcl-demoted-audit-2026-06/output
```

No production code changes required for skeleton phase.

---

## References

| Artifact | Use |
| --- | --- | --- |
| `experiments/weak-lfcl-sufficient-bound-2026-06/` | Baseline weak L_FCL sufficient-bound results | 
| `experiments/prefix-state-lfcl-decisive-2026-06/FINDINGS.md` | L2 falsification context | 
| `experiments/chamber-tension-closure-falsification-2026-06/` | Tier structure & pre-spec style | 
| Lean `PGS/ChamberReset/DemotedZeroExcessSignature` + L4 proved modules | Demoted signature definition & audit | 
| `PROOF.md` (to be updated) | GWR, NLSC, chamber invariants, d=4 bounds | 
| June 15 commits (d=4 fractional bound, chamber budget 1e7) | Invariant baselines to preserve | 
| `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html` | Parent H_CTC weak/strong split | 

---

**Next action after pilot:** Fill exact pilot metrics, adjust thresholds if needed, then execute full R2. Ready for implementation.