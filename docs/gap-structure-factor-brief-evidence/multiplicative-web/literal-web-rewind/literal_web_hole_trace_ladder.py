#!/usr/bin/env python3
"""Scale the literal web hole-trace method until signal or feasibility fails."""

from __future__ import annotations

import json
import time
from pathlib import Path

from literal_web_hole_trace import analyze_case, write_jsonl

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "literal_web_hole_trace_ladder"

RADIUS_MULTIPLIER = 6
TOP_K = 18
MAX_RADIUS = 50_000

RUNG_FACTORS = [
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
    (7_500_013, 29_999_989),
]


def classify(result):
    if result["direct_row_count"] < TOP_K:
        return "boundary_measurement"
    if result["top18_direct_hits"] == TOP_K:
        return "works"
    return "signal_failure"


def rung_case(index, p, q):
    radius = RADIUS_MULTIPLIER * p
    return {"name": f"rung_{index:02d}_{p}x{q}", "p": p, "q": q, "radius": radius}


def write_summary(rows, stop):
    lines = [
        "# Literal Web Hole Trace Ladder",
        "",
        f"Scaling rule: `radius = {RADIUS_MULTIPLIER} * p`.",
        f"Signal rule: top {TOP_K} supported holes must all be held-out `p/q` thread rows.",
        f"Feasibility stop: do not run a rung requiring radius > {MAX_RADIUS}.",
        "",
        "| rung | p | q | radius | direct rows | supported direct | top18 direct hits | seconds | status |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['name']} | {row['p']} | {row['q']} | {row['radius']} | "
            f"{row['direct_row_count']} | {row['supported_direct_count']} | "
            f"{row['top18_direct_hits']} | {row['seconds']:.3f} | {row['status']} |"
        )
    lines += ["", "## Stop", "", stop]
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    stop = "No stop reached."
    for index, (p, q) in enumerate(RUNG_FACTORS):
        case = rung_case(index, p, q)
        if case["radius"] > MAX_RADIUS:
            stop = (
                f"Stopped before {case['name']}: required radius {case['radius']} exceeds "
                f"MAX_RADIUS {MAX_RADIUS}. Literal hole tracing needs a window that reaches "
                "the hidden-thread offsets; at this rung the direct sweep becomes the limiting factor."
            )
            break
        started = time.perf_counter()
        result = analyze_case(case)
        result["seconds"] = time.perf_counter() - started
        result["status"] = classify(result)
        rows.append(result)
        if result["status"] != "works":
            stop = f"Stopped at {result['name']}: status {result['status']}."
            break

    (OUT / "rungs.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "rungs.jsonl", rows)
    write_summary(rows, stop)
    print(stop)


if __name__ == "__main__":
    main()
