# Preliminary PEDK Candidate Exclusion Rule

## Status

This is a preliminary sidecar rule for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It does not identify
`p` or `q`. It does not close a factor pair. It formalizes the first measured
compatibility exclusions so they can be tested unchanged on larger exact
corpora.

## Observable Objects

A semiprime modulus `N = pq` sits inside a public PGS gap:

```text
L_N < N < R_N
```

where `L_N` and `R_N` are public endpoints in the ordered prime-gap structure.

The public modulus gap gives two measurements:

```text
reduced_state(gap(N))
phase(N in gap(N))
```

The phase is computed from the position of `N` inside the containing gap:

```text
position_mpermille = floor(1000 * (N - L_N) / (R_N - L_N))
```

The coarse phase map is:

```text
early      -> position_mpermille < 250
mid        -> 250 <= position_mpermille < 750
late       -> 750 <= position_mpermille < 900
very_late  -> 900 <= position_mpermille
```

The public phase state is:

```text
S(N) = reduced_state(gap(N)) @ phase(N in gap(N))
```

Example:

```text
o2_d4_odd|d<=4@late
```

For corpus labeling only, each known factor endpoint has a left and right
neighboring PGS gap. The unordered pair of those two factor neighborhoods gives
a factor-neighborhood signature:

```text
F(p, q)
```

This factor-neighborhood signature is downstream label data. It is not available
to live public inference until a candidate factor location has already been
proposed by some other public mechanism.

## Candidate Rule

Let `C` be the measured corpus.

For a public phase state `S`, define:

```text
Rows(S) = { row in C : S(row.N) = S }
Obs(S) = { F(row.p, row.q) : row in Rows(S) }
AllF = { F(row.p, row.q) : row in C }
```

With support threshold:

```text
min_support = 50
```

the preliminary exclusion set is:

```text
Excl(S) = AllF \ Obs(S), if |Rows(S)| >= min_support.
```

Candidate exclusion statement:

```text
If S(N) = S and F is in Excl(S), then F is a candidate-incompatible
factor-neighborhood signature for public phase state S.
```

The rule excludes a factor-neighborhood signature class, not a factor.

## Current Measured Candidate Set

The current corpus has:

```text
semiprime_triple_count = 3834
factor_neighborhood_signature_count = 45
phased_n_state_count = 33
supported_phased_n_state_count = 12
candidate_phased_exclusion_count = 64
min_support = 50
```

The supported public phase states with candidate exclusions are:

```text
o4_d4_odd|d<=4@mid    -> 735 rows, 44 / 45 signatures observed
o6_d4_odd|d<=4@mid    -> 461 rows, 43 / 45 signatures observed
o2_d4_odd|d<=4@early  -> 353 rows, 43 / 45 signatures observed
o4_d4_even|d<=4@mid   -> 223 rows, 40 / 45 signatures observed
o6_d4_odd|d<=4@late   -> 184 rows, 41 / 45 signatures observed
o6_d4_even|d<=4@mid   -> 168 rows, 41 / 45 signatures observed
o2_d4_odd|d<=4@late   -> 163 rows, 36 / 45 signatures observed
o4_d4_odd|d<=4@late   -> 163 rows, 39 / 45 signatures observed
o4_d4_odd|d<=4@early  -> 156 rows, 38 / 45 signatures observed
o6_d4_even|d<=4@late  -> 75 rows, 32 / 45 signatures observed
o2_d4_even|d<=4@mid   -> 65 rows, 34 / 45 signatures observed
```

The most important candidate family is:

```text
late or even public d4 states exclude more heavily o4/o6 factor-neighborhood
signatures than mid odd d4 states.
```

One high-support example:

```text
S = o4_d4_odd|d<=4@mid
support = 735
observed = 44 / 45

candidate excluded signature:
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
||
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
```

A more restrictive late-state example:

```text
S = o2_d4_odd|d<=4@late
support = 163
observed = 36 / 45
candidate exclusions = 9
```

## Machine-Readable Artifact

The experiment emits the rule as:

```text
output/gap_compatibility_search/preliminary_candidate_exclusion_rule.json
```

That artifact contains:

```text
candidate_rule_id = pedk_phase_gap_exclusion_candidate_v1
status = candidate_sidecar_rule_not_live_pedk_inference
source_rule_id = pedk_gap_compatibility_search_v1
exclusions_by_public_phase_state = {...}
```

## Falsification

One held-out row falsifies a candidate exclusion for state `S` if:

```text
S(row.N) = S
F(row.p, row.q) is in Excl(S)
```

That exclusion must then be removed from the candidate set.

The candidate rule itself survives only if a nontrivial subset of exclusions
persists under scale expansion and held-out testing.

## Promotion Boundary

Promotion to a live PEDK exclusion requires:

```text
same public phase-state definition;
larger exact corpus;
held-out validation;
zero falsifying held-out rows for each promoted exclusion;
physical separation between audit labels and live inference;
explicit unresolved state when no public candidate factor neighborhood is
available.
```

Until then, the rule is a measured compatibility sidecar.
