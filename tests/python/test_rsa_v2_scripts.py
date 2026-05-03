from __future__ import annotations

import ast
import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "experiments" / "rsa" / "v2"
SCRIPT_NAMES = (
    "build_ladder_fixtures.py",
    "generate_ladder_rung.py",
    "run_experiment.py",
    "audit_experiment.py",
)
CASE_ID = "rsa_v2_40bit_static_001"
N_VALUE = "1099507433251"
P_VALUE = "1048559"
Q_VALUE = "1048589"
CASE_50_ID = "rsa_v2_50bit_static_001"
RULE_ID = "reciprocal_pgs_deadline_lock_v1"
GENERATED_50_N = "1027435935526951"
GENERATED_50_P = "30729371"
GENERATED_50_Q = "33434981"


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def parse_script(name: str) -> ast.Module:
    """Parse one v2 script for static boundary checks."""
    return ast.parse((V2 / name).read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test fixture path."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def build_fixtures(tmp_path: Path) -> None:
    """Write fixture files into one temporary directory."""
    module = load_module(V2 / "build_ladder_fixtures.py")
    assert module.main(["--output-dir", str(tmp_path)]) == 0


def run_inference(tmp_path: Path) -> Path:
    """Run inference over temporary fixture files and return the output directory."""
    module = load_module(V2 / "run_experiment.py")
    output_dir = tmp_path / "out"
    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0
    return output_dir


def test_scripts_and_algorithm_docs_exist():
    """As a reviewer, I want all v2 entry points and contract docs present."""
    for name in SCRIPT_NAMES:
        assert (V2 / name).exists()
    for name in (
        "AGENTS.md",
        "ALGORITHM.md",
        "ARITHMETIC.md",
        "METRICS.md",
        "README.md",
        "ladder_spec.json",
        "audit_spec.json",
    ):
        assert (V2 / name).exists()


def test_scripts_have_module_and_function_docstrings():
    """As a reviewer, I want every script construct to explain its contract."""
    for name in SCRIPT_NAMES:
        tree = parse_script(name)
        assert ast.get_docstring(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                assert ast.get_docstring(node)


def test_fixture_builder_writes_public_case_and_separate_audit_file(tmp_path):
    """As a reviewer, I want public cases physically separate from audit endpoints."""
    build_fixtures(tmp_path)

    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "audit_factors.jsonl",
        "ladder_cases.jsonl",
    ]
    for path in tmp_path.iterdir():
        data = path.read_bytes()
        assert b"\r\n" not in data
        assert data.endswith(b"\n")


def test_ladder_spec_is_public_and_contains_no_audit_factors():
    """As a reviewer, I want rung additions to be public data edits."""
    payload = json.loads((V2 / "ladder_spec.json").read_text(encoding="utf-8"))

    assert payload == {
        "cases": [
            {
                "case_id": CASE_ID,
                "description": "40-bit calibration rung for reciprocal PGS deadline-lock machinery.",
                "N": N_VALUE,
            },
            {
                "case_id": CASE_50_ID,
                "description": "50-bit deterministic RSA-like ladder rung generated outside the solver.",
                "N": GENERATED_50_N,
            }
        ]
    }
    for row in payload["cases"]:
        assert {"p", "q"}.isdisjoint(row)


def test_fixture_builder_reads_specs_instead_of_python_constants(tmp_path):
    """As a reviewer, I want the builder to consume JSON specs."""
    ladder_spec = tmp_path / "ladder_spec.json"
    audit_spec = tmp_path / "audit_spec.json"
    output_dir = tmp_path / "fixtures"
    ladder_spec.write_text(
        json.dumps(
            {
                "cases": [
                    {
                        "case_id": CASE_ID,
                        "description": "Spec-driven test rung.",
                        "N": N_VALUE,
                    }
                ]
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    audit_spec.write_text(
        json.dumps(
            {
                "factors": [
                    {
                        "case_id": CASE_ID,
                        "p": P_VALUE,
                        "q": Q_VALUE,
                    }
                ]
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "build_ladder_fixtures.py")

    assert module.main(
        [
            "--ladder-spec",
            str(ladder_spec),
            "--audit-spec",
            str(audit_spec),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    assert read_jsonl(output_dir / "ladder_cases.jsonl")[0]["description"] == "Spec-driven test rung."


def test_public_case_contains_only_public_rung_data(tmp_path):
    """As a reviewer, I want only N-derived public data in the case file."""
    build_fixtures(tmp_path)

    rows = read_jsonl(tmp_path / "ladder_cases.jsonl")
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "description": "40-bit calibration rung for reciprocal PGS deadline-lock machinery.",
            "N": N_VALUE,
        },
        {
            "case_id": CASE_50_ID,
            "bits": 50,
            "description": "50-bit deterministic RSA-like ladder rung generated outside the solver.",
            "N": GENERATED_50_N,
        }
    ]
    for row in rows:
        assert {"p", "q", "radius", "balance_band"}.isdisjoint(row)


def test_runner_reduces_static_40_bit_rung_to_two_deadline_lock_rows(tmp_path):
    """As a user, I want the official solver to reproduce the 40-bit deadline lock."""
    build_fixtures(tmp_path)

    output_dir = run_inference(tmp_path)
    inference = read_jsonl(output_dir / "inference_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    survivors = read_jsonl(output_dir / "survivor_rows.jsonl")

    assert inference == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "status": "resolved",
            "p": P_VALUE,
            "q": Q_VALUE,
            "rule_id": RULE_ID,
        },
        {
            "case_id": CASE_50_ID,
            "bits": 50,
            "N": GENERATED_50_N,
            "status": "unresolved",
            "unresolved_reason": "no_reciprocal_deadline_lock",
            "rule_id": RULE_ID,
        }
    ]
    assert summary["cases"][0]["reciprocal_window_candidates"] == 204
    assert summary["cases"][0]["recursive_lock_survivors"] == 10
    assert summary["cases"][0]["deadline_lock_ordered_rows"] == 2
    assert summary["cases"][0]["deadline_lock_pairs"] == 1
    assert summary["cases"][1]["reciprocal_window_candidates"] == 0
    assert summary["cases"][1]["recursive_lock_survivors"] == 0
    assert summary["cases"][1]["deadline_lock_ordered_rows"] == 0
    assert summary["cases"][1]["deadline_lock_pairs"] == 0
    assert [row["deadline_locked"] for row in survivors].count(True) == 2


def test_deadline_lock_rows_are_selected_before_audit(tmp_path):
    """As a reviewer, I want the selected rows to be produced by deadline state."""
    build_fixtures(tmp_path)
    output_dir = run_inference(tmp_path)

    locked = [
        row
        for row in read_jsonl(output_dir / "survivor_rows.jsonl")
        if row["deadline_locked"]
    ]
    assert [(row["x"], row["y"]) for row in locked] == [
        (P_VALUE, Q_VALUE),
        (Q_VALUE, P_VALUE),
    ]
    assert {row["deadline_lock_reason"] for row in locked} == {"reciprocal_deadline_lock"}
    assert {row["lower_reset_signature"] for row in locked} == {
        "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail"
    }
    assert {row["upper_reset_signature"] for row in locked} == {
        "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail"
    }
    assert {row["lower_reset_deadline_margin"] for row in locked} == {12}
    assert {row["upper_reset_deadline_margin"] for row in locked} == {12}


def test_audit_passes_only_with_separate_factor_file(tmp_path):
    """As a reviewer, I want audit certification separate from inference."""
    build_fixtures(tmp_path)
    output_dir = run_inference(tmp_path)
    audit_output = tmp_path / "audit.csv"
    module = load_module(V2 / "audit_experiment.py")

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--factors",
            str(tmp_path / "audit_factors.jsonl"),
            "--inference",
            str(output_dir / "inference_rows.jsonl"),
            "--output",
            str(audit_output),
        ]
    ) == 0

    with audit_output.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": "40",
            "N": N_VALUE,
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_pass",
        },
        {
            "case_id": CASE_50_ID,
            "bits": "50",
            "N": GENERATED_50_N,
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_fail",
        }
    ]
    for row in rows:
        assert {"p", "q"}.isdisjoint(row)


def test_runner_source_has_no_forbidden_constructs_or_hidden_endpoints():
    """As a reviewer, I want inference free of forbidden machinery."""
    forbidden = (
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
        "sieve",
        "audit_factors",
        P_VALUE,
        Q_VALUE,
    )
    source = (V2 / "run_experiment.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_runner_has_no_per_scale_logic_branches():
    """As a reviewer, I want N to be data and the rule to stay global."""
    source = (V2 / "run_experiment.py").read_text(encoding="utf-8")
    forbidden_fragments = (
        "if case.bits",
        "case.bits ==",
        "case.bits <",
        "case.bits >",
        "40bit",
        "50bit",
        "bits == 40",
        "bits == 50",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_fixture_builder_has_no_generation_or_classical_math_imports():
    """As a reviewer, I want fixture writing to stay static."""
    forbidden = (
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
        "sieve",
    )
    source = (V2 / "build_ladder_fixtures.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source
    assert P_VALUE not in source
    assert Q_VALUE not in source


def test_generation_script_emits_reproducible_50_bit_provenance(tmp_path):
    """As a reviewer, I want 50-bit rung generation to be reproducible and isolated."""
    module = load_module(V2 / "generate_ladder_rung.py")
    output = tmp_path / "rung_50bit_provenance.json"

    assert module.main(["--output", str(output)]) == 0

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["public_ladder_spec_row"] == {
        "case_id": "rsa_v2_50bit_static_001",
        "description": "50-bit externally generated RSA-like ladder rung.",
        "N": GENERATED_50_N,
    }
    assert payload["audit_spec_row"] == {
        "case_id": "rsa_v2_50bit_static_001",
        "p": GENERATED_50_P,
        "q": GENERATED_50_Q,
    }
    assert int(GENERATED_50_P) * int(GENERATED_50_Q) == int(GENERATED_50_N)
    assert int(GENERATED_50_N).bit_length() == 50
    assert payload["selection_rule"] == "first pair from fixed SHA-256 counter streams satisfying all criteria"


def test_generation_script_is_physically_separate_from_solver():
    """As a reviewer, I want rung generation to stay outside inference."""
    source = (V2 / "generate_ladder_rung.py").read_text(encoding="utf-8")
    forbidden = (
        "run_experiment",
        "audit_experiment",
        "ladder_spec.json",
        "audit_spec.json",
        "subprocess",
        "OpenSSL",
        "random",
    )
    for token in forbidden:
        assert token not in source
