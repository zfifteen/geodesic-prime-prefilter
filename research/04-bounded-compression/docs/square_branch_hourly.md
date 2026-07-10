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

## 2026-07-10T11:06:28Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation on the `4e8-5e8` utilization maximum.

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and prior `prefix_tau_floor_probe.json` / 2026-06-19 chamber baselines.
Ran `experiments/square-branch-hourly-2026-07-10/offset_540_chamber_geometry_probe.py`
to evaluate six falsifiable predictions (P1–P6) on four prior segment maxima
plus the new extremal, and chamber checks on per-`o_q` maxima. No d=4 SDA port.

Result:
New extremal `r=424171123`, offset `738`, utilization `0.9341772151898734`,
dynamic cutoff `790`, `o_q=6`.
Chamber predictions P1–P5 hold on the new row: `prefix_min_tau=4`,
`first_tau4_offset=3`, `first_tau3_offset=738`, `tau4_count=96`, `tau5_count=0`.
P6 fixed band `[528, 552]` is **falsified** (`738` outside).
Per-`o_q` chamber checks hold for offsets `542`, `486`, `738`.
Theorem: Prime-Square Proximity remains **proved** (`PROOF.md`); this is residual
audit only. Invalidated: d=4 SDA transfer (not revived).

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.80s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
Falsified fixed near-540 band residual claim on `4e8-5e8` utilization maximum
(`D(r)=738`); early τ=4 / late τ=3 chamber separation (P1–P5) holds; residual
claim table RC1/RC2 + prediction table written.

Artifacts:
`experiments/square-branch-hourly-2026-07-10/offset_540_chamber_geometry_probe.py`;
`experiments/square-branch-hourly-2026-07-10/offset_540_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows (`prefix-tau-extremal-rerun`)
or queue falsification `5e8-6e8`. Do not revive fixed-band 540 as a law.

## 2026-07-10T12:05:10Z run

Mechanism:
Prefix tau-floor probe on the three latest segment extremal rows

Method:
deterministic dispatch: /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py

Result:
Command exit code: 2
stdout tail:
```

```
stderr tail:
```
/Library/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/velocityworks/pgs-hourly/prime-gap-structure/experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py': [Errno 2] No such file or directory
```

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 3.06s
```

Delta classification: command exited nonzero

Research status:
FAILED

Ops status:
OK

Delta:
command exited nonzero

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py; experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json

Next step:
Queue falsification 500M-600M or draft Chamber-Reset Endpoint Resolution Lemma subsection.

## 2026-07-10T13:06:24Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (Claim S1 endpoint identification; Target S1* distance).

Method:
PGS-first draft under `research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Objects: ordered gap, divisor-count field, GWR selected integer, chamber prefix,
square endpoint, `D(r)`. Hypotheses H1–H4; Claim S1 identifies
`D(r) = first_τ3_offset`; Target S1* left UNRESOLVED per `PROOF.md`. Residual
claim table RC1/RC2 retained; invalidated SDA and fixed-540 band not revived.
One minimal falsification command: dynamic-cutoff search on `5e8–6e8`.

Result:
Constructive lemma subsection S1 written with hypotheses, unresolved Target S1*,
residual claim table, and explicit falsification command. No new measured
regime this hour. Theorem: proximity remains unresolved in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain proved.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.94s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S1 (selected-square endpoint identification)
with residual claim table and minimal falsification command for Target S1*
(`5e8–6e8` dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`

Next step:
Run falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claim S1; do not revive residue covers or d=4 SDA.

## 2026-07-10T14:06:37Z run

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
elapsed_seconds: 86.39055705070496

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.75s
```

Delta classification: summary signature matches prior hourly run (replay)

Research status:
NO_DELTA

Ops status:
FAILED

Delta:
summary signature matches prior hourly run (replay)

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001 --max-prime 500000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.

## 2026-07-10T15:07:17Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation — residual claims RC3–RC5 after fixed-band (RC2) death.

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
and prior chamber table from `experiments/square-branch-hourly-2026-07-10/`.
Ran new probe
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_residual_rc3_probe.py`
evaluating P7–P9 (τ4 density band, absolute early τ4, o_q=2 near-540 local
attractor). Did not replay P1–P6 as the sole deliverable.

Result:
RC3 holds: rho4 ∈ [0.10, 0.14] on 5/5 segment util maxima (new max rho4=0.1301).
RC4 holds: first_tau4_offset ≤ 20 on 5/5 (new max first_tau4=3).
RC5 holds: o_q=2 branch max on 4e8-5e8 has D=542 (|D−540|=2 ≤ 20) while global
util max o_q=6 has D=738 (escapes fixed band). Exact D=540 also appears at
o_q ∈ {4,6}, so near-540 is not exclusive to o_q=2.
RC2 retained falsified. Theorem: Prime-Square Proximity proved (`PROOF.md`);
residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.63s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC3–RC5 (τ4 density band, absolute early τ4, o_q=2
local near-540 attractor) with explicit falsification command after fixed-band
RC2 death; not a replay of P1–P6.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_residual_rc3_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_rc3_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc3/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows, or queue falsification
`5e8–6e8`. Keep RC3–RC5 as residual only; do not promote to theorem; do not
revive fixed-band 540 or d=4 SDA.

## 2026-07-10T16:05:11Z run

Mechanism:
Prefix tau-floor probe on the three latest segment extremal rows

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
4 passed in 2.85s
```

Delta classification: summary signature changed versus prior/baseline

Research status:
ADVANCE

Ops status:
OK

Delta:
summary signature changed versus prior/baseline

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 experiments/square-branch-sda-invalidation-2026-06/square_branch_prefix_tau_floor_probe.py; experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json

Next step:
Queue falsification 500M-600M or draft Chamber-Reset Endpoint Resolution Lemma subsection.

## 2026-07-10T17:06:43Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S2 band residual object and chamber-prefix phase order).

Method:
PGS-first constructive subsection under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on prior-hour Claim S1 only. Claim S2-A: under H1–H4 and D(r)≥2,
`1 ≤ first_τ4_offset < first_τ3_offset = D(r)` (early-τ=4 / late-τ=3 phase order).
Claim S2-B: under H1–H3, `D(r) < Band(r) = (r−s)(r+s)`; Target S1* fails at r
iff `D(r) ∈ Annulus(r) = {k : C_dyn(r) < k < Band(r)}`. Residual RC3–RC5
attached as audit only; RC2 retained falsified; d=4 SDA not revived.
`PROOF.md` §Square-Branch Reduction: proximity target remains UNRESOLVED.
One minimal falsification command: dynamic-cutoff search on `5e8–6e8`.

Result:
Constructive lemma subsection S2 written with hypotheses (H1–H4 reused),
unresolved Target S1*, residual claim table RC3–RC5, and explicit falsification
command. No new measured regime this hour. Direct next-prime and Interior
Maximizer remain proved; proximity not claimed.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.94s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S2 (chamber-prefix phase order + band residual
annulus object) with residual RC3–RC5 table and minimal falsification command
for Target S1* (`5e8–6e8` dynamic-cutoff search). Not a replay of S1.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r) ∉ Annulus(r)`; do not revive residue covers, fixed-540, or
d=4 SDA; do not promote RC3–RC5 to theorem status.

## 2026-07-10T18:06:36Z run

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
elapsed_seconds: 86.44854998588562

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.78s
```

Delta classification: new falsification regime through max_prime=500000000

Research status:
ADVANCE

Ops status:
FAILED

Delta:
new falsification regime through max_prime=500000000

Artifacts:
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001 --max-prime 500000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8; research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json

Next step:
Structural audit of recurring offset 540 on new extremal rows if no counterexample.

## 2026-07-10T19:05:57Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation — residual claims RC6–RC8 after RC3–RC5 surface.

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
prior chamber table from `experiments/square-branch-hourly-2026-07-10/`, and
RC3 table. Ran new probe
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_residual_rc6_probe.py`
evaluating P10–P12 (full o_q-panel S2-A phase order, late-dominant phase gap
≥0.95, o_q-stratified near-540 exclusivity). Did not replay RC3–RC5 as the
sole deliverable.

Result:
RC6 holds: S2-A phase order on 3/3 o_q branch maxima (o_q∈{2,4,6}).
RC7 holds: min phase_gap on util maxima + o_q panel = 0.967078 (o_q=4, D=486,
first_τ4=16) ≥ 0.95.
RC8 holds: only o_q=2 near 540 (|D−540|=2); o_q=4 escapes (|D−540|=54);
o_q=6 escapes (|D−540|=198). Strengthens RC5 to panel exclusivity residual.
RC2 retained falsified. Theorem: Prime-Square Proximity proved (`PROOF.md`);
residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.73s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC6–RC8 (full o_q-panel S2-A phase order, late-dominant
phase-gap bound ≥0.95, o_q-stratified near-540 exclusivity) with explicit
falsification command; not a replay of RC3–RC5.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_residual_rc6_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_rc6_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc6/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows, or queue falsification
`5e8–6e8`. Keep RC6–RC8 residual only; do not promote to theorem; do not
revive fixed-band 540 or d=4 SDA.
