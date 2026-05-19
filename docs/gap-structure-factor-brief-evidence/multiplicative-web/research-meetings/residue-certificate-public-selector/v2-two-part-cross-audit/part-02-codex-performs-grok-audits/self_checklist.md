# Self Checklist - Part Two V2 Public Selector Probe (Codex)

**Script:** `reciprocal_shadow_v2_public_selector_probe_codex.py`  
**Contract:** `../../residue_certificate_v2_public_selector_contract.html`  
**Run date:** 2026-05-19  
**Scope:** Writes are confined to this Part Two folder and its `output/` subfolder.

## 14-Item Answers

1. **No hidden `p` or `q` in certificate generation or ranking.** PASS. `p` and `q` are used only in `heldout_rows`, `run_case` construction, and final post-ranking `p % M` audit.
2. **No inference candidate interval, prime stream, segmented sieve, root walk, or candidate list.** PASS. V1 generation enumerates residues modulo public `M`; V2 ranks only emitted residues.
3. **V1 `M` selection unchanged.** PASS. `selected_moduli()` uses highest-degree held-out thread factors with the frozen product fallback.
4. **V1 members produced only by conflict-check plus CRT.** PASS. `v1_certificate()` appends members only after per-`r` agreement and CRT merge.
5. **GWR witness extraction matches Section 6.** PASS. `gwr_witness()` sorts by offset, selects the first global minimum divisor-count row, and records `t_g`.
6. **Support window matches Section 6.** PASS. At most one qualifying left row and one qualifying right row are selected.
7. **V2 arithmetic uses only public values.** PASS. `apply_v2()` uses `a`, `M`, `t_g`, support offsets, and emitted certificate data.
8. **No candidate integer, divisibility gate, product closure, or `gcd(candidate, N)` in V2 ranking.** PASS. V2 ranking contains modular inverse, multiplication, reduction, and summation only.
9. **True, rotated, and deterministic synthetic controls all execute.** PASS. Each case runs all three surfaces.
10. **Runtime logs contain inverse, multiplication, modular reduction, support score, and ranking key.** PASS. `runtime_residue_crt_log.jsonl` has V1 CRT records and V2 deviation records.
11. **Final audit membership occurs only after certificates and structural scores exist.** PASS. `p_mod` is computed after `apply_v2()`.
12. **Final `a` reporting tie-breaks do not count as accepted structural wins.** PASS. `is_structural_winner` is true only when structural rank is 1 and structural tie size is 1.
13. **Raw outputs exist before interpretation.** PASS. The script wrote `summary.json`, `certificate.jsonl`, `runtime_residue_crt_log.jsonl`, and `summary.md` before this checklist.
14. **Implementation witness confirms code matches this contract.** PASS. This implementation follows the V2 contract as written and reports the falsifying outcome directly.

## Overall Assessment

The Part Two implementation is admissible for audit. It produced `0 / 20` structural wins, controls empty on all cases, and aggregate `invalidated_result`.
