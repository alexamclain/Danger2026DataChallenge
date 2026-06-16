# Subsqrt Moonshot Lane B Square-Axis Raw Antiderivative Trace

Date: 2026-06-12

## Result

The raw `C_25` kernel gives a tempting local picture, but not a degree-zero
escape.

There are two natural raw lifts of the diagonal anomaly

```text
A = (1 + D + D^2) * X^3 * Y.
```

The block lift has support `75 = 3 * 25`; its raw `D` boundary has support
`50`, and it is kernel-trivial.

The sparse-section lift puts value `25` on one kernel representative above
each of the three anomaly classes.  It still traces to the same quotient
anomaly, and its raw `D` boundary is only two raw points.  This is the best
local raw shadow of the signed-`D` antiderivative clue.

But both lifts have raw degree:

```text
B * degree(A) = 25 * 3 = 75.
```

Trace-zero kernel modes cannot change that degree.  Forcing raw degree zero
requires adding the same nonzero scalar to every raw source point.  Then both
the block lift and the sparse-section lift have full raw support
`12675/12675`, and their quotient traces are dense on all `507` classes.

## Producer Consequence

The sparse `C_25` section is useful as a diagnostic: it shows what a local raw
edge would look like.  It is not, by itself, a valid degree-zero repair.

A real producer must do more than choose a sparse kernel representative.  It
must either provide a new source-level mechanism that changes the degree
accounting before trace, or accept the dense scalar component and then explain
why selected-defect does not see the diagonal anomaly.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_raw_antiderivative_trace_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_raw_antiderivative_trace_gate.py
```
