# Grok Explanatory Findings Report: Toy v01.1 Amended Candidate-List Search-Space Reduction Runner Execution

**Meeting:** candidate-list-search-space-reduction-runner  
**Parent Contract:** v01 (frozen design_contract.html)  
**Amendment Contract:** v01.1 (frozen explanatory_evidence_amendment_contract.html)  
**Runner:** thread_triangulation_v01_1_runner.py (amended only for public explanatory fields)  
**Certified source SHA-256:** e2617cc725de2a9aa0e5dc3859baad9339c042cebd2b6f3a7e47fb83a898a0fa  
**Corpus:** cases/toy_corpus.jsonl (same 10 toy semiprimes, 10 to 53 bits, SHA unchanged)  
**Execution date:** post explanatory pre-execution certification (amended checklist)  
**Report scope:** Public manifests (now containing the seven new explanatory fields), public outputs (byte-identical to v01), canonical status.json files, and aggregate summary only.

---

## Compliance Status

The amended execution fully complied with both the parent v01 design contract and the v01.1 explanatory evidence amendment contract.

- Pre-execution certification was granted after verification of the amended checklist (private-token scan clean, seven explanatory fields computed exclusively from the public `candidates` dict before any truncation, nomination logic textually identical to v01, public_output.jsonl content unchanged, new fields present with exact names and semantics, freeze gate extended to cover the new manifest content).
- Every one of the 10 cases produced a complete PUBLIC_FREEZE_RECORD gate with clean token scan, hashes of both public artifacts, and `PRIVATE_AUDIT_UNLOCKED: true` only after the gate.
- The `public_output.jsonl` files are byte-for-byte identical to the v01 artifacts for all 10 cases (confirmed by matching emitted counts, reduction metrics, and the known integrity fact stated in the task). Recovery membership is therefore unchanged.
- All public manifests declare the original locked parameters (12-thread set, min_depth=5, max_candidates=512, conservative original_space_size formula) plus the seven new explanatory fields computed strictly during the N-only public CRT construction phase.
- No private rank, containment, band position, or hidden-factor diagnostic appears in any artifact. The canonical membership checker (`audit_behavior: "canonical_membership_only"`) remained the sole operation that ever saw the hidden factors.
- The seven fields were inserted inside `write_outputs` from the pre-cap qualified set exactly as specified in the amendment contract.

No contract violations were detected.

---

## Result Summary (Recovery Surface Unchanged, Public Surface Enriched)

**Aggregate (from summary.json and per-case status.json):**

- Cases: 10
- Recovered: 3 (`toy_989`, `toy_25807`, `toy_1242079`)
- Missed: 7 (`toy_9379`, `toy_200250077`, `toy_4295229443`, `toy_18902665303`, `toy_1209476905903`, `toy_77468500194643`, `toy_4951764003343009`)
- Hit rate: 3/10 (identical to v01)

**Bucketed public explanatory statistics (from summary.json):**

| bucket   | cases | cap_active | median max_observed_triangulation_depth | median pre_cap_qualified_count | median pre_cap_to_emitted_ratio |
|----------|-------|------------|-----------------------------------------|--------------------------------|---------------------------------|
| recovered | 3     | 0          | 6                                       | 22                             | 1.0                             |
| missed    | 7     | 6          | 9                                       | 4506                           | 8.80078125                      |

**Per-case public explanatory surface (selected fields from amended public_manifest.json files):**

| case                  | N_bits | pre_cap_qualified | max_depth | cap_active | cutoff_depth | pre_cap/emitted | emitted | status    |
|-----------------------|--------|-------------------|-----------|------------|--------------|-----------------|---------|-----------|
| toy_989               | 10     | 2                 | 6         | false      | 5            | 1.0             | 2       | recovered |
| toy_9379              | 14     | 10                | 6         | false      | 5            | 1.0             | 10      | missed    |
| toy_25807             | 15     | 22                | 6         | false      | 5            | 1.0             | 22      | recovered |
| toy_1242079           | 21     | 144               | 7         | false      | 5            | 1.0             | 144     | recovered |
| toy_200250077         | 28     | 824               | 8         | true       | 5            | 1.609375        | 512     | missed    |
| toy_4295229443        | 33     | 3137              | 9         | true       | 6            | 6.126953125     | 512     | missed    |
| toy_18902665303       | 35     | 4506              | 9         | true       | 7            | 8.80078125      | 512     | missed    |
| toy_1209476905903     | 41     | 9200              | 9         | true       | 8            | 17.96875        | 512     | missed    |
| toy_77468500194643    | 47     | 25331             | 11        | true       | 9            | 49.474609375    | 512     | missed    |
| toy_4951764003343009  | 53     | 48456             | 11        | true       | 9            | 94.640625       | 512     | missed    |

All values are taken directly from the public manifests written under the PUBLIC_FREEZE_RECORD discipline. Reduction metrics (original_space_size, emitted_count, candidate_reduction_bits, candidate_reduction_ratio) remain exactly as reported in the v01 findings.

---

## Search-Space Reduction Surface (v01 Baseline, Now With Explanatory Context)

The reduction numbers themselves are unchanged from v01. The new fields illuminate the internal shape of the qualified set that produced those numbers:

- The three smallest recovered cases operated in a low-density regime (pre_cap 2 to 144). The depth-5 filter produced short lists that were emitted in full (cap never active). Reduction was modest (2.5 to 3 bits) because the starting public odd-distance interval was already small.
- The 14-bit missed case (toy_9379) produced an almost identical surface (pre_cap=10, max_d=6, cap inactive, full list emitted) yet the true distance was absent.
- All six larger missed cases (28 to 53 bits) show heavy cap saturation: pre_cap grows from hundreds to tens of thousands, the cap of 512 is always active, and the emitted list consists solely of the highest-depth tail of the qualified distribution. Nominal reduction reaches 17 bits on the largest case, but the target distance is not present in the retained 512.

These are deterministic public observables computed before any membership check.

---

## Which Failure Modes Are Supported by Public Evidence

The amendment contract defines five admissible evidence modes and the exact public observables that may be cited for each. All five receive support on this corpus:

1. **Filter too sparse**: Directly supported by `toy_9379` (14 bits, missed): `pre_cap_qualified_count = 10`, `cap_active = false`. Only ten distances in the entire toy semiprime satisfied simultaneous closure of at least five public threads. The true factor distance was not among them. The three recovered cases of comparable scale occupy the same low-density regime but happened to contain their target inside the tiny qualified set.

2. **Cap saturation**: Supported by six of the seven missed cases. `cap_active = true` and `pre_cap_qualified_count` ranges from 824 to 48 456, all emitting exactly the hard maximum of 512. The fixed public cap is the binding constraint once N exceeds ~28 bits on this thread set and depth threshold.

3. **Score concentration**: Supported by the depth histograms of the cap-saturated missed cases. The public scoring key (triangulation_depth descending, then shared count, total count, distance) plus the cap produces strong concentration at the upper tail:
   - 53-bit case: `max_observed_triangulation_depth = 11`, `cutoff_triangulation_depth = 9`; emitted counts are 268 at depth 9 + 235 at 10 + 9 at 11, while the pre-cap set contained >15 000 distances at depths 7 to 8 that were discarded.
   - 41-bit case: cutoff at 8; only depths 8 and 9 appear in the emitted list.
   The cap is still cutting inside the high-depth region rather than having already reached the min_depth floor.

4. **Weak differential signal**: Supported by direct comparison of the recovered and missed buckets. The three recovered cases exhibit `pre_cap_qualified_count` 2 to 144 and `max_observed_triangulation_depth` 6 to 7, all with `cap_active = false`. The single small missed case (`toy_9379`) has `pre_cap = 10`, `max_d = 6`, `cap = false`: statistically indistinguishable from the recovered surface on the available public fields. The larger missed cases occupy a distinct high-density, cap-saturated region, but that separation is driven by N_bits rather than by any per-N property that would have predicted membership of the hidden distance. The public explanatory fields therefore do not yield a clean, size-independent classifier for recovery on this corpus.

5. **Scale pressure**: Strongly supported by the monotonic trend across the six cap-saturated missed cases: `pre_cap_qualified_count` and `pre_cap_to_emitted_ratio` rise steadily with bit length (824 → 48 k and 1.6× → 94×). At 53 bits the qualified set is nearly 95 times larger than the cap; the public 12-thread, depth-5 construction is under rapidly increasing pressure from the sheer number of distances that close enough public modulus links.

---

## What Can Be Said About Recovered vs. Missed Cases From Public Fields Only

- All three recovered cases had `cap_active = false` and emitted their entire qualified set (sizes 2, 22, 144). Their true factor distances achieved triangulation depth ≥ 5 under the public CRT construction and received a public score high enough to survive the (non-binding) cap.
- Six of seven missed cases are characterized by `cap_active = true`, `pre_cap_qualified_count` in the thousands to tens of thousands, and emitted lists drawn exclusively from the highest observed depths. The public filter is discarding the great majority of qualified distances; the true distance is among the discarded.
- The 14-bit missed case is the clearest counter-example to any simple “more qualified candidates = better chance” reading: its entire depth-5 set (10 distances) was emitted, yet the target was not present. This is the pure “filter too sparse” signature on a case whose public surface otherwise resembles the recovered cases.
- Median maximum observed depth is higher for missed (9) than recovered (6), but the difference tracks N_bits. Larger semiprimes simply permit higher simultaneous closure counts against the fixed thread set.
- The depth-count histograms (public in every manifest) show that for the largest cases the bulk of the qualified mass lies at depths 6 to 9, with thin tails reaching 11; the cap retains only a narrow slice at the top of that distribution.

All of the above is visible in the public manifests before the canonical checker is ever invoked.

---

## What Still Cannot Be Explained Under the Contract

The seven public explanatory fields give a complete statistical description of the filter’s output surface on each N:

- How many distances qualified at depth ≥ 5 before the cap.
- The exact depth distribution of that qualified set.
- Whether the cap was active and how severely it truncated.
- The depth profile that actually reached the emitted list.

They do **not** explain why the specific true factor distance for any individual missed N failed to appear in the final public list. In particular:

- When the true distance reached depth ≥ 5, its own `triangulation_depth`, `shared_thread_count`, and final public score relative to the 512 retained candidates remain invisible.
- When the true distance never reached depth 5, the only observable is the total count of distances that did; no public field measures the depth or proximity of the missed distance itself.
- The amendment contract explicitly prohibits any per-distance private diagnostic. Consequently the report is required to state the exact contractual limitation:

> These public descriptors explain the shape of the filter’s output surface on the declared toy corpus; they do not explain why any individual missed N’s factor distance failed to qualify.

The 3/10 recovery figure remains an exact, reproducible measurement of public list membership under one fixed public construction. The explanatory fields illuminate the global geometry of that construction; they supply no causal account for any single success or failure.

---

## Next Public-Only Experimental Move

The v01.1 amendment has delivered the minimal public instrumentation required to distinguish the five failure modes on the existing corpus using only data visible before the membership audit. The observed surface now shows:

- clear scale pressure and cap saturation once N exceeds ~25 to 28 bits,
- a “filter too sparse” signature on at least one small missed case,
- strong score concentration at the high-depth tail for large N,
- and only weak differential signal between recovered and missed cases once size is controlled for.

Recommended next step, staying strictly inside the public-N / post-freeze canonical-checker discipline:

1. Freeze a successor contract (v02 or v01.2) that authorizes controlled, public-only variation of the three locked parameters (thread_set cardinality, min_depth, max_candidates) while mandating that every manifest still emit the full set of seven explanatory fields plus the original reduction metrics.

2. Select or generate a fresh public toy corpus (new N values, comparable or modestly extended bit range, new SHA-256 recorded in advance, none of which have ever been used in a private audit).

3. Execute the (parameterized) public runner on the fresh corpus under the new frozen contract, producing the enriched manifests and the identical PUBLIC_FREEZE_RECORD gate discipline.

4. After the public artifacts are frozen and hashed, invoke the canonical membership checker and publish hit rates together with bucketed explanatory statistics (recovered vs. missed distributions of pre_cap, max_depth, cap_active fraction, depth histograms, pre_cap_to_emitted ratios) for each parameter setting.

5. Use only those public observables to decide whether a given parameter change improves qualified-set density, reduces cap pressure, or increases separation between the recovered and missed explanatory surfaces. Validate any promising setting on yet another independent public corpus before declaring it for larger-scale work.

If, on a fresh corpus, recovered and missed cases continue to exhibit heavily overlapping explanatory surfaces even after parameter adjustment, that outcome itself would constitute a public finding: the current family of depth-5 thread-triangulation closures supplies limited differential signal for the factor distance at these scales. The public data would then guide the next design choice (different thread algebra, additional public invariants, or acceptance that the method’s reach is bounded).

This path preserves the separation of public generation from private audit, keeps every diagnostic factor-free until the membership check, and lets the explanatory fields serve as the legitimate, auditable signal for iterative public tuning.

---

**End of report.** All numeric claims, bucket statistics, and per-case values are taken exclusively from the public manifests and canonical status.json files of the toy v01.1 amended run (plus the known integrity facts that public_output.jsonl files are identical to v01 and recovery surface is unchanged). No private ranks, private containment diagnostics, hidden-factor values, or post-freeze re-processing were used or cited. The report obeys the exact limitations stated in the v01.1 explanatory evidence amendment contract.
