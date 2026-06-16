# p25 Lane B Square-Axis Bridge Theta31 Source-Shear Obstruction

Updated: 2026-06-13

## Result

The canonical square-axis `theta_{3,1}` near miss is not the primitive bridge
under the cheap source-coordinate mixed correction:

```text
right -> alpha * right + beta
C     -> unit * C + row_offset[right]
```

This includes product-affine source maps, row-affine shears
`row_offset[right] = shift + gamma * right`, and even arbitrary per-row
`C_169` offsets.

The support-`<=12` theta edge family is:

```text
directions = 163, 172, 335, 344
support sizes = 12, 6, 6, 12
```

The support-`12` edges cannot map to the six-point bridge under any injective
source shear.  For the support-`6` `+/-D` near misses, the obstruction appears
before offsets or signs:

```text
bridge row signed deltas = (107, 116, 116)
theta +D row signed deltas = (43, 127, 85)
theta -D row signed deltas = (42, 84, 126)
```

No `C_169` unit, for any affine row permutation, sends all three theta row-pair
differences to the bridge row-pair differences.  Therefore row offsets cannot
repair the packet.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_theta31_source_shear_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_theta31_source_shear_obstruction_rows=1/1
```

## Continue / Kill

Kill the source-row-shear repair route for the canonical `theta_{3,1}` packet.
Continue only if the theta packet itself is modified, a new arithmetic mixed
factor is added, or a separate producer realizes the primitive bridge directly.
