# Geometric Aspects of Prime Gap Structure (PGS)

**Note for the project (2026-06-02):** The user has not previously deeply contemplated geometric aspects of the work. This note inventories the latent and explicit geometric elements that already exist in the artifacts, in response to the direct question. It stays within PGS-native objects (divisor-count field, ordered gap interior, GWR w, DNI scores E/Z, square phase) while noting where geometric language, diagrams, constructions, and visualizations have emerged.

## 1. The Fundamental 1D Row/Profile (Observable Geometric Object)
From docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md:

The gap is presented explicitly as a linear "row":

```
23 | 24 25 26 27 28 | 29
number:        24  25  26  27  28
divisor count:  8   3   4   4   6
```

- This is a 1D geometric diagram on the number line.
- Heights/labels = τ(n) form a step profile or bar sequence.
- GWR is the geometric "first (leftmost) minimum" along this row.
- The "selected composite" w is a distinguished point in the geometric interval.

This is the simplest and most direct geometric representation. It turns the abstract ordered set into a visible line with a marked valley.

The document emphasizes that width alone (just the distance 6) "throws away the arithmetic inside"; the row makes the interior structure visible geometrically.

## 2. Score Landscapes and the "Gap Ridge" (Topographic Geometry)
In research/11-gap-ridge/ (and related DNI work):

The raw composite Z(n) = n^{1 - d(n)/2} (or equivalently -E(n)) is treated as a function/curve defined along the 1D gap interval (the segment from p+1 to q-1).

Key measured phenomenon: instead of a central peak, the high-Z (low-excess) structure forms a **"near-edge ridge"**.

- "Ridge" is topographic language: an elevated region or crest in the score landscape.
- Explicitly: the gap-local raw-Z maximum is near-edge (often distance 2 from the left prime), not midpoint.
- Carried predominantly by d(n)=4 composites.
- There are 2D/3D plots, SVG figures ("representative prime-gap slice: the raw-Z ridge rises near the boundary"), residue-conditioned "ridge orientation".
- "Gap ridge (low E near endpoints)" appears in cryptology probes as a structural feature.

This is geometric modeling of the divisor-normalized score as a 1D terrain with ridge morphology, edge effects, and orientation.

Docs like `docs/dni_gap_ridge.md`, `docs/gap_ridge/raw_composite_z_gap_edge.md`, output SVGs, and scripts for plots (raw_z_gap_edge_plots.py, insight_probes.py) formalize and visualize this.

The "ridge" is a geometric framework for describing where the GWR-relevant low-divisor structure concentrates.

## 3. The Square U_□ / Utilization Construction (Explicit Geometric Diagram + Reference)
In research/05-state-budget/ (gwr_phase_budget_hidden_state_probe.py, state_budget_divisor_carrier_sweep.py, related tests and docs):

For d=4 chambers (where the next minimum after current is 4):

- Given GWR winner w in the current chamber.
- next_square_root = nextprime(⌊√w⌋)  (the prime whose square is the next relevant square reference after w)
- next_square = (next_square_root)^2
- square_phase_utilization = (current chamber right prime - w) / (next_square - w)

This is a normalized fractional distance: the "utilization" or how far the current chamber's right boundary has "eaten into" the geometric room from w to the next prime square.

U_□ denotes this square-referenced interval or diagram.

Then:
- Group by "geometry cells": tuples of (carrier_family, winner_offset, first_open_offset).
- Within each cell, take the median of the utilization values.
- Split: d4_low if utilization < median in cell, d4_high otherwise.

This is a full geometric construction:
- Reference object: the prime square geometrically tied to w via sqrt.
- Measurement: linear fraction along the number line segment [w, next_square].
- Classification: median split in a geometric/parameter cell ( "geometry-median" ).

It is used for phase budgeting, hidden state in d=4 chambers, square-phase utilization as a candidate measure in predictions/carrier work.

See `gwr_phase_budget_hidden_state_probe.py` (compute and assign), tests, and `docs/phase_budget_hidden_state_probe_findings.md`.

This is the most developed *native geometric tool* in the active research surface. It directly uses geometric position relative to squares (tying to the square branch in PROOF.md).

## 4. Visual and Interactive Geometry (Rendering Layer)
- **Row and profile diagrams**: Explicit in explanatory docs; extended in ridge plots (edge-distance histograms, score slices).
- **Apps**:
  - `visualizations/apps/prime-pattern-plot-generator/index.html`: Interactive plotter coloring primes, squares (yellow), cubes, even/odd semiprimes, higher tau — a geometric number-line visualization directly relevant to divisor classes and GWR (low-tau points).
  - `visualizations/apps/prime-gap-structure-interactive-mockup/index.html`: Mockup for gap structure (likely rows/profiles/scores).
- **Output artifacts**: Dozens of .png, .svg in research/*/output/ (decoupling sweeps, ratio vs scale on log axes — geometric scaling; ridge profiles, residue wheels, 2D/3D ridge plots).
- **visualizations/pgs-math-explainer/**: Multi-scene narrated video with synced visuals — geometric storytelling of the arithmetic.
- **Assets**: hero images, candidate plots in visualizations/conceptual/.

These are not decorative; they render the 1D row, score landscapes, and class-colored points on the line.

## 5. Other Mentions and Aspirational Language
- Original promotion (X post): "deterministic invariants and **geometric frameworks** for prime gap interiors that go far beyond the Riemann Hypothesis."
  - This language is not heavily substantiated in core docs yet but aligns with the row + ridge + U_□ above.
- Status-map and research notes: "local geometry", "chamber reset mechanics, endpoint determinacy, boundary-drop behavior, and related local geometry", "chamber geometry" (in RH-bridge context, now archived).
- "Gap ridges" as structural features.
- Square branch in PROOF.md: explicit handling of w = r², distances to P(r²), bounds involving squares — geometric objects (positions of squares on the line).
- Multiplicative aspects of DNI (powers, logs) have natural geometric readings (similarity, scaling, hyperbolic if embedded).

"Zero geometry" appears in downstream RH language but is distinguished from the integer source.

## 6. Relation to Recent Thread ( @materion )
@materion's geometric/diagrammatic thinking (gnomons for squares from odds, fractional divisions generating sqrts, "draw little arrows") directly resonates with:
- Odd τ ⇔ squares (geometric objects).
- The square U_□ construction (referencing squares geometrically).
- The row/profile as a diagram.
- The ridge as a geometric shape in the score landscape.

His question about 5 (next after 3 for p^4 = square of square) and "prime related gaps" with powers is probing exactly the geometric extension of these structures.

The computations in this experiment folder (standard + mixed power gaps) show the min-τ restrictions persist even when geometric power objects are included as generators.

## Status and Opportunities
- **Strongest geometric aspects today**: The row/profile (explanatory), the ridge landscape (research/11-gap-ridge with plots and analysis), and the square U_□ utilization + geometry-median (research/05-state-budget, used in predictions).
- These are geometric *descriptions and tools* built on top of the arithmetic core (ordered divisor-count field, GWR min selection, DNI coordinates).
- Core theorems (PROOF.md) are proved arithmetically (comparisons, lemmas on earlier/later integers, finite bases) without needing geometric axioms, but the objects (intervals on the line, positions, fractions to squares) are inherently geometric and have been exploited for visualization and derived measures.
- **Not yet**: Full formal geometric theorems (e.g., "the ridge is a curve with curvature bound X"), embeddings into higher geometry, or diagrams as primary proof objects. The source order remains "divisor counts → ... → zeta compression".
- **Opportunities** (if desired):
  - Produce more canonical diagrams (e.g., standardized row + score overlay + U_□ square reference for a gap).
  - Strengthen the ridge as a geometric invariant (location statistics, residue modulation as directional properties).
  - Develop the U_□ as a diagram with its own lemmas.
  - Interactive tools that let one "draw" the row, mark w, overlay the next square, compute utilization live.
  - Tie more explicitly to geometric number theory intuitions (while staying deterministic/PGS-first).
  - In the math-explainer or new HTML docs, use geometric language and figures to convey the row → GWR → ridge → square phase story.

This inventory shows the work already has geometric "hooks" that someone with @materion's eye naturally reaches for. They are not the primary engine (arithmetic source is), but they are real, documented in specific folders, and could be amplified without leaving the PGS frame.

**Recommended next reads for the user**:
- docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md (the row)
- research/11-gap-ridge/docs/dni_gap_ridge.md and output SVGs (the ridge)
- research/05-state-budget/scripts/gwr_phase_budget_hidden_state_probe.py (the U_□ computation and geometry-median)
- The visualizations/apps/ HTML files (interactive geometry)
- research/11-gap-ridge/README.md and docs/ for the full ridge chapter

The recent experiment artifacts (this folder) already connect the geometric interests of an external interlocutor to these elements.

If the user wants a dedicated "geometric aspects" chapter, more plots, or to prototype a diagram for a specific gap + U_□, that can be executed immediately.
