# Codex Continuity And Shape Contract

This note preserves collaboration state for future sessions in this repository.

The canonical bootstrap file is:

```text
docs/research/codex_continuity/START_HERE.md
```

Read that file first when chat context is incomplete.

## Project Continuity

Project continuity means the repository itself must tell a future Codex session
what is true.

For PGS work, preserve:

- the active mathematical contract;
- the current implementation contract;
- exact measured results;
- downstream audit status;
- proof status;
- known invalid rules;
- the next unresolved question.

Do not leave those only in chat. Put them in Markdown contracts, tests,
fixtures, outputs, and commit messages.

## Global Continuity

Global continuity is the user's collaboration contract with Codex.

The durable preferences are:

- act directly when enough context exists;
- prefer deterministic narrow paths;
- return explicit unresolved states instead of fallback paths;
- separate hypothesis, measurement, audit, and proof;
- write important state into artifacts before chat context is lost;
- use second-opinion model pressure deeply on high-stakes reasoning;
- warn early when the work's shape is wrong.

## Early Warning Language

Use direct, bounded warnings when drift appears:

- "Shape feels wrong: the result is unresolved but the prose sounds solved."
- "Shape feels wrong: this code applies a classical gate before PGS state."
- "Shape feels wrong: we are optimizing for appearance instead of evidence."
- "Asshole mode detected, let's slow the frame down."

The warning should name the drift and the corrective action. It should not
attack the person.

## Grok Collaboration Standard

For RSA/PGS and similarly high-stakes research, Grok is part of the research
pressure system.

A serious Grok collaboration should:

1. provide code, outputs, failed assumptions, and current hypotheses;
2. ask for adversarial critique rather than agreement;
3. force hidden-assumption and shortcut detection;
4. preserve disagreement;
5. continue follow-up rounds until there is convergence, explicit disagreement,
   or a sharply defined unresolved point;
6. state what changes in the implementation plan because of the exchange.

Do not use the minimum number of rounds as the target. Use the number of rounds
needed to improve the reasoning.

## PGS/RSA-Specific Guardrail

Do not describe an RSA/PGS factorizer as solving a rung when it depends on:

- fixed additive chambers around `isqrt(N)`;
- endpoint-walk budgets as coverage;
- hidden factor fixtures;
- product closure as the PGS contraction rule;
- divisibility or `gcd` selectors;
- primality or factor APIs;
- audit data inside inference.

If the PGS invariant has not resolved the pair, the correct status is
unresolved.

## Next Session Bootstrap

For this repository, a future session should first read:

- `docs/research/codex_continuity/START_HERE.md`;
- `AGENTS.md`;
- `PROOF.md`;
- `experiments/collatz/PROOF.md`;
- `experiments/rsa/v2/README.md`;
- `experiments/rsa/v2/ALGORITHM.md`;
- `experiments/rsa/v2/PGS_CERTIFICATE.md`;
- this file.

Then run the narrow relevant tests before claiming progress.
