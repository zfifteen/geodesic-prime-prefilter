# Status map: Leftmost min modular closure falsification

**Share:** https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553  
**Title:** The Leftmost Minimal-Divisor Probe Converts Partial Modular Data into Gap-Closure Rules  
**Package:** `experiments/leftmost-min-modular-closure-falsification-2026-07/`  
**Primary HTML:** `index.html`  
**Findings:** `FINDINGS.md`

## Orchestrator verdict

| Item | Status |
| --- | --- |
| Package on main workspace | **present** (code + artifacts + docs) |
| H-absolute `z(GWR) >= 4 => g = 2` | **invalidated** |
| H-comparative leftmost necessity | **falsified** (`p <= 2.5e7`) |
| GWR / next-prime / modular zero lemma | **theorem** unchanged |
| Program verified / validated | **forbidden** (no `10^18` surface) |
| Continuity `START_HERE` update | **not required** (experiment-local) |
| Verifier | **PASS** |
| Auditor | Preemptive **REJECT** on share framing; re-audit of executed package: **APPROVE with nits** |

## Claim stack (must stay split)

### 1. H-absolute (forcing sufficiency)

- **Statement:** If GWR witness `w` has `z(w) >= 4` on `M_v1`, then `g = 2`.
- **Status:** **invalidated**
- **Evidence:** `PROOF.md` Super-Signal CEs `17666309`, `22284029`; reconfirm in `artifacts/results_pmax_25000000.json` (GWR mismatch count = 2).

### 2. H-comparative (selector necessity)

- **Statement:** Leftmost min-`tau` is necessary for the modular closure pattern; alternatives produce at least one mismatch in multi-thousand-gap regimes and do not beat GWR on mismatch count.
- **Status:** **falsified**
- **Evidence (decisive regime `p <= 2.5e7`):**

  | Selector | mismatches |
  | --- | ---: |
  | GWR leftmost min-`tau` | 2 |
  | alt-A rightmost min-`tau` | 0 |
  | alt-B first interior | 152620 |

  Pre-registered falsifier hit: `mismatches(alt-A) < mismatches(GWR)`.

- **Mechanism (measured on the two CEs):** multi-way min-`tau` ties; leftmost hits `z = 4`, rightmost hits `z = 1`. Leftmost bias creates those mismatches on this surface.

### 3. Modular zero lemma

- **Statement:** `z(w) >= 4 <=> 30 | w` on fixed `M_v1`.
- **Status:** **theorem** (untouched).

### 4. GWR maximizer / next-prime pillars

- **Status:** **theorem** (untouched). Not demoted by this experiment.

### 5. Hypothesis U (prior package)

- **Status:** **invalidated** at `p = 156942923` (unique min + `z >= 4 => g = 2`). Do not re-open as this share.

## Measured regimes (exact)

| p_max | gaps | GWR mm | alt-A mm | alt-B mm | notes |
| ---: | ---: | ---: | ---: | ---: | --- |
| 5e4 | 5129 | 0 | 0 | 421 | verifier smoke |
| 1e5 | 9588 | 0 | 0 | 791 | implementer |
| 2e6 | 148929 | 0 | 0 | 13708 | implementer + verifier match |
| 2e7 | 1270603 | 1 | 0 | 123393 | first Super-Signal CE; alt-A still 0 |
| 2.5e7 | 1565923 | 2 | 0 | 152620 | both pinned CEs; comparative falsified |

## Quartet pressure

| Role | Outcome |
| --- | --- |
| Implementer | Probe, tests, FINDINGS, multi-regime JSON on main package |
| Auditor | Preemptive REJECT on share "certify / force twin" framing; ban May `core-insight-decisive-test` Stage 2; re-audit **APPROVE with nits** (claim split + decisive comparative kill present) |
| Verifier | PASS: unit tests; mid-regime counts match; weaker labels only; no 10^18 |
| Scribe | README exec summary, index.html, this STATUS_MAP |

## Auditor nits (resolved on main)

1. HYPOTHESIS twin-interior wording: **fixed** (length-1 interior `{p+1}`, not empty).
2. Absolute status enum on small regimes: **fixed** in `probe_selectors.py` (always `invalidated_*`, never `not_falsified_in_tested_regime` for H-absolute).
3. CE unit test for rightmost escape: **added** in `test_probe_selectors.py`.
4. Primary comparative kill hierarchy remains rightmost vs GWR (unique-only secondary).

## Merge checklist

- [x] Experiment tree on main under `experiments/leftmost-min-modular-closure-falsification-2026-07/`
- [x] Artifacts present (`results_pmax_*.json`)
- [x] HTML + STATUS_MAP + README with executive summary first
- [x] FINDINGS uses invalidated / falsified / measured only (no verified/validated)
- [x] Auditor re-audit: APPROVE with nits (nits fixed)
- [x] Orchestrator final ack: do not amend `PROOF.md` beyond existing Super-Signal invalidated status
- [x] Orchestrator final ack: no program continuity center change unless user asks

## Unresolved (must stay labeled unresolved)

- Any replacement residual forcing rule after Super-Signal and leftness necessity fail.
- H-210 / H-tau>16 survivors at higher scale: **hypothesis / measured-on-regime only** until a named surface; **verified** requires executed `10^18`.
- Whether a different non-leftmost min-`tau` operationalization (for example random among ties) changes comparative counts.
- Whether rightmost min-`tau` remains zero-mismatch beyond `2.5e7` (measured absence only, not a theorem).
