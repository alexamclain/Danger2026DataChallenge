# Lane B: Bridge Hilbert-90 Source-Chain Corner Raw K-Trace

Date: 2026-06-12

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_gate.py`

## Result

The active half-bridge corner chains require the raw `K`-trace block lift.

For each of the four active corner chains, the tested raw lifts behave as:

```text
block K-trace:
  support 75, trace-correct, kernel mode {0}, raw D^3=Y compatible

sparse section:
  support 3, trace-correct, all 25 kernel modes visible, raw D^3=Y fails

block plus hidden kernel mode:
  support 75, trace-correct, kernel modes {0,1}, raw D^3=Y fails

hidden mode only:
  support 75, raw degree 0, trace-incorrect, raw D^3=Y fails
```

Across the sixteen rows:

```text
trace-correct rows = 12
trace-correct + raw D^3=Y rows = 4
trace-correct + kernel-trivial rows = 4
```

Those four rows are exactly the block `K`-trace lifts.

## Interpretation

The current producer target is now:

```text
half-bridge corner
  + C_3 row balance
  + active C_169 lift
  + raw K-trace block lift
```

The quotient corner or a sparse raw section is not a producer certificate.  The
raw chain still has degree `+/-75` before the first boundary, so the remaining
arithmetic debt is not a finite-support ambiguity anymore: it is realizing the
`K` trace with the already-recorded Kummer cost.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_raw_k_trace_rows=1/1
```
