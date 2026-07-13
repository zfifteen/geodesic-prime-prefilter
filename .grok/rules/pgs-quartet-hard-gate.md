# PGS Quartet Hard Gate (Machine Enforced)

When the gate is **ON**, a PreToolUse hook blocks parent tools until the four
real Quartet subagents are spawned this user turn.

**OFF is operational usability only.** It does not change PGS research rules,
proof status, or the QA closing gate. It only stops the machine spawn lock.

## Toggle (sticky, cross-session)

```bash
pgs-quartet off      # gate OFF (parent tools unrestricted)
pgs-quartet on       # gate ON  (spawn-four required every user turn)
pgs-quartet status   # sticky file + effective setting
```

Sticky file the hook reads on every PreToolUse:

```text
~/.grok/state/pgs-quartet-enabled
```

| Sticky content | Meaning |
| --- | --- |
| `0` / `off` | OFF |
| `1` / `on` | ON |
| missing | default **OFF** |

Helper: `~/.grok/bin/pgs-quartet` (repo copy: `.grok/hooks/bin/pgs-quartet`).
Takes effect on the next PreToolUse; no CLI restart.

### Process env (Grok CLI process only)

Must be set on the **Grok CLI process**. Setting these only inside a blocked
`run_terminal_command` does nothing (PreToolUse never runs that command).

| Env | Effect |
| --- | --- |
| `PGS_QUARTET=0` or `PGS_QUARTET_ENABLED=0` | Gate OFF |
| `PGS_QUARTET=1` or `PGS_QUARTET_ENABLED=1` | Gate ON (overrides sticky file) |
| `PGS_QUARTET_BYPASS=1` | Emergency OFF |

Priority: bypass env > `PGS_QUARTET_ENABLED` / `PGS_QUARTET` > sticky file > default OFF.

Preferred disable path when the parent is already locked: run `pgs-quartet off`
in an external terminal (or any shell that is not blocked by this hook).

## When ON: every user turn (parent session)

Before any non-orchestration tool, call `spawn_subagent` **four times** with:

| Role | `subagent_type` | Typical settings |
| --- | --- | --- |
| Implementer | `pgs-implementer` | `background=true`, `isolation=worktree` |
| Adversarial Auditor | `pgs-auditor` | `background=true`, `capability_mode=read-only` or `all` |
| Empirical Verifier | `pgs-verifier` | `background=true`, `capability_mode=execute` or `all` |
| Continuity Scribe | `pgs-scribe` | `background=true`, `capability_mode=read-write` or `all` |

## Allowed before the quartet is filled (gate ON only)

Only: `spawn_subagent`, `get_command_or_subagent_output`,
`wait_commands_or_subagents`, `kill_command_or_subagent`, `todo_write`,
`update_goal`, `ask_user_question`.

Everything else is **denied** until all four types are recorded this turn.

## Workflow (when gate ON)

1. Spawn all four (prefer parallel background).
2. Implementer drafts.
3. Auditor and Verifier pressure in parallel.
4. Scribe documents after approval pressure.
5. Orchestrator merges only after consensus.
6. Run the universal QA closing gate.

## Do not (when gate ON)

- Print a team acknowledgment instead of spawning
- Use `explore` / `plan` / `general-purpose` as substitutes for the four types
- Work solo on the parent and claim the Quartet ran
- Expect `export PGS_QUARTET=0` or `PGS_QUARTET_BYPASS=1` inside a blocked shell
  tool to unlock the parent

## When OFF

PreToolUse allows all tools immediately. No spawn requirement.

Still in force under OFF:

- QA closing gate in `AGENTS.md`
- PGS-first framing, state separation, and proof contract

OFF only disables machine spawn enforcement.
