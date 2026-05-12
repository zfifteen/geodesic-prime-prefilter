# Current Headline Results

- **The single live proof reference is [../PROOF.md](../PROOF.md).** It is the
  definitive status source for the direct deterministic next-prime theorem and
  the prime-gap maximizer theorem.
- **The direct deterministic next-prime theorem is universal under its stated
  hypotheses.** Given a known prime `p`, exact divisor counts determine the next
  prime `q`.
- **The prime-gap maximizer theorem is universal under its stated hypotheses.**
  In every prime gap with a nonempty interior, the log-score maximizer is the
  first interior integer with the smallest divisor count.
- **Audit tables certify finite cases and preserve provenance.** They do not
  limit the theorem. The proof status comes from `PROOF.md`, not from external
  artifacts, old proof-chain notes, or generated summaries.
- **The maximizer theorem supports deterministic next-prime inference.** It
  identifies the selected interior integer used by the repository's direct
  deterministic `p -> q` algorithm.
- **The exact DNI/GWR next-prime oracle remains exact by construction.** Given
  a known prime `p`, the unbounded walker recovers the next prime from the
  ordered divisor structure of the next-gap interior. See
  [../research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md](../research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md).
- **The recursive walk surface remains exact on the committed tested ladder.**
  The DNI transition rule is exact on `743,075 / 743,075` rows from the
  combined `10^6 + 10^7` next-gap surface, and the recursive walk records
  `664,578 / 664,578` exact consecutive next-prime recoveries from prime `11`
  through prime `10,000,121` with `0` skipped gaps.
- **The semiprime branch clears its first full `127`-bit official gate.** The
  centered `PGS` audit on the committed `12`-case surface passes at rung `2`,
  with `1.0` top-1 routed-window recall, `1.0` top-4 routed-window recall,
  `0.75` exact recovery recall, and the archived exact `127`-bit case recovered
  on the official path. See
  [../research/06-cryptology-rsa/docs/semiprime_branch/pgs_127_official_gate_breakthrough.md](../research/06-cryptology-rsa/docs/semiprime_branch/pgs_127_official_gate_breakthrough.md).
- **The old fixed cutoff theorem is false and stays archived as false.** The
  fixed map `{2:44, 4:60, 6:60}` fails at `q = 24,098,209`.
- **The live bounded walker is certified on the committed exact surface through
  `q <= 10^7`.** The bounded rule is the empirical compression
  `C(q) = max(64, ceil(0.5 * log(q)^2))`, and the live honesty gate is the
  exact compare scan in
  [../research/04-bounded-compression/scripts/gwr_dni_cutoff_counterexample_scan.py](../research/04-bounded-compression/scripts/gwr_dni_cutoff_counterexample_scan.py).
- **Deterministic prefilter performance remains the practical payoff.** The
  current production Python path rejects about `91%` of tested odd candidates
  before Miller-Rabin and produced `2.09x` and `2.82x` end-to-end deterministic
  RSA key-generation speedups on the curated `2048`-bit and `4096`-bit corpora.
  See [research/06-cryptology-rsa/legacy-prefilter/docs/benchmarks.md](../research/06-cryptology-rsa/legacy-prefilter/docs/benchmarks.md).
