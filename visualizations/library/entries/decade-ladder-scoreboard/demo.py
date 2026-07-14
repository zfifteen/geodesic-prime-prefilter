#!/usr/bin/env python3
"""Decade ladder scoreboard from published surface counts in fixtures."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ENTRY_ID = "decade-ladder-scoreboard"
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.data import load_json_fixture  # noqa: E402
from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import save_figure  # noqa: E402
from _common.style import FG, GOLD_BRIGHT, MUTED, apply_library_style  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()
    apply_library_style(plt)

    data = load_json_fixture("surfaces/generator_surfaces.json")
    anchors = data["decade_anchors"]
    per = 256
    # Nominal production form only: constant 256 per decade anchor (not per-decade re-audit).
    labels = [a["label"] for a in anchors]
    xs = np.arange(len(labels))
    heights = np.full(len(labels), per)
    colors = [GOLD_BRIGHT] * len(labels)

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={"width_ratios": [2.2, 1]})
    ax0.bar(xs, heights, color=colors, edgecolor=MUTED, linewidth=0.6)
    ax0.set_xticks(xs)
    ax0.set_xticklabels(labels, rotation=35, ha="right")
    ax0.set_ylabel("nominal primes / decade")
    ax0.set_title("Nominal ladder form (256 / decade anchors)")
    ax0.set_ylim(0, per * 1.2)
    ax0.axhline(per, color=MUTED, linestyle="--", linewidth=0.8)
    ax0.text(
        0.5,
        0.96,
        "schematic of published form · not a live re-audit",
        transform=ax0.transAxes,
        ha="center",
        va="top",
        color=MUTED,
        fontsize=8,
    )

    ladder = next(s for s in data["surfaces"] if s["id"] == "decade_1e8_1e18")
    full = next(s for s in data["surfaces"] if s["id"] == "full_11_1e6")
    names = ["11..1e6\nfull-exact", "1e8..1e18\ndecade ladder"]
    out_n = [full["outputted"], ladder["outputted"]]
    bad = [full["unresolved"] + full["audit_failures"], ladder["unresolved"] + ladder["audit_failures"]]
    ax1.bar([0, 1], out_n, color=GOLD_BRIGHT, label="outputted (fixture)")
    ax1.bar([0, 1], bad, bottom=out_n, color="#ff6b5a", label="unresolved + audit fail")
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(names)
    ax1.set_title("Published totals (fixture mirror)")
    ax1.legend(fontsize=8)
    for i, (o, b) in enumerate(zip(out_n, bad)):
        ax1.text(i, o + b + max(out_n) * 0.02, f"{o}/{o + b}", ha="center", fontsize=9, color=FG)

    fig.suptitle("Generator surface poster (RESULTS.md aggregates via fixture)", color=FG)
    fig.text(
        0.5,
        0.01,
        "Fixture mirrors docs/RESULTS.md. Open committed ladder artifacts for forensic re-audit.",
        ha="center",
        color=MUTED,
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    path = save_figure(
        fig,
        args.out_id,
        meta={
            "status": "measured",
            "kind": "published-surface-scoreboard",
            "ladder_outputted": ladder["outputted"],
            "full_outputted": full["outputted"],
            "includes_10e18_anchor": True,
            "note": "nominal form + fixture totals; not a live ladder re-execution",
        },
        repo_root=REPO_ROOT,
    )
    plt.close(fig)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
