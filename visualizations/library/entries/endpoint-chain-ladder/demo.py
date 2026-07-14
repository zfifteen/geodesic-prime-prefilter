#!/usr/bin/env python3
"""Endpoint-chain / modulus-link ladder schematic (public toy numbers)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ENTRY_ID = "endpoint-chain-ladder"
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import save_figure  # noqa: E402
from _common.style import BG, FG, GOLD_BRIGHT, GRAPHITE, MUTED, apply_library_style  # noqa: E402


def box(ax, xy, w, h, text, face=GRAPHITE):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        edgecolor=GOLD_BRIGHT,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=FG, fontsize=10, wrap=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()
    apply_library_style(plt)

    # Toy public illustration only: N = 15 = 3*5 style messaging without claiming a solver.
    # Use abstract labels to avoid classical factor-search framing.
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(BG)
    fig.patch.set_facecolor(BG)

    stages = [
        (0.05, 0.62, "1. Locked PGS\nendpoint chain\n(upper chamber facts)"),
        (0.28, 0.62, "2. Floor transport\nthrough modulus N\nz = floor(N / endpoint)"),
        (0.51, 0.62, "3. Reciprocal\nendpoint closure\n(lower chamber)"),
        (0.74, 0.62, "4. Residual class\nor structural\ncertificate"),
    ]
    for x, y, text in stages:
        box(ax, (x, y), 0.20, 0.28, text)

    for i in range(3):
        x1 = 0.05 + 0.23 * i + 0.20
        x2 = 0.05 + 0.23 * (i + 1)
        ax.annotate(
            "",
            xy=(x2, 0.76),
            xytext=(x1, 0.76),
            arrowprops=dict(arrowstyle="->", color=GOLD_BRIGHT, lw=1.6),
        )

    box(
        ax,
        (0.15, 0.12),
        0.70,
        0.32,
        "Resolved: certificate commits public chamber facts.\n"
        "Unresolved: residual remains; do not invent factors.\n"
        "Frame: endpoint chain → transport → reciprocal → residual/certificate\n"
        "(not classical gcd / trial division / primality as inference).",
        face="#16161a",
    )

    ax.text(0.5, 0.95, "Modulus-link contract (schematic)", ha="center", va="top", color=FG, fontsize=14)
    ax.text(
        0.5,
        0.02,
        "Schematic only. Toy pedagogy. RSA residual taxonomies are measured per bit-rung elsewhere.",
        ha="center",
        color=MUTED,
        fontsize=9,
    )

    path = save_figure(
        fig,
        args.out_id,
        meta={"kind": "schematic", "status": "editorial-schema-for-research-contract"},
        repo_root=REPO_ROOT,
    )
    plt.close(fig)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
