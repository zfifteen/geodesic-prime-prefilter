# PGS Lean core-stack hourly heartbeat

**Principal:** 2026-07-18 — keep Lean 4 effort moving in #Prime-Gap-Structure; hourly until goal; then disable.  
**Owner / lead:** Hermes  
**Goal:** program DoD in `lean-4/DEFINITION_OF_DONE.md` (machine-checked core stack mirror; PROOF.md authority unchanged).

## Pieces

| Piece | Path |
| --- | --- |
| LaunchAgent label | `com.velocityworks.pgs-lean-heartbeat` |
| Repo plist | `scripts/launchd/com.velocityworks.pgs-lean-heartbeat.plist` |
| Installed plist | `~/Library/LaunchAgents/com.velocityworks.pgs-lean-heartbeat.plist` |
| Schedule | **Hourly** `StartInterval` 3600 |
| Runner | `scripts/lean-heartbeat/lean-core-stack-heartbeat.sh` |
| Prompt | `scripts/lean-heartbeat/lean-core-stack-heartbeat-prompt.txt` |
| Goal check | `scripts/lean-heartbeat/lean_goal_done_check.py` |
| RC notify | `scripts/lean-heartbeat/lean_heartbeat_rc_notify.py` → **#Prime-Gap-Structure** |
| State | `scripts/lean-heartbeat/LEAN_HEARTBEAT_STATE.md` |
| Logs | `~/logs/pgs-lean-heartbeat/` |

## Each fire

1. If state disabled or goal-done check passes → **bootout** LaunchAgent, post disable note, exit 0.  
2. Else run Hermes headless (`-p idea`) on the prompt (cwd repo root).  
3. Write `last_run.json` (Hermes or fallback).  
4. Post `rc_summary` into #Prime-Gap-Structure (may include peer `@tags` for real handoffs).

## Disable conditions (any)

- `LEAN_HEARTBEAT_STATE.md` has `enabled: false`  
- File `lean-4/LEAN_PROGRAM_DONE.md` exists (owner program accept)  
- Auto check: zero `sorry` in `lean-4/PGS/*.lean` **and** `lean-4/peer/M0_DOD_ACCEPT.md` exists **and** inventory has no open M1–M5 blockers noted as remaining — conservative auto path is **owner DONE file** preferred; auto-sorry-zero alone is a **candidate** disable that still requires owner DONE file for final disable to avoid premature stop after M1 only.

**Implemented auto-disable:** owner DONE file **or** explicit state `enabled: false`.  
**Auto-suggest (log only):** zero sorry in PGS/*.lean after lake build green — Hermes should then write DONE when full DoD met.

## Ops

```bash
# status
launchctl print "gui/$(id -u)/com.velocityworks.pgs-lean-heartbeat" | head -40

# manual fire
bash ~/IdeaProjects/prime-gap-structure/scripts/lean-heartbeat/lean-core-stack-heartbeat.sh

# install / reload
cp ~/IdeaProjects/prime-gap-structure/scripts/launchd/com.velocityworks.pgs-lean-heartbeat.plist \
  ~/Library/LaunchAgents/
launchctl bootout "gui/$(id -u)/com.velocityworks.pgs-lean-heartbeat" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" ~/Library/LaunchAgents/com.velocityworks.pgs-lean-heartbeat.plist

# force disable without DONE
# edit LEAN_HEARTBEAT_STATE.md → enabled: false, then next fire bootouts
```
