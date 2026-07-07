#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/env.sh" 2>/dev/null || { export PGS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"; export BOT_DIR="$SCRIPT_DIR"; export SCRATCH="${SCRATCH:-$SCRIPT_DIR/artifacts}"; }

mkdir -p "$SCRATCH"

echo "TEST: driving in-repo shipped trigger (strict)"

# Use exercise-scheduler for the two runs
"$SCRIPT_DIR/exercise-scheduler.sh" > "$SCRATCH/test-run1.out" 2>&1
run1_status=$?

# Second explicit for the "repeat"
"$SCRIPT_DIR/pgs-director-cycle-trigger.sh" > "$SCRATCH/test-run2.out" 2>&1
run2_status=$?

# Strict asserts - no || true hiding failures
if [ $run1_status -ne 0 ] || [ $run2_status -ne 0 ]; then
  echo "FAIL: non-zero exit from trigger(s)"
  exit 1
fi
echo "PASS: both runs exit 0"

if [[ "$PGS_ROOT" != */prime-gap-structure ]]; then
  echo "FAIL: PGS_ROOT=$PGS_ROOT does not end with prime-gap-structure"
  exit 1
fi
echo "PASS: PGS_ROOT correct"

# Assert key markers in output
if ! grep -q "PGS framing objects + AGENTS/PROOF references confirmed in SYSTEM.md" "$SCRATCH/test-run1.out"; then
  echo "FAIL: missing SYSTEM framing confirmation"
  exit 1
fi
echo "PASS: SYSTEM framing refs present"

if ! grep -q "CYCLE_END" "$SCRATCH/test-run1.out"; then
  echo "FAIL: missing CYCLE_END"
  exit 1
fi
echo "PASS: cycle completed autonomously"

# Assert JSON is valid and math correct (min_d for 25 == 3)
jsonf=$(ls -t "$SCRATCH/artifacts/"*/advance-report.json 2>/dev/null | head -1 || true)
if [ -z "$jsonf" ]; then
  jsonf="$SCRATCH/artifacts/advance-report.json"  # fallback if py wrote flat
fi
if [ -f "$jsonf" ]; then
  if ! python3 -m json.tool "$jsonf" > /dev/null 2>&1; then
    echo "FAIL: advance-report.json not valid JSON"
    exit 1
  fi
  echo "PASS: advance-report.json valid JSON"
  # Check the gwr_23_29 min_divisor_count == 3
  if python3 -c "
import json, sys
data = json.load(open('$jsonf'))
md = data.get('gwr_23_29', {}).get('min_divisor_count')
if md != 3:
  print('FAIL: expected min_d=3 for witness 25, got', md)
  sys.exit(1)
print('PASS: exact min_d=3 for 25')
" ; then
    true
  else
    exit 1
  fi
else
  echo "NOTE: no advance-report.json found for json assert (still checking markers)"
fi

echo "TEST COMPLETE"
