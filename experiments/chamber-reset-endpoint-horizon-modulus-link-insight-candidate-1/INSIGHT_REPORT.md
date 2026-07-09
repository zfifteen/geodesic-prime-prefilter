# Chamber-Reset × Endpoint-Chain Horizon × Modulus-Link: Candidate 1

**PGS-first framing.** All objects are deterministic: divisor-count field `τ`, Rule X chamber-reset replay, PGS endpoint-chain emission (`emit_record`), and modulus-link residual `N − ab`. No classical factoring oracle, no trial division, no probabilistic sieve.

**Date:** 2026-07-08  
**Candidate:** 1 of 4  
**Scope:** Interaction of chamber state reset with endpoint-chain horizon under modulus-link closure.

---

## One Sharp Falsifiable Insight

> **Horizon to Residual Duality Gate (HRDG).**  
> Chamber-reset `lower_d_threat_offset` is the *forward* endpoint-chain horizon that demotes false prime-reset survivors inside one gap chamber; modulus-link residual `N − ab` is the *multiplicative* endpoint-chain horizon that demotes false floor-transport endpoint pairs across the locked chain. A semiprime factorization `(p, q)` is selected **iff** both horizons vanish simultaneously at the same oriented chain node: the upper factor’s chamber-reset certificate emits `q` as the unique resolved survivor, and `modulus_link_residual(N, p, q) = 0` with reciprocal floor closure.

**Falsifier.** Find a semiprime `N = pq` and PGS seed such that:

1. `recursive_chain_modulus_lock` stops with `stop_reason = modulus_link_zero_locked` and `modulus_link_residual(N, p, q) = 0`, **but**
2. at the closing chain node `current = max(p, q)`, `pgs_chamber_reset_state_certificate(current)` either returns `None`, emits a different `q`, or has a second post-threat resolved survivor (violating unique reset).

If no such case exists on an extended probe surface, HRDG stands as the governing interaction law.

---

## Mechanism (Deterministic)

### 1. Chamber state reset fixes the forward horizon

Rule X (`pgs_chamber_reset_v1`) walks the divisor-count field in increasing offset order. It locks the GWR carrier at the first `RESOLVED_SURVIVOR`, then scans for a **lower-τ threat** after the lock. Any wheel-open offset strictly beyond that threat is demoted: reset freedom ends.

```89:114:src/python/z_band_prime_predictor/simple_pgs_generator.py
    threat_offset: int | None = None
    if lock_carrier_offset is not None and lock_carrier_d is not None:
        for offset in range(lock_carrier_offset + 1, candidate_bound + 1):
            divisor_count = counts[offset - 1]
            if divisor_count > 2 and divisor_count < lock_carrier_d:
                threat_offset = offset
                break
    ...
        if threat_offset is not None and offset > threat_offset:
            final_status = STATUS_REJECTED
```

The emitted certificate carries `lower_d_threat_offset` (threat horizon), `tail_after_reset_offsets`, and `post_reset_tail_policy = "later_chamber_material"`. This is the **endpoint-chain horizon** for the forward chamber episode at anchor `p`.

The RSA endpoint law names the same horizon as the reset deadline:

```58:62:research/06-cryptology-rsa/docs/endpoint_structure_law.md
The deadline value `d` is the first public upper-side boundary after `r1` where the
certificate's reset freedom ends. It is computed from the certificate's first
tail offset, first lower-divisor threat offset, or candidate bound, whichever
arrives first.
```

### 2. Endpoint-chain traversal accumulates locked horizons

The modulus-link probe does not factor `N`. It walks the PGS prime chain from a seed, locking each emitted endpoint, and tests floor transport at every step:

```104:128:research/06-cryptology-rsa/scripts/scale_pgs_chain_modulus_link.py
    for step in range(1, step_budget + 1):
        current = pgs_next_endpoint(current)
        locked_endpoints.add(current)

        transported = modulus // current
        if transported not in locked_endpoints:
            continue
        if not reciprocal_floor_closes(modulus, current, transported):
            continue

        endpoint_class_upper = max(current, transported)
        endpoint_class_lower = min(current, transported)
        if modulus_link_residual(modulus, endpoint_class_lower, endpoint_class_upper) != 0:
            skipped_floor_closures += 1
            continue

        return WalkResult(..., stop_reason="modulus_link_zero_locked")
```

Each chain node carries its own chamber-reset horizon from step 1. The walk’s **global** horizon is the composition of these per-node reset certificates along the traversed prefix.

### 3. Modulus-link is the multiplicative shadow of chamber-reset threat demotion

`PROOF.md` already treats modulus-link collision as an injectivity failure: two distinct rows sharing the same admissible least factor `ℓ` cannot tile the active row set. The cryptology probe instantiates the same predicate on chain endpoints:

```70:72:research/06-cryptology-rsa/scripts/scale_pgs_chain_modulus_link.py
def modulus_link_residual(modulus: int, left_endpoint: int, right_endpoint: int) -> int:
    """Return the modulus-link residual for two chain endpoints."""
    return modulus - left_endpoint * right_endpoint
```

**HRDG claim:** A reciprocal floor pair `(a, b)` with `b = ⌊N/a⌋` already locked but `N − ab ≠ 0` is a *multiplicative shadow survivor*: the chain-horizon analogue of a wheel-open offset that would survive past `lower_d_threat_offset` if threat demotion were omitted. The probe’s `skipped_floor_closures` counter is the operational witness of this demotion.

### 4. Observed interaction (wide-control witness)

For `N = 15251 = 101 × 151`, seed `97`, the probe skips exactly one false closure before the true lock:

| Step | `current` | `transported` | Reciprocal OK | Residual | Fate |
|-----:|----------:|--------------:|:-------------:|---------:|------|
| 9 | 139 | 109 | yes | **100** | `skipped_floor_closures += 1` |
| 11 | 151 | 101 | yes | **0** | `modulus_link_zero_locked` |

At step 9, both endpoints are on the locked chain and reciprocal floor holds, but the multiplicative horizon is nonzero (`15251 − 139×109 = 100`). Chamber-reset at `p = 139` simultaneously records `lower_d_threat_offset = 30`, marking where forward reset freedom would end inside that gap. The false partner `109` is not the transported factor; the true lock waits until the chain reaches the upper factor `151`, whose reset certificate emits the next prime with zero residual against the lower factor already locked at step 2.

This is the duality: **threat demotion protects forward offset uniqueness; residual demotion protects multiplicative endpoint uniqueness.**

---

## Code Citations (Canonical)

| Role | Location |
|------|----------|
| Chamber-reset threat horizon | `simple_pgs_generator.py` L89 to 114, L146 |
| Reset deadline semantics (public law) | `endpoint_structure_law.md` L58 to 62 |
| Modulus-link walk + residual gate | `scale_pgs_chain_modulus_link.py` L70 to 72, L104 to 128 |
| PGS next-endpoint emission | `simple_pgs_generator.py` L190 to 198 via `emit_record` |
| Modulus-link collision (square branch origin) | `PROOF.md` L615 to 616, Lean `ChamberReset.lean` L348 to 353 |
| Rule X replay mirror (Lean) | `lean-4/PGS/ChamberReset.lean` L83 to 96 |

---

## Testable Predictions

### P1: Skip to residual identity (direct, falsifiable)

On any semiprime probe surface extending `SCALE_CASES`:

```
skipped_floor_closures
  = #{ steps t | transported_t ∈ locked_endpoints_t,
                 reciprocal_floor_closes(N, current_t, transported_t),
                 modulus_link_residual(N, min, max) > 0 }
```

**Test:** Instrument `recursive_chain_modulus_lock` to log every near-closure step; confirm equality for all 8 shipped cases (currently: 0 skips on 7 cases, 1 skip on `wide_control_15251`).

### P2: True lock aligns both horizons (HRDG closure)

When `stop_reason = modulus_link_zero_locked` with pair `(p, q)` (`p < q`):

1. `pgs_chamber_reset_state_certificate(q)` returns a certificate with `gap_offset = q − prev_chain_prime` matching the final PGS hop.
2. `modulus_link_residual(N, p, q) = 0`.
3. No earlier step satisfies (2) with the same `p`.

**Test:** For each `ScaleCase` in `SCALE_CASES`, assert (1) to (3). All 8 cases currently pass `audit_match = True`.

### P3: Threat demotion is necessary for chain purity (cross-law falsifier)

Synthetic intervention: rerun chamber-reset replay **without** threat post-processing (lines 113 to 114 of `simple_pgs_generator.py`) while holding the modulus-link walk fixed. HRDG predicts **new** spurious resolved survivors appear in certificates at offsets corresponding to skipped floor pairs, but the modulus-link walk still rejects them via residual: demonstrating that forward and multiplicative horizons are **independent necessary filters**, not redundant.

**Falsifier for P3:** If omitting threat demotion never creates a second resolved survivor on any chain node that participates in a skipped floor closure, the forward/multiplicative duality is overstated.

### P4: Budget compression (operational consequence)

If HRDG holds, the endpoint-chain step budget for modulus-link closure on semiprime `N` with seed `s ≤ min(p, q)` need not exceed the index distance between `s` and `max(p, q)` in the PGS chain (currently bounded by `CHAIN_STEP_BUDGET = 4096`). Tightening the budget to that graph distance should not break any `SCALE_CASES` row.

---

## PGS-First Deterministic Reading

| Classical / forbidden | PGS replacement |
|-----------------------|-----------------|
| “Try divisors until `N = ab`” | Walk locked PGS endpoint chain; test floor transport + residual |
| “Is `q` prime?” at selection | Chamber-reset demoted signature: resolved survivor without composite witness |
| Fixed search radius | Per-node horizon `min(lower_d_threat_offset, first_tail, B)` |
| Factor-shaped audit output | Oriented endpoint class `(lower, upper)` with zero modulus-link residual |

The HRDG insight does **not** claim a new factorization theorem. It claims a **structural isomorphism** between two already-implemented demotion gates: chamber-reset threat horizon and modulus-link residual, that jointly govern when the endpoint chain may legally halt. That isomorphism is the novel, testable bridge between the proved square-branch modulus-link collision (`PROOF.md`) and the live cryptology chain walker (`scale_pgs_chain_modulus_link.py`).

---

## Summary

**Approach:** Read `PROOF.md` modulus-link collision, Rule X chamber-reset replay, and the streaming modulus-link probe as one coupled horizon system. Trace the `wide_control_15251` skip event to exhibit forward vs multiplicative demotion in a single deterministic walk.

**Deliverable:** One falsifiable insight (HRDG), mechanism, citations, four pinned predictions.

**No code changes** to production generators or probes; this candidate is report-only.