# Square Record Anatomy: 424171123

## Purpose

This note dissects the active square-envelope utilization record:

```text
p = 424,171,123
p^2 = 179,921,141,587,081,129
```

The goal is local anatomy only: explain how this square got close to the
dynamic cutoff boundary without crossing it.

## Record Geometry

| Object | Value |
|---|---:|
| Root p | `424,171,123` |
| Square p^2 | `179,921,141,587,081,129` |
| Previous prime q | `179,921,141,587,080,391` |
| Next prime after q | `179,921,141,587,081,189` |
| Gap size | `798` |
| Square offset | `738` |
| Cutoff | `790` |
| Margin | `52` |
| Utilization | `0.9341772151898734` |
| First-open offset | `6` |

The cutoff lies at offset `790`, while the next prime lies at offset `798`.
So the selected witness is inside the cutoff even though the right endpoint is
outside it.

## Local Witness Table

| Offset | n = q + offset | d(n) | Classification | Selected |
|---:|---:|---:|---|---|
| `3` | `179,921,141,587,080,394` | `4` | `d=4` | `no` |
| `6` | `179,921,141,587,080,397` | `4` | `d=4` | `no` |
| `7` | `179,921,141,587,080,398` | `4` | `d=4` | `no` |
| `10` | `179,921,141,587,080,401` | `4` | `d=4` | `no` |
| `18` | `179,921,141,587,080,409` | `4` | `d=4` | `no` |
| `24` | `179,921,141,587,080,415` | `4` | `d=4` | `no` |
| `31` | `179,921,141,587,080,422` | `4` | `d=4` | `no` |
| `36` | `179,921,141,587,080,427` | `4` | `d=4` | `no` |
| `38` | `179,921,141,587,080,429` | `4` | `d=4` | `no` |
| `56` | `179,921,141,587,080,447` | `4` | `d=4` | `no` |
| `60` | `179,921,141,587,080,451` | `4` | `d=4` | `no` |
| `78` | `179,921,141,587,080,469` | `4` | `d=4` | `no` |
| `732` | `179,921,141,587,081,123` | `8` | `other` | `no` |
| `733` | `179,921,141,587,081,124` | `12` | `other` | `no` |
| `734` | `179,921,141,587,081,125` | `768` | `other` | `no` |
| `735` | `179,921,141,587,081,126` | `8` | `other` | `no` |
| `736` | `179,921,141,587,081,127` | `8` | `other` | `no` |
| `737` | `179,921,141,587,081,128` | `256` | `other` | `no` |
| `738` | `179,921,141,587,081,129` | `3` | `square` | `yes` |
| `739` | `179,921,141,587,081,130` | `64` | `other` | `no` |
| `740` | `179,921,141,587,081,131` | `16` | `other` | `no` |
| `741` | `179,921,141,587,081,132` | `24` | `other` | `no` |
| `742` | `179,921,141,587,081,133` | `16` | `other` | `no` |
| `743` | `179,921,141,587,081,134` | `48` | `other` | `no` |
| `744` | `179,921,141,587,081,135` | `4` | `d=4` | `no` |

## Answers

1. The exact local gap is from
   `179,921,141,587,080,391` to `179,921,141,587,081,189`.
2. The previous right prime is `q = 179,921,141,587,080,391`.
3. The next prime after `q` is `179,921,141,587,081,189`.
4. The square sits at offset `738` inside a gap of width `798`.
5. The first nearby `d=4` carriers occur at offsets `3`, `6`, `7`, `10`,
   `18`, `24`, `31`, `36`, `38`, `56`, `60`, and `78`; another nearby
   `d=4` carrier occurs at offset `744`, after the square.
6. The square beats the first `d=4` carrier because `d(p^2) = 3`, while the
   first carrier has divisor count `4`.
7. The first-open offset is `6`.
8. Before the square, there are `96` interior `d=4` carriers and no interior
   divisor-count carrier below `4`.
9. This square became the standing utilization record because the previous
   prime lies `738` before the square, while the dynamic cutoff is `790`.
   The square is late enough to stress the cutoff, but still `52` offsets
   inside it.
10. Falsification at this local scale would have required the previous prime
    to sit more than `790` before the square, so that the square offset was at
    least `791`.

## Status

This is a finite local anatomy note, not a proof of the square-offset envelope.
It turns the current record into a concrete mechanism:

```text
many early d=4 carriers -> late prime square with d=3 -> square wins inside cutoff
```
