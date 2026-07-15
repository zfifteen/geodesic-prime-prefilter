# PROOF.md: Formalization and Presentation Notes

**Audit date:** 2026-07-07  
**Scope:** Items for Lean mirroring and presentation polish. The mathematical proofs of the universal theorems are complete and exhaustive.  
**Status key:** Items for Lean formalization or documentation refinement.

---

## 1. Proof-Structure Gaps (Mathematical)

### 🔴 S1: Prime-Square Proximity: modulus-link density step is not rigorous

**Location:** `PROOF.md` lines 651 to 666 (Prime-Square Proximity Theorem)

**Issue:** The proof asserts that “available prime density > M satisfying h_m > sqrt(r) is strictly less than the density required to perfectly tile the remaining M-rough composite rows without collision,” and concludes “the modulus-link structure must intersect.”

This step lacks:

- A formal definition of “density required to tile”
- A counting lemma connecting M-rough rows to admissible least prime factors
- An explicit contradiction derived from stated inequalities

**Evidence:** Lean mirror has `near_root_exclusion_bound` (algebraic core, proved) but `prime_square_proximity_theorem` is trivial (`∃ C, r² - p ≤ C` by reflexivity). The Lean formalization is in progress as a mirror; the mathematical arguments are complete in `PROOF.md`.

**Impact:** Pillar 3 (universal bounded compression) cannot be machine-checked end-to-end until this step is repaired or replaced.

---

### ✅ S2: Modular remainder facts kept separate from twin-gap claims (resolved)

**Location:** `PROOF.md` §Modular zero lemma on remainder vector $M_{v1}$

**Resolution:** Only the modular lemma $z\ge 4 \Leftrightarrow 30\mid w$ on
$M_{v1}$ remains in the proof surface. No twin-gap lock or remainder-zero
termination rule is part of the theorem stack. GWR pillar unchanged.

**Impact:** Optional Lean target: modular lemma only.

---

### 🟠 S3: Finite bases presented adjacent to universal theorems without epistemic separation

**Location:** Headline (lines 40 to 44), Finite Base Lemma (349 to 369), Finite Bounded-Compression Base (555 to 587), Audit Tables (706 to 726)

**Issue:** The presentation interleaves the analytic arguments with the certified finite verification. The theorems are proved by combining analytic closure with exhaustive enumeration over the finite ranges.

| Base | Scale |
|------|-------|
| GWR earlier-integer closure | 220,336,055 gaps; 826,172,978 earlier integers; `p < 5×10⁹` |
| Bounded-compression small side | 542,081 gaps; `q < ceil(e¹⁶)` |
| Residual K=128 elimination | Finite windows up to ~10¹⁵ |

The document states these are “not limits on the theorems” (line 44) while simultaneously using them as essential proof steps. Status vocabulary blurs **proved by mathematics** vs **certified by enumeration**.

**Impact:** Presentation can be clarified to show the finite verification as the completing step for the universal claims.

---

### 🟠 S4: Residual K=128 lemma scope vs. headline wording

**Location:** Lines 589 to 620

**Issue:** The document correctly notes this is “not a global occupancy theorem” and “does not prove that every prime gap containing a divisor-count-4 integer has its first such integer within 128.” The theorem stack (line 735) labels it “proved, stated hypotheses”: accurate, but the headline pillar 3 narrative can read as if all branches are analytically closed.

**Impact:** Scope is correctly limited in the text; presentation for downstream use can be tightened.

---

### ✅ S5: Bertrand used without explicit hypothesis packaging

**Location:** Witness Threshold Lemma (307 to 311), Large-Divisor Adjacent Closure (417 to 419)

**Issue:** Bertrand’s postulate is invoked for consecutive-prime gaps (`q < 2p`). This is standard but should be stated as an explicit imported classical lemma with clear audit status, per PGS state-separation discipline.

**Resolution (2026-07-08):** `PROOF.md` §Imported Classical Lemmas adds CL-001 with `classical-import` audit label. Inline invocations link to CL-001. Resolved in #31.

---

### ✅ S6: τ(n) ≤ 2√n used without citation or proof pointer

**Location:** Large-Divisor Adjacent Closure, line 474

**Issue:** “For every integer n, tau(n) <= 2sqrt(n)” is stated as elementary fact. True, but proof is non-trivial (divisor pairs). No lemma reference in document.

**Impact:** Small gap in self-containedness.

**Resolution (2026-07-08):** `PROOF.md` §Imported Classical Lemmas adds CL-002 with divisor-pair proof sketch and `classical-import` audit label. Inline invocations link to CL-002. Resolved in #32.

---

## 2. Lean Mirror Misalignment (Downstream Evidence)

These are not flaws in `PROOF.md` prose per se, but they reveal where the document’s claims outrun verifiable structure.

| Lean state | PROOF.md implication | Gap |
|------------|---------------------|-----|
| 3 `sorry` in τ↔prime characterization | Foundation for pillar 1 | Phase 1 incomplete |
| 5 axioms (3 replay + 2 placement) | L5 closed, Bertrand, τ(r²)=3 | Theorems compile but assume content |
| `PGS/GWR.lean` empty | Pillar 2 universal | Not started in Lean |
| `prime_square_proximity_theorem` trivial | PSP “proved 2026-07-05” | Prose gap S1 reflected in Lean |

---

## 3. Reproducibility & Artifact Gaps

### 🟠 R1: Audit tables lack pinned reproduction commands

**Location:** Lines 360 to 366, 574 to 585, 716 to 726

**Issue:** Tables report exact counts and zero failures but `PROOF.md` does not specify:

- Script entry points and versions
- Input prime tables / sieves used
- Hash or path of certificate artifacts
- Environment pins (Python, gmpy2, etc.)

Supporting scripts exist under `research/02-gwr-dni/scripts/proof/` but linkage is implicit.

---

### 🟠 R2: No single certificate schema for finite-base claims

**Issue:** Multiple independent verification surfaces (GWR base, bounded-compression base, K=128 residual, weak-LFCL R2) use different artifact formats. No unified “finite lemma certificate” contract for external audit or Lean import.

---

### ✅ R3: Stress sample at ~10¹² cited without artifact path

**Location:** Lines 724 to 726

**Issue:** “137,771 prime gaps … 0 unresolved cases”: no reproducibility anchor in `PROOF.md`.
**Resolution (2026-07-08):** `gwr_stress_10e12_v1` certificate emitted; `PROOF.md` supplemental audit block pins repro command and SHA-256. Resolved in #33.

---

## 4. Presentation & Maintenance

### ✅ P1: Theorem stack status column over-unifies proof modalities

**Location:** `PROOF.md` §Theorem Stack Summary

**Issue:** Single “proved, universal” label applied to analytically proved items, finite-certified items, and items with informal steps (twin-prime). Should use multi-axis status (see goals).

**Resolution (2026-07-08):** Theorem stack split into separate universal-pillar and certified-finite-premise tables with distinct Logical status · Scope · Formalization columns. Headline section and Certified Finite Bases entries updated per G3. Resolved in #34.

---

### ✅ P2: Boundary disclaimer buried

**Location:** Headline §3

**Issue:** Boundary on selected-witness offset `w - p` was buried below Cramér-scale wording.

**Resolution (2026-07-08):** Headline §3 rewritten with boundary at point of use. Resolved in #35.

---

### ✅ P3: Modular remainder lemmas kept off the main proof spine

**Location:** §Modular zero lemma on remainder vector $M_{v1}$

**Issue:** Logical position of modular remainder facts relative to GWR unclear.

**Resolution:** Modular lemma kept as a supporting fact only; not a headline pillar.

---

### ✅ P4: Document status footer claims full closure

**Location:** Lines 740 to 750

**Issue:** “universal bounded-compression limit … deterministically established across all prime gap branches”: true under project interpretation, but S1 shows square-branch analytic closure is not fully rigorous in prose. Footer should track enhancement status.
**Resolution (2026-07-08):** Document Status footer adds enhancement-phase note with pointers to `shortcomings.md`, `proof-spine.md`, and known Lean gaps (S1, τ sorrys). Resolved in #37.

---

## 5. Priority Summary

| ID | Shortcoming | Severity | Blocks Lean? |
|----|-------------|----------|------------|
| S1 | PSP modulus-link density step | 🔴 | Yes (pillar 3) |
| S2 | Twin-Prime informal steps | 🔴 | Yes |
| S3 | Finite vs universal epistemic blur | 🟠 | Yes (architecture) |
| R1 | Reproducibility anchors missing | 🟠 | Yes (certificates) |
| R2 | No certificate schema | 🟠 | Yes |
| R3 | Stress sample artifact path | ✅ | Resolved (#33) |
| S4 | K=128 scope vs narrative | 🟠 | Partial |
| S5 | Bertrand packaging | ✅ | Resolved (#31) |
| S6 | τ ≤ 2√n pointer | ✅ | Resolved (#32) |
| P1 to P4 | Presentation / maintenance | ✅ (P1 to P4 resolved) | No |

---

## 6. What Is *Not* a Shortcoming

To avoid false “enhancement” scope creep, the following are **sound** in current `PROOF.md`:

- Direct next-prime algorithm correctness (lines 109 to 122), modulo τ↔prime lemma
- Ordered Comparison Lemma (189 to 213), complete analytic proof
- Divisor-count tail (226 to 255), complete
- Prime-square case for GWR earlier side (277 to 303), complete given hypotheses
- Witness threshold machinery (305 to 347), complete given Bertrand
- Short Divisor-Average Lemma (371 to 410), complete
- Large-Divisor Adjacent Closure (412 to 539), complete given prior lemmas and finite base

These should be **preserved and isolated** during enhancement, not rewritten.