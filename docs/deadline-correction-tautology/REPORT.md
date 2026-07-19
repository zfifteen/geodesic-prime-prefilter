# Deadline Correction Tautology: A Mathematical Verification

## Executive Summary
This document formalizes a structural insight discovered and mathematically verified by the Adversarial Auditor on 2026-07-18. The insight proves that the backward transport evaluation in the deadline correction branch of `run_experiment.py` (specifically `transported_corrected_lower == corrected_lower_endpoint`) is a 100% pure algebraic tautology. By relying on the Dirichlet hyperbola reflection property, we have demonstrated that this specific evaluation provides zero independent filtering power if the forward check passes. Consequently, it can be safely removed to optimize solver performance without altering the deterministic output.

## Context: The Mutual Closure Metric
In the repository's deterministic RSA solvers, the "mutual closure" metric is used to evaluate the structural rigidity of candidate certificate chains. The algorithm attempts to verify a two-way lock:
1. **Forward Check:** Does the lower endpoint transport to the upper endpoint? (`transported_upper == upper.reset_endpoint`)
2. **Backward Check:** Does the upper endpoint transport back to the lower endpoint? (`transported_lower == lower.reset_endpoint`)

While this metric appears to strictly enforce a mutual lock, an adversarial mathematical analysis reveals that the backward check is often a redundant algebraic identity masquerading as a structural filter.

## The Dirichlet Hyperbola Reflection Property
The insight fundamentally relies on the behavior of integer division (flooring) across the center line of a modulus $N$.

For any modulus $N$ and an integer $L \le \lfloor\sqrt{N}\rfloor$, the forward transport evaluates to $U = \lfloor N / L \rfloor$. 
The backward transport evaluates to $\lfloor N / U \rfloor$, which simplifies to $\lfloor N / \lfloor N / L \rfloor \rfloor$.

According to the Dirichlet hyperbola reflection property, as long as $L \le \lfloor\sqrt{N}\rfloor$, the equation evaluates unconditionally to:
$$ \lfloor N / \lfloor N / L \rfloor \rfloor = L $$

## The Tautology in Deadline Correction
In the deadline correction branch, the solver enforces the invariant that `corrected_lower_endpoint` ($L$) must be less than `lower.anchor`. By design, `lower.anchor` is strictly bounded by $\lfloor\sqrt{N}\rfloor$. Therefore, the constraint $L < \lfloor\sqrt{N}\rfloor$ is absolutely guaranteed.

### Proof of Redundancy
If the forward check passes, we establish that $U = \lfloor N / L \rfloor$. The backward check then tests if $\lfloor N / U \rfloor = L$. 

Let $N = U \cdot L + R$, where $R = N \pmod L$. The backward check fails if and only if $R \ge U$. 
Since $R < L$ by the definition of the modulo operator, a failure condition ($R \ge U$) mathematically requires $L > U$.

However, because $L < \lfloor\sqrt{N}\rfloor$, the upper bound $U = \lfloor N / L \rfloor$ is mathematically forced to be $U \ge \lfloor\sqrt{N}\rfloor$. 
This guarantees $U > L$. 

Therefore, we have the inequality $R < L < U$. Because $R < U$ is strictly and always satisfied, $\lfloor N / U \rfloor = L$ identically.

The backward check is not evaluating structural rigidity; it is merely recomputing a mathematically guaranteed integer division identity.

## Critical Distinction: The Stealth Boundary Filter
It is vital to distinguish the deadline correction branch from the primary evaluation branch. 

In the primary branch, the check `transported_lower == lower.reset_endpoint` is **not** a pure tautology. The solver includes fallback logic: if `lower.reset_endpoint > center`, the transport coordinate falls back to `lower.anchor`. In this scenario, `transported_lower` evaluates to `lower.anchor`, and the check tests `lower.anchor == lower.reset_endpoint`. This is strictly **FALSE**.

Thus, the primary backward check acts as a "stealth boundary filter," implicitly enforcing the rule that `lower.reset_endpoint` must not cross the center. Removing the primary backward check would allow false positive candidates to leak through. Only the **deadline correction** backward check is a pure tautology.

## Adversarial Auditor Verification
This finding was rigorously tested against the project's strict evidentiary standards by the Adversarial Auditor:

1. **Null Hypothesis:** Disproven. The auditor verified that failure requires $L > U$, which is mathematically impossible given the strict bounds enforced by the solver.
2. **Tautologies:** Ruled out as a spurious correlation. The finding correctly identified a true algebraic tautology embedded in the solver, free from heuristic or statistical assumptions.
3. **Selection Bias:** Ruled out. The proof is derived entirely from fundamental integer arithmetic and applies unconditionally to all positive integers $N$.

## Conclusion
The `transported_corrected_lower == corrected_lower_endpoint` evaluation provides zero filtering power. It can be safely excised from `run_experiment.py` as a verified optimization.
