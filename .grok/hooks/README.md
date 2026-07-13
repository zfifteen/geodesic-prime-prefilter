# PGS Quartet hard gate

When **ON**, parent sessions inside `prime-gap-structure` must spawn four real
subagents every user turn before other tools run.

When **OFF**, the machine spawn lock is disabled. That is operational usability
only: it does not change PGS research rules, proof status, or the QA gate.

## Layout

| Path | Purpose |
| --- | --- |
| `bin/pgs_quartet_gate.py` | Gate logic (allow/deny + turn ledger + sticky/env) |
| `bin/pgs-quartet` | Sticky on/off/status helper (install to `~/.grok/bin/`) |
| `pgs-quartet-gate.json` | Project hook registration |
| `tests/test_pgs_quartet_gate.py` | Offline unit tests |
| `../agents/pgs-*.md` | The four spawnable agent types |
| `../rules/pgs-quartet-hard-gate.md` | Prompt-side hard rule + toggle cheat sheet |
| `~/.grok/hooks/pgs-quartet-gate.json` | **Always-trusted global install** pointing at this script |
| `~/.grok/state/pgs-quartet-enabled` | Sticky enable flag (`0`/`1`) |

Global install is required because project hooks are silent until `/hooks-trust`.
The global hook only enforces when `cwd` / workspace contains `prime-gap-structure`.

## Toggle (preferred)

```bash
pgs-quartet off       # sticky OFF: parent tools unrestricted
pgs-quartet on        # sticky ON: spawn-four required again
pgs-quartet status
```

Sticky file the hook reads every PreToolUse:

```text
~/.grok/state/pgs-quartet-enabled   # 0=off, 1=on; missing=default OFF
```

Helper: `~/.grok/bin/pgs-quartet` (repo: `.grok/hooks/bin/pgs-quartet`).
Takes effect on the next PreToolUse; no CLI restart.

If the parent is already locked, run `pgs-quartet off` in an **external**
terminal (a shell that is not waiting on a denied tool).

### Process env (Grok CLI process only)

These must be set for the **Grok CLI process**. Putting them only inside a
blocked `run_terminal_command` does nothing (PreToolUse denies before the
command runs).

| Env | Effect |
| --- | --- |
| `PGS_QUARTET=0` or `PGS_QUARTET_ENABLED=0` | Gate OFF |
| `PGS_QUARTET=1` or `PGS_QUARTET_ENABLED=1` | Gate ON (overrides sticky file) |
| `PGS_QUARTET_BYPASS=1` | Emergency OFF |

Priority: bypass > `PGS_QUARTET_ENABLED` / `PGS_QUARTET` > sticky file > default OFF.

## Activate in a running TUI

1. `/hooks` then reload (`r`), or start a new session.
2. Confirm the gate appears under Global hooks.
3. Optional: `/hooks-trust` so the project-local copy is also active.

## Verify

```bash
python3 .grok/hooks/tests/test_pgs_quartet_gate.py -v
pgs-quartet status
```

Live harness checks (grok 0.2.93, 2026-07-11; gate ON):

| Case | Result |
| --- | --- |
| Parent `read_file` before quartet | **Denied** (`cancellationCategory=HookDenied`) |
| Four `pgs-*` spawns then `read_file` | **Allowed**; ledger records all four roles |
| Next user turn without re-spawn | **Denied** again (turn ledger reset) |
| Child tools (`subagentType` present) | **Allowed** |
| Wrong `subagent_type` (e.g. `explore`) before complete | **Denied** |
| Sticky file `0` or process env off | **Allowed** without spawn |

## Harness behaviors that matter

1. **Spawn first within a turn (gate ON).** A PreToolUse deny cancels the whole
   turn (`HookDenied`). The model cannot recover mid-turn after a blocked tool.
2. **SubagentStart payload:** `sessionId` is the **parent**; `subagentId` is the
   child. The gate marks only `subagentId` as open.
3. **Child PreToolUse** includes `subagentType` and is not gated.

## State

Per-session turn ledger: `~/.grok/pgs-quartet-state/<session_id>.json`

Parent ledgers must keep `"is_subagent": false`. Child ledgers use the child
session id and `"is_subagent": true`.
