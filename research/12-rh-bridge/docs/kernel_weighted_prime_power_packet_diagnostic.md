# Kernel-Weighted Prime-Power Packet Diagnostic

Date: 2026-05-24

Status: deterministic finite diagnostic for the Kernel-Weighted Prime-Power Packet Estimate.

## Scope

- Prime endpoint limit: `q <= 1000000`.
- Nonempty chambers checked: `78496`.
- Chambers with interior prime-power packet mass: `231`.
- Z grid: `1.000000e-12, 1.000000e-10, 1.000000e-08, 1.000000e-06, 1.000000e-04, 0.001, 0.01, 0.1, 1, 10`.

For each chamber, the packet is the endpoint prime plus all interior prime powers.
The diagnostic computes

$$
\frac{|D_{p,q}(z)|}{R_{p,q}(z)}
$$

with

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n),
\qquad
R_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)K_z(x_n).
$$

Since $J_z(x)=xK_z(x)$ and all packet weights are nonnegative,
`D/R` is a weighted average of the centered coordinates `x_n`. Thus

$$
\frac{|D_{p,q}(z)|}{R_{p,q}(z)}\le \max_{n\in P(p,q)}|x_n|.
$$

## Global Worst Case

- `p=3`, `q=5`, `w=4`, `z=10`, `ratio=0.187939118`, `max_abs_x=0.255412812`, `selector=selector_prime_power`, `pp_bucket=largest_pp_right_of_center`, `largest_pp=4`, `largest_pp_x=0.032269261`

## Worst Case By Z

| z | worst ratio | chamber | selector type | largest interior prime-power position | max_abs_x |
|---:|---:|---|---|---|---:|
| `1.000000e-12` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `1.000000e-10` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `1.000000e-08` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `1.000000e-06` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `1.000000e-04` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `0.001` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `0.01` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `0.1` | `0.168236118` | `(5,7]` | `selector_composite` | `no_interior_prime_power` / `none` | `0.168236118` |
| `1` | `0.185286022` | `(3,5]` | `selector_prime_power` | `largest_pp_right_of_center` / `0.032269261` | `0.255412812` |
| `10` | `0.187939118` | `(3,5]` | `selector_prime_power` | `largest_pp_right_of_center` / `0.032269261` | `0.255412812` |

## Worst Case By Selector Type

| selector type | worst ratio | chamber | z | largest interior prime power | largest_pp_x |
|---|---:|---|---:|---:|---:|
| `selector_composite` | `0.168236118` | `(5,7]` | `0.1` | `none` | `none` |
| `selector_prime_power` | `0.187939118` | `(3,5]` | `10` | `4` | `0.032269261` |

## Worst Case By Largest Interior Prime-Power Position

| position bucket | worst ratio | chamber | z | selector type | largest interior prime power | largest_pp_x |
|---|---:|---|---:|---|---:|---:|
| `largest_pp_left_of_center` | `0.065075513` | `(31,37]` | `10` | `selector_composite` | `32` | `-0.056716656` |
| `largest_pp_right_of_center` | `0.187939118` | `(3,5]` | `10` | `selector_prime_power` | `4` | `0.032269261` |
| `no_interior_prime_power` | `0.168236118` | `(5,7]` | `0.1` | `selector_composite` | `none` | `none` |

## Top Ten Realized Ratios

1. `p=3`, `q=5`, `w=4`, `z=10`, `ratio=0.187939118`, `max_abs_x=0.255412812`, `selector=selector_prime_power`, `pp_bucket=largest_pp_right_of_center`, `largest_pp=4`, `largest_pp_x=0.032269261`
2. `p=3`, `q=5`, `w=4`, `z=1`, `ratio=0.185286022`, `max_abs_x=0.255412812`, `selector=selector_prime_power`, `pp_bucket=largest_pp_right_of_center`, `largest_pp=4`, `largest_pp_x=0.032269261`
3. `p=5`, `q=7`, `w=6`, `z=0.1`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
4. `p=5`, `q=7`, `w=6`, `z=10`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
5. `p=5`, `q=7`, `w=6`, `z=1.000000e-12`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
6. `p=5`, `q=7`, `w=6`, `z=1.000000e-10`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
7. `p=5`, `q=7`, `w=6`, `z=1.000000e-08`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
8. `p=5`, `q=7`, `w=6`, `z=1.000000e-06`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
9. `p=5`, `q=7`, `w=6`, `z=1.000000e-04`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`
10. `p=5`, `q=7`, `w=6`, `z=0.001`, `ratio=0.168236118`, `max_abs_x=0.168236118`, `selector=selector_composite`, `pp_bucket=no_interior_prime_power`, `largest_pp=none`, `largest_pp_x=none`

## Finding

The finite surface does not falsify the kernel-weighted packet estimate.
The worst observed ratio is controlled by the endpoint-only early chamber
and every measured case obeys the structural bound by `max_abs_x`.

The diagnostic also shows that the current arithmetic target can be sharpened:
before completion, `|D|/R` is exactly the absolute value of a positive
`K_z`-weighted average of local centered packet coordinates.
