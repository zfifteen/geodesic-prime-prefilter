#!/bin/bash
# lib/env.sh - reliable path resolution for PGS Research Director

if [ -n "${_PGS_ENV_SOURCED:-}" ]; then
  return 0
fi
_PGS_ENV_SOURCED=1

# Prefer explicit CONFIG_DIR or SCRIPT_DIR set by the caller before sourcing.
if [ -n "${CALLER_CONFIG_DIR:-}" ]; then
  CONFIG_DIR="$CALLER_CONFIG_DIR"
elif [ -n "${SCRIPT_DIR:-}" ]; then
  CONFIG_DIR="$SCRIPT_DIR"
else
  # Fallback: try to resolve from how we were sourced
  _src="${BASH_SOURCE[0]}"
  if [ -z "$_src" ]; then
    # Last resort: assume we are being sourced from within the config dir
    CONFIG_DIR="$(pwd)"
  else
    _dir="$(cd "$(dirname "$_src")" 2>/dev/null && pwd || echo "")"
    if [ -n "$_dir" ]; then
      # If we resolved to the lib/ dir, go up one
      if [ "$(basename "$_dir")" = "lib" ]; then
        CONFIG_DIR="$(cd "$_dir/.." && pwd)"
      else
        CONFIG_DIR="$_dir"
      fi
    else
      CONFIG_DIR="$(pwd)"
    fi
  fi
fi

PGS_ROOT="$(cd "$CONFIG_DIR/../.." 2>/dev/null && pwd || echo "$CONFIG_DIR/../..")"

BOT_DIR="${BOT_DIR:-$CONFIG_DIR}"
SCRATCH="${SCRATCH:-/var/folders/k_/spz3zlj566sc4qh29g0tk6jh0000gn/T/grok-goal-0d6b73be5153/implementer}"

export PGS_ROOT BOT_DIR SCRATCH CONFIG_DIR

# Enforce
case "$PGS_ROOT" in
  */prime-gap-structure) ;;
  *)
    # Try one more time with known structure
    if [ -d "$CONFIG_DIR/../../prime-gap-structure" ]; then
      PGS_ROOT="$(cd "$CONFIG_DIR/../../prime-gap-structure" && pwd)"
      export PGS_ROOT
    else
      echo "ERROR: PGS_ROOT resolved to $PGS_ROOT (CONFIG_DIR=$CONFIG_DIR)" >&2
      exit 1
    fi
    ;;
esac
