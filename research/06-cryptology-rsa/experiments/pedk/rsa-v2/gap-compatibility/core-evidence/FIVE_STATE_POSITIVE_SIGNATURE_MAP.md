# Five-State Positive Signature Map

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It maps the positive side of the current strongest exclusion candidate. The
five public phase states exclude the all-`o6` factor-neighborhood signature in
the tested bands, but they also admit stable factor-neighborhood signatures.

## Object

The public object is:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The downstream factor-neighborhood object is:

```text
F(p,q) = unordered factor-neighborhood signature
```

The five public phase states are:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

## Experiment

Script:

```text
five_state_positive_signature_map.py
```

Inputs:

```text
output/five_state_all_o6_refinement_check/summary.json
output/five_state_all_o6_refinement_check/candidate_rule_rows.jsonl
```

Output:

```text
output/five_state_positive_signature_map/
```

Bands:

```text
601..1000
1001..1400
1401..1800
1801..2200
2201..2600
```

## Measured Result

The all-`o6` factor-neighborhood signature was not observed in the five public
phase states across the five bands:

```text
all_o6_observed_count = 0
```

Stable positive signatures were observed in every supported band:

```text
stable_positive_signature_count = 72
```

Counts by public phase state:

```text
o2_d4_odd|d<=4@late   stable_positive_signature_count = 13
o4_d4_odd|d<=4@early  stable_positive_signature_count = 14
o4_d4_odd|d<=4@late   stable_positive_signature_count = 9
o4_d4_odd|d<=4@mid    stable_positive_signature_count = 33
o6_d4_odd|d<=4@late   stable_positive_signature_count = 3
```

The largest repeated positive signatures occur in `o4_d4_odd|d<=4@mid`. The
top observed count is:

```text
S(N) = o4_d4_odd|d<=4@mid
F(p,q) =
L=o2_higher_divisor_odd|d<=4|R=o2_higher_divisor_odd|d<=4
||
L=o4_higher_divisor_odd|d<=4|R=o4_higher_divisor_odd|d<=4
total_observed_count = 71
```

## Interpretation

The five-state all-`o6` exclusion is not an absence-only artifact. The same
public phase states carry positive compatibility structure: they repeatedly
admit other factor-neighborhood signatures across all five tested bands.

The current map contains both sides:

```text
excluded:
  all-o6 factor-neighborhood signature

stable positive:
  72 state-signature pairs observed in every supported band
```

This is a stronger multiplication-map object than a bare exclusion list because
it records what is absent and what persists.

## Machine-Readable Artifacts

```text
output/five_state_positive_signature_map/summary.json
output/five_state_positive_signature_map/state_band_support_rows.jsonl
output/five_state_positive_signature_map/signature_count_rows.jsonl
output/five_state_positive_signature_map/stable_positive_signature_rows.jsonl
```

## Boundary

This is measured sidecar evidence. The positive signatures are downstream
labels from known `(N,p,q)` triples. They do not locate factors and do not make
PEDK inference live.

The unresolved target is a grammar-level explanation for why the all-`o6`
signature is excluded while the stable positive signatures remain compatible.
