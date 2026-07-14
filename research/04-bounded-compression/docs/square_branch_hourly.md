# Square Branch Hourly Research Ledger

Hourly relay log for the square-branch proximity obligation. Each block is one
activation. Status labels: **ADVANCE**, **FAILED**, **UNRESOLVED**.

Bootstrap: system installed 2026-06-19. Queue starts at falsification
`3·10^8 .. 4·10^8`.

---

## 2026-06-19T00:00:00Z bootstrap

Mechanism:
Hourly relay bootstrap - dispatcher, wrapper, launchd, ACTIVE_TARGET contract.

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
Square-branch dynamic-cutoff falsification sweep on prime roots 300M-400M

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
Square-branch dynamic-cutoff falsification sweep on prime roots 300M-400M

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
to evaluate six falsifiable predictions (P1-P6) on prior and new extremal rows.
No d=4 SDA port.

Result:
New extremal `r=358018553`, offset `546`, utilization `0.7036082474226805`.
All six predictions hold on the new row: `prefix_min_tau=4`, `first_tau4_offset=4`,
`first_tau3_offset=546`, `tau4_count=64`, `tau5_count=0`, offset in `[528,552]`.
Prior rows: offsets `540`, `462`, `540` - chamber separation 3/3.

Theorem: square-branch proximity obligation remains **unresolved** (`PROOF.md`).
Invalidated: d=4 SDA transfer (not revived).
Measured: P1-P6 hold 4/4 extremal rows tested.

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
to evaluate six falsifiable predictions (P1-P6) on four prior segment maxima
plus the new extremal, and chamber checks on per-`o_q` maxima. No d=4 SDA port.

Result:
New extremal `r=424171123`, offset `738`, utilization `0.9341772151898734`,
dynamic cutoff `790`, `o_q=6`.
Chamber predictions P1-P5 hold on the new row: `prefix_min_tau=4`,
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
(`D(r)=738`); early τ=4 / late τ=3 chamber separation (P1-P5) holds; residual
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
square endpoint, `D(r)`. Hypotheses H1-H4; Claim S1 identifies
`D(r) = first_τ3_offset`; Target S1* left UNRESOLVED per `PROOF.md`. Residual
claim table RC1/RC2 retained; invalidated SDA and fixed-540 band not revived.
One minimal falsification command: dynamic-cutoff search on `5e8-6e8`.

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
(`5e8-6e8` dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`

Next step:
Run falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
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
chamber separation - residual claims RC3-RC5 after fixed-band (RC2) death.

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
and prior chamber table from `experiments/square-branch-hourly-2026-07-10/`.
Ran new probe
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_residual_rc3_probe.py`
evaluating P7-P9 (τ4 density band, absolute early τ4, o_q=2 near-540 local
attractor). Did not replay P1-P6 as the sole deliverable.

Result:
RC3 holds: rho4 ∈ [0.10, 0.14] on 5/5 segment util maxima (new max rho4=0.1301).
RC4 holds: first_tau4_offset ≤ 20 on 5/5 (new max first_tau4=3).
RC5 holds: o_q=2 branch max on 4e8-5e8 has D=542 (|D-540|=2 ≤ 20) while global
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
New residual claim table RC3-RC5 (τ4 density band, absolute early τ4, o_q=2
local near-540 attractor) with explicit falsification command after fixed-band
RC2 death; not a replay of P1-P6.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_residual_rc3_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc3/offset_540_rc3_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc3/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows, or queue falsification
`5e8-6e8`. Keep RC3-RC5 as residual only; do not promote to theorem; do not
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
Builds on prior-hour Claim S1 only. Claim S2-A: under H1-H4 and D(r)≥2,
`1 ≤ first_τ4_offset < first_τ3_offset = D(r)` (early-τ=4 / late-τ=3 phase order).
Claim S2-B: under H1-H3, `D(r) < Band(r) = (r-s)(r+s)`; Target S1* fails at r
iff `D(r) ∈ Annulus(r) = {k : C_dyn(r) < k < Band(r)}`. Residual RC3-RC5
attached as audit only; RC2 retained falsified; d=4 SDA not revived.
`PROOF.md` §Square-Branch Reduction: proximity target remains UNRESOLVED.
One minimal falsification command: dynamic-cutoff search on `5e8-6e8`.

Result:
Constructive lemma subsection S2 written with hypotheses (H1-H4 reused),
unresolved Target S1*, residual claim table RC3-RC5, and explicit falsification
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
annulus object) with residual RC3-RC5 table and minimal falsification command
for Target S1* (`5e8-6e8` dynamic-cutoff search). Not a replay of S1.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r) ∉ Annulus(r)`; do not revive residue covers, fixed-540, or
d=4 SDA; do not promote RC3-RC5 to theorem status.

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
chamber separation - residual claims RC6-RC8 after RC3-RC5 surface.

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
prior chamber table from `experiments/square-branch-hourly-2026-07-10/`, and
RC3 table. Ran new probe
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_residual_rc6_probe.py`
evaluating P10-P12 (full o_q-panel S2-A phase order, late-dominant phase gap
≥0.95, o_q-stratified near-540 exclusivity). Did not replay RC3-RC5 as the
sole deliverable.

Result:
RC6 holds: S2-A phase order on 3/3 o_q branch maxima (o_q∈{2,4,6}).
RC7 holds: min phase_gap on util maxima + o_q panel = 0.967078 (o_q=4, D=486,
first_τ4=16) ≥ 0.95.
RC8 holds: only o_q=2 near 540 (|D-540|=2); o_q=4 escapes (|D-540|=54);
o_q=6 escapes (|D-540|=198). Strengthens RC5 to panel exclusivity residual.
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
New residual claim table RC6-RC8 (full o_q-panel S2-A phase order, late-dominant
phase-gap bound ≥0.95, o_q-stratified near-540 exclusivity) with explicit
falsification command; not a replay of RC3-RC5.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_residual_rc6_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc6/offset_540_rc6_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc6/FINDINGS.md`

Next step:
Run prefix τ probe variant on newest extremal rows, or queue falsification
`5e8-6e8`. Keep RC6-RC8 residual only; do not promote to theorem; do not
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
proved direct next-prime rule. Claim S3-A: `F(r) = q - r²` and `q - p = D(r) + F(r)`.
Claim S3-B: chamber-reset residual triple
`ResetResidual(r) = (D(r), F(r), first_τ4_offset)`; Target S1* fails iff
`D(r) ∈ Annulus(r)`. Claim S3-C: late-dominant phase residual
`phase_gap(r) = (D - first_τ4)/D` with `0 < phase_gap < 1`. Residual RC6-RC8
attached as audit only; RC2 retained falsified; d=4 SDA not revived.
`PROOF.md` §Square-Branch Reduction: proximity target remains UNRESOLVED.
One minimal falsification command: dynamic-cutoff search on `5e8-6e8`.

Result:
Constructive lemma subsection S3 written with hypotheses (H1-H4 reused + H5),
unresolved Target S1*, residual claim table RC6-RC8 attached, and explicit
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
RC6-RC8 table attachment and minimal falsification command for Target S1*
(`5e8-6e8` dynamic-cutoff search). Not a replay of S1 or S2.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r) ∉ Annulus(r)` via `ResetResidual(r)`; do not revive residue
covers, fixed-540, or d=4 SDA; do not promote RC6-RC8 to theorem status.

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
chamber separation - residual claims RC9-RC11 on the interior τ4 offset set.

Method:
Read falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived).
Built minimal probe
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_residual_rc9_probe.py`
recomputing the full τ4 offset set on 5 segment util maxima + 3 o_q branch-max
rows from the prior chamber table. Predictions P13-P15:

- P13/RC9: early-half τ4 mass ≥ 0.40
- P14/RC10: last_τ4 / D ≥ 0.95
- P15/RC11: max consecutive τ4 gap (lead+interior+trail) / D ≤ 0.10

Does not replay P1-P12 / RC3-RC8 as primary deliverable. Fixed-band RC2 retained
falsified. Prime-Square Proximity remains proved (`PROOF.md`); residual audit only.

Result:
All three new residuals hold on the surface through 4e8-5e8:

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
New residual claim table RC9-RC11 (early-half τ4 mass, late-span τ4 presence,
max inter-τ4 gap bound) with explicit falsification command on recomputed τ4
offset geometry; not a replay of RC6-RC8 or fixed-band 540.

Artifacts:
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_residual_rc9_probe.py`;
`experiments/square-branch-hourly-2026-07-10-rc9/offset_540_rc9_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-10-rc9/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8-6e8` or prefix-tau extremal rerun on newest rows.
Re-check RC9-RC11 on any new util maximum; do not revive fixed-band 540 or
d=4 SDA; do not promote RC9-RC11 to theorem status.

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
Builds on Claims S1-S3 only. Objects: ordered chamber prefix, full τ4 offset
set `Tau4(r)`, cover residual functionals
`(early_half_mass, late_span, max_gap_frac)`, extended reset residual
`ResetResidual⁺(r) = (D(r), F(r), first_τ4_offset, Cover(r))`. Hypotheses
H1-H5 reused; H6 adds nonempty interior τ4 field under H4. Target S1* left
UNRESOLVED per `PROOF.md` §Square-Branch Reduction. Residual table RC9-RC11
attached as audit only; RC2 remains falsified; d=4 SDA and fixed-540 not
revived. Minimal falsification command: dynamic-cutoff search on `5e8-6e8`;
optional RC9 cover-panel probe.

Result:
Constructive lemma subsection S4 written with hypotheses H6, Claims S4-A/B/C,
status separation update, residual cover table on the 4e8-5e8 o_q branch-max
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
functionals, extended `ResetResidual⁺`) with residual claim table RC9-RC11 and
minimal falsification command for Target S1* (`5e8-6e8` dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C; re-check RC9-RC11 on any
new util maximum; do not promote Cover residuals or RC9-RC11 to theorem status.

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
late-tau=3 chamber separation - next residual after RC9-RC11.

Method:
Read latest falsification summary
`square_branch_dynamic_cutoff_search_4e8_5e8/..._summary.json` and
`prefix_tau_floor_probe.json` (SDA-invalidation note only). Produced residual
claim table RC12-RC14 with minimal probe under
`experiments/square-branch-hourly-2026-07-11-rc12/`. Did not port d=4 SDA.
Did not restate RC9-RC11 as the sole deliverable.

Objects: ordered chamber prefix before selected square `w=r^2`; divisor-count
field `tau`; offset `D(r)`; Tau4 offset set; first-quarter / last-quarter mass
and median location of Tau4.

Result:
RC12 first-quarter τ4 mass ≥ 0.15: **holds** (min 0.1833 on 2e8-3e8 util max).
RC13 last-quarter τ4 mass ≥ 0.15: **holds** (min 0.2000 on o_q=2 branch max).
RC14 median τ4 / D ∈ [0.40, 0.65]: **holds** (observed [0.448, 0.572]).
RC2 fixed near-540 band: retained **falsified**.
RC9-RC11: retained holds (not primary surface).
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
New residual claim table RC12-RC14 (first-quarter τ4 mass, last-quarter τ4 mass,
median mid-band) with explicit falsification command on util maxima + o_q panel
through 4e8-5e8.

Artifacts:
`experiments/square-branch-hourly-2026-07-11-rc12/offset_540_residual_rc12_probe.py`;
`experiments/square-branch-hourly-2026-07-11-rc12/offset_540_rc12_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-11-rc12/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8-6e8`, or re-check RC12-RC14 on any new util / o_q
branch maximum. Do not promote RC12-RC14 to theorem status.

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
Builds on Claims S1-S4 only. Objects: ordered interior τ4 field `Tau4(r)`,
chamber quarter cuts `Q1=⌊D/4⌋`, `Q3=⌊3D/4⌋`, outer-early / mid / outer-late
zones, quartile-balance functionals
`(first_quarter_mass, last_quarter_mass, median_frac)`, balanced extended
reset residual
`ResetResidual^Q(r) = (D(r), F(r), first_τ4_offset, Cover(r), QuartileBalance(r))`.
Hypotheses H1-H6 reused; no new hypothesis. Target S1* left UNRESOLVED per
`PROOF.md` §Square-Branch Reduction. Residual table RC12-RC14 attached as
audit only (from prior hour probe; not re-proved as theorem). RC2 remains
falsified; d=4 SDA and fixed-540 not revived. Minimal falsification command:
dynamic-cutoff search on `5e8-6e8`; optional RC12 quartile probe.

Result:
Constructive lemma subsection S5 written with Claims S5-A/B/C, status
separation update, residual quartile table on the 4e8-5e8 o_q branch-max
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
residuals, balanced `ResetResidual^Q`) with residual claim table RC12-RC14
attached and minimal falsification command for Target S1* (`5e8-6e8`
dynamic-cutoff search).

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C, S5-C; re-check RC9-RC14
on any new util maximum; do not promote QuartileBalance or RC12-RC14 to theorem
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
Builds on Claims S1-S5 only. Objects: ordered field `Tau4(r)`, last-τ4 marker
`last_τ4_offset = max Tau4(r)`, late trail `trail_gap(r) = D(r) - last_τ4_offset`,
dual early/late marker pair `Dual(r) = (first_τ4_offset, trail_gap(r))`, and
trail-extended chamber-reset residual
`ResetResidual^T(r) = (D(r), F(r), first_τ4_offset, Cover(r), QuartileBalance(r), Trail(r))`
with `Trail(r) = (last_τ4_offset, trail_gap(r), Dual(r))`. Hypotheses H1-H6
reused; no new hypothesis. Target S1* left UNRESOLVED per `PROOF.md`
§Square-Branch Reduction. Residual table RC15-RC17 attached as audit only
(from prior hour probe; not promoted to theorem). RC2 remains falsified;
d=4 SDA and fixed-540 not revived. Minimal falsification command:
dynamic-cutoff search on `5e8-6e8`; optional RC15 dual-marker probe.

Result:
Constructive lemma subsection S6 written with Claims S6-A/B/C, residual claim
table update (S6-A/B/C + RC15-RC17), status separation update, dual-marker
panel on the 4e8-5e8 o_q branch-max rows, and explicit falsification commands.
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
RC15-RC17 attached and minimal falsification command for Target S1*
(`5e8-6e8` dynamic-cutoff search). Not a prose restatement of S5 or of the
RC15 probe alone.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C, S5-C, S6-C; re-check
RC9-RC17 on any new util maximum; do not promote Trail/Dual or RC15-RC17 to
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
late-tau=3 chamber separation (Dual L1 and tau4 span residuals RC18-RC20).

Method:
Read falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`.
Built minimal probe under `experiments/square-branch-hourly-2026-07-11-rc18/`
recomputing Dual(r)=(first_τ4, trail_gap) on segment utilization maxima through
4e8-5e8 and the full o_q∈{2,4,6} branch-max panel. New residual claims (not a
restatement of RC15-RC17 componentwise bounds):
- P22/RC18: Dual L1 = first_τ4 + trail_gap ≤ 24
- P23/RC19: (last_τ4 - first_τ4)/(D-1) ≥ 0.95
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
- util max 4e8-5e8 still D=738 (RC2 falsified)
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
New residual claim table RC18-RC20 (Dual L1 envelope, tau4 support span
fraction, relative Dual L1) with explicit falsification command; not a prose
restatement of RC15-RC17.

Artifacts:
`experiments/square-branch-hourly-2026-07-11-rc18/offset_540_residual_rc18_probe.py`;
`experiments/square-branch-hourly-2026-07-11-rc18/offset_540_rc18_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-11-rc18/FINDINGS.md`;
`research/04-bounded-compression/docs/square_branch_hourly.md`

Next step:
Queue falsification `5e8-6e8` (or re-check RC15-RC20 on any new util maximum).
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
chamber separation - residual claims RC21-RC23 after Dual L1 surface (RC18-RC20).

Method:
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json` (SDA-invalidation note; d=4 SDA not revived),
prior chamber table from `experiments/square-branch-hourly-2026-07-10/`, and
RC18 Dual L1 table. Ran new probe
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_residual_rc21_probe.py`
evaluating P25-P27 (τ4 density envelope, Dual max-component share, near-540
Dual L1 floor). Did not restate P22-P24 as the sole deliverable.

Result:
RC21 holds: τ4 density dens = tau4_count/(D-1) ∈ [0.10, 0.135] on 8/8 rows
(range `[0.1093, 0.1303]`).
RC22 holds: Dual max-component share max(first, trail)/L1 ≤ 0.85 on 8/8
(range `[0.50, 0.833]`).
RC23 holds (conditional): if |D-540|≤20 then Dual L1 ≥ 14 on 4/4 near-540 rows
(near L1 range `[14, 24]`); escape util-max D=738 remains outside near-540.
RC2 retained falsified (D=738). RC18-RC20 retained holds (not primary surface).
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
New residual claim table RC21-RC23 (τ4 density envelope, Dual max-component
share, near-540 Dual L1 floor) with explicit falsification command; all three
hold on util maxima through 4e8-5e8 + o_q panel. Not a replay of RC18-RC20.
Theorem-status continuity corrected to PROOF.md (proximity unresolved).

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_residual_rc21_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc21/offset_540_rc21_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc21/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md`

Next step:
Queue falsification `5e8-6e8` and re-check RC21-RC23 on any new util maximum.
Keep RC21-RC23 residual only; do not promote to theorem; do not revive
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

## 2026-07-13T03:08:22Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S7 Dual L1 residual, τ4 density, dual-balance residual).

Method:
PGS-first constructive draft under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Builds on Claims S1-S6 only. Objects: Dual L1
`L1(r) = first_τ4_offset + trail_gap(r)`, relative Dual L1 `L1_rel(r) = L1/D`,
support span fraction `span_frac(r)`, τ4 density
`dens(r) = |Tau4(r)|/(D-1)`, Dual max-component share
`max_share(r) = max(first_τ4, trail_gap)/L1`, dual-balance package
`DualBalance(r)`, dual-balance extended residual
`ResetResidual^D(r)`. Hypotheses H1-H6 reused; no new hypothesis. Target S1*
left UNRESOLVED per `PROOF.md` §Square-Branch Reduction. Residual table
RC18-RC23 attached as audit only (from prior RC18 Dual L1 and RC21 density/share
probes; not re-proved as theorem). RC2 remains falsified; d=4 SDA and fixed-540
not revived. Minimal falsification command: dynamic-cutoff search on `5e8-6e8`;
optional RC18/RC21 residual probes.

Result:
Constructive lemma subsection S7 written with Claims S7-A/B/C, status
separation update, residual Dual-balance table on the 4e8-5e8 o_q branch-max
panel, and explicit falsification commands. No new measured regime this hour.
Theorem: prime-square proximity remains UNRESOLVED in `PROOF.md`; direct
next-prime and Interior Maximizer remain proved.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.33s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S7 (Dual L1 residual, τ4 density, Dual
max-component share, dual-balance `ResetResidual^D`) with residual claim table
RC18-RC23 attached and minimal falsification command for Target S1* (`5e8-6e8`
dynamic-cutoff search). Not a prose restatement of S6; DualBalance is a new
named residual package.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/04-bounded-compression/docs/square_branch_hourly.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (re-aligned to PROOF.md: proximity OPEN/UNRESOLVED);
`experiments/square-branch-hourly-2026-07-11-rc18/` (attached residual surface);
`experiments/square-branch-hourly-2026-07-13-rc21/` (attached residual surface)

Next step:
Return to falsification queue on `5e8-6e8` (or H_CTC square-branch probe). Keep
pressure on `D(r)` under Claims S1, S2-B, S3-B, S4-C, S5-C, S6-C, S7-C; re-check
RC9-RC23 / DualBalance on any new util maximum; do not promote DualBalance or
RC18-RC23 to theorem status.

## 2026-07-13T04:06:34Z run

Mechanism:
Walk every prime root `r` in the already-measured band 400M-500M. For each
selected prime square `w = r^2`, measure the backward distance `D(r) = r^2 - p`
to the previous prime `p`, and compare `D(r)` to the dynamic cutoff
`C = max(64, ceil(0.5 * log(r^2)^2))`. Report utilization `D/C` and any first
counterexample (`D > C`).

Method:
deterministic dispatch (replay of certified band):
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001 --max-prime 500000000 --output-dir research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8`

Result:
Command exit code: 0. Same scientific signature as the already-recorded
`4e8-5e8` surface (no new regime).

```
square-branch-dynamic-cutoff-search: primes=5019541 first_counterexample=none max_utilization=0.9341772151898734 max_p=424171123
```

| Field | Value |
| --- | --- |
| Prime roots tested | 5,019,541 |
| First counterexample | none |
| Max utilization | 0.9341772151898734 |
| Extremal root `r` | 424,171,123 |
| Offset `D(r)` | 738 |
| `o_q` at max row | 6 |
| Dynamic cutoff at max row | 790 |
| Elapsed seconds | 82.91 |

pytest exit code: 0 (4 passed in 2.36s).

Theorem boundary: prime-square proximity remains UNRESOLVED in `PROOF.md`
section Square-Branch Reduction. This band is audit corroboration only. Direct
next-prime and Interior Maximizer remain proved. RC2 (fixed near-540 as a law
on util maxima) stays falsified by `D=738`.

Research status:
NO_DELTA

Ops status:
OK

Delta:
Replay of certified `4e8-5e8` dynamic-cutoff surface. Signature matches prior
measured band (max util 0.934..., `r=424171123`, `D=738`, first_counterexample=none).
Per contract, replay is NO_DELTA, not ADVANCE.

Artifacts:
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`;
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_frontier.csv`

Next step:
Offset-540 structural audit on the recurring chamber geometry (queue item
`offset-540-structural-audit`). Honest next falsification band is `5e8-6e8`,
not another `4e8-5e8` replay.

## 2026-07-13T05:07:20Z run

Mechanism:
On each extremal chamber before a selected prime square `w = r^2`, mark the
first and last early composite-semiprime offsets with `tau = 4`, the late
`tau = 3` square endpoint at offset `D(r)`, and the Dual trail gap after the
last `tau = 4`. From those plain marks, form three residual quantities: mean
spacing of `tau = 4` hits, signed early/late Dual imbalance, and the fraction
of chamber length that is open after the first `tau = 4`. Project terms:
RC24 mean inter-hit gap, RC25 Dual signed imbalance, RC26 chamber open fraction.

Method:
PGS-native residual probe (no d=4 SDA port). Read
`square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json`, prior chamber table
`experiments/square-branch-hourly-2026-07-10/`, and RC21 density/share table.
Ran new probe
`experiments/square-branch-hourly-2026-07-13-rc24/offset_540_residual_rc24_probe.py`
evaluating P28-P30 on segment util maxima through `4e8-5e8` plus the full
`o_q in {2,4,6}` branch-max panel (8 rows). Did not restate P25-P27 as the sole
deliverable.

Result:
| Claim | Bound | Observed | Rows |
| --- | --- | --- | --- |
| RC24 / P28 mean gap | `[7.0, 10.0]` | `[7.653, 8.980]` | 8/8 hold |
| RC25 / P29 signed Dual | `[-0.55, 0.70]` | `[-0.455, 0.667]` | 8/8 hold |
| RC26 / P30 open fraction | `>= 0.96` | `[0.9671, 0.9959]` | 8/8 hold |

RC2 retained falsified (`r=424171123`, `D=738`). RC21-RC23 retained holds (not
primary surface this hour). Theorem: prime-square proximity remains UNRESOLVED
in `PROOF.md` section Square-Branch Reduction; direct next-prime and Interior
Maximizer remain proved. Residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.43s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC24-RC26 (Tau4 mean inter-hit gap
envelope, Dual signed imbalance, chamber open fraction) with explicit
falsification command; all three hold on util maxima through `4e8-5e8` + `o_q`
panel. Not a replay of RC21-RC23 density/share/near-540 floor.

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc24/offset_540_residual_rc24_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc24/offset_540_rc24_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc24/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (theorem-status continuity: proximity OPEN/UNRESOLVED)

Next step:
Queue falsification `5e8-6e8` and re-check RC24-RC26 (and RC18-RC23) on any
new util maximum. Keep RC24-RC26 residual only; do not promote to theorem; do
not revive fixed-band 540 or d=4 SDA.


## 2026-07-13T06:05:10Z run

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
4 passed in 2.40s
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

## 2026-07-13T07:07:06Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (S8: Tau4 mean inter-hit gap, Dual signed imbalance,
chamber open fraction; SpacingBalance extended reset residual).

Method:
PGS-native constructive lemma draft only. Appended Subsection S8 to
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`
with hypotheses H1-H6 reused, Claims S8-A / S8-B / S8-C, residual claim table
RC24-RC26 attached as audit, and explicit falsification commands for Target S1*
(`5e8-6e8` dynamic-cutoff search) and RC24-RC26 panel recheck. Corrected
`ACTIVE_TARGET.md` theorem-status continuity so prime-square proximity is
OPEN/UNRESOLVED under `PROOF.md` §Square-Branch Reduction (removed false
CLOSED/PROVED bootstrap). No classical inference gate. No SDA or fixed-cutoff
revival.

Result:
Constructive lemma subsection S8 written. Residual audit table RC24-RC26 held
on prior measured surface (util maxima through `4e8-5e8` + o_q panel, 8/8):

| Claim | Bound | Observed | Rows |
| --- | --- | --- | --- |
| RC24 mean_gap | `[7.0, 10.0]` | `[7.653, 8.980]` | 8/8 hold |
| RC25 signed Dual | `[-0.55, 0.70]` | `[-0.455, 0.667]` | 8/8 hold |
| RC26 open_frac | `>= 0.96` | `[0.9671, 0.9959]` | 8/8 hold |

RC2 retained falsified (`r=424171123`, `D=738`). Theorem: prime-square
proximity remains UNRESOLVED in `PROOF.md` §Square-Branch Reduction; direct
next-prime and Interior Maximizer remain proved. S8 does not close Target S1*.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.44s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S8 (mean inter-hit gap, Dual signed imbalance,
chamber open fraction; `SpacingBalance` / `ResetResidual^S`) with residual claim
table RC24-RC26 and explicit falsification commands. Continuity fix: ACTIVE_TARGET
now matches PROOF.md (proximity OPEN/UNRESOLVED). Not a replay of S1-S7 and not
a measured new regime.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/00-index/continuity/ACTIVE_TARGET.md`;
`experiments/square-branch-hourly-2026-07-13-rc24/offset_540_residual_rc24_probe.py` (falsification command for RC24-RC26)

Next step:
Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe. Re-check
RC24-RC26 / SpacingBalance on any new util maximum. Keep S8 residual only; do not
promote mean gap, signed Dual, or open fraction to theorem; do not revive fixed
band 540 or d=4 SDA.

## 2026-07-13T08:06:33Z run

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
elapsed_seconds: 83.65388488769531

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.37s
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

## 2026-07-13T09:08:06Z run

Mechanism:
On each extremal chamber before a selected prime square `w = r^2`, mark the
ordered offsets with `tau = 4`, the late `tau = 3` square endpoint at offset
`D(r)`, and the successive gaps between consecutive `tau = 4` hits. From those
plain marks, form three residual quantities: peak successive gap over mean gap,
coefficient of variation of successive gaps, and Dual isolation measured in
mean-gap units. Project terms: RC27 max/mean ratio, RC28 gap CV envelope,
RC29 Dual L1 / mean_gap.

Method:
PGS-native residual probe (no d=4 SDA port). Read
`square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json`, prior chamber table
`experiments/square-branch-hourly-2026-07-10/`, and RC24 table.
Ran new probe
`experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py`
evaluating P31-P33 on segment util maxima through `4e8-5e8` plus full
`o_q in {2,4,6}` branch-max panel (8 rows; 7 unique chambers). Did not
restate RC24-RC26 as the sole deliverable. Continuity: `ACTIVE_TARGET.md`
restored to `PROOF.md` §Square-Branch Reduction (proximity OPEN/UNRESOLVED;
residual package through RC29).

Result:
| Claim | Bound | Observed | Rows |
| --- | --- | --- | --- |
| RC27 / P31 max/mean | `<= 5.5` | `[2.605, 5.012]` | 8/8 hold |
| RC28 / P32 gap CV | `[0.55, 1.0]` | `[0.663, 0.891]` | 8/8 hold |
| RC29 / P33 Dual/mean | `[0.30, 3.0]` | `[0.445, 2.744]` | 8/8 hold |

RC2 retained falsified (`r=424171123`, `D=738`). RC24-RC26 retained holds
(not primary surface this hour). Theorem: prime-square proximity remains
UNRESOLVED in `PROOF.md` §Square-Branch Reduction; direct next-prime and
Interior Maximizer remain proved. Residual audit only. Invalidated d=4 SDA
not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.40s
```

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC27-RC29 (Tau4 successive max/mean
ratio, successive gap CV envelope, Dual isolation in mean-gap units) with
explicit falsification command; all three hold on util maxima through
`4e8-5e8` + `o_q` panel. Continuity fix: ACTIVE_TARGET matches PROOF.md
(proximity OPEN/UNRESOLVED). Not a replay of RC24-RC26 mean-gap / signed
imbalance / open fraction.

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc27/offset_540_rc27_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc27/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (theorem-status continuity restored: proximity OPEN/UNRESOLVED; residual package through RC29)

Next step:
Queue falsification `5e8-6e8` and re-check RC27-RC29 (and RC18-RC26) on any
new util maximum. Keep RC27-RC29 residual only; do not promote max/mean, CV,
or Dual/mean to theorem; do not revive fixed-band 540 or d=4 SDA.

## 2026-07-13T10:05:10Z run

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
4 passed in 2.40s
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

## 2026-07-13T11:05:06Z run

Mechanism:
On each selected-square chamber, form the ordered list of successive gaps between
consecutive interior `tau = 4` hits. From that plain gap list, name three residual
quantities beyond mean spacing: the peak successive gap over the mean gap, the
coefficient of variation of the successive-gap list, and Dual L1 isolation
measured in mean-gap units. Project terms: Claims S9-A/B/C, `GapRegularity(r)`,
`ResetResidual^G(r)`, residual audit RC27-RC29.

Method:
PGS-native constructive lemma draft only (job `chamber-reset-lemma-draft`).
Appended Subsection S9 to
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`
with hypotheses H1-H6 reused, Claims S9-A / S9-B / S9-C, residual claim table
RC27-RC29 attached as audit from
`experiments/square-branch-hourly-2026-07-13-rc27/`, and explicit falsification
commands for Target S1* (`5e8-6e8` dynamic-cutoff search) and RC27-RC29 panel
recheck. Corrected `ACTIVE_TARGET.md` theorem-status continuity so prime-square
proximity is OPEN/UNRESOLVED under `PROOF.md` §Square-Branch Reduction (removed
false CLOSED/PROVED bootstrap). No classical inference gate. No SDA or fixed-cutoff
revival. Not a prose restatement of S8 alone: successive-gap list, max/mean, CV,
and Dual-over-mean are new constructive objects relative to `SpacingBalance`.

Result:
Constructive lemma subsection S9 written. Residual audit table RC27-RC29 held
on prior measured surface (util maxima through `4e8-5e8` + o_q panel, 8/8):

| Claim | Bound | Observed | Rows |
| --- | --- | --- | --- |
| RC27 / P31 max/mean | `<= 5.5` | `[2.605, 5.012]` | 8/8 hold |
| RC28 / P32 gap CV | `[0.55, 1.0]` | `[0.663, 0.891]` | 8/8 hold |
| RC29 / P33 Dual/mean | `[0.30, 3.0]` | `[0.445, 2.744]` | 8/8 hold |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | max_over_mean | gap_cv | dual_over_mean |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 5.012 | 0.891 | 2.734 |
| 4 | 482342527 | 486 | 2.914 | 0.785 | 2.466 |
| 6 | 424171123 | 738 | 3.920 | 0.811 | 1.437 |

RC2 retained falsified (`r=424171123`, `D=738`). Theorem: prime-square
proximity remains UNRESOLVED in `PROOF.md` §Square-Branch Reduction; direct
next-prime and Interior Maximizer remain proved. S9 does not close Target S1*.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.52s
```
RC27 residual probe exit code: 0 (RC27-RC29 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S9 (successive Tau4 gaps, max/mean ratio, gap
CV, Dual isolation in mean-gap units; `GapRegularity` / `ResetResidual^G`) with
residual claim table RC27-RC29 attached and explicit falsification commands.
Continuity fix: ACTIVE_TARGET rewritten to match PROOF.md (proximity
OPEN/UNRESOLVED; false CLOSED/PROVED bootstrap removed). Not a replay of S8
mean-gap / signed Dual / open fraction and not a new measured regime.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/00-index/continuity/ACTIVE_TARGET.md`;
`experiments/square-branch-hourly-2026-07-13-s9/FINDINGS.md`;
`experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py` (falsification command for RC27-RC29);
`experiments/square-branch-hourly-2026-07-13-rc27/offset_540_rc27_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc27/FINDINGS.md`

Next step:
Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe. Re-check
RC27-RC29 / GapRegularity on any new util maximum. Keep S9 residual only; do not
promote max/mean, CV, or Dual/mean to theorem; do not revive fixed band 540 or
d=4 SDA.

## 2026-07-13T12:06:32Z run

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
elapsed_seconds: 83.02018713951111

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.25s
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

## 2026-07-13T13:31:24Z run

Mechanism:
On each extremal chamber before a selected prime square `w = r^2`, mark the
ordered offsets with `tau = 4`, the late `tau = 3` square endpoint at offset
`D(r)`, and the successive gaps between consecutive `tau = 4` hits. From those
plain marks, form three residual quantities beyond peak ratio and CV: the median
successive gap over the mean gap, the fraction of successive gaps at most the
mean, and the share of Tau4 hits in the first half of the Tau4 body
`[first_tau4, last_tau4]`. Project terms: RC30 median/mean, RC31 sub-mean
majority, RC32 body early-mass balance.

Method:
PGS-native residual probe (no d=4 SDA port). Job `offset-540-structural-audit`.
Read `square_branch_dynamic_cutoff_search_4e8_5e8` summary JSON,
`prefix_tau_floor_probe.json`, prior chamber table
`experiments/square-branch-hourly-2026-07-10/`, and RC27 table.
Ran new probe
`experiments/square-branch-hourly-2026-07-13-rc30/offset_540_residual_rc30_probe.py`
evaluating P34-P36 on segment util maxima through `4e8-5e8` plus full
`o_q in {2,4,6}` branch-max panel (8 evaluation rows; 7 unique chambers). Did
not restate RC27-RC29 as the sole deliverable. Continuity: `ACTIVE_TARGET.md`
aligned with `PROOF.md` §Square-Branch Reduction (proximity OPEN/UNRESOLVED;
residual package through RC32).

Result:
| Claim | Bound | Observed | Rows |
| --- | --- | --- | --- |
| RC30 / P34 med/mean | `[0.65, 0.95]` | `[0.683, 0.891]` | 8/8 hold |
| RC31 / P35 frac <= mean | `>= 0.50` | `[0.549, 0.677]` | 8/8 hold |
| RC32 / P36 early body mass | `[0.40, 0.55]` | `[0.415, 0.538]` | 8/8 hold |

Branch-max panel (`F(r)` = o_q):

| o_q | r | D | med/mean | frac_le_mean | early_body_frac |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.683 | 0.644 | 0.500 |
| 4 | 482342527 | 486 | 0.784 | 0.577 | 0.415 |
| 6 | 424171123 | 738 | 0.784 | 0.632 | 0.469 |

RC2 retained falsified (`r=424171123`, `D=738`). RC27-RC29 retained holds
(not primary surface this hour). Theorem: prime-square proximity remains
UNRESOLVED in `PROOF.md` §Square-Branch Reduction; direct next-prime and
Interior Maximizer remain proved. Residual audit only. Invalidated d=4 SDA
not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.35s
```
RC30 residual probe exit code: 0 (RC30-RC32 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC30-RC32 (Tau4 successive median/mean
ratio, sub-mean successive gap majority, Tau4 body early-mass balance) with
explicit falsification command; all three hold on util maxima through
`4e8-5e8` + `o_q` panel. Continuity: ACTIVE_TARGET residual package through
RC32; proximity remains OPEN/UNRESOLVED. Not a replay of RC27-RC29 max/mean,
gap CV, or Dual/mean.

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc30/offset_540_residual_rc30_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc30/offset_540_rc30_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc30/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (residual package through RC32; proximity OPEN/UNRESOLVED)

Next step:
Queue falsification `5e8-6e8` and re-check RC30-RC32 (and RC18-RC29) on any
new util maximum. Keep RC30-RC32 residual only; do not promote median/mean,
sub-mean majority, or body early-mass to theorem; do not revive fixed-band 540
or d=4 SDA.

## 2026-07-13T14:05:10Z run

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
4 passed in 2.27s
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

## 2026-07-13T15:07:59Z run

Mechanism:
Draft one constructive subsection of the Chamber-Reset Endpoint Resolution
Lemma on the selected-square branch: successive median/mean central shape,
sub-mean successive-gap majority, and Tau4 body early-mass balance, then
extend the chamber-reset residual by that shape package. Project terms:
Claims S10-A / S10-B / S10-C, `GapShape(r)`, `ResetResidual^S(r)`, residual
RC30-RC32 (audit only).

Method:
Job `chamber-reset-lemma-draft`. PGS-native constructive draft only (no d=4
SDA port, no classical inference gate). Extended
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`
with Subsection S10. Attached residual table RC30-RC32 from prior measured
surface (util maxima through 4e8-5e8 + o_q panel). Continuity:
`ACTIVE_TARGET.md` rewritten to OPEN/UNRESOLVED matching `PROOF.md`
§Square-Branch Reduction (false CLOSED/PROVED bootstrap removed again after
prefix-tau clobber). Companion FINDINGS under
`experiments/square-branch-hourly-2026-07-13-s10/`.

Result:
| Claim | Role | Status |
| --- | --- | --- |
| S10-A | successive median_gap and median_over_mean | constructive |
| S10-B | frac_le_mean and early_body_frac on Dual body | constructive |
| S10-C | GapShape package; ResetResidual^S | constructive residual-state |
| RC30 | 0.65 <= med/mean <= 0.95 | holds audit; range [0.683, 0.891] |
| RC31 | frac_le_mean >= 0.50 | holds audit; range [0.549, 0.677] |
| RC32 | 0.40 <= early_body_frac <= 0.55 | holds audit; range [0.415, 0.538] |
| RC2 | fixed band [528, 552] as law | retained falsified (D=738) |

Branch-max panel (F(r) = o_q):

| o_q | r | D | med/mean | frac_le_mean | early_body_frac |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.683 | 0.644 | 0.500 |
| 4 | 482342527 | 486 | 0.784 | 0.577 | 0.415 |
| 6 | 424171123 | 738 | 0.784 | 0.632 | 0.469 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Residual and constructive draft only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.30s
```
RC30 residual probe exit code: 0 (RC30-RC32 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S10 (median/mean central shape, sub-mean
successive-gap majority, Tau4 body early-mass; `GapShape` / `ResetResidual^S`)
with residual claim table RC30-RC32 attached and explicit falsification
commands. Continuity fix: ACTIVE_TARGET rewritten to match PROOF.md
(proximity OPEN/UNRESOLVED; false CLOSED/PROVED bootstrap removed). Not a
replay of S9 max/mean / CV / Dual-over-mean and not a new measured regime.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`;
`research/00-index/continuity/ACTIVE_TARGET.md`;
`experiments/square-branch-hourly-2026-07-13-s10/FINDINGS.md`;
`experiments/square-branch-hourly-2026-07-13-rc30/offset_540_residual_rc30_probe.py` (falsification command for RC30-RC32)

Next step:
Return to falsification queue on `5e8-6e8`, or H_CTC square-branch probe.
Re-check RC30-RC32 / GapShape on any new util maximum. Keep S10 residual only;
do not promote median/mean, sub-mean majority, or body early-mass to theorem;
do not revive fixed band 540 or d=4 SDA.

## 2026-07-13T16:06:31Z run

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
elapsed_seconds: 81.79909491539001

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.31s
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

## 2026-07-13T17:08:01Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation: successive gap IQR/median robust scale,
trail closing isolation in mean-gap units, and Tau4 body last-quartile mass.
Project terms: residual claims RC33-RC35 / predictions P37-P39.

Method:
Job `offset-540-structural-audit`. Read latest falsification summary
`square_branch_dynamic_cutoff_search_4e8_5e8` and `prefix_tau_floor_probe.json`.
New probe under `experiments/square-branch-hourly-2026-07-13-rc33/`.
PGS-native Dual markers and Tau4 successive gaps only (no d=4 SDA port,
no classical inference gate). Continuity: ACTIVE_TARGET residual package
through RC35; proximity remains OPEN/UNRESOLVED per PROOF.md.

Result:
| Claim | Bound | Observed | Status |
| --- | --- | --- | --- |
| RC33 / P37 IQR/median | 0.70 <= IQR/med <= 1.55 | [0.833, 1.417] | holds |
| RC34 / P38 trail/mean | 0.15 <= trail/mean <= 2.50 | [0.223, 2.278] | holds |
| RC35 / P39 body last-Q | 0.18 <= last_Q <= 0.35 | [0.233, 0.297] | holds |
| RC2 fixed band [528, 552] | law on util maxima | D=738 | retained falsified |

Branch-max panel (F(r) = o_q):

| o_q | r | D | trail | IQR/med | trail/mean | last_Q |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 20 | 1.333 | 2.278 | 0.233 |
| 4 | 482342527 | 486 | 6 | 1.357 | 0.672 | 0.283 |
| 6 | 424171123 | 738 | 8 | 1.167 | 1.045 | 0.240 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.47s
```
RC33 residual probe exit code: 0 (RC33-RC35 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC33-RC35 (Tau4 successive IQR/median
robust scale, trail/mean closing isolation, Tau4 body last-quartile mass)
with explicit falsification command; all three hold on util maxima through
`4e8-5e8` + `o_q` panel. Continuity: ACTIVE_TARGET residual package through
RC35; proximity remains OPEN/UNRESOLVED. Not a replay of RC30-RC32 median/mean,
sub-mean majority, or body early-mass.

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc33/offset_540_residual_rc33_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc33/offset_540_rc33_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc33/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (residual package through RC35; proximity OPEN/UNRESOLVED)

Next step:
Queue falsification `5e8-6e8` and re-check RC33-RC35 (and RC18-RC32) on any
new util maximum. Keep RC33-RC35 residual only; do not promote IQR/median,
trail/mean, or body last-quartile mass to theorem; do not revive fixed-band
540 or d=4 SDA.

## Auditor errata 2026-07-13 (ledger reclassification)

Mechanism:
Two prior hourly blocks carried dispatcher label ADVANCE on replay
surfaces. This errata records the honest research label without rewriting
the original blocks (dual labels retained).

Method:
Auditor pressure on `square_branch_hourly.md` entries
`2026-07-13T14:05:10Z` (prefix-tau re-run) and `2026-07-13T16:06:31Z`
(4e8-5e8 dynamic-cutoff sweep). Contract: same scientific signature or
certified-regime replay is NO_DELTA, not ADVANCE. Main hour deliverable
RC33-RC35 remains at `e38cfd70` and is not reclassified here.

Result:

| Timestamp | Surface | Ledger label (kept) | Honest label | Reason |
| --- | --- | --- | --- | --- |
| 2026-07-13T14:05:10Z | prefix-tau re-run on latest extremal rows | ADVANCE | NO_DELTA | Re-run; same boolean payload (`d4_tau5` / `tau4_sda` false); no new residual claim or regime |
| 2026-07-13T16:06:31Z | dynamic-cutoff `4e8-5e8` | ADVANCE | NO_DELTA | Replay of certified band (max util 0.934..., `r=424171123`, `D=738`, first_counterexample=none) |

No theorem claim. Prime-square proximity / Target S1* remains UNRESOLVED in
`PROOF.md` section Square-Branch Reduction. Direct next-prime and Interior
Maximizer remain proved. Invalidated d=4 SDA not revived.

Research status:
NO_DELTA

Ops status:
OK

Delta:
Errata only: reclassify the two timestamps above ADVANCE -> honest NO_DELTA.
Original blocks keep their written ADVANCE labels (dual labels). Does not
touch RC33-RC35 ADVANCE at `e38cfd70`.

Artifacts:
`research/04-bounded-compression/docs/square_branch_hourly.md` (this block)

Next step:
Honest next falsification band remains `5e8-6e8`. Re-check residual package
through RC35 on any new util maximum. Do not re-sweep `4e8-5e8` as ADVANCE.

## 2026-07-13T18:05:11Z run

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
4 passed in 2.35s
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

## 2026-07-13T19:07:20Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (job `chamber-reset-lemma-draft`).

Method:
Constructive subsection S11 under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
PGS-native objects only: ordered chamber prefix, divisor-count field, Tau4
successive gaps, Dual trail marker, Dual body support. No classical inference
gate. No d=4 SDA port. No theorem inflation. Continuity: residual package
through RC35 attached as audit only; Target S1* remains UNRESOLVED per PROOF.md
§Square-Branch Reduction.

Result:
| Claim | Content | Status |
| --- | --- | --- |
| S11-A | IQR / median successive-gap robust scale | constructive |
| S11-B | trail/mean closing isolation; body last-quartile mass | constructive |
| S11-C | RobustScale + ResetResidual^R chamber-reset residual | constructive |
| RC33 | 0.70 <= IQR/med <= 1.55; observed [0.833, 1.417] | holds (audit) |
| RC34 | 0.15 <= trail/mean <= 2.50; observed [0.223, 2.278] | holds (audit) |
| RC35 | 0.18 <= last_Q <= 0.35; observed [0.233, 0.297] | holds (audit) |
| RC2 | fixed band [528, 552] law on util maxima | retained falsified |
| S1* | D(r) <= max(64, ceil(0.5*log(r^2)^2)) | UNRESOLVED |

Branch-max panel (F(r)=o_q):

| o_q | r | D | IQR/med | trail/mean | last_Q |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 1.333 | 2.278 | 0.233 |
| 4 | 482342527 | 486 | 1.357 | 0.672 | 0.283 |
| 6 | 424171123 | 738 | 1.167 | 1.045 | 0.240 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.36s
```
RC33 residual probe exit code: 0 (RC33-RC35 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S11 (Claims S11-A/S11-B/S11-C) with
explicit falsification commands: RobustScale residual package formalizing
IQR/median, trail/mean closing isolation, and Tau4 body last-quartile mass
into ResetResidual^R; attaches measured RC33-RC35 as audit only. Not a replay
of S10 median/mean / sub-mean majority / body early-mass, and not a proof of
S1*.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html` (S11);
`experiments/square-branch-hourly-2026-07-13-s11/FINDINGS.md`;
`experiments/square-branch-hourly-2026-07-13-rc33/` (falsification residual panel)

Next step:
Return to falsification queue on `5e8-6e8` or H_CTC square-branch probe.
Re-check RC33-RC35 / RobustScale on any new util maximum. Keep S11 residual
only; do not promote IQR/median, trail/mean, or body last-quartile mass to
theorem; do not revive fixed-band 540 or d=4 SDA.

## 2026-07-13T20:06:32Z run

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
elapsed_seconds: 81.46313810348511

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.31s
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

## 2026-07-13T21:05:06Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation (queue job `offset-540-structural-audit`).

Method:
Read latest falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`.
Built residual claim package RC36-RC38 under
`experiments/square-branch-hourly-2026-07-13-rc36/` with explicit
falsification probe. Did not port d=4 SDA. RC2 fixed-band remains falsified.

Result:

| Claim | Bound | Observed | Status |
| --- | --- | --- | --- |
| RC36 / P40 open/mean | 0.15..2.00 | [0.223, 1.793] | holds |
| RC37 / P41 max/med | 2.50..8.00 | [3.143, 7.333] | holds |
| RC38 / P42 IQR/mean | 0.50..1.20 | [0.594, 1.065] | holds |
| RC2 fixed band [528, 552] | law on util maxima | D=738 escape | retained falsified |
| RC33-RC35 | prior residual | retained | holds (not primary) |
| S1* proximity | D(r) bound | — | UNRESOLVED (PROOF.md) |

Branch-max panel (F(r) = o_q):

| o_q | r | D | first | trail | open/mean | max/med | IQR/mean |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 4 | 20 | 0.456 | 7.333 | 0.911 |
| 4 | 482342527 | 486 | 16 | 6 | 1.793 | 3.714 | 1.065 |
| 6 | 424171123 | 738 | 3 | 8 | 0.392 | 5.000 | 0.915 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.43s
```
RC36 residual probe exit code: 0 (RC36-RC38 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC36-RC38 (opening isolation in mean-gap
units, peak successive gap vs median, IQR scaled by mean) with explicit
falsification command; all three hold on util maxima through `4e8-5e8` +
`o_q` panel. Continuity: residual package through RC38; proximity remains
OPEN/UNRESOLVED. Not a replay of RC33-RC35 IQR/median, trail/mean, or body
last-quartile mass.

Artifacts:
`experiments/square-branch-hourly-2026-07-13-rc36/offset_540_residual_rc36_probe.py`;
`experiments/square-branch-hourly-2026-07-13-rc36/offset_540_rc36_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-13-rc36/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (residual package through RC38; proximity OPEN/UNRESOLVED)

Next step:
Queue falsification `5e8-6e8` and re-check RC36-RC38 (and RC18-RC35) on any
new util maximum. Keep RC36-RC38 residual only; do not promote open/mean,
max/median, or IQR/mean to theorem; do not revive fixed-band 540 or d=4 SDA.

## 2026-07-13T21:53:19Z run

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
4 passed in 2.23s
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

## 2026-07-13T21:55:11Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (queue job `chamber-reset-lemma-draft`).

Method:
Read `PROOF.md` §Square-Branch Reduction, blocker acceptance, prior S1–S11
constructive chain, and residual package RC36–RC38. Appended constructive
subsection **S12** under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`
naming OpeningScale / ResetResidual^O with explicit falsification commands.
Did not port d=4 SDA. RC2 fixed-band remains falsified. Target S1* remains
UNRESOLVED.

Result:

| Claim | Role | Status |
| --- | --- | --- |
| S12-A open_over_mean | constructive | drafted |
| S12-B max_over_median + iqr_over_mean | constructive | drafted |
| S12-C OpeningScale / ResetResidual^O | constructive residual state | drafted |
| RC36 open/mean [0.15, 2.00] | residual audit | holds [0.223, 1.793] |
| RC37 max/med [2.50, 8.00] | residual audit | holds [3.143, 7.333] |
| RC38 IQR/mean [0.50, 1.20] | residual audit | holds [0.594, 1.065] |
| RC2 fixed band [528, 552] | law on util maxima | retained falsified |
| S1* proximity | D(r) bound | UNRESOLVED (PROOF.md) |

Branch-max panel (F(r) = o_q):

| o_q | r | D | open/mean | max/med | IQR/mean |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.456 | 7.333 | 0.911 |
| 4 | 482342527 | 486 | 1.793 | 3.714 | 1.065 |
| 6 | 424171123 | 738 | 0.392 | 5.000 | 0.915 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Constructive lemma pressure only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.37s
```
RC36 residual probe exit code: 0 (RC36-RC38 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S12 (OpeningScale: open/mean, max/median,
IQR/mean; ResetResidual^O) with hypotheses H1–H6 reuse, unresolved S1* status,
and explicit falsification commands for Target S1* and residual RC36–RC38.
Companion package under experiments/square-branch-hourly-2026-07-13-s12/.
Not a replay of S11 robust-scale prose; not a promotion of RC36–RC38 to theorem.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html` (S12);
`experiments/square-branch-hourly-2026-07-13-s12/FINDINGS.md`;
`experiments/square-branch-hourly-2026-07-13-rc36/` (falsification probe retained)

Next step:
Queue falsification `5e8-6e8` and re-check RC36–RC38 / OpeningScale on any new
util maximum. Keep S12 residual only; do not promote open/mean, max/median, or
IQR/mean to theorem; do not revive fixed-band 540 or d=4 SDA.

## 2026-07-14T01:56:53Z run

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
elapsed_seconds: 82.85577869415283

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.45s
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
## 2026-07-14T06:45:36Z run

Mechanism:
PGS-native structural audit of recurring offset 540 and early-tau=4 /
late-tau=3 chamber separation (queue job `offset-540-structural-audit`).
Project terms: residual claims RC39-RC41 / predictions P43-P45
(median-scaled Dual isolation: open/median, trail/median, dual/median).

Method:
Read falsification summary
`research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json`
and `experiments/square-branch-sda-invalidation-2026-06/prefix_tau_floor_probe.json`.
Built residual claim package RC39-RC41 under
`experiments/square-branch-hourly-2026-07-14-rc39/` with explicit
falsification command. Recomputed Dual markers and median successive Tau4
gaps on segment util maxima through 4e8-5e8 plus full o_q branch-max panel.
Did not port d=4 SDA. RC2 fixed-band retained falsified.

Result:

| Claim | Bound | Observed | Status |
| --- | --- | --- | --- |
| RC39 / P43 open/med | 0.20..2.50 | [0.250, 2.286] | holds |
| RC40 / P44 trail/med | 0.20..3.50 | [0.250, 3.333] | holds |
| RC41 / P45 dual/med | 0.40..4.50 | [0.500, 4.000] | holds |
| RC2 fixed band [528, 552] | law on util maxima | D=738 at r=424171123 | falsified (retained) |
| RC36-RC38 | prior residual | retained | holds (not primary) |

Branch-max panel (median-scaled Dual isolation):

| o_q | r | D | first | trail | open/med | trail/med | dual/med |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 4 | 20 | 0.667 | 3.333 | 4.000 |
| 4 | 482342527 | 486 | 16 | 6 | 2.286 | 0.857 | 3.143 |
| 6 | 424171123 | 738 | 3 | 8 | 0.500 | 1.333 | 1.833 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Residual audit only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.62s
```
RC39 residual probe exit code: 0 (RC39-RC41 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New falsifiable residual claim table RC39-RC41 (Dual isolation in median-gap
units: open/median, trail/median, dual/median) on util maxima through
4e8-5e8 + o_q panel. Continuity: residual package through RC41; proximity
remains OPEN/UNRESOLVED. Not a replay of RC36-RC38 open/mean, max/med, or
IQR/mean; not a promotion of median-scaled Dual isolation to theorem.

Artifacts:
`experiments/square-branch-hourly-2026-07-14-rc39/offset_540_residual_rc39_probe.py`;
`experiments/square-branch-hourly-2026-07-14-rc39/offset_540_rc39_prediction_table.json`;
`experiments/square-branch-hourly-2026-07-14-rc39/FINDINGS.md`;
`research/00-index/continuity/ACTIVE_TARGET.md` (residual package through RC41; proximity OPEN/UNRESOLVED)

Next step:
Queue falsification `5e8-6e8` and re-check RC39-RC41 (and RC18-RC38) on any
new util maximum. Keep RC39-RC41 residual only; do not promote open/median,
trail/median, or dual/median to theorem; do not revive fixed-band 540 or d=4 SDA.

## 2026-07-14T11:03:01Z run

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
4 passed in 2.31s
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

## 2026-07-14T15:05:26Z run

Mechanism:
Draft one subsection of the Chamber-Reset Endpoint Resolution Lemma on the
selected-square branch (queue job `chamber-reset-lemma-draft`). Project terms:
Claims S13-A / S13-B / S13-C, residual package RC39-RC41, MedianDual(r),
ResetResidual^M(r).

Method:
Read PROOF.md §Square-Branch Reduction, square_branch_blocker_acceptance.md,
prior lemma HTML S1–S12, and residual package
`experiments/square-branch-hourly-2026-07-14-rc39/`. Appended constructive
subsection S13 (median Dual isolation: open/median, trail/median, dual/median)
under
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html`.
Wrote companion FINDINGS under
`experiments/square-branch-hourly-2026-07-14-s13/`. Re-ran RC39 residual probe
(holds). Did not promote RC39-RC41 to theorem. Did not revive d=4 SDA or
fixed-band 540. Target S1* remains UNRESOLVED.

Result:

| Claim | Object | Status |
| --- | --- | --- |
| S13-A | open_over_median = first_τ4 / median_gap | constructive (lemma) |
| S13-B | trail_over_median, dual_over_median | constructive (lemma) |
| S13-C | MedianDual + ResetResidual^M | constructive residual-state id |
| RC39 / open/med | 0.20..2.50; obs [0.250, 2.286] | holds (audit) |
| RC40 / trail/med | 0.20..3.50; obs [0.250, 3.333] | holds (audit) |
| RC41 / dual/med | 0.40..4.50; obs [0.500, 4.000] | holds (audit) |
| RC2 fixed band [528, 552] | law on util maxima | falsified (retained) |
| Target S1* | D(r) ≤ C_dyn(r) universal | UNRESOLVED |

Branch-max panel (median Dual):

| o_q | r | D | open/med | trail/med | dual/med |
| --- | --- | --- | --- | --- | --- |
| 2 | 468917503 | 542 | 0.667 | 3.333 | 4.000 |
| 4 | 482342527 | 486 | 2.286 | 0.857 | 3.143 |
| 6 | 424171123 | 738 | 0.500 | 1.333 | 1.833 |

Theorem: prime-square proximity / Target S1* remains UNRESOLVED in `PROOF.md`
§Square-Branch Reduction; direct next-prime and Interior Maximizer remain
proved. Constructive lemma subsection only. Invalidated d=4 SDA not revived.

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.68s
```
RC39 residual probe exit code: 0 (RC39-RC41 hold; RC2 retained falsified).

Research status:
ADVANCE

Ops status:
OK

Delta:
New constructive lemma subsection S13 (median Dual isolation: open/median,
trail/median, dual/median) with Claims S13-A/B/C, MedianDual(r),
ResetResidual^M(r), explicit falsification command for Target S1*, and residual
panel RC39-RC41 formalized under the lemma. Continuity: lemma through S13;
residual package through RC41; proximity remains OPEN/UNRESOLVED. Not a replay
of S12 open/mean package; not a promotion of median Dual isolation to theorem.

Artifacts:
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/index.html` (S13);
`experiments/square-branch-hourly-2026-07-14-s13/FINDINGS.md`;
`experiments/square-branch-hourly-2026-07-14-rc39/` (residual panel source, re-run holds)

Next step:
Queue falsification `5e8-6e8` or H_CTC square-branch probe. Re-check RC39-RC41 /
MedianDual on any new util maximum. Keep S13 residual only; do not promote
open/median, trail/median, or dual/median to theorem; do not revive fixed-band
540 or d=4 SDA.

## 2026-07-14T19:08:09Z run

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
elapsed_seconds: 86.07205080986023

pytest exit code: 0
```
....                                                                     [100%]
4 passed in 2.31s
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
