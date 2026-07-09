# Structured Neighborhood Corpus Schema for Gap Compatibility / PEDK

**Purpose:**  
This schema defines a structured way to record the gap-neighborhood grammar features around the factors (`p` and `q`) and around their product (`N`) for the purpose of discovering the multiplication map at the level of PGS gap grammar.

The corpus is an **analysis and hypothesis-generation tool only**. All `p` and `q` values are used solely for labeling during research and are never part of any public inference rule.

---

## Core Philosophy

- We treat the detailed gap-neighborhood configuration around each factor as a **structured input**.
- We treat observable features of the gap around `N` as **structured outputs**.
- The goal is to discover compatibility and transformation rules between input neighborhood grammars and output neighborhood features under multiplication.

---

## Schema Overview

Each row represents one known triple `(N, p, q)` with rich neighborhood descriptors on both the input (factor) side and output (product) side.

### Top-Level Fields

| Field                        | Type     | Description |
|-----------------------------|----------|-----------|
| `case_id`                   | string   | Unique identifier (e.g., `rsa_v2_50bit_static_001`) |
| `bits`                      | integer  | Bit length of N |
| `N`                         | string   | The public semiprime (as string for large numbers) |
| `p`                         | string   | Known factor (audit-only) |
| `q`                         | string   | Known factor (audit-only) |

### Output Side: Neighborhood Around N

| Field                                      | Type     | Description |
|--------------------------------------------|----------|-----------|
| `gap_N_reduced_state`                      | string   | e.g., `o1_d4_odd\|d<=4` |
| `gap_N_width`                              | integer  | Width of the gap containing N |
| `gap_N_position`                           | integer  | Offset of N from the previous prime |
| `gap_N_relative_position`                  | float    | `position / width` (3 decimal places) |
| `gap_N_position_bucket`                    | string   | `Early`, `Mid`, `Late`, or `Very Late` |
| `gap_N_first_open_offset`                  | integer  | First wheel-open offset after previous prime |
| `gap_N_dcount`                             | integer  | Divisor count of N |

### Input Side: p-Neighborhood (Lower)

| Field                                      | Type     | Description |
|--------------------------------------------|----------|-----------|
| `p_gap_width`                              | integer  | Gap width around p |
| `p_lock_offset`                            | integer  | Lock carrier offset within the gap |
| `p_lock_fraction`                          | float    | `lock_offset / gap_width` |
| `p_carrier_d`                              | integer  | Divisor count of the locked carrier |
| `p_lock_carrier_d`                         | integer  | Divisor count of the locked carrier (same as above, for clarity) |
| `p_reset_signature`                        | string   | Full reset signature (e.g., `carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail`) |
| `p_deadline_source`                        | string   | `tail` or `threat` |
| `p_deadline_margin`                        | integer  | Reset deadline margin |
| `p_tail_length`                            | integer  | Number of entries in tail_after_reset_offsets |
| `p_first_tail_offset`                      | integer  | First entry in the tail (if any) |
| `p_transported_deadline_width`             | integer  | Transported deadline width (if computed) |

### Input Side: q-Neighborhood (Upper)

Same fields as above, prefixed with `q_` instead of `p_`.

### Derived / Cross Features

| Field                                      | Type     | Description |
|--------------------------------------------|----------|-----------|
| `margin_asymmetry`                         | float    | Absolute difference or ratio of transported deadline widths between p-side and q-side |
| `lock_position_asymmetry`                  | float    | Difference in lock fractions between p and q sides |
| `both_d4_tail_based`                       | boolean  | True if both sides are d=4 and deadline=tail |
| `threat_dominance`                         | string   | `none`, `p_only`, `q_only`, `both` |

### Outcome / Label Fields (for analysis only)

| Field                                      | Type     | Description |
|--------------------------------------------|----------|-----------|
| `resolution_status`                        | string   | `correct`, `false_positive`, `difficult`, `unresolved` |
| `gap_N_was_late_d4`                        | boolean  | Whether gap(N) was `o1_d4_odd\|d<=4 + Late/Very Late` |
| `notes`                                    | string   | Free-text observations |

---

## Versioning

- Schema version: `v0.1` (initial rich neighborhood schema)
- This schema is expected to evolve as we identify stronger features.

---

## Usage Notes

- All numerical fields involving large integers should be stored as strings when necessary.
- The corpus is stored as JSON Lines (`.jsonl`) for easy incremental addition.
- `p` and `q` fields exist only for corpus construction and validation. They must never be used in any public PEDK inference path.

---

## File Location

Primary future corpus location:
`research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/design/structured_neighborhood_corpus.jsonl`

Schema definition:
`research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/design/NEIGHBORHOOD_CORPUS_SCHEMA.md` (this document)

The old prototype output is archived under:
`research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/archive/classical-prime-api-scratch/output/structured_neighborhood_corpus.jsonl`
