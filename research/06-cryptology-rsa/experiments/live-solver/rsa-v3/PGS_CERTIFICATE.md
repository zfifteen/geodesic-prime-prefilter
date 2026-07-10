# Structural certificate contract (v3)

Schema id: `pgs_structural_certificate_v3`

## Chamber-reset certificate fields (embedded)

Each side certificate includes:

- `anchor`, `reset_endpoint`, `gap_offset`, `candidate_bound`
- `active_count`, `resolved_count`, `unresolved_count`
- `closed_offsets_before_q`
- `carrier_w`, `carrier_d`
- `lock_carrier_offset`, `lock_carrier_d`
- `lower_d_threat_offset`
- `tail_after_reset_offsets`
- `reset_deadline_value`, `reset_deadline_margin`, `reset_signature`

## Structural package fields

- `schema`, `algorithm_version`, `rule_id`, `git_commit`
- `case_id`, `bits`, `N`
- `center`, `step_index`
- `closure_status` (endpoint class status only on resolved packages)
- `endpoint_class` with `lower`, `upper` public endpoints
- `lower_certificate`, `upper_certificate`, optional `corrected_lower_certificate`
- `transport` with oriented coordinate and floor images
- `gwr_carrier_closure` predicate results
- `content_hash` (SHA-256 over canonical JSON without the hash field)

## Forbidden fields

Public certificates and endpoint-class records must not contain:

- audit labels
- factor flags
- confidence scores
- private factors `p` / `q`
