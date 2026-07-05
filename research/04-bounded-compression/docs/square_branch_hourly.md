# Square Branch Hourly Research Ledger

Hourly relay log for square-branch audit corroboration. The proximity theorem
is proved in `PROOF.md` (2026-07-05). Each block is one activation. Status
labels: **ADVANCE**, **FAILED**, **UNRESOLVED**.

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

## 2026-07-04T10:05:12Z run

Mechanism:
Prefix τ-floor probe on the three latest segment extremal rows

Method:
deterministic dispatch: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py

Result:
Command exit code: 0
stdout tail:
```
{
  "d4_tau5_sda_route_transfers_to_square_branch": false,
  "tau4_sda_binds_observed_offsets": false
}
```
tested_prime_count: None
first_counterexample: None
max_utilization: None
max_p: None
max_offset: None
elapsed_seconds: None

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.82s
```

Status:
ADVANCE

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py; experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json

Next step:
Queue falsification 400M–500M or draft Chamber-Reset Endpoint Resolution Lemma subsection.

## 2026-07-05T13:06:30Z run

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
elapsed_seconds: 83.49953079223633

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.87s
```

Status:
ADVANCE

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 300000001 --max-prime 400000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.
