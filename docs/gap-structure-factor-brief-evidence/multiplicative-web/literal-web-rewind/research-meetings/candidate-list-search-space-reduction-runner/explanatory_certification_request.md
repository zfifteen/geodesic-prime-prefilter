# Explanatory Amendment Certification Request

## Scope

Certify whether the amended v01.1 runner source may be executed under the
public-only explanatory evidence amendment contract.

This is not a math review and not a findings review. Review only compliance
before execution.

## Contracts

Parent design contract:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/design_contract.html`

Explanatory amendment contract:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/explanatory_evidence_amendment_contract.html`

## Amended Runner Source

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_v01_1_runner.py`

SHA-256:

`812de62285df1c24e0d9cde6f8a4298c89aa2fa2bd526020ec53c330147e693e`

## Required Amendment

The amended runner must add only these seven public manifest fields:

- `pre_cap_qualified_count`
- `max_observed_triangulation_depth`
- `depth_counts_pre_cap`
- `cap_active`
- `emitted_depth_counts`
- `cutoff_triangulation_depth`
- `pre_cap_to_emitted_ratio`

The public output list must remain unchanged from the certified v01 runner for
each N.

## Codex Checks

Compile:

```text
python3 -m py_compile thread_triangulation_v01_1_runner.py
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

Return one of:

- `certified_for_execution`
- `not_certified`
- `certified_with_required_corrections`

If certified, state exactly what is certified and residual risks. Do not run
the experiment. Do not evaluate results.
