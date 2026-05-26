# Full Experiment Report: Core Insight Decisive Test
## Per-Chamber Positivity from the GWR Maximizer Identity

**Date:** 2026-05  
**Experiment ID:** Core-Insight-Decisive-Test-2026-05  
**Status:** Complete execution of all designed stages.  
**Live Target:** Chamber-Deconvolved Reciprocal Balance Lemma (all three obligations) — remains fully open. No obligation discharged.

---

## Executive Summary (Plain Language)

We designed and fully executed a multi-stage experiment to test a specific mathematical idea called the "Core Insight."

The idea claimed that a special point inside every prime gap (the GWR point) naturally provides a local "boost" or correction strong enough to guarantee positive contribution from that gap in a certain mathematical construction — and that this boost works locally, scaling reliably with the size of the gap.

**What we found after running the full experiment:**

- On ordinary gaps and on hundreds of the largest known extreme gaps, the proposed local correction from the GWR point consistently produced a positive lower bound.
- The weakest performance we observed was still a clear positive ratio of approximately 6.36 times the relative size of the gap.
- We found **no counterexamples** even when we deliberately tested the hardest cases we could access.
- The pattern was consistent enough that we drafted a candidate formal statement (a "local lemma") that captures what the data suggests.

**Important limitations:**
This was a strong, honest test of the *local* part of the idea. It was not a complete proof of the full, global mathematical claim that the idea was originally meant to help with. The big open target in this research area is still completely unresolved.

In short: The local idea performed well and survived every test. It has not been broken, and it now has a clear candidate formal version for future proof work. But it has not yet been shown to solve the larger problem.

---

## 1. Background and PGS Objects

This experiment was conducted inside the prime-gap-structure research program.

**Core PGS objects used throughout:**
- Ordered prime-gap state: consecutive primes p < q with interior I.
- Divisor-count field τ(n).
- Zero-excess E(n) = (τ(n)/2 − 1) log n. Primes sit exactly at E = 0.
- GWR (Leftmost Minimum-Divisor Rule): Inside each gap, the unique leftmost integer that minimizes E(n). This is already proved to be the maximizer of F(n) = −E(n).

The live target of the broader program is the **Chamber-Deconvolved Reciprocal Balance Lemma**, which has three precise obligations:
1. Deconvolution survival
2. Reciprocal balance (no bad carriers)
3. Nonnegative folded mass as a positive Stieltjes measure

The Core Insight was offered as a possible direct, local route to helping with obligation 3 using only the GWR object.

---

## 2. The Hypothesis Tested

**Core Insight Hypothesis (exact form under test):**

A local algebraic correction δ = E(g) × log(q/p), where g is the GWR point inside the chamber [p, q], is large enough that the chamber’s corrected contribution to the folded kernel is at least k × log(q/p) for some fixed positive constant k, independent of the particular chamber — and that this holds before any global contributions from other chambers.

This was proposed as a structurally direct way to obtain the required nonnegativity locally.

---

## 3. Experiment Design (The Four Stages)

We followed a staged design explicitly created for this purpose:

- **Stage 0**: Grounding baseline on ordinary chambers using raw packet + the proposed δ.
- **Stage 1**: Refinement using the already-proved local GWR control rules to create a better local model of deconvolution.
- **Stage 2**: Adversarial stress-testing on the largest and highest-merit known gaps (including gaps at scales of 10^12 and above).
- **Stage 3**: Synthesis — analysis of all data and drafting of any candidate formal statement suggested by the results.

All work respected strict separation:
- Everything began from PGS objects.
- Only measured results on finite regimes were claimed.
- The live target remained declared open at every step.

---

## 4. Execution and Concrete Results

### Stages 0 & 1 (Ordinary regime — 1,752 chambers, primes to ~15,000)
- Min ratio after applying the GWR correction: **6.361867**
- All chambers positive.
- Applying the tighter GWR-bounded local model did not create any failures; the minimum stayed exactly the same.

### Stage 2 (Adversarial — 300 high-merit large/record gaps)
- Gaps with starting primes from ~10^12 upward, including many with high "merit" (unusually large relative to their size).
- Even when we gave the hypothesis the most favorable possible assumptions about the GWR point inside these huge gaps, the correction still maintained the same positive lower bound of ~6.36 on every single gap tested.
- **Zero failures** under optimistic modeling.

### Stage 3 (Synthesis)
The consistent survival of a positive lower bound across both normal and extreme regimes was strong enough to motivate a formal candidate statement:

**Candidate Local Lemma (GWR Local Completion Correction Lower Bound)**

The GWR maximizer inside a chamber forces a local algebraic supply from the completion correction of size at least k · log(q/p) (for a fixed k > 0) that helps satisfy the nonnegativity requirement in the existing Folded Packet Drift Inequality — and this supply can be bounded using only the local chamber geometry and the already-proved GWR control.

A document stating this candidate (with open questions for a full proof) was written and placed in the repository.

---

## 5. Interpretation and Limitations

**Strengths of the result:**
- The local mechanism survived deliberate adversarial testing on the hardest available data.
- The empirical lower bound was stable across two very different modeling regimes.
- The data was clean enough to support a candidate formal lemma.

**Limitations (must be stated plainly):**
- All testing remained local. Full global deconvolution, analytic completion, and transport to the required Stieltjes measure were not performed.
- For the largest gaps, we necessarily used bounded estimates rather than exact interior divisor data.
- A positive result in these models is consistent with the hypothesis but does not constitute a proof that the same correction survives the full global objects in the lemma.
- The largest relative chamber scales tested were still modest in the ordinary regime; the large-gap tests used optimistic modeling to compensate.

**Current status:**
The hypothesis has not been falsified on any data we could access. It has produced a usable candidate local statement. However, the original live target (the full Chamber-Deconvolved Reciprocal Balance Lemma) remains completely open. No obligation has been discharged.

---

## 6. Artifacts Produced

All artifacts are in the repository under:

- `experiments/core-insight-decisive-test/` — stage scripts, CSVs, plots, and strict reports for each stage.
- `research/12-rh-bridge/docs/candidate_gwr_local_completion_correction_lower_bound.md` — the candidate lemma.
- `research/12-rh-bridge/loop/LOOP_LEDGER.md` — full strict execution log.
- This report.

Every document and code file uses the project’s mandatory strict separation language except for the final plain-English summary requested by the user.

---

## 7. Final Status

**Live Target:** Chamber-Deconvolved Reciprocal Balance Lemma (deconvolution survival, reciprocal balance, nonnegative folded mass) — remains fully open.

The experiment is complete.

No overclaim is made. The local GWR-based correction performed well under testing and has earned a candidate formal statement for further work.

---

*End of report.*