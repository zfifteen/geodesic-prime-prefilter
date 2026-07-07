# Lean Readiness Gate — PROOF.md Sections

**Status:** Stub (Phase 0)  
**Rule:** Lean formalization of a section begins only when prose passes gates in [goals.md](./goals.md) G10.

| PROOF.md section | Shortcoming IDs | Prose gate | Certificate | Lean status |
|------------------|-----------------|------------|-------------|-------------|
| Next-prime algorithm (§Why…) | — | 🟡 τ↔prime needs appendix pointer | — | `lean-partial` (3 sorries) |
| Interior Maximizer | S3 | 🟡 finite base separation | ❌ | `not-started` (GWR.lean empty) |
| Ordered Comparison | — | ✅ | — | `not-started` |
| Divisor-count tail | — | ✅ | — | `not-started` |
| Earlier integers / threshold | S5, S6 | 🟡 classical appendix | — | `not-started` |
| Finite Base Lemma | S3, R1 | ❌ | ❌ | `lean-blocked` |
| Short Divisor-Average | — | ✅ | — | `not-started` |
| Large-Divisor Closure | S3 | 🟡 depends finite base | ❌ | `lean-blocked` |
| Finite Bounded-Compression Base | S3, R1 | ❌ | ❌ | `lean-blocked` |
| Residual K=128 | S4, R1 | 🟡 scope fencing | ❌ | `lean-blocked` |
| Prime-Square Proximity | **S1** | ❌ density step | — | `lean-blocked` |
| Twin-Prime Resonance | **S2** | ❌ informal steps | — | `lean-blocked` |
| Universal bounded compression (composite) | S1, S3, P2 | ❌ | partial | `lean-blocked` |
| Weak L_FCL / Rule X replay | — | 🟡 | measured R2 | `lean-partial` (axioms) |

**Legend:** ✅ ready · 🟡 minor hygiene · ❌ blocker