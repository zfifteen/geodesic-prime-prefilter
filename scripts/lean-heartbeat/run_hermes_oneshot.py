#!/usr/bin/env python3
"""Run Hermes oneshot for Lean heartbeat with argv list (no shell quoting)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: run_hermes_oneshot.py PROMPT_FILE REPO_ROOT", file=sys.stderr)
        return 2
    prompt_path = Path(sys.argv[1])
    repo = Path(sys.argv[2])
    hermes = os.environ.get("HERMES_BIN") or "hermes"
    prompt = prompt_path.read_text(encoding="utf-8")
    # Prefer HERMES_PROFILE env for idea; -p is ambiguous across CLI versions.
    env = os.environ.copy()
    env.setdefault("HERMES_PROFILE", "idea")
    cmd = [
        hermes,
        "--yolo",
        "--accept-hooks",
        "-z",
        prompt,
    ]
    # Also try profile subcommand style if wrapper exists
    # Keep simple oneshot.
    proc = subprocess.run(
        cmd,
        cwd=str(repo),
        env=env,
        check=False,
    )
    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
