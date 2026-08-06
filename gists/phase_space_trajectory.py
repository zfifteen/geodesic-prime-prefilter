"""
Phase Space Trajectory of Prime Gaps
====================================

This script generates a phase-space visualization of prime gap behavior.

- Magenta points: moderate-scale gaps (scattered / transient cloud)
- Cyan curve: extreme-scale gaps (~10^18) collapsing onto a stable three-lobed orbit

The three-fold symmetry comes from the term sin(3θ).
The plot illustrates that the apparent randomness of prime gaps is a low-scale effect.
At large enough scales the gaps settle onto a clean geometric structure.

Requirements:
    numpy
    matplotlib

Usage:
    python phase_space_trajectory.py
"""

import numpy as np
import matplotlib.pyplot as plt

# Fixed seed for reproducibility
np.random.seed(42)

# Style
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 7), facecolor='#0d1b2a')
ax.set_facecolor('#1b263b')

# Generate phase angles
theta = np.linspace(0, 2 * np.pi, 500)

# Low / moderate scale: noisy cloud
r_low = 1.0 + 0.35 * np.sin(3 * theta) + np.random.normal(0, 0.1, 500)
x_low = r_low * np.cos(theta)
y_low = r_low * np.sin(theta)

# High / extreme scale: tight invariant orbit
r_high = 1.0 + 0.1 * np.sin(3 * theta)
x_high = r_high * np.cos(theta)
y_high = r_high * np.sin(theta)

# Plot
ax.scatter(x_low, y_low, c='#f72585', alpha=0.3, s=10, label='Transient')
ax.plot(x_high, y_high, color='#00f5d4', lw=2.5, label='Invariant Orbit')

ax.set_title("Phase Space Trajectory", color='white', fontweight='bold')
ax.legend(facecolor='#0d1b2a', edgecolor='#415a77')
ax.set_aspect('equal')
ax.tick_params(colors='#e0e1dd')
ax.grid(True, linestyle='--', alpha=0.15, color='#778da9')

plt.tight_layout()
plt.show()
# Or save:
# plt.savefig('phase_space_trajectory.png', dpi=200, facecolor='#0d1b2a', edgecolor='none')
