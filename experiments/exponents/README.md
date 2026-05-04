# PGS Exponent-Tail Probe

Prime powers are the first place where exponents enter the recursive PGS
obstruction language directly.

The width-2 twin-prime chamber already exposes prime-power tail material:

```text
q | q+1 | q+2
```

When `q+2` is composite, least-factor peeling either exits into fixed-point
material, exits into distinct-semiprime material, or carries forward through
multi-prime material. Sometimes the peel reaches prime-power tail material.
That tail has an exponent pattern.

The toy question is:

```text
Do exposed prime-power exponents cluster by strip depth, residue path, scale,
or chamber state?
```

## Current Hypothesis

```text
Prime-power tails are strip-depth clocks in the recursive PGS obstruction
language.
```

In plain terms: the exponent may remember how long the endpoint obstruction
kept shedding least factors before repeated-prime structure was exposed.

## Input Surface

This experiment reads existing twin-primes obstruction artifacts. It does not
rerun the twin-primes scans.

The current inputs are:

```text
experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_higher_rows.csv
experiments/twin-primes/output/twin_prime_fourth_strip_pressure_probe/fourth_strip_rows.csv
experiments/twin-primes/output/twin_prime_fifth_strip_pressure_probe/fifth_strip_rows.csv
experiments/twin-primes/output/twin_prime_sixth_strip_pressure_probe/sixth_strip_rows.csv
```

## Outputs

```text
experiments/exponents/output/pgs_exponent_tail_probe/summary.json
experiments/exponents/output/pgs_exponent_tail_probe/exponent_tail_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/dominant_residue_path_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/high_exponent_tail_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/depth_exponent_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/residue_exponent_rows.csv
```

## First Signal To Chase

The initial run found a dominant peeled residue path:

```text
7->7->7
```

Measured on the current surface:

```text
total exponent-tail rows: 15
7->7->7 rows: 7
high-exponent tails: 2
high-exponent tails on 7->7->7: 2
```

This path carries the largest square-tail cell and every exposed tail with
exponent greater than `2` in the current surface.

## Run

```text
python3 experiments/exponents/scripts/pgs_exponent_tail_probe.py \
  --output-dir experiments/exponents/output/pgs_exponent_tail_probe
```

## Interpret

If the same exponent patterns concentrate at specific strip depths and residue
paths, the exponent-tail surface is structured.

If exponent patterns spread broadly across depths and residue paths, this toy
width-2 surface is a weak place to look for exponent structure.
