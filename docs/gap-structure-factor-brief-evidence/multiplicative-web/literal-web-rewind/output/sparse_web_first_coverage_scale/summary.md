# Sparse Web First-Coverage Scale

Frozen method: presence-only public thread set `2,3,5` with exact-factor top-5 audit scoring.

Benchmark window: `radius = min(p,q)`. Known factors are used only to set first coverage and audit exact recovery. This is not a public RSA controller.

| case | bits | radius | classification | recovered | rank | support | trials |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| continuation_00_131101x144203 | 35 | 131101 | one_factor_success | 131101 | 1 | 2 | 480702 |
| continuation_01_1048583x1153441 | 41 | 1048583 | one_factor_success | 1048583 | 1 | 3 | 3844802 |
| continuation_02_8388617x9227479 | 47 | 8388617 | one_factor_success | 8388617 | 1 | 2 | 30758260 |
| continuation_03_67108879x73819771 | 53 | 67108879 | one_factor_success | 67108879 | 1 | 3 | 246065888 |
| continuation_04_536870923x590558011 | 59 | 536870923 | one_factor_success | 536870923 | 1 | 3 | 1968526716 |
| continuation_05_104869x10485767 | 41 | 104869 | one_factor_success | 104869 | 1 | 2 | 384518 |
| continuation_06_10487x104857601 | 41 | 10487 | one_factor_success | 10487 | 1 | 2 | 38450 |
| continuation_07_6710887x671088667 | 53 | 6710887 | one_factor_success | 6710887 | 1 | 2 | 24606584 |
| continuation_08_671093x6710886407 | 53 | 671093 | one_factor_success | 671093 | 1 | 2 | 2460672 |
| continuation_09_53687099x5368709131 | 59 | 53687099 | one_factor_success | 53687099 | 1 | 3 | 196852694 |
| continuation_10_5368739x53687091251 | 59 | 5368739 | one_factor_success | 5368739 | 1 | 2 | 19685374 |
| scale_00_63bit | 63 | 2147496017 | one_factor_success | 2147496017 | 1 | 3 | 7874152060 |
| scale_01_79bit | 79 | 549755826239 | one_factor_success | 549755826239 | 1 | 2 | 2015771362874 |
| scale_02_95bit | 95 | 140737488367699 | one_factor_success | 140737488367699 | 1 | 3 | 516037457348228 |
| scale_03_111bit | 111 | 36028797018976327 | one_factor_success | 36028797018976327 | 1 | 2 | 132105589069579864 |
| scale_04_127bit | 127 | 9223372036854788173 | one_factor_success | 9223372036854788173 | 1 | 2 | 33819030801800889966 |
| scale_05_159bit | 159 | 604462909807314587365499 | one_factor_success | 604462909807314587365499 | 1 | 2 | 2216364002626820153673494 |
| scale_06_191bit | 191 | 39614081257132168796771987681 | one_factor_success | 39614081257132168796771987681 | 1 | 2 | 145251631276151285588163954828 |
| scale_07_255bit | 255 | 170141183460469231731687303715884118099 | one_factor_success | 170141183460469231731687303715884118099 | 1 | 2 | 623851006021720516349520113624908433028 |

## Result

`19 / 19` benchmark first-coverage cases recovered one exact factor inside the top 5.
This confirms the frozen web arithmetic scales on the measured benchmark surface. The unresolved problem remains the public controller that finds a first-covering window without `p/q`.
