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
| `research/03-gap-types/infographics/prime-gap-grammar-infographics/` | `research/03-gap-types/infographics/` |
| `research/03-gap-types/experiments/chamber-relationship/` | `research/03-gap-types/chamber-relationship/` |
| `research/03-gap-types/experiments/insight-001-modular-congestion-scaling/` | `research/03-gap-types/insight-001-modular-congestion-scaling/` |
| `research/04-bounded-compression/docs/` | `research/04-bounded-compression/docs/` |
| bounded-compression, cutoff, d4 fallback, and square-branch artifacts | `research/04-bounded-compression/` |
| state-budget and hidden-state artifacts | `research/05-state-budget/` |
| `experiments/rsa/` | `research/06-cryptology-rsa/experiments/rsa/` |
| `docs/research/cryptology/` | `research/06-cryptology-rsa/docs/cryptology/` |
| `docs/research/semiprime_branch/` | `research/06-cryptology-rsa/docs/semiprime-branch/` |
| 256-bit competition, geofac, modulus-link, and semiprime artifacts | `research/06-cryptology-rsa/` |
| legacy prefilter benchmarks and comparison outputs | `research/06-cryptology-rsa/legacy-prefilter/` |
| `research/11-gap-ridge/scripts/` | `research/11-gap-ridge/scripts/` |
| `research/11-gap-ridge/output/` | `research/11-gap-ridge/output/` |
| `research/11-gap-ridge/tests/` | `research/11-gap-ridge/tests/` |
| RH bridge docs/tests | `research/12-rh-bridge/` |
| `research/13-prime-spiral/scripts/` | `research/13-prime-spiral/scripts/` |
| `research/13-prime-spiral/output/` | `research/13-prime-spiral/output/` |
| `research/13-prime-spiral/tests/` | `research/13-prime-spiral/tests/` |
| `research/14-sha-nonce/scripts/` | `research/14-sha-nonce/scripts/` |
| `research/14-sha-nonce/output/` | `research/14-sha-nonce/output/` |
| `research/14-sha-nonce/tests/` | `research/14-sha-nonce/tests/` |

## Stop Rule

If a tracked research artifact does not fit this manifest by path, filename, or
contents, stop that migration slice and classify it explicitly before commit.
