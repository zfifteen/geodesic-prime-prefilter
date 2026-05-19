# Paragraph 08 Evidence: Invalidated Shadow Selector

## Public Claim To Support

The branch also made progress by ruling out a tempting shortcut. A shadow
surface was real, but it appeared on survivor lanes too, so it could not be the
missing selector.

## Supporting Evidence

- `research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/ROUND19_SHADOW_SURFACE_DEBRIEF.md`
  states that the missing compression does not cleanly live in the Round 17
  shadow surface under the tested definition.
- The debrief records:
  - `shadow_row_count = 152`
  - `broad_shadow_pair_collapse_signal = true`
  - `survivor_shadow_contamination = true`
  - `shadow_compression_success = false`
  - `factor_found = false`
- It explains that the width/residue shadow defect appears on both excluded
  lanes and survivor lanes, so it is not the missing factor-lane selector by
  itself.
- Relevant commits:
  - `790956b8` - Add PEDK round 17 partial width certificate
  - `5ebce779` - Add PEDK round 18 compression matrix
  - `115c9bea` - Add PEDK round 19 shadow surface test

## Status Boundary

- Valid measured result: the broad shadow signal exists.
- Invalidated as selector: it does not separate excluded lanes from survivor
  lanes.
- Theorem status: hypothesis not proved.

## Infographic Concept

Two groups of lanes, excluded and survivor. The same shadow mark appears in
both groups. A red line crosses out "selector" while preserving "real signal".

