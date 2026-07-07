---
name: gwr-resonance
description: Compute GWR (Leftmost Minimum-Divisor Rule / selected composite), divisor counts, zero-excess DNI E(n), Z(n), and primorial modular resonance for a range or gap. Use for any PGS advance, chamber analysis, or data surface update. PGS-native only.
---
# GWR + Resonance Skill

## Setup (one time in container)
cd $PGS_ROOT && python3 -m pip install -e ./src/python -q || true

## Usage
node skills/gwr-resonance/gwr-resonance.cjs "start_p" "end_p"   # or range of integers
# Outputs JSON with gwr_witness, e_n, resonance, etc. for PGS director.

Example:
node skills/gwr-resonance/gwr-resonance.cjs 89 97
