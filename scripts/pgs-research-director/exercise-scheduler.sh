#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/env.sh" 2>/dev/null || export PGS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)" BOT_DIR="$SCRIPT_DIR" SCRATCH="${SCRATCH:-$SCRIPT_DIR/artifacts}"

echo "=== Exercise scheduler (two runs using only env exports) ==="
export PGS_ROOT BOT_DIR SCRATCH
"$BOT_DIR/pgs-director-cycle-trigger.sh" || { echo "run1 failed"; exit 1; }
"$BOT_DIR/pgs-director-cycle-trigger.sh" || { echo "run2 failed"; exit 1; }
echo "Scheduler exercised with exit 0 both times."
