"""Tests for PGSMPG baseline stats capture."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
STATS_PATH = (
    ROOT
    / "experiments"
    / "exponents"
    / "validation"
    / "pgs_mersenne_prime_generator_baseline_stats.py"
)


def load_module():
    """Load the baseline stats module."""
    spec = importlib.util.spec_from_file_location(
        "pgs_mersenne_prime_generator_baseline_stats",
        STATS_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load baseline stats module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_value_ceiling_maps_to_exponent_ceiling():
    """The value ceiling should map to the largest possible Mersenne exponent."""
    module = load_module()

    assert module.max_exponent_for_value_ceiling(10**18) == 59
    assert module.max_exponent_for_value_ceiling(2**31 - 1) == 31


def test_small_baseline_stats_include_terminal_scan():
    """Stats capture should include the terminal unresolved scan to the ceiling."""
    module = load_module()
    exponents, transition_rows, tau_rows = module.collect_stats(
        start_exponent=2,
        value_ceiling=2**31 - 1,
        candidate_bound=4096,
    )

    assert exponents == [2, 3, 5, 7, 13, 17, 19, 31]
    assert transition_rows[-1]["p"] == 31
    assert transition_rows[-1]["status"] == "terminal_unresolved"
    assert transition_rows[-1]["q"] == ""
    assert len(tau_rows) == sum(int(row["tau_call_count"]) for row in transition_rows)


def test_baseline_stats_preserve_interleaved_tau_call_roles():
    """Tau call roles should follow actual exponent and pressure execution order."""
    module = load_module()
    _exponents, _transition_rows, tau_rows = module.collect_stats(
        start_exponent=2,
        value_ceiling=2**31 - 1,
        candidate_bound=4096,
    )

    transition_rows = [
        row for row in tau_rows if int(row["transition_p"]) == 7
    ]
    roles = [row["call_role"] for row in transition_rows]
    first_pressure_index = roles.index("residue_return")

    assert "exponent" in roles[first_pressure_index + 1:]
    assert "boundary" not in roles


def test_cli_writes_lf_baseline_outputs(tmp_path):
    """The CLI should write compact LF-terminated baseline artifacts."""
    module = load_module()
    output_dir = tmp_path / "out"

    assert module.main(
        [
            "--value-ceiling",
            str(2**31 - 1),
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    paths = [
        output_dir / "summary.json",
        output_dir / "transition_stats_rows.csv",
        output_dir / "tau_call_rows.csv",
        output_dir / "mersenne_exponents.jsonl",
    ]
    for path in paths:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    transition_rows = list(
        csv.DictReader(
            (output_dir / "transition_stats_rows.csv").open(encoding="utf-8", newline="")
        )
    )
    tau_rows = list(
        csv.DictReader((output_dir / "tau_call_rows.csv").open(encoding="utf-8", newline=""))
    )
    exponent_rows = [
        json.loads(line)
        for line in (output_dir / "mersenne_exponents.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    assert summary["mersenne_exponents"] == [2, 3, 5, 7, 13, 17, 19, 31]
    assert int(transition_rows[-1]["max_exponent"]) == 31
    assert transition_rows[-1]["status"] == "terminal_unresolved"
    assert all("n" not in row for row in tau_rows)
    assert all("value" not in row for row in exponent_rows)
    assert exponent_rows[-1] == {"e": 31, "mersenne_value_bit_length": 31}
