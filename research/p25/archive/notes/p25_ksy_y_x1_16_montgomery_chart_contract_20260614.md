# P25 KSY-y X1(16) Montgomery-Chart Contract

Updated: 2026-06-14 12:04 PDT

## Purpose

The `X_1(8112)` torsion-gluing contract can produce an exact `16`-torsion
component on the same curve as the odd KSY/Yang/H90 target.  The practical
search still needs that component in the actual Montgomery chart used by
`src/pomerance.c`.

This note separates:

```text
abstract exact P16 torsion
```

from:

```text
practical X_1(16) y/x/A/xP16 extraction data
```

## Active Production Surface

The active production mode is:

```text
x16halvenonsplit
```

It starts the halving chain at:

```text
halve_chain_from_depth(A, xP16, depth=4, k=42)
```

The active surface requires:

```text
y != 0
y != 1
y^2 - 2y != 0
x - y != 0

(y^2-2y)*x^2 + (2y^2-y^3)*x + (1-y) = 0
D=(2y^2-y^3)^2 - 4*(y^2-2y)*(1-y) square

A=N(y)/(4*(y-1)^4)
N=y^8-8y^7+24y^6-32y^5+8y^4+32y^3-48y^2+32y-8

xP16 = x/(x-y)

(y^2-2)*(y^2-4y+2) nonsquare
```

Equivalently, a theorem may bypass `y` and emit the direct practical payload:

```text
A, xP16
```

but then it still needs the halving chain to `x0`.

## Optional D-Gate Surface

The stronger optional mode is:

```text
x16halvenonsplitdgate
```

It uses one certified first half and starts the remaining halving at:

```text
halve_chain_from_depth(A, x32, depth=5, k=42)
```

The extra optional data are:

```text
(y-1)*(y^2-2)*(y^2-2y+2) square
z^2=(y-1)*(y^2-2)*(y^2-2y+2)
sd=y*z/(2*(x-y)*(y-1)^2)
```

This is not required by the active `x16halvenonsplit` production route.

## Route Classifier

```text
same-curve abstract P16:
  decision = abstract_p16_not_practical_chart
  missing  = X_1(16) y-chart parameter or direct A,xP16

X_1(16) y only:
  decision = y_chart_missing_model_root
  missing  = model root x satisfying the X_1(16) quadratic

y and model root:
  decision = active_surface_reached_halving_missing
  missing  = halve chain from xP16 at depth 4 to x0

direct A,xP16:
  decision = active_surface_reached_halving_missing
  missing  = halve chain from xP16 at depth 4 to x0

d-gate first-half surface:
  decision = optional_depth5_surface_reached_halving_missing
  missing  = halve chain from x32 at depth 5 to x0
```

## Consequence

A cross-level theorem does not have to produce the optional first-half `z/sd`
data.  For the active production route, it is enough to emit either:

```text
y and model root x, hence A and xP16
```

or directly:

```text
A and xP16
```

Then the remaining obligation is the halving chain to `x0` and official
`vpp.py` verification.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_16_montgomery_chart_contract_gate.py
```

Marker:

```text
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
```
