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

## Exact `PROOF.md` Dependency Map

`PROOF.md` supplies local source-chamber laws for one consecutive-prime
interval. In certificate notation, let the source chamber have endpoint
`r(C)=q`, carrier `w(C)=w`, and label `lambda(C)=tau(w)`.

The proved local statements available for Lemma 1 and Lemma 2 are:

```text
Endpoint interval:
  I(C) = {a(C)+1, ..., r(C)-1}
  every n in I(C) is composite

GWR / carrier selection:
  w(C) = min{n in I(C): tau(n) = min_{m in I(C)} tau(m)}

Leftmost strictness:
  if a(C) < k < w(C), then tau(k) > lambda(C)

NLSC / right-side non-descent:
  there is no t with w(C) < t < r(C) and tau(t) < lambda(C)

Threat horizon consequence:
  if T_<(w(C)) = min{t > w(C): tau(t) < lambda(C)} exists,
  then r(C) <= T_<(w(C)).
```

The threat-horizon consequence is a direct restatement of NLSC: a first later
lower-divisor point cannot lie inside the source prime-gap interval before the
reset endpoint.

The proved local statements support these proof steps:

```text
Lemma 1 strict prefix branch:
  a lower-label source lift inside (w(C), r(C)) is incompatible with NLSC.

Lemma 1 equal-label prefix branch:
  an equal-label source lift later than w(C) is not a new leftmost carrier for
  the source chamber, because GWR has already selected the first minimum.

Lemma 2A threat-suffix branch:
  when d(C) = T_<(w(C)), the source reset endpoint is no later than the first
  lower-divisor threat, so [r(C), d(C)] is the endpoint-to-threat horizon.
```

The proved local statements do not supply these transported statements:

```text
reciprocal floor commitment:
  T_N-images of source committed segments remain committed material for the
  induced opposite certificate.

transported label comparability:
  lambda(C') <= lambda(C) has the same ordering role as a source-side divisor
  count comparison after floor transport.

transported frontier exclusion:
  committed transported material cannot also be a new valid transported
  frontier commitment.

Psi(RB):
  a public chamber-balance language separating direct frontier states from
  transported material states.
```

Therefore local GWR/NLSC are necessary source laws for Lemma 1 and Lemma 2A,
but they are not sufficient by themselves. The missing theorem is the
reciprocal transport law that carries those local source commitments through
`T_N` into the induced opposite certificate state.

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

## Lemma 1 And Lemma 2 Derivation Start

This section records the current proof derivation state. It does not promote
`transported_story_law_v1` to theorem status.

### Exact GWR/NLSC Inputs From `PROOF.md`

The required proved input is the local prime-gap theorem.

Terminology normalization:

```text
GWR names the `PROOF.md` selected-integer fact:
  w is the first interior integer with the minimum divisor count.

NLSC names the `PROOF.md` right-side non-descent consequence:
  no later interior point before q has divisor count below tau(w).

Neither name adds a transported theorem, a reciprocal-floor theorem, or a
post-reset deadline theorem beyond what PROOF.md proves.
```

For consecutive primes `p < q` with nonempty interior

$$I=\{p+1,\ldots,q-1\},$$

define

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}.$$

Then `w` is the leftmost interior integer with minimum divisor count. In the
certificate language, `w` is the GWR carrier and

$$\lambda=\tau(w).$$

The left side of the carrier satisfies:

$$k<w,\ k\in I \Rightarrow \tau(k)>\lambda.$$

The right side of the carrier satisfies:

$$w<t<q \Rightarrow \tau(t)\ge \lambda.$$

The strict form used as NLSC is:

$$T_{<}(w)=\min\{n>w:\tau(n)<\tau(w)\}\quad\Rightarrow\quad q\le T_{<}(w),$$

when the set defining `T_<` is nonempty. Equivalently, no later interior
composite with strictly smaller divisor count occurs before the endpoint `q`.

These statements are local to one committed prime-gap interval. They do not, by
themselves, say how a reciprocal floor image inherits the same chamber
commitment.

### RSA v2 Certificate Identification Kernel

The RSA v2 certificate object supplies public names for the local theorem
objects. For a public previous-endpoint anchor `a`, the certificate runner calls
the PGSPG chamber-reset generator at `a` and records:

```text
r(C) = reset_endpoint = emitted q
w(C) = carrier_w
lambda(C) = lock_carrier_d
d(C) = reset_deadline_value
```

The local theorem from `PROOF.md` supports the following identifications when
the certificate is present and the generator has resolved the chamber:

```text
Endpoint identity:
  r(C) is the next emitted endpoint after a(C).

Carrier identity:
  w(C) is the first interior integer with the minimum divisor count in
  (a(C), r(C)).

Left-side strictness:
  every earlier interior point before w(C) has divisor count > lambda(C).

Right-side non-descent:
  no point between w(C) and r(C) has divisor count < lambda(C).

Threat horizon:
  PROOF.md supports the abstract statement that if
  T_<(w(C)) = min{n > w(C): tau(n) < lambda(C)} exists, then
  r(C) <= T_<(w(C)).
```

These are source-chamber facts. They justify the local carrier/reset/deadline
vocabulary used below.

The public `lower_threat` field is not a separate theorem in `PROOF.md`. It is
an implementation/certificate field: `simple_pgs_generator.py` scans offsets
after the locked carrier and records the first composite offset with divisor
count below `lock_carrier_d`. When that field is present and used as the
deadline, the proof may identify it with `T_<(w(C))`; the identification comes
from the certificate construction, not from an additional transported theorem.

They do not prove:

```text
floor transport preserves carrier commitment;
floor transport preserves lock-label comparability;
an induced opposite certificate is measuring the transported source segment;
a transported equal-label prefix carrier is non-frontier;
a transported strict lower suffix carrier is non-frontier;
RC(C, C') is a frontier/non-frontier invariant.
```

Those statements are the new transported proof obligations. Treating any of
them as already proved by `PROOF.md` is the closed route.

### Reciprocal Floor Cell Lemma

The reciprocal floor map gives one exact public arithmetic fact before any
frontier interpretation enters.

Let

$$T_N(x)=\lfloor N/x\rfloor.$$

For positive integers `l < u` and integer `z`,

$$z\in[T_N(u),T_N(l)]$$

if and only if

$$zl\le N < (z+1)u.$$

Proof:

```text
z <= floor(N / l)  iff  z l <= N
floor(N / u) <= z  iff  N / u < z + 1  iff  N < (z + 1)u
```

Therefore the transported prefix and suffix carrier-zone predicates have the
following exact public forms:

```text
w(C') in [T_N(r(C)), T_N(w(C))]
iff
w(C') w(C) <= N < (w(C') + 1) r(C)

w(C') in [T_N(d(C)), T_N(r(C))]
iff
w(C') r(C) <= N < (w(C') + 1) d(C)
```

This closes only the floor-membership part of the proof. It does not prove that
the floor cell is committed story material, and it does not define `Psi(RB)`.

### Integer Preimage Refinement

Membership in the closed floor-image interval is not, by itself, the same as
integer source-preimage existence. The exact integer-preimage condition is:

```text
there exists integer y in [l, u] with floor(N / y) = z
iff
max(l, floor(N / (z + 1)) + 1) <= min(u, floor(N / z)).
```

Measured support on `transported_story_law_v1`:

```text
prefix carrier-zone rows = 109
prefix integer-preimage rows = 109
prefix symmetric difference = 0

suffix carrier-zone rows = 219
suffix integer-preimage rows = 219
suffix symmetric difference = 0
```

The measured integer preimage is always a singleton on the current surface:

```text
prefix carrier-zone singleton preimages = 109 / 109
suffix carrier-zone singleton preimages = 219 / 219
PrefixMaterial singleton preimages = 101 / 101
ThreatMaterial singleton preimages = 12 / 12
```

This refines the public arithmetic side of the transported zones. It still does
not prove that the integer preimage inherits the source chamber's carrier,
deadline, or lock-label commitment.

The stronger recorded-event shortcut fails:

```text
prefix carrier-zone rows = 109
prefix rows with recorded source story-event preimage = 42

suffix carrier-zone rows = 219
suffix rows with recorded source story-event preimage = 58

PrefixMaterial rows = 101
PrefixMaterial rows with recorded source story-event preimage = 36

ThreatMaterial rows = 12
ThreatMaterial rows with recorded source story-event preimage = 9
```

Therefore the remaining commitment theorem cannot require the induced carrier to
be the reciprocal image of a recorded source story event. It must treat the whole
integer source segment as committed material, or prove a different structural
criterion for the unrecorded preimage points.

The unique lifted source integer also does not provide lock-label transport by
its own divisor count.

Measured comparison of `tau(floor(N / w(C')))` against source and induced lock
labels:

```text
PrefixMaterial, lift divisor count vs source lambda:
  lower = 21, equal = 18, higher = 62

PrefixMaterial, lift divisor count vs induced lambda:
  lower = 21, equal = 7, higher = 73

ThreatMaterial, lift divisor count vs source lambda:
  lower = 9, equal = 0, higher = 3

ThreatMaterial, lift divisor count vs induced lambda:
  lower = 6, equal = 2, higher = 4
```

Thus lock-label transport is not the statement that the lifted source integer's
ordinary divisor count equals either lock label. The remaining proof must explain
how the source and induced lock labels compare across reciprocal transport as
certificate commitments, not as direct equality of `tau` on the lifted integer.

The unique lift position classes further sharpen the commitment target:

```text
prefix carrier-zone lift positions:
  unrecorded_prefix_interior = 67
  reset = 27
  carrier = 11
  closed_offset = 4

suffix carrier-zone lift positions:
  unrecorded_suffix_interior = 161
  reset = 27
  closed_offset = 18
  deadline = 10
  lower_threat = 3

PrefixMaterial lift positions:
  unrecorded_prefix_interior = 65
  reset = 21
  carrier = 11
  closed_offset = 4

ThreatMaterial lift positions:
  reset = 6
  unrecorded_suffix_interior = 3
  lower_threat = 3
```

Therefore floor-cell commitment cannot be a theorem only about named source
story events. It must cover the committed integer segment between those events,
including unrecorded interior source integers.

For PrefixMaterial rows, the reset endpoint accounts for every measured source
lift whose ordinary divisor count falls below the source lock label. All
non-reset prefix lifts obey source-side non-descent:

```text
PrefixMaterial lift divisor-count relation to source lambda, by lift position:
  unrecorded_prefix_interior: higher = 60, equal = 5
  reset: lower = 21
  carrier: equal = 11
  closed_offset: higher = 2, equal = 2

PrefixMaterial non-reset lifts below source lambda = 0
```

This is the first positive local alignment for Lemma 1 after floor lifting. It
uses the source divisor-count field directly: away from the reset endpoint, the
integer lift inside the carrier-to-reset segment does not descend below
`lambda(C)`. It does not prove transported non-frontier status, because it does
not define `Psi(RB)`, transported label comparability, or floor-cell
commitment.

For ThreatMaterial rows, the lower source-lift cases are boundary cases. The
unrecorded suffix-interior lifts do not descend below the source lock label:

```text
ThreatMaterial lift divisor-count relation to source lambda, by lift position:
  reset: lower = 6
  unrecorded_suffix_interior: higher = 3
  lower_threat: lower = 3

ThreatMaterial unrecorded suffix-interior lifts below source lambda = 0
```

This aligns the narrowed Lemma 2A target with the source threat boundary:
measured source-side lower descent occurs at the reset endpoint or the named
lower-threat endpoint, not inside the unrecorded suffix interior. It does not
prove transported threat-horizon coherence.

### Conventional Restatement Of Lemma 1

Let `C` be a valid public PGSPG certificate with ordered commitment story

$$a(C)<w(C)<r(C)\le d(C).$$

Let

$$T_N(x)=\lfloor N/x\rfloor,$$

and let `C'` be the public certificate induced from the previous endpoint before
`T_N(r(C))`. Since `T_N` reverses order, the transported prefix is the image of
the source carrier-to-reset segment:

$$I_{\mathrm{prefix}}(C)=[T_N(r(C)),T_N(w(C))].$$

The prefix non-rewrite claim is:

$$w(C')\in I_{\mathrm{prefix}}(C),\quad \lambda(C')\le\lambda(C)
\Rightarrow C'\text{ is not a new transported frontier commitment.}$$

Using the reciprocal floor cell lemma, the same antecedent is:

$$w(C')w(C)\le N < (w(C')+1)r(C),\quad \lambda(C')\le\lambda(C).$$

### Lemma 1 Proof Skeleton

1. `C` commits `w(C)` as the leftmost minimum-divisor carrier of its source
   chamber, with label `lambda(C)`.
2. GWR gives leftmost uniqueness for the minimum label: an equal-label carrier
   later than `w(C)` cannot replace the already committed leftmost carrier.
3. NLSC gives strict right-side closure: a later carrier in the same committed
   chamber with label `< lambda(C)` cannot occur before the reset endpoint.
4. If `w(C')w(C) <= N < (w(C')+1)r(C)`, then `w(C')` lies in the reciprocal
   floor cell of the source carrier-to-reset segment. The remaining transport
   reading must show that this public cell is already committed material of `C`.
5. On the measured public surface, the unique source lift of a PrefixMaterial
   row has no non-reset descent below `lambda(C)`. The lower source-lift cases
   are exactly reset endpoint cases. This supports the source-side NLSC reading
   but does not prove the reciprocal transport step.
6. If `lambda(C') < lambda(C)`, then `C'` is a transported strict-descent
   rewrite of the committed carrier segment, contradicting the transported
   NLSC reading of step 3.
7. If `lambda(C') = lambda(C)`, then `C'` is not a strict NLSC contradiction.
   It is excluded only by the transported leftmost non-rewrite reading of GWR:
   an equal-label later carrier is a tie after the committed leftmost carrier,
   not a new frontier commitment.

The strict branch rests on NLSC after transport. The equal-label branch rests on
leftmost carrier uniqueness after transport. This distinction is necessary:
`PROOF.md` does not prohibit equal-label composites after `w`; it prevents them
from replacing the leftmost selected carrier.

### Lemma 1A And 1B Split

Lemma 1 has two different mathematical branches.

Threat-style strict prefix branch:

```text
w(C') in I_prefix(C)
lambda(C') < lambda(C)
=> transported strict-descent rewrite
```

This branch can only follow from NLSC after a transported prefix-coherence
lemma is proved.

Equal-label prefix branch:

```text
w(C') in I_prefix(C)
lambda(C') = lambda(C)
=> transported equal-label non-rewrite
```

This branch cannot follow from strict NLSC. It must follow from transported
GWR leftmostness: an equal-label carrier inside already committed prefix
material is a later tie against the committed leftmost carrier, not a new
frontier commitment.

The current collapse depends on this equal-label branch. Removing equal-label
prefix elimination while preserving strict prefix and suffix eliminations
changes the direct effective survivor count:

```text
with equal-label prefix elimination = 202
without equal-label prefix elimination = 268
```

So Lemma 1B carries 66 effective direct eliminations on the current public
surface. It is a core proof obligation, not a cosmetic strengthening.

### Lemma 1 Unresolved Sublemmas

The proof is blocked until these bridge statements are proved or falsified:

```text
Prefix transport coherence:
  w(C')w(C) <= N < (w(C') + 1)r(C) means C' is measuring the transported image
  of C's committed carrier-to-reset segment, not an unrelated opposite chamber
  segment.

Transported label comparability:
  lambda(C') <= lambda(C) has the same minimum-divisor ordering role after
  reciprocal floor transport that tau(u) <= tau(w(C)) has inside a source
  prime-gap chamber.

Equal-label frontier uniqueness:
  a transported equal-label carrier in the committed prefix is a non-rewrite
  tie, not a new public frontier state.

Floor-cell commitment:
  exact floor-cell membership is public arithmetic, but the proof still needs a
  transport law saying the cell inherits source carrier-to-reset commitment.
```

### Minimal Lemma 1 Counterexample Condition

A public counterexample to Lemma 1 has this exact shape:

```text
C is a valid public PGSPG certificate
C' is induced from previous_endpoint(T_N(r(C)))
w(C') in [T_N(r(C)), T_N(w(C))]
equivalently w(C')w(C) <= N < (w(C') + 1)r(C)
lambda(C') <= lambda(C)
C' supplies a new transported frontier commitment under GWR/NLSC
```

If `lambda(C') < lambda(C)`, the counterexample falsifies prefix transport
coherence plus transported NLSC. If `lambda(C') = lambda(C)`, it falsifies the
equal-label frontier uniqueness sublemma, not the local GWR theorem in
`PROOF.md`.

### PrefixMaterial Definition Candidate

Define `PrefixMaterial(C, C')` by the following public conditions:

```text
1. C' is the induced opposite certificate from previous_endpoint(T_N(r(C))).
2. w(C') in [T_N(r(C)), T_N(w(C))].
3. lambda(C') <= lambda(C).
```

Equivalent implementation-level public predicates on the current story-law
rows:

```text
induced_carrier_in_prefix_zone = true
induced_lock_carrier_d <= source_lock_carrier_d
```

This definition is non-circular:

```text
it does not read DirectFrontier(C, C')
it does not read Psi(RB(C, C'))
it does not read ledger_prefix_elimination
it does not read ledger_effective_survivor
it does not read recursive survivor state
```

Measured support:

```text
PrefixMaterial rows = 101
effective = 0
prefix_elimination = 101
strict lock descent rows = 25
equal lock rows = 76
stale overlap rows = 10
```

The remaining theorem obligation is:

```text
PrefixMaterial(C, C') => not Psi(RB(C, C'))
```

This implication splits into the two Lemma 1 branches:

```text
lambda(C') < lambda(C): transported strict-descent prefix material
lambda(C') = lambda(C): transported equal-label prefix material
```

The second branch remains essential because the equal-label rows carry 76
measured prefix eliminations.

### TypedMaterial Reduction

Define the typed material predicate:

```text
TypedMaterial(C, C') := PrefixMaterial(C, C') or ThreatMaterial(C, C')
```

Measured direct surface:

```text
row_count = 512
PrefixMaterial rows = 101
ThreatMaterial rows = 12
PrefixMaterial and ThreatMaterial overlap = 6
TypedMaterial rows = 107

TypedMaterial effective rows = 0
TypedMaterial direct eliminated rows = 107
TypedMaterial stale overlap rows = 10

non-TypedMaterial effective rows = 202
non-TypedMaterial direct eliminated rows = 3
non-TypedMaterial stale rows = 203
```

The three direct eliminated non-`TypedMaterial` rows are the measured redundant
tail/non-threat suffix rows already left outside the theorem target.

Therefore the typed theorem candidate reduces to:

```text
TypedMaterial(C, C') => not Psi(RB(C, C'))
```

This reduction is measured evidence. It does not prove the implication, and it
does not define `Psi(RB)`.

### Conventional Restatement Of Lemma 2

Using the same certificate notation, the transported suffix is the image of the
source reset-to-deadline segment:

$$I_{\mathrm{suffix}}(C)=[T_N(d(C)),T_N(r(C))].$$

The suffix strict-descent claim is:

$$w(C')\in I_{\mathrm{suffix}}(C),\quad \lambda(C')<\lambda(C)
\Rightarrow C'\text{ is not a new transported frontier commitment.}$$

Using the reciprocal floor cell lemma, the same antecedent is:

$$w(C')r(C)\le N < (w(C')+1)d(C),\quad \lambda(C')<\lambda(C).$$

### Lemma 2 Proof Skeleton

1. `C` commits `w(C)` with label `lambda(C)` and then resets at `r(C)`.
2. NLSC controls the source chamber only up to the reset endpoint: no later
   interior composite before `r(C)` has divisor count `< lambda(C)`.
3. The suffix interval is not the carrier-to-reset interior. It is the
   transported image of the reset-to-deadline story.
4. Therefore Lemma 2 needs a reset-deadline commitment statement in addition to
   the local GWR/NLSC theorem: after `r(C)` has reset the source chamber, the
   public story through `d(C)` remains committed transport material for the
   reciprocal frontier.
5. Under that reset-deadline transport commitment, an induced carrier satisfying
   `w(C')r(C) <= N < (w(C')+1)d(C)` with `lambda(C') < lambda(C)` is a strict
   lower-divisor descent inside committed transported suffix material, so it is
   excluded as a new frontier state.

The strict inequality is essential. Unlike Lemma 1, no equal-label suffix
predicate is currently claimed.

### Lemma 2A: Threat-Suffix Strict-Descent Candidate

The deadline used by the implementation is:

```text
d(C) = first available offset among:
  first post-reset tail offset,
  first lower-divisor threat offset after w(C),
  candidate bound
```

When `deadline=threat`, the deadline has direct NLSC meaning:

$$d(C)=T_{<}(w(C)),$$

the first later composite after `w(C)` with divisor count below
`lambda(C)`, as observed inside the public certificate chamber.

The narrowed theorem candidate is:

$$\begin{aligned}
&d(C)=T_{<}(w(C)),\\
&w(C')r(C)\le N < (w(C')+1)d(C),\\
&\lambda(C')<\lambda(C)
\end{aligned}
\Rightarrow C'\text{ is not a new transported frontier commitment.}$$

This is the suffix claim that currently matters for the measured collapse.
The `deadline=tail` suffix rows are not promoted by this narrowed candidate.

Proof skeleton:

1. `C` locks `w(C)` with label `lambda(C)`.
2. `d(C)=T_<(w(C))` is the first later lower-divisor threat in the public
   chamber story.
3. NLSC says the valid source endpoint must satisfy
   `r(C) <= T_<(w(C))`. In the certificate story, the reset endpoint `r(C)`
   is therefore the committed endpoint before the lower-divisor threat.
4. The public inequality `w(C')r(C) <= N < (w(C')+1)d(C)` places `w(C')` in the
   reciprocal floor cell of the committed endpoint-to-threat horizon.
5. On the measured public surface, the lower source-lift cases for
   ThreatMaterial are exactly reset or lower-threat boundary cases; unrecorded
   suffix-interior lifts do not descend below `lambda(C)`. This supports the
   narrowed threat-horizon reading but does not prove transported
   threat-horizon coherence.
6. If `lambda(C') < lambda(C)`, then `C'` tries to install the lower-divisor
   threat as an opposite-side frontier carrier inside material already bounded
   by the source NLSC horizon.
7. Under transported threat-horizon coherence, that is a transported strict
   rewrite rather than a new frontier commitment.

The remaining proof bridge is narrower than the full suffix lemma:

```text
Transported threat-horizon coherence:
  the reciprocal image of [r(C), T_<(w(C))] is committed horizon material;
  an induced lower-label carrier inside that image is the transported image of
  the same NLSC threat boundary, not an independent opposite frontier.
```

Minimal counterexample condition for Lemma 2A:

```text
C has deadline=threat
C' is induced from previous_endpoint(T_N(r(C)))
w(C')r(C) <= N < (w(C') + 1)d(C)
lambda(C') < lambda(C)
C' supplies a new transported frontier commitment
```

Such a row would falsify transported threat-horizon coherence. It would not
falsify local GWR/NLSC inside `PROOF.md`.

### Lemma 2 Unresolved Sublemmas

The proof is blocked until these bridge statements are proved or falsified:

```text
Reset-deadline commitment:
  the public reset-to-deadline story d(C) is committed material for reciprocal
  frontier transport, not merely source-side post-reset tail data.

Suffix transport coherence:
  w(C')r(C) <= N < (w(C') + 1)d(C) means C' is measuring that committed
  transported suffix.

Transported strict-descent transfer:
  lambda(C') < lambda(C) inside the transported suffix has the same exclusion
  force as a lower-divisor threat inside a GWR/NLSC-locked chamber.

Deadline boundary coherence:
  the implementation deadline d(C), whether tail, threat, or bound, has a
  single mathematical status strong enough for the suffix lemma.
```

### Minimal Lemma 2 Counterexample Condition

`PROOF.md` alone does not rule out a lower-divisor carrier in material that has
already passed the reset endpoint, because GWR/NLSC are local to one prime-gap
interior. A public counterexample to Lemma 2 has this exact shape:

```text
C is a valid public PGSPG certificate
C' is induced from previous_endpoint(T_N(r(C)))
w(C')r(C) <= N < (w(C') + 1)d(C)
lambda(C') < lambda(C)
C' supplies a new transported frontier commitment under GWR/NLSC
the suffix point is not governed by a proved reset-deadline commitment law
```

This would not contradict the proved local GWR/NLSC theorem. It would show that
the suffix predicate needs a stronger transported reset-deadline law than the
one currently proved in `PROOF.md`.

### Existing Row Pressure On The Bridge Sublemmas

The current public `transported_story_law_v1` rows sharpen the proof target.
They do not prove the lemmas.

Prefix eliminations split as:

```text
total prefix eliminations = 101
lambda(C') < lambda(C) = 25
lambda(C') = lambda(C) = 76
```

The 76 equal-label prefix eliminations mean Lemma 1 cannot be derived from the
strict NLSC inequality alone. The proof must establish transported equal-label
frontier uniqueness.

The equal-label prefix rows are not only boundary coincidences:

```text
equal-label prefix at transported interior = 61
equal-label prefix at transported low endpoint = 14
equal-label prefix at transported high endpoint = 1
```

So floor-image endpoint collapse is not the whole equal-label issue. The main
obligation is genuinely a transported non-rewrite rule for equal-label carriers
inside the committed prefix.

Suffix eliminations split as:

```text
total suffix eliminations = 16
lambda(C') < lambda(C) = 16
lambda(C') = lambda(C) = 0
```

The suffix predicate is therefore a strict-descent predicate on the measured
surface.

Its source deadline provenance is:

```text
suffix eliminations with deadline=threat = 12
suffix eliminations with deadline=tail = 4
```

The 4 `deadline=tail` suffix rows mean Lemma 2 cannot be proved only as a
lower-threat commitment law. It must either prove reset-deadline commitment for
post-reset tail material or narrow the suffix predicate to the `deadline=threat`
case and mark the `deadline=tail` suffix rows unresolved.

The current collapse does not depend on the tail-suffix rows. If Lemma 2 is
narrowed to `deadline=threat` suffix descent, the existing public rows preserve:

```text
direct effective survivors = 202
recursive depth 0 survivors = 200
recursive depth 1 survivors = 1
recursive final survivors = 0
```

The 4 `deadline=tail` suffix rows are redundant on this measured surface:

```text
1 row is also prefix-eliminated
3 rows are stale transported states
```

So the sharper proof path is:

```text
prove Lemma 2 first for deadline=threat suffix descent;
keep deadline=tail suffix descent as an unresolved extension unless a
reset-deadline tail commitment law is proved.
```

The current row pressure therefore reduces the next proof work to two exact
questions:

```text
Lemma 1:
  Does transported GWR preserve equal-label non-rewrite inside the prefix?

Lemma 2:
  Does transported strict descent hold for deadline=threat suffix rows?
  Does reset-deadline commitment also include tail deadlines, or should tail
  suffix descent stay unresolved?
```

### Proof-Source Insufficiency Result

The current `PROOF.md` foundation does not by itself prove Lemma 1B or Lemma
2A.

This is a structural obstruction, not a missing row count.

The proved GWR/NLSC statements quantify over one prime-gap interval:

```text
p < q consecutive primes
I = {p + 1, ..., q - 1}
w = leftmost minimum-divisor integer in I
no later interior t with tau(t) < tau(w) before q
```

Those statements do not mention:

```text
public modulus N
T_N(x) = floor(N / x)
previous_endpoint(T_N(r(C)))
the induced opposite certificate C'
comparability of lambda(C') with lambda(C)
frontier novelty under reciprocal transport
```

Therefore the implication

```text
local GWR/NLSC for C
=> transported prefix/suffix exclusion for C'
```

requires an additional transport law. The current candidates are:

```text
Transported equal-label prefix non-rewrite:
  equal-label carriers in the transported committed prefix are ties against the
  already committed leftmost carrier, not new frontier commitments.

Transported threat-horizon coherence:
  the reciprocal image of a source NLSC threat horizon is committed horizon
  material on the induced opposite side.
```

Without one of these transport laws, an induced certificate satisfying the
local GWR theorem in its own chamber can coexist with the source certificate
satisfying local GWR/NLSC. Local correctness of both chambers does not decide
whether the induced certificate is a new transported frontier state or a
rewrite of committed source story material.

So the current status is:

```text
proved: local GWR/NLSC
measured: transported story-law collapse
unproved: the transport law that turns local GWR/NLSC into transported
  non-rewrite
```

This blocks theorem promotion and resolver promotion.

### Local-Only Counterexample Pressure

The current public rows contain concrete pressure against any proof that uses
only local GWR/NLSC.

For Lemma 1B, there are fresh induced certificates with equal lock label whose
carrier lies in the transported prefix. Example:

```text
case_id = rsa_v2_40bit_static_001
source_anchor = 1048507
source_w = 1048511
source_r = 1048517
lambda(C) = 4
I_prefix(C) = [1048631, 1048637]
induced_anchor = 1048627
induced_w = 1048631
induced_r = 1048633
lambda(C') = 4
induced certificate exists = true
frontier_new_transport_state = true
```

For Lemma 2A, there are fresh induced certificates with smaller lock label whose
carrier lies in a transported `deadline=threat` suffix. Example:

```text
case_id = rsa_v2_40bit_static_001
source_anchor = 1047469
source_w = 1047473
source_r = 1047479
source_d = 1047481
lambda(C) = 6
I_suffix(C) = [1049668, 1049670]
induced_anchor = 1049663
induced_w = 1049669
induced_r = 1049677
lambda(C') = 4
induced certificate exists = true
frontier_new_transport_state = true
```

These are not counterexamples to local GWR/NLSC. They are counterexamples to
the stronger claim that local GWR/NLSC alone excludes the induced certificate.
Each induced certificate is locally valid as a certificate object. The missing
step is exactly the transported non-rewrite law that reclassifies the induced
certificate as a rewrite of committed source story material rather than as a
new transported frontier state.

### Local GWR/NLSC Non-Entailment Lemma

Local GWR/NLSC does not entail transported story-law exclusion.

Formal status:

```text
proved negative result for the current proof source
```

Argument:

1. `PROOF.md` proves statements over one ordered prime-gap interval
   `(p, q)`.
2. A PGSPG certificate `C` packages one such local chamber commitment.
3. The induced certificate `C'` is constructed by applying
   `previous_endpoint(T_N(r(C)))` and then building a new local PGSPG
   certificate at that induced anchor.
4. Local GWR/NLSC can hold for `C`.
5. Local GWR/NLSC can also hold for `C'`.
6. The predicate "C' is a new transported frontier commitment" is not a
   predicate in `PROOF.md`.
7. Therefore local GWR/NLSC alone cannot decide whether `C'` is a new
   transported frontier state or a rewrite of committed transported source
   material.

The public examples above instantiate the obstruction on the measured surface.
They show locally valid fresh induced certificates satisfying the transported
forbidden-zone antecedents. Since the local theorem language has no frontier
novelty predicate, it supplies no contradiction.

The transport law still needed has the exact form:

```text
source local chamber commitment
+ reciprocal floor image of committed story material
+ induced opposite certificate
=> induced certificate is a rewrite, not a new frontier state
```

This negative result closes one proof route:

```text
closed route:
  derive Lemma 1B or Lemma 2A directly from PROOF.md local GWR/NLSC

open route:
  prove a new transported non-rewrite law whose hypotheses include reciprocal
  floor image state and frontier novelty
```

### Existing Commitment-Ledger Constraint

The existing `transported_commitment_story_ledger_v1` sidecar confirms that the
open route is already materialized as public story data, but it also prevents a
too-broad proof claim.

Measured commitment-ledger summary:

```text
row_count = 512
story_rewrite_count = 276
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
```

The broad `story_rewrite` predicate is not itself an exclusion law:

```text
story_rewrite and not effective survivor = 152
story_rewrite and effective survivor = 124
```

So the next transport theorem cannot say:

```text
any transported committed-story rewrite is impossible
```

The theorem must be narrower. The measured elimination predicates currently
used by the collapse are:

```text
prefix + lower/equal lock label
suffix + lower lock label
frontier recurrence/staleness
```

The proof target is therefore a typed transported non-rewrite law, not a broad
rewrite ban.

### Typed Transported Non-Rewrite Law Candidate

The next theorem candidate should be stated as a typed law over the public
transported story fields:

```text
C = source public PGSPG certificate
C' = induced opposite public PGSPG certificate
z(C, C') = transported zone occupied by w(C')
rho(C, C') = relation between lambda(C') and lambda(C)
```

where:

```text
z(C, C') in {prefix, suffix, outside}
rho(C, C') in {lower, equal, higher, missing}
```

The candidate typed exclusion law is:

```text
z(C, C') = prefix and rho(C, C') in {lower, equal}
=> C' is a rewrite of committed prefix material, not a new frontier state

z(C, C') = suffix and rho(C, C') = lower and deadline(C) = threat
=> C' is a rewrite of committed threat-horizon material, not a new frontier state

a(C') in prior recursive frontier
=> C' is recurrent frontier material, not a new frontier state
```

Here "new frontier state" means valid transported frontier commitment after
typed rewrite tests. It is not the same as the sidecar field
`frontier_new_transport_state`, which records raw induced-anchor novelty before
ledger elimination.

The distinction is necessary because the measured surface contains rows with:

```text
frontier_new_transport_state = true
ledger_prefix_elimination = true
```

Those rows are raw new induced anchors, but they are not accepted as new
transported frontier commitments under the typed theorem candidate.

Everything else remains outside the theorem candidate:

```text
z(C, C') = outside
z(C, C') = suffix and rho(C, C') = equal
z(C, C') = suffix and deadline(C) = tail
z(C, C') in {prefix, suffix} and rho(C, C') = higher
missing induced lock labels
```

This candidate exactly matches the current proof pressure:

```text
Lemma 1A: prefix + lower
Lemma 1B: prefix + equal
Lemma 2A: suffix + lower + deadline=threat
Lemma 3: repeated recursive frontier anchor
```

It also preserves unresolved state:

```text
tail-suffix descent remains unresolved
broad story_rewrite remains non-theorem
official PGSMD inference remains unresolved
```

### Typed Candidate Coverage Audit

Applied to the current public rows, the typed theorem candidate has this direct
coverage:

```text
typed direct eliminated union = 107
typed direct effective survivors = 202
```

The typed direct eliminations split as:

```text
prefix + equal + deadline=tail = 76
prefix + lower + deadline=tail = 2
prefix + lower + deadline=threat = 23
suffix + lower + deadline=threat = 6
```

This typed candidate is narrower than the original measured ledger:

```text
original ledger eliminated rows = 110
typed candidate eliminated rows = 107
```

The difference is exactly the redundant tail-suffix material already marked
outside the theorem candidate. The typed candidate still preserves the measured
collapse:

```text
direct effective survivors = 202
recursive depth 0 survivors = 200
recursive depth 1 survivors = 1
recursive final survivors = 0
```

This is coverage evidence, not proof. It shows that proving the typed theorem
candidate would recover the current transported-story collapse without proving
the unresolved tail-suffix extension or the broad `story_rewrite` predicate.

### Typed Theorem Proof Decomposition

The typed theorem candidate reduces to three proof obligations.

#### T1: Prefix Commitment Transport

Statement:

```text
If w(C') lies in I_prefix(C) and lambda(C') <= lambda(C),
then C' is measuring committed carrier-to-reset material from C.
```

Required mechanism:

```text
T_N([w(C), r(C)]) = [T_N(r(C)), T_N(w(C))]
```

must preserve commitment identity, not divisor-count equality. The proof does
not need `tau(T_N(x)) = tau(x)`, which is false as a general expectation. It
needs only that the induced certificate's carrier lies in the transported image
of a source segment already committed by the source certificate story.

If `lambda(C') < lambda(C)`, the induced carrier is a strict transported
descent inside committed prefix material.

If `lambda(C') = lambda(C)`, the induced carrier is an equal-label transported
tie inside committed prefix material. This is Lemma 1B and is the essential
equal-label non-rewrite branch.

#### T2: Threat-Horizon Transport

Statement:

```text
If deadline(C) = threat,
w(C') lies in I_suffix(C),
and lambda(C') < lambda(C),
then C' is measuring committed endpoint-to-threat material from C.
```

Required mechanism:

```text
d(C) = T_<(w(C))
T_N([r(C), d(C)]) = [T_N(d(C)), T_N(r(C))]
```

must preserve the NLSC threat-horizon commitment. The proof does not require
the full reset-to-deadline story for `deadline=tail`. It only needs the source
NLSC fact that `r(C)` has reset before the first lower-divisor threat.

This is Lemma 2A.

#### T3: Frontier Commitment Exclusivity

Statement:

```text
If C' measures transported committed material from C, then C' cannot also be a
new valid transported frontier commitment for the same transported story.
```

This is the missing transport law. It is not contained in local GWR/NLSC.
It must be proved as a PGSPG endpoint-chain law over transported story
commitments.

T3 must not be made true by definition. If "new valid transported frontier
commitment" is defined as "not a rewrite," then T3 is circular and proves
nothing. The proof needs an independent frontier-commitment criterion.

Required separation:

```text
frontier novelty:
  raw induced-anchor novelty before ledger elimination

frontier commitment:
  a PGSPG certificate state that contributes a new transported endpoint-chain
  commitment under an independently stated frontier rule

rewrite exclusion:
  a typed law that prevents committed transported source material from being
  counted again as a new frontier commitment
```

The missing theorem is therefore not:

```text
rewrite => not rewrite
```

It is:

```text
independent frontier rule accepts only states that are not typed rewrites of
already committed transported story material
```

Current implementation status:

```text
frontier_new_transport_state = raw induced-anchor novelty
ledger_effective_survivor = ledger_survivor and frontier_new_transport_state
ledger_recursive_survivor = ledger_effective_survivor and not cycle_state
```

These are measured sidecar classifications. They are not an independent
frontier-commitment theorem. The code currently derives "effective survivor"
from the same ledger predicates whose proof is under study, so it cannot serve
as the independent criterion needed for T3.

The next missing definition is therefore:

```text
PGSPG transported frontier commitment:
  a public endpoint-chain condition, independent of typed rewrite elimination,
  that says when an induced certificate contributes a new transported story
  commitment.
```

### Transported Frontier Commitment Definition Contract

The missing definition must be stated before T3 can be proved.

Allowed inputs:

```text
public modulus N
source certificate C
induced certificate C'
T_N images of public story coordinates
ordered public endpoint-chain anchors
prior recursive frontier anchors
public reduced grammar signatures
```

Forbidden inputs:

```text
gcd
N % x
product closure
hidden factors
audit factors
factor APIs
primality APIs
random search
fallback search
typed rewrite labels as the definition itself
```

A valid definition must decide this predicate without using typed rewrite
elimination as an input:

```text
FrontierCommit(C, C') = true
```

where the meaning is:

```text
C' contributes a new transported endpoint-chain commitment to the public
transported story generated from C.
```

Minimal acceptance gate:

```text
FrontierCommit(C, C') must be computable before applying:
  prefix + lower/equal rewrite exclusion
  suffix + lower + deadline=threat rewrite exclusion
  recursive recurrence exclusion
```

Acceptance tests for any proposed definition:

```text
1. It is computed before PrefixMaterial, ThreatMaterial, TypedMaterial, and
   recursive recurrence are applied.
2. It uses only public endpoint-chain transport objects and admissible public
   grammar signatures.
3. It does not read ledger_effective_survivor, ledger_recursive_survivor,
   ledger_prefix_elimination, ledger_suffix_elimination, or story_rewrite.
4. It does not define frontier commitment as not PrefixMaterial, not
   ThreatMaterial, not TypedMaterial, or not recurrent.
5. It gives a positive public condition for a new transported endpoint-chain
   commitment.
6. It has a falsifiable overlap test against TypedMaterial:

   TypedMaterial(C, C') and FrontierCommit(C, C')

   must be impossible by proof, not by definition.
```

Measured target if such a definition is found:

```text
TypedMaterial rows = 107
TypedMaterial effective rows = 0
direct effective rows outside TypedMaterial = 202
recursive stale/non-frontier rows outside TypedMaterial = 203
redundant tail/non-threat direct eliminated rows outside TypedMaterial = 3
```

This measured target is not the definition. It is the audit surface the
definition must explain.

Rejected shortcut:

```text
FrontierCommit(C, C') := not TypedMaterial(C, C') and not recurrent(C')
```

Reason:

```text
This makes TypedMaterial(C, C') => not DirectFrontier(C, C') true by
definition. It does not prove the typed exclusion theorem.
```

Rejected positive candidate:

```text
FrontierCommit(C, C') :=
  frontier_new_transport_state(C, C') and not recurrent(C')
```

Measured failure:

```text
candidate rows = 299
effective rows = 202
direct eliminated rows = 97
stale rows = 0
TypedMaterial overlap = 97
```

Reason:

```text
Raw induced-anchor novelty plus non-recurrence still accepts typed material.
It is not enough to distinguish a new transported endpoint-chain commitment
from transported source material.
```

Measured perfect but table-based candidate:

```text
FrontierCommit_RC(C, C') :=
  frontier_new_transport_state(C, C')
  and not recurrent(C')
  and RC(C, C') is not in the observed TypedMaterial RC-class set.
```

Measured result:

```text
candidate rows = 202
effective rows = 202
direct eliminated rows = 0
stale rows = 0
TypedMaterial overlap = 0
missed effective rows = 0
```

Status:

```text
measured perfect candidate: yes
definition of current Psi(RB): no
theorem proof: no
```

Reason:

```text
The candidate uses an observed finite RC-class set. It becomes a valid proof
route only if the excluded RC classes are characterized by a structural public
transport law, not by table membership in the current 512-row surface.
```

Open structural target:

```text
Find a public condition Φ(RC(C, C')) such that:
  Φ holds for exactly the measured effective frontier candidates,
  TypedMaterial(C, C') => not Φ(RC(C, C')),
  recurrence(C') => not Φ(RC(C, C')),
  and Φ is not defined by observed class lookup.
```

This RC target is superseded by the smaller `Psi(RB)` interface unless a proof
forces the full RC signature back into the theorem.

Partial structural candidate:

```text
FrontierCommit_run(C, C') :=
  frontier_new_transport_state(C, C')
  and not recurrent(C')
  and R(C, C') is not in the observed TypedMaterial run-word set.
```

Measured result:

```text
candidate rows = 150
effective rows = 150
direct eliminated rows = 0
stale rows = 0
TypedMaterial overlap = 0
missed effective rows = 52
```

Status:

```text
sound on the measured surface: yes
complete on the measured surface: no
definition of current Psi(RB): no
```

Reason:

```text
Run-word exclusion alone is too coarse. It gives no false positives, but it
misses 52 effective frontier rows whose run words also appear in TypedMaterial.
The event-count part of RC(C, C') is required for measured completeness unless
a different structural invariant is found.
```

Run-word completion obstruction:

```text
The 52 missed effective rows use 9 run words that also appear in TypedMaterial:

SPOSO  = 32
OSPO   = 8
OPO    = 5
OBO    = 2
SOPO   = 1
OSPOPO = 1
POBO   = 1
POPOP  = 1
OBPO   = 1
```

TypedMaterial rows sharing those run words have no full run-count overlap with
the missed effective rows:

```text
shared-run TypedMaterial rows = 29
RC overlap with missed effective rows = 0
```

However, no one-field threshold over the six public event counts separates the
missed effective rows from the typed rows sharing the same run words. The
checked fields were:

```text
source_closed_count
source_tail_count
source_threat_count
induced_closed_count
induced_tail_count
induced_threat_count
```

The direct count differences, sums, and total-count deltas also fail as
single-threshold separators.

Status:

```text
pure run word: incomplete
single event-count threshold: insufficient
full RC(C, C') joint signature: still separates measured direct
  effective/typed rows
structural theorem inside joint RC(C, C'): missing
```

Proof consequence:

```text
The next Psi definition cannot be a scalar count rule. It must be a structural
condition on RB(C, C'), or a theorem that replaces RB(C, C') with a smaller
public invariant without losing the typed exclusion.
```

### Smaller Joint Run-Balance Candidate

The full six-count event vector is not minimal on the current direct surface.
A smaller public joint signature preserves direct effective/eliminated
separation:

```text
RB(C, C') =
(
  R(C, C'),
  source_closed_count - source_tail_count,
  induced_closed_count - induced_tail_count
)
```

Measured class counts:

```text
all RB classes = 475
effective RB classes = 193
direct eliminated RB classes = 104
TypedMaterial RB classes = 101
stale RB classes = 200
singleton RB classes = 441
non-singleton RB classes = 34
non-singleton rows = 71
```

Measured overlaps:

```text
effective/direct eliminated RB overlap = 0
effective/TypedMaterial RB overlap = 0
effective/stale RB overlap = 9
direct eliminated/stale RB overlap = 13
TypedMaterial/stale RB overlap = 10
```

RB label-set structure:

```text
effective-only RB classes = 184
direct-eliminated-only RB classes = 104
stale-only RB classes = 178
effective/stale mixed RB classes = 9
effective/direct-eliminated mixed RB classes = 0
direct-eliminated/stale mixed RB classes = 0
```

Interpretation:

```text
RB separates direct frontier candidates from direct committed material on the
measured surface. It does not separate recurrence; the 9 mixed classes are
effective/stale classes and therefore belong to Lemma 3.
```

Endpoint-history boundary:

```text
The 9 effective/stale mixed RB classes are not direct material ambiguity.
Each mixed class contains rows whose direct difference is public endpoint
history:

frontier_new_transport_state = true   -> effective direct frontier row
frontier_new_transport_state = false  -> stale direct row
```

Measured mixed RB classes:

```text
('O',      33, 11)
('OSO',    33, 21)
('OSOPO',  33, 25)
('OSPO',   33, 20)
('OSPO',   33, 21)
('SPOSO',  19, 25)
('SPOSPO', 17, 17)
('SPOSPO', 20, 20)
('SPOSPO', 22, 19)
```

Proof consequence:

```text
RB(C, C') is a direct material/frontier separator only after endpoint-history
freshness is supplied. It must not absorb Lemma 3. Recursive recurrence remains
an independent public endpoint-chain condition.
```

The corresponding observed-class candidate is:

```text
FrontierCommit_RB(C, C') :=
  frontier_new_transport_state(C, C')
  and not recurrent(C')
  and RB(C, C') is not in the observed TypedMaterial RB-class set.
```

Measured result:

```text
candidate rows = 202
effective rows = 202
direct eliminated rows = 0
stale rows = 0
TypedMaterial overlap = 0
missed effective rows = 0
```

Status:

```text
measured perfect candidate: yes
definition of Psi(RB): no
theorem proof: no
near-row partition: yes
```

Reason:

```text
The candidate still depends on observed finite RB-class exclusion. It becomes a
proof route only if the two closed-tail balances are proved to be the public
chamber-balance coordinates that distinguish frontier run words from committed
material run words.
The 441 singleton RB classes also show that RB remains close to a row-level
signature unless a structural chamber-balance language is proved.
```

Run-balance linear-threshold obstruction:

```text
Within run-word families that contain both effective rows and TypedMaterial
rows, small linear separators in the two balance coordinates fail for multiple
families.
```

Checked per run word:

```text
coordinates = (
  source_closed_count - source_tail_count,
  induced_closed_count - induced_tail_count
)
linear forms = a * source_balance + b * induced_balance
coefficients a,b in {-3,-2,-1,0,1,2,3}
```

No such separator exists for these shared run-word families:

```text
OBO
OPO
OSPO
OSPOPO
```

The large shared family `SPOSO` does have a simple measured split by source
balance on the current surface:

```text
effective SPOSO source balance <= 29
TypedMaterial SPOSO source balance >= 32
```

but that pattern is not universal across the shared run words.

Status:

```text
single global balance inequality: unsupported
small per-run linear inequality: unsupported for several shared run words
observed RB class exclusion: measured perfect, still table-shaped
```

Proof consequence:

```text
The structural law must account for the ordered run-word family together with
both chamber-balance coordinates. It cannot presently be replaced by a
single threshold, a single balance comparison, or a uniform small linear
inequality.
```

New proof target:

```text
Find a public structural condition Ψ(RB(C, C')) such that:
  Ψ holds for exactly the measured direct frontier candidates,
  TypedMaterial(C, C') => not Ψ(RB(C, C')),
  recurrence(C') => not Ψ(RB(C, C')),
  and Ψ is not observed class lookup.
```

Guarded invalidations now exclude the broadest run-balance shortcuts:

```text
threat run-word superset:
  rows = 128
  effective survivors = 44

threat run-word plus induced_balance < source_balance:
  rows = 63
  effective survivors = 21

threat run-word plus induced_balance < source_balance and source_balance >= 32:
  rows = 32
  effective survivors = 7

equal-prefix run-word superset:
  rows = 128
  effective survivors = 8

equal-prefix run-word plus induced_balance <= source_balance:
  effective survivors = 7

equal-prefix run-word plus induced_balance >= source_balance:
  effective survivors = 1
```

Therefore `Ψ(RB)` cannot be a threat run-word superset, an equal-prefix run-word
superset, or a simple balance-threshold refinement of either. The remaining
candidate must use a sharper structural chamber-balance law.

Guarded monotone-balance invalidation also excludes coordinate-monotone
balance regions inside shared run families. For each orientation, there are
shared run families where an effective balance point dominates a typed balance
point in that orientation:

```text
source_up_induced_up:
  OBO, OSPO, OPO, POBO, OSPOPO

source_up_induced_down:
  OBO, OSPO, OPO, SOPO

source_down_induced_up:
  OBO, SPOSO, POPOP, OSPO, OPO, OBPO, POBO, OSPOPO

source_down_induced_down:
  OBO, SPOSO, OSPO, OPO, OSPOPO
```

Thus `Psi(RB)` cannot be a per-run coordinate-monotone frontier region in the
two closed-tail balance coordinates. A successful candidate must use additional
ordered chamber-balance structure.

### Current Frontier Predicate Interface

The measured evidence now supports a cleaner division between direct frontier
status and recursive endpoint history:

```text
FreshEndpoint(C') :=
  the induced anchor of C' has not appeared earlier in the public endpoint-chain
  traversal for this recursion layer.

DirectFrontier(C, C') :=
  FreshEndpoint(C') and Ψ(RB(C, C')).
```

Here `Ψ` is the missing structural chamber-balance language. It must be defined
from:

```text
R(C, C')
source_closed_count - source_tail_count
induced_closed_count - induced_tail_count
```

It must not read:

```text
PrefixMaterial(C, C')
ThreatMaterial(C, C')
TypedMaterial(C, C')
ledger_prefix_elimination
ledger_suffix_elimination
ledger_effective_survivor
observed effective RB classes
observed TypedMaterial RB classes
```

Under this interface, the first three proof targets become:

```text
Lemma 1 RB form:
  PrefixMaterial(C, C') => not Ψ(RB(C, C')).

Lemma 2 RB form:
  ThreatMaterial(C, C') => not Ψ(RB(C, C')).

Lemma 3 endpoint-history form:
  not FreshEndpoint(C') => not DirectFrontier(C, C').
```

The separation is important:

```text
RB handles direct material/frontier status.
FreshEndpoint handles stale or recurrent endpoint-chain state.
Neither predicate may be defined from the other.
```

The guarded RB recurrence boundary is:

```text
effective/stale mixed RB classes = 9
effective/stale mixed RB classes ∩ direct eliminated RB classes = 0
```

Those mixed classes do not create direct material ambiguity. They show that the
same chamber-balance shape can recur in endpoint history, so recurrence must be
handled by `FreshEndpoint(C')` rather than by changing `Psi(RB)`.

Current proof status:

```text
FreshEndpoint as public endpoint-history predicate: implementation-level
  sidecar field exists
Ψ(RB) structural definition: missing
Lemma 1 RB form: unproved
Lemma 2 RB form: unproved
Lemma 3 endpoint-history form: closed by DirectFrontier definition
resolver promotion: blocked
```

### Minimal `Psi(RB)` Candidate Contract

A proposed `Psi(RB)` is admissible only if it is stated before typed rewrite
elimination and before endpoint recurrence. It must be a public structural
language over:

```text
R(C, C')
source_closed_count - source_tail_count
induced_closed_count - induced_tail_count
```

It may use ordinary structural properties of the run word and the two balance
coordinates. It may not use finite observed class membership, typed rewrite
labels, ledger survivor labels, audit state, hidden factors, or post-recursion
state.

For the current proof target, the candidate must satisfy:

```text
PrefixMaterial(C, C') => not Psi(RB(C, C'))
ThreatMaterial(C, C') => not Psi(RB(C, C'))
FreshEndpoint(C') and Psi(RB(C, C')) => direct transported frontier candidate
```

Minimal public falsification condition:

```text
there exists a public certificate pair (C, C') such that
  PrefixMaterial(C, C') or ThreatMaterial(C, C')
  and Psi(RB(C, C'))
```

Such a row falsifies the typed exclusion theorem against that `Psi`. It does
not falsify local GWR/NLSC.

Minimal circularity condition:

```text
Psi reads PrefixMaterial, ThreatMaterial, TypedMaterial, ledger elimination,
ledger survivor state, observed effective RB classes, or observed material RB
classes.
```

Such a definition is not a theorem candidate. It restates the measured ledger
instead of deriving the frontier language.

Lemma 3 endpoint-history proof under this interface:

```text
DirectFrontier(C, C') := FreshEndpoint(C') and Ψ(RB(C, C')).

If not FreshEndpoint(C'), then the first conjunct of DirectFrontier is false.
Therefore not DirectFrontier(C, C').
```

This closes only the endpoint-history exclusion in the narrowed interface. It
does not prove the older recursive-collapse theorem by itself:

```text
recursive final survivor count = 0
```

That measured collapse still also needs `Ψ(RB)` for direct frontier status and
the layer-by-layer endpoint-chain recurrence argument.

### Next Theorem To Prove

The remaining direct-frontier theorem is now a single structural language
problem.

Define:

```text
RB(C, C') =
(
  R(C, C'),
  source_closed_count - source_tail_count,
  induced_closed_count - induced_tail_count
)
```

Find a public predicate `Ψ` on `RB(C, C')` such that:

```text
1. Ψ is computed before PrefixMaterial, ThreatMaterial, TypedMaterial, and
   recurrence.
2. Ψ does not read ledger labels or observed class sets.
3. PrefixMaterial(C, C') => not Ψ(RB(C, C')).
4. ThreatMaterial(C, C') => not Ψ(RB(C, C')).
5. If FreshEndpoint(C') and Ψ(RB(C, C')), then C' is a direct transported
   frontier commitment candidate.
6. If not FreshEndpoint(C'), then Lemma 3 handles the row as endpoint-history
   recurrence, independently of Ψ.
```

Already guarded measured prerequisites:

```text
carrier-local prefix equivalence:
  prefix interval + non-increasing lock
  ==
  carrier symbol in {P, B} + non-increasing lock

carrier-local threat equivalence:
  threat suffix interval + strict lower lock
  ==
  deadline_threat + carrier symbol in {S, B} + strict lower lock

RB direct separation:
  effective RB classes ∩ direct eliminated RB classes = empty
  effective/stale RB overlap = 9 endpoint-history classes
```

Invalidated shortcuts:

```text
Ψ as observed RB-class lookup
Ψ as run-word exclusion alone
Ψ as a single event-count threshold
Ψ as a single global balance inequality
Ψ as a uniform small per-run linear balance inequality
Lemma 2 widened to threat run-word or threat run-balance supersets
Lemma 1 reduced to strict descent or carrier symbol without lock condition
floor-cell commitment reduced to recorded source story-event image matching
```

This is the shortest current proof target:

```text
prove Ψ as a structural chamber-balance language,
then prove PrefixMaterial and ThreatMaterial are outside that language,
then use FreshEndpoint for the independent recurrence boundary.
```

### TypedMaterial RB Language Split

The measured `TypedMaterial` RB language splits into a large prefix component
and a small threat-suffix component.

Prefix component:

```text
PrefixMaterial rows = 101
PrefixMaterial RB classes = 95
PrefixMaterial run words = 20
PrefixMaterial effective RB overlap = 0
```

The most common prefix run words are:

```text
POPO   = 48
SPOPO  = 9
OPO    = 7
SPOPOP = 5
BPOBO  = 4
POPOP  = 4
SOPO   = 4
```

Threat-suffix component:

```text
ThreatMaterial rows = 12
ThreatMaterial RB classes = 12
ThreatMaterial run words = 6
ThreatMaterial effective RB overlap = 0
```

Threat-suffix run words:

```text
OBO   = 3
SPOSO = 3
OSPO  = 2
POBO  = 2
OBPO  = 1
OSOSO = 1
```

Overlap between the typed components:

```text
PrefixMaterial RB classes ∩ ThreatMaterial RB classes = 6

('OBO', 33, 17)
('OBO', 33, 20)
('OBO', 34, 17)
('OBPO', 34, 33)
('POBO', 33, 19)
('POBO', 34, 21)
```

Balance profile:

```text
ThreatMaterial has induced_balance < source_balance on 12 / 12 rows.
PrefixMaterial has mixed balance relation:
  induced_balance < source_balance: 59
  induced_balance > source_balance: 37
  induced_balance = source_balance: 5
```

Proof consequence:

```text
Lemma 2 RB form is the smaller strict-balance threat language.
Lemma 1 RB form is the larger prefix language and cannot be reduced to
induced_balance < source_balance.
The shared six RB classes show that prefix and threat material are two routes
into the same committed-material region, not disjoint frontier obstructions.
```

Threat-language broadening obstruction:

```text
ThreatMaterial itself remains the clean measured Lemma 2 branch:

deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d < source_lock_carrier_d

rows = 12
effective = 0
eliminated = 12
stale = 0
```

Broader run/balance supersets are not clean:

```text
run_word in ThreatMaterial run words:
  rows = 128
  effective = 44
  eliminated = 13
  stale = 72

run_word in ThreatMaterial run words and induced_balance < source_balance:
  rows = 63
  effective = 21
  eliminated = 13
  stale = 30

run_word in ThreatMaterial run words and source_balance >= 32
and induced_balance < source_balance:
  rows = 32
  effective = 7
  eliminated = 12
  stale = 13
```

Even per-run broadening is not uniformly clean:

```text
OBO, source_balance >= 32, induced_balance < source_balance:
  effective = 1

OSPO, source_balance >= 32, induced_balance < source_balance:
  effective = 5

POBO, source_balance >= 32, induced_balance < source_balance:
  effective = 1
```

Clean per-run broadening occurs only for measured subfamilies:

```text
OBPO, source_balance >= 32, induced_balance < source_balance:
  effective = 0

OSOSO, source_balance >= 32, induced_balance < source_balance:
  effective = 0

SPOSO, source_balance >= 32, induced_balance < source_balance:
  effective = 0
```

Status:

```text
Lemma 2 clean measured antecedent: ThreatMaterial
ThreatMaterial run-word superset: invalidated
ThreatMaterial run-balance superset: invalidated
```

Proof consequence:

```text
Lemma 2 should not be widened beyond the strict threat-suffix antecedent unless
a new source-threat transport law is proved. The RB theorem must show why that
specific antecedent lands outside Ψ(RB); the run words and balance inequality
alone are insufficient.
```

### Prefix RB Language Split

The prefix material language has two distinct branches.

Strict-prefix branch:

```text
PrefixMaterial(C, C')
lambda(C') < lambda(C)

rows = 25
RB classes = 23
run words = 9
effective RB overlap = 0
induced_balance < source_balance on 25 / 25 rows
```

Strict-prefix run words:

```text
POPO   = 9
OPO    = 5
OBO    = 3
POBO   = 2
OSPOPO = 2
BPOBO  = 1
OBPO   = 1
SOPO   = 1
SPOPO  = 1
```

Equal-prefix branch:

```text
PrefixMaterial(C, C')
lambda(C') = lambda(C)

rows = 76
RB classes = 72
run words = 17
effective RB overlap = 0
```

Equal-prefix run words:

```text
POPO    = 39
SPOPO   = 8
SPOPOP  = 5
POPOP   = 4
BPOBO   = 3
SOPO    = 3
BPOBPO  = 2
POBPO   = 2
OPO     = 2
```

Equal-prefix balance direction is mixed:

```text
induced_balance < source_balance: 34
induced_balance > source_balance: 37
induced_balance = source_balance: 5
```

The two prefix branches are disjoint in RB:

```text
strict-prefix RB classes ∩ equal-prefix RB classes = 0
```

Run-word broadening is invalid:

```text
run_word in equal-prefix run words:
  rows = 128
  effective = 8
  eliminated = 95
  stale = 35

run_word in equal-prefix run words and induced_balance >= source_balance:
  effective = 1

run_word in equal-prefix run words and induced_balance <= source_balance:
  effective = 7
```

Status:

```text
strict-prefix RB language: smaller strict-balance branch
equal-prefix RB language: essential mixed-balance branch
equal-prefix run-word superset: invalidated
equal-prefix balance-threshold broadening: invalidated
```

Proof consequence:

```text
Lemma 1 cannot be reduced to strict descent or a balance inequality. The equal
branch requires transported leftmostness: equal-label prefix material must be a
non-frontier tie against the already committed source carrier.
```

Carrier-local prefix restatement:

```text
The prefix predicate can be read directly from the induced carrier event:

induced carrier symbol in {P, B}
and lambda(C') <= lambda(C)
```

Measured equivalence with the interval predicate:

```text
induced_carrier_in_prefix_zone and lambda(C') <= lambda(C):
  rows = 101

induced carrier symbol in {P, B} and lambda(C') <= lambda(C):
  rows = 101

symmetric difference = 0
```

Measured result:

```text
carrier symbol in {P, B} and lambda(C') = lambda(C):
  rows = 76
  eliminated = 76
  effective = 0

carrier symbol in {P, B} and lambda(C') <= lambda(C):
  rows = 101
  eliminated = 101
  effective = 0

carrier symbol in {P, B} with no lock restriction:
  rows = 109
  eliminated = 101
  effective = 8
```

The 8 effective rows have carrier symbol in `{P, B}` but higher lock label.
Therefore the non-increasing lock condition is essential:

```text
carrier in committed prefix/both material alone is too broad;
carrier in committed prefix/both material with non-increasing lock is the
measured Lemma 1 antecedent.
```

Carrier-local threat equivalence:

```text
deadline_threat
and induced_carrier_in_suffix_zone
and lambda(C') < lambda(C):
  rows = 12

deadline_threat
and induced carrier symbol in {S, B}
and lambda(C') < lambda(C):
  rows = 12

symmetric difference = 0
```

Thus Lemma 2 can also be stated carrier-locally on the measured surface:

```text
deadline_threat
and induced carrier symbol in {S, B}
and lambda(C') < lambda(C)
=> not Ψ(RB(C, C')).
```

Minimal falsification condition:

```text
If Psi(RB(C, C')) or DirectFrontier(C, C') depends on any typed rewrite
predicate, then it is circular and cannot support the typed exclusion theorem.
```

The useful proof shape is:

```text
1. Define Psi(RB(C, C')) as a public structural chamber-balance language.
2. Prove that typed prefix/suffix rewrites imply not Psi(RB(C, C')).
3. Use FreshEndpoint(C') to handle recursive anchor recurrence independently.
4. Only then promote the typed transported story law from measured evidence to
   theorem candidate.
```

### Rejected FrontierCommit Definitions

The following definitions are rejected.

Raw anchor novelty:

```text
FrontierCommit(C, C') := frontier_new_transport_state
```

Rejected because raw induced-anchor novelty occurs before typed ledger
elimination. The measured surface contains fresh induced anchors that are
prefix-eliminated.

Ledger effective survivor:

```text
FrontierCommit(C, C') := ledger_effective_survivor
```

Rejected because `ledger_effective_survivor` is computed after prefix/suffix
rewrite predicates. Using it would make T3 circular.

Recursive survivor:

```text
FrontierCommit(C, C') := ledger_recursive_survivor
```

Rejected because it depends on `ledger_effective_survivor` and recurrence
filtering. It is a measured post-elimination state, not an independent
frontier-commitment rule.

Broad non-rewrite:

```text
FrontierCommit(C, C') := not story_rewrite
```

Rejected because `story_rewrite` is too broad and is not itself an exclusion
law. The measured commitment ledger contains `124` story-rewrite rows that
remain effective survivors.

The admissible direct-frontier language must therefore be narrower and earlier:

```text
Psi(RB(C, C')) must be computed from public endpoint-chain transport state
before typed rewrite and recurrence predicates are applied.
```

### Candidate Psi Ingredient: Reduced Grammar

The existing `commitment_story_word_projection_v1` surface is an admissible
candidate ingredient because it is built from public endpoint-chain grammar
signatures rather than from typed rewrite labels.

Current projection status:

```text
projection_row_count = 50
projected_lag23_collision_count = 0
fresh_rsa_100_lag23_collision_count = 0
projected_lag2_hit_count = 32
projected_lag3_hit_count = 30
component_sharing_word_exclusion_count = 42
```

This does not define `Psi(RB)`. It only suggests a possible public ingredient:

```text
Psi(RB(C, C')) may need an endpoint-chain grammar condition, where
ordered lag-2 + lag-3 collision is excluded while component sharing remains
allowed.
```

Status:

```text
admissible candidate ingredient: yes
definition of Psi(RB): no
typed exclusion proof against Psi(RB): no
resolver promotion: no
```

Standalone reduced-grammar definition is rejected on the current projection
surface:

```text
projected_lag23_collision = False on 50 / 50 rows
projected_recursive_reduced_collision = False on 50 / 50 rows
```

Those fields preserve the ordered-word exclusion, but they do not discriminate
frontier commitment by themselves. Component-sharing fields vary:

```text
component_sharing_word_exclusion = True on 42 / 50 rows
projected_lag2_hit = True on 32 / 50 rows
projected_lag3_hit = True on 30 / 50 rows
```

So reduced grammar remains a possible ingredient for `Psi(RB)`, not a
standalone definition.

Projection-surface boundary:

```text
commitment_story_word_projection_v1 has 50 projection rows;
transported_story_law_v1 has 512 direct transported-story rows.
```

The projection rows preserve the solved/fresh ordered-word exclusion bridge.
They are not a row-wise classifier for the 512 direct rows and cannot be used as
`Psi(RB)` without an additional theorem connecting the grammar projection to
direct chamber-balance status.

### Rejected Standalone Frontier Ingredients: Threat/Tail Images And Width

Two existing public diagnostics were checked as possible non-circular `Psi(RB)`
ingredients.

`transported_threat_tail_images_v1` is public endpoint-chain transport
evidence, but it is not a standalone frontier predicate. Its position fields
split across multiple regimes:

```text
threat_image_position: missing = 380 / 512, before_upper_reset = 132 / 512
tail_image_position: before_upper_reset = 397 / 512, missing = 115 / 512
induced_threat_position: missing = 477 / 512, inside_upper_interval = 23 / 512,
                         after_upper_deadline = 12 / 512
induced_tail_position: inside_upper_interval = 489 / 512, missing = 23 / 512
diagnostic_status = positions_have_multiple_regimes
```

The field most strongly aligned with transport, `induced_tail_position`, is
broad but not universal, and it does not distinguish typed rewrites from valid
frontier commitments.

`transported_width_diagnostic_v1` is also public and non-circular, but it has
measured false positives against both unresolved and static-frontier surfaces:

```text
row_count = 512
exact_symmetric_width_match_count = 41
exact_false_positive_against_unresolved_count = 41
exact_false_positive_against_static_frontier_count = 19
carrier_symmetric_width_match_count = 208
carrier_false_positive_against_unresolved_count = 208
carrier_false_positive_against_static_frontier_count = 105
diagnostic_status = diagnostic_only_no_closure_claim
```

Therefore neither threat/tail image position nor symmetric width matching is a
standalone `Psi(RB)` definition. They remain admissible boundary data for a
future definition, but they do not prove Lemma 1, Lemma 2, or typed exclusion.

### Rejected Standalone Frontier Ingredient: Story-Kind Grammar

The public story-event kind sequence is also insufficient as a standalone
`FrontierCommit(C, C')` definition.

Measured obstruction:

```text
raw story-kind groups with at least one effective survivor
and at least one ledger-eliminated row: 26
```

The grouped key was:

```text
source_story_event_kinds
induced_story_event_kinds
frontier_new_transport_state
ledger_stale_transport_state
```

So two rows can share the same public source/induced event-kind grammar and the
same raw novelty/staleness state while one remains effective and the other is
removed by typed prefix or suffix exclusion.

Even adding the coarse public fact that the induced carrier lies in the
transported prefix or suffix band leaves mixed status:

```text
source_story_event_kinds
induced_story_event_kinds
induced_carrier_in_prefix_zone
induced_carrier_in_suffix_zone
```

has a mixed group with:

```text
effective survivors = 1
ledger-eliminated rows = 1
```

Therefore `FrontierCommit(C, C')` cannot be only a story-kind grammar predicate.
The missing definition must use finer ordered endpoint-chain transport state
than event-kind grammar, and it must still be independent of the typed
prefix/suffix rewrite predicates.

### Interval-Position Word Check

A finer public candidate is the ordered position word obtained by classifying
each induced story event value against the transported prefix and suffix bands:

```text
P = inside transported prefix band only
S = inside transported suffix band only
B = inside both transported bands
O = outside both transported bands
```

Using the full ordered word together with source/induced event-kind grammar and
raw novelty/staleness state produced no mixed effective/eliminated groups on
the current 512 rows:

```text
mixed full interval-position groups = 0
group_count = 507
singleton_groups = 502
max_group_size = 2
```

This is not a theorem candidate yet. The full interval word is almost a row
identifier on the measured surface, so it avoids contradictions by preserving
too much incidental row detail.

Coarser interval features do not support a standalone rule. For the coarse
presence signature:

```text
P/p = some/no induced event in prefix
S/s = some/no induced event in suffix
B/b = some/no induced event in both
```

the measured split is:

```text
PSB: n = 51, effective = 28, eliminated = 4, stale = 21
PSb: n = 286, effective = 116, eliminated = 27, stale = 147
PsB: n = 28, effective = 8, eliminated = 12, stale = 9
Psb: n = 83, effective = 14, eliminated = 59, stale = 14
pSB: n = 2, effective = 1, eliminated = 1, stale = 0
pSb: n = 30, effective = 18, eliminated = 3, stale = 11
psB: n = 13, effective = 4, eliminated = 4, stale = 5
psb: n = 19, effective = 13, eliminated = 0, stale = 6
```

Thus coarse interval occupancy is rejected as a standalone
`FrontierCommit(C, C')` definition. The full ordered interval word remains an
admissible ingredient, but it must be compressed into a genuine transport law
before it can support T3.

### Run-Count Separation Candidate

The first non-failing compression of the full interval-position word is:

```text
full interval run word
+ source public event counts
+ induced public event counts
```

The full interval run word collapses consecutive equal symbols in the ordered
`P/S/B/O` interval-position word. The public event counts are:

```text
source_closed_count
source_tail_count
source_threat_count
induced_closed_count
induced_tail_count
induced_threat_count
```

Measured without using raw novelty/staleness fields:

```text
group_count = 481
singleton_groups = 453
max_group_size = 3
mixed effective/eliminated groups = 0
mixed effective/stale groups = 7
```

Interpretation:

```text
The run-count signature separates direct effective survivors from direct
prefix/suffix eliminations on the current 512-row public surface.

It does not separate recursive stale states. That remaining mixture belongs to
Lemma 3, not Lemma 1 or Lemma 2.
```

This is the current best candidate ingredient for the missing
`FrontierCommit(C, C')` definition. It is still not a theorem and not a
resolver rule:

```text
proof of why the run-count signature is invariant under PGSPG transport:
  missing

proof that typed prefix/suffix rewrites force the non-frontier side of the
run-count signature:
  missing

proof that the 7 stale mixtures are exactly recursive recurrence states:
  superseded by the narrowed DirectFrontier interface
```

The next proof step is therefore:

```text
derive the run-count signature from source chamber commitment
+ reciprocal floor image
+ induced opposite certificate grammar

then prove:
  prefix + lower/equal => not Psi(RB(C, C'))
  threat-suffix + lower => not Psi(RB(C, C'))
```

### Run-Count Proof Skeleton

Let `C` be a public source certificate and `C'` its induced opposite
certificate. Let:

```text
P(C) = [T_N(r(C)), T_N(w(C))]
S(C) = [T_N(d(C)), T_N(r(C))]
```

where `P(C)` is the transported prefix band and `S(C)` is the transported
suffix band.

For each public induced story value `e_i(C')`, define its interval symbol:

```text
B if e_i(C') in P(C) and e_i(C') in S(C)
P if e_i(C') in P(C) and e_i(C') notin S(C)
S if e_i(C') in S(C) and e_i(C') notin P(C)
O if e_i(C') notin P(C) and e_i(C') notin S(C)
```

The ordered interval word is:

```text
W(C, C') = symbol(e_1(C')) symbol(e_2(C')) ... symbol(e_m(C'))
```

The interval run word `R(C, C')` is obtained from `W(C, C')` by deleting
consecutive repeated symbols.

The event-count vector is:

```text
E(C, C') =
  (source_closed_count,
   source_tail_count,
   source_threat_count,
   induced_closed_count,
   induced_tail_count,
   induced_threat_count)
```

The run-count signature is:

```text
RC(C, C') = (R(C, C'), E(C, C'))
```

Measured direct-separation fact:

```text
RC(C, C') has 0 mixed direct effective/direct eliminated classes
on the current 512-row public transported-story surface.
```

This gives a candidate frontier predicate form:

```text
FrontierCommit(C, C') depends on RC(C, C') plus a recursive recurrence test.
```

It does not yet give a definition. A valid definition must say which
run-count signatures are frontier signatures without reading the measured
ledger labels.

Candidate proof decomposition:

```text
R1. Run Transport Lemma
    Reciprocal floor transport sends source carrier/reset/deadline commitment
    into an ordered interval run word over {P, S, B, O}.

R2. Event-Count Conservation Lemma
    The source and induced public event counts encode chamber story length,
    tail horizon, and lower-threat presence under public PGSPG certificate
    construction.

R3. Prefix Run Exclusion Lemma
    If w(C') lies in P(C) and lambda(C') <= lambda(C), then RC(C, C') is a
    committed-prefix run-count state, not a frontier run-count state.

R4. Threat-Suffix Run Exclusion Lemma
    If deadline(C) is the lower-threat deadline, w(C') lies in S(C), and
    lambda(C') < lambda(C), then RC(C, C') is a committed-threat run-count
    state, not a frontier run-count state.

R5. Recursive Run Recurrence Lemma
    The 7 measured effective/stale mixed RC classes are separated by prior
    recursive frontier anchors, not by direct prefix/suffix run-count state.
```

#### Compact Run-Word Pressure

A first compact projection of `R(C, C')` is:

```text
terminal prefix/both-to-outside alternation
```

meaning:

```text
R(C, C') contains P or B,
and after the first P/B symbol there is no later S symbol.
```

Measured split:

```text
terminal prefix/both-to-outside = false:
  rows = 214
  effective = 149
  eliminated = 7
  stale = 61
  prefix_elimination = 0
  suffix_elimination = 7

terminal prefix/both-to-outside = true:
  rows = 298
  effective = 53
  eliminated = 103
  stale = 152
  prefix_elimination = 101
  suffix_elimination = 9
```

Conclusion:

```text
terminal prefix/both-to-outside is necessary for every measured prefix
elimination, but it is not sufficient for prefix exclusion.
```

This is useful pressure for R3:

```text
prefix non-rewrite is not a pure run-word law;
it needs the event-count part of RC(C, C') or another public chamber-count
condition.
```

The direct suffix eliminations that remain outside this projection are the
separate R4 target.

#### R4 Suffix-Only Surface

The measured suffix branch is smaller than the prefix branch.

Direct suffix rows:

```text
suffix_elimination rows = 16
suffix_only rows = 9
suffix_with_prefix rows = 7
```

Deadline split:

```text
suffix_elimination + deadline_threat = true: 12
suffix_elimination + deadline_threat = false: 4
```

Suffix-only split:

```text
suffix_only + deadline_threat = true: 6
suffix_only + deadline_threat = false: 3
```

The suffix-only run words are:

```text
OSO: 1 suffix-only elimination, but also effective and stale rows
OSOSO: 1 suffix-only elimination
OSPO: 2 suffix-only eliminations, but also effective and stale rows
SOSO: 1 suffix-only elimination
SPOSO: 4 suffix-only eliminations on the measured surface
```

Therefore R4 is not a pure run-word theorem. The theorem-relevant branch is:

```text
deadline_threat = true
+ suffix lower lock relation
+ induced carrier in transported suffix band
=> non-frontier threat-suffix state
```

The `deadline_threat = false` suffix rows are measured redundant tail/non-threat
rows. They remain outside the current theorem target unless a separate tail
transport theorem is proved.

#### R4 Strict-Descent Antecedent Check

The theorem-relevant R4 antecedent is:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d < source_lock_carrier_d
```

Measured result:

```text
rows = 12
effective = 0
eliminated = 12
stale = 0
prefix_elimination = 6
suffix_elimination = 12
```

The non-strict variant is false as an exclusion surface:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d <= source_lock_carrier_d

rows = 13
effective = 1
eliminated = 12
stale = 0
```

Conclusion:

```text
R4 requires strict lock descent.
```

This is measured evidence for the R4 theorem branch, not a proof. The missing
proof is:

```text
source threat deadline
+ reciprocal suffix image
+ induced suffix carrier
+ strict lower lock label
=> transported threat-horizon material, not a new frontier commitment
```

#### R4 Formal Proof Obligation

Let `C` be a source PGSPG certificate and `C'` the induced opposite certificate.
Write:

```text
w = w(C)
r = r(C)
d = d(C)
w' = w(C')
lambda = lambda(C)
lambda' = lambda(C')
T_N(x) = floor(N / x)
S(C) = [T_N(d), T_N(r)]
```

R4 is the following threat-suffix theorem candidate:

```text
If
  d is the lower-threat deadline of C,
  w' in S(C),
  lambda' < lambda,
then
  C' is transported threat-horizon material committed by C,
  not a new transported frontier commitment.
```

The proof skeleton is:

1. Since `d` is the lower-threat deadline of `C`, local NLSC gives the source
   chamber relation:

   ```text
   r occurs before the first later point with divisor count below lambda.
   ```

2. The source interval `[r, d]` is therefore the closed threat-horizon segment
   after reset and before the first lower threat.

3. The reciprocal floor image gives the transported suffix band:

   ```text
   T_N([r, d]) = [T_N(d), T_N(r)] = S(C)
   ```

4. The condition `w' in S(C)` says the induced carrier is inside the image of
   that source threat-horizon segment.

5. The condition `lambda' < lambda` says the induced carrier is a strict lower
   lock relative to the source carrier.

6. The missing sublemma is:

   ```text
   Threat-Horizon Transport Sublemma:
   a strict lower induced carrier inside S(C) measures transported source
   threat-horizon material, not an independent frontier commitment.
   ```

7. With that sublemma, R4 follows.

Current theorem status:

```text
local NLSC source fact: proved in PROOF.md
reciprocal floor image as ordered public interval: arithmetic definition
Threat-Horizon Transport Sublemma: unproved
R4 theorem: unproved
```

Minimal public counterexample condition:

```text
d is the lower-threat deadline of C
w(C') in [T_N(d), T_N(r)]
lambda(C') < lambda(C)
C' is not a recursive recurrence state
C' supplies a valid new transported frontier commitment
```

Such a row would not falsify local NLSC. It would falsify the new
Threat-Horizon Transport Sublemma.

#### R4 Non-Circularity Requirement

The phrase "transported threat-horizon material" must be defined before using
R4 as an exclusion theorem.

Allowed definition shape:

```text
ThreatMaterial(C, C') is computed from:
  public source certificate C
  public induced certificate C'
  T_N([r(C), d(C)])
  source lower-threat deadline identity
  induced carrier position
  strict lock-label descent
```

Forbidden definition shape:

```text
ThreatMaterial(C, C') := not DirectFrontier(C, C')
ThreatMaterial(C, C') := not Psi(RB(C, C'))
ThreatMaterial(C, C') := ledger_suffix_elimination
ThreatMaterial(C, C') := ledger_effective_survivor = false
```

Reason:

```text
R4 must prove:
  ThreatMaterial(C, C') => not Psi(RB(C, C'))

If ThreatMaterial is defined by frontier failure or ledger elimination, the
proof is circular.
```

Current R4 proof status:

```text
clean measured antecedent: yes
public ThreatMaterial definition: candidate exists
proof against Psi(RB): missing
```

#### ThreatMaterial Definition Candidate

Define `ThreatMaterial(C, C')` by the following public conditions:

```text
1. d(C) is the lower-threat deadline of C.
2. C' is the induced opposite certificate from previous_endpoint(T_N(r(C))).
3. w(C') in [T_N(d(C)), T_N(r(C))].
4. lambda(C') < lambda(C).
```

Equivalent implementation-level public predicates on the current story-law
rows:

```text
deadline_threat = true
induced_carrier_in_suffix_zone = true
induced_lock_carrier_d < source_lock_carrier_d
```

This definition is non-circular:

```text
it does not read FrontierCommit(C, C')
it does not read ledger_suffix_elimination
it does not read ledger_effective_survivor
it does not read recursive survivor state
```

Measured support:

```text
ThreatMaterial rows = 12
effective = 0
direct eliminated = 12
stale = 0
```

The non-strict variant is invalid:

```text
lambda(C') <= lambda(C)
```

admits one effective row on the current surface.

The remaining theorem obligation is no longer the definition of
`ThreatMaterial`. It is:

```text
ThreatMaterial(C, C') => not Psi(RB(C, C'))
```

That implication still requires a structural definition of `Psi(RB)` or a
theorem showing that the chamber-balance frontier language excludes
`ThreatMaterial` states.

#### Simple Chamber-Count Refinement Fails

The next smallest refinement is to add only lower-threat presence to the
terminal prefix/both-to-outside condition.

Measured inside `terminal prefix/both-to-outside = true`:

```text
source_threat_count = 0, induced_threat_count = 0:
  rows = 195
  effective = 11
  eliminated = 76
  stale = 118
  prefix_elimination = 76

source_threat_count = 0, induced_threat_count = 1:
  rows = 11
  effective = 11
  eliminated = 0
  stale = 0
  prefix_elimination = 0

source_threat_count = 1, induced_threat_count = 0:
  rows = 81
  effective = 24
  eliminated = 23
  stale = 34
  prefix_elimination = 22
  suffix_elimination = 7

source_threat_count = 1, induced_threat_count = 1:
  rows = 11
  effective = 7
  eliminated = 4
  stale = 0
  prefix_elimination = 3
  suffix_elimination = 2
```

Conclusion:

```text
induced lower-threat presence is protective in one measured branch, but lower
threat presence alone does not define prefix non-frontier status.
```

Tail-count pairs and closed/tail count deltas also mix effective, eliminated,
and stale rows under the terminal prefix/both-to-outside condition. Therefore
R3 is not supported by a one-field chamber-count threshold. It requires the
ordered `RC(C, C')` object or a new proof that collapses the event-count vector
to a smaller invariant.

#### RC Table-Lookup Boundary

The full run-count signature separates direct effective rows from direct
prefix/suffix eliminated rows on the measured surface, but it is close to a
finite row partition.

Measured class counts:

```text
rows = 512
RC classes = 481

direct effective rows = 202
direct effective RC classes = 194

direct eliminated rows = 110
direct eliminated RC classes = 105

stale rows = 213
stale RC classes = 202
```

Overlap:

```text
effective/eliminated RC overlap = 0
effective/stale RC overlap = 7
eliminated/stale RC overlap = 13
```

Conclusion:

```text
RC(C, C') is a measured separating signature, not a definition of
FrontierCommit(C, C').
```

A theorem cannot define frontier status by a finite table of observed RC
classes. The next mathematical step must prove a structural condition inside
`RC(C, C')`, or prove that `RC(C, C')` itself is the invariant image of a PGSPG
transport law independent of the measured ledger.

#### RC Non-Entailment From Local GWR/NLSC

The run-count signature also cannot be derived from local GWR/NLSC alone.

Reason:

```text
GWR/NLSC input:
  one local ordered prime-gap chamber
  carrier w(C)
  local divisor-count minimum lambda(C)
  reset endpoint r(C)
  optional lower-threat deadline d(C)

RC(C, C') input:
  public modulus N
  reciprocal floor map T_N(x) = floor(N / x)
  transported prefix and suffix bands
  induced opposite certificate C'
  ordered induced story-event values
  source and induced event-count vectors
```

The second list is not definable from the first list without an additional
transport theorem. Local GWR/NLSC determines the source chamber's local
carrier/reset relation. It does not determine:

```text
the image of that relation under T_N
the previous endpoint before T_N(r(C))
the induced opposite certificate story
the ordered P/S/B/O interval run word
the source/induced event-count vector as a frontier invariant
```

Therefore:

```text
local GWR/NLSC
does not entail
RC(C, C') frontier separation
```

The open route is narrower:

```text
prove a new transported run-count theorem:
  source chamber commitment
  + reciprocal floor image
  + induced PGSPG certificate grammar
  => structural frontier/non-frontier condition inside RC(C, C')
```

This closes another proof shortcut:

```text
closed route:
  use RC(C, C') as if it were already a GWR/NLSC consequence

open route:
  prove RC(C, C') as a new transported invariant, or find a smaller
  structural condition inside RC(C, C')
```

Exact GWR/NLSC inputs available from `PROOF.md`:

```text
GWR fixes w(C) as the leftmost minimum-divisor carrier in one chamber.
NLSC forbids a later lower-divisor reset before the chamber endpoint.
Threat deadline d(C) is meaningful only when it is the local lower-threat
deadline from the same chamber.
```

Missing transport inputs not supplied by local GWR/NLSC:

```text
floor image preserves the ordered commitment role of carrier/reset/deadline
induced certificate event counts are determined by transported source story
run-count frontier classes can be defined without ledger labels
typed prefix/suffix antecedents force non-frontier RC classes
recursive stale mixtures are exactly prior-frontier recurrence states
```

Minimal public counterexample condition:

```text
There exist public C and C' such that:
  RC(C, C') is assigned frontier status by a non-circular run-count definition,
  w(C') lies in P(C) with lambda(C') <= lambda(C), or
  w(C') lies in threat-suffix S(C) with lambda(C') < lambda(C),
  and C' is not a recursive recurrence state.

Such a row would falsify the run-count version of Lemma 1 or Lemma 2.
```

### FrontierCommit Candidate-Space Audit

The existing public surfaces leave the candidate space sharply bounded.

Public row families inspected:

```text
transported_story_law_v1
transported_commitment_story_ledger_v1
commitment_story_word_projection_v1
transported_threat_tail_images_v1
transported_width_diagnostic_v1
```

The fields already separate into three proof roles:

```text
raw public state:
  source and induced anchors
  public source and induced story event values
  transported prefix and suffix intervals
  reduced grammar signatures
  threat/tail image positions
  symmetric width measurements

typed rewrite antecedents:
  transported_zone
  lock_carrier_d_relation
  prefix/suffix zone membership

post-elimination sidecar state:
  ledger_prefix_elimination
  ledger_suffix_elimination
  ledger_effective_survivor
  ledger_recursive_survivor
```

A valid `FrontierCommit(C, C')` definition must live in the first role. It
cannot use the typed rewrite antecedents as its definition, because those
antecedents are exactly what T1 and T2 must prove exclude frontier commitment.
It cannot use the post-elimination sidecar state, because that would make T3
circular.

The measured ledger also forbids a broad rewrite criterion:

```text
story_rewrite = true and ledger_effective_survivor = true: 124 rows
story_rewrite = true and ledger_effective_survivor = false: 152 rows
```

So the theorem cannot be:

```text
any public transported story rewrite is not a frontier commitment
```

The remaining admissible proof target is narrower:

```text
public endpoint-chain transport state
+ independently defined Psi(RB) chamber-balance criterion
+ typed prefix/suffix rewrite antecedent
=> not Psi(RB(C, C'))
```

### Transported Commitment-Exclusivity Bridge Candidate

The current proof target can be stated as one bridge theorem.

Definitions:

```text
PrefixMaterial(C, C') :=
  w(C') in [T_N(r(C)), T_N(w(C))]
  and lambda(C') <= lambda(C).

ThreatMaterial(C, C') :=
  d(C) = T_<(w(C))
  and w(C') in [T_N(d(C)), T_N(r(C))]
  and lambda(C') < lambda(C).

DirectFrontier(C, C') :=
  FreshEndpoint(C') and Psi(RB(C, C')).
```

Bridge theorem candidate:

```text
For every valid public transported certificate pair (C, C'),
if PrefixMaterial(C, C') or ThreatMaterial(C, C'), then not Psi(RB(C, C')).
```

Together with `DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C,C'))`,
this gives:

```text
PrefixMaterial(C, C') or ThreatMaterial(C, C')
=> not DirectFrontier(C, C')
```

The theorem has three independent source obligations:

```text
T1 prefix commitment transport:
  reciprocal floor transport sends carrier-to-reset source commitment into
  committed transported prefix material.

T2 threat-horizon transport:
  reciprocal floor transport sends endpoint-to-lower-threat source commitment
  into committed transported threat-horizon material.

T3 frontier commitment exclusivity:
  committed transported source material cannot also satisfy the independently
  defined direct frontier language Psi(RB).
```

Bridge-obligation audit:

```text
T1 prefix commitment transport
  proved source input:
    GWR selects w(C) as the first minimum-divisor carrier.
    NLSC gives no later lower-divisor interior point before r(C).
  closed arithmetic input:
    w(C') in [T_N(r(C)), T_N(w(C))]
    iff w(C')w(C) <= N < (w(C') + 1)r(C).
  measured support:
    PrefixMaterial rows = 101.
    PrefixMaterial non-reset source lifts below source lambda = 0.
  missing theorem step:
    reciprocal floor image of [w(C), r(C)] inherits source carrier-to-reset
    commitment as transported prefix material for C'.
  falsification condition:
    PrefixMaterial(C, C') and Psi(RB(C, C')).

T2 threat-horizon transport
  proved source input:
    if T_<(w(C)) exists, NLSC gives r(C) <= T_<(w(C)).
  certificate input:
    deadline=threat identifies d(C) with the public lower-threat point.
  closed arithmetic input:
    w(C') in [T_N(d(C)), T_N(r(C))]
    iff w(C')r(C) <= N < (w(C') + 1)d(C).
  measured support:
    ThreatMaterial rows = 12.
    ThreatMaterial unrecorded suffix-interior lifts below source lambda = 0.
  missing theorem step:
    reciprocal floor image of [r(C), T_<(w(C))] inherits endpoint-to-threat
    commitment as transported threat-horizon material for C'.
  falsification condition:
    ThreatMaterial(C, C') and Psi(RB(C, C')).

T3 frontier commitment exclusivity
  available public interface:
    DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C, C')).
  measured support:
    TypedMaterial rows = 107, direct effective rows = 0.
    effective/direct eliminated RB overlap = 0.
  guarded invalidations:
    Psi cannot be raw novelty, ledger survivor state, observed RB-class lookup,
    broad story rewrite, run-word superset, simple balance threshold, or
    per-run coordinate-monotone balance region.
  missing theorem step:
    define Psi(RB) as an independent structural chamber-balance language and
    prove committed transported material is outside it.
  falsification condition:
    typed material satisfies Psi(RB), or Psi reads typed/post-elimination state.
```

### Implementation Construction Order

The current sidecar implementation in `transported_story_law_probe.py`
constructs one row in this deterministic order:

```text
1. build source PGSPG certificate story from public source certificate C
2. extract public carrier, reset, deadline, and optional lower-threat events
3. transport source story coordinates through T_N(x) = floor(N / x)
4. define transported prefix and suffix intervals from those public images
5. derive induced anchor from previous_endpoint(T_N(r(C)))
6. build induced PGSPG certificate story C'
7. evaluate public carrier-in-prefix and carrier-in-suffix interval flags
8. evaluate lock-label comparisons
9. write ledger prefix/suffix/threat elimination labels
10. write stale, survivor, and effective-survivor labels
```

Therefore an admissible `Psi(RB)` must be stated no later than step 7 from the
public endpoint-chain transport state and chamber-balance signature. It cannot
read steps 9 or 10. Reading those fields would convert T3 into a circular
restatement of the sidecar ledger.

The source and induced story rows used by that sidecar are generated by
`certificate_commitment_story_probe.py` in a fixed public grammar:

```text
closed_offset*
carrier_lock?
reset
lower_threat?
tail*
deadline
```

This fixed event order is the implementation source of the ordered interval run
word `R(C, C')` and the source/induced closed-tail balance coordinates. It is
also why the RB preservation guards are meaningful: they are testing a public
story grammar projection, not a post-ledger classifier. The remaining proof
step is to derive the same projection as a PGSPG transport law.

Guarded implementation fact:

```text
all measured source and induced story event-kind words match
closed_offset* carrier_lock? reset lower_threat? tail* deadline
```

Guarded RB implementation fact:

```text
RB(C, C') is unchanged after deleting ledger labels, raw frontier novelty,
carrier-in-prefix/suffix flags, and threat-ceiling flags from the sidecar row.
```

This makes `RB` an admissible pre-ledger input for `Psi`. It does not define
`Psi`, and it does not prove the bridge theorem.

Guarded measured separation:

```text
TypedMaterial RB classes = 101
non-TypedMaterial RB classes = 374
TypedMaterial RB classes ∩ non-TypedMaterial RB classes = empty
```

This means the current measured surface has no lock-label ambiguity inside one
RB class: every typed material RB class is disjoint from the non-typed RB
classes. This supports the narrowed `Psi(RB)` interface, but it is still
measured evidence rather than a structural definition of `Psi`.

Guarded carrier-local preservation:

```text
RB classes = 475
RB classes with more than one induced-carrier interval symbol = 0
RB classes with more than one source/induced lock-label relation = 0
RB classes with more than one source deadline-threat boundary state = 0
```

Thus, on the current measured surface, `RB(C, C')` determines whether the
induced carrier is in transported `P`, `S`, `B`, or `O` position, and it also
determines the measured source/induced lock-label relation and deadline-threat
boundary. This supports using RB as a carrier-local chamber-balance object. It
does not prove that carrier symbol, lock relation, or deadline-threat boundary
is structurally determined by RB in all valid transported certificate pairs.

Guarded typed-branch RB topology:

```text
PrefixMaterial RB classes = 95
ThreatMaterial RB classes = 12
PrefixMaterial RB classes ∩ ThreatMaterial RB classes = 6
TypedMaterial RB classes = 101
TypedMaterial RB classes ∩ effective RB classes = empty
TypedMaterial RB classes subset direct eliminated RB classes = true
```

The measured branch-class partition by RB is:

```text
non-typed RB classes = 374
prefix-only RB classes = 89
prefix+threat RB classes = 6
threat-only RB classes = 6
RB classes with mixed branch labels = 0
```

The measured prefix/threat RB-class intersection is:

```text
('OBO', 33, 17)
('OBO', 33, 20)
('OBO', 34, 17)
('OBPO', 34, 33)
('POBO', 33, 19)
('POBO', 34, 21)
```

Thus T1 and T2 have overlapping chamber-balance boundary classes. The bridge
theorem must allow the prefix and threat-horizon transport readings to meet on
those classes without turning the overlap into a table-defined `Psi`.

### RB Sufficiency Sublemma

Measured sublemma:

```text
On the current 512-row public transported-story surface, RB(C, C') determines
the carrier-local data needed to classify the narrowed typed antecedents:
  induced-carrier interval symbol,
  source/induced lock-label relation,
  source deadline-threat boundary,
  typed branch class.
```

Proof role:

```text
If this sublemma is proved structurally for valid transported certificate
pairs, then Lemma 1 and Lemma 2A can be stated entirely against Psi(RB):

  PrefixMaterial(C, C') => not Psi(RB(C, C'))
  ThreatMaterial(C, C') => not Psi(RB(C, C'))
```

Current status:

```text
measured support: guarded
structural proof: missing
resolver promotion: blocked
```

Proof skeleton:

```text
1. Certificate story grammar fixes event-kind order:
   closed_offset* carrier_lock? reset lower_threat? tail* deadline.

2. Reciprocal transport classifies each induced story value against the public
   transported prefix and suffix bands, producing the ordered interval word.

3. Collapsing adjacent equal interval symbols gives R(C, C').

4. The two balance coordinates
     source_closed_count - source_tail_count
     induced_closed_count - induced_tail_count
   summarize the closed-tail chamber load on each side of the transported
   pair.

5. To prove RB Sufficiency, show that within this fixed story grammar and
   reciprocal interval transport, the triple
     (R(C, C'), source_balance, induced_balance)
   determines:
     induced-carrier interval symbol,
     source/induced lock-label relation,
     source deadline-threat boundary,
     typed branch class.
```

Missing proof step:

```text
The measured guards show step 5 on the current 512-row surface. They do not
prove that fixed grammar plus the two closed-tail balances determine those
carrier-local fields for every valid transported certificate pair.
```

The sublemma is falsified by a valid public transported certificate pair where
two rows have the same `RB(C, C')` but different carrier interval symbol,
different lock-label relation, different deadline-threat boundary, or different
typed branch class.

Conventional form:

Let `V_N` be the set of valid public transported certificate pairs for a fixed
public modulus `N`. Define

```text
pi(C, C') = RB(C, C')
chi(C, C') = induced-carrier interval symbol
rho(C, C') = sign(lambda(C') - lambda(C))
theta(C, C') = source deadline-threat boundary state
beta(C, C') = typed branch class
```

RB Sufficiency is the refinement statement:

```text
pi(C1, C1') = pi(C2, C2')
=>
chi(C1, C1') = chi(C2, C2')
rho(C1, C1') = rho(C2, C2')
theta(C1, C1') = theta(C2, C2')
beta(C1, C1') = beta(C2, C2')
```

for all pairs `(C1, C1')` and `(C2, C2')` in `V_N`, or in the intended
cross-modulus valid transported-pair family if the theorem is stated globally.

This is not a scalar invariant claim. It is a projection-refinement claim:
`RB` must be fine enough to determine exactly the carrier-local predicates
needed by Lemma 1 and Lemma 2A.

### RB Sufficiency Derivation Attempt

The currently listed ingredients are:

```text
fixed certificate story grammar
reciprocal interval transport
collapsed interval run word R(C, C')
source closed-tail balance
induced closed-tail balance
```

These ingredients do not by themselves prove RB Sufficiency. The fixed grammar
plus balances are compatible with different carrier symbols before PGSPG
validity and reciprocal floor geometry are imposed.

Symbolic obstruction:

```text
grammar word: closed_offset carrier_lock reset deadline
event-symbol word A: O P O O
event-symbol word B: O O P O
collapsed run word for A: OPO
collapsed run word for B: OPO
induced closed-tail balance for A: 1
induced closed-tail balance for B: 1
carrier symbol for A: P
carrier symbol for B: O
```

The source balance can be held fixed independently, so both symbolic rows have
the same formal `RB = (OPO, source_balance, 1)` and different carrier symbols.

Status of this obstruction:

```text
PGS counterexample: not established
proof-source countermodel: established for grammar plus balances alone
```

It shows that step 5 in the RB Sufficiency skeleton cannot be discharged from
the fixed grammar and the two balances alone. A structural proof must use an
additional PGSPG transport law that rules out the symbolic ambiguity for valid
transported certificate pairs.

The needed law can be stated narrowly:

```text
Carrier Localization Under Reciprocal Transport:
  in a valid transported certificate pair, the collapsed interval run word and
  closed-tail balances determine which interval run contains the induced
  carrier event.
```

This law is not currently in `PROOF.md`, and it is not implied by local
GWR/NLSC. It must be proved from reciprocal transport geometry plus certificate
validity, or replaced by a minimal public counterexample.

Formal carrier-localization target:

Let the induced certificate story have event kinds

```text
closed_offset^c carrier_lock reset lower_threat? tail^t deadline
```

and let

```text
sigma_i in {P, S, B, O}
```

be the transported interval symbol of the `i`th induced story event. Let
`R` be the collapsed run word obtained from the sequence `sigma_i`, and let
`run(i)` be the one-based collapsed run ordinal containing event `i`. The
induced carrier has index `c + 1`. Carrier localization asks for a structural
function

```text
kappa(R, source_balance, induced_balance)
```

such that, for every valid transported certificate pair,

```text
run(c+1) = kappa(R, source_balance, induced_balance).
```

The carrier interval symbol is then the `kappa(...)`th symbol of `R`.

Proof skeleton:

```text
1. The induced story grammar locates the carrier event after all induced
   closed_offset events and before reset, tail, and deadline events.

2. The reciprocal interval symbols are computed from public floor images of
   source carrier/reset/deadline values.

3. RB keeps only the collapsed symbol run word and the two closed-tail
   balances; it does not keep c, t, the carrier index c+1, or the event-kind
   attached to each run boundary.

4. Therefore a proof must show that valid reciprocal transport geometry
   reconstructs the carrier run from the retained balance data.

5. After carrier localization is proved, lock-relation and deadline-threat
   refinement remain separate; they do not follow merely from knowing the
   carrier symbol.
```

Unresolved sublemmas for carrier localization:

```text
Run-Boundary Count Law:
  the number of induced closed_offset events before each transported interval
  boundary is determined by RB for valid transported pairs.

Carrier-Run Boundary Law:
  the carrier index c+1 cannot cross a transported interval boundary without
  changing RB in a way detected by source_balance or induced_balance.

Closed-Tail Compensation Exclusion:
  adding one induced closed_offset before the carrier and one induced tail after
  reset preserves induced_balance, so valid PGSPG transport must prohibit this
  compensation from moving the carrier into a different interval symbol while
  preserving the same collapsed run word.
```

Minimal carrier-localization counterexample condition:

```text
there exist valid public transported certificate pairs (C1, C1') and
(C2, C2') with the same R(C, C'), the same source closed-tail balance, and the
same induced closed-tail balance, but the induced carrier events occupy
different transported interval symbols.
```

This counterexample would falsify Carrier Localization Under Reciprocal
Transport and therefore falsify RB Sufficiency. It would leave the measured
512-row guard intact as finite evidence.

Measured carrier-localization extension:

```text
direct story-law rows = 512
direct RB classes = 475
direct RB classes with mixed carrier symbols = 0
direct RB classes with mixed carrier run ordinals = 0

recursive story-law rows = 713
recursive RB classes = 661
recursive RB classes with mixed carrier symbols = 0
recursive RB classes with mixed carrier run ordinals = 0

combined direct plus recursive rows = 1225
combined RB classes = 661
combined RB classes with mixed carrier symbols = 0
combined RB classes with mixed carrier run ordinals = 0
```

This extends the finite carrier-localization guard from the direct surface to
the recursive public surface. It is still measured evidence, not a proof of the
Carrier Localization Under Reciprocal Transport law.

Measured non-target:

```text
direct RB classes with mixed exact carrier index = 5
recursive RB classes with mixed exact carrier index = 5
combined RB classes with mixed exact carrier index = 5

direct RB classes with mixed induced closed_offset count = 5
recursive RB classes with mixed induced closed_offset count = 5
combined RB classes with mixed induced closed_offset count = 5

direct RB classes with mixed induced story length = 5
recursive RB classes with mixed induced story length = 5
combined RB classes with mixed induced story length = 5
```

Therefore Carrier Localization Under Reciprocal Transport must not be stated as
exact carrier-index reconstruction. The supported target is collapsed interval
run localization of the carrier, not recovery of the full induced event-kind
alignment.

Measured projection boundary:

```text
combined direct plus recursive surface

projection -> RB carrier-run ambiguity count
R(C, C') alone -> 12
(R(C, C'), source_balance) -> 18
(R(C, C'), induced_balance) -> 17
(R(C, C'), induced_balance - source_balance) -> 6
(R(C, C'), source_balance, induced_balance) -> 0
```

Thus the current measured surface requires the full RB triple for carrier-run
localization. A proof route that uses only the collapsed run word, one balance
coordinate, or the balance delta is already invalidated by public rows.

The other RB Sufficiency fields show the same measured dependence on the full
triple:

```text
combined direct plus recursive surface

lock relation ambiguity:
  R alone -> 26
  (R, source_balance) -> 8
  (R, induced_balance) -> 36
  (R, induced_balance - source_balance) -> 16
  full RB -> 0

deadline-threat boundary ambiguity:
  R alone -> 22
  (R, source_balance) -> 0
  (R, induced_balance) -> 39
  (R, induced_balance - source_balance) -> 17
  full RB -> 0

typed branch ambiguity:
  R alone -> 16
  (R, source_balance) -> 11
  (R, induced_balance) -> 19
  (R, induced_balance - source_balance) -> 6
  full RB -> 0
```

The `deadline-threat` field is already determined by `(R, source_balance)` on
the measured combined surface. The full RB triple is still required for the
whole RB Sufficiency package because carrier-run localization, lock relation,
and typed branch classification are ambiguous under every smaller projection
listed above.

Simple structural `Psi(RB)` candidates remain invalid. On the direct measured
RB-class surface, each of the following leaks against the `not TypedMaterial`
target:

```text
R has no P or B
R starts with S or O
induced_balance >= source_balance
induced_balance > source_balance
source_balance >= induced_balance
induced_balance >= source_balance and R has no B
induced_balance > source_balance or R has no B
R has no P
R has no B
R ends with P
```

The measured ranges overlap:

```text
TypedMaterial delta range = [-24, 16]
non-TypedMaterial delta range = [-25, 23]
effective delta range = [-25, 23]
```

Therefore `Psi(RB)` is still not an inequality or coarse word-shape predicate
over the current ingredients. The missing object remains a structural
chamber-balance language, not a scalar threshold.

Lock-relation refinement also requires the full collapsed run word, not only
the localized carrier run:

```text
combined direct plus recursive surface

(carrier_run, source_balance, induced_balance) -> 4 lock-relation ambiguities
(carrier_symbol, source_balance, induced_balance) -> 5 lock-relation ambiguities
(carrier_run, induced_balance - source_balance) -> 48 lock-relation ambiguities
(carrier_symbol, induced_balance - source_balance) -> 38 lock-relation ambiguities
full RB -> 0 lock-relation ambiguities
```

Thus carrier localization is a necessary refinement step, but it is not enough
to recover the lock relation. The full ordered run word still carries
structural information needed by the Lock-Relation Balance Law.

The four measured `(carrier_run, source_balance, induced_balance)` ambiguity
groups are:

```text
(3, 33, 31):
  BOSPO -> equal
  POBO  -> higher

(2, 34, 33):
  OBPO -> lower
  OSBP -> higher

(3, 33, 33):
  OPOP  -> equal
  POSBP -> higher

(2, 33, 33):
  BOP  -> equal
  OSBO -> lower
  OSBP -> higher
```

Therefore the Lock-Relation Balance Law must use off-carrier run context. The
carrier's localized run and the two balances do not determine the relation
between `lambda(C')` and `lambda(C)`.

Typed branch projection has a smaller measured form after the carrier symbol,
lock relation, and deadline-threat state are known:

```text
combined direct plus recursive surface

(carrier_run, lock_relation, deadline_threat) -> 11 typed-branch ambiguities
(carrier_symbol, lock_relation, deadline_threat) -> 0 typed-branch ambiguities
(carrier_run, lock_relation, deadline_threat, source_balance, induced_balance)
  -> 57 typed-branch ambiguities
(carrier_symbol, lock_relation, deadline_threat, source_balance, induced_balance)
  -> 0 typed-branch ambiguities
full RB -> 0 typed-branch ambiguities
```

Thus the typed branch does not need the full run word once the earlier
refinements are available. It needs the carrier interval symbol, not merely the
carrier run ordinal:

```text
carrier symbol + lock relation + deadline-threat boundary
=> typed branch class
```

This is a measured candidate for the Typed-Branch Projection Law.

The remaining RB Sufficiency proof then splits into three further refinement
laws:

```text
Lock-Relation Balance Law:
  RB determines the sign of lambda(C') - lambda(C).

Deadline-Threat Boundary Law:
  RB determines whether d(C) is the lower-threat deadline.

Typed-Branch Projection Law:
  after the carrier symbol, lock relation, and deadline-threat state are fixed,
  RB determines whether the pair is prefix material, threat material, both, or
  neither.
```

Measured guards currently support all four refinement laws on the 512-row
surface. The structural proof is missing for all four.

Measured refinement projection boundary on the combined direct plus recursive
surface:

```text
Lock relation ambiguity counts:
  R alone -> 26
  R plus source_balance -> 8
  R plus induced_balance -> 36
  R plus balance_delta -> 16
  full RB -> 0

Deadline-threat ambiguity counts:
  R alone -> 22
  R plus source_balance -> 0
  R plus induced_balance -> 39
  R plus balance_delta -> 17
  full RB -> 0

Typed-branch ambiguity counts:
  R alone -> 16
  R plus source_balance -> 11
  R plus induced_balance -> 19
  R plus balance_delta -> 6
  full RB -> 0
```

This separates the proof pressure:

```text
deadline-threat boundary has a smaller measured projection:
  source_balance alone

carrier-run localization, lock relation, and typed branch class require the
full RB triple on the measured combined surface.
```

Measured deadline-threat threshold:

```text
combined direct plus recursive surface

source_balance = 8..31  => deadline-threat boundary = false
source_balance = 32..34 => deadline-threat boundary = true
```

Equivalently, on the measured public surface:

```text
deadline_threat(C) iff source_balance(C) >= 32.
```

This is a candidate for the Deadline-Threat Boundary Law. It is measured
evidence, not a proved universal threshold.

Minimal valid-pair counterexample condition:

```text
there exist valid public transported certificate pairs (C1, C1') and
(C2, C2') with the same RB(C, C') but with different carrier interval symbols,
different lock-label relations, different deadline-threat states, or different
typed branch classes.
```

Such a counterexample would falsify RB Sufficiency. It would not falsify
`PROOF.md` local GWR/NLSC, because those theorems do not contain the transported
projection `pi(C, C')`.

The following definition is therefore rejected:

```text
Psi(RB(C, C')) := RB(C, C') is not in the measured TypedMaterial RB-class set.
```

It is measured-perfect on the current direct surface, but it is a finite class
lookup. The structural replacement must explain why those RB classes are
committed transported material classes using public chamber-balance laws, not
by naming the observed material-class table.

The bridge theorem is falsified by:

```text
a valid public pair (C, C') with
  PrefixMaterial(C, C') or ThreatMaterial(C, C')
  and Psi(RB(C, C')).
```

It is circular if `Psi` reads PrefixMaterial, ThreatMaterial, TypedMaterial,
ledger elimination, ledger survivor state, observed RB class tables, recurrence
state, audit state, or hidden factor state.

Minimal non-circular requirements for the missing definition:

```text
1. It is computed before prefix/suffix rewrite and recurrence predicates.
2. It uses only public endpoint-chain transport state.
3. It distinguishes valid transported frontier commitment from raw anchor
   novelty.
4. It does not reject all story rewrites, because suffix/equal rewrites can
   remain measured effective survivors.
5. It gives a falsifiable condition for a prefix lower/equal or threat-suffix
   lower row to be a genuine new frontier commitment.
```

Current status:

```text
definition of Psi(RB): missing
typed exclusion proof against Psi(RB): missing
official resolver promotion: blocked
```

The exact unresolved core is:

```text
committed source story segment
+ reciprocal floor image
+ induced opposite certificate carrier in that image
+ non-increasing typed lock relation
=> rewrite, not new transported frontier commitment
```

Until T3 is proved, typed coverage remains measured evidence rather than a
transported certificate theorem.

## Lemma 3: Recursive Anchor Recurrence Lemma

Under the narrowed frontier interface, the endpoint-history form of this lemma
is closed:

```text
DirectFrontier(C, C') := FreshEndpoint(C') and Ψ(RB(C, C')).

not FreshEndpoint(C') => not DirectFrontier(C, C')
```

The remaining open part is the older recursive-collapse lift:

```text
direct frontier status from Ψ(RB)
+ layer-by-layer endpoint-chain recurrence
=> recursive_final_survivor_count = 0
```

That broader statement remains measured evidence, not theorem status.

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
local GWR/NLSC non-entailment: proved negative result for the current proof source
transported_story_law_v1 collapse: measured public evidence
reciprocal floor-cell membership: closed arithmetic sublemma
integer source-preimage equivalence: measured on the 512-row surface;
  symmetric difference with carrier-zone flags is 0
lower_threat field identity: implementation/certificate fact; PROOF.md supplies
  only the abstract T_<(w) horizon statement
prefix elimination: proof skeleton exists; transport coherence and equal-label
  frontier uniqueness are unresolved
PrefixMaterial(C, C'): non-circular public candidate exists for prefix
  material; implication to not Psi(RB(C, C')) is unproved
prefix equal-label branch: essential to current collapse and unproved
suffix threat branch: narrowed Lemma 2A proof skeleton exists; transported
  threat-horizon coherence is unresolved
ThreatMaterial(C, C'): non-circular public candidate exists for strict
  threat-suffix material; implication to not Psi(RB(C, C')) is unproved
TypedMaterial(C, C'): measured reduction exists as PrefixMaterial or
  ThreatMaterial; covers 107 direct eliminated rows with 0 effective rows;
  implication to not Psi(RB(C, C')) is unproved
suffix tail branch: redundant on the current measured collapse and unresolved
Psi(RB): structural chamber-balance language missing under the narrowed
  DirectFrontier interface
rejected FrontierCommit definitions: raw novelty, ledger survivor states,
  broad non-rewrite, reduced grammar alone, threat/tail image positions alone,
  width matching alone, story-kind grammar alone, coarse interval occupancy
reduced grammar: admissible candidate ingredient, not a definition; projection
  surface has 50 rows and is not a row-wise classifier for the 512 direct rows
full ordered interval-position word: admissible candidate ingredient, too
  close to row identity as currently measured
RB signature: current best measured admissible Psi input;
  separates direct effective from direct eliminated rows in the measured
  512-row surface, but structural language proof is missing
RB Sufficiency Sublemma: measured support guarded; structural proof missing;
  required before Lemma 1 and Lemma 2A can be stated entirely against Psi(RB)
recurrence elimination: unproved proof obligation
grammar projection: measured bridge, not proved
official PGSMD status: unresolved
```

The next mathematical task is not another ledger search. It is to prove or
falsify a structural `Psi(RB)` chamber-balance language from public
endpoint-chain transport state, then prove typed rewrite exclusion against that
language. Lemma 3 then supplies the independent endpoint-history boundary, and
Lemma 4 connects the result to the reduced grammar evidence.
