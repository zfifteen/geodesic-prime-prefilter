# Collatz-PGS Terminal Geometry Probe

## Strongest Measured Result

The terminal-contact signal is carried by a smaller positive subset with
stronger reset deltas, and that subset is more centered on the exact PGS
witness.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It kept the terminal-vs-no-witness comparison matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata, then measured the final
source prime-gap geometry for the terminal-contact class.

## Geometry Result

| Measurement | Positive terminal carriers | Negative terminal carriers |
|---|---:|---:|
| Strata | `141` | `122` |
| Matched weight share | `0.2431613157089351` | `0.7568386842910649` |
| Weighted mean of stratum median reset delta | `1.7526101771071119` | `-0.12664612350652749` |
| Weighted mean of stratum median reset ratio | `1.1767217242376298` | `0.9962916837610672` |
| Weighted mean terminal exact-witness hit rate | `0.8720123654427132` | `0.7452117085795563` |
| Weighted mean terminal adjacent-projected hit rate | `0.12798763455728673` | `0.2547882914204434` |
| Weighted mean terminal median final gap width | `12.875157326940366` | `11.859816683355156` |
| Weighted mean terminal median final endpoint distance | `3.47629607431825` | `2.3052838327043057` |
| Weighted mean no-witness final composite rate | `0.7429507228667794` | `0.7921494551344104` |
| Weighted mean no-witness median final witness distance | `6.840455498951154` | `6.2612262189016406` |

The top positive terminal carriers are concentrated in exact-step/final-`v2`
strata such as `(3, 8)`, `(3, 9)`, `(4, 9)`, and `(4, 6)`. Their terminal
sources are usually exact witness hits rather than adjacent projected hits.

## Disposition

The terminal signal now has a visible geometric shape. It is not spread evenly
across terminal-contact strata. Most matched terminal weight sits in negative
or nearly flat strata, but those strata are only mildly negative. The positive
side is smaller and sharper: fewer matched blocks, much stronger median reset
advantage, and more exact witness-centered terminal sources.

This does not make exact witness contact a law. Negative carriers also contain
many exact witness hits. The useful read is narrower: exact witness-centered
terminal contact appears to be where the terminal effect is most concentrated,
while adjacent projected terminal contact looks more like a weaker or noisier
version of the same geometry.

The follow-on exact-versus-adjacent probe found that exact terminal hits do not
carry the terminal reset profile more strongly than adjacent projected terminal
hits after exact-step and final-`v2` matching. The later adjacent-side probe
found that this adjacent advantage is carried by final sources at
`witness - 1`, not `witness + 1`.

## Artifact Surface

- Probe: `scripts/collatz_pgs_terminal_geometry_probe.py`
- Contract test: `tests/test_collatz_pgs_terminal_geometry_probe.py`
- Summary: `output/collatz_pgs_terminal_geometry_probe/summary.json`
- Geometry rows: `output/collatz_pgs_terminal_geometry_probe/geometry_rows.jsonl`
