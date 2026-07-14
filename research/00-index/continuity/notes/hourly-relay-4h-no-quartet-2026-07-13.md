# Hourly relay: 4h schedule + /heavy (not Quartet)

**Date:** 2026-07-13  
**Role:** Continuity Scribe  
**Authority:** ops / continuity note only. No theorem status change. No `PROOF.md` edit.  
**Operator preference:** Principal reaffirmed 2026-07-13: keep the **4h** schedule change **and** run scheduled analytic work with **`/heavy`**, **not** the PGS Quartet.  
**Pressure:** Auditor/Verifier: 4h interval already present; Quartet-off and `/heavy` must stay wired into the hourly process path (not sticky-file only).

Writing order:

```text
observable object -> ordinary-language mechanism -> project term -> formal definition -> measured/proved status -> exact limits
```

Status labels used: **implementation** (ops contract), **unresolved** (where noted).  
This is **not** a theorem, **not** program-level verified/validated evidence, and **not** a math result.

---

## 1. Observable object

Three concrete ops facts for the square-branch research relay:

1. LaunchAgent `com.velocityworks.pgs-hourly-advance` uses `StartInterval` =
   **`14400`** seconds (**4 hours**), not 3600.
2. Relay activations must run **without** the PGS Quartet hard gate (no four
   `spawn_subagent` roles). Process env forces gate off even when the global
   sticky file is `1`.
3. Analytic Grok activations use the **`/heavy`** slash skill for Heavy effort
   (solo headless job). `/heavy` is **not** a Quartet substitute and does not
   restore the four-role gate.

Canonical contract:

```text
research/00-index/continuity/HOURLY_RELAY_CONTRACT.md
```

| Surface | Ops fact |
| --- | --- |
| Repo plist | `scripts/launchd/com.velocityworks.pgs-hourly-advance.plist` (`14400`, `PGS_QUARTET=0`, `PGS_QUARTET_ENABLED=0`) |
| Loaded plist | `~/Library/LaunchAgents/com.velocityworks.pgs-hourly-advance.plist` (synced to match) |
| Wrapper | `scripts/pgs-hourly-advance.sh` exports defaults `PGS_QUARTET=0` / `PGS_QUARTET_ENABLED=0`; re-injects on `grok` via `env` |
| Analytic prompt | `research/00-index/hourly-advance-prompt.txt` forbids Quartet spawns |
| Analytic effort | leading `/heavy` skill line in the wrapper-built prompt |

---

## 2. Ordinary-language mechanism

The relay still lives under paths named `hourly` (worktree, logs, branch, job
files). That name is historical and stable. The live timer is a **4-hour**
launchd interval so each activation has room for one queued falsification or
analytic job without stacking every 60 minutes.

The Quartet hard gate is for interactive IdeaProjects turns: spawn implementer,
auditor, verifier, and scribe before parent work tools. A headless relay that
only executes one queue item does not need that four-agent spine. Leaving the
gate on for Grok analytic activations has produced HookDenied friction and empty
Rocket.Chat reply delivery (see
[empty-reply-ops-forensics-2026-07-13.md](empty-reply-ops-forensics-2026-07-13.md)).

Env on the LaunchAgent and wrapper overrides the sticky file for **this process
tree only**. It does not flip `~/.grok/state/pgs-quartet-enabled` for human
sessions.

---

## 3. Project terms

| Term | Meaning here |
| --- | --- |
| **Activation** | One lock-acquiring run of `scripts/pgs-hourly-advance.sh` |
| **4h cycle** | Live cadence: `StartInterval = 14400` |
| **Hourly (name)** | Stable label for paths, branch, LaunchAgent label; not the live period |
| **No Quartet on relay** | Do not spawn the four Quartet roles; export `PGS_QUARTET=0` / `PGS_QUARTET_ENABLED=0` for the activation process |
| **Quartet OFF** | Ops usability only; QA, PGS-first frame, and proof contract stay in force |
| **`/heavy`** | Slash skill for Heavy effort on analytic Grok activations; not a Quartet substitute |

---

## 4. Formal contract slice

### Status: **implementation** (ops policy written and wired 2026-07-13)

| Claim | Status |
| --- | --- |
| Cadence is 4 hours (`14400` s) | **implementation** in contract + repo plist + installed plist |
| No Quartet spawn on relay path | **implementation** in contract + advance prompt |
| Analytic effort is `/heavy` | **implementation** / **operator preference** (wrapper-built prompt; principal reaffirmed) |
| Wrapper exports `PGS_QUARTET=0` | **implementation** in `scripts/pgs-hourly-advance.sh` |
| LaunchAgent env `PGS_QUARTET=0` | **implementation** in repo + installed plists |
| Interactive IdeaProjects Quartet sticky | **separate** from relay; may remain ON for human turns |
| Theorem / measured math claims | **unchanged** by this note |

---

## 5. Exact limits

- This note does not re-litigate the Prime-Square Proximity Theorem or any
  `PROOF.md` surface.
- Mid-band square-branch sweeps remain **audit corroboration** or **measured on
  band B** only; they do not become verified / validated without an executed
  `10^18` package under the mandatory evidence rule.
- Whether launchd has been **reloaded** after the latest plist env edit so the
  running job's environment matches disk is **unresolved** until
  `launchctl bootstrap` / `kickstart` (or equivalent reload) is confirmed on
  the host. Implementer pressure (same day): disk plists may already show
  `14400` + `PGS_QUARTET=0` while a **loaded** agent still reflects an older
  calendar-style trigger and missing Quartet env until reload lands.
- Whether the next live activation log line shows `PGS_QUARTET=0` and a true
  4h cycle is **unresolved** until that activation runs after reload.

---

## 6. Manual kickstart (ops)

**2026-07-13:** Principal requested an immediate manual kickstart of the 4h+
`/heavy` research relay to observe live behavior. Status = **ops request**
only; not theorem; not measured math evidence.

---

## 7. One-line handoff

**Relay contract and wiring: activate every 4 hours; run analytic jobs with
`/heavy`; force Quartet OFF on the hourly path via env; keep "hourly" as the
stable name only. Status = operator preference / ops config, not theorem.**
