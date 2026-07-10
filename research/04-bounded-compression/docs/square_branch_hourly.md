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

## 2026-06-19T08:46:09Z run

Mechanism:
Square-branch dynamic-cutoff falsification sweep on prime roots 300M–400M

Method:
deterministic dispatch: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 300000001 --max-prime 400000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8

Result:
Command exit code: 0
stdout tail:
```
square-branch-dynamic-cutoff-search: primes=5084001 first_counterexample=none max_utilization=0.7036082474226805 max_p=358018553
```
tested_prime_count: 5084001
first_counterexample: None
max_utilization: 0.7036082474226805
max_p: 358018553
max_offset: 546
elapsed_seconds: 83.1661810874939

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.71s
```

Status:
ADVANCE

Artifacts:
python3; research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py; --min-prime; 300000001; --max-prime; 400000000; --output-dir; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.

## 2026-06-19T09:05:51Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation on the `3e8-4e8` utilization maximum.

Method:
Read `square_branch_dynamic_cutoff_search_3e8_4e8/square_branch_dynamic_cutoff_search_summary.json`
and `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`.
Ran `experiments/square-branch-hourly-2026-06-19/offset_540_chamber_geometry_probe.py`
to evaluate six falsifiable predictions (P1–P6) on prior and new extremal rows.
No d=4 SDA port.

Result:
New extremal `r=358018553`, offset `546`, utilization `0.7036082474226805`.
All six predictions hold on the new row: `prefix_min_tau=4`, `first_tau4_offset=4`,
`first_tau3_offset=546`, `tau4_count=64`, `tau5_count=0`, offset in `[528,552]`.
Prior rows: offsets `540`, `462`, `540` — chamber separation 3/3.

Theorem: square-branch proximity obligation remains **unresolved** (`PROOF.md`).
Invalidated: d=4 SDA transfer (not revived).
Measured: P1–P6 hold 4/4 extremal rows tested.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.75s
```

Status:
ADVANCE

Artifacts:
`experiments/square-branch-hourly-2026-06-19/offset_540_chamber_geometry_probe.py`;
`experiments/square-branch-hourly-2026-06-19/offset_540_prediction_table.json`;
`experiments/square-branch-hourly-2026-06-19/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows or queue next falsification segment.

## 2026-07-10T10:11:43Z run

Mechanism:
Square-branch dynamic-cutoff falsification sweep on prime roots 400M-500M

Method:
deterministic dispatch: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001 --max-prime 500000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8

Result:
Command exit code: 0
stdout tail:
```
square-branch-dynamic-cutoff-search: primes=5019541 first_counterexample=none max_utilization=0.9341772151898734 max_p=424171123
```
tested_prime_count: 5019541
first_counterexample: None
max_utilization: 0.9341772151898734
max_p: 424171123
max_offset: 738
elapsed_seconds: 84.23241710662842

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.74s
```

Delta classification: new falsification regime through max_prime=500000000

Research status:
ADVANCE

Ops status:
OK

Delta:
new falsification regime through max_prime=500000000

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001 --max-prime 500000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.
