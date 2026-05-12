# Square-Tail Infinite-Tail Completion Audit

## Objective

Find a deterministic infinite-tail proof for the remaining PGS tail structure
using PGS-native reduction, recursion, and elimination rather than
probabilistic or classical heuristic framing.

## Success Criteria

The active square-tail goal is complete only when the repo contains one of the
following:

1. A deterministic proof that every selected-square branch satisfies

   ```text
   r^2 - P(r^2) <= max(64, ceil(0.5 * log(r^2)^2)).
   ```

2. A deterministic finite reduction plus an exact finite verifier covering the
   reduced range.

3. A first explicit counterexample, with its exact obstruction certificate.

## Prompt-To-Artifact Checklist

| Requirement | Evidence | Status |
|---|---|---|
| Preserve the proved PGS theorem boundary | `PROOF.md`, `Square-Branch Reduction` | complete |
| Keep the square branch deterministic | `square_branch_blocker_acceptance.md` | complete |
| Define the obstruction word for a hypothetical counterexample | `square_tail_obstruction_word_target.md` and `square_tail_obstruction_word.py` | complete |
| Show pointwise child projection is not proof | `square_tail_recursive_projection_audit_424171123.md` | complete |
| Record the transitive projection graph | `square_tail_projection_graph_424171123.md` | complete |
| Convert prefix coverage into moving-cover arithmetic | `square_tail_cover_audit_424171123.md` | complete |
| Separate repeat-capable carriers from singleton carriers | `square_tail_carrier_economy_424171123.md` | complete |
| Isolate the exact M-rough defect theorem | `square_tail_rough_defect_audit_424171123.md` | complete |
| Test rough-defect recursive descent | `square_tail_rough_descent_audit_424171123.md` | complete |
| Identify the missing rough-descent edge semantics | `square_tail_edge_semantics_blocker.md` | complete |
| Exclude pure residue-cover contradiction as sufficient | `square_tail_rough_cover_model_blocker.md` | complete |
| Exclude root-primality and selected-square constraints alone | `square_tail_rough_cover_model_blocker.md` | complete |
| Classify the dynamic tail after the source CRT cover | `square_tail_dynamic_tail_audit_509.md` | complete |
| Project dynamic-tail rough composites to child squares | `square_tail_dynamic_tail_descent_audit_509.md` | complete |
| Exclude full-cutoff congruence-only contradiction | `square_tail_full_cutoff_crt_model_509.md` | complete |
| Separate artificial singleton carriers from actual least factors | `square_tail_model_actual_carrier_compare_509.md` | complete |
| Expose ordered first-arrival carrier frontier | `square_tail_carrier_arrival_frontier_509.md` | complete |
| Separate bounded carrier scans from square-root no-arrival proof | `square_tail_arrival_boundary_gap_509.md` | complete |
| Prove a prime-valued M-rough defect must occur before the cutoff | No proof artifact exists. | missing |
| Produce a counterexample | No counterexample artifact exists. | missing |

## Current Exact Reduction

For a prime root `r`, set

```text
S = r^2
C = max(64, ceil(0.5 * log(S)^2))
M = floor(C / 2).
```

The repeat-capable carriers are the primes

```text
3 <= ell <= M.
```

Each such `ell` covers the positions

```text
r^2 == 2m mod ell.
```

After every repeat-capable carrier is applied, the uncovered positions are
exactly the M-rough defects:

```text
r^2 - 2m has no prime factor <= M.
```

A complete square-tail counterexample is equivalent to:

```text
Every M-rough defect value r^2 - 2m is composite with least factor > M.
```

Therefore the square-tail theorem is equivalent to:

```text
Every selected-square root has at least one prime-valued M-rough defect before
the cutoff.
```

## Current Record

For the standing record

```text
r = 424,171,123
```

the rough-defect audit records:

| Quantity | Value |
|---|---:|
| `M` | `395` |
| Repeat-capable prime carriers | `76` |
| Positions covered by repeat-capable carriers | `330 / 395` |
| M-rough defects | `65` |
| Prime-valued M-rough defects | `3` |
| Prime-valued defect offsets | `738, 756, 758` |
| Composite M-rough defects | `62` |
| Minimum least factor among rough composites | `419` |

The first prime-valued rough defect is the actual preceding prime:

```text
P(r^2) = r^2 - 738.
```

## Second-Opinion State

Grok accepted the M-rough equivalence:

```text
complete obstruction word
<=> every M-rough defect is composite with least factor > M
<=> no prime-valued M-rough defect occurs before the cutoff.
```

Grok also stated that the selected-square predicate does not currently add a
usable deterministic constraint on the M-rough defect set beyond branch
selection.

## Unresolved Lemma

The live missing lemma is:

```text
For every selected-square root r, the M-rough defect set contains at least one
prime-valued member.
```

Equivalently:

```text
No selected-square root can have all M-rough defects composite with least
factor greater than M.
```

This lemma is not proved by the current artifacts.

## Invalid Completion Signals

The following are useful evidence but do not complete the goal:

- finite square-envelope scans;
- the standing record closing below the cutoff;
- child projection closure;
- transitive projection graph descent;
- prefix factor coverage;
- rough-defect equivalence itself;
- closed rough-defect child audits without an edge-semantics theorem;
- rough-descent measurements without a transport law;
- local CRT rough-cover consistency models;
- prime representatives of local CRT classes that close after the modeled window;
- dynamic-tail classifications that restate the remaining rough-prime target;
- dynamic-tail descent audits without a parent-to-child transport law;
- full-cutoff CRT obstruction models without an ordered PGS condition;
- artificial singleton-carrier models that do not encode actual least factors;
- bounded first-arrival frontiers that do not prove no later carrier exists;
- square-root boundary comparisons that restate the no-arrival target;
- Grok agreement with the equivalence.

## Next Valid Work

The next theorem-bearing step must attack the unresolved lemma directly:

```text
prime-valued M-rough defect existence on selected-square roots.
```

Valid routes:

1. A deterministic exclusion showing that all M-rough defects cannot be
   composite with least factor greater than `M`.
2. A rough-defect transport law connecting closed child roots to parent
   elimination.
3. A finite reduction that leaves only a checked finite root range.
4. A counterexample certificate.

Until one of these exists, the active goal is not complete.
