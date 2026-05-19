# Reciprocal Shadow Residue Certificate Probe (Grok Part One)

Controlling contract: reciprocal_shadow_correct_experiment_design.html
Implementation strictly follows the residue-certificate mechanism (conflict filter + CRT).
No candidate walks, no hidden p/q in generator, deterministic controls only.

## Surface Summary (20 cases: 16 original + 4 new natural-ratio >10M sqrtN)

| idx | N | p | p/sqrtN | M | selected r | |C_true| | p rank true | |C_rot| | |C_synth| | classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 713 | 23 | 0.8846 | 210 | [2, 3, 5, 7] | 48 | 6 | 0 | 0 | boundary_measurement |
| 1 | 2537 | 43 | 0.8600 | 210 | [2, 3, 5, 7] | 48 | 11 | 0 | 0 | boundary_measurement |
| 2 | 5063 | 61 | 0.8592 | 210 | [2, 3, 5, 7] | 48 | 15 | 0 | 0 | boundary_measurement |
| 3 | 10057 | 89 | 0.8900 | 210 | [2, 3, 5, 7] | 48 | 21 | 0 | 0 | boundary_measurement |
| 4 | 13837 | 101 | 0.8632 | 210 | [2, 3, 5, 7] | 48 | 23 | 0 | 0 | boundary_measurement |
| 5 | 21877 | 131 | 0.8912 | 210 | [2, 3, 5, 7] | 48 | 30 | 0 | 0 | boundary_measurement |
| 6 | 36503 | 173 | 0.9058 | 210 | [2, 3, 5, 7] | 48 | 40 | 0 | 0 | boundary_measurement |
| 7 | 63433 | 229 | 0.9124 | 210 | [2, 3, 5, 7] | 48 | 5 | 0 | 0 | boundary_measurement |
| 8 | 112669 | 307 | 0.9164 | 210 | [2, 3, 5, 7] | 48 | 22 | 0 | 0 | boundary_measurement |
| 9 | 201703 | 401 | 0.8931 | 210 | [2, 3, 5, 7] | 48 | 44 | 0 | 0 | boundary_measurement |
| 10 | 368177 | 557 | 0.9191 | 210 | [2, 3, 5, 7] | 48 | 31 | 0 | 0 | boundary_measurement |
| 11 | 621787 | 701 | 0.8896 | 210 | [2, 3, 5, 7] | 48 | 17 | 0 | 0 | boundary_measurement |
| 12 | 1242079 | 1009 | 0.9057 | 210 | [2, 3, 5, 7] | 48 | 39 | 0 | 0 | boundary_measurement |
| 13 | 3206803 | 1601 | 0.8944 | 210 | [2, 3, 5, 7] | 48 | 30 | 0 | 0 | boundary_measurement |
| 14 | 12007001 | 3001 | 0.8661 | 210 | [2, 3, 5, 7] | 48 | 15 | 0 | 0 | boundary_measurement |
| 15 | 35026003 | 5003 | 0.8454 | 210 | [2, 3, 5, 7] | 48 | 40 | 0 | 0 | boundary_measurement |
| 16 | 225000307499857 | 7500013 | 0.5000 | 210 | [2, 3, 5, 7] | 48 | 18 | 0 | 0 | boundary_measurement |
| 17 | 225000094499417 | 6000011 | 0.4000 | 210 | [2, 3, 5, 7] | 48 | 23 | 0 | 0 | boundary_measurement |
| 18 | 225000309499937 | 4500007 | 0.3000 | 210 | [2, 3, 5, 7] | 48 | 29 | 0 | 0 | boundary_measurement |
| 19 | 225000215993999 | 3000017 | 0.2000 | 210 | [2, 3, 5, 7] | 48 | 38 | 0 | 0 | boundary_measurement |

## Observed Result (under exact operationalization)

For every case the top-4 r were always [2, 3, 5, 7], M=210.
True-web admissible set C is exactly the 48 residues a mod 210 with gcd(a,210)=1
(the a's for which modular inverses exist and the shared-offset congruence of the
true web guarantees b-agreement within each r).
Controls (rotated and synthetic) produce |C|=0 because the reassigned offsets
destroy the per-r congruence, causing b-conflicts on every a.

p always lies in true C (p large prime => coprime to 210).
p never lies in control C (empty).
Rank of p inside true C (sorted by a asc) is the order statistic of (p mod 210)
among the 48 coprime residues; typically mid-range (~5-40), never 1 or 2 for these p.

Classifications: 0 accepted_measured_result, 20 boundary_measurement,
0 invalidated_result, 0 unresolved_implementation_failure.

This is a boundary measurement of the closure rule as defined: the rule
nominates the full coprime class set (size 48 <=64), which contains p, while
controls nominate nothing. It does not achieve the hoped rank <=2 selector.
The result is deterministic, fully logged, and falsifiable under the contract.

## Checklist Status (see self_checklist.md for 12-item answers)

All 12 items answered explicitly in self_checklist.md. The surface satisfies
the structural-certificate contract and the explicit Part One requirements
(original 16 + 4 new with 4 low-ratio cases, deterministic controls,
p/q only in construction+final audit, runtime CRT log, raw outputs).

No files written outside the Part One folder.
