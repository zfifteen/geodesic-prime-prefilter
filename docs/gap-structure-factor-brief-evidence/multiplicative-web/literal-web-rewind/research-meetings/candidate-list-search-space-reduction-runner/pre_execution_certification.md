# Pre-Execution Certification

Status:

```text
certified_for_execution
```

Grok certified the corrected v01 runner source for execution under the frozen
design contract.

Certified source:

`thread_triangulation_v01_runner.py`

Source SHA-256:

`dd1b0d9f1d69f25c845f2812214da92187f4e3750609b1b94963934d3fd03878`

Public corpus:

`cases/toy_corpus.jsonl`

Corpus SHA-256:

`8cce09d3651e8808dc8b9e79cbc46f077e1416205d9d87071b9d360ae1200520`

## Exact Compliance Verified By Grok

- The source compiles.
- The private-token scan is clean for all required tokens.
- The `PUBLIC_FREEZE_RECORD` gate includes paths, hashes, public command,
  record count, original-space size, reduction ratio, reduction bits, public
  nominations summary, and `PRIVATE_AUDIT_UNLOCKED: true`.
- All seven pre-implementation checklist items in the frozen HTML contract are
  satisfied.
- The runner accepts only `--n`.
- The runner never opens the corpus or reads labels.
- The runner never accepts private factors.
- The runner never invokes or embeds any checker.
- Arithmetic is public CRT combination of thread residues of `N`.

## Grok Residual Risks

The remaining risks are the contract's own residual risks:

- pre-freeze oracle influence on the frozen v01 parameters;
- cross-session smuggling of private measurements into future design;
- future temptation to change thread set, depth, or cap on the same corpus
  without a new contract version.

No experiment results were reviewed during certification.
