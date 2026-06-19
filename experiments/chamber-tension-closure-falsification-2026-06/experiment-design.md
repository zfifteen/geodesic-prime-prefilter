# Experiment Design: Falsifying H<sub>CTC</sub> via Forward Chamber-Closure Probe

**Date:** 2026-06-19  
**Revision:** 4 (critical-defect loop — closed)
**Hypothesis artifact:** `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html`  
**Status:** Pre-specified design — implementation not yet in this folder  
**PGS frame:** objects → invariants → rule → resolved / falsified / unresolved

---

## Design Review Summary

### Revision 2 (first pass)

| Issue | Severity | Finding | Revision |
| --- | --- | --- | --- |
| **F2a law invalid** | Critical | Retired F2a picks interior semiprimes (`τ=4`) before `q`. Example: `p=73` → `77` not `79`. | Removed as primary law. |
| **Construct conflation** | Critical | F1 tests implementation equivalence, not H<sub>CTC</sub> selector independence. | Split tiers **A / B / C**. |
| **Early-closure ill-posed** | Major | Rule X certificate never stabilizes at `B < gap` on **5 128** gaps tested. | **decision_offset** metric. |

### Revision 3 (second pass)

| Issue | Severity | Finding | Revision |
| --- | --- | --- | --- |
| **F0 negative control broken** | Critical | Retired F2a as F0 matches `q_ref` on **≈48.5%** of gaps (`8 729 / 17 979`, `p < 200 000`) — often when the first wheel-open offset after lock **is** `q`. Cannot expect `match_f0 = 0%`. | Replace F0 with **`q_f0 = p + lock_carrier_offset`** (GWR-offset confound; **0%** match on same surface). |
| **Tier B is syntactic** | Major | F2-RX is logically equivalent to F1 (`not (τ>2)` ⟺ `τ≤2` for integer τ). Pilot: **0 mismatches** vs F1 on `p < 20 000`. Tier B pass is **pre-registered expected**; it does not substantively test chamber-tension forcing. | Reframe tier B as **notational independence check**, not L<sub>FCL</sub> evidence. |
| **Tier C estimand wrong** | Critical | Existing composite-exclusion probe on `11..10 000`, `B=64`: `unique_survivor_count=1225` but **`unique_resolved_survivor_count=0`** and **`no_unique_boundary_count=1225`** (`composite_exclusion_boundary_probe.md`). Survivor collapse ≠ resolved closure. | Tier C primary estimand → **`unique_resolved_survivor_count`**; pre-register **unresolved** on default rule set. |
| **Decision-offset cost** | Minor | Full scan `B=1..gap` per gap is **O(Σ gap) ~ O(n log n)**; costly at `10^6`. | Sample **decision_offset** on fixed gap buckets + all gaps with `gap > 64`. |
| **F2-EXCL R2 wrapper unspecified** | Minor | Per-gap `candidate_bound=gap` wrapper is not implemented in the existing probe CLI. | Stage C on fixed probe first; per-gap wrapper is **Phase C2** optional. |

### Revision 4 (critical-defect loop)

| Issue | Severity | Finding | Revision |
| --- | --- | --- | --- |
| **Forbidden-dependency field hallucinated** | Critical | `forbidden_dependency_status` is **not** in probe summary JSON. AST gate on the whole probe file reports **3 violations** (`sympy` / `primerange` in `label_offsets` — audit-only). Expecting `violations = 0` on the wrapper would false-fail. | Tier C gate runs on **`eliminate_candidates` + `classify_candidate` AST slice only**; label/audit functions excluded. Wrapper sympy documented as audit-only. |
| **F0 coupled to resolution semantics** | Critical | `lock_carrier_offset` is defined only after first `RESOLVED_SURVIVOR` (Rule X resolution path). F0 was not a clean negative control independent of selection machinery. | F0 now uses **`gwr_offset`** = first offset achieving running minimum `τ>2` in prefix (pilot **0%** match, `p < 200k`). |
| **Tier C ≠ L<sub>FCL</sub> State(p)** | Critical | Tier C uses **bounded composite witnesses**, not full divisor-count chamber state (`B(I)`, Rule X reset). It tests an **adjacent** exclusion path, not the hypothesis artifact's `State(p, prefix)`. | Tier C relabeled **adjacent closure path**; primary Rule X substantive target stays tiers A/B + prefix-forcing metrics. |
| **Per-gap / summary integration** | Critical | Per-gap table listed `f2excl_*` fields, but C1-EXCL is **anchor-level** output from a separate script — not mergeable per gap without a join key. | Split artifacts: `output/R2/summary.json` (gap probe) and `output/C1-EXCL/composite_exclusion_boundary_probe_summary.json`. `summarize_probe.py` ingests both. |
| **Objective wording stale** | Major | Objective still said “unique survivor” not “resolved-unique”. | Fixed in objective list. |

**Validity verdict (rev 4):** No remaining **critical** defects under the stated scope. Substantive H<sub>CTC</sub> closure remains **pre-registered unresolved** (tier C baseline `unique_resolved_survivor_count = 0`; prefix forcing at `B < gap` always `None` on pilot).

---

## Hypothesis (Tiered)

### Parent framing (from hypothesis artifact)

**H<sub>CTC</sub>:** Chamber excess geometry forces a unique reset point `q`. Divisor
count `τ=2` is the zero-excess audit signature, not necessarily the inference
selector.

### Testable tiers (this experiment)

| Tier | Claim under test | Lane | What would falsify it |
| --- | --- | --- | --- |
| **H<sub>CTC</sub>-A** (audit separation) | Production chamber-reset Rule X returns the proved next prime; `τ(q)=2` is always true post-hoc. | F1 + V | `q_f1 ≠ q_ref` on R2, or `τ(q_f1) ≠ 2` |
| **H<sub>CTC</sub>-B** (notational independence) | Rule X can be source-coded with **no literal** `τ==2` / `τ≤2` selection branches; equivalent surrogate uses only `τ>2` composite witnesses. **Expected to pass** (syntactic refactor). | F2-RX + V | `q_f2rx ≠ q_ref`, forbidden-branch guard trips, or F2-RX ≠ F1 |
| **H<sub>CTC</sub>-C** (adjacent exclusion closure) | Bounded-witness composite-exclusion yields **`unique_resolved_survivor`** matching the post-hoc label — **not** the Rule X `State(p, prefix)` from L<sub>FCL</sub>. | F2-EXCL + V | `true_boundary_rejected > 0`; default rule set **0 / 1225** resolved-unique (reproduced 2026-06-19) |

**L<sub>FCL</sub> (forward closure law)** remains the unresolved proof target. This
experiment supplies finite-surface evidence for which tier survives, not a theorem.

---

## Objective

On pinned regimes, decide:

1. Does production Rule X match the proved next-prime rule (tier A)?
2. Does an equivalent Rule X isomorph select `q` without `τ==2` / `τ≤2` branches (tier B)?
3. Does composite-exclusion produce any **resolved-unique** survivor at the audited label (tier C — adjacent path)?
4. Does the negative control F0 fail on every gap (harness sanity)?
5. Does tier C show any **resolved-unique** exclusion closure on the stated rule set (likely unresolved)?

One sentence: **which chamber-tension closure tier is supported, falsified, or
unresolved on the stated surface?**

---

## Scope

### In scope

- Consecutive prime gaps with `p ≥ 11`.
- Exact divisor-count field `τ(n)` on declared bound `B`.
- GWR carrier, NLSC / lower-divisor threat, wheel-open residues mod 30.
- Lanes F0, F1, F2-RX, F2-EXCL, R, V.
- Regimes R1 (production bound), R2 (sufficient bound), optional R3 (high-scale).

### Out of scope

- RH / zeta / PNT consequences.
- `nextprime` / `isprime` inside forward selectors.
- Theorem promotion from finite scans.
- Integer-start chambers (separate existing probe).
- Reinventing the full composite-exclusion rule engine (wrap existing script).

---

## Method

### Lanes

| Lane | Role | `τ=2` in selector? | Tests tier |
| --- | --- | --- | --- |
| **R** | Reference ground truth: `q_ref = min{n>p : τ(n)=2}` | N/A (audit label only) | All |
| **F0** | GWR-offset confound: `q_f0 = p + gwr_offset` (running-min `τ`, no resolution semantics) | No | Harness sanity |
| **F1** | Production `resolve_q` / `pgs_chamber_reset_state_certificate` | Yes (`τ≤2` resolved branch) | A |
| **F2-RX** | Rule X isomorph (spec below) | **Forbidden** `τ==2`, `τ≤2` | B |
| **F2-EXCL** | Wrapper around `composite_exclusion_boundary_probe.py` | Forbidden in elimination path | C |
| **V** | Post-hoc: `τ(q_pred)==2`, `q_pred==q_ref` | Yes (verification only) | All |

**Lane isolation:** F0, F1, F2-RX, F2-EXCL must not read `q_ref` during selection.
Only R computes `q_ref`. V runs after selection.

### Allowed vs forbidden divisor-count use (F2 lanes)

| Use | F2-RX / F2-EXCL |
| --- | --- |
| `τ(n) > 2` as composite witness | Allowed |
| GWR via running minimum `τ` | Allowed |
| `unresolved_count` driven by non-composite offsets (`τ ≤ 2` at any offset) | Allowed in F2-RX (matches production semantics) |
| `τ(n) == 2` or `τ(n) ≤ 2` as **endpoint selection** branch | **Forbidden** |
| `d(n) = 2` / prime-marker identity in F2-EXCL elimination | **Forbidden** (per composite-exclusion contract) |

### F0 — Negative control (GWR-offset confound)

Deliberately wrong law: predict the endpoint equals the **running GWR carrier offset**
(leftmost minimum-`τ` position in the prefix), not the chamber-reset survivor.

```text
gwr_offset = first offset k in 1..B where τ(p+k) achieves the running minimum among τ>2 values seen
q_f0 = p + gwr_offset
```

Computed from prefix `τ` only. Does **not** use wheel-open mask, lock carrier,
threat, or resolved-survivor semantics. Not imported from F1.

Pilot `p < 200 000`, `B = gap`: **`match_f0 = 0%`** (17 979 mismatches).

**Pre-registered expectation:** `match_f0 = 0%` on R2. Any match → halt (harness bug).

**Retired controls (do not use):**

- **F2a** (first wheel-open after lock): ≈48.5% accidental match.
- **`p + lock_carrier_offset`**: also 0% on pilot, but couples to resolution semantics — replaced by `gwr_offset`.

### F1 — Production Rule X (tier A)

Call `resolve_q(p, B)` from `simple_pgs_generator.py`. No modification.

### F2-RX — Rule X isomorph without `τ==2` selection (tier B)

Reimplement `pgs_chamber_reset_state_certificate` in the experiment script with
identical state machine, but replace resolved-survivor classification:

**Production (forbidden in F2-RX source text):**

```python
elif divisor_count <= 2:  # literal τ≤2 selection branch
    status = RESOLVED_SURVIVOR
```

**F2-RX surrogate (required):**

```python
elif not composite_witness(divisor_count) and unresolved_count == 0:
    status = RESOLVED_SURVIVOR

def composite_witness(tau: int) -> bool:
    return tau > 2
```

Forbidden-branch audit uses **AST comparison** (not substring scan): reject
`ast.Compare` nodes testing `τ == 2`, `τ <= 2`, `τ < 3`, etc., in selection code;
allow `τ > 2` composite-witness checks only. The `unresolved_count` increment uses
`else:` on the `composite_witness` branch — semantically `τ≤2`, syntactically allowed.

**Pre-registered expectation:** `match_f2rx = match_f1 = 100%` on R2. Tier B passing
confirms notational refactor only; it is **not** evidence that chamber tension forces
`q` without the divisor-count field.

All other production fields preserved: wheel-open mask, GWR carrier update, lock
carrier, threat ceiling, post-threat rejection, first resolved survivor output.

### F2-EXCL — Composite exclusion (tier C)

Invoke the existing offline probe:

`research/01-generator/scripts/prime_inference_generator/composite_exclusion_boundary_probe.py`

Parameters for this experiment:

| Parameter | Value |
| --- | --- |
| `--start-anchor` | `11` |
| `--max-anchor` | `10_000` (Phase C1; matches documented probe surface) |
| `--candidate-bound` | `64` (documented default) |

Record per anchor from probe summary:

- `unique_survivor_count` / `unique_resolved_survivor_count` (**primary tier C estimand**)
- `no_unique_boundary_count`
- `true_boundary_rejected_count`
- `unique_survivor_match_rate` (secondary — label match when one survivor remains)

**Forbidden-dependency audit (tier C):** run `forbidden_dependency_gate.py` AST scan on
the bodies of `classify_candidate` and `eliminate_candidates` only. The probe wrapper
may import `sympy.primerange` for `label_offsets` (audit-only); **3 violations on the
full probe file are expected and allowed**.

Classical label attachment happens **after** elimination (probe contract: `eliminate_candidates` → `attach_label`).

**Phase C1:** invoke existing probe unchanged (reproduce documented surface).

**Phase C2 (optional):** per-gap `candidate_bound = gap` wrapper — requires new
script; not required for first falsification signal.

**Pre-registered baseline** (reproduced 2026-06-19, `11..10 000`, `B=64`):
`unique_resolved_survivor_count = 0`, `no_unique_boundary_count = 1225`,
`true_boundary_rejected_count = 0`, `row_count = 1225`. Tier C on default rules is
expected **unresolved**, not supported.

**Prefix forcing (Rule X substantive read):** at `B = gap - 1`, pilot shows
`pgs_chamber_reset_state_certificate` returns `None` on **5 128 / 5 128** gaps
(`p < 50 000`, `gap ≥ 2`). Chamber-reset does not resolve one step early.

### Decision-offset analysis (replaces early_closure)

For each gap, increment `B = 1, 2, …, gap` and record:

| Field | Definition |
| --- | --- |
| `decision_offset_f1` | Minimum `B` where F1 certificate `q == q_ref` |
| `decision_offset_f2rx` | Same for F2-RX |

**Pre-registered expectation (pilot):** `decision_offset == gap` for essentially all
sampled rows. A value `< gap` would be strong evidence for forward forcing before arrival.

**Sampling (R2 at `10^6`):** compute `decision_offset` for all gaps with `gap > 64`,
plus a deterministic 1-in-64 sample of remaining gaps (`p mod 64 == 0`). Report
`decision_offset_eq_gap_rate` on the sample; do not require full enumeration at `10^6`.

### Per-gap row fields

| Field | Meaning |
| --- | --- |
| `p`, `q_ref`, `gap` | Lane R |
| `w_offset`, `w_tau`, `B_I` | Full-gap chamber geometry |
| `q_f0`, `q_f1`, `q_f2rx` | Lane outputs |
| `match_f0`, `match_f1`, `match_f2rx` | Equality with `q_ref` |
| `audit_tau2_*` | Lane V |
| `decision_offset_f1`, `decision_offset_f2rx` | Stabilization index (sampled) |
| `prefix_cert_none_at_gap_minus_1` | Rule X returns `None` at `B = gap - 1` |
| `gwr_offset`, `lock_carrier_offset`, `lower_d_threat_offset` | Diagnostic |

---

## Regimes

| Regime | Prime surface | Bound `B` | Primary tiers |
| --- | --- | --- | --- |
| **R1** | All consecutive gaps, `11 ≤ p < 10^6` | `128` fixed | A, B, F0; bound-miss diagnostics |
| **R2** | Same | `gap` (exact sufficient bound per pair) | **Primary decision regime** for A, B |
| **R3** | Decade ladder `10^8..10^18`, 256 primes/decade | `1024` | A only (optional parity) |
| **C1-EXCL** | Input primes `11..10_000` (documented probe surface) | `64` fixed | C (Phase C1) |

---

## Reproducibility

| Pin | Value |
| --- | --- |
| Python | `python3` |
| `PYTHONPATH` | `src/python` for F1 |
| Generator freeze | `pgs_inference_generator_v1_1_pgs_only` |
| Chamber rule | `pgs_chamber_reset_v1` |
| Wheel | `WHEEL_OPEN_RESIDUES_MOD30` |
| Excess | `E(n) = (τ(n)/2 - 1) * ln n` |
| RNG | None (deterministic) |
| τ table | Divisor sieve (same pattern as `pgs_chamber_budget_analyzer.py`) |

### Commands (after implementation)

```bash
# Core probe: F0, F1, F2-RX, decision offsets
PYTHONPATH=src/python python3 \
  experiments/chamber-tension-closure-falsification-2026-06/forward_chamber_closure_probe.py \
  --regime R2 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/R2

# Production-bound stress
PYTHONPATH=src/python python3 \
  experiments/chamber-tension-closure-falsification-2026-06/forward_chamber_closure_probe.py \
  --regime R1 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/R1

# Tier C Phase C1: composite exclusion (documented surface)
python3 research/01-generator/scripts/prime_inference_generator/composite_exclusion_boundary_probe.py \
  --start-anchor 11 --max-anchor 10000 --candidate-bound 64 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/C1-EXCL

python3 experiments/chamber-tension-closure-falsification-2026-06/summarize_probe.py \
  --gap-summary experiments/chamber-tension-closure-falsification-2026-06/output/R2/summary.json \
  --excl-summary experiments/chamber-tension-closure-falsification-2026-06/output/C1-EXCL/composite_exclusion_boundary_probe_summary.json
```

---

## Success / Falsification Criteria

### Harness gate (must pass before tier claims)

| Check | Condition |
| --- | --- |
| F0 negative control | `match_f0 = 0%` on R2 (GWR-offset confound; pilot verified) |
| F1 blockers | `match_f1 = 100%` on R2; else fix harness |
| F2-RX ≡ F1 | `match_f2rx = match_f1` on R2; else implementation drift |

### Tier A (audit separation)

| Outcome | Condition |
| --- | --- |
| **Supported on regime** | `match_f1 = 100%` and `audit_tau2_f1 = 100%` |
| **Falsified** | Any `q_f1 ≠ q_ref` on R2 |

### Tier B (notational independence)

| Outcome | Condition |
| --- | --- |
| **Expected pass** | `match_f2rx = 100%` on R2, F2-RX ≡ F1, forbidden-token scan clean, `audit_tau2_f2rx = 100%` |
| **Falsified** | Any `q_f2rx ≠ q_ref` or F2-RX ≠ F1 on R2 |
| **Interpretation** | Pass confirms refactor only. **Does not support L<sub>FCL</sub> or substantive H<sub>CTC</sub>.** |

### Tier C (exclusion closure)

| Outcome | Condition |
| --- | --- |
| **Supported (staged)** | `unique_resolved_survivor_count > 0` on C1-EXCL with `true_boundary_rejected_count = 0` and label match on those rows |
| **Falsified** | `true_boundary_rejected_count > 0` |
| **Unresolved (pre-registered default)** | `unique_resolved_survivor_count = 0` with `no_unique_boundary_count` dominating — current exclusion rule set does not close chamber (documented: **0 / 1225** on `11..10 000`) |
| **Secondary** | `unique_survivor_match_rate ≈ 0.81` with survivors but unresolved alternatives — informative, not closure |

### Parent H<sub>CTC</sub> aggregation (FINDINGS.md)

| Verdict | Rule |
| --- | --- |
| **Tier A supported** | Chamber-reset implementation matches proved next prime; audit signature holds. |
| **Tier B expected** | Notational independence only (pre-registered pass). |
| **Tier C supported** | `unique_resolved_survivor_count > 0` on C1-EXCL — first evidence for **adjacent** exclusion closure (not Rule X `State`). |
| **H<sub>CTC</sub> substantively falsified** | Tier C rejects true boundary (`true_boundary_rejected_count > 0`). Tier B failure = implementation bug. |
| **Unresolved (default expectation)** | Tier C baseline `0 / 1225` resolved-unique; prefix forcing at `B < gap` absent on pilot. **Parent H<sub>CTC</sub> substantive claim remains open.** |

### Experiment power (honest scope)

This probe is **confirmatory** on tiers A/B (Rule X ≡ `min{τ=2}`), **sanity** on F0,
and **baseline reproduction** on tier C. It does **not** include a forward law that is
both (i) independent of Rule X equivalence and (ii) derived from full chamber-tension
`State(p, prefix)`. Developing such a law is out of scope until specified elsewhere.

### Summary counters (`summary.json`)

```text
gaps_total
f0_match_rate          # expect 0
f1_match_rate          # expect 1 on R2
f2rx_match_rate        # primary H_CTC-B estimand
decision_offset_eq_gap_rate
f2excl_unique_survivor_count
f2excl_unique_resolved_survivor_count   # primary tier C
f2excl_no_unique_boundary_count
f2excl_label_match_rate                 # secondary
true_boundary_rejected_count
excl_elimination_forbidden_violations  # expect 0 on classify+eliminate slice only
prefix_none_at_gap_minus_1_rate       # expect 1.0 on sample
first_mismatch_row
```

---

## Expected Artifacts

```
experiments/chamber-tension-closure-falsification-2026-06/
  experiment-design.md
  design-review-rev2.md          # optional extract; review is §Design Review above
  forward_chamber_closure_probe.py
  summarize_probe.py
  test_forward_closure.py
  FINDINGS.md
  output/
    R1/ R2/ R3/ C1-EXCL/
      summary.json
      mismatches.csv
      gaps.csv.gz              # optional compressed per-gap rows
```

---

## Failure Modes & Mitigations

| Failure mode | Mitigation |
| --- | --- |
| F0 accidentally matches | Halt — harness bug (pilot: 0 matches on `p < 200k`) |
| Tier B pass misread as H<sub>CTC</sub> proof | FINDINGS labels tier B as notational only |
| Tier C survivor=1 misread as closure | Report `unique_resolved_survivor_count` prominently |
| F2-RX drifts from production | Diff test on small gap table; must match F1 on R2 |
| Literal `τ==2` sneaks into F2-RX | Static source scan + code review checklist |
| Tier C scope explosion | Stage on `p < 10^4` before `10^6` |
| Confusing tier A pass with H<sub>CTC</sub>-C pass | FINDINGS.md uses tier labels explicitly |
| R1 bound miss | Report separately; do not use R1 for tier B/C decisions |
| sympy dependency in F2-EXCL | Already in probe; audit labels only |

---

## Implementation Roadmap

1. **`forward_chamber_closure_probe.py`** — sieve, R, F0, F1 import, F2-RX, decision offsets.
2. **`test_forward_closure.py`** — F0 (`gwr_offset`) fails on `p=73`; F2-RX ≡ F1; AST forbidden-branch scan; tier C elimination-slice gate clean.
3. **Run R2** — primary tier A/B decision.
4. **Run R1** — bound-miss profile.
5. **`summarize_probe.py` + `FINDINGS.md`** — tier-separated conclusions.
6. **Run C1-EXCL** — reproduce composite-exclusion baseline; expect `unique_resolved_survivor_count=0`.
7. **Optional R3** — F1 only, decade parity.
8. **Optional C2** — per-gap bound wrapper if tier C needs extension.

**Successor experiment (L<sub>FCL</sub> decisive probe):**
`experiments/prefix-state-lfcl-decisive-2026-06/experiment-design.md` — prefix-state
forced-closure laws L0–L4 with semantic-independence audit.

---

## Rollback

```bash
rm -rf experiments/chamber-tension-closure-falsification-2026-06/output
```

No production code changes required.

---

## References

| Artifact | Use |
| --- | --- |
| `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html` | Parent hypothesis |
| `PROOF.md` | `q_ref` definition; GWR; NLSC |
| `src/python/z_band_prime_predictor/simple_pgs_generator.py` | F1; F2-RX reference |
| `research/01-generator/docs/composite_exclusion_generator_path.md` | Tier C contract |
| `research/01-generator/docs/composite_exclusion_boundary_probe.md` | Tier C baseline (`0 / 1225` resolved-unique) |
| `research/01-generator/scripts/.../composite_exclusion_boundary_probe.py` | F2-EXCL engine |
| `research/01-generator/scripts/.../forbidden_dependency_gate.py` | Tier C elimination-slice audit |
| `experiments/gwr_min_tau_five_absence/FINDINGS.md` | FINDINGS format |