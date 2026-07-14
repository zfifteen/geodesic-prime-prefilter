# PGS Quartet retired; Expert / Heavy replace multi-agent depth

**Date:** 2026-07-13  
**Authority:** ops / continuity note only. No theorem status change. No `PROOF.md` edit.  
**Principal:** After implementing **Expert** and **Heavy** effort skills, the PGS
Quartet is no longer needed.

Writing order:

```text
observable object -> ordinary-language mechanism -> project term -> formal definition -> measured/proved status -> exact limits
```

Status labels used: **implementation** (ops contract).  
This is **not** a theorem and **not** program-level verified math evidence.

---

## 1. Observable object

| Surface | Change |
| --- | --- |
| Sticky | `~/.grok/state/pgs-quartet-enabled` = `0` (OFF) |
| Global hook | `~/.grok/hooks/pgs-quartet-gate.json` → `*.retired-2026-07-13` (not loaded) |
| Global agents | `~/.grok/agents/pgs-*.md` → `~/.grok/agents/_retired/pgs-quartet-2026-07-13/` |
| Repo agents | `.grok/agents/pgs-*.md` → `.grok/agents/_retired/pgs-quartet-2026-07-13/` |
| `AGENTS.md` | Quartet hard-rule section replaced by Expert/Heavy slash skills |
| `AGENTS-WEB.md` | Same |
| Rules / hooks README | Marked **RETIRED** |
| Hourly relay | Still **4h** + **`/heavy`**; Quartet language updated to global retirement |

---

## 2. Ordinary-language mechanism

The Quartet was a machine PreToolUse lock: parent tools denied until four named
roles spawned each turn. Expert and Heavy are **skill policies** (slash-invoked
fixed teams of 4 or 12 analytic local subagents, then leader synthesis). They
cover multi-agent depth without a four-role hard gate or dedicated `pgs-*`
agent types.

---

## 3. Project terms

| Term | Meaning here |
| --- | --- |
| **Quartet retired** | No spawn lock; agents archived; do not re-enable without principal request |
| **`/expert`** | Fixed 4 local specialists |
| **`/heavy`** | Fixed 12 local specialists (≥1 contrarian) |
| **`/normal`** | Clear Expert/Heavy overlays |

---

## 4. Formal contract slice

### Status: **implementation** (ops, 2026-07-13)

| Claim | Status |
| --- | --- |
| Quartet hard gate not required | **implementation** in AGENTS.md |
| Expert/Heavy are multi-agent path | **implementation** in `~/.grok/skills/{expert,heavy,normal}/` |
| Sticky OFF + hook not loaded | **implementation** under `~/.grok/` |
| PGS research rules / QA / proof contract unchanged | **unchanged** |
| Theorem / measured math claims | **unchanged** by this note |

---

## 5. Exact limits

- Does not change `PROOF.md` or any measured regime.
- Historical experiment notes may still mention "Quartet pressure"; that is
  ledger archaeology, not a live spawn requirement.
- Hook Python tests may still pass offline; they are not a live gate.

---

## 6. One-line handoff

**PGS Quartet retired; multi-agent depth = `/expert` or `/heavy`; QA and
PGS-first contracts stay. Ops only, not theorem.**
