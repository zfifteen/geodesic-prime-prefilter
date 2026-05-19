#!/usr/bin/env python3
"""Reciprocal shadow V2 public selector probe (Part One - Grok performs).

V2 experiment: frozen V1 certificate layer (conflict-check + CRT on held-out
threads) + GWR leftmost minimum-divisor witness extraction + public reciprocal
deviation ranking over the true certificate only.

This script is self-contained. It reproduces the V1 certificate generator
exactly (selected [2,3,5,7] -> M=210 on this surface) then applies the exact
V2 ranking rule from residue_certificate_v2_public_selector_contract.html.

p and q appear ONLY inside build_case (for N construction and direct-row hold-out)
and in the final post-ranking audit block (p % M membership after all scores exist).
No hidden factors, no candidate intervals, no gcd, no divisibility gates inside
certificate generation or V2 ranking.

Controls: rotated-offset (cyclic) and deterministic synthetic-offset (factor-sig sort).
Both must remain empty at the certificate layer for any admissible result.

Required outputs: summary.json, certificate.jsonl (true only), runtime_residue_crt_log.jsonl
(with V1 CRT + V2 deviation records), summary.md, plus the two MDs at folder root.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from itertools import groupby
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Core web construction (exact copy of audited V1 reference for bit-identity)
# ---------------------------------------------------------------------------


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def factorization(n: int) -> dict[int, int]:
    value = n
    factors: dict[int, int] = {}
    if value % 2 == 0:
        cnt = 0
        while value % 2 == 0:
            cnt += 1
            value //= 2
        factors[2] = cnt
    if value % 3 == 0:
        cnt = 0
        while value % 3 == 0:
            cnt += 1
            value //= 3
        factors[3] = cnt
    d = 5
    while d * d <= value:
        if value % d == 0:
            cnt = 0
            while value % d == 0:
                cnt += 1
                value //= d
            factors[d] = cnt
        d += 2
        if d * d <= value and value % d == 0:
            cnt = 0
            while value % d == 0:
                cnt += 1
                value //= d
            factors[d] = cnt
        d += 4
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def composite_rows(n_value: int, radius: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for value in range(n_value - radius, n_value + radius + 1):
        if value < 4 or value == n_value or is_prime(value):
            continue
        factors = factorization(value)
        rows.append(
            {
                "value": value,
                "offset": value - n_value,
                "factors": factors,
                "divisor_count": int(math.prod((e + 1) for e in factors.values())),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Control row generators (exact deterministic copies)
# ---------------------------------------------------------------------------


def rotated_offset_control_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    offsets = [int(row["offset"]) for row in rows]
    rotated_offsets = offsets[1:] + offsets[:1]
    out = []
    for row, off in zip(rows, rotated_offsets, strict=True):
        copied = {k: v for k, v in row.items() if k != "offset"}
        copied["offset"] = off
        out.append(copied)
    return out


def deterministic_synthetic_offset_control_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deterministic synthetic: reorder by canonical factor signature, assign
    consecutive centered offsets. Destroys true offset pairing while preserving
    r multiset. No randomness.
    """
    if not rows:
        return []
    def factor_sig(row: dict[str, Any]) -> tuple[tuple[int, int], ...]:
        fac = row["factors"]
        return tuple(sorted((int(k), int(v)) for k, v in fac.items()))
    ordered = sorted(rows, key=factor_sig)
    n = len(ordered)
    synth_offs = list(range(-n // 2, -n // 2 + n))
    out = []
    for row, off in zip(ordered, synth_offs, strict=True):
        copied = {k: v for k, v in row.items() if k != "offset"}
        copied["offset"] = off
        out.append(copied)
    return out


# ---------------------------------------------------------------------------
# V1 certificate generator (frozen, exact from cross-audited V1 implementation)
# ---------------------------------------------------------------------------


def compute_residue_certificate(
    heldout_rows: list[dict[str, Any]],
    log_entries: list[dict[str, Any]],
    case_id: str,
    surface: str,
) -> dict[str, Any]:
    """Exact V1: top-4 (or 3) r by degree, per-a conflict check on b_r
    agreement, CRT merge when every selected r has exactly one b.
    Only thread-derived data; no p/q/N inside after caller.
    """
    degree: Counter[int] = Counter()
    r_to_offsets: dict[int, list[int]] = defaultdict(list)
    for row in heldout_rows:
        off = int(row["offset"])
        for r in row.get("factors", {}):
            r = int(r)
            degree[r] += 1
            r_to_offsets[r].append(off)

    if not degree:
        return {"M": 1, "selected_rs": [], "admissible": [], "cardinality": 0}

    sorted_r = sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))
    top4 = [r for r, _ in sorted_r[:4]]
    M = 1
    for r in top4:
        M *= r
    if M > 5_000_000:
        selected_rs = [r for r, _ in sorted_r[:3]]
        M = 1
        for r in selected_rs:
            M *= r
    else:
        selected_rs = top4

    if not selected_rs:
        return {"M": 1, "selected_rs": [], "admissible": [], "cardinality": 0}

    admissible: list[dict[str, Any]] = []

    for a in range(M):
        b_per_r: dict[int, int] = {}
        per_r_details: dict[int, Any] = {}
        conflict = False
        for r in selected_rs:
            offsets = r_to_offsets[r]
            a_r = a % r
            if a_r == 0:
                conflict = True
                break
            try:
                inv = pow(a_r, -1, r)
            except ValueError:
                conflict = True
                break
            b_set: set[int] = set()
            for off in offsets:
                b = ((-off % r) * inv) % r
                b_set.add(b)
            if len(b_set) != 1:
                conflict = True
                break
            b = next(iter(b_set))
            b_per_r[r] = b
            per_r_details[r] = {
                "a_r": a_r,
                "inv": inv,
                "b": b,
                "num_threads": len(offsets),
            }
        if conflict:
            continue

        # CRT merge
        y = 0
        mod_so_far = 1
        crt_steps: list[dict[str, Any]] = []
        for r in selected_rs:
            b = b_per_r[r]
            diff = (b - y) % r
            inv_mod = pow(mod_so_far % r, -1, r)
            k = (diff * inv_mod) % r
            y = (y + mod_so_far * k) % (mod_so_far * r)
            crt_steps.append(
                {
                    "r": r,
                    "b": b,
                    "mod_before": mod_so_far,
                    "k": k,
                    "y_after": y,
                    "M_after": mod_so_far * r,
                }
            )
            mod_so_far *= r

        entry = {
            "a": a,
            "y": y,
            "M": M,
            "selected_rs": selected_rs,
        }
        admissible.append(entry)

        log_entries.append(
            {
                "case_id": case_id,
                "surface": surface,
                "phase": "v1_crt",
                "a": a,
                "y": y,
                "M": M,
                "selected_rs": selected_rs,
                "per_r": per_r_details,
                "crt_steps": crt_steps,
            }
        )

    # V1 legacy sort (score constant, then a asc) - will be replaced by V2 sort on true
    admissible.sort(key=lambda x: (x["a"]))
    for rank, item in enumerate(admissible, 1):
        item["v1_rank"] = rank

    return {
        "M": M,
        "selected_rs": selected_rs,
        "admissible": admissible,
        "cardinality": len(admissible),
    }


# ---------------------------------------------------------------------------
# Build case (p/q confined to construction + hold-out only)
# ---------------------------------------------------------------------------


def build_case(p: int, q: int, radius: int) -> dict[str, Any]:
    """N = p*q, composite rows, hold out any row containing p or q as factor.
    Returns only row lists (true heldout + two control variants). p/q do not
    escape except to the caller's final audit after certificates and scores.
    """
    N = p * q
    rows = composite_rows(N, radius)
    heldout = [
        row
        for row in rows
        if p not in row["factors"] and q not in row["factors"]
    ]
    rotated = rotated_offset_control_rows(heldout)
    synth = deterministic_synthetic_offset_control_rows(heldout)
    return {
        "N": N,
        "heldout_rows": heldout,
        "rotated_rows": rotated,
        "synth_rows": synth,
        "heldout_count": len(heldout),
        "direct_removed": len(rows) - len(heldout),
    }


# ---------------------------------------------------------------------------
# V2 GWR witness + ranking (public, after V1 certificate exists)
# ---------------------------------------------------------------------------


def extract_gwr_witness(heldout_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Exact Section 6 of V2 contract.
    Sort held-out rows by offset ascending.
    d_min = min divisor_count.
    g = first (leftmost) row with divisor_count == d_min; t_g = its offset.
    Left support = nearest (max offset < t_g) row with divisor_count <= d_min+2.
    Right support = nearest (min offset > t_g) row with divisor_count <= d_min+2.
    Supports may be 0, 1, or 2 rows.
    """
    if not heldout_rows:
        return {
            "t_g": 0,
            "d_min": 0,
            "g": None,
            "left_support": None,
            "right_support": None,
            "support_offsets": [],
        }
    sorted_rows = sorted(heldout_rows, key=lambda r: int(r["offset"]))
    d_min = min(int(r["divisor_count"]) for r in sorted_rows)
    g = None
    for r in sorted_rows:
        if int(r["divisor_count"]) == d_min:
            g = r
            break
    t_g = int(g["offset"])

    left_cand = [
        r for r in sorted_rows
        if int(r["offset"]) < t_g and int(r["divisor_count"]) <= d_min + 2
    ]
    left_support = max(left_cand, key=lambda r: int(r["offset"])) if left_cand else None

    right_cand = [
        r for r in sorted_rows
        if int(r["offset"]) > t_g and int(r["divisor_count"]) <= d_min + 2
    ]
    right_support = min(right_cand, key=lambda r: int(r["offset"])) if right_cand else None

    support_offsets: list[int] = []
    if left_support:
        support_offsets.append(int(left_support["offset"]))
    if right_support:
        support_offsets.append(int(right_support["offset"]))

    def row_to_dict(r: dict[str, Any] | None) -> dict[str, Any] | None:
        if r is None:
            return None
        return {
            "value": int(r["value"]),
            "offset": int(r["offset"]),
            "divisor_count": int(r["divisor_count"]),
        }

    return {
        "t_g": t_g,
        "d_min": d_min,
        "g": row_to_dict(g),
        "left_support": row_to_dict(left_support),
        "right_support": row_to_dict(right_support),
        "support_offsets": support_offsets,
    }


def apply_v2_ranking(
    admissible: list[dict[str, Any]],
    gwr: dict[str, Any],
    M: int,
    log_entries: list[dict[str, Any]],
    case_id: str,
) -> dict[str, Any]:
    """Exact V2 deviation ranking (Sections 7-8 of contract) applied only to
    the non-empty true certificate. Computes inv_a, dev_primary from t_g,
    support_score from the (at most two) support offsets, structural key
    (dev_primary, support_score). Sorts, assigns dense structural ranks per
    distinct key + tie sizes, final reporting ranks by (key, a). Emits V2
    log records for every true residue. Returns min-key info for winner audit.
    """
    if not admissible or M <= 1:
        return {
            "min_struct_key": None,
            "min_tie_size": 0,
            "unique_structural_winner_a": None,
            "is_unique_win": False,
        }

    t_g = int(gwr["t_g"])
    support_offsets: list[int] = [int(x) for x in gwr["support_offsets"]]

    for item in admissible:
        a = int(item["a"])
        inv_a = pow(a, -1, M)
        d_primary = (t_g * inv_a) % M
        dev_primary = min(d_primary, M - d_primary)
        support_score = 0
        for ts in support_offsets:
            d_s = (ts * inv_a) % M
            dev_s = min(d_s, M - d_s)
            support_score += dev_s
        item["inv_a"] = inv_a
        item["d_primary"] = d_primary
        item["dev_primary"] = dev_primary
        item["support_score"] = support_score
        item["_struct_key"] = (dev_primary, support_score)

    # Sort by structural key then a (reporting order)
    admissible.sort(key=lambda x: (x["_struct_key"], x["a"]))

    for rank, item in enumerate(admissible, 1):
        item["final_reporting_rank"] = rank

    # Group by exact structural key for tie sizes and dense structural ranks
    struct_groups: list[tuple[tuple[int, int], int, list[dict[str, Any]]]] = []
    for key, g_iter in groupby(admissible, key=lambda x: x["_struct_key"]):
        g_list = list(g_iter)
        sz = len(g_list)
        for it in g_list:
            it["structural_tie_size"] = sz
        struct_groups.append((key, sz, g_list))

    for srank, (key, sz, g_list) in enumerate(struct_groups, 1):
        for it in g_list:
            it["structural_rank"] = srank

    min_key, min_sz, min_g_list = struct_groups[0]
    unique_winner_a = min_g_list[0]["a"] if min_sz == 1 else None

    for item in admissible:
        is_win = (item["_struct_key"] == min_key and min_sz == 1)
        item["is_structural_winner"] = is_win

    # V2 deviation audit log (one per true residue)
    for item in admissible:
        log_entries.append(
            {
                "case_id": case_id,
                "surface": "true_web",
                "phase": "v2_deviation",
                "a": item["a"],
                "M": M,
                "t_g": t_g,
                "support_offsets": support_offsets,
                "inv_a": item["inv_a"],
                "d_primary": item["d_primary"],
                "dev_primary": item["dev_primary"],
                "support_score": item["support_score"],
                "structural_key": [item["dev_primary"], item["support_score"]],
                "structural_rank": item["structural_rank"],
                "structural_tie_size": item["structural_tie_size"],
                "final_reporting_rank": item["final_reporting_rank"],
                "is_structural_winner": item["is_structural_winner"],
            }
        )

    # cleanup temp key
    for item in admissible:
        if "_struct_key" in item:
            del item["_struct_key"]

    return {
        "min_struct_key": min_key,
        "min_tie_size": min_sz,
        "unique_structural_winner_a": unique_winner_a,
        "is_unique_win": min_sz == 1,
    }


# ---------------------------------------------------------------------------
# Case list (exact 20 from V2 contract / V1 surface)
# ---------------------------------------------------------------------------

CASES: list[tuple[int, int]] = [
    (23, 31), (43, 59), (61, 83), (89, 113),
    (101, 137), (131, 167), (173, 211), (229, 277),
    (307, 367), (401, 503), (557, 661), (701, 887),
    (1009, 1231), (1601, 2003), (3001, 4001), (5003, 7001),
    (7500013, 29999989), (6000011, 37499947),
    (4500007, 49999991), (3000017, 74999647),
]

FIXED_RADIUS = 300


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    out_dir = base_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_case_summaries: list[dict[str, Any]] = []
    all_cert_rows: list[dict[str, Any]] = []
    runtime_log_for_write: list[dict[str, Any]] = []

    for idx, (p, q) in enumerate(CASES):
        built = build_case(p, q, FIXED_RADIUS)

        logs: list[dict[str, Any]] = []
        cert_true = compute_residue_certificate(
            built["heldout_rows"], logs, f"case{idx}_true", "true_web"
        )
        cert_rot = compute_residue_certificate(
            built["rotated_rows"], logs, f"case{idx}_rot", "rotated_offset_control"
        )
        cert_synth = compute_residue_certificate(
            built["synth_rows"], logs, f"case{idx}_synth", "synthetic_offset_control"
        )

        # V2 ranking ONLY on true (controls are empty on this surface)
        gwr_info: dict[str, Any] = {}
        v2_info: dict[str, Any] = {
            "min_tie_size": 0,
            "is_unique_win": False,
            "unique_structural_winner_a": None,
        }
        p_is_struct_winner = False
        pmod = 0
        winner_a = None
        num_tied_min = 0

        M = cert_true["M"]
        selected_r = cert_true["selected_rs"]

        if cert_true["cardinality"] > 0 and M > 1:
            gwr_info = extract_gwr_witness(built["heldout_rows"])
            v2_info = apply_v2_ranking(
                cert_true["admissible"], gwr_info, M, logs, f"case{idx}_true"
            )
            num_tied_min = v2_info["min_tie_size"]
            if v2_info["is_unique_win"]:
                winner_a = v2_info["unique_structural_winner_a"]

            pmod = p % M
            for item in cert_true["admissible"]:
                if item["a"] == pmod:
                    p_is_struct_winner = bool(item.get("is_structural_winner", False))
                    break

        controls_nonempty = cert_rot["cardinality"] > 0 or cert_synth["cardinality"] > 0
        case_class = (
            "invalidated_result" if controls_nonempty
            else ("structural_win" if p_is_struct_winner else "boundary_measurement")
        )

        summary = {
            "case_idx": idx,
            "N": built["N"],
            "p": p,
            "q": q,
            "radius": FIXED_RADIUS,
            "p_mod_M": pmod,
            "M": M,
            "selected_r": selected_r,
            "cardinality_true": cert_true["cardinality"],
            "cardinality_rot": cert_rot["cardinality"],
            "cardinality_synth": cert_synth["cardinality"],
            "gwr_witness": gwr_info.get("g"),
            "support_rows": [gwr_info.get("left_support"), gwr_info.get("right_support")],
            "p_is_unique_structural_winner": p_is_struct_winner,
            "structural_winner_a": winner_a,
            "min_structural_tie_size": num_tied_min,
            "v2_classification": case_class,
        }
        all_case_summaries.append(summary)

        # certificate.jsonl: only true certificate residues (per V2 spec)
        for item in cert_true["admissible"]:
            all_cert_rows.append(
                {
                    "case_id": f"case{idx}",
                    "surface": "true_web",
                    "a": item["a"],
                    "y": item["y"],
                    "M": M,
                    "selected_r": selected_r,
                    "dev_primary": item["dev_primary"],
                    "support_score": item["support_score"],
                    "structural_rank": item["structural_rank"],
                    "structural_tie_size": item["structural_tie_size"],
                    "final_reporting_rank": item["final_reporting_rank"],
                    "p_mod_M": pmod,
                    "is_p_member": item["a"] == pmod,
                    "is_structural_winner": item["is_structural_winner"],
                }
            )

        # runtime log already received V1 entries from compute + V2 from apply
        runtime_log_for_write.extend(logs)

        print(
            f"case {idx}: N={built['N']} M={M} |C_true|={cert_true['cardinality']} "
            f"p_win={p_is_struct_winner} tie={num_tied_min} class={case_class}"
        )

    # aggregate classification per V2 contract table
    structural_wins = sum(
        1 for s in all_case_summaries if s["p_is_unique_structural_winner"]
    )
    controls_all_empty = all(
        s["cardinality_rot"] == 0 and s["cardinality_synth"] == 0
        for s in all_case_summaries
    )
    if not controls_all_empty:
        final_classification = "invalidated_result"
    elif structural_wins >= 18:
        final_classification = "accepted_measured_result"
    elif structural_wins >= 14:
        final_classification = "boundary_measurement"
    else:
        final_classification = "invalidated_result"

    aggregate = {
        "structural_win_count": structural_wins,
        "final_classification": final_classification,
        "total_cases": 20,
        "controls_all_empty": controls_all_empty,
        "note": "V2 structural win requires unique minimal (dev_primary, support_score) with tie_size==1; a tie-break does not count as structural win.",
    }

    # write summary.json (object with per_case + aggregate)
    summary_data = {"per_case": all_case_summaries, "aggregate": aggregate}
    (out_dir / "summary.json").write_text(
        json.dumps(summary_data, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    # certificate.jsonl (true only, V2 augmented)
    cert_path = out_dir / "certificate.jsonl"
    cert_path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in all_cert_rows),
        encoding="utf-8",
    )

    # runtime_residue_crt_log.jsonl (V1 crt + V2 deviation)
    log_path = out_dir / "runtime_residue_crt_log.jsonl"
    log_path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in runtime_log_for_write),
        encoding="utf-8",
    )

    # summary.md written by script
    write_summary_md(out_dir / "summary.md", all_case_summaries, aggregate)

    print(f"\nWrote outputs to {out_dir}")
    print(f"Total cases: {len(all_case_summaries)}")
    print(f"Total true cert rows (V2): {len(all_cert_rows)}")
    print(f"Total runtime log entries: {len(runtime_log_for_write)}")
    print(f"Structural wins (unique by (dev,support)): {structural_wins}/20")
    print(f"Final classification: {final_classification}")


def write_summary_md(
    path: Path, summaries: list[dict[str, Any]], aggregate: dict[str, Any]
) -> None:
    lines: list[str] = [
        "# V2 Public Selector Probe - Grok Part One (reciprocal_shadow_v2_public_selector_probe_grok.py)",
        "",
        "Controlling contract: residue_certificate_v2_public_selector_contract.html",
        "V1 certificate layer reproduced exactly (conflict + CRT). V2 GWR + deviation ranking applied only to true certificate.",
        "No files written outside the designated Part One folder.",
        "",
        "## Per-Case Surface (20 cases, radius=300, M from top-4 held-out thread degrees)",
        "",
        "| idx | N | p | p_mod_M | M | sel_r | |C_t| | |C_r| | |C_s| | t_g | d_min | supports | p_struct_win | tie | winner_a | class |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in summaries:
        g = s.get("gwr_witness") or {}
        t_g = g.get("offset", "?")
        d_min = g.get("divisor_count", "?")
        sup = s.get("support_rows") or [None, None]
        sup_str = ",".join(
            str(x["offset"]) if x else "-" for x in sup
        )
        lines.append(
            f"| {s['case_idx']} | {s['N']} | {s['p']} | {s['p_mod_M']} | {s['M']} | {s['selected_r']} | "
            f"{s['cardinality_true']} | {s['cardinality_rot']} | {s['cardinality_synth']} | "
            f"{t_g} | {d_min} | {sup_str} | {s['p_is_unique_structural_winner']} | "
            f"{s['min_structural_tie_size']} | {s['structural_winner_a']} | {s['v2_classification']} |"
        )

    wins = aggregate["structural_win_count"]
    final = aggregate["final_classification"]
    lines.extend(
        [
            "",
            "## Aggregate Result (V2 contract classification table)",
            "",
            f"Structural wins (p % M is unique minimal (dev_primary, support_score) with tie_size=1): {wins}/20",
            f"Both controls empty at certificate layer on all 20 cases: {aggregate['controls_all_empty']}",
            f"Final classification under V2 table: **{final}**",
            "",
            "Hypothesis under test: the public GWR leftmost-min-divisor reciprocal deviation ranking",
            "over the V1 certificate produces a tight selector in which true p % M is the unique",
            "structural winner on 18-20 of the 20 cases (with controls remaining empty).",
            "",
            "Raw artifacts (summary.json, certificate.jsonl, runtime_residue_crt_log.jsonl) were",
            "written by the probe before this summary or any interpretive document.",
            "",
            "See self_checklist.md for the 14-item contract verification and grok_execution_notes.md",
            "for hypothesis / measured / audit separation.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
