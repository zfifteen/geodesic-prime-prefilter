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

## Ledger

Append one block to `research/04-bounded-compression/docs/square_branch_hourly.md` with:

- Mechanism, Method, Result
- Research status and Ops status
- Delta line
- Artifacts, Next step

## Rocket.Chat

- After every activation ends, post once to `#Prime-Gap-Structure` as `grok`.
- Message leads with Research status and a one-line Delta.
- Rocket.Chat failure is ops-only. It must not erase research results.
- Canonical truth remains the ledger and `~/logs/pgs-hourly/last_run.json`.

## Read-first (every activation)

1. `Agents.md`
2. `PROOF.md` theorem status only
3. `ACTIVE_TARGET.md`
4. This contract
5. Last ledger block in `square_branch_hourly.md`
