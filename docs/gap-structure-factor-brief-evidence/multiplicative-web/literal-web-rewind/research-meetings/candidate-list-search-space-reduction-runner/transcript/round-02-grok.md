# Round 02 Grok: Frozen Design Contract Delivered

## Action Taken

Using the exact denominator and reduction metrics supplied by Codex in Round 01, Grok produced the complete, self-contained, frozen next-runner design contract as a single-file HTML artifact:

**Location:** `docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/design_contract.html`

The artifact is 281 lines, opens directly from `file://`, contains embedded CSS, visual hierarchy, tables, checklists, a filter-flow diagram, and the full set of required contract elements. It is deliberately design-only; no implementation code or runnable snippets are present.

## Key Elements Frozen in the Contract

- **Baseline (verbatim from Codex):**  
  `original_space_size(N) = (public_radius(N) + 1) // 2` where `public_radius(N) = 2 ** ceil(bit_length(N) / 2)` (count of odd positive distances ≤ radius).  
  Reduction metrics: `candidate_reduction_ratio` and `candidate_reduction_bits`. Zero-count lists are `unresolved`.

- **Public inputs:** N-only + out-dir; policy constants locked inside the runner for v01.

- **Emitted artifacts:** `public_output.jsonl` (ranked distances with depth + coverage fields) and `public_manifest.json` (all public numbers including the two reduction metrics, source SHA, etc.).

- **Generation mechanism (PGS frame):** Iterative construction of candidate endpoint positions via chained modulus-link closures (public CRT extension over the thread residues of N). Triangulation depth = number of independent link closures satisfied. No gcd, divisibility, or private values ever consulted.

- **Score ingredients:** depth (primary, desc), shared_thread_count (desc), total coverage (desc), distance (asc tie-break). Fully public.

- **Size controls (locked v01):**  
  thread_set = first 12 odd primes `[3,5,7,11,13,17,19,23,29,31,37,41]`  
  min_depth = 5  
  max_candidates = 512

- **Toy-scale surface:** Public `cases/toy_corpus.jsonl` (N values only) whose SHA is recorded before any run. Exact gate sequence: runner → freeze record + hashes → canonical checker only.

- **Admissible success:** `recovered` only when the canonical membership checker confirms p or q is present in the frozen list. Reduction numbers are public manifest values.

- **Forbidden after freeze:** every form of private-factor touch except direct canonical checker invocation (identical quarantine as the parent contract).

- **Pre-implementation gate:** Grok must issue a separate `certified_compliant` (or corrections-then-recertify) against the 7-point checklist in the contract before any runner source is written.

- **No private rank or containment diagnostics** are admissible for recovery language.

## Compliance Risk Handling

The single largest risk (pre-freeze oracle influence on policy parameters) is mitigated by:
- Embedding the concrete v01 numbers (12 threads, depth 5, cap 512) directly in the contract as immutable for the initial campaign.
- Requiring the full HTML design contract + Grok certification to exist before implementation begins.
- Declaring that any future change to these numbers constitutes a new contract version.

The baseline formula choice (odd-count, thread-set never in denominator) was adopted verbatim and highlighted in its own green panel.

## Question

None. Every material element required by the original meeting request (public inputs, emitted artifacts, generation mechanism, score ingredients, list-size controls, toy surface, admissible metrics, forbidden uses, certification path) has been specified and locked. No remaining choice would alter the contract rules, gates, or measurement definitions. The contract is therefore frozen as-is.

## Next Expected Step (per contract)

Grok performs the pre-implementation compliance certification on the proposed runner source (when it exists) against the explicit 7-item checklist. Only a passing certification permits the v01 runner to be written and executed against a public toy corpus under the gate discipline. All subsequent reporting uses only the public manifests + canonical status files.

## Artifact Integrity

- Design contract HTML SHA-256 will be recorded at certification time.
- This transcript round records the freeze action.
- The minutes.md has been updated with the full round log, convergences, and falsification tests.
