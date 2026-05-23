#!/usr/bin/env python3
"""
PGA Grammar Pruner Scaling Ladder

Measures how much of the 198-word factor-neighborhood hypothesis space the
current public grammar rules remove at increasing bit lengths.

Modes:
- synthetic: deterministic motif sequence from the frozen observed motif mix.
- real: deterministic public semiprime sequence, live public motif derivation,
  explicit derivation statuses.

No hidden randomness, no synthetic substitution in real mode, and no private
factor information.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gmpy2

from pga_grammar_pruner import REFERENCE_FACTOR_SPACE, prune_factor_space

try:
    from public_motif_derivation import (
        DERIVATION_BACKEND,
        PublicMotifBackendError,
        PublicMotifUnresolved,
        derive_public_motif,
        get_last_derivation_diagnostics,
    )
except Exception as exc:
    DERIVATION_BACKEND = {
        "name": "public_motif_derivation_import_failed",
        "kind": "import_error",
        "classification": "classical_assisted_backend",
        "scale_capable": False,
        "pgs_native": False,
        "classical_assisted": True,
    }
    PublicMotifBackendError = None  # type: ignore[assignment]
    PublicMotifUnresolved = None  # type: ignore[assignment]
    derive_public_motif = None  # type: ignore[assignment]
    get_last_derivation_diagnostics = lambda: {}  # type: ignore[assignment]
    DERIVATION_IMPORT_ERROR = exc
else:
    DERIVATION_IMPORT_ERROR = None


DEFAULT_BIT_LENGTHS = [24, 28, 32, 36, 40, 44, 48]
DEFAULT_SAMPLES_PER_LEVEL = 30
STRICT_SCALE_BIT_THRESHOLD = 256

SYNTHETIC_MOTIF_COUNTS: tuple[tuple[str, int], ...] = (
    ("o2_d4_a2_d4_odd@mid", 55),
    ("o2_d4_a2_d4_odd@early", 12),
    ("o4_d4_a4_d4_odd@mid", 18),
    ("o6_d4_a6_d4_odd@mid", 8),
    ("o2_d4_a2_d4_odd@mid + o4_d4_odd prev", 4),
    ("o4_d4_a4_d4_odd@mid + o2_d4_odd prev", 3),
)

SYNTHETIC_MOTIF_SEQUENCE: tuple[str, ...] = tuple(
    motif for motif, count in SYNTHETIC_MOTIF_COUNTS for _ in range(count)
)


def synthetic_motif(bits: int, sample_index: int) -> str:
    """Return a deterministic motif from the frozen observed mix."""
    offset = (bits * 17) % len(SYNTHETIC_MOTIF_SEQUENCE)
    return SYNTHETIC_MOTIF_SEQUENCE[(offset + sample_index) % len(SYNTHETIC_MOTIF_SEQUENCE)]


def deterministic_public_semiprime_n(bits: int, sample_index: int) -> int:
    """
    Return a deterministic public semiprime N = p * q at the requested bit length.

    p and q are constructed deterministically from (bits, sample_index) using
    gmpy2.next_prime. This function is used **only** for fixture construction
    of the test corpus. The p and q values are never returned to the caller,
    never recorded in the output artifacts, and never used by
    derive_public_motif or prune_factor_space.

    The measured path remains strictly:
        N -> derive_public_motif(N) -> prune_factor_space(motif)
    """
    if bits < 4:
        raise ValueError("bit length must be at least 4")

    p_bits = bits // 2
    q_bits = bits - p_bits

    p = _deterministic_prime_in_upper_quarter(p_bits, sample_index, salt=17)
    q = _deterministic_prime_in_upper_quarter(q_bits, sample_index, salt=31)
    if p == q:
        q = _deterministic_prime_in_upper_quarter(q_bits, sample_index, salt=47)

    n_value = int(p * q)
    if n_value.bit_length() != bits:
        raise RuntimeError(
            "deterministic fixture construction failed exact bit-length contract: "
            f"target_bits={bits}, actual_bit_length={n_value.bit_length()}"
        )

    return n_value


def _deterministic_prime_in_upper_quarter(bit_count: int, sample_index: int, salt: int) -> gmpy2.mpz:
    """Return a deterministic prime with exactly bit_count bits."""
    if bit_count < 2:
        raise ValueError("prime bit length must be at least 2")
    if bit_count == 2:
        return gmpy2.mpz(3)

    upper = gmpy2.mpz(1) << bit_count
    floor = (gmpy2.mpz(3) * upper) >> 2
    window = upper - floor
    offset = ((sample_index + 1) * (salt * 104729)) % int(window)
    base = floor + offset
    if base % 2 == 0:
        base += 1

    candidate = gmpy2.next_prime(base)
    if candidate < upper:
        return candidate

    candidate = gmpy2.next_prime(floor | 1)
    if candidate < upper:
        return candidate

    raise RuntimeError(f"no deterministic {bit_count}-bit fixture prime found")


def backend_is_scale_capable() -> bool:
    return DERIVATION_BACKEND.get("scale_capable") is True


def scale_backend_block_reason() -> str | None:
    if backend_is_scale_capable():
        return None
    name = DERIVATION_BACKEND.get("name", "unknown")
    kind = DERIVATION_BACKEND.get("kind", "unknown")
    return (
        "scale_backend_unavailable: backend does not declare measured 256+ "
        f"capability (name={name}, kind={kind}, "
        f"classification={DERIVATION_BACKEND.get('classification')}, "
        f"scale_capable={DERIVATION_BACKEND.get('scale_capable')}, "
        f"pgs_native={DERIVATION_BACKEND.get('pgs_native')}, "
        f"classical_assisted={DERIVATION_BACKEND.get('classical_assisted')})"
    )


def real_motif(bits: int, sample_index: int, require_scale_backend: bool = False) -> dict[str, Any]:
    """Derive a motif from a deterministic public semiprime, with exact status."""
    n_value = deterministic_public_semiprime_n(bits, sample_index)
    if require_scale_backend:
        block_reason = scale_backend_block_reason()
        if block_reason is not None:
            return {
                "motif": None,
                "n_value": n_value,
                "status": "derivation_blocked",
                "error": block_reason,
                "diagnostic_tag": "scale_backend_unavailable",
                "derivation_diagnostics": None,
            }
    if derive_public_motif is None:
        return {
            "motif": None,
            "n_value": n_value,
            "status": "derivation_blocked",
            "error": f"public_motif_derivation import failed: {DERIVATION_IMPORT_ERROR}",
            "diagnostic_tag": "motif_derivation_import_failed",
            "derivation_diagnostics": None,
        }
    try:
        motif = derive_public_motif(n_value)
    except Exception as exc:
        diagnostics = get_last_derivation_diagnostics()
        if PublicMotifBackendError is not None and isinstance(exc, PublicMotifBackendError):
            return {
                "motif": None,
                "n_value": n_value,
                "status": "backend_error",
                "error": f"{type(exc).__name__}: {exc}",
                "diagnostic_tag": "tier3_classification_backend_error",
                "derivation_diagnostics": diagnostics,
            }
        if PublicMotifUnresolved is not None and isinstance(exc, PublicMotifUnresolved):
            return {
                "motif": None,
                "n_value": n_value,
                "status": "unresolved",
                "error": f"{type(exc).__name__}: {exc}",
                "diagnostic_tag": "motif_derivation_unresolved",
                "derivation_diagnostics": diagnostics,
            }
        return {
            "motif": None,
            "n_value": n_value,
            "status": "backend_error",
            "error": f"{type(exc).__name__}: {exc}",
            "diagnostic_tag": "motif_derivation_backend_error",
            "derivation_diagnostics": diagnostics,
        }
    if motif.startswith("UNRESOLVED:"):
        return {
            "motif": motif,
            "n_value": n_value,
            "status": "unresolved",
            "error": "public motif derivation returned unresolved",
            "diagnostic_tag": "motif_derivation_unresolved",
            "derivation_diagnostics": get_last_derivation_diagnostics(),
        }
    return {
        "motif": motif,
        "n_value": n_value,
        "status": "resolved",
        "error": None,
        "diagnostic_tag": None,
        "derivation_diagnostics": get_last_derivation_diagnostics(),
    }


def motif_for_sample(
    mode: str,
    bits: int,
    sample_index: int,
    require_scale_backend: bool = False,
) -> dict[str, Any]:
    if mode == "synthetic":
        return {
            "motif": synthetic_motif(bits, sample_index),
            "n_value": None,
            "status": "resolved",
            "error": None,
            "diagnostic_tag": None,
            "derivation_diagnostics": None,
        }
    if mode == "real":
        return real_motif(bits, sample_index, require_scale_backend=require_scale_backend)
    raise ValueError(f"unknown mode: {mode}")


def run_ladder(
    bit_lengths: list[int],
    samples_per_level: int,
    mode: str,
    strict_scale: bool = False,
    diagnostic_only: bool = False,
) -> dict[str, Any]:
    results: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "strict_scale": strict_scale,
        "diagnostic_only": diagnostic_only,
        "scale_claim": bool(strict_scale and not diagnostic_only),
        "derivation_backend": DERIVATION_BACKEND,
        "reference_space": REFERENCE_FACTOR_SPACE,
        "samples_per_level": samples_per_level,
        "levels": {},
    }

    for bits in bit_lengths:
        reductions: list[float] = []
        rule_usage: Counter[str] = Counter()
        unresolved_count = 0
        blocked_count = 0
        backend_error_count = 0
        bit_mismatch_count = 0
        unresolved_examples: list[dict[str, Any]] = []
        blocked_examples: list[dict[str, Any]] = []
        backend_error_examples: list[dict[str, Any]] = []
        motif_usage: Counter[str] = Counter()

        per_case: list[dict[str, Any]] = []
        seen_n: set[int] = set()

        for sample_index in range(samples_per_level):
            if mode == "real":
                print(f"Deriving real motif: bits={bits} sample={sample_index}", flush=True)
            motif_result = motif_for_sample(
                mode,
                bits,
                sample_index,
                require_scale_backend=strict_scale and bits >= STRICT_SCALE_BIT_THRESHOLD,
            )
            motif = motif_result["motif"]
            n_value = motif_result["n_value"]
            derivation_status = str(motif_result["status"])
            error = motif_result["error"]

            if mode == "real":
                if n_value in seen_n:
                    raise RuntimeError(
                        f"Duplicate N generated for bit length {bits}, sample_index {sample_index}. "
                        "Fixture construction must produce distinct public semiprimes."
                )
                seen_n.add(n_value)
                print(
                    f"  N={n_value} status={derivation_status} motif={motif or '-'} error={error or '-'}",
                    flush=True,
                )

            backend_error = derivation_status == "backend_error"
            blocked = derivation_status == "derivation_blocked"
            derivation_unresolved = derivation_status == "unresolved"
            if backend_error:
                res = {
                    "rules_fired": [],
                    "pruned": None,
                    "remaining": None,
                    "reduction_percent": None,
                    "status": "backend_error",
                }
                reduction_percent = None
                unresolved = False
                coverage_gap = False
                diagnostic_tag = motif_result["diagnostic_tag"]
                motif_key = f"BACKEND_ERROR:{n_value}"
            elif blocked:
                res = {
                    "rules_fired": [],
                    "pruned": None,
                    "remaining": None,
                    "reduction_percent": None,
                    "status": "derivation_blocked",
                }
                reduction_percent = None
                unresolved = False
                coverage_gap = False
                diagnostic_tag = motif_result["diagnostic_tag"]
                motif_key = f"DERIVATION_BLOCKED:{n_value}"
            elif derivation_unresolved:
                res = {
                    "rules_fired": [],
                    "pruned": None,
                    "remaining": None,
                    "reduction_percent": None,
                    "status": "unresolved",
                }
                reduction_percent = None
                unresolved = True
                coverage_gap = False
                diagnostic_tag = motif_result["diagnostic_tag"]
                motif_key = motif or f"UNRESOLVED:{n_value}"
            else:
                res = prune_factor_space(str(motif))
                reduction_percent = round(float(res.get("reduction_percent", 0.0)), 2)
                unresolved = res.get("status") == "unresolved"
                coverage_gap = (not unresolved) and reduction_percent < 20
                diagnostic_tag = None
                if unresolved:
                    diagnostic_tag = "grammar_pruning_unresolved"
                elif coverage_gap:
                    diagnostic_tag = "low_reduction_coverage_gap"
                motif_key = str(motif)

            motif_usage[motif_key] += 1

            case_record = {
                "case_id": f"semiprime_{bits}_{sample_index}",
                "bit_length": bits,
                "target_bits": bits,
                "actual_bit_length": None if n_value is None else int(n_value).bit_length(),
                "N": n_value,
                "motif": motif,
                "derived_motif": motif,
                "motif_source": "derive_public_motif(N_only)" if mode == "real" else "synthetic_motif_sequence",
                "construction_method": "deterministic_public_semiprime" if mode == "real" else "synthetic_motif_mix",
                "factors_discarded": mode == "real",
                "original_search_space_size": REFERENCE_FACTOR_SPACE,
                "rules_fired": res.get("rules_fired", []),
                "pruned": res.get("pruned", 0),
                "remaining": res.get("remaining", REFERENCE_FACTOR_SPACE),
                "pruned_count": res.get("pruned", 0),
                "reduction_percent": reduction_percent,
                "status": (
                    "backend_error"
                    if backend_error
                    else ("derivation_blocked" if blocked else ("unresolved" if unresolved else "resolved"))
                ),
                "unresolved_flag": unresolved,
                "derivation_blocked_flag": blocked,
                "backend_error_flag": backend_error,
                "actual_bit_length_mismatch": (
                    False if n_value is None else int(n_value).bit_length() != bits
                ),
                "pruning_status": "not_attempted" if backend_error or blocked or derivation_unresolved else "attempted",
                "derivation_error": error,
                "derivation_diagnostics": motif_result.get("derivation_diagnostics"),
                "diagnostic_tag": diagnostic_tag,
                "coverage_gap": coverage_gap,
            }
            per_case.append(case_record)

            if case_record["actual_bit_length_mismatch"]:
                bit_mismatch_count += 1

            if backend_error:
                backend_error_count += 1
                if len(backend_error_examples) < 5:
                    backend_error_examples.append(
                        {
                            "sample_index": sample_index,
                            "N": n_value,
                            "error": error,
                            "diagnostic_tag": diagnostic_tag,
                        }
                    )
                continue

            if blocked:
                blocked_count += 1
                if len(blocked_examples) < 5:
                    blocked_examples.append(
                        {
                            "sample_index": sample_index,
                            "N": n_value,
                            "error": error,
                            "diagnostic_tag": diagnostic_tag,
                        }
                    )
                continue

            if unresolved:
                unresolved_count += 1
                if len(unresolved_examples) < 5:
                    unresolved_examples.append(
                        {
                            "sample_index": sample_index,
                            "N": n_value,
                            "motif": motif,
                            "error": error or res.get("reason", "unresolved"),
                        }
                    )
                continue

            reductions.append(float(res["reduction_percent"]))
            for rid in res["rules_fired"]:
                rule_usage[str(rid)] += 1

        avg = sum(reductions) / len(reductions) if reductions else 0.0
        std = (
            (sum((r - avg) ** 2 for r in reductions) / len(reductions)) ** 0.5
            if len(reductions) > 1
            else 0.0
        )

        level_data = {
            "bit_length": bits,
            "samples": samples_per_level,
            "measured_case_count": len(reductions),
            "average_reduction_percent": round(avg, 2) if reductions else None,
            "std_dev": round(std, 2) if reductions else None,
            "min_reduction": round(min(reductions), 2) if reductions else None,
            "max_reduction": round(max(reductions), 2) if reductions else None,
            "unresolved_count": unresolved_count,
            "derivation_blocked_count": blocked_count,
            "backend_error_count": backend_error_count,
            "actual_bit_length_mismatch_count": bit_mismatch_count,
            "unresolved_examples": unresolved_examples,
            "derivation_blocked_examples": blocked_examples,
            "backend_error_examples": backend_error_examples,
            "top_motifs": motif_usage.most_common(8),
            "top_rules": rule_usage.most_common(8),
            "reduction_distribution": {
                "0-20%": sum(1 for r in reductions if r < 20),
                "20-40%": sum(1 for r in reductions if 20 <= r < 40),
                "40-60%": sum(1 for r in reductions if 40 <= r < 60),
                "60-80%": sum(1 for r in reductions if 60 <= r < 80),
                "80%+": sum(1 for r in reductions if r >= 80),
            },
        }

        if mode == "real":
            level_data["per_case"] = per_case

        results["levels"][str(bits)] = level_data

    if mode == "real":
        all_cases = [
            case
            for level in results["levels"].values()
            for case in level.get("per_case", [])
        ]
        resolved_cases = [case for case in all_cases if not case["unresolved_flag"]]
        resolved_cases = [
            case
            for case in resolved_cases
            if not case.get("derivation_blocked_flag", False)
        ]
        resolved_cases = [
            case
            for case in resolved_cases
            if not case.get("backend_error_flag", False)
        ]
        unresolved_cases = [case for case in all_cases if case["unresolved_flag"]]
        blocked_cases = [
            case
            for case in all_cases
            if case.get("derivation_blocked_flag", False)
        ]
        backend_error_cases = [
            case
            for case in all_cases
            if case.get("backend_error_flag", False)
        ]
        bit_mismatch_cases = [
            case
            for case in all_cases
            if case.get("actual_bit_length_mismatch", False)
        ]
        resolved_reductions = [case["reduction_percent"] for case in resolved_cases]
        measured_cases = [
            case
            for case in all_cases
            if case["reduction_percent"] is not None
        ]
        all_reductions = [case["reduction_percent"] for case in measured_cases]
        top_rules: Counter[str] = Counter()
        motif_breakdown: dict[str, dict[str, Any]] = {}
        coverage_gap_motifs: Counter[str] = Counter()

        for case in all_cases:
            for rule_id in case["rules_fired"]:
                top_rules[str(rule_id)] += 1
            motif_data = motif_breakdown.setdefault(
                case["derived_motif"] or case["status"],
                {"frequency": 0, "reductions": []},
            )
            motif_data["frequency"] += 1
            if case["reduction_percent"] is not None:
                motif_data["reductions"].append(case["reduction_percent"])
            if case["coverage_gap"]:
                coverage_gap_motifs[case["derived_motif"] or case["status"]] += 1

        results["aggregate"] = {
            "total_cases": len(all_cases),
            "resolved_count": len(resolved_cases),
            "unresolved_count": len(unresolved_cases),
            "derivation_blocked_count": len(blocked_cases),
            "backend_error_count": len(backend_error_cases),
            "actual_bit_length_mismatch_count": len(bit_mismatch_cases),
            "measured_case_count": len(measured_cases),
            "average_reduction_over_measured_cases": round(
                sum(all_reductions) / len(all_reductions), 2
            )
            if all_reductions
            else None,
            "average_reduction_over_all_cases": round(
                sum(all_reductions) / len(all_reductions), 2
            )
            if all_reductions and len(measured_cases) == len(all_cases)
            else None,
            "average_reduction_over_resolved_cases_only": round(
                sum(resolved_reductions) / len(resolved_reductions), 2
            )
            if resolved_reductions
            else None,
            "min_reduction": round(min(all_reductions), 2) if all_reductions else None,
            "max_reduction": round(max(all_reductions), 2) if all_reductions else None,
            "top_rules": top_rules.most_common(5),
            "coverage_gap_motifs": coverage_gap_motifs.most_common(),
            "motif_breakdown": {
                motif: {
                    "frequency": data["frequency"],
                    "average_reduction": round(
                        sum(data["reductions"]) / len(data["reductions"]), 2
                    )
                    if data["reductions"]
                    else None,
                }
                for motif, data in sorted(motif_breakdown.items())
            },
        }

    return results


def strict_scale_failure_reasons(results: dict[str, Any]) -> list[str]:
    """Return strict-scale failure reasons without averaging blocked work."""
    if not results.get("strict_scale"):
        return []

    reasons: list[str] = []
    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        if int(bits) < STRICT_SCALE_BIT_THRESHOLD:
            continue
        if data.get("measured_case_count") != data.get("samples"):
            reasons.append(
                f"{bits}: measured_case_count={data.get('measured_case_count')} "
                f"of {data.get('samples')}"
            )
        if data.get("unresolved_count", 0):
            reasons.append(f"{bits}: unresolved_count={data['unresolved_count']}")
        if data.get("derivation_blocked_count", 0):
            reasons.append(f"{bits}: derivation_blocked_count={data['derivation_blocked_count']}")
        if data.get("backend_error_count", 0):
            reasons.append(f"{bits}: backend_error_count={data['backend_error_count']}")
        if data.get("actual_bit_length_mismatch_count", 0):
            reasons.append(
                f"{bits}: actual_bit_length_mismatch_count={data['actual_bit_length_mismatch_count']}"
            )
    return reasons


def has_backend_error(results: dict[str, Any]) -> bool:
    return any(data.get("backend_error_count", 0) > 0 for data in results["levels"].values())


def as_diagnostic_results(results: dict[str, Any], diagnostic_reason: str) -> dict[str, Any]:
    """Return a report copy that cannot be mistaken for a reduction surface."""
    diagnostic = copy.deepcopy(results)
    diagnostic["artifact_type"] = "diagnostic"
    diagnostic["not_reduction_surface"] = True
    diagnostic["scale_claim"] = False
    diagnostic["diagnostic_reason"] = diagnostic_reason

    for level in diagnostic["levels"].values():
        level["average_reduction_percent"] = None
        level["std_dev"] = None
        level["min_reduction"] = None
        level["max_reduction"] = None

    aggregate = diagnostic.get("aggregate")
    if aggregate:
        for key in (
            "average_reduction_over_measured_cases",
            "average_reduction_over_all_cases",
            "average_reduction_over_resolved_cases_only",
            "min_reduction",
            "max_reduction",
        ):
            aggregate[key] = None
        for data in aggregate.get("motif_breakdown", {}).values():
            data["average_reduction"] = None

    return diagnostic


def write_reports(results: dict[str, Any], out_dir: Path, artifact_name: str = "ladder_summary") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{artifact_name}.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    mode = results["mode"]
    diagnostic = bool(results.get("not_reduction_surface"))

    def pct(value: object) -> str:
        return "-" if value is None else f"{float(value):.2f}%"

    def pct1(value: object) -> str:
        return "-" if value is None else f"{float(value):.1f}%"

    md_lines = [
        "# PGA Grammar Pruner Diagnostic" if diagnostic else "# PGA Grammar Pruner Scaling Ladder",
        "",
        f"**Date**: {results['timestamp']}",
        f"**Mode**: `{mode}`",
        f"**Artifact type**: `{results.get('artifact_type', 'ladder_summary')}`",
        f"**Scale claim**: `{results.get('scale_claim', False)}`",
        f"**Reference factor space**: {results['reference_space']} words",
        f"**Samples per level**: {results['samples_per_level']}",
    ]
    if diagnostic:
        md_lines += [
            "",
            "**This artifact is not a reduction surface.**",
            f"**Diagnostic reason**: {results.get('diagnostic_reason', 'unspecified')}",
        ]
    if mode == "real":
        md_lines += [
            "",
            "## Backend",
            "",
            f"- name: `{results['derivation_backend'].get('name')}`",
            f"- kind: `{results['derivation_backend'].get('kind')}`",
            f"- classification: `{results['derivation_backend'].get('classification')}`",
            f"- scale_capable: `{results['derivation_backend'].get('scale_capable')}`",
            f"- pgs_native: `{results['derivation_backend'].get('pgs_native')}`",
            f"- classical_assisted: `{results['derivation_backend'].get('classical_assisted')}`",
        ]
    md_lines += [
        "",
        "## Results by Bit Length",
        "",
        "| Bits | Measured | Avg Reduction | Std Dev | Min | Max | Unresolved | Derivation Blocked | Backend Error | Bit Mismatch |",
        "|------|----------|---------------|---------|-----|-----|------------|--------------------|---------------|--------------|",
    ]

    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        md_lines.append(
            f"| {bits} | {data.get('measured_case_count', data['samples'])}/{data['samples']} | "
            f"{pct(data['average_reduction_percent'])} | {pct(data['std_dev'])} | "
            f"{pct1(data['min_reduction'])} | {pct1(data['max_reduction'])} | "
            f"{data['unresolved_count']} | {data.get('derivation_blocked_count', 0)} | "
            f"{data.get('backend_error_count', 0)} | {data.get('actual_bit_length_mismatch_count', 0)} |"
        )

    md_lines += ["", "## Mode Contract", ""]
    if mode == "synthetic":
        md_lines += [
            "Synthetic mode uses a fixed motif sequence derived from the frozen observed motif mix.",
            "It is deterministic and does not call live public motif derivation.",
        ]
    else:
        md_lines += [
            "Real mode derives motifs from deterministic public semiprimes.",
            "The corpus is constructed using gmpy2.next_prime **only for fixture generation**.",
            "p and q are discarded before any call to derive_public_motif or prune_factor_space.",
            "Implementation-blocked derivations are reported as derivation_blocked, not unresolved.",
            "Backend errors are reported as backend_error and do not contribute to averages.",
            "No synthetic motif is substituted.",
        ]

    # Add per-level top motifs table (makes motif-mix sensitivity explicit)
    md_lines += ["", "## Top Motifs per Level", ""]

    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        md_lines.append(f"**{bits} bits**")
        if data.get("top_motifs"):
            for motif, count in data["top_motifs"]:
                md_lines.append(f"- `{motif}`: {count}")
        else:
            md_lines.append("- (no motif data)")
        md_lines.append("")

    # Per-case detail + summary for real mode (small probes)
    if mode == "real":
        aggregate = results["aggregate"]

        md_lines += ["", "## Summary (Real Derivation)", ""]
        md_lines.append(f"- Total cases: {aggregate['total_cases']}")
        md_lines.append(f"- Measured cases: {aggregate['measured_case_count']}")
        md_lines.append(f"- Resolved cases: {aggregate['resolved_count']}")
        md_lines.append(f"- Unresolved cases: {aggregate['unresolved_count']}")
        md_lines.append(f"- Derivation-blocked cases: {aggregate['derivation_blocked_count']}")
        md_lines.append(f"- Backend-error cases: {aggregate['backend_error_count']}")
        md_lines.append(f"- Actual bit-length mismatches: {aggregate['actual_bit_length_mismatch_count']}")
        if not diagnostic:
            md_lines.append(
                f"- Average reduction (measured cases): {pct(aggregate['average_reduction_over_measured_cases'])}"
            )
            md_lines.append(
                f"- Average reduction (all cases): {pct(aggregate['average_reduction_over_all_cases'])}"
            )
            md_lines.append(
                f"- Average reduction (resolved cases): {pct(aggregate['average_reduction_over_resolved_cases_only'])}"
            )
            md_lines.append(
                f"- Min / Max reduction: {pct(aggregate['min_reduction'])} / {pct(aggregate['max_reduction'])}"
            )
        md_lines.append(
            f"- Motifs with coverage gaps: {len(aggregate['coverage_gap_motifs'])}"
        )

        md_lines += ["", "## Motif Breakdown", ""]
        md_lines.append("| motif | frequency | avg reduction | coverage gap cases |")
        md_lines.append("|-------|-----------|---------------|--------------------|")
        gap_counts = dict(aggregate["coverage_gap_motifs"])
        for motif, data in aggregate["motif_breakdown"].items():
            md_lines.append(
                f"| `{motif}` | {data['frequency']} | {pct(data['average_reduction'])} | "
                f"{gap_counts.get(motif, 0)} |"
            )

        md_lines += ["", "## Top Rules", ""]
        for rule_id, count in aggregate["top_rules"]:
            md_lines.append(f"- {rule_id}: {count}")

        md_lines += ["", "## Per-Case Results (Real Derivation)", ""]
        for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
            per_case = data.get("per_case", [])
            if not per_case:
                continue
            md_lines.append(f"### {bits} bits")
            md_lines.append("")
            md_lines.append("| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |")
            md_lines.append("|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|")
            for case in per_case:
                rules_str = ",".join(case.get("rules_fired", [])) or "-"
                error = case.get("derivation_error") or "-"
                gap = "yes" if case.get("coverage_gap") else "no"
                fd = "yes" if case.get("factors_discarded") else "no"
                pruned = "-" if case.get("pruned") is None else str(case["pruned"])
                remaining = "-" if case.get("remaining") is None else str(case["remaining"])
                md_lines.append(
                    f"| {case['case_id']} | {case['target_bits']} | {case.get('actual_bit_length', '-')} | "
                    f"{case['N']} | `{case['motif'] or '-'}` | {case.get('motif_source','')} | "
                    f"{fd} | {case.get('pruning_status', 'attempted')} | {rules_str} | {pruned} | {remaining} | "
                    f"{pct(case['reduction_percent'])} | {case['status']} | {gap} | {error} |"
                )
            md_lines.append("")

    md_lines += [
        "## Interpretation",
        "",
        "This ladder measures grammar-rule reduction after a public motif is available.",
        "Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures",
        "the live raw-N public derivation path plus rule coverage.",
    ]

    (out_dir / f"{artifact_name}.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Ladder results written to: {out_dir}")


def parse_levels(levels: str) -> list[int]:
    parsed = [int(x.strip()) for x in levels.split(",") if x.strip()]
    if not parsed:
        raise ValueError("at least one bit length is required")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description="PGA Grammar Pruner Scaling Ladder")
    parser.add_argument(
        "--levels",
        type=str,
        default=",".join(map(str, DEFAULT_BIT_LENGTHS)),
        help="Comma-separated bit lengths, for example 32,40,48",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES_PER_LEVEL,
        help="Number of deterministic samples per bit length",
    )
    parser.add_argument(
        "--mode",
        choices=("synthetic", "real"),
        default="synthetic",
        help="synthetic uses fixed motifs; real derives motifs from deterministic public semiprimes",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="Explicit output directory. If omitted, a mode-derived path is used (e.g. output/ladder/synthetic_48_80_samples_30/).",
    )
    parser.add_argument(
        "--diagnostic-only",
        action="store_true",
        help=(
            "Write diagnostic artifacts only. For real runs at 256+ bits this permits "
            "blocked rows while making no reduction-surface claim."
        ),
    )
    args = parser.parse_args()

    bit_lengths = parse_levels(args.levels)
    strict_scale = (
        args.mode == "real"
        and any(bits >= STRICT_SCALE_BIT_THRESHOLD for bits in bit_lengths)
    )

    print("=== PGA Grammar Pruner Scaling Ladder ===")
    print(f"Mode: {args.mode}")
    print(f"Bit lengths: {bit_lengths}")
    print(f"Samples per level: {args.samples}")
    print(f"Strict scale mode: {strict_scale}")
    print(f"Diagnostic only: {args.diagnostic_only}")
    if args.mode == "real":
        print(f"Derivation backend: {DERIVATION_BACKEND}")
    print()

    results = run_ladder(
        bit_lengths,
        args.samples,
        mode=args.mode,
        strict_scale=strict_scale,
        diagnostic_only=args.diagnostic_only,
    )
    strict_failures = strict_scale_failure_reasons(results)
    backend_error = has_backend_error(results)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if args.out_dir:
        out_dir = Path(args.out_dir)
    elif args.diagnostic_only:
        out_dir = (
            Path(__file__).resolve().parent
            / "output"
            / "ladder"
            / f"diagnostic_real_run_{timestamp}"
        )
    elif strict_failures:
        out_dir = (
            Path(__file__).resolve().parent
            / "output"
            / "ladder"
            / f"failed_real_scale_run_{timestamp}"
        )
    else:
        min_b = min(bit_lengths)
        max_b = max(bit_lengths)
        prefix = "real_semiprime" if args.mode == "real" else args.mode
        out_dir = (
            Path(__file__).resolve().parent
            / "output"
            / "ladder"
            / f"{prefix}_{min_b}_{max_b}_samples_{args.samples}"
        )

    if args.diagnostic_only:
        reason = "diagnostic_only_requested"
        report_results = as_diagnostic_results(results, reason)
        artifact_name = "diagnostic"
    elif strict_failures:
        reason = "strict_scale_failed: " + "; ".join(strict_failures)
        report_results = as_diagnostic_results(results, reason)
        artifact_name = "diagnostic"
    else:
        report_results = results
        artifact_name = "ladder_summary"

    write_reports(report_results, out_dir, artifact_name=artifact_name)

    print("\n=== Ladder Summary ===")
    for bits, data in sorted(report_results["levels"].items(), key=lambda x: int(x[0])):
        avg = "-" if data["average_reduction_percent"] is None else f"{data['average_reduction_percent']:6.2f}%"
        std = "-" if data["std_dev"] is None else f"+/-{data['std_dev']:.1f}%"
        min_r = "-" if data["min_reduction"] is None else f"{data['min_reduction']:.0f}%"
        max_r = "-" if data["max_reduction"] is None else f"{data['max_reduction']:.0f}%"
        print(
            f"{bits:>3} bits : {avg} avg "
            f"({std}) "
            f"[{min_r} to {max_r}] "
            f"measured={data.get('measured_case_count', data['samples'])}/{data['samples']} "
            f"unresolved={data['unresolved_count']} "
            f"blocked={data.get('derivation_blocked_count', 0)}"
        )

    print(f"\nDetailed reports: {out_dir / (artifact_name + '.md')}")
    if strict_failures and not args.diagnostic_only:
        print("Strict scale run failed:")
        for failure in strict_failures:
            print(f"  - {failure}")
        raise SystemExit(1)
    if backend_error:
        print("Backend error occurred; run is not valid.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
