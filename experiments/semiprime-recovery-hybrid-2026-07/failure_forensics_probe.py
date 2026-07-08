#!/usr/bin/env python3
"""Forensic probe for 127-bit routed-but-not-recovered semiprime cases.

Uses the shipped pgs_geofac_scaleup harness helpers without reimplementing
routing or recovery logic. Writes failure_forensics.json beside this script.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCALEUP_PATH = ROOT / "research" / "06-cryptology-rsa" / "scripts" / "pgs_geofac_scaleup.py"
OUTPUT_JSON = Path(__file__).resolve().parent / "failure_forensics.json"

FAILING_CASE_IDS = (
    "s127_moderate_112",
    "s127_moderate_127",
    "s127_archived_shape_112",
)

PRIME_WALK_BUDGETS = (256, 1024, 4096, 16384)
SEED_BUDGETS = (64, 256, 1024)
RESIDUE_TOP_N = 10

RUNG = 2
SEED = 0
ROUTER_MODE = "audited_family_prior"


def _load_scaleup():
    """Load the committed scale-up harness module."""
    spec = importlib.util.spec_from_file_location("pgs_geofac_scaleup", SCALEUP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load scale-up module from {SCALEUP_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pgs_geofac_scaleup"] = module
    spec.loader.exec_module(module)
    return module


def _case_by_id(module, case_id: str):
    """Return one 127-bit corpus case by case_id."""
    for case in module.CORPUS[127]:
        if case.case_id == case_id:
            return case
    raise KeyError(f"case_id not in CORPUS[127]: {case_id}")


def _best_ranked_window(module, case, windows: list) -> tuple[int, object]:
    """Mirror _evaluate_case window selection for the factor-containing window."""
    factor_log2 = case.small_factor_log2
    for index, window in enumerate(windows, start=1):
        if module._window_contains_factor(window, factor_log2):
            return index, window
    raise RuntimeError(f"no window contains factor for {case.case_id}")


def _prime_walk_hit(module, case, window, budget: int) -> tuple[bool, int]:
    """Run shipped prime-walk recovery on one window."""
    low, high, midpoint = module._window_to_interval(window)
    return module._local_router_only_prime_walk(case, [window], budget)


def _seed_recovery_hit(module, case, low: int, high: int, budget: int) -> tuple[bool, int]:
    """Run shipped seed recovery on one interval."""
    return module._pgs_seed_recovery_in_interval(case, low, high, budget)


def _residue_rank_hit(module, case, low: int, high: int, budget: int) -> tuple[bool, list[int]]:
    """Check whether small_factor appears in top-N residue-ranked recovered primes."""
    ranked = module._recovery_ranked_recovered_primes_in_interval(
        case,
        low,
        high,
        budget,
    )
    top = list(ranked[:RESIDUE_TOP_N])
    return case.small_factor in top, top


def probe_case(module, case_id: str) -> dict[str, object]:
    """Forensic record for one failing case."""
    case = _case_by_id(module, case_id)
    windows, router_probe_count = module._route_case(
        case,
        RUNG,
        SEED,
        router_mode=ROUTER_MODE,
    )
    best_window_rank, window = _best_ranked_window(module, case, windows)
    low, high, midpoint = module._window_to_interval(window)

    prime_walk_sweep: dict[str, bool] = {}
    prime_walk_tests: dict[str, int] = {}
    for budget in PRIME_WALK_BUDGETS:
        hit, tests = _prime_walk_hit(module, case, window, budget)
        prime_walk_sweep[str(budget)] = hit
        prime_walk_tests[str(budget)] = tests

    seed_sweep: dict[str, bool] = {}
    seed_tests: dict[str, int] = {}
    for budget in SEED_BUDGETS:
        hit, tests = _seed_recovery_hit(module, case, low, high, budget)
        seed_sweep[str(budget)] = hit
        seed_tests[str(budget)] = tests

    residue_hit, residue_top = _residue_rank_hit(
        module,
        case,
        low,
        high,
        module.RUNG_CONFIGS[RUNG].local_seed_budget,
    )

    return {
        "case_id": case_id,
        "family": case.family,
        "case_bits": case.case_bits,
        "n": str(case.n),
        "small_factor": str(case.small_factor),
        "small_factor_log2": case.small_factor_log2,
        "factor_in_final_window": True,
        "best_window_rank": best_window_rank,
        "final_window_bits": window.width_bits,
        "router_probe_count": router_probe_count,
        "window": {
            "low": low,
            "high": high,
            "midpoint": midpoint,
            "center_log2": window.center_log2,
        },
        "prime_walk_sweep": prime_walk_sweep,
        "prime_walk_tests": prime_walk_tests,
        "prime_walk_16384_hit": prime_walk_sweep["16384"],
        "seed_recovery_sweep": seed_sweep,
        "seed_recovery_tests": seed_tests,
        "seed_recovery_1024_hit": seed_sweep["1024"],
        "residue_rank_top_n": RESIDUE_TOP_N,
        "residue_rank_budget": module.RUNG_CONFIGS[RUNG].local_seed_budget,
        "residue_rank_top_primes": [str(p) for p in residue_top],
        "residue_rank_contains_factor": residue_hit,
    }


def main() -> int:
    """Run forensic probe and write JSON."""
    module = _load_scaleup()
    records = [probe_case(module, case_id) for case_id in FAILING_CASE_IDS]
    payload = {
        "rung": RUNG,
        "seed": SEED,
        "router_mode": ROUTER_MODE,
        "failing_case_count": len(records),
        "cases": records,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())