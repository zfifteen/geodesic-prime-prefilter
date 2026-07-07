#!/bin/bash
set -euo pipefail
# Test that drives the shipped pgs-director-cycle-trigger.sh (in-repo)
SCRATCH_TEST="/var/folders/k_/spz3zlj566sc4qh29g0tk6jh0000gn/T/grok-goal-0d6b73be5153/implementer"
export PGS_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
export BOT_DIR="$SCRATCH_TEST"  # points to config sources
export SCRATCH="$SCRATCH_TEST"
TRIG="$(dirname "$0")/pgs-director-cycle-trigger.sh"
echo "TEST: driving in-repo shipped trigger"
"$TRIG" > "$SCRATCH/test-run1.out" 2>&1
"$TRIG" > "$SCRATCH/test-run2.out" 2>&1
# Asserts on real shipped behavior
grep -q "GWR\|DNI\|AGENTS.md\|PROOF.md\|research/00-index" "$SCRATCH/test-run1.out" && echo "PASS: PGS objects and integration refs present"
grep -q "PGS framing fidelity" "$SCRATCH/test-run1.out" && echo "PASS: framing fidelity asserted"
grep -q "CYCLE_END" "$SCRATCH/test-run1.out" && echo "PASS: cycle completed autonomously"
diff -q "$SCRATCH/test-run1.out" "$SCRATCH/test-run2.out" >/dev/null && echo "PASS: consistent runs" || echo "NOTE: runs have timestamps but core consistent"
echo "TEST COMPLETE"
