# Hourly Square-Branch Research Relay Contract

**Updated:** 2026-07-13  
**LaunchAgent:** `com.velocityworks.pgs-hourly-advance`  
**Task branch:** `codex/hourly-square-branch`  
**Isolated root:** `~/pgs-hourly/prime-gap-structure`

## Purpose

Each scheduled activation must either move a PGS frontier object or record an
honest non-progress outcome. Process completion alone is not success.

The historical name of this relay is "hourly." That name is a stable label for
paths, logs, and the LaunchAgent. It is **not** the live cadence.

## Schedule (live ops)

| Field | Value |
| --- | --- |
| Cadence | **Every 4 hours** |
| launchd key | `StartInterval` |
| Seconds | `14400` |
| Plist (repo) | `scripts/launchd/com.velocityworks.pgs-hourly-advance.plist` |
| Plist (loaded) | `~/Library/LaunchAgents/com.velocityworks.pgs-hourly-advance.plist` |
| Log root | `~/logs/pgs-hourly/` |

One **activation** means one LaunchAgent fire of `scripts/pgs-hourly-advance.sh`
that acquires the single-flight lock and runs the dispatcher (or analytic Grok
path). The contract still says "per activation" everywhere else; do not rewrite
every "hour" token in legacy ledgers. New prose should prefer **activation** or
**4h cycle** when the schedule itself matters.

If the installed LaunchAgent and the repo plist disagree on `StartInterval`,
treat the **loaded** agent as ops reality and open a hygiene fix so both match
`14400`.

## Effort mode: `/heavy`; PGS Quartet retired (ops policy)

**Status class:** operator preference / ops config. Not a theorem, not measured
math, and not program-level verified language.

**Principal standing preference (2026-07-13):** keep the **4h** schedule and
execute scheduled analytic activations with **`/heavy`**. The **PGS Quartet is
retired globally** (sticky OFF, global hook uninstalled, agent defs archived);
interactive and relay paths both use Expert/Heavy skills when multi-agent depth
is wanted, not the four-role PreToolUse gate.

**Hourly / 4h relay activations:**

| Rule | Requirement |
| --- | --- |
| Analytic effort | Leading **`/heavy`** slash skill in the wrapper-built prompt |
| Fixed Quartet roles | **Do not spawn** (roles retired; archive only) |
| Parent tools | Unrestricted by Quartet (gate retired) |
| Legacy env (harmless belt-and-suspenders) | `PGS_QUARTET=0` / `PGS_QUARTET_ENABLED=0` may remain on LaunchAgent + wrapper |

### Why (observable mechanism)

The square-branch relay is a **headless activation**: one queue item, one ledger
block, one Rocket.Chat memo. Multi-agent depth, when used, comes from the
**Heavy** skill policy (`/heavy`), not from a machine spawn lock on four
named roles. Global Quartet retirement removes HookDenied risk from the former
hard gate.

### Enforcement wiring (implementation)

| Layer | Behavior |
| --- | --- |
| Global Quartet | Retired: sticky `0`, hook file renamed `*.retired-*`, agents under `_retired/` |
| LaunchAgent env | Optional `PGS_QUARTET=0`, `PGS_QUARTET_ENABLED=0` (legacy) |
| Wrapper defaults | Same optional exports |
| Analytic prompt file | `/heavy` + no retired Quartet roles |
| Analytic effort | Leading `/heavy` in the wrapper-built prompt |

### What still applies

Retirement of the Quartet does **not** relax:

- PGS-first framing;
- theorem / measured / audit / hypothesis / unresolved / invalidated separation;
- `PROOF.md` theorem status;
- Mandatory `10^18` evidence surface for verified / validated language;
- Quality Assurance closing discipline for the activation's own deliverable
  (ledger honesty, status labels, commit policy).

### What this is not

- Not permission to use classical inference as PGS gates.
- Not a theorem claim and not program-level verification language.
- Not a requirement to fan out 12 agents on every relay job if the Heavy skill
  solo waiver or prompt path keeps the job solo (see analytic prompt + wrapper).

## Isolation

- Execution runs only in the isolated worktree (`PGS_ROOT`).
- The human IdeaProjects checkout may be dirty. That must never skip the activation.
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

Relay bands below `10^18` are **audit corroboration** or **measured on band B**
only. They do not authorize program-level verified / validated language for an
implementation. That language still requires the mandatory executed `10^18`
surface in root `AGENTS.md` (**Mandatory 10^18 Evidence Surface**). Relay work
must not promote mid-band green into theorem or program-level validation prose.

## Queue policy

- Execute exactly one queue item per activation.
- After each completed attempt (`ADVANCE`, `NO_DELTA`, `FAILED`, `UNRESOLVED`), rotate the queue so `NO_DELTA` escalates to the next frontier job.
- Default falsification bands must extend beyond already certified regimes.
- When a job claims high-scale behavior, prefer bands that include magnitude
  `10^18` (or state honestly that the activation is audit-on-band only).

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

Never end an activation with uncommitted research or ops artifacts in the
isolated worktree. A research `FAILED` (missing script, nonzero exit, pytest
red) is still a commit: ledger + queue rotation + any partial outputs.

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
  - **What this activation actually did** (job id, mechanism, delta)
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
  activation. Emergency override only: `--force-same-activation` (do not use in
  the LaunchAgent path).

## Read-first (every activation)

1. `Agents.md`
2. `PROOF.md` theorem status only
3. `ACTIVE_TARGET.md`
4. This contract (schedule = 4h; `/heavy`; Quartet off for this path)
5. Last ledger block in `square_branch_hourly.md`
