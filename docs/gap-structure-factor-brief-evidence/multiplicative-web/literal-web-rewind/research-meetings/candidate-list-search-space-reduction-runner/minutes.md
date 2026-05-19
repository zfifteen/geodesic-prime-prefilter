# Candidate List Search Space Reduction Runner Research Meeting Minutes

## Context

Design meeting to produce the next public N-only triangulation-based candidate-list runner under the public-evidence-integrity contract. Focus: search-space reduction measurement at toy scales with post-freeze canonical membership audit only.

## Participants

- Codex
- Grok CLI

## Command Capability Notes

Design-only session. No code implementation. All artifacts must satisfy the six-gate prevention contract and PUBLIC_EVIDENCE_INTEGRITY_CONTRACT.md.

## Agenda

1. Lock the original_space_size formula (Codex supplied exact definition).
2. Produce a complete, frozen, self-contained design contract artifact specifying all runner parameters, mechanisms, metrics, gates, and compliance path.
3. Pin v01 toy-campaign parameters so the contract is actionable without further ambiguity.

## Negotiated Deliverable

A frozen design contract (HTML, self-contained, file://-openable) located at:

`docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/design_contract.html`

The contract uses the exact Codex-supplied baseline formula, declares the full public input/output surface, the modulus-link-closure (thread triangulation) generation rule, the locked v01 parameters, the measurement protocol, admissible vs forbidden language, and the pre-implementation Grok certification checklist.

## Round Log

### Round 00 (Opening)

Grok restated the shift to search-space-reduction measurement, proposed the runner shape, identified pre-freeze oracle influence on policy params as primary compliance risk, and asked for the exact public original_space_size formula.

### Round 01 (Codex)

Codex supplied the locked denominator:

`original_space_size(N) = (2**ceil(bit_length(N)/2) + 1) // 2`

(count of odd d, 1 ≤ d ≤ public_radius(N))

plus the two reduction metrics and the unresolved rule for zero-count lists.

### Round 02 (Grok — Contract Freeze)

Grok produced the complete frozen design contract HTML using the supplied formula verbatim. All required elements (inputs, emitted artifacts, generation mechanism framed as chained modulus-link closures, score ingredients, size controls, toy surface, admissible metrics, forbidden uses, freeze gates, certification checklist) are specified. Conservative v01 campaign parameters were pinned inside the contract (12 odd primes, min_depth=5, max_candidates=512) so that no remaining choice materially alters the contract rules or metrics. No additional question was required.

## Candidate Insights

- The conservative odd-count baseline prevents the filter from claiming credit for classical sieving work.
- Freezing the three numeric controls (thread count, depth, cap) inside the contract itself is the strongest available mitigation against parameter-level oracle contamination.
- The HTML format satisfies the repo preference for visually structured, checklist-rich design artifacts that can be audited directly from file:// without build steps.

## Falsification Tests

- Any future runner that emits a list whose reduction ratio uses a different denominator, or that emits > max_candidates distances, or that contains private-derived branches, falsifies compliance with this contract.
- Any narrative that cites a private rank or containment number before the canonical checker has spoken for that N falsifies the quarantine.

## Convergences

- Both parties agree that the public filter's value is now defined by observable list cardinality reduction + membership, not by any internal score or private position.
- The contract is deliberately implementation-neutral: the exact iterative CRT code can vary as long as it respects the public mechanism description, the locked parameters, and the N-only invariant.

## Unresolved Questions

None that would change the frozen contract. Refinement of thread_set, depth, or cap for a later campaign will be handled as a new contract version with a new toy corpus or explicit invalidation of prior comparisons.

## Next Research Move

1. Grok performs the pre-implementation compliance certification review of the proposed runner source (once written) against the checklist in the design contract.
2. Upon certification, the v01 runner is implemented and executed against a public toy_corpus.jsonl (to be supplied) under full gate discipline.
3. Results are reported only via the public manifests + canonical status files; any private diagnostic work occurs under a separate, explicitly declared contract.
