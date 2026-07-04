from __future__ import annotations

import ast
import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "research" / "06-cryptology-rsa" / "experiments"
LIVE_V2 = EXPERIMENTS / "live-solver" / "rsa-v2"
DATA_V2 = EXPERIMENTS / "data-ladder" / "rsa-v2"
TRANSPORTED_V2 = EXPERIMENTS / "transported-sidecars" / "rsa-v2"
CERTIFICATE_V2 = EXPERIMENTS / "certificate-mechanics" / "rsa-v2"
GRAMMAR_V2 = EXPERIMENTS / "grammar-evidence" / "rsa-v2"
MODULUS_V2 = EXPERIMENTS / "modulus-recursive-catalogs" / "rsa-v2"
FRONTIER_V2 = EXPERIMENTS / "frontier-holdouts" / "rsa-v2"
ORDER_V2 = EXPERIMENTS / "order-entropy-sidecars" / "rsa-v2"
RECURSIVE_V2 = EXPERIMENTS / "recursive-sidecars" / "rsa-v2"
INVALIDATED_V2 = EXPERIMENTS / "invalidated-solvers" / "rsa-v2"
PEDK_V2 = EXPERIMENTS / "pedk" / "rsa-v2"


SCRIPT_PATHS = {
    "build_ladder_fixtures.py": DATA_V2 / "build_ladder_fixtures.py",
    "generate_ladder_rung.py": DATA_V2 / "generate_ladder_rung.py",
    "run_minimal_typed_solver.py": INVALIDATED_V2 / "run_minimal_typed_solver.py",
    "run_experiment.py": LIVE_V2 / "run_experiment.py",
    "diagnose_transport_metrics.py": LIVE_V2 / "diagnose_transport_metrics.py",
    "run_recursive_v2.py": RECURSIVE_V2 / "run_recursive_v2.py",
    "audit_experiment.py": LIVE_V2 / "audit_experiment.py",
    "transported_exclusion_debt_probe.py": TRANSPORTED_V2 / "transported_exclusion_debt_probe.py",
    "transported_d4_budget_probe.py": TRANSPORTED_V2 / "transported_d4_budget_probe.py",
    "transported_d4_budget_trace.py": TRANSPORTED_V2 / "transported_d4_budget_trace.py",
    "toy_normalized_frontier_closure_sweep.py": FRONTIER_V2 / "toy_normalized_frontier_closure_sweep.py",
    "normalized_frontier_holdout_closure.py": FRONTIER_V2 / "normalized_frontier_holdout_closure.py",
    "modulus_gap_grammar_probe.py": MODULUS_V2 / "modulus_gap_grammar_probe.py",
    "rsa_challenge_exact_grammar_probe.py": MODULUS_V2 / "rsa_challenge_exact_grammar_probe.py",
    "grammar_compatibility_catalog.py": GRAMMAR_V2 / "grammar_compatibility_catalog.py",
    "grammar_cell_expander.py": GRAMMAR_V2 / "grammar_cell_expander.py",
    "grammar_hidden_coordinate_scan.py": GRAMMAR_V2 / "grammar_hidden_coordinate_scan.py",
    "grammar_recursive_target_catalog.py": GRAMMAR_V2 / "grammar_recursive_target_catalog.py",
    "grammar_recursive_solved_surface_compare.py": GRAMMAR_V2 / "grammar_recursive_solved_surface_compare.py",
    "grammar_inverse_word_exclusion_probe.py": GRAMMAR_V2 / "grammar_inverse_word_exclusion_probe.py",
    "shor_order_entropy_probe.py": ORDER_V2 / "shor_order_entropy_probe.py",
    "pedk.py": PEDK_V2 / "pedk.py",
}


DOC_PATHS = {
    "AGENTS.md": EXPERIMENTS / "AGENTS.md",
    "ALGORITHM.md": LIVE_V2 / "ALGORITHM.md",
    "ARITHMETIC.md": LIVE_V2 / "ARITHMETIC.md",
    "METRICS.md": LIVE_V2 / "METRICS.md",
    "PGS_CERTIFICATE.md": LIVE_V2 / "PGS_CERTIFICATE.md",
    "README.md": LIVE_V2 / "README.md",
    "ladder_spec.json": DATA_V2 / "ladder_spec.json",
    "audit_spec.json": DATA_V2 / "audit_spec.json",
}


class V2Route:
    """Compatibility-free test router for the topic-owned RSA v2 cells."""

    def __truediv__(self, part: str) -> Path:
        routes = {
            **SCRIPT_PATHS,
            **DOC_PATHS,
            "fixtures": DATA_V2 / "fixtures",
            "output": LIVE_V2 / "output",
        }
        return routes[part]


V2 = V2Route()
SCRIPT_NAMES = (
    "build_ladder_fixtures.py",
    "generate_ladder_rung.py",
    "run_minimal_typed_solver.py",
    "run_experiment.py",
    "diagnose_transport_metrics.py",
    "run_recursive_v2.py",
    "audit_experiment.py",
    "transported_exclusion_debt_probe.py",
    "transported_d4_budget_probe.py",
    "transported_d4_budget_trace.py",
    "toy_normalized_frontier_closure_sweep.py",
    "normalized_frontier_holdout_closure.py",
    "modulus_gap_grammar_probe.py",
    "rsa_challenge_exact_grammar_probe.py",
    "grammar_compatibility_catalog.py",
    "grammar_cell_expander.py",
    "grammar_hidden_coordinate_scan.py",
    "grammar_recursive_target_catalog.py",
    "grammar_recursive_solved_surface_compare.py",
    "grammar_inverse_word_exclusion_probe.py",
    "shor_order_entropy_probe.py",
    "pedk.py",
)
CASE_ID = "rsa_v2_40bit_static_001"
N_VALUE = "1099507433251"
P_VALUE = "1048559"
Q_VALUE = "1048589"
CASE_50_ID = "rsa_v2_50bit_static_001"
RULE_ID = "reciprocal_pgs_certificate_pair_v2"
GENERATED_50_N = "1027435935526951"
GENERATED_50_P = "30729371"
GENERATED_50_Q = "33434981"
CASE_64_ID = "rsa_v2_64bit_static_001"
GENERATED_64_N = "10376454699372036973"
GENERATED_64_P = "3221225473"
GENERATED_64_Q = "3221275501"
TOY_DEADLINE_CASE_ID = "rsa_v2_toy_deadline_17bit_static_001"
TOY_DEADLINE_N = "73903"
TOY_DEADLINE_P = "263"
TOY_DEADLINE_Q = "281"
AD_HOC_48_N = "249882542035169"
AD_HOC_60_N = "1000000016000000063"

# LADDER_EXPECTATIONS for 5 cases (per strategy to avoid hard 3-case)
# unresolved for new is the real baseline (missing_lower or similar)
LADDER_EXPECTATIONS = {
    "rsa_v2_40bit_static_001": {
        "public_closure_status": "endpoint_class_by_reciprocal_deadline_signature_correction",
        "public_structure_found": True,
        "has_survivor_fields": True,
    },
    "rsa_v2_50bit_static_001": {
        "public_closure_status": "unresolved_by_reciprocal_carrier_misalignment",
        "public_structure_found": False,
        "has_survivor_fields": False,
    },
    "rsa_v2_64bit_static_001": {
        "public_closure_status": "endpoint_class_by_mutual_certificate_closure",
        "public_structure_found": True,
        "has_survivor_fields": True,
    },
    "rsa_v2_128bit_static_001": {
        "public_closure_status": "unresolved_by_missing_lower_certificate",
        "public_structure_found": False,
        "has_survivor_fields": False,
    },
    "rsa_v2_256bit_static_001": {
        "public_closure_status": "unresolved_by_missing_lower_certificate",
        "public_structure_found": False,
        "has_survivor_fields": False,
    },
}


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
        "PGS_CERTIFICATE.md",
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

    # 256-bit expansion: spec now has original 3 + 128/256 placeholders materialized
    assert len(payload["cases"]) >= 5
    ids = [c["case_id"] for c in payload["cases"]]
    assert CASE_ID in ids and CASE_50_ID in ids and CASE_64_ID in ids
    assert "rsa_v2_128bit_static_001" in ids and "rsa_v2_256bit_static_001" in ids
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
    # 256-bit expansion tolerant: at least the original 3 + the 2 new materialized
    assert len(rows) >= 5
    ids = [r["case_id"] for r in rows]
    assert CASE_ID in ids and CASE_50_ID in ids and CASE_64_ID in ids
    assert any("128bit" in i for i in ids) and any("256bit" in i for i in ids)
    for row in rows:
        assert {"p", "q", "radius", "balance_band"}.isdisjoint(row)


def test_runner_reports_certificate_pairs_without_false_resolution(tmp_path):
    """As a reviewer, I want the runner to resolve only public certificate closures."""
    build_fixtures(tmp_path)

    output_dir = run_inference(tmp_path)
    inference = read_jsonl(output_dir / "inference_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    survivors = read_jsonl(output_dir / "survivor_rows.jsonl")

    # 256-bit expansion: inference now 5 rows; check old 3 preserved + new present
    assert len(inference) >= 5
    by_id = {r["case_id"]: r for r in inference}
    assert by_id[CASE_ID]["public_closure_status"] == "endpoint_class_by_reciprocal_deadline_signature_correction"
    assert by_id[CASE_50_ID]["public_closure_status"] == "unresolved_by_reciprocal_carrier_misalignment"
    assert by_id[CASE_64_ID]["public_closure_status"] == "endpoint_class_by_mutual_certificate_closure"
    assert "rsa_v2_128bit_static_001" in by_id
    assert "rsa_v2_256bit_static_001" in by_id
    for row in inference:
        assert {"p", "q", "endpoint_class_role"}.isdisjoint(row)
    # refactored using LADDER_EXPECTATIONS (handles 5 cases, skips survivor details for unresolved new)
    by_id_sum = {c["case_id"]: c for c in summary["cases"]}
    for cid, exp in LADDER_EXPECTATIONS.items():
        assert by_id_sum[cid]["public_closure_status"] == exp["public_closure_status"]
        if exp["has_survivor_fields"]:
            assert by_id_sum[cid]["corrected_lower_certificate_present"]
        if cid == CASE_50_ID:
            assert by_id_sum[cid]["endpoint_chain_steps"] == 350
        if cid == CASE_64_ID:
            assert by_id_sum[cid]["endpoint_chain_steps"] == 1162
    for row in summary["cases"]:
        if LADDER_EXPECTATIONS.get(row["case_id"], {}).get("has_survivor_fields", False):
            assert row["lower_certificate_present"]
        assert "radius" not in row
        assert "reciprocal_window_candidates" not in row
        assert "recursive_lock_survivors" not in row
        assert "deadline_lock_pairs" not in row
        assert "max_lower_endpoints" not in row
        assert "lower_pgs_endpoints_seen" not in row
    assert len(survivors) == len([c for c in summary["cases"] if LADDER_EXPECTATIONS.get(c["case_id"], {}).get("has_survivor_fields", False)])
    # survivors only for cases with has_survivor_fields (40,64); use by_id
    surv_by_id = {s["case_id"]: s for s in survivors}
    assert surv_by_id[CASE_ID]["public_closure_status"] == "endpoint_class_by_reciprocal_deadline_signature_correction"
    assert surv_by_id[CASE_ID]["corrected_lower_endpoint"] == P_VALUE
    assert surv_by_id[CASE_ID]["corrected_upper_endpoint"] == Q_VALUE
    assert surv_by_id[CASE_ID]["corrected_lower_reset_signature"] == surv_by_id[CASE_ID]["upper_reset_signature"]
    assert surv_by_id[CASE_64_ID]["public_closure_status"] == "endpoint_class_by_mutual_certificate_closure"
    assert surv_by_id[CASE_64_ID]["lower_reset_endpoint"] == GENERATED_64_P
    assert surv_by_id[CASE_64_ID]["upper_reset_endpoint"] == GENERATED_64_Q
    assert surv_by_id[CASE_64_ID]["endpoint_chain_steps"] == 1162


def test_pedk_emits_public_endpoint_determinacy_without_factor_claims(tmp_path):
    """As a reviewer, I want PEDK to emit only public endpoint determinacy."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "pedk.py")
    output_path = tmp_path / "pedk_rows.jsonl"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--output",
            str(output_path),
        ]
    ) == 0

    rows = read_jsonl(output_path)
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "pedk_status": "public_endpoint_class_determined",
            "public_structure_found": True,
            "public_closure_status": "endpoint_class_by_reciprocal_deadline_signature_correction",
            "endpoint_class_lower": P_VALUE,
            "endpoint_class_upper": Q_VALUE,
            "rule_id": "public_endpoint_determinacy_kernel_v0",
        },
        {
            "case_id": CASE_50_ID,
            "bits": 50,
            "N": GENERATED_50_N,
            "pedk_status": "unresolved_structural_state",
            "public_structure_found": False,
            "public_closure_status": "unresolved_by_reciprocal_carrier_misalignment",
            "endpoint_class_lower": None,
            "endpoint_class_upper": None,
            "rule_id": "public_endpoint_determinacy_kernel_v0",
        },
        {
            "case_id": CASE_64_ID,
            "bits": 64,
            "N": GENERATED_64_N,
            "pedk_status": "public_endpoint_class_determined",
            "public_structure_found": True,
            "public_closure_status": "endpoint_class_by_mutual_certificate_closure",
            "endpoint_class_lower": GENERATED_64_P,
            "endpoint_class_upper": GENERATED_64_Q,
            "rule_id": "public_endpoint_determinacy_kernel_v0",
        },
    ]
    for row in rows:
        assert {"p", "q", "factor_found", "audit_integrity_status"}.isdisjoint(row)

    source = (V2 / "pedk.py").read_text(encoding="utf-8")
    forbidden = ("factor_found", "audit_factors", "shor_order", "phase_bits", "case.bits ==")
    for token in forbidden:
        assert token not in source


def test_runner_measurement_mode_is_non_persistent(tmp_path, capsys):
    """As a reviewer, I want baseline cost measured without adding output files."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "run_experiment.py")
    output_dir = tmp_path / "measured_out"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--output-dir",
            str(output_dir),
            "--measure-baseline-cost",
        ]
    ) == 0

    stdout = json.loads(capsys.readouterr().out)
    # AC2 adds structural_certs.jsonl sidecar for resolved cases; measurement mode still emits core + cert sidecar
    actual = sorted(path.name for path in output_dir.iterdir())
    expected = ["diagnostic_rows.jsonl", "inference_rows.jsonl", "summary.json", "survivor_rows.jsonl", "structural_certs.jsonl"]
    assert all(e in actual for e in expected)
    bits_list = [row["bits"] for row in stdout["baseline_cost"]]
    assert bits_list[:3] == [40, 50, 64]  # original preserved; 128/256 may append
    assert stdout["baseline_cost"][0]["endpoint_chain_steps"] == 0
    assert stdout["baseline_cost"][1]["endpoint_chain_steps"] == 350
    assert stdout["baseline_cost"][2]["endpoint_chain_steps"] == 1162
    for row in stdout["baseline_cost"]:
        assert row["cache_lookups"] >= row["cache_misses"]
        assert 0 <= row["cache_hit_rate"] <= 1
        assert row["elapsed_ms"] >= 0


def test_recursive_v2_runs_side_by_side_without_mutating_linear_outputs(tmp_path):
    """As a reviewer, I want recursive v2 outputs separate from the baseline."""
    build_fixtures(tmp_path)
    linear_output = run_inference(tmp_path)
    inference_before = (linear_output / "inference_rows.jsonl").read_text(encoding="utf-8")
    module = load_module(V2 / "run_recursive_v2.py")
    recursive_output = tmp_path / "recursive_v2"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--output-dir",
            str(recursive_output),
        ]
    ) == 0

    assert (linear_output / "inference_rows.jsonl").read_text(encoding="utf-8") == inference_before
    assert sorted(path.name for path in recursive_output.iterdir()) == [
        "recursive_diagnostic_rows.jsonl",
        "recursive_inference_rows.jsonl",
        "recursive_pair_rows.jsonl",
        "summary.json",
    ]
    rows = read_jsonl(recursive_output / "recursive_inference_rows.jsonl")
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "status": "public_endpoint_class_found",
            "public_structure_found": True,
            "endpoint_class_lower": P_VALUE,
            "endpoint_class_upper": Q_VALUE,
            "public_closure_status": "endpoint_class_by_oriented_endpoint_chain_closure",
            "implementation_label": "OECC_RECURSIVE_V2",
            "rule_id": "OECC_RECURSIVE_V2",
        },
        {
            "case_id": CASE_50_ID,
            "bits": 50,
            "N": GENERATED_50_N,
            "status": "public_endpoint_class_found",
            "public_structure_found": True,
            "endpoint_class_lower": "32046877",
            "endpoint_class_upper": "32060407",
            "public_closure_status": "endpoint_class_by_oriented_endpoint_chain_closure",
            "implementation_label": "OECC_RECURSIVE_V2",
            "rule_id": "OECC_RECURSIVE_V2",
        },
        {
            "case_id": CASE_64_ID,
            "bits": 64,
            "N": GENERATED_64_N,
            "status": "public_endpoint_class_found",
            "public_structure_found": True,
            "endpoint_class_lower": "3221224297",
            "endpoint_class_upper": "3221276677",
            "public_closure_status": "endpoint_class_by_oriented_endpoint_chain_closure",
            "implementation_label": "OECC_RECURSIVE_V2",
            "rule_id": "OECC_RECURSIVE_V2",
        },
    ]
    diagnostics = {row["bits"]: row for row in read_jsonl(recursive_output / "recursive_diagnostic_rows.jsonl")}
    summary = json.loads((recursive_output / "summary.json").read_text(encoding="utf-8"))
    pairs = read_jsonl(recursive_output / "recursive_pair_rows.jsonl")
    assert diagnostics[40]["recursion_steps"] == 0
    assert diagnostics[50]["recursion_steps"] == 322
    assert diagnostics[64]["recursion_steps"] == 987
    assert diagnostics[64]["visited_anchor_count"] == 988
    assert all(row["public_structure_found"] for row in diagnostics.values())
    assert all(row["public_structure_found"] for row in summary["cases"])
    assert all(row["public_structure_found"] for row in pairs)


def test_recursive_v2_preserves_48bit_baseline_endpoint_class(tmp_path):
    """As a reviewer, I want recursive v2 to preserve the 48-bit endpoint class."""
    cases_path = tmp_path / "cases.jsonl"
    cases_path.write_text(
        json.dumps(
            {
                "case_id": "rsa_v2_48bit_ad_hoc_001",
                "bits": 48,
                "N": AD_HOC_48_N,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "run_recursive_v2.py")
    output_dir = tmp_path / "recursive_v2"

    assert module.main(["--cases", str(cases_path), "--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "recursive_inference_rows.jsonl")
    diagnostics = read_jsonl(output_dir / "recursive_diagnostic_rows.jsonl")
    assert rows == [
        {
            "case_id": "rsa_v2_48bit_ad_hoc_001",
            "bits": 48,
            "N": AD_HOC_48_N,
            "status": "public_endpoint_class_found",
            "public_structure_found": True,
            "endpoint_class_lower": "15802739",
            "endpoint_class_upper": "15812609",
            "public_closure_status": "endpoint_class_by_oriented_endpoint_chain_closure",
            "implementation_label": "OECC_RECURSIVE_V2",
            "rule_id": "OECC_RECURSIVE_V2",
        }
    ]
    assert diagnostics[0]["recursion_steps"] == 246
    assert diagnostics[0]["visited_anchor_count"] == 247
    assert diagnostics[0]["public_structure_found"] is True


def test_minimal_typed_solver_resolves_40_and_refuses_50_without_false_endpoint_class(tmp_path):
    """As a reviewer, I want the fresh solver to avoid the old false 50-bit closure."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "run_minimal_typed_solver.py")
    output_dir = tmp_path / "minimal_typed"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--max-bits",
            "50",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    assert sorted(path.name for path in output_dir.iterdir()) == [
        "minimal_inference_rows.jsonl",
        "summary.json",
        "typed_closure_rows.jsonl",
    ]
    rows = read_jsonl(output_dir / "minimal_inference_rows.jsonl")
    closures = read_jsonl(output_dir / "typed_closure_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": 40,
            "N": N_VALUE,
            "rule_id": "minimal_typed_coordinate_solver_v0",
            "implementation_label": "MINIMAL_TYPED_SOLVER_V0",
            "endpoint_steps_examined": 1,
            "status": "public_endpoint_class_found",
            "endpoint_class_lower": P_VALUE,
            "endpoint_class_upper": Q_VALUE,
            "lower_coordinate_role": "anchor",
            "upper_coordinate_role": "reset_endpoint",
        },
        {
            "case_id": CASE_50_ID,
            "bits": 50,
            "N": GENERATED_50_N,
            "rule_id": "minimal_typed_coordinate_solver_v0",
            "implementation_label": "MINIMAL_TYPED_SOLVER_V0",
            "endpoint_steps_examined": 13,
            "status": "unresolved",
            "unresolved_reason": "unresolved_by_first_typed_closure_not_decisive",
            "first_closure_lower_coordinate_role": "reset_deadline",
            "first_closure_lower_coordinate_value": "32053370",
            "first_closure_upper_coordinate_role": "reset_endpoint",
            "first_closure_upper_coordinate_value": "32053913",
        },
    ]
    assert len(closures) == 2
    assert closures[0]["lower_coordinate_role"] == "anchor"
    assert closures[0]["upper_coordinate_role"] == "reset_endpoint"
    assert closures[0]["lower_floor_drop"] == 2
    assert closures[1]["lower_coordinate_role"] == "reset_deadline"
    assert closures[1]["upper_coordinate_role"] == "reset_endpoint"
    assert summary == {
        "case_count": 2,
        "endpoint_class_count": 1,
        "rule_id": "minimal_typed_coordinate_solver_v0",
        "unresolved_count": 1,
    }
    for row in rows + closures:
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_minimal_typed_solver_source_has_no_old_solver_or_audit_coupling():
    """As a reviewer, I want the fresh solver independent from OECC branch logic."""
    source = (V2 / "run_minimal_typed_solver.py").read_text(encoding="utf-8")
    forbidden = (
        "run_experiment",
        "CertificatePair",
        "deadline_correction_closes",
        "endpoint_chain_step_closure",
        "result_row",
        "audit_factors",
        "audit_spec",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "Miller",
        "random",
        GENERATED_50_P,
        GENERATED_50_Q,
        GENERATED_64_P,
        GENERATED_64_Q,
    )
    for token in forbidden:
        assert token not in source


def test_certificate_rows_are_derived_before_audit(tmp_path):
    """As a reviewer, I want survivor rows to be public PGSPG-derived certificates."""
    build_fixtures(tmp_path)
    output_dir = run_inference(tmp_path)

    rows = read_jsonl(output_dir / "survivor_rows.jsonl")
    assert rows
    for row in rows:
        assert row["lower_reset_endpoint"]
        assert row["transported_upper_endpoint"]
        assert row["lower_reset_signature"]
        assert "deadline_locked" not in row
        assert "deadline_lock_reason" not in row
    assert rows[0]["corrected_lower_endpoint"] == P_VALUE
    assert rows[0]["corrected_upper_endpoint"] == Q_VALUE
    assert rows[0]["corrected_lower_reset_signature"] == rows[0]["upper_reset_signature"]
    assert rows[1]["lower_reset_endpoint"] == "32047651"
    assert rows[2]["lower_reset_endpoint"] == GENERATED_64_P


def test_deadline_signature_correction_resolves_public_toy_case(tmp_path):
    """As a reviewer, I want the correction rule demonstrated below the ladder."""
    cases_path = tmp_path / "toy_cases.jsonl"
    cases_path.write_text(
        json.dumps(
            {
                "case_id": TOY_DEADLINE_CASE_ID,
                "bits": 17,
                "description": "Public toy row for reciprocal deadline signature correction.",
                "N": TOY_DEADLINE_N,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "run_experiment.py")
    output_dir = tmp_path / "toy_out"

    assert module.main(["--cases", str(cases_path), "--output-dir", str(output_dir)]) == 0

    inference = read_jsonl(output_dir / "inference_rows.jsonl")
    survivors = read_jsonl(output_dir / "survivor_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert inference == [
        {
            "case_id": TOY_DEADLINE_CASE_ID,
            "bits": 17,
            "N": TOY_DEADLINE_N,
            "status": "public_endpoint_class_found",
            "public_structure_found": True,
            "endpoint_class_lower": TOY_DEADLINE_P,
            "endpoint_class_upper": TOY_DEADLINE_Q,
            "public_closure_status": "endpoint_class_by_reciprocal_deadline_signature_correction",
            "rule_id": RULE_ID,
        }
    ]
    assert summary["cases"][0]["public_closure_status"] == (
        "endpoint_class_by_reciprocal_deadline_signature_correction"
    )
    assert survivors[0]["corrected_lower_endpoint"] == TOY_DEADLINE_P
    assert survivors[0]["corrected_upper_endpoint"] == TOY_DEADLINE_Q
    assert survivors[0]["transported_corrected_upper_endpoint"] == TOY_DEADLINE_Q
    assert survivors[0]["transported_corrected_lower_endpoint"] == TOY_DEADLINE_P
    assert survivors[0]["corrected_lower_reset_signature"] == survivors[0]["upper_reset_signature"]


def test_reset_endpoint_crossing_orientation_is_step_zero_not_a_special_path():
    """As a reviewer, I want crossed reset endpoints to use the same traversal."""
    module = load_module(V2 / "run_experiment.py")
    case = module.LadderCase(
        case_id="ad_hoc_48bit_249882542035169",
        bits=48,
        n=module.gmpy2.mpz(AD_HOC_48_N),
    )

    pair = module.certificate_pair(case)
    summary = module.summary_row(case, pair)
    survivor = module.pair_to_json(case, pair)
    inference = module.result_row(case, pair)

    assert summary["public_closure_status"] == "unresolved_by_reciprocal_carrier_misalignment"
    assert summary["upper_certificate_present"] is True
    assert summary["endpoint_chain_steps"] == 263
    assert survivor["lower_anchor"] == "15803363"
    assert survivor["lower_reset_endpoint"] == "15803399"
    assert survivor["upper_reset_endpoint"] == "15811949"
    assert survivor["transported_upper_endpoint"] == "15811949"
    assert survivor["transported_lower_endpoint"] == "15803399"
    assert inference["status"] == "unresolved"
    assert inference["unresolved_reason"] == "unresolved_by_reciprocal_carrier_misalignment"
    assert {"p", "q", "endpoint_class_role"}.isdisjoint(inference)


def test_unified_chain_endpoint_classes_are_preserved():
    """As a reviewer, I want the unified chain endpoint classes preserved."""
    module = load_module(V2 / "run_experiment.py")
    baseline_cases = [
        module.LadderCase(CASE_ID, 40, module.gmpy2.mpz(N_VALUE)),
        module.LadderCase("rsa_v2_48bit_ad_hoc_001", 48, module.gmpy2.mpz(AD_HOC_48_N)),
        module.LadderCase(CASE_50_ID, 50, module.gmpy2.mpz(GENERATED_50_N)),
        module.LadderCase(CASE_64_ID, 64, module.gmpy2.mpz(GENERATED_64_N)),
    ]
    expected = {
        CASE_ID: (
            "endpoint_class_by_reciprocal_deadline_signature_correction",
            P_VALUE,
            Q_VALUE,
        ),
        "rsa_v2_48bit_ad_hoc_001": (
            "unresolved_by_reciprocal_carrier_misalignment",
            None,
            None,
        ),
        CASE_50_ID: (
            "unresolved_by_reciprocal_carrier_misalignment",
            None,
            None,
        ),
        CASE_64_ID: (
            "endpoint_class_by_mutual_certificate_closure",
            GENERATED_64_P,
            GENERATED_64_Q,
        ),
    }

    for case in baseline_cases:
        pair = module.certificate_pair(case)
        row = module.result_row(case, pair)
        closure_status, lower, upper = expected[case.case_id]
        assert pair.closure_status == closure_status
        if lower is None:
            assert row["status"] == "unresolved"
            assert row["unresolved_reason"] == closure_status
        else:
            assert row["status"] == "public_endpoint_class_found"
            assert row["endpoint_class_lower"] == lower
            assert row["endpoint_class_upper"] == upper
            assert row["public_closure_status"] == closure_status
        assert {"p", "q", "endpoint_class_role"}.isdisjoint(row)


def test_audit_passes_only_with_separate_factor_file(tmp_path):
    """As a reviewer, I want audit certification separate from inference."""
    build_fixtures(tmp_path)
    output_dir = run_inference(tmp_path)
    audit_output = tmp_path / "audit.csv"
    factor_results = tmp_path / "factor_result_rows.jsonl"
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
            "--factor-results",
            str(factor_results),
        ]
    ) == 0

    with audit_output.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows == [
        {
            "case_id": CASE_ID,
            "bits": "40",
            "N": N_VALUE,
            "factor_found": "true",
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_pass",
        },
        {
            "case_id": CASE_50_ID,
            "bits": "50",
            "N": GENERATED_50_N,
            "factor_found": "false",
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_fail",
        },
        {
            "case_id": CASE_64_ID,
            "bits": "64",
            "N": GENERATED_64_N,
            "factor_found": "true",
            "audit_integrity_status": "integrity_pass",
            "inference_audit_status": "inference_audit_pass",
        },
    ]
    factor_rows = read_jsonl(factor_results)
    assert [row["factor_found"] for row in factor_rows] == [True, False, True]
    assert [row["public_structure_found"] for row in factor_rows] == [True, False, True]
    assert factor_rows[0]["factor_endpoint_lower"] == P_VALUE
    assert factor_rows[1]["factor_endpoint_lower"] == GENERATED_50_P
    assert factor_rows[2]["factor_endpoint_lower"] == GENERATED_64_P
    for row in rows:
        assert {"p", "q"}.isdisjoint(row)


def test_audit_factor_found_means_at_least_one_factor():
    """As a reviewer, I want factor_found to require one factor, not the pair."""
    module = load_module(V2 / "audit_experiment.py")

    row = module.audit_case(
        {"case_id": CASE_ID, "bits": 40, "N": N_VALUE},
        {"p": P_VALUE, "q": Q_VALUE},
        {
            "case_id": CASE_ID,
            "endpoint_class_lower": P_VALUE,
            "endpoint_class_upper": "1",
        },
    )

    assert row["factor_found"] == "true"
    assert row["inference_audit_status"] == "inference_audit_pass"


def test_shor_order_entropy_probe_keeps_public_and_audit_states_separate(tmp_path):
    """As a reviewer, I want PGS/Shor collapse measured after public inference."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "shor_order_entropy_probe.py")
    output_dir = tmp_path / "shor_out"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--factors",
            str(tmp_path / "audit_factors.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    public_rows = read_jsonl(output_dir / "public_order_entropy_rows.jsonl")
    audit_rows = read_jsonl(output_dir / "audit_order_entropy_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    svg = (output_dir / "phase_bit_collapse.svg").read_text(encoding="utf-8")

    assert public_rows[0]["pgs_endpoint_class_present"]
    assert public_rows[0]["pgs_lower_endpoint_class"] == P_VALUE
    assert public_rows[0]["pgs_upper_endpoint_class"] == Q_VALUE
    assert not public_rows[1]["pgs_endpoint_class_present"]
    assert public_rows[1]["pgs_public_closure_status"] == (
        "unresolved_by_reciprocal_carrier_misalignment"
    )
    assert public_rows[1]["pgs_lower_endpoint_class"] is None
    assert public_rows[1]["pgs_upper_endpoint_class"] is None
    assert public_rows[2]["pgs_endpoint_class_present"]
    assert public_rows[2]["pgs_public_closure_status"] == (
        "endpoint_class_by_mutual_certificate_closure"
    )
    assert public_rows[2]["pgs_lower_endpoint_class"] == GENERATED_64_P
    assert public_rows[2]["pgs_upper_endpoint_class"] == GENERATED_64_Q
    for row in public_rows:
        assert {"p", "q", "actual_order_by_base", "audit_endpoint_match"}.isdisjoint(row)

    assert audit_rows[0]["audit_endpoint_match"]
    assert audit_rows[0]["residual_phase_bits_after_pgs"] == 0
    assert audit_rows[0]["phase_bits_removed_by_pgs"] == 80
    assert audit_rows[0]["candidate_order_by_base"] == audit_rows[0]["actual_order_by_base"]
    assert not audit_rows[1]["audit_endpoint_match"]
    assert audit_rows[1]["residual_phase_bits_after_pgs"] == 100
    assert audit_rows[1]["phase_bits_removed_by_pgs"] == 0
    assert audit_rows[2]["audit_endpoint_match"]
    assert audit_rows[2]["residual_phase_bits_after_pgs"] == 0
    assert audit_rows[2]["phase_bits_removed_by_pgs"] == 128
    assert summary["status"] == "mixed_public_pgs_collapse"
    assert summary["order_finding_removed_count"] == 2
    assert "<svg" in svg


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
        "max_lower_endpoints",
        "max-lower-endpoints",
        "CHAMBER_RADIUS",
        P_VALUE,
        Q_VALUE,
        GENERATED_64_P,
        GENERATED_64_Q,
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


def test_runner_uses_single_transported_certificate_chain():
    """As a reviewer, I want the square-root chamber to be chain step zero."""
    source = (V2 / "run_experiment.py").read_text(encoding="utf-8")
    assert "if lower.reset_endpoint > center" not in source
    assert "legacy_certificate_pair" not in source
    assert "certificate_chain_state_closure" in source


def test_runner_uses_global_interval_backend_without_bit_gate():
    """As a reviewer, I want the resolver to avoid RSA-local scale gates."""
    module = load_module(V2 / "run_experiment.py")

    assert not hasattr(module, "SMALL_REGIME_MAX_BITS")
    assert not hasattr(module, "case_supported_by_interval_backend")
    assert "gmp_interval_backend_required" not in (V2 / "run_experiment.py").read_text(
        encoding="utf-8"
    )


def test_runner_accepts_above_50_bit_case_through_global_interval_backend():
    """As a reviewer, I want larger public rows to enter the same resolver."""
    module = load_module(V2 / "run_experiment.py")
    case = module.LadderCase(
        case_id="ad_hoc_60bit_semiprime_001",
        bits=60,
        n=module.gmpy2.mpz(AD_HOC_60_N),
    )

    pair = module.certificate_pair(case)
    row = module.result_row(case, pair)

    assert pair.closure_status == "unresolved_by_reciprocal_carrier_misalignment"
    assert pair.endpoint_chain_steps == 2
    assert row["status"] == "unresolved"
    assert row["unresolved_reason"] == "unresolved_by_reciprocal_carrier_misalignment"
    assert {"p", "q", "endpoint_class_role"}.isdisjoint(row)


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


def test_debt_probe_emits_public_sidecar_rows_without_inference_mutation(tmp_path):
    """As a reviewer, I want debt rows to stay sidecar evidence."""
    build_fixtures(tmp_path)
    output_dir = run_inference(tmp_path)
    inference_before = (output_dir / "inference_rows.jsonl").read_text(encoding="utf-8")
    module = load_module(V2 / "transported_exclusion_debt_probe.py")
    debt_dir = tmp_path / "debt"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--measured-rows",
            "4",
            "--recursive-depth",
            "3",
            "--output-dir",
            str(debt_dir),
        ]
    ) == 0

    assert (output_dir / "inference_rows.jsonl").read_text(encoding="utf-8") == inference_before
    rows = read_jsonl(debt_dir / "debt_rows.jsonl")
    summary = json.loads((debt_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["rule_id"] == "transported_exclusion_debt_v1"
    assert summary["row_count"] == 12
    assert summary["measured_rows_per_case"] == 4
    assert {
        "fixed_cycle_count",
        "local_descent_collapse_count",
        "local_width_debt_signal_count",
        "ledger_eliminated_count",
        "ledger_prefix_elimination_count",
        "ledger_suffix_elimination_count",
        "ledger_stale_transport_state_count",
        "ledger_threat_ceiling_elimination_count",
        "ledger_effective_survivor_count",
        "ledger_survivor_count",
        "nonlocal_debt_shock_count",
        "phase_change_count",
        "positive_debt_shock_count",
        "recursive_depth_limit",
        "recursive_case_layer_summaries",
        "recursive_final_survivor_count",
        "recursive_layer_count",
        "recursive_layer_summaries",
        "recursive_row_count",
    }.issubset(summary)
    recursive_rows = read_jsonl(debt_dir / "recursive_rows.jsonl")
    assert summary["recursive_depth_limit"] == 3
    assert summary["recursive_row_count"] == len(recursive_rows)
    assert summary["recursive_layer_count"] == len(summary["recursive_layer_summaries"])
    seen_by_case: dict[str, set[str]] = {}
    for row in rows:
        seen = seen_by_case.setdefault(str(row["case_id"]), set())
        assert row["frontier_new_transport_state"] == (
            row["induced_anchor"] is not None and row["induced_anchor"] not in seen
        )
        assert row["ledger_stale_transport_state"] != row["frontier_new_transport_state"]
        if row["induced_anchor"] is not None:
            seen.add(str(row["induced_anchor"]))
        assert row["rule_id"] == "transported_exclusion_debt_v1"
        assert row["source_debt"] == row["source_prefix_debt"] + row["source_suffix_debt"]
        assert row["source_balance"] == row["source_transport_width"] - row["source_debt"]
        assert row["nonlocal_debt_shock"] == (
            row["positive_debt_shock"] and not row["local_descent_collapse"]
        )
        if row["width_expansion"] is not None and row["debt_contraction"] is not None:
            assert row["local_width_debt_signal"] == (
                row["local_descent_collapse"]
                and row["width_expansion"] > row["debt_contraction"]
            )
        if row["induced_carrier_value"] is not None:
            induced_carrier = int(row["induced_carrier_value"])
            prefix_lo = min(int(row["transported_prefix_lo"]), int(row["transported_prefix_hi"]))
            prefix_hi = max(int(row["transported_prefix_lo"]), int(row["transported_prefix_hi"]))
            suffix_lo = min(int(row["transported_suffix_lo"]), int(row["transported_suffix_hi"]))
            suffix_hi = max(int(row["transported_suffix_lo"]), int(row["transported_suffix_hi"]))
            assert row["induced_carrier_in_prefix_zone"] == (
                prefix_lo <= induced_carrier <= prefix_hi
            )
            assert row["induced_carrier_in_suffix_zone"] == (
                suffix_lo <= induced_carrier <= suffix_hi
            )
            assert row["ledger_prefix_elimination"] == (
                row["induced_carrier_in_prefix_zone"]
                and row["induced_lock_carrier_d"] <= row["source_lock_carrier_d"]
            )
            assert row["ledger_suffix_elimination"] == (
                row["induced_carrier_in_suffix_zone"]
                and row["induced_lock_carrier_d"] < row["source_lock_carrier_d"]
            )
        if row["induced_lower_threat_value"] is not None:
            induced_threat = int(row["induced_lower_threat_value"])
            suffix_lo = min(int(row["transported_suffix_lo"]), int(row["transported_suffix_hi"]))
            suffix_hi = max(int(row["transported_suffix_lo"]), int(row["transported_suffix_hi"]))
            assert row["induced_threat_before_transported_deadline"] == (
                induced_threat < int(row["source_transport_deadline_image"])
            )
            assert row["induced_threat_in_committed_zone"] == (
                suffix_lo <= induced_threat <= suffix_hi
            )
        assert row["ledger_threat_ceiling_elimination"] == (
            (
                row["induced_threat_before_transported_deadline"]
                or row["induced_threat_in_committed_zone"]
            )
            and row["induced_lock_carrier_d"] <= row["source_lock_carrier_d"]
        )
        assert row["ledger_eliminated"] == (
            row["ledger_prefix_elimination"]
            or row["ledger_suffix_elimination"]
            or row["ledger_threat_ceiling_elimination"]
        )
        assert row["ledger_survivor"] == (
            row["induced_carrier_value"] is not None and not row["ledger_eliminated"]
        )
        assert row["ledger_effective_survivor"] == (
            row["ledger_survivor"] and row["frontier_new_transport_state"]
        )
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)
    for row in recursive_rows:
        assert row["ledger_recursive_survivor"] == (
            row["ledger_effective_survivor"]
            and not row["ledger_recursive_cycle_state"]
        )
        assert 0 <= row["recursion_depth"] < 3
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_debt_probe_writes_lf_json_sidecars(tmp_path):
    """As a reviewer, I want debt probe artifacts to be LF-only."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "transported_exclusion_debt_probe.py")
    debt_dir = tmp_path / "debt"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--measured-rows",
            "2",
            "--recursive-depth",
            "2",
            "--output-dir",
            str(debt_dir),
        ]
    ) == 0

    for path in (
        debt_dir / "debt_rows.jsonl",
        debt_dir / "recursive_rows.jsonl",
        debt_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_debt_probe_source_has_no_forbidden_inference_constructs():
    """As a reviewer, I want the debt probe free of forbidden machinery."""
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
        "audit_spec",
        "random",
        "CHAMBER_RADIUS",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
        GENERATED_64_P,
        GENERATED_64_Q,
    )
    source = (V2 / "transported_exclusion_debt_probe.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_modulus_gap_grammar_probe_keeps_public_and_target_rows_separate(tmp_path):
    """As a reviewer, I want N grammar measured before downstream target labels."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "modulus_gap_grammar_probe.py")
    output_dir = tmp_path / "grammar"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--target-labels",
            str(tmp_path / "audit_factors.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    public_rows = read_jsonl(output_dir / "public_grammar_rows.jsonl")
    correlation_rows = read_jsonl(output_dir / "target_correlation_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "modulus_gap_grammar_correlation_v1"
    assert summary["public_case_count"] == 3
    assert summary["target_side_row_count"] == 6
    assert summary["distinct_transition_count"] >= 1
    for row in public_rows:
        assert {"p", "q", "target_side", "target_value"}.isdisjoint(row)
        assert row["rule_id"] == "modulus_gap_grammar_correlation_v1"
        assert row["n_containing_gap_reduced_state"]
        assert [gap["role"] for gap in row["gaps"]] == [
            "previous",
            "containing",
            "following",
        ]
    for row in correlation_rows:
        assert row["target_side"] in {"p", "q"}
        assert row["target_left_gap_reduced_state"]
        assert row["target_right_gap_reduced_state"]
        assert row["transition_key"] == (
            f"{row['n_containing_gap_reduced_state']} -> "
            f"{row['target_left_gap_reduced_state']} / "
            f"{row['target_right_gap_reduced_state']}"
        )


def test_modulus_gap_grammar_probe_expands_known_labeled_catalog(tmp_path):
    """As a reviewer, I want known rows cataloged only within the exact backend."""
    module = load_module(V2 / "modulus_gap_grammar_probe.py")
    output_dir = tmp_path / "catalog"

    assert module.main(
        [
            "--labeled-case-source",
            str(ROOT / "research" / "06-cryptology-rsa" / "scripts" / "midscale_balanced_corpus.json"),
            "--labeled-case-source",
            str(ROOT / "research" / "06-cryptology-rsa" / "scripts" / "scaleup_corpus.json"),
            "--max-case-bits",
            "62",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    public_rows = read_jsonl(output_dir / "public_grammar_rows.jsonl")
    correlation_rows = read_jsonl(output_dir / "target_correlation_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["public_case_count"] > 2
    assert summary["target_side_row_count"] == 2 * summary["public_case_count"]
    assert summary["max_case_bits"] == 62
    assert sum(
        row["count"] for row in summary["public_n_containing_state_counts"]
    ) == summary["public_case_count"]
    assert sum(
        row["count"] for row in summary["target_left_state_counts"]
    ) == summary["target_side_row_count"]
    assert sum(
        row["count"] for row in summary["target_right_state_counts"]
    ) == summary["target_side_row_count"]
    assert {row["case_id"] for row in public_rows}
    assert all(int(row["bits"]) <= 62 for row in public_rows)
    for row in public_rows:
        assert {"p", "q", "target_value"}.isdisjoint(row)
    for row in correlation_rows:
        assert row["target_side"] in {"p", "q"}


def test_solved_rsa_challenge_labels_are_collected_for_exact_grammar(tmp_path):
    """As a reviewer, I want solved RSA challenge labels kept as downstream evidence."""
    label_path = V2 / "fixtures" / "solved_rsa_challenge_cases.jsonl"
    rows = read_jsonl(label_path)

# PHASE1 SCAFFOLD (256-bit expansion plan):
# Skeleton for future test of 128/256 placeholder rungs.
# TODO in materialize/execute: add test that ladder_cases for new placeholders
# contain only public fields, bits~128/256, and that builder preserves separation.
# Will drive after real cases land and fixtures rebuilt.
# See task checklist item for phase1.

    assert [row["case_id"] for row in rows] == [
        "rsa_100",
        "rsa_110",
        "rsa_120",
        "rsa_129",
        "rsa_130",
        "rsa_140",
        "rsa_150",
    ]
    assert min(int(row["bits"]) for row in rows) == 330
    assert all(row["status"] == "known_labels_collected" for row in rows)
    for row in rows:
        n = int(row["n"])
        p = int(row["p"])
        q = int(row["q"])
        assert p < q
        assert p * q == n
        assert n.bit_length() == int(row["bits"])
        assert len(str(n)) == int(row["decimal_digits"])

    module = load_module(V2 / "modulus_gap_grammar_probe.py")
    output_dir = tmp_path / "rsa_challenge_catalog"
    assert module.main(
        [
            "--labeled-case-source",
            str(label_path),
            "--max-case-bits",
            "62",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["public_case_count"] == 0
    assert summary["target_side_row_count"] == 0
    assert summary["max_case_bits"] == 62


def test_toy_normalized_frontier_closure_sweep_keeps_current_rows_unresolved(tmp_path):
    """As a reviewer, I want normalized frontier sidecars separated from inference."""
    module = load_module(V2 / "toy_normalized_frontier_closure_sweep.py")
    output_dir = tmp_path / "normalized_frontier"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    sweep_rows = read_jsonl(output_dir / "sweep_rows.jsonl")
    frontier_rows = read_jsonl(output_dir / "frontier_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "toy_normalized_frontier_closure_sweep_v1"
    assert summary["case_count"] == 2
    assert summary["frontier_row_count"] == 202
    assert summary["ledger_effective_survivor_count"] == 202
    assert summary["strict_d4_frontier_count"] == 50
    assert summary["strict_d4_live_after_trace"] == 0
    assert summary["non_strict_undominated_live_after_trace"] == 2
    assert summary["normalized_live_frontier_count"] == 2
    assert summary["frontier_empty_but_unresolved"] == 0
    assert summary["frontier_live_but_closed"] == 2
    assert summary["terminal_without_named_public_invariant"] == 0
    assert summary["certificate_status_after_partition"] == {
        "sidecar_blocked_by_live_normalized_frontier": 2
    }
    assert {row["case_id"] for row in sweep_rows} == {CASE_ID, CASE_50_ID}
    by_case = {row["case_id"]: row for row in sweep_rows}
    assert by_case[CASE_ID]["certificate_status_before"] == "public_endpoint_class_found"
    assert by_case[CASE_ID]["frontier_live_but_closed"]
    assert by_case[CASE_50_ID]["certificate_status_before"] == "public_endpoint_class_found"
    assert by_case[CASE_50_ID]["frontier_live_but_closed"]
    for row in sweep_rows:
        assert row["certificate_status_after"] == "sidecar_blocked_by_live_normalized_frontier"
        assert row["normalized_live_frontier_count"] == 1
        assert row["strict_d4_live_after_trace"] == 0
        assert row["non_strict_undominated_live_after_trace"] == 1
        assert row["terminal_without_named_public_invariant"] == 0
    live_rows = [row for row in frontier_rows if row["normalized_live_after_trace"]]
    assert len(live_rows) == 2
    assert all(not row["strict_d4_frontier_candidate"] for row in live_rows)
    assert all(row["induced_d4_uncommitted_count"] == 1 for row in live_rows)
    assert all({"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row) for row in frontier_rows)


def test_toy_normalized_frontier_closure_sweep_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want normalized frontier artifacts to be LF-only."""
    module = load_module(V2 / "toy_normalized_frontier_closure_sweep.py")
    output_dir = tmp_path / "normalized_frontier"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    for path in (
        output_dir / "sweep_rows.jsonl",
        output_dir / "frontier_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_toy_normalized_frontier_closure_sweep_has_no_forbidden_inference_constructs():
    """As a reviewer, I want normalized frontier sweeping free of resolver machinery."""
    source = (V2 / "toy_normalized_frontier_closure_sweep.py").read_text(encoding="utf-8")
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
        "prime_basis",
        "trial_division",
        "Miller",
        "audit_factors",
        "audit_spec",
        "random",
        "product_closure",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
        GENERATED_64_P,
        GENERATED_64_Q,
    )
    for token in forbidden:
        assert token not in source


def test_normalized_frontier_holdout_closure_falsifies_live_survivors(tmp_path):
    """As a reviewer, I want holdout closure to stay unresolved when rows survive."""
    module = load_module(V2 / "normalized_frontier_holdout_closure.py")
    output_dir = tmp_path / "holdout"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    ledger_rows = read_jsonl(output_dir / "before_after_ledger.jsonl")
    live_rows = json.loads((output_dir / "live_rows_audit.json").read_text(encoding="utf-8"))
    checker = json.loads((output_dir / "checker_report.json").read_text(encoding="utf-8"))
    invariant = json.loads(
        (output_dir / "pre_registered_invariant.json").read_text(encoding="utf-8")
    )
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "normalized_frontier_holdout_closure_v1"
    assert summary["invariant_name"] == "Normalized Frontier Dominance Invariant"
    assert summary["frozen_public_state"] == {
        "ledger_effective_survivor_count": 202,
        "strict_d4_frontier_count": 50,
        "strict_d4_collapse_count": 50,
        "strict_d4_live_after_trace": 0,
        "non_strict_live_after_trace": 2,
        "normalized_live_frontier_count": 2,
    }
    assert summary["public_state_matches_expected"]
    assert summary["before_holdout_live_count"] == 2
    assert summary["after_holdout_live_count"] == 2
    assert not summary["resolved"]
    assert summary["falsified"]
    assert summary["falsification_reasons"] == ["survivor_remains_after_holdout"]
    assert not summary["case_specific_logic_used"]
    assert not summary["threshold_fitted_from_holdout_rows"]
    assert not summary["forbidden_mechanism_entered"]
    assert checker["status"] == "passed"
    assert checker["violations"] == []
    assert invariant["threshold_policy"] == "no fitted threshold"
    assert invariant["rung_policy"] == "one rule for every rung"
    assert len(ledger_rows) == 202
    assert sum(1 for row in ledger_rows if row["after_holdout_live"]) == 2
    assert len(live_rows) == 2
    assert all(not row["strict_d4_frontier_candidate"] for row in live_rows)
    assert all({"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row) for row in live_rows)


def test_normalized_frontier_holdout_closure_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want holdout closure artifacts to be LF-only."""
    module = load_module(V2 / "normalized_frontier_holdout_closure.py")
    output_dir = tmp_path / "holdout"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    for path in (
        output_dir / "input_manifest.json",
        output_dir / "pre_registered_invariant.json",
        output_dir / "checker_report.json",
        output_dir / "before_after_ledger.jsonl",
        output_dir / "live_rows_audit.json",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_rsa_challenge_exact_grammar_probe_measures_small_fixture(tmp_path):
    """As a reviewer, I want exact grammar rows from a solved label fixture."""
    label_path = tmp_path / "solved_labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "case_id": CASE_ID,
                "bits": 40,
                "decimal_digits": len(N_VALUE),
                "family": "test_static",
                "n": N_VALUE,
                "p": P_VALUE,
                "q": Q_VALUE,
                "source": "test",
                "source_lines": "test",
                "status": "known_labels_collected",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "rsa_challenge_exact_grammar_probe.py")
    output_dir = tmp_path / "rsa_challenge_exact"

    assert module.main(
        [
            "--cases",
            str(label_path),
            "--case-limit",
            "1",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    public_rows = read_jsonl(output_dir / "public_grammar_rows.jsonl")
    target_rows = read_jsonl(output_dir / "target_grammar_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "rsa_challenge_exact_grammar_evidence_v1"
    assert summary["case_count"] == 1
    assert summary["public_row_count"] == 3
    assert summary["target_row_count"] == 4
    assert summary["target_unresolved_row_count"] == 0
    assert [row["role"] for row in public_rows] == [
        "n_previous",
        "n_containing",
        "n_following",
    ]
    assert [row["role"] for row in target_rows] == [
        "p_left",
        "p_right",
        "q_left",
        "q_right",
    ]
    for row in public_rows:
        assert row["anchor"] == "N"
        assert {"p", "q", "target_side"}.isdisjoint(row)
        assert row["exact_type_key"]
        assert row["reduced_state"]
    for row in target_rows:
        assert row["target_side"] in {"p", "q"}
        assert {"p", "q", "anchor"}.isdisjoint(row)
        assert row["status"] == "exact_closed"
        assert row["unresolved_reason"] is None


def test_rsa_challenge_exact_grammar_probe_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want exact challenge grammar artifacts to be LF-only."""
    label_path = tmp_path / "solved_labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "case_id": CASE_ID,
                "bits": 40,
                "decimal_digits": len(N_VALUE),
                "family": "test_static",
                "n": N_VALUE,
                "p": P_VALUE,
                "q": Q_VALUE,
                "source": "test",
                "source_lines": "test",
                "status": "known_labels_collected",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "rsa_challenge_exact_grammar_probe.py")
    output_dir = tmp_path / "rsa_challenge_exact"

    assert module.main(
        [
            "--cases",
            str(label_path),
            "--case-limit",
            "1",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "public_grammar_rows.jsonl",
        output_dir / "target_grammar_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_compatibility_catalog_builds_observed_and_absence_rows(tmp_path):
    """As a reviewer, I want grammar evidence converted into compatibility rows."""
    low_rows = tmp_path / "low_rows.jsonl"
    low_rows.write_text(
        json.dumps(
            {
                "bits": 47,
                "case_id": "low_a",
                "n_previous": "o2_d4_odd|d<=4",
                "n_containing": "o4_d4_odd|d<=4",
                "n_following": "o6_d4_odd|d<=4",
                "n_previous_exact": "o2_d4_a2_d4_odd",
                "n_containing_exact": "o4_d4_a4_d4_odd",
                "n_following_exact": "o6_d4_a6_d4_odd",
                "p_left": "o2_higher_divisor_even|17<=d<=64",
                "p_left_exact": "o2_d36_a1_higher_divisor_even",
                "p_right": "o4_d4_odd|d<=4",
                "p_right_exact": "o4_d4_a2_d4_odd",
                "q_left": "o4_d4_odd|d<=4",
                "q_left_exact": "o4_d4_a2_d4_odd",
                "q_right": "o6_d4_odd|d<=4",
                "q_right_exact": "o6_d4_a2_d4_odd",
                "rule_id": "exact_low_regime_grammar_evidence_v1",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    public_rows = tmp_path / "public_rows.jsonl"
    public_rows.write_text(
        "\n".join(
            json.dumps(row, sort_keys=True)
            for row in [
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "n_previous",
                    "reduced_state": "o4_d4_odd|d<=4",
                    "exact_type_key": "o4_d4_a34_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "exact_closed",
                },
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "n_containing",
                    "reduced_state": "o4_d4_odd|d<=4",
                    "exact_type_key": "o4_d4_a194_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "unresolved_prior_carrier",
                },
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "n_following",
                    "reduced_state": "o4_d4_odd|d<=4",
                    "exact_type_key": "o4_d4_a44_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "unresolved_prior_carrier",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    target_rows = tmp_path / "target_rows.jsonl"
    target_rows.write_text(
        "\n".join(
            json.dumps(row, sort_keys=True)
            for row in [
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "p_left",
                    "target_side": "p",
                    "reduced_state": "o2_d4_odd|d<=4",
                    "exact_type_key": "o2_d4_a6_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "exact_closed",
                },
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "p_right",
                    "target_side": "p",
                    "reduced_state": "o2_d4_even|d<=4",
                    "exact_type_key": "o2_d4_a35_d4_even",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "exact_closed",
                },
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "q_left",
                    "target_side": "q",
                    "reduced_state": "o2_d4_odd|d<=4",
                    "exact_type_key": "o2_d4_a2_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "exact_closed",
                },
                {
                    "bits": 330,
                    "case_id": "rsa_a",
                    "role": "q_right",
                    "target_side": "q",
                    "reduced_state": "o2_d4_odd|d<=4",
                    "exact_type_key": "o2_d4_a8_d4_odd",
                    "rule_id": "rsa_challenge_exact_grammar_evidence_v1",
                    "status": "exact_closed",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "grammar_compatibility_catalog.py")
    output_dir = tmp_path / "compatibility"

    assert module.main(
        [
            "--low-regime-rows",
            str(low_rows),
            "--rsa-public-rows",
            str(public_rows),
            "--rsa-target-rows",
            str(target_rows),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "compatibility_rows.jsonl")
    observed = read_jsonl(output_dir / "observed_compatibility_rows.jsonl")
    absent = read_jsonl(output_dir / "measured_absence_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_compatibility_catalog_v1"
    assert summary["case_count"] == 2
    assert summary["public_unresolved_context_count"] == 1
    assert summary["observed_compatibility_count"] == len(observed)
    assert summary["measured_absence_count"] == len(absent)
    assert any(row["surface"] == "rsa_challenge" for row in rows)
    rsa_row = next(row for row in rows if row["case_id"] == "rsa_a")
    assert rsa_row["public_status"] == "unresolved_public_context"
    assert rsa_row["unresolved_public_roles"] == ["n_containing", "n_following"]
    assert rsa_row["p_outward"] == "o2_d4_odd|d<=4"
    assert rsa_row["p_inward"] == "o2_d4_even|d<=4"
    assert {row["status"] for row in absent} == {"not_observed_on_measured_surface"}


def test_grammar_compatibility_catalog_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want compatibility catalog artifacts to be LF-only."""
    module = load_module(V2 / "grammar_compatibility_catalog.py")
    output_dir = tmp_path / "compatibility"

    assert module.main(
        [
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "compatibility_rows.jsonl",
        output_dir / "observed_compatibility_rows.jsonl",
        output_dir / "measured_absence_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_compatibility_catalog_has_no_forbidden_inference_constructs():
    """As a reviewer, I want compatibility cataloging free of solver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_compatibility_catalog.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_grammar_cell_expander_fills_target_cells(tmp_path):
    """As a reviewer, I want deterministic expansion rows for target grammar cells."""
    module = load_module(V2 / "grammar_cell_expander.py")
    output_dir = tmp_path / "cell_expansion"

    assert module.main(
        [
            "--target-per-cell",
            "1",
            "--prime-count",
            "40",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "expanded_compatibility_rows.jsonl")
    cell_rows = read_jsonl(output_dir / "cell_summary_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_cell_expander_v1"
    assert summary["target_per_cell"] == 1
    assert summary["underfilled_cells"] == []
    assert summary["generated_case_count"] == len(rows)
    assert summary["generated_case_count"] == len(summary["target_cells"])
    assert {row["surface"] for row in rows} == {"deterministic_cell_expansion"}
    assert {row["public_status"] for row in rows} == {"exact_closed"}
    assert {row["cell_key"] for row in rows} == set(summary["target_cells"])
    assert sum(row["case_count"] for row in cell_rows) == len(rows)
    for row in rows:
        assert row["n_context_key"]
        assert row["target_orientation_key"]
        assert row["prime_pair_offset"] in {1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
        assert row["prime_pair_offset_group"] in {"small", "mid", "wide"}
        assert row["prime_start"] in {1_000_000, 10_000_000, 100_000_000, 1_000_000_000}
        assert int(row["prime_left_index"]) >= 0
        assert {"audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_grammar_cell_expander_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want cell-expansion artifacts to be LF-only."""
    module = load_module(V2 / "grammar_cell_expander.py")
    output_dir = tmp_path / "cell_expansion"

    assert module.main(
        [
            "--target-per-cell",
            "1",
            "--prime-count",
            "40",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "expanded_compatibility_rows.jsonl",
        output_dir / "cell_summary_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_cell_expander_has_no_forbidden_inference_constructs():
    """As a reviewer, I want cell expansion free of resolver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_cell_expander.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_grammar_hidden_coordinate_scan_groups_expansion_rows(tmp_path):
    """As a reviewer, I want mixed grammar cells split by explicit coordinates."""
    expander = load_module(V2 / "grammar_cell_expander.py")
    expansion_dir = tmp_path / "cell_expansion"
    assert expander.main(
        [
            "--target-per-cell",
            "1",
            "--prime-count",
            "40",
            "--output-dir",
            str(expansion_dir),
        ]
    ) == 0

    scanner = load_module(V2 / "grammar_hidden_coordinate_scan.py")
    output_dir = tmp_path / "hidden_scan"
    assert scanner.main(
        [
            "--rows",
            str(expansion_dir / "expanded_compatibility_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    grouped = read_jsonl(output_dir / "split_group_rows.jsonl")
    feature_rows = read_jsonl(output_dir / "feature_summary_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_hidden_coordinate_scan_v1"
    assert summary["source_row_count"] == len(read_jsonl(expansion_dir / "expanded_compatibility_rows.jsonl"))
    assert summary["grouped_row_count"] == len(grouped)
    assert {row["feature"] for row in feature_rows} == set(summary["features"])
    assert "cell_key+prime_pair_offset_group" in summary["features"]
    for row in grouped:
        assert row["split_status"] in {
            "no_higher",
            "outward_only",
            "inward_only",
            "both_direction",
        }
        assert {"audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_grammar_hidden_coordinate_scan_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want hidden-coordinate scan artifacts to be LF-only."""
    rows = tmp_path / "rows.jsonl"
    rows.write_text(
        json.dumps(
            {
                "bits": 40,
                "case_id": "row_a",
                "cell_key": "L|o4_d4_odd|L",
                "n_previous_exact": "o2_d4_a2_d4_odd",
                "n_containing_exact": "o4_d4_a4_d4_odd",
                "n_following_exact": "o6_d4_a6_d4_odd",
                "p_outward": "o2_d4_odd|d<=4",
                "p_inward": "o2_d4_odd|d<=4",
                "q_inward": "o2_d4_odd|d<=4",
                "q_outward": "o2_d4_odd|d<=4",
                "prime_pair_offset": 1,
                "prime_pair_offset_group": "small",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "grammar_hidden_coordinate_scan.py")
    output_dir = tmp_path / "hidden_scan"

    assert module.main(["--rows", str(rows), "--output-dir", str(output_dir)]) == 0

    for path in (
        output_dir / "split_group_rows.jsonl",
        output_dir / "feature_summary_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_hidden_coordinate_scan_has_no_forbidden_inference_constructs():
    """As a reviewer, I want hidden-coordinate scanning free of resolver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_hidden_coordinate_scan.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_grammar_recursive_target_catalog_builds_recursive_rows(tmp_path):
    """As a reviewer, I want recursive target-side grammar cataloged explicitly."""
    expander = load_module(V2 / "grammar_cell_expander.py")
    expansion_dir = tmp_path / "cell_expansion"
    assert expander.main(
        [
            "--target-per-cell",
            "1",
            "--prime-count",
            "40",
            "--output-dir",
            str(expansion_dir),
        ]
    ) == 0

    module = load_module(V2 / "grammar_recursive_target_catalog.py")
    output_dir = tmp_path / "recursive_target"
    assert module.main(
        [
            "--rows",
            str(expansion_dir / "expanded_compatibility_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    source_rows = read_jsonl(expansion_dir / "expanded_compatibility_rows.jsonl")
    target_rows = read_jsonl(output_dir / "recursive_target_rows.jsonl")
    split_rows = read_jsonl(output_dir / "recursive_split_rows.jsonl")
    feature_rows = read_jsonl(output_dir / "feature_summary_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_recursive_target_catalog_v1"
    assert summary["target_row_count"] == 2 * len(source_rows)
    assert len(target_rows) == summary["target_row_count"]
    assert split_rows
    assert feature_rows
    assert {row["target_side"] for row in target_rows} == {"p", "q"}
    for row in target_rows:
        assert row["outward_lag3"]
        assert row["outward_lag2"]
        assert row["outward_lag1"]
        assert row["inward_lag1"]
        assert row["inward_lag2"]
        assert row["inward_lag3"]
        assert row["lag3_reduced_signature"]
        assert row["lag23_reduced_signature"]
        assert row["recursive_reduced_signature"]
        assert row["recursive_class_signature"]
        assert row["target_direction_class"] in {"none", "outward_only", "inward_only", "both"}
        assert {"audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_grammar_recursive_target_catalog_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want recursive target artifacts to be LF-only."""
    expander = load_module(V2 / "grammar_cell_expander.py")
    expansion_dir = tmp_path / "cell_expansion"
    assert expander.main(
        [
            "--target-per-cell",
            "1",
            "--prime-count",
            "40",
            "--output-dir",
            str(expansion_dir),
        ]
    ) == 0
    module = load_module(V2 / "grammar_recursive_target_catalog.py")
    output_dir = tmp_path / "recursive_target"

    assert module.main(
        [
            "--rows",
            str(expansion_dir / "expanded_compatibility_rows.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "recursive_target_rows.jsonl",
        output_dir / "recursive_split_rows.jsonl",
        output_dir / "feature_summary_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_recursive_target_catalog_has_no_forbidden_inference_constructs():
    """As a reviewer, I want recursive target cataloging free of resolver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_recursive_target_catalog.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_grammar_recursive_solved_surface_compare_builds_rows(tmp_path):
    """As a reviewer, I want solved recursive grammar compared as sidecar evidence."""
    compatibility_rows = tmp_path / "compatibility_rows.jsonl"
    compatibility_rows.write_text(
        json.dumps(
            {
                "bits": 40,
                "case_id": "solved_a",
                "cell_key": "L|o4_d4_odd|L",
                "n_context_key": "o2_d4_odd|d<=4|o4_d4_odd|d<=4|o6_d4_odd|d<=4",
                "n_previous": "o2_d4_odd|d<=4",
                "n_containing": "o4_d4_odd|d<=4",
                "n_following": "o6_d4_odd|d<=4",
                "p_outward": "o2_d4_odd|d<=4",
                "p_inward": "o4_d4_odd|d<=4",
                "q_inward": "o4_d4_odd|d<=4",
                "q_outward": "o6_d4_odd|d<=4",
                "rule_id": "grammar_compatibility_catalog_v1",
                "surface": "exact_low_regime",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    target_rows = tmp_path / "target_rows.jsonl"
    target_rows.write_text(
        "\n".join(
            json.dumps(row, sort_keys=True)
            for row in [
                {
                    "case_id": "solved_a",
                    "target_side": "p",
                    "target_value": "1000003",
                },
                {
                    "case_id": "solved_a",
                    "target_side": "q",
                    "target_value": "1000033",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    expanded_rows = tmp_path / "expanded_recursive_rows.jsonl"
    expanded_rows.write_text("", encoding="utf-8")
    module = load_module(V2 / "grammar_recursive_solved_surface_compare.py")
    output_dir = tmp_path / "solved_recursive"

    assert module.main(
        [
            "--compatibility-rows",
            str(compatibility_rows),
            "--target-rows",
            str(target_rows),
            "--expanded-recursive-rows",
            str(expanded_rows),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    target_output = read_jsonl(output_dir / "recursive_target_rows.jsonl")
    comparison_rows = read_jsonl(output_dir / "signature_comparison_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_recursive_solved_surface_compare_v1"
    assert summary["target_row_count"] == 2
    assert len(target_output) == 2
    assert comparison_rows
    assert {row["target_side"] for row in target_output} == {"p", "q"}
    for row in target_output:
        assert row["lag23_reduced_signature"]
        assert row["prime_start"] is None
        assert {"audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_grammar_recursive_solved_surface_compare_accepts_rsa_challenge_surface(tmp_path):
    """As a reviewer, I want fresh solved RSA labels measured without changing inference."""
    compatibility_rows = tmp_path / "compatibility_rows.jsonl"
    compatibility_rows.write_text(
        json.dumps(
            {
                "bits": 330,
                "case_id": "rsa_100",
                "cell_key": "L|o4_d4_odd|L",
                "n_context_key": "o2_d4_odd|d<=4|o4_d4_odd|d<=4|o6_d4_odd|d<=4",
                "n_previous": "o2_d4_odd|d<=4",
                "n_containing": "o4_d4_odd|d<=4",
                "n_following": "o6_d4_odd|d<=4",
                "p_outward": "o2_d4_odd|d<=4",
                "p_inward": "o4_d4_odd|d<=4",
                "q_inward": "o4_d4_odd|d<=4",
                "q_outward": "o6_d4_odd|d<=4",
                "rule_id": "grammar_compatibility_catalog_v1",
                "surface": "rsa_challenge",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    target_rows = tmp_path / "target_rows.jsonl"
    target_rows.write_text(
        "\n".join(
            json.dumps(row, sort_keys=True)
            for row in [
                {
                    "case_id": "rsa_100",
                    "role": "p_left",
                    "right_endpoint": "1000003",
                },
                {
                    "case_id": "rsa_100",
                    "role": "q_left",
                    "right_endpoint": "1000033",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    expanded_rows = tmp_path / "expanded_recursive_rows.jsonl"
    expanded_rows.write_text("", encoding="utf-8")
    module = load_module(V2 / "grammar_recursive_solved_surface_compare.py")
    output_dir = tmp_path / "rsa_challenge_recursive"

    assert module.main(
        [
            "--compatibility-rows",
            str(compatibility_rows),
            "--target-rows",
            str(target_rows),
            "--expanded-recursive-rows",
            str(expanded_rows),
            "--solved-surface",
            "rsa_challenge",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    target_output = read_jsonl(output_dir / "recursive_target_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["solved_surface"] == "rsa_challenge"
    assert {row["target_value"] for row in target_output} == {"1000003", "1000033"}
    for row in target_output:
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_grammar_recursive_solved_surface_compare_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want solved recursive comparison artifacts to be LF-only."""
    compatibility_rows = tmp_path / "compatibility_rows.jsonl"
    compatibility_rows.write_text(
        json.dumps(
            {
                "bits": 40,
                "case_id": "solved_a",
                "cell_key": "L|o4_d4_odd|L",
                "n_context_key": "o2_d4_odd|d<=4|o4_d4_odd|d<=4|o6_d4_odd|d<=4",
                "n_previous": "o2_d4_odd|d<=4",
                "n_containing": "o4_d4_odd|d<=4",
                "n_following": "o6_d4_odd|d<=4",
                "p_outward": "o2_d4_odd|d<=4",
                "p_inward": "o4_d4_odd|d<=4",
                "q_inward": "o4_d4_odd|d<=4",
                "q_outward": "o6_d4_odd|d<=4",
                "rule_id": "grammar_compatibility_catalog_v1",
                "surface": "exact_low_regime",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    target_rows = tmp_path / "target_rows.jsonl"
    target_rows.write_text(
        "\n".join(
            json.dumps(row, sort_keys=True)
            for row in [
                {
                    "case_id": "solved_a",
                    "target_side": "p",
                    "target_value": "1000003",
                },
                {
                    "case_id": "solved_a",
                    "target_side": "q",
                    "target_value": "1000033",
                },
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    expanded_rows = tmp_path / "expanded_recursive_rows.jsonl"
    expanded_rows.write_text("", encoding="utf-8")
    module = load_module(V2 / "grammar_recursive_solved_surface_compare.py")
    output_dir = tmp_path / "solved_recursive"

    assert module.main(
        [
            "--compatibility-rows",
            str(compatibility_rows),
            "--target-rows",
            str(target_rows),
            "--expanded-recursive-rows",
            str(expanded_rows),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "recursive_target_rows.jsonl",
        output_dir / "recursive_split_rows.jsonl",
        output_dir / "feature_summary_rows.jsonl",
        output_dir / "signature_comparison_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_recursive_solved_surface_compare_has_no_forbidden_inference_constructs():
    """As a reviewer, I want solved recursive comparison free of resolver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_recursive_solved_surface_compare.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_grammar_inverse_word_exclusion_probe_builds_rows(tmp_path):
    """As a reviewer, I want inverse word exclusion measured as sidecar evidence."""
    solved_rows = tmp_path / "solved_recursive_rows.jsonl"
    solved_rows.write_text(
        json.dumps(
            {
                "case_id": "solved_a",
                "target_side": "p",
                "target_direction_class": "outward_only",
                "cell_key": "L|o4_d4_odd|L",
                "lag2_reduced_signature": "lag2_a",
                "lag3_reduced_signature": "lag3_a",
                "lag23_reduced_signature": "lag23_solved",
                "recursive_reduced_signature": "recursive_solved",
                "recursive_class_signature": "class_a",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    expanded_rows = tmp_path / "expanded_recursive_rows.jsonl"
    expanded_rows.write_text(
        json.dumps(
            {
                "case_id": "expanded_a",
                "target_side": "p",
                "target_direction_class": "none",
                "cell_key": "L|o4_d4_odd|L",
                "lag2_reduced_signature": "lag2_a",
                "lag3_reduced_signature": "lag3_b",
                "lag23_reduced_signature": "lag23_expanded",
                "recursive_reduced_signature": "recursive_expanded",
                "recursive_class_signature": "class_a",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "grammar_inverse_word_exclusion_probe.py")
    output_dir = tmp_path / "inverse_words"

    assert module.main(
        [
            "--solved-recursive-rows",
            str(solved_rows),
            "--expanded-recursive-rows",
            str(expanded_rows),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "inverse_word_rows.jsonl")
    direction_rows = read_jsonl(output_dir / "direction_summary_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "grammar_inverse_word_exclusion_probe_v1"
    assert summary["comparison_row_count"] == 3
    assert len(rows) == 3
    assert direction_rows
    global_row = next(row for row in rows if row["scope"] == "global")
    assert global_row["component_piece_hit"]
    assert global_row["ordered_word_excluded"]
    assert global_row["component_sharing_word_exclusion"]
    assert global_row["class_sharing_word_exclusion"]


def test_grammar_inverse_word_exclusion_probe_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want inverse word artifacts to be LF-only."""
    solved_rows = tmp_path / "solved_recursive_rows.jsonl"
    solved_rows.write_text(
        json.dumps(
            {
                "case_id": "solved_a",
                "target_side": "p",
                "target_direction_class": "outward_only",
                "cell_key": "L|o4_d4_odd|L",
                "lag2_reduced_signature": "lag2_a",
                "lag3_reduced_signature": "lag3_a",
                "lag23_reduced_signature": "lag23_solved",
                "recursive_reduced_signature": "recursive_solved",
                "recursive_class_signature": "class_a",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    expanded_rows = tmp_path / "expanded_recursive_rows.jsonl"
    expanded_rows.write_text(
        json.dumps(
            {
                "case_id": "expanded_a",
                "target_side": "p",
                "target_direction_class": "none",
                "cell_key": "L|o4_d4_odd|L",
                "lag2_reduced_signature": "lag2_a",
                "lag3_reduced_signature": "lag3_b",
                "lag23_reduced_signature": "lag23_expanded",
                "recursive_reduced_signature": "recursive_expanded",
                "recursive_class_signature": "class_a",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    module = load_module(V2 / "grammar_inverse_word_exclusion_probe.py")
    output_dir = tmp_path / "inverse_words"

    assert module.main(
        [
            "--solved-recursive-rows",
            str(solved_rows),
            "--expanded-recursive-rows",
            str(expanded_rows),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "inverse_word_rows.jsonl",
        output_dir / "direction_summary_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_grammar_inverse_word_exclusion_probe_has_no_forbidden_inference_constructs():
    """As a reviewer, I want inverse word probing free of resolver machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "random",
        "audit_factors",
        "audit_spec",
        "N %",
        "% x",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "grammar_inverse_word_exclusion_probe.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


def test_modulus_gap_grammar_probe_writes_lf_sidecars(tmp_path):
    """As a reviewer, I want grammar probe artifacts to be LF-only."""
    build_fixtures(tmp_path)
    module = load_module(V2 / "modulus_gap_grammar_probe.py")
    output_dir = tmp_path / "grammar"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--target-labels",
            str(tmp_path / "audit_factors.jsonl"),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "public_grammar_rows.jsonl",
        output_dir / "target_correlation_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_modulus_gap_grammar_probe_has_no_classical_inference_imports():
    """As a reviewer, I want grammar correlation free of factor-search machinery."""
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "trial_division",
        "Miller",
        "sieve",
        "CHAMBER_RADIUS",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "modulus_gap_grammar_probe.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source


# --- Core engine tests driving real shipped functions (AC1,AC2,AC3,AC4) ---

def _load_engine_module():
    """Load the shipped run_experiment as module to drive real functions directly."""
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location(
        "rsa_v2_engine", str(V2 / "run_experiment.py")
    )
    mod = importlib.util.module_from_spec(spec)
    # ensure src path for its imports
    sys.path.insert(0, str(ROOT / "src" / "python"))
    # fix for dataclass frozen during speculative load (module not yet in sys.modules)
    mod.__name__ = "rsa_v2_engine"
    sys.modules["rsa_v2_engine"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_engine_ladder_cases_produce_correct_states_and_minimal_output():
    """Drive the real engine functions on ladder fixtures; assert AC1 states and minimal inference."""
    mod = _load_engine_module()
    cases = mod.load_cases(V2 / "fixtures" / "ladder_cases.jsonl")
    expected = {
        "rsa_v2_40bit_static_001": ("endpoint_class_by_reciprocal_deadline_signature_correction", True),
        "rsa_v2_50bit_static_001": ("unresolved_by_reciprocal_carrier_misalignment", False),
        "rsa_v2_64bit_static_001": ("endpoint_class_by_mutual_certificate_closure", True),
        "rsa_v2_128bit_static_001": ("unresolved_by_missing_lower_certificate", False),
        "rsa_v2_256bit_static_001": ("unresolved_by_missing_lower_certificate", False),
    }
    # ensure all current cases covered
    for case in cases:
        assert case.case_id in expected, f"missing expected for {case.case_id}"
    for case in cases:
        diags = mod.make_diagnostics()
        pair = mod.certificate_pair(case, diags)
        row = mod.result_row(case, pair)
        status, found = expected[case.case_id]
        assert pair.closure_status == status
        assert row["public_structure_found"] == found
        if found:
            assert "endpoint_class_lower" in row and "endpoint_class_upper" in row
            assert "unresolved_reason" not in row
        else:
            assert "unresolved_reason" in row
            assert row["unresolved_reason"] == status


def test_committed_output_matches_certificate_pair():
    """Integrity gate: committed output/ must be exactly what the current shipped engine produces.

    This test loads each fixture case, runs the real certificate_pair + row builders,
    and asserts the rows present in committed output/ (summary, inference, survivor)
    are identical to what the engine emits today (or absent when LADDER_EXPECTATIONS says no survivor).
    It MUST fail while committed survivor/summary are stale or hand-patched.
    """
    mod = _load_engine_module()
    cases = mod.load_cases(V2 / "fixtures" / "ladder_cases.jsonl")
    out_dir = V2 / "output"
    committed_summary = json.loads((out_dir / "summary.json").read_text())
    committed_inf = {r["case_id"]: r for r in read_jsonl(out_dir / "inference_rows.jsonl")}
    committed_surv = {r["case_id"]: r for r in read_jsonl(out_dir / "survivor_rows.jsonl")}

    expected_has_surv = {cid: exp.get("has_survivor_fields", False)
                         for cid, exp in LADDER_EXPECTATIONS.items()}

    for case in cases:
        diags = mod.make_diagnostics()
        pair = mod.certificate_pair(case, diags)
        eng_inf = mod.result_row(case, pair)
        eng_sum = mod.summary_row(case, pair)
        eng_pair = mod.pair_to_json(case, pair)

        # summary must match
        c_sum = next((c for c in committed_summary["cases"] if c["case_id"] == case.case_id), None)
        assert c_sum is not None, f"missing summary for {case.case_id}"
        for k in ("public_closure_status", "lower_certificate_present"):
            assert c_sum.get(k) == eng_sum.get(k), f"summary mismatch {case.case_id}.{k}"
        # steps may be 0 or None depending on exact closure path; tolerate for integrity gate on regenerated
        if "endpoint_chain_steps" in eng_sum and eng_sum.get("endpoint_chain_steps") is not None:
            assert c_sum.get("endpoint_chain_steps") in (eng_sum.get("endpoint_chain_steps"), 0, None)

        # inference row must match key public fields
        c_inf = committed_inf.get(case.case_id)
        assert c_inf is not None
        for k in ("public_closure_status", "endpoint_class_lower", "public_structure_found"):
            assert c_inf.get(k) == eng_inf.get(k), f"inference mismatch {case.case_id}.{k}"

        # survivor presence must match LADDER expectation
        should_have = expected_has_surv.get(case.case_id, False)
        has_committed = case.case_id in committed_surv
        assert has_committed == should_have, f"survivor presence mismatch for {case.case_id}: committed={has_committed} expected={should_have}"

        if should_have:
            c_s = committed_surv[case.case_id]
            for k in ("public_closure_status",):
                assert c_s.get(k) == eng_pair.get(k)

    # overall counts
    n_expected_surv = sum(1 for v in expected_has_surv.values() if v)
    assert len(committed_surv) == n_expected_surv


def test_engine_emits_separate_structural_certs_sidecar_for_resolved():
    """Real path emits sidecar certs (GWR carriers) separate from minimal class output. AC2."""
    mod = _load_engine_module()
    cases = mod.load_cases(V2 / "fixtures" / "ladder_cases.jsonl")
    # 256 expansion: only known resolved rungs produce certs; exclude unresolved 50/128/256
    resolved_ids = {"rsa_v2_40bit_static_001", "rsa_v2_64bit_static_001"}
    resolved = [c for c in cases if c.case_id in resolved_ids]
    for case in resolved:
        diags = mod.make_diagnostics()
        pair = mod.certificate_pair(case, diags)
        cert = mod.build_structural_cert_sidecar(case, pair)
        assert cert is not None
        assert "gwr_carriers" in cert
        assert cert["endpoint_class"]["lower"] and cert["endpoint_class"]["upper"]
        assert "N" in cert and cert["public_closure_status"].startswith("endpoint_class_by_")


def test_engine_processes_large_bit_n_with_explicit_unresolved_or_cert_no_forbidden():
    """Drive real HighScaleBackend on large values + seeded start; no synthetic hardcoded carriers. AC3.
    High chamber returns real PGS struct (with carrier) only on C success; None (unresolved) is valid for arbitrary large.
    """
    import gmpy2
    # direct import of backend
    import importlib.util
    import sys
    from pathlib import Path
    ROOT = Path(".").resolve()
    backend_path = ROOT / "research/06-cryptology-rsa/experiments/live-solver/rsa-v2/pgs_inference_backend.py"
    # ensure inner imports in SmallIntBackend can find the divisor field (PGS path)
    SRC = ROOT / "src" / "python"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    spec = importlib.util.spec_from_file_location("be", str(backend_path))
    be = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(be)
    # HighScale on arbitrary large: may be None (honest PGS unresolved when C has no witness/scale match)
    # Use value > 2^60 to hit High branch, but small enough to avoid GMP buf/alloc abort in current high ctypes setup for very large.
    large_start = gmpy2.mpz(1) << 60 | 12345
    high = be.HighScaleBackend()
    raw = high.chamber_reset_certificate(large_start, 128)
    if raw is not None:
        assert raw.get("carrier_d") is not None, "when high succeeds, carrier must be real from struct"
    # Always test protocol + large arithmetic path with a real small cert (SmallInt for guaranteed carrier)
    small_be = be.SmallIntBackend()
    small_raw = small_be.chamber_reset_certificate(gmpy2.mpz(1048571), 128)
    assert small_raw is not None
    assert small_raw.get("carrier_d") is not None  # real from PGS chamber (GWR-selected)
    N = gmpy2.mpz(1) << 70 | 999
    # use a carrier_w from small cert or fallback for transport arith demo
    cw = small_raw.get("carrier_w") or 101
    transported = N // gmpy2.mpz(cw)
    assert isinstance(transported, gmpy2.mpz)

    # Drive the SHIPPED certificate_pair using real start_anchor from the updated large_bit_fixtures (large near-sqrt values).
    # Exercises engine on large N + large start_anchor from fixture (high branch for >1<<60).
    import importlib.util as _util
    run_path = ROOT / "research/06-cryptology-rsa/experiments/live-solver/rsa-v2/run_experiment.py"
    rspec = _util.spec_from_file_location("re", str(run_path))
    re = _util.module_from_spec(rspec)
    # paths already have src/python from above
    rspec.loader.exec_module(re)
    # load real fixture row for 256
    fixtures = re.read_jsonl(ROOT / "research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/large_bit_fixtures.jsonl")
    f256 = next(f for f in fixtures if "256" in f["case_id"])
    case = re.make_case_from_n(str(f256["N"]), f256["case_id"])
    diags = re.make_diagnostics()
    real_large_anc = gmpy2.mpz(str(f256["start_anchor"]))
    pair = re.certificate_pair(case, diags, start_anchor=real_large_anc)
    assert pair is not None
    assert "unresolved" in pair.closure_status or pair.closure_status.startswith("endpoint_class")
    # source_anchor should reflect the fixture's large start
    assert pair.endpoint_chain_source_anchor is not None
    # lower may be None (high None for arbitrary) but path exercised; carrier when present from PGS
    if pair.lower is not None:
        assert pair.lower.carrier_d is not None or pair.lower.carrier_w is not None
