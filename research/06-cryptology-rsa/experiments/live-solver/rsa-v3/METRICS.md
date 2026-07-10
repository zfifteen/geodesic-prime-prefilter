# Metrics contract (A1 / rsa-v3)

## Summary row fields (every case)

| Field | Meaning |
| --- | --- |
| `case_id` | Public case identifier |
| `bits` | Public modulus bit size |
| `N` | Public modulus |
| `center` | `isqrt(N)` orientation only |
| `algorithm_version` | Resolver algorithm version |
| `git_commit` | Git commit or `unknown` |
| `closure_status` | Endpoint class status or residual code |
| `rule_id` | Inference rule identifier |
| `lower_certificate_present` | Bool |
| `upper_certificate_present` | Bool |
| `corrected_lower_certificate_present` | Bool |
| `endpoint_class_emitted` | Bool |
| `residual_code` | Residual code when unresolved, else null |
| `elapsed_ms` | Measured wall time |

## Aggregate measured metrics (report only)

- resolution rate by bit length (measured only; not a pass threshold)
- residual histogram
- certificate verify pass rate
- wall time and peak memory notes

## Residual rows

Every unresolved case writes a residual row with:

- `case_id`, `bits`, `N`
- `residual_code`
- `step_index`
- `stage`
- `lower_certificate_present`, `upper_certificate_present`
- `diagnostics` object
