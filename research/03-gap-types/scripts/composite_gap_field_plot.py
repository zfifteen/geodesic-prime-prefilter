#!/usr/bin/env python3
"""Generate a composite-field visualization of prime-gap interiors."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap, LogNorm


LIMIT = 5000
HEATMAP_ROWS = 56
HEATMAP_COLS = 48
MIN_GAP = 6
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]


def prime_flags(limit: int) -> list[bool]:
    flags = [True] * (limit + 1)
    flags[0] = False
    flags[1] = False
    for n in range(2, int(limit**0.5) + 1):
        if flags[n]:
            for multiple in range(n * n, limit + 1, n):
                flags[multiple] = False
    return flags


def divisor_counts(limit: int) -> list[int]:
    counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            counts[multiple] += 1
    return counts


def gap_records(primes: list[int], tau: list[int]) -> list[dict[str, object]]:
    records = []
    for p, q in zip(primes, primes[1:]):
        interior = list(range(p + 1, q))
        records.append(
            {
                "p": p,
                "q": q,
                "gap": q - p,
                "interior": interior,
                "tau": [tau[n] for n in interior],
                "load": sum(tau[n] for n in interior),
            }
        )
    return records


def resampled_tau(values: list[int], width: int) -> list[float]:
    if not values:
        return [math.nan] * width
    if len(values) == 1:
        return [float(values[0])] * width

    row = []
    for col in range(width):
        pos = col * (len(values) - 1) / (width - 1)
        left = int(math.floor(pos))
        right = int(math.ceil(pos))
        if left == right:
            row.append(float(values[left]))
        else:
            blend = pos - left
            row.append(values[left] * (1.0 - blend) + values[right] * blend)
    return row


def main() -> None:
    out_dir = Path(__file__).resolve().parents[1] / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "composite_gap_field_plot.png"

    flags = prime_flags(LIMIT)
    primes = [n for n in range(2, LIMIT + 1) if flags[n]]
    tau = divisor_counts(LIMIT)
    records = gap_records(primes, tau)
    visible = [record for record in records if record["gap"] >= MIN_GAP]
    visible = visible[-HEATMAP_ROWS:]
    widest = max(records, key=lambda record: (record["gap"], -record["p"]))

    heat = [resampled_tau(record["tau"], HEATMAP_COLS) for record in visible]
    labels = [f'{record["p"]}->{record["q"]}' for record in visible]

    fig = plt.figure(figsize=(16, 10), dpi=180)
    fig.patch.set_facecolor("#111418")
    grid = fig.add_gridspec(
        2,
        2,
        width_ratios=[1.25, 1.0],
        height_ratios=[1.1, 1.0],
        hspace=0.34,
        wspace=0.22,
    )

    ax_heat = fig.add_subplot(grid[:, 0])
    ax_band = fig.add_subplot(grid[0, 1])
    ax_scatter = fig.add_subplot(grid[1, 1])

    image = ax_heat.imshow(
        heat,
        aspect="auto",
        interpolation="nearest",
        cmap="magma",
        norm=LogNorm(vmin=2, vmax=max(max(row) for row in heat if row)),
    )
    ax_heat.set_title(
        "Prime gaps as composite-field chambers",
        color="#f4f1ea",
        fontsize=18,
        pad=14,
    )
    ax_heat.set_xlabel("normalized interior position between consecutive primes", color="#c8d0d8")
    ax_heat.set_ylabel("gap endpoint pair", color="#c8d0d8")
    tick_positions = list(range(0, len(labels), max(1, len(labels) // 14)))
    ax_heat.set_yticks(tick_positions)
    ax_heat.set_yticklabels([labels[i] for i in tick_positions], fontsize=7, color="#c8d0d8")
    ax_heat.set_xticks([0, HEATMAP_COLS // 2, HEATMAP_COLS - 1])
    ax_heat.set_xticklabels(["left prime", "interior", "right prime"], color="#c8d0d8")
    ax_heat.tick_params(colors="#c8d0d8")
    for spine in ax_heat.spines.values():
        spine.set_color("#3b4652")
    cbar = fig.colorbar(image, ax=ax_heat, fraction=0.035, pad=0.025)
    cbar.ax.tick_params(colors="#c8d0d8")
    cbar.set_label("divisor count in the composite interior", color="#c8d0d8")

    p = int(widest["p"])
    q = int(widest["q"])
    interiors = list(widest["interior"])
    band_matrix = []
    for divisor in SMALL_PRIMES:
        band_matrix.append([1 if n % divisor == 0 else 0 for n in interiors])
    ax_band.imshow(
        band_matrix,
        aspect="auto",
        interpolation="nearest",
        cmap=ListedColormap(["#101820", "#ffd166"]),
        vmin=0,
        vmax=1,
    )
    ax_band.set_title(
        f"Widest chamber under {LIMIT}: {p}->{q}",
        color="#f4f1ea",
        fontsize=14,
        pad=12,
    )
    ax_band.set_xlabel("composite integers inside the gap", color="#c8d0d8")
    ax_band.set_ylabel("small divisor band", color="#c8d0d8")
    ax_band.set_yticks(range(len(SMALL_PRIMES)))
    ax_band.set_yticklabels([str(n) for n in SMALL_PRIMES], color="#c8d0d8", fontsize=8)
    x_ticks = list(range(0, len(interiors), max(1, len(interiors) // 8)))
    ax_band.set_xticks(x_ticks)
    ax_band.set_xticklabels([str(interiors[i]) for i in x_ticks], rotation=45, ha="right", fontsize=7, color="#c8d0d8")
    ax_band.tick_params(colors="#c8d0d8")
    for spine in ax_band.spines.values():
        spine.set_color("#3b4652")

    scatter_records = [record for record in records if record["gap"] >= 4]
    gaps = [int(record["gap"]) for record in scatter_records]
    loads = [float(record["load"]) / max(1, int(record["gap"]) - 1) for record in scatter_records]
    starts = [int(record["p"]) for record in scatter_records]
    ax_scatter.scatter(
        gaps,
        loads,
        c=starts,
        cmap="viridis",
        s=32,
        alpha=0.82,
        edgecolors="#111418",
        linewidths=0.35,
    )
    ax_scatter.set_title(
        "Interior composite load by gap width",
        color="#f4f1ea",
        fontsize=14,
        pad=12,
    )
    ax_scatter.set_xlabel("prime gap q - p", color="#c8d0d8")
    ax_scatter.set_ylabel("mean divisor count across interior", color="#c8d0d8")
    ax_scatter.grid(color="#2d3742", linewidth=0.7, alpha=0.7)
    ax_scatter.tick_params(colors="#c8d0d8")
    for spine in ax_scatter.spines.values():
        spine.set_color("#3b4652")

    label_offsets = [(7, 7), (7, -11), (-56, 8)]
    for offset, record in zip(
        label_offsets,
        sorted(scatter_records, key=lambda item: item["gap"], reverse=True)[:3],
    ):
        gap = int(record["gap"])
        load = float(record["load"]) / max(1, gap - 1)
        ax_scatter.annotate(
            f'{record["p"]}->{record["q"]}',
            (gap, load),
            textcoords="offset points",
            xytext=offset,
            fontsize=7,
            color="#f4f1ea",
        )

    fig.suptitle(
        "Composite structure inside prime gaps",
        color="#f4f1ea",
        fontsize=22,
        y=0.985,
    )
    fig.text(
        0.5,
        0.025,
        "Deterministic measurement plot: primes mark chamber endpoints; interior color and bands come from divisor-count and divisibility structure of composites.",
        color="#aab4bf",
        ha="center",
        fontsize=10,
    )

    for ax in [ax_heat, ax_band, ax_scatter]:
        ax.set_facecolor("#171c22")

    rect = patches.Rectangle(
        (0, 0),
        1,
        1,
        transform=fig.transFigure,
        fill=False,
        edgecolor="#2d3742",
        linewidth=2,
    )
    fig.add_artist(rect)
    fig.savefig(out_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(out_path)


if __name__ == "__main__":
    main()
