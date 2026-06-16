# P25 KSY-y H0 Order-8112 To X1(16) Chart Specialization

Updated: 2026-06-14 16:05 PDT

## Purpose

The H0 `X_1(8112)` bridge payload contract tells us what same-`j` bridge data
must look like.  This checkpoint says what that bridge must still emit to
become the practical `X_1(16)` surface used by the production search.

## Required Chart

Active production mode:

```text
x16halvenonsplit
start depth = 4
k = 42
active halvings needed = 38
```

Required active formulas:

```text
y != 0, y != 1, y^2-2y != 0, x-y != 0
(y^2-2y)*x^2 + (2y^2-y^3)*x + (1-y) = 0
D=(2y^2-y^3)^2 - 4*(y^2-2y)*(1-y) must be square
A=N(y)/(4*(y-1)^4)
N=y^8-8y^7+24y^6-32y^5+8y^4+32y^3-48y^2+32y-8
xP16=x/(x-y)
(y^2-2)*(y^2-4y+2) is nonsquare
```

Optional d-gate surface:

```text
x16halvenonsplitdgate
start depth = 5
optional halvings needed = 37
(y-1)*(y^2-2)*(y^2-2y+2) is square
sd=y*z/(2*(x-y)*(y-1)^2)
```

## Route Rows

```text
order-8112 bridge only:
  decision = order8112_bridge_not_practical_chart

order-8112 bridge with y only:
  decision = y_chart_missing_model_root

order-8112 bridge with y, model root x, A, xP16:
  decision = active_surface_reached_halving_missing

order-8112 bridge with direct A and xP16:
  decision = active_surface_reached_halving_missing

order-8112 bridge with optional first-half d-gate:
  decision = optional_depth5_surface_reached_halving_missing

order-8112 bridge with A, xP16, and x0:
  decision = extraction_ready_vpp_missing

officially verified triple:
  decision = submission_ready
```

## Counts

```text
formula_count                 = 10
active_formula_rows           = 7
optional_dgate_formula_rows   = 3
route_count                   = 7
order8112_bridge_rows         = 7
chart_surface_rows            = 5
optional_dgate_rows           = 1
extraction_ready_rows         = 2
submission_ready_rows         = 1
```

## Interpretation

An order-`8112` bridge is still too abstract until it emits the practical
chart variables.  The shortest active submission path is:

```text
order-8112 H0 bridge
  -> y, x, A, xP16 or direct A,xP16
  -> 38 depth-4 halvings or direct x0
  -> official vpp.py
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_order8112_x16_chart_specialization_gate.py
```

Marker:

```text
ksy_y_h0_order8112_x16_chart_specialization_rows=1/1
```
