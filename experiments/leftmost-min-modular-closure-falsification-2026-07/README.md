# Leftmost min modular closure falsification

## Executive summary

**The share Core insight is falsified on its comparative edge. Its absolute forcing reading remains invalidated.**

Share: https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553  
Theme: *The Leftmost Minimal-Divisor Probe Converts Partial Modular Data into Gap-Closure Rules*

On the decisive regime (left prime `p` in `[11, 2.5e7]`, 1,565,923 consecutive gaps):

| Selector | Mismatches (`z >= 4` and `g > 2`) |
| --- | ---: |
| GWR (leftmost min-`tau`) | **2** |
| alt-A (rightmost min-`tau`) | **0** |
| alt-B (first interior `p+1`) | **152,620** |

**Mechanism (measured on the two Super-Signal CEs):** both counterexample gaps are multi-way min-`tau` ties. Leftmost min hits a highly divisible witness (`z = 4`). Rightmost min hits a different min-`tau` point with `z = 1` (no mismatch). So leftmost bias is what *creates* those false positives on this surface, opposite to the share story that leftmost is necessary for clean modular closure.

| Claim | Status |
| --- | --- |
| H-absolute: `z(GWR) >= 4 => g = 2` universal | **invalidated** (reconfirm; already in `PROOF.md`) |
| H-comparative: leftmost necessity / superiority | **falsified** on `p <= 2.5e7` |
| Modular zero lemma; GWR maximizer; next-prime | **theorem** (untouched) |
| Program verified / validated | **not claimed** (max regime `2.5e7`, no `10^18`) |

Full narrative: [FINDINGS.md](FINDINGS.md) · structured HTML: [index.html](index.html) · orchestrator map: [STATUS_MAP.md](STATUS_MAP.md)

---

## Package contents

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Formal claims and falsifiers |
| `experiment_design.md` | Protocol design |
| `probe_selectors.py` | Deterministic comparative probe |
| `test_probe_selectors.py` | Local unit checks (6 tests) |
| `artifacts/results_pmax_*.json` | Measured outputs |
| `FINDINGS.md` | Implementer findings |
| `index.html` | Self-contained status HTML |
| `STATUS_MAP.md` | Merge / claim stack map |
| `README.md` | This file |

## Repro

```bash
python3 -m pytest experiments/leftmost-min-modular-closure-falsification-2026-07/test_probe_selectors.py -q

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 100000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_100000.json

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 2000000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_2000000.json

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 25000000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_25000000.json
```

## Quartet pressure (summary)

| Role | Outcome |
| --- | --- |
| Implementer | Probe, tests, multi-regime artifacts, FINDINGS |
| Verifier | **PASS** (unit tests + mid-regime count match; weaker claim language OK; nits fixed on main) |
| Auditor | Preemptive **REJECT** on share strong "certify" framing; re-audit of executed package: **APPROVE with nits** |
| Scribe | This package documentation on main |

## Exact limits

- Highest left-prime regime: `2.5e7`. Not `10^18`.
- Do not use verified / validated / program-level measured-pass language for this package.
- Rightmost min having zero mismatches is **measured** on regime D, not a theorem.
- Theorems in `PROOF.md` are not demoted.
