from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"
STORY_SCRIPT = V2 / "transported_story_law_probe.py"
BUDGET_SCRIPT = V2 / "transported_d4_budget_probe.py"
RULE_ID = "transported_d4_budget_v1"


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


def build_story_rows(tmp_path: Path) -> Path:
    """Write a compact transported-story surface for budget tests."""
    module = load_module(STORY_SCRIPT)
    output_dir = tmp_path / "story"
    assert module.main(
        [
            "--measured-rows",
            "8",
            "--recursive-depth",
            "3",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0
    return output_dir


def run_budget(tmp_path: Path, story_dir: Path) -> Path:
    """Run the transported d=4 budget probe over a story-law surface."""
    module = load_module(BUDGET_SCRIPT)
    output_dir = tmp_path / "budget"
    assert module.main(
        [
            "--story-rows",
            str(story_dir / "story_law_rows.jsonl"),
            "--recursive-rows",
            str(story_dir / "recursive_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0
    return output_dir


def test_transported_d4_budget_probe_measures_public_budget_rows(tmp_path):
    """The d=4 budget sidecar measures story rows without mutating inference."""
    story_dir = build_story_rows(tmp_path)
    output_dir = run_budget(tmp_path, story_dir)

    story_rows = read_jsonl(story_dir / "story_law_rows.jsonl")
    budget_rows = read_jsonl(output_dir / "budget_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert len(budget_rows) == len(story_rows) == 16
    assert summary["rule_id"] == RULE_ID
    assert summary["row_count"] == 16
    assert summary["ledger_eliminated_count"] == sum(
        1 for row in story_rows if row["ledger_eliminated"]
    )
    assert summary["ledger_effective_survivor_count"] == sum(
        1 for row in story_rows if row["ledger_effective_survivor"]
    )
    for row in budget_rows:
        assert row["rule_id"] == RULE_ID
        assert row["source_d4_count"] == len(row["source_d4_values"])
        assert row["source_d4_count"] == len(row["transported_source_d4_values"])
        assert row["source_d4_count"] == len(row["transported_source_d4_symbols"])
        assert row["induced_d4_count"] == len(row["induced_d4_values"])
        assert row["induced_d4_count"] == len(row["induced_d4_symbols"])
        assert row["net_frontier_budget"] == (
            row["induced_d4_uncommitted_count"] - row["transported_d4_debt"]
        )
        assert row["budget_blocks_frontier"] == (
            row["net_frontier_budget"] <= 0
            or (
                row["induced_carrier_is_d4"]
                and row["induced_carrier_committed"]
            )
        )
        assert row["open_d4_carrier"] == (
            row["induced_carrier_is_d4"]
            and row["induced_carrier_symbol"] == "O"
        )
        assert row["strict_budget_frontier_candidate"] == (
            row["opposite_orientation_polarity"]
            and row["ledger_effective_survivor"]
            and row["open_d4_carrier"]
        )
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_transported_d4_budget_marks_official_40bit_typed_row(tmp_path):
    """The official 40-bit typed row has a committed d=4 carrier."""
    story_dir = build_story_rows(tmp_path)
    output_dir = run_budget(tmp_path, story_dir)
    rows = read_jsonl(output_dir / "budget_rows.jsonl")

    official = next(
        row
        for row in rows
        if row["case_id"] == "rsa_v2_40bit_static_001"
        and row["source_anchor"] == "1048571"
    )

    assert official["ledger_eliminated"]
    assert official["induced_carrier_is_d4"]
    assert official["induced_carrier_committed"]
    assert official["budget_blocks_frontier"]
    assert not official["strict_budget_frontier_candidate"]


def test_transported_d4_budget_writes_lf_json_sidecars(tmp_path):
    """The d=4 budget sidecar writes LF-only JSON and JSONL."""
    story_dir = build_story_rows(tmp_path)
    output_dir = run_budget(tmp_path, story_dir)

    for path in (
        output_dir / "budget_rows.jsonl",
        output_dir / "recursive_budget_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_transported_d4_budget_source_has_no_forbidden_inference_constructs():
    """The d=4 budget probe stays out of forbidden inference machinery."""
    source = BUDGET_SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_tokens = (
        "sympy",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "prime_basis",
        "trial_division",
        "Miller",
        "audit_factors",
        "audit_spec",
        "random",
        "product_closure",
    )
    for token in forbidden_tokens:
        assert token not in source
    assert ast.get_docstring(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            assert ast.get_docstring(node)
