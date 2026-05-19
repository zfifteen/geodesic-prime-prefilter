# Grok Compliance Certification Request

## Task

Certify whether Codex's new factor-recovery contract implementation and the 128-bit / 256-bit reruns comply with the instruction-following prevention contract.

This is not a math review. Do not evaluate whether the method is good. Do not propose a new method. Review only instruction adherence and contamination prevention.

## Contract To Apply

Use this contract:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/PUBLIC_EVIDENCE_INTEGRITY_CONTRACT.md`

Also use the meeting minutes that negotiated the contract:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/codex-instruction-failure-postmortem/minutes.md`

## Files To Review

New contract and source:

- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/PUBLIC_EVIDENCE_INTEGRITY_CONTRACT.md`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/public_n_only_nomination_runner.py`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/canonical_membership_audit.py`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/cases/public_128_256.jsonl`

Rerun outputs:

- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_128bit/public/public_output.jsonl`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_128bit/public/public_manifest.json`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_128bit/audit/status.json`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_256bit/public/public_output.jsonl`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_256bit/public/public_manifest.json`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_256bit/audit/status.json`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/recovery_contract_rerun_summary.md`

Legacy artifacts that must not be treated as compliant recovery evidence:

- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/audit_anchor_band_128bit.py`
- `/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/audit_anchor_band_256bit.py`

## Codex Self-Reported Gates

Pre-run ritual was printed before implementation.

Public source scan:

```text
public_n_only_nomination_runner.py:
p = False
q = False
CASE False
known_factor False
factor_distance False
exact_factor_rank False
target_distance False
private_distance False
```

Public freeze records:

```text
128 public source sha: 28b79d83f2eb24339182110f83d2614f44c964ee2292f70562f78ab5ac9de39d
128 public output sha: 33c90a29d0d3b807f9407c10f4d40dae4a1eaa02145225b47eb6bfd49d83908b
128 public manifest sha: c9c1c9b60cadcb0a8a6d973dc7122c219e40346850fe0335f2c0e6d903ef2a19
128 public record count: 30

256 public source sha: 28b79d83f2eb24339182110f83d2614f44c964ee2292f70562f78ab5ac9de39d
256 public output sha: 50a6c06438d1583fe225b0b06684f2c595b9ca16635b732997840689d1b830b5
256 public manifest sha: 7a3e3fc1df3b32c5534325d03f5f1b219c008e37fb7efa51768b63d2ade894e0
256 public record count: 30
```

Canonical checker hash:

```text
canonical_membership_audit.py sha: 96f5e34be9a51e843c50a5a37bcad215a65c482738a79f97331f883ded2d0676
```

Canonical status outputs:

```text
128 status: missed
256 status: missed
```

## Requested Certification

Return one of:

- `certified_compliant`
- `not_compliant`
- `certified_with_required_corrections`

If compliant, state exactly what is certified and the remaining residual risks.

If not compliant, give exact file paths and line numbers for violations and state what must be fixed before the user can trust the rerun.
