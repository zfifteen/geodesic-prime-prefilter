#!/usr/bin/env python3
"""LWM-CROSS-01: Cross-family scoring experiment (left vs right origin thread families).

Isolated implementation extending the literal_web_hole_trace.py baseline
under the literal multiplicative-web / public-thread-triangulation contract.

- Families defined strictly from public offset signs of heldout composites
  (left: offset < 0; right: offset > 0). Never uses p/q knowledge.
- Direct p/q rows held out before any scoring.
- Cross-family bonus applied only to holes supported by >=1 left-origin thread
  AND >=1 right-origin thread (dual-origin threads qualify for both).
- Raw within-family counts and total kept as secondary signals.
- Runs on 4 toy cases (public sqrt radius) + available ladder rungs (6*p radius).
- Emits flat baseline view + cross-family view side-by-side for comparison.
- All outputs public; audit labels written after public artifacts.

See baseline_literal_web_hole_trace.py for the exact starting point.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

# Toy cases use the baseline public sqrt-radius rule (identical to literal_web_hole_trace.py)
CASES = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
]

# Ladder rung factors (available from historical literal ladder; we apply 6*p radius here)
LADDER_RUNG_FACTORS = [
    (23, 31),
    (43, 59),
    (61, 83),
    (89, 113),
    (101, 137),
    (131, 167),
    (173, 211),
    (229, 277),
    (307, 367),
    (401, 503),
    (557, 661),
    (701, 887),
    (1009, 1231),
    (1601, 2003),
    (3001, 4001),
    (5003, 7001),
    (6007, 8009),
    (7001, 9001),
    (8009, 10007),
]

WINDOW_SQRT_RATIO = (1, 1)
RADIUS_MULTIPLIER = 6


def ceil_ratio(value, numerator, denominator):
    return (value * numerator + denominator - 1) // denominator


def public_radius(n):
    numerator, denominator = WINDOW_SQRT_RATIO
    return (math.isqrt(n) * numerator) // denominator


def factor_label(factors):
    return " * ".join(
        str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
    )


def rows_around(n, radius):
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


def thread_slots(n, radius, r):
    start = -radius
    residue = (-n) % r
    first = start + ((residue - start) % r)
    return [t for t in range(first, radius + 1, r) if t != 0 and n + t >= 4]


def direct_kind(row, p, q):
    has_p = p in row["factors"]
    has_q = q in row["factors"]
    if has_p and has_q:
        return "center"
    if has_p:
        return "p_thread"
    if has_q:
        return "q_thread"
    return None


def analyze_case_cross(case):
    """Extended analyze with left/right family partitioning and cross-family scoring.

    Contract preserved exactly:
    - public rows only for thread construction
    - direct p/q rows held out before support or family assignment
    - families derived solely from sign of public heldout offsets
    """
    p, q = case["p"], case["q"]
    n = p * q
    # Support optional explicit radius (for ladder rungs); default to baseline public rule
    radius = case.get("radius") or public_radius(n)
    rows = rows_around(n, radius)
    by_offset = {row["offset"]: row for row in rows}
    direct_offsets = {
        row["offset"]: direct_kind(row, p, q)
        for row in rows
        if direct_kind(row, p, q)
    }
    heldout = [row for row in rows if row["offset"] not in direct_offsets]
    heldout_offsets = {row["offset"] for row in heldout}

    # === Cross-family partition: purely public offset signs (left <0, right >0) ===
    left_heldout = [row for row in heldout if row["offset"] < 0]
    right_heldout = [row for row in heldout if row["offset"] > 0]

    r_left = set()
    for row in left_heldout:
        r_left.update(row["factors"].keys())

    r_right = set()
    for row in right_heldout:
        r_right.update(row["factors"].keys())

    # Factors observed in heldout (public only)
    factors = sorted({r for row in heldout for r in row["factors"]})

    # Raw thread support (identical collection rule to baseline)
    support = defaultdict(list)
    for r in factors:
        for offset in thread_slots(n, radius, r):
            if offset not in heldout_offsets:
                support[offset].append(r)

    # Dedup and attach family data (post-holdout)
    cross_data = {}
    for offset, rs in support.items():
        rs_unique = sorted(set(rs))
        left_fs = [r for r in rs_unique if r in r_left]
        right_fs = [r for r in rs_unique if r in r_right]
        left_c = len(left_fs)
        right_c = len(right_fs)
        has_cross = 1 if (left_c > 0 and right_c > 0) else 0
        total_c = len(rs_unique)
        max_within = max(left_c, right_c) if (left_c or right_c) else 0

        cross_data[offset] = {
            "left_family_support": left_c,
            "right_family_support": right_c,
            "cross_bonus": has_cross,
            "total_support": total_c,
            "max_within_family": max_within,
            "left_family_factors": left_fs,
            "right_family_factors": right_fs,
            "all_supporting_factors": rs_unique,
        }

    # Flat baseline top tier (exact same rule as literal_web_hole_trace.py)
    max_support = max((len(supporters) for supporters in support.values()), default=0)
    top_flat_offsets = {
        offset for offset, supporters in support.items()
        if len(supporters) == max_support
    }

    # Cross-family nomination: primary key = (cross_bonus desc, total_support desc, |offset| asc, offset asc)
    # This promotes inter-family alignments while retaining total support as strong secondary.
    def cross_key(o):
        d = cross_data[o]
        return (-d["cross_bonus"], -d["total_support"], abs(o), o)

    if cross_data:
        best_cross_key = min(cross_key(o) for o in cross_data)  # min because negated for desc
        top_cross_offsets = {o for o in cross_data if cross_key(o) == best_cross_key}
    else:
        top_cross_offsets = set()

    # Build full holes list (flat order) augmented with cross fields
    holes = []
    for offset, supporters in sorted(
        support.items(), key=lambda item: (-len(item[1]), abs(item[0]), item[0])
    ):
        row = by_offset.get(offset)
        audit = direct_offsets.get(offset)
        cd = cross_data.get(offset, {})
        holes.append({
            "offset": offset,
            "value": n + offset,
            "support": len(supporters),
            "supporting_factors": supporters,
            "support_truncated": False,
            "audit_kind": audit if audit else ("other_composite" if row else "not_composite"),
            "audit_factorization": row["factorization"] if row else None,
            # Cross-family extensions (public only)
            "left_family_support": cd.get("left_family_support", 0),
            "right_family_support": cd.get("right_family_support", 0),
            "cross_bonus": cd.get("cross_bonus", 0),
            "max_within_family": cd.get("max_within_family", 0),
            "left_family_factors": cd.get("left_family_factors", []),
            "right_family_factors": cd.get("right_family_factors", []),
        })

    top_flat_holes = [hole for hole in holes if hole["offset"] in top_flat_offsets]
    top_cross_holes = [hole for hole in holes if hole["offset"] in top_cross_offsets]

    # Direct rows (audit only, after public freeze)
    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        row = by_offset[offset]
        direct_rows.append({
            "offset": offset,
            "kind": kind,
            "value": row["value"],
            "factorization": row["factorization"],
            "support": len(support.get(offset, [])),
            "supporting_factors": support.get(offset, []),
        })

    # True factor distance offsets: fundamental +/-p, +/-q (and small multiples) inside window
    # These are the canonical "factor distances" in the web geometry (t multiples of p or of q).
    true_dist_offsets = set()
    for base in (p, q):
        for m in range(-10, 11):
            if m == 0:
                continue
            t = m * base
            if abs(t) <= radius:
                true_dist_offsets.add(t)

    # Rank maps (1-based position in the ordered supported holes under each rule)
    flat_sorted = sorted(support.items(), key=lambda kv: (-len(kv[1]), abs(kv[0]), kv[0]))
    flat_rank_map = {off: rank for rank, (off, _) in enumerate(flat_sorted, 1)}

    cross_sorted = sorted(cross_data.keys(), key=cross_key)
    cross_rank_map = {off: rank for rank, off in enumerate(cross_sorted, 1)}

    # Stats for true distances under both views
    true_dist_details = []
    for t in sorted(true_dist_offsets, key=lambda x: (abs(x), x)):
        flat_s = len(support.get(t, []))
        cd = cross_data.get(t, {})
        cross_b = cd.get("cross_bonus", 0)
        left_c = cd.get("left_family_support", 0)
        right_c = cd.get("right_family_support", 0)
        flat_r = flat_rank_map.get(t)
        cross_r = cross_rank_map.get(t)
        true_dist_details.append({
            "offset": t,
            "flat_support": flat_s,
            "cross_bonus": cross_b,
            "left_family_support": left_c,
            "right_family_support": right_c,
            "flat_rank": flat_r,
            "cross_rank": cross_r,
            "rank_improved": (cross_r is not None and flat_r is not None and cross_r < flat_r),
            "rank_worsened": (cross_r is not None and flat_r is not None and cross_r > flat_r),
            "in_flat_top": t in top_flat_offsets,
            "in_cross_top": t in top_cross_offsets,
        })

    # Aggregate improvement signals
    improved_count = sum(1 for d in true_dist_details if d["rank_improved"])
    worsened_count = sum(1 for d in true_dist_details if d["rank_worsened"])
    num_true_in_flat_top = sum(1 for d in true_dist_details if d["in_flat_top"])
    num_true_in_cross_top = sum(1 for d in true_dist_details if d["in_cross_top"])

    # Cross vs flat emitted tier sizes (noise proxy at the nomination threshold)
    flat_emitted_count = len(top_flat_offsets)
    cross_emitted_count = len(top_cross_offsets)

    emitted_direct_hits_flat = sum(
        1 for hole in top_flat_holes if hole["audit_kind"] in {"p_thread", "q_thread"}
    )
    emitted_direct_hits_cross = sum(
        1 for hole in top_cross_holes if hole["audit_kind"] in {"p_thread", "q_thread"}
    )

    supported_direct = sum(1 for row in direct_rows if row["support"] > 0)

    return {
        "name": case["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "row_count_full": len(rows),
        "row_count_heldout": len(heldout),
        "max_support": max_support,
        "emitted_hole_count_flat": flat_emitted_count,
        "emitted_hole_count_cross": cross_emitted_count,
        "direct_row_count": len(direct_rows),
        "supported_direct_count": supported_direct,
        "emitted_direct_hits_flat": emitted_direct_hits_flat,
        "emitted_direct_hits_cross": emitted_direct_hits_cross,
        "max_cross_bonus": max((d["cross_bonus"] for d in cross_data.values()), default=0),
        "num_true_factor_dists": len(true_dist_offsets),
        "num_true_in_flat_top": num_true_in_flat_top,
        "num_true_in_cross_top": num_true_in_cross_top,
        "true_dist_rank_improved_count": improved_count,
        "true_dist_rank_worsened_count": worsened_count,
        "true_dist_details": true_dist_details,
        "direct_rows": direct_rows,
        "top_flat_holes": top_flat_holes,
        "top_cross_holes": top_cross_holes,
        # Public thread family sizes (for audit of partition balance)
        "left_origin_r_count": len(r_left),
        "right_origin_r_count": len(r_right),
        "dual_origin_r_count": len(r_left & r_right),
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_manifest(out_dir, files_written):
    """Public reproducibility manifest with SHA256 of key artifacts."""
    manifest = {
        "experiment": "LWM-CROSS-01",
        "contract": "literal multiplicative-web / thread-triangulation (public before audit)",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": []
    }
    for p in sorted(files_written):
        if p.exists():
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            manifest["files"].append({
                "path": str(p.relative_to(HERE)),
                "sha256": h,
                "size": p.stat().st_size
            })
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def write_summary_md(results, toy_results, ladder_results):
    lines = [
        "# LWM-CROSS-01 Cross-Family Scoring Results (Literal Web)",
        "",
        "Experiment: explicit left-origin vs right-origin thread families (public offset sign only).",
        "Cross-family bonus awarded to offsets supported by threads from both families.",
        "Baseline flat support retained for direct comparison.",
        "All scoring after mandatory holdout of direct p/q rows.",
        "",
        "## Toy Cases (public sqrt-radius, identical contract to baseline)",
        "",
        "| case | radius | flat emitted | cross emitted | max flat supp | max cross bonus | true dists in flat top | true dists in cross top | improved ranks |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in toy_results:
        lines.append(
            f"| {r['name']} | {r['radius']} | {r['emitted_hole_count_flat']} | {r['emitted_hole_count_cross']} | "
            f"{r['max_support']} | {r['max_cross_bonus']} | {r['num_true_in_flat_top']}/{r['num_true_factor_dists']} | "
            f"{r['num_true_in_cross_top']}/{r['num_true_factor_dists']} | {r['true_dist_rank_improved_count']} |"
        )

    lines += [
        "",
        "## Ladder Rungs (6*p radius, historical scale)",
        "",
        "| case | radius | flat emitted | cross emitted | max flat supp | max cross bonus | true dists in flat top | true dists in cross top | improved ranks |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in ladder_results:
        lines.append(
            f"| {r['name']} | {r['radius']} | {r['emitted_hole_count_flat']} | {r['emitted_hole_count_cross']} | "
            f"{r['max_support']} | {r['max_cross_bonus']} | {r['num_true_in_flat_top']}/{r['num_true_factor_dists']} | "
            f"{r['num_true_in_cross_top']}/{r['num_true_factor_dists']} | {r['true_dist_rank_improved_count']} |"
        )

    lines += ["", "## Key Observations (data only)", ""]
    # Will be filled by post-run analysis in FINDINGS, but include raw aggregates here
    total_improved = sum(r["true_dist_rank_improved_count"] for r in results)
    total_worsened = sum(r["true_dist_rank_worsened_count"] for r in results)
    lines.append(f"Across all runs: true factor distance ranks improved in {total_improved} instances, worsened in {total_worsened}.")
    lines.append("See top_*.jsonl and full_results.json for per-hole family scores and exact supporting factors.")
    lines.append("")

    for result in results:
        lines.append(f"### {result['name']} (radius={result['radius']})")
        lines.append("")
        lines.append(f"Flat max support tier size: {result['emitted_hole_count_flat']} (hits on direct p/q rows: {result['emitted_direct_hits_flat']})")
        lines.append(f"Cross-family tier size: {result['emitted_hole_count_cross']} (hits on direct p/q rows: {result['emitted_direct_hits_cross']})")
        lines.append(f"Origin balance: left_r={result['left_origin_r_count']}, right_r={result['right_origin_r_count']}, dual={result['dual_origin_r_count']}")
        lines.append("")
        lines.append("True factor distance details (offset, flat_supp/cross_bonus, flat_rank -> cross_rank):")
        for td in result["true_dist_details"]:
            imp = " (improved)" if td["rank_improved"] else (" (worsened)" if td["rank_worsened"] else "")
            lines.append(
                f"  {td['offset']}: flat={td['flat_support']}, cross_b={td['cross_bonus']} (L={td['left_family_support']}/R={td['right_family_support']}), "
                f"rank {td['flat_rank']} -> {td['cross_rank']}{imp}"
            )
        lines.append("")
        lines.append("Flat top holes (max raw support):")
        for h in result["top_flat_holes"][:5]:  # first few
            lines.append(f"  offset {h['offset']}: supp={h['support']}, cross_b={h['cross_bonus']}, audit={h['audit_kind']}")
        if len(result["top_flat_holes"]) > 5:
            lines.append(f"  ... +{len(result['top_flat_holes'])-5} more")
        lines.append("")
        lines.append("Cross top holes (max cross_key):")
        for h in result["top_cross_holes"][:5]:
            lines.append(f"  offset {h['offset']}: supp={h['support']}, cross_b={h['cross_bonus']}, audit={h['audit_kind']}")
        if len(result["top_cross_holes"]) > 5:
            lines.append(f"  ... +{len(result['top_cross_holes'])-5} more")
        lines.append("")

    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    all_results = []

    # 1. Four toy cases under identical baseline radius rule
    print("Running 4 toy cases (sqrt-radius baseline contract)...")
    toy_results = []
    for case in CASES:
        started = time.perf_counter()
        res = analyze_case_cross(case)
        res["seconds"] = time.perf_counter() - started
        res["scale"] = "toy_sqrt"
        all_results.append(res)
        toy_results.append(res)
        print(f"  {res['name']}: flat_emitted={res['emitted_hole_count_flat']}, cross_emitted={res['emitted_hole_count_cross']}, improved_true={res['true_dist_rank_improved_count']}")

    # 2. Available ladder rungs at 6*p scale (public thread web at larger but still literal radius)
    print("\nRunning ladder rungs at 6*p radius...")
    ladder_results = []
    for idx, (pp, qq) in enumerate(LADDER_RUNG_FACTORS):
        case = {
            "name": f"ladder_rung_{idx:02d}_{pp}x{qq}",
            "p": pp,
            "q": qq,
            "radius": RADIUS_MULTIPLIER * pp,
        }
        started = time.perf_counter()
        res = analyze_case_cross(case)
        res["seconds"] = time.perf_counter() - started
        res["scale"] = "ladder_6p"
        all_results.append(res)
        ladder_results.append(res)
        print(f"  {res['name']}: flat_emitted={res['emitted_hole_count_flat']}, cross_emitted={res['emitted_hole_count_cross']}, improved_true={res['true_dist_rank_improved_count']}")

    # Write public artifacts
    (OUT / "full_results.json").write_text(json.dumps(all_results, indent=2) + "\n", encoding="utf-8")

    # JSONL for flat top holes (baseline view)
    flat_jsonl_rows = []
    for res in all_results:
        for h in res["top_flat_holes"]:
            flat_jsonl_rows.append({"case": res["name"], "scale": res["scale"], "view": "flat", **{k: h[k] for k in h}})
    write_jsonl(OUT / "top_flat_holes.jsonl", flat_jsonl_rows)

    # JSONL for cross top holes (new view)
    cross_jsonl_rows = []
    for res in all_results:
        for h in res["top_cross_holes"]:
            cross_jsonl_rows.append({"case": res["name"], "scale": res["scale"], "view": "cross", **{k: h[k] for k in h}})
    write_jsonl(OUT / "top_cross_holes.jsonl", cross_jsonl_rows)

    # Also emit all supported holes with family data for deeper audit (one per case slice)
    all_supported_jsonl = []
    # We don't store every supported in memory for huge cases, but for completeness on toys + small ladders we can rely on full_results
    # For now, the top views + full_results (which includes per-case true_dist_details + top lists) are the primary public artifacts.

    write_summary_md(all_results, toy_results, ladder_results)

    # Manifest of public outputs
    written = [
        OUT / "full_results.json",
        OUT / "top_flat_holes.jsonl",
        OUT / "top_cross_holes.jsonl",
        OUT / "summary.md",
    ]
    manifest = write_manifest(OUT, written)

    print(f"\nWrote artifacts to {OUT}")
    print(f"Manifest: {len(manifest['files'])} files sha256-recorded.")

    # Quick stdout comparison table for immediate inspection
    print("\n=== QUICK COMPARISON (flat vs cross emitted tier size) ===")
    for r in all_results:
        delta = r['emitted_hole_count_cross'] - r['emitted_hole_count_flat']
        print(f"{r['name']:25s}  flat={r['emitted_hole_count_flat']:3d}  cross={r['emitted_hole_count_cross']:3d}  delta={delta:+d}  true_improved={r['true_dist_rank_improved_count']}")


if __name__ == "__main__":
    main()
