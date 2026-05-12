#!/usr/bin/env python3
import csv
import statistics
import subprocess
import time
from pathlib import Path

ROOT = Path('/Users/velocityworks/IdeaProjects/prime-gap-structure')
PGS = ROOT / 'src/c/high-scale-pgs/bin/pgs_cli'
Z5D = Path('/Users/velocityworks/IdeaProjects/archive/z5d-prime-predictor/src/c/z5d-predictor-c/bin/z5d_cli')
OUT = ROOT / 'research/01-generator/output/performance_comparisons/pgs_vs_z5dp_cli.csv'
SCALES = [3, 6, 9, 12, 15, 16, 1233]
REPS = 3
TIMEOUT_SECONDS = 90

def run_one(name, cmd):
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
        elapsed = (time.perf_counter() - t0) * 1000.0
        return {
            'tool': name,
            'status': proc.returncode,
            'elapsed_ms': elapsed,
            'stdout_bytes': len(proc.stdout),
            'stderr_bytes': len(proc.stderr),
            'stderr_preview': proc.stderr[:160].decode('utf-8', 'replace').replace('\n', ' '),
        }
    except subprocess.TimeoutExpired:
        return {
            'tool': name,
            'status': 'timeout',
            'elapsed_ms': TIMEOUT_SECONDS * 1000.0,
            'stdout_bytes': 0,
            'stderr_bytes': 0,
            'stderr_preview': 'timeout',
        }

rows = []
for e in SCALES:
    pgs_arg = f'10^{e}'
    z5d_arg = '1' + ('0' * e)
    for rep in range(1, REPS + 1):
        for name, cmd, contract in [
            ('pgs_cli', [str(PGS), pgs_arg], 'next_prime_after_anchor'),
            ('z5d_cli', [str(Z5D), z5d_arg], 'nth_prime_predictor'),
        ]:
            result = run_one(name, cmd)
            rows.append({
                'scale_exp': e,
                'input': pgs_arg if name == 'pgs_cli' else f'10^{e}',
                'rep': rep,
                'tool': result['tool'],
                'contract': contract,
                'status': result['status'],
                'elapsed_ms': f"{result['elapsed_ms']:.3f}",
                'stdout_bytes': result['stdout_bytes'],
                'stderr_bytes': result['stderr_bytes'],
                'stderr_preview': result['stderr_preview'],
            })

with OUT.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

summary_path = ROOT / 'research/01-generator/output/performance_comparisons/pgs_vs_z5dp_cli_summary.csv'
summary_rows = []
for e in SCALES:
    for tool in ['pgs_cli', 'z5d_cli']:
        sample = [r for r in rows if r['scale_exp'] == e and r['tool'] == tool]
        good = [float(r['elapsed_ms']) for r in sample if str(r['status']) == '0']
        statuses = sorted(set(str(r['status']) for r in sample))
        summary_rows.append({
            'scale_exp': e,
            'tool': tool,
            'contract': sample[0]['contract'],
            'successful_runs': len(good),
            'statuses': '|'.join(statuses),
            'min_ms': f"{min(good):.3f}" if good else '',
            'median_ms': f"{statistics.median(good):.3f}" if good else '',
            'max_ms': f"{max(good):.3f}" if good else '',
            'stdout_bytes_last': sample[-1]['stdout_bytes'],
            'stderr_preview_last': sample[-1]['stderr_preview'],
        })
with summary_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()), lineterminator='\n')
    writer.writeheader()
    writer.writerows(summary_rows)

print(summary_path)
with summary_path.open() as f:
    print(f.read())
