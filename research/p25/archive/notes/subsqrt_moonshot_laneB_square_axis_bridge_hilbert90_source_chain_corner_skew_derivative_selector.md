# Lane B: Bridge Hilbert-90 Source-Chain Corner Skew-Derivative Selector

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_gate.py`

## Result

Scanning all `506` nonzero source translations for each active corner gives a
sharp twofold near miss.

The only skew derivatives with:

```text
one Newton-vertex cancellation
two primitive row-local C_169 residual edges
residual short lengths 31 and 53
```

are the two directions:

```text
q directions: 197 and 310
D directions: 122 and 385
```

The recorded direction is the unique one whose half-potential also satisfies
the Hilbert-90 bridge-pair orientation and inverts to the signed bridge.  The
opposite `197/310` short derivative is a real near miss in all four active
rows.

The `q=0` endpoint condition is not enough: in two of the four active rows,
both short skew derivatives contain the `q=0` endpoint.

## Interpretation

The producer target has tightened again:

```text
row-quadratic source corner
  -> oriented 197/310 skew derivative
  -> one canceled Newton vertex
  -> selected 31/53 residual edges
  -> Hilbert-90 bridge-pair orientation
  -> signed S-layer bridge
```

A candidate that produces the right row-quadratic corner and a `31/53` short
skew derivative can still be wrong by choosing the opposite half-boundary.  The
bridge-pair orientation is part of the finite contract.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_skew_derivative_selector_rows=1/1
```
