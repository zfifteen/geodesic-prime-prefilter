# Round 00 Opening: Candidate List Search-Space Reduction Runner

## Agenda

Design the next public `N`-only runner as a triangulation-based candidate-list generator whose success is measured by search-space reduction plus post-freeze membership audit.

## User Starting Material, Preserved Verbatim

```text
Now success will need to come in the form of finding the true factors in a list of candidates. This is a win because it far less computationally instense than trying to factor classically.

So, this amounts to a search space reduction. Make sense? [$reiterate](/Users/velocityworks/.codex/skills/reiterate/SKILL.md)
```

```text
Yes, so the triangulation is going to elimiate huge portions of the search space.

So at 256 bits, instead of testing millions of candidates, we can test maye a few hundres or less

What I don't know yet is the amount of that search space reduction.

Let's flesh this out at toy scales first and refine as needed.

 [$reiterate](/Users/velocityworks/.codex/skills/reiterate/SKILL.md)
```

```text
perfect. communicate that to grok and together design the next runner.
```

## Current Evidence And Boundaries

This is a design meeting, not an implementation run.

The new runner must preserve the contract created after the instruction-failure postmortem:

- input to public inference is `N` only;
- public output is a frozen candidate list;
- private factors are used only after the public output is frozen;
- success means `p` or `q` appears in the emitted candidate list;
- the measured win is search-space reduction;
- no known-factor ranking, private containment measurement, or private band-position diagnostic is admissible recovery evidence.

Relevant contract files:

- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/PUBLIC_EVIDENCE_INTEGRITY_CONTRACT.md`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/canonical_membership_audit.py`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_rerun_summary.md`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/grok-compliance-certification/certification.md`

Current compliant rerun status:

- 128-bit: `missed` under the first public `N`-only emitter.
- 256-bit: `missed` under the first public `N`-only emitter.

That result is not a failure of the broader concept. It means the first emitted list was too sparse or poorly shaped. The next runner should be designed to measure candidate-list containment and search-space reduction at toy scales before scaling upward.

## Desired Runner Concept

The next runner should treat triangulation as a public filter:

```text
large factor-distance search space -> public thread triangulation -> much smaller candidate list
```

The output should be an ordered candidate list with a clear size, so the audit can report:

- whether the true factor distance appeared;
- candidate count;
- original public search-space size;
- reduction ratio;
- rank within the emitted list, if recovered;
- no private rank outside the emitted list.

## Requested Meeting Deliverable

Produce a concrete next-runner design contract. It should specify:

- public inputs;
- public emitted artifacts;
- candidate generation mechanism;
- triangulation score ingredients;
- candidate-list size controls;
- toy-scale measurement surface;
- exact admissible success and reduction metrics;
- forbidden private-factor uses;
- how Grok will certify compliance before implementation.

Do not implement code in this meeting. Do not design a private rank audit. Do not propose hidden-factor diagnostics.

## Grok Opening Request

Grok, opine first.

Apply your maximum available reasoning. Be adversarial about instruction-following risk and practical about runner design.

First:

1. Restate the user's intended research shift in your own words.
2. Propose a concrete next-runner design for public candidate-list search-space reduction.
3. Identify the single largest compliance risk in that design.
4. Ask exactly one question for Codex to answer next.
