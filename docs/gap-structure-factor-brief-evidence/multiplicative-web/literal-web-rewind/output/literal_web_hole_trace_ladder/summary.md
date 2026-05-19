# Literal Web Hole Trace Ladder

Scaling rule: `radius = 6 * p`.
Signal rule: top 18 supported holes must all be held-out `p/q` thread rows.
Feasibility stop: do not run a rung requiring radius > 50000.

| rung | p | q | radius | direct rows | supported direct | top18 direct hits | seconds | status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| rung_00_23x31 | 23 | 31 | 138 | 20 | 20 | 18 | 0.001 | works |
| rung_01_43x59 | 43 | 59 | 258 | 20 | 20 | 18 | 0.002 | works |
| rung_02_61x83 | 61 | 83 | 366 | 20 | 20 | 18 | 0.003 | works |
| rung_03_89x113 | 89 | 113 | 534 | 20 | 20 | 18 | 0.005 | works |
| rung_04_101x137 | 101 | 137 | 606 | 20 | 20 | 18 | 0.005 | works |
| rung_05_131x167 | 131 | 167 | 786 | 20 | 20 | 18 | 0.007 | works |
| rung_06_173x211 | 173 | 211 | 1038 | 20 | 20 | 18 | 0.009 | works |
| rung_07_229x277 | 229 | 277 | 1374 | 20 | 20 | 18 | 0.014 | works |
| rung_08_307x367 | 307 | 367 | 1842 | 22 | 22 | 18 | 0.020 | works |
| rung_09_401x503 | 401 | 503 | 2406 | 20 | 20 | 18 | 0.031 | works |
| rung_10_557x661 | 557 | 661 | 3342 | 22 | 22 | 18 | 0.047 | works |
| rung_11_701x887 | 701 | 887 | 4206 | 20 | 20 | 18 | 0.070 | works |
| rung_12_1009x1231 | 1009 | 1231 | 6054 | 20 | 20 | 18 | 0.123 | works |
| rung_13_1601x2003 | 1601 | 2003 | 9606 | 20 | 20 | 18 | 0.272 | works |
| rung_14_3001x4001 | 3001 | 4001 | 18006 | 20 | 20 | 18 | 0.776 | works |
| rung_15_5003x7001 | 5003 | 7001 | 30018 | 20 | 20 | 18 | 1.666 | works |
| rung_16_6007x8009 | 6007 | 8009 | 36042 | 20 | 20 | 18 | 2.145 | works |
| rung_17_7001x9001 | 7001 | 9001 | 42006 | 20 | 20 | 18 | 2.668 | works |
| rung_18_8009x10007 | 8009 | 10007 | 48054 | 20 | 20 | 18 | 3.343 | works |

## Stop

Stopped before rung_19_9001x11003: required radius 54006 exceeds MAX_RADIUS 50000. Literal hole tracing needs a window that reaches the hidden-thread offsets; at this rung the direct sweep becomes the limiting factor.
