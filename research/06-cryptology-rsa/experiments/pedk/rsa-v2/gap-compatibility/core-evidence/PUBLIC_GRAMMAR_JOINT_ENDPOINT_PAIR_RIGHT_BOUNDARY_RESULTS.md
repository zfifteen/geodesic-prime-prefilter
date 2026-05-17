# Public Grammar Joint Endpoint-Pair Right-Boundary Results

## Claim

The right-boundary signal becomes much stronger when it is used as a gate on
exact directed endpoint-pair exclusions instead of replacing the endpoint-pair
object.

The current best measured exclusion surface is:

```text
public at-winner grammar
    gates
exact unordered directed endpoint-pair exclusions
    by
right-boundary residue class
```

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Tested Object

The primary factor-side key remains the exact unordered directed endpoint pair:

```text
L=<left slot>|R=<right slot> || L=<left slot>|R=<right slot>
```

Each endpoint pair keeps left and right boundary order. The two hidden factor
endpoints are sorted as an unordered pair, so downstream `p/q` naming is not
the law object.

The right-boundary gate is an indexed attribute:

```text
right_residues = sorted residues of the two endpoint right boundaries
```

The experiment keeps an exact endpoint-pair candidate only when both conditions
hold across the prior bands:

1. The exact public/endpoint-pair cell is independently supported and jointly
   absent.
2. The at-winner public/right-residue cell is independently supported and
   jointly absent.

Forward falsification is still measured on exact endpoint-pair observation.
The right-residue class is a gate, not a replacement key.

## Forward Windows

The experiment was run across three rolling windows.

| strict forward band | joint candidates | testable exact cells | exact falsifications | rate per million | top 200 | top 500 | top 1000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `21001..23000` | `15641` | `12765` | `4` | `313` | `0 / 182` | `0 / 458` | `0 / 913` |
| `23001..25000` | `15023` | `9383` | `3` | `319` | `0 / 180` | `0 / 447` | `0 / 896` |
| `25001..27000` | `12572` | `9584` | `4` | `417` | `0 / 169` | `1 / 422` | `2 / 840` |

The rates are below one per mille in all three windows. The integer per-mille
field in the output is therefore `0`; the per-million field records the
measured nonzero rate.

## Comparison With Prior Surfaces

The broad exact endpoint-pair carrier remains real, but the right-residue gate
materially sharpens it.

| strict forward band | broad exact pair rate | at-winner exact pair rate | right-residue gated exact rate |
| --- | ---: | ---: | ---: |
| `21001..23000` | `19` per mille | `33` per mille | `313` per million |
| `23001..25000` | `29` per mille | `50` per mille | `319` per million |
| `25001..27000` | `23` per mille | `39` per mille | `417` per million |

The at-winner exact-pair slice by itself is not enough. It is worse than the
broad carrier. The improvement appears only when exact endpoint-pair absence is
conditioned by an independently absent at-winner right-residue class.

That is the current strongest evidence that the law is not merely:

```text
public word -> factor endpoint pair
```

It is closer to:

```text
public at-winner grammar constrains which right-boundary residue classes can
carry exact directed endpoint-pair absences
```

## Boundary

The result does not prove the compatibility law. It identifies the current
best measured object for rule extraction.

The right-residue gate alone also has forward falsifications. Its role is not
to exclude factors by itself. Its role is to select exact endpoint-pair
exclusions that survive much more strongly than the ungated exact-pair surface.

Do not promote `right_values_only`, `right_residues`, or any other collapsed
right-boundary projection as the factor-side law object. The exact directed
endpoint pair remains the atom.

## Reproduction

Build the fresh corpus:

```text
python3 enriched_multiplication_map_corpus.py \
  --band 25001:27000 \
  --output-dir output/enriched_multiplication_map_corpus_25001_27000
```

Run the latest forward window:

```text
python3 joint_endpoint_pair_right_boundary_surface.py \
  --train-dir output/enriched_multiplication_map_corpus_19001_21000 \
  --calibration-dir output/enriched_multiplication_map_corpus_21001_23000 \
  --prior-forward-dir output/enriched_multiplication_map_corpus_23001_25000 \
  --forward-dir output/enriched_multiplication_map_corpus_25001_27000 \
  --output-dir output/joint_endpoint_pair_right_boundary_surface_25001_27000
```

Primary outputs:

```text
output/joint_endpoint_pair_right_boundary_surface_21001_23000/summary.json
output/joint_endpoint_pair_right_boundary_surface_23001_25000/summary.json
output/joint_endpoint_pair_right_boundary_surface_25001_27000/summary.json
output/hybrid_endpoint_pair_surface_25001_27000/summary.json
```
