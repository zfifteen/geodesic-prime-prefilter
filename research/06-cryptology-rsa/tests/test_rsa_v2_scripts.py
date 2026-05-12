from __future__ import annotations

import ast
import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"
SCRIPT_NAMES = (
    "build_ladder_fixtures.py",
    "generate_ladder_rung.py",
    "run_experiment.py",
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
TOY_DEADLINE_CASE_ID = "rsa_v2_toy_deadline_17bit_static_001"
TOY_DEADLINE_N = "73903"
TOY_DEADLINE_P = "263"
TOY_DEADLINE_Q = "281"


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


def test_runner_reports_certificate_pairs_without_false_resolution(tmp_path):
    """As a reviewer, I want the runner to resolve only public certificate closures."""
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
            "unresolved_reason": "unresolved_by_certificate_pair_not_closed",
            "rule_id": RULE_ID,
        }
    ]
    assert summary["cases"][0]["closure_status"] == (
        "resolved_by_reciprocal_deadline_signature_correction"
    )
    assert summary["cases"][0]["corrected_lower_certificate_present"]
    assert summary["cases"][1]["closure_status"] == "unresolved_by_certificate_pair_not_closed"
    assert not summary["cases"][1]["corrected_lower_certificate_present"]
    for row in summary["cases"]:
        assert row["lower_certificate_present"]
        assert "radius" not in row
        assert "reciprocal_window_candidates" not in row
        assert "recursive_lock_survivors" not in row
        assert "deadline_lock_pairs" not in row
        assert "max_lower_endpoints" not in row
        assert "lower_pgs_endpoints_seen" not in row
    assert len(survivors) == len(summary["cases"])
    assert survivors[0]["closure_status"] == (
        "resolved_by_reciprocal_deadline_signature_correction"
    )
    assert survivors[0]["corrected_lower_endpoint"] == P_VALUE
    assert survivors[0]["corrected_upper_endpoint"] == Q_VALUE
    assert survivors[0]["transported_corrected_upper_endpoint"] == Q_VALUE
    assert survivors[0]["transported_corrected_lower_endpoint"] == P_VALUE
    assert survivors[0]["corrected_lower_reset_signature"] == survivors[0]["upper_reset_signature"]
    assert survivors[1]["closure_status"] == "unresolved_by_certificate_pair_not_closed"


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
    assert rows[1]["corrected_lower_endpoint"] is None


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
            "status": "resolved",
            "p": TOY_DEADLINE_P,
            "q": TOY_DEADLINE_Q,
            "rule_id": RULE_ID,
        }
    ]
    assert summary["cases"][0]["closure_status"] == (
        "resolved_by_reciprocal_deadline_signature_correction"
    )
    assert survivors[0]["corrected_lower_endpoint"] == TOY_DEADLINE_P
    assert survivors[0]["corrected_upper_endpoint"] == TOY_DEADLINE_Q
    assert survivors[0]["transported_corrected_upper_endpoint"] == TOY_DEADLINE_Q
    assert survivors[0]["transported_corrected_lower_endpoint"] == TOY_DEADLINE_P
    assert survivors[0]["corrected_lower_reset_signature"] == survivors[0]["upper_reset_signature"]


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
        "max_lower_endpoints",
        "max-lower-endpoints",
        "CHAMBER_RADIUS",
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


def test_runner_declares_small_regime_interval_backend_boundary():
    """As a reviewer, I want the current interval backend boundary explicit."""
    module = load_module(V2 / "run_experiment.py")

    assert module.SMALL_REGIME_MAX_BITS == 50
    assert module.case_supported_by_interval_backend(
        module.LadderCase("small", 50, module.gmpy2.mpz(1))
    )
    assert not module.case_supported_by_interval_backend(
        module.LadderCase("large", 100, module.gmpy2.mpz(1))
    )


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
    assert summary["row_count"] == 8
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
    assert summary["public_case_count"] == 2
    assert summary["target_side_row_count"] == 4
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
    assert summary["frontier_live_but_closed"] == 1
    assert summary["terminal_without_named_public_invariant"] == 0
    assert summary["certificate_status_after_partition"] == {
        "sidecar_blocked_by_live_normalized_frontier": 2
    }
    assert {row["case_id"] for row in sweep_rows} == {CASE_ID, CASE_50_ID}
    by_case = {row["case_id"]: row for row in sweep_rows}
    assert by_case[CASE_ID]["certificate_status_before"] == "resolved"
    assert by_case[CASE_ID]["frontier_live_but_closed"]
    assert by_case[CASE_50_ID]["certificate_status_before"] == (
        "unresolved_by_certificate_pair_not_closed"
    )
    assert not by_case[CASE_50_ID]["frontier_live_but_closed"]
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
