# P25 Lane B: Robert KSY / Kato-Siegel theta2 Even-D Gate

Updated: 2026-06-13 14:25 PDT

## Purpose

The lit scout identified the classical identity behind the current finite
footprint:

```text
wp'(z) = -sigma(2z) / sigma(z)^4
theta_2(Q) ~ g(Q)^4 / g(2Q)
```

This gate tests whether the even-`D` / `theta_2` interpretation gives a free
finite escape from the doubled-layer obstruction.

## Result

It does not.

```text
theta2 inverse footprint = double_pushforward(bridge) - 4*bridge
theta2 footprint         = 4*bridge - double_pushforward(bridge)
support                  = 300
coefficient counts       = (-4,75), (-1,75), (1,75), (4,75)
```

The finite source group is `C_75 x C_169`, so multiplication by `2` has trivial
kernel.  The `theta_2` norm over the `[2]` kernel is therefore just `theta_2`
again, and inverse-doubling transport only relabels the same 300-cell
footprint.

Square-root-style normalization also fails in the exponent footprint:

```text
theta2 integral square root exists         = false
theta2 inverse integral square root exists = false
dlog integral half exists                  = true
half-dlog support                          = 300
```

For the half-dlog scan, only subtracting one doubled layer reduces support:

```text
half_dlog + lambda*doubled, -4 <= lambda <= 4
only lambda=-1 reduces support to 150
lambda=-1 gives -2*bridge; exact divide by -2 recovers bridge
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_even_gate.py
```

Expected marker:

```text
robert_ksy_theta2_even_rows=1/1
```

## Interpretation

The even-`D` / `theta_2` route remains a precise theorem target, but it needs a
real extra identity.  A formal `[2]` norm, `[2]` transport, integral square
root, or half-dlog normalization does not remove the doubled `g(2Q)` layer.
