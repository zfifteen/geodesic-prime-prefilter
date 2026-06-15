#!/usr/bin/env python3
"""
Generate vibrant, stunning PGS visualizations: 2D profiles, 3D surfaces, 
polar, networks, interactive Plotly, etc.

Focus on core objects: divisor-count field in gaps, GWR w, DNI Z/E scores, ridges.
"""

import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.io as pio
import sympy
from sympy import primerange, divisor_count
import networkx as nx
from collections import defaultdict

# Output dir
OUT_DIR = Path(__file__).parent / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Vibrant PGS color palette (from existing apps + enhanced)
PGS_COLORS = {
    'prime': '#8fd3ff',
    'square': '#ffe66d',  # tau=3
    'cube': '#ffb703',
    'd4': '#43d4c8',      # semiprime/tau=4
    'higher_even': '#6d8cff',
    'higher_odd': '#b76aff',
    'selected': '#ff4f49', # GWR w
    'ridge': '#ff9f1c',
    'background': '#0a0e14',
    'grid': '#253140',
    'surface': '#10161d',
}

def get_gap_data(p, q):
    """Compute interior n, d(n), Z(n), E(n) for gap p to q."""
    interior = list(range(p + 1, q))
    ds = [divisor_count(n) for n in interior]
    ns = np.array(interior)
    ds_arr = np.array(ds)
    # DNI Z = n ** (1 - d/2)
    zs = ns ** (1 - ds_arr / 2.0)
    # E = (d/2 - 1) * ln(n)
    es = (ds_arr / 2.0 - 1) * np.log(ns)
    # Find GWR w: leftmost min d
    min_d = min(ds)
    w_idx = ds.index(min_d)
    w = interior[w_idx]
    return ns, ds_arr, zs, es, w, min_d

def get_multiple_gaps(max_p=1000, num_gaps=50):
    """Get data for many consecutive gaps."""
    primes = list(primerange(2, max_p))
    gaps = []
    for i in range(min(num_gaps, len(primes)-1)):
        p, q = primes[i], primes[i+1]
        if q - p > 1:
            ns, ds, zs, es, w, min_d = get_gap_data(p, q)
            gaps.append({
                'p': p, 'q': q, 'ns': ns, 'ds': ds, 'zs': zs, 'es': es,
                'w': w, 'min_d': min_d, 'gap_width': q - p
            })
    return gaps

def plot_vibrant_2d_profile(gap_data, title, filename):
    """Stunning 2D gap profile with colored bars, Z curve, markers."""
    ns, ds, zs, es, w, min_d = gap_data['ns'], gap_data['ds'], gap_data['zs'], gap_data['es'], gap_data['w'], gap_data['min_d']
    p, q = gap_data['p'], gap_data['q']
    
    fig, ax1 = plt.subplots(figsize=(14, 8), facecolor=PGS_COLORS['background'])
    ax1.set_facecolor(PGS_COLORS['background'])
    
    # Color bars by d(n) class
    colors = []
    for d in ds:
        if d == 2: colors.append(PGS_COLORS['prime'])
        elif d == 3: colors.append(PGS_COLORS['square'])
        elif d == 4: colors.append(PGS_COLORS['d4'])
        elif d % 2 == 0: colors.append(PGS_COLORS['higher_even'])
        else: colors.append(PGS_COLORS['higher_odd'])
    
    # Bar plot for divisor counts (height proportional to d, but vibrant)
    bar_heights = ds
    bars = ax1.bar(ns, bar_heights, width=0.8, color=colors, alpha=0.85, edgecolor='white', linewidth=0.3)
    
    # Highlight GWR w
    w_idx = list(ns).index(w)
    ax1.bar(w, bar_heights[w_idx], width=0.8, color=PGS_COLORS['selected'], alpha=1.0, edgecolor='white', linewidth=2, zorder=5)
    
    ax1.set_xlabel('n (gap interior)', color='white', fontsize=12)
    ax1.set_ylabel('divisor count τ(n)', color='white', fontsize=12)
    ax1.tick_params(colors='white')
    ax1.set_ylim(0, float(max(ds)) * 1.2)
    
    # Overlay Z(n) curve on twin axis (vibrant line)
    ax2 = ax1.twinx()
    ax2.plot(ns, zs, color=PGS_COLORS['ridge'], linewidth=3, label='Z(n) = n^(1-τ(n)/2)', zorder=6)
    ax2.plot(ns, zs, color='white', linewidth=1, alpha=0.3, zorder=5)  # glow
    ax2.set_ylabel('Z(n) (DNI score)', color=PGS_COLORS['ridge'], fontsize=12)
    ax2.tick_params(colors=PGS_COLORS['ridge'])
    
    # Mark w on Z
    ax2.scatter([w], [zs[w_idx]], color=PGS_COLORS['selected'], s=200, zorder=7, edgecolors='white', linewidths=2, marker='*', label=f'GWR w={w} (τ={min_d})')
    
    # Annotations
    ax1.axvline(p, color='white', linestyle='--', alpha=0.5, label=f'p={p}')
    ax1.axvline(q, color='white', linestyle='--', alpha=0.5, label=f'q={q}')
    
    # Next square for U_□ if relevant
    import math
    sqrt_w = int(math.isqrt(w))
    next_prime_after_sqrt = sympy.nextprime(sqrt_w)
    next_sq = next_prime_after_sqrt ** 2
    if next_sq < q + 100:
        ax1.axvline(next_sq, color=PGS_COLORS['square'], linestyle=':', alpha=0.7, linewidth=2)
        ax1.text(next_sq, max(ds)*0.9, f'next square\n{next_sq}', color=PGS_COLORS['square'], fontsize=9, ha='left')
    
    ax1.set_title(f'PGS Gap Profile: {p} → {q} (width={q-p})\nVibrant Divisor Field + DNI Z Ridge + GWR Selection', 
                  color='white', fontsize=14, pad=20)
    ax1.legend(loc='upper left', facecolor=PGS_COLORS['surface'], edgecolor='white', labelcolor='white')
    ax2.legend(loc='upper right', facecolor=PGS_COLORS['surface'], edgecolor='white', labelcolor='white')
    
    # Style
    for spine in ax1.spines.values():
        spine.set_color('white')
    for spine in ax2.spines.values():
        spine.set_color(PGS_COLORS['ridge'])
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, facecolor=PGS_COLORS['background'], edgecolor='none')
    plt.close()
    print(f"Saved 2D profile: {filename}")

def plot_3d_ridge_stack(gaps, filename):
    """Stunning 3D: stacked Z surfaces for multiple gaps, ridge visible."""
    fig = plt.figure(figsize=(16, 12), facecolor=PGS_COLORS['background'])
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor(PGS_COLORS['background'])
    
    max_len = max(len(g['ns']) for g in gaps[:20])  # limit for viz
    
    for i, gap in enumerate(gaps[:20]):
        ns = gap['ns']
        zs = gap['zs']
        # Normalize x to 0-1 for stacking
        x = np.linspace(0, 1, len(ns))
        y = np.full(len(ns), i)
        z = np.asarray(zs, dtype=float)
        
        # Color by d
        colors = []
        for d in gap['ds']:
            if d == 3: c = PGS_COLORS['square']
            elif d == 4: c = PGS_COLORS['d4']
            elif d % 2 == 0: c = PGS_COLORS['higher_even']
            else: c = PGS_COLORS['higher_odd']
            colors.append(c)
        
        # Filter finite positive for 3D stability
        valid = np.isfinite(z) & (z > 0)
        if np.any(valid):
            ax.plot(x[valid], y[valid], z[valid], color=PGS_COLORS['ridge'], linewidth=1.5, alpha=0.7)
            ax.scatter(x[valid], y[valid], z[valid], c=[c for c,v in zip(colors, valid) if v], s=10, alpha=0.6)
        
        # Highlight w
        w_idx = list(ns).index(gap['w'])
        ax.scatter([x[w_idx]], [i], [z[w_idx]], c=PGS_COLORS['selected'], s=50, marker='*', zorder=10)
    
    ax.set_xlabel('Normalized position in gap', color='white')
    ax.set_ylabel('Gap index (increasing p)', color='white')
    ax.set_zlabel('Z(n) DNI score', color='white')
    ax.set_title('3D Stacked DNI Z "Ridge Mountains" Across Consecutive Gaps\n(near-edge ridge emerges as low-excess peaks near boundaries)', 
                 color='white', fontsize=14, pad=20)
    
    # Style
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.edgecolor = PGS_COLORS['grid']
    ax.yaxis.pane.edgecolor = PGS_COLORS['grid']
    ax.zaxis.pane.edgecolor = PGS_COLORS['grid']
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, facecolor=PGS_COLORS['background'])
    plt.close()
    print(f"Saved 3D ridge stack: {filename}")

def plot_interactive_3d_scatter(gaps, filename_html):
    """Interactive Plotly 3D: points (p, gap_width, min_d) colored by w_offset, size by enrichment."""
    xs, ys, zs, colors, texts, sizes = [], [], [], [], [], []
    for g in gaps:
        xs.append(np.log10(g['p']))
        ys.append(g['gap_width'])
        zs.append(g['min_d'])
        # Color by relative w position (left=0, right=1)
        w_offset = g['w'] - g['p']
        rel_pos = w_offset / g['gap_width']
        colors.append(rel_pos)
        texts.append(f"p={g['p']}<br>q={g['q']}<br>width={g['gap_width']}<br>min_d={g['min_d']}<br>w={g['w']} (rel={rel_pos:.2f})")
        sizes.append(5 + g['gap_width'] / 2)
    
    fig = go.Figure(data=[go.Scatter3d(
        x=xs, y=ys, z=zs,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='GWR w relative position (0=left,1=right)')
        ),
        text=texts,
        hoverinfo='text'
    )])
    
    fig.update_layout(
        title='Interactive 3D PGS Feature Space: log(p) x gap_width x min_τ(n)<br>Color = relative position of GWR-selected w in gap',
        scene=dict(
            xaxis_title='log10(p)',
            yaxis_title='gap width',
            zaxis_title='min divisor count τ(w)',
            bgcolor='#0a0e14'
        ),
        paper_bgcolor='#0a0e14',
        font_color='white',
        width=1200, height=800
    )
    
    fig.write_html(filename_html)
    print(f"Saved interactive 3D: {filename_html}")

def plot_polar_ridge(gaps, filename):
    """Polar plot: angle = mod 30 residue, radius = 1/Z or something, color ridge strength."""
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'}, facecolor=PGS_COLORS['background'])
    ax.set_facecolor(PGS_COLORS['background'])
    
    residues = []
    ridge_strengths = []
    for g in gaps[:100]:
        # Simple: use left edge enrichment as "ridge strength"
        # For demo, use inverse min_d or gap features
        strength = 1.0 / g['min_d']  # stronger for low min_d (stronger structure)
        res = g['p'] % 30
        residues.append(res)
        ridge_strengths.append(strength)
    
    # Bin by residue
    from collections import defaultdict
    res_bins = defaultdict(list)
    for r, s in zip(residues, ridge_strengths):
        res_bins[r].append(s)
    
    thetas = []
    rs = []
    for res in sorted(res_bins):
        avg_strength = np.mean(res_bins[res])
        thetas.append(res * np.pi / 15)  # scale to 0-2pi
        rs.append(avg_strength)
    
    ax.scatter(thetas, rs, c=rs, cmap='plasma', s=100, alpha=0.8, edgecolors='white')
    ax.set_title('Polar View: Ridge Strength by mod-30 Residue Class\n(Stronger low-τ structure in certain arithmetic progressions)', 
                 color='white', pad=20)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, facecolor=PGS_COLORS['background'])
    plt.close()
    print(f"Saved polar: {filename}")

def plot_divisor_network(gap_data, filename):
    """Network graph: nodes = interior n, edges if share prime factors (divisor relation), highlight w."""
    ns = gap_data['ns']
    G = nx.Graph()
    for n in ns:
        G.add_node(n, d=divisor_count(n))
    
    # Connect if gcd >1 (share factor) - simplistic for viz
    for i, n1 in enumerate(ns):
        for n2 in ns[i+1:]:
            if sympy.gcd(n1, n2) > 1:
                G.add_edge(n1, n2)
    
    pos = nx.spring_layout(G, seed=42)
    
    fig, ax = plt.subplots(figsize=(12, 10), facecolor=PGS_COLORS['background'])
    ax.set_facecolor(PGS_COLORS['background'])
    
    # Color nodes
    node_colors = []
    for n in G.nodes():
        d = G.nodes[n]['d']
        if n == gap_data['w']:
            node_colors.append(PGS_COLORS['selected'])
        elif d == 3: node_colors.append(PGS_COLORS['square'])
        elif d == 4: node_colors.append(PGS_COLORS['d4'])
        elif d % 2 == 0: node_colors.append(PGS_COLORS['higher_even'])
        else: node_colors.append(PGS_COLORS['higher_odd'])
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, ax=ax, alpha=0.9)
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='white', ax=ax)
    
    # Label w
    w = gap_data['w']
    ax.annotate(f'GWR w={w}', xy=pos[w], xytext=(pos[w][0]+0.1, pos[w][1]+0.1),
                color='white', fontsize=10, arrowprops=dict(arrowstyle='->', color='white'))
    
    ax.set_title(f'Divisor Factor Network for Gap {gap_data["p"]}→{gap_data["q"]}\n(Edges = shared prime factors; star = GWR selected)', 
                 color='white', fontsize=12)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, facecolor=PGS_COLORS['background'])
    plt.close()
    print(f"Saved network: {filename}")

def main():
    print("Generating stunning PGS visualizations...")
    
    # Small example gap for detailed profiles (classic 23-29)
    small_gap = get_gap_data(23, 29)
    small_gap_dict = {'ns': small_gap[0], 'ds': small_gap[1], 'zs': small_gap[2], 
                      'es': small_gap[3], 'w': small_gap[4], 'min_d': small_gap[5],
                      'p':23, 'q':29}
    
    plot_vibrant_2d_profile(small_gap_dict, "23-29 Profile", OUT_DIR / "gap_23_29_vibrant_profile.png")
    
    # Many gaps
    gaps = get_multiple_gaps(max_p=5000, num_gaps=80)
    
    plot_3d_ridge_stack(gaps, OUT_DIR / "3d_ridge_mountains.png")
    plot_interactive_3d_scatter(gaps, str(OUT_DIR / "3d_feature_space.html"))
    plot_polar_ridge(gaps, OUT_DIR / "polar_ridge_mod30.png")
    
    # Network for one larger gap
    larger_gap = get_gap_data(113, 127)  # example
    larger_dict = {'ns': larger_gap[0], 'ds': larger_gap[1], 'zs': larger_gap[2], 
                   'es': larger_gap[3], 'w': larger_gap[4], 'min_d': larger_gap[5],
                   'p':113, 'q':127}
    plot_divisor_network(larger_dict, OUT_DIR / "divisor_network_113_127.png")
    
    print(f"\nAll plots saved to {OUT_DIR}")
    print("Ideas realized:")
    print("1. Vibrant 2D gap profile (colored τ bars + Z curve + U_□ square ref + GWR star)")
    print("2. 3D stacked ridge 'mountains' across gaps")
    print("3. Interactive Plotly 3D scatter of gap features (hover for details)")
    print("4. Polar plot of ridge strength by arithmetic progression (mod 30)")
    print("5. Factor-sharing network graph (divisor relations in interior, GWR highlighted)")
    print("\nOther imaginable: t-SNE embeddings of gap signatures, recursive square-branch trees,")
    print("volume renders of E(n) fields, animated ridge evolution, etc.")

if __name__ == "__main__":
    main()
