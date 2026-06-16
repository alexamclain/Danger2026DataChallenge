# Lane B: Bridge Hilbert-90 Source-Chain Corner K-Trace Minimality

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_gate.py`

## Result

The full 25-point `K` trace is not just the best tested lift.  It is forced by
trace-correctness plus K-invariance.

On raw lifts invariant under the order-25 kernel shift, normalized trace is an
isomorphism back to the `507` quotient blocks:

```text
K-invariant dimension: 507
trace rank:            507
trace kernel:          0
```

So each nonzero quotient corner point has exactly one K-invariant trace-correct
lift: the full constant 25-point `K` orbit.  Since the active corner has three
nonzero quotient points, the K-invariant raw corner support is forced to be:

```text
3 * 25 = 75
```

Proper K-subtraces can be trace-correct but fail the raw producer relation:

```text
trace order 1:  support 3,  K-boundary/D^3-Y defects 6
trace order 5:  support 15, K-boundary/D^3-Y defects 30
trace order 25: support 75, K-boundary/D^3-Y defects 0
```

The defect counts agree exactly with the previous K-invariance mechanism.

## Interpretation

This removes another escape hatch.  A producer cannot use a sparse section or a
proper `K^5` subtrace to lower the raw corner support while keeping the raw
contract.  The target is the full order-25 K trace on the fixed Newton triangle.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_k_trace_minimality_rows=1/1
```
