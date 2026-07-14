#!/usr/bin/env python3
"""Dual panel: d(n) bars and zero-excess E(n) on one chamber."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ENTRY_ID = "dual-e-z-field"
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.data import materialize_gap_field  # noqa: E402
from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import save_figure  # noqa: E402
from _common.style import ACCENT_WITNESS, FG, GOLD_BRIGHT, apply_library_style, d_color  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=89)
    parser.add_argument("--q", type=int, default=97)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()

    apply_library_style(plt)
    field = materialize_gap_field(args.p, args.q)
    values = field["values"]
    ds = field["divisors"]
    es = field["excess"]
    w = field["w"]
    xs = list(range(len(values)))

    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax0.bar(xs, ds, color=[d_color(d) for d in ds], width=0.85)
    ax0.set_ylabel("d(n)")
    ax0.set_title(f"Divisor-count field on [{args.p}, {args.q}]")
    ax0.axhline(2, color=GOLD_BRIGHT, linestyle="--", linewidth=0.9, alpha=0.7)
    wi = values.index(w)
    ax0.scatter([wi], [ds[wi] + 0.3], color=ACCENT_WITNESS, marker="v", s=60, zorder=5, label=f"GWR w={w}")
    ax0.legend(loc="upper right")
    ax0.grid(axis="y", alpha=0.35)

    ax1.plot(xs, es, color=GOLD_BRIGHT, linewidth=1.6, marker="o", markersize=4)
    ax1.axhline(0.0, color=FG, linewidth=1.0, alpha=0.8)
    ax1.scatter([wi], [es[wi]], color=ACCENT_WITNESS, s=70, zorder=5)
    for i, (n, d, e) in enumerate(zip(values, ds, es)):
        if d == 2:
            ax1.scatter([i], [0.0], color=GOLD_BRIGHT, s=80, zorder=4)
    ax1.set_ylabel("E(n) = (d(n)/2 - 1) ln n")
    ax1.set_xlabel("position in chamber (left = p)")
    ax1.set_xticks(xs)
    ax1.set_xticklabels([str(v) for v in values])
    ax1.set_title("Zero-excess coordinate (primes sit at E=0)")
    ax1.grid(True, alpha=0.35)

    # Z dual note in text
    z_w = pow(2.718281828, -es[wi]) if es[wi] == es[wi] else float("nan")
    fig.suptitle(
        f"DNI dual view: E and d on one chamber  |  at w={w}, E≈{es[wi]:.3f}, Z=e^{{-E}}≈{z_w:.3f}",
        color=FG,
    )
    fig.tight_layout()
    path = save_figure(
        fig,
        args.out_id,
        meta={
            "kind": "scientific-demo",
            "p": args.p,
            "q": args.q,
            "w": w,
            "regime": f"single toy chamber p={args.p}, q={args.q}",
        },
        repo_root=REPO_ROOT,
    )
    plt.close(fig)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
