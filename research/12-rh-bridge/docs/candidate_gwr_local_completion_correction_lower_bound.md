# Candidate Local Lemma: GWR Local Completion Correction Lower Bound

**Date:** 2026-05  
**Status:** Candidate statement emerging from numerical experiments in the Core Insight decisive test. Not proved. The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open. No obligation discharged.

**PGS objects first (per AGENTS.md):**  
- Ordered prime-gap state (p < q with interior I).  
- Divisor-count field τ(n) and zero-excess E(n) = (τ(n)/2 − 1) log n.  
- GWR: the unique leftmost n ∈ I minimizing E(n) (maximizer of F = −E per PROOF.md).  
- The packet completion correction terms required by the Folded Packet Drift Inequality and Aggregate Completion-Cost Bound (after local GWR control on the deconvolved packet measure).

## Candidate Statement

**Conjecture (GWR Local Completion Correction Lower Bound):**  

Let p < q be consecutive primes and let g be the GWR point inside (p, q). Let δ = E(g) · log(q/p).  

Then, under the local control already established by the GWR maximizer on the deconvolved positive mass of the chamber packet, the quantity δ supplies a lower bound on the local contribution needed from the completion correction to satisfy the nonnegativity side of the Folded Packet Drift Inequality for all chambers with log(q/p) greater than some absolute constant (with the bound holding with an explicit positive constant k independent of the particular chamber).

In other words: the GWR maximizer forces a per-chamber algebraic supply of positivity in the completion correction that is at least k · log(q/p) for a fixed k > 0, before any global effects from other chambers are considered.

## Evidence from Numerical Experiments (Stages 0–2)

- On 1752 ordinary chambers (primes to ~15,000): the ratio after applying δ remained ≥ 6.36 in both raw and GWR-bounded local models.
- On 300 high-merit large gaps (p ≳ 10^12, merit ≥ 15): even under optimistic assumptions about the lowest possible E(g) inside the gap, the simple δ form maintained a ratio above the same floor.
- No counterexample was found in the tested regimes despite deliberate stress on wider and higher-merit chambers.

These are finite measured results on toy and extreme regimes using local models only. They are consistent with the candidate statement but do not prove it.

## Relation to Existing Reduction

This candidate lemma, if proved, would strengthen the "What Existing Control Already Supplies" section of folded_packet_drift_inequality.md by giving an explicit, local, GWR-derived lower bound on the size of the completion correction term required for the even (folded-mass) part of the inequality.

It would not by itself close the full reciprocal balance (odd part) or the global transport to the Stieltjes measure.

## Open Questions / Required Work for Proof

- Derive the precise constant k (or functional form) directly from the GWR maximizer property and the existing local control theorems.
- Show that the bound survives the transition from the local packet model to the actual contribution after the full (but still local) action of the deconvolution operator.
- Integrate any proved version as a new input into the existing completion transport and localization arguments.

## Status

This is a candidate local lemma suggested by the numerical behavior observed in the Core Insight decisive test. It has not been proved. It remains a hypothesis.

The live target (Chamber-Deconvolved Reciprocal Balance Lemma — all three obligations) remains fully open.

PGS objects surfaced at every step in the experiments that motivated this candidate. Strict separation language used throughout. No claim is made that this closes any part of the analytic lemma.