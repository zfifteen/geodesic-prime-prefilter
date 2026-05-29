#!/bin/bash
set -euo pipefail

echo "=== PGS Lean 4 Build (Self-Contained Skeleton) ==="
echo "Started at: $(date)"
echo ""

cd /Users/velocityworks/IdeaProjects/prime-gap-structure/lean-4

echo "Cleaning build artifacts..."
rm -rf .lake/build

echo "Running: lake build..."
/Users/velocityworks/.hermes/profiles/resume-project/home/.elan/bin/elan run leanprover/lean4:v4.30.0 -- lake build

echo ""
echo "=== Running smoke test ==="
/Users/velocityworks/.hermes/profiles/resume-project/home/.elan/bin/elan run leanprover/lean4:v4.30.0 -- lake env lean /Users/velocityworks/IdeaProjects/prime-gap-structure/lean-4/smoke-test.lean

echo ""
echo "=== PGS Lean 4 skeleton VERIFIED COMPLETE at: $(date) ==="
