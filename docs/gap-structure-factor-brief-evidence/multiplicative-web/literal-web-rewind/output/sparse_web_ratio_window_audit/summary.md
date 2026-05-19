# Sparse Web Ratio Window Audit

Frozen method: presence-only public thread set `2,3,5` with exact-factor top-5 audit scoring.

Benchmark variable: `radius = ratio * min(p,q)`. This uses known factors only to measure the safe ratio band; it is not a public RSA-scale controller.

| case | bits | first success ratio | last success ratio | first failure after success | recovered at first success | rank |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| toy_23x31 | 10 | 1 | 128 |  | 23 | 1 |
| toy_43x59 | 12 | 1 | 128 |  | 43 | 1 |
| toy_61x83 | 13 | 1 | 128 |  | 61 | 1 |
| toy_89x113 | 14 | 1 | 128 |  | 89 | 1 |
| rung_04_101x137 | 14 | 1 | 40 | 48 | 101 | 1 |
| rung_05_131x167 | 15 | 1 | 40 | 48 | 131 | 1 |
| rung_06_173x211 | 16 | 1 | 128 |  | 173 | 1 |
| rung_07_229x277 | 16 | 1 | 32 | 40 | 229 | 1 |
| rung_08_307x367 | 17 | 1 | 32 | 40 | 307 | 1 |
| rung_09_401x503 | 18 | 1 | 32 | 40 | 401 | 1 |
| rung_10_557x661 | 19 | 1 | 128 |  | 557 | 1 |
| rung_11_701x887 | 20 | 1 | 40 | 48 | 701 | 1 |
| rung_12_1009x1231 | 21 | 1 | 128 |  | 1009 | 1 |
| rung_13_1601x2003 | 22 | 1 | 32 | 40 | 1601 | 1 |
| rung_14_3001x4001 | 24 | 1 | 128 |  | 3001 | 1 |
| rung_15_5003x7001 | 26 | 1 | 40 | 48 | 5003 | 1 |
| rung_16_6007x8009 | 26 | 1 | 128 |  | 6007 | 1 |
| rung_17_7001x9001 | 26 | 1 | 128 |  | 7001 | 1 |
| rung_18_8009x10007 | 27 | 1 | 128 |  | 8009 | 1 |
| rung_19_9001x11003 | 27 | 1 | 128 |  | 9001 | 1 |
| rung_20_7500013x29999989 | 48 | 1 | 48 | 56 | 7500013 | 1 |
| continuation_00_131101x144203 | 35 | 1 | 128 |  | 131101 | 1 |
| continuation_01_1048583x1153441 | 41 | 1 | 128 |  | 1048583 | 1 |
| continuation_02_8388617x9227479 | 47 | 1 | 40 | 48 | 8388617 | 1 |
| continuation_03_67108879x73819771 | 53 | 1 | 128 |  | 67108879 | 1 |
| continuation_04_536870923x590558011 | 59 | 1 | 128 |  | 536870923 | 1 |
| continuation_05_104869x10485767 | 41 | 1 | 64 | 80 | 104869 | 1 |
| continuation_06_10487x104857601 | 41 | 1 | 64 | 80 | 10487 | 1 |
| continuation_07_6710887x671088667 | 53 | 1 | 64 | 80 | 6710887 | 1 |
| continuation_08_671093x6710886407 | 53 | 1 | 64 | 80 | 671093 | 1 |
| continuation_09_53687099x5368709131 | 59 | 1 | 128 |  | 53687099 | 1 |
| continuation_10_5368739x53687091251 | 59 | 1 | 64 | 80 | 5368739 | 1 |

## Result

First observed post-success failure ratio: `40`.
The adaptive controller target is therefore not a large fixed window. It is a small covering window near the first success ratio, with a measured upper danger band recorded separately.
