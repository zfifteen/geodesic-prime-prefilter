# Grok Session Log Convention

Use this directory for substantial RSA v2 Grok collaborations.

Grok is part of the research review system, not a checkbox.

## Filename

Use:

```text
YYYY-MM-DD-short-topic.md
```

Example:

```text
2026-05-03-transported-certificate-invariant.md
```

## Required Sections

Each log should contain:

- problem statement;
- local context supplied to Grok;
- Round 1 prompt and response;
- follow-up prompts and responses;
- material disagreements;
- accepted changes to the implementation plan;
- rejected suggestions and why;
- next concrete action.

Do not log raw JSON unless it is useful. Render prompts and responses as
readable Markdown.

## Minimum Bar

A useful Grok session asks for adversarial critique:

- hidden assumptions;
- smuggled classical shortcuts;
- falsification paths;
- invariant framing;
- implementation risks.

The session ends when there is convergence, explicit disagreement, or a sharply
defined unresolved point.
