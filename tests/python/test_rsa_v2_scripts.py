from __future__ import annotations

import ast
import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "experiments" / "rsa" / "v2"
SCRIPT_NAMES = (
    "build_ladder_fixtures.py",
    "run_experiment.py",
    "audit_experiment.py",
)
CASE_ID = "rsa_v2_40bit_static_001"
N_VALUE = 1099507433251
P_VALUE = 1048559
Q_VALUE = 1048589


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def parse_script(name: str) -> ast.Module:
    """Parse one v2 script for static boundary checks."""
    return ast.parse((V2 / name).read_text())


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test fixture path."""
    return [json.loads(line) for line in path.read_text().splitlines()]


def write_jsonl(rows: list[dict[str, object]], path: Path) -> None:
    """Write JSONL rows with LF line endings."""
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def build_fixtures(tmp_path: Path) -> None:
    """Write the static fixture files into one temporary directory."""
    module = load_module(V2 / "build_ladder_fixtures.py")
    assert module.main(["--output-dir", str(tmp_path)]) == 0


def run_inference(tmp_path: Path, output_name: str = "rows.jsonl") -> Path:
    """Run inference over temporary fixture files and return the output path."""
    module = load_module(V2 / "run_experiment.py")
    output = tmp_path / output_name
    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--state",
            str(tmp_path / "ladder_pgs_state.jsonl"),
            "--output",
            str(output),
        ]
    ) == 0
    return output


def test_scripts_and_algorithm_doc_exist():
    """As a reviewer, I want all v2 entry points and the algorithm note present."""
    for name in SCRIPT_NAMES:
        assert (V2 / name).exists()
    assert (V2 / "ALGORITHM.md").exists()


def test_scripts_have_module_and_function_docstrings():
    """As a reviewer, I want every script construct to explain its contract."""
    for name in SCRIPT_NAMES:
        tree = parse_script(name)
        assert ast.get_docstring(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                assert ast.get_docstring(node)


def test_fixture_builder_writes_exact_static_files(tmp_path):
    """As a reviewer, I want exactly the three planned fixture files."""
    build_fixtures(tmp_path)

    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "audit_factors.jsonl",
        "ladder_cases.jsonl",
        "ladder_pgs_state.jsonl",
    ]
    for path in tmp_path.iterdir():
        data = path.read_bytes()
        assert b"\r\n" not in data
        assert data.endswith(b"\n")


def test_public_case_contains_no_audit_factors(tmp_path):
    """As a reviewer, I want public case rows free of audit-only factors."""
    build_fixtures(tmp_path)

    rows = read_jsonl(tmp_path / "ladder_cases.jsonl")
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "radius": 1024,
        }
    ]
    assert {"p", "q"}.isdisjoint(rows[0])


def test_runner_resolves_static_40_bit_ladder(tmp_path):
    """As a user, I want the one-row experiment to emit the resolved pair."""
    build_fixtures(tmp_path)

    output = run_inference(tmp_path)

    assert read_jsonl(output) == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "status": "resolved",
            "p": P_VALUE,
            "q": Q_VALUE,
            "rule_id": "reciprocal_reset_deadline_lock_v1",
        }
    ]


def test_runner_returns_unresolved_without_unique_lock(tmp_path):
    """As a reviewer, I want missing or duplicated locks to stay unresolved."""
    build_fixtures(tmp_path)
    state_path = tmp_path / "ladder_pgs_state.jsonl"
    rows = read_jsonl(state_path)

    write_jsonl(
        [row for row in rows if int(row["lower_value"]) != P_VALUE],
        state_path,
    )
    output = run_inference(tmp_path, "missing_lock.jsonl")
    assert read_jsonl(output) == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "status": "unresolved",
            "unresolved_reason": "no_reciprocal_reset_deadline_lock",
        }
    ]

    write_jsonl(rows + [rows[-1]], state_path)
    output = run_inference(tmp_path, "duplicated_lock.jsonl")
    assert read_jsonl(output) == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "status": "unresolved",
            "unresolved_reason": "multiple_reciprocal_reset_deadline_locks",
        }
    ]


def test_audit_passes_only_with_separate_factor_file(tmp_path):
    """As a reviewer, I want audit certification separate from inference."""
    build_fixtures(tmp_path)
    inference_path = run_inference(tmp_path)
    audit_output = tmp_path / "audit.csv"
    module = load_module(V2 / "audit_experiment.py")

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--factors",
            str(tmp_path / "audit_factors.jsonl"),
            "--inference",
            str(inference_path),
            "--output",
            str(audit_output),
        ]
    ) == 0

    with audit_output.open() as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": "40",
            "N": str(N_VALUE),
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_pass",
        }
    ]
    assert {"p", "q"}.isdisjoint(rows[0])


def test_runner_source_has_no_forbidden_constructs():
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
    )
    source = (V2 / "run_experiment.py").read_text()
    for token in forbidden:
        assert token not in source


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
    source = (V2 / "build_ladder_fixtures.py").read_text()
    for token in forbidden:
        assert token not in source
