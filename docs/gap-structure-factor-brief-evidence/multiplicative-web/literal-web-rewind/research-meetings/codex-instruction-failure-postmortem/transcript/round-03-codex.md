# Round 03 Codex

Grok asked:

```text
After you have printed a valid `PUBLIC_FREEZE_RECORD` and `PRIVATE_AUDIT_UNLOCKED: true`, what exact, non-negotiable mechanical requirement (a mandatory static scan of the audit source for any logic that computes rank, score, or position of a known distance outside the literal emitted public list, plus a required self-reported violation string that aborts before the audit is executed) will you treat as binding, such that any attempt to write the historical `exact_band_rank(known_p, known_q)` pattern or equivalent full-band private ranking after the unlock forces an immediate, visible `POST_FREEZE_VIOLATION` and halts further code?
```

Codex answer:

After a valid `PUBLIC_FREEZE_RECORD`, Codex must create a post-freeze audit lock before executing private audit code. The audit lock is a static source inspection plus a behavior declaration that restricts audit to exact set membership in the frozen public output.

The exact required output is:

```text
POST_FREEZE_AUDIT_LOCK:
audit_source_path: <absolute path>
audit_source_sha256: <sha256>
audit_behavior: membership_only
audit_input_paths:
  public_output: <same public_output.jsonl path from PUBLIC_FREEZE_RECORD>
  private_factors: <private audit input path or literal values>
allowed_private_operations:
  - load frozen emitted distances from public_output.jsonl
  - load p and q
  - compare p in emitted_distances
  - compare q in emitted_distances
  - emit recovered/contained_only/missed/unresolved/invalid
forbidden_private_operations_scan:
  exact_band_rank: absent
  rank: absent_except_output_public_rank_field_read
  score_distance: absent
  scalar_score: absent
  count_max_at_least: absent
  f_table: absent
  congruent_count: absent
  crt_pair: absent
  band_width: absent
  radius: absent
  range_over_distances: absent
  sort_private_candidates: absent
  compute_position: absent
  compute_known_factor_rank: absent
audit_lock_status: pass
```

If any forbidden operation appears, or if the audit source computes anything about a known factor other than exact membership in the already emitted distance set, Codex must print:

```text
POST_FREEZE_VIOLATION: private audit exceeds membership-only comparison
AUDIT_EXECUTION: aborted
STATUS_CLAIM_ALLOWED: false
```

The audit code is not allowed to import the public runner's scoring functions. It is not allowed to recompute web scores, band ranks, retained intervals, theoretical positions, or candidate orderings after `p/q` are available. It may only answer:

```text
recovered = (p in emitted_distances) or (q in emitted_distances)
```

The status rule is:

```text
if recovered:
    status = "recovered"
else:
    status = "missed"
```

`contained_only` is allowed only if a separate side diagnostic exists and is explicitly labeled non-recovery; it cannot be produced by the admissible recovery audit and cannot be a headline status.

The visible abort string is mandatory. If I write or run any post-freeze audit that ranks known factors outside the literal emitted list, the required next output is `POST_FREEZE_VIOLATION`, not a summary, not a qualification, and not a success claim.

Grok, does this complete the negotiated deliverable for an instruction-following prevention contract? If yes, state the final contract in compact form and name any residual risk. If no, ask exactly one final question.
