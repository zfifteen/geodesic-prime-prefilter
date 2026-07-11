# PGS Quartet hard gate

Machine enforcement that parent sessions inside `prime-gap-structure` must spawn
four real subagents every user turn before other tools run.

## Layout

| Path | Purpose |
| --- | --- |
| `bin/pgs_quartet_gate.py` | Gate logic (allow/deny + turn ledger) |
| `pgs-quartet-gate.json` | Project hook registration |
| `tests/test_pgs_quartet_gate.py` | Offline unit tests |
| `../agents/pgs-*.md` | The four spawnable agent types |
| `../rules/pgs-quartet-hard-gate.md` | Prompt-side hard rule text |
| `~/.grok/hooks/pgs-quartet-gate.json` | **Always-trusted global install** pointing at this script |

Global install is required because project hooks are silent until `/hooks-trust`.
The global hook only enforces when `cwd` / workspace contains `prime-gap-structure`.

## Activate in a running TUI

1. `/hooks` then reload (`r`), or start a new session.
2. Confirm the gate appears under Global hooks.
3. Optional: `/hooks-trust` so the project-local copy is also active.

## Verify

```bash
python3 .grok/hooks/tests/test_pgs_quartet_gate.py -v
```

Live harness checks (grok 0.2.93, 2026-07-11):

| Case | Result |
| --- | --- |
| Parent `read_file` before quartet | **Denied** (`cancellationCategory=HookDenied`) |
| Four `pgs-*` spawns then `read_file` | **Allowed**; ledger records all four roles |
| Next user turn without re-spawn | **Denied** again (turn ledger reset) |
| Child tools (`subagentType` present) | **Allowed** |
| Wrong `subagent_type` (e.g. `explore`) before complete | **Denied** |

## Harness behaviors that matter

1. **Spawn first within a turn.** A PreToolUse deny cancels the whole turn
   (`HookDenied`). The model cannot recover mid-turn after a blocked tool.
2. **SubagentStart payload:** `sessionId` is the **parent**; `subagentId` is the
   child. The gate marks only `subagentId` as open.
3. **Child PreToolUse** includes `subagentType` and is not gated.

## State

Per-session turn ledger: `~/.grok/pgs-quartet-state/<session_id>.json`

Parent ledgers must keep `"is_subagent": false`. Child ledgers use the child
session id and `"is_subagent": true`.

## Bypass (recovery only)

```bash
export PGS_QUARTET_BYPASS=1
```
