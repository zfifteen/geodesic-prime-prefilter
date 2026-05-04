# Twin-Prime Chamber Recurrence Target

Twin-prime gaps are the one-cell chambers of prime-gap structure.

For a twin-prime pair `p, p+2`, the only interior integer is `p+1`. Because
there is only one interior integer, `p+1` is automatically the leftmost
minimum-divisor integer. This makes the twin-prime gap the smallest possible
nonempty chamber where the selected-integer rule is visible without internal
competition.

The current research target is:

```text
Describe twin-prime recurrence as recurrence of the one-cell PGS chamber inside
the ordered sequence of prime-gap chamber types.
```

## Working Hypothesis

Twin-prime occurrences are predictable from gap structure because gap structure
predicts the local prime-gap chamber type. In this framing, a twin-prime
occurrence is not just the event `q-p=2`; it is the return of the chamber
sequence to the width-2 state, where the unique interior integer is forced to
be the selected minimizer.

The first testable form is:

```text
Neighboring PGS chamber types carry predictive information about returns to the
width-2 one-cell chamber.
```

The hypothesis is not yet a twin-prime theorem. It becomes a theorem target
only if the predictive channel can be stated without using the future endpoint
as an input.

## Current Measured Surface

The committed probe through right primes `q <= 1000000` found:

| Quantity | Value |
|---|---:|
| Twin-prime pairs | `8169` |
| Twin pairs with defined preceding gap type | `8168` |
| Distinct preceding gap types | `117` |
| Distinct following gap types | `88` |
| Distinct outer-pair signatures | `1312` |
| Same outer-family share | `0.3828354554358472` |

The leading outer-pair signature was:

| Preceding type | Following type | Count | Share |
|---|---|---:|---:|
| `o2_d4_a2_odd_semiprime` | `o4_d4_a4_odd_semiprime` | `315` | `0.03856513222331048` |

## Next Question

The next pass should not broaden into every twin-prime statistic. It should test
one exact explanation:

```text
Do the top outer-pair signatures form deterministic return channels to the
width-2 one-cell chamber, or are they only enriched neighborhood motifs?
```

The first useful output is a compact motif certificate:

- top outer-pair signatures;
- residue-conditioned baseline lift;
- exact preceding and following carrier families;
- gap-width distributions around the twin chamber;
- whether any motif deterministically forces a width-2 middle chamber.

The return-gate harness implements the no-future-endpoint version of this test.
For each current prime `q`, it uses only the two completed chambers behind `q`
and `q mod 30` as inputs. The label is whether the next chamber has width `2`.

The deterministic signature is:

```text
(previous_type_key, current_type_key, q mod 30, current_gap_width,
 current_carrier_family, current_peak_offset)
```

The measured quantities are:

```text
signature_count
twin_return_count
twin_return_rate
residue_baseline_rate
lift
train_lift
test_lift
```

A signature is promoted to a candidate return gate only when it clears support
and lift thresholds in both chronological splits.

## Stop Condition

The target is closed only in one of two forms:

```text
Closed bounded certificate:
Within the measured surface, the dominant twin-prime chamber returns are
accounted for by a small set of enriched outer-pair motifs.
```

or:

```text
Not closed:
The one-cell chamber recurs, but the outer-pair signatures do not reduce to a
small deterministic or enriched motif family on the measured surface.
```
