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