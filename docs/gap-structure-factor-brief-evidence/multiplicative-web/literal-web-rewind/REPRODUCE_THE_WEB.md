# Reproduce The Semiprime Web

A semiprime has a visible neighborhood. The nearby composites have factor
threads. Those threads form intersections around the center number.

The fastest way to reproduce the web is to generate one small visual example,
then run the literal hole-trace reset, then run the frozen public benchmark
audit.

## 1. Clone The Repository

```bash
git clone https://github.com/zfifteen/prime-gap-structure.git
cd prime-gap-structure
```

## 2. Draw One Web

This command draws the exact factor-thread web around `N = 23 * 31`.

```bash
python3 docs/gap-structure-factor-brief-evidence/multiplicative-web/plot_multiplicative_web.py \
  --p 23 \
  --q 31 \
  --radius 40 \
  --out-dir /tmp/pgs-web-23x31

open /tmp/pgs-web-23x31/web.svg
```

The plotting script uses known `p` and `q` to build a visual audit surface. It
shows the web; it is not the public inference runner.

Reference files:

- Web plot script: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/plot_multiplicative_web.py>
- Example SVG output: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/output/toy_23x31_r40/web.svg>
- Example summary: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/output/toy_23x31_r40/summary.md>

## 3. Reproduce The Literal Hole Trace

This reset experiment holds out direct factor-thread rows, then asks which
missing offsets are still supported by public factor threads.

```bash
python3 -m pip install sympy
python3 docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py

open docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/index.html
cat docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/summary.md
```

Reference files:

- Literal trace script: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py>
- Literal trace HTML: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/index.html>
- Literal trace summary: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/summary.md>
- Ladder summary: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/literal_web_hole_trace_ladder/summary.md>

## 4. Reproduce The Public Benchmark Audit

This is the current frozen public benchmark surface for the anchor-confirmed
band runner. The public runner receives only `N`. The private audit checks the
frozen public nominations afterward against known factors.

```bash
cd docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop
python3 audit_anchor_band_expansion.py
cat output/audit_anchor_band_expansion/summary.md
```

Expected summary:

```text
Status: success
toy_23x31: p=23, band rank 7
toy_43x59: p=43, band rank 14
toy_61x83: p=61, band rank 48
toy_89x113: p=89, band rank 28
131101x144203: q=144203, band rank 140
1048583x1153441: p=1048583, band rank 2136
```

The audit output is large because the public nominations are frozen to disk.
The checked-in result directory is about 249 MB.

Reference files:

- Public runner: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/public_anchor_band_runner.py>
- Public policy engine: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/public_loop_policy.py>
- Private audit runner: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/audit_anchor_band_expansion.py>
- Audit summary: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/true-triangulation-iteration-loop/output/audit_anchor_band_expansion/summary.md>

## 5. Read The Visual Explanation

- HTML essay: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/graphical-novel-method/index.html>
- PowerPoint deck: <https://github.com/zfifteen/prime-gap-structure/blob/main/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/graphical-novel-method/the-web-around-a-semiprime.pptx>

## What Counts As Reproduction

The reproduction target is the public web behavior:

- the visual web can be regenerated from a small semiprime;
- the literal hole trace shows held-out factor-thread offsets supported by
  public threads;
- the anchor-confirmed benchmark audit recovers one factor distance in each of
  the six frozen benchmark cases after public nominations are written.

The measured result is a benchmark result. It is not a formal proof.
