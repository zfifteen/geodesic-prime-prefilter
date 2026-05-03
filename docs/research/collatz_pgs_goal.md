# Collatz-PGS Research Goal

## Goal

Determine whether PGS-selected same-gap witness contact predicts Collatz
first-descent reset behavior.

The object under study is the accelerated odd Collatz map:

$$C(n)=\frac{3n+1}{2^{v_2(3n+1)}}$$

For an odd seed `s`, follow odd source states until the first target below
`s`. For each source state, attach its containing prime gap, exact divisor
count, PGS witness, endpoint status, same-gap witness distance, and transition
`v2`.

The next research target is not only whether Collatz source states visit PGS
witness positions above same-gap background. That is already measured at
`3 <= s <= 19999`. The next target is whether witness contact changes the
reset profile of the block.

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
4. Carrier-strata and coarse `v2` composition probe: complete in this
   iteration.
5. PGS source-position pattern inside favorable carrier strata: next.

## Primary Question

For first-descent blocks, does PGS witness contact predict stronger reset?

Use the reset measurement:

$$R(s)=\frac{s}{t}$$

where `t` is the first odd target below the seed `s`.

Compare blocks with at least one composite source at odd-projected witness
distance `0` against blocks with no such source. Measure:

- median `R(s)`;
- upper-tail `R(s)`;
- odd steps to first descent;
- maximum source over seed;
- final-source witness contact rate.

## Success Criterion

The next probe is valuable if same-gap witness enrichment remains above
background at larger scale and witness-contact blocks have a distinct reset
profile.

The strongest next positive result would be:

```text
same-gap witness ratio remains above background at scale, and witness-contact
blocks reset harder or faster than no-witness-contact blocks.
```

## Invalidated Path

Do not pursue a one-step prime-rank monovariant. Accelerated odd Collatz steps
such as `3 -> 5`, `7 -> 11`, and `27 -> 41` move upward in prime-ladder
position.

## Next Artifact

The same-gap-only scale probe exists:

```text
benchmarks/python/predictor/collatz_pgs_same_gap_scale_probe.py
```

The reset length-strata probe exists:

```text
benchmarks/python/predictor/collatz_pgs_reset_length_strata_probe.py
```

The reset carrier-strata probe exists:

```text
benchmarks/python/predictor/collatz_pgs_reset_carrier_strata_probe.py
```

The next question is whether the favorable exact-step carrier strata share a
PGS source-position pattern beyond the block-level witness-contact label.
