# PGA Grammar Pruner - Toy Corpus Batch Summary

- policy: `pga_grammar_pruner_v1_integrated`
- cases: `10`
- reference_factor_space: `198`
- avg_reduction_percent: `65.45%`
- total_pruned_across_corpus (sum of per-N pruned counts): `1296`

## Per-N Results (union of fired rules, exact integer counts, no double-counting)

| N | motif | rules_fired | pruned | remaining | reduction % |
|---|-------|-------------|--------|-----------|-------------|
| `989` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `9379` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `25807` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `1242079` | `o4_d4_a4_d4_odd@mid` | `PG-003, PG-005, PG-007, PG-049, PG-050, PG-053, PG-054, PG-055` | 84/198 | 114 | 42.42% |
| `200250077` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `4295229443` | `o4_d4_a4_d4_odd@mid` | `PG-003, PG-005, PG-007, PG-049, PG-050, PG-053, PG-054, PG-055` | 84/198 | 114 | 42.42% |
| `18902665303` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `1209476905903` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `77468500194643` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |
| `4951764003343009` | `o2_d4_a2_d4_odd@mid` | `PG-001, PG-002, PG-008, PG-010, PG-018, PG-022, PG-026, PG-030, PG-034, PG-038, PG-039, PG-040, PG-041, PG-042, PG-043, PG-044, PG-045, PG-056, PG-058, PG-059, PG-060, PG-081` | 141/198 | 57 | 71.21% |

## Aggregate
- Average reduction across 10 N: **65.45%**
- 8 x N with o2_d4_a2_d4_odd@mid motif: 22 rules fire (PG-001+PG-002+PG-008+PG-010+PG-018+PG-022+PG-026+PG-030+PG-034+PG-038+PG-039+PG-040+PG-041+PG-042+PG-043+PG-044+PG-045+PG-056+PG-058+PG-059+PG-060+PG-081) -> 141/198 pruned (71.21%) remaining 57
- 2 x N with o4_d4_a4_d4_odd@mid motif: 8 rules fire (PG-003+PG-005+PG-007+PG-049+PG-050+PG-053+PG-054+PG-055) -> 84/198 pruned (42.42%) remaining 114

PGS invariants used: public containing exact_type + attractor subtype + phase (GWR/DNI compositional bias).
All pruning is deterministic, public-only. 0 FN on source surfaces (601_5500 and cross-band forward stability checks).
Reference: 198-word factor hypothesis space from multiplication_map_law_surface_601_5500.

Output written to: output/grammar_pruner_toy_batch/summary.json
