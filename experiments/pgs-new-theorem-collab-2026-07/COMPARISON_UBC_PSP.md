# Comparison: New Candidate vs. UBC / PSP

This document ensures the new GWR Offset Law candidate stays clean and dual to existing objects.

## UBC (Universal Bound on Composites)
- **Scope:** Bounds the offset `δ` relative to the Cramér scale in `q`.
- **Nature:** An absolute worst-case bound on where the witness can fall, typically scaling as `0.5 log(q)^2`.
- **Target:** The new candidate is **gap-local**. It describes `δ` relative to the gap width `g`, not the prime `q`. It addresses typical/mean behavior in small gaps, whereas UBC is a hard boundary condition for large `q`.

## PSP (Prime Signature Partition)
- **Scope:** Partitions the integers into structural classes based on prime signatures (e.g., cell `R`, cell `P`).
- **Nature:** A classification of integers.
- **Target:** The new candidate classifies the *placement* (offset `δ`) of a specific integer (the GWR witness) inside a gap. The witness will have a specific prime signature, but the candidate focuses on its *index* relative to `p`, rather than its class in PSP. 

**Conclusion:** The Gap-Width Offset candidate is strictly complementary. It provides fine-grained local structure (relative to `g`) underneath the global Cramér-scale umbrella of the UBC.
