# Square-Tail Global Obstruction-Collapse Target

## Status

Proof target. Not proved.

## Object

Let `r` be a selected-square prime root and set

```text
S = r^2
C = max(64, ceil(0.5 * log(S)^2))
M = floor(C / 2).
```

For each

```text
1 <= m <= M
```

consider the odd row

```text
x_m = r^2 - 2m.
```

The repeat-capable carriers are the primes

```text
3 <= ell <= M.
```

After all repeat-capable carriers are applied, the remaining positions are the
M-rough defects:

```text
R(r) = {m <= M : x_m has no prime factor <= M}.
```

The complete obstruction predicate is

```text
O(r): every x_m with m in R(r) is composite.
```

Equivalently:

```text
O(r): no prime-valued M-rough defect occurs before the cutoff.
```

For each composite M-rough defect, define its least-factor child root:

```text
ell_m = least prime factor of x_m.
```

Since `m in R(r)`, every such child satisfies

```text
ell_m > M.
```

Since `x_m < r^2`, every such child also satisfies

```text
ell_m < r.
```

Thus a complete obstruction word creates a finite set of strictly smaller
prime child roots:

```text
Child(r) = {ell_m : m in R(r)}.
```

## Target Theorem

The global obstruction-collapse theorem is:

```text
If r is a selected-square root and O(r) holds, then there exists
ell in Child(r) such that ell is a selected-square root and O(ell) holds.
```

This is the exact infinite-descent target.

If the theorem is proved, the square-tail branch closes immediately. Suppose a
selected-square root with a complete obstruction exists, and choose the
smallest such root. The collapse theorem produces a smaller selected-square
root with a complete obstruction, contradicting minimality.

Therefore no selected-square root carries a complete obstruction, and every
selected-square root has at least one prime-valued M-rough defect before the
dynamic cutoff.

This target contains two proof obligations:

```text
O(r) on a selected-square parent
-> at least one selected-square child ell in Child(r).
```

and

```text
O(r) on a selected-square parent
-> at least one such child also satisfies O(ell).
```

The first obligation is child-state inheritance. The second is obstruction
inheritance. Both are unresolved.

## Equivalent Contrapositive

The theorem can also be attacked in contrapositive form:

```text
If every selected-square child in Child(r) is closed, then O(r) is impossible.
```

This form must not be weakened to a pointwise child-to-parent claim. The
direct pointwise routes have already failed.

The required statement is global:

```text
complete parent obstruction
+ closed selected-square child surfaces
-> parent obstruction contradiction.
```

## What This Is Not

This target is not the measured fact that observed composite children are
closed. The standing record is closed at the parent, so it cannot prove an
obstruction-collapse implication.

This target is not child selected-square inheritance. That property appears in
actual descent and in the local CRT singleton-carrier model.

This target is not direct back-cover by child closing primes. On the measured
surfaces, child closing primes do not land inside the parent cutoff window.

This target is not a local CRT contradiction. Full-cutoff local CRT obstruction
models exist.

## Required Proof Shape

A proof must establish one of the following deterministic statements.

### Collapse Form

```text
O(r)
-> at least one selected-square child ell_m also satisfies O(ell_m).
```

Together with strict descent `ell_m < r`, this gives a contradiction by
minimal counterexample.

### Closed-Child Incompatibility Form

```text
O(r)
+ every selected-square child ell_m is closed
-> contradiction inside the parent obstruction word.
```

This form must use the whole obstruction word or a global cover invariant. A
single child closing prime returning to the parent is not enough.

### Direct Exclusion Form

```text
O(r) is impossible for every selected-square root r.
```

This bypasses child descent, but must still operate on M-rough defects and not
on prime-density language.

### Selection-Free Strengthening

A stronger route avoids child selected-square inheritance:

```text
For every prime root r in the positive-row regime, O(r) implies that some
ell in Child(r) also satisfies O(ell).
```

This statement descends on prime roots rather than selected-square roots. If
proved with an exact finite base for the small positive-row boundary, it also
closes the selected-square branch.

## Acceptance Criteria

A proposed proof completes this target only if it provides:

1. A universal argument for all selected-square roots.
2. A deterministic mechanism using the obstruction word, M-rough defects, or a
   well-defined global cascade invariant.
3. A strict descent step or a direct contradiction.
4. No reliance on probabilistic prime density, PNT heuristics, or finite
   measured surfaces as theorem substitutes.
5. A clear separation between theorem proof, measured evidence, invalidated
   routes, and unresolved state.

## Current Boundary

The target remains open.

Grok response `52f17e75-b4a3-96e9-806a-750f7e8580ef` agreed that the target is
non-circular and would close the square-tail branch by infinite descent. It
also identified child-state inheritance as an auxiliary lemma if the descent
stays inside the selected-square branch.

The already-invalidated local routes are recorded in:

```text
research/04-bounded-compression/docs/square_tail_edge_semantics_blocker.md
research/04-bounded-compression/docs/findings/square_tail_child_selected_square_inheritance_audit.md
research/04-bounded-compression/docs/findings/square_tail_child_closure_parent_residue_audit.md
research/04-bounded-compression/docs/findings/square_tail_crt_model_arrival_order_audit_509.md
research/04-bounded-compression/docs/findings/square_tail_full_cutoff_crt_model_509.md
```
