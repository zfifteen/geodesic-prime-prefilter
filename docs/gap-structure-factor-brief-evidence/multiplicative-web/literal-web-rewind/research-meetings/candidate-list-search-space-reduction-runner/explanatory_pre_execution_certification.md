# Explanatory Amendment Pre-Execution Certification

Status:

```text
certified_with_required_corrections
```

Grok certified the amended v01.1 runner source for execution under the frozen
explanatory evidence amendment contract, subject to one required correction
detailed below.

Certified source (pre-correction SHA):

`thread_triangulation_v01_1_runner.py`

Source SHA-256 (as reviewed):

`812de62285df1c24e0d9cde6f8a4298c89aa2fa2bd526020ec53c330147e693e`

Public corpus (unchanged):

`cases/toy_corpus.jsonl`

Corpus SHA-256 (baseline, identical to v01 campaign):

`8cce09d3651e8808dc8b9e79cbc46f077e1416205d9d87071b9d360ae1200520`

## Exact Compliance Verified By Grok

- The source compiles cleanly (`python3 -m py_compile` succeeds).
- The private-token scan returns false for every token in the request list and for the full `private_token_labels()` set (identical to certified v01): p, q, CASE, known_factor, factor_distance, exact_factor_rank, target_distance, private_distance, gcd, factorint, isprime, nextprime, sqrt, random. The splitting defense in `private_token_labels()` is unchanged from v01.
- The seven required public manifest fields are present with exact names and semantics per the amendment contract table:
  - `pre_cap_qualified_count`
  - `max_observed_triangulation_depth`
  - `depth_counts_pre_cap`
  - `cap_active`
  - `emitted_depth_counts`
  - `cutoff_triangulation_depth`
  - `pre_cap_to_emitted_ratio`
- All seven fields are computed exclusively inside `nominate_with_explanatory_fields` (public path) from the `candidates` dict populated by `extend_assignments`, using only N + the locked public constants THREAD_SET, MIN_DEPTH, MAX_CANDIDATES. No hidden-factor values, no post-freeze re-processing, no private paths.
- The code that constructs distances, depths, and scores (`extend_assignments`, `add_candidate`, `thread_profile`, CRT helpers, scoring key) is textually identical to the certified v01 runner. The truncation `sorted(... )[:MAX_CANDIDATES]` for the emitted rows is equivalent. Therefore the `public_output.jsonl` content (row schema, ordering, values) for any given N is guaranteed identical to the v01 artifact; only the manifest gains the seven new keys.
- Original v01 manifest keys are all still emitted with unchanged values (N, N_bits, policy, thread_set, min_depth, max_candidates, public_radius, original_space_*, emitted_count, candidate_reduction_*, reduction_status, source_sha256, score_key, elapsed_seconds). The seven new fields are appended via `manifest.update(explanatory_fields)` before the sorted JSON write.
- The PUBLIC_FREEZE_RECORD gate is extended exactly as required: clean token scan still blocks before any output; both output files are hashed and printed; the seven new field values are printed explicitly; the full manifest (now containing the new fields) is echoed at the end; `PRIVATE_AUDIT_UNLOCKED: true` appears only after the gate.
- No new command-line flags, environment variables, config files, or runtime inputs were added. The runner remains strictly `--n` + `--out-dir`.
- The runner never opens the toy corpus, never reads labels, never accepts or uses private factors, never invokes any checker. All arithmetic remains public CRT modulus-link construction on thread residues of N only.

## Required Correction (One-Line, Public Only)

The source contains a copy-paste remnant in `main()` (line 269):

```python
public_command = f"python3 thread_triangulation_v01_runner.py --n {args.n} --out-dir {args.out_dir}"
```

This causes the PUBLIC_FREEZE_RECORD to print an inaccurate `public_command` value (naming the v01 file instead of the actual v01.1 runner) while the `source_sha256` printed in the same gate is the correct v01.1 hash. The gate record is therefore internally inconsistent on the invocation command.

**Correction:** Change the string literal to reference the actual filename (`thread_triangulation_v01_1_runner.py`), or (preferred) compute it dynamically from `__file__` or `sys.argv[0]` so the gate is self-describing for any future rename.

This change:
- touches only a print-formatting literal,
- does not alter any of the seven explanatory fields,
- does not alter the emitted `public_output.jsonl` rows or ordering,
- does not introduce any private tokens or private computation,
- does not change behavior or timing of the nomination logic in any material way.

After the one-line edit, recompute the source SHA-256, re-run the identical private-token scan (will remain clean), and record the new SHA in the execution log. The corrected source then satisfies `certified_for_execution` under this amendment contract.

## Grok Residual Risks

The remaining risks are exactly those stated in the frozen amendment contract and its parent design contract:

- Pre-freeze oracle influence on the choice of the locked v01 parameters (THREAD_SET of 12 threads, MIN_DEPTH=5, MAX_CANDIDATES=512). These remain public, frozen, and non-adjustable without a new contract version + fresh corpus.
- Cross-session smuggling of private measurements into the design conversation (mitigated by the requirement that this certification precede any execution of the amended runner).
- Future temptation to enlarge the thread set, lower min_depth, or raise the cap on the same toy corpus after seeing explanatory surfaces. Such a change would require a new contract version and would invalidate direct comparison to the 3/10 v01 baseline.
- The explanatory fields describe only the public shape of the filter output (filter density, cap saturation, depth distribution, scale pressure). They do not and must not be used to explain why any individual missed N's true factor distance failed to qualify.

No new risks are introduced by the v01.1 implementation itself. The amendment adds only public aggregates derived before the PUBLIC_FREEZE_RECORD gate.

No experiment was executed and no output artifacts were generated or inspected during this certification. The determination rests solely on static source inspection, compile, token scan, SHA verification, and direct comparison against the two frozen contracts (design_contract.html and explanatory_evidence_amendment_contract.html).

## Contract References

- Explanatory amendment contract: `explanatory_evidence_amendment_contract.html` (FROZEN, v01.1)
- Parent design contract: `design_contract.html` (FROZEN, v01)
- Certification request: `explanatory_certification_request.md`
- Baseline v01 certification: `pre_execution_certification.md` (for the original runner SHA `dd1b0d9f1d69f25c845f2812214da92187f4e3750609b1b94963934d3fd03878`)
