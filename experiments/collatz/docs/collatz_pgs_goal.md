# Collatz-PGS Research Goal

## Goal

Determine whether PGS-selected same-gap witness contact predicts Collatz
first-descent reset behavior.

Current working target: leave broad reset-profile measurement and attack the
short-block terminal-residue families algebraically. The reset-certificate
experiment has measured same-gap enrichment, separated the reset profiles,
localized the positive median carrier to below-minimizer terminal adjacency,
and put that terminal-adjacent carrier into an exact Collatz residue normal
form. The exact 3-step, final-`v2` `4` and `8` surface has now reduced to a
two-branch inverse formula. The universal branch-selection version is false:
a targeted inverse scan through odd seeds `<= 100000000` found branch-1
counterexamples. The live target is now the branch-occupancy imbalance:
below-minimizer hits strongly favor the doubled reset branch.

The object under study is the accelerated odd Collatz map:

$$C(n)=\frac{3n+1}{2^{v_2(3n+1)}}$$

## Definitions

For an odd seed `s`, a first-descent block is the finite list of accelerated
odd Collatz transitions beginning at `s` and ending at the first odd target
`t < s`.

The first-descent block length is the number of accelerated odd transitions in
that list, including the final transition to `t`.

The reset strength is:

$$R(s)=\frac{s}{t}$$

where `t` is the first odd target below the seed `s`.

The terminal source is the final odd source state in the block, immediately
before the first target below `s`.

For consecutive primes `p < q`, the leftmost divisor-count minimizer `w` is
the first integer in the open interval `p < n < q` whose divisor count is
minimal over that interval.

The odd cells nearest the minimizer are the odd interior cells among
`w - 1`, `w`, and `w + 1`.

The same-gap background rate replaces each visited composite source with all
odd interior cells of its own containing prime gap, excludes prime endpoints,
and counts the share of those odd cells that are nearest to the same `w`.

For an odd seed `s`, follow odd source states until the first target below
`s`. For each source state, attach its containing prime gap, exact divisor
count, PGS witness, endpoint status, same-gap witness distance, and transition
`v2`.

The next research target is not only whether Collatz source states visit PGS
witness positions above same-gap background. That is already measured at
`3 <= s <= 999999`. The next target is whether the short-block terminal
families yield a closed reset inequality rather than only a matched empirical
reset advantage.

## Current Evidence

The same-gap scale probe reached `1000000`:

| Measurement | Ratio |
|---|---:|
| Source composite odd-projected witness hit rate versus same-gap background | `1.7637165846198448` |
| `v2=1` same-gap witness ratio | `1.9275212321500066` |
| `v2=2` same-gap witness ratio | `1.5582563147270216` |
| `v2=3-4` same-gap witness ratio | `1.6324415254370295` |
| `v2>=5` same-gap witness ratio | `1.659162945066948` |

Witness-contact blocks had median reset strength `2.078632113914513`; no-
witness-contact blocks had median reset strength `1.8728822607686915`.

The reset length-strata probe compared blocks only inside exact
`odd_steps_to_first_descent` strata. Witness-contact median reset was higher in
`19` matched strata; no-witness-contact median reset was higher in `18` matched
strata. The matched-weighted mean of stratum median reset ratios was
`1.6163417109769`, and the matched-weighted mean of stratum P90 reset deltas
was `-0.028322861082362694`.

The reset carrier-strata probe localized the positive matched reset effect.
Exact steps `1`, `2`, and `3` supplied the three largest positive delta
contributions: `0.4382401881898264`, `0.23780172921923806`, and
`0.23673527139383527`. Exact steps `4`, `5`, and `6` supplied the three
largest negative delta contributions: `-0.14396095926820723`,
`-0.11366913299919518`, and `-0.056179924837349154`. Favorable strata carried
matched weight share `0.7457362101345207`; unfavorable strata carried matched
weight share `0.25426378986547926`.

The source-position carrier probe found the carrier mechanism candidate.
Favorable strata had matched-weighted final-source witness hit rate
`0.6330294377004576`; unfavorable strata had `0.2518013666558681`. Favorable
strata also carried matched-weighted median final-`v2` delta
`0.5953211176443776`, while unfavorable strata were nearly flat at
`0.004912937401824805`.

The terminal contact decomposition probe matched blocks inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Terminal witness contact
remained positive against no-witness blocks with matched-weighted mean of
stratum median reset delta `0.33031631110499143` and ratio
`1.0401652897967644`. Nonterminal-only witness contact also remained mildly
positive against no-witness blocks with matched-weighted mean delta
`0.3036864937903315`, so the effect is not terminal-only.

The terminal geometry probe found that positive terminal carriers are a
smaller, sharper subset. They carry matched weight share
`0.2431613157089351` and weighted mean of stratum median reset delta
`1.7526101771071119`; negative terminal carriers carry matched weight share
`0.7568386842910649` and delta `-0.12664612350652749`. Positive carriers also
have higher terminal exact-witness hit rate: `0.8720123654427132` versus
`0.7452117085795563`.

The terminal exact-versus-adjacent probe split terminal contact into exact
witness hits and adjacent projected witness hits, still matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Exact terminal hits remained
positive against no-witness blocks with weighted mean of stratum median reset
delta `0.22135903401835988` and ratio `1.0430527903690756`. Adjacent projected
terminal hits were stronger against no-witness blocks with delta
`0.4047035698439424` and ratio `1.0756384568540225`. Exact terminal hits did
not beat adjacent projected terminal hits directly: exact-vs-adjacent delta
was `-0.29644357588214204` and ratio `0.9803814153462154`.

The terminal adjacent-side probe split adjacent projected terminal hits into
final sources at `witness - 1` and `witness + 1`, still matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata. Below-witness terminal hits
beat above-witness terminal hits directly with weighted mean of stratum median
reset delta `0.9934374958512522` and ratio `1.1600562928929092`.
Below-witness terminal hits remained positive against no-witness blocks with
delta `0.48311171458205104` and ratio `1.0866506651606216`. Above-witness
terminal hits did not carry the median-reset delta against no-witness blocks:
their delta was `-0.20290860147945028`.

The below-witness stability probe kept the same exact
`(odd_steps_to_first_descent, final_v2)` matching and measured median, P90, and
P99 reset-strength deltas. Below-witness terminal hits were stable against
above-witness terminal hits at all three levels: median delta
`0.9934374958512522`, P90 delta `0.9997759684812527`, and P99 delta
`0.9754731838240228`. Against no-witness blocks, below-witness contact was
median-positive with delta `0.48311171458205104`, but tail-negative with P90
delta `-0.06565152576687666` and P99 delta `-0.08685398078967067`.

The below-witness exact-family probe decomposed the below-vs-no-witness result
by exact `(odd_steps_to_first_descent, final_v2)` families. It conserved the
stability-probe aggregate exactly across `175` matched families and total
matched weight `12813`: median contribution `0.48311171458205115`, P90
contribution `-0.06565152576687669`, and P99 contribution
`-0.08685398078967059`. Exact step `1` carried `0.7998907359712791` of the
matched weight but almost no contribution. Exact step `3` carried the main
positive median contribution: `0.2734251548497368` from matched weight `1064`.
The sign pattern `positive_positive_positive` carried matched weight share
`0.056817294934831813` and contributed `0.2199992755453345` to the median
delta and `0.05122416092527163` to the P99 delta. The sign pattern
`negative_negative_negative` carried matched weight share
`0.28455474908296263` and contributed `-0.09483951129888446` to the P99 tail.

The terminal adjacent residue probe verified the exact residue normal form
behind the side split. Across `15558` terminal adjacent rows, the PGS witness
matched the forced Collatz residue modulo `2^k`, the exact-`v2`
non-overdivisibility check, the recomputed `v2`, and the terminal target at
rate `1.0`. For a below-witness terminal source `n=w-1`,

$$C(w-1)=\frac{3w-2}{2^{k}}$$

and the exact final exponent condition is:

$$3w \equiv 2 \pmod {2^{k}}$$

$$3w \not\equiv 2 \pmod {2^{k+1}}$$

Equivalently, the witness satisfies:

$$w \equiv 2\cdot 3^{-1}\pmod {2^{k}}$$

For an above-witness terminal source `n=w+1`,

$$C(w+1)=\frac{3w+4}{2^{k}}$$

and the exact final exponent condition is:

$$3w \equiv -4 \pmod {2^{k}}$$

$$3w \not\equiv -4 \pmod {2^{k+1}}$$

Equivalently, the witness satisfies:

$$w \equiv -4\cdot 3^{-1}\pmod {2^{k}}$$

This gives terminal adjacent PGS contact its exact Collatz residue normal form
on the PGS witness.

The short-block reset candidate probe extracted the exact 3-step, final-`v2`
`4` and `8` target surface. It found `249` rows, all with first transition
`v2=1`, middle transition `v2` in `{1, 2}`, zero seed-formula failures, and
zero reset-formula failures. The below-minimizer terminal subset had `6` rows:
`5` at final `v2=4` and `1` at final `v2=8`. All `6` were on the
`middle_v2=2`, `w mod 9 = 5` inverse branch, with exact below-residue rate
`1.0`.

Against all no-witness controls in the exact 3-step, final-`v2` target
surface, below-minimizer terminal rows showed near-`2x` median reset:
`1.999948151743171` at final `v2=4` and `1.9997055127510488` at final
`v2=8`. Inside the fixed `middle_v2=2` branch, that extra separation collapsed:
the ratios were `1.0000093335242783` at final `v2=4` and
`0.9998475550817735` at final `v2=8`. The result identifies the current
mechanism as branch selection, not a separate within-branch reset law.

The short-block branch counterexample probe then inverted the exact 3-step
formulas directly through odd seeds `<= 100000000`. It found branch-1
counterexamples, so the universal claim that below-minimizer terminal contact
always selects the `w mod 9 = 5` branch is false. The first branch-1
counterexample is:

| Field | Value |
|---|---:|
| seed | `6000471` |
| witness `w` | `13501062` |
| terminal source `w-1` | `13501061` |
| final `v2` | `4` |
| middle `v2` | `1` |
| reset strength | `2.3703700923858233` |

The branch imbalance remained large:

| Family | Candidate count | Hit count | Hit rate |
|---|---:|---:|---:|
| `k=4`, branch `1` | `781250` | `36` | `0.00004608` |
| `k=4`, branch `2` | `390625` | `11510` | `0.0294656` |
| `k=8`, branch `1` | `48828` | `5` | `0.00010240026214467109` |
| `k=8`, branch `2` | `24415` | `708` | `0.028998566455048128` |

This changes the proof target from absolute branch selection to a distribution
law for leftmost divisor-count minimizers across the two inverse residue
branches.

The `20000` first-descent surface measured:

| Measurement | Ratio |
|---|---:|
| Source prime endpoint hit rate versus deterministic block background | `1.7087413960199178` |
| Source composite odd-projected witness hit rate versus same-gap background | `1.589006897032753` |
| Final-source composite odd-projected witness hit rate versus same-gap background | `1.4802996732650835` |

The same-gap witness ratio by transition `v2` stratum is:

| `v2(3n+1)` stratum | Ratio |
|---|---:|
| `1` | `1.7529488673287874` |
| `2` | `1.4675000302182195` |
| `3-4` | `1.3810570046013555` |
| `>=5` | `1.3912139699704087` |

These measurements justify treating PGS witness contact as a live Collatz
block variable.

## Current Plan Position

1. Same-gap witness enrichment at `1000000`: complete.
2. Reset-profile split by witness-contact block class: complete.
3. Exact odd-step matched reset comparison: complete.
4. Carrier-strata and coarse `v2` composition probe: complete.
5. PGS source-position pattern inside favorable carrier strata: complete.
6. Terminal witness-contact split under exact-step and final-`v2` matching:
   complete.
7. Terminal-contact geometry by reset magnitude or final-source prime-gap
   state: complete.
8. Exact terminal witness hits versus adjacent projected terminal hits under
   exact-step and final-`v2` matching: complete.
9. Adjacent terminal side split under exact-step and final-`v2` matching:
   complete.
10. Below-witness terminal carrier sign and tail-stability check: complete.
11. Below-vs-no-witness exact carrier-family decomposition: complete.
12. Terminal adjacent Collatz-residue identity check: complete.
13. Exact 3-step final-`v2` `4`/`8` branch algebra and reset-candidate
   extraction: complete.
14. Targeted inverse scan for branch-1 counterexamples through `100000000`:
   complete; universal branch selection is false.
15. Explain the branch-2 occupancy advantage among inverse-eligible
   witnesses: next.

## Primary Question

For first-descent blocks, does PGS witness contact predict stronger reset?

Use the reset measurement `R(s)=s/t`.

Compare blocks with at least one composite source at odd-projected witness
distance `0` against blocks with no such source. Measure:

- median `R(s)`;
- upper-tail `R(s)`;
- odd steps to first descent;
- maximum source over seed;
- final-source witness contact rate.

## Success Criterion

The broad reset-certificate experiment has already met its empirical success
criterion: same-gap witness enrichment remains above background at scale, and
witness-contact blocks have a distinct reset profile.

The strongest next positive result would now be:

```text
below-minimizer terminal contact in the exact 3-step final-v2 4/8 surface
has a provable branch-occupancy advantage for the doubled inverse branch.
```

## Invalidated Path

Do not pursue a one-step prime-rank monovariant. Accelerated odd Collatz steps
such as `3 -> 5`, `7 -> 11`, and `27 -> 41` move upward in prime-ladder
position.

## Next Artifact

The same-gap-only scale probe exists:

```text
scripts/collatz_pgs_same_gap_scale_probe.py
```

The reset length-strata probe exists:

```text
scripts/collatz_pgs_reset_length_strata_probe.py
```

The reset carrier-strata probe exists:

```text
scripts/collatz_pgs_reset_carrier_strata_probe.py
```

The source-position carrier probe exists:

```text
scripts/collatz_pgs_source_position_carrier_probe.py
```

The terminal contact decomposition probe exists:

```text
scripts/collatz_pgs_terminal_contact_decomposition_probe.py
```

The terminal geometry probe exists:

```text
scripts/collatz_pgs_terminal_geometry_probe.py
```

The terminal exact-versus-adjacent probe exists:

```text
scripts/collatz_pgs_terminal_exact_vs_adjacent_probe.py
```

The terminal adjacent-side probe exists:

```text
scripts/collatz_pgs_terminal_adjacent_side_probe.py
```

The below-witness stability probe exists:

```text
scripts/collatz_pgs_below_witness_stability_probe.py
```

The below-witness family probe exists:

```text
scripts/collatz_pgs_below_witness_family_probe.py
```

The terminal adjacent residue probe exists:

```text
scripts/collatz_pgs_terminal_adjacent_residue_probe.py
```

The short-block reset candidate probe exists:

```text
scripts/collatz_pgs_short_block_reset_candidate_probe.py
```

The short-block branch counterexample probe exists:

```text
scripts/collatz_pgs_short_block_branch_counterexample_probe.py
```

The next question is why inverse-eligible witnesses on the `middle_v2=2`,
`w mod 9 = 5` branch become below-minimizer terminal hits far more often than
inverse-eligible witnesses on the `middle_v2=1`, `w mod 9 = 0` branch.
