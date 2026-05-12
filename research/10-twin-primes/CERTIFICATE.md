# Width-2 Twin-Prime Chamber Certificate

## Abstract

This note gives a bounded computational certificate for the width-2 prime-gap
chamber. The current center of gravity is the sampled decade ladder from
`10^6` through `10^18`, where endpoint status remains audit-clean and the
exposed `10^18` obstruction layer recursively compresses under least-factor
peeling:

```text
154 -> 55 -> 9 -> 2
```

For each eligible prime `q`, the candidate chamber is:

```text
q | q+1 | q+2
```

The interior integer `q+1` is forced. The endpoint `q+2` either closes the
chamber as a prime endpoint or appears as a composite endpoint obstruction.

The measured result is:

```text
Twin-prime closures are the complement of a recursive least-factor obstruction
language on the composite endpoint side.
```

The `q <= 1000000` surface remains a closed base certificate where the
obstruction language closes by depth `3`. The decade ladder shows that the
grammar deepens with scale through a multi-prime carrier. The open theorem
target is to prove the recursive obstruction language symbolically.

## Scope Of Measurement

| Item | Scope |
|---|---|
| Tested rungs | `10^6, 10^7, ..., 10^18` |
| Decade sample | `4096` eligible anchors below each rung |
| Base certificate | exhaustive eligible anchors through `q <= 1000000` |
| Chamber | width-2 only: `q | q+1 | q+2` |
| Operator | deterministic least-factor peeling |
| Input contracts | strict focused probes |
| Audit status | `PASS` at every sampled rung and focused probe |
| Measurement boundary | tested ranges and width-2 chambers |

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

The least-factor peeling order is canonical for this certificate: it is the
deterministic left-to-right reading of a composite under its standard prime
factorization. This certificate fixes that order throughout.

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

Multi-prime material means the remaining factor material has at least three
distinct prime factors and remains available for another peel.

The recursive least-factor obstruction language is:

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

It is the carrier because it is the only family whose remainder is itself
forwarded as the input to another peel.

## Base Certificate Regime

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

## Base Certificate Statement

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

The `21257` endpoint obstructions are fully accounted for by the base
factor-strip grammar:

| Reduction layer | Count |
|---|---:|
| First strip reaches fixed-point or distinct-semiprime material | `19772` |
| Second strip reaches fixed-point or distinct-semiprime material | `1302` |
| Third strip reaches fixed-point or distinct-semiprime material | `169` |
| Remaining third-strip rows, all prime-power tails | `14` |
| Total endpoint obstructions accounted | `21257` |

Therefore, within the measured regime:

```text
Endpoint misses exit into fixed-point material, distinct-semiprime material,
or prime-power tail material by depth 3.
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
unaccounted rows: 0
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

These exact arithmetic identities keep the obstruction grammar auditable.

## Decade Ladder

A deterministic high-scale ladder sampled eligible anchor primes immediately
below each power of ten from `10^6` through `10^18`.

The sample size was:

```text
4096 eligible anchors per decade scale
13 decade scales
53248 total sampled anchors
```

This ladder is a deterministic sampled high-scale certificate surface.

The ladder recasts the result as a three-axis certificate surface:

```text
scale x strip depth x terminal family
```

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

The base depth-3 obstruction language carried most of the ladder and then
exposed the next structural layer. Its ladder coverage was:

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
The recursive obstruction language deepens into a high-scale multi-prime
carrier. This identifies the next symbolic target beyond the base certificate.
```

## Fourth-Strip Pressure At `10^18`

The next focused pressure test used exactly the `10^18` decade-window
next-layer rows exposed by the ladder, preserving the ladder surface and state
space.

The input surface was:

```text
scale: 10^18
input next-layer rows: 154
input terminal family: multi_prime_family
```

The fourth strip removes one more least prime factor from the third remainder
and classifies the fourth remainder.

The result was:

| Quantity | Count |
|---|---:|
| Input next-layer rows | `154` |
| Fourth strip reaches distinct-semiprime material | `98` |
| Fourth strip reaches prime-power tail material | `1` |
| Fourth strip accounted rows | `99` |
| Fifth-layer rows exposed | `55` |
| Fourth-strip compression rate | `0.6428571428571429` |
| Grammar disposition | `FIFTH_LAYER_FOUND` |

The fourth remainder family distribution was:

| Fourth remainder family | Count |
|---|---:|
| `semiprime_distinct` | `98` |
| `multi_prime_family` | `55` |
| `two_prime_power_family` | `1` |

Thus the fourth strip compresses the `10^18` next layer by:

```text
99 / 154 = 0.6428571428571429
```

and exposes a smaller fifth layer:

```text
55 fifth-layer rows, all multi_prime_family
```

The high-scale obstruction grammar now has this measured shape:

```text
The low-scale three-strip grammar exposes a high-scale multi-prime layer.
At 10^18, a fourth strip accounts for most of that layer and exposes a
smaller fifth-layer multi-prime surface.
```

## Fifth-Strip Pressure At `10^18`

The next focused pressure test used exactly the `55` fifth-layer rows exposed
by the fourth strip and preserved that fifth-layer surface as the input
contract.

The input surface was:

```text
scale: 10^18
input fifth-layer rows: 55
input fourth remainder family: multi_prime_family
```

The fifth strip removes one more least prime factor from the fourth remainder
and classifies the fifth remainder.

The result was:

| Quantity | Count |
|---|---:|
| Input fifth-layer rows | `55` |
| Fifth strip reaches distinct-semiprime material | `46` |
| Fifth strip reaches prime-power tail material | `0` |
| Fifth strip accounted rows | `46` |
| Sixth-layer rows exposed | `9` |
| Fifth-strip compression rate | `0.8363636363636363` |
| Grammar disposition | `SIXTH_LAYER_FOUND` |

The fifth remainder family distribution was:

| Fifth remainder family | Count |
|---|---:|
| `semiprime_distinct` | `46` |
| `multi_prime_family` | `9` |

Thus the fifth strip compresses the `10^18` fifth layer by:

```text
46 / 55 = 0.8363636363636363
```

and exposes a smaller sixth layer:

```text
9 sixth-layer rows, all multi_prime_family
```

The fourth and fifth strips together show the recursive carrier shape:

```text
The high-scale next layer remains carried by multi-prime material until another
strip removes enough factor load to expose distinct-semiprime material. The
surviving deeper layer remains multi-prime.
```

## Sixth-Layer Normal Form At `10^18`

The next pass inspected the `9` sixth-layer rows as a finite object before the
sixth-strip pressure test.

The input surface was:

```text
scale: 10^18
input sixth-layer rows: 9
input fifth remainder family: multi_prime_family
```

The normal-form pass records the full endpoint factor signature, the first five
least factors stripped from the endpoint, and the remaining factor material
after five strips.

The endpoint multiplicity distribution was:

| Total prime factors with multiplicity | Count |
|---:|---:|
| `8` | `7` |
| `9` | `1` |
| `10` | `1` |

The remaining material after five strips had divisor-count distribution:

| `tau` of fifth remainder | Count |
|---:|---:|
| `8` | `7` |
| `16` | `1` |
| `24` | `1` |

The sixth-layer normal-form distribution was:

| Sixth-layer normal form | Count |
|---|---:|
| `distinct_3_prime_product` | `7` |
| `distinct_4_prime_product` | `1` |
| `one_square_3_distinct_prime_product` | `1` |

Thus the nine-row sixth layer has a tight normal form:

```text
After five least-factor strips, 7 / 9 rows are distinct products of three
primes, 1 / 9 is a distinct product of four primes, and 1 / 9 is one square
times three distinct primes.
```

The measured normal-form disposition is:

```text
TIGHT_NORMAL_FORM
```

## Sixth-Strip Pressure At `10^18`

The next pressure test attacked only the `9` sixth-layer normal-form rows. It
used the existing fifth-remainder factor signatures and removed exactly one
least factor from each row.

The input surface was:

```text
scale: 10^18
input sixth-layer rows: 9
input normal-form surface: TIGHT_NORMAL_FORM
```

The result was:

| Quantity | Count |
|---|---:|
| Input sixth-layer rows | `9` |
| Sixth strip reaches distinct-semiprime material | `7` |
| Sixth strip reaches prime-power tail material | `0` |
| Sixth strip accounted rows | `7` |
| Seventh-layer rows exposed | `2` |
| Sixth-strip compression rate | `0.7777777777777778` |
| Grammar disposition | `SEVENTH_LAYER_FOUND` |

The sixth remainder family distribution was:

| Sixth remainder family | Count |
|---|---:|
| `semiprime_distinct` | `7` |
| `multi_prime_family` | `2` |

Thus the sixth strip compresses the nine-row normal-form surface by:

```text
7 / 9 = 0.7777777777777778
```

The `2` seventh-layer rows are exactly the two sixth-layer boundary forms:

| Sixth-layer normal form | Seventh-layer row count |
|---|---:|
| `distinct_4_prime_product` | `1` |
| `one_square_3_distinct_prime_product` | `1` |

The `10^18` chain now has this focused shape:

```text
154 next-layer rows
55 fifth-layer rows
9 sixth-layer normal-form rows
2 seventh-layer boundary rows
```

## What Is Measured And What Remains Open

Measured in this certificate:

```text
The width-2 endpoint status is audit-clean on the sampled 10^6 through 10^18
decade ladder, and the exposed 10^18 obstruction layer recursively compresses
from 154 rows to 2 rows under least-factor peeling.
```

The open symbolic target is:

```text
prove symbolically that the width-2 composite endpoint surface is governed by
the recursive least-factor obstruction language, with terminal exits and a
multi-prime carrier.
```

## Reproducibility

Run the focused tests:

```text
python3 -m pytest research/10-twin-primes/tests
```

Regenerate the certificate output:

```text
python3 research/10-twin-primes/scripts/twin_prime_endpoint_fixed_point_decomposition_probe.py --max-right-prime 1000000 --output-dir research/10-twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe
```

Check the generated summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe/summary.json")
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
python3 research/10-twin-primes/scripts/twin_prime_decade_ladder_probe.py --sample-size 4096 --min-exponent 6 --max-exponent 18 --output-dir research/10-twin-primes/output/twin_prime_decade_ladder_probe
```

Check the ladder summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_decade_ladder_probe/summary.json")
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

Run the focused `10^18` fourth-strip pressure test:

```text
python3 research/10-twin-primes/scripts/twin_prime_fourth_strip_pressure_probe.py --input research/10-twin-primes/output/twin_prime_decade_ladder_probe/next_layer_rows.csv --scale 1000000000000000000 --output-dir research/10-twin-primes/output/twin_prime_fourth_strip_pressure_probe
```

Check the fourth-strip summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_fourth_strip_pressure_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "scale",
    "input_next_layer_count",
    "fourth_strip_accounted_count",
    "fifth_layer_count",
    "fourth_strip_compression_rate",
    "grammar_disposition",
]:
    print(f"{key}: {summary[key]}")
PY
```

Expected values:

```text
scale: 1000000000000000000
input_next_layer_count: 154
fourth_strip_accounted_count: 99
fifth_layer_count: 55
fourth_strip_compression_rate: 0.6428571428571429
grammar_disposition: FIFTH_LAYER_FOUND
```

Run the focused `10^18` fifth-strip pressure test:

```text
python3 research/10-twin-primes/scripts/twin_prime_fifth_strip_pressure_probe.py --input research/10-twin-primes/output/twin_prime_fourth_strip_pressure_probe/fifth_layer_rows.csv --scale 1000000000000000000 --output-dir research/10-twin-primes/output/twin_prime_fifth_strip_pressure_probe
```

Check the fifth-strip summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_fifth_strip_pressure_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "scale",
    "input_fifth_layer_count",
    "fifth_strip_accounted_count",
    "sixth_layer_count",
    "fifth_strip_compression_rate",
    "grammar_disposition",
]:
    print(f"{key}: {summary[key]}")
PY
```

Expected values:

```text
scale: 1000000000000000000
input_fifth_layer_count: 55
fifth_strip_accounted_count: 46
sixth_layer_count: 9
fifth_strip_compression_rate: 0.8363636363636363
grammar_disposition: SIXTH_LAYER_FOUND
```

Run the focused `10^18` sixth-layer normal-form pass:

```text
python3 research/10-twin-primes/scripts/twin_prime_sixth_layer_normal_form_probe.py --input research/10-twin-primes/output/twin_prime_fifth_strip_pressure_probe/sixth_layer_rows.csv --scale 1000000000000000000 --output-dir research/10-twin-primes/output/twin_prime_sixth_layer_normal_form_probe
```

Check the sixth-layer normal-form summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_sixth_layer_normal_form_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "scale",
    "sixth_layer_count",
    "normal_form_disposition",
]:
    print(f"{key}: {summary[key]}")
print(summary["sixth_layer_normal_form_distribution"])
PY
```

Expected values:

```text
scale: 1000000000000000000
sixth_layer_count: 9
normal_form_disposition: TIGHT_NORMAL_FORM
```

Run the focused `10^18` sixth-strip pressure test:

```text
python3 research/10-twin-primes/scripts/twin_prime_sixth_strip_pressure_probe.py --input research/10-twin-primes/output/twin_prime_sixth_layer_normal_form_probe/sixth_layer_normal_form_rows.csv --scale 1000000000000000000 --output-dir research/10-twin-primes/output/twin_prime_sixth_strip_pressure_probe
```

Check the sixth-strip summary:

```text
python3 - <<'PY'
import json
from pathlib import Path

path = Path("research/10-twin-primes/output/twin_prime_sixth_strip_pressure_probe/summary.json")
summary = json.loads(path.read_text())
for key in [
    "scale",
    "input_sixth_layer_count",
    "sixth_strip_accounted_count",
    "seventh_layer_count",
    "sixth_strip_compression_rate",
    "grammar_disposition",
]:
    print(f"{key}: {summary[key]}")
PY
```

Expected values:

```text
scale: 1000000000000000000
input_sixth_layer_count: 9
sixth_strip_accounted_count: 7
seventh_layer_count: 2
sixth_strip_compression_rate: 0.7777777777777778
grammar_disposition: SEVENTH_LAYER_FOUND
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
| `output/twin_prime_fourth_strip_pressure_probe/summary.json` | Focused `10^18` fourth-strip summary. |
| `output/twin_prime_fourth_strip_pressure_probe/fourth_strip_rows.csv` | Classified `10^18` fourth-strip rows. |
| `output/twin_prime_fourth_strip_pressure_probe/fifth_layer_rows.csv` | The `55` fifth-layer rows. |
| `output/twin_prime_fifth_strip_pressure_probe/summary.json` | Focused `10^18` fifth-strip summary. |
| `output/twin_prime_fifth_strip_pressure_probe/fifth_strip_rows.csv` | Classified `10^18` fifth-strip rows. |
| `output/twin_prime_fifth_strip_pressure_probe/sixth_layer_rows.csv` | The `9` sixth-layer rows. |
| `output/twin_prime_sixth_layer_normal_form_probe/summary.json` | Focused `10^18` sixth-layer normal-form summary. |
| `output/twin_prime_sixth_layer_normal_form_probe/sixth_layer_normal_form_rows.csv` | The `9` classified sixth-layer rows. |
| `output/twin_prime_sixth_strip_pressure_probe/summary.json` | Focused `10^18` sixth-strip summary. |
| `output/twin_prime_sixth_strip_pressure_probe/sixth_strip_rows.csv` | Classified `10^18` sixth-strip rows. |
| `output/twin_prime_sixth_strip_pressure_probe/seventh_layer_rows.csv` | The `2` seventh-layer boundary rows. |

## Open Target

The current result is a bounded certificate.

The next theorem target is:

```text
Prove symbolically why low-scale width-2 endpoint misses reduce to fixed-point
material, distinct-semiprime material, or prime-power tail material, then
extend the grammar through the high-scale fourth-strip and fifth-layer
multi-prime surfaces. The next concrete object is the `9`-row sixth-layer
multi-prime surface at `10^18`, now compressed to the `2` seventh-layer
boundary rows above.
```

Only after that symbolic obstruction result is proved should the document be
promoted from certificate status to theorem status.
