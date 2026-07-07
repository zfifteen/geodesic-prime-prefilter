"""Tests for proof certificate emission."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "docs" / "proof-enhancements" / "scripts" / "emit_certificates.py"


def load_module():
    spec = importlib.util.spec_from_file_location("emit_certificates", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load emit_certificates")
    module = importlib.util.module_from_spec(spec)
    sys.modules["emit_certificates"] = module
    spec.loader.exec_module(module)
    return module


def test_emit_certificates_writes_schema_conformant_payloads(tmp_path, monkeypatch):
    module = load_module()
    cert_dir = tmp_path / "certificates"
    cert_dir.mkdir()
    monkeypatch.setattr(module, "CERT_DIR", cert_dir)
    monkeypatch.setattr(module, "git_commit_hash", lambda: "deadbeef" * 5)

    paths = module.write_certificates()
    assert len(paths) == 3

    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["failure_examples"] == []
        assert payload["counts"]["failures"] == 0
        assert payload["artifact_hash"].startswith("sha256:")
        assert payload["generator"]["commit_hash"] == "deadbeef" * 5
        assert "verified_at" in payload