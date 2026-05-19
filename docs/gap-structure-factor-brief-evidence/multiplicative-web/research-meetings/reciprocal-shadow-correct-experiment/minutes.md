# Reciprocal Shadow Correct Experiment Research Meeting Minutes

## Context

Design the corrected reciprocal-shadow experiment after three documented failures (hidden-p bound, sqrt-downward candidate walk, 97/100 construction bias). The experiment must test whether the local multiplicative web itself nominates the hidden lower endpoint via a residue certificate, without ordinary numeric walking or secret-factor leakage.

## Participants

- Grok (lead)
- Codex (facilitator, recorder, implementation witness)

## Command Capability Notes

Local repository only. No external search or APIs during design. All reasoning anchored in PGS-native objects (local web threads, reciprocal transport, modulus-link closure, reciprocal residue closure, structural certificate). Classical methods permitted only for web construction (factoring N+/-t) and final audit membership test.

## Agenda

Design the corrected reciprocal-shadow experiment so it tests whether the local multiplicative web selects a factor without hidden-factor leakage or ordinary candidate walking.

## Negotiated Deliverable

Single self-contained HTML design contract (written 2026-05-19):

`research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html`

Contains the 7 required elements + forbidden-patterns audit table (with citations to the three invalidated scripts) + 12-item acceptance checklist. The Reciprocal Residue Closure Invariant (Codex Round 1) is recorded verbatim and classified as unresolved. The first probe target is the weaker structural-certificate test: "compact residue certificate whose class contains p on true web, does not on rotated-offset control."

## Round Log

### Round 1

- Grok focus: Converted the full meeting packet + Codex Round-1 answer into a single, implementation-ready design contract (the HTML deliverable). Enforced PGS-native frame (modulus-link transport -> reciprocal residue closure as selector -> structural certificate). Explicitly rejected all walk/hidden-p patterns from the three invalidated scripts. Operationalized the unresolved Reciprocal Residue Closure Invariant as a concrete 4-r (highest-degree) conflict-check + CRT-merge residue generator for the v1 probe only.
- Grok question: (none - deliverable had no remaining unresolved choice after incorporating the exact invariant sketch and the structural-certificate target; concrete v1 operationalization and 12-item checklist were fixed in the document).
- Codex answer: (Round 1 supplied the anchoring invariant and the weaker "residue certificate whose class contains p, control does not" target).
- New object or invariant: Reciprocal Residue Closure Invariant (unresolved) - "a lower endpoint class is admissible only if its transported partner residues produce a stable divisor-count shadow across the same offset-indexed web under all offset-preserving controls." Hierarchy recorded: modulus-link closure = transport plane, reciprocal residue closure = selector, endpoint-chain traversal = downstream audit.
- Open issue: None for the design contract itself. The v1 probe must still be written and the first surface executed under the 12-item acceptance checklist before any numbers are treated as evidence.

## Candidate Insights

- The transport (modulus-link) is always tautological per r; the selector is the cross-thread consistency filter that only the true pairing survives.
- Enumerating residues mod M built from highest-degree r's is a deterministic, non-walking generator for the first surface; later surfaces can replace the enum with generating-set construction from pairs of threads.
- The 16/16 coherence ranking is now re-interpretable as "the true p mod M is the unique (or top) residue that produces a globally consistent y across the thread constraints."

## Falsification Tests

- Rotated-offset web must destroy the high-closure classes that contain p.
- Synthetic random-offset web with identical r multiset must not spontaneously produce a compact certificate that still contains p at top rank.
- Any code path that builds an integer interval or uses p/q after build_case must fail the static audit before the surface run is admitted.

## Convergences

- All three participants (original user, Codex, Grok) converged on the same failure mode: previous probes were measuring encounter during a walk, not nomination by the web.
- The structural-certificate target (residue class, not the number) is the minimal clean observable that still exercises the reciprocal transport and closure.

## Unresolved Questions

- Exact scaling of the closure procedure when the product of the top-4 r's exceeds practical enumeration (future work; v1 uses the 16 + 4 natural-ratio cases where M stays enumerable).
- Whether "stable divisor-count shadow" requires an additional predictor that uses the merged y to forecast divisor counts on the web rows (the v1 operationalization uses consistency of the b predictions themselves as the shadow).

## Next Research Move

Implementation witness (Codex) writes the v1 probe script `reciprocal_shadow_residue_certificate_probe.py` strictly against the HTML contract, runs the first surface, and signs the 12-item checklist. Only after sign-off are any measured results published. The Reciprocal Residue Closure Invariant itself stays open; the HTML is the current frozen contract for evidence collection.
