#!/usr/bin/env python3
"""Find the measured breakpoint for the current literal-web method."""

from __future__ import annotations

import json
import math
import time
from multiprocessing import Process, Queue
from pathlib import Path

from literal_web_hole_trace import analyze_case, write_jsonl

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "literal_web_breakpoint_ladder"

PER_RUNG_TIMEOUT_SECONDS = 180

COARSE_RUNG_FACTORS = [
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
    (9001, 11003),
    (12007, 14009),
    (16001, 18013),
    (20011, 24001),
    (30011, 36007),
    (40009, 48017),
    (50021, 60013),
    (75011, 90001),
    (100003, 120011),
    (131101, 144203),
    (160001, 180001),
    (200003, 240007),
    (300007, 360007),
    (500009, 600011),
    (750019, 900001),
    (1048583, 1153441),
]

REFINEMENT_RUNG_FACTORS = {
    ((89, 113), (101, 137)): [(97, 127)],
    ((101, 137), (131, 167)): [(113, 149)],
    ((131, 167), (173, 211)): [(151, 191)],
    ((173, 211), (229, 277)): [(199, 251)],
    ((229, 277), (307, 367)): [(269, 331)],
    ((307, 367), (401, 503)): [(353, 431)],
    ((401, 503), (557, 661)): [(479, 587)],
    ((557, 661), (701, 887)): [(631, 773)],
    ((701, 887), (1009, 1231)): [(839, 1031)],
    ((1009, 1231), (1601, 2003)): [(1301, 1601)],
}


def case_name(index, p, q):
    return f"rung_{index:02d}_{p}x{q}"


def exact_factor_hits(result):
    factors = {result["p"], result["q"]}
    hits = []
    for rank, hole in enumerate(result["top_holes"], start=1):
        if abs(hole["offset"]) in factors:
            hits.append({
                "rank": rank,
                "offset": hole["offset"],
                "factor": abs(hole["offset"]),
                "support": hole["support"],
                "audit_kind": hole["audit_kind"],
            })
    return hits


def emitted_offsets(result):
    return [hole["offset"] for hole in result["top_holes"]]


def summarize_success(result, seconds, stage):
    hits = exact_factor_hits(result)
    classification = "success" if hits else "signal_break"
    return {
        "stage": stage,
        "name": result["name"],
        "p": result["p"],
        "q": result["q"],
        "N": result["N"],
        "bits": result["N"].bit_length(),
        "radius": result["radius"],
        "row_count_full": result["row_count_full"],
        "row_count_heldout": result["row_count_heldout"],
        "max_support": result["max_support"],
        "emitted_hole_count": result["emitted_hole_count"],
        "emitted_offsets": emitted_offsets(result),
        "factor_hit": bool(hits),
        "factor_hits": hits,
        "seconds": seconds,
        "classification": classification,
    }


def analyze_worker(case, queue):
    try:
        queue.put(("ok", analyze_case(case)))
    except Exception as exc:
        queue.put(("error", repr(exc)))


def run_case(index, p, q, stage):
    case = {"name": case_name(index, p, q), "p": p, "q": q}
    started = time.perf_counter()
    queue = Queue()
    process = Process(target=analyze_worker, args=(case, queue))
    process.start()
    process.join(PER_RUNG_TIMEOUT_SECONDS)
    seconds = time.perf_counter() - started
    n = p * q

    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "stage": stage,
            "name": case["name"],
            "p": p,
            "q": q,
            "N": n,
            "bits": n.bit_length(),
            "radius": math.isqrt(n),
            "row_count_full": None,
            "row_count_heldout": None,
            "max_support": None,
            "emitted_hole_count": None,
            "emitted_offsets": [],
            "factor_hit": False,
            "factor_hits": [],
            "seconds": seconds,
            "classification": "feasibility_break",
        }

    if queue.empty():
        return {
            "stage": stage,
            "name": case["name"],
            "p": p,
            "q": q,
            "N": n,
            "bits": n.bit_length(),
            "radius": math.isqrt(n),
            "row_count_full": None,
            "row_count_heldout": None,
            "max_support": None,
            "emitted_hole_count": None,
            "emitted_offsets": [],
            "factor_hit": False,
            "factor_hits": [],
            "seconds": seconds,
            "classification": "runner_error",
            "error": "worker exited without result",
        }

    status, payload = queue.get()
    if status == "ok":
        result = payload
        seconds = time.perf_counter() - started
        return summarize_success(result, seconds, stage)

    return {
        "stage": stage,
        "name": case["name"],
        "p": p,
        "q": q,
        "N": n,
        "bits": n.bit_length(),
        "radius": math.isqrt(n),
        "row_count_full": None,
        "row_count_heldout": None,
        "max_support": None,
        "emitted_hole_count": None,
        "emitted_offsets": [],
        "factor_hit": False,
        "factor_hits": [],
        "seconds": seconds,
        "classification": "runner_error",
        "error": payload,
    }


def refine_pairs(last_success, first_break):
    if not last_success or not first_break:
        return []
    key = ((last_success["p"], last_success["q"]), (first_break["p"], first_break["q"]))
    return REFINEMENT_RUNG_FACTORS.get(key, [])


def write_summary(rows):
    last_success = None
    first_break = None
    for row in rows:
        if row["classification"] == "success":
            last_success = row
        elif first_break is None:
            first_break = row

    lines = [
        "# Literal Web Breakpoint Ladder",
        "",
        f"Per-rung feasibility bound: `{PER_RUNG_TIMEOUT_SECONDS}s`.",
        "",
        "Method: `radius = floor(sqrt(N))`; emit the max-support shell; audit checks whether `abs(offset)` equals `p` or `q` after emission.",
        "",
        "| stage | rung | bits | radius | max support | emitted holes | factor hit | seconds | classification |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['stage']} | {row['name']} | {row['bits']} | {row['radius']} | "
            f"{row['max_support'] if row['max_support'] is not None else ''} | "
            f"{row['emitted_hole_count'] if row['emitted_hole_count'] is not None else ''} | "
            f"{'yes' if row['factor_hit'] else 'no'} | {row['seconds']:.3f} | {row['classification']} |"
        )

    lines += ["", "## Breakpoint", ""]
    if first_break:
        lines.append(f"Last success: `{last_success['name']}`." if last_success else "Last success: none.")
        lines.append(f"First break: `{first_break['name']}`.")
        lines.append(f"Break type: `{first_break['classification']}`.")
    else:
        lines.append("No break reached on the tested ladder.")

    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index_html(rows):
    table_rows = []
    for row in rows:
        hit = "yes" if row["factor_hit"] else "no"
        table_rows.append(
            "<tr>"
            f"<td>{row['stage']}</td>"
            f"<td>{row['name']}</td>"
            f"<td>{row['bits']}</td>"
            f"<td>{row['radius']}</td>"
            f"<td>{row['max_support'] if row['max_support'] is not None else ''}</td>"
            f"<td>{row['emitted_hole_count'] if row['emitted_hole_count'] is not None else ''}</td>"
            f"<td>{hit}</td>"
            f"<td>{row['seconds']:.3f}</td>"
            f"<td>{row['classification']}</td>"
            "</tr>"
        )

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Literal Web Breakpoint Ladder</title>
<style>
body {{ margin:0; background:#fbfcfd; color:#1f2933; font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:28px 20px 56px; }}
h1 {{ font-size:1.8rem; margin:0 0 8px; }}
table {{ width:100%; border-collapse:collapse; font-size:12px; margin-top:14px; }}
th, td {{ border:1px solid #d8dee6; padding:6px 8px; text-align:left; }}
th {{ background:#f4f6f8; }}
code {{ background:#f1f5f9; padding:1px 4px; border-radius:3px; }}
</style>
</head>
<body>
<main>
<h1>Literal Web Breakpoint Ladder</h1>
<p>Measures the first rung where the current literal-web max-support shell no longer emits <code>p</code> or <code>q</code>, or where direct composite factoring becomes infeasible.</p>
<table>
<tr><th>stage</th><th>rung</th><th>bits</th><th>radius</th><th>max support</th><th>emitted holes</th><th>factor hit</th><th>seconds</th><th>classification</th></tr>
{''.join(table_rows)}
</table>
</main>
</body>
</html>
"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


def write_outputs(rows):
    (OUT / "rungs.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "rungs.jsonl", rows)
    write_summary(rows)
    write_index_html(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    last_success = None
    first_break = None

    for index, (p, q) in enumerate(COARSE_RUNG_FACTORS):
        row = run_case(index, p, q, "coarse")
        rows.append(row)
        write_outputs(rows)
        if row["classification"] == "success":
            last_success = row
            continue
        first_break = row
        break

    if first_break:
        for refine_index, (p, q) in enumerate(refine_pairs(last_success, first_break), start=len(rows)):
            row = run_case(refine_index, p, q, "refine")
            rows.append(row)
            write_outputs(rows)
            if row["classification"] == "success":
                last_success = row
            else:
                first_break = row
                break

    write_outputs(rows)
    print(f"wrote {len(rows)} breakpoint rows to {OUT}")


if __name__ == "__main__":
    main()
