#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
TIMESTAMP="${TIMESTAMP:-$(date -u +"%Y%m%dT%H%M%SZ")}"
BASE_OUTPUT_DIR="${1:-$ROOT_DIR/benchmarks/output/python/sha_nonce}"
NAMESPACE="${NAMESPACE:-cdl-prime-z-band}"
BIT_LENGTH="${BIT_LENGTH:-2048}"
STEADY_START_INDEX="${STEADY_START_INDEX:-100000}"
STEADY_BATCH_SIZE="${STEADY_BATCH_SIZE:-1024}"
STEADY_BATCH_COUNT="${STEADY_BATCH_COUNT:-500}"
ROLLOVER_START_INDEX="${ROLLOVER_START_INDEX:-999000}"
ROLLOVER_BATCH_SIZE="${ROLLOVER_BATCH_SIZE:-1024}"
ROLLOVER_BATCH_COUNT="${ROLLOVER_BATCH_COUNT:-200}"
STEADY_OUTPUT_DIR="$BASE_OUTPUT_DIR/ascii_delta_geometry_probe_run1_steady_$TIMESTAMP"
ROLLOVER_OUTPUT_DIR="$BASE_OUTPUT_DIR/ascii_delta_geometry_probe_run2_rollover_$TIMESTAMP"

echo "timestamp=$TIMESTAMP"
echo "steady_output_dir=$STEADY_OUTPUT_DIR"
echo "rollover_output_dir=$ROLLOVER_OUTPUT_DIR"

cd "$ROOT_DIR"

PYTHONPATH=src/python python3 benchmarks/python/sha_nonce/ascii_delta_geometry_probe.py \
  --namespace "$NAMESPACE" \
  --bit-length "$BIT_LENGTH" \
  --start-index "$STEADY_START_INDEX" \
  --batch-size "$STEADY_BATCH_SIZE" \
  --batch-count "$STEADY_BATCH_COUNT" \
  --output-dir "$STEADY_OUTPUT_DIR"

PYTHONPATH=src/python python3 benchmarks/python/sha_nonce/ascii_delta_geometry_probe.py \
  --namespace "$NAMESPACE" \
  --bit-length "$BIT_LENGTH" \
  --start-index "$ROLLOVER_START_INDEX" \
  --batch-size "$ROLLOVER_BATCH_SIZE" \
  --batch-count "$ROLLOVER_BATCH_COUNT" \
  --output-dir "$ROLLOVER_OUTPUT_DIR"

echo "steady_json=$STEADY_OUTPUT_DIR/ascii_delta_geometry_probe.json"
echo "rollover_json=$ROLLOVER_OUTPUT_DIR/ascii_delta_geometry_probe.json"
