# Public Grammar Slot-Lock Probe Results

## Claim

The factor side carries slot-specific information. The strongest compression
tested so far preserves all four factor-neighborhood slots:

```text
p-left, p-right, q-left, q-right
```

with each slot reduced only to residue plus phase.

This supports the slot-lock hypothesis in a measured, bounded form: the public
gap grammar around `N` is compatible with some four-slot factor arrangements
and incompatible with others. Collapsing those slots into a token multiset
destroys much of the signal.

## Test Design

The test used four bands:

```text
train = factors 9001..11000
calibration = factors 11001..13000
prior_forward = factors 13001..15000
strict_forward = factors 15001..17000
```

A candidate incompatibility cell had to satisfy:

```text
public key supported in train, calibration, and prior_forward
factor key supported in train, calibration, and prior_forward
public/factor pair absent in train, calibration, and prior_forward
```

The strict forward boundary was:

```text
any observed public/factor pair in 15001..17000 falsifies that candidate cell
```

All results use:

```text
min_public_support = 5
min_factor_support = 5
```

## Public Quotient Sweep

The first probe fixed the factor side to:

```text
slot_residue_phase =
pL=residue@phase | pR=residue@phase | qL=residue@phase | qR=residue@phase
```

and tested several public-side quotients.

| public quotient | testable cells | survived cells | falsified cells | strict falsification rate |
| --- | ---: | ---: | ---: | ---: |
| `public_word_gwr_side` | `213222` | `209863` | `3359` | `15` per mille |
| `public_word` | `218358` | `214522` | `3836` | `17` per mille |
| `containing_next_side` | `209564` | `204273` | `5291` | `25` per mille |
| `prev_containing_side` | `202246` | `196933` | `5313` | `26` per mille |
| `containing_gwr_bucket` | `93860` | `89929` | `3931` | `41` per mille |
| `containing_side` | `52777` | `49829` | `2948` | `55` per mille |

The best public side remains the full public word with GWR side. Public-side
loosening degrades stability.

## Factor Compression Sweep

The second probe tested whether the four factor slots could be collapsed.

The best result was:

```text
public_word_gwr_side -> slot_residue_phase
testable = 213222
falsified = 3359
strict_falsification_rate = 15 per mille
```

The next best factor compression collapsed `p/q` endpoint identity but
preserved left/right structure inside each endpoint:

```text
public_word_gwr_side -> unordered_endpoint_pair_residue_phase
testable = 189195
falsified = 4128
strict_falsification_rate = 21 per mille
```

Collapsing both endpoint identity and left/right structure was weaker:

```text
public_word_gwr_side -> unordered_endpoint_lr_multiset_residue_phase
testable = 112867
falsified = 4286
strict_falsification_rate = 37 per mille
```

Fully collapsing the four factor slots into a residue/phase multiset was weaker
again:

```text
public_word_gwr_side -> slot_residue_phase_multiset
testable = 88973
falsified = 4429
strict_falsification_rate = 49 per mille
```

The previously tested broader token multiset family had a strict falsification
rate of `510` per mille. The slot-residue-phase surface reduces that to `15`
per mille under the same strict forward philosophy.

## Interpretation

The ordering of results is the signal:

```text
four slots preserved                         = strongest
p/q collapsed, left/right preserved          = weaker
p/q and left/right collapsed into pairs      = weaker
all four factor slots collapsed as multiset  = weaker
```

That ordering is exactly what the slot-lock hypothesis predicts. The public
gap word does not merely care about which factor-side ingredients exist. It
also cares where those ingredients sit around the two factors.

The public side should not be loosened first. The best next object keeps:

```text
public_word_gwr_side
```

and searches for a compact factor-side grammar that preserves slot identity.

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = slot_lock_supported_by_forward_probe
strongest_measured_surface = public_word_gwr_side -> slot_residue_phase
active_decision_rule = preserve p-left, p-right, q-left, q-right before
                       testing any further factor-side compression
```

This does not prove a factor-location theorem. It identifies the next stable
grammar object for rule discovery.

## Reproduction

Run the public quotient and factor compression sweep:

```text
python3 slot_factor_public_quotient_test.py \
  --output-dir output/slot_factor_public_quotient_test_15001_17000_factor_modes
```

The script writes:

```text
output/slot_factor_public_quotient_test_15001_17000_factor_modes/summary.json
output/slot_factor_public_quotient_test_15001_17000_factor_modes/public_quotient_rows.jsonl
output/slot_factor_public_quotient_test_15001_17000_factor_modes/public_quotient_sample_cells.jsonl
```

The brainstorm visual probes are:

```text
output/slot_lock_brainstorm_probe_15001_17000/slot_lock_projection_falsification_rates.png
output/slot_lock_brainstorm_probe_15001_17000/slot_lock_support_sweep_heatmap.png
output/slot_factor_public_quotient_test_15001_17000_factor_modes/slot_factor_compression_sweep_top12.png
```
