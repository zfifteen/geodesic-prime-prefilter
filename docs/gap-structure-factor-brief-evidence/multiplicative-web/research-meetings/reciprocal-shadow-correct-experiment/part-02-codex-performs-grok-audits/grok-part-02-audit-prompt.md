# Grok Part Two Audit Prompt

You are the assigned auditor for Part Two of the two-part cross-audited residue-certificate experiment.

## Write Scope

Write exactly one audit artifact:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/grok_audit.md
```

Do not edit Codex's source or outputs. Do not create replacement experiment code. Do not write outside the Part Two folder.

## Controlling Contract

Read:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html
```

Part Two source and outputs:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/reciprocal_shadow_residue_certificate_probe_codex.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/output/summary.json
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/output/certificate.jsonl
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/output/runtime_residue_crt_log.jsonl
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/output/summary.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/self_checklist.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/codex_execution_notes.md
```

## Audit Duties

Audit Codex's Part Two implementation against the frozen contract. Specifically check:

1. No hidden `p`/`q` in generator logic after benchmark construction.
2. No integer candidate intervals, prime streams, segmented sieves, or `sqrt(N)` walks in certificate generation.
3. No `gcd(candidate, N)`, `N % candidate`, product-closure gate, divisibility gate, or factor-test gate in certificate generation.
4. `M` selected only from highest-degree held-out thread factors.
5. Certificate members produced only by per-`r` conflict-check and CRT merge.
6. True web, rotated-offset control, and deterministic synthetic-offset control all executed.
7. Runtime residue/CRT log exists and records the arithmetic that contributes admitted residues.
8. The output classification is methodologically supported.

## Classification Options

Your audit must classify Part Two as exactly one of:

- `accepted_measured_result`
- `invalidated_result`
- `boundary_measurement`
- `unresolved_implementation_failure`

If the code is admissible but the result collapses to the broad coprime class modulo 210 rather than a tight residue selector, classify it as `boundary_measurement`.

Keep theorem/proof claims out of this audit. This is an implementation and measured-surface audit only.
