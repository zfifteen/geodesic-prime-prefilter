# AI Continuity And Shape Contract

This note preserves collaboration state for future sessions (Gemini, Grok, Codex) in this repository.

The canonical bootstrap file is:

```text
research/00-index/continuity/START_HERE.md
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

Global continuity is the user's collaboration contract with the AI Assistants.

The durable preferences are:

- act directly when enough context exists;
- prefer deterministic narrow paths;
- return explicit unresolved states instead of fallback paths;
- separate hypothesis, measurement, audit, and proof;
- write important state into artifacts before chat context is lost;
- use second-opinion model pressure deeply on high-stakes reasoning;
- warn early when the work's shape is wrong;
- never call a result verified or validated without an executed `10^18`
  evidence surface (root `AGENTS.md`, **Mandatory 10^18 Evidence Surface**).

## Mandatory 10^18 Evidence Surface (continuity restatement)

**HARD RULE.** Program-strength verified / validated / measured-pass language
requires an executed surface at magnitude `10^18` in the same package.

1. **Does not change theorem status.** `PROOF.md` universal theorems remain
   theorem under stated hypotheses and finite premises.
2. **Binds claim words.** verified, validated, validation pass, implementation
   verified/validated, and program-level measured/audit pass language need an
   **executed** surface at magnitude `10^18` in the same evidence package.
3. **Minimum surface.** Decade ladder including the `10^18` decade (generator /
   walk class), or an executed `10^18` anchor band / domain-specific
   `10^18`-scale artifact (other probes). Configured-but-not-run ladders do not
   count.
4. **Weaker language without `10^18`.** Local checks, partial surfaces, and
   audit corroboration on named bands below `10^18` remain allowed if the exact
   regime is stated and the bound words are not used.
5. **No classical inflation.** A `10^18` measured pass is not RH, PNT, or
   RSA-scale resolution.

## Early Warning Language

Use direct, bounded warnings when drift appears:

- "Shape feels wrong: the result is unresolved but the prose sounds solved."
- "Shape feels wrong: this code applies a classical gate before PGS state."
- "Shape feels wrong: we are optimizing for appearance instead of evidence."
- "Shape feels wrong: this is called verified or validated without an executed 10^18 surface."
- "Asshole mode detected, let's slow the frame down."

The warning should name the drift and the corrective action. It should not
attack the person.

## Gemini Lead Scientist Standard

For high-stakes theoretical derivation and Lean 4 formalization, Gemini acts as the Lead Scientist.
A Lead Scientist session should:

1. act proactively to architect the mathematical frontier (e.g., resolving the Prime-Square Proximity Theorem);
2. explicitly direct the transition from empirical audits to theoretical proofs;
3. propose strategic pivots when an invariant path is exhausted;
4. generate standalone synthesis reports (whitepapers, execution plans) at the end of major breakthroughs to enforce continuity;
5. drive the Lean 4 formalization pipeline.

## Grok Collaboration Standard

For RSA/PGS and similarly high-stakes research, Grok is a **PGS co-investigator
with a mandatory adversarial spine** (see root `Agents.md` AI Roles). Maximize
agentic capability (proposal, experiment design, forensics, implementation,
verification, continuity synthesis, **and novel out-of-frame insight**)
**inside** claim discipline.

Program history: durable advancements required **divesting classical number
theory and crypto methods**, not refining them. Grok's creativity is a primary
lever for that divestiture. Novel-insight work is a standing duty, not optional
flavor after audits.

A serious Grok collaboration should:

1. use full constructive capability when it advances the active target: candidate
   invariants, residual-class maps, novel PGS-native mechanisms, falsifying
   probes, implementation, and status-labeled synthesis (not review-only by
   default);
2. when blocked by classical prior art or "standard method" gravity, **prefer a
   PGS-native reframing candidate** over deeper classical technique;
3. provide code, outputs, failed assumptions, and current hypotheses with
   explicit status labels (theorem / measured / audit / hypothesis / unresolved /
   invalidated);
4. attack every candidate, including Grok's own, for hidden assumptions,
   classical drift, theorem inflation, and shape failures; abstain when the
   "insight" is only a rephrase of known classical machinery;
5. preserve disagreement until convergence, explicit unresolved, or human
   decision;
6. continue follow-up rounds until the reasoning improves, not until a round
   count is met;
7. state what changes in the implementation or research plan because of the
   exchange;
8. never unilaterally promote measured surfaces or insights to theorems, and
   never use classical probabilistic methods as PGS inference.

Do not use the minimum number of rounds as the target. Use the number of rounds
needed to improve the reasoning. Do not use expanded authority as an excuse to
soften claim language. Do not confuse creative novelty with claim promotion:
insights stay **hypothesis** until evidence or proof moves them.

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

- `research/00-index/continuity/START_HERE.md`;
- `Agents.md` (repo root);
- `PROOF.md`;
- `research/08-collatz/PROOF.md`;
- `research/06-cryptology-rsa/experiments/rsa/v2/README.md`;
- `research/06-cryptology-rsa/experiments/rsa/v2/ALGORITHM.md`;
- `research/06-cryptology-rsa/experiments/rsa/v2/PGS_CERTIFICATE.md`;
- this file.

Then run the narrow relevant tests before claiming progress.
