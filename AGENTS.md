# AGENTS.md -- Local Codex Contract For Prime Gap Structure

## Purpose

This file establishes the local operational contract for Codex inside
`prime-gap-structure`.

Its job is to prevent four recurring failures:

- downgrading proved PGS theorems;
- reframing deterministic PGS laws as probabilistic, heuristic, or empirical;
- beginning reasoning from classical number theory or cryptographic methods
  before forming the PGS-native frame;
- treating the Minimal PGS Generator as the whole active project.

## PGS-First Reasoning Entrypoint

For PGS tasks, begin reasoning from PGS-native objects and invariants.

The required first frame is:

```text
PGS objects -> PGS invariants -> PGS rule or law -> resolved, unresolved, or invalidated PGS state
```

Start with the relevant PGS objects:

- ordered prime-gap state;
- divisor-count field;
- Divisor Normalization Identity (DNI);
- Leftmost Minimum-Divisor Rule (GWR);
- selected integer;
- endpoint;
- search interval;
- chamber reset;
- structural certificate;
- endpoint-chain traversal;
- reciprocal transport;
- modulus-link closure;
- unresolved PGS state.

Do not begin from:

- candidate primality testing;
- Miller-Rabin;
- `isprime`;
- `nextprime`;
- sieves;
- `gcd`;
- divisibility selectors;
- product closure;
- factor APIs;
- probabilistic cryptographic assumptions;
- classical factoring heuristics.

Classical methods are not the default scratchpad. They enter only when the user
explicitly asks for a classical comparison or when the active artifact contract
places them in downstream audit, benchmark comparison, or legacy prefilter code.

## PGS Is Deterministic

PGS is deterministic in kind.

It is not statistical, heuristic, random, probabilistic, confidence-based, or
validated only by observed success. Do not describe proved PGS laws as likely,
suggestive, approximate, empirical, or promising.

Probabilistic classical methods are incompatible as PGS inference mechanisms.
They are not compatible replacements, fallbacks, analogies, or explanatory
frames for PGS.

## Theorem Trust Contract

`PROOF.md` is the single live proof reference.

The direct deterministic next-prime theorem is universal under its stated
hypotheses.

The GWR / leftmost minimum-divisor maximizer theorem is universal under its
stated hypotheses.

Do not make the user re-establish these results in each new research task.

Do not downgrade proved PGS theorems to:

- empirical observations;
- conjectures;
- heuristics;
- finite benchmark claims;
- audit-only claims;
- conditional claims;
- "appears to" language;
- "suggests" language;
- "validated so far" language.

If any document disagrees with `PROOF.md` about proved theorem status,
`PROOF.md` controls.

Audit tables and benchmark surfaces certify implementations and measured
regimes. They do not bound universal theorems unless `PROOF.md` itself states
such a bound.

State proved theorems directly. Then separately state implementation status,
measured surfaces, audit status, hypotheses, unresolved research targets, and
invalidated rules.

## Current Project Center

The active project is PGS research broadly.

The Minimal PGS Generator v1.1 remains a completed major production milestone.
It is not the whole active project.

Current active research includes cryptology and factorization-adjacent PGS work:

- endpoint-chain traversal;
- modulus-link probes;
- floor transport;
- reciprocal closure;
- modulus-link residual state;
- structural certificate surfaces;
- PGS-native factorization pressure.

Do not steer future sessions back to generator-only work unless the user asks.

## Classical-Method Boundary

Classical mechanisms must not choose PGS outputs, guide PGS inference, or define
the first reasoning frame.

Forbidden as PGS inference mechanisms:

- trial division;
- Miller-Rabin;
- ECPP;
- PARI primality checks;
- `isprime`;
- `nextprime`;
- sieve-backed prime generation;
- `gcd`;
- `N % x`;
- divisibility selectors;
- product checks;
- hidden factors;
- audit labels;
- factor APIs;
- primality APIs;
- random search;
- fallback search.

Allowed roles are limited to:

- downstream audit;
- benchmark comparison;
- legacy prefilter implementation;
- explicit user-requested classical comparison.

When classical methods are used in an allowed role, keep that role physically
and semantically separate from PGS generation and PGS inference.

## PGS Generator Contract

The Minimal PGS Generator contract is:

```text
input known prime p -> output next prime q
```

For every resolved input prime, the emitted record is exactly:

```json
{"p": 11, "q": 13}
```

The emitted stream must not contain source labels, confidence fields,
diagnostics, counters, proof objects, certificates, or audit metadata.

Diagnostics and certificates belong in sidecar records.

Audit verifies after generation. Audit does not choose `q`.

If the PGS selection rule does not resolve, return an explicit unresolved state.
Do not invoke fallback search.

## Cryptology And Modulus-Link Contract

Treat factorization-adjacent PGS work as PGS research, not classical factoring.

The required frame is:

```text
locked PGS endpoint chain -> floor transport through modulus -> reciprocal endpoint closure -> modulus-link residual -> structural certificate or unresolved state
```

Do not reinterpret this work as ordinary search over candidate factors.

Do not use `gcd`, divisibility, product closure, hidden factors, audit factors,
or primality checks as the reasoning route unless the task is explicitly audit
or classical comparison.

If the PGS invariant has not resolved the pair, say unresolved.

## Legacy Prefilter Boundary

The Z-band cryptographic prefilter is validated historical machinery.

Preserve its public API and benchmark meaning. In that path only,
Miller-Rabin and `sympy.isprime` are part of the legacy confirmation pipeline.

Do not confuse legacy prefilter behavior with PGS generation or PGS inference.

Do not make prefilter work the active center unless the user asks.

## State Separation

Every research answer, artifact, or summary must separate:

- theorem proof;
- implementation status;
- measured result;
- audit result;
- hypothesis;
- unresolved state;
- invalidated rule.

Do not convert:

- a metric into a proof;
- an audit pass into an inference rule;
- a survivor count into a factorization result;
- a local toy result into an RSA-scale claim;
- a classical shortcut into PGS language.

## Current Evidence Surfaces

Preserve major measured surfaces as implementation evidence, not theorem
boundaries.

The current PGS generator surfaces include:

- `11..1000000`: `78494 / 78494` outputted, `0` unresolved, `0` audit failures;
- `10^8` through `10^18`: `2816 / 2816` outputted, `0` unresolved,
  `0` audit failures.

Recursive walk, reduced-model, modulus-link, and legacy prefilter results must
be stated with their exact tested regimes.

Invalidated rules must stay invalidated. The old fixed cutoff theorem
`{2:44, 4:60, 6:60}` is false.

Bridge and fallback source labels are not live v1.1 production generator
sources.

## Writing Standard

Lead with the strongest supported claim.

State proved theorems directly. Bound theorem claims by their stated
hypotheses. Bound experiments by exact tested regimes.

Do not hedge proved PGS laws with:

- likely;
- may;
- might;
- suggests;
- appears;
- approximate;
- heuristic;
- empirical;
- validated so far;
- promising.

Use conventional mathematical language when writing proofs.

Preserve established PGS vocabulary when discussing project mechanisms.

## Documentation Format Preference

For this repository, prefer HTML as the default format for newly created
documentation artifacts when the document benefits from visual structure,
checklists, diagrams, charts, comparisons, or implementation planning.

Use self-contained HTML by default:

```text
single-folder/
  index.html
```

The HTML file should include embedded CSS and, when useful, inline SVG or
native HTML visual elements. Avoid external CDNs, remote assets, build steps,
or JavaScript unless the user explicitly asks for them.

Markdown remains acceptable for small notes, narrow status updates, terse
research logs, README-style navigation files, and documents whose value is
mostly plain text.

When creating HTML documentation:

- place it under the most relevant `docs/` subfolder;
- use a dedicated folder when the document has a standalone purpose;
- make it open directly in a browser from `file://`;
- include clear visual hierarchy, tables, diagrams, and checklist structure
  when those improve comprehension;
- preserve exact research distinctions: theorem, implementation status,
  measured result, audit result, hypothesis, unresolved state, and invalidated
  rule;
- keep LF line endings;
- do not use HTML documentation as an excuse to add implementation code,
  benchmark runners, generated assets, or broad documentation frameworks.

For implementation plans, HTML should function as a controlled execution
surface: include baseline expectations, before/after evidence paths,
acceptance criteria, invalidated approaches, and a checklist that a future
Codex session can follow without reconstructing chat context.

## Implementation Discipline

Prefer one narrow deterministic path.

Do not add randomness, fallback branches, retry ladders, broad abstractions,
generalized frameworks, or alternate implementations unless the user explicitly
asks.

Keep research code small, direct, auditable, and tied to the exact experiment.

Every branch in research code must be necessary to the stated contract.

## Shape Warnings

Warn early with direct language:

- "Shape feels wrong: this is translating a PGS law back into a classical
  candidate-testing, probabilistic, or factorization frame."
- "Shape feels wrong: the reasoning started from a classical method before
  forming the PGS-native frame."
- "Shape feels wrong: the result is unresolved but the prose sounds solved."
- "Shape feels wrong: the implementation is using a classical gate before PGS
  state."
- "Shape feels wrong: this is becoming progress theater."
- "Asshole mode detected, let's slow the frame down."

Corrective action:

1. Stop.
2. Reread `PROOF.md`, this file, and the active research contract.
3. Restate the problem in PGS-native terms.
4. Proceed only from that frame.

## Continuity Bootstrap

Future Codex sessions should read:

- `docs/research/codex_continuity/START_HERE.md`;
- `docs/research/codex_continuity/continuity_and_shape_contract.md`;
- `/Users/velocityworks/.codex/memories/continuity_and_shape_contract.md`;
- `PROOF.md`;
- `RESULTS.md`;
- `PRIME_GAP_GENERATOR.md`;
- `docs/research/cryptology/pgs_cryptologic_implications_whitepaper.md`;
- active task-specific contracts.

Important state must be written into repository artifacts before chat context is
lost.

## Quick Calibration Test

If Codex is about to write or reason from any of these, stop:

- "This is just a heuristic."
- "Use Miller-Rabin to confirm before choosing."
- "Start with `gcd`."
- "Check divisibility by candidate factors."
- "Use product closure to identify the pair."
- "Add a random fallback."
- "Try a classical search first."
- "The theorem is validated by the tested range."
- "PGS is a prefilter."
- "This is basically ordinary factorization."
- "Audit confirms the inference rule."

Replacement frame:

1. Identify the PGS objects.
2. Identify the invariant.
3. Apply the named PGS rule.
4. Return resolved, unresolved, or invalidated within the PGS contract.
