"""Tests for scripts/check_repo_thinness.py — drives the real gate entry points."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "check_repo_thinness.py"

# Import the shipped module by path so we exercise the real functions.
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import check_repo_thinness as thin  # noqa: E402


def test_script_file_exists():
    assert SCRIPT.is_file(), f"missing stay-thin script at {SCRIPT}"


def test_check_thinness_function_on_this_repo():
    """Real function on the real working tree index."""
    violations = thin.check_thinness(REPO_ROOT)
    # After slim work, the live tip should pass. If it fails, surface messages.
    assert isinstance(violations, list)
    assert violations == [], "unexpected thinness violations:\n" + "\n".join(violations)


def test_cli_entry_point_passes_on_this_repo():
    """Real CLI entry point (python3 scripts/check_repo_thinness.py)."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"CLI failed rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
    )
    assert "PASSED" in proc.stdout


def test_check_thinness_detects_forbidden_output_path(tmp_path: Path):
    """Synthetic git repo: tracked path under output/ must fail the real checker."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    out = tmp_path / "research" / "demo" / "output"
    out.mkdir(parents=True)
    blob = out / "rows.json"
    blob.write_text('{"n": 1}\n', encoding="utf-8")
    subprocess.run(["git", "add", "research/demo/output/rows.json"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "seed"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    violations = thin.check_thinness(tmp_path)
    assert any("output" in v for v in violations), violations


def test_check_thinness_detects_oversized_tracked_file(tmp_path: Path):
    """Synthetic git repo: tracked file > 500 KiB must fail the real checker."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    big = tmp_path / "big.bin"
    big.write_bytes(b"x" * (thin.MAX_TRACKED_FILE_BYTES + 1))
    subprocess.run(["git", "add", "big.bin"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "seed"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    violations = thin.check_thinness(tmp_path)
    assert any("exceeds" in v for v in violations), violations


def test_cli_fails_on_synthetic_fat_repo(tmp_path: Path):
    """CLI must return 1 when the real gate sees a fat tracked dump."""
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    p = tmp_path / "scan_checkpoints_5e9" / "segment.json"
    p.parent.mkdir(parents=True)
    p.write_text("{}", encoding="utf-8")
    subprocess.run(["git", "add", "scan_checkpoints_5e9/segment.json"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", "seed"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "FAILED" in proc.stderr
