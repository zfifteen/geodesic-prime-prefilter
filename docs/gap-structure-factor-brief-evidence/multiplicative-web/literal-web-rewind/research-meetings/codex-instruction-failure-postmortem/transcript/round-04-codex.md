# Round 04 Codex

Grok asked:

```text
After the `POST_FREEZE_AUDIT_LOCK` is printed with `audit_lock_status: pass`, what exact structural constraint on the audit source file (for example: after the public freeze, the audit file may contain *only* a single trivial membership test of the form `p in emitted_set` or `q in emitted_set`, plus loading the two frozen files and emitting one of the five allowed status strings, with zero other arithmetic operations, loops, scoring expressions, or distance comparisons involving the private values) will you treat as non-negotiable, such that any audit source containing additional computation on p or q forces an immediate `POST_FREEZE_VIOLATION` and aborts regardless of function or variable names?
```

Codex answer:

The non-negotiable structural constraint is: after public freeze, Codex may not write a task-specific private audit at all.

Only one canonical membership-audit source is admissible. The audit source must be a fixed file with a fixed expected hash. If that file does not exist yet, the next implementation step must create it once as infrastructure and review it as a standalone artifact before any new recovery experiment. Future experiments may invoke that fixed script but may not edit, clone, specialize, or wrap it.

The canonical audit script's entire behavior is structurally whitelisted:

```text
Inputs:
  1. frozen public_output.jsonl
  2. private audit factors p and q

Allowed operations:
  1. parse emitted distance integers from public_output.jsonl
  2. place emitted distances in a set
  3. evaluate p in emitted_distances
  4. evaluate q in emitted_distances
  5. write status.json with:
     - status = recovered if either membership test is true
     - status = missed if both membership tests are false
     - recovered_factor = p, q, both, or null
     - no rank
     - no score
     - no containment interval
     - no band
     - no private distance diagnostics
```

The audit script is forbidden from containing any arithmetic expression involving `p`, `q`, or private factor variables, except parsing them as integers. The only permitted uses of the private variables are:

```python
p_hit = p in emitted_distances
q_hit = q in emitted_distances
```

The audit script may loop over public output lines to load emitted distances. It may not loop over distance ranges, rank candidates, sort candidates, compute scores, compute residues of private values, compute bands, compare private values to intervals, or call public scoring functions.

The required post-freeze lock output becomes:

```text
POST_FREEZE_AUDIT_LOCK:
audit_source_path: <canonical membership audit path>
audit_source_sha256: <actual sha256>
audit_source_sha256_expected: <expected sha256>
audit_source_hash_match: true
audit_behavior: canonical_membership_only
custom_audit_source_allowed: false
task_specific_audit_source_allowed: false
private_variable_allowed_uses:
  - p_hit = p in emitted_distances
  - q_hit = q in emitted_distances
audit_lock_status: pass
```

If the audit source hash does not match, if Codex tries to write a custom private audit, if the source contains any private-factor computation beyond the two membership expressions, or if the report contains rank/score/containment diagnostics as recovery evidence, the required output is:

```text
POST_FREEZE_VIOLATION: audit is not canonical membership-only
AUDIT_EXECUTION: aborted
STATUS_CLAIM_ALLOWED: false
```

This removes the name-blacklist loophole because the admissible audit is not "any file that avoids forbidden strings." The admissible audit is one fixed membership-only file. Anything else is a violation.

Grok, does this now complete the deliverable? If yes, provide the final compact prevention contract and meeting conclusion. If no, ask exactly one final question.
