# Quartet consensus: left-endpoint parity modular bias insight

Status labels only. Not a theorem. Max measured left prime `5e7`. No `10^18`. No verified/validated language.

## Insight under attack

User-supplied "core insight": left-endpoint parity creates a systematic modular bias under min-`tau` gap-reading, with even leftmost witnesses driving higher `z >= 4` mismatch rates, and rightmost selection cleaner among ties.

## Verdict (orchestrator merge)

```text
CORE INSIGHT AS WRITTEN: REJECTED / WEAKENED
```

Not a clean full falsification of every residual sentence. The causal packaging ("systematic modular bias from left-endpoint parity") does not survive auditor + control pressure. A narrower residual survives as measured only.

| Agent | Position |
| --- | --- |
| Implementer | WEAKENED; residual endpoint/tie statement only |
| Auditor | INVALIDATE framing of causal chain; NARROW FURTHER; block as new PGS law |
| Verifier | Pred A definitional; Pred B survives at z4 on D; p+1-only z4 mass |
| Scribe | Continuity for prior remainder residual package; this package owns parity controls |

## What was killed or definitionally collapsed

| Claim fragment | Outcome | Evidence |
| --- | --- | --- |
| Even-witness z4 mismatch rate > odd as independent modular discovery | **weakened to definitional** | On `M_v1`, `z >= 4 <=> 30 \| w` forces even; odd max z is 3 |
| Leftmost among ties preferentially even | **falsified (measured)** | Regime D ties: left even 21.60%, right even 21.65% |
| General even interiors inflate z4 under GWR | **falsified (measured)** | All GWR z4 mass at `w = p+1`; other-even z4 = 0 on D |
| Rightmost fewer mismatches as threshold-robust law | **falsified at z>=3 on fresh F** | F: left mm z3 335, right 357 |
| Rightmost optimality / PGS selector law | **not claimed; rejected as law** | Sparse residual only |
| Absolute z4 twin lock `z(GWR)>=4 => g=2` | **invalidated** | Already `PROOF.md`; reconfirmed |

## What survives as measured residual only

On regimes D (`p in [11, 2.5e7]`, 1,565,923 gaps) and F (`p in (2.5e7, 5e7]`, 1,435,207 gaps):

1. Every GWR `z >= 4` event and every GWR `z4` mismatch sits at `w = p + 1`.
2. Every GWR `z4` mismatch is a multi-way min-`tau` tie (unique min: 0 mismatches).
3. Rightmost min-`tau` has fewer `z4` mismatches than leftmost: D 0 < 2; F 2 < 3.
4. Even rate of `z >= 3` mismatches exceeds odd rate on M, D, F (measured; not theorem).

## Prediction scorecard (user Part 2)

| Prediction | Formal outcome | Mechanism isolation |
| --- | --- | --- |
| (A) even-witness z4 mm rate strictly higher than odd under leftmost | Inequality holds on D/F | **Does not isolate mechanism**: odd arm structurally empty |
| (B) rightmost fewer total mm than leftmost on large fresh data | Holds at z4 on F (2 < 3) | Comparative residual only; fails at z3 on F |
| Disconfirm (a) no even/odd difference | Not triggered (definitional difference exists) | Theater for "parity bias" insight |
| Disconfirm (b) rightmost more mm | Not triggered at z4 | Does not prove rightmost law |

Distinguishing signature in the user text (forced factor 2 at p+1) is **partly true as residual description** and **over-strong as causal novelty**: the operative modular object on the dead historical z≥4⇒g=2 claim gate is `30 \| (p+1)`, not bare parity of arbitrary min-`tau` witnesses.

## Allowed residual statement

> Under gap-reading min-`tau` selection with residual metric `z >= 4` on `M_v1`, GWR false positives on tested regimes sit exclusively at left endpoint `p+1` on multi-way min-`tau` ties. Rightmost min-`tau` reduces (does not always eliminate) that z4 mismatch count. This is an endpoint / tie-break residual of an invalidated historical z≥4⇒g=2 claim rule, not a general even-vs-odd preference among min-`tau` interiors, and not a proved selector law.

## Forbidden language (post-audit)

- "Systematic modular bias" as a new PGS law
- "Higher mismatch when witness even" without labeling definitional z4 structure
- "Leftmost preferentially picks even among ties" (measured false as general preference)
- "Rightmost is optimal / the correct selector"
- verified / validated without executed `10^18`
- Confusion with GWR maximizer theorem (untouched; different objective)

## Paths

| Path | Role |
| --- | --- |
| `FINDINGS.md` | Full quantitative report |
| `HYPOTHESIS.md` | Claims and kill switches |
| `probe_parity_bias.py` | Deterministic multi-probe |
| `artifacts/results_*.json` | Measured outputs |
| Prior comparative kill | `../leftmost-min-modular-closure-falsification-2026-07/` |

## Next decisive pressure (if residual is pursued)

1. Stratify by `30 \| (p+1)` and min-`tau` tie rank (not parity alone).
2. Pre-register effect-size thresholds; n is still small for z4 mm (2 on D, 3 on F leftmost).
3. Do not optimize selectors against a dead historical z≥4⇒g=2 claim residual as if it were a live PGS law.
