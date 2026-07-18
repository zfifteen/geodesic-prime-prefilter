#!/usr/bin/env bash
# PGS Lean core-stack hourly heartbeat — launchd StartInterval 3600
# Hermes advances Lean toward DEFINITION_OF_DONE; posts into #Prime-Gap-Structure.
# Auto-disables when LEAN_HEARTBEAT_STATE enabled:false or lean-4/LEAN_PROGRAM_DONE.md exists.
#
# Usage: ./scripts/lean-heartbeat/lean-core-stack-heartbeat.sh
# Label: com.velocityworks.pgs-lean-heartbeat

set -euo pipefail

export PATH="${HOME}/.local/bin:${HOME}/.grok/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="${HOME:-/Users/velocityworks}"

PYTHON_BIN="${PYTHON_BIN:-$(command -v python3)}"
HERMES_BIN="${HERMES_BIN:-$(command -v hermes)}"
REPO_ROOT="${REPO_ROOT:-$HOME/IdeaProjects/prime-gap-structure}"
HB_DIR="${HB_DIR:-$REPO_ROOT/scripts/lean-heartbeat}"
LOG_DIR="${LOG_DIR:-$HOME/logs/pgs-lean-heartbeat}"
LOCK_DIR="${LOCK_DIR:-$LOG_DIR/heartbeat.lock.d}"
PROMPT_FILE="${PROMPT_FILE:-$HB_DIR/lean-core-stack-heartbeat-prompt.txt}"
GOAL_CHECK="${GOAL_CHECK:-$HB_DIR/lean_goal_done_check.py}"
NOTIFY="${NOTIFY:-$HB_DIR/lean_heartbeat_rc_notify.py}"
LAST_RUN="${LAST_RUN:-$LOG_DIR/last_run.json}"
STATE_FILE="${STATE_FILE:-$HB_DIR/LEAN_HEARTBEAT_STATE.md}"
LABEL="${LABEL:-com.velocityworks.pgs-lean-heartbeat}"
export RC_BASE="${RC_BASE:-http://127.0.0.1:3000}"
export PGS_LEAN_HB_RC_CHANNEL="${PGS_LEAN_HB_RC_CHANNEL:-Prime-Gap-Structure}"
export PGS_LEAN_HB_ROOM_ID="${PGS_LEAN_HB_ROOM_ID:-6a4f9a42b0e299fde39d6a14}"
export PGS_LEAN_HB_LAST_RUN="$LAST_RUN"
export LOG_DIR

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_DIR/heartbeat.log"
}

acquire_lock() {
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    echo "$$" >"$LOCK_DIR/pid"
    return 0
  fi
  if [[ -d "$LOCK_DIR" ]]; then
    local age
    age=$(( $(date +%s) - $(stat -f %m "$LOCK_DIR" 2>/dev/null || echo 0) ))
    if (( age > 5400 )); then
      log "breaking stale lock age=${age}s"
      rm -rf "$LOCK_DIR"
      mkdir "$LOCK_DIR"
      echo "$$" >"$LOCK_DIR/pid"
      return 0
    fi
  fi
  return 1
}

release_lock() {
  rm -rf "$LOCK_DIR" 2>/dev/null || true
}

write_last_run() {
  local unit="$1"
  local ops="${2:-OK}"
  local next="${3:-}"
  local disable_reason="${4:-}"
  "$PYTHON_BIN" - "$LAST_RUN" "$unit" "$ops" "$next" "$disable_reason" <<'PY'
import json, sys
from datetime import datetime, timezone
path, unit, ops, nxt, dis = sys.argv[1:6]
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
payload = {
    "activated_at": now,
    "completed_at": now,
    "ops_status": ops,
    "unit_done": unit,
    "paths_touched": [],
    "peer_handoffs": "",
    "rc_summary": unit,
    "next_step": nxt,
    "disable_reason": dis or None,
}
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
}

notify_rc() {
  set +e
  "$PYTHON_BIN" "$NOTIFY" "$LAST_RUN" >>"$LOG_DIR/heartbeat.log" 2>&1
  local rc=$?
  set -e
  if [[ "$rc" -ne 0 ]]; then
    log "rocketchat notify failed (non-fatal) exit=$rc"
  else
    log "rocketchat notify ok"
  fi
}

bootout_self() {
  local uid
  uid="$(id -u)"
  set +e
  launchctl bootout "gui/${uid}/${LABEL}" >>"$LOG_DIR/heartbeat.log" 2>&1
  local rc=$?
  set -e
  log "launchctl bootout ${LABEL} exit=$rc"
}

if ! acquire_lock; then
  log "skip — another heartbeat holds lock $LOCK_DIR"
  exit 0
fi
trap release_lock EXIT

# --- disable gate ---
set +e
"$PYTHON_BIN" "$GOAL_CHECK" >"$LOG_DIR/goal_check.out" 2>"$LOG_DIR/goal_check.err"
GC=$?
set -e
cat "$LOG_DIR/goal_check.out" >>"$LOG_DIR/heartbeat.log" || true
if [[ "$GC" -eq 0 ]]; then
  REASON="$(head -1 "$LOG_DIR/goal_check.out" 2>/dev/null || echo DISABLE)"
  log "goal/state disable: $REASON"
  write_last_run "Lean hourly heartbeat disabled. $REASON" "DONE" "none" "$REASON"
  export PGS_LEAN_HB_DISABLED_POST=1
  notify_rc
  bootout_self
  # keep state file honest
  if [[ -f "$STATE_FILE" ]]; then
    "$PYTHON_BIN" - "$STATE_FILE" <<'PY' || true
from pathlib import Path
import re, sys
p = Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t2 = re.sub(r"(?im)^(\s*enabled\s*:\s*)true(\s*)$", r"\1false\2", t, count=1)
if t2 != t:
    p.write_text(t2, encoding="utf-8")
PY
  fi
  log "disabled and exiting"
  exit 0
fi
if [[ "$GC" -eq 2 ]]; then
  log "goal check error — continuing cautiously"
fi

if [[ ! -x "$HERMES_BIN" ]] && ! command -v "$HERMES_BIN" >/dev/null 2>&1; then
  log "missing hermes binary: $HERMES_BIN"
  write_last_run "Heartbeat blocked: hermes binary not found." "BLOCKED" "Install hermes on PATH"
  notify_rc
  exit 1
fi
if [[ ! -f "$PROMPT_FILE" ]]; then
  log "missing prompt: $PROMPT_FILE"
  write_last_run "Heartbeat blocked: missing prompt file." "FAILED" "Restore prompt file"
  notify_rc
  exit 1
fi

ACTIVATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "pgs lean heartbeat start root=$REPO_ROOT"

TMP_PROMPT="$(mktemp "${TMPDIR:-/tmp}/pgs-lean-heartbeat-prompt.XXXXXX")"
{
  cat "$PROMPT_FILE"
  printf '\n\n## Injected activation context\n'
  printf -- '- Activated at (UTC): %s\n' "$ACTIVATED_AT"
  printf -- '- Repo root: %s\n' "$REPO_ROOT"
  printf -- '- last_run.json (required write): %s\n' "$LAST_RUN"
  printf -- '- RC channel: #%s room_id=%s\n' "$PGS_LEAN_HB_RC_CHANNEL" "$PGS_LEAN_HB_ROOM_ID"
  printf -- '- After finish, script posts rc_summary to #Prime-Gap-Structure.\n'
  printf -- '- Effort lead: hermes. Peer FOR: @hermes.\n'
  if [[ -f "$LOG_DIR/goal_check.out" ]]; then
    printf -- '- Goal check: %s\n' "$(tr '\n' ' ' <"$LOG_DIR/goal_check.out")"
  fi
} >"$TMP_PROMPT"

# Hermes oneshot via Python argv list (avoids shell/quoting breakage on large prompts).
set +e
"$PYTHON_BIN" "$HB_DIR/run_hermes_oneshot.py" "$TMP_PROMPT" "$REPO_ROOT" \
  >>"$LOG_DIR/heartbeat.log" 2>&1
HERMES_STATUS=$?
set -e
rm -f "$TMP_PROMPT"

if [[ ! -f "$LAST_RUN" ]]; then
  log "hermes finished but last_run.json missing (exit=$HERMES_STATUS) — writing fallback"
  write_last_run \
    "Lean heartbeat Hermes exit=$HERMES_STATUS without last_run.json. Check heartbeat.log." \
    "PARTIAL" \
    "Re-run heartbeat or open #Prime-Gap-Structure @hermes"
fi

"$PYTHON_BIN" - "$LAST_RUN" "$ACTIVATED_AT" <<'PY' || true
import json, sys
from datetime import datetime, timezone
path, activated = sys.argv[1:3]
try:
    data = json.loads(open(path, encoding="utf-8").read())
except Exception:
    data = {}
data.setdefault("activated_at", activated)
data.setdefault("completed_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
open(path, "w", encoding="utf-8").write(json.dumps(data, indent=2) + "\n")
PY

# If Hermes marked program done this fire, flip state for next gate
if [[ -f "$REPO_ROOT/lean-4/LEAN_PROGRAM_DONE.md" ]]; then
  log "owner DONE file present after fire — will disable next gate path now"
  write_last_run "$(python3 -c "import json;print(json.load(open('$LAST_RUN')).get('rc_summary','Lean program DONE'))")" "DONE" "none" "owner_done_file"
  export PGS_LEAN_HB_DISABLED_POST=1
  notify_rc
  bootout_self
  exit 0
fi

notify_rc

if [[ "$HERMES_STATUS" -ne 0 ]]; then
  log "pgs lean heartbeat finished with hermes exit=$HERMES_STATUS"
  exit "$HERMES_STATUS"
fi
log "pgs lean heartbeat completed ok"
exit 0
