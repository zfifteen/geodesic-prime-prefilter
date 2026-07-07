---
name: log-analyzer
description: Analyze previous PGS Research Director job logs for patterns, failures, slow paths, self-review opportunities, and PGS framing fidelity. Used for autonomous improvement of crons, skills, and prompts.
---
# Log Analyzer for Self-Review

## Usage
node skills/log-analyzer/log-analyzer.cjs [log_dir_or_glob]
# Scans recent logs, emits summary + improvement suggestions.
