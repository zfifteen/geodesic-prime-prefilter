# Grok Audit - Part Two V2 Public Selector

**Experiment lane:** Part Two - Codex performs, Grok audits  
**Performer source:** `reciprocal_shadow_v2_public_selector_probe_codex.py`  
**Raw outputs:** `output/summary.json`, `output/certificate.jsonl`, `output/runtime_residue_crt_log.jsonl`, `output/summary.md`  
**Controlling contract:** `../../residue_certificate_v2_public_selector_contract.html`  
**Audit classification:** `invalidated_result`

## Audit Result

Part Two is admissible as an implementation of the V2 contract. The measured result invalidates the V2 public ranking hypothesis on the first 20-case surface.

The implementation preserves the V1 certificate layer (conflict-check + CRT), applies the frozen GWR witness extraction and V2 deviation ranking exactly as specified, executes all three control surfaces, and emits the required raw artifacts. The result is falsifying: true `p % M` is the unique structural winner in `0 / 20` cases. Both rotated and deterministic synthetic controls emit empty certificates on every case.

## Source Audit Evidence

- `v1_certificate(rows, ...)` receives only the already-held-out rows, case_id, surface label, and runtime log. It contains no `p`, `q`, or `N` references inside the member-generation loop. p/q appear only in the caller `run_case` for N construction and the post-V2 final membership audit.
- `gwr_witness(rows)` implements Section 6 precisely: sorts held-out rows by offset ascending, selects the first (leftmost) row achieving global `d_min`, records `t_g`, and selects at most the nearest qualifying left and right support rows with divisor_count <= d_min + 2.
- `apply_v2(cert, gwr, ...)` and `deviation(offset, inv_a, m)` implement Section 7 exactly: `inv_a = pow(a, -1, m)`, `d_primary = (t_g * inv_a) % m`, `dev_primary = min(d_primary, m - d_primary)`, per-support `dev_s`, `support_score = sum(dev_s)`, structural key `(dev_primary, support_score)`. The final sort appends `a` only for reporting order. `is_structural_winner` is set only when structural rank 1 and structural tie size == 1.
- `rotated_rows` and `synthetic_rows` are deterministic transformations (cyclic offset shift; factor-signature sort with reassigned sorted offsets). No randomness.
- No candidate intervals, prime streams, sieves, root walks, `gcd`, `N % candidate`, divisibility gates, or product-closure checks appear in the V1 generation or V2 ranking paths. The only `range` is inside `composite_rows` for public held-out web construction (allowed by contract Sections 3-4). All thresholds (RADIUS=300, M_LIMIT) are fixed module constants.
- `selected_moduli` and the per-r conflict check + `crt_merge` reproduce the frozen V1 layer that always yields M=210 and the 48-residue unit group.
- Final `p % M` lookup and `is_p_member` tagging occur only after `apply_v2` returns.

## Output Audit Evidence

- 20 cases executed.
- True certificate: cardinality 48, M=210, selected_r=[2, 3, 5, 7] on every case.
- Rotated control cardinality: 0 on every case.
- Deterministic synthetic control cardinality: 0 on every case.
- `controls_all_empty`: true.
- Structural wins by true `p % M`: 0 of 20.
- Every case reports `min_structural_tie_size` of 2 or 4; `structural_winner_a` is null for all 20; `p_is_unique_structural_winner` is false for all 20.
- `certificate.jsonl` contains 960 true-web rows, each augmented with `a`, `y`, `M`, `dev_primary`, `support_score`, `structural_rank`, `structural_tie_size`, `final_reporting_rank`, `p_mod_M`, `is_p_member`, `is_structural_winner`.
- `runtime_residue_crt_log.jsonl` contains V1 CRT records (inverse, per-r b-values, CRT merge steps) and V2 deviation records (inv_a, d_primary, dev_primary, support_details, support_score, structural_key) for every nominee.
- `summary.json` and `summary.md` report per-case tables and the aggregate `structural_win_count: 0`, `controls_all_empty: true`, `final_classification: "invalidated_result"`.
- Self checklist and execution notes are present and self-consistent.

## Boundaries

The web-construction path (range + sympy factorint to populate divisor_count) is identical in purpose and shape to the prior cross-audited V1 experiment; it supplies the public divisor-count field required by Sections 6-7. It is not an inference engine for the selector.

The measured surface shows that the structural key `(dev_primary, support_score)` never isolates a unique minimum at the true `p % M` residue. Ties of size 2 or 4 always exist at the lowest key; the final `a` reporting tie-break is never required because no case produces a unique structural winner.

The audit makes no proof claims and no factor-discovery claims. It records only implementation fidelity and the measured surface on the contract-specified 20-case set.

## Grok Classification

Part Two is accepted as an admissible `invalidated_result`.

Under the exact V2 contract, the public GWR/deviation ranking rule over the frozen 48-residue V1 certificate produces 0 structural wins against a clean control surface. The hypothesis is falsified on the audited first surface.
