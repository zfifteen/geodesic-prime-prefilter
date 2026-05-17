# Public Grammar Direction-Lock Probe Results

## Claim

The next probe sharpened slot lock into oriented endpoint-pair grammar.

The public grammar around `N` does not interact with a loose collection of
factor-side residues and phases. It interacts most strongly with the directed
left/right boundary pair belonging to each hidden factor.

## Test Design

The public side was fixed:

```text
public_word_gwr_side
```

The bands were:

```text
train = factors 9001..11000
calibration = factors 11001..13000
prior_forward = factors 13001..15000
strict_forward = factors 15001..17000
```

A candidate cell had to be supported and absent across the first three bands.
Any observed matching cell in `15001..17000` strictly falsified it.

## Direction And Pairing Ablation

The tested factor projections were:

| factor projection | structure preserved | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `slot_residue_phase` | `pL`, `pR`, `qL`, `qR` all preserved | `213222` | `3359` | `15` per mille |
| `unordered_endpoint_pair_residue_phase` | endpoint L/R pairs preserved, `p/q` collapsed | `189195` | `4128` | `21` per mille |
| `left_right_boundary_multiset_residue_phase` | global left multiset and global right multiset preserved | `197195` | `4851` | `24` per mille |
| `unordered_endpoint_lr_multiset_residue_phase` | endpoint pairing preserved, L/R inside endpoints collapsed | `112867` | `4286` | `37` per mille |
| `slot_residue_phase_multiset` | all four slots collapsed | `88973` | `4429` | `49` per mille |

The ordering matters more than any single row. Preserving the directed boundary
pair inside each endpoint performs better than preserving global left/right
direction without endpoint pairing. It also performs much better than
preserving endpoint pairing after erasing left/right direction.

## Interpretation

The signal is not just:

```text
left boundary versus right boundary
```

and it is not just:

```text
which two local boundaries belong to the same factor
```

The strongest object is:

```text
which left boundary and which right boundary form the directed neighborhood
of the same factor
```

That is why the best compact representation after full four-slot identity is:

```text
unordered_endpoint_pair_residue_phase
```

It discards the artificial `p/q` label, but keeps each factor's directed
left/right boundary pair intact.

## Current Rule Object

The active factor-side grammar object is now:

```text
oriented endpoint-pair grammar
```

The current best measured surface remains:

```text
public_word_gwr_side -> slot_residue_phase
```

The best compact candidate is:

```text
public_word_gwr_side -> unordered_endpoint_pair_residue_phase
```

The compact candidate is only slightly weaker:

```text
full four-slot rate = 15 per mille
unordered directed endpoint-pair rate = 21 per mille
```

That difference measures the value of retaining the downstream `p/q` assignment.
The larger jumps measure the value of keeping directed endpoint-pair structure.

## Next Probe

The next probe should test whether the remaining gap between `15` and `21` per
mille comes from inner/outer boundary roles.

The natural boundary classes are:

```text
outer boundaries = pL and qR
inner boundaries = pR and qL
```

Test these factor projections while keeping `public_word_gwr_side` fixed:

```text
inner_outer_boundary_multiset_residue_phase
inner_outer_endpoint_pair_residue_phase
slot_residue_phase_with_inner_outer_summary
```

The strict question:

```text
Does preserving inner/outer role recover part of the 15 vs 21 per mille gap
without restoring the artificial p/q labels?
```

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = oriented_endpoint_pair_grammar_supported
active_compact_candidate = public_word_gwr_side ->
                           unordered_endpoint_pair_residue_phase
next_test = inner_outer_boundary_role_probe
```

## Reproduction

Run:

```text
python3 slot_factor_public_quotient_test.py \
  --public-mode public_word_gwr_side \
  --output-dir output/direction_lock_probe_15001_17000
```

The visual is:

```text
output/direction_lock_probe_15001_17000/direction_lock_probe_rates.png
```
