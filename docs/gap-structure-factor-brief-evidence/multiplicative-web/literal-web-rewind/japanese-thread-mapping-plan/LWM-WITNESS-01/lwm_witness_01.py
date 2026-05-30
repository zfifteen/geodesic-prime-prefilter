#!/usr/bin/env python3
"""LWM-WITNESS-01: Witness completeness / GWR-DNI coverage signatures.

Isolated extension of the literal multiplicative-web baseline (public thread support only).
For each high-support offset (and selected near-high for comparison), emits a sidecar
"coverage_signature" vector built exclusively from PGS-native GWR (leftmost min-divisor
among public heldout composites) and DNI excess at the public composites that generated
the supporting threads.

Signatures are audit-only sidecar metadata. Primary nomination/ranking remains
flat thread support cardinality (max support holes). No leakage into offset selection.

Contract: public composites only -> GWR/DNI on their divisor counts and values ->
sidecar signatures for post-nomination structural analysis. Deterministic. No classical
search, no candidate gen, no private labels in nomination path.

Run on toys + ladder subset. Outputs include raw data for true vs false high-support
signature vector comparison.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(parents=True, exist_ok=True)

# Toy cases (identical to baseline)
CASES = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
]

# Ladder rungs (subset of baseline; stop at feasibility for this isolated run)
LADDER_RUNGS = [
    (23, 31), (43, 59), (61, 83), (89, 113),
    (101, 137), (131, 167), (173, 211), (229, 277),
    (307, 367), (401, 503), (557, 661), (701, 887),
    (1009, 1231), (1601, 2003), (3001, 4001),
    (5003, 7001), (6007, 8009), (7001, 9001), (8009, 10007),
]

WINDOW_SQRT_RATIO = (1, 1)
RADIUS_MULTIPLIER = 6
MAX_RADIUS = 50_000
TOP_K_LADDER = 18


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


def dni_excess(value: int, divisor_count: int) -> float:
    """DNI zero-excess coordinate E(n) = (d(n)/2 - 1) * ln(n)."""
    if value <= 1 or divisor_count <= 1:
        return 0.0
    return (divisor_count / 2.0 - 1.0) * math.log(value)


def compute_gwr_dni_on_heldout(heldout):
    """PGS-native: GWR as leftmost min divisor_count among public heldout composites.
    DNI excess precomputed per composite. Purely from public data in window.
    """
    if not heldout:
        return {
            "global_min_d": 0,
            "leftmost_gwr_offset": None,
            "leftmost_gwr_value": None,
            "leftmost_gwr_excess": 0.0,
            "per_offset": {},  # offset -> {"is_gwr_min": bool, "dni_excess": float, "d": int}
        }
    global_min_d = min(r["divisor_count"] for r in heldout)
    gwr_rows = [r for r in heldout if r["divisor_count"] == global_min_d]
    leftmost_gwr = min(gwr_rows, key=lambda r: r["offset"])
    leftmost_gwr_offset = leftmost_gwr["offset"]
    leftmost_gwr_value = leftmost_gwr["value"]
    leftmost_gwr_excess = dni_excess(leftmost_gwr_value, global_min_d)

    per_offset = {}
    for r in heldout:
        off = r["offset"]
        d = r["divisor_count"]
        val = r["value"]
        per_offset[off] = {
            "is_gwr_min": (d == global_min_d),
            "dni_excess": dni_excess(val, d),
            "d": d,
            "value": val,
        }
    return {
        "global_min_d": global_min_d,
        "leftmost_gwr_offset": leftmost_gwr_offset,
        "leftmost_gwr_value": leftmost_gwr_value,
        "leftmost_gwr_excess": leftmost_gwr_excess,
        "per_offset": per_offset,
    }


def originating_witness_composites(heldout, supporters):
    """Return unique heldout rows whose factors intersect the supporters set.
    These are the public composites that generated the threads supporting the offset.
    """
    witnesses = []
    seen = set()
    for row in heldout:
        if any(r in row["factors"] for r in supporters):
            off = row["offset"]
            if off not in seen:
                seen.add(off)
                witnesses.append(row)
    return witnesses


def coverage_signature_for_offset(offset, supporters, heldout, gwr_dni):
    """Build deterministic sidecar coverage signature vector from GWR/DNI at originating public composites.
    Does NOT influence which offsets are selected as high-support.
    """
    witnesses = originating_witness_composites(heldout, supporters)
    num_w = len(witnesses)
    if num_w == 0:
        return {
            "support": len(supporters),
            "num_witness_composites": 0,
            "num_gwr_min_witnesses": 0,
            "has_leftmost_gwr": False,
            "avg_dni_excess": 0.0,
            "min_dni_excess": 0.0,
            "gwr_min_d": gwr_dni["global_min_d"],
            "witness_offsets": [],
            "signature_vector": [len(supporters), 0, 0, 0, 0.0, 0.0],
        }

    gwr_min_d = gwr_dni["global_min_d"]
    leftmost_off = gwr_dni["leftmost_gwr_offset"]
    num_gwr = sum(1 for w in witnesses if w["divisor_count"] == gwr_min_d)
    has_left = any(w["offset"] == leftmost_off for w in witnesses) if leftmost_off is not None else False

    excesses = [dni_excess(w["value"], w["divisor_count"]) for w in witnesses]
    avg_e = sum(excesses) / len(excesses)
    min_e = min(excesses)

    # Compact numeric vector for easy tabular comparison and certification:
    # [support, num_witnesses, num_gwr_mins, has_leftmost_gwr (0/1), avg_excess, min_excess]
    sig_vec = [
        len(supporters),
        num_w,
        num_gwr,
        1 if has_left else 0,
        round(avg_e, 6),
        round(min_e, 6),
    ]

    return {
        "support": len(supporters),
        "num_witness_composites": num_w,
        "num_gwr_min_witnesses": num_gwr,
        "has_leftmost_gwr": has_left,
        "avg_dni_excess": round(avg_e, 6),
        "min_dni_excess": round(min_e, 6),
        "gwr_min_d": gwr_min_d,
        "witness_offsets": sorted([w["offset"] for w in witnesses]),
        "signature_vector": sig_vec,
    }


def analyze_case(case, *, include_near_high_for_signature: bool = True):
    """Core literal web analysis + sidecar GWR-DNI coverage signatures.
    Primary emitted holes = flat max-support (unchanged from baseline).
    """
    p, q = case["p"], case["q"]
    n = p * q
    radius = case.get("radius", public_radius(n))
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
    support = defaultdict(list)
    for r in factors:
        for offset in thread_slots(n, radius, r):
            if offset not in heldout_offsets:
                support[offset].append(r)

    max_support = max((len(supporters) for supporters in support.values()), default=0)
    top_offsets = {
        offset
        for offset, supporters in support.items()
        if len(supporters) == max_support
    }

    # GWR/DNI on public heldout composites only (PGS objects)
    gwr_dni = compute_gwr_dni_on_heldout(heldout)

    holes = []
    for offset, supporters in sorted(support.items(), key=lambda item: (-len(item[1]), abs(item[0]), item[0])):
        row = by_offset.get(offset)
        audit = direct_offsets.get(offset)
        sig = coverage_signature_for_offset(offset, supporters, heldout, gwr_dni)
        holes.append({
            "offset": offset,
            "value": n + offset,
            "support": len(supporters),
            "supporting_factors": supporters,
            "audit_kind": audit if audit else ("other_composite" if row else "not_composite"),
            "audit_factorization": row["factorization"] if row else None,
            "coverage_signature": sig,
        })

    # Primary emitted (flat support, no signature leakage)
    top_holes = [hole for hole in holes if hole["offset"] in top_offsets]

    # For secondary analysis only: collect near-high support offsets (support >= max(2, max_support-1))
    # These are used solely for signature discrimination tables vs true direct hits.
    min_support_for_table = max(2, max_support - 1)
    near_high = [hole for hole in holes if hole["support"] >= min_support_for_table]

    # Direct (true factor distance) rows with their support + signatures
    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        row = by_offset[offset]
        sup = support.get(offset, [])
        sig = coverage_signature_for_offset(offset, sup, heldout, gwr_dni) if sup else None
        direct_rows.append({
            "offset": offset,
            "kind": kind,
            "value": row["value"],
            "factorization": row["factorization"],
            "support": len(sup),
            "supporting_factors": sup,
            "coverage_signature": sig,
        })

    emitted_direct_hits = sum(1 for hole in top_holes if hole["audit_kind"] in {"p_thread", "q_thread"})
    supported_direct = sum(1 for row in direct_rows if row["support"] > 0)

    # Simple discrimination stats (sidecar only)
    true_high = [h for h in near_high if h["audit_kind"] in {"p_thread", "q_thread"}]
    false_high = [h for h in near_high if h["audit_kind"] not in {"p_thread", "q_thread"}]

    def avg_sig(key, items):
        vals = [h["coverage_signature"][key] for h in items if h["coverage_signature"]]
        return round(sum(vals) / len(vals), 6) if vals else None

    discrimination = {
        "min_support_for_table": min_support_for_table,
        "num_true_high_support": len(true_high),
        "num_false_high_support": len(false_high),
        "true_avg_dni_excess": avg_sig("avg_dni_excess", true_high),
        "false_avg_dni_excess": avg_sig("avg_dni_excess", false_high),
        "true_avg_num_gwr_min_witnesses": avg_sig("num_gwr_min_witnesses", true_high),
        "false_avg_num_gwr_min_witnesses": avg_sig("num_gwr_min_witnesses", false_high),
        "true_has_leftmost_gwr_frac": (
            sum(1 for h in true_high if h["coverage_signature"] and h["coverage_signature"]["has_leftmost_gwr"])
            / len(true_high) if true_high else None
        ),
        "false_has_leftmost_gwr_frac": (
            sum(1 for h in false_high if h["coverage_signature"] and h["coverage_signature"]["has_leftmost_gwr"])
            / len(false_high) if false_high else None
        ),
    }

    return {
        "name": case["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "row_count_full": len(rows),
        "row_count_heldout": len(heldout),
        "max_support": max_support,
        "emitted_hole_count": len(top_holes),
        "direct_row_count": len(direct_rows),
        "supported_direct_count": supported_direct,
        "emitted_direct_hits": emitted_direct_hits,
        "gwr_dni": {
            "global_min_d": gwr_dni["global_min_d"],
            "leftmost_gwr_offset": gwr_dni["leftmost_gwr_offset"],
            "leftmost_gwr_excess": round(gwr_dni["leftmost_gwr_excess"], 6),
        },
        "direct_rows": direct_rows,
        "top_holes": top_holes,
        "near_high_support_for_signature_analysis": near_high,
        "discrimination_stats": discrimination,
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_summary_md(results, ladder_mode=False, filename="summary.md"):
    lines = [
        "# LWM-WITNESS-01 Findings (Raw Data)",
        "",
        "Experiment: Witness completeness / GWR-DNI coverage signatures as sidecar on literal web baseline.",
        "Primary ranking: unchanged flat max-support cardinality.",
        "GWR = leftmost min-divisor_count among public heldout composites (PGS Leftmost Minimum-Divisor Rule applied to observed public divisor-count field).",
        "DNI excess = (d(n)/2 - 1) * ln(n) at those public composites.",
        "Signatures emitted only for post-nomination / structural certificate analysis.",
        "",
        "Contract compliance: All inputs public. No p/q used for window, bands, or nomination. No ratio pruning or candidate machinery.",
        "",
    ]
    if ladder_mode:
        lines += [
            f"Scaling: radius = {RADIUS_MULTIPLIER} * p (capped).",
            "",
            "| rung | N | radius | max_support | emitted | gwr_min_d | true_high | false_high | true_avg_excess | false_avg_excess |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for r in results:
            ds = r.get("discrimination_stats", {})
            lines.append(
                f"| {r['name']} | {r['N']} | {r['radius']} | {r['max_support']} | {r['emitted_hole_count']} | "
                f"{r['gwr_dni']['global_min_d']} | {ds.get('num_true_high_support',0)} | {ds.get('num_false_high_support',0)} | "
                f"{ds.get('true_avg_dni_excess','N/A')} | {ds.get('false_avg_dni_excess','N/A')} |"
            )
    else:
        lines += [
            "| case | radius | max_support | emitted holes | gwr_min_d | leftmost_gwr_off | true_high | false_high | true_avg_excess | false_avg_excess |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for r in results:
            ds = r.get("discrimination_stats", {})
            lines.append(
                f"| {r['name']} | {r['radius']} | {r['max_support']} | {r['emitted_hole_count']} | "
                f"{r['gwr_dni']['global_min_d']} | {r['gwr_dni']['leftmost_gwr_offset']} | "
                f"{ds.get('num_true_high_support',0)} | {ds.get('num_false_high_support',0)} | "
                f"{ds.get('true_avg_dni_excess','N/A')} | {ds.get('false_avg_dni_excess','N/A')} |"
            )
    lines += ["", "## Per-Case Top Holes (primary flat-support emission, with sidecar signatures)"]
    for r in results:
        lines.append(f"\n### {r['name']} (N={r['N']}, max_support={r['max_support']})")
        lines.append(f"GWR/DNI global: min_d={r['gwr_dni']['global_min_d']}, leftmost_gwr_offset={r['gwr_dni']['leftmost_gwr_offset']}")
        for hole in r["top_holes"]:
            sig = hole["coverage_signature"]
            lines.append(
                f"- offset {hole['offset']}: support={hole['support']}, audit={hole['audit_kind']}, "
                f"sig_vec={sig['signature_vector']}, has_gwr={sig['has_leftmost_gwr']}, "
                f"avg_e={sig['avg_dni_excess']}, witnesses={sig['num_witness_composites']}"
            )
    (OUT / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    # Toys (primary contract verification)
    toy_results = []
    for case in CASES:
        res = analyze_case(case)
        toy_results.append(res)

    (OUT / "lwm_witness_01_toys.json").write_text(json.dumps(toy_results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "top_holes_toys.jsonl", [
        {"case": r["name"], **hole} for r in toy_results for hole in r["top_holes"]
    ])
    write_jsonl(OUT / "near_high_toys.jsonl", [
        {"case": r["name"], **hole} for r in toy_results for hole in r["near_high_support_for_signature_analysis"]
    ])
    write_summary_md(toy_results, ladder_mode=False, filename="summary_toys.md")

    # Ladder (scale check, limited rungs to keep run practical; includes up to last feasible)
    ladder_results = []
    for idx, (p, q) in enumerate(LADDER_RUNGS):
        radius = RADIUS_MULTIPLIER * p
        if radius > MAX_RADIUS:
            break
        case = {"name": f"rung_{idx:02d}_{p}x{q}", "p": p, "q": q, "radius": radius}
        res = analyze_case(case)
        res["seconds"] = 0.0  # timing omitted for isolation focus; prior baseline had it
        ladder_results.append(res)

    (OUT / "lwm_witness_01_ladder.json").write_text(json.dumps(ladder_results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "ladder_rungs.jsonl", ladder_results)
    write_summary_md(ladder_results, ladder_mode=True, filename="summary_ladder.md")

    # Manifest for reproducibility
    manifest = {
        "experiment": "LWM-WITNESS-01",
        "contract": "literal-web-rewind + PGS GWR/DNI sidecar signatures only",
        "toy_cases": [c["name"] for c in CASES],
        "ladder_rungs_run": len(ladder_results),
        "primary_nomination": "flat max thread support (no signature input)",
        "signature_source": "public heldout composites' divisor_count field only",
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"LWM-WITNESS-01 complete. Artifacts in {OUT}")
    print(f"Toys: {len(toy_results)} cases. Ladder rungs: {len(ladder_results)}")


if __name__ == "__main__":
    main()
