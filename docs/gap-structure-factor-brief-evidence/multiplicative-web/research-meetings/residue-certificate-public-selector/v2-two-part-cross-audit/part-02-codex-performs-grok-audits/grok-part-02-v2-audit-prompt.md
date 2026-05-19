# Grok Part Two Audit Prompt - V2 Public Selector

You are the assigned auditor for Part Two of the V2 two-part cross-audited public selector experiment.

## Write Scope

Write exactly one audit artifact:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/grok_audit.md
```

Do not edit Codex's source or outputs. Do not create replacement experiment code. Do not write outside the Part Two folder.

## Controlling Contract

Audit against:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/residue_certificate_v2_public_selector_contract.html
```

Part Two artifacts:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/reciprocal_shadow_v2_public_selector_probe_codex.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/output/summary.json
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/output/certificate.jsonl
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/output/runtime_residue_crt_log.jsonl
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/output/summary.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/self_checklist.md
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/v2-two-part-cross-audit/part-02-codex-performs-grok-audits/codex_execution_notes.md
```

## Audit Duties

Check:

1. No hidden `p` or `q` in certificate generation or V2 ranking after construction/holdout.
2. No candidate integer intervals, prime streams, segmented sieves, root walks, `gcd(candidate, N)`, `N % candidate`, divisibility gates, product closure, random controls, or unfixed thresholds.
3. V1 certificate layer remains conflict-check plus CRT over top held-out thread factors.
4. GWR witness extraction matches Section 6 of the V2 contract.
5. V2 deviation formula matches Section 7 exactly.
6. `a` is only a reporting tie-break and does not create structural wins.
7. True, rotated, and deterministic synthetic controls all execute and are reported.
8. Required artifact classes exist and contain the V2 fields.
9. Aggregate classification matches the V2 table.

## Classification Options

Classify Part Two as exactly one of:

- `accepted_measured_result`
- `boundary_measurement`
- `invalidated_result`
- `unresolved_implementation_failure`

If implementation is admissible and the measured result is `0 / 20` structural wins with controls empty, classify it as `invalidated_result`.

Keep proof claims and factor-discovery claims out of this audit. This is an implementation and measured-surface audit only.
