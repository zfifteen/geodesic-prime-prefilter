# Research Meeting Opening Prompt

## Meeting Title

Reciprocal Shadow Correct Experiment

## Created

2026-05-19T00:02:36

## Instructions For Grok

You are assigned as the lead for this experiment-design meeting. Codex is
facilitator, recorder, and implementation witness.

Use your maximum available reasoning for this meeting. Opine freely on the
agenda and starting material first. Then propose a concrete deliverable for the
meeting. After that, ask Codex exactly one question.

Do not optimize for encouragement. Identify leakage, circularity, hidden
factor use, ordinary candidate walking, factor APIs, and any construct that
would make the experiment invalid as a gap-to-factor inference test.

Classify every claim as one of: measured result, boundary measurement,
invalidated result, hypothesis, unresolved, or proof target.

## Agenda

Design the corrected reciprocal-shadow experiment so it tests whether the local
multiplicative web selects a factor without hidden-factor leakage or ordinary
candidate walking.

## Starting Material

User request:

```text
Assign Grok as the lead on this experiment hold a [$research-meeting](/Users/velocityworks/.codex/skills/research-meeting/SKILL.md) with the goal of designing the experiment correctly.
```

Immediate failure context, preserved from the user:

```text
" builds the prime stream from p_value to sqrt(N)." For fucks sake, Codex!
```

```text
What the fuck, Codex? Why did you do that?!?!? You KNOW what the rules are!
```

```text
Fix it and start over
```

## Current Evidence And Boundaries

Repository root:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure
```

Core artifacts:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/reciprocal_shadow_vote_probe.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/RECIPROCAL_SHADOW_VOTE_FINDING.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/INVALIDATED_64_BIT_NEW_RUNGS.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/BLIND_RESTART_BOUNDARY.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/reciprocal_shadow_vote_blind_restart.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/index.html
```

Current status:

```text
measured result:
  fixed-window ranking run scored all prime lower-endpoint candidates in each
  finite tested surface and ranked p first in 16 / 16 tested semiprimes.

boundary measurement:
  48-bit candidate-walk ladder and blind restart through 52 bits are not valid
  factor-selection evidence. They walk public candidates until an audit factor
  is encountered.

invalidated result:
  first 52..64-bit new-rung run used hidden p as candidate-stream lower bound.
  It must not be cited as inference evidence.

unresolved:
  produce an experiment where the reciprocal-shadow field itself defines a
  compact candidate set, candidate order, certificate, or falsification target,
  without hidden p/q and without ordinary candidate walking to the factor.
```

Hard experiment rules:

```text
p and q may be used for case construction and final audit only.
p and q must not define candidate bounds, filters, ordering, stopping logic
before scoring, or feature construction.
Do not use gcd against N, divisibility by candidate, product closure, factor
APIs, primality APIs as inference gates, random search, or fallback branches.
The method must distinguish factor selection by reciprocal-shadow structure
from merely encountering a factor during a public numeric walk.
```

Meeting deliverable requested from Grok:

```text
A corrected experiment design with:
1. the object being measured;
2. allowed and forbidden inputs;
3. candidate-generation or certificate mechanism;
4. exact success condition;
5. exact falsification condition;
6. controls that catch candidate-walk leakage and hidden-factor leakage;
7. the smallest implementation path for the next valid probe.
```

Grok, opine first as lead. Then propose or refine the deliverable. Then ask
Codex exactly one question needed to complete the deliverable.
