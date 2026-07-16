# Findings: PGS × sieve five-direction collab

**Date:** 2026-07-15  
**Collab status:** **done**  
**Package:** `experiments/pgs-sieve-research-directions-collab-2026-07/`

## Done bar

| # | Requirement | Result |
| --- | --- | --- |
| 1 | CHARTER + DIRECTIONS map | met |
| 2 | D4 bridge note | met (`D4_TWO_BOUNDS_BRIDGE.md`) |
| 3 | D1 probe contract | met (`D1_BOUNDED_GAP_INTERIOR_ATLAS.md`) |
| 4 | Kill shapes D1–D3 | met (`KILL_SHAPES.md`; D2/D3/D5 scoping included) |
| 5 | Single prioritized next step | **Implement and run D1 on regime R0** (p ≤ 10^6) per Hermes contract; report measured-on-R0 only |

## Peer deliveries

| Peer | Artifact |
| --- | --- |
| hermes | `D1_BOUNDED_GAP_INTERIOR_ATLAS.md` |
| agy | `D4_TWO_BOUNDS_BRIDGE.md`, `DIRECTIONS.md` |
| claude | `KILL_SHAPES.md` |
| lead | `CHARTER.md`, synthesis, status fix on D4 label |

## Prioritized next step (principal)

Run **Direction 1 R0**: bounded-gap interior atlas for consecutive primes with p ≤ 10^6, H ∈ {246, 600, 1000}, log-binned control for gap > 1000, PGS-only interior columns as in D1 contract. Language: **measured on R0** only. Do not say verified/validated.

## Explicit non-claims

- No theorem change; PROOF.md untouched  
- No Super-Signal  
- No Zhang–Maynard ⇔ PGS compression equivalence  
- D2–D5 remain design / optional until after D1 R0 measured
