# Super Sleuth Scientific Detective Agent Team: Manifest

**Team name:** Super Sleuth Scientific Detective Agent Team  
**Mission:** Independent forensic review of Remainder Research Super Team evidence  
**Forensic report:** `research/remainders/REMAINDER_FORENSIC_REPORT.md`  
**Verifier:** `research/remainders/forensic_verify.py`

Six lane detectives mirror the Super Team roster (`SUPER_TEAM_MANIFEST.md`). Each detective audits one lane: regime labels, repro commands, numeric claims vs pinned JSON, and epistemic classification. No re-collection; read-only cross-examination.

| Detective ID | Lane audited | Primary evidence examined |
|--------------|--------------|---------------------------|
| `detective_interior` | Interior `R(n,M)` | `output/1.5e6/summary.json`, `interior_placement_stats.json` |
| `detective_super_signal` | GWR Super-Signal (epistemic) | `super_signal_status.json`, `PROOF.md`, `goals.md` G2 |
| `detective_endpoint` | Endpoint `q mod` mask | `endpoint_residue_probe_fresh.json`, `endpoint_lane_summary.json` |
| `detective_mod30` | Left-prime `p mod 30` ridge | `mod30_ridge_probe_fresh.json`, `mod30_ridge_lane_summary.json` |
| `detective_state_budget` | State-budget residue cells | `state_budget_lane_summary.json` |
| `detective_rsa` | RSA backward modulus/remainder | `rsa_lane_summary.json`, semiprime closure summary |

```bash
python research/remainders/forensic_verify.py
python -m pytest research/remainders/test_forensic_report.py -q
```