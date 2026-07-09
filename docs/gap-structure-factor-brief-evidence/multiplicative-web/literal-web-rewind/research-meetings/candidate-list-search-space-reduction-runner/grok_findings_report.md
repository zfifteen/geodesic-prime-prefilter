# Grok Findings Report: Toy v01 Candidate-List Search-Space Reduction Runner Execution

**Meeting:** candidate-list-search-space-reduction-runner  
**Contract:** v01 (frozen design_contract.html)  
**Runner:** thread_triangulation_v01_runner.py  
**Certified source SHA-256:** dd1b0d9f1d69f25c845f2812214da92187f4e3750609b1b94963934d3fd03878  
**Corpus:** cases/toy_corpus.jsonl (10 toy semiprimes, 10 to 53 bits)  
**Execution date:** post pre-execution certification  
**Report scope:** Public manifests, public outputs, canonical status files, and aggregate summary only.

---

## Compliance Status

The execution fully complied with the frozen v01 design contract.

- Pre-execution certification was granted by Grok after verifying the seven checklist items.
- Runner source SHA-256 exactly matches the certified value.
- Every one of the 10 cases produced a complete PUBLIC_FREEZE_RECORD gate with:
  - Clean private-token scan (`pass` for all 19 forbidden tokens).
  - Hashes of public_output.jsonl and public_manifest.json.
  - Public reduction metrics and record count.
  - `PRIVATE_AUDIT_UNLOCKED: true` only after the gate.
- The runner accepted only `--n` (public N), never read labels or corpus metadata, and performed no post-freeze re-scoring.
- The canonical membership checker (audit/status.json with `audit_behavior: "canonical_membership_only"`) was the sole operation that ever saw the hidden factors.
- All public manifests declare the locked parameters: 12-thread set, `min_depth=5`, `max_candidates=512`, and the exact conservative `original_space_size` formula.
- Source private-token scan inside the runner itself was clean at certification and at every runtime freeze.

No contract violations were detected in the delivered artifacts.

---

## Result Summary

**Aggregate (from summary.json and per-case status.json):**

- Cases: 10
- Recovered: 3 (`toy_989`, `toy_25807`, `toy_1242079`)
- Missed: 7 (`toy_9379`, `toy_200250077`, `toy_4295229443`, `toy_18902665303`, `toy_1209476905903`, `toy_77468500194643`, `toy_4951764003343009`)
- Hit rate: 3/10

**Per-case public reduction surface (public_manifest.json values):**

| case                  | N_bits | original_space | emitted | reduction_bits | reduction_ratio     | status    | recovered_factor |
|-----------------------|--------|----------------|---------|----------------|---------------------|-----------|------------------|
| toy_989               | 10     | 16             | 2       | 3.000          | 16/2                | recovered | p                |
| toy_9379              | 14     | 64             | 10      | 2.678          | 64/10               | missed    | :                |
| toy_25807             | 15     | 128            | 22      | 2.541          | 128/22              | recovered | q                |
| toy_1242079           | 21     | 1024           | 144     | 2.830          | 1024/144            | recovered | p                |
| toy_200250077         | 28     | 8192           | 512     | 4.000          | 8192/512            | missed    | :                |
| toy_4295229443        | 33     | 65536          | 512     | 7.000          | 65536/512           | missed    | :                |
| toy_18902665303       | 35     | 131072         | 512     | 8.000          | 131072/512          | missed    | :                |
| toy_1209476905903     | 41     | 1048576        | 512     | 11.000         | 1048576/512         | missed    | :                |
| toy_77468500194643    | 47     | 8388608        | 512     | 14.000         | 8388608/512         | missed    | :                |
| toy_4951764003343009  | 53     | 67108864       | 512     | 17.000         | 67108864/512        | missed    | :                |

All manifests and outputs were produced under identical locked v01 parameters and carry the certified runner SHA.

---

## Search-Space Reduction Interpretation

The measured reduction is the publicly observable shrinkage from the conservative baseline (count of odd positive distances d with 1 ≤ d ≤ public_radius(N)) to the size of the emitted list after depth-5 filtering and public scoring / capping.

- For the three smallest recovered cases the depth-5 modulus-link filter already produced very short lists (2 to 144 candidates), yielding modest 2.5 to 3 bit reductions.
- For N ≥ 28 bits the hard cap of 512 dominated; the filter emitted the maximum allowed list and delivered 4 to 17 bits of nominal reduction.
- The largest case (53 bits) achieved a 17-bit nominal reduction (67 M → 512) while still missing the target distance.

These are deterministic, reproducible public figures. They quantify how many odd distances up to the public radius survive the simultaneous residue-closure test against the fixed 12-thread set.

---

## What Worked

1. The public-only contract was enforced end-to-end. The freeze gate, token scan, and separation of public generation from canonical membership checking operated exactly as specified.
2. The thread-triangulation mechanism (iterative CRT closure of public left/right residues of N against the fixed thread set) is fully deterministic and requires only N and the public thread primes.
3. On three toy semiprimes the true factor distance achieved triangulation depth ≥ 5, survived deduplication, and ranked high enough under the public score key (depth primary, shared count secondary, total count tertiary, distance tie-break) to appear inside the emitted list.
4. Reduction numbers are stable and auditable from the public manifests alone; no private data is required to compute or verify them.

---

## What Failed

1. For seven of the ten cases the true factor distance(s) never entered the depth-5 set or were culled by the public scoring / 512 cap. This includes the 14-bit case toy_9379 (only 10 candidates emitted) and all seven larger instances.
2. Even when substantial nominal reduction occurred (11 to 17 bits on the four largest missed cases), the target distance was absent from the final public list.
3. The v01 parameter set (depth 5, 12 threads, cap 512) proved insufficient to guarantee recovery on this corpus once N exceeded 21 bits.

---

## Methodological Meaning of 3 Recovered / 10

Under the strict public-candidate-list contract the result is:

> At the locked v01 parameters the public thread-triangulation filter (depth ≥ 5 over the first 12 odd primes, capped at 512) placed the hidden-factor distance inside its emitted shortlist for 3 out of 10 declared toy semiprimes.

This is an exact, reproducible measurement of public list membership on a fixed public corpus. It demonstrates that, for certain small semiprimes, the factor distance satisfies enough simultaneous public modulus-link closures to survive the filter and public ranking. For the other seven it does not.

The 3/10 figure does not:
- Prove the filter “factors” N.
- Indicate that the true factors are “usually” or “often” captured.
- License any statement about behavior at cryptographic sizes.
- Supply evidence about why the three succeeded and the seven did not (that would require private diagnostics, which are outside the allowed surface).

It is simply the observed containment rate of the true distance under one fixed public construction on one small public corpus.

---

## Constraints on What Cannot Be Claimed

- No general recovery claim. The experiment supplies no warrant that the method recovers factors on arbitrary or larger N.
- No private-position claims. Private rank, “how close,” containment interval, or band diagnostics are contractually excluded from recovery evidence and from this report.
- No scale extrapolation. All 10 cases are toy (< 54 bits). Results on this corpus do not bound or predict performance at 256-bit or RSA scales.
- Reduction bits are nominal only. They are computed against the deliberately conservative public odd-distance count; they do not measure advantage relative to classical sieves, ECM, or any other prefilter.
- Parameter choice was pre-freeze. The thread set, depth 5, and cap 512 were locked before any results were seen. The measured hit rate therefore does not validate those specific values for future use.
- No hybrid-system claims. The public CRT construction may not be inserted into a larger classical pipeline without a fresh, separate public-N-only contract.

---

## Grok's Recommended Next Research Move (Strictly Inside Public-Candidate-List Framing)

Stay inside the public-N, public-manifest, post-freeze canonical-checker discipline.

**Proposed next surface (v01.1 or v02 contract):**

1. Freeze a new contract (or v01.1 amendment) that adds only public histogram fields to every manifest:
   - count of distances reaching each triangulation depth (before any cap)
   - maximum depth achieved
   - number of candidates at min_depth and at max observed depth
   - size of the pre-cap depth-5 set
   All numbers must be derivable from the public CRT construction alone.

2. Select a fresh public toy corpus (new N values, same or modestly extended bit range, new SHA) never used in any prior private audit.

3. Execute the identical v01 runner (or a v02 with one declared parameter change) on the new corpus under the new contract, producing the extended public manifests and the same freeze-gate discipline.

4. After the public surface is frozen, run the canonical membership checker and publish the same style of aggregate table plus the new public depth-distribution statistics for recovered vs. missed cases.

**Rationale (public only):**  
If recovered cases systematically exhibit higher pre-cap depth counts, higher maximum depth, or larger depth-5 sets than missed cases, that observable public statistic would be a legitimate, factor-free signal for tuning the next parameter set (different depth threshold or thread count) on yet another fresh corpus. If the depth profiles are statistically indistinguishable, the public data themselves would indicate that depth-5 closure over this thread set carries little differential signal for the factor distance on these scales.

This move keeps every artifact public until the membership check, preserves the freeze gate, and generates new, auditable public evidence without ever reopening private diagnostics.

---

**End of report.** All statements are bounded by the declared toy corpus, the locked v01 parameters, and the public-only contract. No private ranks, containment diagnostics, or hidden-factor computations were used or cited.
