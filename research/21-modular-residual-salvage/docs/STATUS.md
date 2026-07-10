# Status: Modular Residual Salvage track

Last updated: 2026-07-10 (optional targets completed)

## Separation table

| Object | Status | Notes |
| --- | --- | --- |
| Super-Signal `z(GWR) >= 4 => g = 2` | **invalidated** | CEs `ce_17666309`, `ce_22284029`; `PROOF.md` |
| Competitor lemma (strict tau beater when `g > 2` and `30 | w`) | **invalidated** | False; ties allowed under leftmost GWR |
| Modular lemma `z >= 4 <=> 30 | w` on `M_v1` | **proved** | Survives Super-Signal demotion |
| GWR leftmost minimum definition | **proved** | Untouched |
| Soft density salvage as PGS inference | **rejected / outside spine** | Wrong shape |
| Empty Residual Modular Certificate (ERMC) | **elementary certificate** | Tiny empty-residual regime |
| Residual-open / modular-closed language | **design object** | Formalized + implemented |
| Pure residual implementation | **implemented** | `scripts/residual_partition.py` |
| Dynamic modulus family path | **hypothesis / optional** | `M_DYNAMIC_HYPOTHESIS`, `moduli_family_from_primes` |
| Unit tests | **passing** | residual + pressure predicates |
| Modular-closed rate `[11, 50000)` | **measured only** | 1/229 closed |
| Modular-closed rate `[11, 250000)` | **measured only** | 1/843 closed (broader) |
| H-210 pressure on `[11, 200000)` | **hypothesis / measured** | 0 CEs; `not_falsified_in_tested_regime` |
| H-tau16 pressure on `[11, 200000)` | **hypothesis / measured** | 0 CEs; `not_falsified_in_tested_regime` |
| Hypothesis U (unique min + z>=4) | **falsified** | External experiment suite |
| Generator residual trial inference | **forbidden** | Not wired |

## Implementation status

| Item | Status |
| --- | --- |
| Chapter docs + formal partition | **done** |
| Pure residual logic | **done** |
| Broader modular-closed measurement | **done** (`modular_closed_measure_broader.json`) |
| H-210 / H-tau16 CE pressure entry point | **done** (`pressure_h210_htau16.py`) |
| Dynamic-wheel optional path + tests | **done** |
| Public residual-approach X link in background | **done** |
| STATUS/README optional items closed | **done** |

## Reproduce commands

```text
python3 -m pytest research/21-modular-residual-salvage/tests -q

python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py \
  --p-max 50000 \
  --out research/21-modular-residual-salvage/output/modular_closed_measure.json

python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py \
  --p-max 250000 \
  --out research/21-modular-residual-salvage/output/modular_closed_measure_broader.json

python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py \
  --p-max 200000 \
  --out research/21-modular-residual-salvage/output/h210_htau16_pressure.json

python3 docs/proof-enhancements/scripts/verify_super_signal_counterexamples.py
```

## Optional targets (status)

| Target | Status |
| --- | --- |
| Broader measured regime beyond 50k | **complete** (`[11, 250000)`) |
| H-210 / H-tau16 CE pressure | **complete** (regime above; not falsified in-regime) |
| Dynamic wheel beyond `M_v1` | **complete** (hypothesis API + tests) |
| X approach post link + STATUS polish | **complete** |

## Unresolved research targets (future, not open polish)

1. Multi-hour CE pressure on H-210 / H-tau16 past `2e5` (optional science).
2. Proof-promotion process (human-approved only) if any secondary seat ever
   earns theorem status.
3. Generator wiring of residual trial: **never** (standing non-goal).

## Invalidated rules (do not revive)

- Universal Super-Signal twin lock.
- Soft density near primorials as a PGS law.
- Unique-min Super-Signal repair (Hypothesis U).

## Continuity note

Read [background-x-exchange.md](./background-x-exchange.md) for the full X
thread, including the residual approach follow-up. Residual partition is the
build surface; classical salvage is not.
