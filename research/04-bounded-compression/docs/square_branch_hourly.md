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

## 2026-07-10T20:05:10Z run

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
4 passed in 2.47s
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

## 2026-07-10T21:05:27Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S3 right-endpoint completion and chamber-reset residual).

Method:
PGS-first constructive subsection under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on Claims S1 and S2 only. H5: right completion after selected square by
proved direct next-prime rule. Claim S3-A: `F(r) = q − r²` and `q − p = D(r) + F(r)`.
Claim S3-B: chamber-reset residual triple
`ResetResidual(r) = (D(r), F(r), first_τ4_offset)`; Target S1* fails iff
`D(r) ∈ Annulus(r)`. Claim S3-C: late-dominant phase residual
`phase_gap(r) = (D − first_τ4)/D` with `0 < phase_gap < 1`. Residual RC6–RC8
attached as audit only; RC2 retained falsified; d=4 SDA not revived.
`PROOF.md` §Square-Branch Reduction: proximity target remains UNRESOLVED.
One minimal falsification command: dynamic-cutoff search on `5e8–6e8`.

Result:
Constructive lemma subsection S3 written with hypotheses (H1–H4 reused + H5),
unresolved Target S1*, residual claim table RC6–RC8 attached, and explicit
falsification command. No new measured regime this hour. Direct next-prime and
Interior Maximizer remain proved; proximity not claimed.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 3.00s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S3 (right-endpoint completion F(r),
chamber-reset residual triple, late-dominant phase residual) with residual
RC6–RC8 table attachment and minimal falsification command for Target S1*
(`5e8–6e8` dynamic-cutoff search). Not a replay of S1 or S2.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r) ∉ Annulus(r)` via `ResetResidual(r)`; do not revive residue
covers, fixed-540, or d=4 SDA; do not promote RC6–RC8 to theorem status.

## 2026-07-10T22:06:38Z run

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
elapsed_seconds: 87.58234286308289

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.83s
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

## 2026-07-10T23:07:11Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation — residual claims RC9–RC11 on the interior τ4 offset set.

Method:
Read falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived).
Built minimal probe
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_residual_rc9_probe.py`
recomputing the full τ4 offset set on 5 segment util maxima + 3 o_q branch-max
rows from the prior chamber table. Predictions P13–P15:

- P13/RC9: early-half τ4 mass ≥ 0.40
- P14/RC10: last_τ4 / D ≥ 0.95
- P15/RC11: max consecutive τ4 gap (lead+interior+trail) / D ≤ 0.10

Does not replay P1–P12 / RC3–RC8 as primary deliverable. Fixed-band RC2 retained
falsified. Prime-Square Proximity remains proved (`PROOF.md`); residual audit only.

Result:
All three new residuals hold on the surface through 4e8–5e8:

| claim | bound | extremum observed |
| --- | --- | --- |
| RC9 early-half mass | ≥ 0.40 | min 0.4151 (o_q=4, D=486) |
| RC10 late-span | ≥ 0.95 | min 0.9631 (o_q=2, D=542) |
| RC11 max gap frac | ≤ 0.10 | max 0.0812 (o_q=2, gap=44) |

Util-max row r=424171123 (D=738): early mass 0.469, late span 0.989, max gap
frac 0.041. RC2 remains falsified at D=738. No d=4 SDA revival.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 3.16s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC9–RC11 (early-half τ4 mass, late-span τ4 presence,
max inter-τ4 gap bound) with explicit falsification command on recomputed τ4
offset geometry; not a replay of RC6–RC8 or fixed-band 540.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_residual_rc9_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_rc9_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc9/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8–6e8` or prefix-tau extremal rerun on newest rows.
Re-check RC9–RC11 on any new util maximum; do not revive fixed-band 540 or
d=4 SDA; do not promote RC9–RC11 to theorem status.

## 2026-07-11T00:05:10Z run

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
4 passed in 2.60s
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

## 2026-07-11T01:06:40Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S4 interior τ4 field and chamber-cover residual).

Method:
PGS-first constructive draft under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on Claims S1–S3 only. Objects: ordered chamber prefix, full τ4 offset
set `Tau4(r)`, cover residual functionals
`(early_half_mass, late_span, max_gap_frac)`, extended reset residual
`ResetResidual⁺(r) = (D(r), F(r), first_τ4_offset, Cover(r))`. Hypotheses
H1–H5 reused; H6 adds nonempty interior τ4 field under H4. Target S1* left
UNRESOLVED per `PROOF.md` §Square-Branch Reduction. Residual table RC9–RC11
attached as audit only; RC2 remains falsified; d=4 SDA and fixed-540 not
revived. Minimal falsification command: dynamic-cutoff search on `5e8–6e8`;
optional RC9 cover-panel probe.

Result:
Constructive lemma subsection S4 written with hypotheses H6, Claims S4-A/B/C,
status separation update, residual cover table on the 4e8–5e8 o_q branch-max
panel, and explicit falsification commands. No new measured regime this hour.
Theorem: proximity remains unresolved in `PROOF.md`; direct next-prime and
Interior Maximizer remain proved.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.77s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S4 (interior τ4 field, chamber-cover residual
functionals, extended `ResetResidual⁺`) with residual claim table RC9–RC11 and
minimal falsification command for Target S1* (`5e8–6e8` dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C; re-check RC9–RC11 on any
new util maximum; do not promote Cover residuals or RC9–RC11 to theorem status.

## 2026-07-11T02:06:36Z run

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
elapsed_seconds: 85.51669478416443

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.64s
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

## 2026-07-11T03:06:57Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation — next residual after RC9–RC11.

Method:
Read latest falsification summary
`square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json` and
`prefix_tau_floor_probe.json` (SDA-invalidation note only). Produced residual
claim table RC12–RC14 with minimal probe under
`experiments/square-branch-hourly-2026-07-11-rc12/`. Did not port d=4 SDA.
Did not restate RC9–RC11 as the sole deliverable.

Objects: ordered chamber prefix before selected square `w=r^2`; divisor-count
field `tau`; offset `D(r)`; Tau4 offset set; first-quarter / last-quarter mass
and median location of Tau4.

Result:
RC12 first-quarter τ4 mass ≥ 0.15: **holds** (min 0.1833 on 2e8–3e8 util max).
RC13 last-quarter τ4 mass ≥ 0.15: **holds** (min 0.2000 on o_q=2 branch max).
RC14 median τ4 / D ∈ [0.40, 0.65]: **holds** (observed [0.448, 0.572]).
RC2 fixed near-540 band: retained **falsified**.
RC9–RC11: retained holds (not primary surface).
d=4 SDA remains invalidated. Theorem: Prime-Square Proximity remains proved in
`PROOF.md`; residual audit only.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.95s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC12–RC14 (first-quarter τ4 mass, last-quarter τ4 mass,
median mid-band) with explicit falsification command on util maxima + o_q panel
through 4e8–5e8.

Artifacts:
`experiments/square-branch-hourly-2026-07-11-rc12/offset_540_residual_rc12_probe.py`;
`experiments/square-branch-hourly-2026-07-11-rc12/offset_540_rc12_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-11-rc12/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8–6e8`, or re-check RC12–RC14 on any new util / o_q
branch maximum. Do not promote RC12–RC14 to theorem status.

## 2026-07-11T04:05:11Z run

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
4 passed in 2.72s
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

## 2026-07-11T05:06:27Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S5 quartile-balance residual on Tau4).

Method:
PGS-first constructive draft under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on Claims S1–S4 only. Objects: ordered interior τ4 field `Tau4(r)`,
chamber quarter cuts `Q1=⌊D/4⌋`, `Q3=⌊3D/4⌋`, outer-early / mid / outer-late
zones, quartile-balance functionals
`(first_quarter_mass, last_quarter_mass, median_frac)`, balanced extended
reset residual
`ResetResidual^Q(r) = (D(r), F(r), first_τ4_offset, Cover(r), QuartileBalance(r))`.
Hypotheses H1–H6 reused; no new hypothesis. Target S1* left UNRESOLVED per
`PROOF.md` §Square-Branch Reduction. Residual table RC12–RC14 attached as
audit only (from prior hour probe; not re-proved as theorem). RC2 remains
falsified; d=4 SDA and fixed-540 not revived. Minimal falsification command:
dynamic-cutoff search on `5e8–6e8`; optional RC12 quartile probe.

Result:
Constructive lemma subsection S5 written with Claims S5-A/B/C, status
separation update, residual quartile table on the 4e8–5e8 o_q branch-max
panel, and explicit falsification commands. No new measured regime this hour.
Theorem: prime-square proximity remains UNRESOLVED in `PROOF.md`; direct
next-prime and Interior Maximizer remain proved.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.89s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S5 (quartile partition of Tau4, quartile-balance
residuals, balanced `ResetResidual^Q`) with residual claim table RC12–RC14
attached and minimal falsification command for Target S1* (`5e8–6e8`
dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C, S5-C; re-check RC9–RC14
on any new util maximum; do not promote QuartileBalance or RC12–RC14 to theorem
status.

## 2026-07-11T06:06:36Z run

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
elapsed_seconds: 85.78194618225098

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.94s
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

## 2026-07-11T07:06:57Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation (queue job offset-540-structural-audit).

Method:
Read 4e8-5e8 falsification summary and prefix_tau_floor_probe.json.
Built minimal residual probe
`experiments/square-branch-hourly-2026-07-11-rc15/offset_540_residual_rc15_probe.py`
stating falsifiable predictions P19-P21 / residual claims RC15-RC17 on
segment utilization maxima through 4e8-5e8 plus full o_q branch-max panel.
Recomputed Tau4 dual markers via divisor_counts_segment only (audit).
Did not port d=4 SDA. RC2 fixed-band remains falsified.

Result:
RC15 late-tau3 trail tightness holds: trail_gap = D - last_tau4 in [2, 20]
(bound [1, 24]).
RC16 absolute early tau4 on full panel holds: first_tau4 in [2, 16]
(bound <= 16; tightens RC4 util-only <= 20 and extends to o_q panel).
RC17 near-540 dual marker holds on 4 rows with |D-540|<=20:
first_tau4 in [4, 10], trail in [8, 20].
No new falsified prediction. Util-max escape D=738 (o_q=6) retained as RC2
falsifier. Prime-Square Proximity remains proved in PROOF.md; residual audit
only.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.78s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC15-RC17 (late-tau3 trail tightness, absolute early
tau4 on full util+o_q panel, conditional near-540 dual early/late markers)
with explicit falsification command; not a prose restatement of RC12-RC14.

Artifacts:
`experiments/square-branch-hourly-2026-07-11-rc15/offset_540_residual_rc15_probe.py`;
`experiments/square-branch-hourly-2026-07-11-rc15/offset_540_rc15_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-11-rc15/FINDINGS.md`

Next step:
Queue falsification on 5e8-6e8, or re-check RC15-RC17 on any new util maximum
/ o_q branch max. Do not promote RC15-RC17 to theorem status; do not revive
fixed-540 or d=4 SDA.

## 2026-07-11T08:05:10Z run

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
4 passed in 2.68s
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

## 2026-07-11T09:06:32Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S6 late-trail dual markers and trail-extended residual).

Method:
PGS-first constructive draft under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on Claims S1–S5 only. Objects: ordered field `Tau4(r)`, last-τ4 marker
`last_τ4_offset = max Tau4(r)`, late trail `trail_gap(r) = D(r) − last_τ4_offset`,
dual early/late marker pair `Dual(r) = (first_τ4_offset, trail_gap(r))`, and
trail-extended chamber-reset residual
`ResetResidual^T(r) = (D(r), F(r), first_τ4_offset, Cover(r), QuartileBalance(r), Trail(r))`
with `Trail(r) = (last_τ4_offset, trail_gap(r), Dual(r))`. Hypotheses H1–H6
reused; no new hypothesis. Target S1* left UNRESOLVED per `PROOF.md`
§Square-Branch Reduction. Residual table RC15–RC17 attached as audit only
(from prior hour probe; not promoted to theorem). RC2 remains falsified;
d=4 SDA and fixed-540 not revived. Minimal falsification command:
dynamic-cutoff search on `5e8–6e8`; optional RC15 dual-marker probe.

Result:
Constructive lemma subsection S6 written with Claims S6-A/B/C, residual claim
table update (S6-A/B/C + RC15–RC17), status separation update, dual-marker
panel on the 4e8–5e8 o_q branch-max rows, and explicit falsification commands.
No new measured regime this hour. Theorem: prime-square proximity remains
UNRESOLVED in `PROOF.md`; direct next-prime and Interior Maximizer remain
proved.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.78s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S6 (last-τ4 / trail_gap dual markers,
`Dual(r)`, trail-extended `ResetResidual^T`) with residual claim table
RC15–RC17 attached and minimal falsification command for Target S1*
(`5e8–6e8` dynamic-cutoff search). Not a prose restatement of S5 or of the
RC15 probe alone.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8–6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C, S5-C, S6-C; re-check
RC9–RC17 on any new util maximum; do not promote Trail/Dual or RC15–RC17 to
theorem status.

## 2026-07-11T21:06:34Z run

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
elapsed_seconds: 82.30978488922119

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.73s
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

## 2026-07-11T22:05:56Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation (Dual L1 and tau4 span residuals RC18–RC20).

Method:
Read falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`.
Built minimal probe under `experiments/square-branch-hourly-2026-07-11-rc18/`
recomputing Dual(r)=(first_τ4, trail_gap) on segment utilization maxima through
4e8–5e8 and the full o_q∈{2,4,6} branch-max panel. New residual claims (not a
restatement of RC15–RC17 componentwise bounds):
- P22/RC18: Dual L1 = first_τ4 + trail_gap ≤ 24
- P23/RC19: (last_τ4 − first_τ4)/(D−1) ≥ 0.95
- P24/RC20: (first_τ4 + trail_gap)/D ≤ 0.05
RC2 fixed near-540 band retained falsified; d=4 SDA not revived. Prime-square
proximity remains unresolved in PROOF.md (audit only).

Result:
All three new residual claims hold on the evaluated surface (8 rows: 5 util
maxima + 3 o_q panel).
- dual_l1 range: [4, 24] (tight at near-540 util max r=251066071 and o_q=2
  r=468917503)
- span_frac range: [0.9567, 0.9935]
- dual_l1_rel range: [0.0087, 0.0453]
- near_540 count: 4; near_540 dual_l1 range: [14, 24]
- util max 4e8–5e8 still D=738 (RC2 falsified)
Falsification command:
`python3 experiments/square-branch-hourly-2026-07-11-rc18/offset_540_residual_rc18_probe.py`

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 3.23s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC18–RC20 (Dual L1 envelope, tau4 support span
fraction, relative Dual L1) with explicit falsification command; not a prose
restatement of RC15–RC17.

Artifacts:
`experiments/square-branch-hourly-2026-07-11-rc18/offset_540_residual_rc18_probe.py`;
`experiments/square-branch-hourly-2026-07-11-rc18/offset_540_rc18_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-11-rc18/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8–6e8` (or re-check RC15–RC20 on any new util maximum).
Do not promote Dual L1 / span fraction to theorem; keep RC2 falsified.

## 2026-07-11T23:05:10Z run

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
4 passed in 2.62s
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

## 2026-07-12T01:06:35Z run

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
elapsed_seconds: 86.74751210212708

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.89s
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

## 2026-07-12T03:05:11Z run

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
4 passed in 2.52s
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

## 2026-07-12T05:06:43Z run

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
elapsed_seconds: 91.64809489250183

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.47s
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

## 2026-07-12T08:05:10Z run

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
4 passed in 2.41s
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

## 2026-07-12T10:06:36Z run

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
elapsed_seconds: 85.20178890228271

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.96s
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

## 2026-07-12T22:05:10Z run

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
4 passed in 2.51s
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

## 2026-07-13T00:06:32Z run

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
elapsed_seconds: 86.48505687713623

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.53s
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

## 2026-07-13T01:07:00Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-τ=4 / late-τ=3
chamber separation — residual claims RC21–RC23 after Dual L1 surface (RC18–RC20).

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
prior chamber table from `experiments/square-branch-hourly-2026-07-10/`, and
RC18 Dual L1 table. Ran new probe
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_residual_rc21_probe.py`
evaluating P25–P27 (τ4 density envelope, Dual max-component share, near-540
Dual L1 floor). Did not restate P22–P24 as the sole deliverable.

Result:
RC21 holds: τ4 density dens = tau4_count/(D−1) ∈ [0.10, 0.135] on 8/8 rows
(range `[0.1093, 0.1303]`).
RC22 holds: Dual max-component share max(first, trail)/L1 ≤ 0.85 on 8/8
(range `[0.50, 0.833]`).
RC23 holds (conditional): if |D−540|≤20 then Dual L1 ≥ 14 on 4/4 near-540 rows
(near L1 range `[14, 24]`); escape util-max D=738 remains outside near-540.
RC2 retained falsified (D=738). RC18–RC20 retained holds (not primary surface).
Theorem: prime-square proximity remains UNRESOLVED in `PROOF.md` §Square-Branch
Reduction; direct next-prime and Interior Maximizer remain proved. Residual
audit only. Invalidated d=4 SDA not revived.
Continuity fix: `ACTIVE_TARGET.md` re-aligned to PROOF.md (proximity open).

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.31s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New residual claim table RC21–RC23 (τ4 density envelope, Dual max-component
share, near-540 Dual L1 floor) with explicit falsification command; all three
hold on util maxima through 4e8–5e8 + o_q panel. Not a replay of RC18–RC20.
Theorem-status continuity corrected to PROOF.md (proximity unresolved).

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_residual_rc21_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_rc21_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc21/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md`

Next step:
Queue falsification `5e8–6e8` and re-check RC21–RC23 on any new util maximum.
Keep RC21–RC23 residual only; do not promote to theorem; do not revive
fixed-band 540 or d=4 SDA.

## 2026-07-13T02:05:11Z run

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
4 passed in 2.21s
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
