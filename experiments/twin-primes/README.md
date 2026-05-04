# Twin-Prime Chamber Experiment

Twin primes are pairs of primes with exactly one integer between them.

For example:

```text
11 | 12 | 13
```

The middle integer is forced. There is no competition inside the gap, because
there is only one interior integer.

This experiment studies that shape as a one-cell prime-gap chamber:

```text
q | q+1 | q+2
```

The question is direct:

```text
Does q+2 close the one-cell chamber as a prime endpoint, or does it fail as a
structured composite obstruction?
```

## Headline Result

On the measured width-2 chamber surface through `q <= 1000000`, every failed
twin endpoint is accounted for by a three-part obstruction grammar.

The measured split is:

| Quantity | Count |
|---|---:|
| Eligible anchor primes `q` | `29424` |
| Prime closures `q+2` | `8167` |
| Composite endpoint failures `q+2` | `21257` |
| False exclusions | `0` |
| Unresolved composites | `0` |

The `21257` failed endpoints do not behave like featureless composite noise.
They reduce into this grammar:

```text
fixed-point material
distinct-semiprime material
prime-power tail material
```

The reduction is:

| Endpoint obstruction layer | Count |
|---|---:|
| First strip reaches fixed-point or distinct-semiprime material | `19772` |
| Second strip reaches fixed-point or distinct-semiprime material | `1302` |
| Third strip reaches fixed-point or distinct-semiprime material | `169` |
| Remaining third-strip rows, all prime-power tails | `14` |
| Total accounted endpoint failures | `21257` |

So inside this measured regime, failed one-cell chambers are fully accounted
for by endpoint factor structure.

## High-Scale Decade Ladder

A deterministic decade-window ladder sampled `4096` eligible anchors below
each scale from `10^6` through `10^18`.

The PGS decision audit stayed exact:

| Quantity | Count |
|---|---:|
| Sampled eligible anchors | `53248` |
| Prime closures | `7626` |
| Composite endpoint failures | `45622` |
| False exclusions | `0` |
| Unresolved composites | `0` |

The low-scale three-strip grammar carried most of the high-scale surface and
then exposed the next structural layer. It accounted for `44770 / 45622`
endpoint failures. The remaining `852` rows were all `multi_prime_family`
extension rows.

The focused fourth-strip pressure test on the `10^18` decade-window next-layer
rows compressed that layer again:

| Quantity | Count |
|---|---:|
| `10^18` next-layer rows tested | `154` |
| Fourth strip reaches distinct-semiprime material | `98` |
| Fourth strip reaches prime-power tail material | `1` |
| Fourth strip accounted rows | `99` |
| Fifth-layer rows exposed | `55` |
| Fourth-strip compression rate | `0.6428571428571429` |

The fifth strip then attacked only those `55` fifth-layer rows:

| Quantity | Count |
|---|---:|
| Fifth-layer rows tested | `55` |
| Fifth strip reaches distinct-semiprime material | `46` |
| Sixth-layer rows exposed | `9` |
| Fifth-strip compression rate | `0.8363636363636363` |

The sixth-layer normal-form pass inspected those `9` rows directly:

| Sixth-layer normal form | Count |
|---|---:|
| Distinct three-prime product after five strips | `7` |
| Distinct four-prime product after five strips | `1` |
| One square times three distinct primes after five strips | `1` |

That gives the current high-scale picture:

```text
PGS endpoint status remains audit-exact on the sampled decade ladder.
The obstruction grammar deepens by factor strips: the 10^18 next layer
compresses at strips four and five and exposes a nine-row sixth layer with a
tight normal form.
```

## The Story In Plain Language

A twin-prime gap has only one integer between the endpoints. That middle
integer is automatically the selected interior integer.

For an eligible prime `q`, the candidate chamber is:

```text
q | q+1 | q+2
```

If `q+2` is prime, the chamber closes as a twin-prime gap.

If `q+2` is composite, the chamber fails. The experiment asks what kind of
failure appears.

The answer is not a broad smear of unrelated composites. When the failed
endpoint is factored layer by layer, almost all failures immediately expose
prime or distinct-semiprime material. The few rows that survive three layers
are not random leftovers; all `14` are prime-power tails.

That is the current prime-gap-structure (PGS) finding:

```text
The one-cell chamber does not merely fail. It fails through a compact
endpoint-obstruction grammar.
```

## Technical Certificate

The technical document is:

```text
CERTIFICATE.md
```

It gives the definitions, measured regime, certificate statement, reduction
tables, verification commands, and open theorem target.

This experiment does not claim to settle the twin-prime conjecture. The current
claim is narrower and bounded:

```text
For eligible anchor primes q <= 1000000, every composite q+2 endpoint failure
in the width-2 chamber reduces to fixed-point material, distinct-semiprime
material, or prime-power tail material.
```

## Artifact Map

| Path | Role |
|---|---|
| `CERTIFICATE.md` | Self-contained technical certificate for the bounded result. |
| `docs/twin_prime_chamber_recurrence_target.md` | Working research log and next-target note. |
| `scripts/twin_prime_width2_pgs_generator_probe.py` | Width-2 chamber generator side probe with downstream audit. |
| `scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py` | Endpoint obstruction decomposition and factor-strip grammar probe. |
| `scripts/twin_prime_fourth_strip_pressure_probe.py` | Focused fourth-strip pressure probe for high-scale next-layer rows. |
| `scripts/twin_prime_fifth_strip_pressure_probe.py` | Focused fifth-strip pressure probe for the `10^18` fifth layer. |
| `scripts/twin_prime_sixth_layer_normal_form_probe.py` | Normal-form analyzer for the `10^18` sixth layer. |
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/summary.json` | Committed `q <= 1000000` endpoint obstruction summary. |
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_higher_rows.csv` | The `14` prime-power tail rows. |
| `output/twin_prime_decade_ladder_probe/summary.json` | `10^6` through `10^18` sampled ladder summary. |
| `output/twin_prime_decade_ladder_probe/next_layer_rows.csv` | High-scale multi-prime extension rows. |
| `output/twin_prime_fourth_strip_pressure_probe/summary.json` | Focused `10^18` fourth-strip summary. |
| `output/twin_prime_fourth_strip_pressure_probe/fifth_layer_rows.csv` | The `55` exposed fifth-layer rows. |
| `output/twin_prime_fifth_strip_pressure_probe/summary.json` | Focused `10^18` fifth-strip summary. |
| `output/twin_prime_fifth_strip_pressure_probe/sixth_layer_rows.csv` | The `9` exposed sixth-layer rows. |
| `output/twin_prime_sixth_layer_normal_form_probe/summary.json` | Focused `10^18` sixth-layer normal-form summary. |
| `output/twin_prime_sixth_layer_normal_form_probe/sixth_layer_normal_form_rows.csv` | The `9` classified sixth-layer rows. |

## Quick Commands

Run the focused tests:

```text
python3 -m pytest experiments/twin-primes/tests
```

Regenerate the endpoint obstruction certificate output:

```text
python3 experiments/twin-primes/scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py --max-right-prime 1000000 --output-dir experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe
```

Run the width-2 generator side probe:

```text
python3 experiments/twin-primes/scripts/twin_prime_width2_pgs_generator_probe.py --max-right-prime 1000000 --output-dir /tmp/twin_prime_width2_pgs_generator_probe_1e6
```

Run the high-scale decade ladder:

```text
python3 experiments/twin-primes/scripts/twin_prime_decade_ladder_probe.py --sample-size 4096 --min-exponent 6 --max-exponent 18 --output-dir experiments/twin-primes/output/twin_prime_decade_ladder_probe
```

Run the focused `10^18` fourth-strip pressure test:

```text
python3 experiments/twin-primes/scripts/twin_prime_fourth_strip_pressure_probe.py --input experiments/twin-primes/output/twin_prime_decade_ladder_probe/next_layer_rows.csv --scale 1000000000000000000 --output-dir experiments/twin-primes/output/twin_prime_fourth_strip_pressure_probe
```

Run the focused `10^18` fifth-strip pressure test:

```text
python3 experiments/twin-primes/scripts/twin_prime_fifth_strip_pressure_probe.py --input experiments/twin-primes/output/twin_prime_fourth_strip_pressure_probe/fifth_layer_rows.csv --scale 1000000000000000000 --output-dir experiments/twin-primes/output/twin_prime_fifth_strip_pressure_probe
```

Run the focused `10^18` sixth-layer normal-form pass:

```text
python3 experiments/twin-primes/scripts/twin_prime_sixth_layer_normal_form_probe.py --input experiments/twin-primes/output/twin_prime_fifth_strip_pressure_probe/sixth_layer_rows.csv --scale 1000000000000000000 --output-dir experiments/twin-primes/output/twin_prime_sixth_layer_normal_form_probe
```
