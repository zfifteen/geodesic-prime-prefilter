# Research Meeting Opening - Residue-Certificate Public Selector

## Agenda

Review the cross-audited residue-certificate experiment result and methodology, then produce a stronger public selector for `M` or for certificate ranking that avoids collapse to the small-prime unit group.

## User Starting Material, Preserved Verbatim

Review the experiments result and metholody in a [$research-meeting](/Users/velocityworks/.codex/skills/research-meeting/SKILL.md) 

The product of this meeting should be a stronger public selector for M or for certificate ranking that avoids collapsing to the small-prime unit group.

## Current Evidence

Repository root:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure
```

Meeting output folder:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/residue-certificate-public-selector/
```

Controlling prior contract:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html
```

Final cross-audit report:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/final-cross-audit-report.md
```

Part One audit:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-01-grok-performs-codex-audits/codex_audit.md
```

Part Two audit:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/grok_audit.md
```

## Current Result Summary

Both independent implementations were methodologically admissible and classified as `boundary_measurement`.

Measured behavior:

- 20 cases executed in both lanes.
- True-web certificate cardinality was always `48`.
- Rotated-control certificate cardinality was always `0`.
- Deterministic synthetic-control certificate cardinality was always `0`.
- Selected modulus factors were always `[2, 3, 5, 7]`, so `M = 210`.
- `p % M` appeared in every true-web certificate.
- The true-web certificate was exactly the small-prime unit group modulo 210.
- The true-web rank of `p % M` was mid-range, not a tight nomination.

The current operationalization distinguishes the true offset-to-factor pairing from controls, but it does not select the hidden factor residue. It admits every residue invertible modulo 210.

## Boundaries For This Meeting

Stay inside the PGS-native and residue-certificate frame:

- No hidden factors in generation.
- No candidate integer walks.
- No prime streams or root scans.
- No divisibility, product-closure, or `gcd(candidate, N)` inference gates.
- True, rotated, and deterministic synthetic controls remain mandatory.
- Any proposed selector is a hypothesis or proof target until tested.
- We need a public selector for `M` or a public ranking rule over certificate residues, not a numeric factor search.

## Requested Grok Role

Apply your maximum available reasoning.

Opine first on why the current method collapses to the small-prime unit group. Then propose or negotiate one concrete meeting deliverable. The deliverable must be specific enough that Codex can write it into meeting minutes as the next experimental contract.

After your opening opinion and proposed deliverable, ask exactly one question for Codex to answer before the next round.
