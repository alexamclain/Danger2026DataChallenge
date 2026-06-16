# Lane B: Bridge Hilbert-90 Source-Chain Corner K-Trace Invariance

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_invariance_gate.py`

## Result

The raw `K` trace is exactly the mechanism that makes the corner compatible
with the raw `D^3 = Y` relation.

The identity is:

```text
3*S_STEP - Y_STEP = 507
```

and `507` is the raw kernel shift.  In the primitive raw `D` coordinate, that
kernel shift is:

```text
K = D^4056
```

Therefore raw `D^3 = Y` on a corner lift is equivalent to invariance under the
25-point `K` orbit.

Across all four active half-bridge corners:

```text
block K trace:          0 K-boundary defects, 0 raw D^3/Y defects
sparse section:         6 K-boundary defects, 6 raw D^3/Y defects
block plus hidden mode: 75 K-boundary defects, 75 raw D^3/Y defects
hidden mode only:       75 K-boundary defects, 75 raw D^3/Y defects
```

The sparse section is trace-correct, but it breaks exactly two kernel-boundary
edges at each of the three corner points.  Nontrivial hidden modes break the
full 25-point kernel cycle at each corner point.

## Interpretation

This replaces a black-box raw-relation requirement with a concrete algebraic
mechanism: the producer must realize the `K`-invariant row triangle, not merely
the quotient triangle or a sparse raw section.  The remaining arithmetic debt
is now sharper: produce the fixed Newton triangle while also producing the
order-25 kernel trace that makes `D^3` descend to `Y`.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_k_trace_invariance_rows=1/1
```
