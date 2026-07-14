# PGS Quartet hard gate — RETIRED (2026-07-13)

**Status:** retired. Principal preference: use `/expert` and `/heavy` skills
instead of the four-role Quartet spawn lock.

This directory keeps the gate implementation for history and offline tests only.
It must **not** be re-installed under `~/.grok/hooks/` as an active always-on
hook without an explicit principal request.

## Live multi-agent policy

| Slash | Spec |
| --- | --- |
| `/expert` | `~/.grok/skills/expert/SKILL.md` (4 specialists) |
| `/heavy` | `~/.grok/skills/heavy/SKILL.md` (12 specialists) |
| `/normal` | `~/.grok/skills/normal/SKILL.md` |

Repo contract: `AGENTS.md` → **Multi-agent effort (Expert / Heavy) — PGS Quartet
retired**.

## Layout (historical)

| Path | Purpose |
| --- | --- |
| `bin/pgs_quartet_gate.py` | Former gate logic (allow/deny + turn ledger + sticky/env) |
| `bin/pgs-quartet` | Sticky on/off/status helper (still writes sticky file) |
| `pgs-quartet-gate.json` | Former project hook registration (**do not re-trust as required**) |
| `tests/test_pgs_quartet_gate.py` | Offline unit tests for the retired gate |
| `../agents/_retired/pgs-quartet-2026-07-13/` | Archived four agent types |
| `../rules/pgs-quartet-hard-gate.md` | Retirement notice |

Global install (if still present) should be named
`~/.grok/hooks/pgs-quartet-gate.json.retired-*` so the harness does not load it.

## Sticky / env (legacy only)

```bash
pgs-quartet off       # sticky OFF
pgs-quartet status
```

Sticky file: `~/.grok/state/pgs-quartet-enabled` — keep at `0`.

Env `PGS_QUARTET=0` on the hourly relay remains a belt-and-suspenders no-op once
the global hook is uninstalled.

## Offline tests (optional archaeology)

```bash
python3 .grok/hooks/tests/test_pgs_quartet_gate.py -v
```
