# PGS Quartet Hard Gate — RETIRED (2026-07-13)

**Status:** retired. Do not re-enable without an explicit principal request.

The four-role PreToolUse spawn lock (`pgs-implementer`, `pgs-auditor`,
`pgs-verifier`, `pgs-scribe`) is no longer part of the live contract.

## Replacement

| Slash skill | Role |
| --- | --- |
| `/expert` | Fixed team of 4 local analytic specialists + leader synthesis |
| `/heavy` | Fixed team of 12 local analytic specialists (≥1 contrarian) + leader synthesis |
| `/normal` | Clear Expert/Heavy overlays |

Canonical skill bodies: `~/.grok/skills/{expert,heavy,normal}/SKILL.md`.

Parent `AGENTS.md` section: **Multi-agent effort (Expert / Heavy) — PGS Quartet
retired**.

## What remains in force

- Universal QA closing gate in `AGENTS.md`
- PGS-first framing, state separation, and proof contract
- Mandatory `10^18` evidence surface for program-level verified / validated language

## Historical artifacts (do not load as live agents)

- Agent defs: `.grok/agents/_retired/pgs-quartet-2026-07-13/`
- Hook script / tests: `.grok/hooks/` (gate logic retained for archaeology only)
- Sticky file (if present): `~/.grok/state/pgs-quartet-enabled` should stay `0`
- Global hook install was renamed to
  `~/.grok/hooks/pgs-quartet-gate.json.retired-2026-07-13` so it does not load
