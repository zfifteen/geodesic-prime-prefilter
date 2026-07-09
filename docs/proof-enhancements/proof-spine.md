# PROOF.md Proof Spine Map

**Date:** 2026-07-08  
**Authority:** `PROOF.md` (theorem status) · [goals.md](goals.md) G7

One-page dependency map: which universal claims depend on analytic closure,
finite certificates, and classical imports.

## Universal pillars

| Claim | PROOF.md anchor | Depends on | Classical imports |
| --- | --- | --- | --- |
| Next-prime rule | Headline §1 | τ characterization; chamber scan | : |
| Interior maximizer (GWR) | Headline §2; §Interior Maximizer | Ordered comparison; earlier integers | : |
| Universal bounded compression | Headline §3 | GWR; finite bases; square branch | CL-001 (gap bounds) |
| Prime-Square Proximity | §Prime-Square Proximity | Near-root exclusion; modulus-link | CL-001 |

## Corollaries (not headline pillars)

| Claim | PROOF.md anchor | Depends on | Status |
| --- | --- | --- | --- |
| Twin-Prime Resonance (GWR Super-Signal) universal implication | §Twin-Prime Resonance | GWR winner + remainder zeros | **invalidated** (CE certificates 2026-07-09) |
| Modular zero lemma on $M_{v1}$ | §Twin-Prime Resonance (surviving) | remainder-vector case analysis | proved; not a twin-gap lock |

The universal Super-Signal twin-gap implication is **invalidated**. The modular
lemma $z(w)\ge 4 \Leftrightarrow 30\mid w$ on $M_{v1}$ survives. Super-Signal
is not a premise for the three headline pillars.

## Finite-certified premises

| Certificate | Closes | Used by |
| --- | --- | --- |
| `gwr_finite_base_v1` | earlier-integer side for `p < 5×10⁹` | Pillars 1 to 2; earlier-integer closure |
| `bounded_compression_base_v1` | small-`q` bounded compression | Pillar 3 |
| `residual_k128_v1` | high-τ branch elimination | Pillar 3 (odd-adjacent `d=4`) |
| `gwr_stress_10e12_v1` | measured corroboration only | Supplemental audit (not a premise) |

## Classical imports (`PROOF.md` §Imported Classical Lemmas)

| ID | Used in |
| --- | --- |
| CL-001 Bertrand | Witness Threshold; Large-Divisor Adjacent Closure |
| CL-002 divisor-pair bound | Short Divisor-Average; Large-Divisor Adjacent Closure |
| CL-003 `τ(r²)=3` | Prime-Square Case; Placement.lean (roadmap M2) |

## Lean module mirror (planned)

```text
PGS/Basic.lean          → τ characterization (M1)
PGS/Placement.lean      → d=4 placement (RH-080)
PGS/ChamberReset.lean   → near-root exclusion; PSP (M4)
PGS/GWR.lean            → interior maximizer (M5)
```

See [lean-4/PLACEMENT_FORMALIZATION_ROADMAP.md](../../lean-4/PLACEMENT_FORMALIZATION_ROADMAP.md).