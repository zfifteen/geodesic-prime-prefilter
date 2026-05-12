# Collatz-PGS Short-Block Reset Candidate Probe

## Summary

The exact 3-step, final-`v2` `4` and `8` carrier has a closed Collatz algebra.
At odd seeds `3 <= s <= 999999`, every below-minimizer terminal row in the
committed first-descent block table lands on the same inverse branch:

```text
middle v2 = 2
w mod 9 = 5
```

That branch has twice the reset asymptote of the `middle_v2=1` branch. This
explains the observed near-`2x` median reset separation against all no-witness
controls in the target family. Inside fixed `(final_v2, middle_v2)`, the reset
advantage largely disappears, so the current theorem candidate is a
branch-selection statement, not a new within-branch reset law.

A later targeted inverse scan through odd seeds `<= 100000000` found rare
branch-1 below-minimizer counterexamples. The durable theorem-level result in
this note is the exact branch algebra. The live empirical result is branch-2
overrepresentation, not universal branch-2 selection.

## Definitions

The target family is:

- exact first-descent block length `3`;
- final exponent `k` in `{4, 8}`;
- terminal source `n=w-1`;
- `w` is the leftmost divisor-count minimizer in its prime gap.

The accelerated odd Collatz path is:

$$s \to a \to n \to t$$

where `t < s` is the first odd target below the seed.

For every exact 3-step block in this target surface, the first transition must
have `v2=1`, and the middle transition must have `v2=1` or `v2=2`.

## Exact Branch Algebra

Let the terminal source be `n=w-1` and let:

$$v_2(3w-2)=k$$

The final target is:

$$t=\frac{3w-2}{2^k}$$

If the middle exponent is `1`, then the inverse branch closes only when
`w mod 9 = 0`:

$$s=\frac{4w-9}{9}$$

and the reset strength is:

$$R(s)=\frac{2^k(4w-9)}{9(3w-2)}$$

with large-`w` asymptote:

$$\frac{2^{k+2}}{27}$$

If the middle exponent is `2`, then the inverse branch closes only when
`w mod 9 = 5`:

$$s=\frac{8w-13}{9}$$

and the reset strength is:

$$R(s)=\frac{2^k(8w-13)}{9(3w-2)}$$

with large-`w` asymptote:

$$\frac{2^{k+3}}{27}$$

The second branch has exactly twice the asymptotic reset strength of the first
branch at fixed `k`.

## Measured Target Surface

The probe extracted `249` exact 3-step rows with final `v2` in `{4, 8}` from
the committed `1000000` first-descent block table.

| Check | Result |
|---|---:|
| first-`v2` distribution | `{"1": 249}` |
| middle-`v2` distribution | `{"1": 166, "2": 83}` |
| seed formula failures | `0` |
| reset formula failures | `0` |

The below-minimizer target subset has `6` rows:

| Measurement | Result |
|---|---:|
| final `v2=4` rows | `5` |
| final `v2=8` rows | `1` |
| middle-`v2=2` rows | `6 / 6` |
| `w mod 9 = 5` rows | `6 / 6` |
| exact below-residue rate | `1.0` |

## Reset Comparison

Against all no-witness controls in the same exact 3-step, final-`v2` target
surface, the below-minimizer class shows a near-`2x` median reset separation.

| Final `v2` | Below median | No-witness median | Ratio |
|---:|---:|---:|---:|
| `4` | `4.740388590326582` | `2.370255741977521` | `1.999948151743171` |
| `8` | `75.83636363636364` | `37.92376585091947` | `1.9997055127510488` |

When the comparison is restricted to the same middle branch `middle_v2=2`, the
extra reset separation collapses:

| Final `v2` | Below median | No-witness median | Ratio |
|---:|---:|---:|---:|
| `4` | `4.740388590326582` | `4.7403443462075385` | `1.0000093335242783` |
| `8` | `75.83636363636364` | `75.84792626728111` | `0.9998475550817735` |

This identifies the current mechanism cleanly in the committed `1000000`
first-descent table: below-minimizer terminal contact selected the doubled
reset branch in the observed `k=4,8` short-block surface.

## Independent Residue Pressure

The probe also measured unique visited final-source prime gaps without using
terminal adjacency as the selection condition. Across `2469` unique non-prime
final-source gaps:

| Measurement | Value |
|---|---:|
| even minimizer rate | `0.27014985824220333` |
| exact `v2=4` below-residue gap rate | `0.029566626164439044` |
| exact `v2=4` below-residue rate among even minimizers | `0.10944527736131934` |
| exact `v2=8` below-residue gap rate | `0.0032401782098015392` |
| exact `v2=8` below-residue rate among even minimizers | `0.01199400299850075` |

This is a visited-gap pressure check, not a global prime-gap distribution
theorem.

## Theorem Candidate

For exact 3-step below-minimizer terminal blocks with final exponent `k`, the
reset strength is determined by two inverse branches:

```text
w mod 9 = 0 -> middle_v2 = 1 -> asymptote 2^(k+2)/27
w mod 9 = 5 -> middle_v2 = 2 -> asymptote 2^(k+3)/27
```

At final `v2=4` and `v2=8`, every below-minimizer row in the committed
`1000000` first-descent table is on the second branch. The clean theorem target
after the wider inverse scan is therefore weaker and more precise:

```text
In the exact 3-step final-v2 4/8 surface, the w mod 9 = 5 inverse branch has
a large below-minimizer occupancy advantage over the w mod 9 = 0 branch, and
the w mod 9 = 5 branch forces the doubled reset scale.
```

## Obstruction

The universal branch-selection claim is false. The first targeted inverse-scan
branch-1 counterexample appears at seed `6000471`, with witness `13501062`,
middle `v2=1`, final `v2=4`, and reset strength
`2.3703700923858233`.

The reset advantage is also not currently a within-branch law. Once final `v2`
and middle `v2` are both fixed, the reset formula is the ordinary exact 3-step
Collatz formula. The remaining proof pressure is to explain the branch-2
occupancy advantage among leftmost divisor-count minimizers.

## Output

```text
output/collatz_pgs_short_block_reset_candidate_probe/summary.json
output/collatz_pgs_short_block_reset_candidate_probe/target_rows.jsonl
output/collatz_pgs_short_block_reset_candidate_probe/class_rows.jsonl
output/collatz_pgs_short_block_reset_candidate_probe/branch_rows.jsonl
output/collatz_pgs_short_block_reset_candidate_probe/gap_width_rows.jsonl
output/collatz_pgs_short_block_reset_candidate_probe/residue_gap_width_rows.jsonl
```
