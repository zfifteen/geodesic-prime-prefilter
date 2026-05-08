# PGSMD Next Experiments

## Strongest Current Direction

The next experiments should test whether the recursive transported ledger and
the inverse-word exclusion surface are two projections of the same public
certificate object:

```text
PGSPG certificate
-> ordered commitment story
-> reciprocal transport
-> induced opposite certificate
-> recursive lag-2 / lag-3 grammar projection
-> exclusion, survivor, or unresolved
```

The official decomposer remains unresolved. These experiments are sidecars.
They must not mutate `output/inference_rows.jsonl` or select factors.

## Experiment 1: Certificate Commitment Story Rows

### Purpose

Materialize the ordered public provenance currently missing from
`PGSCertificate`.

The current field `closed_offsets_before_q` says which offsets are closed. It
does not say which public event closes or dominates each interval. This
experiment records that story without using it as resolver logic.

### Inputs

```text
N
source_anchor
PGSPG certificate at source_anchor
closed_offsets_before_q
carrier_w
lock_carrier_offset
lock_carrier_d
reset_endpoint
lower_d_threat_offset
tail_after_reset_offsets
reset_deadline_value
```

### Output Rows

Write:

```text
output/certificate_commitment_story/story_rows.jsonl
output/certificate_commitment_story/summary.json
```

Each event row:

```text
case_id
source_anchor
event_index
event_kind = closed_offset | carrier_lock | reset | lower_threat | tail | deadline
event_offset
event_value
carrier_d_at_event
lock_carrier_d
dominates_offset_lo
dominates_offset_hi
reduced_state_before
reduced_state_after
rule_id = certificate_commitment_story_v1
```

### Test

For every certificate row already emitted by the runner, the story must
reconstruct:

```text
closed_offsets_before_q
carrier_w
reset_endpoint
reset_deadline_value
```

If the reconstruction fails, the story encoding is invalid.

### Status

This is a public provenance surface, not an invariant.

## Experiment 2: Transported Commitment Story Ledger

### Purpose

Test whether ledger prefix/suffix elimination can be explained as an ordered
story conflict rather than as interval membership alone.

### Inputs

Use Experiment 1 story rows plus existing fields from:

```text
output/transported_exclusion_debt/debt_rows.jsonl
output/transported_exclusion_debt/recursive_rows.jsonl
```

### Comparison

For each source certificate `C` and induced opposite certificate `C'`:

```text
transport C commitment events through floor(N / event_value)
locate C'.carrier_w, C'.reset_endpoint, C'.lower_threat, C'.tail in the transported zones
detect whether C' rewrites a previously committed source event with non-increasing lock_carrier_d
```

### Output Rows

Write:

```text
output/transported_commitment_story_ledger/ledger_rows.jsonl
output/transported_commitment_story_ledger/summary.json
```

Required fields:

```text
case_id
recursion_depth
source_anchor
induced_anchor
source_event_kind
source_event_value
source_transport_image
induced_event_kind
induced_event_value
transported_zone = prefix | suffix | outside
lock_carrier_d_relation = lower | equal | higher | missing
story_rewrite
ledger_prefix_elimination
ledger_suffix_elimination
ledger_recursive_cycle_state
ledger_recursive_survivor
rule_id = transported_commitment_story_ledger_v1
```

### Falsification

The story ledger must reproduce the existing recursive ledger counts:

```text
row_count = 512
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
```

Any divergence must be explained by a named story field. If the divergence is
caused by wider traversal, endpoint budget changes, or missing public fields,
the experiment fails.

### Status

This tests whether the ledger predicates have public ordered provenance. It
does not prove them.

## Experiment 3: Commitment Story To Lag-2 / Lag-3 Projection

### Purpose

Test whether the inverse-word exclusion result is the reduced grammar
projection of transported commitment stories.

### Inputs

```text
certificate_commitment_story rows
grammar_recursive_target_catalog rows
fresh_rsa_challenge_recursive_surface rows
grammar_inverse_word_exclusion rows
```

### Projection

For every certificate story, derive:

```text
lag2_reduced_signature
lag3_reduced_signature
lag23_reduced_signature
recursive_reduced_signature
```

Use the exact orientation convention from `grammar_recursive_target_catalog.py`:

```text
lag23 = outward_lag3 | outward_lag2 | inward_lag2 | inward_lag3
```

### Output Rows

Write:

```text
output/commitment_story_word_projection/projection_rows.jsonl
output/commitment_story_word_projection/summary.json
```

Required summary counts:

```text
projected_lag2_hit_count
projected_lag3_hit_count
projected_lag23_collision_count
projected_recursive_reduced_collision_count
component_sharing_word_exclusion_count
```

### Falsification

On the existing solved surfaces, the projection must preserve:

```text
global lag-2 + lag-3 ordered word hits = 0
fresh RSA-100 lag-2 + lag-3 ordered word hits = 0
```

If the commitment-story projection creates ordered-word collisions where the
existing inverse-word probe has zero, the projection is wrong.

### Status

This is the bridge experiment. It tests whether commitment stories and
recursive words are the same object at different resolutions.

## Experiment 4: Transported Threat And Tail Images

### Purpose

Measure whether transported threat/tail coordinates carry more discriminating
structure than reset/deadline width.

### Inputs

```text
N
source certificate C
C.lower_d_threat_offset
C.tail_after_reset_offsets[0]
C.reset_endpoint
C.reset_deadline_value
induced opposite certificate C'
```

### Derived Fields

```text
transported_threat_image =
  floor(N / (C.anchor + C.lower_d_threat_offset))

transported_tail_image =
  floor(N / (C.anchor + C.tail_after_reset_offsets[0]))
```

### Output Rows

Write:

```text
output/transported_threat_tail_images/rows.jsonl
output/transported_threat_tail_images/summary.json
```

Measure:

```text
threat_image_position = before_upper_reset | inside_upper_interval | after_upper_deadline | missing
tail_image_position = before_upper_reset | inside_upper_interval | after_upper_deadline | missing
induced_threat_position
induced_tail_position
```

### Falsification

If threat/tail positions are constant across most rows or reproduce the broad
static frontier class, they are not discriminating and should not enter the
next invariant.

### Status

Diagnostic only.

## Experiment 5: Symmetric Width Diagnostic

### Purpose

Quickly falsify or retain transported reset-to-deadline width as a diagnostic.

### Predicate

```text
abs(
  abs(floor(N / C_l.reset_deadline_value)
      - floor(N / C_l.reset_endpoint))
  - (C_u.reset_deadline_value - C_u.reset_endpoint)
) <= 1
```

and symmetrically.

Also run the relaxed carrier tolerance:

```text
<= max(C_l.carrier_d, C_u.carrier_d)
```

### Output

Write:

```text
output/transported_width_diagnostic/rows.jsonl
output/transported_width_diagnostic/summary.json
```

### Falsification

If this fires on many rows already rejected by the strict runner or static
frontier-class tests, discard it.

### Status

Low-priority diagnostic. Raw source-side margin equality is already invalid.

## Execution Order

Run in this order:

```text
1. certificate_commitment_story_v1
2. transported_commitment_story_ledger_v1
3. commitment_story_word_projection_v1
4. transported_threat_tail_images_v1
5. transported_width_diagnostic_v1
```

The first three are the real research path. The last two are cheap diagnostics.

## Promotion Rule

No experiment may be promoted to official decomposer inference until it has:

```text
public inputs only
deterministic construction
no endpoint-budget coverage claim
no audit labels
no product closure
explicit unresolved state
named falsification result
PGS-law argument from GWR/NLSC or PROOF.md-compatible certificate logic
```

Until then the official runner remains:

```text
unresolved_by_certificate_pair_not_closed
```
