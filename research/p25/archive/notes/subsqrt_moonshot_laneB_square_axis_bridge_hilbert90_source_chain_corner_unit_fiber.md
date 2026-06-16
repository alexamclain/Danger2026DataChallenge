# Lane B: Bridge Hilbert-90 Source-Chain Corner Unit Fiber

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_fiber_gate.py`

## Result

The cancellation-line selector reduces to a two-sign local formula.

Let `eps` be the primitive `D`-coordinate sign of the cancellation unit vertex:

```text
eps = +1 for q=172
eps = -1 for q=335
```

Let `a` be the branch coefficient:

```text
a = -1 for q=197
a = +1 for q=310
```

In signed `F_13` low/fiber coordinates:

```text
cancellation = (3*eps, (eps - 1)/2)
intercept    = fiber - low
neighbor     = cancellation + 2*a*(1,1)
tangent      = -2*a*(1,1)
```

After multiplying by the branch coefficient, the recorded tangent is always:

```text
(-2,-2)
```

## Interpretation

The staged selector is now:

```text
primitive D-unit sign eps
  -> cancellation low/fiber point
  -> slope-one line through that unit point
  -> branch coefficient a
  -> coefficient-selected diagonal neighbor
  -> recorded edge back to the cancellation point
  -> signed S=172 bridge image
```

This makes the cancellation line less like a fitted geometric coincidence and
more like a producer-facing local law. A candidate arithmetic producer should
recover the primitive unit vertex and branch sign; separately choosing the
line intercept, neighbor, or tangent is now an explicit failure mode.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_unit_fiber_rows=1/1
```
