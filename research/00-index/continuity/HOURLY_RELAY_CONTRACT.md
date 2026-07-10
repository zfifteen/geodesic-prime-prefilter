# Hourly Square-Branch Research Relay Contract

**Updated:** 2026-07-10  
**LaunchAgent:** `com.velocityworks.pgs-hourly-advance`  
**Task branch:** `codex/hourly-square-branch`  
**Isolated root:** `~/pgs-hourly/prime-gap-structure`

## Purpose

One activation per hour must either move a PGS frontier object or record an honest
non-progress outcome. Process completion alone is not success.

## Isolation

- Execution runs only in the isolated worktree (`PGS_ROOT`).
- The human IdeaProjects checkout may be dirty. That must never skip the hour.
- Never stash, reset, or commit unrelated human work in IdeaProjects.

## Status labels

### Research status

| Label | Meaning |
| --- | --- |
| `ADVANCE` | New measured regime, new residual claim, new falsification, or new constructive proof-pressure artifact with a falsification command |
| `NO_DELTA` | Command succeeded but the scientific signature matches a prior baseline (replay) |
| `FAILED` | Command or pytest failed |
| `UNRESOLVED` | Ran without a decisive delta or failure (explicit open state) |

### Ops status

| Label | Meaning |
| --- | --- |
| `OK` | Isolation, run, ledger, and commit path completed; push optional |
| `PARTIAL` | Research path produced artifacts but push or secondary step failed |
| `BLOCKED` | Could not start (lock held, worktree bootstrap failure) |
| `FAILED` | Ops machinery crashed before a research status was established |

`ADVANCE` requires a concrete artifact delta. Pytest green alone is not enough.

## Queue policy

- Execute exactly one queue item per activation.
- After each completed attempt (`ADVANCE`, `NO_DELTA`, `FAILED`, `UNRESOLVED`), rotate the queue so `NO_DELTA` escalates to the next frontier job.
- Default falsification bands must extend beyond already certified regimes.

## Commit policy (mandatory)

After **every** activation ends, regardless of research status
(`ADVANCE`, `NO_DELTA`, `FAILED`, `UNRESOLVED`):

1. Append the ledger block.
2. Stage and **commit** on `codex/hourly-square-branch`:
   - relay code + queue + ledger + signatures + contract/ACTIVE_TARGET
   - queue command scripts that exist on disk
   - `summary_json`, sibling frontier CSV, companion `*.json`, and local `FINDINGS.md`
   - gitignored measured summaries under `**/output/*` via `git add -f`
3. Push to `origin/codex/hourly-square-branch` when network allows
   (`ops=PARTIAL` if push fails; local commit must still exist).

Never end an hour with uncommitted research or ops artifacts in the isolated
worktree. A research `FAILED` (missing script, nonzero exit, pytest red) is
still a commit: ledger + queue rotation + any partial outputs.

## Ledger

Append one block to `research/04-bounded-compression/docs/square_branch_hourly.md` with:

- Mechanism, Method, Result
- Research status and Ops status
- Delta line
- Artifacts, Next step

## Rocket.Chat

- After every activation ends, post once to `#Prime-Gap-Structure` as `grok`.
- Format is a **thorough structured research memo** (same clarity bar as
  operator Q&A in-channel), rendered by
  `scripts/pgs_hourly_rocketchat_notify.py`:
  - **Headline** in plain English
  - status labels (research · ops)
  - **What this hour actually did** (job id, mechanism, delta)
  - **Measured / residual result** (prose + tables for quantities and RC/P claims)
  - **Why this matters for the schedule** (ADVANCE vs replay vs failed)
  - **Next pressure**
  - **Not claiming** (no theorem inflation, no RH/RSA overclaim)
  - artifacts + branch/commit footnote
- Do not post `key=value` soup as the primary body.
- Rocket.Chat failure is ops-only. It must not erase research results.
- Canonical truth remains the ledger and `~/logs/pgs-hourly/last_run.json`.
- **One post per activation.** Only `scripts/pgs-hourly-advance.sh` may call
  `pgs_hourly_rocketchat_notify.py` (EXIT trap). Analytic/Grok jobs must **not**
  post to Rocket.Chat themselves.
- Dedupe is by **activation key** (`job_id` + `activated_at` [+ `completed_at`]),
  not by memo wording. Reformatting or `--force` alone must not repost the same
  hour. Emergency override only: `--force-same-activation` (do not use in the
  LaunchAgent path).

## Read-first (every activation)

1. `Agents.md`
2. `PROOF.md` theorem status only
3. `ACTIVE_TARGET.md`
4. This contract
5. Last ledger block in `square_branch_hourly.md`
