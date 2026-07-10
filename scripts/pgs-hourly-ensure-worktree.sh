#!/usr/bin/env bash
# Ensure the isolated PGS hourly worktree exists and is on the task branch.
# Usage: pgs-hourly-ensure-worktree.sh
# Env:
#   PGS_SOURCE  main clone (default: ~/IdeaProjects/prime-gap-structure)
#   PGS_ROOT    isolated worktree (default: ~/pgs-hourly/prime-gap-structure)
#   TASK_BRANCH default: codex/hourly-square-branch

set -euo pipefail

PGS_SOURCE="${PGS_SOURCE:-$HOME/IdeaProjects/prime-gap-structure}"
PGS_ROOT="${PGS_ROOT:-$HOME/pgs-hourly/prime-gap-structure}"
TASK_BRANCH="${TASK_BRANCH:-codex/hourly-square-branch}"
LOG_DIR="${LOG_DIR:-$HOME/logs/pgs-hourly}"

mkdir -p "$LOG_DIR" "$(dirname "$PGS_ROOT")"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ensure-worktree: $*" | tee -a "$LOG_DIR/hourly.log"
}

if [[ ! -d "$PGS_SOURCE/.git" && ! -f "$PGS_SOURCE/.git" ]]; then
  log "PGS_SOURCE is not a git checkout: $PGS_SOURCE"
  exit 1
fi

cd "$PGS_SOURCE"
git fetch origin --quiet || git fetch origin

if [[ -d "$PGS_ROOT/.git" || -f "$PGS_ROOT/.git" ]]; then
  log "worktree present at $PGS_ROOT"
else
  if [[ -e "$PGS_ROOT" && ! -d "$PGS_ROOT/.git" && ! -f "$PGS_ROOT/.git" ]]; then
    log "refusing to reuse non-git path: $PGS_ROOT"
    exit 1
  fi
  log "creating worktree $PGS_ROOT on $TASK_BRANCH"
  if git show-ref --verify --quiet "refs/heads/$TASK_BRANCH"; then
    git worktree add "$PGS_ROOT" "$TASK_BRANCH"
  elif git show-ref --verify --quiet "refs/remotes/origin/$TASK_BRANCH"; then
    git worktree add -b "$TASK_BRANCH" "$PGS_ROOT" "origin/$TASK_BRANCH"
  else
    git worktree add -b "$TASK_BRANCH" "$PGS_ROOT" origin/main
  fi
fi

cd "$PGS_ROOT"
current="$(git branch --show-current || true)"
if [[ "$current" != "$TASK_BRANCH" ]]; then
  if git show-ref --verify --quiet "refs/heads/$TASK_BRANCH"; then
    git checkout "$TASK_BRANCH"
  elif git show-ref --verify --quiet "refs/remotes/origin/$TASK_BRANCH"; then
    git checkout -B "$TASK_BRANCH" "origin/$TASK_BRANCH"
  else
    git checkout -B "$TASK_BRANCH"
  fi
fi

git fetch origin --quiet || git fetch origin
if git show-ref --verify --quiet "refs/remotes/origin/$TASK_BRANCH"; then
  git merge --ff-only "origin/$TASK_BRANCH" 2>/dev/null || true
fi

# Sync relay code/contracts from the human source tree so launchd can pick up
# local ops improvements without requiring a clean IdeaProjects commit.
# Do not overwrite mutable queue/prior/ledger state once the worktree owns it.
code_sync_paths=(
  "scripts/pgs-hourly-advance.sh"
  "scripts/pgs-hourly-ensure-worktree.sh"
  "scripts/pgs_hourly_rocketchat_notify.py"
  "scripts/launchd/com.velocityworks.pgs-hourly-advance.plist"
  "research/00-index/scripts/hourly_advance_dispatch.py"
  "research/00-index/scripts/hourly_delta.py"
  "research/00-index/scripts/hourly_research_relay_common.py"
  "research/00-index/hourly-advance-prompt.txt"
  "research/00-index/continuity/HOURLY_RELAY_CONTRACT.md"
  "research/00-index/continuity/hourly_baseline_signature.json"
  "research/00-index/continuity/ACTIVE_TARGET.md"
)

for rel in "${code_sync_paths[@]}"; do
  src="$PGS_SOURCE/$rel"
  dst="$PGS_ROOT/$rel"
  if [[ -f "$src" ]]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
done

# Seed mutable queue only when the worktree does not already have one.
if [[ ! -f "$PGS_ROOT/research/00-index/continuity/hourly_queue.json" \
   && -f "$PGS_SOURCE/research/00-index/continuity/hourly_queue.json" ]]; then
  cp "$PGS_SOURCE/research/00-index/continuity/hourly_queue.json" \
     "$PGS_ROOT/research/00-index/continuity/hourly_queue.json"
fi

log "ready branch=$(git branch --show-current) sha=$(git rev-parse --short HEAD) root=$PGS_ROOT"
echo "$PGS_ROOT"
