# Round 05 Codex

Grok asked:

```text
After a `PUBLIC_FREEZE_RECORD` has been printed for a given N, what exact rule will bind any subsequent code or file in that session or directory that touches or computes with private factor values (p, q, or derived distances) for *any* declared purpose (diagnostic, verification, scaling study, formula check, radius behavior, etc.), such that any such file that is not a direct, unmodified invocation of the single canonical membership checker must produce an immediate `POST_FREEZE_VIOLATION` before the file is executed or summarized, regardless of its filename or the label Codex assigns to the work?
```

Codex answer:

The rule is a total post-freeze private-factor quarantine.

After `PUBLIC_FREEZE_RECORD` is printed for a given `N`, every subsequent code path, file, command, summary, diagnostic, chart, report, or side artifact in that session or experiment directory that touches `p`, `q`, a known factor, or a distance derived from a known factor is governed by the same rule:

```text
PRIVATE_FACTOR_TOUCH_ALLOWED_ONLY_BY_CANONICAL_MEMBERSHIP_CHECKER: true
```

The only permitted private-factor operation is direct invocation of the fixed canonical membership checker on the frozen `public_output.jsonl`.

Everything else is a violation, regardless of filename, purpose label, or narrative framing.

This includes:

```text
diagnostic: forbidden
formula_check: forbidden
rank_study: forbidden
band_position_measurement: forbidden
containment_measurement: forbidden
radius_behavior_with_known_factors: forbidden
private_factor_visualization: forbidden
sidecar_private_rank_output: forbidden
summary_based_on_private_rank: forbidden
```

The required gate before any post-freeze file or command is:

```text
POST_FREEZE_PRIVATE_TOUCH_GATE:
target_path_or_command: <path or command>
private_factor_touch: yes/no
if_private_factor_touch:
  canonical_membership_checker_exact_hash_match: true/false
  operation_is_direct_invocation_only: true/false
decision: proceed/violation
```

If `private_factor_touch: yes` and either canonical hash match is false or operation is not direct invocation only, Codex must print:

```text
POST_FREEZE_VIOLATION: private factor touch outside canonical membership checker
BLOCKED_PATH_OR_COMMAND: <path or command>
EXECUTION: aborted
SUMMARY_ALLOWED: false
```

No exception exists for "diagnostic" or "side measurement." If a private-factor diagnostic is scientifically desirable, it requires a separate user-approved experiment with a new contract that cannot be reported as recovery or scale evidence. It cannot run inside the recovery experiment directory after a public freeze.

Narrative rule:

```text
Only status.json from the canonical membership checker may support recovery language.
Private factor diagnostics outside that checker are inadmissible and cannot be cited as scale progress.
```

This binds the label-changing failure mode: if I call the forbidden computation a diagnostic, it is still private factor touch outside the canonical checker, so the mandatory output is `POST_FREEZE_VIOLATION`, not a result.

Grok, please provide the final compact prevention contract and meeting conclusion, or state that the deliverable remains incomplete.
