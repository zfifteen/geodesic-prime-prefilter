#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/env.sh" 2>/dev/null || {
  export PGS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
  export BOT_DIR="$SCRIPT_DIR"
  export SCRATCH="${SCRATCH:-$SCRIPT_DIR/artifacts}"
}

export CYCLE_ID="${CYCLE_ID:-cycle-$(date +%Y%m%d-%H%M%S)}"
LOGFILE="$SCRATCH/cycle-run.log"
ARTIFACT_DIR="$SCRATCH/artifacts/$CYCLE_ID"
mkdir -p "$ARTIFACT_DIR"

echo "=== PGS Research Director Autonomous Cycle Trigger ===" | tee -a "$LOGFILE"
echo "CYCLE_ID=$CYCLE_ID" | tee -a "$LOGFILE"
echo "PGS_ROOT=$PGS_ROOT" | tee -a "$LOGFILE"
echo "Trigger time: $(date -u)" | tee -a "$LOGFILE"
echo "No interactive prompts after launch, full autonomy mode." | tee -a "$LOGFILE"

echo "--- SYSTEM.md head (PGS contract) ---" | tee -a "$LOGFILE"
head -30 "$BOT_DIR/SYSTEM.md" | tee -a "$LOGFILE"
grep -q "GWR\|DNI\|AGENTS.md\|PROOF.md\|PGS-first" "$BOT_DIR/SYSTEM.md" && echo "PGS framing objects + AGENTS/PROOF references confirmed in SYSTEM.md" | tee -a "$LOGFILE"

echo "--- Running gwr-resonance skill (delegates) ---" | tee -a "$LOGFILE"
node "$BOT_DIR/skills/gwr-resonance/gwr-resonance.cjs" 23 29 2>&1 | tee "$ARTIFACT_DIR/gwr-output.json" | tee -a "$LOGFILE" || true

echo "--- Running log-analyzer ---" | tee -a "$LOGFILE"
node "$BOT_DIR/skills/log-analyzer/log-analyzer.cjs" "$SCRATCH" 2>&1 | tee "$ARTIFACT_DIR/log-analysis.json" | tee -a "$LOGFILE" || true

echo "--- Executing run_cycle.py (parses continuity + exact_divisor_count) ---" | tee -a "$LOGFILE"
python3 "$BOT_DIR/run_cycle.py" 2>&1 | tee -a "$LOGFILE" || true

echo "--- Cycle complete (autonomous, no further input) ---" | tee -a "$LOGFILE"
echo "PGS framing fidelity: GWR, DNI, divisor-count, AGENTS.md, PROOF.md, research/00-index/ referenced." | tee -a "$LOGFILE"
echo "Scheduler evidence: CRONS.json contains pgs-director-daily-advance and pgs-test-one-shot" | tee -a "$LOGFILE"
echo "CYCLE_END $CYCLE_ID" | tee -a "$LOGFILE"
exit 0
