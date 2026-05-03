# Collatz-PGS Terminal Adjacent Residue Probe

## Summary

Terminal adjacent PGS contact is an exact Collatz residue condition on the PGS
witness.

At odd seeds `3 <= s <= 999999`, every terminal source at `witness - 1` or
`witness + 1` satisfied the corresponding residue identity, the exact
non-overdivisibility condition for its final `v2`, and the recorded terminal
target.

This gives the side split an algebraic form. The below-witness result is not
only a positional marker. It is the event that a PGS witness lands in the
Collatz residue class that makes `witness - 1` the terminal source.

## Residue Identities

Let `w` be the PGS witness in the final source's prime gap and let `k` be the
terminal value of `v2(3n+1)`.

For a below-witness terminal source, `n=w-1`, so:

$$C(w-1)=\frac{3w-2}{2^{k}}$$

The witness must satisfy:

$$w \equiv 2\cdot 3^{-1}\pmod {2^{k}}$$

and exact terminal exponent `k` means it must not also satisfy the same
below-witness residue modulo `2^{k+1}`.

For an above-witness terminal source, `n=w+1`, so:

$$C(w+1)=\frac{3w+4}{2^{k}}$$

The witness must satisfy:

$$w \equiv -4\cdot 3^{-1}\pmod {2^{k}}$$

and exact terminal exponent `k` again requires failure of the corresponding
modulo `2^{k+1}` residue.

## Measurement

The probe reads:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It keeps only terminal adjacent rows:

- `final_source = witness - 1`;
- `final_source = witness + 1`.

It excludes exact witness hits and nonterminal witness hits.

| Measurement | Value |
|---|---:|
| Adjacent terminal rows | `15558` |
| Residue identity rate | `1.0` |
| Exact-`v2` residue rate | `1.0` |
| Recomputed `v2` agreement rate | `1.0` |
| Terminal-target agreement rate | `1.0` |

## Side Counts

| Side | Count | Median reset strength | P90 reset strength | P99 reset strength |
|---|---:|---:|---:|---:|
| `below_witness_terminal_hit` | `12876` | `2.1068160333614414` | `10.666657962764708` | `85.33329153605015` |
| `above_witness_terminal_hit` | `2682` | `2.666665168801689` | `10.6666628852764` | `170.66511627906976` |

These raw side summaries are not matched comparisons. The matched adjacent-side
probe remains the correct source for below-versus-above reset advantage. This
probe supplies the arithmetic identity behind the side labels.

## Interpretation

The empirical side split now has a precise algebraic object:

```text
PGS witness in a Collatz terminal residue class modulo 2^k.
```

The broad reset experiment has therefore reached a useful stopping point.
The next work should leave broad measurement and attack the residue families
directly, starting with exact step `3` and final `v2=4` or `v2=8`.

For final `v2=4`, the below-witness residue is:

$$w \equiv 6 \pmod {16}$$

A terminal source `w-1` in that family has:

$$C(w-1)=\frac{3w-2}{16}$$

The proof-pressure question is whether PGS witness placement in this residue
class forces a stronger first-descent reset than the matched no-witness
population, or whether the measured median advantage remains a distributional
fact without a closed descent inequality.

## Output

```text
output/collatz_pgs_terminal_adjacent_residue_probe/summary.json
output/collatz_pgs_terminal_adjacent_residue_probe/residue_rows.jsonl
output/collatz_pgs_terminal_adjacent_residue_probe/side_rows.jsonl
output/collatz_pgs_terminal_adjacent_residue_probe/side_final_v2_rows.jsonl
```
