# Simple Balance Proof Goal

## Goal

Prove the simple reason that the selected public position stabilizes
endpoint-space absence exactly at the balanced right endpoint condition.

The proof should not introduce another compatibility catalog. The current
object has already collapsed to two concrete facts:

```text
N is the first minimum-divisor composite in its public prime gap
and
the two factor endpoints reach the middle right-open boundary without crossing it
```

That is the goal now.

## Public Side

In this corpus, `N = pq` with distinct prime factors. Therefore:

```text
tau(N) = 4
```

If `N` is the selected public position inside its containing prime gap, then the
gap winner has divisor count `4`. The active six-window corpus verifies:

```text
public at selected position, selected divisor count 4: 31679 rows
public at selected position, selected divisor count not 4: 0 rows
```

So the public condition can be read without extra terminology:

```text
N is the first integer in its public prime gap where the divisor count reaches 3 or 4
```

Equivalently:

```text
no earlier integer in the same public prime gap has divisor count 3 or 4
```

The first-minimum balance probe verifies that this literal condition is exactly
equivalent to the public selected-position label in the active six-window
corpus:

```text
row_count = 138602
literal first divisor-count-3-or-4 mismatches = 0
```

This is the first simplification. The public side is a first-minimum statement.

The shared load-boundary probe gives the next simplification. On the active
candidate surface, the public selected divisor count is always `4`, and the
clean endpoint boundary is also `4`:

```text
endpoint right boundary = public selected divisor count
```

The old endpoint transport defect is just the normalized version of this same
load difference:

```text
endpoint right boundary - public selected divisor count = 0
```

The probe verifies:

```text
load-delta / endpoint-defect mismatches = 0
```

The same load match stays clean locally:

```text
public containing types with load-match falsification = 0
public words with load-match falsification = 0
```

The support profile rules out a cheap explanation. The load-match row is not
clean because it is weakly supported:

```text
load-match prior pair support median = 14
load-match prior boundary support median = 1145
load-match exact falsifications = 0
```

The leaking rows have comparable pair support and weaker boundary support.

The reentry profile sharpens the target again. The shared load boundary does
not keep the coarse right-boundary cell absent:

```text
load-match boundary reentry rows = 90
load-match exact endpoint-pair reentry rows = 0
```

So the proof is not a boundary-absence proof. It is a blocked-lift proof:

```text
under shared load equality,
right-boundary reentry does not lift to exact endpoint-pair reentry
```

The left-phase probe identifies the missing lift component:

```text
load-match boundary reentry rows = 90
load-match left residue reappears = 23
load-match left phase reappears = 0
load-match exact endpoint-pair reentry = 0
```

Thus the current obstruction is:

```text
under shared load equality,
right-boundary reentry cannot preserve the old left phase arrangement
```

The phase-shift probe makes that obstruction concrete:

```text
load-match boundary reentry rows = 90
candidate left phases containing very_late = 0
observed replacement left phases containing very_late = 90
candidate left phase reappears = 0
```

So the measured blocked lift is:

```text
shared load equality
    -> right-boundary reentry shifts the left phase into a very_late family
    -> old exact endpoint pair remains absent
```

The reentry-cell probe removes another layer of vocabulary. The load-match
boundary reentry is not a large cloud:

```text
candidate load-match reentry rows = 90
distinct load-match reentered boundary cells = 2
observed forward exact rows in load-match reentered cells = 2
```

Both exact replacement rows have the same right boundary:

```text
right boundary residues = o4|o4
```

In both rows, the `very_late` left phase is a literal endpoint approach:

```text
left selected point is two units before the right endpoint
```

The neighboring load states do not share this exact profile:

```text
shortfall delta -2: 3 observed exact reentry rows, 0 with minimum left right-distance 2
balance  delta  0: 2 observed exact reentry rows, 2 with minimum left right-distance 2
overshoot delta +2: 51 observed exact reentry rows, 14 with minimum left right-distance 2
```

So the current arithmetic obstruction is:

```text
shared load equality
    -> right-boundary reentry lifts through a left gap with right-distance 2
    -> old candidate left phases cannot reappear
```

The factor-left semantics audit gives the literal meaning of that
right-distance:

```text
factor-side records audited = 561444
stored left winner is immediate previous endpoint = 561444
```

The current factor-left record is a bridge from the second previous endpoint to
the factor endpoint. Its selected point is the immediate previous endpoint. So:

```text
left selected point two units before the factor
    =
immediate previous endpoint is two units before the factor
```

The proof target is now:

```text
shared load equality
    -> right-boundary reentry lifts through a factor with immediate-left
       endpoint distance 2
    -> old exact endpoint pair remains absent
```

The terminal-twin lift probe separates the replacement rows from the prior
supported candidate classes:

```text
candidate load-match reentry rows = 90
prior pair support rows = 8253
prior pair support rows with terminal-twin lift = 0
observed replacement rows = 2
observed replacement rows with terminal-twin lift = 2
```

Here:

```text
terminal-twin lift =
    immediate-left endpoint distance 2
    inside a factor-left bridge of width at least 20
```

Equivalently:

```text
terminal-twin lift =
    one replacement factor is the right endpoint of a twin endpoint pair
    whose preceding gap has width at least 18
```

Distance `2` alone is not enough. Prior support rows do contain distance `2`
inside shorter bridges. The balanced replacement rows require the terminal
twin inside a long enough bridge.

So the current proof target is:

```text
shared load equality
    -> right-boundary reentry forces terminal-twin lift
    -> old supported exact-pair class cannot be the lift
    -> exact endpoint-pair absence remains stable
```

The public o6 terminal-twin trigger probe sharpens the scope. The terminal-twin
lift is not a general property of every `o6_d4_a6` public row. It appears in the
supported prior-absent balanced reentry cells for two public keys:

```text
o4 even -> o6@mid -> o4 odd
o4 odd  -> o6@early -> o6 odd
```

Measured per-public-key support:

```text
candidate rows = 46 and 44
public-key prior support rows = 8080 and 8063
prior terminal-twin rows = 0 and 0
observed replacements = 1 and 1
observed terminal-twin replacements = 1 and 1
```

So the current falsifiable arithmetic statement is:

```text
For the two supported prior-absent public o6_d4_a6 balanced right-boundary
cells, any forward reentry of Rres=o4|o4 requires terminal-twin lift.
```

The public o6 residue bridge probe extracts the wheel arithmetic underneath the
two triggers:

```text
endpoint residues with first right-open offset 4 = 7, 13, 19
N mod 30 = 7
only ordered o4|o4 factor residue pairs with product 7 = 13|19 and 19|13
```

So:

```text
public selected residue 7
and
balanced right endpoint boundary o4|o4
    -> factor residues are 13 and 19, in some order
```

The residue bridge alone does not force terminal-twin lift:

```text
trigger Rres=o4|o4 rows = 11
trigger terminal-twin rows = 3
```

The supported prior-absent reentry condition is the active filter:

```text
observed replacement rows = 2
observed terminal-twin replacement rows = 2
```

The remaining proof object is therefore:

```text
inside the supported prior-absent trigger cells,
the 13|19 balanced residue bridge reenters only through terminal-twin lift
```

The residue bridge itself is now proved as a mod-30 lemma:

```text
public o6 selected offset 6
and
balanced right endpoint boundary o4|o4
    -> {p mod 30, q mod 30} = {13, 19}
```

Reason:

```text
o4 endpoint residues = {7, 13, 19}
o4|o4 product residues = {1, 7, 13, 19}
public o6 selected offset 6 gives N residues {7, 29}
intersection = {7}
only o4|o4 products equal to 7 are 13*19 and 19*13
```

So this part is no longer merely measured. The current unproved object is the
terminal-twin lift after the residue bridge has forced `{13, 19}`.

The lower terminal-twin orientation probe sharpens the lift direction:

```text
trigger Rres=o4|o4 rows = 11
terminal side none = 8
terminal side p = 2
terminal side p|q = 1
terminal side q only = 0
```

For the two supported prior-absent replacement rows:

```text
observed terminal side p = 2
observed terminal side q only = 0
observed terminal side p|q = 0
```

The lower terminal residue is trigger-specific on the replacement surface:

```text
o4 even -> o6@mid -> o4 odd: lower terminal residue = 13
o4 odd  -> o6@early -> o6 odd: lower terminal residue = 19
```

The current statement is therefore:

```text
inside the supported prior-absent trigger cells,
the 13|19 balanced residue bridge reenters only when the lower factor is the
right endpoint of a terminal twin endpoint pair, with the lower residue chosen
by the public trigger
```

The next clean band `34001..35000` preserves the simple boundary surface.
With the earlier windows used as train, calibration, and prior-forward support,
the fresh band gives:

```text
right_residues: 1201 testable cells, 0 falsified
right_residue_phases: 1370 testable cells, 1 falsified
both_residues: 1394 testable cells, 6 falsified
left_residue_phases: 441 testable cells, 3 falsified
```

The terminal-twin trigger counts remain unchanged after the fresh band:

```text
observed replacement rows = 2
observed terminal-twin replacement rows = 2
prior terminal-twin support rows = 0
```

So the fresh result supports the current reduction. The proof should stay on
the right-residue boundary and the lower-factor terminal-twin lift, not return
to a larger phase grammar.

The span-36 terminal-lift probe adds one more arithmetic reduction. In the 11
public `o6` residue-bridge trigger rows, the two observed supported
prior-absent replacements are exactly the rows where:

```text
q - p = 0 mod 36
and
the lower factor has terminal-twin lift
```

Since the mod-30 residue bridge has already forced the factor residues to
`13|19` or `19|13`, the span-36 condition is a factor phase-lock:

```text
p mod 36 = q mod 36
```

The two observed replacement lanes modulo `180` are:

```text
43|79
49|13
```

The phase lock also fixes the public product residue:

```text
N = 37 mod 60
```

Since the public selected offset is `6`, the public left endpoint is:

```text
31 mod 60
```

Same-lane prior support reaches that public anchor without lifting:

```text
same-lane prior rows in observed mod-180 lanes = 42
same-lane prior rows with public left endpoint 31 mod 60 = 7
same-lane prior rows with lower twin distance = 8
same-lane prior rows with both = 0
```

Span divisibility alone is not enough:

```text
prior pair support rows = 8253
prior rows with q - p = 0 mod 36 = 1336
prior rows in observed mod-180 lanes = 42
prior rows with q - p = 0 mod 36 and lower terminal lift = 0
prior rows in observed mod-180 lanes with lower terminal lift = 0
```

So neither span-36 nor the resulting mod-180 lane is the whole explanation. The
remaining obstruction is still the lower-factor terminal-twin lift.

The same-lane contrast makes the lift literal. Same-lane prior rows can place
the lower factor two units after the previous endpoint, but only after short
preceding gaps:

```text
same-lane prior lower twin rows = 8
same-lane prior lower twin preceding gap widths = 4, 10, 12
same-lane prior maximum preceding gap width = 12
```

The observed replacement rows have:

```text
lower twin preceding gap widths = 18 and 22
```

So the current obstruction is not simply "lower twin." It is:

```text
lower twin after a preceding gap of width at least 18
```

Equivalently, in the observed lanes, that preceding gap contains four interior
wheel-open slots:

```text
observed lower twin interior open slots = 4
same-lane prior lower twin interior open slots = 0 or 2
```

So the current proof target has sharpened again:

```text
shared load equality
and
public left endpoint 31 mod 60
and
balanced endpoint right boundary
and
span-36 reentry
and
lower twin distance
    -> lower factor is two units after the previous endpoint
       whose preceding gap contains four interior wheel-open slots
```

The former two-zero statement is therefore a shared-boundary statement:

```text
first public load 4
and
right endpoint boundary 4
```

## Endpoint Side

Each factor endpoint has a first open position to its right. Let:

```text
a = first right-open offset after p
b = first right-open offset after q
```

For the current wheel states:

```text
a, b are in {2, 4, 6}
```

The clean endpoint condition is:

```text
max(a, b) = 4
```

That means:

```text
at least one endpoint reaches the middle right-open offset
and neither endpoint reaches the high right-open offset
```

In residue form:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

This is the second simplification. The endpoint side is a middle-boundary
statement.

## Transport

Right movement at the factor endpoints transports through multiplication:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The first available right movements around `p` and `q` therefore become the
first directed outward product movements from `N`.

The balanced endpoint condition is the exact middle case of the three possible
right-boundary states:

```text
shortfall: max(a, b) = 2
balance:   max(a, b) = 4
overshoot: max(a, b) = 6
```

## Current Measured Law

Over supported prior-absent endpoint cells, the measured surface is:

```text
selected public position and max(a, b) = 4
    -> 45337 exclusions, 0 exact falsifications
```

The neighboring endpoint states leak:

```text
selected public position and max(a, b) = 2
    -> 14232 testable cells, 3 exact falsifications

selected public position and max(a, b) = 6
    -> 5663 testable cells, 27 exact falsifications
```

The balanced endpoint condition also leaks away from the selected public
position:

```text
after selected public position and max(a, b) = 4
    -> 1810 testable cells, 25 exact falsifications
```

So neither side is sufficient alone. The stable surface is the joint event:

```text
first divisor-count-3-or-4 position in the public gap
and
right endpoint boundary equal to the selected public divisor load
```

## Proof Shape

The proof should reduce to four small lemmas.

### Lemma 1: First-Minimum Public Lemma

For a semiprime `N = pq` with `p != q`, if `N` is the selected public position
inside its containing prime gap, then `N` is the first interior integer in that
gap with divisor count `3` or `4`.

This follows from `tau(N) = 4` and the definition of the selected gap position
as the first integer attaining the minimum divisor count.

### Lemma 2: Right-Boundary Trichotomy

The first right-open endpoint offsets fall into exactly three ordered states:

```text
2 < 4 < 6
```

The balanced state is the middle state:

```text
max(a, b) = 4
```

### Lemma 3: Directed Product Transport

The first right-open endpoint movements transport into product space by:

```text
aq
bp
aq + bp + ab
```

Thus the endpoint boundary is not decoration around the factors. It is the
first directed product boundary available from `N`.

### Lemma 4: Shared-Load Phase-Shift Lemma

For supported endpoint cells that are absent before the forward band, the
balanced endpoint realization has only one remaining escape route. The coarse
right-boundary cell can reenter, but the exact endpoint pair can reenter only
if the old left phase also reappears.

```text
right-boundary reentry
and
old left phase reentry
    -> exact endpoint-pair reentry remains possible
```

The measured load-match rows show the old left phase is forced out:

```text
candidate left phases: early|late, early|mid, late|late, late|mid, mid|mid
observed replacement phases: early|very_late, mid|very_late
```

The theorem target is therefore the phase shift itself:

```text
first public load 4
and
right endpoint boundary 4
and
right-boundary reentry
    -> terminal-twin lift
```

In the measured rows, terminal-twin lift is what appears as the `very_late`
left phase in the current bridge representation. Since the previously absent
balanced candidates do not contain terminal-twin lift in prior support, the old
left phase cannot reappear. That gives the desired contradiction:

```text
selected public position
and supported prior absence
and max(a, b) = 4
    -> endpoint cell remains absent
```

This is the remaining proof step.

## Current Status

```text
theorem_status = hypothesis_not_proved
measured_status = 45337 exclusions, 0 exact falsifications
proof_reduction_status = reduced_to_terminal_twin_lift_lemma
```

The next move is to prove why shared load equality forces the replacement lift
through terminal-twin lift in the two public o6 trigger neighborhoods after the
residue bridge has forced factor residues `13` and `19`, and why that lift is
lower-factor directed.
