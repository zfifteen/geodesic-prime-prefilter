# Codex Execution Notes - Part Two

## Scope

Part Two independently implements the same residue-certificate experiment that Grok executed in Part One. The implementation is not copied from Grok's source structure. It keeps one compact script under the Part Two folder and writes raw outputs under `output/`.

## Construction Boundary

The script uses deterministic factorization of the public composites `N + offset` for web construction. That is the allowed web-construction role in the frozen contract. The certificate generator itself receives only held-out rows and never receives `p`, `q`, or candidate integers.

## Run Command

```bash
python3 docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/part-02-codex-performs-grok-audits/reciprocal_shadow_residue_certificate_probe_codex.py
```

## Output

- `output/summary.json`
- `output/certificate.jsonl`
- `output/runtime_residue_crt_log.jsonl`
- `output/summary.md`
- `self_checklist.md`

## Observed Result

All 20 cases classify as `boundary_measurement`.

Every case selects `[2, 3, 5, 7]`, giving `M = 210`. The true-web certificate contains 48 residues, exactly the coprime residue classes modulo 210. Rotated and deterministic synthetic controls emit empty certificates.

This agrees with Grok's Part One structural behavior and does not meet the target of a tight factor-residue nomination.
