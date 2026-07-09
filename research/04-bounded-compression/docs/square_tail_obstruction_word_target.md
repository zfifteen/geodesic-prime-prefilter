# Square-Tail Obstruction Word Target

## Status: RESOLVED 2026-07-05

The square branch is **proved** in [PROOF.md](../../../PROOF.md) §Prime-Square
Proximity Theorem. The obstruction-word research below is retained as historical
context for how the proof route was explored.

The target was not a probabilistic claim about prime density. It was a
deterministic obstruction-elimination problem, now closed.

## PGS Object

Let `r` be an odd prime and let

```text
S = r^2.
```

Let

```text
p = P(S)
```

be the greatest prime below `S`, and put

```text
D(r) = S - p.
```

The dynamic cutoff is

```text
C(p) = max(64, ceil(0.5 * log(p)^2)).
```

The square branch closes exactly when

```text
D(r) <= C(p).
```

If `D(r) > C(p)`, then every odd integer

```text
r^2 - 2m,  1 <= m <= floor(C(p) / 2),
```

is composite.

## Obstruction Word

For a hypothetical square-tail counterexample, define

```text
ell_m = least prime factor of r^2 - 2m
```

for every

```text
1 <= m <= floor(C(p) / 2).
```

Since `r^2 - 2m < r^2`, every composite term has a prime factor below `r`.
Thus

```text
ell_m < r.
```

The obstruction word is the ordered finite word

```text
W(r) = (ell_1, ell_2, ..., ell_floor(C(p)/2)).
```

Equivalently, each letter records the congruence

```text
r^2 == 2m mod ell_m.
```

The infinite-tail proof target is to show that no prime root `r` in the
selected square branch can carry a full obstruction word. The route must be a
deterministic collapse:

```text
full obstruction word
-> recursive smaller obstruction
-> chamber contradiction or closed base case
```

## Base Closures

A root is closed immediately when any of the following holds:

1. `D(r) <= C(p)`.
2. The corresponding gap lies in the finite bounded-compression base recorded
   in `PROOF.md`.
3. The obstruction word fails to exist at some offset, which means
   `r^2 - 2m` is prime and the predecessor lies inside the cutoff.

The hard case is therefore only:

```text
D(r) > C(p)
```

with a complete obstruction word of length `floor(C(p)/2)`.

The selected-square condition also has an offset form. If `s` is the previous
prime root before `r`, then selected-square means

```text
r^2 - P(r^2) < r^2 - s^2.
```

This is a broad deadline. It does not imply the dynamic cutoff. The audit is
recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_selected_square_deadline_audit.md
```

## Current Record Calibration

The current high-utilization record is

```text
r = 424,171,123
r^2 = 179,921,141,587,081,129
p = 179,921,141,587,080,391
D(r) = 738
C(p) = 790
```

So the row is closed:

```text
D(r) / C(p) = 0.9341772151898734.
```

The obstruction-prefix certificate is:

```text
research/04-bounded-compression/output/square_tail_obstruction_word_424171123.json
```

It records:

| Quantity | Value |
|---|---:|
| Full counterexample word length `floor(C(p)/2)` | `395` |
| Actual composite prefix length before `p` | `368` |
| Prefix fraction of counterexample word | `0.9316455696202531` |
| Distinct least factors in prefix | `99` |
| Most frequent least factor | `3`, appearing `123` times |
| Largest least factor in prefix | `159,673,649` at offset `152` |
| Distinct child square projections | `99` |
| Child projections closed by their own cutoff | `99` |
| Child projections satisfying selected-square condition | `99` |
| Largest child utilization | root `509`, offset `48`, cutoff `78` |

The current record therefore nearly realizes a full obstruction word but stops
because the predecessor prime occurs at offset `738`, before the cutoff at
`790`.

Every distinct least-factor letter in the current record projects to a smaller
closed selected-square branch. The strongest child projection is

```text
root = 509
root^2 = 259,081
previous prime = 259,033
offset = 48
cutoff = 78
```

This is a measured recursive shape, not yet a proof. The missing theorem is
the parent-to-child implication: a complete obstruction word must collapse to
one or more smaller closed square-tail states in a way that eliminates the
parent counterexample.

The pointwise projection fact is not a proof. The direct-containment version
is invalidated by the strongest current child projection:

```text
parent root = 424,171,123
child root = 509
```

The parent word contains `509` once, at offset `498`. The child word for
`509` has an actual obstruction prefix of length `23` and a counterexample
length of `39`; it also uses least factors `83` and `449`, which are absent
from the parent word. The surviving recursive target is therefore a global
cascade or covering-impossibility theorem, not direct child-word containment.

The audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_recursive_projection_audit_424171123.md
```

The transitive projection graph for the same record has `208` nodes, `900`
edges, maximum depth `6`, and no observed open descendant. Every edge strictly
decreases the root, and every observed node is closed by its own dynamic cutoff
and satisfies the selected-square condition.

That graph is measured cascade anatomy, not a proof. The missing theorem is
the edge semantics from complete parent obstruction to eliminated parent
counterexample.

The graph audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_projection_graph_424171123.md
```

The moving-cover audit records the exact residue-cover burden. The `99`
observed least-factor classes in the current record cover `385 / 395` positions
in the full counterexample window and miss the offsets

```text
738, 740, 750, 756, 758, 762, 770, 776, 782, 786.
```

The predecessor-prime offset `738` is one of the uncovered positions. The
remaining proof route must therefore explain why a hypothetical counterexample
cannot inject new least factors into every uncovered suffix position while
preserving least-factor minimality and the selected-square condition.

When the seven actual composite-defect least factors are added, the same
record covers `392 / 395` positions. The remaining uncovered offsets are
exactly the actual prime positions:

```text
738, 756, 758
```

The moving-cover audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_cover_audit_424171123.md
```

The carrier-economy audit separates repeat-capable factors from singleton
factors. For the current record, `43` prefix factors satisfy `ell <= M` and
cover `329 / 395` positions. The `56` prefix factors with `ell > M` cover one
position each, raising the prefix cover to `385 / 395`.

This gives the cover route a non-tautological pressure point: a hypothetical
counterexample must complete the suffix by adding enough non-propagating
singleton fills, or by introducing new repeat-capable factors, without leaving
a prime-valued defect.

The carrier-economy audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_carrier_economy_424171123.md
```

The M-rough defect audit gives the cleanest equivalent target. Apply every
repeat-capable carrier `ell <= M` to the whole moving window. The remaining
positions are exactly the values `r^2 - 2m` with no prime factor at most `M`.
For the current record, the repeat-capable carriers cover `330 / 395`
positions, leaving `65` M-rough defects. Three of those defects are prime,
at offsets:

```text
738, 756, 758
```

A complete counterexample is therefore equivalent to every M-rough defect
being composite with least factor greater than `M`. The square-tail theorem is
equivalent to forcing at least one prime-valued M-rough defect before the
cutoff.

The rough-defect audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_rough_defect_audit_424171123.md
```

The rough-defect descent audit checks the composite rough defects recursively.
For the current record, all `62` composite M-rough defect least-factor children
are smaller roots, and all `62` children have their own prime-valued M-rough
defect. The missing theorem is still the edge-semantics implication from
closed children to parent elimination.

The descent audit is recorded in:

```text
research/04-bounded-compression/docs/findings/square_tail_rough_descent_audit_424171123.md
```

The edge-semantics blocker records why this descent is not yet a proof.
The parent relation

```text
r^2 - 2m = ell * c
```

and child closure

```text
ell^2 - 2u is prime
```

do not imply parent closure under the current definitions. A new transport law
is required.

The blocker is recorded in:

```text
research/04-bounded-compression/docs/square_tail_edge_semantics_blocker.md
```

## Next Lemma Targets

The next theorem work should target one of these exact statements.

### Recursive Collapse Lemma

Every complete obstruction word `W(r)` forces a smaller square-tail obstruction
state or a finite descending cascade with root strictly below `r`, unless the
counterexample is already eliminated by a base closure.

The weaker claim that one projected child directly contains its own child word
inside the parent word is false on the current record.

### Covering Impossibility Lemma

No prime root `r` can satisfy all congruences

```text
r^2 == 2m mod ell_m
```

for `1 <= m <= floor(C(p)/2)` with each `ell_m` the least prime factor below
`r`, while also satisfying the selected-square branch condition.

### Chamber-Elimination Boundary

A carrier with divisor count `4` or larger before `r^2` does not contradict a
square witness, because the square has divisor count `3`. Direct chamber
elimination only works if the obstruction word fails and produces a prime
inside the cutoff.

The active proof routes are therefore the recursive collapse lemma and the
covering impossibility lemma. Both are deterministic. Neither requires density
language.

The global collapse target is stated in:

```text
research/04-bounded-compression/docs/square_tail_global_obstruction_collapse_target.md
```
