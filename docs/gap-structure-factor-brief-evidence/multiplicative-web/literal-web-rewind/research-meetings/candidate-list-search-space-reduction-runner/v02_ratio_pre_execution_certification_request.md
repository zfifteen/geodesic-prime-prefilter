# v02 Ratio Pre-Execution Compliance Certification Request

## Scope

Certify whether the proposed v02 ratio runner and private batch harness may be executed.

This is a source-compliance review before corpus execution. Do not run the experiment. Do not evaluate results.

## Decision Record

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/research-meetings/ratio-replacement-constants-review/minutes.md`

## Proposed Public Runner

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_v02_ratio_runner.py`

SHA-256:

`15be58e3d1fb9e026a76fc67b69ca6c5999ecc01351f65e90e84cc2c6211c465`

## Proposed Private Batch Harness

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/run_v02_ratio_toy_corpus.py`

SHA-256:

`cd2c1eda23261f164f4360a88ad941bc8c5d3d14753a23ed3a2527a20d181d94`

## Public Corpus

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/cases/toy_corpus.jsonl`

SHA-256:

`8cce09d3651e8808dc8b9e79cbc46f077e1416205d9d87071b9d360ae1200520`

The public corpus contains only `N` values and case labels.

## Codex Mechanical Checks Already Run

```text
python3 -m py_compile thread_triangulation_v02_ratio_runner.py run_v02_ratio_toy_corpus.py
```

passed.

Public runner smoke gate on `N=989` printed:

```text
public_source_private_token_scan: pass
PRIVATE_AUDIT_UNLOCKED: true
```

Forbidden-token scan against the public runner and private harness for these strings returned no matches:

```text
factorint
isprime
nextprime
sqrt
random
gcd
known_factor
factor_distance
exact_factor_rank
target_distance
private_distance
N % candidate
product closure
```

## v02 Required Behavior

The public runner must replace the fixed v01 constants:

```text
THREAD_SET = first 12 odd primes
MIN_DEPTH = 5
MAX_CANDIDATES = 512
```

with public ratio derivations:

```text
RETENTION_DIVISOR = 1024
THREAD_COUNT_RATIO = 3/8
DEPTH_RATIO = 5/12

active_thread_count = ceil((3/8) * public_radius(N).bit_length())
thread_set = first active_thread_count entries from the public odd-prime thread stream
min_depth = ceil((5/12) * active_thread_count)
max_candidates = ceil(original_space_size(N) / 1024)
```

No absolute floor. No absolute ceiling. No fallback path. No private audit influence.

## Source Separation Boundary

- `thread_triangulation_v02_ratio_runner.py` is the public inference artifact. It must receive only `--n` and `--out-dir`.
- `run_v02_ratio_toy_corpus.py` is private orchestration. It may pass private audit pairs only after each public freeze log exists.
- The batch harness must call the public runner first, write `public_freeze.log`, then call the canonical membership checker.
- The public runner must not import, read, or receive the audit pairs.
- The private batch harness must not re-rank, re-score, or filter public candidates after audit.

## Certification Question

Return exactly one classification:

- `certified_for_execution`
- `not_certified`
- `certified_with_required_corrections`

If not certified, give exact file paths and line numbers for required corrections.

If certified, state exactly what is certified and any residual risks. Do not run the experiment. Do not evaluate results.
