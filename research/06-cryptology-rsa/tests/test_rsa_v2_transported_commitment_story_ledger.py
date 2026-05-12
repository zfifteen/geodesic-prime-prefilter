from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"
SCRIPT = V2 / "transported_commitment_story_ledger_probe.py"
INPUT_DIR = V2 / "output" / "transported_exclusion_debt"


def load_module():
    """Load the story-ledger probe from its script path."""
    spec = importlib.util.spec_from_file_location(SCRIPT.stem, SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a probe output path."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_probe_reproduces_transported_ledger_count_contract(tmp_path):
    """The story ledger preserves the existing public transported-ledger counts."""
    module = load_module()
    output_dir = tmp_path / "story_ledger"

    assert module.main(["--input-dir", str(INPUT_DIR), "--output-dir", str(output_dir)]) == 0

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["falsification_status"] == "passed"
    assert summary["divergences"] == []
    assert summary["row_count"] == 512
    assert summary["ledger_effective_survivor_count"] == 202
    assert summary["recursive_row_count"] == 713
    assert summary["recursive_final_survivor_count"] == 0

    for name in ("ledger_rows.jsonl", "summary.json"):
        data = (output_dir / name).read_bytes()
        assert b"\r\n" not in data
        assert data.endswith(b"\n")


def test_story_ledger_rows_expose_required_public_diagnostic_fields(tmp_path):
    """The emitted rows contain the required story-conflict diagnostic surface."""
    module = load_module()
    output_dir = tmp_path / "story_ledger"

    assert module.main(["--input-dir", str(INPUT_DIR), "--output-dir", str(output_dir)]) == 0
    rows = read_jsonl(output_dir / "ledger_rows.jsonl")

    required_fields = {
        "case_id",
        "recursion_depth",
        "source_anchor",
        "induced_anchor",
        "source_event_kind",
        "source_event_value",
        "source_transport_image",
        "induced_event_kind",
        "induced_event_value",
        "transported_zone",
        "lock_carrier_d_relation",
        "story_rewrite",
        "ledger_prefix_elimination",
        "ledger_suffix_elimination",
        "ledger_recursive_cycle_state",
        "ledger_recursive_survivor",
        "rule_id",
    }
    assert len(rows) == 512
    assert required_fields.issubset(rows[0])
    assert rows[0] == {
        "case_id": "rsa_v2_40bit_static_001",
        "induced_anchor": "1048573",
        "induced_event_kind": "carrier_lock",
        "induced_event_value": "1048574",
        "ledger_effective_survivor": False,
        "ledger_prefix_elimination": True,
        "ledger_recursive_cycle_state": False,
        "ledger_recursive_survivor": False,
        "ledger_suffix_elimination": True,
        "lock_carrier_d_relation": "lower",
        "recursion_depth": 0,
        "rule_id": "transported_commitment_story_ledger_v1",
        "source_anchor": "1048571",
        "source_event_kind": "carrier_lock",
        "source_event_value": "1048572",
        "source_transport_image": "1048575",
        "story_rewrite": True,
        "transported_zone": "prefix",
    }


def test_story_ledger_probe_uses_no_forbidden_factorization_or_random_apis():
    """The diagnostic script does not use forbidden resolver or random APIs."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    forbidden_names = {
        "gcd",
        "isprime",
        "nextprime",
        "factorint",
        "randint",
        "random",
        "randrange",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            assert node.id not in forbidden_names
        if isinstance(node, ast.Attribute):
            assert node.attr not in forbidden_names
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, ast.Mod)
