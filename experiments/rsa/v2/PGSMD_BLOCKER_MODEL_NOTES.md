# PGSMD Blocker Model Notes

## Useful Extracts

### Gemini

- Frame the current blocker as a public grammar-linkage gap: local PGSPG
  chamber-reset certificates exist, but no public reciprocal grammar relation
  links the transported endpoint neighborhoods.
- Treat inverse-word exclusion as a negative invariant first, not as positive
  resolver logic.
- Candidate object: Reciprocal Recursive Word Mask.
- Candidate exclusion relation:

```text
x -> recursive lag-2 / lag-3 word
y = floor(N / x) -> recursive lag-2 / lag-3 word
component sharing allowed
ordered lag-2 + lag-3 word collision excluded
```

- Candidate unresolved states:

```text
unresolved_by_grammar_collision
unresolved_by_carrier_mismatch
unresolved_by_transport_scaling_violation
```

- Missing-field hypothesis: a recursive depth or lock-depth field may be needed
  to turn negative word exclusion into positive reciprocal closure.

- Immediate falsification target: apply the word-collision check to existing
  40-bit and 50-bit transported certificate rows and see whether the current
  unresolved state gains a structural grammar-collision explanation.

### Grok

- Strong useful claim: the missing public object is the reduced recursive
  grammar word attached to each PGSPG chamber-reset certificate, especially the
  ordered lag-2 + lag-3 reduced signature.

- Candidate invariant shape:

```text
certificate C
-> reset endpoint
-> recursive lag-2 / lag-3 reduced word at that endpoint
-> transport by T_N(x) = floor(N / x)
-> opposite certificate recursive lag-2 / lag-3 reduced word
-> component sharing allowed
-> ordered word collision excluded
```

- Useful distinction: current certificate fields expose reset/deadline,
  carrier, lock carrier, threat, and tail state, but not the recursive
  refinement that separates solved target grammar from deterministic expanded
  grammar.

- Sidecar-only implementation target: add recursive grammar word fields to
  PGSPG certificate rows without making them resolver logic.

- Required unresolved cases:

```text
transported side has no certificate -> unresolved
recursive grammar word undefined -> unresolved
ordered word collision -> unresolved_by_recursive_word_collision
existing 40-bit / 50-bit rungs close -> candidate invariant is falsified
```

- Useful falsification checks:

```text
40-bit and 50-bit live rungs must remain unresolved
fresh RSA-100 rows must preserve component sharing and zero ordered collisions
48-row solved surface must preserve zero ordered lag-2 + lag-3 collisions
```

### Meta

- Useful falsified alternatives to preserve:

```text
static frontier-class tuple over-closes:
  40-bit: 172 / 256
  50-bit: 186 / 256

strict mutual reset-floor hits are selective but not sufficient:
  40-bit: 21 / 256
  50-bit: 0 / 256

raw reset-deadline margin equality is invalid:
  true 50-bit endpoints have lower margin 2 and upper margin 12

row-local debt balance is invalid as phase signal:
  512 rows measured
  negative = 512
  phase_change_count = 0
  zero_balance_count = 0
```

- Candidate invariant name: Transported Recursive Word Exclusion Invariant.

- Proposed public fields to materialize on PGSPG certificates:

```text
lag2_reduced
lag3_reduced
ordered_word = lag2_reduced || lag3_reduced
```

- Candidate comparison relation:

```text
C_u.reset_endpoint in T_N([C_l.reset_endpoint, C_l.reset_deadline_value])
C_l.reset_endpoint in T_N([C_u.reset_endpoint, C_u.reset_deadline_value])
{C_l.lag2_reduced, C_l.lag3_reduced}
  intersects {C_u.lag2_reduced, C_u.lag3_reduced}
C_l.ordered_word != C_u.ordered_word
C_l.ordered_word not in public expanded ordered-word set
C_u.ordered_word not in public expanded ordered-word set
```

- Candidate unresolved states:

```text
unresolved_by_missing_recursive_grammar_fields
unresolved_by_transported_recursive_word_exclusion_not_closed
```

- Useful sharper blocker statement: under the current certificate fields, the
  recursive word exclusion relation cannot be evaluated from public certificate
  state. The certificate must first expose lag-2, lag-3, and ordered-word
  fields as public endpoint-chain derivatives.

- Important open pressure point: the proposed expanded ordered-word set must be
  defined from public N-side PGSPG derivation only. If it depends on solved
  target labels, it remains evidence, not decomposer inference.

### Deepseek

- Useful refinement of the missing field: attach a recursive grammar signature
  for the chamber context around the reset endpoint.

```text
recursive_grammar_signature =
  outward_lag2_reduced
  | outward_lag1_reduced
  | inward_lag1_reduced
  | inward_lag2_reduced
```

- Useful transport formulation:

```text
C_l.reset_endpoint -> y = floor(N / C_l.reset_endpoint)
y -> public chamber containing y
public chamber containing y -> transported recursive grammar signature
```

- Useful public expanded-surface hypothesis:

```text
E(N) = ordered lag-2 + lag-3 reduced words collected from a deterministic
public endpoint-chain walk outward from isqrt(N)
```

- Important boundary for `E(N)`: any finite walk depth is a measurement cap,
  not solver coverage. A cap can support sidecar evidence but must not be used
  as proof that all endpoint pairs have been covered.

- Useful sidecar shape:

```text
derive lower certificate
derive recursive grammar signature around lower reset endpoint
transport lower reset endpoint through floor(N / x)
derive recursive grammar signature around transported chamber
compare component sharing and ordered-word exclusion against E(N)
repeat symmetrically
emit resolved only if the public structural predicate closes
otherwise emit unresolved
```

- Open question worth preserving: whether public `E(N)` built from the N-side
  endpoint chain is a faithful proxy for the expanded surface used in solved
  target-side evidence.

### Copilot

- Useful missing-field refinement: expose a canonical ordered component
  signature, not just the raw reduced recursive word.

```text
ordered_component_signature =
  canonical token sequence extracted from the reduced recursive grammar word
```

- Useful reason for canonicalization: reciprocal floor transport changes raw
  scale and interval widths, so the compared object should be component
  identity and order, not raw distances.

- Candidate comparison refinement:

```text
S(C_transport) == transport_map(S(C_source))
or
S(C_transport) is a deterministic prefix/suffix of transport_map(S(C_source))
```

- Useful open requirement: define `transport_map` and canonical component IDs
  as fixed public rules. Without that definition, the signature idea remains a
  label, not an invariant.

- Useful unresolved reasons:

```text
lower_transport_mismatch
upper_transport_mismatch
forbidden_ordered_subsequence
```

- Useful implementation pressure: first publish the deterministic canonical
  extraction rule for ordered component signatures; then test whether it adds
  information beyond the existing lag-2 / lag-3 reduced strings.

### Claude

- Useful alternate blocker frame: the recursive transported ledger already
  gives a sharp measured elimination surface, but its elimination predicates
  are not yet stated as consequences of a PGS law.

- Missing-law hypothesis:

```text
prove carrier-zone elimination and cycle-state elimination from GWR/NLSC
applied across T_N(x) = floor(N / x)
```

- Useful ledger rules to preserve:

```text
carrier-zone elimination:
  induced carrier falls inside transported source prefix/suffix zone
  and induced lock_carrier_d <= source lock_carrier_d

cycle-state elimination:
  recursive transport returns to an anchor already present on the frontier
```

- Candidate unresolved state:

```text
unresolved_by_missing_law_contract_for_recursive_elimination
```

- Useful warning: a single-row predicate over only carrier_d, lock_carrier_d,
  threat presence, and tail presence cannot distinguish the true pair from the
  common local regime. Any viable invariant must include transported interval
  positions of certificate coordinates.

- Candidate sidecar name: Transported Committed-Story Ledger.

- Candidate sidecar fields:

```text
transported carrier position
transported deadline position
lock_carrier_d non-regression
cycle-state exclusion
```

- Useful proof obligation: before promoting any ledger predicate, write the
  mathematical argument that the predicate follows from GWR/NLSC under
  reciprocal floor transport.

### ChatGPT

- Useful synthesis: combine the recursive transported ledger with recursive
  word exclusion. Treat lag-2 / lag-3 grammar words as the reduced projection
  of an ordered transported certificate story.

- Candidate sidecar name:

```text
transported_committed_word_ledger_v1
```

- Useful missing-field refinement:

```text
certificate_commitment_story
```

Minimal intended content:

```text
closed offsets
carrier lock
reset
lower threat
tail
deadline
ordered public reason each event closes or dominates an interval
GWR/NLSC/tail/bound closure operator
reduced_state_before / reduced_state_after
```

- Useful sharper unresolved state:

```text
unresolved_by_missing_public_commitment_story
unresolved_by_unproved_transported_commitment_ledger_law
```

- Useful distinction: `closed_offsets_before_q` says which offsets are closed,
  but not the ordered public reason they are closed or which event dominates
  which interval. That provenance gap prevents transported interval membership
  from becoming a proof-grade contradiction.

- Candidate public object:

```text
ordered transported certificate commitment ledger
projected into recursive lag-2 + lag-3 reduced grammar words
```

- Useful sidecar discipline: keep the official inference rows unchanged; emit
  only measurement rows for transported committed-word ledger status.

- Useful hard gate: if transported committed-word exclusion fires while
  certificate_commitment_story is absent, return unresolved rather than
  promoting measured exclusion to resolver closure.

### Perplexity Computer

- Useful candidate name:

```text
Transported Ordered Word Frontier
```

- Useful composition: keep strict mutual reset-floor closure as the selection
  front door, then add ordered-word and recursive-ledger clauses only as
  additional exclusion structure.

- Important clause-order discipline:

```text
If strict reciprocal reset-floor clause fails, report that failure first.
Do not let grammar-word or ledger clauses appear to explain a pair that already
fails the existing front-door condition.
```

- Useful falsification gate:

```text
TOW clauses 1 and 2 must exactly reproduce the existing strict mutual reset-floor
condition.

On current 40-bit and 50-bit rungs, TOW must fail at clause 1 or 2, not at the
word or ledger clauses.
```

- Useful missing-field refinement:

```text
transported_endpoint_chain_lag2_word
transported_endpoint_chain_lag3_word
transported_endpoint_chain_cell_key
```

- Useful reason: if transported endpoint-chain words are re-derived ad hoc by
  the sidecar, the large-coordinate backend boundary remains outside the
  certificate object. Promoting them to certificate-level public fields would
  make the invariant expressible as certificate comparison instead of overlay
  measurement.

- Useful unresolved state:

```text
unresolved_by_missing_transported_endpoint_chain_certificate_field
```

- Useful guardrail: any proposed invariant must strictly reduce the existing
  static frontier-class closure counts. If it does not strictly subset the
  172/256 and 186/256 tuple closures, its new clauses are inert.

### Perplexity Research

- Useful emphasis: the transported ledger object is a trajectory over
  consecutive transported layers, not a row-local acceptance flag.

- Candidate sidecar name:

```text
TCL-v1 = Transported Committed-Story Ledger
```

- Useful law-contract target:

```text
transported carrier image in committed prefix/suffix zone
+ non-increasing lock_carrier_d
=> structural impossibility under PGSPG endpoint-chain laws
```

- Useful formalization pressure:

```text
prefix-zone elimination and suffix-zone elimination should be stated as
PGS-law contradictions, not as measured filters.
```

- Useful distinction: recursive ledger collapse to zero survivors is an
  elimination result, not factor-pair selection.

- Candidate unresolved state:

```text
unresolved_by_insufficient_frontier_entry
```

- Useful proof obligation:

```text
If a transported carrier image falls inside the committed prefix zone with
non-increasing lock_carrier_d, then PGSPG cannot produce a valid certificate
at that transported position consistent with the committed lower story.
```

- Useful sidecar contract:

```text
complete output states only:
  tcl_v1_resolved_by_carrier_cycle_closure
  tcl_v1_unresolved_by_no_cycle_before_depth_cap
  tcl_v1_unresolved_by_stale_state_termination
  tcl_v1_unresolved_by_missing_certificate
```

- Important caution: any "resolved" TCL state requires a reviewed proof that
  cycle closure is a PGS closure law. Until then, official decomposer output
  must remain unresolved.

### Sonar

- Useful untested predicate to measure, not promote:

```text
symmetric transported reset-to-deadline width
```

- Candidate sidecar check:

```text
abs(
  (floor(N / C_l.reset_endpoint) - floor(N / C_l.reset_deadline_value))
  - (C_u.reset_deadline_value - C_u.reset_endpoint)
) <= 1

and symmetrically upper -> lower
```

- Useful placement: run this only after certificate existence and ledger
  elimination context are established. It is not a standalone resolver.

- Useful trajectory-state suggestion:

```text
ledger_state =
  lower carrier_d / lock_carrier_d / threat presence / first-tail presence /
  closed-offset count
  plus corresponding induced upper fields
  plus transported reset-to-deadline width
```

- Useful falsification target: measure whether symmetric transported width
  creates false positives among rows already rejected by strict closure or
  static frontier-class tests.

- Boundary: because raw source-side margin equality is already invalidated,
  this width relation should be treated as a measurement target only until it
  either fails or gains a PGS-law derivation.

### Nemotron

- Useful proof-style statement: no single-row invariant over only
  `carrier_d`, `lock_carrier_d`, threat presence, and tail presence can select
  a unique transported pair, because the common low-regime tuple appears across
  broad public endpoint families. The needed information lives in the
  transported trajectory.

- Candidate sidecar name:

```text
Transported Committed-Story Ledger
```

- Useful committed-story monotonicity idea:

```text
If a previous layer locked carrier k with lock_carrier_d = d, then a later
transported layer may not rewrite the same transported reset story with
lock_carrier_d < d.
```

- Candidate trajectory field:

```text
ordered sequence over:
  closed_offsets_before_q
  tail_after_reset_offsets
  reset_endpoint
  carrier_value
  lower_d_threat_offset
```

- Useful activation test:

```text
Count committed-story rewrites blocked per case.
If zero rewrites are blocked on both rungs, the monotonicity clause is inert
and should not be treated as useful.
```

- Useful grammar cross-check:

```text
For any depth-1 survivor, verify that its target-side ordered lag-2 + lag-3
word does not collide with the excluded ordered-word set.
```

- Useful sharper unresolved statement: interval membership between transported
  closed coordinates is measurable but not yet a proved PGS-law contradiction.
  Promotion requires a derivation that transported closed-offset membership
  inside a committed suffix/prefix zone contradicts chamber grammar.

### Kimo

- Useful quick sidecar measurement:

```text
transported lower deadline image lands inside upper reset-to-deadline interval

T_dl = floor(N / C_l.reset_deadline_value)
check: C_u.reset_endpoint <= T_dl <= C_u.reset_deadline_value
```

- Related width diagnostic:

```text
abs(
  abs(floor(N / C_l.reset_deadline_value)
      - floor(N / C_l.reset_endpoint))
  - (C_u.reset_deadline_value - C_u.reset_endpoint)
) <= max(C_l.carrier_d, C_u.carrier_d)
```

- Useful placement: treat deadline containment and width consistency as
  diagnostics only. They are not resolver logic and must still be bounded by
  existing certificate-pair unresolved status.

- Useful missing-field refinement:

```text
transported_threat_image =
  floor(N / (C_l.anchor + C_l.lower_d_threat_offset))

transported_tail_image =
  floor(N / (C_l.anchor + first_tail_after_reset_offset))
```

- Useful reason: threat and tail offsets are already certificate fields, but
  their reciprocal images are not yet materialized as interval-position objects
  against the opposite certificate. These may carry more of the recursive word
  distinction than reset/deadline width alone.

- Boundary: raw deadline or width containment has no proof status and should be
  discarded if it creates false positives on current unresolved rows.

## Current Narrowed Blocker: `Psi(RB)`

The current active proof target has moved past the broad recursive-word and
diagnostic hypotheses above.

The strongest measured transported-story result remains:

```text
transported_story_law_v1
row_count = 512
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
```

This is measured public evidence, not a theorem and not resolver promotion.
The official runner remains:

```text
rsa_v2_40bit_static_001 unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved_by_certificate_pair_not_closed
```

The narrowed frontier interface is:

```text
DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C, C'))

RB(C, C') =
(
  R(C, C'),
  source_closed_count - source_tail_count,
  induced_closed_count - induced_tail_count
)
```

The bridge theorem candidate is:

```text
PrefixMaterial(C, C') or ThreatMaterial(C, C')
=> not Psi(RB(C, C')).
```

Independent proof obligations:

```text
T1 prefix commitment transport
T2 threat-horizon transport
T3 frontier commitment exclusivity against independently defined Psi(RB)
```

Current guarded facts:

```text
Certificate story grammar is fixed and guarded:
  closed_offset* carrier_lock? reset lower_threat? tail* deadline.
RB is computable from public pre-ledger fields.
RB is unchanged after deleting ledger labels, raw frontier novelty, interval
flags, and threat-ceiling flags.
RB classes determine induced-carrier interval symbol on the measured surface.
RB classes determine source/induced lock-label relation on the measured surface.
RB classes determine source deadline-threat boundary on the measured surface.
RB classes determine typed branch class on the measured surface.
TypedMaterial RB classes are disjoint from non-TypedMaterial RB classes.
PrefixMaterial and ThreatMaterial RB classes have a six-class overlap.
Broad run-word, simple balance-threshold, and per-run coordinate-monotone
balance definitions are invalid.
Observed TypedMaterial RB-class complement is measured-perfect but rejected as
a finite table lookup.
FreshEndpoint handles recurrence outside Psi(RB).
```

Immediate proof blocker:

```text
RB Sufficiency Sublemma
measured support: guarded
structural proof: missing
```

The sublemma must prove that fixed certificate story grammar plus reciprocal
interval classification, run-word collapse, and source/induced closed-tail
balances determine the carrier symbol, lock relation, deadline-threat boundary,
and typed branch class for valid transported certificate pairs.

Derivation state:

```text
fixed grammar plus balances alone are insufficient
symbolic obstruction: O P O O and O O P O both collapse to OPO with the same
induced closed-tail balance but put the carrier in different interval symbols
PGS counterexample: not established
proof-source countermodel: established for grammar plus balances alone
```

Therefore the first structural proof target is:

```text
Carrier Localization Under Reciprocal Transport
```

That law must show that valid PGSPG transport geometry rules out the symbolic
carrier-position ambiguity before RB can determine lock relation,
deadline-threat state, and typed branch class.

Measured carrier-localization extension:

```text
direct RB classes with mixed carrier symbols = 0 / 475
recursive RB classes with mixed carrier symbols = 0 / 661
combined direct plus recursive RB classes with mixed carrier symbols = 0 / 661
combined direct plus recursive RB classes with mixed carrier run ordinals =
  0 / 661
```

This strengthens the finite guard only. It does not prove the carrier-local
transport law.

Do not strengthen this into exact event-index recovery:

```text
combined direct plus recursive RB classes with mixed exact carrier index = 5
combined direct plus recursive RB classes with mixed induced closed count = 5
combined direct plus recursive RB classes with mixed induced story length = 5
```

The admissible target is collapsed interval-run localization of the induced
carrier, not reconstruction of the full induced story alignment.

Measured projection boundary on the combined direct plus recursive surface:

```text
R alone ambiguous for carrier run = 12
R plus source balance ambiguous for carrier run = 18
R plus induced balance ambiguous for carrier run = 17
R plus balance delta ambiguous for carrier run = 6
full RB ambiguous for carrier run = 0
```

The proof target must use the full RB triple.

Measured refinement projection boundary:

```text
deadline-threat boundary is determined by source balance alone on the combined
surface:
  source_balance = 8..31  => false
  source_balance = 32..34 => true
carrier run, lock relation, and typed branch class require full RB on the
combined surface
```

Simple `Psi(RB)` candidates remain invalid. Coarse word-shape predicates and
balance inequalities leak against `not TypedMaterial`; the typed, non-typed,
and effective delta ranges overlap. This preserves the boundary: do not replace
the missing chamber-balance language with a scalar threshold or coarse run-word
rule.

Lock-relation refinement still needs the full collapsed run word. Carrier-run
localization plus source/induced balances has 4 measured lock-relation
ambiguities on the combined public surface; full RB has 0.

The ambiguous groups are:

```text
(3, 33, 31): BOSPO equal, POBO higher
(2, 34, 33): OBPO lower, OSBP higher
(3, 33, 33): OPOP equal, POSBP higher
(2, 33, 33): BOP equal, OSBO lower, OSBP higher
```

So the Lock-Relation Balance Law must use off-carrier run context, not only the
carrier's localized run plus balances.

Typed-branch projection is simpler after the preceding refinements:

```text
carrier symbol + lock relation + deadline-threat boundary
=> typed branch class
```

On the combined public surface this projection has 0 ambiguity. Replacing
carrier symbol with carrier run ordinal gives measured ambiguity, so the branch
law needs the interval symbol specifically.

The missing item is not another sidecar or scalar hunt. It is first a structural
proof of RB Sufficiency, then a public chamber-balance law defining `Psi(RB)`
before typed rewrite and recurrence labels, followed by a proof that committed
transported prefix and threat-horizon material lie outside that language.
