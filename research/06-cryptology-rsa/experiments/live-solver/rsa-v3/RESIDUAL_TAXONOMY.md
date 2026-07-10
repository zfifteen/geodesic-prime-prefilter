# Residual taxonomy (A1 / rsa-v3)

Unresolved is a successful contract outcome when invariants do not close.
Every residual code below may appear in inference outputs.

| Code | Meaning | Required diagnostics |
| --- | --- | --- |
| `unresolved_by_missing_lower_certificate` | No lower chamber-reset certificate at start anchor | step_index, stage, lower_present |
| `unresolved_by_endpoint_chain_boundary` | Walk exhausted lower balance without closure | step_index, stage, steps |
| `unresolved_by_endpoint_chain_cycle` | Repeated anchor in chain walk | step_index, stage, steps |
| `unresolved_by_certificate_pair_not_closed` | Transport/certificates present but no reset or deadline closure | step_index, stage |
| `unresolved_by_reciprocal_carrier_misalignment` | GWR-carrier floor transport bound failed | step_index, stage, carrier fields |
| `unresolved_by_first_tail_misalignment` | First-tail reciprocal proximity failed | step_index, stage, tail fields |
| `unresolved_by_lower_lock_misalignment` | Lower lock dominance failed | step_index, stage, lock fields |
| `unresolved_by_profile_count_mismatch` | Active/unresolved profile counts mismatched | step_index, stage, counts |
| `unresolved_by_gwr_carrier_fields_absent` | Carrier fields required for GWR closure were missing | step_index, stage |
| `unresolved_by_instrumentation_limit` | Large-bit instrumentation hit max_steps or bootstrap limit with no class | step_index, stage, max_steps, bits |

No residual code encodes classical factor information.
