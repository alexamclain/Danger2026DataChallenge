# P25 KSY-y DANGER3 Extraction Surface

Updated: 2026-06-14 11:42 PDT

## Purpose

The H90/Y507 intake identifies live theorem targets, but DANGER3 accepts only a
concrete Pomerance triple:

```text
(p, A, x0)
```

verified by official `vpp.py`.  This note records the extraction surface that
the practical search actually uses.

## Practical X1(16) Surface

For p25:

```text
p = 10^25 + 13
p mod 8 = 5
k = 42
```

The `x16halvenonsplit` practical route starts from an `X_1(16)` parameter `y`.
The Montgomery curve parameter is:

```text
A = N(y) / (4*(y-1)^4)
N(y) =
  y^8 - 8y^7 + 24y^6 - 32y^5 + 8y^4
  + 32y^3 - 48y^2 + 32y - 8
```

The auxiliary model root `x` satisfies:

```text
(y^2 - 2y)*x^2 + (2y^2 - y^3)*x + (1 - y) = 0
```

and the marked `16`-torsion x-coordinate is:

```text
xP16 = x / (x - y)
```

The production mode additionally uses:

```text
nonsplit filter     = (y^2 - 2) * (y^2 - 4y + 2) is nonsquare
first-half gate     = (y - 1) * (y^2 - 2) * (y^2 - 2y + 2) is square
first-half square   = z^2 = (y - 1) * (y^2 - 2) * (y^2 - 2y + 2)
first-half sd       = y*z / (2*(x-y)*(y-1)^2)
```

Then one must choose a valid halving chain from `xP16` down to a concrete `x0`
that passes official `vpp.py`.

## Extraction States

```text
exact P / theta2 / bridge divisor payload:
  missing = map from bridge/theta2 data to Montgomery A and x0

Y_507 or canonical H0 value/divisor payload:
  missing = map from Y507/H0 value to X1(16) y, A, xP16, or x0

X1(16) y, A, xP16 payload:
  missing = valid halving chain to concrete x0

X1(16) y, A, x0 payload:
  missing = official vpp.py verification

direct verified Pomerance triple:
  submission ready
```

## Consequence

The current moonshot gap is no longer just "find a theorem."  A theorem hit
must either:

```text
1. map the KSY/Yang/H0 value to the X1(16) Montgomery surface above, then
   provide or imply a halving chain to x0; or
2. directly output a concrete (p,A,x0) that passes vpp.py.
```

Anything else is theorem progress, but not extraction progress.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_extraction_surface_gate.py
```

Marker:

```text
ksy_y_danger3_extraction_surface_rows=1/1
```
