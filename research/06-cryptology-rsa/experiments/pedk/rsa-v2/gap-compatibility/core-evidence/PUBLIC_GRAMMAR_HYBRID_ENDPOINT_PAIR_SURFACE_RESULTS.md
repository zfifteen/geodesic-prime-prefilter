# Public Grammar Hybrid Endpoint-Pair Surface Results

## Claim

The hybrid surface confirms that right-boundary values carry real exclusion
signal, but the result is still not the law object.

The strongest broad object remains the exact unordered directed endpoint-pair
surface. The strongest thin object is now:

```text
public_word_at_winner -> right_values_only
```

That thin object is useful as a discriminator. It should not be promoted to a
complete compatibility law because it collapses the paired endpoint structure.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Tested Object

The hybrid test preserves the endpoint-pair frame while varying how much of
each endpoint pair is retained.

The public modes were:

```text
public_word_gwr_side
public_word_at_winner
containing_type_at_winner
containing_phase_at_winner
```

The factor modes were:

```text
exact_endpoint_pair
right_class_left_full
right_class_left_residue
right_class_left_phase
right_class_left_residue_right_phase
right_values_only
```

The mode `right_class_left_full` is a semantic rewrite of the exact endpoint
pair:

```text
unordered pairs L=x|R=y
```

becomes:

```text
right boundary class y carries left boundary x
```

It keeps the same information as the exact endpoint pair, but makes the
right-boundary coordinate explicit.

## Forward Window: 21001..23000

The first hybrid test used:

```text
train = factors 15001..17000
calibration = factors 17001..19000
prior_forward = factors 19001..21000
strict_forward = factors 21001..23000
```

Top surfaces:

| public mode | factor mode | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `containing_phase_at_winner` | `right_values_only` | `67` | `0` | `0` per mille |
| `public_word_gwr_side` | `exact_endpoint_pair` | `174303` | `3328` | `19` per mille |
| `public_word_gwr_side` | `right_class_left_full` | `174303` | `3328` | `19` per mille |
| `containing_type_at_winner` | `right_values_only` | `35` | `1` | `28` per mille |
| `public_word_at_winner` | `right_values_only` | `194` | `6` | `30` per mille |
| `public_word_at_winner` | `exact_endpoint_pair` | `10103` | `335` | `33` per mille |
| `public_word_at_winner` | `right_class_left_full` | `10103` | `335` | `33` per mille |
| `public_word_gwr_side` | `right_class_left_residue_right_phase` | `113661` | `4437` | `39` per mille |

## Forward Window: 23001..25000

The shifted hybrid test used:

```text
train = factors 17001..19000
calibration = factors 19001..21000
prior_forward = factors 21001..23000
strict_forward = factors 23001..25000
```

Top surfaces:

| public mode | factor mode | testable cells | falsified cells | strict falsification rate |
| --- | --- | ---: | ---: | ---: |
| `public_word_at_winner` | `right_values_only` | `180` | `3` | `16` per mille |
| `public_word_gwr_side` | `exact_endpoint_pair` | `125208` | `3695` | `29` per mille |
| `public_word_gwr_side` | `right_class_left_full` | `125208` | `3695` | `29` per mille |
| `containing_phase_at_winner` | `right_values_only` | `67` | `2` | `29` per mille |
| `containing_type_at_winner` | `right_values_only` | `34` | `1` | `29` per mille |
| `public_word_gwr_side` | `right_class_left_residue_right_phase` | `92346` | `3980` | `43` per mille |
| `public_word_at_winner` | `exact_endpoint_pair` | `8580` | `429` | `50` per mille |
| `public_word_at_winner` | `right_class_left_full` | `8580` | `429` | `50` per mille |

## Interpretation

The hybrid experiment separates two facts.

First, exact endpoint-pair identity remains the best broad carrier:

```text
public_word_gwr_side -> exact_endpoint_pair
```

It measured:

```text
19 per mille on 21001..23000
29 per mille on 23001..25000
```

Second, public at-winner rows have a thin but strong right-boundary signal:

```text
public_word_at_winner -> right_values_only
```

It measured:

```text
30 per mille on 21001..23000 with 194 testable cells
16 per mille on 23001..25000 with 180 testable cells
```

The right-boundary-only signal is too thin and too compressed to serve as the
law object. Its value is diagnostic: it identifies a coordinate inside the
endpoint-pair grammar that the eventual law must preserve.

The current candidate law object is now:

```text
public_word_gwr_side -> exact directed endpoint pair
```

with an internal discriminator:

```text
public at-winner word -> endpoint-pair right-boundary values
```

## Current Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = hybrid_endpoint_pair_surface_measured
broad_carrier = public_word_gwr_side -> exact_endpoint_pair
thin_discriminator = public_word_at_winner -> right_values_only
unresolved_object = how to combine the broad carrier and thin discriminator
                    into one stable exclusion law
```

## Reproduction

Run the first hybrid window:

```text
python3 hybrid_endpoint_pair_surface.py \
  --train-dir output/enriched_multiplication_map_corpus_15001_17000 \
  --calibration-dir output/enriched_multiplication_map_corpus_17001_19000 \
  --prior-forward-dir output/enriched_multiplication_map_corpus_19001_21000 \
  --forward-dir output/enriched_multiplication_map_corpus_21001_23000 \
  --output-dir output/hybrid_endpoint_pair_surface_21001_23000
```

Run the shifted hybrid window:

```text
python3 hybrid_endpoint_pair_surface.py
```

The output files are:

```text
output/hybrid_endpoint_pair_surface_21001_23000/summary.json
output/hybrid_endpoint_pair_surface_21001_23000/surface_rows.jsonl
output/hybrid_endpoint_pair_surface_21001_23000/candidate_rows.jsonl
output/hybrid_endpoint_pair_surface_23001_25000/summary.json
output/hybrid_endpoint_pair_surface_23001_25000/surface_rows.jsonl
output/hybrid_endpoint_pair_surface_23001_25000/candidate_rows.jsonl
```
