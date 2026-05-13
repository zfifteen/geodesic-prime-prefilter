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
Equivalently, a child prime-valued rough row cannot be treated as an induced
smaller factor of a parent row without proving a new global mechanism.

This target is not a local CRT contradiction. Full-cutoff local CRT obstruction
models exist.

This target is not carrier inheritance in a local CRT model. The full-cutoff
local CRT model has a complete local parent carrier cover, `569` assigned
singleton carriers, and `569` distinct first-arrival carriers. All assigned
carriers and all first-arrival carriers are closed. Therefore the obstruction
inheritance theorem must use actual prime-root/global PGS structure, not local
congruence consistency or local first-arrival ordering alone.

The rough-factor disjointness lemma gives the first universal least-factor
constraint on a complete obstruction word: every prime factor above `M` is
private to one row in the parent M-window. The direct impossibility proof must
use that row-private factorization structure or a stronger invariant.

The lemma is recorded in:

```text
research/04-bounded-compression/docs/square_tail_rough_factor_disjointness_lemma.md
```

The near-root factor lemma gives the corresponding cofactor geometry in the
infinite tail. When `2M < r`, every M-rough composite row has a private
factorization straddling the root:

```text
r^2 - 2m = (r - h_m)(r + t_m)
```

with `t_m >= h_m` and

```text
2m = h_m^2 - (t_m - h_m)(r - h_m).
```

The lemma is recorded in:

```text
research/04-bounded-compression/docs/square_tail_near_root_factor_lemma.md
```

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

The positive-row regime means:

```text
r^2 - 2M > 1.
```

With the current cutoff definition, every odd prime root `r >= 11` is in this
regime. The roots `3`, `5`, and `7` are finite-base cases outside this
selection-free descent target.

For `r >= 11`, the fixed floor `C = 64` gives `r^2 - 2M >= 121 - 64 > 1`.
Once the logarithmic cutoff exceeds `64`,

```text
2M <= C <= 2 log(r)^2 + 1 < r^2 - 1,
```

where the final inequality holds at the first logarithmic-cutoff prime root
`293` and then widens with `r`. Thus the positive-row inequality remains true.

This strengthening removes the child-state inheritance obligation. It requires
only obstruction inheritance:

```text
O(r)
-> some least-factor child ell in Child(r) satisfies O(ell).
```

Since every child satisfies `ell < r`, this gives a well-founded descent on
prime roots directly.

## Child-State Boundary

Child-state inheritance should not be treated as automatic. For a prime child
root `ell`, selected-square status says:

```text
s_ell^2 < P(ell^2) < ell^2,
```

where `s_ell` is the previous prime root before `ell`. This is a prime between
consecutive prime-root squares. It is an additional square-gap statement, not a
consequence of the local parent congruence

```text
r^2 == 2m mod ell.
```

The selection-free strengthening avoids this extra obligation.

## Finite Base For Selection-Free Descent

The selected-square roots outside the positive-row regime are exactly:

| Root `r` | `r^2` | `P(r^2)` | Offset `r^2 - P(r^2)` | Cutoff `C` | Closed |
|---:|---:|---:|---:|---:|---:|
| `3` | `9` | `7` | `2` | `64` | yes |
| `5` | `25` | `23` | `2` | `64` | yes |
| `7` | `49` | `47` | `2` | `64` | yes |

Thus the selection-free descent target only needs to operate on prime roots
`r >= 11`. If the strengthening is proved there, the roots below `11` are
already closed by direct arithmetic.

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

Grok response `f0953ef5-1ed9-990d-a52a-4f9bd098aad5` agreed that the
selection-free strengthening is cleaner and sufficient: descent on all
positive-row prime roots avoids the selected-square child-state obligation,
with `3`, `5`, and `7` handled by the finite base above.

Grok response `7088e0c9-85bf-8d4f-0368-b051b1c099b0` proposed using child
prime-valued rough rows to force a smaller parent factor. That route is not
adopted here because it reduces to direct child-prime back-cover, already
invalidated by the parent-residue audit. The response also assumed one
prime-valued rough defect per child; the standing-record descent artifact has
`62` children with prime-valued rough-defect counts ranging from `3` to `21`.

Grok response `cad9c1e1-0889-9eeb-8b74-feb21382ecd7` agreed that the local CRT
model rules out assigned-carrier obstruction inheritance. The artifact now also
records the stronger first-arrival-carrier boundary. The result does not refute
the actual-prime-root theorem because the CRT model root is not an actual
prime-root theorem instance. It shows that the next proof must use global PGS
structure absent from the local CRT construction, or prove direct impossibility
of `O(r)` for positive-row prime roots.

Grok response `338a5565-ff4d-9be1-9d2d-75727e0fc1ca` agreed with the corrected
first-arrival boundary. The next theorem-bearing target remains direct
impossibility of `O(r)` for positive-row prime roots, unless a global
actual-prime-root invariant is isolated.

The already-invalidated local routes are recorded in:

```text
research/04-bounded-compression/docs/square_tail_edge_semantics_blocker.md
research/04-bounded-compression/docs/findings/square_tail_child_selected_square_inheritance_audit.md
research/04-bounded-compression/docs/findings/square_tail_child_closure_parent_residue_audit.md
research/04-bounded-compression/docs/findings/square_tail_obstruction_inheritance_local_model_audit.md
research/04-bounded-compression/docs/findings/square_tail_crt_model_arrival_order_audit_509.md
research/04-bounded-compression/docs/findings/square_tail_full_cutoff_crt_model_509.md
```
