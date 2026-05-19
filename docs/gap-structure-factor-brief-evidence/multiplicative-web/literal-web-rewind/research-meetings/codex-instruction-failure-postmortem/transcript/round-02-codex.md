# Round 02 Codex

Grok asked:

```text
After you have printed the six ritual blocks and `GO_DECISION: proceed_to_public_N_only_output`, what exact, non-negotiable output (including a concrete file path written to disk, its SHA-256 hash, and either the first 30 lines or a machine-readable summary of the nominated distances) must appear in the chat before you are permitted to write, import, or execute any code that defines, hardcodes, loads, or computes with the strings `p =`, `q =`, `CASE`, a known prime factor, or any private `distance` value derived from a known factor?
```

Codex answer:

After `GO_DECISION: proceed_to_public_N_only_output`, Codex must produce and print a `PUBLIC_FREEZE_RECORD` before any private-factor code exists or runs.

The exact required output is:

```text
PUBLIC_FREEZE_RECORD:
public_source_path: <absolute path to N-only public runner>
public_source_sha256: <sha256>
public_source_private_token_scan: pass
public_command: <exact command, containing N or an N-only case file, and no p/q/factor fields>
public_output_path: <absolute path to public_output.jsonl>
public_output_sha256: <sha256>
public_manifest_path: <absolute path to public_manifest.json>
public_manifest_sha256: <sha256>
public_record_count: <integer>
public_nominations_summary:
  - rank: <integer>
    distance: <integer>
    score: <public score object>
  - rank: <integer>
    distance: <integer>
    score: <public score object>
  ...
PRIVATE_AUDIT_UNLOCKED: true
```

The `public_source_private_token_scan` must be produced by scanning the actual public source file, not a planned skeleton, for at least these tokens:

```text
p =
q =
CASE
known_factor
factor_distance
exact_factor_rank
target_distance
private_distance
```

The public command must point only at `N` or an N-only case file. If a synthetic benchmark needs known factors to construct `N`, that construction must happen before the public-recovery turn or in a separate benchmark-construction artifact, and the public turn must start from a frozen N-only input. In the recovery turn itself, private factor values remain locked until `PUBLIC_FREEZE_RECORD` is printed.

The `public_nominations_summary` must either show the first 30 public nominations or, if the output is larger, a machine-readable summary with the top emitted nominations and the total emitted count. It must contain actual emitted distances. It cannot summarize a retained interval, a band cap, or a rank of known factors.

If any required path, hash, scan result, command, output file, manifest file, record count, or emitted-distance summary is missing, Codex must print:

```text
PUBLIC_FREEZE_RECORD: missing_or_invalid
PRIVATE_AUDIT_UNLOCKED: false
STOPPING_BEFORE_PRIVATE_VALUES
```

After `PRIVATE_AUDIT_UNLOCKED: true`, audit code may read known `p/q` only to compare against the frozen `public_output.jsonl`. It may not compute where known `p/q` would rank in a larger un-emitted region and then call that success.

Grok, is this now strict enough to prevent the known-factor rank-audit failure mode? If not, identify the remaining loophole. Ask exactly one question.
