# Public Grammar Directional Boundary Gate Results

## Claim

The public minimum-divisor position filters the right-following gaps around
the hidden factor endpoints much more cleanly than the left-preceding gaps.

The tested comparison keeps exact directed endpoint-pair identity fixed and
changes only the at-winner boundary gate:

```text
left boundary residues
right boundary residues
left boundary residue+phase slots
right boundary residue+phase slots
both left and right boundary residues
```

The right-residue gate is strongest in every tested forward window.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Directional Comparison

The non-overlapping `27001..30000` falsifier is the cleanest comparison because
it follows the three windows that selected the current object.

| boundary gate | joint candidates | testable exact cells | exact falsifications | rate per million | top 1000 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `right_residues` | `13185` | `12404` | `12` | `967` | `3 / 1000` |
| `right_residue_phases` | `20392` | `19119` | `180` | `9414` | `13 / 1000` |
| `both_residues` | `22023` | `20619` | `280` | `13579` | `32 / 1000` |
| `left_residue_phases` | `12614` | `10947` | `220` | `20096` | `38 / 1000` |
| `left_residues` | `547` | `479` | `10` | `20876` | `10 / 479` |

The same ordering appeared in the prior three windows:

| strict forward band | best gate | best gate ppm | left-residue ppm | both-residue ppm |
| --- | --- | ---: | ---: | ---: |
| `21001..23000` | `right_residues` | `313` | `14048` | `7241` |
| `23001..25000` | `right_residues` | `319` | `15082` | `10891` |
| `25001..27000` | `right_residues` | `417` | `8658` | `8098` |
| `27001..30000` | `right_residues` | `967` | `20876` | `13579` |

The directionality is the result. Adding the left boundary to the right
boundary weakens the surface. Using the left boundary alone weakens it much
more.

## Interpretation

The public at-winner condition is the public condition where the selected
composite sits at the minimum-divisor point inside its containing prime gap.
Under that condition, the gaps immediately after the hidden factor endpoints
carry a sharper compatibility trace than the gaps immediately before those
same endpoints.

This supports the current working law object:

```text
public at-winner grammar
    gates
exact directed endpoint-pair exclusions
    through
right-following factor boundary residues
```

The right-following boundary is not a replacement for exact endpoint-pair
identity. It is the directional gate that selects stable exact-pair absences.

## Boundary

The fourth window degraded the top-K cleanliness:

```text
top_1000_25001_27000 = 2 / 840
top_1000_27001_30000 = 3 / 1000
```

That is not a failure of the directional result. It is a warning that support
ranking alone is not the final grammar rule. The next rule must explain which
right-residue gated exact pairs survive the larger band and which exact pairs
produce the small set of falsifications.

## Reproduction

Run the latest directional comparison:

```text
python3 directional_boundary_gate_surface.py \
  --train-dir output/enriched_multiplication_map_corpus_21001_23000 \
  --calibration-dir output/enriched_multiplication_map_corpus_23001_25000 \
  --prior-forward-dir output/enriched_multiplication_map_corpus_25001_27000 \
  --forward-dir output/enriched_multiplication_map_corpus_27001_30000 \
  --output-dir output/directional_boundary_gate_surface_27001_30000
```

Primary outputs:

```text
output/directional_boundary_gate_surface_21001_23000/summary.json
output/directional_boundary_gate_surface_23001_25000/summary.json
output/directional_boundary_gate_surface_25001_27000/summary.json
output/directional_boundary_gate_surface_27001_30000/summary.json
```
