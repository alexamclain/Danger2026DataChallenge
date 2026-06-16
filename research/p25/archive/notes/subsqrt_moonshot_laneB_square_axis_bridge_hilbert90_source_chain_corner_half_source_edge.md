# Lane B: Bridge Hilbert-90 Source-Chain Corner Half Source Edge

Date: 2026-06-13

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_gate.py`

## Result

The selected four-block half-potential is now expressed in source coordinates
`C_3 x C_169`.

For mask `1`, the half-potential is:

```text
row 0:  -[c=0]   + [c=31]
row 2:  +[c=28]  - [c=144]
```

For mask `6`, it is:

```text
row 0:  +[c=0]   - [c=138]
row 1:  +[c=25]  - [c=141]
```

In both cases:

```text
q=0 is an endpoint of one row edge
the two primitive C_169 short steps are 31 and 53
the C_13 shadows of those short steps are 5 and 1
```

The shape `q=0` plus two primitive row edges with short steps `31` and `53` is
not always enough.  In two of the four active rows, the opposite half-boundary
direction has the same coarse source-edge profile.  The bridge-pair orientation
from the half-potential selector is what singles out the recorded direction.

## Interpretation

The producer target is now a very concrete source object:

```text
curved three-point corner
  -> recorded +/-122 half-boundary
  -> q=0 fixed repair plus two oriented primitive C_169 row edges
  -> signed S-layer bridge image
```

A candidate that only produces two primitive source-row edges is not enough; it
must also orient them as the selected bridge-pair half-potential.

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_corner_half_source_edge_rows=1/1
```
