#!/usr/bin/env python3
"""Generate style-locked noir editorial PNG plates for the PGS website.

Palette and bans follow website/assets/docs/STYLE_BIBLE.md.
These plates are structural-literal geometric exhibitions (no people, no text).
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import cairo

ROOT = Path(__file__).resolve().parents[1] / "plates"

BG = (0.027, 0.027, 0.031)
GOLD = (0.788, 0.663, 0.384)
GOLD_BRIGHT = (0.878, 0.769, 0.478)
CHAMPAGNE = (0.910, 0.835, 0.639)
GRAPHITE = (0.165, 0.165, 0.188)
GRAPHITE2 = (0.227, 0.227, 0.259)
DIM = (0.541, 0.451, 0.251)

SIZES = {
    "16:9": (1600, 900),
    "1:1": (1200, 1200),
    "3:2": (1500, 1000),
    "9:16": (900, 1600),
}


def paint_bg(ctx: cairo.Context, w: int, h: int) -> None:
    ctx.set_source_rgb(*BG)
    ctx.rectangle(0, 0, w, h)
    ctx.fill()
    # soft gold vignette
    g = cairo.RadialGradient(w * 0.5, h * 0.15, 10, w * 0.5, h * 0.2, max(w, h) * 0.75)
    g.add_color_stop_rgba(0, *GOLD, 0.08)
    g.add_color_stop_rgba(1, *BG, 0.0)
    ctx.set_source(g)
    ctx.rectangle(0, 0, w, h)
    ctx.fill()


def hairline(ctx: cairo.Context, x1, y1, x2, y2, a=0.35, width=1.0, color=GOLD):
    ctx.set_source_rgba(*color, a)
    ctx.set_line_width(width)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()


def bar(ctx: cairo.Context, x, base_y, bw, height, color, a=1.0):
    ctx.set_source_rgba(*color, a)
    ctx.rectangle(x, base_y - height, bw, height)
    ctx.fill()


def save(surface: cairo.ImageSurface, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    surface.write_to_png(str(path))


def plate_chamber(path: Path, ratio="16:9", seed=1, selected=None, twin=True):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    base = h * 0.72
    hairline(ctx, w * 0.06, base, w * 0.94, base, 0.45, 1.2, CHAMPAGNE)
    # endpoints
    for ex in (0.1, 0.9):
        bar(ctx, w * ex - 6, base, 12, h * 0.42, GOLD_BRIGHT, 0.95)
        hairline(ctx, w * ex, base - h * 0.42, w * ex, base - h * 0.48, 0.5, 1.0)
    n = 28 if twin else 18
    xs = [w * (0.14 + i * (0.72 / (n - 1))) for i in range(n)]
    heights = []
    for i in range(n):
        t = rng.choice([0.08, 0.1, 0.12, 0.16, 0.2, 0.28, 0.34])
        heights.append(h * t)
    if selected is None:
        selected = min(range(n), key=lambda i: heights[i])
    for i, x in enumerate(xs):
        col = CHAMPAGNE if i == selected else (GRAPHITE2 if heights[i] > h * 0.22 else GRAPHITE)
        a = 0.95 if i == selected else 0.85
        bar(ctx, x - 5, base, 10, heights[i], col, a)
        if i == selected:
            ctx.set_source_rgba(*GOLD_BRIGHT, 0.25)
            ctx.arc(x, base - heights[i] - 14, 16, 0, math.tau)
            ctx.stroke()
    save(surface, path)


def plate_bars_field(path: Path, ratio="1:1", seed=2, highlight=-1):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    base = h * 0.78
    hairline(ctx, w * 0.12, base, w * 0.88, base, 0.4, 1.2, GOLD)
    n = 16
    for i in range(n):
        x = w * (0.14 + i * 0.045)
        ht = h * rng.uniform(0.08, 0.45)
        col = GOLD_BRIGHT if i == highlight else (GOLD if rng.random() > 0.55 else GRAPHITE2)
        bar(ctx, x, base, 14, ht, col, 0.9)
    save(surface, path)


def plate_seal(path: Path, ratio="1:1", seed=3, rings=4):
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    cx, cy = w * 0.5, h * 0.5
    for i in range(rings):
        r = min(w, h) * (0.12 + i * 0.08)
        ctx.set_source_rgba(*GOLD, 0.55 - i * 0.08)
        ctx.set_line_width(1.5)
        ctx.arc(cx, cy, r, 0, math.tau)
        ctx.stroke()
    ctx.set_source_rgba(*CHAMPAGNE, 0.85)
    ctx.arc(cx, cy, min(w, h) * 0.04, 0, math.tau)
    ctx.fill()
    # floor grid transport
    for i in range(8):
        y = h * (0.62 + i * 0.03)
        hairline(ctx, w * 0.2, y, w * 0.8, y, 0.12 + i * 0.02, 1.0, DIM)
    save(surface, path)


def plate_chain(path: Path, ratio="16:9", seed=4, n=7):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    pts = []
    for i in range(n):
        x = w * (0.1 + i * 0.8 / (n - 1))
        y = h * (0.35 + 0.25 * math.sin(i * 0.9 + seed) + rng.uniform(-0.04, 0.04))
        pts.append((x, y))
    ctx.set_source_rgba(*GOLD, 0.45)
    ctx.set_line_width(1.6)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()
    for i, (x, y) in enumerate(pts):
        ctx.set_source_rgba(*CHAMPAGNE if i in (0, n - 1) else GOLD, 0.9)
        ctx.arc(x, y, 8 if i in (0, n - 1) else 5, 0, math.tau)
        ctx.fill()
    save(surface, path)


def plate_nodes(path: Path, ratio="16:9", seed=5, n=8):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    nodes = [(rng.uniform(0.12, 0.88) * w, rng.uniform(0.18, 0.82) * h) for _ in range(n)]
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            if rng.random() > 0.55:
                hairline(ctx, a[0], a[1], b[0], b[1], 0.2, 1.0)
    for i, (x, y) in enumerate(nodes):
        ctx.set_source_rgba(*CHAMPAGNE if i % 3 == 0 else GOLD, 0.85)
        ctx.arc(x, y, 6, 0, math.tau)
        ctx.fill()
    save(surface, path)


def plate_table(path: Path, ratio="3:2", seed=6, rows=5, cols=4):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    x0, y0, x1, y1 = w * 0.12, h * 0.18, w * 0.88, h * 0.82
    hairline(ctx, x0, y0, x1, y0, 0.5, 1.2, GOLD)
    hairline(ctx, x0, y1, x1, y1, 0.3, 1.0, DIM)
    for r in range(1, rows):
        y = y0 + (y1 - y0) * r / rows
        hairline(ctx, x0, y, x1, y, 0.18, 1.0, GRAPHITE2)
    for c in range(1, cols):
        x = x0 + (x1 - x0) * c / cols
        hairline(ctx, x, y0, x, y1, 0.15, 1.0, GRAPHITE2)
    for r in range(rows):
        for c in range(cols):
            if rng.random() > 0.4:
                cx = x0 + (x1 - x0) * (c + 0.5) / cols
                cy = y0 + (y1 - y0) * (r + 0.5) / rows
                ctx.set_source_rgba(*GOLD if rng.random() > 0.5 else CHAMPAGNE, 0.55)
                ctx.arc(cx, cy, 4, 0, math.tau)
                ctx.fill()
    save(surface, path)


def plate_residual(path: Path, ratio="3:2", seed=7):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    for _ in range(120):
        x = rng.uniform(0.15, 0.85) * w
        y = rng.uniform(0.2, 0.8) * h
        r = rng.uniform(1.0, 3.5)
        ctx.set_source_rgba(*CHAMPAGNE, rng.uniform(0.08, 0.35))
        ctx.arc(x, y, r, 0, math.tau)
        ctx.fill()
    # incomplete ring
    ctx.set_source_rgba(*GOLD, 0.55)
    ctx.set_line_width(2)
    ctx.arc(w * 0.5, h * 0.5, min(w, h) * 0.22, 0.3, math.tau - 0.8)
    ctx.stroke()
    save(surface, path)


def plate_monoliths(path: Path, ratio="1:1", seed=8):
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    base = h * 0.75
    hairline(ctx, w * 0.2, base, w * 0.8, base, 0.4, 1.2)
    bar(ctx, w * 0.32 - 18, base, 36, h * 0.4, GOLD, 0.95)
    bar(ctx, w * 0.68 - 18, base, 36, h * 0.4, CHAMPAGNE, 0.95)
    hairline(ctx, w * 0.32, base - h * 0.42, w * 0.68, base - h * 0.42, 0.35, 1.0)
    save(surface, path)


def plate_walk(path: Path, ratio="16:9", seed=9):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    base = h * 0.65
    hairline(ctx, w * 0.08, base, w * 0.92, base, 0.4, 1.2, GOLD)
    for i in range(20):
        x = w * (0.1 + i * 0.04)
        ht = h * rng.uniform(0.06, 0.28)
        col = GRAPHITE2
        if i == 0:
            col, ht = GOLD_BRIGHT, h * 0.38
        if i == 17:
            col, ht = CHAMPAGNE, h * 0.4
        bar(ctx, x, base, 10, ht, col, 0.9)
    # arrow energy
    hairline(ctx, w * 0.12, h * 0.3, w * 0.82, h * 0.3, 0.35, 1.2, CHAMPAGNE)
    save(surface, path)


def plate_boundary(path: Path, ratio="3:2", seed=10):
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    # left wall
    bar(ctx, w * 0.18, h * 0.75, 14, h * 0.4, GOLD_BRIGHT, 0.95)
    # short compression interval
    hairline(ctx, w * 0.18, h * 0.42, w * 0.42, h * 0.42, 0.7, 2.0, CHAMPAGNE)
    ctx.set_source_rgba(*GOLD, 0.8)
    ctx.arc(w * 0.42, h * 0.42, 6, 0, math.tau)
    ctx.fill()
    # faint longer forbidden stretch
    hairline(ctx, w * 0.42, h * 0.42, w * 0.82, h * 0.42, 0.15, 1.0, GRAPHITE2)
    save(surface, path)


def plate_chips(path: Path, ratio="1:1", seed=11):
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    colors = [GOLD, CHAMPAGNE, DIM, GRAPHITE2, GOLD_BRIGHT]
    for i, col in enumerate(colors):
        x = w * (0.18 + (i % 3) * 0.25)
        y = h * (0.32 + (i // 3) * 0.28)
        ctx.set_source_rgba(*col, 0.85)
        ctx.rectangle(x - 50, y - 22, 100, 44)
        ctx.fill()
        ctx.set_source_rgba(*BG, 0.35)
        ctx.rectangle(x - 40, y - 10, 80, 8)
        ctx.fill()
    save(surface, path)


def plate_modulus_plane(path: Path, ratio="16:9", seed=12):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    # perspective grid
    for i in range(12):
        y = h * (0.35 + i * 0.04)
        inset = i * 12
        hairline(ctx, w * 0.15 + inset, y, w * 0.85 - inset, y, 0.12 + i * 0.02, 1.0, GOLD)
    for i in range(9):
        x = w * (0.2 + i * 0.075)
        hairline(ctx, x, h * 0.35, w * 0.5 + (x - w * 0.5) * 0.3, h * 0.85, 0.15, 1.0, DIM)
    # reciprocal loop
    ctx.set_source_rgba(*CHAMPAGNE, 0.55)
    ctx.set_line_width(2)
    ctx.arc(w * 0.5, h * 0.48, min(w, h) * 0.12, 0, math.tau * 0.85)
    ctx.stroke()
    save(surface, path)


def plate_void_ornament(path: Path, ratio="3:2", seed=13):
    rng = random.Random(seed)
    w, h = SIZES[ratio]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    paint_bg(ctx, w, h)
    hairline(ctx, w * 0.15, h * 0.5, w * 0.85, h * 0.5, 0.35, 1.0, GOLD)
    for i in range(9):
        x = w * (0.2 + i * 0.075)
        ht = h * (0.05 + (0.15 if i % 4 == 0 else 0.06))
        bar(ctx, x - 3, h * 0.5, 6, ht, GOLD if i % 4 == 0 else GRAPHITE2, 0.85)
    save(surface, path)


def ensure_ai_preserved(chapter: str, names: list[str]) -> set[str]:
    d = ROOT / chapter
    return {p.name for p in d.glob("*.png")} if d.exists() else set()


def gen_chapter(chapter: str, specs: list[tuple[str, str, callable, dict]]):
    """specs: (filename, ratio, fn, kwargs). Preserve large AI plates already on disk."""
    for filename, ratio, fn, kwargs in specs:
        path = ROOT / chapter / filename
        if path.exists() and path.stat().st_size > 200_000:
            continue
        fn(path, ratio=ratio, **kwargs)


def main():
    # HOME - fill missing slots; keep existing AI files if large
    gen_chapter(
        "home",
        [
            ("01-hero-chamber.png", "16:9", plate_chamber, {"seed": 101, "selected": 8}),
            ("02-course-atlas.png", "16:9", plate_nodes, {"seed": 102, "n": 10}),
            ("03-pillar-nextprime.png", "1:1", plate_bars_field, {"seed": 103, "highlight": 12}),
            ("04-pillar-maximizer.png", "1:1", plate_chamber, {"seed": 104, "selected": 5, "twin": True}),
            ("05-pillar-compression.png", "1:1", plate_boundary, {"seed": 105}),
            ("06-dual-voice.png", "3:2", plate_void_ornament, {"seed": 106}),
            ("07-status-materials.png", "1:1", plate_chips, {"seed": 107}),
            ("08-flow-stations.png", "16:9", plate_chain, {"seed": 108, "n": 5}),
            ("09-proof-seals.png", "3:2", plate_seal, {"seed": 109, "rings": 5}),
            ("10-gold-field.png", "3:2", plate_residual, {"seed": 110}),
            ("11-gap-abstract.png", "1:1", plate_chamber, {"seed": 111, "selected": 3}),
            ("12-closing-constellation.png", "16:9", plate_nodes, {"seed": 112, "n": 14}),
            ("13-museum-wall.png", "16:9", plate_table, {"seed": 113, "rows": 4, "cols": 6}),
            ("14-endpoint-pair.png", "1:1", plate_monoliths, {"seed": 114}),
        ],
    )

    gen_chapter(
        "gaps",
        [
            ("01-hero-gap.png", "16:9", plate_chamber, {"seed": 201, "selected": 10}),
            ("02-two-walls.png", "3:2", plate_monoliths, {"seed": 202}),
            ("03-interior-composites.png", "16:9", plate_bars_field, {"seed": 203, "highlight": -1}),
            ("04-hallway.png", "16:9", plate_chamber, {"seed": 204, "selected": 6}),
            ("05-tiny-gap.png", "1:1", plate_chamber, {"seed": 205, "selected": 0, "twin": False}),
            ("06-medium-gap.png", "1:1", plate_chamber, {"seed": 206, "selected": 4}),
            ("07-long-gap.png", "16:9", plate_chamber, {"seed": 207, "selected": 12}),
            ("08-ruler-ticks.png", "3:2", plate_walk, {"seed": 208}),
            ("09-gap-question.png", "1:1", plate_void_ornament, {"seed": 209}),
            ("10-composite-field.png", "3:2", plate_bars_field, {"seed": 210, "highlight": 3}),
            ("11-open-interval.png", "16:9", plate_chamber, {"seed": 211, "selected": 7}),
            ("12-closing-wall.png", "1:1", plate_monoliths, {"seed": 212}),
            ("13-structure-not-void.png", "3:2", plate_nodes, {"seed": 213, "n": 9}),
            ("14-gap-recap.png", "16:9", plate_chain, {"seed": 214, "n": 6}),
        ],
    )

    gen_chapter(
        "mechanism",
        [
            ("01-hero-walk.png", "16:9", plate_walk, {"seed": 301}),
            ("02-divisor-count.png", "1:1", plate_bars_field, {"seed": 302, "highlight": 5}),
            ("03-tau-two.png", "1:1", plate_bars_field, {"seed": 303, "highlight": 14}),
            ("04-ordered-scan.png", "16:9", plate_walk, {"seed": 304}),
            ("05-chamber-landmark.png", "16:9", plate_chamber, {"seed": 305, "selected": 5}),
            ("06-leftmost-min.png", "3:2", plate_chamber, {"seed": 306, "selected": 2}),
            ("07-comparison-score.png", "1:1", plate_bars_field, {"seed": 307, "highlight": 8}),
            ("08-zero-excess.png", "1:1", plate_seal, {"seed": 308, "rings": 3}),
            ("09-not-lottery.png", "3:2", plate_void_ornament, {"seed": 309}),
            ("10-deterministic-path.png", "16:9", plate_chain, {"seed": 310, "n": 8}),
            ("11-interior-scan.png", "16:9", plate_chamber, {"seed": 311, "selected": 9}),
            ("12-score-peak.png", "3:2", plate_bars_field, {"seed": 312, "highlight": 7}),
            ("13-objects-strip.png", "16:9", plate_nodes, {"seed": 313, "n": 7}),
            ("14-mechanism-recap.png", "1:1", plate_monoliths, {"seed": 314}),
        ],
    )

    gen_chapter(
        "laws",
        [
            ("01-hero-pillars.png", "16:9", plate_nodes, {"seed": 401, "n": 6}),
            ("02-pillar-I.png", "1:1", plate_walk, {"seed": 402}),
            ("03-pillar-II.png", "1:1", plate_chamber, {"seed": 403, "selected": 4}),
            ("04-pillar-III.png", "1:1", plate_boundary, {"seed": 404}),
            ("05-next-prime-law.png", "16:9", plate_walk, {"seed": 405}),
            ("06-maximizer-law.png", "16:9", plate_chamber, {"seed": 406, "selected": 3}),
            ("07-compression-law.png", "16:9", plate_boundary, {"seed": 407}),
            ("08-square-branch.png", "3:2", plate_seal, {"seed": 408, "rings": 4}),
            ("09-boundary-rh.png", "3:2", plate_void_ornament, {"seed": 409}),
            ("10-dynamic-cutoff.png", "1:1", plate_boundary, {"seed": 410}),
            ("11-three-seals.png", "3:2", plate_seal, {"seed": 411, "rings": 6}),
            ("12-speak-carefully.png", "1:1", plate_chips, {"seed": 412}),
            ("13-universal-field.png", "16:9", plate_residual, {"seed": 413}),
            ("14-laws-recap.png", "16:9", plate_chain, {"seed": 414, "n": 3}),
        ],
    )

    gen_chapter(
        "generator",
        [
            ("01-hero-pair.png", "16:9", plate_monoliths, {"seed": 501}),
            ("02-minimal-record.png", "1:1", plate_monoliths, {"seed": 502}),
            ("03-clean-stream.png", "3:2", plate_void_ornament, {"seed": 503}),
            ("04-gap-question.png", "16:9", plate_chamber, {"seed": 504, "selected": 7}),
            ("05-not-candidate-loop.png", "1:1", plate_bars_field, {"seed": 505, "highlight": -1}),
            ("06-contract.png", "3:2", plate_seal, {"seed": 506, "rings": 3}),
            ("07-unresolved-gate.png", "1:1", plate_residual, {"seed": 507}),
            ("08-audit-after.png", "3:2", plate_chips, {"seed": 508}),
            ("09-evidence-surface.png", "16:9", plate_table, {"seed": 509, "rows": 5, "cols": 4}),
            ("10-high-scale.png", "16:9", plate_nodes, {"seed": 510, "n": 12}),
            ("11-sidecar.png", "1:1", plate_void_ornament, {"seed": 511}),
            ("12-production-path.png", "16:9", plate_chain, {"seed": 512, "n": 5}),
            ("13-json-pair-abstract.png", "1:1", plate_monoliths, {"seed": 513}),
            ("14-generator-recap.png", "3:2", plate_walk, {"seed": 514}),
        ],
    )

    gen_chapter(
        "cryptology",
        [
            ("01-hero-modulus.png", "16:9", plate_modulus_plane, {"seed": 601}),
            ("02-frame-lock.png", "3:2", plate_seal, {"seed": 602, "rings": 5}),
            ("03-endpoint-chain.png", "16:9", plate_chain, {"seed": 603, "n": 8}),
            ("04-floor-transport.png", "16:9", plate_modulus_plane, {"seed": 604}),
            ("05-reciprocal-closure.png", "1:1", plate_seal, {"seed": 605, "rings": 4}),
            ("06-residual-state.png", "3:2", plate_residual, {"seed": 606}),
            ("07-certificate.png", "1:1", plate_seal, {"seed": 607, "rings": 6}),
            ("08-unresolved.png", "1:1", plate_residual, {"seed": 608}),
            ("09-public-ladder.png", "16:9", plate_table, {"seed": 609, "rows": 3, "cols": 5}),
            ("10-no-factor-bag.png", "3:2", plate_void_ornament, {"seed": 610}),
            ("11-transport-loop.png", "16:9", plate_chain, {"seed": 611, "n": 6}),
            ("12-endpoint-class.png", "1:1", plate_monoliths, {"seed": 612}),
            ("13-honesty-wall.png", "3:2", plate_chips, {"seed": 613}),
            ("14-crypto-recap.png", "16:9", plate_modulus_plane, {"seed": 614}),
        ],
    )

    gen_chapter(
        "evidence",
        [
            ("01-hero-surfaces.png", "16:9", plate_table, {"seed": 701, "rows": 6, "cols": 5}),
            ("02-measured-not-proved.png", "3:2", plate_chips, {"seed": 702}),
            ("03-generator-surface.png", "16:9", plate_table, {"seed": 703, "rows": 4, "cols": 4}),
            ("04-decade-windows.png", "1:1", plate_nodes, {"seed": 704, "n": 10}),
            ("05-recursive-walk.png", "16:9", plate_walk, {"seed": 705}),
            ("06-zero-unresolved.png", "1:1", plate_seal, {"seed": 706, "rings": 3}),
            ("07-audit-corroboration.png", "3:2", plate_bars_field, {"seed": 707, "highlight": 2}),
            ("08-rsa-ladder.png", "16:9", plate_table, {"seed": 708, "rows": 3, "cols": 3}),
            ("09-resolved-row.png", "1:1", plate_seal, {"seed": 709, "rings": 4}),
            ("10-unresolved-row.png", "1:1", plate_residual, {"seed": 710}),
            ("11-regime-map.png", "3:2", plate_nodes, {"seed": 711, "n": 11}),
            ("12-not-inflation.png", "3:2", plate_void_ornament, {"seed": 712}),
            ("13-evidence-grid.png", "16:9", plate_table, {"seed": 713, "rows": 5, "cols": 6}),
            ("14-evidence-recap.png", "16:9", plate_chain, {"seed": 714, "n": 4}),
        ],
    )

    gen_chapter(
        "glossary",
        [
            ("01-hero-lexicon.png", "16:9", plate_nodes, {"seed": 801, "n": 16}),
            ("02-prime-gap-term.png", "1:1", plate_chamber, {"seed": 802, "selected": 6}),
            ("03-chamber-term.png", "1:1", plate_chamber, {"seed": 803, "selected": 4}),
            ("04-tau-term.png", "1:1", plate_bars_field, {"seed": 804, "highlight": 6}),
            ("05-witness-term.png", "1:1", plate_chamber, {"seed": 805, "selected": 2}),
            ("06-gwr-term.png", "3:2", plate_chamber, {"seed": 806, "selected": 1}),
            ("07-dni-term.png", "1:1", plate_seal, {"seed": 807, "rings": 3}),
            ("08-compression-term.png", "3:2", plate_boundary, {"seed": 808}),
            ("09-generator-term.png", "1:1", plate_monoliths, {"seed": 809}),
            ("10-unresolved-term.png", "1:1", plate_residual, {"seed": 810}),
            ("11-endpoint-term.png", "3:2", plate_chain, {"seed": 811, "n": 5}),
            ("12-certificate-term.png", "1:1", plate_seal, {"seed": 812, "rings": 5}),
            ("13-audit-term.png", "3:2", plate_chips, {"seed": 813}),
            ("14-glossary-mosaic.png", "16:9", plate_nodes, {"seed": 814, "n": 18}),
        ],
    )

    gen_chapter(
        "about",
        [
            ("01-hero-status.png", "16:9", plate_chips, {"seed": 901}),
            ("02-proved-band.png", "3:2", plate_seal, {"seed": 902, "rings": 5}),
            ("03-implemented-band.png", "3:2", plate_monoliths, {"seed": 903}),
            ("04-measured-band.png", "3:2", plate_table, {"seed": 904, "rows": 4, "cols": 4}),
            ("05-research-band.png", "3:2", plate_modulus_plane, {"seed": 905}),
            ("06-open-band.png", "3:2", plate_residual, {"seed": 906}),
            ("07-not-claims.png", "1:1", plate_void_ornament, {"seed": 907}),
            ("08-lean-mirror.png", "1:1", plate_seal, {"seed": 908, "rings": 4}),
            ("09-site-role.png", "16:9", plate_nodes, {"seed": 909, "n": 8}),
            ("10-source-links.png", "1:1", plate_chain, {"seed": 910, "n": 4}),
            ("11-continuity.png", "16:9", plate_walk, {"seed": 911}),
            ("12-program-map.png", "16:9", plate_nodes, {"seed": 912, "n": 12}),
            ("13-about-recap.png", "3:2", plate_chamber, {"seed": 913, "selected": 5}),
            ("14-final-seal.png", "1:1", plate_seal, {"seed": 914, "rings": 6}),
        ],
    )

    # count
    total = 0
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and d.name != "masters":
            n = len(list(d.glob("*.png")))
            total += n
            print(f"{d.name}: {n}")
    print(f"total chapter plates: {total}")


if __name__ == "__main__":
    main()
