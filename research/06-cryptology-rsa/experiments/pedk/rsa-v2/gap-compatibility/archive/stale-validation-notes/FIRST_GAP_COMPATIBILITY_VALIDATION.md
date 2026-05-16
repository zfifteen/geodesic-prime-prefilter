# First Gap Compatibility Validation Experiment

**Date:** Current session  
**Status:** Experiment designed and launched. Awaiting results.

## Experiment Design (Judgement Call)

**Purpose:** Perform the smallest possible empirical check of the Gap Compatibility Hypothesis intuition using the project's existing reduced gap grammar.

**Hypothesis being tested (first-order version):**
The reduced PGS gap type of the interval containing the public semiprime `N` shows recurring compatibility or incompatibility relationships with the reduced gap types of the gaps containing the actual factors `p` and `q`.

**Scope:** Restricted to the three official committed RSA v2 rungs (40-bit, 50-bit, 64-bit) for which we have known factor pairs.

**Method:**
- For each known triple `(N, p, q)`, compute the reduced gap state (in the established `oX_family|bucket` grammar) for:
  - The gap containing N
  - The gap containing p
  - The gap containing q
- Produce a side-by-side comparison table.
- Look for any immediate patterns that distinguish the 50-bit false-positive case from the two correct resolutions.

**Design Choices Made:**
- Used the project's existing style of reduced gap states (inspired by the 14-state core grammar and functions such as `reduced_state` in the modulus-recursive-catalogs work).
- First-pass classification is intentionally coarse (wheel-30 style first-open buckets + divisor-count family + size bucket).
- Focused on the single gap containing each number rather than richer neighborhoods for this initial validation.
- Kept the script self-contained and auditable.

**Why this design?**
- It directly tests the core intuition ("gap containing N is not independent of factor-side gap types") with minimal new machinery.
- It uses only the documented and tested gap typing grammar the project already has.
- It is small enough that any signal or lack of signal will be immediately visible.
- It serves as a baseline before deciding whether richer neighborhood descriptors (carriers, tails, reset signatures, transported alignments) are needed.

**Script:** `first_gap_compatibility_check.py`

**Output:** `output/first_gap_compatibility_check.jsonl`

## Next Actions (After Results)

1. Review the produced gap types for all three cases.
2. Look specifically at whether the 50-bit case sits in a different compatibility class than 40-bit and 64-bit.
3. Decide whether to expand the classification (richer neighborhood, more precise first-open calculation, more cases) or move to a different angle.
4. Record findings in this document and the main PEDK log.

This experiment is deliberately narrow and evidence-first, in line with the instruction to let the data drive the development of PEDK rather than committing to a particular architecture upfront.