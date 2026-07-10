"""A1 boundary tests: forbidden classical selectors (BD)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from boundary import scan_file, scan_inference_tree  # noqa: E402
from resolver import load_public_cases  # noqa: E402


def test_tp_bd_001_inference_import_scan_clean():
    violations = scan_inference_tree(V3)
    assert violations == [], violations


def test_tp_bd_001_detects_forbidden_import(tmp_path: Path):
    bad = tmp_path / "bad.py"
    bad.write_text("import sympy\nfrom math import gcd\n", encoding="utf-8")
    v = scan_file(bad)
    assert any("sympy" in x or "gcd" in x for x in v)


def test_tp_bd_005_rejects_private_factor_fields(tmp_path: Path):
    path = tmp_path / "cases.jsonl"
    path.write_text(
        json.dumps({"case_id": "x", "bits": 8, "N": "15", "p": 3, "q": 5}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="audit|factor"):
        load_public_cases(path)
