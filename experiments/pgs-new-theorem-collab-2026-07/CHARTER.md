# Collab charter: develop a new PGS theorem (candidate)

**Date:** 2026-07-15  
**Epoch:** pgs-new-theorem-collab-2026-07  
**Lead:** grok  
**Peers:** hermes, agy, claude  
**Status:** done (lead closed 2026-07-15; T0 candidate package; no PROOF.md edit)  

## Shared goal

Develop **one** new **candidate** PGS theorem: a precise statement in PGS objects, a proof-path sketch (or finite/case lemmas), falsifiers, and honest status labels. **Do not edit `PROOF.md` or promote to theorem** without the human-approved promotion process. Output is a proof-support package labeled **hypothesis / candidate** until that gate.

## Hard contracts

- PGS-first frame only (ordered gap → divisor field → GWR → law → resolved/unresolved).  
- No classical primality/sieve as inference.  
- No Super-Signal revival (invalidated).  
- No RSA/RH inflation.  
- Measured R0/R1 supports **motivation**, not proof.  
- Lead may **not** unilaterally write theorem status into `PROOF.md`.

## Primary candidate (lead seed — open to revision)

### Working name

**Gap-Width GWR Offset Monotone Saturation Law** (candidate; **hypothesis**)

### Ordinary-language claim

Inside consecutive prime gaps, the GWR-selected witness (leftmost min-divisor carrier) tends to sit closer to the left prime when the gap is tiny, and its typical offset grows with gap width only up to a short plateau — after which wider gaps do not keep pushing the average witness farther left in the same way. Twin gaps force the witness at the only interior point.

### Formal candidate statement (draft — to be tightened by peers)

Let `p < q` be consecutive primes, `g = q − p ≥ 2`, and let `w` be the GWR-selected interior integer (leftmost `n ∈ (p,q)` minimizing `d(n)`), with offset `δ = w − p` when the interior is nonempty.

**Part A (theorem-ready, nearly definitional + finite):**  
- If `g = 2`, then the unique interior is `p+1` and `w = p+1`, `δ = 1`.  
- If `g = 4`, the interior is `{p+1,p+2,p+3}` and `w` is the leftmost min-`d` among those three (explicit case analysis possible).

**Part B (candidate structural law — needs proof or stay measured):**  
For `g ≥ 2`, `δ ≤ g − 1` always (trivial). Nontrivial target: an explicit **gap-dependent** upper envelope on typical or worst-case `δ` that is **sharper than UBC** for small `g`, or a proved ordering:
for fixed magnitude band, the distribution of `δ` is stochastically nondecreasing in `g` on `2 ≤ g ≤ G0` for an explicit `G0`, then saturates.

**Part C (endpoint subclass — measured redesign, partial theorem path):**  
Partition witnesses as left-adjacent (`δ=1`), right-adjacent (`δ=g−1`), or genuine interior. Prove rates or forced classes for small fixed `g`.

UBC (already theorem) bounds `δ` at Cramér scale in `q`; this candidate aims at **gap-local** structure complementary to UBC, not a replacement.

## Done bar

1. `CANDIDATE_STATEMENT.md` — single locked formal statement (A/B/C separated by claim strength)  
2. `PROOF_PATH.md` — lemmas, dependence on existing PROOF.md stack, gaps marked unresolved  
3. `FALSIFIERS.md` — what measured/proof outcome kills each part  
4. `MEASURED_PRESSURE.md` — R0/R1 only as support; no verified inflation  
5. `PROMOTION_GATE.md` — what remains before any PROOF.md edit (human process)  
6. Lead `FINDINGS.md` synthesis; status remains **candidate/hypothesis** unless human promotes  

## Artifacts home

`experiments/pgs-new-theorem-collab-2026-07/`
