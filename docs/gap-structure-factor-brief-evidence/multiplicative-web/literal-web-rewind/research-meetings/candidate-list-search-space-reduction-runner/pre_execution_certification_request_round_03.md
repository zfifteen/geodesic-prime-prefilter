# Pre-Execution Compliance Certification Request Round 03

## Scope

Certify whether the corrected v01 runner source may be executed under the
frozen candidate-list search-space reduction design contract.

This is not a math review and not a findings review. Review only compliance
with the contract before execution.

## Contract

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/design_contract.html`

## Corrected Runner Source

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_v01_runner.py`

SHA-256:

`e18c222b0af84c2c4e25454123143a6230e90bd4ad98a2f640017beb1283caf7`

## Public Corpus

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/cases/toy_corpus.jsonl`

SHA-256:

`8cce09d3651e8808dc8b9e79cbc46f077e1416205d9d87071b9d360ae1200520`

## Corrections Applied From Round 02

- Added explicit construction-depth tracking in the recursive CRT closure path.
- `MIN_DEPTH` now gates construction depth, not post-hoc coverage count.
- `triangulation_depth` now stores construction depth.
- The score tuple is now `[triangulation_depth, shared_thread_count, total_thread_count, -distance]`.
- Public coverage fields remain separate: left/right/shared/total thread counts.

## Codex Pre-Execution Checks

Compile:

```text
python3 -m py_compile thread_triangulation_v01_runner.py
```

Private-token scan:

```text
p = False
q = False
CASE False
known_factor False
factor_distance False
exact_factor_rank False
target_distance False
private_distance False
gcd False
factorint False
isprime False
nextprime False
sqrt False
random False
```

## Certification Question

Return exactly one classification:

- `certified_for_execution`
- `not_certified`
- `certified_with_required_corrections`

If not certified, give exact file paths and line numbers for required
corrections.

If certified, state exactly what is certified and any residual risks. Do not
run the experiment. Do not evaluate results.
