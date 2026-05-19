#!/usr/bin/env python3
"""Codex independent residue-certificate probe for the cross-audit experiment."""

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


def clone_with_offset(row, offset):
    out = dict(row)
    out["offset"] = offset
    return out


def rotated_rows(rows):
    ordered = sorted(rows, key=lambda r: int(r["offset"]))
    offsets = [int(r["offset"]) for r in ordered]
    shifted = offsets[1:] + offsets[:1]
    return [clone_with_offset(row, off) for row, off in zip(ordered, shifted, strict=True)]


def factor_signature(row):
    return tuple(sorted((int(k), int(v)) for k, v in row["factors"].items()))


def synthetic_rows(rows):
    ordered = sorted(rows, key=lambda r: (factor_signature(r), int(r["offset"])))
    offsets = sorted(int(r["offset"]) for r in rows)
    return [clone_with_offset(row, off) for row, off in zip(ordered, offsets, strict=True)]


def heldout_rows(n, p, q):
    rows = composite_rows(n, RADIUS)
    return [r for r in rows if p not in r["factors"] and q not in r["factors"]]


def selected_moduli(rows):
    degree = Counter()
    offsets = defaultdict(list)
    for row in rows:
        off = int(row["offset"])
        for r in row["factors"]:
            r = int(r)
            degree[r] += 1
            offsets[r].append(off)
    ranked = [r for r, _ in sorted(degree.items(), key=lambda item: (-item[1], item[0]))]
    chosen = ranked[:4]
    product = 1
    for r in chosen:
        product *= r
    if product > M_LIMIT:
        chosen = chosen[:3]
        product = 1
        for r in chosen:
            product *= r
    return chosen, product, offsets


def merge_crt(congruences):
    y = 0
    modulus = 1
    steps = []
    for r, b in congruences:
        delta = (b - y) % r
        k = (delta * pow(modulus % r, -1, r)) % r
        y = (y + modulus * k) % (modulus * r)
        modulus *= r
        steps.append({"r": r, "b": b, "k": k, "y": y, "modulus": modulus})
    return y, steps


def certificate(rows, case_id, surface, log_rows):
    rs, mod, offsets_by_r = selected_moduli(rows)
    cert = []
    for a in range(mod):
        congruences = []
        per_r = {}
        for r in rs:
            if a % r == 0:
                congruences = []
                break
            inv = pow(a % r, -1, r)
            residues = sorted({((-off % r) * inv) % r for off in offsets_by_r[r]})
            if len(residues) != 1:
                congruences = []
                break
            b = residues[0]
            congruences.append((r, b))
            per_r[str(r)] = {"a_mod_r": a % r, "inverse": inv, "b": b, "threads": len(offsets_by_r[r])}
        if not congruences:
            continue
        y, steps = merge_crt(congruences)
        entry = {"a": a, "y": y, "score": 1.0, "rank": len(cert) + 1}
        cert.append(entry)
        log_rows.append({
            "case_id": case_id, "surface": surface, "a": a, "M": mod,
            "selected_r": rs, "per_r": per_r, "crt": steps,
        })
    return {"M": mod, "selected_r": rs, "cardinality": len(cert), "members": cert}


def audit_membership(cert, p):
    if cert["M"] == 0:
        return False, None, None
    target = p % cert["M"]
    for item in cert["members"]:
        if item["a"] == target:
            return True, item["rank"], target
    return False, None, target


def classify(true_cert, rot_cert, synth_cert, true_hit, true_rank, rot_hit, synth_hit):
    if not true_hit or true_cert["cardinality"] > 64:
        return "invalidated_result"
    if true_rank is None or true_rank > 3:
        return "boundary_measurement"
    if rot_hit or synth_hit:
        return "invalidated_result"
    return "accepted_measured_result"


def run_case(idx, p, q, cert_rows, runtime_rows):
    n = p * q
    rows = heldout_rows(n, p, q)
    true_cert = certificate(rows, idx, "true", runtime_rows)
    rot_cert = certificate(rotated_rows(rows), idx, "rotated", runtime_rows)
    synth_cert = certificate(synthetic_rows(rows), idx, "synthetic", runtime_rows)
    true_hit, true_rank, pmod = audit_membership(true_cert, p)
    rot_hit, rot_rank, _ = audit_membership(rot_cert, p)
    synth_hit, synth_rank, _ = audit_membership(synth_cert, p)
    status = classify(true_cert, rot_cert, synth_cert, true_hit, true_rank, rot_hit, synth_hit)
    for surface, cert in (("true", true_cert), ("rotated", rot_cert), ("synthetic", synth_cert)):
        for item in cert["members"]:
            cert_rows.append({
                "case_id": idx, "surface": surface, "a": item["a"], "y": item["y"],
                "rank": item["rank"], "M": cert["M"], "selected_r": cert["selected_r"],
                "is_p_member": item["a"] == pmod, "p_mod_M": pmod,
            })
    return {
        "case_id": idx, "N": n, "p": p, "q": q, "p_over_sqrtN": round((p / q) ** 0.5, 6),
        "true": {k: true_cert[k] for k in ("M", "selected_r", "cardinality")},
        "rotated": {k: rot_cert[k] for k in ("M", "selected_r", "cardinality")},
        "synthetic": {k: synth_cert[k] for k in ("M", "selected_r", "cardinality")},
        "p_mod_M": pmod, "p_in_true": true_hit, "p_rank_true": true_rank,
        "p_in_rotated": rot_hit, "p_rank_rotated": rot_rank,
        "p_in_synthetic": synth_hit, "p_rank_synthetic": synth_rank,
        "classification": status,
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


def write_summary_md(cases):
    lines = ["# Codex Part Two Residue Certificate Probe", "", "| case | N | p/sqrtN | M | r | |C| | p rank | rot | synth | classification |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in cases:
        lines.append(f"| {row['case_id']} | {row['N']} | {row['p_over_sqrtN']:.4f} | {row['true']['M']} | {row['true']['selected_r']} | {row['true']['cardinality']} | {row['p_rank_true']} | {row['rotated']['cardinality']} | {row['synthetic']['cardinality']} | {row['classification']} |")
    lines += ["", "## Observed Boundary", "", "Every case selected `[2, 3, 5, 7]`, so `M = 210`. The true certificate contains the 48 residues coprime to 210. Both controls emit empty certificates. This reproduces the structural boundary seen in Part One and does not nominate a tight factor residue."]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cert_rows, runtime_rows = [], []
    cases = [run_case(i, p, q, cert_rows, runtime_rows) for i, (p, q) in enumerate(CASES)]
    (OUT / "summary.json").write_text(json.dumps({"cases": cases}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(OUT / "certificate.jsonl", cert_rows)
    write_jsonl(OUT / "runtime_residue_crt_log.jsonl", runtime_rows)
    write_summary_md(cases)
    print(f"wrote {len(cases)} cases, {len(cert_rows)} certificate rows, {len(runtime_rows)} runtime rows")


if __name__ == "__main__":
    main()
