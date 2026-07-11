# Layer 4: Chamber / source geometry

**Status mix:** `proved`, `measured`, `hypothesis`, `unresolved`, `invalidated`  
**Proves RH?** No  
**May drive new work?** Yes, as **integer** chamber geometry only

Chamber invariants, d=4 carrier geometry, and empirics. This layer asks:
**where** does the GWR witness sit inside its prime-gap interior, and what
deterministic bounds hold on that integer placement?

It does **not** ask how to place poles of \(R(s)\). Spectral transfer drafts
are downstream and dormant unless a new source law forces them. Hard rule:
[FRAME_CONTRACT.md](../FRAME_CONTRACT.md).

**Canonical folder:** [pgs-rh-placement-empirics-2026-06](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md)

---

## Deferred scan paths (boundary text)

| Path | Why deferred | Does not prove |
|------|--------------|----------------|
| `pgs_rh_bridge_placement_focus_prompt.md` | **Superseded** by FRAME_CONTRACT (was RH-resolution activation) | Do not use as task driver |
| `docs/faq/**` | Reviewer vocabulary | RH or compression |
| `research/12-rh-bridge/**` (beyond RH-090 to 092) | Archived workbench | Live placement route |
| `research/18-derived-half-coefficient/FORMALIZATION_PROPOSAL.md` | Lean scaffolding memo | F18-001 (already RH-006) |

Indexed placement findings: RH-030 to 035, RH-071, RH-080 to 081. See [GAP_ANALYSIS.md](../GAP_ANALYSIS.md).

---

## Geometry primitives

| Primitive | Definition | Status |
|-----------|------------|--------|
| $frac\_pos$ | $(w-p)/(q-p-1)$ in nonempty interior | proved bounds for d=4 branch |
| Chamber budget | Log-weight spend inside gap | measured at $10^6$ |
| Resonance | Primorial remainder zeros at $w$ | modular pattern only; **not** universal twin termination ([RH-005](../FINDINGS_INDEX.md) **invalidated**) |
| Half-scale rhyme | $\tfrac12$ in $C(q)$ vs $\operatorname{Re}(s)=\tfrac12$ | [RH-040](../FINDINGS_INDEX.md) **quarantined** hypothesis; not a work target |

Uniform $frac\_pos\le\tfrac12$ was **falsified** ([RH-033](../FINDINGS_INDEX.md)): 8,505
counterexamples at $10^6$.

---

## GWR witness placement (source geometry)

Before d=4 fractional bounds, the chamber already has proved placement structure:

| Object | Role | Authority |
|--------|------|-----------|
| GWR $w$ | Leftmost min-$\tau$ in $I=\{p+1,\ldots,q-1\}$ | [RH-002](../FINDINGS_INDEX.md) |
| Offset $w-p$ | Bounded by $C(q)=\max(64,\lceil\tfrac12(\log q)^2\rceil)$ | [RH-003](../FINDINGS_INDEX.md), [RH-006](../FINDINGS_INDEX.md) |
| Square branch | $\tau(w)=3$, $w=r^2$ closed by Prime-Square Proximity | [RH-004](../FINDINGS_INDEX.md) |
| Non-square near-max | F18-004 rough-witness discipline (measured) | [RH-103](../FINDINGS_INDEX.md) |
| Residual $d=4$ | Odd-adjacent first $\tau=4$ carrier geometry | [RH-030](../FINDINGS_INDEX.md) to [RH-032](../FINDINGS_INDEX.md) |

$$
\mathrm{frac\_pos}(p,q)=\frac{w-p}{q-p-1}\qquad(|I|\ge 1).
$$

L3 maps the same chamber into Dirichlet increments $\Delta D$, $\Delta B$
([03-zeta-compression.md](./03-zeta-compression.md)); L4 owns the **position** of $w$,
not the zeta series.

### RH-033 replacement principle (Q8 / #46)

| Item | Status | Artifact |
|------|--------|----------|
| Invalidated rule | RH-033 uniform `frac_pos ≤ ½` | [pgs_d4_frac_pos_falsification_1000000.json](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_1000000.json) |
| **Replacement (proved)** | RH-030 gap-dependent bound | [d4_fractional_position_bound.md](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) §Phase 5 to 6 |
| Scale corroboration | RH-071 measured at $10^7$ | [pgs_d4_frac_pos_falsification_10000000.json](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json) |

**Principle:** Do not use a global half-line placement rule. Use the gap-dependent
`frac_pos` bound tied to right margin `m = q - w`. A falsification of the
replacement would be a chamber where RH-030 is violated (re-run
`research/pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification.py`
at $10^7+$).

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-030](../FINDINGS_INDEX.md) | proved | [d=4 fractional-position bound](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) | [d4_fractional_position_bound.md](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) |
| [RH-031](../FINDINGS_INDEX.md) | proved | [d=4 first τ=4 arrival](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) | [d4_fractional_position_bound.md](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) (first τ=4 corollary) |
| [RH-032](../FINDINGS_INDEX.md) | proved | [Prime-square threat closure](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) | [d4_fractional_position_bound.md](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) (prime-square threat closure) |
| [RH-033](../FINDINGS_INDEX.md) | invalidated | [Uniform frac_pos ≤ ½](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_1000000.json) | [pgs_d4_frac_pos_falsification_1000000.json](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_1000000.json) |
| [RH-034](../FINDINGS_INDEX.md) | measured | [Chamber budget empirics](../../pgs-rh-placement-empirics-2026-06/pgs_chamber_budget_summary_1000000.md) | [pgs_chamber_budget_summary_1000000.md](../../pgs-rh-placement-empirics-2026-06/pgs_chamber_budget_summary_1000000.md) |
| [RH-035](../FINDINGS_INDEX.md) | unresolved / dormant draft | [Transfer lemma draft](../../pgs-rh-placement-empirics-2026-06/source_to_spectral_transfer_lemma.md) | Source-first redesign only; not live RH path |
| [RH-040](../FINDINGS_INDEX.md) | hypothesis / quarantined | [Half-scale correspondence](../../18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md) | Not a work target; frame-risk rhyme |
| [RH-071](../FINDINGS_INDEX.md) | measured | [d=4 falsification 10⁷](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json) | [pgs_d4_frac_pos_falsification_10000000.json](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json) |
| [RH-080](../FINDINGS_INDEX.md) | measured | [Lean Placement.lean](../../../lean-4/PGS/Placement.lean) | [lean-4/PGS/Placement.lean](../../../lean-4/PGS/Placement.lean) : [closure roadmap](../../../lean-4/PLACEMENT_FORMALIZATION_ROADMAP.md) M0 to M3 |
| [RH-081](../FINDINGS_INDEX.md) | measured | [Lean placement invariants](../../../lean-4/pgs-rh-placement-invariants.lean) | [lean-4/pgs-rh-placement-invariants.lean](../../../lean-4/pgs-rh-placement-invariants.lean), smoke re-export; roadmap M0/M3.2 |
| [RH-092](../FINDINGS_INDEX.md) | archived | [Off-axis pair carrier](../../12-rh-bridge/README.md) | [12-rh-bridge/docs/off_axis_pair_carrier_lemma_resolution.md](../../12-rh-bridge/README.md) |

**Folder home:** [pgs-rh-placement-empirics-2026-06](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md)

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md)