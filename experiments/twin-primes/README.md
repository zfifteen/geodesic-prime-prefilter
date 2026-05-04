# Twin-Prime Chamber Experiment

Twin primes are pairs of primes with exactly one integer between them.

For an eligible prime `q`, the candidate width-2 chamber is:

```text
q | q+1 | q+2
```

The single interior cell forces the middle integer `q+1`.

The endpoint `q+2` has only two possible roles:

```text
closure: q+2 is prime
obstruction: q+2 is composite
```

This experiment studies twin primes by classifying the obstruction side. The
current framing is:

```text
Twin primes are the complement of a recursive least-factor obstruction
language.
```

## Headline Result

On the deterministic decade-window ladder from `10^6` through `10^18`, the
width-2 endpoint decision stayed audit-clean, and the exposed high-scale
obstruction layer recursively compressed under the same least-factor peeling
language.

The ladder sampled `4096` eligible anchors below each decade scale:

| Quantity | Count |
|---|---:|
| Decade scales | `13` |
| Sampled eligible anchors | `53248` |
| Prime closures | `7626` |
| Composite endpoint obstructions | `45622` |
| False exclusions | `0` |
| Unresolved composites | `0` |
| Audit status | `PASS` |

The low-scale base grammar accounted for most high-scale obstructions:

| Quantity | Count |
|---|---:|
| Endpoint obstructions | `45622` |
| Accounted by the base grammar | `44770` |
| High-scale next-layer rows | `852` |

At `10^18`, the exposed next layer compressed as:

```text
154 -> 55 -> 9 -> 2
```

The focused `10^18` chain was:

| Stage | Count | Meaning |
|---|---:|---|
| Next layer | `154` | Multi-prime rows exposed by the decade ladder |
| Fifth layer | `55` | Rows surviving the fourth strip |
| Sixth layer | `9` | Rows surviving the fifth strip |
| Seventh-layer boundary | `2` | Boundary rows surviving the sixth strip |

The two surviving boundary rows are exactly:

```text
1 distinct four-prime product
1 one-square-plus-three-primes product
```

## Recursive Obstruction Language

The language is a deterministic peeling process:

```text
peel the least factor;
if the remainder is fixed-point material, exit;
if the remainder is distinct-semiprime material, exit;
if the remainder is prime-power tail material, exit;
if the remainder is multi-prime material, carry forward.
```

The terminal exits are:

```text
fixed-point material
distinct-semiprime material
prime-power tail material
```

The recursive carrier is:

```text
multi-prime material
```

It is the carrier because it is the only family whose remainder is carried
forward as another peelable input.

So the measured object has three axes:

```text
scale x strip depth x terminal family
```

The `q <= 1000000` result is the shallow base certificate. The decade ladder
adds scale. The focused `10^18` probes show deeper recursive compression.

## Base Certificate

Through eligible anchors `q <= 1000000`, the obstruction language closes by
depth `3`.

| Quantity | Count |
|---|---:|
| Eligible anchor primes `q` | `29424` |
| Prime closures `q+2` | `8167` |
| Composite endpoint obstructions `q+2` | `21257` |
| False exclusions | `0` |
| Unresolved composites | `0` |

The `21257` obstructions reduce as:

| Endpoint obstruction layer | Count |
|---|---:|
| First strip reaches fixed-point or distinct-semiprime material | `19772` |
| Second strip reaches fixed-point or distinct-semiprime material | `1302` |
| Third strip reaches fixed-point or distinct-semiprime material | `169` |
| Remaining third-strip rows, all prime-power tails | `14` |
| Total accounted endpoint obstructions | `21257` |

This base certificate remains closed as the low-scale shallow-depth instance of
the recursive language.

## Technical Certificate

The technical document is:

```text
CERTIFICATE.md
```

It gives the definitions, measured regimes, factor-strip tables, decade ladder,
focused `10^18` compression chain, verification commands, and open symbolic
target.

The current measured claim is bounded and multi-scale:

```text
On the sampled 10^6 through 10^18 decade ladder, endpoint status is audit-clean,
and the exposed 10^18 obstruction layer recursively compresses from 154 to 2
under the same least-factor peeling language.
```

## Artifact Map

| Path | Role |
|---|---|
| `CERTIFICATE.md` | Self-contained technical certificate. |
| `docs/twin_prime_chamber_recurrence_target.md` | Working research log and next-target note. |
| `scripts/twin_prime_width2_pgs_generator_probe.py` | Width-2 chamber generator side probe with downstream audit. |
| `scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py` | Base endpoint obstruction decomposition probe. |
| `scripts/twin_prime_decade_ladder_probe.py` | `10^6` through `10^18` sampled decade ladder. |
| `scripts/twin_prime_fourth_strip_pressure_probe.py` | Focused fourth-strip probe for high-scale next-layer rows. |
| `scripts/twin_prime_fifth_strip_pressure_probe.py` | Focused fifth-strip probe for the `10^18` fifth layer. |
| `scripts/twin_prime_sixth_layer_normal_form_probe.py` | Normal-form analyzer for the `10^18` sixth layer. |
| `scripts/twin_prime_sixth_strip_pressure_probe.py` | Focused sixth-strip probe for the `10^18` normal-form surface. |
| `output/twin_prime_decade_ladder_probe/summary.json` | Pooled sampled ladder summary. |
| `output/twin_prime_decade_ladder_probe/next_layer_rows.csv` | High-scale multi-prime extension rows. |
| `output/twin_prime_sixth_strip_pressure_probe/summary.json` | Focused `10^18` sixth-strip summary. |
| `output/twin_prime_sixth_strip_pressure_probe/seventh_layer_rows.csv` | The `2` exposed seventh-layer boundary rows. |

## Quick Commands

Run the focused tests:

```text
python3 -m pytest experiments/twin-primes/tests
```

Regenerate the base endpoint obstruction certificate output:

```text
python3 experiments/twin-primes/scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py --max-right-prime 1000000 --output-dir experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe
```

Run the high-scale decade ladder:

```text
python3 experiments/twin-primes/scripts/twin_prime_decade_ladder_probe.py --sample-size 4096 --min-exponent 6 --max-exponent 18 --output-dir experiments/twin-primes/output/twin_prime_decade_ladder_probe
```

Run the focused `10^18` sixth-strip pressure test:

```text
python3 experiments/twin-primes/scripts/twin_prime_sixth_strip_pressure_probe.py --input experiments/twin-primes/output/twin_prime_sixth_layer_normal_form_probe/sixth_layer_normal_form_rows.csv --scale 1000000000000000000 --output-dir experiments/twin-primes/output/twin_prime_sixth_strip_pressure_probe
```
