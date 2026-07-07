#!/bin/bash
# lib/env.sh - single source of truth for paths (no hardcodes)

if [ -n "${_PGS_ENV_SOURCED:-}" ]; then
  return 0
fi
_PGS_ENV_SOURCED=1

# Prefer CALLER_CONFIG_DIR or SCRIPT_DIR set by caller
if [ -n "${CALLER_CONFIG_DIR:-}" ]; then
  CONFIG_DIR="$CALLER_CONFIG_DIR"
elif [ -n "${SCRIPT_DIR:-}" ]; then
  CONFIG_DIR="$SCRIPT_DIR"
else
  _src="${BASH_SOURCE[0]}"
  if [ -z "$_src" ]; then
    CONFIG_DIR="$(pwd)"
  else
    _dir="$(cd "$(dirname "$_src")" 2>/dev/null && pwd || echo "")"
    if [ -n "$_dir" ] && [ "$(basename "$_dir")" = "lib" ]; then
      CONFIG_DIR="$(cd "$_dir/.." && pwd)"
    else
      CONFIG_DIR="$_dir"
    fi
  fi
fi

PGS_ROOT="$(cd "$CONFIG_DIR/../.." 2>/dev/null && pwd || echo "")"

BOT_DIR="${BOT_DIR:-$CONFIG_DIR}"
# Respect SCRATCH if provided by caller; otherwise use a safe default under the config dir
if [ -z "${SCRATCH:-}" ]; then
  SCRATCH="$CONFIG_DIR/artifacts"
fi

export PGS_ROOT BOT_DIR SCRATCH

# Enforce correct root
case "$PGS_ROOT" in
  */prime-gap-structure) ;;
  *)
    echo "ERROR: PGS_ROOT=$PGS_ROOT" >&2
    exit 1
    ;;
esac
