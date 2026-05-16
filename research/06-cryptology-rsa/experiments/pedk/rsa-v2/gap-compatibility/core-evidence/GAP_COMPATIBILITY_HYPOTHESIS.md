# PEDK Gap Compatibility Hypothesis

## Status

This document records a research hypothesis for the Public Endpoint
Determinacy Kernel, abbreviated PEDK.

It is not a theorem. It is not a live inference rule. It is not an audit result.

The proved starting point is that prime gaps have structured PGS types and
grammar. The hypothesis below concerns a further relationship between the gap
that contains a public semiprime modulus and the gap structures around its
hidden factor endpoints.

## Concrete Objects

Let:

```text
N = p q
```

where `N` is public and `p`, `q` are the two prime factors used only for
downstream analysis and corpus construction.

There are three local PGS objects of interest:

```text
gap(N)
gap-neighborhood(p)
gap-neighborhood(q)
```

The first object is the prime gap whose interior contains the public integer
`N`.

The second and third objects are the local PGS structures surrounding the factor
endpoints `p` and `q`. They include the immediate adjacent prime gaps and may
also include the chamber-reset, carrier, tail, threat, and endpoint-chain
certificate fields computed around those factor-side neighborhoods.

Each object has a typed PGS description. At minimum, this description includes:

- gap endpoints;
- gap width;
- interior position of the selected integer or endpoint;
- divisor-count profile over the local interval;
- GWR carrier state;
- reset endpoint;
- lock position;
- tail and threat fields;
- reset signature;
- endpoint-chain role where applicable.

## Hypothesis

The PGS type of `gap(N)` constrains the possible PGS types of
`gap-neighborhood(p)` and `gap-neighborhood(q)`.

Equivalently:

```text
type(gap(N)) is not independent of
type(gap-neighborhood(p)) and type(gap-neighborhood(q)).
```

There exist compatibility and incompatibility relations between these typed
gap structures.

The target relation has the form:

```text
type(gap(N)) -> allowed factor-side gap types
type(gap(N)) -> excluded factor-side gap types
```

The strongest useful version is an exclusion law:

```text
Given the public PGS type of gap(N),
some factor-side gap types are incompatible and can be ruled out.
```

## PEDK Interpretation

PEDK is not trying to guess factors by ordinary candidate search.

PEDK asks whether public PGS structure around `N` determines, restricts, or
excludes public endpoint classes for the hidden factor locations.

Under this hypothesis, `gap(N)` carries information about where `p` and `q`
can be located in the endpoint-chain field. The information is not a direct
factor value. It is a structural compatibility constraint between typed gaps.

The desired PEDK mechanism is:

```text
public N
-> compute PGS type of gap(N)
-> compare against a compatibility corpus
-> exclude incompatible factor-side gap neighborhoods
-> reduce or resolve the public endpoint class state
```

Any rule promoted from this hypothesis must remain public-only at inference
time. It must not use `p`, `q`, product closure, divisibility, `gcd`, primality
APIs, or audit labels as a selection mechanism.

## Corpus Target

The empirical object needed to test the hypothesis is a database of known
triples:

```text
(N, p, q)
```

For each triple, the corpus should record the PGS type of:

```text
gap(N)
gap-neighborhood(p)
gap-neighborhood(q)
```

Small scales are the correct first regime because the full local structures are
cheap to compute, inspect, and compare. The corpus should begin where exact PGS
certificate fields, gap interiors, and endpoint-chain neighborhoods can be
computed without backend ambiguity.

The corpus is an analysis surface, not an inference input for the live solver.
It uses `p` and `q` only to label known factor-side structures while searching
for recurring compatibility and incompatibility patterns.

## Candidate Pattern Classes

The first compatibility searches should look for repeated relationships among:

- gap width classes of `gap(N)`, `gap-neighborhood(p)`, and
  `gap-neighborhood(q)`;
- reset signatures;
- carrier divisor classes;
- lock position as a fraction of local gap width;
- tail length and first-tail position;
- threat presence and threat offset;
- active, resolved, and unresolved certificate counts;
- transported carrier and first-tail alignment;
- endpoint-chain depth to the first closure candidate;
- orientation of the factor-side neighborhood relative to the square-root
  transport field.

The expected output of this work is not a single fitted threshold. The expected
output is a typed compatibility table with explicit exclusions.

## Rule Promotion Boundary

A pattern may become a candidate PEDK rule only if it satisfies all of the
following conditions:

1. It is stated entirely in public PGS terms.
2. It separates compatibility from downstream audit.
3. It has an explicit exclusion condition.
4. It preserves known factor-bearing rows.
5. It rejects known false endpoint-class rows or marks them unresolved.
6. It is tested on held-out triples not used to name the pattern.

Until those conditions are met, the pattern remains a hypothesis or measured
correlation.

## Current Research Boundary

The active measured boundary is:

```text
40-bit official rung: public endpoint class found, factor_found = true
50-bit official rung: unresolved_by_reciprocal_carrier_misalignment
64-bit official rung: public endpoint class found, factor_found = true
```

The 50-bit row is especially important. It shows that reciprocal closure alone
can produce a coherent but false endpoint class. That failure motivates the
gap-compatibility hypothesis: a stronger public grammar relation may distinguish
factor-bearing endpoint neighborhoods from structurally coherent but
incompatible neighborhoods.

## Summary Statement

PEDK rests on the hypothesis that semiprime factor location is partially encoded
in prime gap grammar. The gap containing `N` should constrain the possible gap
types around `p` and `q`. A compatibility corpus over known `(N, p, q)` triples
is the research instrument for discovering those constraints and separating
true public endpoint determinacy from false structural closure.
