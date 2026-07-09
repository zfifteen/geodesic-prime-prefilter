#!/usr/bin/env python3
"""
Buck-wild, jaw-dropping PGS visualizations.
Pushes beyond standard 2D/3D: fractals, animations, cosmic 3D, mandalas, 4D projections, nebulae.
Uses real PGS data (square branch offsets, gap features, Z scores) + synthetic for scale.
Generates PNG, GIF (via imageio), interactive Plotly HTML.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import sympy
from sympy import primerange, divisor_count
import networkx as nx
from pathlib import Path
import imageio.v2 as imageio
from collections import defaultdict
import math

OUT_DIR = Path(__file__).parent
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Stunning dark cosmic palette
COSMIC = {
    'bg': '#05070a',
    'nebula': '#1a0a2e',
    'star': '#f0e6d2',
    'ridge': '#ff6b35',
    'square': '#ffd700',
    'd4': '#00ff9f',
    'selected': '#ff2d55',
    'u_square': '#7b2cbf',
    'grid': '#2a2a4a',
    'accent1': '#00d4ff',
    'accent2': '#ff00aa',
}

def load_square_branch_data():
    """Real data: p, square=w, previous_prime, offset=w-p, o_q, cutoffs."""
    df = pd.read_csv('/Users/velocityworks/IdeaProjects/prime-gap-structure/research/04-bounded-compression/output/square_branch_gap_audit_violations.csv')
    df['violation'] = (df['offset'] > df['dynamic_cutoff']).astype(int)
    return df

def get_sample_gaps(n=200, max_p=10000):
    """Fresh gaps with full τ field for profiles/animations."""
    primes = list(primerange(2, max_p))
    gaps = []
    for i in range(min(n, len(primes)-1)):
        p, q = primes[i], primes[i+1]
        if q - p < 3: continue
        ns = list(range(p+1, q))
        ds = np.array([divisor_count(n) for n in ns])
        zs = np.array([n ** (1 - d/2.0) for n,d in zip(ns, ds)])
        min_d = int(ds.min())
        w_idx = int(np.argmin(ds))
        w = ns[w_idx]
        gaps.append({'p':p, 'q':q, 'ns':np.array(ns), 'ds':ds, 'zs':zs, 'w':w, 'min_d':min_d, 'width':q-p})
    return gaps

# 1. JAW-DROPPING: Square Branch Cosmos 3D + "violations" as supernovae
def generate_square_branch_cosmos(df):
    fig = plt.figure(figsize=(16,12), facecolor=COSMIC['bg'])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(COSMIC['bg'])
    
    # Sample for clarity
    sample = df.sample(min(3000, len(df)), random_state=42)
    x = np.log10(sample['p'].values + 1)
    y = sample['offset'].values
    z = sample['dynamic_cutoff'].values
    c = sample['violation'].values  # 0/1 for color
    s = np.clip(sample['o_q'].values * 10, 5, 80)
    
    # Base stars (non-violations)
    non_v = sample[sample['violation']==0]
    ax.scatter(np.log10(non_v['p']+1), non_v['offset'], non_v['dynamic_cutoff'], 
               c=COSMIC['star'], s=3, alpha=0.4, label='Square branch points')
    
    # Violations as exploding stars
    v = sample[sample['violation']==1]
    ax.scatter(np.log10(v['p']+1), v['offset'], v['dynamic_cutoff'], 
               c=COSMIC['selected'], s=s[v.index.isin(v.index)]*2, alpha=0.9, marker='*', edgecolors='white', linewidths=0.5, label='Violations (offset > dynamic cutoff)')
    
    # "Constellations" - connect nearby in logp-offset space
    G = nx.Graph()
    coords = list(zip(x, y))
    for i, (xi,yi) in enumerate(coords[:500]):
        for j in range(i+1, min(i+5, len(coords))):
            dist = np.hypot(xi - coords[j][0], yi - coords[j][1])
            if dist < 0.5:
                G.add_edge(i, j)
    for edge in list(G.edges())[:200]:
        i,j = edge
        ax.plot([x[i],x[j]], [y[i],y[j]], [z[i],z[j]], color=COSMIC['accent1'], alpha=0.15, lw=0.5)
    
    ax.set_xlabel('log10(p) [cosmic distance]', color='white', fontsize=11)
    ax.set_ylabel('w - p offset (light years?)', color='white', fontsize=11)
    ax.set_zlabel('Dynamic cutoff (energy barrier)', color='white', fontsize=11)
    ax.set_title('PGS Square Branch Cosmos\n3D "Universe" of prime squares: stars = r², red supernovae = structural violations, blue lines = "constellations" of similar gaps', 
                 color='white', fontsize=13, pad=20)
    ax.tick_params(colors='white')
    ax.legend(loc='upper left', facecolor=COSMIC['nebula'], edgecolor='white', labelcolor='white')
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.edgecolor = COSMIC['grid']
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'square_branch_cosmos_3d.png', dpi=180, facecolor=COSMIC['bg'])
    plt.close()
    print("Saved jaw-dropping: square_branch_cosmos_3d.png")

# 2. Recursive Fractal Square Branch Tree (2D artistic + 3D)
def generate_fractal_square_tree(df, max_depth=6):
    fig, ax = plt.subplots(figsize=(14,10), facecolor=COSMIC['bg'])
    ax.set_facecolor(COSMIC['bg'])
    
    # Sort by p for "time"
    df = df.sort_values('p').head(200)
    squares = df['square'].values
    offsets = df['offset'].values
    violations = df['violation'].values
    
    def draw_branch(x, y, angle, length, depth, is_violation):
        if depth <= 0 or length < 1: return
        rad = math.radians(angle)
        x2 = x + length * math.cos(rad)
        y2 = y + length * math.sin(rad)
        color = COSMIC['selected'] if is_violation else (COSMIC['square'] if depth % 2 == 0 else COSMIC['u_square'])
        ax.plot([x, x2], [y, y2], color=color, lw=max(0.5, depth*0.8), alpha=0.7 + 0.3*(depth/max_depth))
        # Sub-branches
        for da in [-35, 35]:
            draw_branch(x2, y2, angle + da, length * 0.65, depth-1, is_violation and (depth<3))
    
    # Root at origin
    ax.plot(0, 0, 'o', color=COSMIC['star'], markersize=12)
    for i, (sq, off, viol) in enumerate(zip(squares[:50], offsets[:50], violations[:50])):
        # Map to angle/length
        angle = (i % 12 - 6) * 8 + (off % 20 - 10)
        length = 20 + off * 0.3
        draw_branch(0, 0, angle, length, max_depth, viol)
    
    ax.set_xlim(-180, 180)
    ax.set_ylim(-120, 120)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('PGS Square Branch Fractal Tree\nRecursive "unfolding" of prime squares (r²). Red branches = violations of bounded compression. Depth encodes scale.', 
                 color='white', fontsize=12, pad=10)
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'square_branch_fractal_tree.png', dpi=180, facecolor=COSMIC['bg'], bbox_inches='tight')
    plt.close()
    print("Saved jaw-dropping: square_branch_fractal_tree.png")

# 3. Animated "Flight Through the Ridge" GIF
def generate_ridge_flight_gif(gaps, n_frames=40):
    frames = []
    for f in range(n_frames):
        fig, ax = plt.subplots(figsize=(10,6), facecolor=COSMIC['bg'])
        ax.set_facecolor(COSMIC['bg'])
        idx = int(f / n_frames * len(gaps))
        gap = gaps[min(idx, len(gaps)-1)]
        ns, ds, zs = gap['ns'], gap['ds'], gap['zs']
        w = gap['w']
        
        colors = [COSMIC['square'] if d==3 else COSMIC['d4'] if d==4 else COSMIC['accent1'] if d%2==0 else COSMIC['accent2'] for d in ds]
        ax.bar(ns, ds, color=colors, alpha=0.7, width=0.8)
        ax.bar(w, gap['min_d'], color=COSMIC['selected'], alpha=0.95, width=0.8)
        
        ax2 = ax.twinx()
        ax2.plot(ns, zs, color=COSMIC['ridge'], lw=2.5)
        ax2.scatter([w], [zs[list(ns).index(w)]], color=COSMIC['selected'], s=120, marker='*', zorder=10)
        
        ax.set_title(f'Flight Through PGS Ridges. Gap {gap["p"]}→{gap["q"]} (frame {f+1}/{n_frames})\nRed = GWR w; Orange curve = Z(n) ridge "terrain"', color='white', fontsize=11)
        ax.tick_params(colors='white')
        ax2.tick_params(colors=COSMIC['ridge'])
        for sp in ax.spines.values(): sp.set_color(COSMIC['grid'])
        
        fig.canvas.draw()
        frame = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(frame[:,:,:3])  # RGB
        plt.close(fig)
    
    gif_path = OUT_DIR / 'ridge_flight_animation.gif'
    imageio.mimsave(gif_path, frames, duration=0.15, loop=0)
    print(f"Saved jaw-dropping animation: {gif_path}")

# 4. PGS Mandala (multi-layer polar artistic)
def generate_pgs_mandala(gaps):
    fig, ax = plt.subplots(figsize=(12,12), subplot_kw={'projection': 'polar'}, facecolor=COSMIC['bg'])
    ax.set_facecolor(COSMIC['bg'])
    
    # Layer 1: mod30 ridge strength (inner)
    res_str = defaultdict(list)
    for g in gaps[:80]:
        res_str[g['p'] % 30].append(1.0 / g['min_d'])
    thetas = np.array([r * np.pi /15 for r in sorted(res_str)])
    rs = np.array([np.mean(res_str[r]) for r in sorted(res_str)])
    ax.bar(thetas, rs*2, width=0.15, color=COSMIC['ridge'], alpha=0.6, bottom=1)
    
    # Layer 2: gap widths as petals
    for i, g in enumerate(gaps[:36]):
        theta = (i / 36) * 2 * np.pi
        r = 4 + g['width'] / 5
        ax.plot([theta, theta], [3, r], color=COSMIC['d4'], lw=2, alpha=0.7)
        ax.scatter([theta], [r], s=30, color=COSMIC['accent1'] if g['min_d']<=4 else COSMIC['accent2'])
    
    # Layer 3: square branch "petals" outer (use real data)
    df = load_square_branch_data().head(60)
    for i, row in df.iterrows():
        theta = (i / 60) * 2 * np.pi + 0.1
        r = 8 + row['offset'] / 8
        color = COSMIC['selected'] if row['violation'] else COSMIC['square']
        ax.plot([theta]*2, [6, r], color=color, lw=1.5, alpha=0.8)
    
    ax.set_title('PGS Mandala: Multi-Layer Sacred Geometry\nInner: mod30 ridge strength | Mid: gap width "petals" + GWR min_d | Outer: Square branch offsets (red=violations)', 
                 color='white', fontsize=11, pad=15, y=1.08)
    ax.tick_params(colors='white')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'pgs_mandala.png', dpi=180, facecolor=COSMIC['bg'])
    plt.close()
    print("Saved jaw-dropping: pgs_mandala.png")

# 5. "4D" Projection Animation (slices of multi-feature space)
def generate_4d_projection(gaps):
    # Features: [logp, width, min_d, w_offset, avg_z, p%30]
    feats = []
    for g in gaps[:150]:
        logp = np.log10(g['p'])
        w_off = g['w'] - g['p']
        avg_z = g['zs'].mean()
        res = g['p'] % 30
        feats.append([logp, g['width'], g['min_d'], w_off, avg_z, res])
    feats = np.array(feats)
    
    # Simple 4D -> 3D by using 4th dim as time/color in animation frames
    fig = plt.figure(figsize=(10,8), facecolor=COSMIC['bg'])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(COSMIC['bg'])
    
    def update(frame):
        ax.clear()
        ax.set_facecolor(COSMIC['bg'])
        t = (frame / 20) % 1.0
        # Project: x=logp, y=width, z=min_d, color=4th (w_off) modulated by t, size=5th
        c = feats[:,3] * (0.5 + 0.5*np.sin(t * 2*np.pi))  # oscillating 4th dim
        s = np.full(len(feats), 20) + feats[:,4] * 30
        scatter = ax.scatter(feats[:,0], feats[:,1], feats[:,2], c=c, s=s, cmap='coolwarm', alpha=0.7)
        ax.set_xlabel('log p', color='white')
        ax.set_ylabel('gap width', color='white')
        ax.set_zlabel('min τ', color='white')
        ax.set_title(f'4D Projection Slice (t={t:.2f}): logp x width x min_d\nColor/Size encode w_offset + avgZ "hidden dims"', color='white', fontsize=10)
        ax.tick_params(colors='white')
        return scatter,
    
    ani = animation.FuncAnimation(fig, update, frames=20, interval=200, blit=False)
    gif_path = OUT_DIR / '4d_projection_slice.gif'
    ani.save(gif_path, writer='pillow', fps=5)
    plt.close()
    print(f"Saved jaw-dropping animation: {gif_path}")

# 6. Plotly Cosmic Nebula (interactive 3D "universe")
def generate_plotly_nebula(gaps):
    df = pd.DataFrame({
        'logp': [np.log10(g['p']) for g in gaps],
        'width': [g['width'] for g in gaps],
        'min_d': [g['min_d'] for g in gaps],
        'w_rel': [(g['w']-g['p'])/g['width'] for g in gaps],
        'avg_z': [g['zs'].mean() for g in gaps],
        'res': [g['p']%30 for g in gaps]
    })
    
    fig = go.Figure(data=[go.Scatter3d(
        x=df['logp'], y=df['width'], z=df['min_d'],
        mode='markers',
        marker=dict(
            size=df['avg_z']*40 + 5,
            color=df['w_rel'],
            colorscale='Rainbow',
            opacity=0.75,
            colorbar=dict(title='Relative GWR position')
        ),
        text=[f"p={g['p']}, w={g['w']}, minτ={g['min_d']}, Z~{g['zs'].mean():.3f}" for g in gaps],
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='PGS Cosmic Nebula (Interactive 3D)<br>Stars = gaps. Size ~ avg Z (DNI "brightness"). Color = w position in gap. Fly through with plotly!',
        scene=dict(
            xaxis_title='log10(p)',
            yaxis_title='Gap Width',
            zaxis_title='min τ(w)',
            bgcolor=COSMIC['bg']
        ),
        paper_bgcolor=COSMIC['bg'],
        font_color='white',
        width=1100, height=800
    )
    html_path = OUT_DIR / 'cosmic_nebula_3d.html'
    fig.write_html(html_path)
    print(f"Saved jaw-dropping interactive: {html_path}")

def main():
    print("=== Generating BUCK-WILD jaw-dropping PGS visualizations ===")
    gaps = get_sample_gaps(120, 8000)
    df_square = load_square_branch_data()
    
    generate_square_branch_cosmos(df_square)
    generate_fractal_square_tree(df_square)
    generate_pgs_mandala(gaps)
    generate_4d_projection(gaps)
    generate_plotly_nebula(gaps)
    
    # Animation (may be slower)
    try:
        generate_ridge_flight_gif(gaps[:25], n_frames=30)
    except Exception as e:
        print("Animation skipped (imageio/pillow issue):", e)
    
    print("\n=== All buck-wild viz generated in visualizations/core-diagrams/plots/generated/jawdropping/ ===")
    print("Ideas include: 3D cosmic universes with constellations, recursive fractals, mandalas, 4D time-sliced projections, animated flights, interactive nebulae.")
    print("These push the geometric + arithmetic intuition of PGS (square branches as cosmic structures, ridges as nebulae, etc.).")

if __name__ == "__main__":
    main()
