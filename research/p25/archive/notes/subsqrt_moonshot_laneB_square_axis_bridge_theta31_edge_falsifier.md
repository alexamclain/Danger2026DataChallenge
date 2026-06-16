# p25 Lane B Square-Axis Bridge Theta31 Edge Falsifier

Updated: 2026-06-12

## Result

The closest p24-amortized producer shape, the square-axis ray-local
`theta_{3,1}` carry pullback, does not produce the primitive bridge by taking
natural finite differences along the bridge directions.

The canonical `D` edge is a genuine near miss:

```text
raw_support = 150
quotient_support = 6
block_constancy_hits = 507/507
kernel_modes = (0,)
raw_relation_mismatches = 0
pure_C_characters = 168
mixed_right_C_characters = 336
```

But it fails the bridge itself:

```text
theta31 D-edge support = 0, 43, 86, 129, 169, 338
bridge support         = 25, 138, 197, 310, 369, 482
support overlap        = 0
translate/sign matches = none
```

The `T` and `-T` edges are not small bridge candidates at all:

```text
T quotient support = 338
T raw support      = 8450
```

The `D^3` edge is the expected `Y`-style boundary:

```text
quotient support = 18
raw support      = 450
```

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_theta31_edge_falsifier_gate.py
```

Expected row:

```text
square_axis_bridge_theta31_edge_falsifier_rows=1/1
```

## Continue / Kill

Continue searching for a mixed correction to the p24-amortized
`theta_{3,1}` producer shape.  Kill the direct edge explanation: even the
best `D` edge has the right harness-adjacent invariants but lands on the wrong
six quotient classes.
