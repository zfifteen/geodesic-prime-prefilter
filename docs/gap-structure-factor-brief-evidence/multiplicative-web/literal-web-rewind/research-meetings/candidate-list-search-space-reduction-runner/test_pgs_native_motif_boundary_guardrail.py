#!/usr/bin/env python3
"""Guardrail for the live PGS-native motif derivation boundary."""

from __future__ import annotations

import ast
import inspect

import pga_grammar_pruner_ladder as ladder
import public_motif_derivation as pmd


FORBIDDEN_NAMES = {
    "is_prime",
    "isprime",
    "next_prime",
    "nextprime",
    "prevprime",
    "factorint",
    "gcd",
    "miller_rabin",
    "ecpp",
    "_prime_table",
    "_neighboring_gaps_gmp",
    "_gap_grammar_gmp",
    "_divisor_count_gmp",
}


def called_names(function: object) -> set[str]:
    source = inspect.getsource(function)
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name):
            names.add(func.id)
        elif isinstance(func, ast.Attribute):
            names.add(func.attr)
    return names


def modulo_operator_count(function: object) -> int:
    source = inspect.getsource(function)
    tree = ast.parse(source)
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod))


def test_backend_metadata_is_blocked_pgs_native() -> None:
    backend = pmd.DERIVATION_BACKEND
    assert backend["name"] == "pgs_native_motif_derivation_unavailable"
    assert backend["pgs_native"] is True
    assert backend["classical_assisted"] is False
    assert backend["scale_capable"] is False
    assert backend["motif_certificate_available"] is False


def test_toy_lookup_still_works() -> None:
    assert pmd.derive_public_motif(989) == "o2_d4_a2_d4_odd@mid"


def test_non_toy_live_derivation_blocks() -> None:
    try:
        pmd.derive_public_motif(15)
    except pmd.PublicMotifDerivationBlocked as exc:
        assert "pgs_native_motif_certificate_unavailable" in str(exc)
        return
    raise AssertionError("non-toy live derivation must block without a PGS-native certificate")


def test_live_derivation_entrypoint_uses_no_forbidden_decision_mechanism() -> None:
    forbidden = called_names(pmd.derive_public_motif) & FORBIDDEN_NAMES
    assert forbidden == set(), f"forbidden live derivation calls: {sorted(forbidden)}"
    assert modulo_operator_count(pmd.derive_public_motif) == 0


def test_real_mode_blocks_before_fixture_construction() -> None:
    original = ladder.deterministic_public_semiprime_n

    def forbidden_fixture_construction(_bits: int, _sample_index: int) -> int:
        raise AssertionError("fixture construction must not run while live PGS motif derivation is blocked")

    ladder.deterministic_public_semiprime_n = forbidden_fixture_construction
    try:
        row = ladder.real_motif(64, 0)
    finally:
        ladder.deterministic_public_semiprime_n = original

    assert row["status"] == "derivation_blocked"
    assert row["n_value"] is None
    assert row["diagnostic_tag"] == "pgs_native_motif_certificate_unavailable"
    assert row["fixture_constructed"] is False


def main() -> None:
    test_backend_metadata_is_blocked_pgs_native()
    test_toy_lookup_still_works()
    test_non_toy_live_derivation_blocks()
    test_live_derivation_entrypoint_uses_no_forbidden_decision_mechanism()
    test_real_mode_blocks_before_fixture_construction()
    print("PGS-native motif boundary guardrail passed")


if __name__ == "__main__":
    main()
