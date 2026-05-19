# Codex Audit - Part One V2 Public Selector

**Experiment lane:** Part One - Grok performs, Codex audits  
**Performer source:** `reciprocal_shadow_v2_public_selector_probe_grok.py`  
**Raw outputs:** `output/summary.json`, `output/certificate.jsonl`, `output/runtime_residue_crt_log.jsonl`, `output/summary.md`  
**Controlling contract:** `../../residue_certificate_v2_public_selector_contract.html`  
**Audit classification:** `invalidated_result`

## Audit Result

Part One is admissible as an implementation of the V2 contract. The measured result invalidates the V2 public ranking hypothesis on the first 20-case surface.

The implementation keeps the V1 certificate layer intact, adds the frozen GWR/deviation ranking layer, runs true/rotated/deterministic synthetic surfaces, and records the required raw artifacts. The result is not positive: true `p % M` is the unique structural winner in `0 / 20` cases. Both controls remain empty at the certificate layer.

## Source Audit Evidence

- `compute_residue_certificate` receives only rows, logs, case label, and surface label. AST inspection found no `p`, `q`, or `N` names inside the V1 certificate generator.
- `extract_gwr_witness` receives only held-out rows and implements the leftmost minimum-divisor witness plus one-neighbor-per-side support window.
- `apply_v2_ranking` receives only the emitted certificate, `M`, GWR data, logs, and case label. It computes `inv_a`, `d_primary`, `dev_primary`, support deviations, `support_score`, structural ranks, and tie sizes without `p`, `q`, `N`, candidate integers, or divisibility gates.
- `build_case` uses `p` and `q` for construction and direct-row holdout. This is allowed by the contract.
- `main` computes `p % M` only after the V1 certificate and V2 ranking fields exist. This is final audit membership only.
- Grep/manual inspection found no candidate interval, prime stream, segmented sieve, root walk, `gcd(candidate, N)`, `N % candidate`, product-closure gate, random control, or threshold not fixed by the contract inside the generation/ranking path.

## Output Audit Evidence

- Cases executed: 20.
- True certificate cardinality: 48 for every case.
- Rotated certificate cardinality: 0 for every case.
- Deterministic synthetic certificate cardinality: 0 for every case.
- Selected modulus factors: `[2, 3, 5, 7]` for every case, giving `M = 210`.
- V2 structural wins by true `p % M`: 0 of 20.
- Minimal structural key tie sizes: 2 or 4 in every case.
- Aggregate classification emitted by the run: `invalidated_result`.
- `certificate.jsonl` contains 960 true-web rows with `dev_primary`, `support_score`, structural rank, structural tie size, final reporting rank, `p_mod_M`, membership, and structural-winner fields.
- `runtime_residue_crt_log.jsonl` contains 1920 entries: 960 V1 CRT records and 960 V2 deviation records.

## Boundaries

The implementation is larger than ideal at 719 lines, but that is an implementation-form issue rather than a leakage issue. The code is self-contained and auditable enough for this Part One record.

The result invalidates only this V2 ranking rule on this frozen 20-case surface. It does not alter the prior V1 boundary measurement and does not make any numeric factor-discovery claim.

## Codex Classification

Part One is accepted as an admissible `invalidated_result`.

The public GWR/deviation score, exactly as frozen, does not isolate the hidden lower-factor residue. It partitions the 48-unit certificate into tied structural minima that never uniquely select `p % M` on the tested surface.
