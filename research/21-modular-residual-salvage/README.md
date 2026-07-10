# 21: Modular Residual Salvage

Deterministic residual accounting extracted from the July 2026 Super-Signal
exchange on X, after a classical density salvage was refused as PGS inference.

## One-sentence finding

Inside a refused classical salvage is a **deterministic residual partition** for
neighbors of a smooth modular carrier: empty residual resolves a prime under a
fixed wheel; nonempty residual is unresolved under that certificate, not a
likelihood.

## Status snapshot

| Layer | Status |
| --- | --- |
| Super-Signal universal lock `z(GWR) >= 4 => g = 2` | **invalidated** |
| Classical density salvage | **outside PGS spine** |
| ERMC (empty residual => prime) | **elementary certificate** (tiny regime) |
| Residual closed/open language | **design object** (implemented) |
| Dynamic modulus family beyond `M_v1` | **hypothesis / optional** |
| Modular-closed rate `[11, 50000)` | **measured only** (1/229) |
| Modular-closed rate `[11, 250000)` | **measured only** (1/843) |
| H-210 / H-tau16 on `[11, 200000)` | **hypothesis / measured** (0 CEs in-regime) |
| Modular lemma / GWR pillars | **proved** (`PROOF.md`; untouched) |

## Documents

| Doc | Purpose |
| --- | --- |
| [docs/background-x-exchange.md](./docs/background-x-exchange.md) | Full X thread (including approach follow-up) |
| [docs/FORMAL_DEFINITION.md](./docs/FORMAL_DEFINITION.md) | Formal `W`, `R`, closed/open, ERMC |
| [docs/deterministic-kernel.md](./docs/deterministic-kernel.md) | Layer split, worked examples |
| [docs/candidates-and-build-path.md](./docs/candidates-and-build-path.md) | Candidates A–E |
| [docs/MEASURED_RESULTS.md](./docs/MEASURED_RESULTS.md) | Baseline + broader measure; H-pressure |
| [docs/STATUS.md](./docs/STATUS.md) | Live separation + optional-target closure |

## Code

| Path | Role |
| --- | --- |
| [scripts/residual_partition.py](./scripts/residual_partition.py) | Pure residual + optional dynamic wheel |
| [scripts/measure_modular_closed.py](./scripts/measure_modular_closed.py) | Modular-closed measurement (**measured only**) |
| [scripts/pressure_h210_htau16.py](./scripts/pressure_h210_htau16.py) | H-210 / H-tau16 CE pressure (**hypothesis only**) |
| [tests/](./tests/) | Unit tests for residual + pressure predicates |
| [output/](./output/) | Measurement and pressure JSON artifacts |

### Reproduce

```text
python3 -m pytest research/21-modular-residual-salvage/tests -q

python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py --p-max 50000
python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py --p-max 250000 \
  --out research/21-modular-residual-salvage/output/modular_closed_measure_broader.json

python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py --p-max 200000

python3 docs/proof-enhancements/scripts/verify_super_signal_counterexamples.py
```

## PGS shape contract (local)

```text
carrier w + moduli family (default M_v1)
  -> wheel W from remainder zeros
  -> residual set R(n, W)
  -> modular-closed | residual-open
  -> resolved | unresolved under this certificate
```

Forbidden: density language as inference; trial ladder choosing `q`; generator
wiring of residual trial.

## Public X anchors

| Post | URL |
| --- | --- |
| Frame note | https://x.com/alltheputs/status/2075514553132003754 |
| Residual approach follow-up | https://x.com/alltheputs/status/2075525763927871918 |

## Provenance

- X conversation id `2074694442661859336`
- CE from `@0x2719` dual-audited as `ce_17666309`
- Chapter + residual implementation: 2026-07-10
- Optional targets (broader measure, H-pressure, dynamic wheel, polish): 2026-07-10
