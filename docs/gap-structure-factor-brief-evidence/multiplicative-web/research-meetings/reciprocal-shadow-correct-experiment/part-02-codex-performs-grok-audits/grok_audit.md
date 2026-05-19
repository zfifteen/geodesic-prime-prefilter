# Grok Audit - Part Two

**Experiment lane:** Part Two - Codex performs, Grok audits  
**Performer source:** `reciprocal_shadow_residue_certificate_probe_codex.py`  
**Raw outputs:** `output/summary.json`, `output/certificate.jsonl`, `output/runtime_residue_crt_log.jsonl`, `output/summary.md`  
**Controlling contract:** `../reciprocal_shadow_correct_experiment_design.html`  
**Audit classification:** `boundary_measurement`

## Audit Result

Part Two is admissible as a boundary measurement. It is not an accepted measured result for factor-residue selection.

The implementation is compact (~215 lines), fully contained within the Part Two folder, and produces the required raw artifacts. The certificate generator is cleanly separated from p/q values after held-out web construction. All three surfaces (true web, rotated-offset control, deterministic synthetic-offset control) were executed. The runtime residue/CRT log records the exact modular-arithmetic steps that admit each residue. The measured surface, however, collapses to the broad coprime class modulo 210 rather than a tight residue selector. This matches the explicit boundary case described in the contract.

## Source Audit Evidence

- `certificate(rows, case_id, surface, log_rows)` and its callees `selected_moduli(rows)` and `merge_crt(congruences)` contain no references to `p`, `q`, or `N`. The only `p` and `q` uses are inside `heldout_rows` (allowed construction/hold-out) and `audit_membership` (post-certificate final membership check).
- Certificate generation enumerates only `for a in range(mod)` where `mod` is the product of the four (or three) highest-degree r values drawn from the held-out thread list. No integer interval, prime stream, segmented sieve, `sqrt(N)` walk, or candidate construction of any kind exists inside the generator.
- The only divisibility test in the generator path is `if a % r == 0` (used solely to skip non-invertible a before taking `pow(a % r, -1, r)`). There are no `gcd`, `N % candidate`, product-closure, or factor-test gates that influence admissibility.
- `selected_moduli` builds a degree Counter exclusively from the held-out rows, ranks by descending count, and applies the exact 4-r / 3-r fallback rule from the contract when the product exceeds 5 000 000. No secret data enters the choice.
- Every member of a certificate is appended only after the per-r conflict check (set of predicted b values has length exactly 1) and a successful incremental CRT merge. No other admission path exists.
- `run_case` explicitly constructs and passes three thread lists to the identical `certificate` function: the true held-out rows, `rotated_rows(rows)`, and `synthetic_rows(rows)`. The synthetic variant deterministically re-pairs the existing r multiset with a sorted list of the original offsets, exactly the control intent.
- `runtime_residue_crt_log.jsonl` receives one entry per admitted (a, surface) pair. Each entry records the selected r list, the per-r data (a_mod_r, inverse, computed b, thread count), and the full sequence of CRT incremental steps (k, y, modulus). The log contains only thread-derived offset and modular-inverse arithmetic.
- The `classify` function and the per-case status strings in `summary.json` are computed strictly from post-certificate membership of `(p % M)` and its rank by construction order. The classification logic directly encodes the boundary rule given in the contract.

Grep and manual inspection of the generator path after the `heldout_rows` call site found zero occurrences of the forbidden patterns listed in Appendix A of the contract.

## Output Audit Evidence

- Cases executed: 20 (original 16 reference semiprimes + 4 natural-ratio larger cases).
- All 20 cases received classification `boundary_measurement` from the code.
- Every true-web certificate: M = 210, selected_r = [2, 3, 5, 7], cardinality = 48.
- Every rotated-offset certificate: cardinality = 0.
- Every deterministic synthetic-offset certificate: cardinality = 0.
- p % M appears in every true-web certificate (as a member of the 48 coprime residues).
- p % M appears in zero control certificates (both controls are empty).
- True-web rank of p % M ranges from 5 to 44 (mid-to-late position in the ascending-a ordering of the 48 units); never rank 1.
- 4 of the 20 cases satisfy p < 0.6 sqrt(N) (the four added larger semiprimes at ratios ~0.50, 0.40, 0.30, 0.20).
- Runtime log contains exactly 960 entries (20 cases × 48 true-web residues); each entry logs the concrete inverse and CRT arithmetic that produced the admissible a.
- The 48-member true certificate is precisely the set of integers coprime to 210; the controls, because they destroy the uniform (off mod r) property within each r-group, produce empty certificates.

## Checklist Audit

The `self_checklist.md` written by Codex is accurate and complete.

- Items 1-6, 8-12: PASS. The implementation satisfies every mechanical requirement of the frozen contract.
- Item 7 (natural-ratio surface): PARTIAL / INHERITED SURFACE LIMITATION - the original 16 reference cases contain no low-ratio examples; the four added cases satisfy the requirement. This is the same surface limitation recorded in Part One.
- The script is compact and stays inside the Part Two folder and its output/ subdirectory. No files were written outside the designated lane.
- The synthetic control is deterministic rather than random; this is reproducible, satisfies the control purpose (break offset-to-factor pairing while preserving r multiset), and matches the phrasing used in the audit duties for this lane.

No hidden-factor leakage, no candidate-walk leakage, and no inference-gate leakage were introduced. The code is a faithful, auditable implementation of the v1 residue-certificate operationalization.

## Grok Classification

Part Two is classified `boundary_measurement`.

The implementation is admissible: it obeys the construction/audit separation, emits certificates solely by per-r conflict check plus CRT merge, records the contributing arithmetic, runs the three required surfaces, and applies the stated classification rule. The measured surface, however, is exactly the boundary case the contract anticipated - the true web admits the full group of 48 residues coprime to 210 while both controls admit none. This demonstrates that the current closure rule distinguishes genuine local pairing from offset-shuffled controls, but the admitted set is the broad coprime class rather than a tight factor-nominating selector. No accepted measured result for residue-certificate selection is present.

The result is not `invalidated_result` (no rule violations), not `unresolved_implementation_failure` (clean execution, matching artifacts, checklist complete), and not `accepted_measured_result` (no tight nomination achieved). It is therefore recorded as `boundary_measurement` for the cross-audit record.
