# Transported Story Law Proof Obligations

This file is the proof-facing workbench for `transported_story_law_v1`.

The implemented sidecar has already shown that the recursive transported
elimination surface is computable from public PGSPG certificate stories alone.
The remaining task is mathematical: derive the elimination predicates from the
core PGSPG laws.

## Status

The current result is a measured public relation, not a theorem and not a
resolver.

The official RSA v2 runner still returns:

```text
rsa_v2_40bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
```

The proof target is:

```text
PGSPG certificate story
+ reciprocal floor transport
+ induced opposite certificate
+ GWR/NLSC
=> transported prefix, suffix, and recurrence elimination
```

## Global Picture

For a public modulus `N`, the sidecar constructs PGSPG certificates from public
endpoint anchors, transports distinguished certificate points through:

```text
T_N(x) = floor(N / x)
```

and derives the induced opposite certificate from the transported reset
coordinate.

The current measured surface is:

```text
row_count = 512
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
```

The measurement means:

```text
512 public certificate-story rows
-> 202 effective transported survivors after prefix/suffix/stale filtering
-> 713 recursive story-law rows across three layers
-> 0 final recursive survivors
```

This collapse is evidence that the public certificate story carries the
transported structure. It does not prove the predicates. The lemmas below are
the exact proof obligations.

## Public Objects

Let `C` be a public PGSPG chamber-reset certificate for `N`.

Use the following notation:

```text
a(C) = certificate anchor
w(C) = carrier point
r(C) = reset endpoint
d(C) = reset deadline
lambda(C) = lock-carrier divisor-count label
T_N(x) = floor(N / x)
```

The induced opposite certificate `C'` is the public certificate obtained from
the previous endpoint before `T_N(r(C))`.

Define the transported intervals:

```text
I_prefix(C) = [T_N(r(C)), T_N(w(C))]
I_suffix(C) = [T_N(d(C)), T_N(r(C))]
```

Both intervals are closed and endpoint-sorted in implementation because `T_N`
is order-reversing.

Allowed public objects are:

```text
N
a(C), w(C), r(C), d(C), lambda(C)
T_N(a public certificate point)
C'
a(C'), w(C'), r(C'), d(C'), lambda(C')
public recursive endpoint-chain state
public reduced grammar signatures
```

Forbidden as proof inputs:

```text
gcd
N % x
product closure
hidden factors
audit factors
primality APIs
factor APIs
random search
fallback search
```

## Lemma 1: Prefix Non-Rewrite Lemma

### Formal Statement

For a valid transported reciprocal certificate state, the induced carrier cannot
occupy the transported prefix interval with non-increasing lock label:

```text
w(C') in I_prefix(C) and lambda(C') <= lambda(C)
=> C' is excluded as a new valid transported frontier state.
```

### Allowed Public Objects

```text
C
C'
w(C')
I_prefix(C)
lambda(C)
lambda(C')
```

### Measured Support

In the current `transported_story_law_v1` surface:

```text
ledger_prefix_elimination_count = 101
```

These 101 rows are eliminated by this predicate.

### Proof Obligation Against GWR/NLSC

Derive that a carrier selected in the transported prefix interval with
`lambda(C') <= lambda(C)` rewrites an already committed carrier-to-reset segment
of `C`. Under GWR/NLSC, that rewrite must contradict the leftmost
minimum-divisor carrier commitment or the no-later-simpler-closure condition
inside the transported chamber.

### Falsification Condition

A public certificate pair falsifies this lemma if:

```text
w(C') in I_prefix(C)
lambda(C') <= lambda(C)
C' remains a valid new transported frontier state under GWR/NLSC
```

### Finite vs Universal Status

Finite support exists for the current 512-row public surface. The universal lift
over all valid PGSPG certificates is unproved.

## Lemma 2: Suffix Strict-Descent Lemma

### Formal Statement

For a valid transported reciprocal certificate state, the induced carrier cannot
occupy the transported suffix interval with strictly smaller lock label:

```text
w(C') in I_suffix(C) and lambda(C') < lambda(C)
=> C' is excluded as a new valid transported frontier state.
```

### Allowed Public Objects

```text
C
C'
w(C')
I_suffix(C)
lambda(C)
lambda(C')
```

### Measured Support

In the current `transported_story_law_v1` surface:

```text
ledger_suffix_elimination_count = 16
```

These 16 rows are eliminated by this predicate.

### Proof Obligation Against GWR/NLSC

Derive that a strictly smaller lock label inside the transported suffix interval
would create a later simpler carrier inside a segment whose reset-to-deadline
story is already committed by `C`. Under NLSC, the transported chamber cannot
admit that strict descent as a valid new frontier state.

### Falsification Condition

A public certificate pair falsifies this lemma if:

```text
w(C') in I_suffix(C)
lambda(C') < lambda(C)
C' remains a valid new transported frontier state under GWR/NLSC
```

### Finite vs Universal Status

Finite support exists for the current 512-row public surface. The universal lift
over all valid PGSPG certificates is unproved.

## Lemma 3: Recursive Anchor Recurrence Lemma

### Formal Statement

A transported state whose induced anchor has already appeared on the recursive
frontier is not a new public frontier state:

```text
a(C') in prior_recursive_frontier
=> C' is a recurrent state, not a new transported survivor.
```

### Allowed Public Objects

```text
C
C'
a(C')
the ordered set of prior recursive frontier anchors
```

### Measured Support

In the current `transported_story_law_v1` recursive surface:

```text
depth 0 recursive survivors = 200
depth 1 recursive cycle states = 199
depth 2 recursive cycle states = 1
recursive_final_survivor_count = 0
```

This recurrence rule accounts for the recursive collapse after the direct
prefix and suffix eliminations have selected the effective transported
survivors.

### Proof Obligation Against GWR/NLSC

Derive that recurrence under `T_N(r(C))` contributes no new PGSPG chamber
commitment. The repeated anchor must represent a previously measured public
certificate state rather than a new reciprocal closure state.

### Falsification Condition

A public recursive frontier falsifies this lemma if:

```text
a(C') has already appeared on the frontier
C' nevertheless supplies a new valid PGSPG commitment state
```

### Finite vs Universal Status

Finite support exists for the current recursive surface of 713 rows. The
universal lift over all transported certificate graphs is unproved.

## Lemma 4: Grammar Projection Lemma

### Formal Statement

The transported story conflict has a reduced grammar projection: solved
target-side rows may share individual lag-2 or lag-3 components with the
expanded surface, but they do not reproduce the expanded surface's ordered
combined lag-2 plus lag-3 word.

```text
component sharing is allowed
ordered lag-2 + lag-3 collision is excluded
```

### Allowed Public Objects

```text
public endpoint-chain grammar rows
lag-2 reduced signature
lag-3 reduced signature
ordered lag-2 + lag-3 reduced word
commitment story projection rows
```

### Measured Support

Current solved-surface grammar evidence:

```text
solved rows = 48
lag-2 hits = 30
lag-3 hits = 29
ordered lag-2 + lag-3 word hits = 0
full recursive reduced-word hits = 0
component-sharing word exclusions = 40
```

Fresh RSA-100 target evidence:

```text
solved target rows = 2
lag-2 hits = 2
lag-3 hits = 1
ordered lag-2 + lag-3 word hits = 0
full recursive reduced-word hits = 0
component-sharing word exclusions = 2
```

The `commitment_story_word_projection_v1` bridge preserves:

```text
projected_lag23_collision_count = 0
fresh_rsa_100_lag23_collision_count = 0
```

### Proof Obligation Against GWR/NLSC

Derive that the ordered recursive word collision would encode the same kind of
transported story rewrite prohibited by the prefix and suffix lemmas. The proof
must show that the lag-2 plus lag-3 exclusion is the reduced grammar image of
the same PGSPG carrier/reset/deadline commitment law.

### Falsification Condition

A public grammar row falsifies this lemma if:

```text
it is a valid transported story state
it reproduces an ordered lag-2 + lag-3 expanded-surface word
and it does not violate prefix, suffix, or recurrence constraints
```

### Finite vs Universal Status

Finite support exists for the solved low-regime and fresh RSA-100 grammar
surfaces. The universal grammar projection theorem is unproved.

## Current Proof Boundary

The current theorem status is:

```text
PGSPG local laws: proved in PROOF.md under their stated hypotheses
transported_story_law_v1 collapse: measured public evidence
prefix/suffix/recurrence elimination: unproved proof obligations
grammar projection: measured bridge, not proved
official PGSMD status: unresolved
```

The next mathematical task is not another ledger search. It is to derive Lemma
1 and Lemma 2 from GWR/NLSC. Lemma 3 then gives the recursive frontier
interpretation, and Lemma 4 connects the result to the reduced grammar evidence.

