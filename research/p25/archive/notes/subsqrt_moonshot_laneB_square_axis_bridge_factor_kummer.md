# Subsqrt Moonshot Lane B Square-Axis Bridge Factor Kummer

Date: 2026-06-12

## Result

The raw bridge factors have distinct local source costs.

In raw source logs `C_75 x C_169`:

```text
kernel trace = (57,0)
D segment    = (22,3)
bridge edge  = (38,113)
```

Their local multipliers and orders are:

```text
kernel trace: (125 mod151, 1 mod677),    order 25
D segment:    (55 mod151,  85 mod677),  order 12675
bridge edge:  (45 mod151, 667 mod677),  order 12675
```

Kummer costs:

```text
kernel trace: right C75 degree 25, invisible on the quotient C3 side
D segment:    right C75 degree 75 and C169 degree 169
bridge edge:  right C75 degree 75 and C169 degree 169
```

## Raw Monodromy

The raw `D` factor does not satisfy `D^3 = Y` before trace-down:

```text
D^3      = (66,9)
Y_raw    = (9,9)
D^3 - Y = (57,0) = kernel trace shift
```

So `D^3 = Y` becomes true only after the `25`-kernel trace has been collapsed.

## Consequence

A raw producer must account for three separate ingredients:

```text
25-point right-kernel trace
primitive D-segment motion
primitive bridge-edge motion
```

It cannot treat the quotient relation `D^3 = Y` as a raw equality, and it
cannot hide the kernel trace in a phase.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_factor_kummer_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_factor_kummer_gate.py
```

Standalone marker:

```text
square_axis_bridge_factor_kummer_rows=1/1
```
