# Subsqrt Moonshot Lane B Square-Axis Bridge Source-Line Lift

Date: 2026-06-12

## Result

The bridge has a precise source-line normal form.

In `C_3 x C_169` source-log coordinates, write

```text
D = (1,3)
T = (2,113)
```

Then the positive layer is the length-three `D` segment

```text
(1,25), (2,28), (0,31),
```

and the negative layer is exactly its `T` translate:

```text
(0,138), (1,141), (2,144).
```

This same negative layer is also the inversion of the positive layer.

## Projection

The bridge has a real `C_13` shadow:

```text
+ at (0,5), (1,12), (2,2)
- at (0,8), (1,11), (2,1)
rank over F_2    = 3
rank over F_2029 = 3
```

But the full `C_169` lift is not optional.  Among all `507` possible
length-three `D` segments in `C_3 x C_169`, requiring the `T` translate to be
the inversion of the segment picks exactly one:

```text
base = (1,25).
```

## Consequence

A producer may use the `C_13` shadow as a clue, but it must still explain the
specific `C_169` lift.  The target is now:

```text
the unique inversion-compatible D-segment lift joined by T = (2,113).
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_source_line_lift_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_source_line_lift_gate.py
```
