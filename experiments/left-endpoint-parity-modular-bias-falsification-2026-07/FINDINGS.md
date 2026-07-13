# Findings: left-endpoint parity modular bias falsification

## Executive summary

**Overall status of the insight package: WEAKENED (not fully FALSIFIED).**

The pre-registered primary even-vs-odd claim at `z >= 4` is **not an independent modular discovery**: on `M_v1`, `z >= 4` forces `30 | w`, hence even. Odd GWR witnesses cannot mismatch under that definition. That arm is **weakened** to a logical consequence of the modular zero structure plus the mismatch gate.

What **survives as measured** (not theorem) on regimes that actually contain mismatches:

1. **Endpoint concentration:** every GWR `z >= 4` event and every GWR `z4` mismatch sits at `w = p + 1`.
2. **Tie-break isolation:** every GWR `z4` mismatch is a multi-way min-`tau` tie; unique-min never mismatches at `z4` on these surfaces.
3. **Rightmost fewer at `z >= 4`:** on the prior window and on a **fresh** band, rightmost min-`tau` has strictly fewer `z4` mismatches than leftmost.

What **fails or weakens the broader narrative**:

1. Among multi-way ties, leftmost is **not** systematically more even than rightmost (cross-parity counts nearly balance).
2. On the fresh band, at the **alternate** gate `z >= 3`, rightmost has **more** mismatches than leftmost (`357 > 335`). Prediction 2 is **threshold-sensitive**.
3. Small regimes with zero `z4` mismatches give equal even/odd rates (both zero): labeled **vacuous / no mismatch surface**, not a clean kill.

No `verified` / `validated` language. Highest left prime `5e7`. Not a `10^18` surface. Theorems in `PROOF.md` untouched.

---

## Inventory of prior package (definitions reused)

Source: `experiments/leftmost-min-modular-closure-falsification-2026-07/`

| Term | Definition used here |
| --- | --- |
| Interior | integers `n` with `p < n < q` |
| `tau` | divisor count (field prep by linear accumulation) |
| GWR / leftmost min-`tau` | leftmost interior with minimal `tau` |
| Rightmost min-`tau` | rightmost interior with minimal `tau` |
| Unique min | `\|min-tau set\| = 1` |
| `z(w)` | remainder-zero count on `M_v1 = (2,3,5,7,30,210,2310)` |
| Mismatch (primary) | `z(w) >= 4` and `g = q - p > 2` |
| Mismatch (alt) | `z(w) >= 3` and `g > 2` |
| Endpoint | `w == p + 1` (always even for odd prime `p`) |

Prior package already **falsified** leftmost *necessity* for modular closure (`rightmost mm < GWR mm` on `p <= 2.5e7`). This package attacks a **different** claim: parity / left-endpoint bias as the mechanism of mismatch inflation.

Pinned Super-Signal CEs (`PROOF.md`): `p = 17666309`, `p = 22284029` (both reconfirmed; both `w = p + 1`).

---

## Hypotheses and disconfirmation criteria

See `HYPOTHESIS.md`. Short form:

| Claim | Prediction | Kill switch |
| --- | --- | --- |
| H-parity | even GWR subset has strictly higher `z4` mismatch rate than odd | D-a: no measurable difference |
| H-parity non-deg | same at `z >= 3` | D-a3: even not strictly higher |
| H-rightmost | rightmost total `z4` mm **fewer** than leftmost on fresh large data | D-b: rightmost **more** |
| H-endpoint | mismatches concentrate at `w = p + 1` | D-c: not concentrated |
| H-tie-break | effect is ties + leftmost at `p+1`, not unique-even alone | D-d: unique carries the load |

---

## Execution

```bash
python3 -m pytest experiments/left-endpoint-parity-modular-bias-falsification-2026-07/test_probe_parity_bias.py -q

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 11 --p-max 100000 \
  --out experiments/left-endpoint-parity-modular-bias-falsification-2026-07/artifacts/results_pmin_11_pmax_100000.json

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 11 --p-max 2000000 \
  --out experiments/left-endpoint-parity-modular-bias-falsification-2026-07/artifacts/results_pmin_11_pmax_2000000.json

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 11 --p-max 25000000 \
  --out experiments/left-endpoint-parity-modular-bias-falsification-2026-07/artifacts/results_pmin_11_pmax_25000000.json

python3 experiments/left-endpoint-parity-modular-bias-falsification-2026-07/probe_parity_bias.py \
  --p-min 25000000 --p-max 50000000 --exclusive-min \
  --out experiments/left-endpoint-parity-modular-bias-falsification-2026-07/artifacts/results_pgt_25000000_pmax_50000000.json
```

Environment: Python 3.13, worktree, deterministic enumeration (no RNG).  
Unit tests: **5 passed**.

---

## Results by regime

### Regime S (smoke): `p in [11, 1e5]`, 9588 gaps

| Slice | gaps | z4 | mm z4 | mm z3 |
| --- | ---: | ---: | ---: | ---: |
| GWR even | 3709 | 407 | 0 | 0 |
| GWR odd | 5879 | 0 | 0 | 0 |
| GWR at `p+1` | 2291 | 407 | 0 | 0 |
| GWR not `p+1` | 7297 | 0 | 0 | 0 |
| Leftmost total mm z4 / Rightmost | 0 / 0 | | | |

Notes: all 407 GWR `z4` events are twins at `p+1`. No mismatch surface (D-a / D-a3 vacuous). Odd `z4 = 0` structural.

### Regime M: `p in [11, 2e6]`, 148929 gaps

| Slice | gaps | z4 | mm z4 | mm z3 | rate mm z3 |
| --- | ---: | ---: | ---: | ---: | ---: |
| GWR even | 50910 | 4919 | 0 | 26 | 5.107e-4 |
| GWR odd | 98019 | 0 | 0 | 12 | 1.224e-4 |
| Leftmost / rightmost mm z4 | 0 / 0 | | | | |
| Leftmost / rightmost mm z3 | 38 / 22 | | | | |

At `z >= 3`, even rate strictly higher than odd (**H-parity z3 survives** on this regime). Still no `z4` mismatch.

### Regime D (prior decisive window, new parity forensics): `p in [11, 2.5e7]`, 1,565,923 gaps

#### Probe 1: even vs odd (GWR)

| Slice | gaps | z4 | mm z4 | rate mm z4 | mm z3 | rate mm z3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Even | 492629 | 43170 | **2** | 4.06e-6 | 253 | 5.136e-4 |
| Odd | 1073294 | **0** | **0** | 0 | 106 | 9.876e-5 |

- Strict even higher at `z4`: yes, but **structurally forced** (`odd z4 events = 0`).
- Strict even higher at `z3`: yes (**survives measured**).

#### Probe 2: endpoint concentration (GWR)

| Slice | gaps | z4 | mm z4 |
| --- | ---: | ---: | ---: |
| `w = p + 1` | 263418 | 43170 | **2** |
| `w != p + 1` | 1302505 | **0** | **0** |

- Fraction of GWR `z4` at `p+1`: **1.0**
- Fraction of GWR `z4` mismatches at `p+1`: **1.0** (2/2)

#### Probe 3: left vs right

| Gate | leftmost mm | rightmost mm |
| --- | ---: | ---: |
| `z >= 4` | **2** | **0** |
| `z >= 3` | 359 | 335 |

Rightmost strictly fewer at primary gate (**survives**).

#### Probe 4: unique vs ties

| Slice | gaps | mm z4 |
| --- | ---: | ---: |
| Unique min | 578479 | **0** |
| Ties (left != right) | 987444 | **2** |
| Ties and left at `p+1` | 81880 | **2** |
| Ties and left not `p+1` | 905564 | **0** |

**All** mismatches are ties with left witness at `p+1`.

#### Tie parity structure (regime D)

| Quantity | Count / rate |
| --- | ---: |
| Ties | 987444 |
| Left is `p+1` | 81880 (8.29%) |
| Right is `p+1` | **0** (definitional for multi-way ties) |
| Left even | 213289 (21.60%) |
| Right even | 213744 (21.65%) |
| Left even, right odd | 176761 |
| Left odd, right even | 177216 |

**Key control:** leftmost is **not** more even than rightmost among ties. The narrative "leftmost preferentially lands on even" is **false as a general tie bias**. The operative fact is narrower: if `p+1` is in the min-`tau` set, leftmost **must** select it, and that point is always even and is the only place GWR `z4` fires.

#### Mismatch samples (regime D)

| p | q | g | w_left | z_left | w_right | z_right | min set | unique |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 17666309 | 17666317 | 8 | 17666310 | 4 | 17666315 | 1 | 5 | no |
| 22284029 | 22284037 | 8 | 22284030 | 4 | 22284035 | 1 | 5 | no |

Both: `w_left = p + 1`, multi-way ties, rightmost escapes `z4`.

### Regime F (FRESH): `p in (2.5e7, 5.0e7]`, 1,435,207 gaps

Independent of prior package upper window.

#### Probe 1 / 2

| Slice | gaps | z4 | mm z4 | rate mm z4 | mm z3 | rate mm z3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Even | 432806 | 36306 | **3** | 6.932e-6 | 243 | 5.615e-4 |
| Odd | 1002401 | 0 | 0 | 0 | 92 | 9.178e-5 |
| at `p+1` | 223017 | 36306 | **3** | | | |
| not `p+1` | 1212190 | 0 | 0 | | | |

Again: all `z4` and all `z4` mismatches at `p+1`. Odd `z4 = 0`.

#### Probe 3 (fresh left vs right)

| Gate | leftmost mm | rightmost mm | Prediction 2 |
| --- | ---: | ---: | --- |
| `z >= 4` | **3** | **2** | rightmost fewer: **holds** |
| `z >= 3` | 335 | **357** | rightmost fewer: **fails** |

Disconfirmation D-b (rightmost **more** at primary `z4`) is **not met**.  
But the comparative claim is **not robust** to lowering the zero threshold to 3 on this fresh band.

#### Probe 4 (fresh)

| Slice | mm z4 |
| --- | ---: |
| Unique | **0** |
| Ties | **3** |
| Ties left at `p+1` | **3** |
| Ties left not `p+1` | **0** |

#### Fresh mismatch samples

| p | q | g | w_left | z_left | w_right | z_right | min set |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 39110069 | 39110077 | 8 | 39110070 | 4 | 39110074 | 1 | 4 |
| 45515369 | 45515377 | 8 | 45515370 | 4 | 45515375 | 1 | 5 |
| 49117829 | 49117837 | 8 | 49117830 | 4 | 49117835 | 1 | 5 |

Pattern matches Super-Signal CEs: `g = 8`, `w = p + 1`, multi-way min-`tau` ties, rightmost often escapes (here z_right = 1 on all three listed). Yet rightmost still has **2** total `z4` mismatches on this band (not zero).

Tie parity again nearly balanced: left even 20.90%, right even 20.89%.

---

## Disconfirmation scorecard

| ID | Criterion | Regime D (`<=2.5e7`) | Regime F (fresh `(2.5e7,5e7]`) |
| --- | --- | --- | --- |
| D-a | no even/odd z4 mm difference | **not met** (even > odd) but **structurally forced** | same |
| D-a3 | even not strictly higher at z3 | **not met** (even higher) | **not met** (even higher) |
| D-b | rightmost MORE z4 mm than left | **not met** (0 < 2) | **not met** (2 < 3) |
| D-c | mm not concentrated at p+1 | **not met** (2/2 at p+1) | **not met** (3/3 at p+1) |
| D-d | unique alone carries mm | **not met** (ties only) | **not met** (ties only) |

No pre-registered kill switch fully fires against the **narrow** endpoint/tie residual. Several fire against **loose** readings of "parity bias among all min-tau witnesses."

---

## Status labels (final)

| Claim | Status | Precise note |
| --- | --- | --- |
| H-parity at `z >= 4` (independent insight) | **weakened** | Logically forced by `z >= 4 => 30\|w => even` on `M_v1` |
| H-parity at `z >= 3` | **survives (measured)** | Even mm rate > odd on M, D, F |
| H-endpoint (`w = p+1` concentration) | **survives (measured)** | 100% of GWR z4 and z4-mm on D and F |
| H-rightmost fewer total mm at `z4` | **survives (measured)** | D: 0<2; F: 2<3 |
| H-rightmost fewer at `z3` | **falsified on F** | F: 357 > 335 |
| H-tie-break (ties + p+1, not unique) | **survives (measured)** | Unique mm z4 = 0 on D and F |
| "Leftmost prefers even among ties" | **falsified (measured)** | Left/right even rates ~equal; cross-parity nearly balanced |
| Absolute Super-Signal `z4 => g=2` | **invalidated** | Reconfirmed; already in `PROOF.md` |
| GWR maximizer / modular zero lemma | **theorem** | Untouched |
| Program verified / validated | **not claimed** | Max regime `5e7`, no `10^18` |

### Overall insight verdict

```text
WEAKENED
```

**Not FALSIFIED** as a whole: the distinguishing signature (mismatches under leftmost concentrated on even `p+1` multi-way ties; rightmost fewer at `z4` on fresh large data) **holds on measured regimes D and F**.

**Not SURVIVES cleanly either:** the insight overstates (1) even-vs-odd as a free modular bias rather than the modular zero lemma, and (2) a general leftmost-even preference among ties that the control table rejects.

**Best residual statement (hypothesis, measured support only):**

> Under gap-reading min-`tau` selection with the primary modular gate `z >= 4`, GWR false positives on the tested regimes sit exclusively at the left endpoint `p + 1` on multi-way min-`tau` ties. Rightmost min-`tau` reduces (does not always eliminate) that `z4` mismatch count. This is an endpoint / tie-break phenomenon, not a general even-vs-odd preference among min-`tau` interiors.

---

## Limitations

- Upper left prime `5e7` only. No `10^18` surface.
- Rightmost having fewer `z4` mismatches is **measured**, not a theorem (and fails at `z3` on F).
- Fresh band still mid-scale relative to program ladder decades.
- Concentration threshold for D-c was soft (`>= 0.5`); observed fractions were `1.0`, so the call is robust to that choice.
- Classical sieves prepare primes and `tau` only.

---

## Provenance

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Claims and kill switches |
| `experiment_design.md` | Protocol |
| `probe_parity_bias.py` | Deterministic multi-probe |
| `test_probe_parity_bias.py` | Local unit checks |
| `artifacts/results_*.json` | Raw measured outputs |
| `FINDINGS.md` | This report |

Related prior (leftmost necessity, already falsified):  
`experiments/leftmost-min-modular-closure-falsification-2026-07/`

---

## Auditor / Verifier checklist (for Quartet peers)

1. Confirm mismatch definition matches primary gate `z >= 4 and g > 2`.
2. Confirm fresh band is `p > 2.5e7` and `p <= 5e7` (exclusive min).
3. Confirm no `verified`/`validated` language without `10^18`.
4. Confirm odd `z4 == 0` is treated as structural (modular zero), not marketed as novel parity physics.
5. Confirm rightmost mm z4 on F is 2 (not 0): do not claim rightmost is perfect.
6. Re-run unit tests and one mid regime if independent verification is required.
