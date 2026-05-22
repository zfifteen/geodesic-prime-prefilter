# PGA Grammar Pruner – Scaling Snapshot (2026-05-22)

**Status**: Active fail-fast scaling research toward Wikipedia RSA challenge numbers (public-only, deterministic, PGS grammar rules).

**Goal of this document**: Provide a single, citable snapshot of measured reduction power when the pruner is fed *real public motifs* derived from actual semiprimes at increasing bit lengths.

## Executive Summary

- Public motif derivation (GWR/DNI attractor + phase from the production gap-grammar engine) is now operational and scales to at least 74 bits.
- On real derived public motifs at ~60 bits the current rule set (81 rules, PG-001–PG-081) delivers **41.16%** average hypothesis-space reduction.
- On a real-derivation ladder (48–72 bits, 15 samples/level) average reduction declines gradually from **38.4%** (48 bits) to **27.9%** (72 bits).
- The dominant remaining gap is coverage on certain medium-to-high attractor families (`a4_d4_a6`, `o2_d4_a6`, `o4_d4_a2@very_late`, `o4_d8_a7_higher_divisor`, etc.) that become common at 60+ bits but were rare or absent in the original 601_5500 mining surface.

The grammar lever is real, measurable, and still improving with targeted rule addition from larger enriched surfaces (27k–34k bands). We are not yet at the point of diminishing returns for the current approach.

## Key Measured Results

### 1. Real-Derivation Mid-Scale Probe (58–66 bit semiprimes, 10 samples, final rule set)

- Average reduction: **44.95%** (end of current mining cycle)
- Best cases (well-covered `o2_d4_a2_d4_odd@mid` variants): 71–74%
- Typical exotic high-a cases (a7–a20+): 52–60%
- Remaining stubborn cases (specific a1/a2/a3 with bad phases): ~2%

### 2. Real-Derivation Scaling Ladder (48–72 bits, 15 samples per level)

| Bit Length | Avg Reduction | Std Dev | Range     | Unresolved |
|------------|---------------|---------|-----------|------------|
| 48         | 38.42%        | ±24.8%  | 0–72%     | 0          |
| 56         | 35.89%        | ±29.7%  | 0–69%     | 0          |
| 64         | 34.11%        | ±20.0%  | 0–73%     | 0          |
| 72         | 27.91%        | ±26.8%  | 0–73%     | 0          |

All samples used actual public motifs derived from generated semiprimes at the target size (no synthetic motif sampling).

### 3. Evolution of Real-Derivation Performance (same 10-sample mid-scale set)

- Initial real-derivation baseline (before any high-a rules): ~14%
- After first high-a batch: 25.7%
- After precision 32k mining (a8/a10/a1/a3 focus): 35.1%
- After final stubborn-family batch (a6/a4/a2@very_late + higher exotic): **44.95%** (84 rules active)

Each batch was derived directly from patterns observed in the 27k–34k enriched multiplication-map surfaces.

## Remaining Coverage Gaps (from 64–74 bit diagnostic)

Most frequent motifs still delivering <15% reduction:

- `o4_d4_a6_d4_odd@mid` / `@very_late`
- `o2_d4_a6_d4_odd@early` / `@mid`
- `o2_d4_a2_d4_odd@very_late`
- `o4_d8_a7_higher_divisor_even@early`
- `o6_d4_a4_d4_odd@mid`

These families are well-represented in the 32k–34k enriched maps but were only lightly covered by the original 601_5500 rules.

## Interpretation for the RSA Goal

1. **The public grammar lever is scale-relevant.** Even with current coverage gaps we are deleting 25–41% of the factor-neighborhood hypothesis space using only public structural information on real 60–72 bit semiprimes.

2. **Coverage is the current limiter**, not the fundamental validity of the approach. The same multiplicative incompatibility patterns (high-divisor factor signatures incompatible with certain high-a / specific-phase chambers) continue to appear in the 32k data.

3. **The fail-fast loop is working.** We now have a repeatable pipeline:
   - Real public motif derivation
   - Mid-scale probe on fresh semiprimes
   - Targeted mining from larger enriched surfaces
   - Measurable lift

4. **Next branch point** (to be decided after one more short mining round):
   - Continue mining the 27k–35k family for the remaining stubborn motifs (likely to push mid-scale average into the mid-40s or low-50s).
   - Freeze the current rule set and build infrastructure (efficient motif derivation + candidate generation) to test at 80–100+ bits and eventually the Wikipedia RSA numbers.
   - Hybrid: finish the obvious high-a gaps, then move to infrastructure.

## Rule Set Status (as of this snapshot)

- Total rules: 81 (PG-001 through PG-081)
- All rules remain strictly public-only, deterministic, and carry 0 observed false negatives on their source surfaces.
- High-a / exotic attractor coverage has been the primary focus of the last four batches and accounts for the majority of the lift from 14% → 41%.

## Files & Reproducibility

- Live pruner: `pga_grammar_pruner.py` (with real `derive_public_motif` integration)
- Public motif derivation: `public_motif_derivation.py`
- Scaling ladder (real derivation mode): `pga_grammar_pruner_ladder.py`
- This snapshot + raw numbers: `SCALING_SNAPSHOT_2026-05-22.md` + associated JSON in the same directory
- Source enriched surfaces: `research/06-cryptology-rsa/.../core-evidence/output/enriched_multiplication_map_corpus_*`

All numbers above are reproducible with the checked-in code and the public 27k–34k enriched map files.

---

**Bottom line**: The public PGS grammar approach is delivering meaningful, measurable search-space reduction on real derived motifs at scales well beyond the original toy corpus. We have a working, auditable, fail-fast improvement loop. The only question left in this phase is how much further we can push coverage before the marginal cost of additional rules from the current surface family exceeds the benefit.

Next action owned by Codex lead: one final short mining pass on the remaining diagnostic motifs, followed by a clean decision gate on infrastructure vs. continued mining.