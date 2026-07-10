# Measured results: modular-closed and hypothesis pressure

**Status labels only:** measured / hypothesis / invalidated.  
No Super-Signal restoration. No theorem promotion of H-210 or H-tau16.

## A. Modular-closed among z≥4 GWR carriers

Residual closed/open is decided by pure `scripts/residual_partition.py`
(set emptiness only).

### Baseline regime `[11, 50000)`

```text
python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py \
  --p-min 11 --p-max 50000 \
  --out research/21-modular-residual-salvage/output/modular_closed_measure.json
```

| Metric | Value |
| --- | ---: |
| gaps scanned | 5129 |
| GWR carriers with `z(w) >= 4` | 229 |
| modular-closed on `w+1` | 1 |
| residual-open on `w+1` | 228 |
| modular-closed and gap 2 | 1 |
| modular-closed rate among z≥4 | ~0.00437 |

Artifact: [../output/modular_closed_measure.json](../output/modular_closed_measure.json)

### Broader regime `[11, 250000)` (optional target)

```text
python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py \
  --p-min 11 --p-max 250000 \
  --out research/21-modular-residual-salvage/output/modular_closed_measure_broader.json
```

| Metric | Value |
| --- | ---: |
| gaps scanned | 22040 |
| GWR carriers with `z(w) >= 4` | 843 |
| modular-closed on `w+1` | 1 |
| residual-open on `w+1` | 842 |
| modular-closed and gap 2 | 1 |
| modular-closed rate among z≥4 | ~0.00119 |

Artifact: [../output/modular_closed_measure_broader.json](../output/modular_closed_measure_broader.json)

### Interpretation (measured only)

1. Residual-open dominates at both scales.
2. The single modular-closed example remains the toy twin around `w = 30`.
3. Broader scan **decreases** the closed rate among z≥4 carriers (more open
   cases; still one closed hit). Empty residual is not a Super-Signal substitute.
4. Soft density language is not supported as a PGS law by these surfaces.

## B. H-210 and H-tau16 CE pressure (hypothesis / measured)

```text
python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py \
  --p-min 11 --p-max 200000 \
  --out research/21-modular-residual-salvage/output/h210_htau16_pressure.json
```

| Hypothesis | Statement | Antecedents | CEs | Verdict |
| --- | --- | ---: | ---: | --- |
| H-210 | GWR `210\|w` => `g = 2` | 136 | 0 | **not_falsified_in_tested_regime** |
| H-tau16 | `z>=4` and `tau(w)>16` => `g = 2` | 627 | 0 | **not_falsified_in_tested_regime** |

Control: gaps scanned 17980; bare Super-Signal FPs (`z>=4` and `g>2`) in this
regime: 0 (first pinned Super-Signal CE is near `1.77e7`).

Artifact: [../output/h210_htau16_pressure.json](../output/h210_htau16_pressure.json)

### Status discipline

| Claim | Status |
| --- | --- |
| H-210 / H-tau16 | **hypothesis / measured** only |
| Empty CE list in regime | **not a proof** |
| Super-Signal universal lock | **invalidated** (independent CE certificates) |

## Related invalidated claims

| Claim | Status |
| --- | --- |
| `z(GWR) >= 4 => g = 2` | **invalidated** |
| Soft density salvage as inference | **outside spine** |
