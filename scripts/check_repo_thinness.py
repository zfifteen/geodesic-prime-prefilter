#!/usr/bin/env python3
"""Stay-thin gate for prime-gap-structure.

Fails if tracked git content re-introduces experiment dumps or multi-MB blobs
that belong in the sibling artifacts store, not the live clone surface.

Usage:
  python3 scripts/check_repo_thinness.py
  python3 scripts/check_repo_thinness.py --root /path/to/repo

Exit codes:
  0  pass
  1  policy violation
  2  usage / environment error
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Hard caps for the live tip surface (bytes).
MAX_TRACKED_FILE_BYTES = 512_000  # 500 KiB
FORBIDDEN_PATH_SUBSTRINGS = (
    "/output/",
    "scan_checkpoints_",
)
# Extensions that must never re-enter at any size under output-like names
FORBIDDEN_NAME_SUFFIXES = (
    "diagnostics.jsonl",
    "profile_rows.jsonl",
    "candidate_records.csv",
    "public_result.json",
)

# Small allowlist: paths that may exceed MAX_TRACKED_FILE_BYTES (rare).
# Prefer empty; add explicit principal-approved exceptions only.
SIZE_ALLOWLIST: frozenset[str] = frozenset()


def _git_ls_files(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    if not proc.stdout:
        return []
    return [p.decode("utf-8", errors="replace") for p in proc.stdout.split(b"\0") if p]


def check_thinness(root: Path) -> list[str]:
    """Return a list of human-readable violation strings (empty => pass)."""
    root = root.resolve()
    violations: list[str] = []
    try:
        paths = _git_ls_files(root)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return [f"environment: cannot list git files under {root}: {exc}"]

    for rel in paths:
        posix = rel.replace("\\", "/")
        for frag in FORBIDDEN_PATH_SUBSTRINGS:
            if frag in posix:
                violations.append(f"forbidden path fragment {frag!r}: {posix}")
                break
        for suffix in FORBIDDEN_NAME_SUFFIXES:
            if posix.endswith(suffix):
                violations.append(f"forbidden dump name {suffix!r}: {posix}")

        if posix in SIZE_ALLOWLIST:
            continue
        full = root / rel
        if not full.is_file():
            continue
        try:
            size = full.stat().st_size
        except OSError as exc:
            violations.append(f"stat failed for {posix}: {exc}")
            continue
        if size > MAX_TRACKED_FILE_BYTES:
            violations.append(
                f"tracked file exceeds {MAX_TRACKED_FILE_BYTES} bytes "
                f"({size} bytes): {posix}"
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args(argv)
    root = args.root
    if root is None:
        root = Path(__file__).resolve().parents[1]

    violations = check_thinness(root)
    if violations:
        print("REPO THINNESS GATE FAILED", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        print(
            f"\n{len(violations)} violation(s). "
            "Move dumps to prime-gap-structure-artifacts and untrack them.",
            file=sys.stderr,
        )
        return 1
    print(
        f"REPO THINNESS GATE PASSED "
        f"(max file {MAX_TRACKED_FILE_BYTES} bytes; no output/ or scan_checkpoints_)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
