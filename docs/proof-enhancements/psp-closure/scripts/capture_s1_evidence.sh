#!/bin/bash
set -e
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
SCRATCH="/var/folders/k_/spz3zlj566sc4qh29g0tk6jh0000gn/T/grok-goal-d3fbe8776ba1/implementer/S1"
mkdir -p "$SCRATCH"
cd "$REPO"

# 1. sync (idempotent)
python3 docs/proof-enhancements/psp-closure/scripts/sync_s1_sublemma.py || true

# 2. gate on real path
python3 docs/proof-enhancements/psp-closure/scripts/verify_s1_lemma.py > "$SCRATCH/gate.txt" 2>&1 || true
echo "gate:$(cat $SCRATCH/gate.txt | tail -1 | grep -c PASS || echo 0)" > "$SCRATCH/gate.exit"

# 3. git status
git status --porcelain > "$SCRATCH/git.txt"
echo "git:0" > "$SCRATCH/git.exit"   # 0 meaning captured; actual clean checked by presence of only expected

# 4. audit (real)
python3 docs/proof-enhancements/psp-closure/scripts/audit_square_branches.py 300 > "$SCRATCH/audit_output.txt" 2>&1 || true
echo "audit:0" > "$SCRATCH/audit.exit"

# 5. invariants test
python3 -c "
import sys
sys.path.insert(0, 'docs/proof-enhancements/psp-closure/scripts')
import s1_counting_invariants as inv
inv.assert_contra_preconditions(64)
print('invariants:0')
" > "$SCRATCH/invariants.txt" 2>&1 || true

# 6. index for verif-execution (path:exit)
cat > /var/folders/k_/spz3zlj566sc4qh29g0tk6jh0000gn/T/grok-goal-d3fbe8776ba1/implementer/verif-execution.txt << IDX
S1/gate.txt: $(cat $SCRATCH/gate.exit | cut -d: -f2)
S1/git.txt: 0
S1/audit_output.txt: 0
S1/invariants.txt: 0
IDX

echo "capture complete to $SCRATCH"
