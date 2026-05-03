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

## Disposition

The terminal-source hypothesis survived its first serious control. Matching on
final `v2` did not erase the terminal-contact reset advantage, so terminal PGS
contact is not only a shadow of stronger ordinary Collatz division at the final
step.

The result is not terminal-only. Nonterminal-only contact also remains mildly
positive against no-witness blocks under the same exact-step and final-`v2`
matching. That keeps the research line broader: terminal contact looks like
the cleanest reset-local expression of the effect, while nonterminal contact
still looks like a block-geometry marker.

The next pressure point is to split the terminal-contact comparison by reset
magnitude bands or by exact final-source prime-gap state. The goal is to learn
whether terminal PGS contact contributes through a small number of high-reset
carrier strata or through a stable local endpoint/witness geometry.

## Artifact Surface

- Probe: `benchmarks/python/predictor/collatz_pgs_terminal_contact_decomposition_probe.py`
- Contract test: `tests/python/predictor/test_collatz_pgs_terminal_contact_decomposition_probe.py`
- Summary: `output/collatz_pgs_terminal_contact_decomposition_probe/summary.json`
- Strata rows: `output/collatz_pgs_terminal_contact_decomposition_probe/strata_rows.jsonl`
