# v02 Ratio Pre-Execution Certification

**Classification:** `certified_for_execution`

Grok certified the following for execution against the stated public corpus under the exact rules in the v02 request document and the Decision Record:

- Public runner: `thread_triangulation_v02_ratio_runner.py`
  - SHA-256: `15be58e3d1fb9e026a76fc67b69ca6c5999ecc01351f65e90e84cc2c6211c465`
- Private batch harness: `run_v02_ratio_toy_corpus.py`
  - SHA-256: `cd2c1eda23261f164f4360a88ad941bc8c5d3d14753a23ed3a2527a20d181d94`
- Public corpus: `cases/toy_corpus.jsonl`
  - SHA-256: `8cce09d3651e8808dc8b9e79cbc46f077e1416205d9d87071b9d360ae1200520`

## Verified

- SHAs on disk match the proposed values exactly.
- `py_compile` state and the described smoke-gate / forbidden-token scan are consistent with the request.
- Public runner receives only `--n` and `--out-dir`; it has zero references to audit pairs, `p/q`, or any private path.
- Ratio derivations are implemented exactly:
  - `RETENTION_DIVISOR = 1024`
  - `THREAD_COUNT_RATIO = 3/8`
  - `DEPTH_RATIO = 5/12`
  - `active_thread_count = ceil((3/8) * public_radius(N).bit_length())`
  - `thread_set = first active_thread_count` entries from the public odd-prime stream
  - `min_depth = ceil((5/12) * active_thread_count)`
  - `max_candidates = ceil(original_space_size(N) / 1024)`
- No `max(...)`, `min(...)`, hardcoded floors/ceilings, fallback paths, or private-conditioned branches are present in the public controls.
- All required manifest fields are emitted.
- The public freeze gate is present and private audit unlock occurs only after a clean public token scan.
- The private harness strictly sequences public runner execution and `public_freeze.log` before canonical membership audit.
- The private harness does not re-rank, re-score, or post-audit filter public candidates.
- The public runner never imports, reads, or receives audit pairs.

## Residual Risks

- The pure-ratio formulas produce low `active_thread_count` / `min_depth` regimes for the smallest toy cases. That is expected formula behavior without floors.
- Recursive CRT enumeration grows with active thread count. The `3/8` ratio keeps the 64-bit surface near 13 threads, but higher-bit runs may hit feasibility limits in the current enumeration tree.
- Zero-candidate outputs remain possible and are reported as unresolved, with no fallback search.
- The public thread stream generator is quadratic in small active thread counts, but that is not a blocker at this scale.

## Certification Close

The artifacts satisfy the v02 source-compliance contract and source-separation boundary. Execution may proceed. No corrections required.
