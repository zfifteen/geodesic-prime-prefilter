# Width-2 Twin-Prime Chamber Certificate

## Abstract

This note gives a bounded computational certificate for the width-2 prime-gap
chamber through eligible anchor primes `q <= 1000000`.

For each eligible prime `q`, the candidate chamber is:

```text
q | q+1 | q+2
```

The interior integer `q+1` is forced. The endpoint `q+2` either closes the
chamber as a prime endpoint or fails as a composite endpoint obstruction.

The measured result is:

```text
Every composite q+2 endpoint failure reduces to fixed-point material,
distinct-semiprime material, or prime-power tail material.
```

This is a bounded certificate for the measured regime. The open theorem target
is to prove symbolically that the same obstruction grammar persists beyond the
measured range.

## Definitions

An eligible anchor prime is a prime `q > 5` with:

```text
q mod 30 in {11, 17, 29}
```

These are exactly the residue classes in which `q+2` can also be prime.

The width-2 chamber anchored at `q` is:

```text
q | q+1 | q+2
```

The forced interior integer is:

```text
w = q+1
```

The endpoint is:

```text
e = q+2
```

The endpoint fixed-point locus is the divisor-count condition:

```text
tau(e) = 2
```

where `tau(n)` is the number of positive divisors of `n`. Thus `e` is on the
endpoint fixed-point locus exactly when `e` is prime.

An endpoint miss is a candidate endpoint with:

```text
tau(e) > 2
```

A factor strip removes the least prime factor from the current composite
material and classifies the remaining factor material.

Fixed-point material means the remaining factor material has divisor count
`2`, hence is prime.

Distinct-semiprime material means the remaining factor material has the form
`ab`, where `a` and `b` are distinct primes.

Prime-power tail material means the remaining factor material is one of:

```text
prime_square
prime_cube
prime_power
two_prime_power_family
```

## Measured Regime

The measured regime is:

```text
eligible anchor primes q <= 1000000
q mod 30 in {11, 17, 29}
candidate endpoint e = q+2
```

The endpoint decomposition probe found:

| Quantity | Count |
|---|---:|
| Eligible anchor primes | `29424` |
| Endpoint fixed-point closures | `8167` |
| Endpoint obstructions | `21257` |
| Status mismatches | `0` |
| Audit status | `PASS` |

The width-2 generator side probe found the same split downstream:

| Quantity | Count |
|---|---:|
| Excluded composite candidates | `21257` |
| Unresolved prime closures | `8167` |
| False exclusions | `0` |
| Unresolved composites | `0` |

## Certificate Statement

For every eligible anchor prime `q <= 1000000`, the candidate endpoint `q+2`
is classified as either:

```text
endpoint fixed-point closure
```

or:

```text
endpoint obstruction
```

The endpoint fixed-point closures are exactly the `8167` cases where
`tau(q+2) = 2`.

The `21257` endpoint obstructions are fully accounted for by the following
bounded factor-strip grammar:

| Reduction layer | Count |
|---|---:|
| First strip reaches fixed-point or distinct-semiprime material | `19772` |
| Second strip reaches fixed-point or distinct-semiprime material | `1302` |
| Third strip reaches fixed-point or distinct-semiprime material | `169` |
| Remaining third-strip rows, all prime-power tails | `14` |
| Total endpoint obstructions accounted | `21257` |

Therefore, within the measured regime:

```text
Endpoint misses reduce either to fixed-point material,
distinct-semiprime material, or prime-power tail material.
```

## Factor-Strip Reduction

The first strip removes the least prime factor of `q+2`.

The first-strip distribution is:

| First-strip family | Count |
|---|---:|
| Least factor times fixed-point material | `13308` |
| Least factor times distinct-semiprime material | `6464` |
| Least factor times higher material | `1485` |

Thus:

```text
19772 / 21257 = 0.9301406595474432
```

of endpoint obstructions reduce after one strip.

The second strip attacks only the `1485` higher-material rows.

The second-strip distribution is:

| Second-strip family | Count |
|---|---:|
| Second factor times distinct-semiprime material | `1239` |
| Second factor times fixed-point material | `63` |
| Second factor times higher material | `183` |

Thus:

```text
21074 / 21257 = 0.9913910702356861
```

of endpoint obstructions reduce after at most two strips.

The third strip attacks only the `183` rows still higher after the second
strip.

The third-strip distribution is:

| Third-strip family | Count |
|---|---:|
| Third factor times distinct-semiprime material | `108` |
| Third factor times fixed-point material | `61` |
| Third factor times higher material | `14` |

Thus:

```text
21243 / 21257 = 0.999341393423342
```

of endpoint obstructions reduce to fixed-point or distinct-semiprime material
after at most three strips.

The remaining `14` rows are all prime-power tails:

| Third remainder family | Count |
|---|---:|
| `prime_square` | `10` |
| `two_prime_power_family` | `2` |
| `prime_cube` | `1` |
| `prime_power` | `1` |

So the final measured accounting is:

```text
fixed-point material: accounted
distinct-semiprime material: accounted
prime-power tail material: accounted
unstructured residual rows: 0
```

## Residue Constraint

Every endpoint miss satisfies the exact wheel-residue product relation:

```text
candidate residue = least-factor residue * cofactor residue mod 30
```

The same relation persists under later strips:

```text
cofactor residue = second-factor residue * second-remainder residue mod 30
```

and, for rows that reach the third strip:

```text
second-remainder residue = third-factor residue * third-remainder residue mod 30
```

These are not statistical conditions. They are exact arithmetic identities
recorded to keep the obstruction grammar auditable.

## Decade Ladder

A deterministic high-scale ladder sampled eligible anchor primes immediately
below each power of ten from `10^6` through `10^18`.

The sample size was:

```text
4096 eligible anchors per decade scale
13 decade scales
53248 total sampled anchors
```

This ladder is not an exhaustive scan. It is a deterministic sampled
high-scale certificate surface.

The pooled ladder result was:

| Quantity | Count |
|---|---:|
| Sampled eligible anchors | `53248` |
| Endpoint fixed-point closures | `7626` |
| Endpoint obstructions | `45622` |
| Endpoint obstructions accounted by the low-scale grammar | `44770` |
| Next-layer rows exposed by the low-scale grammar | `852` |
| False exclusions | `0` |
| Unresolved composites | `0` |
| Audit status | `PASS` |
| Grammar disposition | `NEXT_LAYER_FOUND` |

The PGS endpoint decision remained audit-exact across the ladder:

```text
false exclusions: 0
unresolved composites: 0
```

The low-scale three-strip obstruction grammar carried most of the ladder and
then exposed the next structural layer. Its ladder coverage was:

```text
44770 / 45622 = 0.9813247994388672
```

All `852` next-layer rows had terminal family:

```text
multi_prime_family
```

The per-scale ladder summary was:

| Scale | Anchors | Closures | Obstructions | Accounted | Next layer | Coverage | Audit |
|---:|---:|---:|---:|---:|---:|---:|---|
| `10^6` | `4096` | `1064` | `3032` | `3032` | `0` | `1.0` | `PASS` |
| `10^7` | `4096` | `862` | `3234` | `3230` | `4` | `0.9987631416202845` | `PASS` |
| `10^8` | `4096` | `804` | `3292` | `3282` | `10` | `0.996962332928311` | `PASS` |
| `10^9` | `4096` | `718` | `3378` | `3365` | `13` | `0.9961515689757253` | `PASS` |
| `10^10` | `4096` | `609` | `3487` | `3468` | `19` | `0.9945511901347863` | `PASS` |
| `10^11` | `4096` | `559` | `3537` | `3495` | `42` | `0.9881255301102629` | `PASS` |
| `10^12` | `4096` | `537` | `3559` | `3508` | `51` | `0.9856701320595673` | `PASS` |
| `10^13` | `4096` | `501` | `3595` | `3517` | `78` | `0.9783031988873435` | `PASS` |
| `10^14` | `4096` | `425` | `3671` | `3575` | `96` | `0.9738490874421138` | `PASS` |
| `10^15` | `4096` | `427` | `3669` | `3558` | `111` | `0.9697465249386754` | `PASS` |
| `10^16` | `4096` | `415` | `3681` | `3555` | `126` | `0.9657701711491442` | `PASS` |
| `10^17` | `4096` | `376` | `3720` | `3572` | `148` | `0.9602150537634409` | `PASS` |
| `10^18` | `4096` | `329` | `3767` | `3613` | `154` | `0.9591186620653039` | `PASS` |

The decade ladder therefore separates two facts:

```text
The width-2 PGS endpoint status remains audit-exact on the sampled high-scale
surface.
```

and:

```text
The obstruction grammar deepens into a high-scale multi-prime layer. This is
the next symbolic target, not a defect in the low-scale certificate.
```

## Reproducibility

Run the focused tests:

```text
python3 -m pytest experiments/twin-primes/tests
```

Regenerate the certificate output:

```text
python3 experiments/twin-primes/scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py --max-right-prime 1000000 --output-dir experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe
```

Check the generated summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "eligible_anchor_count",
    "endpoint_fixed_point_count",
    "endpoint_obstruction_count",
    "low_complexity_cofactor_obstruction_count",
    "second_strip_low_complexity_remainder_count",
    "third_strip_low_complexity_remainder_count",
    "third_strip_higher_remainder_count",
    "third_strip_prime_power_tail_count",
    "audit_status",
]:
    print(f"{key}: {summary[key]}")
PY
```

Expected values:

```text
eligible_anchor_count: 29424
endpoint_fixed_point_count: 8167
endpoint_obstruction_count: 21257
low_complexity_cofactor_obstruction_count: 19772
second_strip_low_complexity_remainder_count: 1302
third_strip_low_complexity_remainder_count: 169
third_strip_higher_remainder_count: 14
third_strip_prime_power_tail_count: 14
audit_status: PASS
```

Run the high-scale decade ladder:

```text
python3 experiments/twin-primes/scripts/twin_prime_decade_ladder_probe.py --sample-size 4096 --min-exponent 6 --max-exponent 18 --output-dir experiments/twin-primes/output/twin_prime_decade_ladder_probe
```

Check the ladder summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("experiments/twin-primes/output/twin_prime_decade_ladder_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "scale_count",
    "eligible_anchor_count",
    "prime_closure_count",
    "endpoint_obstruction_count",
    "low_scale_grammar_accounted_obstruction_count",
    "next_layer_count",
    "false_exclusion_count",
    "unresolved_composite_count",
    "audit_status",
    "grammar_disposition",
]:
    print(f"{key}: {summary[key]}")
PY
```

Expected values:

```text
scale_count: 13
eligible_anchor_count: 53248
prime_closure_count: 7626
endpoint_obstruction_count: 45622
low_scale_grammar_accounted_obstruction_count: 44770
next_layer_count: 852
false_exclusion_count: 0
unresolved_composite_count: 0
audit_status: PASS
grammar_disposition: NEXT_LAYER_FOUND
```

## Artifact References

The committed certificate artifacts are:

| Path | Role |
|---|---|
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/summary.json` | Summary counts and grouped distributions. |
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/endpoint_decomposition_rows.csv` | Full endpoint decomposition rows. |
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_higher_rows.csv` | The `14` prime-power tail rows. |
| `output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_grammar_rows.csv` | Compact third-strip grouped grammar. |
| `output/twin_prime_decade_ladder_probe/summary.json` | Pooled high-scale ladder summary. |
| `output/twin_prime_decade_ladder_probe/scale_summary_rows.csv` | Per-decade ladder summary rows. |
| `output/twin_prime_decade_ladder_probe/next_layer_rows.csv` | High-scale multi-prime extension rows. |

## Open Target

The current result is a bounded certificate, not a general theorem.

The next theorem target is:

```text
Prove symbolically why low-scale width-2 endpoint misses reduce to fixed-point
material, distinct-semiprime material, or prime-power tail material, then
extend the grammar to the high-scale multi-prime layer.
```

Only after that symbolic obstruction result is proved should the document be
promoted from certificate status to proof status.
