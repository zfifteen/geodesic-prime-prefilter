**Confirmed. Here is the single authoritative classification table (the only version permitted in the v2 HTML contract):**

| Count of cases in which true `p % M` is the unique structural winner by the keys `(dev_primary, support_score)` | Controls | Other conditions | Classification                      | Meaning for publication |
|-------------------------------------------------------------------------------------------------------------|----------|------------------|-------------------------------------|---------------------------|
| 18-20                                                                                                       | Both empty at certificate layer | None | `accepted_measured_result`         | The v2 ranking rule supplies a tight public residue selector on this surface. |
| 14-17                                                                                                       | Both empty at certificate layer | None | `boundary_measurement`             | Interesting signal above the original v1 "14 of 20" line, but does not yet meet the stricter falsification-protected acceptance threshold. |
| <14                                                                                                         | Any      | Or any forbidden inference pattern or control produces non-empty certificate | `invalidated_result`               | The rule fails under its own stated falsification conditions on this surface. |
| Any                                                                                                         | -        | Implementation deviates from the frozen contract or fails to emit required artifacts and logs | `unresolved_implementation_failure`| Engineering or audit issue; the selector itself was never tested. |

**Additional rule (already agreed, now explicit):** If the true `p % M` reaches the top position only because of the final deterministic `a` tie-break (i.e., `dev_primary` and `support_score` are tied with one or more other residues), the case is classified `boundary_measurement` for acceptance purposes, even if the raw count would otherwise suggest a higher band.

The methodological conflict is resolved. The HTML may now be written using exactly this table.
