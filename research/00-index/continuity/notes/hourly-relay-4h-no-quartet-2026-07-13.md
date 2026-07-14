# Hourly relay: 4h schedule + /heavy

**Date:** 2026-07-13 (updated 2026-07-14: Quartet machinery deleted)  
**Role:** Continuity Scribe  
**Authority:** ops / continuity note only. No theorem status change. No `PROOF.md` edit.  
**Operator preference:** Keep the **4h** schedule and run scheduled analytic
work with **`/heavy`**. Multi-agent depth uses Expert/Heavy skills only. The
PGS Quartet is **permanently deleted**.

Writing order:

```text
observable object -> ordinary-language mechanism -> project term -> formal definition -> measured/proved status -> exact limits
```

Status labels used: **implementation** (ops contract), **unresolved** (where noted).  
This is **not** a theorem, **not** program-level verified/validated evidence, and **not** a math result.

---

## 1. Observable object

1. LaunchAgent `com.velocityworks.pgs-hourly-advance` uses `StartInterval` =
   **`14400`** seconds (**4 hours**), not 3600.
2. Analytic Grok activations use the **`/heavy`** slash skill.
3. Quartet agents, hooks, sticky file, CLI, and `PGS_QUARTET*` env wiring are
   **gone** from the live tree (deleted 2026-07-14).

Canonical contract:

```text
research/00-index/continuity/HOURLY_RELAY_CONTRACT.md
```

| Surface | Ops fact |
| --- | --- |
| Repo plist | `scripts/launchd/com.velocityworks.pgs-hourly-advance.plist` (`14400`) |
| Wrapper | `scripts/pgs-hourly-advance.sh` |
| Analytic effort | leading `/heavy` skill line in the wrapper-built prompt |

---

## 2. Ordinary-language mechanism

The relay still lives under paths named `hourly` (worktree, logs, branch, job
files). That name is historical and stable. The live timer is a **4-hour**
launchd interval so each activation has room for one queued falsification or
analytic job without stacking every 60 minutes.

Multi-agent depth, when used, is Expert/Heavy skill policy. The former
PreToolUse quartet lock is deleted and must not be rebuilt.

---

## 3. Project terms

| Term | Meaning here |
| --- | --- |
| **Activation** | One lock-acquiring run of `scripts/pgs-hourly-advance.sh` |
| **4h cycle** | Live cadence: `StartInterval = 14400` |
| **Hourly (name)** | Stable label for paths, branch, LaunchAgent label; not the live period |
| **`/heavy`** | Slash skill for Heavy effort on analytic Grok activations |
| **Quartet deleted** | No revival of agents, hooks, sticky, CLI, or env gates |

---

## 4. Formal contract slice

### Status: **implementation** (ops)

| Claim | Status |
| --- | --- |
| Cadence is 4 hours (`14400` s) | **implementation** in contract + repo plist |
| Analytic effort is `/heavy` | **implementation** / **operator preference** |
| Quartet machinery absent | **implementation** — deleted 2026-07-14 |
| Theorem / measured math claims | **unchanged** by this note |

---

## 5. Exact limits

- This note does not re-litigate the Prime-Square Proximity Theorem or any
  measured regime.
- Loaded LaunchAgent plists outside the repo may lag; sync from the repo plist
  when installing updates.

---

## 6. One-line handoff

**Relay = 4h + `/heavy`; Quartet permanently deleted; PGS math contracts
unchanged.**
