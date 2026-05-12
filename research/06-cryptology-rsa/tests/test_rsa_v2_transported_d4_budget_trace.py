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
TRACE_SCRIPT = V2 / "transported_d4_budget_trace.py"
RULE_ID = "transported_d4_budget_trace_v1"


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
    """Write a compact transported-story surface for trace tests."""
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


def run_trace(tmp_path: Path, budget_dir: Path) -> Path:
    """Run the strict d=4 budget trace over budget sidecar rows."""
    module = load_module(TRACE_SCRIPT)
    output_dir = tmp_path / "trace"
    assert module.main(
        [
            "--budget-rows",
            str(budget_dir / "budget_rows.jsonl"),
            "--recursive-budget-rows",
            str(budget_dir / "recursive_budget_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0
    return output_dir


def test_transported_d4_budget_trace_follows_public_anchor_links(tmp_path):
    """The trace follows only induced-anchor to recursive source-anchor links."""
    story_dir = build_story_rows(tmp_path)
    budget_dir = run_budget(tmp_path, story_dir)
    output_dir = run_trace(tmp_path, budget_dir)

    budget_rows = read_jsonl(budget_dir / "budget_rows.jsonl")
    trace_rows = read_jsonl(output_dir / "trace_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    strict_rows = [row for row in budget_rows if row["strict_budget_frontier_candidate"]]

    assert summary["rule_id"] == RULE_ID
    assert summary["strict_candidate_count"] == len(strict_rows) == len(trace_rows)
    assert summary["still_unresolved_count"] == sum(
        1 for row in trace_rows if row["terminal_class"] == "still_unresolved"
    )
    assert sum(summary["terminal_partition"].values()) == len(trace_rows)

    for row in trace_rows:
        assert row["rule_id"] == RULE_ID
        assert row["start"]["strict_budget_frontier_candidate"]
        path = row["path"]
        if path:
            assert path[0]["source_anchor"] == row["start"]["induced_anchor"]
        for index, path_row in enumerate(path[1:], start=1):
            assert path_row["source_anchor"] == path[index - 1]["induced_anchor"]
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_transported_d4_budget_trace_reports_recursive_survivor_children(tmp_path):
    """The trace inspects non-depth0 recursive survivors without promoting them."""
    story_dir = build_story_rows(tmp_path)
    budget_dir = run_budget(tmp_path, story_dir)
    output_dir = run_trace(tmp_path, budget_dir)

    recursive_rows = read_jsonl(budget_dir / "recursive_budget_rows.jsonl")
    survivor_rows = read_jsonl(output_dir / "recursive_survivor_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    expected_survivors = [
        row
        for row in recursive_rows
        if int(row["recursion_depth"]) > 0 and row["ledger_recursive_survivor"]
    ]

    assert summary["non_depth0_recursive_survivor_count"] == len(expected_survivors)
    assert len(survivor_rows) == len(expected_survivors)
    for row in survivor_rows:
        survivor = row["survivor"]
        assert survivor["ledger_recursive_survivor"]
        assert int(survivor["recursion_depth"]) > 0
        for parent in row["parents"]:
            assert parent["induced_anchor"] == survivor["source_anchor"]
        if row["child"] is not None:
            assert row["child"]["source_anchor"] == survivor["induced_anchor"]
            assert row["child_terminal_class"] == row["child"]["terminal_class"]


def test_transported_d4_budget_trace_terminal_priority_is_explicit():
    """Terminal priority gives typed and stale state precedence over later states."""
    module = load_module(TRACE_SCRIPT)
    typed_cycle_budget = {
        "ledger_eliminated": True,
        "ledger_stale_transport_state": False,
        "ledger_recursive_cycle_state": True,
        "budget_blocks_frontier": True,
        "ledger_recursive_survivor": False,
    }
    cycle_budget = {
        "ledger_eliminated": False,
        "ledger_stale_transport_state": False,
        "ledger_recursive_cycle_state": True,
        "budget_blocks_frontier": True,
        "ledger_recursive_survivor": False,
    }
    stale_cycle_budget = {
        "ledger_eliminated": False,
        "ledger_stale_transport_state": True,
        "ledger_recursive_cycle_state": True,
        "budget_blocks_frontier": True,
        "ledger_recursive_survivor": False,
    }

    assert module.terminal_class(None) == "missing"
    assert module.terminal_class(typed_cycle_budget) == "typed"
    assert module.terminal_class(stale_cycle_budget) == "stale"
    assert module.terminal_class(cycle_budget) == "recursive_cycle"


def test_transported_d4_budget_trace_writes_lf_json_sidecars(tmp_path):
    """The trace sidecar writes LF-only JSON and JSONL."""
    story_dir = build_story_rows(tmp_path)
    budget_dir = run_budget(tmp_path, story_dir)
    output_dir = run_trace(tmp_path, budget_dir)

    for path in (
        output_dir / "trace_rows.jsonl",
        output_dir / "recursive_survivor_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_transported_d4_budget_trace_source_has_no_forbidden_inference_constructs():
    """The trace probe stays out of forbidden inference machinery."""
    source = TRACE_SCRIPT.read_text(encoding="utf-8")
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
