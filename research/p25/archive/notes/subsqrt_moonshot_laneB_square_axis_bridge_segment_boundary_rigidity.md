# Subsqrt Moonshot Lane B Square-Axis Bridge Segment Boundary Rigidity

Date: 2026-06-12

## Result

The bridge positive layer has a forced sparse boundary direction.

After quotienting the `25`-point kernel trace, the visible positive bridge is a
three-point `D` segment in `C_507`:

```text
base + {0,D,2D}
D = 172
```

Among all `506` nonzero first-difference directions:

```text
support 2: only  D, -D
support 4: only  2D, -2D
support 6: all other directions
```

Before quotienting, the positive raw trace rectangle is:

```text
base + <507>_25 + {0,D,2D} in C_12675
```

The boundary profile is:

```text
support 0:   24 pure nonzero kernel shifts
support 50:  only +/-D plus a kernel shift
support 100: only +/-2D plus a kernel shift
support 150: all other directions
```

## Consequence

A divisor-style producer that tries to create the positive bridge layer by a
sparse first-difference boundary has no freedom in the direction.  It must use
the `D` direction, up to the trace kernel in the raw lift.

This rules out modular-unit or finite-field candidates whose small boundary is
in an unrelated local direction.  The only zero-boundary escape is pure kernel
trace invariance, which does not create the visible three-point segment.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_segment_boundary_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_segment_boundary_rigidity_gate.py
```
