# p25 Lane B Square-Axis Bridge Theta31 Edge Direction Scan

Updated: 2026-06-12

## Result

No single finite-difference edge of the canonical square-axis `theta_{3,1}`
pullback is the primitive bridge.

All `506` nonzero quotient directions were scanned.  Only the two signed `D`
directions have six-point support:

```text
D = 172: support 0, 43, 86, 129, 169, 338
-D = 335: support 166, 335, 378, 421, 464, 504
```

Both are disjoint from the primitive bridge support:

```text
bridge support = 25, 138, 197, 310, 369, 482
```

The next-smallest directions have support `12`:

```text
163 = -2D
344 = +2D
```

No direction gives the bridge up to scalar, sign, or translation.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_theta31_edge_direction_scan_gate.py
```

Expected row:

```text
square_axis_bridge_theta31_edge_direction_scan_rows=1/1
```

## Continue / Kill

Continue with mixed corrections or modified theta packets.  Kill the remaining
single-edge explanation: the best theta edges are exactly the previously found
`±D` near misses, and neither lands on the primitive bridge.
