# Lane B: Bridge Hilbert-90 Source-Chain Corner Unit Quadratic

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_quadratic_gate.py`

## Result

The unit-fiber selector also determines the full quadratic residual after the
forced slope-one line is subtracted.

Let `eps` be the primitive `D`-unit sign and `a` the branch coefficient:

```text
eps = +1 for q=172, eps = -1 for q=335
a   = -1 for q=197, a   = +1 for q=310
```

In signed `F_13` coordinates:

```text
x_c = 3*eps
y_c = (eps - 1)/2
x_n = x_c + 2*a
s   = y_c - x_c
```

The line-subtracted residual is:

```text
R_{eps,a}(x) = lambda_{eps,a} * (x - x_c) * (x - x_n)
lambda_{eps,a} = -1 + 2*eps - a + eps*a
```

Adding the forced line back gives the active fiber section:

```text
f_{eps,a}(x) = x + s + R_{eps,a}(x)
```

This recovers all four active `C_13`-to-`C_169` quadratic sections exactly,
including both roots and the leading scalar.

## Interpretation

The local producer target has tightened again:

```text
primitive D-unit sign eps
  -> branch coefficient a
  -> two-sign quadratic residual R_{eps,a}
  -> forced slope-one line
  -> active C_169 fiber section
  -> coefficient-selected diagonal neighbor
  -> signed S=172 bridge image
```

The scalar in the residual is no longer independent data. A candidate producer
that recovers the roots but chooses a different quadratic scalar fails this
gate.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_unit_quadratic_rows=1/1
```
