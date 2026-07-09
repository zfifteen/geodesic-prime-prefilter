# Dash Remediation Plan

**Goal:** Completely eliminate all instances of en dashes (Unicode U+2013) and em dashes (Unicode U+2014) across the repository while maintaining grammatical correctness, technical precision, and the conversational prose style mandated by `AGENTS.md`.

**Constraint:** Do not simply remove the dashes or replace them with hyphens if it compromises sentence structure. Sentences must be intentionally rewritten (using parentheses, colons, commas, or split into multiple distinct sentences) to flow naturally without accommodating dashes.

**Verification note:** Search for the actual Unicode dash characters U+2013 and U+2014. Do not search for ordinary colons (`:`) or the English word `to`; those are valid prose and will never reach zero hits.

## Phase 1: High-Visibility Files

*   **Files Touched:**
    *   `README.md`
    *   `docs/OVERVIEW.md`
    *   `PROOF.md`
    *   `AGENTS.md` (if applicable)
*   **Commands to Run:**
    *   `rg -n $'\u2013|\u2014' README.md docs/OVERVIEW.md PROOF.md AGENTS.md` (baseline count of en/em dashes)
*   **Action:** Manually restructure every sentence containing a dash. For example, list items using en dashes for definitions become colon definitions (`- Item: description`). Parenthetical thoughts convert to actual parentheses or distinct sentences.
*   **Verification:** Re-run the Unicode dash search on these files to ensure 0 hits. Self-review the text to guarantee grammatical soundness and adherence to Section 10 of `AGENTS.md`.
*   **Estimated Operator Review Point:** After Phase 1 completion, to ensure the new prose style meets expectations before scaling to the rest of the repository.

## Phase 2: Core Documentation

*   **Files Touched:**
    *   `docs/core/*.md`
    *   `docs/rh/*.md`
    *   `docs/RESULTS.md`
    *   Other supporting documents directly within `docs/`.
*   **Commands to Run:**
    *   `rg -n $'\u2013|\u2014' docs/core/ docs/rh/ docs/RESULTS.md`
*   **Action:** Systematically rewrite sentences containing en/em dashes in foundational explanations. Prefer colons, commas, parentheses, or split sentences. Never leave `  to  ` as a stand-in for a title en dash.
*   **Verification:** Zero Unicode dash hits in `docs/core/` and `docs/rh/`.

## Phase 3: Broad Research Directory Remediation

*   **Files Touched:**
    *   All markdown and text files within the `research/` directory, which likely holds the bulk of the instances.
*   **Commands to Run:**
    *   `rg -n $'\u2013|\u2014' research/`
*   **Action:** Because the research directory is vast, this phase will be broken down into sub-batches (e.g., `research/00-index/`, `research/remainders/`, etc.) to carefully restructure the technical notes without altering the math or meaning.
*   **Verification:** Zero Unicode dash hits in the specified sub-batches.
*   **Estimated Operator Review Point:** Mid-way through Phase 3 to confirm no technical meaning is being lost during sentence restructuring.

## Phase 4: Final Global Verification and Polish

*   **Files Touched:**
    *   Any remaining source code files, scripts, or obscure documentation.
*   **Commands to Run:**
    *   `rg -n $'\u2013|\u2014' .` (global search; may exclude binary dirs as needed)
*   **Action:** Catch any straggling en/em dash characters. Repair accidental replacement artifacts such as glued colons (`word:word`) or title separators written as `  to  `. Prefer `:` / comma / ASCII `-` with normal spacing. Perform a final read-through of major modified sections.
*   **Verification:** The global Unicode dash search must return 0 hits on tracked text files (or only documented exceptions). Spot-check that title separators use `:` or ` - `, not `  to  `.
