#!/usr/bin/env python3
"""
Buck-wild crazy PGS visualizations: animations (GIFs), tapestry composite, 3D model export (OBJ), more interactive.
Uses real data + generated gaps. Produces GIFs, PNGs, OBJ, HTML.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import imageio.v2 as imageio
from pathlib import Path
from sympy import primerange, divisor_count, nextprime
from collections import defaultdict
import math

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

COSMIC = {
    'bg': '#05070a',
    'nebula': '#0a0520',
    'star': '#f0e6d2',
    'ridge': '#ff6b35',
    'square': '#ffd700',
    'd4': '#00ff9f',
    'selected': '#ff2d55',
    'u_square': '#7b2cbf',
    'grid': '#2a2a4a',
    'accent1': '#00d4ff',
    'accent2': '#ff00aa',
    'white': '#ffffff',
}

def load_square_branch():
    df = pd.read_csv('/Users/velocityworks/IdeaProjects/prime-gap-structure/research/04-bounded-compression/output/square_branch_gap_audit_violations.csv')
    df['violation'] = (df['offset'] > df['dynamic_cutoff']).astype(int)
    return df

def get_gaps(n_gaps=80, max_p=6000):
    primes = list(primerange(2, max_p))
    gaps = []
    for i in range(min(n_gaps, len(primes)-1)):
        p, q = primes[i], primes[i+1]
        if q - p < 3: continue
        ns = list(range(p+1, q))
        ds = np.array([divisor_count(n) for n in ns])
        zs = np.array([float(n ** (1 - d/2)) for n,d in zip(ns, ds)])
        min_d = int(ds.min())
        w_idx = int(np.argmin(ds))
        w = ns[w_idx]
        gaps.append({'p': p, 'q': q, 'ns': np.array(ns), 'ds': ds, 'zs': zs, 'w': w, 'min_d': min_d, 'width': q-p})
    return gaps

# 1. Animated Ridge Flight GIF (camera "flying" through evolving gaps)
def generate_ridge_flight_gif(gaps, n_frames=36, out_name="ridge_flight_crazy.gif"):
    frames = []
    for f in range(n_frames):
        fig, ax = plt.subplots(figsize=(11, 6), facecolor=COSMIC['bg'])
        ax.set_facecolor(COSMIC['bg'])
        idx = int((f / n_frames) * (len(gaps) - 1))
        g = gaps[idx]
        ns, ds, zs, w = g['ns'], g['ds'], g['zs'], g['w']
        
        # Color bars by class, vibrant
        colors = []
        for d in ds:
            if d == 3: colors.append(COSMIC['square'])
            elif d == 4: colors.append(COSMIC['d4'])
            elif d % 2 == 0: colors.append(COSMIC['accent1'])
            else: colors.append(COSMIC['accent2'])
        
        bars = ax.bar(ns, ds, color=colors, alpha=0.75, width=0.7)
        # Highlight GWR w
        w_idx = list(ns).index(w)
        ax.bar(w, ds[w_idx], color=COSMIC['selected'], alpha=0.95, width=0.7, edgecolor=COSMIC['white'], linewidth=2)
        
        ax2 = ax.twinx()
        ax2.plot(ns, zs, color=COSMIC['ridge'], linewidth=2.5, alpha=0.9)
        ax2.scatter([w], [zs[w_idx]], color=COSMIC['selected'], s=180, marker='*', zorder=10, edgecolors=COSMIC['white'])
        
        # Dynamic square ref
        sqrt_w = int(math.isqrt(w))
        next_p = nextprime(sqrt_w)
        next_sq = next_p ** 2
        if next_sq < g['q'] + 50:
            ax.axvline(next_sq, color=COSMIC['u_square'], linestyle='--', alpha=0.6, lw=1.5)
        
        ax.set_title(f'PGS RIDGE FLIGHT — Gap {g["p"]} → {g["q"]} (frame {f+1}/{n_frames})\nRed star = GWR w | Orange = Z(n) ridge terrain | Yellow/Teal = squares/d4', 
                     color=COSMIC['white'], fontsize=10)
        ax.tick_params(colors=COSMIC['white'], labelsize=7)
        ax2.tick_params(colors=COSMIC['ridge'], labelsize=7)
        for spine in ax.spines.values(): spine.set_color(COSMIC['grid'])
        
        fig.canvas.draw()
        frame = np.array(fig.canvas.renderer.buffer_rgba())[:, :, :3]
        frames.append(frame)
        plt.close(fig)
    
    gif_path = OUT_DIR / out_name
    imageio.mimsave(gif_path, frames, duration=0.12, loop=0)
    print(f"Saved crazy animation: {gif_path}")

# 2. Tapestry composite using PIL (huge artistic image)
def generate_tapestry(gaps, out_name="pgs_tapestry_crazy.png"):
    from PIL import Image, ImageDraw, ImageFont
    try:
        import matplotlib.cm as cm
    except:
        cm = None
    
    tile_w, tile_h = 180, 120
    cols = 12
    rows = min(8, (len(gaps) + cols - 1) // cols)
    big_w, big_h = cols * tile_w, rows * tile_h
    tapestry = Image.new('RGB', (big_w, big_h), COSMIC['bg'])
    draw = ImageDraw.Draw(tapestry)
    
    for idx, g in enumerate(gaps[:cols*rows]):
        row = idx // cols
        col = idx % cols
        x0, y0 = col * tile_w, row * tile_h
        
        ns, ds, zs, w = g['ns'], g['ds'], g['zs'], g['w']
        # Mini bar plot
        max_d = max(ds)
        for i, (n, d) in enumerate(zip(ns, ds)):
            bx = x0 + 5 + int((i / max(1, len(ns))) * (tile_w - 10))
            bh = int((d / max_d) * (tile_h - 30))
            color = (255, 215, 0) if d == 3 else (0, 255, 159) if d == 4 else (0, 212, 255) if d % 2 == 0 else (255, 0, 170)
            draw.rectangle([bx, y0 + tile_h - 25 - bh, bx + 2, y0 + tile_h - 25], fill=color)
        
        # Mark w
        if w in ns:
            wi = list(ns).index(w)
            wx = x0 + 5 + int((wi / max(1, len(ns))) * (tile_w - 10))
            draw.ellipse([wx-3, y0 + tile_h - 28, wx+3, y0 + tile_h - 22], fill=(255, 45, 85))
        
        # Label
        draw.text((x0 + 3, y0 + 2), f"{g['p']}-{g['q']}", fill=COSMIC['white'])
    
    # Add cosmic border and title overlay
    draw.rectangle([0, 0, big_w-1, big_h-1], outline=COSMIC['ridge'], width=4)
    tapestry.save(OUT_DIR / out_name)
    print(f"Saved crazy tapestry: {out_name}")

# 3. 3D OBJ export for cosmos (simple point cloud + some lines for "printable")
def export_3d_obj_for_print(df, out_name="square_branch_cosmos.obj"):
    # Sample and normalize to unit cube-ish for 3D printing
    sample = df.sample(min(2000, len(df)), random_state=42)
    xs = np.log10(sample['p'].values + 1)
    ys = sample['offset'].values
    zs = sample['dynamic_cutoff'].values
    viol = sample['violation'].values
    
    # Normalize
    xs = (xs - xs.min()) / (xs.max() - xs.min() + 1e-9)
    ys = (ys - ys.min()) / (ys.max() - ys.min() + 1e-9)
    zs = (zs - zs.min()) / (zs.max() - zs.min() + 1e-9)
    
    lines = []
    lines.append("# PGS Square Branch Cosmos - 3D printable point cloud + violation highlights")
    lines.append("# x=logp_norm, y=offset_norm, z=cutoff_norm ; red stars for violations")
    
    for i, (x,y,z,v) in enumerate(zip(xs, ys, zs, viol)):
        lines.append(f"v {x:.6f} {y:.6f} {z:.6f}")
    
    # Add some "constellation" edges for structure
    for i in range(0, len(xs)-1, 3):
        lines.append(f"l {i+1} {i+4}")
    
    obj_path = OUT_DIR / out_name
    with open(obj_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Saved 3D model for printing/blender: {out_name} (open in Blender, scale up, add spheres for points)")

# 4. Enhanced interactive multi-view HTML (Plotly dashboard style)
def generate_crazy_interactive_dashboard(gaps, df_square, out_name="pgs_jawdropping_dashboard.html"):
    # View 1: 3D nebula from gaps
    dfg = pd.DataFrame({
        'logp': [np.log10(g['p']) for g in gaps],
        'width': [g['width'] for g in gaps],
        'min_d': [g['min_d'] for g in gaps],
        'w_rel': [(g['w']-g['p'])/g['width'] for g in gaps],
        'avg_z': [np.mean(g['zs']) for g in gaps]
    })
    fig1 = go.Figure(go.Scatter3d(
        x=dfg['logp'], y=dfg['width'], z=dfg['min_d'],
        mode='markers', marker=dict(size=dfg['avg_z']*35+4, color=dfg['w_rel'], colorscale='Viridis', opacity=0.7),
        text=[f"p={g['p']} minτ={g['min_d']}" for g in gaps], hoverinfo='text'
    ))
    fig1.update_layout(title="3D Gap Nebula", scene=dict(xaxis_title="log p", yaxis_title="width", zaxis_title="min τ"), height=500)
    
    # View 2: Square branch scatter
    fig2 = go.Figure(go.Scatter(
        x=np.log10(df_square['p']), y=df_square['offset'],
        mode='markers', marker=dict(size=4, color=df_square['violation'], colorscale=[[0,'#ffd700'],[1,'#ff2d55']], opacity=0.6),
        text=[f"p={p} off={o} viol={v}" for p,o,v in zip(df_square['p'], df_square['offset'], df_square['violation'])],
        hoverinfo='text'
    ))
    fig2.update_layout(title="Square Branch Offsets (red=violation)", height=400)
    
    # Combined HTML
    html = f"""
<!doctype html><html><head><title>PGS Jaw-Dropping Dashboard</title>
<style>body {{background:#05070a; color:#f0e6d2; font-family:sans-serif;}} .plot {{border:1px solid #2a2a4a; margin:10px;}}</style>
</head><body>
<h1>PGS Buck-Wild Dashboard - Go Crazy Visualizations</h1>
<p>Interactive 3D + Square Branch + more. All from real PGS data (divisor fields, GWR, square violations).</p>
<div class="plot">{fig1.to_html(full_html=False, include_plotlyjs=True)}</div>
<div class="plot">{fig2.to_html(full_html=False, include_plotlyjs=False)}</div>
<p><strong>More crazy assets in this folder:</strong> cosmos 3D PNG, fractal tree, mandala, ridge flight GIF (if generated), OBJ for 3D print, this dashboard.</p>
<p>Tie-in: These visualize the geometric frameworks, square branch (PROOF.md), ridges (research/11-gap-ridge), etc. Open in browser for full effect.</p>
</body></html>
"""
    (OUT_DIR / out_name).write_text(html)
    print(f"Saved crazy interactive dashboard: {out_name}")

def main():
    print("=== GOING ABSOLUTELY CRAZY WITH PGS VIZ ===")
    gaps = get_gaps(100, 7000)
    df_square = load_square_branch()
    
    generate_ridge_flight_gif(gaps, n_frames=30)
    generate_tapestry(gaps)
    export_3d_obj_for_print(df_square)
    generate_crazy_interactive_dashboard(gaps, df_square)
    
    print("\n=== CRAZY OUTPUTS IN jawdropping/ ===")
    print("Open the HTML dashboard and GIF for motion. OBJ for Blender/3D print the cosmos.")
    print("These are vibrant, scientific, and trippy - perfect for the visualizations suite.")

if __name__ == "__main__":
    main()
