# Literal Web Hole Trace

This resets the experiment to the original multiplicative-web object: factor threads around N, direct p/q rows held out for audit, and public thread holes left behind by those held-out intersections.

| case | radius | emitted holes | heldout rows | direct rows | supported direct rows | direct hits in emitted holes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| toy_23x31 | 40 | 2 | 64 | 4 | 4 | 2 |
| toy_43x59 | 141 | 8 | 240 | 10 | 10 | 8 |
| toy_61x83 | 282 | 14 | 485 | 14 | 14 | 14 |
| toy_89x113 | 559 | 20 | 980 | 20 | 20 | 20 |

## Per-Case Notes

### toy_23x31

Top supported holes:
- offset -23: support 3, audit `p_thread`
- offset -31: support 2, audit `q_thread`

### toy_43x59

Top supported holes:
- offset 43: support 3, audit `p_thread`
- offset -59: support 3, audit `q_thread`
- offset -43: support 2, audit `p_thread`
- offset 59: support 2, audit `q_thread`
- offset -86: support 2, audit `p_thread`
- offset 118: support 2, audit `q_thread`
- offset -129: support 2, audit `p_thread`
- offset 129: support 2, audit `p_thread`

### toy_61x83

Top supported holes:
- offset 61: support 3, audit `p_thread`
- offset -83: support 3, audit `q_thread`
- offset -61: support 2, audit `p_thread`
- offset 83: support 2, audit `q_thread`
- offset 122: support 2, audit `p_thread`
- offset 166: support 2, audit `q_thread`
- offset -183: support 2, audit `p_thread`
- offset 183: support 2, audit `p_thread`

### toy_89x113

Top supported holes:
- offset 89: support 3, audit `p_thread`
- offset 113: support 3, audit `q_thread`
- offset -267: support 3, audit `p_thread`
- offset -89: support 2, audit `p_thread`
- offset -113: support 2, audit `q_thread`
- offset -178: support 2, audit `p_thread`
- offset 178: support 2, audit `p_thread`
- offset -226: support 2, audit `q_thread`

