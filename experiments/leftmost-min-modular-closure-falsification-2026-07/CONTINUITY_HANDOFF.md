# Continuity handoff: leftmost-min modular closure falsification

**Date:** 2026-07-11  
**Package:** `experiments/leftmost-min-modular-closure-falsification-2026-07/`  
**Primary HTML:** `index.html`  
**Status map:** `STATUS_MAP.md`  
**Share (historical claim source only, not proof):**  
`https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553`  
Related thread status id (context only): `2076070453479882932`

This note is for the next session. It does not amend `PROOF.md`. It does not
move the program center.

---

## 1. Observable object

For consecutive primes `p < q`, the interior integers carry divisor counts
`tau(n)` and remainder-zero counts `z(n)` on the fixed vector
`M_v1 = (2, 3, 5, 7, 30, 210, 2310)`.

A **mismatch** is:

```text
z(w) >= 4  and  g = q - p > 2
```

The share claimed that the **leftmost** min-`tau` witness is what turns a high
`z` into a gap-closure signal, and that alternative witnesses lose that power.

---

## 2. Axis status after falsification pressure

| Axis | Claim in one line | Status | Regime / evidence |
| --- | --- | --- | --- |
| Absolute forcing | `z(GWR) >= 4 => g = 2` universal | **invalidated** | Already in `PROOF.md`; reconfirm GWR mismatch = 2 at `p <= 2.5e7` |
| Comparative leftness necessity | Leftmost is required for clean modular closure; alts must mismatch more / at least once | **falsified** | Decisive: GWR 2, rightmost min 0, first-interior 152620 |
| Share "certify remaining interior empty" prose | Strong forcing / certification language | **invalidated** (framing) | Auditor preemptive REJECT of share framing |
| Tau minimization matters | Non-min probe loses sufficiency | **kept** (measured only) | First-interior mismatch load is huge on all regimes |
| Modular zero lemma | `z >= 4 <=> 30 \| w` on `M_v1` | **theorem** (kept) | Untouched |
| GWR maximizer / next-prime | Proved pillars | **theorem** (kept) | Untouched; not demoted |
| Rightmost is "better" universally | Rightmost min never mismatches | **not claimed** | Measured zero mismatches on `p <= 2.5e7` only |
| Program verified / validated | Implementation validated language | **forbidden** | Max surface `2.5e7`; no executed `10^18` |

**Orchestrator one-liner:** insight is **falsified** on leftness necessity and
**invalidated** on absolute forcing. Tau-min mattering is the only non-theorem
fragment still supported by measurement, and it does **not** rescue the share.

---

## 3. Exact measured regimes and numbers

Mismatch definition: `z(w) >= 4` and `g > 2`.

| left prime max | gaps | GWR mm | alt-A rightmost mm | alt-B first mm | artifact |
| ---: | ---: | ---: | ---: | ---: | --- |
| 5e4 | 5,129 | 0 | 0 | 421 | `artifacts/results_pmax_50000.json` |
| 1e5 | 9,588 | 0 | 0 | 791 | `artifacts/results_pmax_100000.json` |
| 2e6 | 148,929 | 0 | 0 | 13,708 | `artifacts/results_pmax_2000000.json` |
| 2e7 | 1,270,603 | 1 | 0 | 123,393 | `artifacts/results_pmax_20000000.json` |
| 2.5e7 | 1,565,923 | **2** | **0** | **152,620** | `artifacts/results_pmax_25000000.json` |

Decisive regime detail (`p in [11, 2.5e7]`):

| Selector | z4 | hit_twin | mismatch | twin_rate among z4 |
| --- | ---: | ---: | ---: | ---: |
| GWR leftmost min-`tau` | 43,170 | 43,168 | 2 | 0.999954 |
| alt-A rightmost min-`tau` | 43,168 | 43,168 | 0 | 1.0 |
| alt-A unique-only | 43,168 | 43,168 | 0 | 1.0 |
| alt-B first interior | 195,788 | 43,168 | 152,620 | 0.220483 |

Pinned GWR mismatches (also historical z≥4⇒g=2 claim certificates in `PROOF.md`):

```text
p=17666309  q=17666317  g=8  w=17666310  tau=16  z=4
p=22284029  q=22284037  g=8  w=22284030  tau=16  z=4
```

On both rows: multi-way min-`tau` ties; rightmost min escapes with `z < 4`;
unique-only does not fire. Gaps where rightmost differs from GWR on this
surface: **987,444** of 1,565,923.

**Artifact enum note:** probe code now always emits `invalidated_*` for
H-absolute. Some older JSON files (`results_pmax_50000.json`,
`results_pmax_2000000.json`) may still carry a stale
`not_falsified_in_tested_regime` string for H-absolute while mismatch counts
remain correct. Prefer mismatch counts and `PROOF.md` over the stale enum.

---

## 4. Quartet pressure (for merge)

| Role | Outcome |
| --- | --- |
| Implementer | Probe, tests, multi-regime artifacts, `FINDINGS.md` |
| Auditor | Preemptive REJECT of share strong "certify" framing; re-audit of executed package: **APPROVE with nits** (nits fixed on main) |
| Verifier | **PASS** on unit tests and mid-regime count match; weaker claim language only; no `10^18` |
| Scribe | This handoff + aligned `STATUS_MAP.md` / `index.html` / README |

Unit tests in package: **6** local tests (not a scale surface).

---

## 5. What remains unresolved

Keep these labeled **unresolved** (or **hypothesis** / **measured-on-regime**):

1. Any **replacement residual forcing rule** after residual-class and leftness
   necessity both fail.
2. Whether **rightmost** min-`tau` stays zero-mismatch **beyond** `2.5e7`
   (measured absence only; not a theorem).
3. Other non-leftmost operationalizations among ties (for example mid-index or
   random among minima): comparative counts **unresolved**.
4. H-210 / H-tau>16 style residual filters at higher scale: **hypothesis /
   measured-on-regime only** until a named surface; **verified** requires an
   executed `10^18` surface under program policy.
5. Whether a position-index histogram of min-`tau` set members that carry
   `z >= 4` and `g > 2` yields a new residual class (new hypothesis, not a
   rescue of the share).

Do **not** re-open Hypothesis U (unique min + `z >= 4 => g = 2`): already
**invalidated** at `p = 156942923` in prior work.

---

## 6. Continuity: next decisive pressure

### Insight survival

The share insight as stated does **not** survive. Do not schedule "rescue the
leftmost modular closure story" work.

### If residual research continues (optional, not mandatory)

**Next decisive pressure** (new hypothesis package, not this share):

```text
On gaps with multi-way min-tau ties, histogram the index of each min-tau
member that carries z >= 4 and g > 2.
Question: does false-positive mass concentrate at the leftmost min only?
```

Acceptance rules for that **new** package (sketch):

- Pre-register mismatch definition (same as here unless justified).
- Report exact regime; no verified / validated without executed `10^18`.
- Separate theorem / measured / hypothesis / unresolved.
- Do not promote rightmost min to a universal rule from finite zeros.

### What not to do next

- Do not amend `PROOF.md` beyond existing historical z≥4⇒g=2 claim **invalidated** status.
- Do not route through May `core-insight-decisive-test` Stage 2.
- Do not demote GWR maximizer or modular zero lemma.
- Do not change program continuity center unless the user asks.

---

## 7. Paths for orchestrator merge

| Path | Role |
| --- | --- |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/index.html` | Self-contained status HTML |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/STATUS_MAP.md` | Claim stack + merge checklist |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/FINDINGS.md` | Full narrative |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/README.md` | Executive summary |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/CONTINUITY_HANDOFF.md` | This file |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_*.json` | Measured outputs |

`START_HERE.md` update: **not required** (experiment-local; program center unchanged).
