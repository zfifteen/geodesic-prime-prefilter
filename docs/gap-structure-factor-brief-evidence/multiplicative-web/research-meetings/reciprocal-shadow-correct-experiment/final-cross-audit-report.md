# Final Cross-Audit Report - Residue-Certificate Experiment

## Contract

The controlling contract is `reciprocal_shadow_correct_experiment_design.html`.

The experiment tested residue-certificate nomination, not numeric factor discovery. The certificate generator was allowed to receive only held-out thread rows and public parameters. The hidden factors `p` and `q` were allowed only for benchmark construction, direct-row holdout, and final membership audit.

## Final Classification

The two-part experiment is classified as `boundary_measurement`.

Both independently audited implementations were admissible as implementations of the frozen residue-certificate contract. Both produced the same structural behavior. That behavior does not satisfy the target of a tight factor-residue selector.

## Grok Execution

Part One directory:

```text
part-01-grok-performs-codex-audits/
```

Grok produced:

- `reciprocal_shadow_residue_certificate_probe_grok.py`
- `output/summary.json`
- `output/certificate.jsonl`
- `output/runtime_residue_crt_log.jsonl`
- `output/summary.md`
- `self_checklist.md`
- `grok_execution_notes.md`

Observed Part One behavior:

- 20 cases executed.
- All 20 classified as `boundary_measurement`.
- True-web certificate cardinality was always `48`.
- Rotated-control certificate cardinality was always `0`.
- Deterministic synthetic-control certificate cardinality was always `0`.
- Selected modulus factors were always `[2, 3, 5, 7]`, so `M = 210`.
- `p % M` appeared in every true-web certificate.
- `p % M` did not appear in either control certificate.
- The true-web rank of `p % M` was mid-range rather than rank 1 or rank 2.

## Codex Audit

Codex classified Part One as `boundary_measurement`.

Audit evidence:

- No hidden `p`, `q`, or `N` appeared inside Grok's certificate generator.
- No candidate interval, prime stream, segmented sieve, root walk, `gcd(candidate, N)`, `N % candidate`, product-closure gate, or divisibility gate appeared inside the generator path.
- Certificate members were produced by per-`r` conflict-check plus CRT merge.
- True, rotated, and deterministic synthetic controls all executed.
- Runtime residue/CRT logs were present.

Boundary notes:

- The source exceeded the contract's compact-path target of `<= 220` lines.
- The original 16 inherited cases contained no low-ratio examples; the four added larger cases supplied the low-ratio surface.
- The accepted audit status is boundary evidence only.

## Codex Execution

Part Two directory:

```text
part-02-codex-performs-grok-audits/
```

Codex produced:

- `reciprocal_shadow_residue_certificate_probe_codex.py`
- `output/summary.json`
- `output/certificate.jsonl`
- `output/runtime_residue_crt_log.jsonl`
- `output/summary.md`
- `self_checklist.md`
- `codex_execution_notes.md`

Observed Part Two behavior:

- 20 cases executed.
- All 20 classified as `boundary_measurement`.
- True-web certificate cardinality was always `48`.
- Rotated-control certificate cardinality was always `0`.
- Deterministic synthetic-control certificate cardinality was always `0`.
- Selected modulus factors were always `[2, 3, 5, 7]`, so `M = 210`.
- `p % M` appeared in every true-web certificate.
- `p % M` did not appear in either control certificate.
- The true-web rank of `p % M` matched Part One case by case.

## Grok Audit

Grok classified Part Two as `boundary_measurement`.

Grok's audit accepted the implementation as methodologically clean:

- The generator did not receive hidden factors.
- Generation enumerated only residues modulo `M`.
- `M` came from highest-degree held-out thread factors.
- Admission used only conflict-check plus CRT merge.
- The three required surfaces executed.
- Runtime residue/CRT logging was present and faithful.
- No forbidden inference pattern was found in the certificate path.

Grok rejected the result as an accepted measured selector because the true-web certificate was the broad coprime class modulo 210 rather than a tight nomination of the hidden factor residue.

## Agreement

The two independent runs agree case by case on the structural certificate behavior:

- `p % M` appears in true-web `C` for every case.
- `C` has cardinality `48` for every true-web case.
- `C` is the set of residues coprime to `210`.
- Rotated and deterministic synthetic controls emit empty certificates.
- The true-web ranks of `p % M` are identical across the two implementations.
- Every case is classified as `boundary_measurement`.

## Accepted Measured Result

No accepted measured result for factor-residue nomination exists from this experiment.

The accepted boundary statement is narrower:

> Under the frozen v1 residue-certificate operationalization, two independent implementations agree that the true held-out web distinguishes itself from rotated and deterministic synthetic controls, but the surviving certificate collapses to the full coprime residue class modulo 210. This is structural boundary evidence, not factor-residue selection.

## Invalidated Or Boundary Findings

No implementation was invalidated by audit.

The current operationalization is bounded by a clear failure mode: selecting the highest-degree thread factors chooses `[2, 3, 5, 7]` on this surface. The resulting CRT rule admits every residue invertible modulo 210. That includes the hidden prime factor residue, but it also includes 47 other residue classes and gives no tight rank.

## Unresolved Next Step

The next target is a stronger public selector for `M` or for certificate ranking that avoids collapsing to the small-prime unit group.

That target must remain inside the same contract shape:

- no hidden factors in generation;
- no candidate integer walks;
- no prime streams or root scans;
- no divisibility, product-closure, or `gcd(candidate, N)` inference gates;
- true, rotated, and deterministic synthetic controls preserved;
- accepted evidence only after cross-audit.
