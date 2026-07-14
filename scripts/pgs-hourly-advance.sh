#!/usr/bin/env bash
# PGS Hourly Square-Branch Research Relay
# Runs one queued falsification or analytic job per activation in an isolated worktree.
# Usage: ./scripts/pgs-hourly-advance.sh
# Scheduler: launchd com.velocityworks.pgs-hourly-advance (StartInterval 14400 = every 4 hours)
#
# Unattended policy:
# - Analytic path invokes grok with the /heavy skill (slash skill; no --skill CLI flag).
# - PGS Quartet machinery is permanently deleted; no PGS_QUARTET* env gate.

set -euo pipefail

PYTHON_CANDIDATES=(
  "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
  "${PYTHON_BIN:-}"
  "$(command -v python3 2>/dev/null || true)"
)
PYTHON_BIN=""
for candidate in "${PYTHON_CANDIDATES[@]}"; do
  [[ -n "$candidate" && -x "$candidate" ]] || continue
  if "$candidate" -c "import gmpy2" >/dev/null 2>&1; then
    PYTHON_BIN="$candidate"
    break
  fi
done
if [[ -z "$PYTHON_BIN" ]]; then
  echo "Error: no Python with gmpy2 found for hourly relay." >&2
  exit 1
fi
export PYTHON_BIN
export PATH="${HOME}/.grok/bin:$(dirname "$PYTHON_BIN"):/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Bootstrap lives in the human clone; execution moves to the isolated worktree.
SCRIPT_SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_CANDIDATE="$(dirname "$SCRIPT_SOURCE")"
if [[ -z "${PGS_SOURCE:-}" ]]; then
  if [[ -d "$SOURCE_CANDIDATE/.git" || -f "$SOURCE_CANDIDATE/.git" ]]; then
    PGS_SOURCE="$SOURCE_CANDIDATE"
  else
    PGS_SOURCE="$HOME/IdeaProjects/prime-gap-structure"
  fi
fi
PGS_ROOT="${PGS_ROOT:-$HOME/pgs-hourly/prime-gap-structure}"
TASK_BRANCH="${TASK_BRANCH:-codex/hourly-square-branch}"
GROK_BIN="${GROK_BIN:-grok}"
LOG_DIR="${LOG_DIR:-$HOME/logs/pgs-hourly}"
LOCK_DIR="${LOCK_DIR:-$LOG_DIR/hourly.lock.d}"
export LOG_DIR
export PGS_SOURCE
export PGS_ROOT
export TASK_BRANCH

PROMPT_FILE="research/00-index/hourly-advance-prompt.txt"
DISPATCH="research/00-index/scripts/hourly_advance_dispatch.py"
NOTIFY="$PGS_SOURCE/scripts/pgs_hourly_rocketchat_notify.py"
ENSURE="$PGS_SOURCE/scripts/pgs-hourly-ensure-worktree.sh"
LAST_RUN="$LOG_DIR/last_run.json"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_DIR/hourly.log"
}

write_blocked_last_run() {
  local delta="$1"
  local ops="${2:-BLOCKED}"
  "$PYTHON_BIN" - "$LAST_RUN" "$delta" "$ops" "$PGS_ROOT" <<'PY'
import json, sys
from datetime import datetime, timezone
path, delta, ops, root = sys.argv[1:5]
payload = {
    "activated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "job_id": None,
    "job_type": None,
    "research_status": "UNRESOLVED",
    "ops_status": ops,
    "delta": delta,
    "key_numbers": {},
    "artifacts": [],
    "commit": None,
    "task_branch": "codex/hourly-square-branch",
    "next_step": "Inspect hourly.log.",
    "pgs_root": root,
    "error": delta,
}
with open(path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)
    handle.write("\n")
PY
}

notify_rc() {
  set +e
  "$PYTHON_BIN" "$NOTIFY" "$LAST_RUN" >>"$LOG_DIR/hourly.log" 2>&1
  local rc=$?
  set -e
  if [[ "$rc" -ne 0 ]]; then
    log "rocketchat notify failed (non-fatal) exit=$rc"
  else
    log "rocketchat notify ok"
  fi
}

EXIT_CODE=0
cleanup() {
  local ec=$?
  if [[ -d "$LOCK_DIR" ]]; then
    rmdir "$LOCK_DIR" 2>/dev/null || true
  fi
  # Always attempt RC when last_run exists or was written.
  if [[ -f "$LAST_RUN" ]]; then
    notify_rc
  fi
  exit "${EXIT_CODE:-$ec}"
}
trap cleanup EXIT

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  log "prior hourly run still active (lock held)"
  write_blocked_last_run "prior hourly run still active (single-flight lock)" "BLOCKED"
  EXIT_CODE=0
  exit 0
fi

log "hourly relay starting; source=$PGS_SOURCE isolated_root=$PGS_ROOT"

if [[ ! -x "$ENSURE" ]]; then
  chmod +x "$ENSURE" 2>/dev/null || true
fi

set +e
ENSURE_OUT="$("$ENSURE" 2>&1)"
ENSURE_EC=$?
set -e
printf '%s\n' "$ENSURE_OUT" | tee -a "$LOG_DIR/hourly.log"
if [[ "$ENSURE_EC" -ne 0 ]]; then
  log "ensure-worktree failed"
  write_blocked_last_run "ensure-worktree failed" "FAILED"
  EXIT_CODE=1
  exit 1
fi

# Prefer the path echoed by ensure; fall back to configured PGS_ROOT.
ISOLATED="$(printf '%s\n' "$ENSURE_OUT" | tail -n 1)"
if [[ -d "$ISOLATED/.git" || -f "$ISOLATED/.git" ]]; then
  PGS_ROOT="$ISOLATED"
fi
export PGS_ROOT
cd "$PGS_ROOT"

SHA="$(git rev-parse --short HEAD)"
log "isolated worktree ready at $PGS_ROOT sha=$SHA branch=$(git branch --show-current)"

set +e
DISPATCH_OUTPUT="$("$PYTHON_BIN" "$DISPATCH" 2>&1)"
DISPATCH_STATUS=$?
set -e
printf '%s\n' "$DISPATCH_OUTPUT" | tee -a "$LOG_DIR/hourly.log"

if [[ "$DISPATCH_STATUS" -eq 0 ]]; then
  log "deterministic dispatch completed with research ADVANCE"
  EXIT_CODE=0
  exit 0
fi

if [[ "$DISPATCH_STATUS" -eq 1 ]]; then
  # NO_DELTA or FAILED still wrote last_run; treat as completed activation.
  log "deterministic dispatch finished with non-advance research status"
  EXIT_CODE=0
  exit 0
fi

if [[ "$DISPATCH_STATUS" -ne 2 ]]; then
  log "dispatch failed with status $DISPATCH_STATUS"
  if [[ ! -f "$LAST_RUN" ]]; then
    write_blocked_last_run "dispatch failed with status $DISPATCH_STATUS" "FAILED"
  fi
  EXIT_CODE="$DISPATCH_STATUS"
  exit "$DISPATCH_STATUS"
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  log "missing prompt file: $PROMPT_FILE"
  write_blocked_last_run "missing prompt file: $PROMPT_FILE" "FAILED"
  EXIT_CODE=1
  exit 1
fi

TMP_PROMPT="$(mktemp "${TMPDIR:-/tmp}/pgs-hourly-prompt.XXXXXX")"
{
  # Skills are slash-activated (see ~/.grok/skills/heavy/SKILL.md). There is no
  # grok --skill flag; leading /heavy loads Heavy effort mode for this turn.
  printf '/heavy\n\n'
  cat "$PROMPT_FILE"
  printf '\n\nCURRENT ACTIVATION CONTEXT (injected by wrapper):\n'
  printf -- '- Repo root (isolated): %s\n' "$PGS_ROOT"
  printf -- '- Source clone: %s\n' "$PGS_SOURCE"
  printf -- '- Task branch: %s\n' "$TASK_BRANCH"
  printf -- '- Pulled commit: %s\n' "$SHA"
  printf -- '- Log: %s\n' "$LOG_DIR/hourly.log"
  printf -- '- Effort mode: HEAVY via /heavy skill (local subagents)\n'
  printf -- '- Read job file: research/00-index/continuity/hourly_current_job.json\n'
  printf -- '- Contract: research/00-index/continuity/HOURLY_RELAY_CONTRACT.md\n'
  printf -- '- Research success requires a concrete delta, not pytest alone.\n'
} >"$TMP_PROMPT"

log "invoking grok /heavy for analytic hourly job"
set +e
# Unattended launchd needs --always-approve; Heavy skill interactive policy prefers
# otherwise, but this path cannot prompt a human.
caffeinate -i \
  "$GROK_BIN" \
  --prompt-file "$TMP_PROMPT" \
  --always-approve \
  --cwd "$PGS_ROOT" \
  >>"$LOG_DIR/hourly.log" 2>&1
GROK_STATUS=$?
set -e
rm -f "$TMP_PROMPT"

if [[ "$GROK_STATUS" -ne 0 ]]; then
  log "grok exited with $GROK_STATUS"
  if [[ ! -f "$LAST_RUN" ]]; then
    write_blocked_last_run "grok exited with $GROK_STATUS" "FAILED"
  fi
  EXIT_CODE="$GROK_STATUS"
  exit "$GROK_STATUS"
fi

log "analytic hourly relay completed"
EXIT_CODE=0
exit 0
