# Round 18 Flight Debrief

## Flight Status

Round 18 climbed back to the 12-lane selector surface and produced a mechanically auditable mechanism-compression matrix.

The measured result is:

```text
total_lanes = 12
survivor_lanes = ["43|79", "49|13"]
excluded_lanes = 10
component_law_count_before_compression = 4
mechanism_law_count_after_compression = 4
compression_success = false
theorem_status = hypothesis_not_proved
universal_proof_complete = false
factor_found_claimed = false
```

The current finite matrix does not compress the Round 10/11 component laws into a smaller mechanism family.

## What Was Built

Round 18 added two executable mirror artifacts:

```text
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/codex_round18_component_obstruction_compression.py
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/grok_round18_component_obstruction_compression.py
```

Each artifact emits the same output shape:

```text
lane_mechanism_matrix.jsonl
mechanism_groups.json
compression_summary.json
proposed_next_proof_object.json
falsifier_contracts.jsonl
```

The output folders are generated under:

```text
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output/codex_round18_component_obstruction_compression/
research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output/grok_round18_component_obstruction_compression/
```

## Mechanism Classes

The derived mechanism classes are computed from explicit `mechanism_features`, not copied from Round 10/11 labels.

The measured excluded-lane grouping is:

```text
directed_tuple_mismatch:
  103|139
  109|73
  133|169
  139|103
  13|49
  169|133
  73|109

entry_d_bound_failure:
  79|43

entry_width_residue_open_offset_mismatch:
  19|163

exit_offset_parity_mismatch:
  163|19
```

The survivor class is:

```text
survivor_terminal_lift_aligned:
  43|79
  49|13
```

## Mathematical Meaning

Round 18 tested whether the ten excluded same-phase lanes collapse into fewer reusable public gap mechanisms when width, residue, first-open, tuple, and parity fields are analyzed uniformly.

On the current representative surface, they do not. The four component-law structure remains the smallest measured obstruction structure:

```text
prev_open_offset_4
prev_d_le4
directed_tuple
next_parity_odd
```

The two factor-relevant survivor lanes remain:

```text
43|79 -> lower-terminal four-slot lift
49|13 -> lower-terminal four-slot lift
```

This is structural endpoint-class alignment. It is not `factor_found`.

## Limitation

Grok identified the important surface limitation.

The Round 18 matrix uses the Round 9 pipeline order and `last_nonzero_rows` as the representative prior surface. Under that rule, lane `163|19` is represented at the exit-parity surface and is classified as:

```text
exit_offset_parity_mismatch
```

The Round 17 `a10` finite certificate lives on a relaxed sub-surface, where:

```text
a10 -> width 14 -> previous_left_mod30 17 -> first_open_offset 2 -> not prev_open_offset 4
```

That `a10` sub-surface is not represented in the Round 18 main matrix. Therefore Round 18 does not rule out a later, wider matrix that includes relaxed sub-surfaces and discovers a shared width/residue mechanism.

## Cockpit Transcript

ATC: Handing ChatGPT comms to Codex. Begin pre-flight, then takeoff, cruise, and landing.

Pilot: Copy. Establishing first-officer radio through Computer Use and preserving theorem boundaries.

First Officer: PRE_FLIGHT_STATUS: GO. Build independent mirror scripts, emit exactly twelve rows, compute `mechanism_features` first, and derive the class from those features.

Pilot: Takeoff. Codex instrument installed and run. Twelve lanes emitted. No compression found.

Co-pilot: Grok mirror confirms the same measured result. Four mechanism classes remain. No smaller finite invariant found on this representative surface.

Pilot: Landing. Round 18 maps the obstruction surface cleanly, keeps the theorem open, and records the `a10` sub-surface limitation for the next flight.

ATC: Flight record accepted for review.

## Status

```text
ROUND18_STATUS = measured_matrix_landed
COMPRESSION_STATUS = no_compression_on_current_representative_surface
THEOREM_STATUS = hypothesis_not_proved
UNIVERSAL_PROOF_COMPLETE = false
FACTOR_FOUND = false
```

## Next Proof Object

The next direct move is not another blind singleton descent.

The next proof object is:

```text
Decide whether to widen the mechanism matrix to include relaxed sub-surfaces
such as the Round 17 a10 surface, or accept the four component-law structure
as the current minimal proof contract and resume proving the component laws.
```
