"""Chamber-level GWR → zeta compression helpers (imports src/python API only)."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from z_band_prime_invariant import exact_zero_excess
from z_band_prime_rh_bridge.bridge import (
    divisor_counts_up_to,
    evaluate_partial_sum_bridge,
    normalization_load_coefficients_up_to,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
F18_AUDIT_PATH = (
    REPO_ROOT
    / "research"
    / "18-derived-half-coefficient"
    / "output"
    / "near_maximal_audit_results_40M.json"
)

F18_RATIO_THRESHOLD = 0.65
FIXED_POINT_V = math.e**2 / 2.0


@dataclass(frozen=True)
class ChamberGapReport:
    p: int
    q: int
    w: int | None
    tau_w: int | None
    offset: int | None
    c_bound: int
    offset_ratio: float | None
    excess_budget: float
    load_budget: float
    frac_pos: float | None
    f18_branch: str


@dataclass(frozen=True)
class ChamberDirichletIncrements:
    s: float
    delta_d: float
    delta_b: float
    rho_chamber: float
    global_r: float
    global_r_error: float


def compression_bound_c(q: int) -> int:
    """C(q) = max(64, ceil(0.5 * log(q)^2)) from PROOF.md bounded compression."""
    if q < 2:
        raise ValueError("q must be at least 2")
    return max(64, math.ceil(0.5 * math.log(q) ** 2))


def bridge_load(n: int, tau_n: int) -> float:
    """H(n) = tau(n) * log(n) / 2."""
    if n <= 1:
        return 0.0
    return tau_n * math.log(n) / 2.0


def is_prime_square(n: int) -> bool:
    if n < 0:
        return False
    root = math.isqrt(n)
    return root * root == n


def f18_branch_label(
    w: int | None,
    tau_w: int | None,
    q: int,
    offset: int | None,
) -> str:
    """Classify witness branch for compression exposition (F18-004 lanes)."""
    if w is None or tau_w is None or offset is None:
        return "empty_interior"
    ratio = offset / compression_bound_c(q)
    if tau_w == 3 and is_prime_square(w):
        return "prime_square"
    if ratio >= F18_RATIO_THRESHOLD:
        floor_d = max(6, math.floor(0.75 * math.log(q)))
        if tau_w <= 5:
            return "non_square_low_d_high_ratio"
        if tau_w < floor_d:
            return "non_square_below_rough_floor"
        return "non_square_rough_high_ratio"
    return "non_square_subthreshold"


def analyze_chamber_gap(p: int, q: int) -> ChamberGapReport:
    """Build GWR chamber invariants for consecutive primes (p, q)."""
    if p >= q:
        raise ValueError("require p < q")
    counts = divisor_counts_up_to(q)
    interior = list(range(p + 1, q))
    if not interior:
        return ChamberGapReport(
            p=p,
            q=q,
            w=None,
            tau_w=None,
            offset=None,
            c_bound=compression_bound_c(q),
            offset_ratio=None,
            excess_budget=0.0,
            load_budget=0.0,
            frac_pos=None,
            f18_branch="empty_interior",
        )

    min_tau = min(counts[n] for n in interior)
    w = min(n for n in interior if counts[n] == min_tau)
    tau_w = counts[w]
    offset = w - p
    c_bound = compression_bound_c(q)
    excess_budget = sum(exact_zero_excess(n) for n in interior)
    load_budget = sum(bridge_load(n, counts[n]) for n in interior)
    gap_len = q - p
    frac_pos = offset / (gap_len - 1) if gap_len > 1 else None

    return ChamberGapReport(
        p=p,
        q=q,
        w=w,
        tau_w=tau_w,
        offset=offset,
        c_bound=c_bound,
        offset_ratio=offset / c_bound,
        excess_budget=excess_budget,
        load_budget=load_budget,
        frac_pos=frac_pos,
        f18_branch=f18_branch_label(w, tau_w, q, offset),
    )


def chamber_dirichlet_increments(
    s: float,
    p: int,
    q: int,
    terms: int,
) -> ChamberDirichletIncrements:
    """Compute ΔD, ΔB and local ρ_ch for chamber (p,q) at Re(s)>1.

    Note: rho_chamber is a chamber load ratio (tracks ~0.5 log m). It is not a
    sample of global R(s). Do not treat |rho_chamber - global_r| as spectral
    alignment. See research/19-rh-corpus/FRAME_CONTRACT.md.
    """
    if s <= 1.0:
        raise ValueError("require Re(s) > 1")
    if q > terms:
        raise ValueError("terms must cover q")

    counts = divisor_counts_up_to(terms)
    loads = normalization_load_coefficients_up_to(terms, counts)
    interior = range(p + 1, q)

    delta_d = sum(counts[n] * (n ** -s) for n in interior)
    # B(s) uses H(n)/n^s; normalization_load = H(n)/e^2.
    delta_b = sum(FIXED_POINT_V * loads[n] * (n ** -s) for n in interior)
    rho_ch = delta_b / delta_d if delta_d else 0.0

    global_eval = evaluate_partial_sum_bridge(s, terms)
    global_r = global_eval.normalized_ratio.real
    return ChamberDirichletIncrements(
        s=s,
        delta_d=delta_d,
        delta_b=delta_b,
        rho_chamber=rho_ch,
        global_r=global_r,
        global_r_error=global_eval.normalized_ratio_error,
    )


def load_f18_audit_summary() -> dict:
    """Load pinned F18-004 audit summary (40M replay)."""
    if not F18_AUDIT_PATH.is_file():
        raise FileNotFoundError(F18_AUDIT_PATH)
    return json.loads(F18_AUDIT_PATH.read_text(encoding="utf-8"))


def chamber_report_to_dict(report: ChamberGapReport) -> dict:
    return asdict(report)


def increments_to_dict(inc: ChamberDirichletIncrements) -> dict:
    return asdict(inc)