# PROOF.md — Identified Shortcomings

**Audit date:** 2026-07-07  
**Scope:** Full document, cross-checked against `lean-4/` mirror state and project artifacts  
**Severity key:** 🔴 blocks gap-free formalization · 🟠 weakens rigor or reproducibility · 🟡 clarity / maintenance

---

## 1. Proof-Structure Gaps (Mathematical)

### 🔴 S1 — Prime-Square Proximity: modulus-link density step is not rigorous

**Location:** `PROOF.md` lines 651–666 (Prime-Square Proximity Theorem)

**Issue:** The proof asserts that “available prime density > M satisfying h_m > sqrt(r) is strictly less than the density required to perfectly tile the remaining M-rough composite rows without collision,” and concludes “the modulus-link structure must intersect.”

This step lacks:

- A formal definition of “density required to tile”
- A counting lemma connecting M-rough rows to admissible least prime factors
- An explicit contradiction derived from stated inequalities

**Evidence:** Lean mirror has `near_root_exclusion_bound` (algebraic core, proved) but `prime_square_proximity_theorem` is trivial (`∃ C, r² - p ≤ C` by reflexivity). `PROOF.md` line 37 acknowledges Lean carries “structural axioms pending full machine-checked derivation.”

**Impact:** Pillar 3 (universal bounded compression) cannot be machine-checked end-to-end until this step is repaired or replaced.

---

### 🔴 S2 — Twin-Prime Resonance: informal competitive-minimum argument

**Location:** `PROOF.md` lines 676–704

**Issue:** Step 3 uses non-rigorous language:

- “overwhelmingly semiprimes”
- “the gap will inevitably contain other semiprimes with lower divisor counts”
- Parenthetical dismissal of “rare contrived integers” without exclusion proof

The sub-claim “4+ zeros in R(w) ⟺ w ≡ 0 (mod 30)” is argued by example (“e.g., {2,3,7}”) rather than exhaustive case analysis over the remainder-vector definition.

**Impact:** Listed as “proved, universal” in theorem stack (line 738) but not formalizable as stated.

---

### 🟠 S3 — Finite bases presented adjacent to universal theorems without epistemic separation

**Location:** Headline (lines 40–44), Finite Base Lemma (349–369), Finite Bounded-Compression Base (555–587), Audit Tables (706–726)

**Issue:** Universal theorems (GWR maximizer, bounded compression) are proved **conditional on** exhaustive computation for:

| Base | Scale |
|------|-------|
| GWR earlier-integer closure | 220,336,055 gaps; 826,172,978 earlier integers; `p < 5×10⁹` |
| Bounded-compression small side | 542,081 gaps; `q < ceil(e¹⁶)` |
| Residual K=128 elimination | Finite windows up to ~10¹⁵ |

The document states these are “not limits on the theorems” (line 44) while simultaneously using them as essential proof steps. Status vocabulary blurs **proved by mathematics** vs **certified by enumeration**.

**Impact:** Readers (and Lean formalizers) cannot tell which claims require certificate infrastructure vs analytic proof.

---

### 🟠 S4 — Residual K=128 lemma scope vs. headline wording

**Location:** Lines 589–620

**Issue:** The document correctly notes this is “not a global occupancy theorem” and “does not prove that every prime gap containing a divisor-count-4 integer has its first such integer within 128.” The theorem stack (line 735) labels it “proved, stated hypotheses” — accurate — but the headline pillar 3 narrative can read as if all branches are analytically closed.

**Impact:** Scope creep risk in downstream citations and Lean planning.

---

### 🟡 S5 — Bertrand used without explicit hypothesis packaging

**Location:** Witness Threshold Lemma (307–311), Large-Divisor Adjacent Closure (417–419)

**Issue:** Bertrand’s postulate is invoked for consecutive-prime gaps (`q < 2p`). This is standard but should be stated as an explicit imported classical lemma with clear audit status, per PGS state-separation discipline.

**Impact:** Minor for mathematics; significant for Lean contract compliance and external review.

---

### 🟡 S6 — τ(n) ≤ 2√n used without citation or proof pointer

**Location:** Large-Divisor Adjacent Closure, line 474

**Issue:** “For every integer n, tau(n) <= 2sqrt(n)” is stated as elementary fact. True, but proof is non-trivial (divisor pairs). No lemma reference in document.

**Impact:** Small gap in self-containedness.

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

### 🟠 R1 — Audit tables lack pinned reproduction commands

**Location:** Lines 360–366, 574–585, 716–726

**Issue:** Tables report exact counts and zero failures but `PROOF.md` does not specify:

- Script entry points and versions
- Input prime tables / sieves used
- Hash or path of certificate artifacts
- Environment pins (Python, gmpy2, etc.)

Supporting scripts exist under `research/02-gwr-dni/scripts/proof/` but linkage is implicit.

---

### 🟠 R2 — No single certificate schema for finite-base claims

**Issue:** Multiple independent verification surfaces (GWR base, bounded-compression base, K=128 residual, weak-LFCL R2) use different artifact formats. No unified “finite lemma certificate” contract for external audit or Lean import.

---

### 🟡 R3 — Stress sample at ~10¹² cited without artifact path

**Location:** Lines 724–726

**Issue:** “137,771 prime gaps … 0 unresolved cases” — no reproducibility anchor in `PROOF.md`.

---

## 4. Presentation & Maintenance

### 🟡 P1 — Theorem stack status column over-unifies proof modalities

**Location:** Lines 728–738

**Issue:** Single “proved, universal” label applied to analytically proved items, finite-certified items, and items with informal steps (twin-prime). Should use multi-axis status (see goals).

---

### 🟡 P2 — Boundary disclaimer buried

**Location:** Lines 34–38

**Issue:** Important boundary (prefix attainment `w - p`, not raw gap `q - p`; not PNT/RH/Cramér for gaps) appears early but pillar 3 headline (lines 29–32) emphasizes Cramér scale prominently. Risk of misreading by external audience.

---

### 🟡 P3 — Twin-Prime Resonance not integrated into main proof spine

**Location:** Section after PSP, before Audit Tables

**Issue:** Appears as addendum with different proof style. Unclear dependency on GWR theorem, finite bases, or standalone. Enhancement should clarify logical position (corollary? separate theorem? empirical conjecture hardened to proof?).

---

### 🟡 P4 — Document status footer claims full closure

**Location:** Lines 740–750

**Issue:** “universal bounded-compression limit … deterministically established across all prime gap branches” — true under project interpretation, but S1 shows square-branch analytic closure is not fully rigorous in prose. Footer should track enhancement status.

---

## 5. Priority Summary

| ID | Shortcoming | Severity | Blocks Lean? |
|----|-------------|----------|------------|
| S1 | PSP modulus-link density step | 🔴 | Yes (pillar 3) |
| S2 | Twin-Prime informal steps | 🔴 | Yes |
| S3 | Finite vs universal epistemic blur | 🟠 | Yes (architecture) |
| R1 | Reproducibility anchors missing | 🟠 | Yes (certificates) |
| R2 | No certificate schema | 🟠 | Yes |
| S4 | K=128 scope vs narrative | 🟠 | Partial |
| S5 | Bertrand packaging | 🟡 | Partial |
| S6 | τ ≤ 2√n pointer | 🟡 | No |
| P1–P4 | Presentation / maintenance | 🟡 | No |

---

## 6. What Is *Not* a Shortcoming

To avoid false “enhancement” scope creep, the following are **sound** in current `PROOF.md`:

- Direct next-prime algorithm correctness (lines 109–122), modulo τ↔prime lemma
- Ordered Comparison Lemma (189–213) — complete analytic proof
- Divisor-count tail (226–255) — complete
- Prime-square case for GWR earlier side (277–303) — complete given hypotheses
- Witness threshold machinery (305–347) — complete given Bertrand
- Short Divisor-Average Lemma (371–410) — complete
- Large-Divisor Adjacent Closure (412–539) — complete given prior lemmas and finite base

These should be **preserved and isolated** during enhancement, not rewritten.