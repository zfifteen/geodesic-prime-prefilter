# Grok Execution Notes - Part One V2 Public Selector Probe

**Task:** Part One of the V2 two-part cross-audited public selector experiment.  
**Role:** Performer (Grok). Codex will audit in the Part Two lane.  
**Directive followed:** Contract adherence and falsifiability over any positive-result optimization.  
**Date of execution:** single deterministic run that wrote the probe and the four raw output files; the two required MDs were added only after the raw artifacts existed.

## What Was Written (exact inventory)

All artifacts created exclusively inside:

```
.../residue-certificate-public-selector/v2-two-part-cross-audit/part-01-grok-performs-codex-audits/
```

- `reciprocal_shadow_v2_public_selector_probe_grok.py` (self-contained probe, V1 certificate layer + exact V2 GWR + deviation ranking)
- `output/summary.json` (20 per-case records + aggregate with structural_win_count and final_classification)
- `output/certificate.jsonl` (960 rows: every true-web admissible a with full V2 fields: dev_primary, support_score, structural_rank, tie_size, final_reporting_rank, is_structural_winner, is_p_member)
- `output/runtime_residue_crt_log.jsonl` (1920 entries: 960 V1 crt records + 960 V2 deviation records containing every inverse, d_primary, dev, support_score, and ranking key)
- `output/summary.md` (per-case table + aggregate statement)
- `self_checklist.md` (explicit 14-item answers)
- `grok_execution_notes.md` (this file)

No files were created, edited, or touched outside this folder. The probe script and the four output/ files were produced by one execution of the probe before any of the top-level MDs were authored. The present documents were written strictly after the raw run artifacts and the measured counts existed on disk.

## Hypothesis Under Test

The V2 contract defines a public ranking rule over the V1 certificate:

- Extract the leftmost minimum-divisor witness (GWR) from the held-out divisor-count field (t_g and optional left/right supports with divisor_count <= d_min + 2).
- For each admissible a compute the structural key (dev_primary, support_score) via reciprocal transport: inv_a = a^{-1} mod M, d = (t * inv_a) mod M, dev = min(d, M-d).
- Rank by the structural key (tie-break by a only for final reporting order).
- A case counts as a structural win only when p % M is the unique occupant of the minimal structural key (tie_size == 1). An a-only tie-break does not count.

The acceptance threshold in the contract table is 18-20 structural wins with both controls empty at the certificate layer. The hypothesis is that this public selector supplies a tight residue nomination on the 20-case surface.

## Measured Result (plain numbers, no interpretation)

- 20 cases executed (identical surface to the cross-audited V1 experiment).
- Every true-web certificate: M = 210, selected_r = [2, 3, 5, 7], cardinality = 48.
- Every rotated-offset control: cardinality = 0.
- Every deterministic synthetic-offset control: cardinality = 0.
- Controls empty on all 20 cases (satisfies the prerequisite for any non-invalidated classification).
- Structural wins (p % M is the unique minimal (dev_primary, support_score) with tie_size == 1): **0 / 20**.
- Every case had a minimal structural key shared by 2 or 4 residues (tie sizes recorded in summary.json and certificate.jsonl).
- Consequently p % M never received is_structural_winner = true.
- Per-case v2_classification in the records: all "boundary_measurement" (controls empty but no unique structural win).
- Aggregate classification under the V2 table: **invalidated_result**.

The raw counts and the classification string were emitted by the probe into summary.json and summary.md before this document was written.

## Implementation Status

- V1 certificate layer reproduced exactly (degree-based r selection, per-r b-agreement conflict check, CRT merge). Behavior matches the prior cross-audit (48 coprime residues on true web, 0 on controls).
- V2 GWR witness extraction and support window implemented verbatim from Section 6.
- V2 deviation arithmetic and structural-key ranking implemented verbatim from Sections 7-8.
- Runtime log contains the complete arithmetic trace: V1 per-r inverses + CRT steps for every admitted a, plus V2 inv_a / d_primary / dev_primary / support_score / structural_key for every true-web residue.
- p and q appear only in the two roles the contract explicitly permits (construction/hold-out inside build_case, and post-ranking membership audit). No leakage into generator or ranking paths.
- All 14 checklist items answered explicitly; 14/14 mechanical and procedural requirements are satisfied.

The implementation is admissible for audit. The measured outcome is the falsification of the ranking rule on this surface under the contract's own success/falsification criteria.

## Audit Status

- Self-checklist.md is complete and was written after the raw outputs.
- The four required machine-readable artifacts (summary.json, certificate.jsonl, runtime_residue_crt_log.jsonl, summary.md) plus the two human-readable MDs now exist in the Part One folder.
- Independent Codex audit (Part Two lane) is required before any result is considered cross-audited admissible.
- No interpretive claim beyond the measured counts and the classification string produced by the probe itself has been published.

## Invalidated State

The V2 public selector hypothesis is invalidated on the first 20-case surface under the exact operationalization and classification table stated in the controlling contract.

- 0 structural wins (required: 18-20 for accepted_measured_result).
- The rule produces a minimal structural key that is tied (size 2 or 4) in every case; p % M never occupies that key alone.
- Controls remained empty, satisfying the "both controls empty" precondition, but the win count is below the 14-case boundary threshold.
- The implementation did not relax the "unique structural (tie_size == 1)" requirement; the 0-count is therefore a genuine falsification of the selector, not an implementation artifact.

This is recorded as `invalidated_result` exactly as the contract table prescribes for fewer than 14 structural wins.

## Unresolved Next Step and Research Move

The current public ranking (GWR leftmost-min-divisor reciprocal deviation over the V1 M=210 certificate) does not yield a tight residue selector on the tested surface. The admissible set remains the full unit group modulo 210; the added structural key merely partitions that group without isolating the hidden factor residue.

Any next research move must stay inside the same contract shape:

- no hidden factors inside generation or ranking;
- no candidate integer walks, prime streams, or classical inference gates;
- true / rotated / deterministic synthetic controls preserved;
- accepted evidence only after a fresh two-part cross-audit on any revised selector.

The measured boundary (true web distinguishable from controls by the V1 certificate layer, but the V2 ranking does not further tighten nomination) is now part of the public record. Future work on stronger M selection, different public witnesses, or a different ranking functional, if pursued, will be executed under a new or amended contract and will require its own Part One / Part Two cross-audit before any claim is admissible.

All state required for a future independent auditor (source, raw outputs, logs, self-audit, and these notes) is present in this folder.

**Grok** - 2026 Part One performer session (raw execution complete, measured result recorded, ready for Codex audit).  
No further edits to the probe or the four output files will be made by the performer.