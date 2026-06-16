# Subsqrt Moonshot Lane B Square-Axis Fiber Placement Law

Date: 2026-06-12

## Result

The six-word `C_169` fiber alphabet has an exact placement law.

Write:

```text
j = a + 13*b
h = right - a mod 3
```

Then the `b`-fiber is:

```text
C_13 half-arc row h
```

and if the `C_13` trace-shadow bit at `(right, a)` is `1`, add one boundary bit:

```text
fiber[9 - 3*h] = 1
```

Observed:

```text
placement_hits = 39 / 39
h_counts = [13, 13, 13]
zero_trace_unmodified_hits = 21 / 21
one_trace_boundary_hits = 18 / 18
boundary_positions_by_h = [9, 6, 3]
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_fiber_placement_law_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_fiber_placement_law_gate.py
```

Observed:

```text
square_axis_fiber_placement_law_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_fiber_placement_law_gate
```

## Consequence

The `C_169` target is now a deterministic `13`-adic boundary refinement:

```text
C_13 trace-shadow mask
plus
one boundary injection in each carrying trace slot
```

This is a much sharper producer target than the raw `507`-rectangle mask.  A
square-axis CM-Artin or modular-unit candidate should be tested for this
placement law before any larger certificate work:

```text
does it recover h = right - a mod 3?
does it use the correct C_13 half-arc row in every fiber?
does it inject the boundary bit at 9 - 3h precisely on carrying C_13 trace slots?
```

The explicit base-plus-residual decomposition is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_boundary_residual.md
```
