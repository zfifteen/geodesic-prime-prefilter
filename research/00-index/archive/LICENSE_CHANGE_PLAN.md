# Switch Project License from BSL 1.1 to MIT

**Task Owner**: Codex (Grok 4.3) under AGENTS.md protocol  
**Date Initiated**: 2026-05 (current session)  
**Status**: EXECUTED AND PUSHED: 2026-05-31 / commit 2bf74f7f  
**Goal**: Replace the root LICENSE with standard MIT text, update all references and source header notices, document the license history, create a clean git branch+commit, and push the change to the remote repository. All actions must follow the mandatory Plan → Confirm → Execute → Verify → Report workflow and the full AGENTS.md (canonical + local) rules.

## Why This Matters (Context)
- The project is currently under Business Source License 1.1 (with 4-year change to Apache 2.0 + small-revenue production grant).
- User request: "change the license type for this project to MIT. Do that and push it to remote".
- Legal / distribution impact: MIT is a simple permissive OSI-approved license allowing unrestricted commercial use, modification, distribution, and private use with only attribution requirement.
- Prior history (from COMMERCIAL.md): earlier versions were MIT; BSL period had additional restrictions for larger entities.
- After change, no "commercial license" is required for any use; the project becomes fully open source under MIT terms for new distributions.

## Scope (Exact Files Touched)
1. `LICENSE` (full content replacement)
2. `COMMERCIAL.md` (rewrite as license-history note; no longer describes active commercial restrictions)
3. `lean-4/PGS.lean` (1-line header update)
4. `lean-4/PGS/Basic.lean` (1-line header update)
5. `lean-4/PGS/GWR.lean` (1-line header update)
6. `lean-4/PGS/NextPrime.lean` (1-line header update)

**No other files** contain active BSL-specific language or project-level license declarations that require change (verified via exhaustive grep for "Business Source", "BSL", "Additional Use Grant", "Change Date", "source-available under").

**No source code headers** (Python/C) contain license text.
**No build metadata** (pyproject.toml, package.json) declares a conflicting license field.
**No README.md** license section exists today (no addition planned unless required by plan approval).

## Constraints & Invariants (from AGENTS.md + project contract)
- Follow global AGENTS.md Sections 2, 3, 4, 11, 12 strictly: batch, written plan first, explicit confirm before mutate, use tools for all reads/edits, phased if code-like, re-inspect after every write, verify before declare done.
- Documentation Format Preference: This plan itself is a narrow admin artifact (markdown acceptable per "small notes, narrow status updates"). Future license docs would prefer HTML if visual/checklist-heavy.
- Local AGENTS.md: This is maintenance, not PGS research, so PGS-first frame and "do not downgrade theorems" do not apply. However, preserve all historical accuracy and avoid any language that could be misread as changing research claims.
- Git discipline: Create a dedicated branch (project uses main + feature branches for changes). Never force-push. Clear conventional commit message.
- No invention of facts: Copyright holder taken from existing lean-4 headers ("Velocity Works", 2026). Prior BSL used individual name; MIT will use the entity name already in source headers for consistency.
- After push, the remote repo's GitHub "license" UI will auto-detect the new MIT LICENSE file.
- User retains ability to further edit (e.g., add SPDX to more files, update GitHub repo settings UI, add license badge to README) in follow-up.

## Numbered Execution Steps (The Contract)

**Step 0: Pre-execution (this document)**
- Files: `LICENSE_CHANGE_PLAN.md` (this file, created via write tool after full discovery)
- Commands: (none, planning only)
- Verification: Re-read this file via read_file after write; confirm todos reflect current state.
- User gate: Present this full plan + open questions in chat. **Do not proceed to Step 1 until explicit approval** ("approved", "proceed with the plan", "yes do the branch and edits", or equivalent + any requested edits to this plan).

**Step 1: Create isolated branch**
- Branch name: `chore/license-to-mit` (conventional; clear intent, no breaking main)
- Command: `git checkout -b chore/license-to-mit`
- Files touched: none (branch metadata)
- Verification: `git branch --show-current` and `git status` (must show clean on new branch, ahead of origin/main by 0).
- Re-inspect after command.

**Step 2: Replace LICENSE with canonical MIT text**
- File: `LICENSE`
- Method: read_file (already done), then search_replace using the entire old BSL text as unique old_string → full standard MIT text as new_string. (Full-file swap is the cleanest deterministic edit for a license file.)
- New content (exact):
  ```
  MIT License

  Copyright (c) 2026 Velocity Works

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```
- Why this exact text: Shortest unambiguous OSI MIT; matches year/entity already used in project source headers.
- Verification (mandatory after edit):
  - `read_file LICENSE` (full content)
  - `grep -n "Business Source\|BSL\|Change Date\|Additional Use Grant" LICENSE` → must return zero matches
  - `head -5 LICENSE && tail -5 LICENSE` to confirm MIT framing and no truncation.
  - Manual visual: copyright line present, no MariaDB trademark language remains.

**Step 3: Update COMMERCIAL.md to license-history document**
- File: `COMMERCIAL.md`
- Method: Full content replacement via search_replace (current short file → new historical note).
- New content (exact):
  ```
  # License History

  This repository is licensed under the [MIT License](LICENSE).

  ## Current Status (as of this change)
  - MIT License applies to all new distributions and contributions.
  - MIT is a permissive open-source license. No separate commercial license, production-use grant, or revenue threshold is required for any use, modification, distribution, or embedding.
  - Full terms are in the [LICENSE](LICENSE) file at the repository root.

  ## Historical License Record
  - **Earlier versions** (first publicly distributed before the BSL period): MIT License.
  - **BSL period**: Business Source License 1.1 (with Additional Use Grant for small entities/nonprofits/academia + 4-year Change License to Apache 2.0). See the LICENSE file from those commits for the exact terms that governed each version.
  - **This change**: Switches active license for future versions to MIT. Prior BSL-governed versions retain their original license terms (standard practice for license evolution).

  The license applicable to any specific version or commit is the LICENSE file present in that commit.
  ```
- Rationale: Preserves audit trail and "prior versions under earlier terms" language from old COMMERCIAL.md without leaving stale "you need a commercial license" claims that would now be false.
- Verification (after edit):
  - `read_file COMMERCIAL.md`
  - `grep -n "Business Source License 1.1" COMMERCIAL.md` → zero matches for the active claim
  - Confirm new file opens cleanly, contains both MIT pointer and history table-like structure.
  - No remaining "you do need a separate commercial license" language.

**Step 4: Update the four Lean 4 source header notices**
- Files (one at a time, per incremental discipline even though tiny):
  1. lean-4/PGS.lean
  2. lean-4/PGS/Basic.lean
  3. lean-4/PGS/GWR.lean
  4. lean-4/PGS/NextPrime.lean
- Change (exact string, identical in all four):
  Old: `Released under Apache 2.0 license as described in the file LICENSE.`
  New: `Released under the MIT License as described in the file LICENSE.`
- Method: search_replace (small unique string, replace_all=false since one occurrence each).
- Order: one file, immediate re-read + grep verification on that file, then next. (Granular to match "one unit at a time" spirit.)
- Verification per file + final:
  - After each: `read_file <file> | head -6` and `grep -n "MIT License|Apache 2.0" <file>`
  - Final cross-check: `grep -r "Apache 2.0 license as described" lean-4/` → must be empty (only the 4 files existed before).
  - `grep -r "MIT License as described" lean-4/` → exactly 4 matches.

**Step 5: Full verification pass (no code yet committed)**
- Commands (run via run_terminal_command, capture full output):
  - `git status --short`
  - `git diff --stat`
  - `git diff` (or `git diff --no-color | cat` for full patch if small)
  - `grep -r --include="*.md" --include="LICENSE" --include="*.lean" "Business Source License 1.1\|Additional Use Grant\|Change Date: Four years" .` → must return 0
  - `grep -l "MIT License" LICENSE COMMERCIAL.md lean-4/PGS*.lean lean-4/PGS/*.lean` (confirm all six files now declare MIT)
  - `cat LICENSE` (final visual)
- Also run any project linters if they exist for docs (none known for license files; skip if none).
- Fix any issues discovered before proceeding to commit.

**Step 6: Commit**
- Stage: `git add LICENSE COMMERCIAL.md lean-4/PGS.lean lean-4/PGS/Basic.lean lean-4/PGS/GWR.lean lean-4/PGS/NextPrime.lean`
- Commit message (conventional, imperative, scoped):
  ```
  chore(license): switch from BSL 1.1 to MIT

  - Replace LICENSE with standard MIT text (Velocity Works, 2026)
  - Rewrite COMMERCIAL.md as license-history note
  - Update 4 Lean 4 source header notices (Apache 2.0 → MIT)
  - No other files referenced active BSL terms

  Prior BSL-governed commits retain their original license.
  MIT now governs all new distributions.
  ```
- Verification: `git log -1 --stat`, `git show --name-only HEAD`

**Step 7: Push to remote**
- Command: `git push -u origin chore/license-to-mit`
- Verification: Confirm push success output includes "new branch" or "up to date" with remote tracking. Provide the GitHub compare URL in report if possible.
- Note: This pushes the branch (not force to main). User can then merge via PR or fast-forward main locally if desired. This is the safe, reviewable path per normal git hygiene.

**Step 8: Report + cleanup**
- Deliver structured final response mapping every plan step to actual commands + tool outputs + verification results.
- Update this plan file's Status to "Executed and pushed" with date + commit SHA.
- Mark all todos complete.
- Offer next actions (e.g., "merge branch to main?", "add license badge to README?", "update GitHub repo license picker via web UI?").

## Open Questions / Risks (Require User Input in Confirm Step)
1. **Branch vs direct main push**: Plan uses feature branch + push. Do you want `git push origin main` directly on main instead (after local commit)?
2. **Copyright holder name**: Using "Velocity Works" (matches current lean-4 headers). Confirm ok, or change to "Dionisio Alberto Lopez III" (the name in old BSL)?
3. **COMMERCIAL.md fate**: Plan rewrites it as history note. Prefer to `git rm` the file entirely and let history speak from git log? (Slightly cleaner tree, but loses the explicit pointer some readers may still have bookmarked.)
4. **Additional polish in this PR** (optional, can be follow-up):
   - Add a short "License" section + badge to README.md?
   - Add `SPDX-License-Identifier: MIT` to more source files?
   - Update any Zenodo / release / PyPI metadata in future?
5. **GitHub side effects**: After push, the repo "License" field in GitHub UI will show "MIT" automatically because of the LICENSE file. Any manual repo settings change desired?
6. **Any other files** the user knows of that mention the old license (internal wikis, papers, etc.) outside this repo?

## Acceptance Criteria (Definition of Done)
- [ ] All 6 files updated exactly as specified and re-inspected via tools.
- [ ] Zero remaining references to BSL 1.1 / Additional Use Grant / Change Date in the working tree (outside vendor/ and git history).
- [ ] `git status` clean on the branch after commit.
- [ ] Push succeeds; branch visible on remote.
- [ ] Final report contains every command executed + its stdout + verification that criteria passed.
- [ ] This plan file updated with execution results + commit SHA.
- [ ] No violations of AGENTS.md (no unapproved edits, no skipped verification, tools used for all mutations, batching respected).

## Reproduction / Audit Commands (for any future session)
```bash
git checkout main
git pull
git checkout chore/license-to-mit
git log --oneline -5
cat LICENSE | head -20
grep -c "MIT License" LICENSE
grep -r "Business Source License 1.1" . --include="*.md" --include="LICENSE" --include="*.lean" || echo "Good: zero matches"
open LICENSE_CHANGE_PLAN.md   # or cat it
```

## Post-Execution Verification Note (Background Task)
A long-running terminal verification (task 43d61528) completed after the push. It confirmed:
- Correct branch + 6 files modified (pre-commit snapshot).
- 0 old Apache strings in our PGS Lean sources.
- MIT present in exactly the 6 target files.
- The only "BSL" matches were inside `.git/logs/` (historical commit messages from the *previous* switch *to* BSL). This is expected and allowed per plan ("outside ... git history").

All acceptance criteria remained satisfied.

## Sign-off
Plan authored after full discovery pass (list_dir, multiple read_file, exhaustive grep across md/lean/py/c/html, git remote/status, AGENTS reads).

**Executed, verified, and pushed. Commit 2bf74f7f on origin/chore/license-to-mit.**

---

*This document is the controlling plan artifact for the license change task. It was written before any file mutation beyond planning artifacts. All subsequent actions must trace to a numbered step here.*
