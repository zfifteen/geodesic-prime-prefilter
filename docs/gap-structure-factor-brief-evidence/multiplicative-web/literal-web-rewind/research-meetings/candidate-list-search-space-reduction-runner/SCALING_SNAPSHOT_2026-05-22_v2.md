# PGA Grammar Pruner – Scaling Snapshot v2 (2026-05-22)

**Purpose**: Current citable state of the public grammar-rule lever under two distinct measurement surfaces. Surfaces are deliberately kept separate.

## 1. Frozen Toy Evidence Surface (Validated Pre-computed Motifs)

This is the protected benchmark surface using the original pre-computed public structural motifs for the 10-N toy corpus.

- Rule set: **84 rules** (PG-001 through PG-084)
- Average reduction: **65.45%**
- Primary cases (8 × `o2_d4_a2_d4_odd@mid`): **141/198 = 71.21%**
- Secondary cases (2 × `o4_d4_a4_d4_odd@mid`): **84/198 = 42.42%**
- Total pruned instances across corpus: 1296
- Status: Reproducible. The toy batch now consistently reports these numbers when run on the frozen validated motifs.

This surface produced the breakthrough result (originally 69.19% on the dominant motif, now 71.21% with the expanded rule set). It remains the strongest, fully validated claim for the current rule inventory.

## 2. Live Derivation Surface (Real Public Motif Derivation on Raw N)

This surface uses the live `derive_public_motif()` function on freshly generated semiprimes.

- Current best measured result on real derived public motifs at ~58–66 bits: **~45%** average reduction.
- Performance is still materially limited by coverage gaps on exotic/high-a attractor families that become common at these scales but were underrepresented in the original mining surfaces.
- The gap between this surface and the frozen toy evidence surface is the primary remaining engineering signal.

## 3. Ladder Instrument Status

- The scaling ladder (`pga_grammar_pruner_ladder.py`) has been rewritten with an explicit `--mode synthetic|real` split.
- Synthetic mode: fully deterministic motif sequence (no hidden randomness).
- Real mode: uses deterministic public semiprimes and records derivation failures as unresolved (no synthetic substitution).
- No new ladder curves have been generated since the instrument was corrected.

## 4. Next Decision Gate

Two clean options, kept separate by surface:

**Option A – Deterministic Synthetic Ladder First**  
Run a clean, reproducible synthetic-mode ladder across 48–80 bits (or higher) to establish trend lines quickly and cheaply. This gives visibility into scaling behavior without waiting on derivation performance.

**Option B – Limited Real Derivation on Deterministic 64–80 Bit Public N**  
Select a small, fixed set of deterministic public semiprimes in the 64–80 bit range, derive their public motifs live, and measure reduction. This provides the first honest end-to-end scaling data beyond the toy corpus, at the cost of slower execution and potential unresolved cases.

**Recommended sequence (as lead)**: Run Option A first for trend visibility, then Option B on a modest deterministic set to ground the trends in real derivation results.

---

This snapshot deliberately does not blend the two surfaces. The 71.21% figure on the frozen toy evidence surface is the current strongest validated claim. The ~45% figure on the live derivation surface is the current honest scaling reality check. Keeping them distinct preserves the integrity of both measurements.
