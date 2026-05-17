# Zero-To-Zero Bridge Lemma Ladder

## Title

Zero-to-Zero Bridge: Public Load Equals Endpoint Right Load Forces Left-Side
Reentry Carrier

## Scope

This is the proof-facing object produced by the research meeting with Grok CLI.
It explains the current candidate mechanism behind:

```text
public_selected_defect(W) = 0
and endpoint_transport_defect(E) = 0
```

as a load-equality obstruction rather than a broad grammar rule.

The measured bridge is real in the current corpus. The transport necessity in
Rung 2 is still an unresolved proof target.

## Wheel Specificity

The number `4` is the concrete value taken by both:

```text
the first-minimum divisor count at the public GWR winner
```

and:

```text
the middle right-open offset in the current 30-wheel open-state grammar
```

It is not asserted as a universal numerical constant independent of this wheel.

## Rung 1: Residue Bridge

Clean statement:

```text
When the public zero places N at a position whose residue is 7
(public o6 trigger) and the endpoint right load equals 4
(o4|o4 boundary), the unordered factor residues are forced to exactly
{13, 19} by direct mod-30 arithmetic on the open residues.
```

Falsification predicate:

```text
Any semiprime row in which the public containing type is an o6_d4 trigger,
the right boundary value is 4, and the factor residues mod 30 are not
{13, 19}.
```

Status:

```text
arithmetic lemma candidate
```

## Rung 2: Load-Equality Transport Obstruction

Clean statement:

```text
Public zero places N at the GWR winner position where the public selected
load, the divisor count, is 4. Endpoint transport zero makes the endpoint
right load also 4. The resulting load equality removes every right-side
residual movement that could preserve the equality. Therefore any reentry of
a prior-absent supported cell that keeps the two loads matched must be carried
by the opposite directed side: the lower-factor immediate-left slot, realized
as terminal-twin lift.
```

Falsification predicate:

```text
Any row in which public selected load = 4, right boundary value = 4,
the endpoint cell is prior-absent and supported, and the cell re-enters as an
exact endpoint pair without the lower factor satisfying terminal-twin lift.
```

Status:

```text
measured bridge; unresolved transport necessity
```

## Rung 3: Phase-Bookkeeping Obstruction

Clean statement:

```text
The terminal-twin lift required by Rung 2 necessarily shifts the left phase of
the reentering pair into a very_late family that is absent from the prior
support surface of the same public trigger cell; therefore the original exact
endpoint pair cannot be the vehicle of reentry.
```

Falsification predicate:

```text
Any row that satisfies the conditions of Rung 2, load equality plus
terminal-twin lift on the lower factor, whose reentry left phase still belongs
to one of the prior-supported left-phase families for that public trigger cell.
```

Status:

```text
bookkeeping obstruction measured on the current support surface
```

## Bridge Summary

```text
Public zero selects the position at which the public load becomes 4; transport
zero makes the endpoint right load also 4; the load equality pins the right
side so that any preserving reentry must use the lower left side; that specific
left-side carrier, terminal-twin lift, produces a phase mismatch that blocks
the prior-absent exact pair.
```
