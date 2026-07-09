# Layer 4: Placement geometry

**Status mix:** `proved`, `measured`, `hypothesis`, `unresolved`, `invalidated`  
**Proves RH?** No (partial progress toward source-to-spectral target)

Chamber invariants, d=4 carrier geometry, empirics, and the draft source-to-spectral
transfer lemma. This layer asks: **where** does the GWR witness sit inside its gap,
and can that geometry constrain spectral placement?

**Canonical folder:** [pgs-rh-placement-empirics-2026-06](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md)

---

## Deferred scan paths (boundary text)

| Path | Why deferred | Does not prove |
|------|--------------|----------------|
| `pgs_rh_bridge_placement_focus_prompt.md` | Internal research prompt | Any placement theorem |
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
| Resonance | Primorial remainder zeros at $w$ | links to [RH-005](../FINDINGS_INDEX.md) twin termination |
| Half-scale rhyme | $\tfrac12$ in $C(q)$ vs $\operatorname{Re}(s)=\tfrac12$ | [RH-040](../FINDINGS_INDEX.md) hypothesis only |

Uniform $frac\_pos\le\tfrac12$ was **falsified** ([RH-033](../FINDINGS_INDEX.md)): 8,505
counterexamples at $10^6$.

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
| [RH-035](../FINDINGS_INDEX.md) | unresolved | [Source-to-spectral transfer lemma](../../pgs-rh-placement-empirics-2026-06/source_to_spectral_transfer_lemma.md) | [source_to_spectral_transfer_lemma.md](../../pgs-rh-placement-empirics-2026-06/source_to_spectral_transfer_lemma.md) |
| [RH-040](../FINDINGS_INDEX.md) | hypothesis | [Half-scale correspondence](../../18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md) | [18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md](../../18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md) |
| [RH-071](../FINDINGS_INDEX.md) | measured | [d=4 falsification 10⁷](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json) | [pgs_d4_frac_pos_falsification_10000000.json](../../pgs-rh-placement-empirics-2026-06/pgs_d4_frac_pos_falsification_10000000.json) |
| [RH-080](../FINDINGS_INDEX.md) | measured | [Lean Placement.lean](../../../lean-4/PGS/Placement.lean) | [lean-4/PGS/Placement.lean](../../../lean-4/PGS/Placement.lean) : [closure roadmap](../../../lean-4/PLACEMENT_FORMALIZATION_ROADMAP.md) M0 to M3 |
| [RH-081](../FINDINGS_INDEX.md) | measured | [Lean placement invariants](../../../lean-4/pgs-rh-placement-invariants.lean) | [lean-4/pgs-rh-placement-invariants.lean](../../../lean-4/pgs-rh-placement-invariants.lean), smoke re-export; roadmap M0/M3.2 |
| [RH-092](../FINDINGS_INDEX.md) | archived | [Off-axis pair carrier](../../12-rh-bridge/README.md) | [12-rh-bridge/docs/off_axis_pair_carrier_lemma_resolution.md](../../12-rh-bridge/README.md) |

**Folder home:** [pgs-rh-placement-empirics-2026-06](../../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md)

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md)