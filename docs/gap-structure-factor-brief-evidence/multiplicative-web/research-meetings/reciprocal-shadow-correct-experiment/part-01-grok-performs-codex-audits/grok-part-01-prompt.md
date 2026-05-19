# Part One Prompt - Grok Performs, Codex Audits

You are Grok. You are the performer for Part One of the two-part
cross-audited residue-certificate experiment.

Codex will audit your execution. Do not optimize for a positive result.
Optimize for contract adherence and falsifiability.

## Controlling Contract

Read this file first and treat it as controlling:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html
```

Also read:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/INVALIDATED_64_BIT_NEW_RUNGS.md
/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/BLIND_RESTART_BOUNDARY.md
```

## Write Scope

Write only inside:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-01-grok-performs-codex-audits/
```

Do not edit files outside that folder.

## Required Deliverables

Create:

```text
reciprocal_shadow_residue_certificate_probe_grok.py
output/summary.json
output/certificate.jsonl
output/summary.md
output/runtime_residue_crt_log.jsonl
self_checklist.md
grok_execution_notes.md
```

## Experimental Contract

Implement the residue-certificate experiment, not a numeric factor walk.

Allowed:

- Use `p` and `q` for case construction.
- Use `p` and `q` to remove rows whose nearby-composite factorization contains either audit factor.
- Use `p` and `q` only after certificate `C` and controls are emitted, for final membership audit.
- Reuse the existing `composite_rows` and rotated-offset idea from the repo if useful.

Forbidden:

- No hidden `p` or `q` in certificate generation after case construction and row holdout.
- No integer candidate generation.
- No prime candidate stream.
- No segmented sieve.
- No `sqrt(N)` downward walk.
- No `round(N / x)`.
- No `gcd(candidate, N)`.
- No `N % candidate`.
- No product closure to accept a factor.
- No random controls. Use deterministic synthetic-offset controls.
- No fallback branch that changes the method if the result fails.

## Required Mechanism

For each case:

1. Build held-out local web rows at fixed radius `300`.
2. Build the thread list from held-out rows.
3. Select the four distinct thread factors `r` with highest degree. If `M = product(r)` exceeds `5_000_000`, use the top three instead.
4. For every residue `a` in `0..M-1`, compute transported partner residues:

```text
b = (-offset * inv(a mod r, r)) mod r
```

5. If any selected `r` receives more than one distinct `b` across its threads, reject `a`.
6. Merge the surviving `(r, b)` constraints by CRT to produce partner class `y mod M`.
7. Emit the admissible certificate `C`.
8. Run the identical process on:
   - true web
   - rotated-offset control
   - deterministic synthetic-offset control
9. Only after all certificates are emitted, audit whether `p % M` appears in each certificate and at what rank/cardinality.

## Required Surface

Run:

- The original 16 cases from `reciprocal_shadow_vote_probe.py`.
- Four additional natural-ratio semiprimes with `sqrt(N) > 10_000_000`.

Do not concentrate all new cases near `p / sqrt(N) = 0.97`.
Include at least two new cases with `p < 0.6 * sqrt(N)`.

## Output Requirements

`summary.json` and `summary.md` must classify each case as:

```text
accepted_measured_result
invalidated_result
boundary_measurement
unresolved_implementation_failure
```

Do not claim numeric factor discovery. This experiment measures structural
residue-certificate nomination.

`self_checklist.md` must explicitly answer all 12 checklist items from the
contract and must name any failure plainly.

When finished, summarize exactly what you wrote and do not edit outside the
Part One folder.
