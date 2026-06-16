# Subsqrt Moonshot Lane B Square-Axis Bridge Trace Rectangle

Date: 2026-06-12

## Result

The positive raw bridge layer is not a `75`-element subgroup or subgroup coset.
It is a trace rectangle:

```text
positive = base + <507>_25 + {0, D, 2D}
base = 25
D    = 172
```

Here `<507>_25` is the `25`-element trace-kernel subgroup in `C_12675`.

In `D`-coordinates, this becomes:

```text
positive - base = <507>_25 + {0,1,2}
```

The stabilizer of the positive layer is exactly the kernel subgroup:

```text
{0, 507, 1014, ..., 12168}
```

The signed bridge has the same sign-preserving translation stabilizer and no
sign-reversing translation.

## Consequence

A producer should not explain the positive layer as one raw subgroup trace of
size `75`.  The shape is more specific:

```text
25-point kernel trace
times
length-three D segment.
```

So any raw finite-field identity must realize this trace rectangle, not merely
a size-`75` subgroup/coset support.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_trace_rectangle_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_trace_rectangle_gate.py
```
