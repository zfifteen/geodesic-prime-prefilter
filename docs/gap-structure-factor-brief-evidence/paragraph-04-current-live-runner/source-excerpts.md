# Paragraph 04 Source Excerpts

## Source: Live Runner README

Path: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/README.md`

Line evidence:

- `189-207`: states the current outputs and official rungs: 40-bit closure,
  50-bit unresolved, 64-bit closure; downstream audit reports factor found for
  40-bit and 64-bit.

## Source: Inference Rows

Path: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/inference_rows.jsonl`

Line evidence:

- `1`: 40-bit public endpoint class found.
- `2`: 50-bit unresolved by reciprocal carrier misalignment.
- `3`: 64-bit public endpoint class found by mutual certificate closure.

## Source: Audit Results

Path: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/audit_results.csv`

Line evidence:

- `2`: 40-bit `factor_found=true`.
- `3`: 50-bit `factor_found=false`.
- `4`: 64-bit `factor_found=true`.

