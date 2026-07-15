# Insight-OODA loop state: PROOF.md surface

**Updated:** 2026-07-11 (LSCD residual section after auditor APPROVE + verifier PASS)  
**Scribe gate:** written after auditor/verifier pressure on insight-ooda rounds.  
**Scope:** durable loop ledger only. Does **not** edit `PROOF.md`. Does **not**
promote hypotheses to theorems.

## Context

| Field | Value |
| --- | --- |
| Parent mode | `/insight-ooda-loop` on `PROOF.md` |
| Team | Expert/Heavy skills when multi-agent depth is wanted (PGS Quartet deleted) |
| NIE prompt | `research/00-index/novel_insight_engine_prompt.md` (prompt artifact, not a claim) |
| Theorem authority | `PROOF.md` |
| Continuity home | this file |

**Writing order used throughout:**

```text
observable object -> ordinary-language mechanism -> project term -> formal definition -> measured/proved status -> exact limits
```

## Status legend (do not blur)

| Label | Meaning here |
| --- | --- |
| **theorem** | Already established in `PROOF.md` under stated hypotheses |
| **invalidated** | Universal claim killed; stays killed |
| **measured** | Catalog or regime result with exact bound |
| **hypothesis** | Falsifiable candidate; not proved |
| **rejected (novelty)** | NIE / auditor novelty gate failed; measurement may still stand |
| **unresolved** | Open at scales or forms not yet tested |

---

## Round 1: branch-envelope inversion

### Observable object

For consecutive primes `p < q` with nonempty interior, take the GWR selected
witness `w` (leftmost interior minimum of `tau`). Record the selected-witness
offset `w - p` stratified by branch label `tau(w)`.

### Ordinary-language mechanism

The proved UBC envelope `C(q)` is one uniform number for every branch. The
candidate asked whether, **inside a fixed finite regime**, the **largest**
offsets still sit on the square branch (`tau(w) = 3`), with `tau = 4` next, and
higher-`tau` branches smaller.

### Project terms

- GWR selected witness `w`
- Selected-witness offset `w - p` (not raw gap `q - p`)
- Branch label `tau(w)`
- UBC envelope `C(q) = max(64, ceil(0.5 * log(q)^2))` (proved, uniform)

### Prediction tested (falsifiable)

```text
max(w - p | tau(w) = 3) > max(w - p | tau(w) = 4) > max(w - p | tau(w) >= 6)
```

### Loop finding

| Layer | Status |
| --- | --- |
| Strict triple on `p in [11, 200000)` | **measured** (holds: 30 > 18 > 10) |
| Strict triple on `p in [11, 1000000)` | **measured** (holds: 48 > 22 > 14) |
| NIE novelty / insight-OODA promote | **rejected (novelty)** |
| Theorem change | **none** (UBC remains universal and uniform) |

**Round 1 decision:** REJECT novelty. Branch-stratified effective envelope is a
useful probe residual, not a qualifying novel insight relative to existing UBC
and square-branch structure already in `PROOF.md` / chapter 04.

### Probe package

- `research/16-predictions/probes/branch-envelope-inversion-2026-07/README.md`
- `research/16-predictions/probes/branch-envelope-inversion-2026-07/measure.json`

### Exact limits

- Regimes stop at `10^6`. No `10^18` surface. No verified / validated language.
- Does not re-open or restate UBC as empirical.

---

## Parallel implementer Round-1 residual: Level-Set Compression Dichotomy (LSCD)

**Sibling pressure (this package):** Auditor **APPROVE** (residual / hypothesis /
measured only; no contract-blocking rewrites). Verifier **PASS** (re-run at
`q_max=2000000` matches committed counts; unit tests green).

This residual is **separate** from z4 FP residual class R0. It does
**not** demote the leftmost UBC theorem. historical z≥4⇒g=2 claim stays **invalidated**.

### Observable object

Start at a known prime `p`. Walk integers by exact divisor count `tau`. Stop at
the first `tau = 2`; that endpoint is the next prime `q`.

Inside the open gap, the GWR witness `w` is the **leftmost** integer with the
smallest divisor count. Other interior integers can share that same minimal
divisor count. Call that set the **co-minimal level set** `L`, and call its
rightmost member `w_R = max L`.

The proved bound controls only the leftmost offset:

```text
w - p <= C(q) = max(64, ceil(0.5 * log(q)^2))
```

Spill means a late co-minimal lands past that window while the leftmost
witness still sits inside it:

```text
w_R - p > C(q)    while    w - p <= C(q)
```

### Ordinary-language mechanism

The proved bound freezes the **first** min-tau arrival. When the min level is
the common `tau(w) = 4` branch and it locks early (small `alpha = w - p`), the
same low divisor load can reappear much later in a long gap, past the witness
cutoff window. On the measured surface, square-branch mins (`tau(w) = 3`) and
high-tau mins (`tau(w) >= 6`) did not produce that late reappearance.

### Project terms

- GWR selected witness `w` (leftmost min-tau on the interior)
- Co-minimal level set `L = {n in (p, q) : tau(n) = tau(w)}`
- Rightmost co-minimal `w_R = max L`
- UBC envelope `C(q)` (proved, leftmost only)
- Full Level-Set Compression (LSC): every `n in L` has `n - p <= C(q)`
- Level-Set Compression Dichotomy (LSCD): residual shape after LSC fails

### Formal residual (falsifiable)

```text
LSC:   for all n in L,  n - p <= C(q)
LSCD:  if w_R - p > C(q) then tau(w) = 4
       (and, on measured regime, alpha = w - p is small / early lock)
```

### Measured surface (`11..2e6`)

**Regime:** consecutive gaps with left prime `>= 11` and endpoint `q <= 2e6`.

| Quantity | Value | Status |
| --- | ---: | --- |
| Gaps scanned | 148928 | **measured** |
| Spills (`w_R - p > C(q)`) | 17 | **measured** |
| Spills with `tau(w) = 4` | 17 | **measured** |
| Spills with `tau(w) = 3` (square) | 0 | **measured** |
| Spills with `tau(w) >= 6` | 0 | **measured** |
| Leftmost theorem breaks (`w - p > C(q)`) | 0 | **measured** |
| Max `alpha` among spills | 6 | **measured** |
| Max right utilization `(w_R - p)/C(q)` | ~1.325 | **measured** |

Spill alpha histogram (all 17): `alpha=1:2`, `2:8`, `4:4`, `6:3`.

First spill row:

```text
p=31397  q=31469  g=72
w=31399  w_R=31466  tau(w)=4  n_ties=20
alpha=2  right_off=69  C=64  util_L=0.031  util_R=1.078
```

### Status split (mandatory)

| Layer | Status |
| --- | --- |
| Leftmost UBC `w - p <= C(q)` | **theorem** (`PROOF.md`; not demoted) |
| Full LSC (every co-minimal in `C(q)`) | **invalidated** (counterexamples on `11..2e6`) |
| LSCD: spill only on `tau(w)=4` | **hypothesis**, measured hold on `11..2e6` |
| LSCD: no spill on square / high-tau | **hypothesis**, measured hold on `11..2e6` |
| Spill only when early lock (`alpha` small) | **hypothesis**, measured hold on `11..2e6` |
| historical z≥4⇒g=2 claim twin lock | **invalidated** (unchanged; LSCD is not a revival) |
| z4 FP residual R0 | **separate track** (remainder zeros / catalog, not co-minimal geometry) |
| Verified / validated language | **forbidden here** (no executed `10^18` surface) |

### Anti-demotion / anti-revival (auditor pressure)

- Spill language never rewrites the leftmost bound as empirical. UBC remains
  universal under its stated hypotheses.
- LSCD does **not** repair historical z≥4⇒g=2 claim and is **not** residual class R0.
- Do not promote LSCD to theorem from the mid-scale hold.

### Probe package paths

| Path | Role |
| --- | --- |
| `experiments/min-tau-level-set-compression-2026-07/FINDINGS.md` | Human status contract |
| `experiments/min-tau-level-set-compression-2026-07/level_set_compression_probe.py` | Probe runner |
| `experiments/min-tau-level-set-compression-2026-07/test_level_set_compression_probe.py` | Local unit checks |
| `experiments/min-tau-level-set-compression-2026-07/results_qmax_2000000.json` | Committed `11..2e6` totals + spill samples |
| `experiments/min-tau-level-set-compression-2026-07/results_2e6_stratified.json` | Stratified rates / alpha hist |

Reproduce:

```text
python3 -m pytest experiments/min-tau-level-set-compression-2026-07/test_level_set_compression_probe.py -q
python3 experiments/min-tau-level-set-compression-2026-07/level_set_compression_probe.py --q-max 2000000
```

### Exact limits

- Highest package magnitude: `2e6`. Sample: 17 spills, all `tau=4`.
- Universality of LSCD beyond `11..2e6` is **unresolved**.
- No theorem promotion. No `PROOF.md` edit from this residual note.
- No program-level verified / validated language without an executed `10^18`
  surface.

### Falsification (next pressure; stays open)

LSCD fails if an extended regime produces any of:

1. A spill with `tau(w) = 3` (square branch).
2. A spill with `tau(w) >= 6`.
3. A spill with large early lock (for example `alpha > 32`) while still
   `w_R - p > C(q)`.

LSC stays **invalidated** once one spill exists; do not revive full LSC without
a new statement.

### Auditor / Verifier

| Role | Verdict |
| --- | --- |
| Auditor | **APPROVE** as residual map at hypothesis / measured status |
| Verifier | **PASS** (re-run reproduces 17 spills, all `tau=4`, 0 leftmost breaks) |

---

## Rounds 2 to 3: z4 FP residual class R0

### Observable object

A historical z≥4⇒g=2 claim **false positive** (FP) is a non-twin consecutive prime gap
(`g = q - p > 2`) whose GWR selected witness `w` is divisible by 30.

Concrete pinned examples already in `PROOF.md`:

| p | q | g | w |
| ---: | ---: | ---: | ---: |
| 17666309 | 17666317 | 8 | 17666310 |
| 22284029 | 22284037 | 8 | 22284030 |

### Ordinary-language mechanism

The old historical z≥4⇒g=2 claim claim said: if the remainder vector of `w` has at least
four zeros, then the gap must be a twin (`g = 2`). That universal implication
is **invalidated**. Failures still happen. The residual question is whether
those failures share one tight shape (class, gap size, divisor count, and
seven-openness) rather than scattering across many forms.

### Project terms

- historical z≥4⇒g=2 claim (historical packaging of twin-gap lock from remainder zeros)
- Zero-count `z(w)` on moduli `M_v1 = {2, 3, 5, 7, 30, 210, 2310}`
- Modular lemma: `z(w) >= 4` iff `30 | w` on `M_v1` (**proved**, `PROOF.md`)
- Residual class **R0** (descriptive catalog class for observed FPs)

### Formal definition (descriptive R0)

```text
R0 = {
  class-A: w = p + 1,
  tau(w) = 16,
  g = 8,
  seven-open: w % 7 != 0
}
```

Algebraic form **measured on the catalog rows** (not a generative theorem):

```text
w = 2 * 3 * 5 * r    (r prime)
p = 30 * r - 1
q = 30 * r + 7
```

On that form, `tau(w) = 16` is forced when `r` is prime. Residual pressure is
mainly class-A, `g = 8`, and seven-open, plus absence of other forms.

### Measured fact (through `p < 50_000_000`)

| Field | Value | Status |
| --- | --- | --- |
| Regime | `11 <= p < 5e7` | **measured** |
| Non-twin gaps scanned | 2,762,031 | **measured** |
| z4 FP count | 5 | **measured** |
| FPs in R0 | 5 / 5 | **measured** |
| FPs outside R0 | 0 | **measured** |
| All five match `p = 30r-1`, `q = 30r+7`, `w = 2*3*5*r` | true | **measured** |
| Evaluation label | `all_fps_in_R0` | **measured** |

| p | q | g | w | r | tau(w) | w%7 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 17666309 | 17666317 | 8 | 17666310 | 588877 | 16 | 4 |
| 22284029 | 22284037 | 8 | 22284030 | 742801 | 16 | 6 |
| 39110069 | 39110077 | 8 | 39110070 | 1303669 | 16 | 6 |
| 45515369 | 45515377 | 8 | 45515370 | 1517179 | 16 | 5 |
| 49117829 | 49117837 | 8 | 49117830 | 1637261 | 16 | 6 |

First two rows are the pinned `PROOF.md` counterexamples. Last three appear
after extending the scan past `25e6` and still match R0 and the algebraic form.

### Status split (mandatory)

| Layer | Status |
| --- | --- |
| historical z≥4⇒g=2 claim `z(w) >= 4 => g = 2` | **invalidated** (unchanged; do not revive) |
| Modular lemma `z >= 4 <=> 30 \| w` on `M_v1` | **proved** (`PROOF.md`) |
| GWR / Interior Maximizer | **theorem** (not demoted by historical z≥4⇒g=2 claim kill) |
| FP catalog through `p < 5e7` | **measured** |
| Algebraic form on those five FPs | **measured** |
| "Every z4 FP at any scale lies in R0" | **hypothesis** only |
| Theorem `z >= 4 => (g = 2 or R0)` | **not claimed** (anti-revival) |
| Verified / validated language | **forbidden here** (no executed `10^18` surface) |

### Hypothesis (universal R0)

```text
Every z4 FP at any scale lies in R0.
```

**Status:** **hypothesis**. Supported on the measured regime only.

**Disconfirmation:** any z4 FP with `off != 1`, or `tau(w) != 16`,
or `g != 8`, or `7 | w`.

### Anti-revival (auditor pressure)

Class R0 describes **observed failures**. It does **not** repair historical z≥4⇒g=2 claim.
It is **not** a proved residual lock of the form
`z(w) >= 4 => (g = 2 or R0)`. historical z≥4⇒g=2 claim stays **invalidated**.

### Probe package paths

| Path | Role |
| --- | --- |
| `README.md` | Human status contract |
| `measure.json` | Regenerable catalog artifact |
| `probe_fp_signature.py` | Runner (regenerates measure.json) |
| `targeted_extension.json` | Class-A targeted extension to 1e8 |
| `band_5e7_6e7_full.json` | Full-sieve completeness band |

### Auditor (package)

**APPROVE** as residual catalog + hypothesis only (after rewrites). Not theorem.

---

## Rounds 4 to 6: form pressure and completeness

### Round 4 to 5 (targeted class-A extension)

| Field | Value | Status |
| --- | --- | --- |
| Method | candidates `p=30r-1` with `r` prime and `p+2` composite, then GWR | method |
| Through `p < 5e7` | 5 FPs, 0 outside R0 | **measured** (matches full sieve) |
| Through `p < 1e8` | 20 FPs, 0 outside R0 | **measured** under class-A targeting |
| Limitation | misses non-class-A FPs if any exist above full-sieve coverage | exact limit |

### Round 6 (full-sieve band completeness)

| Field | Value | Status |
| --- | --- | --- |
| Band | `p in [5e7, 6e7)` | **measured** |
| Nontwin gaps | 519524 | **measured** |
| z4 FPs | 2 | **measured** |
| Outside R0 | 0 | **measured** |
| Non-class-A FPs | 0 | **measured** |
| Match to targeted hits in band | exact (53276009, 53668469) | **measured** |

**Finding:** on this band, class-A targeting is complete (no missed non-class-A z4 FPs).

---

## Strongest supported finding

**Measured residual catalog:** z4 false positives, on every surface
executed in this loop (full sieve through `5e7`, full band `[5e7,6e7)`, and
class-A targeting through `1e8`), lie in residual class R0 with algebraic form
`p = 30r - 1`, `q = 30r + 7`, `w = 2*3*5*r` (`r` prime).

| Layer | Status |
| --- | --- |
| historical z≥4⇒g=2 claim universal twin lock | **invalidated** |
| R0 catalog on named surfaces | **measured** |
| Universal R0 at all scales | **hypothesis** |
| Mechanism why `g` is forced to 8 | **unresolved** |

## Unresolved (next loop pressure)

1. z4 FP outside R0 at any larger scale
2. Full-sieve completeness above `6e7` (not only class-A targeting)
3. Generative reason for `g = 8` (mechanism hypothesis, not measured fact)
4. Any `10^18` catalog surface if program-level verified language is ever wanted
5. Loop `solution_found` remains **false** (universal residual law not closed)

## Loop control fields

```text
round_number = 6
round_limit = 20
solution_found = false
stop_reason = session_checkpoint_not_stop (skill allows resume; not a skill stop condition)
strongest_supported_finding = R0 residual catalog of z4 FPs
next_best_action = full-sieve band above 6e7 or mechanism probe for g=8
```
| `probe_fp_signature.py` | Scanner that writes `measure.json` |
| `PROOF.md` section modular remainder facts | **invalidated** claim + proved modular lemma + pinned CEs |
| `docs/proof-enhancements/certificates/modular_remainder_invalidated_v1.json` | Invalidation certificate |
| `research/01-generator/tests/test_mod30_adjacent_carrier_generator.py (p=17666309)` | Pinned CE |
| `research/01-generator/tests/test_mod30_adjacent_carrier_generator.py (p=22284029)` | Pinned CE |

Reproduce:

```text
python3 probe_fp_signature.py --p-max 50000000
```

### Related residual tracks (not upgraded)

| Object | Relation | Status |
| --- | --- | --- |
| H-210 | Bare R0 FPs are seven-open; they do not stress H-210 antecedents | separate **hypothesis** |
| H-tau16 | No bare FP in this catalog has `tau(w) > 16` | dual residual note only |

### Exact limits

- Highest package magnitude: `5e7`. Sample size: five FPs.
- Universality of R0 is **unresolved** beyond that regime.
- No theorem promotion. No `PROOF.md` edit from this loop note.
- No program-level verified / validated language without an executed `10^18`
  surface.

---

## Loop ledger summary

| Round | Candidate | Decision | Durable status |
| --- | --- | --- | --- |
| 1 | Branch-envelope inversion (tau-stratified max offsets) | REJECT novelty | **measured** on named regimes; not promoted as NIE insight |
| 1 parallel residual | Level-Set Compression Dichotomy (LSCD) | Keep as residual map | Full LSC **invalidated** on `11..2e6`; LSCD spill-only-on-`tau=4` = **hypothesis** + measured hold; UBC **theorem** untouched |
| 2 to 3 | z4 FP residual class R0 + algebraic form | Keep as residual catalog | **measured** on `p < 5e7`; universal R0 = **hypothesis**; historical z≥4⇒g=2 claim = **invalidated** |

## Unresolved (must stay labeled unresolved)

1. Whether any z4 FP outside R0 appears for `p >= 5e7`.
2. Whether the algebraic form `p = 30r-1`, `q = 30r+7`, `w = 30r` with `r`
   prime is forced for all future FPs, or only for the five known rows.
3. Whether R0 can be turned into a proved residual classification without
   smuggling a historical z≥4⇒g=2 claim revival (auditor gate: description of failures
   only, unless a separate proof package is approved).
4. Any high-scale (`10^18`) catalog surface for z4 FP shape
   (**unresolved**; not present).
5. Whether LSCD (spill only on early `tau(w)=4`) holds past `11..2e6`, or
   whether square / high-tau / large-alpha spills appear (**unresolved**).
6. Any high-scale (`10^18`) surface for LSC / LSCD residual geometry
   (**unresolved**; not present; required only if verified / validated
   language is ever sought).

## Explicit non-actions

- No edit to `PROOF.md`.
- No revival of historical z≥4⇒g=2 claim as theorem or corollary.
- No demotion of GWR, direct next-prime, UBC, or Prime-Square Proximity.
- No verified / validated claim language for this loop.
- No promotion of LSCD from hypothesis / measured residual to theorem.
- No conflation of LSCD co-minimal geometry with z4 FP class R0.

## Next pressure (handoff, not commitment)

- Extend z4 FP scan past `5e7` with the same R0 predicates and
  form check; record first out-of-R0 hit if any.
- Keep branch-envelope package as a **measured residual probe**, not as a
  novelty target, unless a new mechanism appears that is not just UBC
  stratification.
- Extend LSCD probe past `2e6` under the listed falsifiers (square spill,
  high-tau spill, large-alpha spill); keep LSC invalidated; keep UBC as
  theorem.
- Any future claim that wants verified / validated wording must add an
  executed `10^18` evidence surface per `AGENTS.md`.
