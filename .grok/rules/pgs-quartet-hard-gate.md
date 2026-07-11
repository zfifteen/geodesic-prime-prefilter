# PGS Quartet Hard Gate (Machine Enforced)

This is not optional prose. A PreToolUse hook blocks parent tools until the
team is actually spawned.

## Every user turn (parent session)

Before any non-orchestration tool, call `spawn_subagent` **four times** with:

| Role | `subagent_type` | Typical settings |
| --- | --- | --- |
| Implementer | `pgs-implementer` | `background=true`, `isolation=worktree` |
| Adversarial Auditor | `pgs-auditor` | `background=true`, `capability_mode=read-only` or `all` |
| Empirical Verifier | `pgs-verifier` | `background=true`, `capability_mode=execute` or `all` |
| Continuity Scribe | `pgs-scribe` | `background=true`, `capability_mode=read-write` or `all` |

## Allowed before the quartet is filled

Only: `spawn_subagent`, `get_command_or_subagent_output`,
`wait_commands_or_subagents`, `kill_command_or_subagent`, `todo_write`,
`update_goal`, `ask_user_question`.

Everything else is **denied** by the gate until all four types are recorded
for the current user turn.

## Workflow

1. Spawn all four (prefer parallel background).
2. Implementer drafts.
3. Auditor and Verifier pressure in parallel.
4. Scribe documents after approval pressure.
5. Orchestrator merges only after consensus.
6. Run the universal QA closing gate.

## Do not

- Print a team acknowledgment instead of spawning
- Use `explore` / `plan` / `general-purpose` as substitutes for the four types
- Work solo on the parent and claim the Quartet ran

## Emergency only

`PGS_QUARTET_BYPASS=1` disables the gate for recovery. Do not use it for normal work.
