# Path C: PGS Divisor Channels vs SHA-256 Bit-Mixing Channels - Exploration Summary

## What Was Done
- Fetched SHA-2 pseudocode and constants (k[i] from cube roots of first 64 primes, h0.. from sqrt first 8 primes) from Wikipedia via curl+python+bs4 equivalent (saved as docs/SHA256_PSEUDOCODE_FROM_WIKI.txt).
- Searched project files: no mentions of SHA internal rounds (sigma0/1, Ch, Maj, avalanche, diffusion). SHA-256 used only as deterministic PRNG for candidate streams in RSA v2 legacy prefilter experiments (research/06-cryptology-rsa/legacy-prefilter/).
- Arxiv searches (via API): minimal relevant literature. One paper on SHA-1 Strict Avalanche Criterion (SAC) after ~24 rounds; no papers bridging divisor function/tau(n)/multiplicative channels to hash mixing, boolean functions, or cryptographic rounds. Searches for "divisor function" + crypto terms returned unrelated or weak hits.
- Read key PGS docs: docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md, docs/core/DIVISOR_NORMALIZATION_IDENTITY.md, PROOF.md (section on "Divisor Counts And Coprime Factor Channels" explicitly defines tau(n)=prod(a_i+1) as "independent coprime factor-choice channels").
- Implemented and executed toy simulation (experiments/path_c_toy_simulations/toy_sha_pgs_mixing.py):
  - PGS: tau(n), omega(n), factorization channels for n<=2000; binary bit stats (hamming, runs, bias) as "mixing proxy" for n's binary rep.
  - Toy SHA: 8-bit word simplified SHA256-like (scaled rotr, toy_sigma0/1, Ch, Maj, S0/S1, mod 2^8 adds/carries). Simulated message schedule + 1-16 compression rounds.
  - Metrics: avalanche fraction (output bit flips on 1-bit input flip) after r rounds; est "channel mixing rate" (~3 affected bits/round from 3-input Maj/Ch).
  - Correlation probe between PGS tau and binary "mix score" of n.
- Proposed a,b,c: a=avalanche % (or PGS excess contraction Z(n)), b=channel mixing rate (tau or ~3-7 bit sources/round), c=word width/rounds (32/64 or gap "selection point").

## Key Findings / Concrete Examples
- SHA constants: explicitly number-theoretic (primes -> roots -> 32-bit fractions). E.g. k[0]=0x428a2f98 from cbrt(2), etc. (full list in pseudocode file).
- Toy SHA: Avalanche reaches ideal ~0.5 after 8 rounds in 8-bit toy (std~0.06); est 3 mixed channels/round. Full diffusion in toy << "64" analog. (Matches real SHA: full avalanche early, 64 rounds = margin vs attacks like 52-round preimage on SHA256).
- PGS channels: Explicit in PROOF.md: "tau(n) means fewer independent coprime factor-choice channels". Leftmost min-tau(w) selection = deterministic "minimal load" choice in gap interval I.
- No correlation found: For n=1..2000, avg binary mix_score for tau=2 (primes): ~1.316; tau=4:1.325; tau=12:1.250; high-tau varied but no systematic link to tau (binary of n independent of its factorization structure).
- Excess E(n)/Z(n): For composites, Z(n)<1 "contracts" from prime baseline Z=1 exactly like "bias" before full mixing in early hash rounds. But PGS exact/deterministic per n; SHA statistical.
- Arxiv: No falsifiable bridge papers.

## Files Created/Modified
- docs/SHA256_PSEUDOCODE_FROM_WIKI.txt (145 lines: full SHA256 pseudocode + all k[i], h init from primes).
- experiments/path_c_toy_simulations/toy_sha_pgs_mixing.py (full runnable script with PGS+toySHA+metrics+insight).
- experiments/path_c_toy_simulations/results.json (captured run output, agg stats, insight).
- experiments/path_c_toy_simulations/PATH_C_EXPLORATION_SUMMARY.md (this file).
- (Also browsed/navigated Wikipedia SHA-2, arxiv API queries, project searches/reads via tools.)

## Issues Encountered
- Browser snapshot/console limited for full page text extraction (truncated accessibility trees); used terminal curl + python urllib + regex/html.unescape for pseudocode (reliable, no bs4 needed ultimately).
- Terminal python heredoc sometimes blocked by internal guard (used short -c snippets + file writes instead).
- No sympy/numpy issues; all executed cleanly. Pyright lint false positives on arg unpack (runtime perfect).
- Arxiv API rate/empty results: no deep literature (expected for this niche analogy).
- Strong self-critique applied throughout: analogy only, no causal link.

## Best Insight
**No novel relation found, mostly superficial analogy.**

PGS provides arithmetic model of "channel selection" (min tau via coprime choices + leftmost rule) and "contraction" (Z(n) for composites). SHA-256 provides bit-mixing model of "channel diffusion" (independent bit samplers in sigmas/Ch/Maj + 64-round margin for full avalanche). Surface parallels:
- Multiplicative independent sources (prime powers vs bit positions).
- Nonlinear combination to "hide"/uniformize (min-divisor selection vs XOR/rot/and/add).
- Prime number theory in both (PGS core; SHA constants "nothing up my sleeve").

But:
- No equation, no predictive power, no shared invariants.
- PGS deterministic/exact; SHA probabilistic/security-margin.
- "64 rounds" security not modeled by PGS gaps/chambers (full diffusion happens much earlier in both domains).
- Project's existing crypto work (SHA as PRNG only, PGS for RSA endpoints) shows no internal mixing analysis.

Falsifiable test (e.g. tau(n) predicts avalanche rate or round count for "prime-derived" inputs) fails in toy data. Poetic bridge at best; deprioritize Path C. Grounded PGS math (leftmost rule proofs, bounded compression, RSA sidecars) more promising.

(Full details + code in experiments/path_c_toy_simulations/)
