# p25 Lane B Square-Axis Bridge Theta31 Sparse Combination Obstruction

Updated: 2026-06-12

## Result

Sparse combinations of the canonical square-axis `theta_{3,1}` edges do not
produce the primitive bridge.

The checked family is deliberately narrow but high-value:

```text
small theta directions = 163, 172, 335, 344
support sizes = 12, 6, 6, 12
globally minimal directions = 172, 335 = +/-D
translated small edges = 2028
translated minimal edges = 1014
```

Over the verifier field:

```text
single translated small-edge matches = 0
two translated small-edge scalar matches = 0
three translated minimal-edge scalar matches = 0
```

The dense sanity check is also bad for the theta-edge route.  The translated
`D` edge family has Fourier zeros exactly at:

```text
0, 169, 338
```

The bridge is compatible with those zero modes, so it lies in the translated
`D`-edge convolution span.  But the canonical inverse has support `507`, and
after adding the entire three-dimensional nullspace, each `q mod 3` row class
still has `169` distinct coefficient values.  Thus every exact translated
`D`-edge synthesis has at least `504` nonzero translated edges.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_theta31_sparse_combination_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_theta31_sparse_combination_obstruction_rows=1/1
```

## Continue / Kill

Kill the small translated-edge correction route for the canonical
`theta_{3,1}` packet.  Continue only if the theta object is modified, a new
mixed arithmetic factor is added, or the producer realizes the primitive bridge
directly rather than synthesizing it from a sparse sum of canonical theta
edges.
