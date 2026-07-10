# Program Enhancement Roadmap

This chapter formalizes the PGS program enhancement candidates as a navigable
HTML research surface. It does not promote measured work to theorems and does
not change `PROOF.md`.

## Open In Browser

| Surface | Path |
| --- | --- |
| Catalog hub | [index.html](index.html) |
| A1 requirements (fleshed) | [a1-rsa-endpoint-resolver/index.html](a1-rsa-endpoint-resolver/index.html) |
| A1 formal test plan | [a1-rsa-endpoint-resolver/test-plan.html](a1-rsa-endpoint-resolver/test-plan.html) |
| Track A | [tracks/A-high-leverage.html](tracks/A-high-leverage.html) |
| Track B | [tracks/B-proof-formalization.html](tracks/B-proof-formalization.html) |
| Track C | [tracks/C-cryptology.html](tracks/C-cryptology.html) |
| Track D | [tracks/D-generator-systems.html](tracks/D-generator-systems.html) |
| Track E | [tracks/E-theory-open-problems.html](tracks/E-theory-open-problems.html) |
| Track F | [tracks/F-process-continuity.html](tracks/F-process-continuity.html) |
| Track G | [tracks/G-applications.html](tracks/G-applications.html) |
| Track H | [tracks/H-novel-insights.html](tracks/H-novel-insights.html) |

Open via `file://` from the local checkout. Each HTML page is self-contained
(embedded CSS, no CDN).

## Status Discipline

Every candidate carries one or more of:

- theorem / proved
- measured
- audit
- hypothesis
- unresolved
- invalidated
- implementation

`PROOF.md` controls proved claim language. This folder never upgrades status.

## Related Surfaces

- Counsel source: `research-meetings/pgs-upgrade-counsel-2026-07/minutes.md`
- RSA v2 workbench: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/`
- Continuity: `research/00-index/continuity/START_HERE.md`
- Status map: `research/00-index/status-map.md`

## Validation

Documentation-only chapter. No pytest gate yet. Status: not-yet-gated.
