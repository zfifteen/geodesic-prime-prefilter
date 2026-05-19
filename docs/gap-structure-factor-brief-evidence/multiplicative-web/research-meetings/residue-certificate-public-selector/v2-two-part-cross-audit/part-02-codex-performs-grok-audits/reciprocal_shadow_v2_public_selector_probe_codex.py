#!/usr/bin/env python3
"""Codex independent V2 public-selector probe."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
RADIUS = 300
M_LIMIT = 5_000_000

CASES = [
    (23, 31), (43, 59), (61, 83), (89, 113),
    (101, 137), (131, 167), (173, 211), (229, 277),
    (307, 367), (401, 503), (557, 661), (701, 887),
    (1009, 1231), (1601, 2003), (3001, 4001), (5003, 7001),
    (7_500_013, 29_999_989), (6_000_011, 37_499_947),
    (4_500_007, 49_999_991), (3_000_017, 74_999_647),
]


def composite_rows(n, radius):
    rows = []
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        factors = {int(k): int(v) for k, v in factorint(value).items()}
        if factors == {value: 1}:
            continue
        divisor_count = 1
        for exponent in factors.values():
            divisor_count *= exponent + 1
        rows.append({
            "value": value,
            "offset": value - n,
            "side": "left" if value < n else "right",
            "factors": factors,
            "divisor_count": divisor_count,
        })
    return rows


def heldout_rows(n, p, q):
    return [r for r in composite_rows(n, RADIUS) if p not in r["factors"] and q not in r["factors"]]


def with_offset(row, offset):
    copy = dict(row)
    copy["offset"] = offset
    return copy


def rotated_rows(rows):
    ordered = sorted(rows, key=lambda r: int(r["offset"]))
    offsets = [int(r["offset"]) for r in ordered]
    shifted = offsets[1:] + offsets[:1]
    return [with_offset(row, off) for row, off in zip(ordered, shifted, strict=True)]


def factor_signature(row):
    return tuple(sorted((int(k), int(v)) for k, v in row["factors"].items()))


def synthetic_rows(rows):
    ordered = sorted(rows, key=lambda r: (factor_signature(r), int(r["offset"])))
    offsets = sorted(int(r["offset"]) for r in rows)
    return [with_offset(row, off) for row, off in zip(ordered, offsets, strict=True)]


def selected_moduli(rows):
    degree = Counter()
    offsets = defaultdict(list)
    for row in rows:
        off = int(row["offset"])
        for value in row["factors"]:
            r = int(value)
            degree[r] += 1
            offsets[r].append(off)
    chosen = [r for r, _ in sorted(degree.items(), key=lambda item: (-item[1], item[0]))[:4]]
    m = 1
    for r in chosen:
        m *= r
    if m > M_LIMIT:
        chosen = chosen[:3]
        m = 1
        for r in chosen:
            m *= r
    return chosen, m, offsets


def crt_merge(congruences):
    y = 0
    modulus = 1
    steps = []
    for r, b in congruences:
        k = ((b - y) % r) * pow(modulus % r, -1, r) % r
        y = (y + modulus * k) % (modulus * r)
        modulus *= r
        steps.append({"r": r, "b": b, "k": k, "y": y, "modulus": modulus})
    return y, steps


def v1_certificate(rows, case_id, surface, runtime):
    rs, m, offsets = selected_moduli(rows)
    members = []
    for a in range(m):
        congruences = []
        per_r = {}
        for r in rs:
            a_mod = a % r
            if a_mod == 0:
                congruences = []
                break
            inv = pow(a_mod, -1, r)
            b_values = sorted({((-off % r) * inv) % r for off in offsets[r]})
            if len(b_values) != 1:
                congruences = []
                break
            b = b_values[0]
            congruences.append((r, b))
            per_r[str(r)] = {"a_mod_r": a_mod, "inverse": inv, "b": b, "thread_count": len(offsets[r])}
        if not congruences:
            continue
        y, crt = crt_merge(congruences)
        members.append({"a": a, "y": y})
        runtime.append({
            "phase": "v1_crt", "case_id": case_id, "surface": surface,
            "a": a, "M": m, "selected_r": rs, "per_r": per_r, "crt": crt,
        })
    return {"M": m, "selected_r": rs, "cardinality": len(members), "members": members}


def row_summary(row):
    if row is None:
        return None
    return {"value": int(row["value"]), "offset": int(row["offset"]), "divisor_count": int(row["divisor_count"])}


def gwr_witness(rows):
    ordered = sorted(rows, key=lambda r: int(r["offset"]))
    d_min = min(int(r["divisor_count"]) for r in ordered)
    witness = next(r for r in ordered if int(r["divisor_count"]) == d_min)
    t = int(witness["offset"])
    left = [r for r in ordered if int(r["offset"]) < t and int(r["divisor_count"]) <= d_min + 2]
    right = [r for r in ordered if int(r["offset"]) > t and int(r["divisor_count"]) <= d_min + 2]
    support = []
    if left:
        support.append(max(left, key=lambda r: int(r["offset"])))
    if right:
        support.append(min(right, key=lambda r: int(r["offset"])))
    return {
        "d_min": d_min,
        "witness": row_summary(witness),
        "support_rows": [row_summary(r) for r in support],
        "support_offsets": [int(r["offset"]) for r in support],
    }


def deviation(offset, inv_a, m):
    d = (offset * inv_a) % m
    return d, min(d, m - d)


def apply_v2(cert, gwr, case_id, runtime):
    m = cert["M"]
    t_g = int(gwr["witness"]["offset"])
    support_offsets = [int(x) for x in gwr["support_offsets"]]
    for member in cert["members"]:
        a = int(member["a"])
        inv_a = pow(a, -1, m)
        d_primary, dev_primary = deviation(t_g, inv_a, m)
        support_details = []
        support_score = 0
        for offset in support_offsets:
            d_s, dev_s = deviation(offset, inv_a, m)
            support_details.append({"offset": offset, "d": d_s, "dev": dev_s})
            support_score += dev_s
        member.update({
            "inv_a": inv_a,
            "d_primary": d_primary,
            "dev_primary": dev_primary,
            "support_score": support_score,
            "structural_key": [dev_primary, support_score],
        })
        runtime.append({
            "phase": "v2_deviation", "case_id": case_id, "surface": "true",
            "a": a, "M": m, "inv_a": inv_a, "t_g": t_g,
            "d_primary": d_primary, "dev_primary": dev_primary,
            "support_details": support_details, "support_score": support_score,
            "structural_key": [dev_primary, support_score],
        })
    cert["members"].sort(key=lambda item: (item["dev_primary"], item["support_score"], item["a"]))
    current_key = None
    rank = 0
    counts = Counter(tuple(item["structural_key"]) for item in cert["members"])
    for final_rank, item in enumerate(cert["members"], 1):
        key = tuple(item["structural_key"])
        if key != current_key:
            rank += 1
            current_key = key
        item["structural_rank"] = rank
        item["structural_tie_size"] = counts[key]
        item["final_reporting_rank"] = final_rank
        item["is_structural_winner"] = rank == 1 and counts[key] == 1
    winner = next((item for item in cert["members"] if item["is_structural_winner"]), None)
    return {
        "winner_a": None if winner is None else winner["a"],
        "min_structural_tie_size": cert["members"][0]["structural_tie_size"] if cert["members"] else 0,
    }


def classify_aggregate(win_count, controls_empty, implementation_ok=True):
    if not implementation_ok:
        return "unresolved_implementation_failure"
    if not controls_empty or win_count < 14:
        return "invalidated_result"
    if win_count >= 18:
        return "accepted_measured_result"
    return "boundary_measurement"


def run_case(case_id, p, q, cert_rows, runtime):
    n = p * q
    rows = heldout_rows(n, p, q)
    true_cert = v1_certificate(rows, case_id, "true", runtime)
    rot_cert = v1_certificate(rotated_rows(rows), case_id, "rotated", runtime)
    synth_cert = v1_certificate(synthetic_rows(rows), case_id, "synthetic", runtime)
    witness = gwr_witness(rows)
    v2 = apply_v2(true_cert, witness, case_id, runtime)
    p_mod = p % true_cert["M"]
    p_member = next(item for item in true_cert["members"] if item["a"] == p_mod)
    p_wins = bool(p_member["is_structural_winner"])
    for item in true_cert["members"]:
        cert_rows.append({
            "case_id": case_id, "surface": "true", "a": item["a"], "y": item["y"],
            "M": true_cert["M"], "selected_r": true_cert["selected_r"],
            "dev_primary": item["dev_primary"], "support_score": item["support_score"],
            "structural_rank": item["structural_rank"],
            "structural_tie_size": item["structural_tie_size"],
            "final_reporting_rank": item["final_reporting_rank"],
            "p_mod_M": p_mod, "is_p_member": item["a"] == p_mod,
            "is_structural_winner": item["is_structural_winner"],
        })
    return {
        "case_id": case_id, "N": n, "p": p, "q": q, "p_mod_M": p_mod,
        "M": true_cert["M"], "selected_r": true_cert["selected_r"],
        "cardinality_true": true_cert["cardinality"],
        "cardinality_rotated": rot_cert["cardinality"],
        "cardinality_synthetic": synth_cert["cardinality"],
        "gwr_witness": witness["witness"], "support_rows": witness["support_rows"],
        "structural_winner_a": v2["winner_a"],
        "min_structural_tie_size": v2["min_structural_tie_size"],
        "p_is_unique_structural_winner": p_wins,
        "case_classification": "structural_win" if p_wins else "boundary_measurement",
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_summary_md(cases, aggregate):
    lines = [
        "# Codex Part Two V2 Public Selector Probe",
        "",
        "| case | N | p_mod_M | M | |C| | controls | t_g | support | p unique win | tie | winner |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in cases:
        support = ",".join("-" if x is None else str(x["offset"]) for x in row["support_rows"])
        controls = f"{row['cardinality_rotated']}/{row['cardinality_synthetic']}"
        lines.append(
            f"| {row['case_id']} | {row['N']} | {row['p_mod_M']} | {row['M']} | "
            f"{row['cardinality_true']} | {controls} | {row['gwr_witness']['offset']} | "
            f"{support} | {row['p_is_unique_structural_winner']} | "
            f"{row['min_structural_tie_size']} | {row['structural_winner_a']} |"
        )
    lines += [
        "",
        "## Aggregate",
        "",
        f"Structural wins: {aggregate['structural_win_count']} / {aggregate['total_cases']}",
        f"Controls empty on all cases: {aggregate['controls_all_empty']}",
        f"Final classification: `{aggregate['final_classification']}`",
    ]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cert_rows = []
    runtime = []
    cases = [run_case(idx, p, q, cert_rows, runtime) for idx, (p, q) in enumerate(CASES)]
    controls_empty = all(row["cardinality_rotated"] == 0 and row["cardinality_synthetic"] == 0 for row in cases)
    wins = sum(1 for row in cases if row["p_is_unique_structural_winner"])
    aggregate = {
        "total_cases": len(cases),
        "structural_win_count": wins,
        "controls_all_empty": controls_empty,
        "final_classification": classify_aggregate(wins, controls_empty),
    }
    (OUT / "summary.json").write_text(json.dumps({"per_case": cases, "aggregate": aggregate}, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "certificate.jsonl", cert_rows)
    write_jsonl(OUT / "runtime_residue_crt_log.jsonl", runtime)
    write_summary_md(cases, aggregate)
    print(f"wrote {len(cases)} cases, {len(cert_rows)} certificate rows, {len(runtime)} runtime rows")
    print(f"structural wins {wins}/20, classification {aggregate['final_classification']}")


if __name__ == "__main__":
    main()
