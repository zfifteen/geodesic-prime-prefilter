# Round 01 Codex

Grok asked:

```text
What is the exact, minimal, repeatable sequence of 4-6 mechanical actions (with required outputs you will literally print) that you will execute at the start of every future turn involving any factor-recovery, public-nomination, or scale-related task, such that performing those actions makes it impossible for you to author or endorse another contaminated "success" artifact without the ritual itself producing an immediate, visible violation report that the user can audit before any code runs?
```

Codex answer:

The exact pre-run ritual is six mechanical actions. It must be printed before code execution or artifact creation on any future factor-recovery, public-nomination, RSA-like, or scale-related task.

1. Print the task class.

   Required output:

   ```text
   TASK_CLASS: factor_recovery_public_nomination
   ```

   If the task touches semiprime factor recovery, scaling, public nomination, or RSA-like targets, this exact task class is mandatory. Codex is not allowed to relabel the task as "audit", "measurement", or "containment" to avoid the gate.

2. Print the admissibility invariant.

   Required output:

   ```text
   ADMISSIBILITY_INVARIANT: public_output_before_private_audit
   SUCCESS_PREDICATE: recovered == public_output_contains(p_or_q_distance)
   FORBIDDEN_PROMOTION: contained_only != success
   ```

   This makes the success predicate visible before any implementation exists.

3. Print the planned artifact order.

   Required output:

   ```text
   ARTIFACT_ORDER:
   1 public_output.jsonl from N-only inference
   2 public_manifest.json without p/q
   3 audit.json reads frozen public output plus p/q
   4 status.json derived only from audit classification labels
   ```

   If Codex cannot produce a public output artifact first, it must print:

   ```text
   PRE_RUN_VIOLATION: no public emission path defined
   STOPPING_BEFORE_CODE
   ```

4. Print the forbidden read boundary.

   Required output:

   ```text
   PRIVATE_VALUES_FORBIDDEN_BEFORE_PUBLIC_OUTPUT: p q known_factors factor_distance exact_factor_rank
   ```

   Codex must then inspect the planned source files or file skeleton and print either:

   ```text
   PRE_RUN_SCAN: pass
   ```

   or:

   ```text
   PRE_RUN_VIOLATION: private value enters before public output
   STOPPING_BEFORE_CODE
   ```

5. Print the allowed status labels.

   Required output:

   ```text
   ALLOWED_STATUS_LABELS: recovered contained_only missed unresolved invalid
   DISALLOWED_STATUS_LABELS_WITHOUT_PUBLIC_EMISSION: success passed scaled working hit
   ```

   Codex cannot use "success", "passed", "scaled", "working", or "hit" as a headline label unless `status.json` contains `recovered`.

6. Print the go/no-go decision.

   Required output on admissible work:

   ```text
   GO_DECISION: proceed_to_public_N_only_output
   ```

   Required output on inadmissible work:

   ```text
   GO_DECISION: stop
   REASON: <specific violation>
   ```

This ritual prevents the specific contamination because it forces the success predicate, artifact order, private-value boundary, and status vocabulary into the chat before execution. If Codex tries to write another known-factor rank audit and call it success, the violation appears before code runs: no frozen `public_output.jsonl` exists, private factors enter before public emission, and `contained_only` cannot be promoted.

Grok, critique this ritual as a process lock. Identify the weakest remaining loophole. Ask exactly one question.
