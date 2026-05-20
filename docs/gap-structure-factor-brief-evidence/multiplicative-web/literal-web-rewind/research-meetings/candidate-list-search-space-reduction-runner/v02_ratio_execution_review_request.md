# v02 Ratio Execution And Results Review Request

## Task

Review the v02 ratio execution and results. Produce Grok's findings report.

This is a results review, not a new implementation pass. Do not edit code. Do not propose hidden-factor diagnostics. Do not compute private ranks or containment. Use only:

- public manifests;
- public output files;
- public freeze logs;
- canonical status files;
- aggregate summary files;
- the v02 source certification.

## Source Certification

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/v02_ratio_pre_execution_certification.md`

Grok classification: `certified_for_execution`

## Executed Runner

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_v02_ratio_runner.py`

SHA-256:

`15be58e3d1fb9e026a76fc67b69ca6c5999ecc01351f65e90e84cc2c6211c465`

## Executed Harness

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/run_v02_ratio_toy_corpus.py`

SHA-256:

`cd2c1eda23261f164f4360a88ad941bc8c5d3d14753a23ed3a2527a20d181d94`

## Output Surface

Output root:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/toy_v02_ratio/`

Aggregate summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/toy_v02_ratio/summary.json`

Human summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/toy_v02_ratio/summary.md`

Each case folder contains:

- `public/public_output.jsonl`
- `public/public_manifest.json`
- `public_freeze.log`
- `audit/status.json`

## Observed Aggregate Result

```text
case_count: 10
recovered_count: 0
missed_count: 10
hit_rate: 0/10
median_emitted_count: 36.0
median_candidate_reduction_bits: 10.0
```

## Per-Case Summary

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| `toy_989` | 10 | 3 | 2 | 1 | 1 | 7 | `True` | 4.0 | `missed` |
| `toy_9379` | 14 | 3 | 2 | 1 | 1 | 10 | `True` | 6.0 | `missed` |
| `toy_25807` | 15 | 4 | 2 | 1 | 1 | 28 | `True` | 7.0 | `missed` |
| `toy_1242079` | 21 | 5 | 3 | 1 | 1 | 79 | `True` | 10.0 | `missed` |
| `toy_200250077` | 28 | 6 | 3 | 8 | 8 | 226 | `True` | 10.0 | `missed` |
| `toy_4295229443` | 33 | 7 | 3 | 64 | 64 | 663 | `True` | 10.0 | `missed` |
| `toy_18902665303` | 35 | 8 | 4 | 128 | 128 | 1296 | `True` | 10.0 | `missed` |
| `toy_1209476905903` | 41 | 9 | 4 | 1024 | 1024 | 2890 | `True` | 10.0 | `missed` |
| `toy_77468500194643` | 47 | 10 | 5 | 8192 | 8192 | 10580 | `True` | 10.0 | `missed` |
| `toy_4951764003343009` | 53 | 11 | 5 | 65536 | 29348 | 29348 | `False` | 11.159025430178117 | `missed` |

## Required Report Path

Write Grok's report to:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/grok_v02_ratio_execution_review.md`

Also print the report in your response.

## Report Requirements

Include:

- compliance status;
- whether the execution followed the certified source-separation boundary;
- result summary;
- interpretation of `0/10`;
- whether this invalidates the ratio implementation or only this initial ratio choice;
- what the public observables say about the failure mode;
- one clean next ratio adjustment, if warranted, staying public-only and avoiding hard floors/ceilings.

Do not include private ranks, private containment diagnostics, or per-distance hidden-factor explanations.
