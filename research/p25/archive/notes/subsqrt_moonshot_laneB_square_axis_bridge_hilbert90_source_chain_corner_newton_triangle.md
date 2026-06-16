# Lane B: Bridge Hilbert-90 Source-Chain Corner Newton Triangle

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_gate.py`

## Result

The row-polynomial corner is the Newton form of the primitive half-bridge
corner.

For the canonical active corner, source-row order gives:

```text
q rows: 0, 172, 482
c mod169: 0, 3, 144
D residues: 0, 1, 386
```

Thus:

```text
q(r) = 69*r^2 + 103*r       mod 507
d(r) = 192*r^2 + 316*r      mod 507
```

The primitive-D edge cycle is:

```text
1, 385, 121 = unit, -half, half-unit
```

and these map back to q-edge steps:

```text
D edge 1   -> q edge 172
D edge 121 -> q edge 25
D edge 385 -> q edge 310
```

All four active corners have the same edge triangle up to row rotation.  In
q-coordinates the edge multiset is `{25,172,310}`; in `C_169` it is
`{3,25,141}`; in primitive-D coordinates it is `{1,121,385}`.

## Interpretation

The quadratic fiber correction is not a free interpolation parameter.  It is
the Newton curvature of the fixed source-row triangle attached to the
half-bridge corner.  A producer can now be asked to realize this exact row
triangle plus the raw `K` trace, instead of being handed four separate
quadratic fiber sections.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_newton_triangle_rows=1/1
```
