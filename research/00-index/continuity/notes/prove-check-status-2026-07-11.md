# Prove-check continuity note

**Date:** 2026-07-11  
**Role:** Continuity Scribe (after auditor prove-check pressure)  
**Authority:** `PROOF.md` only for theorem status  
**Implementer package this turn:** none (no new code files)

Writing order for this note:

```text
proved -> withdrawn -> next experiment
```

Within each block the default explanatory order still holds when a claim is unpacked:

```text
observable object -> ordinary-language mechanism -> project term -> formal definition -> measured/proved status -> exact limits
```

This note does **not** edit `PROOF.md`. It does **not** promote measured residuals to theorems. It does **not** use program-level verified / validated language (no new executed `10^18` surface in this package).

---

## 1. Proved

### Observable objects

Start from a known prime `p`. Walk later integers by exact divisor count `tau`.
The first integer with `tau = 2` is the next prime `q`. Between `p` and `q`,
when the interior is nonempty, some composites have fewer divisors than others.
The leftmost interior integer with the smallest divisor count is the GWR
selected witness `w`. On the square branch that witness is a prime square
`r^2`. Separately, for the fixed modulus vector
`M_v1 = {2, 3, 5, 7, 30, 210, 2310}`, the zero-count `z(w)` records how many
of those moduli divide `w`.

### Ordinary-language mechanisms

1. **Next prime by divisor count.** Among integers after `p`, primality is
   exactly `tau(n) = 2`. The first such integer is the successor prime.
2. **Leftmost min-divisor carrier.** Inside a gap, the first integer that hits
   the gap-minimum divisor load is the structural selected witness.
3. **Bounded placement of that witness.** That selected witness always sits
   within a Cramér-scale window of `p`, measured as offset `w - p` (not as raw
   gap length `q - p`).
4. **Square-branch proximity.** When the selected witness is a prime square,
   that square sits within the same scale window of `p`.
5. **Four zeros means divisible by 30.** On the fixed vector `M_v1`, having four
   or more remainder zeros is exactly the statement that `30` divides `w`.

### Project terms and formal statements (status: **theorem**)

| Object | Project term | Formal bound / identity | Status |
| --- | --- | --- | --- |
| Successor endpoint | Direct deterministic next-prime rule | `q = min{n > p : tau(n) = 2}` | **theorem** (`PROOF.md`) |
| Selected interior witness | Interior Maximizer (GWR) | `w = min{n in I : tau(n) = min_m tau(m)}` maximizer of `F(n) = (1 - tau(n)/2) log n` | **theorem** (`PROOF.md`) |
| Selected-witness offset | Universal bounded compression (UBC) | `w - p <= max(64, ceil(0.5 * log(q)^2))` | **theorem** (`PROOF.md`) |
| Square-branch offset | Prime-Square Proximity Theorem | `r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))` | **theorem** (`PROOF.md`) |
| Zero-count lattice on `M_v1` | Modular zero lemma | `z(w) >= 4  <=>  30 \| w` | **theorem** (`PROOF.md`, fixed vector only) |

Supporting finite premises named inside `PROOF.md` (proof machinery, not free-standing universal theorems):

- `gwr_finite_base_v1`
- `bounded_compression_base_v1`
- `residual_k128_v1`

### Exact limits on the proved layer

- UBC bounds the **selected-witness offset** `w - p`, not every classical form of
  raw gap size `q - p`.
- UBC and Prime-Square Proximity do **not** by themselves prove RH, PNT, or
  RSA-scale factorization.
- The modular zero lemma is proved **only** for the fixed vector `M_v1`. It is
  not a twin-gap lock.
- Finite premises stay finite. They close analytic steps; they do not re-open
  proved universals as "only checked up to X."
- Theorem status is not bounded by audit tables or mid-scale probes.

### Related measured corroboration (not theorem bounds)

| Surface | Status | Limit |
| --- | --- | --- |
| Generator `11..1000000` and decade ladder through `10^18` | **measured** / production generator evidence | implementation evidence; does not bound theorems |
| Square-branch audit `4*10^8 .. 5*10^8` | **audit corroboration** on that band | not a theorem bound; not a license for RH/PNT inflation |

---

## 2. Withdrawn

### Observable object

A Super-Signal style reading looks at the GWR witness remainder vector on
`M_v1` and treats a high zero-count as a twin-gap certificate.

### Ordinary-language mechanism (historical, false)

"If the selected witness is divisible by enough of the small moduli that four
or more remainders are zero, the gap must be a twin and the next integer must
be the next prime."

### Project term and withdrawn claim

**Twin-Prime Resonance (GWR Super-Signal)** historical packaging:

```text
z(w) >= 4  =>  g = 2
```

and the stronger packaging that `w + 1` is identically `q`.

| Layer | Status |
| --- | --- |
| Universal implication `z(w) >= 4 => g = 2` | **invalidated** (`PROOF.md`, 2026-07-09) |
| Historical corollary packaging from GWR + remainder analysis | **withdrawn** |
| Broken competitor step (non-twin 30-multiple cannot be leftmost min-`tau`) | **invalidated** (later interiors may **tie** `tau(w)`) |
| Modular zero lemma | **kept** as **theorem** (not withdrawn) |
| GWR maximizer / next-prime / UBC / Prime-Square Proximity | **kept** as **theorem** (not demoted) |

### Pinned counterexamples (certificates)

| p | q | g | w | tau(w) | z(w) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 17666309 | 17666317 | 8 | 17666310 | 16 | 4 |
| 22284029 | 22284037 | 8 | 22284030 | 16 | 4 |

Paths:

- `docs/proof-enhancements/certificates/twin_prime_resonance_invalidated_v1.json`
- `docs/proof-enhancements/certificates/counterexamples/ce_17666309.json`
- `docs/proof-enhancements/certificates/counterexamples/ce_22284029.json`
- Repro: `python3 docs/proof-enhancements/scripts/verify_super_signal_counterexamples.py`

### Comparative leftness packaging (experiment-local, not a theorem revival)

Share-driven claim that **leftmost** min-`tau` is necessary for modular gap
closure is **falsified** on measured regime `p <= 2.5e7`
(`experiments/leftmost-min-modular-closure-falsification-2026-07/`). That does
not restore Super-Signal. It does not demote GWR as maximizer of `F`.

### Explicit non-revival

- Do not cite Super-Signal as a proved corollary.
- Do not write "often twin below bound" as a universal twin-gap law.
- Residual class R0 and related catalogs describe **observed failures** only.
  They are **not** a proved repair of the form `z >= 4 => (g = 2 or R0)`.
- Finite "often twin" residue stays **measured** only.

---

## 3. Next experiment

These are handoff pressures, not commitments and not theorem targets unless a
separate proof package is approved. Keep each item status-labeled.

### Program frontiers (from `ACTIVE_TARGET.md`)

| Pressure | Status label | Notes |
| --- | --- | --- |
| Lean 4: promote `near_root_exclusion_bound` and `prime_square_proximity_theorem` from axioms to derived theorems | **implementation** / formalization | `lean-4/PGS/ChamberReset.lean` |
| External review and publication of Prime-Square Proximity | **process** | proof already **theorem** in `PROOF.md` |
| Square-branch audit sweeps on new regimes | **audit corroboration** | hourly queue; do not re-litigate closed theorems |
| RSA endpoint resolver maturation | **unresolved** research track | separate cryptology program |

### Residual research pressures (hypothesis / unresolved only)

| Pressure | Status | Exact limit |
| --- | --- | --- |
| Super-Signal FP outside residual class R0 at larger scale | **unresolved** / **hypothesis** that all FPs stay in R0 | full sieve through `5e7` and band `[5e7, 6e7)` are **measured**; universality **unresolved** |
| Mechanism why Super-Signal FPs force `g = 8` on the R0 form | **unresolved** | catalog is not a generative proof |
| Level-Set Compression Dichotomy (LSCD): spill only on early `tau(w) = 4` | **hypothesis**, measured hold on `11..2e6` | full LSC **invalidated**; UBC **theorem** untouched |
| Rightmost min-`tau` zero-mismatch beyond `2.5e7` | **unresolved** (measured absence only so far) | not a selector law |
| Min-`tau` tie index histogram for `z >= 4` and `g > 2` | optional **new hypothesis** package | not a rescue of Super-Signal or leftness necessity |
| Any residual wanting program-level verified / validated wording | blocked until executed `10^18` surface | `AGENTS.md` Mandatory 10^18 Evidence Surface |

### What not to run as "next experiment"

- Do not re-open Super-Signal as theorem or corollary.
- Do not re-open Hypothesis U (unique min + `z >= 4 => g = 2`): already
  **invalidated**.
- Do not demote GWR, next-prime, UBC, Prime-Square Proximity, or the modular
  zero lemma.
- Do not treat audit green on mid-scale bands as implementation validation of a
  universal theorem.
- Do not change program continuity center unless the user asks.

### Pointers for residual packages already on disk

| Path | Role |
| --- | --- |
| `research/00-index/continuity/notes/insight-ooda-proof-loop.md` | Loop ledger (R0, LSCD, branch-envelope) |
| `experiments/leftmost-min-modular-closure-falsification-2026-07/CONTINUITY_HANDOFF.md` | Leftness falsification handoff |
| `experiments/min-tau-level-set-compression-2026-07/FINDINGS.md` | LSC / LSCD residual |
| `research/16-predictions/probes/super-signal-fp-signature-2026-07/README.md` | Super-Signal FP catalog |
| `research/00-index/continuity/ACTIVE_TARGET.md` | Program center and hourly audit |

---

## Unresolved (must stay labeled unresolved)

1. Universal residual law after Super-Signal kill (no closed replacement).
2. Super-Signal FP outside R0 for larger `p`.
3. Generative mechanism for R0 form and `g = 8`.
4. LSCD hold past `11..2e6` (square spill, high-tau spill, large-alpha spill).
5. Rightmost and other non-leftmost tie operationalizations beyond named regimes.
6. High-scale (`10^18`) residual catalogs if program-level verified language is
   ever sought for those residual families.
7. Lean formalization of proved pillars still **in progress** (not a math
   demotion).

---

## Scribe output contract

| Item | Value |
| --- | --- |
| Paths written | `research/00-index/continuity/notes/prove-check-status-2026-07-11.md` |
| Status labels used | theorem, proved, invalidated, withdrawn, measured, audit corroboration, hypothesis, unresolved, implementation / formalization, process |
| Forbidden words avoided | verified, validated (program-level) |
| En dashes | none |
| `PROOF.md` edits | none |
