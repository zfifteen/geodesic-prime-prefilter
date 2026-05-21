# Literal Web Breakpoint Ladder

Per-rung feasibility bound: `180s`.

Method: `radius = floor(sqrt(N))`; emit the max-support shell; audit checks whether `abs(offset)` equals `p` or `q` after emission.

| stage | rung | bits | radius | max support | emitted holes | factor hit | seconds | classification |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| coarse | rung_00_23x31 | 10 | 26 | 3 | 1 | yes | 0.221 | success |
| coarse | rung_01_43x59 | 12 | 50 | 3 | 1 | yes | 0.211 | success |
| coarse | rung_02_61x83 | 13 | 71 | 3 | 1 | yes | 0.214 | success |
| coarse | rung_03_89x113 | 14 | 100 | 3 | 1 | yes | 0.211 | success |
| coarse | rung_04_101x137 | 14 | 117 | 3 | 1 | yes | 0.214 | success |
| coarse | rung_05_131x167 | 15 | 147 | 3 | 1 | yes | 0.217 | success |
| coarse | rung_06_173x211 | 16 | 191 | 4 | 1 | yes | 0.211 | success |
| coarse | rung_07_229x277 | 16 | 251 | 3 | 1 | yes | 0.212 | success |
| coarse | rung_08_307x367 | 17 | 335 | 3 | 1 | yes | 0.214 | success |
| coarse | rung_09_401x503 | 18 | 449 | 3 | 1 | yes | 0.220 | success |
| coarse | rung_10_557x661 | 19 | 606 | 4 | 1 | yes | 0.220 | success |
| coarse | rung_11_701x887 | 20 | 788 | 3 | 1 | yes | 0.220 | success |
| coarse | rung_12_1009x1231 | 21 | 1114 | 4 | 1 | yes | 0.232 | success |
| coarse | rung_13_1601x2003 | 22 | 1790 | 4 | 1 | yes | 0.259 | success |
| coarse | rung_14_3001x4001 | 24 | 3465 | 4 | 1 | yes | 0.350 | success |
| coarse | rung_15_5003x7001 | 26 | 5918 | 3 | 2 | yes | 0.525 | success |
| coarse | rung_16_6007x8009 | 26 | 6936 | 4 | 2 | yes | 0.612 | success |
| coarse | rung_17_7001x9001 | 26 | 7938 | 3 | 2 | yes | 0.691 | success |
| coarse | rung_18_8009x10007 | 27 | 8952 | 3 | 1 | yes | 0.783 | success |
| coarse | rung_19_9001x11003 | 27 | 9951 | 4 | 1 | yes | 0.867 | success |
| coarse | rung_20_12007x14009 | 28 | 12969 | 4 | 1 | yes | 1.168 | success |
| coarse | rung_21_16001x18013 | 29 | 16977 | 4 | 1 | yes | 1.603 | success |
| coarse | rung_22_20011x24001 | 29 | 21915 | 3 | 2 | yes | 2.155 | success |
| coarse | rung_23_30011x36007 | 31 | 32872 | 4 | 1 | yes | 3.823 | success |
| coarse | rung_24_40009x48017 | 31 | 43830 | 4 | 1 | yes | 5.470 | success |
| coarse | rung_25_50021x60013 | 32 | 54789 | 3 | 2 | yes | 7.409 | success |
| coarse | rung_26_75011x90001 | 33 | 82164 | 3 | 2 | yes | 12.883 | success |
| coarse | rung_27_100003x120011 | 34 | 109551 | 4 | 2 | yes | 18.725 | success |
| coarse | rung_28_131101x144203 | 35 | 137496 | 4 | 1 | yes | 25.249 | success |
| coarse | rung_29_160001x180001 | 35 | 169706 | 3 | 1 | yes | 33.898 | success |
| coarse | rung_30_200003x240007 | 36 | 219093 | 5 | 1 | yes | 45.798 | success |
| coarse | rung_31_300007x360007 | 37 | 328640 | 4 | 1 | yes | 76.257 | success |
| coarse | rung_32_500009x600011 | 39 | 547732 | 4 | 2 | yes | 144.991 | success |
| coarse | rung_33_750019x900001 | 40 | 821594 |  |  | no | 180.004 | feasibility_break |

## Breakpoint

Last success: `rung_32_500009x600011`.
First break: `rung_33_750019x900001`.
Break type: `feasibility_break`.
