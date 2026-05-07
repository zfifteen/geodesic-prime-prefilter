# Solved RSA Challenge Evidence

## Purpose

This note records the first solved RSA Factoring Challenge label tranche for
PGS gap-grammar evidence gathering.

The evidence target is:

```text
public N grammar
-> downstream known p/q grammar labels
-> chamber-orientation compatibility
-> elimination rules for impossible factor-side chambers
```

The labels are not solver inputs. They are downstream evidence labels used to
test whether the public chamber grammar around `N` constrains admissible chamber
grammar around the known factors.

## First Tranche

Local label artifact:

```text
experiments/rsa/v2/fixtures/solved_rsa_challenge_cases.jsonl
```

Rows:

```text
RSA-100
RSA-110
RSA-120
RSA-129
RSA-130
RSA-140
RSA-150
```

Range:

```text
cases: 7
bits: 330..496
decimal digits: 100..150
```

Source:

```text
Wikipedia, "RSA numbers"
https://en.wikipedia.org/wiki/RSA_numbers
```

The local rows preserve known public challenge labels:

```text
case_id
decimal_digits
bits
N
p
q
source
source_lines
status
```

## First Exact Challenge Surface

The first solved challenge measurement is RSA-100:

```text
case_id: rsa_100
bits: 330
public rows: 3
target rows: 4
target exact-closed rows: 4
```

Local artifact:

```text
experiments/rsa/v2/output/rsa_challenge_exact_grammar/
```

The target-side factor grammar closed exactly:

```text
p_left:  o2_d4_a6_d4_odd
p_right: o2_d4_a35_d4_even
q_left:  o2_d4_a2_d4_odd
q_right: o2_d4_a8_d4_odd
```

The public `N` neighborhood produced one exact-closed adjacent chamber and two
explicit unresolved chambers:

```text
n_previous:   exact_closed, o4_d4_a34_d4_odd
n_containing: unresolved_prior_carrier, candidate o4_d4_a194_d4_odd
n_following:  unresolved_prior_carrier, candidate o4_d4_a44_d4_odd
```

The unresolved public rows are not substitute rows. They identify exact interior
offsets that still require closure before the chamber grammar can be used as a
resolved public invariant.

Reason:

```text
requires_gwr_nlsc_prior_carrier_elimination
```

The open public offsets are prior carrier candidates under the leftmost
minimum-divisor rule. The next pass must eliminate them by GWR/NLSC chamber law
before the later candidate can be treated as resolved public grammar.

## Integrity Check

The label file was checked for basic fixture integrity:

```text
p < q
p*q == N
decimal digit count matches label
bit length matches label
LF line endings
```

The product check is a fixture-integrity check only. It is not a PGS inference
mechanism and must not enter the decomposer.

## Next Evidence To Extract

For each solved RSA challenge row, extract public grammar first:

```text
N previous gap
N containing gap
N following gap
N lag-2 previous gap
N lag-2 following gap
```

Then attach downstream known factor labels:

```text
p left gap
p right gap
q left gap
q right gap
```

Required derived labels:

```text
outward higher-divisor intrusion count
inward higher-divisor intrusion count
Outward Intrusion Index
inward intrusion with public reset rhythm
inward intrusion without public reset rhythm
factor proximity rank
```

## Contract

Do not use solved RSA factors as inference.

Do not use divisibility, product closure, `gcd`, primality APIs, factor APIs,
random search, or classical candidate testing to resolve chambers.

Use the labels only after public PGS grammar is computed, as downstream evidence
for testing chamber-compatibility hypotheses.
