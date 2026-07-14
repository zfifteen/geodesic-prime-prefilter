# Next impact task pointer (2026-07-13)

**Role:** Continuity Scribe + Orchestrator merge after Quartet pressure  
**Full report:** [research/00-index/continuity/reports/next-impact-task/index.html](../reports/next-impact-task/index.html)  
**Active goal pin (pursue this):** [ACTIVE_GOAL_50bit_residual_discriminator.md](ACTIVE_GOAL_50bit_residual_discriminator.md)

## Sync

| Field | Value |
| --- | --- |
| Remote | `https://github.com/zfifteen/prime-gap-structure` |
| HEAD | `3825ff5cba242e26ba30da14b0fd9a219c54f616` |
| Pull | Already up to date with `origin/main` |
| Quartet gate | ON (implementer, auditor, verifier, scribe spawned this turn) |

## Executive finding

The single most impactful next research task is:

```text
Derive and pressure-test ONE public PGS residual discriminator D
from public PGSPG certificate fields that either:
  (A) closes the 50-bit residual under public rules, or
  (B) partitions it into a stable residual subclass, or
  (C) leaves it honestly unresolved with stronger diagnostics

Named residual family:
  unresolved_by_reciprocal_carrier_misalignment

Honesty gate:
  ADV-001 (carrier misalignment must not vanish by classical smuggling)
```

## Live residual pin (measured smoke on HEAD, not verified)

Reproduced with rsa-v3 on regression fixtures:

| Case | Outcome |
| --- | --- |
| 40-bit `rsa_v2_40bit_static_001` | `endpoint_class_by_reciprocal_deadline_signature_correction` |
| 50-bit `rsa_v2_50bit_static_001` | `unresolved_by_reciprocal_carrier_misalignment` |

50-bit diagnostics:

```text
endpoint_chain_steps = 350
stage = gwr_carrier_transport_closure
gwr_carrier_fields_present = ok
gwr_carrier_floor_transport_within_gap_bound fails:
  delta=30
  bound=28
  transported=32059651
  upper_w=32059621

bound formula (code):
  max(20, (6 * lower.gap_offset) // 5)   # 1.2 * gap
```

Meaning: certificates and GWR fields exist; reciprocal floor image of the lower
carrier misses the upper carrier by two units past the current public bound.

## Status labels

| Layer | Label |
| --- | --- |
| Task selection under team pressure | **hypothesis** priority choice |
| RSA endpoint structure on live ladder | **measured** (not universal RSA theorem) |
| 40-bit / 64-bit rungs | **measured** + **audit** factor true |
| 50-bit residual | **unresolved** |
| New public discriminator D | **hypothesis** / **unresolved** (not derived yet) |
| Super-Signal; V2 residue ranking; fixed isqrt chambers | **invalidated** |
| UBC / PSP / GWR / next-prime | **theorem** (unchanged; PROOF.md controls) |
| LSCD ladder; co-landing bridge | **secondary** (not the single center) |
| Live `rsa-v2/output/summary.json` | **stale empty** on HEAD; do not use as evidence pin |
| Generator decade ladder through 10^18 | **measured** (generator family only) |

## Team pressure

| Role | #1 preference | Report use |
| --- | --- | --- |
| Auditor | 50-bit modulus-link residual + public discriminator | **Selected as #1** |
| Verifier | A1 residual pressure + residual ledger | **PASS**; live `delta=30;bound=28` pin |
| Implementer | LSCD multi-regime residual pressure | Secondary package |
| Scribe first draft | Public co-landing / remaining bridge | Secondary PEDK structure |

## Why not the other fronts as #1

- LSCD: high-value residual geometry after UBC; lower force than live cryptology residual center.
- Co-landing / gap-compatibility: real measured bridge; not the named 50-bit resolver residual.
- Lean / hourly square-branch audit: important, not residual breakthrough. Note: `ACTIVE_TARGET` path for `4e8..5e8` summary JSON is missing on disk while findings prose exists (hygiene debt, not theorem debt).
- Super-Signal salvage / 256-bit competition theater: invalidated or classical-drift shapes.
- Generator rework: completed production milestone.

## 10^18 claim language

This pointer and the HTML report do **not** use program-level verified / validated language for the residual family.
Any future package that wants those words for this residual family needs an executed `10^18` surface per `AGENTS.md`.
Bit size is not a substitute for that surface.

## Next session first action

1. Freeze baseline residual ledger with current rsa-v3 resolver on regression fixtures into a dated `output/` directory.
2. Write one-page public contract for exactly one discriminator D (start from the `delta=30 > bound=28` miss).
3. Implement and run ADV-001 + 40/50/64 controls.
4. Commit non-empty `inference_rows.jsonl`, `residuals.jsonl`, `summary.json`.

Primary code home:

```text
research/06-cryptology-rsa/experiments/live-solver/rsa-v3/
```

Key predicate site:

```text
research/06-cryptology-rsa/experiments/live-solver/rsa-v3/gwr_carrier_closure.py
  :: gwr_carrier_floor_transport_within_gap_bound
```

Do not edit `PROOF.md` for this task.
