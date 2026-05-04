# Twin-Prime Chamber Recurrence Target

Twin-prime gaps are the one-cell chambers of prime-gap structure.

For a twin-prime pair `p, p+2`, the only interior integer is `p+1`. Because
there is only one interior integer, `p+1` is automatically the leftmost
minimum-divisor integer. This makes the twin-prime gap the smallest possible
nonempty chamber where the selected-integer rule is visible without internal
competition.

The current research target is:

```text
Describe twin-prime occurrence as closure or failure of the one-cell candidate
chamber q | q+1 | q+2.
```

## Working Hypothesis

Twin-prime occurrences are predictable from gap structure because gap structure
predicts the local prime-gap chamber type. In this framing, a twin-prime
occurrence is not just the event `q-p=2`; it is the return of the chamber
sequence to the width-2 state, where the unique interior integer is forced to
be the selected minimizer.

The first PGS-native testable form is:

```text
Composite failures of the one-cell chamber collapse into a compact obstruction
grammar involving tau(q+1), tau(q+2), q mod 30, and continued-chamber
no-later-simpler pressure.
```

The PGSPG-style variant is narrower and more algorithmic:

```text
Specialize the chamber-reset contract to the width-2 chamber. For each eligible
prime q, emit only whether q+2 is excluded by the width-2 PGS contract or
remains unresolved.
```

The earlier transition-signature path asked whether completed chamber history
predicts the next width-2 chamber. That path did not clear the fail-fast signal
rule at `q <= 1000000`; it is retained as a negative sanity check, not as the
active research direction.

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

## One-Cell Closure Result

The one-cell closure probe measures only eligible anchors:

```text
q mod 30 in {11,17,29}
```

For each eligible prime `q`, the candidate chamber is:

```text
q | q+1 | q+2
```

The selected integer is forced:

```text
w = q+1
```

The probe through `q <= 10000000` found:

| Quantity | Value |
|---|---:|
| Eligible anchors | `249230` |
| Prime closures | `58978` |
| Composite obstructions | `190252` |
| Closure rate | `0.23664085382979577` |
| Composite obstructions with later `<= tau(w)` pressure | `189167` |
| Later-pressure rate among composite obstructions | `0.9942970376132708` |

The dominant endpoint obstruction counts were:

| `tau(q+2)` | Composite obstruction count |
|---:|---:|
| `4` | `106819` |
| `8` | `59152` |
| `16` | `11184` |
| `12` | `5688` |
| `6` | `5153` |

The dominant first later `<= tau(w)` pressure offsets were:

| Offset from `q` | Count |
|---:|---:|
| `3` | `146351` |
| `4` | `28963` |
| `5` | `10845` |
| `6` | `2851` |
| `8` | `127` |

## Width-2 PGS Generator Side Probe

The generator side probe uses the same chamber-reset contract shape as the
Minimal PGS Generator, but fixes the chamber bound at `2`. Generation emits no
audit fields:

```json
{"q": 47, "candidate": 49, "status": "excluded"}
```

or:

```json
{"q": 41, "candidate": 43, "status": "unresolved"}
```

Audit is downstream. Through `q <= 1000000`, the audit result was:

| Quantity | Value |
|---|---:|
| Eligible anchors | `29424` |
| Excluded candidates | `21257` |
| Unresolved candidates | `8167` |
| Prime closures | `8167` |
| Composite obstructions | `21257` |
| False exclusions | `0` |
| Unresolved composites | `0` |
| Composite exclusion coverage | `1.0` |

This is an exact bounded closure certificate for the width-2 chamber under the
PGS chamber-reset rule. It is not a pre-endpoint historical predictor; it is the
PGSPG contract specialized to the one-cell candidate chamber.

## Decision-Knob Ablation

The first fine-tuning pass decomposed the width-2 side probe into four decision
knobs:

```text
pgs_width2_full
endpoint_fixed_point
endpoint_below_forced_load
forced_interior_carrier
```

Through `q <= 1000000`, the result was:

| Knob | Excluded | Unresolved | False exclusions | Unresolved composites | Status |
|---|---:|---:|---:|---:|---|
| `pgs_width2_full` | `21257` | `8167` | `0` | `0` | `PASS` |
| `endpoint_fixed_point` | `21257` | `8167` | `0` | `0` | `PASS` |
| `endpoint_below_forced_load` | `773` | `28651` | `0` | `20484` | `FAIL` |
| `forced_interior_carrier` | `29424` | `0` | `8167` | `0` | `FAIL` |

The endpoint fixed-point knob reproduces the full width-2 contract exactly on
the measured surface. The forced interior carrier is universal but not
discriminating: using it alone falsely excludes every prime closure. Comparing
the endpoint load against the forced interior load is also too weak: it leaves
most composite endpoints unresolved.

## Next Question

The next pass should not broaden into every twin-prime statistic. It should use
the width-2 generator side probe as the algorithmic skeleton and test one exact
explanation:

```text
Can the width-2 chamber-reset exclusion be rewritten as a symbolic obstruction
grammar for q+2, with no false exclusions and without leaning on broad
transition statistics?
```

The live fine-tuning target is therefore not outer gap type and not forced
carrier load. It is the symbolic decomposition of the endpoint fixed-point
condition inside the one-cell chamber. The first useful output is a compact
obstruction certificate:

```text
q mod 30
tau(q+1)
factor family of q+1
tau(q+2)
factor family of q+2
first later offset with tau <= tau(q+1)
```

## Stop Condition

The target is closed only in one of two forms:

```text
Closed bounded certificate:
Within the measured surface, failed one-cell chambers are accounted for by a
small endpoint-obstruction and continued-pressure grammar.
```

or:

```text
Not closed:
Failed one-cell chambers do not reduce to endpoint-obstruction or
continued-pressure families on the measured surface.
```
