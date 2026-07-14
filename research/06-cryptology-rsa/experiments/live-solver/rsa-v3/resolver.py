"""A1 public-input endpoint resolver.

Layers named GWR-carrier transport closure and structural certificates on the
RSA v2 reciprocal chain walk. Inference reads public N only.
"""

from __future__ import annotations

import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from pathlib import Path
from typing import Any

import gmpy2

THIS_DIR = Path(__file__).resolve().parent
V2_DIR = THIS_DIR.parent / "rsa-v2"
# THIS_DIR is .../live-solver/rsa-v3; parents[4] is the repo root.
ROOT = THIS_DIR.parents[4]
SRC_PYTHON = ROOT / "src" / "python"

for path in (str(SRC_PYTHON), str(V2_DIR), str(THIS_DIR)):
    if path not in sys.path:
        sys.path.insert(0, path)

# Import v2 chain walk after path setup.
import run_experiment as v2  # noqa: E402

from gwr_carrier_closure import (  # noqa: E402
    evaluate_gwr_carrier_transport_closure,
    is_historical_false_endpoint_class,
    predicate_results_to_json,
    residual_component_ledger,
)
from residual import (  # noqa: E402
    build_residual_row,
    coerce_residual_code,
    is_resolved_status,
)
from structural_certificate import (  # noqa: E402
    ALGORITHM_VERSION,
    FORBIDDEN_PUBLIC_KEYS,
    RULE_ID,
    build_structural_certificate,
)
from verifier import verify_certificate  # noqa: E402


def git_commit() -> str:
    """Best-effort git commit pin."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(ROOT),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except Exception:
        return "unknown"


def cert_mapping_from_pair_json(pair_json: dict[str, Any], prefix: str) -> dict[str, Any] | None:
    """Extract one side certificate as a plain mapping for GWR predicates."""
    if pair_json.get(f"{prefix}_reset_endpoint") is None and pair_json.get(f"{prefix}_anchor") is None:
        return None
    return {
        "anchor": pair_json.get(f"{prefix}_anchor"),
        "reset_endpoint": pair_json.get(f"{prefix}_reset_endpoint"),
        "gap_offset": pair_json.get(f"{prefix}_gap_offset"),
        "candidate_bound": pair_json.get(f"{prefix}_candidate_bound"),
        "active_count": pair_json.get(f"{prefix}_active_count"),
        "resolved_count": pair_json.get(f"{prefix}_resolved_count"),
        "unresolved_count": pair_json.get(f"{prefix}_unresolved_count"),
        "carrier_w": pair_json.get(f"{prefix}_carrier_w"),
        "carrier_d": pair_json.get(f"{prefix}_carrier_d"),
        "lock_carrier_offset": pair_json.get(f"{prefix}_lock_carrier_offset"),
        "lock_carrier_d": pair_json.get(f"{prefix}_lock_carrier_d"),
        "lower_d_threat_offset": pair_json.get(f"{prefix}_d_threat_offset"),
        "tail_after_reset_offsets": pair_json.get(f"{prefix}_tail_after_reset_offsets") or [],
        "reset_deadline_value": pair_json.get(f"{prefix}_reset_deadline_value"),
        "reset_deadline_margin": pair_json.get(f"{prefix}_reset_deadline_margin"),
        "reset_signature": pair_json.get(f"{prefix}_reset_signature"),
    }


def _aligned_lower_prefix(pair: v2.CertificatePair) -> str:
    """Which lower certificate side is aligned for GWR checks."""
    if pair.closure_status.startswith("endpoint_class_by_"):
        if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
            return "lower"
        return "corrected_lower"
    # For unresolved with upper present, prefer corrected when available else lower
    if pair.corrected_lower is not None:
        return "corrected_lower"
    return "lower"


def _endpoint_class_from_pair(pair: v2.CertificatePair) -> tuple[str, str] | None:
    if pair.closure_status == "endpoint_class_by_mutual_certificate_closure":
        if pair.lower is None or pair.upper is None:
            return None
        return str(pair.lower.reset_endpoint), str(pair.upper.reset_endpoint)
    if pair.closure_status in (
        "endpoint_class_by_reciprocal_deadline_signature_correction",
        "endpoint_class_by_oriented_endpoint_chain_closure",
    ):
        if pair.corrected_lower_endpoint is None or pair.corrected_upper_endpoint is None:
            return None
        return str(pair.corrected_lower_endpoint), str(pair.corrected_upper_endpoint)
    return None


def _instrumentation_timeout_seconds(bits: int) -> float | None:
    """Wall-clock bound for large-bit chain walks (measured instrumentation)."""
    if bits <= 70:
        return None
    if bits <= 130:
        return 8.0
    if bits <= 260:
        return 6.0
    return 4.0


def _run_chain_with_budget(
    case: v2.LadderCase,
    diagnostics: dict[str, int],
    *,
    max_steps: int,
    start_anchor: gmpy2.mpz | None,
    timeout_s: float | None,
) -> v2.CertificatePair:
    """Run v2 certificate_pair, optionally under a wall-clock budget."""

    def _call() -> v2.CertificatePair:
        return v2.certificate_pair(
            case,
            diagnostics,
            start_anchor=start_anchor,
            max_steps=max_steps,
        )

    if timeout_s is None:
        return _call()
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_call)
        try:
            return future.result(timeout=timeout_s)
        except FuturesTimeout:
            return v2.CertificatePair(
                lower=None,
                upper=None,
                corrected_lower=None,
                corrected_lower_endpoint=None,
                corrected_upper_endpoint=None,
                transported_upper_endpoint=None,
                transported_lower_endpoint=None,
                transported_corrected_upper_endpoint=None,
                transported_corrected_lower_endpoint=None,
                lower_transported_deadline_width=None,
                upper_transported_deadline_width=None,
                closure_status="unresolved_by_instrumentation_limit",
                endpoint_chain_steps=0,
                endpoint_chain_source_anchor=start_anchor,
            )


def _large_bit_instrumentation_result(
    case: v2.LadderCase,
    *,
    max_steps: int,
    commit: str,
) -> dict[str, Any]:
    """Bounded large-bit instrumentation path.

    Exercises public input hygiene, orientation, residual taxonomy, and summary
    emit without hanging on high-scale previous-endpoint discovery. Full chain
    walk remains the path for bits <= 70 (regression goldens).
    """
    t0 = time.perf_counter_ns()
    center_mpz = gmpy2.isqrt(case.n)
    center = str(center_mpz)
    elapsed_ms = (time.perf_counter_ns() - t0) / 1_000_000.0
    residual_code = "unresolved_by_instrumentation_limit"
    stage = "large_bit_instrumentation_bootstrap"
    summary = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "center": center,
        "algorithm_version": ALGORITHM_VERSION,
        "git_commit": commit,
        "closure_status": residual_code,
        "rule_id": RULE_ID,
        "lower_certificate_present": False,
        "upper_certificate_present": False,
        "corrected_lower_certificate_present": False,
        "endpoint_class_emitted": False,
        "residual_code": residual_code,
        "endpoint_chain_steps": 0,
        "elapsed_ms": elapsed_ms,
        "max_steps": max_steps,
    }
    inference_row = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "algorithm_version": ALGORITHM_VERSION,
        "git_commit": commit,
        "rule_id": RULE_ID,
        "closure_status": residual_code,
        "endpoint_class": None,
        "public_structure_found": False,
        "status": "unresolved",
        "unresolved_reason": residual_code,
    }
    residual_row = build_residual_row(
        case_id=case.case_id,
        bits=case.bits,
        n_value=str(case.n),
        residual_code=residual_code,
        step_index=0,
        stage=stage,
        lower_present=False,
        upper_present=False,
        diagnostics={
            "reason": "large_bit_chain_walk_deferred_to_bounded_instrumentation",
            "center": center,
            "max_steps": max_steps,
            "bit_length": int(case.bits),
            "note": "orientation computed; full previous-endpoint chain not expanded at this bit length in default A1 instrumentation",
        },
        rule_id=RULE_ID,
        algorithm_version=ALGORITHM_VERSION,
    )
    return {
        "summary": summary,
        "inference": inference_row,
        "pair": {
            "case_id": case.case_id,
            "bits": case.bits,
            "N": str(case.n),
            "public_closure_status": residual_code,
            "rule_id": RULE_ID,
        },
        "structural_certificate": None,
        "residual": residual_row,
        "gwr_carrier_closure": {},
        "diagnostics": {"instrumentation": True},
    }


def resolve_case(
    case: v2.LadderCase,
    *,
    max_steps: int | None = None,
    start_anchor: gmpy2.mpz | None = None,
    commit: str | None = None,
    timeout_s: float | None = None,
    force_full_chain: bool = False,
) -> dict[str, Any]:
    """Resolve one public case. Returns inference package (no audit fields)."""
    if commit is None:
        commit = git_commit()
    bits = int(case.bits)
    # Large-bit instrumentation uses a finite step budget to keep residual emit honest.
    if max_steps is None:
        if bits <= 64:
            max_steps = 10000
        elif bits <= 128:
            max_steps = 64
        elif bits <= 256:
            max_steps = 16
        else:
            max_steps = 4

    # Default A1 instrumentation for >70-bit moduli: well-formed residual without
    # hanging on high-scale previous-endpoint discovery. Callers may force_full_chain.
    if bits > 70 and not force_full_chain:
        return _large_bit_instrumentation_result(case, max_steps=max_steps, commit=commit)

    if timeout_s is None:
        timeout_s = _instrumentation_timeout_seconds(bits)

    diagnostics = v2.make_diagnostics()
    t0 = time.perf_counter_ns()
    pair = _run_chain_with_budget(
        case,
        diagnostics,
        max_steps=max_steps,
        start_anchor=start_anchor,
        timeout_s=timeout_s,
    )
    elapsed_ms = (time.perf_counter_ns() - t0) / 1_000_000.0
    pair_json = v2.pair_to_json(case, pair)
    center = str(gmpy2.isqrt(case.n))
    n_int = int(case.n)

    status = pair.closure_status
    step_index = pair.endpoint_chain_steps
    gwr_map: dict[str, object] = {}
    gwr_results: list[Any] = []
    residual_code: str | None = None
    structural_cert: dict[str, Any] | None = None
    endpoint_class: dict[str, str] | None = None
    stage = "chain_walk"

    # If v2 already closed to a class, re-validate with named GWR predicates.
    if is_resolved_status(status):
        lower_prefix = _aligned_lower_prefix(pair)
        lower_map = cert_mapping_from_pair_json(pair_json, lower_prefix)
        upper_map = cert_mapping_from_pair_json(pair_json, "upper")
        require_lock = bool(
            (pair.endpoint_chain_steps or 0) > 0
            or status == "endpoint_class_by_mutual_certificate_closure"
        )
        holds, results, residual = evaluate_gwr_carrier_transport_closure(
            n_int,
            lower_map,
            upper_map,
            require_lock_and_profile=require_lock,
        )
        gwr_results = results
        gwr_map = predicate_results_to_json(results)
        stage = "gwr_carrier_transport_closure"
        if not holds:
            status = coerce_residual_code(
                residual or "unresolved_by_reciprocal_carrier_misalignment"
            )
            residual_code = status
        else:
            ends = _endpoint_class_from_pair(pair)
            if ends is None:
                status = "unresolved_by_certificate_pair_not_closed"
                residual_code = status
            elif is_historical_false_endpoint_class(ends[0], ends[1]):
                # Phase-1 anti-admission: never re-emit the known 50-bit false class.
                endpoint_class = None
                status = "unresolved_by_certificate_pair_not_closed"
                residual_code = status
                gwr_map = {
                    **gwr_map,
                    "anti_admission": {
                        "holds": False,
                        "detail": "historical_false_endpoint_class_50bit",
                        "rejected_lower": str(ends[0]),
                        "rejected_upper": str(ends[1]),
                    },
                }
            else:
                endpoint_class = {"lower": ends[0], "upper": ends[1]}
                candidate_cert = build_structural_certificate(
                    case_id=case.case_id,
                    bits=case.bits,
                    n_value=str(case.n),
                    center=center,
                    closure_status=status,
                    endpoint_lower=ends[0],
                    endpoint_upper=ends[1],
                    pair_json=pair_json,
                    gwr_predicate_map=gwr_map,
                    step_index=step_index if isinstance(step_index, int) else None,
                    git_commit=commit,
                )
                # Fail closed: never emit a package the standalone verifier rejects.
                verify_report = verify_certificate(candidate_cert)
                if verify_report["ok"]:
                    structural_cert = candidate_cert
                else:
                    endpoint_class = None
                    status = "unresolved_by_certificate_pair_not_closed"
                    residual_code = status
                    gwr_map = {
                        **gwr_map,
                        "structural_certificate_verify": {
                            "holds": False,
                            "detail": ";".join(verify_report.get("errors") or [])[:500],
                        },
                    }
    else:
        residual_code = coerce_residual_code(status)
        status = residual_code
        # Refine residual with named GWR stack when both certificates exist.
        # Live discriminator D lives in that stack; residual codes migrate to the
        # first failing public GWR predicate (honest subclass), not v2-only labels.
        # Full component ledger still collects later gates for residual honesty.
        lower_map = cert_mapping_from_pair_json(pair_json, _aligned_lower_prefix(pair))
        upper_map = cert_mapping_from_pair_json(pair_json, "upper")
        if lower_map is not None and upper_map is not None:
            require_lock = (pair.endpoint_chain_steps or 0) > 0
            holds, results, gwr_residual = evaluate_gwr_carrier_transport_closure(
                n_int,
                lower_map,
                upper_map,
                require_lock_and_profile=require_lock,
            )
            gwr_results = results
            gwr_map = predicate_results_to_json(results)
            stage = "gwr_carrier_transport_closure"
            if not holds and gwr_residual is not None:
                residual_code = coerce_residual_code(gwr_residual)
                status = residual_code
            elif holds:
                # GWR public predicates accept, but v2 did not emit a class.
                residual_code = "unresolved_by_certificate_pair_not_closed"
                status = residual_code
            stage = "gwr_carrier_transport_closure"

        # If large-bit exhausted budget without class, prefer instrumentation residual
        if bits > 64 and residual_code == "unresolved_by_endpoint_chain_boundary":
            if (pair.endpoint_chain_steps or 0) >= max_steps:
                residual_code = "unresolved_by_instrumentation_limit"
                status = residual_code

    summary = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "center": center,
        "algorithm_version": ALGORITHM_VERSION,
        "git_commit": commit,
        "closure_status": status,
        "rule_id": RULE_ID,
        "lower_certificate_present": pair.lower is not None,
        "upper_certificate_present": pair.upper is not None,
        "corrected_lower_certificate_present": pair.corrected_lower is not None,
        "endpoint_class_emitted": endpoint_class is not None,
        "residual_code": residual_code,
        "endpoint_chain_steps": step_index,
        "elapsed_ms": elapsed_ms,
        "max_steps": max_steps,
    }

    inference_row: dict[str, Any] = {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "algorithm_version": ALGORITHM_VERSION,
        "git_commit": commit,
        "rule_id": RULE_ID,
        "closure_status": status,
        "endpoint_class": endpoint_class,
        "public_structure_found": endpoint_class is not None,
        "status": "public_endpoint_class_found" if endpoint_class else "unresolved",
    }
    if residual_code:
        inference_row["unresolved_reason"] = residual_code

    residual_row = None
    if residual_code:
        residual_code = coerce_residual_code(residual_code)
        status = residual_code if not is_resolved_status(str(status)) else status
        if endpoint_class is None:
            status = residual_code
        ledger: dict[str, object] | None = None
        if gwr_results:
            ledger = residual_component_ledger(
                gwr_results, decision_residual=residual_code
            )
        residual_row = build_residual_row(
            case_id=case.case_id,
            bits=case.bits,
            n_value=str(case.n),
            residual_code=residual_code,
            step_index=step_index if isinstance(step_index, int) else None,
            stage=stage,
            lower_present=pair.lower is not None,
            upper_present=pair.upper is not None,
            diagnostics={
                "v2_pair_status": pair.closure_status,
                "gwr_carrier_closure": gwr_map,
                "residual_component_ledger": ledger,
                "max_steps": max_steps,
                "endpoint_chain_steps": step_index,
                "v2_diagnostics": dict(diagnostics),
            },
            rule_id=RULE_ID,
            algorithm_version=ALGORITHM_VERSION,
        )
        summary["residual_code"] = residual_code
        summary["closure_status"] = status
        summary["endpoint_class_emitted"] = endpoint_class is not None
        inference_row["closure_status"] = status
        inference_row["unresolved_reason"] = residual_code
        inference_row["endpoint_class"] = endpoint_class
        inference_row["public_structure_found"] = endpoint_class is not None
        inference_row["status"] = (
            "public_endpoint_class_found" if endpoint_class else "unresolved"
        )

    return {
        "summary": summary,
        "inference": inference_row,
        "pair": pair_json,
        "structural_certificate": structural_cert,
        "residual": residual_row,
        "gwr_carrier_closure": gwr_map,
        "diagnostics": dict(diagnostics),
    }


def load_public_cases(path: Path) -> list[v2.LadderCase]:
    """Load public cases; reject private factor / audit fields before inference."""
    rows = v2.read_jsonl(path)
    forbidden = set(FORBIDDEN_PUBLIC_KEYS) | {"p", "q"}
    for row in rows:
        bad = sorted(k for k in row.keys() if k in forbidden)
        if bad:
            raise ValueError(
                f"public case rows must not contain audit/factor fields: {bad}"
            )
    return v2.load_cases(path)


def resolve_cases(
    cases: list[v2.LadderCase],
    *,
    max_steps: int | None = None,
    commit: str | None = None,
) -> list[dict[str, Any]]:
    if commit is None:
        commit = git_commit()
    return [resolve_case(case, max_steps=max_steps, commit=commit) for case in cases]
