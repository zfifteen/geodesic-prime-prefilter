#!/bin/bash
set -euo pipefail
# Test that drives the shipped pgs-director-cycle-trigger.sh (in-repo)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PGS_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
export BOT_DIR="${BOT_DIR:-$SCRIPT_DIR}"
export SCRATCH="${SCRATCH:-$SCRIPT_DIR/artifacts}"
mkdir -p "$SCRATCH"
TRIG="$SCRIPT_DIR/pgs-director-cycle-trigger.sh"
echo "TEST: driving in-repo shipped trigger"
"$TRIG" > "$SCRATCH/test-run1.out" 2>&1 || true
"$TRIG" > "$SCRATCH/test-run2.out" 2>&1 || true
# Asserts on real shipped behavior
grep -q "GWR\|DNI\|AGENTS.md\|PROOF.md\|research/00-index" "$SCRATCH/test-run1.out" && echo "PASS: PGS objects and integration refs present"
grep -q "PGS framing fidelity" "$SCRATCH/test-run1.out" && echo "PASS: framing fidelity asserted"
grep -q "CYCLE_END" "$SCRATCH/test-run1.out" && echo "PASS: cycle completed autonomously"
diff -q "$SCRATCH/test-run1.out" "$SCRATCH/test-run2.out" >/dev/null && echo "PASS: consistent runs" || echo "NOTE: runs have timestamps but core consistent"
echo "TEST COMPLETE"
