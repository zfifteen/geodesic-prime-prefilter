# Recursive Endpoint-Chain Closure Design Analysis

**Status:** Design analysis only. No implementation, no code, no execution plan.

This document examines the current `run_experiment.py` (OECC_LINEAR_V1) against the scalability requirement stated for RSA v2 endpoint-structure work: the algorithm must be the same at every scale; the only limit is computability of the underlying PGS primitives.

## 1. The Scalability Requirement

The design target is an algorithm whose decision structure, closure rules, and state transitions contain no bit-size-dependent branching, no radius that grows with log(N), and no special-case paths that activate only above a certain bit length.

The sole scaling dimension must be:

- How many steps of iteration or recursion are required before a documented closure predicate is satisfied or becomes uncomputable.
- The cost of computing one additional PGSPG reset certificate at the current position in the chain.

If the same relational rules and the same traversal order over PGS objects work for a 40-bit modulus and a 2048-bit modulus, the design satisfies the requirement. Any remaining limitation is a question of whether the local divisor-count state around a previous public endpoint can still be computed, not whether the inference rule itself must be rewritten.

## 2. Current Implementation Shape (OECC_LINEAR_V1)

The live runner in `run_experiment.py` implements three documented closure modes:

- Mutual certificate reset closure
- Reciprocal deadline-signature correction
- Oriented endpoint-chain closure

These modes are real and are derived from the endpoint-structure law. However, they are currently expressed through a control-flow structure that mixes:

- A direct-transport path starting from the previous endpoint before `isqrt(N)`
- An early exit into full chain traversal when the initial lower reset endpoint has already crossed the square-root orientation
- A second, later call to the same chain walker if the direct path plus deadline correction fails
- A `while` loop in `endpoint_chain_closure` that walks backward via `previous_endpoint_at` down to the hard boundary `floor(isqrt(N) / 2)`

The result is a correct but non-uniform implementation. The three closure modes exist as separate predicates, yet the decision of *when* to apply the full chain versus the direct transport is encoded in Python early returns and conditional calls rather than in the structure of the PGS objects themselves. This is the pattern Codex has been able to sustain, and it is the pattern that becomes fragile when the rule set is extended or when the bit size increases.

## 3. The Latent PGS Objects

The repository already contains the complete set of objects needed for a scale-independent formulation. They are:

- **Previous public endpoint**: The right endpoint of the prime gap immediately to the left of a given integer. This relation generates a chain: … → a₂ → a₁ → a₀ where each aᵢ is the previous public endpoint before aᵢ₊₁.
- **PGSPG reset certificate**: The full state record produced by the chamber-reset logic at a previous public endpoint (anchor, reset_endpoint, carrier_w / carrier_d, lock state, lower_d_threat_offset, tail_after_reset_offsets, reset_deadline_value, reset_signature). This is the same certificate used in ordinary next-prime generation.
- **Oriented transport coordinate**: At any lower certificate, the value chosen for reciprocal transport is either `reset_endpoint` (if still on the lower side of the square-root orientation) or `anchor` (if the reset endpoint has crossed). This choice is local to the certificate and the orientation point; it does not require bit-size logic.
- **Reciprocal floor transport**: The operation `floor(N / x)`. This is pure arithmetic and is the only link between the lower and upper sides.
- **Closure predicates** (all already documented):
  - Strict mutual reset closure: `floor(N / L.reset_endpoint) == U.reset_endpoint`, the reverse, and signatures equal.
  - Deadline-signature correction: outward movement (`c < L.anchor` and `d > U.reset_endpoint`), mutual floor images on the corrected pair `(c, d)`, and signature match.
  - The same predicates applied during chain traversal.

Every one of these objects is defined without reference to the bit length of N. The previous-endpoint relation, the certificate contents, the oriented transport choice, and the closure predicates are all local or relational.

## 4. Unified Recursive / Iterative Skeleton

The single scale-independent structure is iteration or recursion over an **oriented transported certificate chain state**.

A chain state at step k can be described as:

- Current lower anchor aₖ (a previous public endpoint)
- Certificate Lₖ derived at aₖ
- Chosen oriented transport coordinate xₖ (Lₖ.reset_endpoint or Lₖ.anchor)
- Transported upper coordinate yₖ = floor(N / xₖ)
- Upper anchor bₖ = previous public endpoint before yₖ
- Certificate Uₖ derived at bₖ
- The set of already-tested closure predicates on (Lₖ, Uₖ)

The transition rule is uniform:

1. Test the documented closure predicates on the current pair (Lₖ, Uₖ).
2. If any predicate is satisfied, emit the corresponding structural endpoint class and terminate.
3. Otherwise, extend the chain by one step: compute aₖ₊₁ = previous public endpoint before aₖ, derive Lₖ₊₁, and repeat from step 1.

The orientation point `isqrt(N)` is used only to decide the transport coordinate inside each certificate; it does not create a separate code path or a different termination condition. The initial square-root chamber is simply the first element of the same chain.

The only termination conditions are:

- A closure predicate returns true (resolved structural endpoint class).
- The next previous public endpoint cannot be computed (computability limit reached).
- The chain has exhausted the public region in which a factor pair is still possible under the balance interval (this limit, if needed, must itself be expressed as a PGS-derived bound rather than an arbitrary `s/2`).

This skeleton makes the three closure modes into alternative outcomes of the same iterative step rather than separate control-flow branches that are entered at different times.

## 5. Mapping of Documented Rules onto the Skeleton

All rules already present in the endpoint-structure law and in `PGS_CERTIFICATE.md` become cases evaluated at each step of the uniform iteration:

- **Strict reset closure** — evaluated first on every (Lₖ, Uₖ) pair.
- **Deadline value selection** — the rule that chooses the minimum among tail[0], lower_d_threat_offset, or candidate_bound is executed once when the certificate is built; the resulting `reset_deadline_value` and `reset_signature` travel with the certificate into the closure test.
- **Deadline-signature correction** — the outward-correction test plus mutual floor images on (c, d) plus signature match is simply another predicate evaluated on the current pair after the direct reset closure has failed.
- **Oriented transport coordinate choice** — a pure function of the current lower certificate and the orientation point; identical at every step of the chain.
- **Signature matching** — part of every closure predicate; the signature is carried unchanged from the PGSPG certificate construction.
- **Previous-endpoint stepping** — the generator of the next state in the iteration; exactly the same operation whether we are still in the initial square-root chamber or deep in the chain.

No additional rule is required when the iteration moves from the first lower anchor to the second, or from bit length 40 to bit length 2048. The only change is the number of previous-endpoint steps that must be taken before one of the predicates succeeds or becomes uncomputable.

## 6. Scale-Sensitive Artifacts in the Current Code

The following elements in `run_experiment.py` and `endpoint_chain_closure` are the parts that would be replaced by the unified skeleton. Each of them introduces either an implicit scale assumption or a control-flow distinction that is not required by the PGS objects:

- The conditional early entry into `endpoint_chain_closure` when `lower.reset_endpoint > center`. In the recursive formulation this case is simply the first iteration step whose transport coordinate happens to be the anchor rather than the reset endpoint.
- The second, later call to `endpoint_chain_closure` inside `certificate_pair` after the direct-transport deadline correction has failed. This duplication disappears when the direct transport is treated as step 0 of the same chain iteration.
- The hard lower termination `anchor >= floor(isqrt(N) / 2)` as the primary loop condition. In a pure PGS formulation the iteration continues while the next previous endpoint exists and while the transported coordinate remains inside the public region where a structural endpoint class can still be formed. The `s/2` bound is an engineering approximation, not a derived closure limit.
- The global constant `RULE_X_CANDIDATE_BOUND = 128` used inside `previous_endpoint`. While a fixed local window is scale-friendly, its status as an unparameterized global makes it easy to treat as "the number that works up to this bit size." In the recursive skeleton the window size would be an explicit parameter of certificate construction, passed down or derived from the certificate state itself.
- The separation between "square-root chamber logic" and "endpoint-chain logic" in the top-level function. The skeleton collapses this into one uniform traversal whose first element happens to be the previous endpoint before `isqrt(N)`.

Removing these artifacts does not change any of the documented closure rules. It only changes the control structure that applies them.

## 7. What the Recursive Skeleton Makes Obvious

Once the algorithm is expressed as iteration over successive previous public endpoints, each carrying a full PGSPG reset certificate, the scalability claim becomes structural rather than empirical:

- At any bit size, the procedure is: start at the previous endpoint before `isqrt(N)`, derive the certificate, transport, test the fixed set of relational predicates, and if none succeed, move to the previous previous endpoint and repeat.
- The number of iterations required is determined by the distance (in previous-endpoint steps) from the square-root region to the factor endpoints, not by any bit-size threshold in the code.
- The cost per iteration is the cost of computing one PGSPG reset certificate (local divisor-count segment + GWR/NLSC chamber state) plus a constant number of `floor(N / ·)` operations and previous-endpoint lookups.
- When that cost becomes prohibitive, the limitation is computability of the local gap structure at that scale, not the absence of a larger-radius rule or a different algorithm for 1024-bit numbers.

This is the precise sense in which the structure "already existed" and the only remaining task is to implement the traversal consistently.

## 8. Relation to Existing Documents

This analysis draws directly from:

- `endpoint_structure_law.md` — the public law statements for reciprocal deadline-signature correction and oriented endpoint-chain closure.
- `PGS_CERTIFICATE.md` — the contract that the certificate, not the raw endpoint, is the unit of inference.
- `ALGORITHM.md` — the stage description that already lists the three closure modes as successive but still separate stages.
- `ORIENTED_ENDPOINT_CHAIN_BASELINE.md` — the explicit labeling of the current linear implementation.

The recursive formulation does not add new rules. It re-expresses the rules already written in those documents as the step logic and termination conditions of a single chain traversal.

## Document Status

This is a design analysis of the gap between the documented PGS rules and the control structure that currently applies them. It does not constitute a proof that a recursive implementation will resolve more rows, nor does it claim that the current linear form is incorrect on the tested surfaces. It identifies the structural change required to make the scalability claim hold by construction rather than by measured success up to a given bit length.

Further analysis can map the exact state that must be carried between recursive steps and the precise point at which each documented closure predicate is evaluated. That mapping remains inside the same PGS object vocabulary already used for ordinary prime-gap generation.