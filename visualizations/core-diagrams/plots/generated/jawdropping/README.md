# PGS Jaw-Dropping / Buck-Wild Visualizations

Generated 2026-06 as part of the visualizations suite.

## Assets (open these for the full crazy experience)

- **ridge_flight_crazy.gif** (1.5MB): 30-frame animation of "flying through" real PGS gap profiles. Watch the divisor field, Z-ridge, GWR w, and U_□ square references evolve dynamically. Pure motion poetry of the ordered gap interior.

- **pgs_tapestry_crazy.png** (26KB but high-res artistic): Seamless composite "quilt" of dozens of gap profiles. Looks like mathematical Persian rug or cosmic tapestry. Print it huge.

- **square_branch_cosmos.obj** (64KB): 3D point cloud + lines from 2000+ real square branch points (p, offset, cutoff). Violations highlighted conceptually. Import to Blender, add metaballs/spheres for points, scale, light, and 3D print the "PGS cosmos" as a sculpture of the square branch (PROOF.md).

- **pgs_jawdropping_dashboard.html** (4.9MB): Full interactive Plotly multi-view dashboard. 3D nebula + square branch scatter + descriptions. Fly, hover, zoom. The ultimate browser experience combining everything.

- Previous jaw-droppers (from buck_wild script):
  - square_branch_cosmos_3d.png (722KB): 3D galaxy of square branches with red violation supernovae and constellation lines.
  - square_branch_fractal_tree.png (929KB): Recursive fractal tree of the square branch, looks alive.
  - pgs_mandala.png (735KB): Sacred geometry mandala layering ridges, GWR, square offsets.
  - cosmic_nebula_3d.html (4.6MB): Interactive 3D particle universe of gaps (size=avg Z, color=GWR pos).

## How generated
- Real data: square_branch_gap_audit_violations.csv (7477 points) + sympy-generated gaps up to ~7k.
- Tools: matplotlib (profiles, 3D, animations via FuncAnimation + imageio GIF), plotly (interactive 3D/HTML dashboards), PIL (tapestry composite), simple OBJ export for 3D models.
- All 100% PGS-native: divisor-count field τ(n), GWR w selection, DNI Z(n), square branch offsets/violations (PROOF.md), ridges, U_□ refs, residues.

## Ideas for more (go even wilder)
- More animations: fractal tree growth GIF, network evolution over scales.
- VR/AR: export more meshes or use the OBJ in Unity/Unreal with PGS data driving particles.
- Video: import frames/GIFs + the pgs-math-explainer scenes into Flaming Horse for full narrated 4K with voice.
- Physical: 3D print the OBJ (scale in Blender, use SLA for fine points), laser-cut the mandala/tapestry, project the GIF on a dome.
- Generative: use these as seeds for AI image/video (e.g., feed descriptions + data to image models for "PGS as living geometry").
- Integration: symlink or copy key ones to research/11-gap-ridge/ or docs/ for papers; embed dashboard in visualizations/index.html gallery.

These prove the "geometric frameworks" claim visually while staying deterministic and source-first (divisor counts → structure → viz).

Run the scripts again with bigger limits for more data, different colormaps, or add sound-reactive viz if you hook up audio from the explainer.

Enjoy the trip through the divisor field!

## User's Favorites: Enhanced (2026-06 follow-up)

The user specifically loved:
- square_branch_fractal_tree.png
- square_branch_cosmos_3d.png

**New enhanced versions generated:**
- square_branch_fractal_tree_enhanced.png (300 DPI + explanatory legend tying directly to PROOF.md square branch, GWR selection, bounded compression violations)
- square_branch_cosmos_3d_enhanced.png (250 DPI + annotations explaining the 3D geometry of the square branch hypothesis)
- square_branch_cosmos_interactive.html (full Plotly 3D interactive, drag to explore the violations as red points)
- square_branch_favorites_diptych.png (side-by-side print-ready composite)
- square_branch_favorites.html (dedicated standalone gallery page with both images + PGS explanations)

These are now prominently featured in visualizations/index.html under a gold-bordered "Your Favorites" callout.

The visuals remain 100% faithful to the project's square branch data and the Interior Maximizer / GWR theorems.

## Other PGS Fractals (User Request Follow-up)

User especially loved square_branch_fractal_tree.png (the square branch recursive tree).

New PGS fractals generated (in ../fractals/ and growth GIF here):

- gwr_subdivision_fractal.png: General GWR leftmost-min recursion on nested intervals (not limited to τ=3 squares). Binary tree of splits at w; colored by τ(w). The attractor set of all GWR points is a deterministic fractal in the number line.

- ridge_self_similarity_fractal.png: From 11-gap-ridge scale data. Recursive branching of Z-peak (ridge) positions across log scales. Visual self-similarity + left (near-edge) bias of the low-excess structure.

- u_square_utilization_fractal.png: Recursion on the U_□ = (right-w)/(next_square-w) ratio in d=4 chambers (05-state-budget). Low util branches "eat" more of the square room, higher square-phase pressure.

- square_branch_fractal_growth.gif: Animation of the user's favorite tree growing (depth + data points). Violations emerge as red branches as more real square branch data is incorporated.

All strictly from PGS objects (divisor-count field, GWR selection, square branch from PROOF.md, ridge from 11-gap-ridge, U_□ geometry-median from 05-state-budget). Scripts in pgs_other_fractals.py.

These extend the geometric frameworks visually while staying source-first.
