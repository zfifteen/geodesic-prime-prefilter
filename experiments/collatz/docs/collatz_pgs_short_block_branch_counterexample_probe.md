# Collatz-PGS Short-Block Branch Counterexample Probe

## Summary

The universal branch-selection theorem candidate is false. A targeted inverse
scan through odd seeds `<= 100000000` found `41` below-minimizer branch-1
counterexamples in the exact 3-step, final-`v2` `4`/`8` surface.

The result does not erase the short-block mechanism. It relocates it: branch 2
is not forced, but it is dramatically overrepresented among below-minimizer
hits. Branch 2 produced `12218` hits; branch 1 produced `41`.

## Method

The probe does not sweep all Collatz orbits. It uses the exact inverse
3-step formulas.

For a below-minimizer terminal source `n=w-1`, branch 1 is:

$$s=\frac{4w-9}{9}$$

with `w mod 9 = 0`, middle `v2=1`, and reset asymptote:

$$\frac{2^{k+2}}{27}$$

Branch 2 is:

$$s=\frac{8w-13}{9}$$

with `w mod 9 = 5`, middle `v2=2`, and reset asymptote:

$$\frac{2^{k+3}}{27}$$

For final `v2` in `{4, 8}`, the probe enumerates inverse-eligible witnesses,
checks the exact final residue, constructs the seed, verifies the exact
3-step first-descent block, and then tests whether `w` is the leftmost
divisor-count minimizer in the prime gap containing `w-1`.

## Counterexample

The first branch-1 counterexample is:

| Field | Value |
|---|---:|
| seed | `6000471` |
| witness `w` | `13501062` |
| terminal source `w-1` | `13501061` |
| terminal target | `2531449` |
| final `v2` | `4` |
| middle `v2` | `1` |
| previous prime | `13501057` |
| next prime | `13501063` |
| gap width | `6` |
| witness divisor count | `12` |
| terminal divisor count | `16` |
| reset strength | `2.3703700923858233` |

This row proves that below-minimizer terminal contact does not universally
select the doubled branch.

## Branch Imbalance

The `100000000` inverse scan measured:

| Family | Candidate count | Hit count | Hit rate |
|---|---:|---:|---:|
| `k=4`, branch `1` | `781250` | `36` | `0.00004608` |
| `k=4`, branch `2` | `390625` | `11510` | `0.0294656` |
| `k=8`, branch `1` | `48828` | `5` | `0.00010240026214467109` |
| `k=8`, branch `2` | `24415` | `708` | `0.028998566455048128` |

At `k=4`, branch 2 has about `639.4444444444445` times the hit rate of
branch 1. At `k=8`, branch 2 has about `283.18877057184596` times the hit
rate of branch 1.

The branch reset scales match the exact algebra:

| Final `v2` | Branch | Hits | First seed | Median reset |
|---:|---:|---:|---:|---:|
| `4` | `1` | `36` | `6000471` | `2.370370339879278` |
| `4` | `2` | `11510` | `9675` | `4.740740657317454` |
| `8` | `1` | `5` | `25957527` | `37.925925522691756` |
| `8` | `2` | `708` | `4171` | `75.85185042289021` |

## Interpretation

The exact reset theorem is now closed at the branch level:

```text
branch 1 -> lower reset scale
branch 2 -> doubled reset scale
```

The open mathematical question is not whether branch 2 is forced. It is not.
The question is why the leftmost divisor-count minimizer becomes a
below-minimizer terminal witness vastly more often on branch 2 than branch 1.

That is a sharper target than the original universal-branch hypothesis, and it
is directly stated in conventional arithmetic terms: divisor-count minimizers
inside prime gaps are strongly imbalanced between two explicit residue branches
that have different Collatz reset scales.

## Output

```text
output/collatz_pgs_short_block_branch_probe/summary.json
output/collatz_pgs_short_block_branch_probe/hit_rows.jsonl
```
