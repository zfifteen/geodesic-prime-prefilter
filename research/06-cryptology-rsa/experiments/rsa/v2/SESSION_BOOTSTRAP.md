# RSA v2 Session Bootstrap

This file exists so a future Codex session can start in `research/06-cryptology-rsa/experiments/rsa/v2`
without reverse-engineering the previous work.

## Headline State

The current v2 experiment is honest but unresolved.

The official runner derives reciprocal PGSPG certificate-pair state from public
moduli. It does not currently solve the 40-bit or 50-bit rungs.

The current transported-story result is proof-facing:

```text
transported_story_law_v1 reproduces the public recursive elimination surface
from certificate stories alone:
512 public rows -> 202 effective survivors -> 713 recursive rows -> 0 final
recursive survivors.
```

Read `TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md` before extending this track.
It names the four lemmas needed to turn the measured relation into PGSPG-derived
theorem candidates.

Current proof-derivation state:

```text
PROOF.md proves local GWR/NLSC inside one prime-gap interval.
It does not by itself prove transported prefix/suffix exclusion after
T_N(x) = floor(N / x) and induced opposite-certificate construction.

Terminology:
  GWR = w is the first interior integer with minimum divisor count.
  NLSC = no later interior point before q has divisor count below tau(w).
  These names do not add reciprocal-floor, endpoint-chain, or post-reset
  deadline theorems beyond PROOF.md.
```

Exact source-chamber kernel now recorded in the proof workbench:

```text
r(C) = reset_endpoint = emitted q
w(C) = carrier_w
lambda(C) = lock_carrier_d
d(C) = reset_deadline_value

PROOF.md supports:
  endpoint identity for the resolved source chamber
  carrier identity as first minimum-divisor interior point
  left-side strictness before w(C)
  right-side non-descent before r(C)
  abstract threat horizon ordering r(C) <= T_<(w(C)), when T_<(w(C)) exists

Implementation/certificate support:
  lower_threat is the first scanned post-carrier composite with divisor count
  below lock_carrier_d; identifying lower_threat with T_<(w(C)) uses the
  certificate construction, not an extra theorem in PROOF.md

PROOF.md does not support:
  reciprocal floor preservation of carrier commitment
  reciprocal floor preservation of lock-label comparability
  induced opposite certificate as transported source material
  transported equal-label prefix non-frontier status
  transported strict lower suffix non-frontier status
  RC(C, C') frontier separation

Exact PROOF.md dependency map now recorded:
  GWR supplies carrier selection as the first minimum-divisor interior point.
  Leftmost strictness supplies tau(k) > lambda(C) before w(C).
  NLSC supplies no t with w(C) < t < r(C) and tau(t) < lambda(C).
  The threat-horizon consequence is:
    if T_<(w(C)) = min{t > w(C): tau(t) < lambda(C)} exists,
    then r(C) <= T_<(w(C)).
  These support source-side Lemma 1 and Lemma 2A ordering only.
  They do not supply reciprocal floor commitment, transported label
  comparability, transported frontier exclusion, or Psi(RB).
```

New closed arithmetic sublemma:

```text
For T_N(x) = floor(N / x), positive l < u, and integer z:
  z in [T_N(u), T_N(l)] iff z*l <= N < (z + 1)*u.

Therefore:
  prefix carrier zone iff w(C')*w(C) <= N < (w(C') + 1)*r(C)
  suffix carrier zone iff w(C')*r(C) <= N < (w(C') + 1)*d(C)

Integer preimage refinement:
  exists y in [l, u] with floor(N / y) = z iff
  max(l, floor(N / (z + 1)) + 1) <= min(u, floor(N / z))
  measured prefix integer-preimage rows = 109
  measured suffix integer-preimage rows = 219
  symmetric difference with carrier-zone flags = 0
  all measured prefix and suffix carrier-zone preimages are singletons
  PrefixMaterial singleton preimages = 101 / 101
  ThreatMaterial singleton preimages = 12 / 12

Invalidated strengthening:
  recorded source story-event image matching is too narrow
  prefix carrier-zone rows with recorded event preimage = 42 / 109
  suffix carrier-zone rows with recorded event preimage = 58 / 219
  PrefixMaterial rows with recorded event preimage = 36 / 101
  ThreatMaterial rows with recorded event preimage = 9 / 12
  lift divisor count is not lock-label transport:
    PrefixMaterial lift-vs-source lower/equal/higher = 21 / 18 / 62
    PrefixMaterial lift-vs-induced lower/equal/higher = 21 / 7 / 73
    ThreatMaterial lift-vs-source lower/equal/higher = 9 / 0 / 3
    ThreatMaterial lift-vs-induced lower/equal/higher = 6 / 2 / 4
  lift position classes show the commitment target includes unrecorded source
    segment interiors:
    PrefixMaterial unrecorded_prefix_interior/reset/carrier/closed =
      65 / 21 / 11 / 4
    ThreatMaterial reset/unrecorded_suffix_interior/lower_threat =
      6 / 3 / 3
  PrefixMaterial non-reset source lifts never descend below source lambda:
    unrecorded_prefix_interior higher/equal = 60 / 5
    carrier equal = 11
    closed_offset higher/equal = 2 / 2
    reset lower = 21
    non-reset lower = 0
  ThreatMaterial source-lift lower cases are boundary cases:
    reset lower = 6
    lower_threat lower = 3
    unrecorded_suffix_interior higher = 3
    unrecorded suffix-interior lower = 0

This closes floor-cell membership only. It does not prove floor-cell
commitment, lock-label transport, or Psi(RB).
```

The active proof blockers are now:

```text
Lemma 1B: transported equal-label prefix non-rewrite
  essential to the current collapse
  with equal-label prefix elimination = 202 effective survivors
  without equal-label prefix elimination = 268 effective survivors

PrefixMaterial(C, C') candidate:
  public predicate exists
  rows = 101
  effective = 0
  prefix_elimination = 101
  strict lock descent rows = 25
  equal lock rows = 76
  implication to not Psi(RB(C, C')) remains unproved

TypedMaterial(C, C') reduction:
  TypedMaterial := PrefixMaterial or ThreatMaterial
  PrefixMaterial rows = 101
  ThreatMaterial rows = 12
  overlap rows = 6
  TypedMaterial rows = 107
  TypedMaterial effective rows = 0
  TypedMaterial direct eliminated rows = 107
  non-TypedMaterial direct eliminated rows = 3 redundant tail/non-threat
  rows outside theorem target

Psi(RB(C, C')) acceptance tests:
  must be computed before PrefixMaterial, ThreatMaterial, TypedMaterial, and
  recursive recurrence
  must use only RB(C, C') as public chamber-balance input
  must not read ledger labels or story_rewrite
  must not be defined as not TypedMaterial and not recurrent
  must give the direct chamber-balance side of DirectFrontier(C, C')
  TypedMaterial(C, C') and Psi(RB(C, C')) must be impossible by proof, not by
  definition

Rejected positive FrontierCommit candidate:
  frontier_new_transport_state and not recurrent
  candidate rows = 299
  effective rows = 202
  direct eliminated rows = 97
  stale rows = 0
  TypedMaterial overlap = 97
  reason = raw induced-anchor novelty plus non-recurrence still accepts typed
  material

Measured perfect but table-based FrontierCommit candidate:
  frontier_new_transport_state
  and not recurrent
  and RC(C, C') not in observed TypedMaterial RC-class set
  candidate rows = 202
  effective rows = 202
  direct eliminated rows = 0
  stale rows = 0
  TypedMaterial overlap = 0
  missed effective rows = 0
  status = measured perfect, not a definition
  reason = depends on observed finite RC-class exclusion unless a structural
  public transport law characterizes the excluded classes

Partial structural FrontierCommit_run candidate:
  frontier_new_transport_state
  and not recurrent
  and R(C, C') not in observed TypedMaterial run-word set
  candidate rows = 150
  effective rows = 150
  direct eliminated rows = 0
  stale rows = 0
  TypedMaterial overlap = 0
  missed effective rows = 52
  status = sound on measured surface, incomplete on measured surface,
           not a definition
  reason = run-word exclusion alone is too coarse; the event-count part of
  RC(C, C') is required for measured completeness unless another structural
  invariant is found
  missed effective run words =
    SPOSO 32, OSPO 8, OPO 5, OBO 2, SOPO 1, OSPOPO 1,
    POBO 1, POPOP 1, OBPO 1
  shared-run TypedMaterial rows = 29
  RC overlap between missed effective rows and shared-run TypedMaterial rows = 0
  single event-count threshold separator = none found

Smaller joint run-balance candidate:
  RB(C, C') =
    (
      R(C, C'),
      source_closed_count - source_tail_count,
      induced_closed_count - induced_tail_count
    )
  all RB classes = 475
  effective RB classes = 193
  direct eliminated RB classes = 104
  TypedMaterial RB classes = 101
  stale RB classes = 200
  singleton RB classes = 441
  non-singleton RB classes = 34
  non-singleton rows = 71
  effective/direct eliminated RB overlap = 0
  effective/TypedMaterial RB overlap = 0
  effective/stale RB overlap = 9
  effective/stale mixed RB classes = 9
  effective/direct-eliminated mixed RB classes = 0
  direct-eliminated/stale mixed RB classes = 0
  effective/stale mixed RB classes =
    ('O', 33, 11), ('OSO', 33, 21), ('OSOPO', 33, 25),
    ('OSPO', 33, 20), ('OSPO', 33, 21), ('SPOSO', 19, 25),
    ('SPOSPO', 17, 17), ('SPOSPO', 20, 20), ('SPOSPO', 22, 19)
  endpoint-history boundary =
    these mixed classes differ by frontier_new_transport_state, not direct
    material status; RB must not absorb Lemma 3
  observed-class FrontierCommit_RB candidate rows = 202
  effective rows = 202
  direct eliminated rows = 0
  stale rows = 0
  TypedMaterial overlap = 0
  missed effective rows = 0
  status = measured perfect, not a definition, theorem proof missing
  reason = still depends on observed finite RB-class exclusion unless a
  structural chamber-balance law is proved
  small per-run linear balance separator =
    fails for shared run-word families OBO, OPO, OSPO, OSPOPO
  implication =
    RB theorem must explain ordered run-word family plus both balance
    coordinates; it is not a single threshold or uniform small linear
    inequality
  near-row partition warning =
    441 singleton RB classes mean RB remains close to row-level signature
    unless a structural chamber-balance language is proved
  current frontier predicate interface =
    FreshEndpoint(C') := induced anchor has not appeared earlier in the public
      endpoint-chain traversal for the recursion layer
    DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C, C'))
    Psi is the missing structural chamber-balance language and must not be an
      observed RB-class lookup
    Lemma 1 RB form: PrefixMaterial(C, C') => not Psi(RB(C, C'))
    Lemma 2 RB form: ThreatMaterial(C, C') => not Psi(RB(C, C'))
    Lemma 3 endpoint-history form: not FreshEndpoint(C') => not DirectFrontier
    next theorem to prove =
      find public structural chamber-balance language Psi(RB(C, C')) computed
      before typed material and recurrence, not an observed class lookup
      prove PrefixMaterial and ThreatMaterial are outside Psi
      keep FreshEndpoint as the independent endpoint-history boundary
    invalidated Psi shortcuts =
      observed RB-class lookup, run-word exclusion alone, single event-count
      threshold, single balance inequality, uniform small per-run linear
      balance inequality
  typed-material RB language split =
    PrefixMaterial rows = 101, RB classes = 95, run words = 20,
      effective RB overlap = 0
    ThreatMaterial rows = 12, RB classes = 12, run words = 6,
      effective RB overlap = 0
    PrefixMaterial RB classes ∩ ThreatMaterial RB classes = 6
    ThreatMaterial has induced_balance < source_balance on 12 / 12 rows
    PrefixMaterial balance relation is mixed: lower 59, higher 37, equal 5
    implication = Lemma 2 RB form is a smaller strict-balance threat language;
      Lemma 1 RB form is the larger prefix language and is not reducible to
      induced_balance < source_balance
    threat-language broadening =
      clean branch remains exact ThreatMaterial:
        deadline_threat = true
        induced_carrier_in_suffix_zone = true
        induced_lock_carrier_d < source_lock_carrier_d
      run_word in ThreatMaterial run words has 44 effective rows
      run_word in ThreatMaterial run words and induced_balance < source_balance
        has 21 effective rows
      adding source_balance >= 32 still leaves 7 effective rows
    implication = Lemma 2 must not be widened beyond the strict threat-suffix
      antecedent unless a new source-threat transport law is proved
    prefix-language split =
      strict-prefix rows = 25, RB classes = 23, run words = 9,
        induced_balance < source_balance on 25 / 25 rows,
        effective RB overlap = 0
      equal-prefix rows = 76, RB classes = 72, run words = 17,
        balance relation mixed: lower 34, higher 37, equal 5,
        effective RB overlap = 0
      strict-prefix RB classes ∩ equal-prefix RB classes = 0
      run_word in equal-prefix run words has 8 effective rows
      implication = Lemma 1 cannot reduce to strict descent or a balance
        inequality; equal prefix requires transported leftmostness
    carrier-local prefix restatement =
      induced carrier symbol in {P, B} and lambda(C') = lambda(C):
        rows = 76, eliminated = 76, effective = 0
      induced carrier symbol in {P, B} and lambda(C') <= lambda(C):
        rows = 101, eliminated = 101, effective = 0
        symmetric difference with interval predicate = 0
      induced carrier symbol in {P, B} with no lock restriction:
        rows = 109, eliminated = 101, effective = 8
      implication = non-increasing lock is essential; higher-lock prefix/both
        carrier rows can remain effective
    carrier-local threat equivalence =
      deadline_threat and induced carrier symbol in {S, B}
      and lambda(C') < lambda(C):
        rows = 12, symmetric difference with strict threat-suffix interval
        predicate = 0

Lemma 2A: transported threat-horizon coherence
  narrowed deadline=threat suffix strict-descent candidate
  tail-suffix rows are redundant on the current measured collapse
```

Do not promote `transported_story_law_v1` until one of those transport laws is
proved or the relevant state is explicitly marked unresolved.

Local-only counterexample pressure now exists in the proof workbench:

```text
fresh induced certificates exist that are locally valid under certificate
construction and still satisfy the transported forbidden-zone predicates.
They are not counterexamples to local GWR/NLSC.
They are counterexamples to deriving transported exclusion from local GWR/NLSC
alone.
```

Closed proof route:

```text
local GWR/NLSC alone => Lemma 1B or Lemma 2A
```

Open proof route:

```text
source local chamber commitment
+ reciprocal floor image of committed story material
+ induced opposite certificate
=> induced certificate is a rewrite, not a new frontier state
```

Do not overgeneralize this route. The existing
`transported_commitment_story_ledger_v1` surface has `story_rewrite_count = 276`,
but `124` story-rewrite rows are still effective survivors. The needed theorem
is a typed transported non-rewrite law for the prefix/suffix predicates, not a
blanket rewrite ban.

Current typed theorem candidate:

```text
prefix + lower/equal lock label => committed-prefix rewrite, not new frontier
suffix + lower lock label + deadline=threat => committed-threat-horizon rewrite,
  not new frontier
repeated recursive frontier anchor => recurrent frontier material, not new frontier
```

"New frontier" in this theorem candidate means valid transported frontier
commitment after typed rewrite tests. It is not the raw sidecar field
`frontier_new_transport_state`, which only records induced-anchor novelty before
ledger elimination.

Outside the current theorem candidate:

```text
suffix + equal
suffix + deadline=tail
higher lock label
outside zone
missing lock label
```

Typed candidate coverage on current public rows:

```text
typed direct eliminated union = 107
typed direct effective survivors = 202
recursive depth 0 survivors = 200
recursive depth 1 survivors = 1
recursive final survivors = 0
```

Typed proof decomposition:

```text
T1 prefix commitment transport:
  prefix + lower/equal means C' measures committed carrier-to-reset material

T2 threat-horizon transport:
  suffix + lower + deadline=threat means C' measures committed
  endpoint-to-threat material

T3 frontier commitment exclusivity:
  transported committed material cannot also be a new valid transported
  frontier commitment for the same story
```

T3 is the missing transport law. It is not contained in local GWR/NLSC.
Do not make T3 true by definition. The next proof step needs an independent
frontier-commitment criterion, then a typed rewrite-exclusion theorem against
that criterion.

Current implementation fields do not supply that independent criterion:

```text
frontier_new_transport_state = raw induced-anchor novelty
ledger_effective_survivor = ledger_survivor and frontier_new_transport_state
ledger_recursive_survivor = ledger_effective_survivor and not cycle_state
```

These are measured sidecar classifications, not a proof-level definition of
PGSPG transported frontier commitment.

The missing definition now has a contract:

```text
FrontierCommit(C, C') must be defined from public endpoint-chain transport
state before applying typed rewrite elimination.

If FrontierCommit(C, C') depends on prefix/suffix rewrite predicates, it is
circular and cannot support T3.
```

Rejected FrontierCommit definitions:

```text
frontier_new_transport_state
ledger_effective_survivor
ledger_recursive_survivor
not story_rewrite
```

Each is either pre-proof novelty, post-elimination/circular state, or too broad
for the measured ledger.

Admissible candidate ingredient, not a definition:

```text
commitment_story_word_projection_v1 reduced grammar
projected_lag23_collision_count = 0
fresh_rsa_100_lag23_collision_count = 0
```

Reduced grammar is not a standalone `Psi(RB)` definition on the current
projection surface:

```text
projected_lag23_collision = False on 50 / 50 rows
projected_recursive_reduced_collision = False on 50 / 50 rows
```

Additional existing diagnostics checked as standalone frontier ingredients:

```text
transported_threat_tail_images_v1: rejected as standalone definition
transported_width_diagnostic_v1: rejected as standalone definition
public story-kind grammar: rejected as standalone definition
coarse induced interval-position occupancy: rejected as standalone definition
```

Reason:

```text
threat/tail image positions have multiple regimes
width matches have measured false positives against unresolved and
static-frontier surfaces
26 raw story-kind groups contain both effective survivors and ledger-eliminated
rows
coarse interval-position signatures mix effective, eliminated, and stale rows
```

They remain admissible boundary data, not a proof of Lemma 1, Lemma 2, or T3.

One finer public ingredient remains live but unproved:

```text
full ordered induced interval-position word against transported prefix/suffix
bands
```

Measured status:

```text
mixed full interval-position groups = 0
group_count = 507
singleton_groups = 502
```

This is too close to row identity to be a theorem by itself. The next proof task
is to compress it into a real ordered transport law or falsify that compression.

Current best compression candidate:

```text
full interval run word
+ source public event counts
+ induced public event counts
```

Measured status without raw novelty/staleness fields:

```text
group_count = 481
singleton_groups = 453
max_group_size = 3
mixed effective/eliminated groups = 0
mixed effective/stale groups = 7
```

This separates direct prefix/suffix eliminations from direct effective
survivors on the current public 512-row surface. It does not separate recursive
stale states; that is Lemma 3 territory.

Status:

```text
admissible Psi(RB) supporting ingredient: yes
definition of Psi(RB): not yet
proof from GWR/NLSC transport: missing
resolver promotion: no
```

The proof workbench now names the required run-count sublemmas:

```text
R1 Run Transport Lemma
R2 Event-Count Conservation Lemma
R3 Prefix Run Exclusion Lemma
R4 Threat-Suffix Run Exclusion Lemma
R5 Recursive Run Recurrence Lemma
```

The missing step is not another row scan. It is a non-circular definition of
which RB chamber-balance states satisfy Psi, followed by proof that the typed
prefix and threat-suffix antecedents force non-Psi states.

Compact run-word pressure:

```text
terminal prefix/both-to-outside alternation is necessary for every measured
prefix elimination, but not sufficient.
```

Measured split:

```text
terminal prefix/both-to-outside = false:
  rows = 214
  prefix_elimination = 0
  suffix_elimination = 7

terminal prefix/both-to-outside = true:
  rows = 298
  prefix_elimination = 101
  effective = 53
  stale = 152
```

So R3 cannot be a pure run-word theorem. It needs the event-count part of
`RC(C, C')` or another public chamber-count condition. The suffix-only rows are
the R4 target.

R4 suffix-only surface:

```text
suffix_elimination rows = 16
suffix_only rows = 9
suffix_with_prefix rows = 7
suffix_elimination + deadline_threat = true: 12
suffix_elimination + deadline_threat = false: 4
suffix_only + deadline_threat = true: 6
suffix_only + deadline_threat = false: 3
```

Suffix-only run words:

```text
OSO, OSOSO, OSPO, SOSO, SPOSO
```

`OSO` and `OSPO` also occur on effective/stale rows, so R4 is not a pure
run-word theorem. The theorem-relevant branch remains:

```text
deadline_threat = true
+ suffix lower lock relation
+ induced carrier in transported suffix band
=> non-frontier threat-suffix state
```

The `deadline_threat = false` suffix rows are measured redundant tail/non-threat
rows, not current theorem material.

R4 strict-descent antecedent check:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d < source_lock_carrier_d

rows = 12
effective = 0
eliminated = 12
stale = 0
prefix_elimination = 6
suffix_elimination = 12
```

The non-strict variant fails:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d <= source_lock_carrier_d

rows = 13
effective = 1
eliminated = 12
```

So R4 requires strict lock descent. The proof is still missing; this is measured
evidence for the theorem branch.

R4 formal proof obligation:

```text
If
  d(C) is the lower-threat deadline,
  w(C') in [T_N(d(C)), T_N(r(C))],
  lambda(C') < lambda(C),
then
  C' is transported threat-horizon material committed by C,
  not a new transported frontier commitment.
```

Missing sublemma:

```text
Threat-Horizon Transport Sublemma:
  a strict lower induced carrier inside the transported suffix band measures
  transported source threat-horizon material, not an independent frontier
  commitment.
```

Status:

```text
local NLSC source fact: proved in PROOF.md
reciprocal floor image as ordered public interval: arithmetic definition
Threat-Horizon Transport Sublemma: unproved
R4 theorem: unproved
```

R4 non-circularity requirement:

```text
ThreatMaterial(C, C') must be defined from public source/induced certificates,
T_N([r(C), d(C)]), source lower-threat deadline identity, induced carrier
position, and strict lock-label descent.
```

It must not be defined as:

```text
not DirectFrontier(C, C')
not Psi(RB(C, C'))
ledger_suffix_elimination
ledger_effective_survivor = false
```

Current R4 proof status:

```text
clean measured antecedent: yes
public ThreatMaterial definition: candidate exists
proof against Psi(RB): missing
```

ThreatMaterial candidate:

```text
ThreatMaterial(C, C') holds iff:
  d(C) is the lower-threat deadline,
  C' is induced from previous_endpoint(T_N(r(C))),
  w(C') in [T_N(d(C)), T_N(r(C))],
  lambda(C') < lambda(C).
```

Implementation-level public predicates:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d < source_lock_carrier_d
```

Measured support:

```text
ThreatMaterial rows = 12
effective = 0
direct eliminated = 12
stale = 0
```

Remaining theorem obligation:

```text
ThreatMaterial(C, C') => not Psi(RB(C, C'))
```

Simple chamber-count shortcut status:

```text
lower-threat presence alone: rejected as standalone R3 gate
tail-count pairs: rejected as standalone R3 gate
closed/tail count deltas: rejected as standalone R3 gate
```

Inside terminal prefix/both-to-outside, lower-threat presence splits the rows
but still mixes effective, eliminated, and stale states except for one
protective measured branch:

```text
source_threat_count = 0, induced_threat_count = 1:
  rows = 11
  effective = 11
  prefix_elimination = 0
```

Current R3 status:

```text
pure run word: insufficient
observed TypedMaterial run-word exclusion: measured sound, incomplete
  candidate rows = 150
  effective rows = 150
  direct eliminated rows = 0
  stale rows = 0
  TypedMaterial overlap = 0
  missed effective rows = 52
  missed effective rows use 9 shared TypedMaterial run words
  full RC(C, C') separates the missed effective rows from the shared-run
  TypedMaterial rows, but no single event-count threshold separates them
one-field chamber-count threshold: insufficient
full RC(C, C') signature: measured direct separation, proof missing
run-balance RB(C, C') signature: smaller measured direct separation,
  proof missing
```

RC table-lookup boundary:

```text
rows = 512
RC classes = 481
direct effective RC classes = 194
direct eliminated RC classes = 105
stale RC classes = 202
effective/eliminated RC overlap = 0
effective/stale RC overlap = 7
eliminated/stale RC overlap = 13
```

Do not promote a finite table of observed RC classes into
`FrontierCommit(C, C')`. The remaining valid route is a structural theorem
inside `RC(C, C')`, or a proof that `RC(C, C')` itself is an invariant image of
PGSPG transport independent of ledger labels.

RC non-entailment status:

```text
local GWR/NLSC does not entail RC(C, C') frontier separation
```

Reason:

```text
RC(C, C') depends on N, T_N, transported prefix/suffix bands, induced
opposite-certificate story values, and source/induced event counts.
Those are not predicates in the local one-chamber GWR/NLSC theorem language.
```

Closed shortcut:

```text
use RC(C, C') as if it were already a GWR/NLSC consequence
```

Open route:

```text
prove RC(C, C') as a new transported invariant,
or prove the smaller RB(C, C') chamber-balance condition
```

Completion audit against the active objective:

```text
objective: finish PGSMD transported-story research completely

prompt-to-artifact checklist:
  canonical proof workbench =
    TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md
  measured public story-law evidence =
    output/transported_story_law/summary.json
  active session entrypoint =
    SESSION_BOOTSTRAP.md
  grammar evidence summary =
    PGS_GRAMMAR_EVIDENCE_FINDINGS.md
  official runner evidence =
    output/inference_rows.jsonl
  proof guards =
    research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py
  regression guards =
    research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
    research/06-cryptology-rsa/tests/test_scale_pgs_chain_modulus_link.py

required theorem artifact:
  status = incomplete
  evidence = proof workbench has bridge theorem candidate and T1/T2/T3 audit,
             not final theorem

Reciprocal floor-cell membership:
  status = closed arithmetic sublemma
  evidence = z in [T_N(u), T_N(l)] iff z*l <= N < (z + 1)*u;
             transported-story-law tests include exact carrier-zone
             floor-cell equivalence and integer-preimage equivalence

lower_threat certificate boundary:
  status = bounded
  evidence = PROOF.md supplies abstract T_<(w); public lower_threat identity
             comes from simple_pgs_generator.py certificate construction;
             deadline=threat branch has 12 ThreatMaterial rows

Lemma 1 prefix non-rewrite:
  status = incomplete
  evidence = PrefixMaterial candidate exists with 101 measured rows, 0
             effective, 101 prefix eliminations; strict/equal branches remain
             unproved against Psi(RB)

Lemma 2 suffix strict-descent:
  status = incomplete
  evidence = narrowed to threat-suffix Lemma 2A; ThreatMaterial candidate
             exists; implication against Psi(RB) remains unproved;
             tail suffix redundant on measured collapse but unproved

Lemma 3 recursive anchor recurrence:
  status = endpoint-history form closed, recursive-collapse theorem incomplete
  evidence = DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C, C'))
             gives not FreshEndpoint(C') => not DirectFrontier(C, C') by
             definition; measured recursive final survivor count is still not
             a theorem without Psi(RB)

Lemma 4 grammar projection:
  status = incomplete
  evidence = measured reduced-grammar bridge recorded; projection surface has
             50 rows and is not a row-wise Psi(RB) classifier for the 512-row
             direct transported-story surface; theorem unproved

Psi(RB) structural chamber-balance language:
  status = missing
  evidence = rejected raw novelty, ledger survivor state, broad non-rewrite,
             reduced grammar alone, threat/tail images alone, width alone,
             story-kind grammar alone, coarse interval occupancy, and finite
             RC table lookup; FrontierCommit_run is measured sound but misses
             52 effective rows and is not complete; observed RB-class lookup is
             measured perfect but is not an admissible definition; minimal
             Psi falsification and circularity contracts are recorded; broad
             threat/equal-prefix run-balance supersets and per-run
             coordinate-monotone balance regions are guarded invalid;
             RB classes are guarded as determining the induced-carrier
             interval symbol and source/induced lock-label relation on the
             measured surface; RB classes are guarded as determining the
             source deadline-threat boundary;
             TypedMaterial RB classes are guarded disjoint from
             non-TypedMaterial RB classes; PrefixMaterial and ThreatMaterial
             RB classes have a guarded six-class overlap; RB classes are
             guarded as determining the typed branch class;
             recurrence is guarded as FreshEndpoint state outside Psi(RB)

RB Sufficiency Sublemma:
  status = measured support guarded, structural proof missing
  evidence = RB determines carrier interval symbol, lock-label relation,
             deadline-threat boundary, and typed branch class on the measured
             512-row surface; proof for all valid transported certificate
             pairs is missing
  narrowed blocker = fixed grammar plus balances alone do not determine carrier
             position; symbolic O P O O and O O P O rows have the same OPO run
             collapse and induced balance but different carrier symbols
  recursive guard = recursive RB classes with mixed carrier symbols = 0 / 661;
             combined direct plus recursive RB classes with mixed carrier
             symbols = 0 / 661; combined direct plus recursive RB classes with
             mixed carrier run ordinals = 0 / 661
  non-target = combined RB classes with mixed exact carrier index = 5, so the
             target is collapsed interval-run localization, not exact event
             index reconstruction
  projection boundary = R alone has 12 carrier-run ambiguities; R plus source
             balance has 18; R plus induced balance has 17; R plus balance
             delta has 6; full RB has 0
  refinement boundary = deadline-threat is determined by source balance alone
             on the measured surface, with false at 8..31 and true at 32..34;
             carrier run, lock relation, and typed branch require full RB on
             the combined direct plus recursive surface
  next proof target = Carrier Localization Under Reciprocal Transport

ThreatMaterial(C, C') definition:
  status = candidate exists
  evidence = public strict threat-suffix predicate has 12 measured rows,
             0 effective, 12 direct eliminated, 0 stale; proof against Psi(RB)
             is missing

PrefixMaterial(C, C') definition:
  status = candidate exists
  evidence = public prefix predicate has 101 measured rows, 0 effective,
             101 prefix eliminations, including 25 strict and 76 equal lock
             rows; proof against Psi(RB) is missing

TypedMaterial(C, C') reduction:
  status = measured reduction exists
  evidence = PrefixMaterial or ThreatMaterial gives 107 rows, 0 effective,
             107 direct eliminated, with 3 redundant tail/non-threat direct
             eliminations outside theorem target; implication against Psi(RB)
             is missing

official runner:
  status = unresolved
  evidence = rsa_v2_40bit_static_001 and rsa_v2_50bit_static_001 remain
             unresolved_by_certificate_pair_not_closed

test surface:
  status = passing
  evidence = 34 transported-story-law tests, 44 rsa_v2 script tests, and 5
             modulus-link tests pass
  coverage limit = tests do not prove transported theorem or resolver promotion
```

The objective is therefore not complete. Do not report victory or mark the goal
complete until the missing Psi(RB) structural language and typed exclusion
theorem are proved, reviewed, implemented if needed, and verified.

The active grammar research track has a new measured result:

```text
inverse recursive grammar appears as component sharing with ordered-word
exclusion.
```

Solved rows reuse recursive pieces from the deterministic expanded surface, but
avoid that surface's ordered lag-2 + lag-3 reduced words.

## Current Commands

From `research/06-cryptology-rsa/experiments/rsa/v2`:

```bash
python3 build_ladder_fixtures.py
python3 run_experiment.py
python3 audit_experiment.py
pytest -q ../../../research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
```

Expected test result:

```text
44 passed
```

For the transported-story-law proof guards:

```bash
pytest -q ../../../research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py
```

Expected result:

```text
32 passed
```

From the repository root, also preserve:

```bash
PYTHONPATH=src/python pytest -q research/06-cryptology-rsa/tests/test_scale_pgs_chain_modulus_link.py
```

Expected result:

```text
5 passed
```

## Current Inference Result

The current `output/inference_rows.jsonl` state is:

```text
rsa_v2_40bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
```

The correct interpretation is:

```text
PGSPG certificate state is being derived, but no reviewed public invariant has
selected a factor pair.
```

## Current Audit Result

The current `output/audit_results.csv` state is:

```text
rsa_v2_40bit_static_001 integrity_pass inference_audit_fail
rsa_v2_50bit_static_001 integrity_pass inference_audit_fail
```

The audit factor file certifies the public moduli, but inference does not match
the audit factors because inference is unresolved.

## Active Algorithm

The active algorithm is:

```text
public N
-> isqrt(N) as orientation
-> previous public endpoint before isqrt(N)
-> lower PGSPG chamber-reset certificate
-> y = floor(N / lower.reset_endpoint)
-> previous public endpoint before y
-> upper PGSPG chamber-reset certificate
-> strict reciprocal certificate closure
-> resolved only if certificates mutually close
```

The current strict closure candidate requires:

```text
floor(N / lower.reset_endpoint) == upper.reset_endpoint
floor(N / upper.reset_endpoint) == lower.reset_endpoint
lower.reset_signature == upper.reset_signature
```

If those conditions fail, inference returns unresolved.

## Current 40-Bit Certificate Snapshot

```text
lower_reset_endpoint = 1048573
transported_upper_endpoint = 1048574
upper_reset_endpoint = 1048583
transported_lower_endpoint = 1048564
closure_status = unresolved_by_certificate_pair_not_closed
```

## Current 50-Bit Certificate Snapshot

```text
lower_reset_endpoint = 32053649
transported_upper_endpoint = 32053634
upper_reset_endpoint = null
transported_lower_endpoint = null
closure_status = unresolved_by_certificate_pair_not_closed
```

## Invalidated Rules

Do not revive:

- fixed additive chambers around `isqrt(N)`;
- radius-limited candidate generation;
- endpoint-walk budgets as solver coverage;
- raw reset-deadline margin equality;
- stationary recursive rounds that revisit the same endpoint;
- product closure as the PGS contraction rule;
- `N % x`, `gcd`, factor APIs, or primality APIs inside inference;
- audit factors or answer-bearing PGS-state fixtures inside inference;
- per-bit or per-rung resolver branches.

The previous 40-bit resolution was withdrawn because it depended on a
close-factor shape. Do not treat that result as a live solve.

## Current Grammar Evidence

Read these before extending the grammar track:

```text
PGS_GRAMMAR_EVIDENCE_FINDINGS.md
GRAMMAR_EVIDENCE_STATUS.md
GRAMMAR_PATTERN_SCAN.md
INVERSE_WORD_EXCLUSION_FINDING.md
output/grammar_inverse_word_exclusion/summary.json
output/fresh_rsa_challenge_inverse_word_exclusion/summary.json
```

Current inverse-word measurement:

```text
global scope:
  solved rows: 48
  lag-2 hits: 30
  lag-3 hits: 29
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 40

public-cell scope:
  solved rows: 48
  lag-2 hits: 14
  lag-3 hits: 11
  lag-2 + lag-3 word hits: 0
  component-sharing word exclusions: 22
```

Current grammar interpretation:

```text
The inverse relation is not a simple low/high opposition. It is component
sharing with ordered-word exclusion.
```

Fresh-row status:

```text
The RSA-100 fresh solved-row test has been run. It preserves the same shape:
component sharing exists, combined lag-2 + lag-3 ordered-word hits remain 0,
and full recursive reduced-word hits remain 0.
```

Status separation:

```text
hypothesis: public grammar excludes incompatible ordered recursive words
measured result: solved rows share pieces but avoid expanded lag-2 + lag-3 words
proof status: not proved
resolver status: not integrated
unresolved state: derive and falsify a public PGS exclusion rule from
certificate-side data
```

Next grammar task:

```text
Use the Grammar Projection Lemma in TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md
to derive the ordered lag-2 + lag-3 exclusion as the reduced grammar image of
transported story conflict.
```

## Live Files

Read these before changing the algorithm:

- `AGENTS.md`;
- `README.md`;
- `TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md`;
- `ALGORITHM.md`;
- `ARITHMETIC.md`;
- `METRICS.md`;
- `PGS_CERTIFICATE.md`;
- `run_experiment.py`;
- `research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py` from the repository root.

The repository-level continuity bootstrap is:

```text
research/00-index/continuity/START_HERE.md
```

## Grok Requirement For Rule Changes

Before major RSA/PGS rule changes, use Grok through the `second-opinion` skill.

Give Grok:

- the exact proposed rule;
- relevant `run_experiment.py` excerpts;
- current `survivor_rows.jsonl` rows;
- known invalidated rules;
- the current unresolved outputs;
- the specific question the new rule must answer.

Ask Grok to look for:

- hidden classical gates;
- product-closure leakage;
- audit leakage;
- non-invariant comparisons;
- false resolution risk;
- falsification tests.

Record substantial sessions in:

```text
grok_sessions/YYYY-MM-DD-topic.md
```

## Next Valid Work

The next valid mathematical task is to prove or falsify the typed transported
non-rewrite law stated in `TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md`:

```text
prefix + lower/equal lock label => committed-prefix rewrite, not new frontier
suffix + lower lock label + deadline=threat => committed-threat-horizon rewrite,
  not new frontier
repeated recursive frontier anchor => recurrent frontier material, not new frontier
```

Until those lemmas are proved, reviewed, implemented as an official rule, and
tested, the correct inference status is unresolved.

## Pause Point: 2026-05-08

Current clean pause state:

```text
strongest measured result:
  transported_story_law_v1 reconstructs the transported ledger collapse from
  public PGSPG certificate stories

measured counts:
  row_count = 512
  ledger_effective_survivor_count = 202
  recursive_row_count = 713
  recursive_final_survivor_count = 0

latest guard suite:
  pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py
  32 passed in 200.59s

official runner:
  rsa_v2_40bit_static_001 unresolved_by_certificate_pair_not_closed
  rsa_v2_50bit_static_001 unresolved_by_certificate_pair_not_closed
```

Proof boundary at pause:

```text
Carrier Localization Under Reciprocal Transport:
  measured boundary sharpened, proof missing

Psi(RB):
  structural definition missing

typed exclusion:
  PrefixMaterial(C, C') => not Psi(RB(C, C')) unproved
  ThreatMaterial(C, C') => not Psi(RB(C, C')) unproved

resolver promotion:
  blocked
```

Measured RB refinement state:

```text
carrier-run localization requires full RB on the combined direct plus
recursive public surface:
  R alone ambiguous = 12
  R plus source balance ambiguous = 18
  R plus induced balance ambiguous = 17
  R plus balance delta ambiguous = 6
  full RB ambiguous = 0

deadline-threat state is determined by source balance alone on the measured
surface:
  source_balance = 8..31  => false
  source_balance = 32..34 => true

do not strengthen RB into exact event-index reconstruction:
  combined RB classes with mixed exact carrier index = 5
```

Next valid task:

```text
derive or falsify Carrier Localization Under Reciprocal Transport as a
structural law over valid transported certificate pairs, then use it inside RB
Sufficiency before defining Psi(RB).
```
