from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "research" / "06-cryptology-rsa" / "experiments"
LIVE_V2 = EXPERIMENTS / "live-solver" / "rsa-v2"
CERTIFICATE_V2 = EXPERIMENTS / "certificate-mechanics" / "rsa-v2"
SCRIPT = CERTIFICATE_V2 / "certificate_commitment_story_probe.py"
RULE_ID = "certificate_commitment_story_v1"


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test fixture path."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def expected_certificates(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    """Return expected reconstruction fields keyed by public certificate anchor."""
    expected: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        for prefix in ("lower", "upper"):
            anchor = row.get(f"{prefix}_anchor")
            if anchor is None:
                continue
            expected[(str(row["case_id"]), str(anchor))] = {
                "closed_offsets_before_q": row[f"{prefix}_closed_offsets_before_q"],
                "carrier_w": row[f"{prefix}_carrier_w"],
                "reset_endpoint": row[f"{prefix}_reset_endpoint"],
                "reset_deadline_value": row[f"{prefix}_reset_deadline_value"],
            }
    return expected


def reconstructed_certificates(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    """Reconstruct certificate fields from story rows."""
    reconstructed: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        key = (str(row["case_id"]), str(row["source_anchor"]))
        fields = reconstructed.setdefault(
            key,
            {
                "closed_offsets_before_q": [],
                "carrier_w": None,
                "reset_endpoint": None,
                "reset_deadline_value": None,
            },
        )
        if row["event_kind"] == "closed_offset":
            fields["closed_offsets_before_q"].append(row["event_offset"])
        elif row["event_kind"] == "carrier_lock":
            fields["carrier_w"] = row["event_value"]
        elif row["event_kind"] == "reset":
            fields["reset_endpoint"] = row["event_value"]
        elif row["event_kind"] == "deadline":
            fields["reset_deadline_value"] = row["event_value"]
    return reconstructed


def test_story_probe_script_exists_and_uses_public_json_only():
    """As a reviewer, I want the story sidecar to avoid forbidden classical gates."""
    assert SCRIPT.exists()
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            assert ast.get_docstring(node)
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, (ast.Mod, ast.Mult))
        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            assert name not in {"gcd", "isprime", "nextprime", "factorint"}


def test_story_rows_reconstruct_existing_public_certificates(tmp_path):
    """As a reviewer, I want story rows to reconstruct the runner certificate fields."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story"

    assert module.main(
        [
            "--certificate-rows",
            str(LIVE_V2 / "output" / "survivor_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    source_rows = read_jsonl(LIVE_V2 / "output" / "survivor_rows.jsonl")
    story_rows = read_jsonl(output_dir / "story_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert reconstructed_certificates(story_rows) == expected_certificates(source_rows)
    assert summary["rule_id"] == RULE_ID
    assert summary["certificate_count"] == 3
    assert summary["source_certificate_row_count"] == len(source_rows)
    assert summary["story_row_count"] == len(story_rows)
    assert {row["rule_id"] for row in story_rows} == {RULE_ID}
    keys = {
        (story["case_id"], story["source_anchor"])
        for story in story_rows
    }
    for key in keys:
        certificate_rows = [
            story
            for story in story_rows
            if (story["case_id"], story["source_anchor"]) == key
        ]
        assert [row["event_index"] for row in certificate_rows] == list(range(len(certificate_rows)))
    for path in (output_dir / "story_rows.jsonl", output_dir / "summary.json"):
        data = path.read_bytes()
        assert b"\r\n" not in data
        assert data.endswith(b"\n")
