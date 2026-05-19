# Grok-Led Public Window Rerun: Opening Brief

## Agenda

Grok is the lead decision-maker for repairing and rerunning the multiplicative-web sparse-window experiment after Codex repeatedly allowed hidden factor data to leak into experiment setup.

## User Request, Preserved Verbatim

> Put Grok is ocntrol of this experiment and descisions. Explain your repeated failures to Grok and have Grok fix the experiment setup and rerun

## Codex Failure Statement

Codex repeatedly made the same methodological error: hidden benchmark factors `p` and `q` leaked from audit-only state into experiment setup and selection.

The immediate invalidated claim was: "scaling through a 255-bit semiprime."

The leakage was:

- the scaling script set `radius = min(p, q)`;
- candidate or "hole" construction used direct offsets derived from known `p` and `q`;
- exact success was then audited against the same hidden factors;
- the result therefore measured answer-aware benchmark scaffolding, not public factor inference.

This invalidates the 255-bit scale-up as evidence of public factor recovery.

## Relevant Existing Paths

Repository root:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure
```

Active research folder:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind
```

Known invalidated or suspect scripts:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/sparse_web_first_coverage_scale.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/sparse_web_scaling_ladder.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/sparse_web_ratio_window_audit.py
```

Prior measured outputs:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/sparse_web_first_coverage_scale/
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/sparse_web_scaling_ladder/
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/sparse_web_ratio_window_audit/
```

New Grok-led meeting and rerun folder:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/
```

## Non-Negotiable Experiment Boundary

The public experiment runner must receive only:

- `N`;
- public constants;
- a public window policy computed from `N` alone;
- the frozen thread rule, if Grok decides to preserve it.

Known `p` and `q` may be used only for:

- deterministic benchmark case construction;
- post-hoc scoring after the public runner has frozen its output;
- audit labels.

Known `p` and `q` must not choose:

- radius;
- offsets;
- candidate set;
- hole set;
- ranking;
- support rows;
- stopping condition;
- any inference branch.

## Current Intended Public Thread Rule

The last intended simple method was:

- scan offsets `t` around `N`;
- for each `N + t`, test public divisibility by `2`, then `3`, then `5`;
- record only the first small public thread found;
- stop per offset as soon as a thread is found;
- use the sparse thread pattern to nominate offsets.

Grok may keep, modify, or reject this rule, but any replacement must remain public, deterministic, and cheap.

## Forbidden Inference Mechanisms

The generator or public selector must not use:

- `p`;
- `q`;
- `min(p, q)`;
- exact factor offsets;
- `gcd`;
- factor APIs such as `factorint`;
- primality APIs such as `isprime` or `nextprime`;
- prime streams;
- `sqrt(N)` walks;
- `N % candidate`;
- product closure;
- random search;
- fallback branches.

Audit code may reference `p` and `q`, but only after public outputs are frozen and written.

## Deliverable Required From Grok

Grok is in control of experiment decisions. Produce and, if feasible, implement:

1. A corrected public experiment contract.
2. A public runner that cannot see `p` or `q`.
3. A private audit runner that scores frozen public outputs against `p` and `q`.
4. A rerun on toy and incremental larger semiprime cases.
5. A plain classification: accepted measured result, invalidated result, boundary measurement, or unresolved implementation failure.

Write all new artifacts only under:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/
```

## Opening Question For Grok

Lead this. What corrected experiment setup should replace Codex's invalidated scale-up, and what exact public window policy should be tested first?

Ask exactly one question if you need one before implementing.
