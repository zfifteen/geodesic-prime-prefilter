# Collatz-PGS Terminal Contact Decomposition Probe

## Strongest Measured Result

Terminal witness contact remains positive after exact matching on odd-step
length and final transition `v2`, but it does not absorb the whole signal.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

For each first-descent block, it reconstructed the accelerated odd Collatz
source sequence and split blocks into three classes:

- `terminal_witness_contact`: the final source before first descent is a
  composite odd-projected PGS witness hit;
- `nonterminal_witness_contact`: some earlier composite source is a witness
  hit, but the final source is not;
- `no_witness_contact`: no composite source is a witness hit.

All comparisons are matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata.

## Decomposition Result

| Comparison | Matched strata | Matched weight | Median reset delta | Median reset ratio | P90 reset delta |
|---|---:|---:|---:|---:|---:|
| Terminal vs no witness | `263` | `68617` | `0.33031631110499143` | `1.0401652897967644` | `-0.06517386977033526` |
| Nonterminal vs no witness | `278` | `59054` | `0.3036864937903315` | `1.0008728144774863` | `0.4710225946278901` |
| Terminal vs nonterminal | `438` | `31505` | `0.3577078179616415` | `1.0949883036454384` | `-1.1454448355919158` |

The block counts were:

| Class | Count |
|---|---:|
| `terminal_witness_contact` | `70227` |
| `nonterminal_witness_contact` | `90979` |
| `no_witness_contact` | `338793` |

## Follow-On Result

The follow-on terminal geometry probe measured final-source prime-gap geometry
inside the terminal-vs-no-witness comparison:

```text
docs/collatz_pgs_terminal_geometry_probe.md
```

Positive terminal carriers have higher terminal exact-witness hit rate:
`0.8720123654427132` versus `0.7452117085795563` in negative terminal
carriers.

## Disposition

The terminal-source hypothesis survived its first serious control and now has
a visible geometric refinement. Matching on final `v2` did not erase the
terminal-contact reset advantage, and the positive terminal carriers are more
exact-witness-centered than the negative carriers.

The result is still not terminal-only. Nonterminal-only contact remains mildly
positive against no-witness blocks under the same exact-step and final-`v2`
matching. That keeps the research line broader: terminal contact looks like
the cleanest reset-local expression of the effect, while nonterminal contact
still looks like a block-geometry marker.

The next pressure point is to split exact terminal witness hits from adjacent
projected terminal hits under exact-step and final-`v2` matching.

## Artifact Surface

- Probe: `scripts/collatz_pgs_terminal_contact_decomposition_probe.py`
- Contract test: `tests/test_collatz_pgs_terminal_contact_decomposition_probe.py`
- Summary: `output/collatz_pgs_terminal_contact_decomposition_probe/summary.json`
- Strata rows: `output/collatz_pgs_terminal_contact_decomposition_probe/strata_rows.jsonl`
