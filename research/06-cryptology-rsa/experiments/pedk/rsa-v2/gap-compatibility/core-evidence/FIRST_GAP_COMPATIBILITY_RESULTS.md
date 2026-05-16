# First PEDK Gap Compatibility Search Results

## Status

This is a measured sidecar result for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It is not an audit
claim. The experiment uses known `(N, p, q)` triples only to label
factor-neighborhood gap types while searching for compatibility patterns.

## Experiment

Script:

```text
first_gap_compatibility_check.py
```

Output directory:

```text
output/gap_compatibility_search/
```

The script constructs a deterministic small semiprime corpus from exact
divisor-count endpoints:

```text
min_factor = 31
max_factor = 600
max_factor_ratio = 4/1
```

For each known triple, it records:

- the PGS reduced state of the gap containing `N`;
- the left and right PGS reduced states around `p`;
- the left and right PGS reduced states around `q`;
- the unordered factor-neighborhood signature;
- the compatibility key from `gap(N)` type to factor-neighborhood signature.

The script uses the existing PGS grammar machinery from
`modulus_gap_grammar_probe.py`. It does not use primality APIs, random search,
`gcd`, product closure as a selection rule, or audit labels as inference.

## Corpus Size

The first run produced:

```text
semiprime_triple_count = 3834
corpus_row_count = 3834
n_containing_state_count = 9
factor_neighborhood_signature_count = 45
observed_compatibility_count = 276
candidate_exclusion_count = 13
position_bucket_count = 10
positioned_n_state_count = 70
observed_positioned_compatibility_count = 1364
candidate_positioned_exclusion_count = 306
supported_positioned_n_state_count = 28
phased_n_state_count = 33
observed_phased_compatibility_count = 663
candidate_phased_exclusion_count = 64
supported_phased_n_state_count = 12
factor_phased_neighborhood_signature_count = 483
observed_phased_factor_compatibility_count = 2103
min_support_for_exclusion = 50
```

The public `gap(N)` types with support at least `50` were:

```text
o2_d4_odd|d<=4   -> 1321 rows
o4_d4_odd|d<=4   -> 1094 rows
o6_d4_odd|d<=4   -> 715 rows
o4_d4_even|d<=4  -> 325 rows
o6_d4_even|d<=4  -> 261 rows
o2_d4_even|d<=4  -> 95 rows
```

## First Compatibility Signal

The first small-scale signal is that public `gap(N)` type changes the set of
factor-neighborhood signatures observed in the corpus.

The broad odd `d4` public states have near-complete observed compatibility:

```text
o2_d4_odd|d<=4 -> observed 45 / 45 factor signatures
o6_d4_odd|d<=4 -> observed 45 / 45 factor signatures
o4_d4_odd|d<=4 -> observed 44 / 45 factor signatures
```

The even `d4` public states show exclusions:

```text
o4_d4_even|d<=4 -> observed 44 / 45 factor signatures
o6_d4_even|d<=4 -> observed 43 / 45 factor signatures
o2_d4_even|d<=4 -> observed 36 / 45 factor signatures
```

This does not prove incompatibility. It gives the first measured search target:
even public `d4` gap states appear more restrictive than odd public `d4` gap
states in this small corpus.

## Position Refinement

The second pass adds the public location of `N` inside its containing gap.

For a containing gap with left endpoint `L`, right endpoint `R`, and modulus
coordinate `N`, the script records:

```text
offset_from_left = N - L
offset_from_right = R - N
gap_width = R - L
position_mpermille = floor(1000 * offset_from_left / gap_width)
position_bucket = one of ten buckets from pos000_099 through pos900_999
```

The positioned public state is:

```text
gap(N) reduced state + position bucket
```

Example:

```text
o4_d4_odd|d<=4@pos600_699
```

The strongest positioned states by support were:

```text
o2_d4_odd|d<=4@pos100_199 -> 244 rows, 38 / 45 signatures observed
o4_d4_odd|d<=4@pos600_699 -> 230 rows, 41 / 45 signatures observed
o2_d4_odd|d<=4@pos300_399 -> 171 rows, 38 / 45 signatures observed
o2_d4_odd|d<=4@pos200_299 -> 170 rows, 38 / 45 signatures observed
o4_d4_odd|d<=4@pos400_499 -> 167 rows, 37 / 45 signatures observed
o6_d4_odd|d<=4@pos700_799 -> 160 rows, 40 / 45 signatures observed
```

Position therefore adds real separation: broad reduced states split into
substates with narrower observed factor-neighborhood sets.

The narrowest supported positioned states in this run were:

```text
o2_d4_odd|d<=4@pos000_099 -> 67 rows, 25 / 45 signatures observed
o4_d4_even|d<=4@pos400_499 -> 56 rows, 25 / 45 signatures observed
o4_d4_odd|d<=4@pos700_799 -> 69 rows, 28 / 45 signatures observed
o6_d4_odd|d<=4@pos200_299 -> 55 rows, 28 / 45 signatures observed
o6_d4_even|d<=4@pos500_599 -> 53 rows, 28 / 45 signatures observed
```

This confirms that relative position belongs in the next compatibility search.
It also increases sparsity. The 306 positioned candidate exclusions are search
targets, not promoted incompatibility rules.

## Coarse Phase Refinement

The decile position surface is useful, but it is too fine for first-pass rule
search. The script therefore also records a coarse phase:

```text
early      -> position_mpermille < 250
mid        -> 250 <= position_mpermille < 750
late       -> 750 <= position_mpermille < 900
very_late  -> 900 <= position_mpermille
```

This phase layer preserves the late-position signal while reducing sparsity:

```text
positioned_n_state_count = 70
phased_n_state_count = 33

candidate_positioned_exclusion_count = 306
candidate_phased_exclusion_count = 64

factor_positioned_neighborhood_signature_count = 2074
factor_phased_neighborhood_signature_count = 483
```

The supported public phase states were led by:

```text
o2_d4_odd|d<=4@mid    -> 766 rows
o4_d4_odd|d<=4@mid    -> 735 rows
o6_d4_odd|d<=4@mid    -> 461 rows
o2_d4_odd|d<=4@early  -> 353 rows
o4_d4_even|d<=4@mid   -> 223 rows
o6_d4_odd|d<=4@late   -> 184 rows
o6_d4_even|d<=4@mid   -> 168 rows
o4_d4_odd|d<=4@late   -> 163 rows
o2_d4_odd|d<=4@late   -> 163 rows
```

The phase surface preserves the same structural theme:

```text
mid odd d4 public states remain broad-compatible;
late odd d4 public states lose more factor-neighborhood signatures;
even d4 public states remain more restrictive than odd d4 public states.
```

Examples:

```text
o4_d4_odd|d<=4@mid  -> 735 rows, 44 / 45 signatures observed
o6_d4_odd|d<=4@mid  -> 461 rows, 43 / 45 signatures observed
o2_d4_odd|d<=4@late -> 163 rows, 36 / 45 signatures observed
o4_d4_odd|d<=4@late -> 163 rows, 39 / 45 signatures observed
o6_d4_even|d<=4@late -> 75 rows, 32 / 45 signatures observed
o2_d4_even|d<=4@mid -> 65 rows, 34 / 45 signatures observed
```

The factor side is now recorded in two ways:

```text
factor_positioned_neighborhood_signature
factor_phased_neighborhood_signature
```

The decile factor-position signature is too sparse for exclusion mining in this
corpus. The coarse factor-phase signature is useful for compatibility counting,
but it is still sidecar evidence rather than a rule.

## Strong Candidate Exclusions

The strongest single absence by support is:

```text
gap(N) type:
  o4_d4_odd|d<=4

absent factor-neighborhood signature:
  L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
  ||
  L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4

n_state_support = 1094
observed_signature_count_for_n_state = 44 / 45
```

The same all-`o6/o6` factor-neighborhood signature is also absent for:

```text
o4_d4_even|d<=4
n_state_support = 325
observed_signature_count_for_n_state = 44 / 45
```

The most restrictive supported public state is:

```text
o2_d4_even|d<=4
n_state_support = 95
observed_signature_count_for_n_state = 36 / 45
candidate_exclusion_count = 9
```

Those nine absent signatures are all factor-neighborhood signatures built from
repeated or heavily `o4/o6` factor-side gap states. This is the first concrete
candidate compatibility family to test on a larger corpus.

## Current Interpretation

The hypothesis is now empirically engaged.

The corpus does not show that every `gap(N)` type has a narrow compatibility
set. It shows a more specific first pattern:

```text
odd d4 public N-gap states are broad-compatible in this small corpus;
even d4 public N-gap states are more exclusionary;
some high-o6 factor-neighborhood signatures are absent from supported N-gap
states.
```

This is a measured correlation surface. It should remain a sidecar until it is
tested under scale expansion and holdout splits.

## Next Validation Target

The next validation target is to rerun the same script at a larger exact scale
and check whether the 13 reduced-state candidate exclusions persist, especially:

```text
o4_d4_odd|d<=4 excludes all-o6/o6 factor-neighborhood pairs
o4_d4_even|d<=4 excludes all-o6/o6 factor-neighborhood pairs
o2_d4_even|d<=4 has a restricted factor-neighborhood signature set
```

The same larger run should also check whether positioned states preserve their
narrower observed signature sets under increased support.

The phase surface should be the next primary surface for scale-up because it
captures the late-position signal with less sparsity than decile buckets.

Promotion to a PEDK rule requires held-out preservation. No exclusion in this
file is a live inference rule yet.
