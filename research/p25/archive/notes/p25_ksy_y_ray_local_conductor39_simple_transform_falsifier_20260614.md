# P25 KSY-y: Ray-Local / Conductor-39 Simple-Transform Falsifier

Updated: 2026-06-14 17:31 PDT

## Purpose

The alignment gate showed that the conductor-`39` source
`U_chi=-chi_3*chi_13` is not the ray-local `theta31` finite payload.  This
checkpoint turns that into a narrower executable falsifier:

```text
Can U_chi be turned into theta31 by a cheap local transform?
```

The checked answer is no for the natural cheap classes:

```text
scalar/sign multiple
product-affine relabel on C_3 x C_13
product-affine relabel plus scalar
row-plus-column additive normalization
separated row/C-axis multiplicative gauge
```

This does not kill the conductor-`39` route.  A genuine finite value/divisor
theorem for `U_chi`, `W`, `Y_507`, or `H0` remains live source progress.  The
falsifier only rejects shortcuts that try to avoid a real bridge or evaluation
theorem.

## Computation

On the common `C_3 x C_13` quotient:

```text
theta31 support        = 18
U_chi support          = 24
theta31 mixed rank     = 2
U_chi rank             = 1
combined mixed rank    = 3
```

All product-affine maps

```text
(r,c) -> (a*r+b mod 3, u*c+v mod 13)
```

were scanned, with `a` a unit mod `3` and `u` a unit mod `13`:

```text
maps checked                         = 936
exact theta support matches          = 0
exact theta-mixed support matches    = 0
max theta support intersection       = 12
max theta-mixed support intersection = 12
theta intersection histogram         = ((10,288), (11,288), (12,360))
theta-mixed intersection histogram   = ((10,432), (12,504))
```

The row-plus-column additive ansatz

```text
target(r,c) = a*U_chi(r,c) + row(r) + col(c)
```

is inconsistent over `Q` for both raw `theta31` and its row/column-free mixed
projection:

```text
raw theta31:
  equations=39 variables=16 rank=16 inconsistent_rows=8 residuals={-1,1}

mixed theta31:
  equations=39 variables=16 rank=16 inconsistent_rows=8 residuals={-3,3}
```

Separated multiplicative gauges preserve mixed rank at most `1`, while
`theta31` has mixed rank `2`.

## Consequence

A future claim of the form:

```text
Koo-Shin 6.2 certifies U_chi, therefore we already have theta31
```

has a concrete first falsifier.  It must provide an explicit bridge/evaluation
theorem that resolves the support/rank/orthogonality obstruction.  Bare
renaming, affine relabeling, row/column normalization, or separated character
gauges are not enough.

The live ask is still:

```text
finite-field value/divisor identity for U_chi, W, Y_507, or H0
plus DANGER3-compatible framing and extraction
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ray_local_conductor39_simple_transform_falsifier_gate.py
```

Marker:

```text
ksy_y_ray_local_conductor39_simple_transform_falsifier_rows=1/1
```
