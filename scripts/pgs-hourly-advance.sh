#!/usr/bin/env bash
# PGS Hourly Square-Branch Research Relay
# Runs one queued falsification or analytic job per activation.
# Usage: ./scripts/pgs-hourly-advance.sh
# Scheduler: launchd com.velocityworks.pgs-hourly-advance (minute 5 each hour)

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

PGS_ROOT="${PGS_ROOT:-$HOME/IdeaProjects/prime-gap-structure}"
BRANCH="${BRANCH:-main}"
GROK_BIN="${GROK_BIN:-grok}"
LOG_DIR="${LOG_DIR:-$HOME/logs/pgs-hourly}"
LOCK_DIR="${LOCK_DIR:-$LOG_DIR/hourly.lock.d}"

PROMPT_FILE="research/00-index/hourly-advance-prompt.txt"
DISPATCH="research/00-index/scripts/hourly_advance_dispatch.py"

mkdir -p "$LOG_DIR"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] skipped: prior hourly run still active" | tee -a "$LOG_DIR/hourly.log"
  exit 0
fi
cleanup_lock() {
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup_lock EXIT

cd "$PGS_ROOT"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_DIR/hourly.log"
}

log "hourly relay starting in $PGS_ROOT"

if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  log "skipped: tracked worktree is dirty"
  exit 2
fi

log "git fetch + pull --ff-only on $BRANCH"
git fetch origin
git checkout "$BRANCH"
git pull --ff-only

SHA=$(git rev-parse --short HEAD)
log "at commit $SHA"

set +e
DISPATCH_OUTPUT="$("$PYTHON_BIN" "$DISPATCH" 2>&1)"
DISPATCH_STATUS=$?
set -e
printf '%s\n' "$DISPATCH_OUTPUT" | tee -a "$LOG_DIR/hourly.log"

if [[ "$DISPATCH_STATUS" -eq 0 ]]; then
  log "deterministic dispatch completed"
  exit 0
fi

if [[ "$DISPATCH_STATUS" -ne 2 ]]; then
  log "dispatch failed with status $DISPATCH_STATUS"
  exit "$DISPATCH_STATUS"
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  log "missing prompt file: $PROMPT_FILE"
  exit 1
fi

TMP_PROMPT="$(mktemp "${TMPDIR:-/tmp}/pgs-hourly-prompt.XXXXXX")"
cleanup_all() {
  rm -f "$TMP_PROMPT"
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup_all EXIT

{
  cat "$PROMPT_FILE"
  printf '\n\nCURRENT ACTIVATION CONTEXT (injected by wrapper):\n'
  printf -- '- Repo root: %s\n' "$PGS_ROOT"
  printf -- '- Base branch synced: %s\n' "$BRANCH"
  printf -- '- Pulled commit: %s\n' "$SHA"
  printf -- '- Task branch: codex/hourly-square-branch\n'
  printf -- '- Log: %s\n' "$LOG_DIR/hourly.log"
  printf -- '- Read job file: research/00-index/continuity/hourly_current_job.json\n'
} >"$TMP_PROMPT"

log "invoking grok for analytic hourly job"
caffeinate -i "$GROK_BIN" \
  --prompt-file "$TMP_PROMPT" \
  --always-approve \
  --cwd "$PGS_ROOT" \
  >> "$LOG_DIR/hourly.log" 2>&1 || {
    STATUS=$?
    log "grok exited with $STATUS"
    exit "$STATUS"
  }

log "analytic hourly relay completed"
exit 0