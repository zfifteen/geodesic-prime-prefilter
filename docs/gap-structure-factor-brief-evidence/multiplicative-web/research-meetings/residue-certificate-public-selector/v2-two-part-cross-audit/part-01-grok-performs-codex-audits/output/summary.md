# V2 Public Selector Probe - Grok Part One (reciprocal_shadow_v2_public_selector_probe_grok.py)

Controlling contract: residue_certificate_v2_public_selector_contract.html
V1 certificate layer reproduced exactly (conflict + CRT). V2 GWR + deviation ranking applied only to true certificate.
No files written outside the designated Part One folder.

## Per-Case Surface (20 cases, radius=300, M from top-4 held-out thread degrees)

| idx | N | p | p_mod_M | M | sel_r | |C_t| | |C_r| | |C_s| | t_g | d_min | supports | p_struct_win | tie | winner_a | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 713 | 23 | 23 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | 128 | 3 | 125,129 | False | 2 | None | boundary_measurement |
| 1 | 2537 | 43 | 43 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | 272 | 3 | 270,274 | False | 2 | None | boundary_measurement |
| 2 | 5063 | 61 | 61 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -22 | 3 | -30,-21 | False | 2 | None | boundary_measurement |
| 3 | 10057 | 89 | 89 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | 144 | 3 | 141,145 | False | 2 | None | boundary_measurement |
| 4 | 13837 | 101 | 101 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -298 | 4 | -,-296 | False | 2 | None | boundary_measurement |
| 5 | 21877 | 131 | 131 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -299 | 4 | -,-298 | False | 2 | None | boundary_measurement |
| 6 | 36503 | 173 | 173 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -22 | 3 | -32,-20 | False | 2 | None | boundary_measurement |
| 7 | 63433 | 229 | 19 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -299 | 4 | -,-296 | False | 2 | None | boundary_measurement |
| 8 | 112669 | 307 | 97 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -300 | 4 | -,-296 | False | 2 | None | boundary_measurement |
| 9 | 201703 | 401 | 191 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -102 | 3 | -105,-101 | False | 2 | None | boundary_measurement |
| 10 | 368177 | 557 | 137 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | 272 | 3 | 264,280 | False | 2 | None | boundary_measurement |
| 11 | 621787 | 701 | 71 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -300 | 4 | -,-296 | False | 2 | None | boundary_measurement |
| 12 | 1242079 | 1009 | 169 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -296 | 4 | -,-294 | False | 2 | None | boundary_measurement |
| 13 | 3206803 | 1601 | 131 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -300 | 4 | -,-296 | False | 2 | None | boundary_measurement |
| 14 | 12007001 | 3001 | 61 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -300 | 4 | -,-298 | False | 2 | None | boundary_measurement |
| 15 | 35026003 | 5003 | 173 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -300 | 4 | -,-284 | False | 2 | None | boundary_measurement |
| 16 | 225000307499857 | 7500013 | 73 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -294 | 4 | -,-286 | False | 2 | None | boundary_measurement |
| 17 | 225000094499417 | 6000011 | 101 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -288 | 4 | -,-280 | False | 4 | None | boundary_measurement |
| 18 | 225000309499937 | 4500007 | 127 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -298 | 4 | -,-292 | False | 2 | None | boundary_measurement |
| 19 | 225000215993999 | 3000017 | 167 | 210 | [2, 3, 5, 7] | 48 | 0 | 0 | -294 | 4 | -,-288 | False | 4 | None | boundary_measurement |

## Aggregate Result (V2 contract classification table)

Structural wins (p % M is unique minimal (dev_primary, support_score) with tie_size=1): 0/20
Both controls empty at certificate layer on all 20 cases: True
Final classification under V2 table: **invalidated_result**

Hypothesis under test: the public GWR leftmost-min-divisor reciprocal deviation ranking
over the V1 certificate produces a tight selector in which true p % M is the unique
structural winner on 18-20 of the 20 cases (with controls remaining empty).

Raw artifacts (summary.json, certificate.jsonl, runtime_residue_crt_log.jsonl) were
written by the probe before this summary or any interpretive document.

See self_checklist.md for the 14-item contract verification and grok_execution_notes.md
for hypothesis / measured / audit separation.
