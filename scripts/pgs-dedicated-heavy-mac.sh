#!/bin/bash
# PGS Dedicated Heavy Worker activation wrapper (for spare Mac / launchd / cron / tmux)
# This node ALWAYS pulls latest from GitHub first, then runs the heavy worker prompt.
# Usage: ./scripts/pgs-dedicated-heavy-mac.sh
# Configure via env or edit the paths below.

set -euo pipefail

# --- CONFIGURE THESE FOR YOUR DEDICATED MAC ---
PGS_ROOT="${PGS_ROOT:-$HOME/pgs/prime-gap-structure}"
BRANCH="${BRANCH:-predictions}"   # or main / whatever the active predictions branch is
GROK_BIN="${GROK_BIN:-grok}"
LOG_DIR="${LOG_DIR:-$HOME/logs}"
mkdir -p "$LOG_DIR"

CHARTER_FILE="research/16-predictions/dedicated-mac-heavy-worker-charter.md"
PROMPT_FILE="research/16-predictions/dedicated-mac-heavy-worker-prompt.txt"
RULES_FILE="research/16-predictions/dedicated-mac-rules.txt"  # optional; create if you want extra baked rules

# Optional: path to a file containing your bus reclaim_token for pgs-dedicated-heavy-mac (one line)
RECLAIM_FILE="${RECLAIM_FILE:-$HOME/.pgs-dedicated-reclaim.txt}"

# Optional: extra env for grok (XAI_API_KEY etc. if not in shell profile)
# export XAI_API_KEY="xai-..."

cd "$PGS_ROOT"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Dedicated heavy activation starting in $PGS_ROOT on branch $BRANCH" | tee -a "$LOG_DIR/pgs-dedicated.log"

# 1. Hard sync from GitHub (user requirement)
echo "[$(date -u)] git fetch + pull --ff-only ..."
git fetch origin
git checkout "$BRANCH"
git pull --ff-only

SHA=$(git rev-parse --short HEAD)
echo "[$(date -u)] Now at $SHA" | tee -a "$LOG_DIR/pgs-dedicated.log"

# 2. (Re)build the prompt for this invocation.
# The prompt file already contains the core instructions + "read the 5 files + charter".
# We append a tiny activation header with the current SHA so the model sees it.
ACTIVATION_PROMPT=$(cat "$PROMPT_FILE")
ACTIVATION_PROMPT="$ACTIVATION_PROMPT

CURRENT ACTIVATION CONTEXT (injected by wrapper):
- Repo root: $PGS_ROOT
- Branch: $BRANCH
- Pulled commit: $SHA
- Charter location (read it now via tools if not already): $CHARTER_FILE
- Log: $LOG_DIR/pgs-dedicated.log
- Reclaim token file (if present, read and use for bus join): $RECLAIM_FILE

Begin the exact activation loop described in the charter and prompt above. PGS-first. Never prompt the human."

# 3. Optional rules (create the file once with extra guardrails if desired)
RULES_ARG=""
if [[ -f "$RULES_FILE" ]]; then
  RULES_ARG="--rules $(cat "$RULES_FILE")"
fi

# 4. Run headless with yolo (the prompt + charter enforce the discipline; yolo lets it use tools without interactive confirms on the dedicated box)
echo "[$(date -u)] Invoking grok headless for heavy worker loop..." | tee -a "$LOG_DIR/pgs-dedicated.log"

"$GROK_BIN" -p "$ACTIVATION_PROMPT" \
  --yolo \
  --cwd "$PGS_ROOT" \
  $RULES_ARG \
  --output-format json \
  >> "$LOG_DIR/pgs-dedicated.log" 2>&1 || {
    STATUS=$?
    echo "[$(date -u)] grok exited with $STATUS" | tee -a "$LOG_DIR/pgs-dedicated.log"
    # Optional: send a minimal Hermes failure digest here if you have a direct hermes call wrapper
    exit $STATUS
  }

echo "[$(date -u)] Dedicated heavy activation completed (see log for details)." | tee -a "$LOG_DIR/pgs-dedicated.log"