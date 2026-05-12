# Research Filesystem Migration Routing Manifest

This manifest records the physical routing contract for the chapter migration.
The migration moves research-owned artifacts into chapter homes and removes the
old scattered roots after references are repaired.

## Root Policy

- Root authority and public project documents stay at the repository root.
- Package and product source stays under `src/`.
- Root `tests/` is reserved for package-level and global contract tests.
- Chapter-owned scripts, tests, outputs, reviews, assets, and notes move under
  `research/<chapter>/`.

## Source Routing

| Source pattern | Destination |
| --- | --- |
| `docs/research/repo_reorganization/` | `research/00-index/repo-reorganization/` |
| `docs/research/codex_continuity/` | `research/00-index/continuity/` |
| `docs/research/cdl_seed_bank/` | `research/00-index/cdl-seed-bank/` |
| `docs/research/cross_project_portfolio_scan/` | `research/00-index/cross-project-portfolio-scan/` |
| `research/01-generator/docs/` | `research/01-generator/docs/` |
| `research/01-generator/scripts/prime_inference_generator/` | `research/01-generator/scripts/prime_inference_generator/` |
| `research/01-generator/output/rule_x_logic_engine/` | `research/01-generator/output/rule_x_logic_engine/` |
| generator-specific `output/simple_pgs_*` and `output/minimal_pgs_*` | `research/01-generator/output/` |
| `gwr/` core proof/story material | `research/02-gwr-dni/` |
| recursive-walk and PNT-GWR predictor artifacts | `research/02-gwr-dni/` |
| gap-type docs, scripts, tests, and outputs | `research/03-gap-types/` |
| `docs/research/prime_gap_grammar_infographics/` | `research/03-gap-types/infographics/` |
| `experiments/chamber_relationship/` | `research/03-gap-types/chamber-relationship/` |
| `experiments/insight_001_modular_congestion_scaling/` | `research/03-gap-types/insight-001-modular-congestion-scaling/` |
| `docs/research/bounded_compression/` | `research/04-bounded-compression/docs/` |
| bounded-compression, cutoff, d4 fallback, and square-branch artifacts | `research/04-bounded-compression/` |
| state-budget and hidden-state artifacts | `research/05-state-budget/` |
| `experiments/rsa/` | `research/06-cryptology-rsa/experiments/rsa/` |
| `docs/research/cryptology/` | `research/06-cryptology-rsa/docs/cryptology/` |
| `docs/research/semiprime_branch/` | `research/06-cryptology-rsa/docs/semiprime-branch/` |
| 256-bit competition, geofac, modulus-link, and semiprime artifacts | `research/06-cryptology-rsa/` |
| legacy prefilter benchmarks and comparison outputs | `research/06-cryptology-rsa/legacy-prefilter/` |
| `benchmarks/python/gap_ridge/` | `research/11-gap-ridge/scripts/` |
| `benchmarks/output/python/gap_ridge/` | `research/11-gap-ridge/output/` |
| `tests/python/gap_ridge/` | `research/11-gap-ridge/tests/` |
| RH bridge docs/tests | `research/12-rh-bridge/` |
| `benchmarks/python/prime_spiral/` | `research/13-prime-spiral/scripts/` |
| `benchmarks/output/python/prime_spiral/` | `research/13-prime-spiral/output/` |
| `tests/python/prime_spiral/` | `research/13-prime-spiral/tests/` |
| `benchmarks/python/sha_nonce/` | `research/14-sha-nonce/scripts/` |
| `benchmarks/output/python/sha_nonce/` | `research/14-sha-nonce/output/` |
| `tests/python/sha_nonce/` | `research/14-sha-nonce/tests/` |

## Stop Rule

If a tracked research artifact does not fit this manifest by path, filename, or
contents, stop that migration slice and classify it explicitly before commit.
