#!/usr/bin/env bash
# Mechanical D1/D2/D4.4b spot-checks for the Lean core-stack DoD.
# Usage (from repo root): bash scripts/lean4-dod-check.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/lean-4"

echo "== D1.1 lake build =="
lake build

echo "== D1.2 smoke-test =="
lake env lean smoke-test.lean

echo "== D2.1 no sorry on PGS/*.lean =="
if rg -n 'sorry' PGS/*.lean; then
  echo "FAIL: sorry found on core path" >&2
  exit 1
fi
echo "PASS: no sorry"

echo "== D2.3 axiom allowlist =="
AXIOMS="$(rg -n '^\s*axiom ' PGS/*.lean || true)"
echo "$AXIOMS"
if echo "$AXIOMS" | rg -v 'tau_prime_square_eq_three' | rg -q 'axiom '; then
  echo "FAIL: unlisted axiom on core path" >&2
  exit 1
fi
if ! echo "$AXIOMS" | rg -q 'tau_prime_square_eq_three'; then
  echo "WARN: expected audit axiom tau_prime_square_eq_three not found"
fi
echo "PASS: axiom allowlist"

echo "== D4.4b empty-shell pattern (informational) =="
if rg -n '∃ C,.*≤ C := by' PGS/*.lean; then
  echo "FAIL: possible empty existential bound shell" >&2
  exit 1
fi
echo "PASS: no empty existential shell pattern"

echo "All mechanical DoD checks passed."
