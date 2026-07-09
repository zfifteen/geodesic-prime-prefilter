# INSIGHT REPORT: Candidate 4

**Experiment:** chamber-reset-endpoint-horizon-modulus-link-insight-candidate-4  
**Date:** 2026-07-08  
**Agent:** Candidate 4 (independent implementation)  
**Status:** Hypothesis + measured cross-surface alignment (not a theorem)

---

## 1. Headline Insight

**Chamber-reset carrier lock, admissible-ℓ injectivity, and endpoint-chain floor transport share one algebraic spine: an injective partition to transport law on a finite active horizon.**

On the square branch, the active row horizon is `M = ⌊C(q)/2⌋` and rows split into small-ℓ absorption `L` versus M-rough excess `R`, with Lemma 4a guaranteeing `m ↦ ℓ_m` is injective on `R`.

On the endpoint-chain modulus link, the active horizon is the PGS chain step budget and endpoints split into **pre-lock accumulation** versus **floor-transport closure**, with closure requiring that the transported class `⌊N/e⌋` already lies in the locked endpoint set and reciprocates.

**Candidate 4's mapping claim:** these are not metaphorically similar:they are the same discrete pattern:

```text
finite horizon H
  → partition into absorbed small class L vs excess rough class R
  → injective assignment on R (no modulus-link / ℓ collision)
  → reciprocal closure forces zero residual or contradiction
```

Carrier lock is the **selection-time commit** that makes the injective assignment well-defined; floor transport is the **reciprocal placement operator** that tests whether the assignment closes to zero residual.

---

## 2. Source Objects (PGS-First)

| Layer | Primary objects | Canonical source |
| --- | --- | --- |
| Chamber reset | `carrier_d`, `lock_carrier_d`, `lower_d_threat_offset`, `carrier_w`, `tail_after_reset_offsets` | `simple_pgs_generator.py` (`pgs_chamber_reset_state_certificate`, lines 32 to 149) |
| Square-branch injectivity | rows `m ∈ {1,…,M}`, admissible `ℓ_m = r − h_m`, partition `L/R`, collision predicate | `PROOF.md` Prime-Square Proximity (lines 593 to 706), `docs/proof-enhancements/psp-closure/README.md` Lemma 4a |
| Endpoint-chain floor transport | locked endpoint set, `pgs_next_endpoint`, `transported = N // e`, reciprocal closure, modulus-link residual | `scale_pgs_chain_modulus_link.py` (`recursive_chain_modulus_lock`) |
| Semiprime one-step walk | odd-semiprime interior carriers, `gcd` factor probe | `semiprime_factor_walk.py` (`gwr_semiprime_factor_step`) |

**Theorem status (from PROOF.md):** Interior Maximizer (GWR), direct next-prime rule, universal bounded compression (including Prime-Square Proximity) are proved. Chamber-reset carrier/lock/threat is load-bearing implementation, not yet a named universal theorem. Endpoint-chain modulus-link closure is measured on the scale probe surface only.

---

## 3. Algebraic Mapping (Candidate 4 Framing)

### 3.1 Unified horizon

| Square branch | Endpoint-chain modulus link |
| --- | --- |
| `H = M = ⌊C(q)/2⌋` active rows under reductio `r² − p > C(q)` | `H = CHAIN_STEP_BUDGET` (4096) active chain steps |
| Row index `m` labels `x_m = r² − 2m` | Step index labels newly locked endpoint `e_k` |
| Activation: every `m ≤ M` is live when gap exceeds cutoff | Activation: every chain step adds one endpoint to `locked_endpoints` |

The **endpoint horizon** in both settings is the same object: the largest index range on which a placement law must close before a contradiction is forced.

### 3.2 Partition isomorphism L / R ↔ locked / transported

**Square branch (PROOF.md Step B):**

```text
L = {m : ℓ_m ≤ M}     (small-ℓ absorption)
R = {m : ℓ_m > M}     (M-rough excess)
|L| + |R| = M
```

**Endpoint chain (`scale_pgs_chain_modulus_link.py`):**

```text
L_chain = {e : e locked before floor match}
R_chain = {e : e is current endpoint whose floor image matches a prior lock}
```

At closure, the probe selects `(endpoint_class_lower, endpoint_class_upper)` with:

```text
modulus_link_residual(N, lower, upper) = N − lower · upper = 0
reciprocal_floor_closes(N, e, ⌊N/e⌋) ⟺ ⌊N/⌊N/e⌋⌋ = e
```

**Mapping insight:** `⌊N/e⌋` plays the role of a **reciprocal admissible prime placement**:the transported endpoint is admissible only if it was already registered in the locked state, exactly as `ℓ_m` is admissible only if it respects the M-rough / near-root exclusion geometry.

### 3.3 Carrier lock ↔ injective commit

**Chamber reset (generator):**

1. Walk offsets; track leftmost minimum-τ carrier (`carrier_d`, `carrier_offset`).
2. First `RESOLVED_SURVIVOR` with a carrier present → **lock** (`lock_carrier_d`, `lock_carrier_offset`).
3. Post-lock threat scan: first offset with `τ ∈ (2, lock_carrier_d)` → **lower_d_threat**.
4. Threat rewrites later survivors to `REJECTED`.

Lock is a **commit point**: after lock, the divisor field cannot admit a strictly simpler composite without violating NLSC pressure. The threat cut is the operational rejection of colliding "later simpler" states.

**Square branch (Lemma 4a):**

Injective commit on `R`: two distinct M-rough rows cannot share the same admissible `ℓ`. Shared `ℓ` would force `ℓ ≤ M` (odd-multiple spacing), contradicting M-roughness.

**Candidate 4 bridge:**

| Chamber-reset | Square-branch |
| --- | --- |
| `lock_carrier_d` commits minimum τ class | `M` commits active row horizon |
| `lower_d_threat` rejects colliding simpler τ | shared-ℓ collision rejected on `R` |
| `RESOLVED_SURVIVOR` uniqueness | `m ↦ ℓ_m` injectivity on `R` |

Carrier lock is the **chamber-scale** injective commit; admissible-ℓ injectivity is the **row-scale** injective commit. Both forbid a second simpler witness occupying the same structural slot.

### 3.4 Floor transport ↔ reciprocal factor placement

In `scale_pgs_chain_modulus_link.py`:

```python
transported = modulus // current
# require transported in locked_endpoints
# require modulus // transported == current
# require modulus - lower * upper == 0
```

This is structurally identical to the square-branch row factorization:

```text
x_m = ℓ_m · (r + h_m + d_m),   ℓ_m = r − h_m
```

Floor division is the **modulus-level** shadow of least-factor placement:

- **Forward:** endpoint `e` maps to transported class `⌊N/e⌋`.
- **Reciprocal:** closure requires the transported class to point back to `e`.
- **Residual:** zero iff the pair is an exact factorization:modulus-link analog of a fully assigned row with no unplaced excess.

The `skipped_floor_closures` counter in the probe is the operational **collision counter**: floor images that land in the locked set but fail reciprocal or residual checks correspond to near-miss ℓ collisions filtered before acceptance.

### 3.5 Semiprime factor walk (boundary role)

`semiprime_factor_walk.py` occupies a **strictly narrower** contract:

- One step only.
- Selects lower odd-semiprime interior carriers from previous/containing gaps.
- Uses `gcd(modulus, candidate)` as explicit factor probe.

On the scale-probe semiprimes (`35, 77, 143, …`), the walk returns `no_factor_progress` (selected carriers share no factor with `N`). The modulus-link chain probe **does** resolve all eight cases to the correct endpoint pair.

**Insight:** semiprime_factor_walk tests **local chamber carrier overlap** (GWR interior geometry), while scale_pgs_chain_modulus_link tests **global endpoint-chain reciprocal closure**. Candidate 4 treats the former as a **necessary local filter** and the latter as the **sufficient horizon closure**:the mapping is sequential, not interchangeable.

---

## 4. Measured Alignment (Scale Probe)

Reproduction:

```bash
cd /Users/velocityworks/IdeaProjects/prime-gap-structure
python3 research/06-cryptology-rsa/scripts/scale_pgs_chain_modulus_link.py
```

| Case | N | Seed | Upper | Lower | Steps | Locked | Skipped | Match |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| toy_35 | 35 | 5 | 7 | 5 | 1 | 2 | 0 | ✓ |
| small_77 | 77 | 5 | 11 | 7 | 2 | 3 | 0 | ✓ |
| small_143 | 143 | 7 | 13 | 11 | 2 | 3 | 0 | ✓ |
| small_221 | 221 | 11 | 17 | 13 | 2 | 3 | 0 | ✓ |
| medium_899 | 899 | 23 | 31 | 29 | 2 | 3 | 0 | ✓ |
| large_10403 | 10403 | 97 | 103 | 101 | 2 | 3 | 0 | ✓ |
| large_1022117 | 1022117 | 997 | 1013 | 1009 | 2 | 3 | 0 | ✓ |
| wide_control_15251 | 15251 | 97 | 151 | 101 | 11 | 12 | 1 | ✓ |

**Observations supporting the mapping:**

1. **Horizon depth scales with factor separation:** most cases close in 2 chain steps (3 locked endpoints); the wide control needs 11 steps and records 1 skipped floor closure:an explicit near-collision absorbed before lock.
2. **Zero residual is exact:** every case achieves `modulus_link_zero_locked`.
3. **Seed sensitivity is explicit:** `wide_control_15251` uses the same seed as `large_10403` but a different modulus geometry, demonstrating that closure is a property of the **locked transport partition**, not a single-step gcd artifact.

---

## 5. Falsification Section

### 5.1 Primary falsifiers (would refute Candidate 4 mapping)

| ID | Falsifier | Observable failure | Surface |
| --- | --- | --- | --- |
| F1 | **Injectivity break on chain horizon** | Two distinct steps yield the same transported endpoint that closes reciprocally with different current endpoints, yet residual is zero | Expand `scale_pgs_chain_modulus_link.py` cases + log all `(e, ⌊N/e⌋)` pairs |
| F2 | **Lock without reciprocal closure** | `lock_carrier_d` emitted, but floor transport from the locked carrier never lands on a prior locked endpoint within budget | Chamber-reset certificates crossed with modulus-link walk on RSA-v2 ladder |
| F3 | **Square-branch collision on audited M-rough rows** | `injectivity_holds = false` in `audit_square_branches.py` output for any certified gap | `docs/proof-enhancements/psp-closure/scripts/audit_square_branches.py` |
| F4 | **Threat before lock implies chain collapse** | Cases where `lower_d_threat_offset < gap_offset` correlate with modulus-link non-closure under the same seed | `pgs_chamber_reset_v1_pre_q_threat_scan_1e6.json` cross-walk |
| F5 | **Semiprime walk success without chain closure** | `factor_found=true` from `gwr_semiprime_factor_walk` but `recursive_chain_modulus_lock` raises budget exceeded | Joint run on expanding semiprime corpus |

### 5.2 Falsification protocol

1. **Run F1/F5** on the eight scale cases plus 20 random semiprimes `< 10^6` with PGS-derived seeds.
2. **Run F3** on the pinned audit transcript (`implementer/S1/audit_output.txt` scope).
3. **Run F2/F4** only on RSA-v2 public ladder rows (downstream audit; not an inference claim).

**Verdict tokens:**

- `mapping_survives`, no falsifier triggered on tested surface.
- `mapping_refuted`, any of F1 to F5 triggered with reproducible artifact.
- `mapping_unresolved`, probe budget exceeded without closure (explicit, not failure of mapping).

### 5.3 Current falsification status

| Falsifier | Result on tested surface | Notes |
| --- | --- | --- |
| F1 | Not observed | 8/8 scale cases: injective locked sets, 0 residual |
| F2 | Not tested at scale | Requires certificate × chain joint probe |
| F3 | Not re-run here | PROOF.md cites zero `BOUND VIOLATION` on pinned audit |
| F4 | Not observed historically | `pgs_chamber_reset_v1_pre_q_threat_scan_1e6.json`: 0 pre-q threats for `p ≥ 5` |
| F5 | Observed partial split | Scale semiprimes: chain resolves, one-step walk does not factor |

**Epistemic label:** `mapping_survives` on the scale-probe + documented finite chamber surfaces; `mapping_unresolved` for full RSA-bit endpoint-chain elevation.

---

## 6. Comparison Table: Four Candidate Insight Framings

Independent implementations were tasked with mapping the same three pillars. Candidate 4's partition to transport isomorphism is one of four defensible framings:

| Dimension | Candidate 1 (expected) | Candidate 2 (expected) | Candidate 3 (expected) | **Candidate 4 (this report)** |
| --- | --- | --- | --- | --- |
| **Core metaphor** | Field-for-field identification | Certificate transport / signature carry | Local carrier → global factor | **Partition to transport isomorphism on horizon** |
| **Chamber lock role** | `lock_carrier_d` ≡ row threshold `M` | Lock fields transported across `⌊N/x⌋` | Lock selects odd-semiprime pool | **Injective commit before reciprocal test** |
| **ℓ injectivity role** | Direct row to offset dictionary | Signature collision forbids duplicate ℓ | gcd injectivity on carriers | **`R`-class injectivity ↔ locked-endpoint injectivity** |
| **Floor transport role** | Secondary / audit-only | Primary: deadline-signature correction | Absent or downstream | **Reciprocal placement operator dual to ℓ·(r+h+d)** |
| **Semiprime walk** | Out of scope | Sidecar diagnostic | Central bridge | **Necessary local filter, not sufficient closure** |
| **Primary proof anchor** | PROOF.md row geometry | RSA-v2 PGS_CERTIFICATE.md | `semiprime_factor_walk.py` | **PROOF.md Lemma 4a + scale probe measured closure** |
| **Falsification emphasis** | Row collision audit | Signature mismatch on ladder | gcd hit without certificate | **Injectivity break + skipped_floor_closures > 0 with wrong endpoints** |
| **Elevation target** | Square-branch only | Cryptology certificate law | Semiprime recovery | **Named object: Horizon-Partition Transport Law** |
| **Risk profile** | Over-identifies distinct layers | Under-tests square-branch audit | Classical gcd drift | **Abstract partition may hide seed-dependence** |

**Candidate 4 differentiation:** refuses to collapse the three layers into a single dictionary (C1) or a single transport story (C2); instead names the **shared injective partition law** as the mathematical common denominator, with semiprime walk demoted to a local necessary condition (contra C3).

---

## 7. Proposed Named Object (Hypothesis Only)

**Horizon-Partition Transport Law (HPTL), provisional**

For a finite active horizon `H` and a commutative placement operator `T` (floor transport or least-factor assignment):

1. Partition indices into absorbed class `L` and excess class `R` (`|L| + |R| = |H|`).
2. Commit a carrier lock selecting the minimum-τ (or minimum-excess) witness.
3. Require injectivity of the placement map on `R`.
4. Require reciprocal closure `T⁻¹(T(x)) = x` on the committed pair.
5. Accept only when the link residual is zero; otherwise emit `unresolved`.

**Status:** hypothesis. Not in PROOF.md. Elevatable only after F1 to F5 gates on expanded surfaces.

---

## 8. Reproduction Commands

```bash
# Modulus-link scale probe (measured alignment)
python3 research/06-cryptology-rsa/scripts/scale_pgs_chain_modulus_link.py

# Semiprime one-step walk (local filter boundary)
python3 -c "
from z_band_prime_predictor.semiprime_factor_walk import gwr_semiprime_factor_walk
for n in [35, 77, 143, 221, 899, 10403]:
    print(n, gwr_semiprime_factor_walk(n)['stop_reason'])
"

# Square-branch injectivity audit (falsifier F3)
python3 docs/proof-enhancements/psp-closure/scripts/audit_square_branches.py
```

---

## 9. State Separation Summary

| Claim | Status |
| --- | --- |
| GWR / next-prime / bounded compression | Theorem (PROOF.md) |
| Lemma 4a admissible-ℓ injectivity on M-rough rows | Theorem (PROOF.md + psp-closure README) |
| Chamber-reset carrier/lock/threat cut | Load-bearing implementation; measured on generator surfaces |
| Endpoint-chain modulus-link zero lock on 8 cases | Measured result (this session) |
| Semiprime factor walk on scale cases | Measured: no factor progress |
| HPTL / partition to transport isomorphism | **Hypothesis** (Candidate 4 mapping) |
| Full RSA-scale elevation of mapping | **Unresolved** |

---

## 10. Recommended Next Actions

1. **Joint probe:** emit `pgs_chamber_reset_state_certificate` at each locked endpoint in `recursive_chain_modulus_lock` and record whether `lock_carrier_d` / threat fields predict `skipped_floor_closures`.
2. **F1 harness:** log full `(step, e, ⌊N/e⌋, residual)` tuples to CSV for falsifier automation.
3. **Synthesis:** compare all four candidate INSIGHT_REPORTs and select either a unified HPTL elevation card or an explicit split (square-branch vs cryptology horizons may require distinct partitions).

---

*Subordinate to PROOF.md for theorem status. PGS-first, deterministic, state-separated. Candidate 4 independent implementation.*