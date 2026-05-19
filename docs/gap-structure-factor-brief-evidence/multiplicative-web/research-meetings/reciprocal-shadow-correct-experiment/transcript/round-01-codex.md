# Round 1 - Codex Answer + Grok Conversion

**Date:** 2026-05-19 (immediate follow-up)

## Codex Answer (verbatim)

Modulus-link closure is the closer PGS-native object. Endpoint-chain traversal is not the constructive step here; it is downstream structure once an endpoint class or endpoint certificate exists.

But modulus-link closure, as currently stated in this branch, is not yet sufficient to name a non-walking generator. It gives the right transport surface: each held-out thread has the form

```
r divides N + t
```

so the public local web supplies reciprocal constraints of the form

```
x y = N
x y = -t mod r
```

and therefore a transport relation between lower-endpoint residues and partner-endpoint residues modulo each thread factor `r`.

The failure is that this relation alone is tautological with respect to `N`. For every invertible residue of `x mod r`, there is a corresponding transported partner residue. That is a closure surface, not yet a selector.

The smallest additional invariant I would state before specifying a non-walking procedure is:

```
Reciprocal Residue Closure Invariant
```

Definition sketch:

Given the held-out local web around public `N`, construct a finite residue certificate over the thread factors. A lower endpoint class is admissible only if its transported partner residues produce a stable divisor-count shadow across the same offset-indexed web under all offset-preserving controls.

The generator must emit residue classes or endpoint classes directly from this closure calculation, not from an interval of numeric candidates. Numeric representatives are introduced only after the certificate exists, and only to audit whether the hidden factor lies in the emitted class.

In short:

```
modulus-link closure supplies the transport plane
reciprocal residue closure supplies the missing selector
endpoint-chain traversal audits or refines the selected endpoint class
```

This should be classified as an unresolved invariant, not a proved rule.

For the experiment design, I would require the next probe to avoid claiming it has found `p` as a number. The first valid target should be weaker and cleaner:

```
Can the reciprocal-shadow field emit a compact residue certificate whose class contains p and whose rotated-offset control does not contain p at the same rank or cardinality?
```

That makes the first corrected experiment a structural-certificate experiment, not a factor resolver.

## Grok (Lead) Conversion

The Codex Round-1 answer was incorporated verbatim into the design contract (sections on the invariant, the hierarchy, the classification as unresolved, and the exact weaker target).

A single concrete, auditable operationalization was added for the v1 probe only:

- Highest-degree 4 r's define M.
- Per-a conflict check inside each r (all threads using the same r must predict the identical b).
- Cross-r CRT merge to a single consistent y.
- Admissible = zero-conflict full merge; certificate = the (usually tiny) list of such a's, ranked by closure coverage.

This satisfies "emit residue classes directly from closure calculation" and "stable ... under offset-preserving controls" (the rotated web is the control; only the true pairing produces consistent global y for the correct a = p mod M).

The design HTML was written to:

`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html`

It contains the full 7-point deliverable + forbidden-patterns table (with citations to the three bad scripts) + 12-item acceptance checklist that the implementation witness must sign before any surface numbers are admitted.

No further design question was required; the deliverable is now a frozen, implementation-ready contract.

## Classifications Recorded in the Design

- 16/16 ranking -> measured result (enumerated-surface regime only)
- Ladders & blind restart -> boundary / invalidated
- Reciprocal Residue Closure Invariant -> unresolved invariant (not proved)
- First corrected target -> structural-certificate experiment (residue-class nomination, not numeric discovery)

## Next Research Move (per minutes)

Implementation witness writes `reciprocal_shadow_residue_certificate_probe.py` against the exact contract in the HTML and executes the first surface (original 16 + 4 natural-ratio larger cases) under the 12-item checklist. Only after checklist sign-off are the numbers treated as evidence. The invariant itself remains open for later strengthening.