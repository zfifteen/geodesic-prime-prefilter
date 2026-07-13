# Left-endpoint parity modular bias falsification

## Executive summary

**Insight under attack (hypothesis):** left-endpoint parity creates a systematic modular bias when using min-`tau` witnesses in observed prime gaps.

**Verdict: WEAKENED** (measured on regimes up to left prime `5e7`; not theorem; not program-verified).

| Arm | Status |
| --- | --- |
| Even vs odd mismatch at `z >= 4` | **weakened** (logically forced: `z >= 4 => even` on `M_v1`) |
| Even vs odd at `z >= 3` | **survives (measured)** |
| Mismatches at `w = p + 1` | **survives (measured)**: 100% of GWR z4-mm on D and F |
| Rightmost fewer z4-mm than leftmost | **survives (measured)** on prior window and **fresh** `(2.5e7, 5e7]` |
| Rightmost fewer at `z >= 3` on fresh | **falsified** (`357 > 335`) |
| Leftmost prefers even among ties | **falsified (measured)** (rates ~equal) |
| Ties (not unique) carry z4-mm | **survives (measured)** |

Fresh band (`p in (2.5e7, 5e7]`, 1,435,207 gaps): leftmost z4-mm = **3**, rightmost = **2**. All three leftmost mismatches at `p + 1` on multi-way ties.

Full tables: [FINDINGS.md](FINDINGS.md). Claims: [HYPOTHESIS.md](HYPOTHESIS.md).

## Package contents

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Formal claims and disconfirmations |
| `experiment_design.md` | Protocol |
| `probe_parity_bias.py` | Deterministic probe |
| `test_probe_parity_bias.py` | Local unit checks |
| `artifacts/results_*.json` | Measured outputs |
| `FINDINGS.md` | Results and verdict |
| `README.md` | This file |

## Repro

```bash
python3 -m pytest experiments/left-endpoint-parity-modular-bias-falsification-2026-07/test_probe_parity_bias.py -q

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 11 --p-max 25000000

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 25000000 --p-max 50000000 --exclusive-min
```

## Exact limits

- Highest left prime: `5e7`. Not `10^18`.
- Do not use verified / validated / program-level measured-pass language.
- Related prior package falsified leftmost *necessity*; this package tests *parity / endpoint bias*.
- Theorems in `PROOF.md` are not demoted.
