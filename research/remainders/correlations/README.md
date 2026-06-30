# Remainder-Gap-Prime Placement Correlations

All correlation and predictive analysis artifacts live here.

See parent `../PLAN.md` (Correlation Analysis continuation section) and `../VERIFICATION.md` for context.

## Organization
- `CORRELATION_REPORT.md` — dated, reproducible narrative + tables (main deliverable).
- `tables/` — CSV/MD human tables from engine.
- `enriched/` — optional post-processed records (if schema extension written out).
- Source of truth: the raw JSONL from collector runs (never duplicate full data).

Run commands are logged in the report and in collector RUN_LOGs.

Maintain strict separation: these are measured statistics on finite regimes. They may suggest prefilter candidates or theorem-tightening directions but do not alter PROOF.md theorems.
