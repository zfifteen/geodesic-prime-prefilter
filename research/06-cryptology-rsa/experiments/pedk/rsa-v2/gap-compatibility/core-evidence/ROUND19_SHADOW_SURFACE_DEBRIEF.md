# Round 19 Shadow Surface Debrief

## Headline

The missing compression does not cleanly live in the Round 17 shadow surface under the tested definition.

Round 19 found a real broad-shadow signal:

```text
163|19 -> entry_width_residue_open_offset_shadow_defect
19|163 -> entry_width_residue_open_offset_shadow_defect
```

But the same primary shadow defect also appears on the two survivor lanes:

```text
43|79 -> entry_width_residue_open_offset_shadow_defect
49|13 -> entry_width_residue_open_offset_shadow_defect
```

The broad shadow collapse is therefore contaminated. It is not a selector.

## Status

```text
ROUND19_STATUS = measured_shadow_surface_test_landed
BROAD_SHADOW_PAIR_COLLAPSE_SIGNAL = true
SHADOW_COMPRESSION_SUCCESS = false
SHADOW_INSIGHT_STATUS = weakened_by_survivor_contamination_or_exact_one_gate_failure
THEOREM_STATUS = hypothesis_not_proved
UNIVERSAL_PROOF_COMPLETE = false
FACTOR_FOUND = false
```

## What Was Built

Round 19 added two executable mirror artifacts:

```text
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/codex_round19_shadow_surface_compression.py
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/grok_round19_shadow_surface_compression.py
```

Each script emits:

```text
shadow_rows.jsonl
exact_one_gate_shadow_rows.jsonl
lane_shadow_profiles.jsonl
exact_one_gate_lane_shadow_profiles.jsonl
shadow_mechanism_groups.json
shadow_derivation_rules.json
lane_blind_boundary.json
shadow_compression_summary.json
```

## Experiment Definition

A broad shadow row is a row that reaches:

```text
same_mod36
factor_mod180_lane = target lane
Rres=o4|o4
public_gwr_side = at_winner
```

and fails at least one later public gate:

```text
prev_open_offset_4
prev_d_le4
directed_tuple_allowed
next_d_le4
next_parity_odd
```

The script computes public transport fields:

```text
previous_left_mod30_by_width =
  public_containing_left_mod30 - public_previous_gap_width mod 30

computed_prev_open_offset =
  first_open_offset(previous_left_mod30_by_width)

computed_next_parity =
  parity(public_containing_right_mod180 + next_winner_offset)
```

The exact-one-gate shadow surface is the subset of broad shadow rows that fail exactly one of the five later public gates.

## Measured Result

Codex and Grok both measured:

```text
shadow_row_count = 152
primary_shadow_mechanism_group_count = 2
broad_shadow_pair_collapse_signal = true
symmetric_pair_collapsed_into_entry_width_residue = true
survivor_shadow_contamination = true
exact_one_gate_symmetric_pair_collapsed = false
shadow_compression_success = false
```

The broad shadow groups are:

```text
entry_width_residue_open_offset_shadow_defect:
  103|139
  109|73
  133|169
  139|103
  163|19
  169|133
  19|163
  43|79
  49|13
  73|109
  79|43

directed_tuple_shadow_defect:
  13|49
```

The exact-one-gate symmetric pair does not collapse:

```text
163|19 -> directed_tuple_shadow_defect
19|163 -> no_shadow_rows
```

## Mathematical Meaning

Round 19 confirms that Round 17 exposed a real local transport mechanism:

```text
width/residue -> previous-left residue -> first-open offset
```

But that mechanism is common on the broad shadow surface. It appears on excluded lanes and survivor lanes alike. Therefore the width/residue shadow defect is not the missing factor-lane selector by itself.

This is a useful negative result. It prevents the project from promoting the Round 17 `a10` certificate into a broader compression law that the wider evidence surface does not support.

## Boundary

The experiment remains lane-conditioned:

```text
same_mod36 + factor_mod180_lane + Rres=o4|o4 + at_winner
```

It is not a lane-blind public factor selector. The script records this explicitly in:

```text
lane_blind_boundary.json
```

## Cockpit Transcript

ATC: Test whether the missing compression lives in the shadow surface exposed by Round 17.

Pilot: Copy. Build the shadow matrix, preserve theorem boundaries, and involve Grok.

Co-pilot: GO for the shadow-surface experiment. Freeze derivation rules before count inspection. Report survivor contamination as a falsifier.

Pilot: Broad shadow surface shows the symmetric pair collapsing into entry-width residue defect.

Co-pilot: Mirror confirms the collapse, but survivor lanes carry the same defect.

Pilot: Exact-one-gate surface does not collapse the pair. The broad-shadow signal is real but not selector-grade.

ATC: The flight lands as a falsifying measurement, not as final theorem progress.

## Next Research Move

The next direct move should not keep widening generic shadow rows.

The next candidate object is a contrastive shadow criterion:

```text
Find a shadow feature that is present on excluded lanes and absent from the
two survivor lanes, or prove that no such feature exists on the current
same-phase/Rres/at_winner surface.
```

The Round 17 `a10` certificate remains valid as a finite local mechanism, but Round 19 shows it does not currently scale into a clean 12-lane compression law.
