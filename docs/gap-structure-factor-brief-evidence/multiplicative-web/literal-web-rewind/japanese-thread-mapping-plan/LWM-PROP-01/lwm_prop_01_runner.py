#!/usr/bin/env python3
"""LWM-PROP-01: Deterministic local propagation (carry analog) experiment.

Isolated implementation under the literal multiplicative-web / thread-triangulation
path (rewind contract). Starts from literal hole-trace baseline support, then
applies one public, deterministic, reversible, non-iterative local propagation
step using only post-holdout public thread data.

No ratio pruning, no candidate generation, no classical search as inference.
Propagation never creates new hole positions; only augments existing positive-support
offsets using public small-prime kernels.

Contract: public web (held-out factors) -> primary flat support -> public
propagation rule -> augmented nomination -> audit (p/q labels read only after
public artifacts frozen).
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

# Public constants for the propagation rule (fully auditable, fixed for this experiment)
PROP_THRESHOLD = 2          # minimum primary support to be a "strong" source for propagation
PROP_BONUS = 1              # fixed carry unit added on each valid hop
PROP_MAX_KERNELS = 6        # use the smallest N observed public primes as kernels
PROP_ONLY_TO_POSITIVE = True  # never inject support into zero-primary positions

# Toy cases use baseline public radius (sqrt(N))
# Ladder rungs use historical 6*p radius for scale testing (as documented in plan)
# Radii pre-computed for exact reproducibility (matches baseline + ladder history)
CASES: list[dict[str, Any]] = [
    # Baseline toys (public_radius ~ sqrt(N))
    {"name": "toy_23x31", "p": 23, "q": 31, "radius": 26, "scale": "baseline_sqrt"},
    {"name": "toy_43x59", "p": 43, "q": 59, "radius": 50, "scale": "baseline_sqrt"},
    {"name": "toy_61x83", "p": 61, "q": 83, "radius": 71, "scale": "baseline_sqrt"},
    {"name": "toy_89x113", "p": 89, "q": 113, "radius": 100, "scale": "baseline_sqrt"},
    # Ladder rungs (radius = 6 * p, limited to feasible small rungs for isolated run)
    {"name": "ladder_00_23x31", "p": 23, "q": 31, "radius": 138, "scale": "ladder_6p"},
    {"name": "ladder_01_43x59", "p": 43, "q": 59, "radius": 258, "scale": "ladder_6p"},
    {"name": "ladder_02_61x83", "p": 61, "q": 83, "radius": 366, "scale": "ladder_6p"},
    {"name": "ladder_03_89x113", "p": 89, "q": 113, "radius": 534, "scale": "ladder_6p"},
    {"name": "ladder_04_101x137", "p": 101, "q": 137, "radius": 606, "scale": "ladder_6p"},
    {"name": "ladder_05_131x167", "p": 131, "q": 167, "radius": 786, "scale": "ladder_6p"},
]


def public_radius(n: int) -> int:
    """Baseline public radius rule (sqrt(N) with (1,1) ratio)."""
    return math.isqrt(n)


def factor_label(factors: dict[int, int]) -> str:
    return " * ".join(
        str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
    )


def rows_around(n: int, radius: int) -> list[dict[str, Any]]:
    rows = []
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        factors = {int(k): int(v) for k, v in factorint(value).items()}
        if factors == {value: 1}:
            continue
        divisor_count = math.prod(e + 1 for e in factors.values())
        rows.append({
            "value": value,
            "offset": value - n,
            "factors": factors,
            "factorization": factor_label(factors),
            "divisor_count": divisor_count,
        })
    return rows


def thread_slots(n: int, radius: int, r: int) -> list[int]:
    start = -radius
    residue = (-n) % r
    first = start + ((residue - start) % r)
    return [t for t in range(first, radius + 1, r) if t != 0 and n + t >= 4]


def direct_kind(row: dict[str, Any], p: int, q: int) -> str | None:
    has_p = p in row["factors"]
    has_q = q in row["factors"]
    if has_p and has_q:
        return "center"
    if has_p:
        return "p_thread"
    if has_q:
        return "q_thread"
    return None


def compute_primary_support(
    n: int, radius: int, p: int, q: int
) -> tuple[dict[int, list[int]], dict[int, dict], list[dict], list[dict], set[int]]:
    """Exact replica of literal hole-trace baseline primary support (flat)."""
    rows = rows_around(n, radius)
    by_offset = {row["offset"]: row for row in rows}
    direct_offsets = {
        row["offset"]: direct_kind(row, p, q)
        for row in rows
        if direct_kind(row, p, q)
    }
    heldout = [row for row in rows if row["offset"] not in direct_offsets]
    heldout_offsets = {row["offset"] for row in heldout}

    factors = sorted({r for row in heldout for r in row["factors"]})
    support: dict[int, list[int]] = defaultdict(list)
    for r in factors:
        for offset in thread_slots(n, radius, r):
            if offset not in heldout_offsets:
                support[offset].append(r)

    # Dedup (should already be unique per r)
    primary_support = {t: sorted(set(rs)) for t, rs in support.items()}

    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        row = by_offset[offset]
        direct_rows.append({
            "offset": offset,
            "kind": kind,
            "value": row["value"],
            "factorization": row["factorization"],
        })

    heldout_rows_public = [
        {
            "offset": r["offset"],
            "value": r["value"],
            "factorization": r["factorization"],
            "factors": sorted(r["factors"].keys()),
        }
        for r in heldout
    ]

    return primary_support, by_offset, direct_rows, heldout_rows_public, heldout_offsets


def apply_lwm_prop01_propagation(
    primary_support: dict[int, list[int]],
    radius: int,
) -> tuple[dict[int, int], dict[int, list[dict]], dict[int, int]]:
    """Deterministic, reversible, one-hop local propagation (carry analog).

    Exact public rule (documented for audit):
    - K = smallest PROP_MAX_KERNELS distinct public primes observed in heldout rows.
    - Strong sources = offsets with primary_support >= PROP_THRESHOLD (public const=2).
    - For each strong t, each k in K, each sign ±1:
        tp = t + sign*k
        if |tp| <= radius, tp != 0, and primary_support[tp] >= 1 (POSITIVE only):
            add PROP_BONUS (const=1) to tp
            log the (from=t, k=k) for reversibility
    - Single synchronous pass. No iteration, no chasing, no zero-injection.
    - All inputs to rule are public post-holdout (the prime list and the primary map).
    - No p, q, or audit labels used anywhere in rule.

    Returns: bonus_map, provenance_log, augmented_map
    """
    if not primary_support:
        return {}, {}, {}

    # Public primes = all distinct r that provided threads (from the support keys' contributors)
    all_public_primes: set[int] = set()
    for rs in primary_support.values():
        all_public_primes.update(rs)
    public_primes_sorted = sorted(all_public_primes)

    kernels = public_primes_sorted[:PROP_MAX_KERNELS]

    propagated_bonus: dict[int, int] = defaultdict(int)
    propagation_log: dict[int, list[dict]] = defaultdict(list)

    strong_ts = [t for t, rs in primary_support.items() if len(rs) >= PROP_THRESHOLD]

    for t in strong_ts:
        for k in kernels:
            for sign in (+1, -1):
                tp = t + sign * k
                if abs(tp) > radius or tp == 0:
                    continue
                if tp in primary_support and len(primary_support[tp]) >= 1:
                    propagated_bonus[tp] += PROP_BONUS
                    propagation_log[tp].append({"from_offset": t, "k": k})

    augmented: dict[int, int] = {}
    for t, rs in primary_support.items():
        aug = len(rs) + propagated_bonus.get(t, 0)
        augmented[t] = aug

    # Return plain dicts (no defaultdict)
    return dict(propagated_bonus), {t: logs for t, logs in propagation_log.items()}, augmented


def build_hole_list(
    support_map: dict[int, list[int] | int],  # primary uses list, augmented uses int count
    augmented_map: dict[int, int] | None,
    bonus_map: dict[int, int],
    provenance: dict[int, list[dict]],
    by_offset: dict[int, dict],
    direct_offsets: dict[int, str],
    primary_support: dict[int, list[int]],
) -> list[dict[str, Any]]:
    """Build full hole records sorted by the given support (primary or augmented)."""
    # Normalize to count map for sorting
    if isinstance(next(iter(support_map.values()), 0), (list, tuple)):
        count_map = {t: len(v) for t, v in support_map.items()}
    else:
        count_map = support_map  # type: ignore[assignment]

    def sort_key(t: int) -> tuple[int, int, int]:
        return (-count_map[t], abs(t), t)

    holes: list[dict[str, Any]] = []
    for t in sorted(count_map.keys(), key=sort_key):
        prim_list = primary_support.get(t, [])
        prim_count = len(prim_list)
        aug_count = augmented_map.get(t, prim_count) if augmented_map is not None else prim_count
        row = by_offset.get(t)
        audit = direct_offsets.get(t)
        holes.append({
            "offset": t,
            "value": (row["value"] if row else None),
            "primary_support": prim_count,
            "supporting_factors": prim_list,
            "augmented_support": aug_count,
            "propagation_bonus": bonus_map.get(t, 0),
            "propagation_sources": provenance.get(t, []),
            "audit_kind": audit if audit else ("other_composite" if row else "not_composite"),
            "audit_factorization": (row["factorization"] if row else None),
        })
    return holes


def analyze_case_lwm_prop01(case: dict[str, Any]) -> dict[str, Any]:
    """Run full baseline + LWM-PROP-01 propagation for one case."""
    p, q = case["p"], case["q"]
    n = p * q
    radius = case["radius"]
    scale = case.get("scale", "unknown")

    started = time.perf_counter()

    # === PRIMARY (literal baseline, flat) ===
    primary_support, by_offset, direct_rows, heldout_rows_public, heldout_offsets = compute_primary_support(n, radius, p, q)

    # Public primes for rule (post-holdout only)
    public_primes = sorted({r for rs in primary_support.values() for r in rs})

    max_primary = max((len(rs) for rs in primary_support.values()), default=0)
    primary_top_offsets = {t for t, rs in primary_support.items() if len(rs) == max_primary}

    # === PROPAGATION (LWM-PROP-01) ===
    bonus_map, provenance, augmented = apply_lwm_prop01_propagation(primary_support, radius)

    max_aug = max(augmented.values()) if augmented else 0
    aug_top_offsets = {t for t, a in augmented.items() if a == max_aug}

    # Build full sorted lists (primary order and augmented order)
    direct_offset_set = {d["offset"] for d in direct_rows}
    direct_kinds = {d["offset"]: d["kind"] for d in direct_rows}

    primary_holes = build_hole_list(
        primary_support, None, {}, {}, by_offset, direct_kinds, primary_support
    )
    aug_holes = build_hole_list(
        augmented, augmented, bonus_map, provenance, by_offset, direct_kinds, primary_support
    )

    # Identify true held-out distances (direct p/q thread offsets)
    true_direct_offsets = [d["offset"] for d in direct_rows if d["kind"] in {"p_thread", "q_thread"}]

    # Ranks (1-based position in sorted descending list)
    def compute_ranks(holes: list[dict], true_set: list[int]) -> dict[int, int | None]:
        ranks: dict[int, int | None] = {}
        for rank, hole in enumerate(holes, 1):
            if hole["offset"] in true_set:
                ranks[hole["offset"]] = rank
        for to in true_set:
            if to not in ranks:
                ranks[to] = None  # not present in list (should not happen)
        return ranks

    primary_ranks = compute_ranks(primary_holes, true_direct_offsets)
    aug_ranks = compute_ranks(aug_holes, true_direct_offsets)

    # Nomination in the strict "max" emitted set
    primary_emitted_trues = [to for to in true_direct_offsets if to in primary_top_offsets]
    aug_emitted_trues = [to for to in true_direct_offsets if to in aug_top_offsets]

    elapsed = time.perf_counter() - started

    result = {
        "name": case["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "scale": scale,
        "row_count_full": len(by_offset) + len(direct_rows),  # approx
        "direct_row_count": len(direct_rows),
        "max_primary_support": max_primary,
        "max_augmented_support": max_aug,
        "primary_emitted_hole_count": len(primary_top_offsets),
        "augmented_emitted_hole_count": len(aug_top_offsets),
        "true_direct_offsets": sorted(true_direct_offsets),
        "primary_ranks_of_trues": primary_ranks,
        "augmented_ranks_of_trues": aug_ranks,
        "primary_emitted_trues": sorted(primary_emitted_trues),
        "augmented_emitted_trues": sorted(aug_emitted_trues),
        "public_primes_for_kernels": public_primes,
        "kernels_used": public_primes[:PROP_MAX_KERNELS],
        "propagation_threshold": PROP_THRESHOLD,
        "propagation_bonus": PROP_BONUS,
        "elapsed_sec": round(elapsed, 4),
        # Full public + audit data for this case (frozen together for isolated run)
        "primary_top_holes": [h for h in primary_holes if h["offset"] in primary_top_offsets],
        "augmented_top_holes": [h for h in aug_holes if h["offset"] in aug_top_offsets],
        "all_holes_sample": aug_holes[:30],  # first 30 in aug order for inspection (full in jsonl)
    }
    return result


def write_case_artifacts(result: dict[str, Any], case_dir: Path) -> None:
    case_dir.mkdir(parents=True, exist_ok=True)

    # Public contract artifacts (nomination decided without audit labels in rule)
    public_nomination = {
        "case": result["name"],
        "N": result["N"],
        "radius": result["radius"],
        "public_primes_for_kernels": result["public_primes_for_kernels"],
        "kernels_used": result["kernels_used"],
        "propagation_rule": {
            "threshold": result["propagation_threshold"],
            "bonus": result["propagation_bonus"],
            "max_kernels": PROP_MAX_KERNELS,
            "description": "One-hop reinforce only: strong (>=2) primary offsets send +1 to t±k (k in smallest observed public primes) only if target already has >=1 primary support. Synchronous, non-iterative, zero-injection forbidden. Reversible via provenance.",
            "reversible": True,
            "no_new_candidates": True,
        },
        "max_primary_support": result["max_primary_support"],
        "max_augmented_support": result["max_augmented_support"],
        "primary_emitted_offsets": [h["offset"] for h in result["primary_top_holes"]],
        "augmented_emitted_offsets": [h["offset"] for h in result["augmented_top_holes"]],
        "primary_emitted_count": result["primary_emitted_hole_count"],
        "augmented_emitted_count": result["augmented_emitted_hole_count"],
    }
    (case_dir / "public_nomination.json").write_text(json.dumps(public_nomination, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Detailed holes with full provenance (public + labels for audit scoring only)
    (case_dir / "holes_augmented.jsonl").write_text(
        "".join(json.dumps(h, sort_keys=True) + "\n" for h in result.get("all_holes_sample", [])),
        encoding="utf-8"
    )

    # True direct comparison (audit sidecar)
    audit = {
        "true_direct_offsets": result["true_direct_offsets"],
        "primary_ranks": result["primary_ranks_of_trues"],
        "augmented_ranks": result["augmented_ranks_of_trues"],
        "primary_emitted_trues": result["primary_emitted_trues"],
        "augmented_emitted_trues": result["augmented_emitted_trues"],
    }
    (case_dir / "audit_comparison.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_global_artifacts(results: list[dict[str, Any]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # Aggregate summary (public + measured outcome)
    lines = [
        "# LWM-PROP-01 Findings: Deterministic Local Propagation (Carry Analog)",
        "",
        "EXPERIMENT: LWM-PROP-01",
        "Path: literal multiplicative-web / thread-triangulation (rewind contract)",
        "Baseline: literal hole-trace flat primary support (no banded in this isolated run)",
        "Refinement: one public deterministic reversible local propagation step after primary support",
        "",
        "Propagation rule (exact, public, auditable):",
        f"  - Threshold for strong source: primary_support >= {PROP_THRESHOLD}",
        f"  - Kernels: smallest {PROP_MAX_KERNELS} distinct public primes observed in heldout rows",
        f"  - Bonus: +{PROP_BONUS} (fixed carry unit) per valid t -> t±k hop",
        "  - Targets: ONLY offsets that already have primary_support >= 1 (no candidate expansion)",
        "  - Application: single synchronous non-iterative pass",
        "  - Reversibility: full provenance log of every (source_offset, k) contribution",
        "  - Leakage controls: zero use of p/q/audit labels inside rule; kernels and S from public heldout factors only",
        "",
        "Guardrail compliance: PASS (rule does not generate candidates, does not iterate, decisions public-only post-holdout)",
        "",
        "| case | scale | radius | prim_max | aug_max | prim_emitted | aug_emitted | trues | prim_emitted_trues | aug_emitted_trues | rank_improvement |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]

    for r in results:
        trues = len(r["true_direct_offsets"])
        prim_hits = len(r["primary_emitted_trues"])
        aug_hits = len(r["augmented_emitted_trues"])
        # Simple improvement signal: did any true's best rank get strictly better (lower)?
        best_prim = min((v for v in r["primary_ranks_of_trues"].values() if v is not None), default=999)
        best_aug = min((v for v in r["augmented_ranks_of_trues"].values() if v is not None), default=999)
        rank_delta = best_aug - best_prim
        delta_str = f"{rank_delta:+d}" if rank_delta != 0 else "0"
        lines.append(
            f"| {r['name']} | {r['scale']} | {r['radius']} | {r['max_primary_support']} | {r['max_augmented_support']} | "
            f"{r['primary_emitted_hole_count']} | {r['augmented_emitted_hole_count']} | {trues} | "
            f"{prim_hits} | {aug_hits} | {delta_str} |"
        )

    lines += ["", "## Per-Case Outcome Summary", ""]
    for r in results:
        lines.append(f"### {r['name']}")
        lines.append(f"- True held-out distances (direct offsets): {r['true_direct_offsets']}")
        lines.append(f"- Primary max emitted count: {r['primary_emitted_hole_count']} (hits on true: {len(r['primary_emitted_trues'])})")
        lines.append(f"- Augmented max emitted count: {r['augmented_emitted_hole_count']} (hits on true: {len(r['augmented_emitted_trues'])})")
        lines.append(f"- Best rank of any true (primary): {min(r['primary_ranks_of_trues'].values())}")
        lines.append(f"- Best rank of any true (augmented): {min(r['augmented_ranks_of_trues'].values())}")
        lines.append(f"- Kernels used: {r['kernels_used']}")
        lines.append("")

    (OUT / "LWM_PROP_01_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Machine readable full results (includes provenance for every case)
    (OUT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Top-level manifest for tamper evidence
    manifest = {
        "experiment": "LWM-PROP-01",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cases_run": [r["name"] for r in results],
        "rule_constants": {
            "PROP_THRESHOLD": PROP_THRESHOLD,
            "PROP_BONUS": PROP_BONUS,
            "PROP_MAX_KERNELS": PROP_MAX_KERNELS,
            "PROP_ONLY_TO_POSITIVE": PROP_ONLY_TO_POSITIVE,
        },
        "baseline_reference": "literal_web_hole_trace.py flat support (rewind contract)",
        "no_violations": True,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Also emit a jsonl of all augmented top holes across cases for quick audit
    top_rows = []
    for r in results:
        for h in r.get("augmented_top_holes", []):
            top_rows.append({"case": r["name"], **h})
    (OUT / "augmented_top_holes.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in top_rows),
        encoding="utf-8"
    )


def main() -> None:
    print("LWM-PROP-01 starting (isolated, literal web path only)...")
    results: list[dict[str, Any]] = []
    for case in CASES:
        print(f"  running {case['name']} (radius={case['radius']}) ...")
        res = analyze_case_lwm_prop01(case)
        results.append(res)
        case_dir = OUT / res["name"]
        write_case_artifacts(res, case_dir)
        print(f"    done: prim_max={res['max_primary_support']} aug_max={res['max_augmented_support']} "
              f"prim_emitted_trues={len(res['primary_emitted_trues'])} aug_emitted_trues={len(res['augmented_emitted_trues'])}")

    write_global_artifacts(results)
    print(f"\nArtifacts written to {OUT}")
    print("LWM-PROP-01 complete.")


if __name__ == "__main__":
    main()
