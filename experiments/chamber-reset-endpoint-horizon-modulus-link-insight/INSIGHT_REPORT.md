# Chamber Reset as Local Horizon Truncation vs Endpoint Chain as Global Horizon Extension

**Best-of-4 tournament winner** (applied 2026-07-08)  
**Candidate:** 3 of 4  
**Status:** Measured alignment on deterministic semiprime modulus-link cases  
**Strongest supported claim:** Local chamber-reset truncation and global endpoint-chain extension are **compositional horizon operators** whose product closes modulus links when three per-step invariants hold simultaneously.

---

## Executive Summary

PGS uses two distinct horizon mechanisms that are easy to conflate:

| Mechanism | Scope | Operator | Primary object |
|-----------|-------|----------|----------------|
| **Chamber reset** | Single anchor `p` | **Local truncation** | `lower_d_threat_offset` inside `candidate_bound` |
| **Endpoint chain** | Semiprime / RSA walk | **Global extension** | `locked_endpoints` grown by repeated `emit_record` |

The novel insight is that **modulus-link closure is not a third horizon law**. It is the **alignment predicate** stating that every local truncation along the chain is sound (does not delete the true next prime), every extension step adds the correct endpoint, and the accumulated locked set eventually contains a reciprocal floor pair `(a, b)` with `N − a·b = 0`.

On eight deterministic semiprime cases from `scale_pgs_chain_modulus_link.py`, a fresh probe confirms **8/8 closure**, **8/8 audit match**, **8/8 local truncation safety**, and **8/8 NLSC horizon containment** on all `d=4` carrier steps.

---

## 1. Local Horizon Truncation — Chamber Reset

### Source: `simple_pgs_generator.pgs_chamber_reset_state_certificate`

Given anchor prime `p` and chamber window `candidate_bound`, chamber reset:

1. Scans exact divisor counts for offsets `1 … candidate_bound`.
2. Tracks the GWR carrier (`lock_carrier_offset`, `lock_carrier_d`) — the running minimum-τ composite witness.
3. Detects a **lower-τ threat** at `lower_d_threat_offset`: the first offset after the lock where `τ(n) < lock_carrier_d`.
4. **Truncates** the local horizon: every wheel-open candidate with offset `> lower_d_threat_offset` is marked `REJECTED`.
5. Emits the first `RESOLVED_SURVIVOR` (first `τ=2` wheel-open offset not blocked by prior unresolved primes or threat truncation).

```text
LOCAL_HORIZON(p, B) = { wheel-open offsets o ≤ B : o ≤ lower_d_threat_offset(p,B) or threat absent }
```

Key certificate fields:

- `gap_offset` — consumed local horizon to reach `q`
- `lower_d_threat_offset` — truncation ceiling (may be `None`)
- `carrier_w`, `lock_carrier_d` — GWR lock state
- `tail_after_reset_offsets` — deferred material (`post_reset_tail_policy = later_chamber_material`)

### PROOF.md connection

- **Direct next-prime rule** (`q = min{n>p : τ(n)=2}`) proves the emitted survivor is exact when the chamber resolves.
- **Interior maximizer (GWR)** supplies the carrier lock whose threat scan drives truncation.
- **Prime-Square Proximity** closes the square branch via modulus-link collision geometry beneath `r²`.

Chamber reset is therefore a **prefix-truncating selector**: it decides `q` using only divisor-count state inside one chamber, without consulting chain history.

---

## 2. Global Horizon Extension — Endpoint Chain

### Source: `scale_pgs_chain_modulus_link.recursive_chain_modulus_lock`

The endpoint chain is a **horizon extension operator** over chamber resets:

```text
GLOBAL_HORIZON(seed, budget) = ⋃_{k=0..budget} { endpoints emitted by k successive chamber resets }
```

Law chain (from the modulus-link script):

1. Start from a locked seed endpoint.
2. Advance: `current ← emit_record(current)["q"]` (one chamber reset per step).
3. Add each emitted endpoint to `locked_endpoints`.
4. Floor-transport: `transported = N // current`.
5. Require `transported ∈ locked_endpoints`.
6. Require reciprocal floor closure: `N // transported == current`.
7. Require **zero modulus-link residual**: `N − min(current, transported) · max(current, transported) = 0`.

Unlike chamber reset, closure here is **history-dependent**: step `t` can succeed only if an earlier step placed `transported` into the locked set.

Production parameters:

- `PGS_CANDIDATE_BOUND = 4096` per chain step (wide local window for scale-up)
- `CHAIN_STEP_BUDGET = 4096` (global extension cap)

---

## 3. NLSC Bridge — Type-Specific Horizon Ceiling

### Source: `gpe_nlsc_selector.py`

For the dominant `d(w)=4` branch, NLSC supplies an invariant **global ceiling within the chamber**:

```text
q ≤ S_+(w)    where    S_+(w) = min{ r² : r prime, r² > w }
```

The selector row exposes:

- `threat_horizon = S_+(w)` (via `d4_closure_ceiling`)
- `square_ceiling_margin = S_+(w) − q`
- Boundary law: `q = S_+(w) − square_ceiling_margin`

Chamber-reset `lower_d_threat_offset` and NLSC `S_+(w)` are **aligned but not identical**:

| Object | Role | Scope |
|--------|------|-------|
| `lower_d_threat_offset` | Local τ-threat truncation inside `candidate_bound` | Prefix elimination |
| `S_+(w)` | Prime-square closure ceiling | Proved bound on `q` for `d=4` |

The bridge identity for alignment:

```text
emitted_q ≤ S_+(w)           (NLSC horizon contains emission)
gap_offset ≤ lower_d_threat    (truncation did not delete true q)
```

When `square_ceiling_margin` is state-derived (not oracle-fed), the NLSC selector recovers exact `q` from `S_+(w)` alone — see `select_d4_nlsc_boundary_prime`.

---

## 4. Alignment Predicate for Modulus-Link Closure

### Compositional law (candidate insight)

Define per-step alignment at anchor `p` with emission `q`:

```text
A_local(p, B):
  (i)   gap_offset ≤ B
  (ii)  lower_d_threat_offset is None  OR  gap_offset ≤ lower_d_threat_offset
  (iii) if d(w)=4: q ≤ S_+(w)

A_global(N, seed, budget):
  ∃ step t ≤ budget, endpoints a,b ∈ locked:
      floor(N/a)=b ∧ floor(N/b)=a ∧ N − a·b = 0

A_align(N, seed, B, budget)  :=  (∀ steps before closure) A_local  ∧  A_global
```

**Insight claim:** Modulus-link closure is equivalent to `A_align` on semiprime cases where both factor primes lie on the PGS chain reachable from `seed`. Chamber reset supplies local soundness; endpoint chain supplies global reachability; NLSC supplies the `d=4` ceiling that prevents emission past the square-threat wall.

### False floor pairs

The probe records **skipped floor closures** when reciprocal transport hits a locked endpoint but `N − a·b ≠ 0` (e.g. `wide_control_15251` step 10: pair `(139, 109)` gives residual `100`). Global extension must continue past these **misaligned floor shadows** until the true factor pair appears.

---

## 5. Measured Probe Results

**Script:** `chamber_horizon_alignment_probe.py`  
**Output:** `output/alignment_probe.json`

| Metric | Result |
|--------|--------|
| Cases | 8 / 8 closed |
| Audit match (expected factor endpoints) | 8 / 8 |
| All steps locally truncation-safe | 8 / 8 |
| All `d=4` steps with `q ≤ S_+(w)` | 8 / 8 |
| Total `d=4` carrier steps | 15 |
| Skipped false floor closures | 1 (`wide_control_15251`) |
| `candidate_bound=4096` vs `128` equivalence | 8 / 8 cases identical closure class |

### Bound comparison insight

On all tested semiprime cases, **local default bound 128 and production chain bound 4096 yield identical modulus-link closure**. This suggests:

- For modest semiprimes, local truncation at `B=128` is already sufficient at every chain step.
- The `4096` production bound is a **global extension safety margin**, not a per-step necessity on this surface.
- Falsification target: find a chain step where `gap_offset > 128` but `gap_offset ≤ 4096` on a modulus-link closure path.

---

## 6. Worked Example — `wide_control_15251`

`N = 15251 = 101 × 151`, seed `97`.

| Step | Anchor `p` | Emitted `q` | Gap | Threat offset | `S_+(w)` contains `q`? | Transport | Closure |
|------|------------|-------------|-----|---------------|------------------------|-----------|---------|
| 1 | 97 | 101 | 4 | 9 | n/a (`d≠4`) | 157 ∉ locked | — |
| … | … | … | … | … | … | … | — |
| 10 | 139 | 149 | 10 | 30 | yes | 109 ∈ locked, residual 100 | **skip** |
| 12 | 151 | 157 | 6 | 38 | yes (`S_+=169`) | 101 ∈ locked, residual 0 | **lock** |

Local truncations at steps 1–12 never exceed threat offsets. Global extension accumulates `{97, 101, …, 151}` until floor transport from `151` hits prior endpoint `101`.

---

## 7. Implications

### For modulus-link / RSA endpoint structure

1. **Do not merge horizons.** Chamber-reset truncation answers “what is the next prime from `p`?” Endpoint-chain extension answers “which prior endpoint does floor transport recall?”
2. **Alignment is the certificate.** A modulus-link success certificate should record per-step `A_local` fields plus the closing reciprocal pair — not merely `N mod p`.
3. **NLSC is the `d=4` alignment bridge** between local threat scans and global square ceilings; unresolved Milestone-2 work (`square_ceiling_margin` state law) is the remaining gap between oracle rows and pure selector state.
4. **False floor shadows are expected** — one skipped closure on the wide control case shows global extension must tolerate misaligned reciprocal hits.

### Relation to PROOF.md pillars

| Pillar | Local truncation role | Global extension role |
|--------|----------------------|----------------------|
| Direct next-prime | Proves single-step emission | Composes emissions into chain |
| GWR maximizer | Supplies `lock_carrier` for threat | Carrier transport in RSA v2 |
| Bounded compression / PSP | Bounds witness offset | Bounds per-step `B` sufficiency |
| Modulus-link collision (PSP) | Square-branch local geometry | Factorization via endpoint pair |

---

## 8. Open Questions and Falsification

| ID | Question | Falsification |
|----|----------|---------------|
| H1 | Does `A_local` at `B=128` hold on every chain step to crypto scale? | Find closure path requiring `gap_offset > 128` |
| H2 | Is `lower_d_threat_offset` always ≤ `square_ceiling_margin` on `d=4` steps? | Counterexample gap with threat beyond NLSC margin |
| H3 | Can `A_align` replace divisor exhaustion in `chain_horizon_closure`? | False chain node not closed by local truncations alone |
| H4 | Does global step budget scale with `log N` or `ω(N)` for RSA chains? | Case needing >64 steps with honest unresolved state |

---

## 9. Artifacts and Reproduction

```bash
# Alignment probe (production bound + local/global comparison)
PYTHONPATH=src/python python3 \
  experiments/chamber-reset-endpoint-horizon-modulus-link-insight-candidate-3/chamber_horizon_alignment_probe.py \
  --candidate-bound 4096 \
  --compare-bounds

# Parent modulus-link reference probe
PYTHONPATH=src/python python3 \
  research/06-cryptology-rsa/scripts/scale_pgs_chain_modulus_link.py
```

```text
experiments/chamber-reset-endpoint-horizon-modulus-link-insight-candidate-3/
  INSIGHT_REPORT.md
  chamber_horizon_alignment_probe.py
  output/alignment_probe.json
```

---

## 10. Candidate-3 Positioning

This candidate frames the insight as a **compositional alignment law**:

- **Local** = chamber-reset threat truncation (prefix operator).  
- **Global** = endpoint-chain locked accumulation (extension operator).  
- **Bridge** = NLSC `S_+(w)` ceiling on `d=4` carriers.  
- **Closure** = modulus-link zero on a reciprocal floor pair in the accumulated set.

The probe turns the insight into auditable per-step predicates rather than a single horizon constant `H(p, s0, chain_state)` — aligning with the open `chain_horizon_closure` question while grounding it in existing production objects (`lower_d_threat_offset`, `emit_record`, `modulus_link_residual`).