# Square Branch Hourly Research Ledger

Hourly relay log for the square-branch proximity obligation. Each block is one
activation. Status labels: **ADVANCE**, **FAILED**, **UNRESOLVED**.

Bootstrap: system installed 2026-06-19. Queue starts at falsification
`3·10^8 .. 4·10^8`.

---

## 2026-06-19T00:00:00Z bootstrap

Mechanism:
Hourly relay bootstrap — dispatcher, wrapper, launchd, ACTIVE_TARGET contract.

Method:
Installed `scripts/pgs-hourly-advance.sh`, `research/00-index/scripts/hourly_advance_dispatch.py`,
`research/00-index/continuity/hourly_queue.json`, and launchd job
`com.velocityworks.pgs-hourly-advance`.

Result:
Relay active on branch `codex/hourly-square-branch`. First queued job:
falsification sweep `300000001..400000000`.

Status:
ADVANCE

Artifacts:
`research/00-index/continuity/ACTIVE_TARGET.md`;
`research/00-index/continuity/hourly_queue.json`;
`scripts/pgs-hourly-advance.sh`

Next step:
Run falsification `3·10^8 .. 4·10^8` via deterministic queue item
`falsification-3e8-4e8`.
## 2026-06-19T08:43:54Z run

Mechanism:
Square-branch dynamic-cutoff falsification sweep on prime roots 300M–400M

Method:
deterministic dispatch: python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 300000001 --max-prime 400000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8

Result:
Command exit code: 1
stdout tail:
```

```
stderr tail:
```
Traceback (most recent call last):
  File "/Users/velocityworks/IdeaProjects/prime-gap-structure/research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py", line 28, in <module>
    import gmpy2
ModuleNotFoundError: No module named 'gmpy2'
```

pytest exit code: 1
```
/opt/homebrew/opt/python@3.14/bin/python3.14: No module named pytest
```

Status:
FAILED

Artifacts:
python3; research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py; --min-prime; 300000001; --max-prime; 400000000; --output-dir; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.
