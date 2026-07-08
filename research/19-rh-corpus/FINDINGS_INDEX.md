# RH Findings Index

**Master catalog.** Stable IDs (`RH-###`) for citation in posts, bus threads, and notes.  
**Canonical paths** are relative to repository root.

| ID | Title | Status | Layer | Canonical path | One-line claim | Boundary |
|----|-------|--------|-------|----------------|----------------|----------|
| RH-001 | Direct next-prime rule | proved | L1 | `PROOF.md` | `q = min{n>p : τ(n)=2}` | Not RH; not PNT |
| RH-002 | Interior maximizer (GWR) | proved | L1 | `PROOF.md` | Leftmost min-τ maximizes `F(n)` | Not RH |
| RH-003 | Universal bounded compression | proved | L1 | `PROOF.md`, `research/04-bounded-compression/` | `w-p ≤ C(q)` at Cramér scale | Bounds witness offset only |
| RH-004 | Prime-Square Proximity | proved | L1 | `PROOF.md` §574–679 | Square branch closure for `C(q)` | Branch-specific |
| RH-005 | Twin-Prime Resonance | proved | L1 | `PROOF.md`, `research/twin-prime-resonance-technical-note-2026-07/` | 4 remainder zeros ⇒ twin gap | Corollary; not RH |
| RH-006 | Derived ½ coefficient (F18-001) | proved | L1 | `research/18-derived-half-coefficient/` | `0.5` from divisor-average closure | Not Cramér/RH proof |
| RH-010 | Zero-excess coordinate | exact | L2 | `docs/rh/dni-to-zeta-compression.md` | `E(n)=0 ⟺` prime | Integer-side; not critical line |
| RH-011 | DNI score `Z(n)` | exact | L2 | `docs/core/DIVISOR_NORMALIZATION_IDENTITY.md` | `Z(n)=n^{1-τ(n)/2}`; primes at 1 | Coordinate only |
| RH-012 | Bridge load `H(n)` | exact | L2 | `docs/rh/dni-to-zeta-compression.md` | `H(n)=log n+E(n)=τ(n)log n/2` | Use in weighted series |
| RH-020 | Divisor series `D(s)=ζ²` | exact | L3 | `docs/rh/dni-to-zeta-compression.md` | `Σ τ(n)n^{-s} = ζ(s)²` | Re(s)>1 then continuation |
| RH-021 | DNI ratio `R(s)` | exact | L3 | `docs/rh/dni-to-zeta-compression.md` | `R(s)=-ζ'(s)/ζ(s)` | Compression; not placement |
| RH-022 | Pole–zero dictionary | exact | L3 | `docs/rh/pole-placement.md` | Zeros of ζ ↔ poles of `R(s)` | Dictionary; not RH proof |
| RH-030 | d=4 fractional-position bound | proved | L4 | `research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md` | Gap-dependent `frac_pos` bound | Not uniform ≤½ |
| RH-031 | d=4 first τ=4 arrival | proved | L4 | `research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md` | First interior τ=4 at GWR | Local geometry |
| RH-032 | Prime-square threat closure | proved | L4 | `research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md` | `q ≤ S_+(w)` before next square | d=4 branch |
| RH-033 | Uniform `frac_pos ≤ ½` | invalidated | L4 | `research/pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_1000000.json` | Conjectured half-line placement | 8,505 counterexamples at 10⁶ |
| RH-034 | Chamber budget empirics | measured | L4 | `research/pgs-rh-placement-empirics-2026-06/pgs_chamber_budget_summary_1000000.md` | Budget stats on gap chambers | Finite regime |
| RH-035 | Source-to-spectral transfer lemma | unresolved | L4 | `research/pgs-rh-placement-empirics-2026-06/source_to_spectral_transfer_lemma.md` | Draft bridge to summatory constraint | Explicitly not RH |
| RH-040 | Half-scale correspondence (F18-003) | hypothesis | L4 | `research/18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md` | ½ in `C(q)` rhymes with Re(s)=½ | Not proved |
| RH-041 | Integer order before zeta | narrative | L1 | `experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md` | Primes fixed before zeta read | Explanatory; not theorem |
| RH-042 | RH is obsolete (essay) | narrative | L1 | `docs/essays/the-riemann-hypothesis-is-obsolete.md` | Reframes RH as downstream | Public consequence |
| RH-043 | Derived ½ tech note | narrative | L1 | `research/18-derived-half-coefficient/30-30-30-technical-note/` | 30/30/30 bundle for F18-001 | Exposition of proved result |
| RH-050 | Off-critical pole exclusion | unresolved | L5 | `docs/rh/off-critical-pole-exclusion.md` | Residual route to pole placement | Obstruction recorded |
| RH-051 | RH pole-placement sentence | unresolved | L5 | `docs/rh/status-ledger.md` | All nontrivial poles of `R` on Re(s)=½ | **Equivalent to RH** |
| RH-052 | Critical line geometry | narrative | L5 | `docs/rh/critical-line-and-zero-geometry.md` | Strip / line as coordinate language | Explanatory |
| RH-060 | Explicit formula bridge | narrative | L6 | `docs/rh/explicit-formula-bridge.md` | `R → Λ → ψ` translation | Not proof path |
| RH-070 | GWR bound audit (F18-002) | measured | L1 | `experiments/grok-share-509b8495/safari_transcript.txt` | 0 violations of `C(q)` to 10⁶ | External corroboration |
| RH-071 | d=4 falsification sweep 10⁷ | measured | L4 | `research/pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json` | Structural check 499,896 chambers | Measured only |
| RH-080 | Lean placement audit | measured | L4 | `lean-4/PGS/Placement.lean` | Machine-checked placement lemmas | Partial formalization |
| RH-081 | Lean RH placement invariants | measured | L4 | `lean-4/pgs-rh-placement-invariants.lean` | Placement invariant scaffold | In progress |
| RH-090 | 12-rh-bridge archive | archived | — | `research/12-rh-bridge/README.md` | Classical completion route archived | External archive only |
| RH-091 | DNI–RH bridge workbench | exact | L3 | `research/12-rh-bridge/docs/dni_rh_bridge.md` | Full ratio bridge reference | Cited; workbench archived |
| RH-092 | Off-axis pair carrier resolution | archived | L4 | `research/12-rh-bridge/docs/off_axis_pair_carrier_lemma_resolution.md` | Placement obstruction notes | Archived path |
| RH-100 | RH bundle status ledger | narrative | — | `docs/rh/status-ledger.md` | Reviewer status separation | Control doc |
| RH-101 | RH reviewer map | narrative | — | `docs/rh/reviewer-map.md` | Checking order for bundle | Reviewer control |
| RH-102 | Source order | narrative | L1 | `docs/rh/source-order.md` | Integer-first reading direction | Explanatory |

---

## Index conventions

- **Layer** — see [SOURCE_STACK.md](./SOURCE_STACK.md)
- **Status** — see [START_HERE.md](./START_HERE.md)
- **Boundary** — what the finding does *not* establish (required for RH-facing rows)

## Adding a finding

1. Assign next `RH-###` ID (increment from last row).
2. Add one row to this table.
3. Add a bullet to the matching `by-status/*.md` and `by-layer/*.md` file.
4. If the finding has a new canonical home, add a row to [README.md](./README.md) § Related chapters.

## Last updated

2026-07-08 — initial corpus (35 rows).