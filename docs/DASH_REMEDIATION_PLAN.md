# Dash Remediation Plan

**Goal:** Completely eliminate all instances of en dashes (`–`) and em dashes (`—`) across the repository while maintaining grammatical correctness, technical precision, and the conversational prose style mandated by `AGENTS.md`.

**Constraint:** Do not simply remove the dashes or replace them with hyphens if it compromises sentence structure. Sentences must be intentionally rewritten (using parentheses, colons, commas, or split into multiple distinct sentences) to flow naturally without accommodating dashes.

## Phase 1: High-Visibility Files

*   **Files Touched:**
    *   `README.md`
    *   `docs/OVERVIEW.md`
    *   `PROOF.md`
    *   `AGENTS.md` (if applicable)
*   **Commands to Run:**
    *   `rg -c "—|–" README.md docs/OVERVIEW.md PROOF.md` (baseline count)
*   **Action:** Manually restructure every sentence containing a dash. For example, list items using dashes for definitions (e.g., `- Item — description`) will be changed to use colons (`- Item: description`). Parenthetical thoughts will be converted to actual parentheses or distinct sentences.
*   **Verification:** Re-run the regex search on these files to ensure 0 hits. Self-review the text to guarantee grammatical soundness and adherence to Section 10 of `AGENTS.md`.
*   **Estimated Operator Review Point:** After Phase 1 completion, to ensure the new prose style meets expectations before scaling to the rest of the repository.

## Phase 2: Core Documentation

*   **Files Touched:**
    *   `docs/core/*.md`
    *   `docs/rh/*.md`
    *   `docs/RESULTS.md`
    *   Other supporting documents directly within `docs/`.
*   **Commands to Run:**
    *   `rg "—|–" docs/core/ docs/rh/`
*   **Action:** Systematically rewrite sentences containing dashes in foundational explanations.
*   **Verification:** Zero regex hits in `docs/core/` and `docs/rh/`.

## Phase 3: Broad Research Directory Remediation

*   **Files Touched:**
    *   All markdown and text files within the `research/` directory, which likely holds the bulk of the "hundreds of instances".
*   **Commands to Run:**
    *   `rg "—|–" research/`
*   **Action:** Because the research directory is vast, this phase will be broken down into sub-batches (e.g., `research/00-index/`, `research/remainders/`, etc.) to carefully restructure the technical notes without altering the math or meaning.
*   **Verification:** Zero regex hits in the specified sub-batches.
*   **Estimated Operator Review Point:** Mid-way through Phase 3 to confirm no technical meaning is being lost during sentence restructuring.

## Phase 4: Final Global Verification and Polish

*   **Files Touched:**
    *   Any remaining source code files, scripts, or obscure documentation.
*   **Commands to Run:**
    *   `rg "—|–" .` (Global search)
*   **Action:** Catch any straggling dash characters. Perform a final read-through of major modified sections.
*   **Verification:** The global search command must return 0 hits.
