# PGS Research Corpus

This directory is the permanent home for PGS research chapters.

Root-level authority files remain at the repository root:

- `AGENTS.md`: local Codex contract and PGS reasoning discipline.
- `PROOF.md`: single live proof reference.
- `RESULTS.md`: repo-wide measured and audit surfaces.
- `PRIME_GAP_GENERATOR.md`: public generator contract.
- `research/00-index/continuity/START_HERE.md`: continuity router.

## Chapter Map

See `status-map.md` for the migration status, validation state, and next action
for each chapter.

| Chapter | Research Family | Migration Status |
| --- | --- | --- |
| `01-generator` | Minimal PGS Generator and production evidence | mapped and validated |
| `02-gwr-dni` | GWR, DNI, divisor-count structure, and chamber mechanics | mapped and validated |
| `03-gap-types` | Gap-type grammar, public framing, and visual sequence surfaces | mapped and validated |
| `04-bounded-compression` | Dynamic cutoff, bounded compression, square-branch pressure | mapped and validated |
| `05-state-budget` | State-budget carriers, `d4_count`, and hidden-state probes | mapped and validated |
| `06-cryptology-rsa` | RSA v2/v3, modulus-link, semiprime, and certificate work | mapped and validated |
| `06-cryptology-rsa/docs/shor_order_entropy` | PGS-Shor order entropy sidecar finding | topic added |
| `07-oeis` | OEIS candidate sequence workflow and submission drafts | workflow initialized |
| `08-collatz` | Collatz-adjacent PGS experiments | migrated and validated |
| `09-exponents` | Mersenne/exponent-wall PGS experiments | migrated and validated |
| `10-twin-primes` | Twin-prime PGS experiments | migrated and validated |
| `11-gap-ridge` | Gap-ridge and chamber-ridge investigations | mapped |
| `12-rh-bridge` | DNI-to-zeta translation and RH-facing explanation | active |
| `13-prime-spiral` | Prime-spiral visualization and structure work | mapped |
| `14-sha-nonce` | SHA/nonce adjacency probes | mapped |
| `15-documentation-correction` | Public documentation correction and framing audit | active |

## Status Vocabulary

- `proved`: universal theorem under the hypotheses stated in a proof artifact.
- `measured`: finite computational result with exact regime and output path.
- `audited`: generated output checked by a separate validation path.
- `hypothesis`: live explanatory candidate awaiting proof or falsification.
- `unresolved`: open blocker, survivor, missing invariant, or non-closing rule.
- `invalidated`: rule or conjecture falsified by a named artifact.
- `archived`: historical output retained for provenance, not active evidence.

## Migration Rule

Move one chapter at a time. Each migration must preserve theorem status,
measured evidence, audit status, invalidated rules, unresolved state, and a
deterministic reproduction path.
