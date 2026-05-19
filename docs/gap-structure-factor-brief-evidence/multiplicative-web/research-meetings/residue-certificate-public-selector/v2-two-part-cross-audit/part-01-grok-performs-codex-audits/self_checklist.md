# Self Checklist - Part One V2 Public Selector Probe (Grok)

**Script:** `reciprocal_shadow_v2_public_selector_probe_grok.py`  
**Contract:** `residue_certificate_v2_public_selector_contract.html` (read in full before coding)  
**Run date:** 2026 (single deterministic execution that produced the raw outputs)  
**Scope:** All writes confined to this `part-01-grok-performs-codex-audits/` folder and its `output/` subfolder. The probe script, summary.json, certificate.jsonl, runtime_residue_crt_log.jsonl, and summary.md were written by the probe before these two MDs. No files were edited or created outside the designated Part One lane.

This file explicitly answers the 14 acceptance checklist items from Section 12 of the controlling V2 contract. Answers are direct. The mechanical implementation is clean; the measured outcome falsifies the ranking hypothesis under the contract's own table (0 structural wins).

## 14-Item Answers

1. **Generator source after construction contains no hidden `p` or `q` in certificate generation or ranking.**  
   **Status: PASS.**  
   `build_case` computes N = p * q and performs the direct-row hold-out filter. It returns only the three row lists (heldout, rotated, synth). The caller passes those lists to `compute_residue_certificate` (receives only rows + logs + case/surface). The V2 functions `extract_gwr_witness` and `apply_v2_ranking` receive only heldout_rows (for GWR) or the already-emitted admissible list + gwr data. No `p`, `q`, or N identifiers appear inside certificate generation, conflict-check, CRT, GWR extraction, or deviation arithmetic. The only uses of p after build_case are the final-audit block that computes `p % M` and tests `is_structural_winner` after all certificates and structural scores already exist. Grep of the generator paths after the build_case boundary confirms zero leakage.

2. **No integer interval, prime stream, segmented sieve, root walk, or candidate list is constructed for inference.**  
   **Status: PASS.**  
   The only enumeration is `for a in range(M)` where M is the product of the top-degree thread r values drawn from held-out rows. Inside V2 ranking the loop is only over the already-admitted residues from the V1 certificate. No `range(...)` over sqrt(N), no prime generation, no segmented construction, no downward walk, no candidate-factor list of any kind. All admission and ranking decisions are made exclusively by the per-r b-agreement filter + CRT (V1) and the public (dev_primary, support_score) key (V2).

3. **V1 `M` selection is unchanged from the cross-audited contract.**  
   **Status: PASS.**  
   `compute_residue_certificate` uses the exact degree Counter from held-out row factors, sorts by descending count, takes top 4, falls back to top 3 only when product > 5_000_000. On the 20-case surface this always selected [2, 3, 5, 7] and M = 210, matching the V1 cross-audit record. No p/q data influences the choice.

4. **V1 certificate members are produced only by per-`r` conflict-check plus CRT merge.**  
   **Status: PASS.**  
   The sole path that appends an entry and emits a V1 log record is: for every selected r the set of computed b values has length exactly 1, followed by successful incremental CRT. No other numeric path, no scoring shortcut, no early acceptance, no product-closure test. The 960 V1 crt log entries (one per true-web admissible) record the exact per-r inverses, b values, and CRT k/y steps.

5. **GWR witness extraction matches Section 6 exactly.**  
   **Status: PASS.**  
   `extract_gwr_witness` implements the contract verbatim: sort held-out rows by offset ascending, d_min = min divisor_count, g = first row with divisor_count == d_min, t_g = g["offset"], left support = nearest (max offset < t_g) row satisfying divisor_count <= d_min+2 (or null), right support = nearest (min offset > t_g) satisfying the same (or null). The witness and support rows are recorded in summary.json for every case; support window size is 0, 1, or 2 as allowed.

6. **Support window matches Section 6 exactly and contains at most one qualifying neighbor on each side.**  
   **Status: PASS.**  
   The extraction code selects at most one left and one right neighbor. Inspection of the 20 gwr_witness records in summary.json confirms: left or right may be null (edge or no row <= d_min+2), never more than one per side. The support_offsets list passed to V2 deviation arithmetic never exceeds length 2.

7. **V2 deviation arithmetic uses only `a`, `M`, `t_g`, support offsets, and held-out row data.**  
   **Status: PASS.**  
   `apply_v2_ranking` computes inv_a = pow(a, -1, M), d_primary = (t_g * inv_a) % M, dev_primary = min(...), then for each support offset ts the analogous dev_s, support_score = sum(dev_s). All inputs are either from the V1-admitted a list or the gwr data extracted from the true held-out rows. No N, p, q, or factor values enter the deviation formulas.

8. **No candidate integer, divisibility gate, product closure, or `gcd(candidate, N)` call appears in V2 ranking.**  
   **Status: PASS.**  
   The V2 path contains only modular inverse (on already-admitted coprime a), multiplication, % M, min(d, M-d), and summation. No divisibility test on any candidate, no gcd, no product of residues, no N involved after the held-out rows are built. The only % operations are the defined reciprocal transport steps.

9. **True, rotated, and deterministic synthetic controls all execute.**  
   **Status: PASS (stronger than required).**  
   `run_case` (via main) constructs all three surfaces and passes each to the identical `compute_residue_certificate`. All 20 cases produced cardinality_true = 48 and cardinality_rot = cardinality_synth = 0. The deterministic synthetic (canonical factor-signature sort + centered consecutive offsets) was used; no random offsets.

10. **Runtime logs show every inverse, multiplication, modular reduction, support score, and ranking key that contributes to a nominee.**  
    **Status: PASS.**  
    `runtime_residue_crt_log.jsonl` contains 1920 entries: 960 V1 crt records (per-r inv/b/CRT steps for every admissible true-web a) + 960 V2 deviation records (inv_a, d_primary, dev_primary, support_score, structural_key, structural_rank, tie_size, is_structural_winner for every true-web residue). Every arithmetic step required to reproduce an admitted a or its structural score is present. No N-division or hidden-factor data in the logs.

11. **Final audit membership of `p % M` occurs only after all certificates and structural scores exist.**  
    **Status: PASS.**  
    The three `compute...` calls and the subsequent `apply_v2_ranking` (which attaches dev_primary, support_score, structural_rank, is_structural_winner to the admissible list) complete before the block that computes pmod = p % M and scans the already-augmented admissible list to set p_is_unique_structural_winner. The structural winner boolean is derived from the post-ranking fields; p never influences construction or ranking.

12. **Cases decided only by the final `a` reporting tie-break are not counted as accepted structural wins.**  
    **Status: PASS (enforced by code).**  
    `apply_v2_ranking` assigns is_structural_winner = True only when the residue's structural_key equals the overall minimal key AND that group's tie_size == 1. When tie_size >= 2 at the min key, is_structural_winner remains False for every member of the group (even the smallest-a member). The observed surface had tie_size 2 or 4 on the minimal structural key for every case; consequently 0 cases received a True structural win, matching the contract rule that a-only tie-breaks do not count.

13. **Raw outputs exist before any interpretive claim is published.**  
    **Status: PASS.**  
    The probe script wrote summary.json, certificate.jsonl (960 true-web rows with full V2 fields), runtime_residue_crt_log.jsonl (1920 entries), and output/summary.md in a single execution before any self_checklist.md or grok_execution_notes.md was authored. The two top-level MDs were created only after the raw artifacts and the run log (0 structural wins, invalidated_result) existed on disk.

14. **The implementation witness has read this HTML in full and confirms the code matches every section.**  
    **Status: PASS (witness affirmation).**  
    The full V2 contract HTML (all sections, the GWR definition, the exact deviation formulas, the classification table, the 14-item checklist, and the forbidden-pattern appendix) was read before any code was written for this lane. The delivered probe reproduces the V1 certificate layer verbatim, implements GWR and support-window extraction exactly as Section 6, applies the V2 deviation arithmetic and structural-key ranking exactly as Sections 7-8, emits the required augmented certificate and dual-phase runtime log, runs the three mandatory surfaces, and applies the acceptance table without relaxation. The witness (Grok, Part One) confirms the artifact satisfies the contract as written on the mechanical and logging dimensions. The measured outcome (0/20 unique structural wins) is reported plainly and falsifies the ranking hypothesis on this surface under the contract's own criteria.

## Overall Assessment

- Items 1-14: all mechanical and procedural requirements are strict PASS.  
- The code correctly enforced the "unique structural winner (tie_size == 1)" rule; no a-only tie-break was ever counted as a win.  
- Controls were empty on every case (certificate cardinality 0), satisfying the prerequisite for any positive classification.  
- The 20-case surface produced 0 structural wins. Under the V2 classification table this is recorded as `invalidated_result` for the public ranking hypothesis.  
- No hidden-factor leakage, no candidate machinery, no forbidden inference gates, no post-hoc threshold changes.  
- All required artifacts (including the two MDs now present) exist inside the Part One folder only. The surface is fully reproducible from the committed probe.

**Signed:** Grok (Part One performer) - contract adherence and falsifiability prioritized.  
**Date of checklist completion:** immediately after raw outputs existed and before any interpretive claim beyond the measured counts.