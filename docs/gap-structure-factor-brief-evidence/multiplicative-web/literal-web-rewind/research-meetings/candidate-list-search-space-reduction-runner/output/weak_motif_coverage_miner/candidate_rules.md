# Focused Weak-Motif Coverage Miner

- status: `measured_candidate_rule_mining`
- stage: `stage_one_public_grammar_pruning`
- promoted rules: `5`

## Promotion Policy

- train bands: `27001_30000, 32001_34000`
- heldout bands: `34001_35000`
- selected zero-observed classes per promoted rule: `30`
- minimum zero-observed classes for promotion: `20`
- broad high-a rules allowed: `False`

## Candidate Rows

| motif | train rows | heldout rows | selected zero classes | contradictions | pruned_count | status | rule |
|-------|------------|--------------|-----------------------|----------------|--------------|--------|------|
| `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | 812 | 52 | 30 | 0 | 30 | promoted | PG-085 |
| `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | 61 | 4 | 30 | 0 | 30 | promoted | PG-086 |
| `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | 407 | 27 | 30 | 0 | 30 | promoted | PG-087 |
| `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | 104 | 7 | 30 | 0 | 30 | promoted | PG-088 |
| `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | 432 | 31 | 30 | 0 | 30 | promoted | PG-089 |

## Promoted Rules

- `PG-085` `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` -> 30/198 pruned
- `PG-086` `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` -> 30/198 pruned
- `PG-087` `o2_d4_a2_d4_odd@late + o4_d4_odd prev` -> 30/198 pruned
- `PG-088` `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` -> 30/198 pruned
- `PG-089` `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` -> 30/198 pruned

No p, q, divisibility, product closure, or recovery logic is used by this miner.
