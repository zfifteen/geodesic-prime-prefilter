from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "experiments" / "rsa" / "v2"
SCRIPT = V2 / "transported_story_law_probe.py"
RULE_ID = "transported_story_law_v1"
EXPECTED_COUNTS = {
    "row_count": 512,
    "ledger_effective_survivor_count": 202,
    "recursive_row_count": 713,
    "recursive_final_survivor_count": 0,
}


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test output path."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_transported_story_law_reproduces_direct_ledger_collapse(tmp_path):
    """The direct story-law probe reproduces the transported-ledger count contract."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == RULE_ID
    assert summary["falsification_status"] == "passed"
    assert summary["divergences"] == []
    assert summary["expected_counts"] == EXPECTED_COUNTS
    for field, expected in EXPECTED_COUNTS.items():
        assert summary[field] == expected

    assert len(rows) == EXPECTED_COUNTS["row_count"]
    assert len(recursive_rows) == EXPECTED_COUNTS["recursive_row_count"]
    assert summary["ledger_prefix_elimination_count"] == 101
    assert summary["ledger_suffix_elimination_count"] == 16
    assert summary["ledger_threat_ceiling_elimination_count"] == 0


def test_transported_story_law_rows_are_public_sidecar_rows(tmp_path):
    """The direct story-law output carries only public diagnostic fields."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(
        [
            "--measured-rows",
            "4",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    forbidden_fields = {
        "p",
        "q",
        "audit_status",
        "audit_integrity_status",
        "inference_audit_status",
        "product_check",
        "product_closure",
        "divisibility",
        "gcd",
        "isprime",
        "nextprime",
        "factorint",
        "resolver_label",
    }
    required_fields = {
        "case_id",
        "bits",
        "N",
        "rule_id",
        "source_anchor",
        "source_story_event_kinds",
        "source_story_event_values",
        "source_transport_carrier_image",
        "source_transport_reset_image",
        "source_transport_deadline_image",
        "transported_prefix_lo",
        "transported_prefix_hi",
        "transported_suffix_lo",
        "transported_suffix_hi",
        "induced_anchor",
        "induced_story_event_kinds",
        "induced_story_event_values",
        "ledger_prefix_elimination",
        "ledger_suffix_elimination",
        "ledger_threat_ceiling_elimination",
        "ledger_effective_survivor",
    }

    assert len(rows) == 8
    for row in rows:
        assert row["rule_id"] == RULE_ID
        assert required_fields.issubset(row)
        assert forbidden_fields.isdisjoint(row)


def test_transported_story_law_writes_lf_json_sidecars(tmp_path):
    """The story-law sidecar writes LF-only JSON and JSONL."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--measured-rows", "2", "--output-dir", str(output_dir)]) == 0

    for path in (
        output_dir / "story_law_rows.jsonl",
        output_dir / "recursive_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_transported_story_law_source_has_no_forbidden_inference_constructs():
    """The direct story-law probe stays out of forbidden inference machinery."""
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_tokens = (
        "transported_exclusion_debt",
        "ledger_fields",
        "sympy",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "direct_divisor_count",
        "prime_basis",
        "trial_division",
        "Miller",
        "audit_factors",
        "audit_spec",
        "random",
    )
    for token in forbidden_tokens:
        assert token not in source
    for node in ast.walk(tree):
        assert not isinstance(node, ast.Mod)
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, ast.Mult)
