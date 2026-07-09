# Remainder Research Super Team: Manifest

**Team name:** Remainder Research Super Team  
**Orchestrator:** `research/remainders/run_investigation.py`  
**Roster source:** `research/remainders/super_team.py`

The objective's "Super Team" is implemented as **six named lane agents** dispatched by the orchestrator. Each agent owns one remainder lane, runs a collector (subprocess or stream), and writes a pinned artifact. Per-run agent status is logged to `correlations/investigation/SUPER_TEAM_RUN.json`.

| Agent ID | Lane | Collector |
|----------|------|-----------|
| `interior_rnm` | Interior `R(n,M)` | `collect_remainder_stats.py` |
| `super_signal_status` | GWR Super-Signal (epistemic) | inline in orchestrator |
| `endpoint_mask` | Endpoint wheel-open mask | `lane_collectors/endpoint_residue_probe.py` |
| `mod30_ridge` | Left-prime mod-30 ridge | `lane_collectors/mod30_ridge_probe.py` |
| `state_budget` | State-budget residue cells | `state_budget_residue_matched_pair_test.py` |
| `rsa_backward` | RSA backward modulus/remainder | `pgs_semiprime_backward_invariant_closure_search.py` |

```bash
python research/remainders/run_investigation.py --run-slow-lanes
```