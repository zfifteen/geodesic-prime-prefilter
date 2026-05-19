# Self Checklist - Part Two Residue Certificate Probe (Codex)

**Script:** `reciprocal_shadow_residue_certificate_probe_codex.py`  
**Contract:** `../reciprocal_shadow_correct_experiment_design.html`  
**Run date:** 2026-05-19  
**Scope:** Writes are confined to `part-02-codex-performs-grok-audits/` and its `output/` subfolder.

## 12-Item Answers

1. **Generator source after construction contains zero references to p or q values or identifiers.**  
   **Status: PASS.** `certificate()` receives only rows, case label, surface label, and a runtime-log list. It contains no `p`, `q`, or `N` names. `p` and `q` appear in construction/holdout and final membership audit only.

2. **No integer interval, prime stream, or segmented sieve is constructed for inference.**  
   **Status: PASS.** The generator loops over residues `a in range(M)`, where `M` is selected from held-out thread factors. No prime stream, segmented sieve, root walk, or candidate integer interval exists in the certificate path.

3. **M is computed solely from the highest-degree held-out thread factors.**  
   **Status: PASS.** `selected_moduli()` counts factors present in held-out rows and selects the four highest-degree values, with the contract's three-factor fallback if the product exceeds `5_000_000`.

4. **Every admissible residue is produced by conflict-check plus CRT merge.**  
   **Status: PASS.** The only append to the certificate follows per-`r` agreement on `b = (-offset * inverse(a mod r)) mod r` and an incremental CRT merge across the selected moduli.

5. **The identical closure procedure is run on the rotated-offset control.**  
   **Status: PASS.** The same `certificate()` function is used for true, rotated, and deterministic synthetic rows.

6. **Success/falsification numbers are computed only from final membership and rank.**  
   **Status: PASS.** `audit_membership()` computes `p % M` after certificates exist, then records membership and rank. That audit does not feed back into certificate construction.

7. **Natural-ratio surface avoids the 97/100 construction bias.**  
   **Status: PARTIAL / INHERITED SURFACE LIMITATION.** The fixed original 16 cases are inherited and have no low-ratio examples. The four added larger cases have `p/sqrt(N)` equal to approximately `0.50`, `0.40`, `0.30`, and `0.20`.

8. **Certificate cardinality is at most 64 on every passing true-web case.**  
   **Status: PASS.** Every true-web certificate has cardinality `48`.

9. **Runtime log lists arithmetic contributing to admitted residues.**  
   **Status: PASS.** `runtime_residue_crt_log.jsonl` has one record per admitted residue and records selected moduli, per-modulus inverse/residue data, and CRT merge steps. It contains no `N` division or `gcd(N, *)` call.

10. **Rotated and deterministic synthetic controls both executed and reported.**  
    **Status: PASS.** Both controls executed for all 20 cases. Each produced certificate cardinality `0`.

11. **Implementation witness confirms the contract matches the code.**  
    **Status: PASS.** The code implements the residue-certificate mechanism in the frozen contract, with deterministic synthetic controls replacing the earlier random-control wording.

12. **Raw output files exist before interpretation.**  
    **Status: PASS.** `summary.json`, `certificate.jsonl`, `runtime_residue_crt_log.jsonl`, and `summary.md` were written by one script execution before this checklist.

## Overall Assessment

The Part Two implementation is admissible as an independent execution artifact, but the result is `boundary_measurement`. It reproduces Part One: true web emits the 48 coprime residues modulo 210, while both controls emit empty certificates. This is not an accepted factor-residue selector.

**Signed:** Codex (Part Two performer) - contract adherence prioritized over outcome optimism.
