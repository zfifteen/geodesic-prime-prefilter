# Status map: Leftmost min modular closure falsification

**Share:** https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553  
**Title:** The Leftmost Minimal-Divisor Probe Converts Partial Modular Data into Gap-Closure Rules  
**Package:** `experiments/leftmost-min-modular-closure-falsification-2026-07/`  
**Primary HTML:** `index.html`  
**Findings:** `FINDINGS.md`  
**Handoff:** `CONTINUITY_HANDOFF.md`  
**Scribe date:** 2026-07-11

## Orchestrator verdict

| Item | Status |
| --- | --- |
| Package on main workspace | **present** (code + artifacts + docs) |
| H-absolute `z(GWR) >= 4 => g = 2` | **invalidated** |
| H-comparative leftmost necessity | **falsified** (`p <= 2.5e7`) |
| Tau-min mattering (non-min probe fails) | **kept** as **measured** only (not a share rescue) |
| GWR / next-prime / modular zero lemma | **theorem** unchanged |
| Program verified / validated | **forbidden** (no `10^18` surface) |
| Continuity `START_HERE` update | **not required** (experiment-local) |
| Verifier | **PASS** |
| Auditor | Preemptive **REJECT** on share framing; re-audit of executed package: **APPROVE with nits** |
| Scribe | Docs aligned; handoff written |

## Axis map (kept / narrowed / weakened / falsified / invalidated)

| Axis | After pressure |
| --- | --- |
| Absolute modular forcing (`z(GWR) >= 4 => g = 2`) | **invalidated** (universal) |
| Leftmost position as necessary for modular closure | **falsified** on `p <= 2.5e7` |
| Share certification / "force twin" framing | **invalidated** (framing; auditor) |
| Min-`tau` selection vs bare first-interior | **kept** as **measured** support that tau-min matters |
| Rightmost min as universal cleaner selector | **not promoted** (measured zero mm on regime D only) |
| Proved GWR maximizer + modular zero lemma | **kept** as **theorem** |

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
| 5e4 | 5129 | 0 | 0 | 421 | smoke; counts from `results_pmax_50000.json` |
| 1e5 | 9588 | 0 | 0 | 791 | multi-thousand-gap zero-mismatch arm for alt-A |
| 2e6 | 148929 | 0 | 0 | 13708 | implementer + verifier mid-regime match |
| 2e7 | 1270603 | 1 | 0 | 123393 | first Super-Signal CE; alt-A still 0 |
| 2.5e7 | 1565923 | 2 | 0 | 152620 | both pinned CEs; comparative **falsified** |

Decisive z4 detail at `2.5e7`: GWR z4=43170 hit_twin=43168 mm=2; rightmost z4=43168 mm=0; first z4=195788 mm=152620.

**Artifact enum note:** `probe_selectors.py` always emits `invalidated_*` for H-absolute. Older JSON (`results_pmax_50000.json`, `results_pmax_2000000.json`) may still show a stale `not_falsified_in_tested_regime` string for H-absolute; mismatch counts remain authoritative.

## Quartet pressure

| Role | Outcome |
| --- | --- |
| Implementer | Probe, tests, FINDINGS, multi-regime JSON on main package |
| Auditor | Preemptive REJECT on share "certify / force twin" framing; ban May `core-insight-decisive-test` Stage 2; re-audit **APPROVE with nits** (claim split + decisive comparative kill present) |
| Verifier | PASS: unit tests; mid-regime counts match; weaker labels only; no 10^18 |
| Scribe | README, index.html, STATUS_MAP, CONTINUITY_HANDOFF (this pass) |

## Auditor nits (resolved on main)

1. HYPOTHESIS twin-interior wording: **fixed** (length-1 interior `{p+1}`, not empty).
2. Absolute status enum on small regimes: **fixed** in `probe_selectors.py` (always `invalidated_*`, never `not_falsified_in_tested_regime` for H-absolute).
3. CE unit test for rightmost escape: **added** in `test_probe_selectors.py` (package has **6** unit tests).
4. Primary comparative kill hierarchy remains rightmost vs GWR (unique-only secondary).

## Merge checklist

- [x] Experiment tree on main under `experiments/leftmost-min-modular-closure-falsification-2026-07/`
- [x] Artifacts present (`results_pmax_*.json`)
- [x] HTML + STATUS_MAP + README with executive summary first
- [x] FINDINGS uses invalidated / falsified / measured only (no verified/validated)
- [x] CONTINUITY_HANDOFF with next pressure and unresolved list
- [x] Auditor re-audit: APPROVE with nits (nits fixed)
- [x] Orchestrator final ack: do not amend `PROOF.md` beyond existing Super-Signal invalidated status
- [x] Orchestrator final ack: no program continuity center change unless user asks

## Unresolved (must stay labeled unresolved)

- Any replacement residual forcing rule after Super-Signal and leftness necessity fail.
- H-210 / H-tau>16 survivors at higher scale: **hypothesis / measured-on-regime only** until a named surface; **verified** requires executed `10^18`.
- Whether a different non-leftmost min-`tau` operationalization (for example random among ties) changes comparative counts.
- Whether rightmost min-`tau` remains zero-mismatch beyond `2.5e7` (measured absence only, not a theorem).
- Position-index histogram of min-`tau` false positives: **new hypothesis** only if pursued; not a rescue of the share.

## Next decisive pressure (insight does not survive)

Share insight as stated is **falsified / invalidated**. Optional residual work is a **new** package: histogram which min-`tau` tie index carries `z >= 4` and `g > 2`. See `CONTINUITY_HANDOFF.md` section 6.
