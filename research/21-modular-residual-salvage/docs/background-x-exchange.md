# Background: Super-Signal X exchange (2026-07-08 to 2026-07-10)

This note freezes the public conversation that produced (1) the Super-Signal
counterexample, (2) a classical salvage attempt, and (3) the program's
deterministic refusal of that salvage as PGS inference.

Readers who only see a residual-set formula later in this chapter need this
context: the salvage was **generous adversarial culture**, not the research
target; the research target is the **deterministic kernel** buried under
probabilistic packaging.

## Actors

| Handle | Display | Role in thread |
| --- | --- | --- |
| `@alltheputs` (Fate) | Program owner | Posted Super-Signal claim; accepted CE; refused classical salvage shape |
| `@0x2719` (SomeDude) | External auditor | Built CE package; full factor audit; offered residual salvage |

Conversation id: `2074694442661859336`

## Timeline (chronological)

### 1. Opening claim (`@alltheputs`)

- **URL:** https://x.com/alltheputs/status/2074694442661859336
- **When:** 2026-07-08 ~03:17 UTC
- **Content (summary):**
  - Gaps are structured interiors; structure is read via divisor count `tau`.
  - **GWR witness** = leftmost interior with minimum `tau`.
  - Remainder vector on moduli `M = (2, 3, 5, 7, 30, 210, 2310)`.
  - **Twin-Prime Resonance / GWR Super-Signal (claimed):** if the GWR witness
    has four or more remainder zeros, then the gap is a twin gap (`g = 2`) and
    the next prime is `w + 1`.
  - Intuition offered: a multiple of 30 has high `tau`, so in a larger gap some
    earlier interior should beat it; only a single-interior twin gap lets that
    density remain GWR.
  - Evidence cited in post: scan to `2e6` (no counterexample); earlier interior
    lane to `1.5e6` (all super-signal cases twins).
  - Language in the post treated the rule as a **proved twin-gap lock**.

**Status of that language today:** the universal implication is **invalidated**
in `PROOF.md`. Finite empty scans never restored universality.

### 2. Disproof by counterexample (`@0x2719`)

- **URL:** https://x.com/0x2719/status/2074994936450371679
- **When:** 2026-07-08 ~23:11 UTC
- **Claim under attack:**

```text
z(w) >= 4 at GWR  =>  g = 2
```

- **Counterexample:**

| Field | Value |
| --- | ---: |
| p | 17,666,309 |
| q | 17,666,317 |
| g | 8 |
| GWR w | 17,666,310 |
| tau(w) | 16 |
| R(w) on M | (0, 0, 0, 4, 0, 60, 1740) |
| z(w) | 4 |

- **Mechanism diagnosis (their contribution):** later interiors **tie**
  `tau = 16` rather than strictly beating the 30-multiple. GWR selects the
  **leftmost** minimum, so the multiple of 30 remains the witness inside a
  non-twin gap.
- **Failed assumption named:** larger gap implies some interior with strictly
  fewer divisors than the multiple of 30.

Repo certificate: `docs/proof-enhancements/certificates/counterexamples/ce_17666309.json`
(source line credits this post; dual-audited 2026-07-09).

### 3. Full prime-factor audit (`@0x2719`)

- **URL:** https://x.com/0x2719/status/2074995293540786673
- **When:** 2026-07-08 ~23:13 UTC
- **Content:** every interior factored; `tau` from exponents; remainder vector;
  pipeline diagram; formal non-implication:

```text
[z(w) >= 4 and w = GWR]  does not imply  [q - p = 2]
```

This is the dual-audit trail. Factorization is used as **audit**, not as a new
PGS inference rule.

### 4. Acceptance of CE (`@alltheputs`)

- **URL:** https://x.com/alltheputs/status/2075117318670082374
- **When:** 2026-07-09 ~07:18 UTC
- **Content:** thanks; validation appreciated; test surface was too small.

### 5. Classical salvage attempt (`@0x2719`)

- **URL:** https://x.com/0x2719/status/2075245771482681616
- **When:** 2026-07-09 ~15:48 UTC
- **Content (paraphrase of residual packaging):**
  - Around dense composites (products of small primes), neighbors are "likely"
    prime.
  - Example: `2 * 3 * 5 = 30` then 29 and 31 (with 31 less than 7 squared).
  - Example: `2 * 3 * 5 * 7 = 210` then check 209 and 211 against primes up to
    sqrt (11, 13, ...).
  - 209 composite, 211 prime.
  - Does not always find prime pairs, but plus or minus one is "often" prime
    near composites with many small factors.
  - Remaining work: trial primes not in the product, up to the square root.
  - Framed as better than guessing when hunting primes.

**Program judgment:** constructive intent, **wrong shape** for PGS inference
(probabilistic density + classical trial ladder).

### 6. Frame note (`@alltheputs`)

- **URL:** https://x.com/alltheputs/status/2075514553132003754
- **When:** 2026-07-10 ~09:36 UTC
- **Content (summary):**
  - Thank you for trying to leave something standing after the kill.
  - CE accepted fully; universal Super-Signal cannot stand.
  - Salvage set aside without dismissing the spirit.
  - PGS is deterministic: resolves, returns unresolved, or is invalidated;
    does not emit likelihood.
  - Examples: GWR leftmost min; explicit unresolved; modular lemma
    `z >= 4 <=> 30 | w` on `M`; generator `p -> q` or unresolved with audit
    after generation.
  - Status separation: invalidated lock; still-standing pillars; salvage
    outside the spine for now.
  - Bottom line: keep the disproof; do not promote salvage into the spine;
    advance only on rules that force a state, not on rules that make a state
    more likely.

### 7. Residual approach follow-up (`@alltheputs`)

- **URL:** https://x.com/alltheputs/status/2075525763927871918
- **When:** 2026-07-10 ~10:21 UTC
- **Content (summary):**
  - Extract deterministic residual core from the salvage (not density language).
  - Wheel `W` from modular zeros; residual set
    `R(n, W) = { primes r <= sqrt(n) not in W }`.
  - Empty residual => modular-closed; nonempty => residual-open (unresolved
    under this certificate, not a trial ladder).
  - Layer split: (A) soft density set aside; (B) trial audit-only;
    (C) residual partition as build surface.
  - Concrete rewrite of 30 / 210 / CE carrier `w = 17,666,310` without
    "likely."
  - Super-Signal universal lock stays dead.
  - Measured note: on a small regime, modular-closed among z>=4 GWR carriers
    is rare (toy twin around 30 dominates the closed class).
  - Pipeline: carrier -> wheel -> residual set -> closed | open ->
    resolved or unresolved under this certificate.

This post is the public statement of the approach formalized in this chapter.

## What entered the repository from this exchange

| Artifact | Status |
| --- | --- |
| `ce_17666309` | pinned invalidating CE (from `@0x2719`) |
| `ce_22284029` | second pinned CE (independent class-A scan) |
| `PROOF.md` Twin-Prime Resonance section | universal implication **invalidated** |
| Modular lemma on `M_v1` | **proved** (survives) |
| Competitor lemma (strict tau beater in larger gaps) | **false** |
| Hypothesis U (unique tau-min repair) | later **falsified** in experiment suite |
| H-210, H-tau16 | secondary **hypotheses / measured** (not theorems) |

## Perspective for this chapter

```text
Accept:   CE arithmetic and competitor-lemma diagnosis
Refuse:   "likely / often" density and trial-as-decision-path
Extract:  deterministic residual partition under a fixed wheel
Build:    residual-open / modular-closed state language;
          deeper modular seats under explicit hypothesis discipline
```

Do not read this chapter as a rehabilitation of Super-Signal.
Do not read the salvage post as program doctrine.
Do read both as the origin of a residual-accounting object that can be stated
without probability.

## Thread map (links)

1. https://x.com/alltheputs/status/2074694442661859336 (claim)
2. https://x.com/0x2719/status/2074994936450371679 (CE)
3. https://x.com/0x2719/status/2074995293540786673 (factor audit)
4. https://x.com/alltheputs/status/2075117318670082374 (accept CE)
5. https://x.com/0x2719/status/2075245771482681616 (classical salvage)
6. https://x.com/alltheputs/status/2075514553132003754 (frame note)
7. https://x.com/alltheputs/status/2075525763927871918 (residual approach follow-up)
