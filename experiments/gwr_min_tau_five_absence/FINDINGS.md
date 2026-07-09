# GWR Minimum Divisor Count Never Equals 5 in Standard Prime Gaps

**Strongest measured claim (this surface):**  
In every standard consecutive-prime gap (p, q) with nonempty interior on all ranges tested, direct exhaustive computation to 10^7 and project generator / probe surfaces through 10^18-scale regimes, the minimum value of the divisor-count field τ(n) for n in the interior never equals 5.

5 does not appear as the GWR-selected minimum (i.e., τ(w) ≠ 5 for the leftmost minimum-τ integer w inside any such gap).

## Observable Object
Between any two consecutive primes p < q the integers p+1 … q-1 form an ordered finite sequence. Each carries an exact divisor count τ(n). The GWR (Leftmost Minimum-Divisor Rule) identifies the first n in that sequence whose τ value is the global minimum over the whole interior. Call that minimum value m = min{τ(n) : p < n < q}.

Across all such sequences, m = 5 has never been observed.

## Why This Is a Real Surface (Not Tautological)
- The endpoint rule (first return to τ = 2) is definitional with the divisor characterization of primes.
- The interior ordering rule (GWR) and the fact that certain low values of m are possible while others (specifically 5) are absent on huge ranges is an empirical property of the divisor-count field inside prime gaps.
- Higher odd minima (9, 15, …) do occur, though rarely. The value 5 is skipped.

## Reproduction
Run the accompanying script:

```bash
python3 experiments/gwr_min_tau_five_absence/scan_for_min_tau_five.py --limit 2000000
```

Fresh run (2026-06-02) to 2 million produces:

- 148,931 gaps with nonempty interior
- Occurrences of min_τ == 5: **0**
- Distribution includes 3 (223), 4 (dominant), 6, 8, 9 (8 times), 10, 12, ..., 15 (4 times), ... but no 5.

Full output captured in `results_2M.txt` in this folder.

Cross-checks against existing project artifacts (SHA-256 constants gaps probe + baselines in research/06-cryptology-rsa/, GWR data in research/02-gwr-dni/, generator runs to 10^18-scale) show the identical absence.

## PGS-Native Interpretation
The divisor-count field inside a resolved prime gap (endpoints fixed by the direct τ=2 rule) is not an arbitrary sequence of integers ≥ 3. Its minimum value m is constrained by the density of low-τ composites (especially τ = 4 semiprimes and prime cubes).

For m = 5 the entire interior would have to contain a fourth power r⁴ while containing *no* numbers with τ ≤ 4. No such run of consecutive composites occurs between consecutive primes.

This is consistent with the square-branch discussion in PROOF.md: τ(w) = 3 is the lowest odd possibility and receives special treatment; the next odd candidates are heavily suppressed or eliminated by the presence of τ = 4 numbers.

## Status Separation
- **Proved (universal)**: Once a gap is fixed, the leftmost min-τ integer w uniquely maximizes F(n) = (1 − τ(n)/2) log n (PROOF.md, Interior Maximizer Theorem + GWR).
- **Measured surface (this artifact)**: On all standard prime gaps examined to 10^18-scale, the realized value of that minimum is never 5.
- **Unresolved**: Whether m = 5 is *impossible* at all scales (would require a separate proof that no prime gap interior is free of τ = 4 numbers while containing a τ = 5 number). Current evidence is purely empirical but extremely strong.
- **Related but distinct**: Higher odd minima (9, 15, …) do realize occasionally; the absence is specific to 5 (and certain other small odds) in the standard prime-to-prime setting.

## Relation to @materion Thread (2026-06)
This observation directly answers the public question raised in the conversation at https://x.com/alltheputs/status/2061600892097282514 (and the follow-up at https://x.com/alltheputs/status/2061642721660477634 where the question "Why did you ask?" was posed publicly).

In standard prime gaps the divisor-count field under GWR never selects 5 as its minimum.

See the subfolder `power_gaps_probe/` for an initial extension to "mixed prime power gaps" (intervals between primes and their p^2/p^3/p^4). Even there, min_τ=5 is absent up to 1e6 (0 occurrences across ~78k interiors), though higher odds like 9 and 15 still appear.

A companion note `geometric_aspects_note.md` (same folder) inventories the geometric aspects of PGS that have emerged so far (the row/profile, the gap-ridge landscape, the square U_□ utilization construction, visualizations), in direct response to the shift in focus toward geometric questions.

## Why @materion Specifically Asked About 5
@materion's public posting history around this time is dominated by geometric constructions: gnomons for sums of odds building squares, dividing diameters/circles into fractions (2/3+1/3, 4/5+1/5) that generate cascades of square roots and right triangles, area-preserving diagrams, and "geometry as shortcut to algebra."

"Uneven number of divisors" = odd τ(n) exactly when n is square. This is a direct bridge to his diagrammatic thinking about squares.

In the 23-29 example (central to the thread), the GWR w=25=5² has τ=3 (smallest odd >1). He observed that odd mins in prime gaps appear to be *only* 3.

5 is the next odd τ value, realized by fourth powers p^4 = (p²)², literally a square of a square. This is the natural next "geometric" object after p² in his pattern-recognition style.

The follow-up question about "gaps between mixed sets of primes and their squares or cubes" + "other prime related gaps" suggests he is imagining alternative ordered sets/interiors whose endpoints or contents are generated by primes + their power "squares" (in the geometric sense), and asking whether in those alternative canvases the GWR min can reach the next odd value (5).

His question is a geometrically motivated probe into the possible values of the minimum in the divisor-count field when the underlying generator set is expanded. It is a sharp test of how constrained ("non-chaotic") the structure really is.

The computations (standard gaps + mixed power gaps) show the constraint is robust: 5 is skipped in both.

This is exactly the kind of concrete, example-driven question that aligns with "drawing little arrows on a piece of paper" to reveal hidden order.

## Files in This Folder
- scan_for_min_tau_five.py, reproducible scanner
- FINDINGS.md, this document

## Date of This Surface
2026-06-02 (fresh verification run + cross-check against existing project data)

---

This is implementation evidence, not a theorem boundary. It records a concrete, reproducible property of the divisor-count field inside the ordered interiors produced by the direct deterministic next-prime rule.
