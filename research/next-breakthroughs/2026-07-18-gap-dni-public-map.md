# Gap-structure + DNI public map for modulus pressure

**Date:** 2026-07-18 (V3 update 2026-08-07)  
**Status labels:** hypothesis (map law) | measured only where named fixtures already exist | not theorem | not RSA solve  
**Frame:** PGS objects -> PGS invariants -> PGS rule -> resolved | unresolved | invalidated  

**Bound words:** verified/validated **absent** (no residual-family or map-family executed 10^18 surface).

## Plain idea (ordinary language first)

You have a large public product `N`. You do **not** start by guessing factors and testing them.

Instead you build a **public map** from:

1. ordered prime-gap structure near the integers that PGS already knows how to walk (endpoints, chambers, selected integers, divisor-count field);
2. DNI / GWR geometry that ranks local structure without classical primality oracles;
3. floor transport of those public objects through `N` (reciprocal map `y = floor(N/x)`);
4. named residual when the transported geometry fails to close.

The map’s job is to **classify the public state** of `N`: certificate (resolved endpoint structure) or a **named residual cell**. Reducing “how many integers you might trial-divide later” is a **downstream audit metric**, never the inference rule.

## Objects on the map

```text
N public
s = floor(sqrt(N))
lower public endpoint chain / previous_public_endpoint_before(s)
PGSPG reset certificates (carrier, lock, gap, reset signature)
GWR-selected fields and DNI-normalized local ranks
floor transport x -> floor(N/x)
reciprocal endpoint closure predicates
residual vector R = (r_carrier, r_tail, r_lock)   [hypothesis ranks]
joint residual cell id  e.g. C1T2L1
pinch_S diagnostic
```

Live measured anchor (not theorem): 50-bit fixture V2 residual was  
`unresolved_by_joint_cell_C1T2L1` with R=(1,2,1), pinch_S=54. V3 (2026-08-07)  
carrier reciprocal closure emits `resolved_by_carrier_reciprocal_closure`  
endpoint_class=[32047633,32059651] (measured-on-regime-only / hypothesis).  
40-bit still resolves. See `notes/ACTIVE_GOAL_50bit_residual_discriminator.md` and  
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/DOCUMENTATION_LOCK_50BIT_V3.md`.

## Map layers (hypothesis design)

### Layer 0 — Chamber / endpoint atlas (public)

Around `s` and along the lower endpoint chain, record chamber resets and certificate fields.

### Layer 1 — DNI / GWR local ranks (public)

On certificate-selected integers, rank divisor-field structure under proved GWR / DNI language.

### Layer 2 — Transport field (public)

For each public coordinate `x` on Layer 0–1, plot `y = floor(N/x)` and the residual of reciprocal closure against the dual certificate.

### Layer 3 — Residual atlas (decision layer)

Collapse Layer 2 failures into a finite residual taxonomy (joint cell R, first-tail, carrier misalignment, lock weak, …).  
**Resolved** = structural certificate emission (including V3 carrier reciprocal closure).  
**Unresolved** = named cell only. Never silent failure; never classical fallback.

## Explicit non-claims

- Not a new factorization algorithm in the classical sense.  
- Not a theorem that RSA is broken.  
- Not promotion of residual cell R to PROOF.md.  
- Not verified/validated residual-family language without 10^18 map surface.

## Sources in-repo

- `research/06-cryptology-rsa/docs/endpoint_structure_law.md`
- `research/next-breakthroughs/2026-07-14-residual-cell-C1T2L1.md`
- `research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/DOCUMENTATION_LOCK_50BIT_V3.md`
