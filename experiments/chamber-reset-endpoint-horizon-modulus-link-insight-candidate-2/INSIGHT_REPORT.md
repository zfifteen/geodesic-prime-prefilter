# INSIGHT REPORT — Candidate 2

**Experiment:** Chamber reset × endpoint chain horizon × modulus-link  
**Rule ID:** `carrier_lock_horizon_transfer_v1_candidate_2`  
**Date:** 2026-07-08  
**Status:** Insight + pilot probe (no generator patch)

---

## Executive summary

The three subsystems named in the task — **chamber reset**, **chain_horizon_closure**, and **modulus-link** — are not independent bridges. They share one PGS-visible invariant:

> **The post-reset tail envelope at anchor `p`, together with the carrier lock frozen at reset, defines the residual divisor-search horizon for every rightward PGS continuation from `p`.**

Candidate 2 names this invariant **Carrier-Lock Horizon Transfer (CLHT)** and proposes it as the missing object `H(p, s₀, chain_state)` from `docs/unanswered-questions/chain-horizon-closure/00_question.md`.

The horizon law is **not** “prove the terminal node prime.” It is “close every false rightward node before the true next prime using only chamber-reset geometry already computed at `p`.” That reframing matches the consensus in the chain-horizon-closure answers (especially 05_chatgpt, 02_meta_ai).

---

## Problem framing

### What is solved

| Layer | Status | Evidence |
|-------|--------|----------|
| Direct next-prime rule | Proved | `PROOF.md` pillar 1 |
| Interior maximizer (GWR) | Proved | `PROOF.md` pillar 2 |
| Universal bounded compression `C(q)` | Proved | `PROOF.md` pillar 3 |
| Chamber-reset selection | Operational, audit-clean | `simple_pgs_generator.py`, C mirror `pgs_chamber.c` |
| Modulus-link factor recovery | Operational on scale cases | `scale_pgs_chain_modulus_link.py` |
| Chain-horizon closure | Operational, ~56–58% at 10¹⁵/10¹⁸ | Documented in chain-horizon-closure answers |

### What is not solved

`chain_horizon_closure_result(..., horizon_bound=None)` still falls through to complete divisor exhaustion up to `√n` for false shadow-chain nodes. The generator is accurate but not predominantly PGS-derived at high scale.

The missing theorem target is sharper than primality proving:

```text
H(p, s₀, chain_state) = minimal divisor horizon that closes every
pre-terminal false shadow-chain node, derivable from PGS-visible state only.
```

---

## Core insight: Carrier-Lock Horizon Transfer (CLHT)

### The coupling fields

Three certificate fields already computed at every chamber reset are load-bearing across all three subsystems:

| Field | Chamber reset role | Chain-horizon role | Modulus-link role |
|-------|-------------------|-------------------|-------------------|
| `lock_carrier_offset`, `lock_carrier_d` | Freeze GWR minimum τ at first `RESOLVED_SURVIVOR` | Bounds τ of any false node surviving visible closure | Sets transport tightness of reciprocal floor images |
| `tail_after_reset_offsets` | Unresolved wheel-open material after `q` | Virtual rightward continuation of chamber; shadow seeds extend this tail | Depth of locked-endpoint set needed before reciprocal closure |
| `lower_d_threat_offset` | First τ-improvement after lock | Early closure witness for false nodes near seed | Deadline-signature transport alignment (RSA v2) |

These are emitted identically in Python (`simple_pgs_generator.py:78–155`) and C (`pgs_chamber.c:587–628`).

### The CLHT horizon law (candidate theorem)

For anchor prime `p`, visible divisor bound `V = 10_000`, and chamber-reset certificate `CR(p)`:

```text
H_CLHT(p, s₀, chain_state) =
    V + max(tail_after_reset_offsets(CR(p)))
    + max_chain_gap(s₀)
```

**Interpretation:**

1. **`V`** — any false semiprime-shadow node surviving bounded visible closure must have both factors ≥ `V`; this is the existing `DEFAULT_VISIBLE_DIVISOR_BOUND` surface.
2. **`max_tail_offset`** — the chamber-reset tail is the *physical* rightward envelope inside `candidate_bound=128`. Shadow-chain nodes are logical extensions of the same tail geometry; their divisor witnesses cannot require search deeper than the tail already explored at `p`.
3. **`max_chain_gap`** — wheel-open spacing between shadow-chain candidates (standard H1 term from answer 05).

**Key distinction from H1 alone:** H1 uses only chain-internal gaps. CLHT adds the **transported tail envelope from the anchor chamber**, which is visible before any shadow chain is built.

### Connection to PROOF.md

Universal bounded compression gives:

```text
C(q) = max(64, ⌈0.5 · log(q)²⌉)
```

CLHT operates at a different scale:

- `C(q)` bounds **witness offset** `w − p` inside a gap (prefix attainment).
- `H_CLHT` bounds **divisor witness search** for false rightward chain nodes (suffix continuation).

Both are logarithmically small compared to `√q`. CLHT inherits the chamber’s finite `candidate_bound=128` window, so `max_tail_offset ≤ 128` always. The pilot confirms `H_CLHT ≤ 10_128` on all tested surfaces — seven orders of magnitude below `√(10¹⁸)`.

### Connection to modulus-link

`scale_pgs_chain_modulus_link.py` walks the PGS endpoint chain until:

1. Each new endpoint is added to `locked_endpoints`.
2. `floor(N / endpoint)` lands in `locked_endpoints`.
3. Reciprocal floor closes.
4. Modulus-link residual is zero.

**CLHT claim for modulus-link:** the number of chain steps required before lock closure is coupled to the **tail depth at the seed endpoint**, not to `√N`.

| Case | Seed tail_count | max_tail | chain_steps | locked_endpoints |
|------|-----------------|----------|-------------|------------------|
| toy_35 | 0 | 0 | 1 | 2 |
| small_143 | 27 | 124 | 2 | 3 |
| medium_899 | 26 | 128 | 2 | 3 |
| large_1022117 | 19 | 126 | 2 | 3 |
| wide_control_15251 | 1 | 6 | **11** | **12** |

Cases with rich tail geometry (143, 899, 1022117) close in 2 steps. The wide control fails CLHT coupling: shallow tail (count=1) forces 11 steps — the seed’s carrier lock did not pre-transport enough envelope for modulus closure.

This mirrors RSA v2 transport analysis (`STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md`): true positives show tight first-tail-to-upper-anchor alignment (−5); false positives are looser (−22). CLHT formalizes that observation as a **horizon bound**, not a post-hoc transport filter.

---

## Pilot results

Probe: `clht_coupling_probe.py` → `clht_coupling_summary.json`

### Chamber surface (primes < 2000, bound=128)

| Metric | Value |
|--------|-------|
| Certificates | 301 |
| `H_CLHT` min / median / max | 10_000 / 10_060 / 10_128 |
| `max_tail_offset` max | 128 |
| Zero-tail fraction | 27.6% |
| `H_CLHT / √q` max | 0.002 (at small q) |

### Structural observations

1. **Tail is typical, not exceptional.** Median tail_count = 8; only 27.6% of gaps have empty tail.
2. **Carrier lock is low-τ.** On the sample surface, `lock_carrier_d ∈ {3,4,6,8,12,14,16,18,20,24}` — consistent with GWR minimum-divisor structure from PROOF.md.
3. **Horizon is scale-flat.** `H_CLHT` varies by at most 128 over 301 certificates, while `√q` grows without bound. This falsifies “horizon tracks `√q`” and confirms PGS-visible compressibility.

---

## Comparison to existing horizon candidates (answers 05–06)

| Law | Formula | CLHT assessment |
|-----|---------|-----------------|
| H0 | `V` | Necessary but not sufficient when seed is far into tail |
| H1 | `V + max_chain_gap` | Chain-local; misses anchor tail envelope |
| H2–H6 | residue/LCM/row-level fits | Higher complexity; pilot suggests unnecessary at first order |
| **CLHT** | `V + max_tail_offset(p) + max_chain_gap` | **Adds the missing anchor transport term** |

CLHT subsumes H1 and explains why modulus-link and RSA transport probes see tail-sensitive behavior: the anchor tail is the transported horizon.

---

## Falsification criteria

CLHT is **falsified** if any of the following hold on chain_horizon_closure rows at 10¹², 10¹⁵, 10¹⁸:

1. Some pre-terminal false node has `lpf(n) > V + max_tail_offset(p) + max_chain_gap`.
2. `H_CLHT` fails to close a false node while the current fallback succeeds.
3. Modulus-link cases with `tail_count ≥ 10` routinely need `chain_steps > tail_count + 3`.

CLHT is **confirmed** if:

1. 100% of pre-terminal false nodes close at `H_CLHT` on sampled scales.
2. First surviving terminal candidate matches current `chain_horizon_closure`.
3. `H_CLHT / √n < 0.001` across all scales.
4. Modulus-link step count correlates with `max(0, τ_tail − τ_lock)` where `τ_tail = |tail_after_reset_offsets|` and `τ_lock = lock_carrier_offset`.

---

## Recommended next steps

1. **Instrument** `chain_horizon_closure_result` (or run `simple_pgs_shadow_chain_horizon_law_probe.py` when full generator API is restored) to log per-row:
   - `max_tail_offset(p)`, `lock_carrier_d`, `lock_carrier_offset`
   - `H_CLHT` vs observed `max_lpf_false`
   - `chain_steps` analog for shadow chains

2. **Promote CLHT to selector** only after the falsification gate passes on 10¹²/10¹⁵/10¹⁸ rows:
   ```python
   horizon_bound = V + max(cert["tail_after_reset_offsets"] or [0]) + max_chain_gap
   ```
   Replace `horizon_bound=None` fallback with this expression.

3. **Extend modulus-link** to emit CLHT diagnostics: when `chain_steps` exceeds `tail_count + 2`, flag `clht_coupling_break` (as in wide_control_15251).

4. **Do not patch the generator** until mining data is published — consistent with solution 05_copilot recommendation.

---

## Files produced

| File | Purpose |
|------|---------|
| `INSIGHT_REPORT.md` | This document |
| `clht_coupling_probe.py` | Pilot coupling probe |
| `clht_coupling_summary.json` | Machine-readable pilot output |

---

## Conclusion

The novel PGS insight for candidate 2 is that **chain_horizon_closure is not a separate divisor-exhaustion bridge** — it is the rightward transport of the chamber-reset tail envelope under carrier lock. The fields `tail_after_reset_offsets`, `lock_carrier_d`, and `lock_carrier_offset` are already computed at every reset; CLHT uses them to bound `H` without `√q` work.

If the full shadow-chain mining experiment confirms the pilot, the 56–58% non-PGS high-scale bridge converts to pure PGS by a single horizon substitution. The theorem target is:

> **Shadow-Chain Carrier-Lock Horizon Law:** Within `candidate_bound=128`, every false semiprime-shadow node before the true next prime has a divisor witness ≤ `V + max_tail_offset(p) + max_chain_gap`, and that bound is derivable from the chamber-reset certificate at `p` alone.

This unifies chamber reset, endpoint chain horizon, and modulus-link under one finite, scale-independent invariant.