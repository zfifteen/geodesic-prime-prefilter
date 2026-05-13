# Transported Certificate Invariant

## Status

This note defines the next research target for the official RSA v2 modulus
decomposer.

The current runner is unresolved. It derives public reciprocal PGSPG
certificate state from `N`, but it does not yet carry a reviewed transported
certificate invariant strong enough to select an endpoint pair.

The target is:

```text
public N
-> PGS endpoint-chain state
-> PGSPG reset certificate at each endpoint
-> floor transport x -> floor(N / x)
-> opposite-side PGSPG certificate
-> invariant closure or explicit unresolved
```

## Object

A PGSPG certificate is local endpoint-chain state. It is derived from one
public previous-endpoint anchor and records:

- `anchor`;
- `reset_endpoint`;
- `gap_offset`;
- `closed_offsets_before_q`;
- `carrier_w`;
- `carrier_d`;
- `lock_carrier_offset`;
- `lock_carrier_d`;
- `lower_d_threat_offset`;
- `tail_after_reset_offsets`;
- `reset_deadline_value`;
- `reset_deadline_margin`;
- `reset_signature`.

For a public modulus `N`, a transported certificate is the image of selected
certificate coordinates under:

```text
T_N(x) = floor(N / x)
```

The reset-to-deadline interval of a certificate `C` is:

```text
R(C) = [C.reset_endpoint, C.reset_deadline_value]
```

Its transported interval is:

```text
T_N(R(C)) =
[
  floor(N / C.reset_deadline_value),
  floor(N / C.reset_endpoint)
]
```

The order reverses because `floor(N / x)` decreases as `x` increases.

## Candidate Invariant

The invariant is not equality of raw local margins. The raw margin

```text
reset_deadline_margin = reset_deadline_value - reset_endpoint
```

is measured in the source-side coordinate scale. The reciprocal floor map does
not preserve that unit scale.

The candidate transported certificate invariant is:

```text
lower certificate C_l
-> transported interval T_N(R(C_l))
-> upper certificate C_u
-> matching upper certificate frontier class
```

and symmetrically:

```text
upper certificate C_u
-> transported interval T_N(R(C_u))
-> lower certificate C_l
-> matching lower certificate frontier class
```

The compared frontier class is the tuple:

```text
(
  reset endpoint position relative to transported interval,
  reset-deadline position relative to transported interval,
  deadline kind,
  carrier_d,
  lock_carrier_d,
  threat presence,
  first tail offset presence
)
```

where `deadline kind` is:

```text
threat   if lower_d_threat_offset supplies the reset deadline
tail     if the first tail_after_reset_offset supplies the reset deadline
bound    if candidate_bound supplies the reset deadline
```

The invariant closes only when both transported intervals land on opposite
certificate frontier classes that agree under this tuple. If either direction
does not land on a public PGSPG certificate frontier, the state is unresolved.

Closure here is structural closure. It means the public transported certificate
state itself determines a unique reciprocal endpoint-pair state.

It does not mean:

```text
candidate pair looks plausible
-> product check succeeds
-> call the result PGS closure
```

The product relation belongs only to downstream audit. If the only fact that
makes a pair special is `p * q = N`, then the transported certificate invariant
has not closed it.

## Certificate Frontier Rule

Endpoint traversal is allowed only through PGSPG output:

```text
current endpoint -> PGSPG next endpoint
```

For each endpoint on the frontier:

1. derive its PGSPG certificate from public endpoint-chain state;
2. transport only certificate coordinates through `floor(N / x)`;
3. derive the opposite certificate from the transported coordinate's previous
   public endpoint;
4. compare transported certificate frontier class;
5. return resolved only if the invariant closes in both directions.

The frontier stops with unresolved when a step fails to produce a new public
transported certificate state.

A temporary endpoint-count cap may be used for measurement and runtime control.
It is not a resolver and must not be described as coverage of the modulus.

## Allowed Fields

Inference may use:

- public `N`;
- `isqrt(N)` as orientation only;
- PGSPG endpoint-chain outputs;
- `anchor`;
- `reset_endpoint`;
- `gap_offset`;
- `closed_offsets_before_q`;
- `carrier_w`;
- `carrier_d`;
- `lock_carrier_offset`;
- `lock_carrier_d`;
- `lower_d_threat_offset`;
- `tail_after_reset_offsets`;
- `reset_deadline_value`;
- `reset_deadline_margin` as a source-side diagnostic only;
- `reset_signature` as a source-side diagnostic only;
- `floor(N / anchor)`;
- `floor(N / reset_endpoint)`;
- `floor(N / reset_deadline_value)`;
- differences between transported certificate coordinates;
- equality of public transported certificate coordinates.

## Forbidden Fields And Operations

Inference must not use:

- audit factors;
- hidden factors;
- `N % x`;
- `gcd(N, x)`;
- `x * y == N` as a selection predicate;
- product closure as the contraction rule;
- factorization APIs;
- primality APIs as endpoint sources;
- Miller-Rabin;
- sieves;
- random search;
- fallback search;
- fixed additive chambers around `isqrt(N)`;
- endpoint-walk budgets as solver coverage;
- raw reset-margin equality as the invariant.

## Unresolved Condition

The correct result is unresolved when:

- no public lower certificate exists;
- no public upper certificate exists;
- transported reset-to-deadline interval does not land on an opposite
  certificate frontier;
- the frontier class fails in either direction;
- a measurement-only cap is reached before invariant closure;
- the current exact interval backend cannot derive the needed PGSPG certificate.

The unresolved state is a valid research result. It must not trigger a fallback
path.

## Falsification Protocol

Audit factors are allowed only after the public invariant has emitted a result.

The audit step may label:

```text
resolved row -> matches audit pair or does not match audit pair
unresolved row -> no inferred pair to certify
```

Audit must not choose endpoints, rank candidates, define frontier traversal, or
provide certificate fields. Audit also must not decide whether the invariant
closed. Closure must be decided entirely by public transported certificate
state before the audit file is read.

## Current Known Facts

The official runner currently emits:

```text
rsa_v2_40bit_static_001 -> unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 -> unresolved_by_certificate_pair_not_closed
```

For the current official 40-bit orientation pair:

```text
lower_reset_endpoint = 1048573
transported_upper_endpoint = 1048574
upper_reset_endpoint = 1048583
transported_lower_endpoint = 1048564
closure_status = unresolved_by_certificate_pair_not_closed
```

For the current official 50-bit orientation pair:

```text
lower_reset_endpoint = 32053649
transported_upper_endpoint = 32053634
upper_reset_endpoint = null
transported_lower_endpoint = null
closure_status = unresolved_by_certificate_pair_not_closed
```

Downstream audit snapshots show why raw reset-margin equality is invalidated as
an invariant candidate. On the true 50-bit audit endpoints, both sides are
valid local PGSPG reset locks, but their source-side reset margins are:

```text
lower reset-deadline margin = 2
upper reset-deadline margin = 12
```

Those margins are not equal because the reciprocal floor map does not preserve
source-side unit scale. The next invariant must compare transported certificate
frontier state, not raw local margins.

## 2026-05-07 Grok Review Result

A second-opinion review with Grok and local public-only probes falsified three
candidate resolver shapes.

The static frontier-class tuple is too weak:

```text
40-bit tuple closures: 172 / 256 measured orientation anchors
50-bit tuple closures: 186 / 256 measured orientation anchors
```

The dominant closure class was the common local regime:

```text
('above', 'above', 'tail', 4, 4, False, True)
```

The reciprocal certificate-generation fixed point is also too weak:

```text
40-bit fixed cycles: 155 / 256
50-bit fixed cycles: 143 / 256
```

Strict mutual reset-floor closure is selective but not sufficient as a
frontier-entry rule:

```text
40-bit mutual reset-floor hits: 21 / 256
50-bit mutual reset-floor hits: 0 / 256
```

The transport-driven chamber jump:

```text
lower_anchor
-> lower PGSPG certificate
-> floor(N / lower.reset_endpoint)
-> upper PGSPG certificate
-> floor(N / upper.reset_endpoint)
-> next lower endpoint
```

reaches the close-factor-shaped 40-bit audit endpoint in one step, but on the
50-bit rung it degenerates into near-linear endpoint descent from `isqrt(N)`.

The reviewed current state is:

```text
unresolved_by_insufficient_frontier_entry
```

for the transported-invariant research question.

The missing object is:

```text
a PGS-native non-local transport operator on R(C) that selects the next lower
chamber without reference to previous_endpoint or linear descent
```

## 2026-05-07 Debt Operator Probe

The first implemented public sidecar harness is:

```text
transported_exclusion_debt_v1
```

It defines:

```text
prefix_debt = max(0, lock_carrier_offset - 1) * max(0, lock_carrier_d - 2)
suffix_debt = max(0, reset_deadline_offset - lock_carrier_offset)
              * max(0, lock_carrier_d - 3)
debt = prefix_debt + suffix_debt
transport_width = floor(N / reset_endpoint) - floor(N / reset_deadline_value)
balance = transport_width - debt
```

On the current `256` measured public rows per case, raw balance is falsified as
a phase signal:

```text
row_count: 512
phase_counts: negative = 512
phase_change_count: 0
zero_balance_count: 0
```

Debt shock is also too broad:

```text
positive_debt_shock_count: 255
nonlocal_debt_shock_count: 107
local_descent_collapse_count: 298
```

The paired width/debt local signal is still too broad:

```text
local_width_debt_signal_count: 156
```

The conclusion is not that transported debt is useless. It is that a row-local
debt predicate is too weak. The next viable form must treat debt as a trajectory
over consecutive public certificates and look for a transported exclusion
turning point, not a single-row acceptance flag.

## 2026-05-07 Transported Exclusion Ledger

The sidecar harness now records transported GWR/NLSC exclusion zones:

```text
source_carrier_value
source_transport_carrier_image = floor(N / source_carrier_value)
transported_prefix_zone =
  [floor(N / reset_endpoint), floor(N / source_carrier_value)]
transported_suffix_zone =
  [floor(N / reset_deadline_value), floor(N / reset_endpoint)]
```

It then derives the induced opposite certificate from the transported reset
image and records whether the induced carrier falls inside the transported
prefix or suffix zone.

The ledger uses these public elimination predicates:

```text
ledger_prefix_elimination:
  induced carrier lies in transported prefix zone
  and induced lock_carrier_d <= source lock_carrier_d

ledger_suffix_elimination:
  induced carrier lies in transported suffix zone
  and induced lock_carrier_d < source lock_carrier_d
```

A second-opinion round agreed that the next law object should be a transported
committed-story ledger: after a selected carrier locks, later transported states
must not freely rewrite the locked carrier-to-reset-to-threat story.

The first NLSC ceiling predicate tested from that advice was:

```text
ledger_threat_ceiling_elimination:
  induced lower threat lies before the transported deadline
  or inside the transported committed suffix zone,
  and induced lock_carrier_d <= source lock_carrier_d
```

On the current public surface it was inert:

```text
ledger_threat_ceiling_elimination_count: 0
```

The frontier novelty layer records repeated induced anchors as stale transported
certificate states, not new public frontier entries.

Default public run with `256` rows per case:

```text
row_count: 512
ledger_eliminated_count: 110
ledger_stale_transport_state_count: 213
ledger_survivor_count: 402
ledger_effective_survivor_count: 202

40-bit effective survivors: 109 / 256
50-bit effective survivors: 93 / 256
```

The strongest supported finding is:

```text
transported carrier-zone elimination plus frontier novelty cuts the measured
surface from 512 rows to 202 effective survivors, but it does not close the
public invariant
```

The unresolved state remains:

```text
unresolved_by_insufficient_frontier_entry
```

The next missing object is sharper than scalar debt: an ordered transported
certificate ledger over closed offsets, tail offsets, reset endpoint, carrier,
and lower-threat coordinates. Span-style closed-offset elimination is not yet
accepted as an inference rule because interval membership between transported
closed coordinates is not itself a proved PGS-law contradiction.

## 2026-05-07 Recursive Transported Ledger

The sidecar harness now includes recursive measurement:

```text
depth 0:
  measured public frontier rows

depth k + 1:
  source anchors are the prior layer's new effective transported survivors

advance rule:
  ledger_recursive_survivor =
    ledger_effective_survivor
    and not ledger_recursive_cycle_state
```

A recursive step is allowed only when the row creates a new public transported
certificate state and does not point back into a source state already present on
the recursive frontier. This keeps recursion from becoming endpoint-count
coverage or linear descent under another name.

Default public run:

```text
measured_rows_per_case: 256
recursive_depth_limit: 4
recursive_row_count: 713
recursive_layer_count: 3

depth 0:
  row_count: 512
  ledger_recursive_survivor_count: 200

depth 1:
  row_count: 200
  ledger_eliminated_count: 46
  ledger_recursive_cycle_state_count: 199
  ledger_recursive_survivor_count: 1

depth 2:
  row_count: 1
  ledger_stale_transport_state_count: 1
  ledger_recursive_cycle_state_count: 1
  ledger_recursive_survivor_count: 0

recursive_final_survivor_count: 0
```

Case split:

```text
40-bit:
  depth 0 survivors: 109
  depth 1 rows: 109
  depth 1 cycle states: 109
  depth 1 survivors: 0

50-bit:
  depth 0 survivors: 91
  depth 1 rows: 91
  depth 1 cycle states: 90
  depth 1 survivors: 1
  depth 2 rows: 1
  depth 2 stale states: 1
  depth 2 cycle states: 1
  depth 2 survivors: 0
```

The strongest supported finding is:

```text
recursive PGS-law elimination collapses the measured transported frontier from
512 public rows to zero recursive survivors within three measured layers
```

This is a research-sidecar result. It does not by itself resolve the official
RSA v2 runner, and it does not identify factors. The result does establish that
the recursion frame is materially stronger than row scoring, row matching, raw
balance, local shock, and one-pass carrier-zone elimination.

## Next Implementation Step

Do not implement the falsified tuple, fixed-point, or local chamber-jump shapes
as resolver logic.

Do not promote the row-local debt balance, debt shock, or paired width/debt
signal to resolver logic.

Do not promote the inert threat-ceiling predicate or broad frontier novelty
filter to resolver logic.

Do not promote recursive survivor exhaustion to official resolver closure until
the row-level elimination rules are reviewed as a formal transported certificate
contract.

The next valid implementation step is to explain the recursive elimination rule
as a math contract, then add tests that require any future resolved row to name
the public recursive ledger reason. The official resolver state must remain
unresolved until that reviewed ledger operator closes before audit.
