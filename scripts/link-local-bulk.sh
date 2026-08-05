#!/usr/bin/env bash
# Optional: park large local trees outside the repo via symlinks.
#
# Fresh clones do NOT need this script. Default workflow is unchanged:
#   cd lean-4 && lake build
# Lake creates lean-4/.lake/ inside the repo automatically.
#
# Use this only when you want bulk (Mathlib/.lake, optional media) on another
# path for disk or IDE reasons. Builds keep using the same in-repo paths.
#
# Usage:
#   bash scripts/link-local-bulk.sh
#   PGS_LOCAL_BULK=~/Caches/pgs-bulk bash scripts/link-local-bulk.sh
#   bash scripts/link-local-bulk.sh --with-media
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BULK="${PGS_LOCAL_BULK:-$HOME/IdeaProjects/pgs-local-bulk}"
WITH_MEDIA=0

for arg in "$@"; do
  case "$arg" in
    --with-media) WITH_MEDIA=1 ;;
    -h|--help)
      sed -n '2,20p' "$0"
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

link_tree() {
  local rel="$1"
  local dest_name="$2"
  local src="$ROOT/$rel"
  local dest="$BULK/$dest_name"

  mkdir -p "$BULK"

  if [ -L "$src" ]; then
    echo "OK  $rel is already a symlink -> $(readlink "$src")"
    return 0
  fi

  if [ -e "$src" ] && [ ! -d "$src" ]; then
    echo "ERROR: $rel exists and is not a directory" >&2
    exit 1
  fi

  if [ -d "$src" ]; then
    if [ -e "$dest" ]; then
      echo "ERROR: both $src and $dest exist; resolve manually before linking" >&2
      exit 1
    fi
    echo "MOVE $src -> $dest"
    mv "$src" "$dest"
  else
    mkdir -p "$dest"
    echo "CREATE $dest"
  fi

  ln -s "$dest" "$src"
  echo "LINK $rel -> $dest"
}

echo "PGS_LOCAL_BULK=$BULK"
echo "Repo root=$ROOT"
echo ""

link_tree "lean-4/.lake" "lean-4.lake"

if [ "$WITH_MEDIA" -eq 1 ]; then
  link_tree "media" "media"
fi

echo ""
echo "Done. Default clone/build for other users is unchanged."
echo "On this machine, lake still uses lean-4/.lake (now external)."
echo "Verify: cd lean-4 && lake build"
