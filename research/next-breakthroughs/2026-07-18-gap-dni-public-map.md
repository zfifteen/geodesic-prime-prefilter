# Gap-structure + DNI public map for modulus pressure

**Date:** 2026-07-18  
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

## Why this is not classical factoring

| Classical default | PGS map |
| --- | --- |
| Sample or enumerate candidate factors | Walk public endpoint / chamber objects |
| `isprime` / sieve / Miller-Rabin chooses survivors | GWR / DNI / certificates choose selected structure |
| `gcd` / product closes the pair | Floor transport + reciprocal closure + residual taxonomy |
| “Smaller list = method works” | Named residual honesty when still open |

Shape warning if the implementation becomes: build map → dump candidate list → trial division. That reverts to candidate search with PGS garnish.

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

Live measured anchor (not theorem): 50-bit fixture remains unresolved under  
`unresolved_by_joint_cell_C1T2L1` with R=(1,2,1), pinch_S=54; 40-bit still resolves.  
See `notes/ACTIVE_GOAL_50bit_residual_discriminator.md` and  
`research/next-breakthroughs/2026-07-14-residual-cell-C1T2L1.md`.

## Map layers (hypothesis design)

### Layer 0 — Chamber / endpoint atlas (public)

Around `s` and along the lower endpoint chain, record chamber resets and certificate fields. This is geometry of **where the public walk is**, not a list of factors.

### Layer 1 — DNI / GWR local ranks (public)

On certificate-selected integers, rank divisor-field structure under proved GWR / DNI language. Output is structural ranks and signatures, not “probably prime.”

### Layer 2 — Transport field (public)

For each public coordinate `x` on Layer 0–1, plot `y = floor(N/x)` and the residual of reciprocal closure against the dual certificate. This is the modulus-link field.

### Layer 3 — Residual atlas (decision layer)

Collapse Layer 2 failures into a finite residual taxonomy (joint cell R, first-tail, carrier misalignment, lock weak, …).  
**Resolved** = structural certificate emission.  
**Unresolved** = named cell only. Never silent failure; never classical fallback.

### Layer 4 — Optional audit metric (not inference)

If and only if audit is requested: count how many classical factor-neighborhood pairs would have been eliminated *had* one listed them. Report as measured search-space reduction on named regimes. Do not feed that count back into choosing `p` or `q`.

## Relation to prior program art

| Prior surface | Overlap | Delta of this packaging |
| --- | --- | --- |
| Endpoint structure law / rsa-v2–v3 | transport + residual | Same spine; map is the multi-layer atlas framing |
| Residual cell C1T2L1 | residual ranks | Cell is one **pixel** of Layer 3, not the whole map |
| Stage-One / PGA grammar pruner / endpoint-space reduction | public grammar reduces space | Those measure pair-elimination; this map **primary** is residual coordinates |
| Classical sieve / ECM / NFS | reduce factor search | Forbidden as PGS inference; comparison only |

## Z-map (intensity of the idea)

- **A (state):** residual mass still open on the public map (named cells unresolved for a fixture family).
- **B (rate):** public constraints applied per cycle (certificate checks, transport residuals, residual-rank updates).
- **C (capacity):** public information budget: only `N` + deterministic PGS certificates / chain objects (no secret factors, no classical gates).
- **Intensity:** ~ A × (B/C). High when many public constraints fire but residual mass stays large → honest hard residual. Low residual mass with high B under fixed C is progress toward certificate.
- **Regime:** mid-scale fixtures (40/50/64-bit class) are the correct pressure band now. High intensity with theorem-inflation prose is theater.
- **Falsifier:** map that only shrinks classical candidate lists while residual taxonomy is unchanged, or any resolve that requires gcd/`%`/isprime inside inference.

## Decision rule (hypothesis)

```text
When Layer 3 emits a stable residual cell for fixture family F under fixed
first-tail windows and public-only fields, treat F as residual-pressure target
(not as “almost factored”).

When Layer 3 collapses to certificate on F without classical gates, treat as
resolved endpoint structure (audit factors downstream only).

When Layer 4 pair-elimination improves but Layer 3 cell is unchanged, label
NO_DELTA for the map law (grammar garnish only).
```

## What would count as ADVANCE for a first probe

1. One public map schema (JSON) for a single `N`: layers 0–3 only.  
2. 40-bit control: Layer 3 empty / certificate class (matches live resolve).  
3. 50-bit pin: Layer 3 = joint cell C1T2L1 (or stricter named subclass), not endpoint.  
4. Kill check: true mutual-close pin must not land in C1T2L1 under fixed windows.  
5. No classical inference fields in the map object.

## Explicit non-claims

- Not a new factorization algorithm in the classical sense.  
- Not a theorem that RSA is broken.  
- Not promotion of residual cell R to PROOF.md.  
- Not verified/validated residual-family language without 10^18 map surface.

## Next pressure (if principal approves build)

Implement a **read-only map emitter** beside rsa-v3 residual ledger:

```text
input: public N + existing resolver public diagnostics
output: map_layers.jsonl (layers 0–3) + residual cell id
test: regression fixtures; 40-bit cert / 50-bit C1T2L1
```

Prefer that over a new candidate-list pruner.

## Sources in-repo (prior art, not external web)

- `research/06-cryptology-rsa/docs/endpoint_structure_law.md`
- `research/next-breakthroughs/2026-07-14-residual-cell-C1T2L1.md`
- `research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`
- Stage-One / grammar pruner docs under `docs/supergrok-stage-one-brief-2026-05-22.md` and PGA pruner surfaces
