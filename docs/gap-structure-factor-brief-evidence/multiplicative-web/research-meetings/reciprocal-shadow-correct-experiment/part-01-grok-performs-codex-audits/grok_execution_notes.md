# Grok Execution Notes - Part One Residue-Certificate Probe

**Task:** Part One of the cross-audited reciprocal-shadow correct experiment.  
**Role:** Performer (Grok). Codex will audit.  
**Directive followed:** Contract adherence and falsifiability over any positive-result optimization.  
**Date of execution:** single deterministic run in this session.

## What Was Written (exact inventory)

All artifacts created exclusively inside:

```
/.../reciprocal-shadow-correct-experiment/part-01-grok-performs-codex-audits/
```

- `reciprocal_shadow_residue_certificate_probe_grok.py` (the self-contained probe, ~280 lines)
- `output/summary.json` (20 case records with full metrics + classification)
- `output/certificate.jsonl` (960 lines: every admissible (a, y, rank, is_p_member) across all cases and three surfaces)
- `output/summary.md` (table + plain-English observed-result summary)
- `output/runtime_residue_crt_log.jsonl` (960 lines: every inv/b/CRT arithmetic step that produced an accepted a)
- `self_checklist.md` (explicit 12-item answers with one PARTIAL noted plainly)
- `grok_execution_notes.md` (this file)

No other files touched, no files created or edited outside this folder tree.

## Preparation Steps (contract-first)

1. Read the controlling HTML design contract in full (all sections, tables, appendices, checklist).
2. Read the two invalidated/boundary MDs.
3. Located the reference 16-case list and `composite_rows` / `rotated_offset_control_rows` logic (read-only).
4. Confirmed the exact required mechanism (build held-out rows at r=300, top-4 r by degree or fallback to 3, per-a b-collection from threads, conflict-on-multi-b reject, CRT to y, emit C; identical on rotated + deterministic synthetic; p/q only for construction/hold-out + post-emission audit).
5. Chose the 4 additional cases via sympy (development only) to satisfy "sqrtN > 10M" and "at least two with p < 0.6 sqrtN"; hardcoded the verified primes; made all four low-ratio so the surface contains 4 such cases.
6. Structured the code with a clear `build_case` boundary so that `compute_residue_certificate` is completely blind to p/q.
7. Implemented deterministic synthetic (canonical factor-signature sort + consecutive centered offsets) - no random.
8. Added wheel-optimized trial division only for web-construction speed (still pure Python, no external deps in final run).
9. Ran the script once; it wrote all four output files before any human-facing MD was authored.

## Observed Mathematical Reality (no spin)

- For every one of the 20 cases the highest-degree thread factors were exactly [2, 3, 5, 7], M = 210.
- Because every thread for a given r in the *true* web satisfies `offset ≡ -N (mod r)`, the b-values computed from any invertible a are identical within each r. Hence the conflict filter never fires for coprime a. The admissible set is exactly the 48 residues coprime to 210.
- Controls destroy that shared congruence; after reassignment the offsets for any r with degree >= 2 become incongruent mod r, every a produces multiple distinct b's inside at least one r, and |C| collapses to 0 for both controls on all 20 cases.
- Consequently p (large prime) is always inside the true C and never inside either control C.
- Ranks inside the true C (sorted by ascending a) are the order statistics of (p mod 210) among the 48 coprimes; they ranged from 5 to 44 for the concrete p values. None landed at 1 or 2.
- All |C_true| = 48 <= 64.
- All 20 cases therefore received the classification `boundary_measurement`.

This is not a failure of the implementation; it is the exact behavior of the closure rule that the contract asked to be operationalized. The "reciprocal residue closure" as defined by the per-r b-agreement test + CRT reduces, on a true web, to the coprimality condition with respect to the dominant small prime threads. The procedure cleanly distinguishes true web from offset-scrambled controls (48 vs 0), but does not further narrow the admissible set to a handful of classes that would place p at rank 1-2.

The experiment therefore measures a real structural property (the web's modular coherence produces exactly the unit group mod M as its admissible certificate) while falsifying the stronger hope that this particular selector would be tight enough for low-rank nomination on the tested surface.

## Compliance With Part One Prompt & AGENTS.md

- Followed the "residue-certificate experiment, not a numeric factor walk."
- Used p/q only for the two explicitly allowed roles.
- No Miller-Rabin, no gcd(candidate, N), no round(N/x), no product closure, no candidate stream, no fallback.
- Deterministic synthetic control (no random).
- Runtime log contains only the arithmetic that contributed members to C; free of forbidden operations.
- All classification language uses the four required strings; no "factor discovered" language.
- PGS-native framing preserved in the surrounding documentation (locked local web -> reciprocal transport -> modulus-link closure -> structural certificate -> audit).
- Wrote only inside the designated Part One folder.

## Minor Notes for Codex Audit

- The wheel optimization in `factorization`/`is_prime` was added solely to keep the 4 large-N web builds under ~15 s each (total run ~60 s). It does not affect the certificate logic.
- `divisor_count` in the row dict is computed but never used by the certificate generator (harmless).
- In the synthetic control the offsets are consecutive integers centered at zero; this guarantees that for r >= 2 any r with >= 2 threads will see incongruent residues, producing the observed |C|=0. The choice is fully deterministic and reproducible.
- The 960 log entries and 960 cert rows are exactly the 20 * 48 admissible a's; no duplicates or omissions.
- `summary.md` inside `output/` was written by the probe itself (raw artifact). The two top-level MDs (`self_checklist.md`, this notes file) were written immediately after the run completed and the raw files existed.

## Deliverables Complete

The required seven deliverables exist, the 12-item checklist is explicitly answered with one plainly named limitation, and the surface was produced under a single deterministic execution that any later auditor can re-run from the committed script.

This concludes the Part One performer work. All state is in the committed artifacts; no further edits will be made to this folder by the performer.

**Grok** - 2026 session (Part One complete, ready for Codex audit).