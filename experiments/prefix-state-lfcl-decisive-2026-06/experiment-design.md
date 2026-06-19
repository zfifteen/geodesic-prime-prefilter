# Experiment Design: Falsifying H<sub>CTC</sub> via Prefix-State Forced-Closure Laws (L<sub>FCL</sub>)

**Date:** 2026-06-19  
**Revision:** 1  
**Parent hypothesis:** `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html`  
**Prior probe:** `experiments/chamber-tension-closure-falsification-2026-06/` (rev 4 — baseline only)  
**Status:** Implemented and executed — see `FINDINGS.md`  
**PGS frame:** objects → invariants → rule → resolved / falsified / unresolved

---

## Hypothesis

**Parent H<sub>CTC</sub> (Chamber-Tension Closure).**  
Source: `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html`

> The ordered excess field inside a prime-gap chamber carries enough deterministic
> constraint (GWR landmark, NLSC ceiling, excess budget, reset geometry) that the
> successor prime `q` is the unique chamber-reset point. Divisor count `τ=2` is the
> zero-excess signature of that reset, usable for verification; it need not be the
> inference mechanism that determines `q` from `p`.

**Unresolved proof target L<sub>FCL</sub> (Forward Chamber Closure).**  
A deterministic functional `Closure(p, State(p, prefix))` must:

1. Select `q` without `τ(n)=2` or `τ(n)≤2` as an endpoint-selection rule.
2. Equal `q_ref = min{n>p : τ(n)=2}` on every input in the stated class.
3. Use `τ(q)=2` only in post-hoc audit lane **V**.

**What the prior probe established (measured, not theorem):**

| Signal | R2 surface (`11 ≤ p < 10^6`) |
| --- | --- |
| Rule X ≡ `min{τ=2}` | 78 493 / 78 493 |
| F2-RX notational isomorph ≡ Rule X | 78 493 / 78 493 (syntactic only) |
| GWR-offset confound F0 | 0 / 78 493 |
| Prefix `B = gap − 1` resolves | 0 / 78 493 |
| `decision_offset == gap` (sampled) | 158 / 158 |
| Tier C `unique_resolved_survivor_count` | 0 / 1225 (`11..10_000`, `B=64`) |

The prior probe did **not** install independent `Closure` laws. This experiment does.

---

## Objective

One sentence: **On pinned consecutive-gap regimes, does any pre-registered geometry-only
`Closure` law declare a forced endpoint before the full gap is traversed, and if so does
that endpoint equal the proved next prime — or does any forced endpoint mismatch falsify
H<sub>CTC</sub> for that law?**

---

## Scope

### In scope

- Consecutive gaps with `p ≥ 11`.
- Prefix traversal `B = 1, 2, …, gap − 1` (and `gap` for audit only).
- PGS chamber state fields derivable from prefix: GWR carrier, lock carrier, NLSC
  composite ceiling, lower-divisor threat, wheel-open mask, partial excess budget.
- Pre-registered closure laws **L1–L4** plus harness control **L0**.
- Semantic-independence audit **SA** on closure-law source.
- Per-prefix admissible-set cardinality **D1** (uniqueness-before-arrival).
- Regime **R2** primary (`B` bound = `gap`); regime **R1** optional parity (`B = 128`).

### Out of scope

- Theorem promotion from finite scans.
- Rule X / F1 / F2-RX re-audit (prior experiment owns that).
- `nextprime`, `isprime`, Miller-Rabin, sieves, `gcd`, divisibility selectors inside
  closure laws.
- RH / zeta / PNT consequences.
- Tier C full rule-stack extension (deferred to Phase 2 optional appendix).

---

## Method

### Lanes

| Lane | Role | Reads `q_ref` during selection? |
| --- | --- | --- |
| **R** | Reference: `q_ref = min{n>p : τ(n)=2}` from τ table | N/A (ground truth) |
| **L0–L4** | Tested forward closure laws | **Forbidden** |
| **V** | Post-hoc: `τ(r)=2`, `r == q_ref` | After selection only |
| **D1** | Uniqueness counter on admissible sets | No `q_ref` in set definition |

**Lane isolation:** Laws L0–L4 and D1 must not import `q_ref`, `gap`, or any
post-hoc label. Only lane R computes `q_ref`. Lane V runs after each law emission.

### Prefix state functional

For known prime `p`, prefix bound `B ≥ 1`, and τ table on `[p+1, p+B]`:

```text
State(p, B) = (
  wheel_open_offsets(B)     # (p+k) mod 30 ∈ WHEEL_OPEN_RESIDUES_MOD30
  gwr_offset, gwr_tau       # leftmost running minimum τ among τ>2 in 1..B
  lock_carrier_offset, lock_carrier_d   # GWR lock after first resolved-survivor event in Rule X semantics — NOT used for selection; computed in parallel track for geometry only from τ>2 + NLSC composite fields
  threat_offset             # first k > lock_carrier with τ>2 and τ < lock_carrier_d
  nlsc_ok(k) for each wheel-open k ≤ B   # ∀ composite m ∈ (gwr_offset, k): τ(m) ≥ gwr_tau
  partial_budget(B)         # Σ_{n=p+1}^{p+B} E(n), E(n) = (τ(n)/2 − 1) ln n
  composite_rejected(k)     # τ(p+k) > 2
)
```

**Critical implementation note:** `lock_carrier` and `threat_offset` for closure laws
are computed from **composite-witness τ>2 fields only**. Positions with `τ ≤ 2` are
recorded as **unresolved** in the parallel geometry track. They must **not** trigger
resolved-survivor classification in L1–L4.

### Allowed vs forbidden divisor-count use

| Use | L1–L4 closure laws |
| --- | --- |
| `τ(n) > 2` composite rejection | Allowed |
| Running minimum `τ` among `τ > 2` (GWR composite carrier) | Allowed |
| NLSC on composite positions (`τ > 2`) | Allowed |
| `τ(n) == 2`, `τ(n) ≤ 2` as endpoint branch | **Forbidden** |
| `unresolved_count == 0` as endpoint branch | **Forbidden** (F2-RX equivalence) |
| Count of wheel-open offsets with `τ ≤ 2` | **Forbidden** |
| `not composite_witness(τ)` as sole survivor pick | **Forbidden** when it selects endpoint |

### Pre-registered closure laws

Each law scans `B = 1..gap−1` in order. The **first** prefix where the law declares
forced closure wins. Record `(law_id, p, B_declare, r_declare)`.

| ID | Name | Forced-closure predicate at prefix `B` | Emitted `r` |
| --- | --- | --- | --- |
| **L0** | GWR-offset harness (negative control) | `gwr_offset` is defined | `p + gwr_offset` |
| **L1** | Threat-ceiling bind | `threat_offset` is defined and `threat_offset ≤ B` | `p + threat_offset` |
| **L2** | Unique NLSC-admissible wheel-open | `\|A(B)\| = 1` where `A(B) = { wheel-open k ≤ B : nlsc_ok(k) ∧ composite_rejected(k) }` | `p + sole(k)` |
| **L3** | Threat-gated unique admissible | `threat_offset = T` defined and `A(B) ∩ {k ≥ T} ` has exactly one element | `p + sole(k)` |
| **L4** | Budget-saturation bind | `partial_budget(B) ≥ gwr_tau · ln(p + gwr_offset)` and `threat_offset` defined | `p + threat_offset` |

**L0 expectation (prior pilot):** `match_rate = 0%` on R2. Any match → halt (harness bug).

**L1–L4 expectations (pre-registered, not verdicts):**

- Prior probe suggests **no early Rule-X-style closure** before `gap`. These laws are
  independent attempts; any may fire early, never fire, or fire with mismatch.
- A law that **never fires** on the full R2 surface is **falsified as a forward
  predictor** on that surface (not a global H<sub>CTC</sub> theorem refutation).
- A law that fires with any `r ≠ q_ref` **falsifies H<sub>CTC</sub> for that law** on
  that gap.

### D1 — Uniqueness-before-arrival (no selection)

At each prefix `B < gap`, compute:

```text
A(B)  = { wheel-open k ≤ B : nlsc_ok(k) ∧ composite_rejected(k) }
U(B)  = |A(B)|
```

Record:

- `max_U_before_gap` = max `U(B)` over `B ∈ [1, gap−1]`
- `first_B_with_U_eq_1` (if any)
- `first_B_with_U_gt_1` (if any)

**Interpretation:**

- `U(B) > 1` at some `B < gap` → chamber geometry under the NLSC-composite admissible
  definition does **not** uniquely determine an endpoint at that prefix (informative,
  not alone a falsification).
- Combined with a law that declares unique closure at the same `B` while `U(B) > 1` →
  implementation bug.

### Semantic-independence audit (SA)

**Static (pre-run):**

- AST scan on `closure_laws.py`: forbid `Compare` nodes against constant `2` with
  `Eq`, `NotEq`, `LtE`, `Lt`, `GtE` on τ selection paths (extend
  `audit_utils.forbidden_tau_selection_violations`).
- Forbid identifier tokens `unresolved_count == 0` in endpoint-emission branches.

**Dynamic (per law invocation):**

- Assert closure emission path never reads `τ(p+k) ≤ 2` for endpoint decision.
- Log `semantic_tau_le_2_branch_taken_count`; must be **0**.

### Regimes

| Regime | Prime surface | Prefix scan | Primary laws |
| --- | --- | --- | --- |
| **R2** | Consecutive gaps, `11 ≤ p < 10^6` | Full `B = 1..gap−1` when `gap ≤ 256`; else deterministic stride (see below) | **Primary** |
| **R1** | Same | Prefix scan to `min(gap, 128)` | Optional parity |

**R2 prefix stride (cost control):**

- If `gap ≤ 256`: evaluate every `B`.
- If `gap > 256`: evaluate every `B` where `B ≡ 0 (mod 4)` plus all `B ∈ {1, gap−1}`.
- **Exception:** if any strided evaluation returns `r_declare ≠ q_ref`, immediately
  re-run full `B = 1..gap−1` on that gap to confirm mismatch (no stride on falsification
  candidates).

Estimated R2 cost: `O(Σ min(gap, gap/4)) ≈ O(n log n)` — comparable to prior
`decision_offset` sampling, acceptable for `p < 10^6`.

### Per-gap output fields

| Field | Meaning |
| --- | --- |
| `p`, `q_ref`, `gap` | Lane R |
| `law_id`, `B_declare`, `r_declare` | First forced closure per law (or null) |
| `early_fire` | `B_declare < gap` |
| `match_ref` | `r_declare == q_ref` when `early_fire` |
| `mismatch` | `r_declare ≠ q_ref` when law fired |
| `max_U_before_gap` | D1 |
| `first_B_U_eq_1`, `first_B_U_gt_1` | D1 diagnostics |
| `gwr_offset`, `threat_offset` | Geometry |

---

## Reproducibility

| Pin | Value |
| --- | --- |
| Python | `python3` |
| `PYTHONPATH` | `src/python` for shared τ / wheel helpers |
| Wheel | `WHEEL_OPEN_RESIDUES_MOD30` from `simple_pgs_generator.py` |
| Excess | `E(n) = (τ(n)/2 − 1) ln n` |
| τ table | Divisor sieve (same as prior probe) |
| RNG | None (deterministic) |
| MIN_PRIME | `11` |
| R2 limit | `p < 1_000_000` |

### Commands (after implementation)

```bash
PYTHONPATH=src/python python3 -m pytest \
  experiments/prefix-state-lfcl-decisive-2026-06/test_prefix_closure.py -q

PYTHONPATH=src/python python3 \
  experiments/prefix-state-lfcl-decisive-2026-06/prefix_state_closure_probe.py \
  --regime R2 \
  --output-dir experiments/prefix-state-lfcl-decisive-2026-06/output/R2

python3 experiments/prefix-state-lfcl-decisive-2026-06/summarize_lfcl_probe.py \
  --summary experiments/prefix-state-lfcl-decisive-2026-06/output/R2/summary.json
```

---

## Success / Falsification Criteria

### Harness gate (must pass before tier claims)

| Check | Condition |
| --- | --- |
| L0 negative control | `l0_match_rate = 0%` on R2 |
| SA static audit | `forbidden_tau_selection_violations = 0` on `closure_laws.py` |
| SA dynamic audit | `semantic_tau_le_2_branch_taken_count = 0` |

### Per-law outcomes (L1–L4)

| Outcome | Condition | Interpretation |
| --- | --- | --- |
| **Substantive support (regime)** | `early_fire_count > 0` AND `mismatch_count = 0` AND `early_match_rate = 100%` on R2 | Law forces correct `q` before full gap on tested surface → proceed to proof attempt for that law |
| **Law falsified** | `mismatch_count > 0` (confirmed on full prefix re-scan) | H<sub>CTC</sub> via that law is **falsified** on that gap; parent hypothesis needs revision or law retirement |
| **Law falsified as predictor** | `early_fire_count = 0` on entire R2 surface | That law never predicts early; **not** global H<sub>CTC</sub> falsification |
| **Unresolved for law** | Law fires only at `B = gap` (if at all) with match — equivalent to post-hoc | No forward forcing demonstrated |

### Parent H<sub>CTC</sub> aggregation (FINDINGS.md)

| Verdict | Rule |
| --- | --- |
| **Substantively supported (finite surface)** | At least one law L1–L4 passes substantive support row above |
| **Substantively falsified** | Any law fires early with `r ≠ q_ref`, OR D1 shows declared unique closure while `U(B) > 1` |
| **Unresolved (default if no early support)** | L0 fails harness; L1–L4 all falsified-as-predictor (no early fire) or only post-hoc match; no mismatch |

**Honest scope:** Universal proof of H<sub>CTC</sub> requires a theorem for the surviving
law. This experiment can **definitively falsify** with one confirmed mismatch. It can
**support on R2** only if early forced closure with zero mismatches occurs under SA.

### Summary counters (`summary.json`)

```text
gaps_total
l0_match_rate                    # expect 0
l1_early_fire_count
l1_mismatch_count                # any > 0 → falsified
l1_early_match_rate              # among early fires only
l2_early_fire_count
l2_mismatch_count
l3_early_fire_count
l3_mismatch_count
l4_early_fire_count
l4_mismatch_count
any_law_mismatch_count           # primary falsification estimand
any_law_early_support_count      # primary support estimand
max_U_before_gap_distribution    # D1 histogram buckets
semantic_audit_pass              # bool
first_mismatch_row               # per law tables
```

---

## Expected Artifacts

```text
experiments/prefix-state-lfcl-decisive-2026-06/
  experiment-design.md
  closure_laws.py              # L0–L4 implementations
  prefix_state.py              # State(p, B) builder
  semantic_audit.py            # SA static + dynamic hooks
  prefix_state_closure_probe.py
  summarize_lfcl_probe.py
  test_prefix_closure.py
  FINDINGS.md
  output/
    R2/
      summary.json
      mismatches.csv
      early_fires.csv
      law_reports.json
```

---

## Failure Modes & Mitigations

| Failure mode | Mitigation |
| --- | --- |
| L0 accidentally matches | Halt — harness bug (prior: 0 / 78 493) |
| Stride misses early fire | Re-scan full prefix on any mismatch; optional confirmation sample `p mod 64 == 0` full scan |
| L2/L3 ≡ hidden τ≤2 pick | SA dynamic audit; forbid `not composite_rejected` as emit condition |
| Law never fires misread as H<sub>CTC</sub> support | FINDINGS labels per-law “falsified as predictor” separately from parent verdict |
| `O(gap²)` blowup | Stride rule above; full scan only on mismatch candidates |
| Confusion with prior Rule X probe | Separate folder; cross-link in FINDINGS; no F1/F2-RX lanes |
| Tier C scope creep | Deferred to Phase 2 appendix |

---

## Implementation Roadmap

1. **`prefix_state.py`** — τ sieve, wheel mask, `State(p, B)` with composite-only GWR/NLSC/threat.
2. **`closure_laws.py`** — L0–L4 first-fire scanners; no `q_ref` imports.
3. **`semantic_audit.py`** — extend prior `audit_utils` patterns.
4. **`test_prefix_closure.py`** — L0 fails on `p=73`; L1–L4 do not import `q_ref`; SA clean; synthetic prefix fixture with known mismatch/silent gap.
5. **`prefix_state_closure_probe.py`** — R2 driver, stride logic, mismatch full re-scan.
6. **Run R2** — write `output/R2/summary.json`.
7. **`summarize_lfcl_probe.py` + `FINDINGS.md`** — tier-separated verdicts.

**Early falsification signal:** Step 4 unit tests + first R2 chunk (`p < 10_000`) before
full million scan.

---

## Phase 2 Optional Appendix (not blocking rev 1)

If all L1–L4 show `early_fire_count = 0` on R2:

- Run composite-exclusion probe with `candidate_bound = gap` per anchor and full rule
  stack (documented in `composite_exclusion_boundary_probe.md`), primary estimand
  `unique_resolved_survivor_count`.
- Outcomes unchanged from prior design: `> 0` with no true rejection → adjacent support;
  `true_boundary_rejected > 0` → falsify; `0 / N` → adjacent path dead on that surface.

---

## Rollback

```bash
rm -rf experiments/prefix-state-lfcl-decisive-2026-06/output
```

No production code changes required.

---

## References

| Artifact | Use |
| --- | --- |
| `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/index.html` | H<sub>CTC</sub>, L<sub>FCL</sub>, minimal decisive loop |
| `PROOF.md` | `q_ref` definition; GWR; NLSC |
| `experiments/chamber-tension-closure-falsification-2026-06/experiment-design.md` | Prior baseline; negative controls |
| `experiments/chamber-tension-closure-falsification-2026-06/forward_chamber_closure_probe.py` | τ sieve, regime pattern, decision-offset precedent |
| `experiments/chamber-tension-closure-falsification-2026-06/audit_utils.py` | AST forbidden-branch scan |
| `src/python/z_band_prime_predictor/simple_pgs_generator.py` | Wheel mask; chamber state field names |
| `research/01-generator/docs/composite_exclusion_boundary_probe.md` | Phase 2 optional baseline |